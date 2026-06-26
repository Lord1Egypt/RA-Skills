from typing import Any
from scripts.common import SkillError, close_imap_safely, connect_imap, load_config, resolve_account, with_runtime


def _skip_spaces(line: str, start: int) -> int:
	while start < len(line) and line[start].isspace():
		start += 1
	return start


def _consume_parenthesized(line: str, start: int) -> tuple[str | None, int]:
	if start >= len(line) or line[start] != "(":
		return None, start

	depth = 0
	index = start
	token: list[str] = []
	while index < len(line):
		char = line[index]
		token.append(char)
		if char == "(":
			depth += 1
		elif char == ")":
			depth -= 1
			if depth == 0:
				return "".join(token), index + 1
		index += 1
	return None, start


def _consume_atom(line: str, start: int) -> tuple[str | None, int]:
	start = _skip_spaces(line, start)
	if start >= len(line):
		return None, start

	if line[start] == '"':
		index = start + 1
		token: list[str] = []
		while index < len(line):
			char = line[index]
			if char == "\\" and index + 1 < len(line):
				token.append(line[index + 1])
				index += 2
				continue
			if char == '"':
				return "".join(token), index + 1
			token.append(char)
			index += 1
		return None, start

	if line[start] == "{":
		end = line.find("}", start)
		if end == -1:
			return None, start
		length_token = line[start + 1:end].strip()
		if not length_token.isdigit():
			return None, start
		literal_length = int(length_token)
		remainder_start = _skip_spaces(line, end + 1)
		remainder = line[remainder_start:]
		if literal_length <= len(remainder):
			return remainder[:literal_length], len(line)
		return remainder or None, len(line)

	index = start
	while index < len(line) and not line[index].isspace():
		index += 1
	return line[start:index], index


def _parse_mailbox_row(line: str) -> dict:
	raw = line.strip()
	index = _skip_spaces(raw, 0)
	flags_token, index = _consume_parenthesized(raw, index)
	if flags_token is None:
		return {
			"name": raw,
			"delimiter": None,
			"flags": [],
			"raw": raw,
		}

	flags = [flag for flag in flags_token[1:-1].split() if flag]
	delimiter_token, index = _consume_atom(raw, index)
	name_token, _ = _consume_atom(raw, index)
	if name_token is None:
		name_token = raw[index:].strip() or raw

	delimiter = None
	if delimiter_token and delimiter_token.upper() != "NIL":
		delimiter = delimiter_token

	return {
		"name": name_token,
		"delimiter": delimiter,
		"flags": flags,
		"raw": raw,
	}


def handler(request: dict[str, Any]):
	config = load_config()
	account_name, account_cfg = resolve_account(config, request.get("account"))

	client = connect_imap(account_cfg)
	try:
		status, rows = client.list()
		if status != "OK":
			raise SkillError(
				"MAILBOX_ERROR",
				"Failed to list mailboxes",
				{"status": status, "detail": str(rows)},
			)

		mailboxes = []
		for row in rows or []:
			if isinstance(row, bytes):
				decoded = row.decode("utf-8", errors="replace")
				mailboxes.append(_parse_mailbox_row(decoded))

		return {
			"account": account_name,
			"mailboxes": mailboxes,
		}
	finally:
		close_imap_safely(client)


if __name__ == "__main__":
	raise SystemExit(with_runtime(handler))
