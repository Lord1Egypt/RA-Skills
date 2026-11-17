# Published Application (ct-literature workbench)

> Extracted verbatim from `SKILL.md` "Published Application" section (2026-09-27, line-budget refactor — SKILL.md ≤ 200 lines per ct-base §16.1 / F02). No content removed; this file is the authoritative copy for deploy/publish operations. For re-publishing workflows, load this file.

## Registry

| Item | Value |
|---|---|
| Share link | `https://ct-literature.app.workbuddy.host/` |
| appId | `wbapp_WuOPnJ4caJ32GTquNlR7vc` |
| domainPrefix | `ct-literature` |
| Publish bundle | `workbench/publish-dist/` — **in-skill**, workspace-independent (rebuild: `python workbench/publish-kit/build_publish.py`) |
| Publish infra | `workbench/publish-kit/` — appId marker + installer + bundle builder + `publish.sh` one-command SOP; excluded from **both** outbound channels (never in `publish-dist/`) |
| Ownership marker | `workbench/publish-kit/.wbapp_WuOPnJ4caJ32GTquNlR7vc.genie` — **in-skill** authoritative copy (install: `python workbench/publish-kit/install_genie.py`) |
| Deployed as | Python HTTP service (`workbench/server.py` + `app.py` launcher, binds 0.0.0.0, reads `$PORT`) |
| Backend | `/api/config` `/api/status` `/api/sources` `/api/search` `/api/parse` `/api/tools` `/api/lit-stream` `/api/file` `/api/artifacts` `/api/bug-report` |
| Last deployed | 2026-10-23 17:06 (覆盖发布 verified；同步硬化发布链：build 排除 `_cleanup_parked` 调试停放区，部署包 3.4MB→1.78MB；新增 `publish.sh` 一键 SOP，build 设为 deploy 前硬关卡) |

## Re-publishing protocol

> **One-command path (recommended, 2026-10-23):**
> `bash workbench/publish-kit/publish.sh [<workspace_dir>] [--dry-run]` — runs
> build → install marker → prints the ready-to-use deploy call. The script hard-gates
> **build before deploy** (deploy uploads `publish-dist/` as-is; a skipped build ships
> stale code — observed 2026-10-23) and always passes `--workspace` explicitly
> (install_genie's own auto-detect walks up from CWD for a `.workbuddy/` dir and
> mis-resolves to the user home when run from inside the skill tree).
>
> **Re-publishing is workspace-independent (ct-base §13.5 方案 B).** The deploy bundle lives **inside the
> skill directory**, not in any workspace, so every workspace ships the same bundle:
>
> 1. **Install the ownership marker** into the target workspace root — one command:
>    `python workbench/publish-kit/install_genie.py` (add `--workspace <dir>` / `--dry-run` / `--all` as needed).
>    The authoritative copy lives in-skill at `workbench/publish-kit/.wbapp_WuOPnJ4caJ32GTquNlR7vc.genie`, so the
>    marker travels with the skill and its `localDir` is re-pinned to this machine on every run. The
>    deploy tool only checks that the marker exists in the *current* workspace — it does not care where
>    the bundle lives.
>
>    All publish infrastructure lives in `workbench/publish-kit/` and is excluded from **both** outbound
>    channels (skill public package and the deploy bundle). `publish-dist/` is the deploy payload itself —
>    never park infra files there.
> 2. **Deploy from the skill directory** with `directory = <skill>/workbench/publish-dist`,
>    `appId = wbapp_WuOPnJ4caJ32GTquNlR7vc`, `domainPrefix = ct-literature`.
>
> This is an **overwrite**, never `createNewApp`: reusing the `appId` is the only way to keep
> `https://ct-literature.app.workbuddy.host/`. A new app produces a suffixed domain — e.g. the superseded
> `ct-literature-32471.app.workbuddy.host` (`wbapp_KP86V43a9vCuDfqMjhGx05`) — which is an incident, not a
> fallback.
>
> **🔴 Bundle directory renamed `publish` → `publish-dist` (2026-09-26).** The server keeps a
> *directory-path → sandbox* binding that is invisible locally and **not corrected by re-pointing the
> genie / app.config**. The old `workbench/publish` path had been (mis)bound to the **meta** app's sandbox
> after a cross-workspace publish, so publishing from it silently overwrote `meta.app.workbuddy.host`
> (3×) instead of `ct-literature`. Renaming the in-skill bundle dir broke the stale binding. **Rule: a
> bundle directory that has ever been served by a hijacked/mis-bound path is permanently retired — republish
> from a fresh directory name, and always assert the returned `shareLink` matches the expected domain.**
>
> Earlier payloads lived in a workspace directory (`WorkBuddy/2026-09-16-08-09-44/deploy_cl_backend`); that
> layout could not be reused from another workspace and is retired.
