# Host Profile Template

Use this template for repeated audits or multi-session repairs on the same OpenClaw host. Keep populated profiles in the user's incident workspace or another private local path, not in the generic skill bundle.

Treat a profile as operator memory, not proof. Always verify live state before claiming health or applying a fix.

## Rules

- Record only non-secret facts: host names, service names, ports, paths, package source, versions, profile names, plugin roots, and redacted config-key names.
- Do not record tokens, OAuth material, env-file contents, session bodies, agent workspace contents, private messages, or prompt text.
- If live discovery disagrees with the profile, mark the profile stale and trust live discovery.
- Update the profile whenever install type, service manager, active user, config path, state dir, port, package source, plugin roots, rescue gateway, or OpenClaw version changes.

## Read-Only Build Commands

Run only the commands that fit the platform and target:

```bash
hostname -s
uname -a
which openclaw
openclaw --version
openclaw config file
openclaw gateway status --deep
openclaw status --deep
openclaw plugins list --json
openclaw channels status --deep
openclaw tasks audit
```

Service-manager probes:

```bash
ps -ef | rg openclaw
lsof -nP -iTCP -sTCP:LISTEN | rg '18789|19001|openclaw'
systemctl list-units '*openclaw*' --no-pager
launchctl list | rg -i openclaw
docker ps --format '{{.Names}} {{.Image}} {{.Ports}}' | rg -i openclaw
```

## Profile

| Field | Value |
|---|---|
| Primary host | unknown |
| Host access pattern | unknown |
| Host type | unknown |
| Container or VM layer | none known |
| Install type | unknown |
| Package source | unknown |
| OpenClaw version last observed | unknown |
| CLI path | unknown |
| Node/runtime path | unknown |
| Service manager | unknown |
| Service name/container name | unknown |
| Active user/service account | unknown |
| Primary profile | default |
| Config path | unknown |
| State directory | unknown |
| Gateway bind/port | unknown |
| Health endpoint | unknown |
| Local shipped docs path | unknown |
| Docs cache path | unknown |
| Managed skills path | unknown |
| Plugin roots | unknown |
| Update channel | unknown |
| Rescue/secondary profile | none |
| Incident workspace path | none |
| Last verification command set | unknown |

## Notable Choices

| Choice | This host |
|---|---|
| Primary model and fallbacks | unknown |
| Fast/no-thinking routes for crons/reviewer | unknown |
| Embedding/rerank provider and models | unknown |
| Auth profile ordering | unknown |
| Secrets provider type/name | unknown |
| Channel-to-agent bindings | unknown |
| Messaging channel policy shape | unknown |
| Approval policy and reviewer route | unknown |
| Plugin slot assignments | unknown |
| `gateway.reload` mode | unknown |
| Sandbox mode | unknown |

## Local Safety Notes

| Constraint | Value |
|---|---|
| Restart approval requirement | ask before restart/stop/service reinstall |
| Backup location/convention | timestamped local backup |
| Destructive cleanup constraint | ask before delete, move, uninstall, or service-manager changes |
| Env/secrets files to reference but not open | unknown |
| Known stale warnings or historical debt | unknown |
