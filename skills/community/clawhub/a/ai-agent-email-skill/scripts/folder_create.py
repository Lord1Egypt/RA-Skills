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
	name = data.get("name")
	if not isinstance(name, str) or not name.strip():
		raise SkillError("VALIDATION_ERROR", "data.name is required")
	
	name = validate_folder_name(name)

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	client = connect_imap(account_cfg)
	try:
		status, detail = client.create(name)
		if status != "OK":
			raise SkillError(
				"MAILBOX_ERROR",
				"Failed to create mailbox",
				{"status": status, "detail": str(detail), "name": name},
			)
		return {"account": account_name, "name": name, "created": True}
	finally:
		close_imap_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))



