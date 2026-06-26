from typing import Any
from email import policy
from email.parser import BytesParser

from scripts.common import (
	SkillError,
	close_imap_safely,
	connect_imap,
	decode_mime_header,
	extract_fetch_tags,
	load_config,
	resolve_account,
	select_mailbox,
	validate_imap_query,
	with_runtime,
)


def _uid_sort_key(uid: str) -> tuple[int, int | str]:
	return (0, int(uid)) if uid.isdigit() else (1, uid)


def _extract_summary(client, uid: str) -> dict[str, object]:
	status, fetched = client.uid("FETCH", uid, "(RFC822.HEADER FLAGS X-GM-LABELS)")
	if status != "OK" or not fetched:
		return {
			"uid": uid,
			"subject": "",
			"from": "",
			"date": "",
			"flags": [],
			"systemTags": [],
			"keywords": [],
			"gmailLabels": [],
			"tags": [],
		}

	raw_header = None
	for row in fetched:
		if isinstance(row, tuple) and len(row) >= 2 and isinstance(row[1], (bytes, bytearray)):
			raw_header = bytes(row[1])
			break

	if raw_header is None:
		return {
			"uid": uid,
			"subject": "",
			"from": "",
			"date": "",
			"flags": [],
			"systemTags": [],
			"keywords": [],
			"gmailLabels": [],
			"tags": [],
		}

	message = BytesParser(policy=policy.default).parsebytes(raw_header)
	return {
		"uid": uid,
		"subject": decode_mime_header(message.get("Subject")),
		"from": decode_mime_header(message.get("From")),
		"date": message.get("Date", ""),
		**extract_fetch_tags(fetched),
	}


def handler(request: dict[str, Any]):
	data = request.get("data", {})
	folder = data.get("folder", "INBOX")
	query = data.get("query", "UNSEEN")
	max_results = data.get("maxResults", 10)

	if not isinstance(folder, str) or not folder.strip():
		raise SkillError("VALIDATION_ERROR", "data.folder must be string")
	if not isinstance(query, str):
		raise SkillError("VALIDATION_ERROR", "data.query must be string when provided")
	if not isinstance(max_results, int) or max_results < 1 or max_results > 10000:
		raise SkillError("VALIDATION_ERROR", "data.maxResults must be an integer between 1 and 10000")

	folder = folder.strip()
	query = validate_imap_query(query)

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	client = connect_imap(account_cfg)
	try:
		select_mailbox(client, folder)
		# Try UTF-8 search first, then fallback for servers that don't support CHARSET.
		status, search_result = client.uid("SEARCH", "CHARSET", "UTF-8", query)
		if status != "OK":
			status, search_result = client.uid("SEARCH", query)
		if status != "OK":
			raise SkillError(
				"MAIL_OPERATION_ERROR",
				"Failed to search mail",
				{"status": status, "query": query, "folder": folder},
			)

		# Parse the search result - it returns bytes in a list with UIDs separated by spaces
		uids = []
		if search_result and isinstance(search_result[0], bytes):
			uid_bytes = search_result[0].decode("utf-8", errors="replace").strip()
			if uid_bytes:
				uids = uid_bytes.split()

		# Normalize ordering to avoid relying on server-side UID order.
		uids = sorted(uids, key=_uid_sort_key)

		total_count = len(uids)

		# Keep the latest UIDs when result set exceeds maxResults.
		if total_count > max_results:
			uids = uids[-max_results:]

		summary = [_extract_summary(client, uid) for uid in uids]

		return {
			"account": account_name,
			"folder": folder,
			"query": query,
			"uids": uids,
			"count": len(uids),
			"totalCount": total_count,
			"hasMore": total_count > max_results,
			"summary": summary,
		}
	finally:
		close_imap_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
