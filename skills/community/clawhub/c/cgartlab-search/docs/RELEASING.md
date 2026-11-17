# 发布流程（RELEASING）

> 本文只写**流程与判据**；规则细则留在单一事实源：版本门槛见立正 skill 的 `references/judgment-criteria.md`（多层门）与 `references/release-versioning.md`，变更记录格式见 `references/changelog-sections.md`，版本载体清单见 `references/version-file-inventory.md`。**本文不复述它们的规则**（复述出的副本正是历史上漂移的地方）。

## 一、版本策略

| 项 | 约定 |
|---|---|
| 当前阶段 | **未切 1.0**：版本保持 `0.x`；未发布变更记入 `CHANGELOG.md` 的 `[Unreleased]`；是否切版、切到几，由维护者决定 |
| 版本载体 | **唯一载体**：`SKILL.md` frontmatter 的 `metadata.version`（立正脚本识别为 `agent-skill` 生态；缺失会导致 `version_files=[]`、`consistent=null`） |
| 编号语义 | semver：`feat` → minor、`fix` → patch、破坏性变更 → major（`0.x` 期间 minor 可含破坏性变更，但必须在 CHANGELOG 写明） |
| tag 命名 | `v<version>`，与 `metadata.version` **逐字一致** |
| 日期字段 | `metadata.date` 用**真实**发布日期 |

## 二、发布前的三道闸

1. **本地预检（只读）**：用立正的黑盒脚本核对仓库状态与版本一致性，要求 `is_git=true`、工作区干净、`version_files` 含 `SKILL.md`、`consistent=true`：

   ```powershell
   pwsh -NoProfile -File $env:USERPROFILE\.dsh\skills\attention\scripts\git_state_snapshot.ps1 --repo .
   pwsh -NoProfile -File $env:USERPROFILE\.dsh\skills\attention\scripts\version_consistency_audit.ps1 --repo .
   ```

2. **内容闸**：`CHANGELOG.md` 的 `[Unreleased]` 内容完整且每条可溯源（追不到 diff 依据的条目写 `［待补充：…］`，**不得**用 commit message 措辞填充）。
3. **版本闸**：`metadata.version` 与拟打 tag 一致；**推送 tag / 开 PR 属远程不可逆动作，执行点需单独最终确认**。

## 三、切一次版的标准动作

1. 确认 `[Unreleased]` 完整且可溯源。
2. 定版本号（拿不准就问维护者；不编造、不擅自跳大版本）。
3. 一致 bump：`SKILL.md` → `metadata.version` / `metadata.date`；`CHANGELOG.md` 把 `[Unreleased]` 改名为 `## [x.y.z] - <真实日期>`，并在其上方新开一个空的 `## [Unreleased]`。
4. 跑闸门（`bash scripts/gate.sh --smoke`，它是 `.github/workflows/ci.yml` 的等价实现 + 逐后端实跑；另跑 `evals/evals.json` 用例）。
5. 提交：`chore(release): x.y.z`。
6. 打本地 tag：`git tag -a v<x.y.z> -m "<摘要>"`；推送 tag 与开 PR 需单独确认。

## 四、本项目的发布边界

- **无 remote 时为纯本地仓库**：只做本地提交与本地 `git tag`，跳过推送与 PR（立正 `environment-and-prereqs.md`）。**不要说"连不上远程"**——没配远程就是没配。
- **首次发布例外（仅此一次）**：`0.1.0` 的导入与发布提交直接落在 `main` 上——新仓库在首个提交前不存在分支，无法走"先建分支"的常规路径。**此后每次发布变更都应走分支 + PR**，除非维护者当次另行裁定。
- **维护者 2026-10-23 裁定**：日常变更可直接提交 `main`（覆盖 `AGENTS.md` 的通用 PR 约定）。不可逆动作仍需单独确认：推送 tag、改写历史、变更仓库可见性。
- 受限出口环境下 `brave` / `exa` / `tencent` / `zhihu` 不可用属**预期状态**，不构成发布阻塞；`references/backends.md` 已记录可达性地图与降级规则。

## 五、发布自动化

| 文件 | 触发 | 职责 |
|---|---|---|
| `.github/workflows/release.yml` | push tag `v*` | 校验 tag == `metadata.version` → 门禁 → 从 CHANGELOG 抽本版小节建 Release → `needs:` 串起发布 |
| `.github/actions/publish/action.yml` | 被 release / publish 调用 | ClawHub 与 SkillHub 的打包与发布（逻辑唯一副本） |
| `.github/workflows/publish.yml` | 手动 dispatch | 只用于补发失败的发布、验证 token（`dry_run=true` 只打包） |

发布逻辑必须留在本仓库：public 仓库不能引用 private 仓库的 reusable workflow，跨仓库复用会让发布静默失效。`version` 由 `release.yml` 校验过的 `SKILL.md` 提供，publish 侧不再读 tag，避免两套版本号。