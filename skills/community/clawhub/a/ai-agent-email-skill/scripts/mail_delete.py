from typing import Any
from scripts.common import (
	SkillError,
	close_imap_safely,
	connect_imap,
	expunge_uids_safely,
	get_imap_capabilities,
	load_config,
	normalize_uids,
	resolve_account,
	select_mailbox,
	with_runtime,
)


def handler(request: dict[str, Any]):
	data = request.get("data", {})
	folder = data.get("folder", "INBOX")
	expunge = data.get("expunge", False)
	uids = normalize_uids(data.get("uids"))

	if not isinstance(folder, str) or not folder.strip():
		raise SkillError("VALIDATION_ERROR", "data.folder must be string")
	if not isinstance(expunge, bool):
		raise SkillError("VALIDATION_ERROR", "data.expunge must be boolean")

	folder = folder.strip()

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	client = connect_imap(account_cfg)
	try:
		select_mailbox(client, folder)
		if expunge and "UIDPLUS" not in get_imap_capabilities(client):
			raise SkillError(
				"MAIL_OPERATION_ERROR",
				"Safe expunge is not supported by this IMAP server",
				{"folder": folder, "uids": uids.split(",")},
			)

		status, detail = client.uid("STORE", uids, "+FLAGS", "(\\Deleted)")
		if status != "OK":
			raise SkillError(
				"MAIL_OPERATION_ERROR",
				"Failed to mark mail deleted",
				{"status": status, "detail": str(detail), "uids": uids, "folder": folder},
			)

		expunged = False
		if expunge:
			expunge_uids_safely(client, uids, folder=folder)
			expunged = True

		return {
			"account": account_name,
			"uids": uids.split(","),
			"folder": folder,
			"deleted": True,
			"expunged": expunged,
		}
	finally:
		close_imap_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
