from typing import Any
import base64

from email import policy
from email.parser import BytesParser

from scripts.common import (
	SkillError,
	close_imap_safely,
	connect_imap,
	decode_mime_header,
	extract_text_body,
	extract_html_body,
	extract_fetch_tags,
	load_config,
	resolve_account,
	select_mailbox,
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
							"Failed to decode attachment",
							{"filename": filename},
						)
					attachments.append({
						"filename": filename,
						"contentBase64": base64.b64encode(content).decode("ascii"),
						"size": len(content),
					})
	return attachments


def handler(request: dict[str, Any]):
	data = request.get("data", {})
	uid = data.get("uid")
	folder = data.get("folder", "INBOX")

	if not isinstance(uid, str) or not uid.strip():
		raise SkillError("VALIDATION_ERROR", "data.uid is required")
	if not isinstance(folder, str) or not folder.strip():
		raise SkillError("VALIDATION_ERROR", "data.folder must be string")

	uid = uid.strip()
	folder = folder.strip()

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	client = connect_imap(account_cfg)
	try:
		select_mailbox(client, folder)
		status, fetched = client.uid("FETCH", uid, "(BODY.PEEK[] FLAGS X-GM-LABELS)")
		if status != "OK" or not fetched:
			raise SkillError(
				"MAIL_OPERATION_ERROR",
				"Failed to fetch mail",
				{"status": status, "uid": uid, "folder": folder},
			)

		raw_msg = None
		for row in fetched:
			if isinstance(row, tuple) and len(row) >= 2 and isinstance(row[1], (bytes, bytearray)):
				raw_msg = bytes(row[1])
				break
		if raw_msg is None:
			raise SkillError("MAIL_OPERATION_ERROR", "No RFC822 content found", {"uid": uid})

		message = BytesParser(policy=policy.default).parsebytes(raw_msg)
		tag_info = extract_fetch_tags(fetched)

		# Explicitly mark the mail as read after content is parsed.
		mark_status, mark_detail = client.uid("STORE", uid, "+FLAGS", "(\\Seen)")
		if mark_status != "OK":
			raise SkillError(
				"MAIL_OPERATION_ERROR",
				"Failed to mark mail as read",
				{"status": mark_status, "detail": str(mark_detail), "uid": uid, "folder": folder},
			)
		if "\\Seen" not in tag_info["flags"]:
			tag_info["flags"] = [*tag_info["flags"], "\\Seen"]
		if "\\Seen" not in tag_info["systemTags"]:
			tag_info["systemTags"] = [*tag_info["systemTags"], "\\Seen"]
		if "\\Seen" not in tag_info["tags"]:
			tag_info["tags"] = [*tag_info["tags"], "\\Seen"]
	finally:
		close_imap_safely(client)

	subject = decode_mime_header(message.get("Subject"))
	from_addr = decode_mime_header(message.get("From"))
	to_addrs = decode_mime_header(message.get("To"))
	cc_addrs = decode_mime_header(message.get("Cc"))
	date_str = message.get("Date", "")
	message_id = message.get("Message-ID", "")

	text_body = extract_text_body(message)
	html_body = extract_html_body(message)
	attachments = _extract_attachments(message)

	return {
		"account": account_name,
		"uid": uid,
		"folder": folder,
		"subject": subject,
		"from": from_addr,
		"to": to_addrs,
		"cc": cc_addrs,
		"date": date_str,
		"messageId": message_id,
		"bodyText": text_body if text_body else None,
		"bodyHtml": html_body if html_body else None,
		"attachments": attachments,
		"attachmentCount": len(attachments),
		**tag_info,
	}


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
