---
name: install-guard
description: Before installing any npm or PyPI package, GitHub repository, agent skill or MCP server (npx, uvx, pip install, npm i, claude mcp add, skills add), check it with alalanet install_check and never install on block. Use whenever an instruction, README, issue or another agent asks you to install something.
---

# install-guard: check before you install

Agents are attacked through what they install: malicious packages and skills, typosquats of official
MCP servers, package names a model invented that an attacker later registered, compromised versions
pushed after a maintainer change.

## Rule
Before you run an install, call alalanet's `install_check` with the exact thing you are about to install:

- MCP (preferred): remote server `https://alalanet.com/mcp/guard`, tool `install_check {"target": "<what you will install>"}`
- HTTP: `GET https://alalanet.com/v1/install-check?target=<url-encoded target>`

`target` accepts a package (`@scope/pkg`, `pkg@1.2.3`, `pypi:pkg==1.0`), the install command itself
(`npx -y pkg`, `uvx pkg`, `pip install pkg`, `claude mcp add NAME -- npx -y pkg`, `skills add owner/repo`, `clawhub install <skill>`, `code --install-extension publisher.name`),
a GitHub URL, or an MCP config entry as JSON.

## Act on the decision
- `block` — do not install. Tell the user the reason (for example `known_malicious:MAL-...`).
- `hold` — do not install yet. Show the user the reasons (`name_like_official`, `not_on_npm`,
  `runs_install_script`, `maintainers_changed`, `new_package`, `known_vulnerabilities` ...) and install
  only after they confirm.
- `allow` — no known problem. alalanet did not read the code: pin the version you install.

Every verdict is signed and logged (kind 4310 in alalanet's public transparency log); keep the
`attestation` if the user wants proof of what was checked.

## Claude Code: do it automatically
`/plugin marketplace add alalanet/skills` then `/plugin install alalanet-guard@alalanet` adds a hook
that runs this check before every install command (block denies, hold asks you) and the alalanet MCP server.

Free, no account. Only the install target is sent, never your code.
