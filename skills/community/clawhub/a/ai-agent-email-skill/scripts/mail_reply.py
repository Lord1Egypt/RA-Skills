from typing import Any
from email.utils import getaddresses

from scripts.common import (
	apply_signatures,
	decode_mime_header,
	ensure_body_alternatives,
	extract_text_body,
	SkillError,
	build_message,
	close_imap_safely,
	close_smtp_safely,
	connect_imap,
	connect_smtp,
	fetch_original_message,
	get_sender_address,
	get_smtp_signatures,
	guess_attachment_type,
	html_to_text,
	load_config,
	parse_base64_attachments,
	resolve_account,
	select_mailbox,
	text_to_html,
	with_runtime,
)


def _dedupe_addresses(addresses: list[str], excluded: set[str] | None = None) -> list[str]:
	seen = set(excluded or set())
	result: list[str] = []
	for address in addresses:
		normalized = address.strip().lower()
		if not normalized or normalized in seen:
			continue
		seen.add(normalized)
		result.append(address.strip())
	return result


def handler(request: dict[str, Any]):
	data = request.get("data", {})
	uid = data.get("uid")
	folder = data.get("folder", "INBOX")
	body_text = data.get("bodyText")
	body_html = data.get("bodyHtml")
	raw_attachments = data.get("attachments")
	reply_all = data.get("replyAll", False)
	priority = data.get("priority", "normal")
	read_receipt = data.get("readReceipt", False)
	requested_in_reply_to = data.get("inReplyTo")
	requested_references = data.get("references")

	if not isinstance(uid, str) or not uid.strip():
		raise SkillError("VALIDATION_ERROR", "data.uid is required")
	if not isinstance(folder, str) or not folder.strip():
		raise SkillError("VALIDATION_ERROR", "data.folder must be string")
	if body_text is not None and not isinstance(body_text, str):
		raise SkillError("VALIDATION_ERROR", "data.bodyText must be string when provided")
	if body_html is not None and not isinstance(body_html, str):
		raise SkillError("VALIDATION_ERROR", "data.bodyHtml must be string when provided")
	if not isinstance(reply_all, bool):
		raise SkillError("VALIDATION_ERROR", "data.replyAll must be boolean")
	if not isinstance(priority, str):
		raise SkillError("VALIDATION_ERROR", "data.priority must be string when provided")
	if not isinstance(read_receipt, bool):
		raise SkillError("VALIDATION_ERROR", "data.readReceipt must be boolean when provided")
	if requested_in_reply_to is not None and not isinstance(requested_in_reply_to, str):
		raise SkillError("VALIDATION_ERROR", "data.inReplyTo must be string when provided")
	if requested_references is not None and not isinstance(requested_references, str):
		raise SkillError("VALIDATION_ERROR", "data.references must be string when provided")

	priority = priority.strip().lower()
	if priority not in {"high", "normal", "low"}:
		raise SkillError("VALIDATION_ERROR", "data.priority must be one of: high, normal, low")
	requested_in_reply_to = (
		requested_in_reply_to.strip()
		if isinstance(requested_in_reply_to, str) and requested_in_reply_to.strip()
		else None
	)
	requested_references = (
		requested_references.strip()
		if isinstance(requested_references, str) and requested_references.strip()
		else None
	)
	body_text, body_html = ensure_body_alternatives(body_text, body_html)
	attachments = parse_base64_attachments(raw_attachments)

	uid = uid.strip()
	folder = folder.strip()

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	envelope_sender, header_sender = get_sender_address(account_cfg)
	signature_text, signature_html = get_smtp_signatures(account_cfg)

	client = connect_imap(account_cfg)
	try:
		select_mailbox(client, folder)
		original = fetch_original_message(client, uid, folder)
	finally:
		close_imap_safely(client)

	original_subject = decode_mime_header(original.get("Subject"))
	if original_subject.lower().startswith("re:"):
		reply_subject = original_subject
	else:
		reply_subject = f"Re: {original_subject}" if original_subject else "Re:"

	reply_to = original.get("Reply-To") or original.get("From")
	reply_candidates = [addr for _, addr in getaddresses([reply_to or ""]) if addr]
	to_addrs = _dedupe_addresses(reply_candidates)
	if not to_addrs:
		raise SkillError("MAIL_OPERATION_ERROR", "Unable to resolve reply recipient from original message")

	cc_addrs: list[str] = []
	if reply_all:
		cc_source = [original.get("To", ""), original.get("Cc", "")]
		cc_candidates = [addr for _, addr in getaddresses(cc_source) if addr]
		excluded = {envelope_sender.lower(), *(addr.lower() for addr in to_addrs)}
		cc_addrs = _dedupe_addresses(cc_candidates, excluded=excluded)

	original_text = extract_text_body(original)
	original_html = original.get_body(preferencelist=("html",))
	original_html_body = original_html.get_content().strip() if original_html else None
	if not original_text and original_html_body:
		original_text = html_to_text(original_html_body)

	body_text, body_html = apply_signatures(body_text, body_html, signature_text, signature_html)
	body_text, body_html = ensure_body_alternatives(body_text, body_html)

	quoted_text = ""
	if original_text:
		quoted_lines = [f"> {line}" if line else ">" for line in original_text.splitlines()]
		quoted_text = "\n\n----- Original Message -----\n" + "\n".join(quoted_lines)

	quoted_html = ""
	quoted_html_body = original_html_body if original_html_body else text_to_html(original_text) if original_text else ""
	if quoted_html_body:
		quoted_html = (
			"<br><br><hr><div>----- Original Message -----</div><blockquote>"
			f"{quoted_html_body}</blockquote>"
		)

	final_body_text = (body_text or "") + quoted_text
	final_body_html = (body_html or text_to_html(body_text or "")) + quoted_html if (body_html or quoted_html) else None
	in_reply_to = requested_in_reply_to or original.get("Message-ID")
	references = requested_references or original.get("References")
	if references and in_reply_to and in_reply_to not in references:
		references = f"{references} {in_reply_to}"
	elif in_reply_to and not references:
		references = in_reply_to

	message = build_message(
		sender=header_sender,
		to_list=to_addrs,
		subject=reply_subject,
		body_text=final_body_text,
		body_html=final_body_html,
		cc_list=cc_addrs,
		in_reply_to=in_reply_to,
		references=references,
	)

	priority_headers = {
		"high": ("1", "urgent", "high"),
		"normal": ("3", "normal", "normal"),
		"low": ("5", "non-urgent", "low"),
	}
	x_priority, priority_value, importance = priority_headers[priority]
	message["X-Priority"] = x_priority
	message["Priority"] = priority_value
	message["Importance"] = importance

	if read_receipt:
		message["Disposition-Notification-To"] = header_sender
		message["Return-Receipt-To"] = header_sender

	for attachment in attachments:
		maintype, subtype = guess_attachment_type(attachment["filename"])
		message.add_attachment(
			attachment["content"],
			maintype=maintype,
			subtype=subtype,
			filename=attachment["filename"],
		)

	smtp = connect_smtp(account_cfg)
	try:
		smtp.send_message(message, from_addr=envelope_sender, to_addrs=to_addrs + cc_addrs)
		return {
			"account": account_name,
			"uid": uid,
			"folder": folder,
			"sent": True,
			"to": to_addrs,
			"cc": cc_addrs,
			"attachmentCount": len(attachments),
			"priority": priority,
			"readReceipt": read_receipt,
			"inReplyTo": in_reply_to,
			"references": references,
			"subject": reply_subject,
		}
	finally:
		close_smtp_safely(smtp)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
