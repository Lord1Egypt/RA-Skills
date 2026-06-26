# ALab Global Admin Commands

## 推荐的 Root Invocation

通过 stdin 传递 root key：

```sh
printf '%s\n' "$ALAB_ROOT_KEY" | alab --key-stdin key list --root
```

关闭 shell tracing，并在分享 command transcript 前 redacted。Generated keys 应写入 ignored local files。

## Root Surface

Global admin 可以使用：

```text
alab auth init
alab auth root regenerate
alab config show|set|reset|validate
alab feedback --kind suggestion|question|bug|other --body "<text>"
alab feedback list|show|archive ...
alab dashboard [--port <0-65535>] [--no-open] [--refresh-seconds <0-3600>]
alab report --project <project_id> [--exp <exp_id>] --out <path> [--overwrite]
alab key create --project <project_id> --role admin
alab key list --root
alab key list --project <project_id>
alab key revoke <key_id>
alab context show|repair
alab project init local|git|empty|harbor|skydiscover ...
alab project list|show|archive|unarchive|remove ...
alab catalog skydiscover add|update|show|remove ...
alab cache prune ...
alab backup prune ...
alab audit list|show ...
```

## 功能明细

每项说明功能、作用、关键参数和输出/注意点。

- **`auth init`**：创建新的 ALab home 和 root key。
  关键参数：可选 `--home <path>`；不需要 credential。
  注意点：Raw root key 只打印一次；只能保存到 ignored 或安全位置。
- **`auth root regenerate`**：替换 active root key。
  关键参数：通过 global `--key-stdin` 或等价安全输入提供 root credential。
  注意点：Revoke 旧 root verifier，并只打印一次 replacement root key。
- **`config show`**：查看 ALab home-level config 和 validity。
  关键参数：无必需参数。
  注意点：显示 home config values 和 validity。
- **`config set`**：修改一个 ALab home-level setting。
  关键参数：必需 `<field> <toml-literal>`；用 `alab help` 或 `config show` 确认 allowed fields。
  注意点：`output.format` 只接受 TOML string `"text"`。
- **`config reset`**：重置一个 home-level setting 或全部 config。
  关键参数：必需 `<field>` 或 `--all`。
  注意点：用于从坏的 local config values 中恢复；不需要 root key。
- **`config validate`**：校验 home config，并可刷新 runtime capability checks。
  关键参数：可选 `--refresh-capabilities`。
  注意点：Docker/runner-sensitive work 前或环境变化后使用。Unsupported/error capability results 会包含可操作的 `next` 修复提示；修复 local runtime 后应再次 refresh。
- **`feedback`**：为 ALab operation、docs、environment issues 或 bugs 留 HOME-level feedback。
  关键参数：`--body <text>` 或 `--body-file <path>` 二选一；可选 `--kind suggestion|question|bug|other` 和 `--title <text>`。
  注意点：Feedback 是 local home-level text，不影响 project evidence。
- **`feedback list|show|archive`**：检查和归档 HOME-level feedback。
  关键参数：`list` 可选 `--kind`、`--query`、`--limit`、`--offset` 和 `--include-archived`；`show` 必需 `<feedback_id>`；`archive` 必需 `<feedback_id>`，可选 `--reason <text>`。
  注意点：Root-only。Archive 是幂等操作，不影响 project evidence。
- **`dashboard`**：打开 root-only local read-only dashboard。
  关键参数：可选 `--port <0-65535>`、`--refresh-seconds <0-3600>` 和 `--no-open`。
  注意点：要求 root credential，只绑定 `127.0.0.1`，渲染 token URL，并阻塞直到 interrupted。不要分享 token URL；dashboard 可以读取 hidden/full logs 和 artifacts，但不得 mutate ALab state。
- **`report`**：导出 Markdown project 或 experiment evidence report。
  关键参数：必需 `--project <project_id>` 和 `--out <path>`；可选 `--exp <exp_id>` 和 `--overwrite`。
  注意点：Root 可以导出 project-wide 或 experiment-scoped reports。Report 有意省略 raw keys、tokens、secret values、hidden-log contents 和 artifact bytes。
