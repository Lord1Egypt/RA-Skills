# 80 · 自迭代协议（本 skill 如何持续升级）

> 目标：让这套能力**越用越准**，而不是越用越臃肿。核心是三件事：**分层写回、版本化发布、可回归验证**。

## 1. 分层：什么写到哪里

| 发现 | 写入位置 | 约束 |
|---|---|---|
| 环境事实变化（版本/路径/阈值/端口/新插件） | `references/00-baseline.md` | 必须带日期 + 复核命令；旧值保留一行「历史值」 |
| 新坑/新规避 | `references/70-playbook.md` | `ERR-YYYYMMDD-NN`；现象可复现、根因有证据、修法可执行 |
| 流程/方法改进 | `references/30–60` | 步骤 + 命令 + 正反例；不写无法验证的口号 |
| 新门禁/检查项 | `scripts/*.ps1` | 5.1 兼容 + BOM + 正例/反例/空跑三种自测 |
| 触发边界变化 | `SKILL.md` frontmatter description | 视为 **MAJOR**（见 §3）；压测字符数 |
| 单次任务经验/决策 | 工作区 `memory/*.md` | `LRN/ERR/ADR` 条目；不进本 skill |
| **用户偏好/交付习惯** | 工作区 `memory/user-profile.md` | 维度 + 来源 + 生效状态（见 `85-ux-memory.md`） |
| 同类 ≥3 次 | 工作区 `memory/rules.md` | ≤120 字/条、≤60 条；超量归档 |

**判断口诀**：跨任务的稳定知识 → 本 skill；本机/本会话的临时状态 → 工作区 memory；两者都不放的 → 不写（避免成为噪音）。

## 2. 一次迭代的标准动作（单次 ≤30 分钟）

1. **触发**：retro、事故、体检 FAIL、用户明确要求迭代本 skill。
2. **取证**：先复现/量化（命令、日志、截图），确认不是偶发。
3. **最小改动**：只改一层（references 或 scripts 或 SKILL.md），能拆就拆到 `references/`。
4. **自测**：
   - 文档类：检查交叉引用路径存在、无死链、无与其它 reference 冲突的阈值；
   - 脚本类：正例 PASS / 反例 FAIL / 空工作区 SKIP，三种都跑（见 §4）；
   - 触发类：用 3 条典型用户措辞验证是否会被加载、2 条不该触发的措辞验证不误触发（人工判断 + 记录）。
5. **版本化**：`version.json` bump + `CHANGELOG.md` 追加（日期/版本/改了什么/为什么/验证/回滚）。
6. **回归**：重跑 §4 清单，并在 `CHANGELOG.md` 写结果。
7. **复盘**：`templates/retro.md` 落一条到工作区 `memory/team-learnings.md`（或设计/决策分册）。

## 3. 版本规则（semver）

| 变更 | 版本 | 例子 |
|---|---|---|
| 修错字、补证据、在既有脚本内修正或收紧校验（`package-skill` 可对不合格包 FAIL；门禁脚本 `loop-gate`/`capability-audit`/`skill-status`/`visual-qa-check` 退出码语义不变） | PATCH | 修正 `70` 里命令的参数名 |
| 新增章节/新脚本/新模板（向后兼容） | MINOR | 新增 `visual-qa-check.ps1` |
| 改 `name`、改触发边界、改门禁口径/退出码语义、删已有章节 | MAJOR | description 增加「也处理单点设计任务」 |

> 口径与 `SKILL.md「版本规则」`、`README.md「版本与更新」` 一致；三处如有冲突，以 `SKILL.md` 为准（`scripts/package-skill.ps1` 校验的是版本一致性，不判定 semver 级别）。

**发布纪律**：
- `name` 除极端情况不改（改名 = 触发与引用全断）；
- description 变更必须在 CHANGELOG 写「旧触发词 → 新触发词」；
- 脚本退出码语义（0/1/2）一旦发布不得悄悄改；要改只能 MAJOR 并在 CHANGELOG 明示；**唯一例外**：打包校验对「不合格产物」更严格（WARN → FAIL）属 PATCH，但必须在 CHANGELOG 写明哪类产物由 WARN 改 FAIL，且不得改 `loop-gate`/`capability-audit`/`skill-status`/`visual-qa-check` 的退出码语义；
- 每次发布保留可回滚副本（`CHANGELOG` 里写「回滚方法」）。

## 4. 回归清单（脚本/门禁改动必跑）

