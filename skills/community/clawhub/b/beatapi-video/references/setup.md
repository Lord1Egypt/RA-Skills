# BeatAPI setup (hosts, keys, CLI)

The main Skill is <https://beatapi.io/skill.md>. This page covers connecting a
host once. Explain to the user only the steps that need their input.

## 1. Key

The user creates a key at <https://beatapi.io/dashboard/apikeys> and enters it
in the host's secure credential field, or configures `BEATAPI_API_KEY` privately.
Never request a key in chat, print it, pass it as a command argument, or put it
in a URL, file or tool input. Disable shell tracing around secrets. The key is
sent as `Authorization: Bearer <key>`, with or without its `sk-` prefix.

## 2. Transport

- **Remote MCP (preferred when the host supports it).** Server URL
  `https://beatapi.io/mcp`, streamable HTTP, header
  `Authorization: Bearer <key>` supplied through the host's secret mechanism.
  An environment variable alone does not add the header; follow the host's own
  documentation for the configuration format. Claude Code example:
  `claude mcp add --transport http beatapi https://beatapi.io/mcp --header "Authorization: Bearer $BEATAPI_API_KEY"`.
- **REST.** Any runtime that can send HTTPS requests: `https://api.beatapi.io`
  with the same header. No installation needed.
- **CLI (terminal hosts).** `npm install --global beatapi`, then
  `beatapi auth login` (the user types the key into a hidden prompt; it is kept
  in the OS credential manager). `beatapi capabilities search|inspect|run|status`
  exist from CLI 0.3.0; check `beatapi --help` before using a command.
- If the host has none of these, say which capability is missing. Reading this
  page does not grant network access.

If the host supports persistent skills, save <https://beatapi.io/skill.md> as
`beatapi/SKILL.md` in its skill directory.

## 3. Verify (read-only, costs nothing)

- **MCP:** list tools and confirm `capabilities_search`, `capabilities_inspect`,
  `capabilities_run`, `web_search`, `web_read`, `web_map`, `web_research`. Then
  search `{"query":"小红书"}` and inspect one example reference.
- **REST:** `GET https://api.beatapi.io/v1/usage` with the key must return 200
  (401 `missing_api_key` = header not sent; `invalid_api_key` = wrong key). Then
  `POST /v1/capabilities/search` with `{"query":""}` shows the catalogue map.
- `GET /v1/models` lists the text models this key can call.

Report the transport, whether the key was accepted, and a few real capabilities.
"Connected" is not "task completed". Do not start a paid run during verification.

## Local files

Capabilities take public HTTPS URLs. Upload local media first with
`POST https://api.beatapi.io/v1/files` (multipart, same key) or
`beatapi files upload <path>`, then pass the returned URL. Never pass a local
path as a URL.