- **`key create`**：为 project-level session 创建 project admin key。
  关键参数：必需 `--project <project_id>`；可选 `--role admin`。
  注意点：Root-only；raw admin key 只打印一次。
- **`key list --root`**：查看 root credentials。
  关键参数：必需 `--root`；与 `--project` 冲突。
  注意点：用于确认 active/revoked root credential ids，不暴露 raw keys。
- **`key list --project`**：查看 project admin credentials。
  关键参数：除非 project context 已提供，否则必需 `--project <project_id>`。
  注意点：Root/admin 可以查看 project credentials；不渲染 raw admin keys。
- **`key revoke`**：按 id revoke credential。
  关键参数：必需 `<key_id>`；可选 `--project <project_id>`。
  注意点：Revocation 是 root-only；先检查 audit 和 scope，避免 revoke 错 active key。
- **`context show`**：查看 path context markers 和 registered ALab paths。
  关键参数：可选 `--path <dir>`；默认 `.`。
  注意点：Repair 前或命令落入意外 project/experiment/inspection context 时使用。
- **`context repair`**：在授权时修复 path context marker。
  关键参数：必需 `--path <dir>`。
  注意点：Root/admin 可修复 scope 内路径；token self-repair 有严格 Git branch 或 pinned-commit checks。
- **`project init`**：创建 project、source、config version、baseline validation 和 project admin key。
  关键参数：Mode `local|git|empty|harbor|skydiscover`；必需 `--config`；common `--name`、`--task`、`--goal`、`--skip-baseline-test`；mode-specific source/task fields；source size limits。
  注意点：Runtime behavior 只来自 config。Generated project admin key 在 project 创建后只打印一次。
- **`project list|show`**：查看 projects。
  关键参数：`list` 接受 `--include-archived`；`show` 接受可选 `--project <project_id>`。
  注意点：用于查找 project ids、statuses、active config version、default source、runner、reward 和 visibility。
- **`project archive|unarchive`**：切换 project lifecycle status。
  关键参数：可选 `--project <project_id>`。
  注意点：Archive 可能被 active locks 或 maintenance 阻止。
- **`project remove`**：以 audited cascade 删除 archived project。
  关键参数：必需 `--cascade`；再加 `--dry-run` 或 `--force --confirm <project_id>`；可选 `--project`、`--reason`。
  注意点：Root-only 且 destructive。始终先 dry-run；actual remove 会把可删除路径移入 ALab trash。
- **`catalog skydiscover add|update`**：安装或修改 pinned SkyDiscover catalog。
  关键参数：可选 `--origin-url <url>`；`--ref <ref>` 和 `--commit <full_sha>` 至多二选一。
  注意点：需要 reproducibility 时优先用 `--commit`。`update` 要求 ALab-managed catalog 干净。
- **`catalog skydiscover show`**：查看 active SkyDiscover catalog state。
  关键参数：不需要 catalog selector。
  注意点：不应访问网络；用于确认 pinned commit 和 local path。
- **`catalog skydiscover remove`**：删除 active SkyDiscover catalog state 和 local checkout。
  关键参数：必需 `--force --confirm skydiscover`；可选 `--reason`。
  注意点：仍有 active configs 或 open experiments 引用 catalog 时会被阻止。
- **`cache prune`**：删除 ALab-owned non-authoritative caches。
  关键参数：Selectors：`--docker-images`、`--skydiscover-envs`、`--trash --older-than <days>`、`--trash-all` 或 `--all`。
  注意点：`--all` 与单项 selectors 冲突；trash retention days 必须非负。
- **`backup prune`**：删除旧 pre-upgrade backups。
  关键参数：`--keep <n>` 或 `--older-than <days>` 二选一。
  注意点：Retention values 必须非负；输出 pruned paths 和 audit id。