```powershell
$sk = "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"

# ① 空跑：无工作区资产时不崩溃、SKIP 合理
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\capability-audit.ps1" -Workspace "$env:TEMP" -OutFile "$env:TEMP\audit-empty.md"

# ② 正例：夹具任务目录具备 brief/tasks/acceptance/record → 应 PASS 或仅 WARN
# ③ 反例：文件夹具缺产物/缺证据 → 应 FAIL 并列出缺口
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-gate.ps1" -TaskDir "<夹具目录>"
```

判定：脚本改动后，**正例仍 PASS、反例仍 FAIL、空跑不崩溃**，三条件全满足才发布。

## 5. 健康度指标（体检报告尾部输出，月度看趋势）

| 指标 | 来源 | 目标 |
|---|---|---|
| catalog 描述总字符 | `capability-audit.ps1` | 不增长（源环境 3,673） |
| 死重量 skill 数 | 同上（依赖缺失/停用清单） | 0 |
| 检索可用 | 索引存在 >100MB + 实测搜索 | 是 |
| 门禁通过率 | 各任务落盘报告 | 逐月提升 |
| 本 skill 版本与 retro 数 | `version.json` + memory | 每月 ≥1 次回顾 |
| 误触发次数 | retro 记录 | 逐月下降；连续 2 月上升 → 改 description（MAJOR） |

## 6. 拆分与淘汰

- `SKILL.md` 正文 **< 300 行**；任一 reference **≤ 200 行**；超限拆分并在 §7 地图登记。
- 淘汰：连续 3 次任务未被引用、且不属「安全网」的章节/规则 → 删除（CHANGELOG 记「淘汰原因 + 恢复方式」）。
- 不再成立的旧事实：在 `00-baseline.md` 标「历史值」并给复核命令，不直接删（便于版本对比）。

## 7. 月度维护（10 分钟）

1. 跑一次 `scripts/capability-audit.ps1 -Strict`，看九组是否有 FAIL/WARN、漂移是否有未解释项；
2. 跑一次 `scripts/skill-status.ps1`，确认安装版与源是否一致（有新版只记录，不自动更新）；
3. 看 `CHANGELOG` 与 `version.json` 是否与磁盘一致；
4. 抽 1 条 `70-playbook` 条目验证「修法是否仍有效」；
5. 回顾过去 30 天 retro 与 `user-profile.md`：是否有条目要提升为规则、或标过期；
6. 若同事侧用了本 skill：只发 CHANGELOG 摘要，**不推送、不自动合并**（尊重对方的修改权）。

## 8. 更新提示、商店发布与自我升级的边界

**商店优先（上架后的正常路径）**：
- 安装/更新/回滚都由**技能市场 UI** 完成；本 skill 不后台下载、不自动覆盖。
- `scripts/skill-status.ps1` 读市场记录：`%USERPROFILE%\.dsh\storages\@montersy123\dsh-skill-market\data\panel.json`（`installed[]` 的 `name/version/latestVersion/origin/directory`）与 `installed.json`；对比安装版 `version.json`：
  - `origin=market` 且 `latestVersion > 安装版` → 提示「商店有新版本，请在市场里更新」；
  - `origin=manual` → 说明「手工安装，上架后由商店接管」；
  - 无记录 → 「未安装/未上架」。
- 源目录（`tools/capability-loop/skill/...`）对比仅用于**开发机**；商店安装版上不应出现源目录。
- 发布：`scripts/package-skill.ps1` 生成 `manifest.json` + `SHA256SUMS.txt` + `ZIP` + `PUBLISH-NOTES.md`；上架目录名约定 `<handle>--<slug>`（由商店决定），`SKILL.md` 的 `name` 保持不变。
- **上架（发布端）**：DSH 技能市场只负责安装，**没有发布入口**。上架 = `clawhub login` → `clawhub skill publish <技能目录> --slug ... --changelog ...` 发布到 ClawHub，SkillHub 由同步管线收录后，DSH 市场才能搜索/安装（命令、证据、未实测项见 `95-store-publish.md`）。
- 版本纪律不变：`PATCH/MINOR/MAJOR` + CHANGELOG 条目 + 回归三条件；上架包必须能通过 `package-skill.ps1` 校验。

**会做**：只读检查并提示差异；生成本地发布包；更新 `CHANGELOG`。
**不会做**：自动下载/覆盖、后台推送、静默改用户文件、把偏好写进通用 skill 正文、手工覆盖商店安装版（会让市场记录与实际不一致）。

**判断口诀**：
- 「这条知识对所有人都成立」→ 写本 skill（版本化，走上架流程）；
- 「只对这台机器/这个用户成立」→ 写工作区 `memory`；
- 「只是一次性的」→ 不写；
- 「同事/用户改过我的 skill」→ 只提示差异，不合并、不回滚对方。**他们的修改权优先。**
