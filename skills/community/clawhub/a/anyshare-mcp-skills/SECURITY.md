# Security

## Treat this skill as operational guidance, not executable trust

- Review `SKILL.md` and scripts before use in production. Third-party or
  registry-installed skills should be audited like any other automation.
- **Never** commit or paste real cookies, OAuth tokens, or Bearer strings into
  Git, ClawHub descriptions, or chat logs.

## Secrets and configuration

- **MCP service URL** defaults to `https://anyshare.aishu.cn/asmcp` in the skill template; override in `~/.mcporter/mcporter.json` (`asmcp.url`) for private deployments. Values are **environment-specific**.
  Do not commit internal-only URLs to public repos if they expose your network topology.
- **Access tokens** are written to `~/.mcporter/mcporter.json` under `asmcp.headers.Authorization` (documented in **`SKILL.md`**, section **「首次配置」**). Do not commit secrets or paste tokens into chat logs.
- **Token renewal**: when a token expires or is revoked, update `headers.Authorization` in `~/.mcporter/mcporter.json` and run `mcporter daemon restart`. Tokens are not cached by the skill itself.
- **Pasted tokens** must not appear in shell history, chat logs, or version control.
- **Environment-variable injection** of tokens is **not** the default path; **`openclaw.skill-entry.json`** only documents **`MCPORTER_CALL_TIMEOUT`**.

## Data handling

- The skill may access enterprise documents only as permitted by your AnyShare
  account and MCP server policy. Follow your organization's data-classification rules.

## Reporting

- For vulnerabilities in **this skill's documentation or packaging**, open an
  issue in the repository that maintains this skill. For product security issues
  in AnyShare itself, follow AISHU's official disclosure channels.