- **`audit list`**：搜索 global 或 project-scoped audit events。
  关键参数：可选 `--project`、`--object-type`、`--object-id`、`--action`、`--actor`、time bounds、`--limit`、`--offset`。
  注意点：Root 可 global query；project admin 仅限 project scope。
- **`audit show`**：查看单个 audit event 和 redacted details。
  关键参数：必需 `<audit_id>`；可选 `--project <project_id>`。
  注意点：用于验证 credential、project、catalog、cleanup、repair 和 remove actions，不暴露 raw secrets。

Root 必要时也可以 inspect 或维护 project-scoped resources，但日常 experiment coordination 应交给带 project admin key 和 `alab-project-controller` skill/instructions 的 project-level session。

## Project Initialization

`project init` 成功后，把打印出的 project admin key 视为 handoff material。除非用户明确要求，否则当前 session 应聚焦 root-scoped setup、credentials、catalogs、cleanup、audit 和 handoff。

使用 `SKILL.md` 中的 layer-specific credential rules：project-level work 只接收 project admin key 和 `alab-project-controller` skill/instructions；experiment work 只接收 experiment worktree token context 和 `alab-experiment-worker` skill/instructions。

Local project：

```sh
printf '%s\n' "$ALAB_ROOT_KEY" | alab --key-stdin project init local \
  --config alab.project.toml \
  --source-path . \
  --name "$PROJECT_NAME" \
  --task "$TASK"
```

SkyDiscover project：

```sh
printf '%s\n' "$ALAB_ROOT_KEY" | alab --key-stdin catalog skydiscover add --commit "$SKYDISCOVER_COMMIT"

printf '%s\n' "$ALAB_ROOT_KEY" | alab --key-stdin project init skydiscover \
  --config alab.project.toml \
  --name "$PROJECT_NAME" \
  --task "$TASK"
```

`project init` 会在 project 创建后只打印一次 generated project admin key。应将其捕获到 ignored local secret file（例如 example `.run/secrets/project.env`）或已批准的 secret store，然后只把 project admin key 交给被委派的 project-level session，绝不交给 experiment workers。
成对配置 `runner.type = "none"` 和 `reward.type = "none"` 会创建 free evaluation projects，用于直接 submit 且不运行 baseline evaluator；仅应搭配 `local`、`git` 或 `empty` project init modes 使用，不与 Harbor 或 SkyDiscover adapter init 混用。
Config 也可以声明 `metrics.reference` entries，用于 dashboard 将 optional numeric run metrics 绘制为 reference curves；这些声明不影响 reward ranking 或 baseline execution。

## Catalog Rules

- 需要 reproducibility 时，用 `--commit` pin SkyDiscover。
- `catalog skydiscover show` 不应访问网络。
- Missing catalog paths 不会 auto-update。
- 仍有 active configs 或 open experiments 引用 catalog 时，`catalog skydiscover remove` 会被阻止。

## Cleanup Rules

Cleanup 只用于 non-authoritative data：

```text
alab cache prune --docker-images
alab cache prune --skydiscover-envs
alab cache prune --trash --older-than <days>
alab cache prune --trash-all
alab cache prune --all
alab backup prune --keep <n>
alab backup prune --older-than <days>
```

对 destructive project 或 lifecycle removal，应先运行 dry-run，检查 blockers，再要求 exact confirmation。

## Handoff

Global admin handoff 应包含：

- 可安全分享时的 ALab home path 和 home id；
- project id、project name 和 active config version；
- generated project admin key delivery path，或已通过 ignored/secure secret 位置完成 handoff 的确认；
- 后续仍有 project 或 experiment work 时，对应的 session/thread 或 subagent handoff target；
- 已向该 target 提供匹配的 ALab skill/instructions（project-level work 用 `alab-project-controller`，experiment worktree work 用 `alab-experiment-worker`）；
- 任何委派 session 需要 key/token 时，对应的 credential delivery path 或 secure-channel note；
- 如适用，catalog pinned commit；
- validation id 和 validation status；
- 已执行的 cleanup 或 audit actions。
