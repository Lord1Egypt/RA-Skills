from typing import Any
from scripts.common import (
	SkillError,
	close_imap_safely,
	connect_imap,
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
		status, detail = client.uid("COPY", uids, target_folder)
		if status != "OK":
			raise SkillError(
				"MAIL_OPERATION_ERROR",
				"Failed to copy mail",
				{
					"status": status,
					"detail": str(detail),
					"uids": uids,
					"sourceFolder": source_folder,
					"targetFolder": target_folder,
				},
			)
		return {
			"account": account_name,
			"uids": uids.split(","),
			"sourceFolder": source_folder,
			"targetFolder": target_folder,
			"copied": True,
		}
	finally:
		close_imap_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))



