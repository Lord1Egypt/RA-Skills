# Changelog — skill-inventory

All notable changes to this skill are documented here. Format follows a reverse-chronological
(newer on top) list per release. Version is bumped per SemVer on every user-facing change.

## [1.5.3] — 2026-10-17 (Display name 双平台同步)
- **ClawHub / SkillHub display name 正式同步**：两平台线上展示名统一为
  「技能盘点+健康体检 · Skill Inventory & Health Check」（与 `SKILL.md` / `SKILL.en.md` 的
  `displayName` 完全一致）。
- SkillHub 来源 = `SKILL.md` frontmatter `displayName`（发布干净副本自动读取）；
  ClawHub 来源 = `references/publishing.md` 发布命令的 `--name` 参数。
- 升版 1.5.2 → 1.5.3（线上 display name 不可原地改，必须各发一版；ClawHub 此前线上停在 v1.4.0）。

## [1.5.2] — 2026-10-17 (Tianxi AI 提交上架)
- **Tianxi (天禧 AI) 技能广场提交成功**：已通过 `lenovoskill push` 上传 `dist/skill-inventory-1.5.2-tianxi.zip`，
  `appId: 202610170048365362`，进入审核队列（约 5 个工作日）。
- **SKILL.md frontmatter `description` 精简**：原 1390 字符超出天禧服务端 1024 上限导致首推校验失败，
  精简至 893 字符（双语摘要保留核心能力与只读/授权写声明），重新打包后通过。
- 配套私有 `.skill-config.json`（git-ignored）已就绪；`push.js` 临时 patch 已重装回滚，无残留。
- **ClawHub / SkillHub display name 对齐**：两平台展示名统一为「技能盘点+健康体检」。
  SkillHub 来源 = SKILL.md / SKILL.en.md 的 `displayName`；ClawHub 来源 = `references/publishing.md`
  发布命令的 `--name` 参数（均改为 `技能盘点+健康体检`）。仓库版本号维持 1.5.2 未升版。

## [1.5.2] — 2026-10-14

### Tianxi (天禧 AI) publish-readiness remediation (P0–P2)
- **P0 — Version alignment**: `config.yaml` bumped `1.5.1 → 1.5.2` so the three in-repo
  version markers (SKILL.md frontmatter / config.yaml / SKILL.en.md frontmatter) agree again.
- **P0 — `config.yaml` contradiction removed for the Tianxi package**: the skill legitimately
  *writes* (consent-gated `--overrides --apply --yes` and `--set-lang`), so `config.yaml`'s
  `permissions.filesystem: read-only` was contradictory. `config.yaml` is **excluded from the
  Tianxi upload zip** (it is a local archive file, not an official upload requirement per the
  2026-10-01 platform doc verification) — eliminating the false read-only claim.
- **P1 — Dedicated white-list packaging script** (`tools/build_tianxi_zip.py`): produces a
  deterministic `dist/skill-inventory-1.5.2-tianxi.zip`, dropping dev noise
  (`references/check_skill_md.py`, `references/__pycache__`, dotfiles) and `config.yaml`.
  Replaces the stale `v1.4.0` package. Includes a post-pack safety scan (no `urllib`/`requests`/
  `http.client`/`socket.create`/`os.system`/`subprocess`/`os.popen`/`eval` in any `.py`;
  `SKILL.md` frontmatter must be valid YAML).
- **P1 — Docs aligned with implementation**: Tianxi AI is now explicitly described as supported
  **via the generic agent mode** (no dedicated profile; sandboxes have no close channel), in both
  `SKILL.md` and `SKILL.en.md` "when to use" sections. No over-claiming of a proprietary profile.
- **P2 — CHANGELOG.md / RELEASE_NOTES.md** added for the Lenovo three-place version-consistency practice.
- **P2 — Project-level `.skill-config.json`** created (private, git-ignored) with the schema the
  `lenovoskill` CLI actually reads (`name`/`description`/`description_zh`/`version`/`updateNotes`/
  `ignore`), pre-filling `ignore` with `config.yaml` for belt-and-suspenders exclusion.

### Carried over from earlier 1.5.x (audit-remediation)
- Non-blocking code-review fixes already shipped in `1.5.2` HEAD `df01c66`:
  - `backup_settings()` returns only the backup path (no misleading tuple).
  - Protected-leaf / safety-heuristic state moved to `main()` locals passed into `scan()` —
    eliminates cross-invocation module-level global leakage.
  - `attach_usage` substring magic number `5` → named constant `MIN_SUBSTR_LEN`.
  - `rows` implicit schema documented above `scan()` row construction (lowers B1 change risk).
  - Backup timestamp gains `%f` microseconds to avoid same-second `--apply` overwrite.
  - New i18n template `.format()` syntax self-test (206 templates all pass).

## [1.5.1] — 2026-10-09
- Resolved ClawHub DBM 91% / Intent-Code 87% contradiction (P0-1..P0-4):
  precise `persistence` wording, repo-wide "no autonomous residency" phrasing, removed shebang,
  added `capabilities`. AGENTIC over-delegation hits → 0.

## [1.5.0] — 2026-10-08
- Initial public-facing inventory skill with four-bucket classification
  (used / protected / closeable / manual-review) and anti-accidental-close guardrails.
