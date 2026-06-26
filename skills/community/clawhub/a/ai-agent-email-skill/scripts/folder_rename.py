from typing import Any
from scripts.common import (
	SkillError,
	close_imap_safely,
	connect_imap,
	load_config,
	resolve_account,
	validate_folder_name,
	with_runtime,
)


def handler(request: dict[str, Any]):
	data = request.get("data", {})
	old_name = data.get("oldName")
	new_name = data.get("newName")

	if not isinstance(old_name, str) or not old_name.strip():
		raise SkillError("VALIDATION_ERROR", "data.oldName is required")
	if not isinstance(new_name, str) or not new_name.strip():
		raise SkillError("VALIDATION_ERROR", "data.newName is required")

	old_name = validate_folder_name(old_name)
	new_name = validate_folder_name(new_name)

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	client = connect_imap(account_cfg)
	try:
		status, detail = client.rename(old_name, new_name)
		if status != "OK":
			raise SkillError(
				"MAILBOX_ERROR",
				"Failed to rename mailbox",
				{
					"status": status,
					"detail": str(detail),
					"oldName": old_name,
					"newName": new_name,
				},
			)
		return {
			"account": account_name,
			"oldName": old_name,
			"newName": new_name,
			"renamed": True,
		}
	finally:
		close_imap_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))



