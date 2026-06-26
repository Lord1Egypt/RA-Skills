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
	source_folder = data.get("sourceFolder", "INBOX")
	target_folder = data.get("targetFolder")
	uids = normalize_uids(data.get("uids"))

	if not isinstance(source_folder, str) or not source_folder.strip():
		raise SkillError("VALIDATION_ERROR", "data.sourceFolder must be string")
	if not isinstance(target_folder, str) or not target_folder.strip():
		raise SkillError("VALIDATION_ERROR", "data.targetFolder is required")

	source_folder = source_folder.strip()
	target_folder = target_folder.strip()

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	client = connect_imap(account_cfg)
	try:
		select_mailbox(client, source_folder)
		capabilities = get_imap_capabilities(client)

		if "MOVE" in capabilities:
			status, detail = client.uid("MOVE", uids, target_folder)
			if status != "OK":
				raise SkillError(
					"MAIL_OPERATION_ERROR",
					"Failed to move mail with IMAP MOVE",
					{
						"status": status,
						"detail": str(detail),
						"uids": uids,
						"sourceFolder": source_folder,
						"targetFolder": target_folder,
					},
				)
		else:
			if "UIDPLUS" not in capabilities:
				raise SkillError(
					"MAIL_OPERATION_ERROR",
					"Safe move requires IMAP MOVE or UIDPLUS support",
					{
						"uids": uids.split(","),
						"sourceFolder": source_folder,
						"targetFolder": target_folder,
						"capabilities": sorted(capabilities),
					},
				)

			status, detail = client.uid("COPY", uids, target_folder)
			if status != "OK":
				raise SkillError(
					"MAIL_OPERATION_ERROR",
					"Failed to copy mail to target folder",
					{
						"status": status,
						"detail": str(detail),
						"uids": uids,
						"sourceFolder": source_folder,
						"targetFolder": target_folder,
					},
				)

			status, detail = client.uid("STORE", uids, "+FLAGS", "(\\Deleted)")
			if status != "OK":
				raise SkillError(
					"MAIL_OPERATION_ERROR",
					"Failed to mark mail deleted in source folder",
					{"status": status, "detail": str(detail), "uids": uids, "folder": source_folder},
				)

			expunge_uids_safely(client, uids, folder=source_folder)

		return {
			"account": account_name,
			"uids": uids.split(","),
			"sourceFolder": source_folder,
			"targetFolder": target_folder,
			"moved": True,
		}
	finally:
		close_imap_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
