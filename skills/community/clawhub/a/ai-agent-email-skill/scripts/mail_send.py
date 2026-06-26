from typing import Any
from scripts.common import (
	apply_signatures,
	ensure_body_alternatives,
	SkillError,
	build_message,
	close_smtp_safely,
	connect_smtp,
	get_sender_address,
	get_smtp_signatures,
	guess_attachment_type,
	load_config,
	parse_base64_attachments,
	parse_recipients,
	resolve_account,
	with_runtime,
)


def handler(request: dict[str, Any]):
	data = request.get("data", {})
	subject = data.get("subject")
	body_text = data.get("bodyText")
	body_html = data.get("bodyHtml")
	raw_attachments = data.get("attachments")
	priority = data.get("priority", "normal")
	read_receipt = data.get("readReceipt", False)
	in_reply_to = data.get("inReplyTo")
	references = data.get("references")

	if not isinstance(subject, str) or not subject.strip():
		raise SkillError("VALIDATION_ERROR", "data.subject is required")
	subject = subject.strip()

	if body_text is not None and not isinstance(body_text, str):
		raise SkillError("VALIDATION_ERROR", "data.bodyText must be string when provided")
	if body_html is not None and not isinstance(body_html, str):
		raise SkillError("VALIDATION_ERROR", "data.bodyHtml must be string when provided")
	if not isinstance(priority, str):
		raise SkillError("VALIDATION_ERROR", "data.priority must be string when provided")
	if not isinstance(read_receipt, bool):
		raise SkillError("VALIDATION_ERROR", "data.readReceipt must be boolean when provided")
	if in_reply_to is not None and not isinstance(in_reply_to, str):
		raise SkillError("VALIDATION_ERROR", "data.inReplyTo must be string when provided")
	if references is not None and not isinstance(references, str):
		raise SkillError("VALIDATION_ERROR", "data.references must be string when provided")

	priority = priority.strip().lower()
	if priority not in {"high", "normal", "low"}:
		raise SkillError("VALIDATION_ERROR", "data.priority must be one of: high, normal, low")
	in_reply_to = in_reply_to.strip() if isinstance(in_reply_to, str) and in_reply_to.strip() else None
	references = references.strip() if isinstance(references, str) and references.strip() else None
	body_text, body_html = ensure_body_alternatives(body_text, body_html)

	to_list, cc_list, bcc_list = parse_recipients(data)
	attachments = parse_base64_attachments(raw_attachments)

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	envelope_sender, header_sender = get_sender_address(account_cfg, data.get("from"))
	signature_text, signature_html = get_smtp_signatures(account_cfg)
	body_text, body_html = apply_signatures(body_text, body_html, signature_text, signature_html)
	body_text, body_html = ensure_body_alternatives(body_text, body_html)

	message = build_message(
		header_sender,
		to_list,
		subject,
		body_text,
		body_html,
		cc_list,
		bcc_list,
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
	all_recipients = to_list + cc_list + bcc_list

	client = connect_smtp(account_cfg)
	try:
		client.send_message(message, from_addr=envelope_sender, to_addrs=all_recipients)
		return {
			"account": account_name,
			"sent": True,
			"to": to_list,
			"cc": cc_list,
			"bccCount": len(bcc_list),
			"attachmentCount": len(attachments),
			"priority": priority,
			"readReceipt": read_receipt,
			"inReplyTo": in_reply_to,
			"references": references,
			"subject": subject,
		}
	finally:
		close_smtp_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
