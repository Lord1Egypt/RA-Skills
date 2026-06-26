from typing import Any
import html
from email import policy
from email.parser import BytesParser

from scripts.common import (
	apply_signatures,
	decode_mime_header,
	ensure_body_alternatives,
	extract_text_body,
	extract_html_body,
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
	parse_recipients,
	resolve_account,
	select_mailbox,
	text_to_html,
	with_runtime,
)


def _extract_attachments(message) -> list:
	attachments = []
	if message.is_multipart():
		for part in message.walk():
			if part.get_content_disposition() == "attachment":
				filename = part.get_filename()
				if filename:
					content = part.get_payload(decode=True)
					if content is None:
						raise SkillError(
							"MAIL_OPERATION_ERROR",
							"Failed to decode original attachment",
							{"filename": filename},
						)
					maintype, subtype = part.get_content_type().split("/", 1)
					attachments.append({
						"filename": filename,
						"content": content,
						"maintype": maintype,
						"subtype": subtype,
					})
	return attachments


def handler(request: dict[str, Any]):
	data = request.get("data", {})
	uid = data.get("uid")
	folder = data.get("folder", "INBOX")
	body_text = data.get("bodyText")
	body_html = data.get("bodyHtml")
	raw_attachments = data.get("attachments")

	if not isinstance(uid, str) or not uid.strip():
		raise SkillError("VALIDATION_ERROR", "data.uid is required")
	if not isinstance(folder, str) or not folder.strip():
		raise SkillError("VALIDATION_ERROR", "data.folder must be string")
	if body_text is not None and not isinstance(body_text, str):
		raise SkillError("VALIDATION_ERROR", "data.bodyText must be string when provided")
	if body_html is not None and not isinstance(body_html, str):
		raise SkillError("VALIDATION_ERROR", "data.bodyHtml must be string when provided")
	body_text, body_html = ensure_body_alternatives(body_text, body_html)

	to_list, cc_list, bcc_list = parse_recipients(data)
	if not to_list:
		raise SkillError("VALIDATION_ERROR", "data.to is required")

	additional_attachments = parse_base64_attachments(raw_attachments)

	uid = uid.strip()
	folder = folder.strip()

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	envelope_sender, header_sender = get_sender_address(account_cfg)
	signature_text, signature_html = get_smtp_signatures(account_cfg)

	client = connect_imap(account_cfg)
	try:
		select_mailbox(client, folder)
		status, fetched = client.uid("FETCH", uid, "(BODY.PEEK[])")
		if status != "OK" or not fetched:
			raise SkillError(
				"MAIL_OPERATION_ERROR",
				"Failed to fetch source mail for forwarding",
				{"status": status, "uid": uid, "folder": folder},
			)

		raw_msg = None
		for row in fetched:
			if isinstance(row, tuple) and len(row) >= 2 and isinstance(row[1], (bytes, bytearray)):
				raw_msg = bytes(row[1])
				break
		if raw_msg is None:
			raise SkillError("MAIL_OPERATION_ERROR", "No RFC822 content found", {"uid": uid})

		original = BytesParser(policy=policy.default).parsebytes(raw_msg)
	finally:
		close_imap_safely(client)

	original_subject = decode_mime_header(original.get("Subject"))
	original_from = decode_mime_header(original.get("From"))
	original_date = original.get("Date", "")

	if original_subject.lower().startswith("fwd:"):
		fwd_subject = original_subject
	else:
		fwd_subject = f"Fwd: {original_subject}" if original_subject else "Fwd:"

	original_text = extract_text_body(original)
	original_html = extract_html_body(original)
	if not original_text and original_html:
		original_text = html_to_text(original_html)
	original_attachments = _extract_attachments(original)

	# Apply signatures to user's body BEFORE adding forwarded content
	user_body_text, user_body_html = apply_signatures(
		body_text,
		body_html,
		signature_text,
		signature_html,
	)

	forwarded_header = (
		f"---------- Forwarded message -----\n"
		f"From: {original_from}\n"
		f"Date: {original_date}\n"
		f"Subject: {original_subject}\n\n"
	)

	if user_body_text:
		fwd_body_text = f"{user_body_text}\n\n{forwarded_header}{original_text}"
	else:
		fwd_body_text = f"{forwarded_header}{original_text}"

	if user_body_html:
		forwarded_header_html = (
			f"<br><br><hr>---------- Forwarded message -----<br>"
			f"From: {html.escape(original_from)}<br>"
			f"Date: {html.escape(original_date)}<br>"
			f"Subject: {html.escape(original_subject)}<br><br>"
		)
		original_html_content = original_html if original_html else text_to_html(original_text)
		fwd_body_html = f"{user_body_html}{forwarded_header_html}{original_html_content}"
	else:
		if not original_html:
			fwd_body_html = None
		else:
			prefix_html = f"{text_to_html(user_body_text)}<br><br>" if user_body_text else ""
			fwd_body_html = (
				f"{prefix_html}<hr>---------- Forwarded message -----<br>"
				f"From: {html.escape(original_from)}<br>"
				f"Date: {html.escape(original_date)}<br>"
				f"Subject: {html.escape(original_subject)}<br><br>"
				f"{original_html}"
			)

	fwd_body_text, fwd_body_html = ensure_body_alternatives(fwd_body_text, fwd_body_html)

	message = build_message(header_sender, to_list, fwd_subject, fwd_body_text, fwd_body_html, cc_list, bcc_list)

	normalized_additional_attachments = []
	for attachment in additional_attachments:
		maintype, subtype = guess_attachment_type(attachment["filename"])
		normalized_additional_attachments.append(
			{
				"filename": attachment["filename"],
				"content": attachment["content"],
				"maintype": maintype,
				"subtype": subtype,
			}
		)

	all_attachments = original_attachments + normalized_additional_attachments
	for attachment in all_attachments:
		message.add_attachment(
			attachment["content"],
			maintype=attachment["maintype"],
			subtype=attachment["subtype"],
			filename=attachment["filename"],
		)

	all_recipients = to_list + cc_list + bcc_list

	smtp_client = connect_smtp(account_cfg)
	try:
		smtp_client.send_message(message, from_addr=envelope_sender, to_addrs=all_recipients)
	finally:
		close_smtp_safely(smtp_client)

	return {
		"account": account_name,
		"forwarded": True,
		"uid": uid,
		"sourceFolder": folder,
		"to": to_list,
		"cc": cc_list,
		"bccCount": len(bcc_list),
		"subject": fwd_subject,
		"originalAttachmentCount": len(original_attachments),
		"additionalAttachmentCount": len(additional_attachments),
	}


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
