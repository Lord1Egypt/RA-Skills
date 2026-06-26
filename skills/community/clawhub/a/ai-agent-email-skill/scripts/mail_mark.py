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
	mark_type = data.get("markType")
	uids = normalize_uids(data.get("uids"))
	folder = data.get("folder", "INBOX")

	if not isinstance(mark_type, str) or not mark_type.strip():
		raise SkillError("VALIDATION_ERROR", "data.markType is required")
	if not isinstance(folder, str) or not folder.strip():
		raise SkillError("VALIDATION_ERROR", "data.folder must be string")

	mark_type = mark_type.strip().lower()
	folder = folder.strip()

	# Map markType to IMAP flags
	mark_map = {
		"read": ("\\Seen", True),
		"unread": ("\\Seen", False),
		"flag": ("\\Flagged", True),
		"unflag": ("\\Flagged", False),
		"spam": ("\\Spam", True),
		"notspam": ("\\Spam", False),
		"junk": ("\\Junk", True),
		"notjunk": ("\\Junk", False),
	}

	if mark_type not in mark_map:
		available = ", ".join(mark_map.keys())
		raise SkillError(
			"VALIDATION_ERROR",
			f"data.markType must be one of: {available}",
			{"provided": mark_type},
		)

	flag_name, should_add = mark_map[mark_type]

	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	client = connect_imap(account_cfg)
	try:
		select_mailbox(client, folder)

		uid_list = uids.split(",")
		flag_op = "+FLAGS" if should_add else "-FLAGS"
		marked_uids: list[str] = []
		failed: list[dict[str, str]] = []
		for uid in uid_list:
			status, detail = client.uid("STORE", uid, flag_op, f"({flag_name})")
			if status == "OK":
				marked_uids.append(uid)
			else:
				failed.append({"uid": uid, "status": str(status), "detail": str(detail)})

		if failed:
			raise SkillError(
				"MAIL_OPERATION_ERROR",
				"Failed to mark one or more mails",
				{
					"uids": uid_list,
					"markedUids": marked_uids,
					"failed": failed,
					"folder": folder,
					"markType": mark_type,
					"flag": flag_name,
				},
			)

		return {
			"account": account_name,
			"uids": uid_list,
			"folder": folder,
			"markType": mark_type,
			"flag": flag_name,
			"marked": True,
		}
	finally:
		close_imap_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
