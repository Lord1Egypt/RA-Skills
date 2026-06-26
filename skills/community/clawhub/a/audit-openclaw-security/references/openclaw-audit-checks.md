# OpenClaw security audit: high-signal checks (quick glossary)

This is a convenience map for interpreting `openclaw security audit --json` and `--deep --json`.

> Treat OpenClaw’s own audit output as the source of truth. This file is intentionally **not exhaustive**.

| checkId | Typical severity | Why it matters | Primary fix key/path | Auto-fix? |
|---|---|---|---|---:|
| `fs.state_dir.perms_world_writable` | Critical | Other users/processes can modify the full OpenClaw state directory. | filesystem perms on `~/.openclaw` | Yes |
| `fs.config.perms_writable` | Critical | Others can change auth, tool policy, and routing config. | perms on `~/.openclaw/openclaw.json` | Yes |
| `fs.config.perms_world_readable` | Critical | The config can leak tokens or security-sensitive settings. | perms on config file | Yes |
| `gateway.bind_no_auth` | Critical | Remote bind without shared secret. | `gateway.bind`, `gateway.auth.*` | No |
| `gateway.loopback_no_auth` | Critical | Reverse-proxied loopback can become unauthenticated. | `gateway.auth.*`, proxy setup | No |
| `gateway.http.no_auth` | Warn/Critical | HTTP endpoints are reachable with `auth.mode="none"`. | `gateway.auth.mode`, `gateway.http.endpoints.*` | No |
| `gateway.tools_invoke_http.dangerous_allow` | Warn/Critical | Dangerous tools are reachable through HTTP API paths. | `gateway.tools.allow` | No |
| `gateway.nodes.allow_commands_dangerous` | Warn/Critical | High-impact node commands are reachable remotely. | `gateway.nodes.allowCommands` | No |
| `gateway.tailscale_funnel` | Critical | Tailscale Funnel makes the Gateway publicly reachable. | `gateway.tailscale.mode` | No |
| `gateway.control_ui.allowed_origins_required` | Critical | Non-loopback Control UI is missing an explicit browser origin allowlist. | `gateway.controlUi.allowedOrigins` | No |
| `gateway.control_ui.host_header_origin_fallback` | Warn/Critical | Host-header fallback weakens DNS rebinding protections. | `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback` | No |
| `gateway.control_ui.insecure_auth` | Warn | Control UI insecure-auth compatibility mode is enabled. | `gateway.controlUi.allowInsecureAuth` | No |
| `gateway.control_ui.device_auth_disabled` | Critical | Device identity checks are disabled entirely. | `gateway.controlUi.dangerouslyDisableDeviceAuth` | No |
| `gateway.real_ip_fallback_enabled` | Warn/Critical | Trusting `X-Real-IP` can enable source-IP spoofing via proxy misconfig. | `gateway.allowRealIpFallback`, `gateway.trustedProxies` | No |
| `discovery.mdns_full_mode` | Warn/Critical | mDNS full mode advertises extra metadata on the local network. | `discovery.mdns.mode`, `gateway.bind` | No |
| `config.insecure_or_dangerous_flags` | Warn | One or more insecure or dangerous debug flags are enabled. | see finding detail | No |
| `hooks.token_too_short` | Warn | Hook ingress token is easier to brute-force. | `hooks.token` | No |
| `hooks.request_session_key_enabled` | Warn/Critical | External callers can choose `sessionKey`, which can create persistence or collisions. | `hooks.allowRequestSessionKey` | No |
| `hooks.request_session_key_prefixes_missing` | Warn/Critical | There is no bound on externally supplied session key shapes. | `hooks.allowedSessionKeyPrefixes` | No |
| `logging.redact_off` | Warn | Sensitive values can leak into logs and status output. | `logging.redactSensitive` | Yes |
| `sandbox.docker_config_mode_off` | Warn | Sandbox Docker config exists but sandboxing is inactive. | `agents.*.sandbox.mode` | No |
| `sandbox.dangerous_network_mode` | Critical | Docker sandbox uses `host` or namespace-join networking. | `agents.*.sandbox.docker.network` | No |
| `tools.exec.host_sandbox_no_sandbox_defaults` | Warn | Default `exec host=sandbox` resolves to host exec when sandbox is off. | `tools.exec.host`, `agents.defaults.sandbox.mode` | No |
| `tools.exec.host_sandbox_no_sandbox_agents` | Warn | Per-agent `exec host=sandbox` resolves to host exec when sandbox is off. | `agents.list[].tools.exec.host`, `agents.list[].sandbox.mode` | No |
| `tools.exec.safe_bins_interpreter_unprofiled` | Warn | `safeBins` includes interpreter/runtime bins without explicit safe profiles. | `tools.exec.safeBins`, `tools.exec.safeBinProfiles` | No |
| `skills.workspace.symlink_escape` | Warn | A skill path in `skills/**` resolves outside the workspace root. | workspace `skills/**` filesystem state | No |
| `security.exposure.open_groups_with_elevated` | Critical | Open groups plus elevated tools create a strong prompt-injection path. | `channels.*.groupPolicy`, `tools.elevated.*` | No |
| `security.exposure.open_groups_with_runtime_or_fs` | Critical/Warn | Open groups can reach command/file tools without sandbox/workspace guards. | `channels.*.groupPolicy`, `tools.profile/deny`, `tools.fs.workspaceOnly`, `agents.*.sandbox.mode` | No |
| `security.trust_model.multi_user_heuristic` | Warn | The config looks multi-user without matching isolation and tool hardening. | `sandbox.mode`, tool deny, workspace scoping | No |
| `tools.profile_minimal_overridden` | Warn | Per-agent overrides bypass a minimal global profile. | `agents.list[].tools.profile` | No |
| `plugins.tools_reachable_permissive_policy` | Warn | Extension/plugin tools are reachable in permissive contexts. | `tools.profile` plus tool allow/deny | No |
| `models.small_params` | Critical/Info | Small or weak models plus tool access increase injection risk. | model choice + sandbox/tool policy | No |

## Notes for auditors

- `openclaw security audit --fix` is useful for some filesystem/logging issues, but it will not safely solve exposure problems for you.
- For shared inboxes, treat `session.dmScope` and DM/group policy as primary security controls, not “nice to have” settings.
- Reverse proxies, Tailscale Serve, browser-origin policy, and open group chats are where real-world OpenClaw incidents tend to get messy.
