# 90 · 血缘与验证证据（Provenance）

> 本 skill 不是凭空写的：它把两个真实会话的产出合并、去重、抽象成可执行闭环。
> 读本文件的目的：知道「哪些结论有实测支撑、哪些是未实测/受环境限制」，避免把历史结论当永久事实。

## 1. 源会话

| 会话 | 时间 | 做了什么 | 主要产物 |
|---|---|---|---|
| `session-0d908c48-92d7-432e-9303-966161df7a81` | 2026-11-12 01:40–13:00 | ①三路并行审计 DSH 安装面（skills/插件/运行时）②按用户决策做升级：修 P0 检索、修桌面壳探活、清 token-insights、收敛市场、停用死重量 skill ③建生产级 UI 设计能力 ④建原生团队契约/需求评审/测试 oracle/需求规格标准 ⑤系统证据驱动需求重建（示例：输差管理）⑥单文件 HTML 总览 ⑦迁移交付包 v1.0 | `DSH-Skill与插件整合审计-2026-11-12.md`、`upgrade/`、`standards/`、`projects/输差管理/`、`handover/01–07`、`dist/DSH-迁移交付-v1.0.zip` |
| `session-3ef140c9-2ed3-4857-a7ad-9374b9107949` | 2026-11-12 08:02–16:31 | 调研「DSH↔Trae 分工」可行性 → 落地方案 A（文档契约 + CLI 唤起 + 回读取证 + 门禁），产出 DSH skill `feature-handoff`、Trae skill `spec-implementation-only`、四脚本、四模板、安装脚本，并登记 `AGENTS.md §2.7` 与 memory | `tools/trae-handoff/`、`~/.dsh/skills/feature-handoff/`、`~/.trae-cn/skills/spec-implementation-only/`、`handover/方案A-*.md`、`handover/断点清单-*.md` |

合并时的取舍：
- 0d908 的「DSH 自身升级+方法体系」与 3ef140c9 的「DSH↔Trae 交接」是同一台 DSH 的**上下游**（治理 → 方法 → 交接 → 验收），因此合并为一条闭环，而不是两个并列 skill。
- 不复制 `ui-design-production` / `feature-handoff` 正文，只在本 skill 里定义**何时加载、如何接线、如何验收**（避免三处维护同一规则）。
- 「审计报告」「升级包」「示例项目」保留在工作区，本 skill 只记录入口与判定口径（它们是可重建产物，不是 skill 内容）。

## 2. 已实测的证据（可引用）

| 结论 | 证据 |
|---|---|
| 检索已恢复 | 预建后 `session_search("断点清单")` 返回真实结果（session id/parent/seq/snippet），秒回；索引 `session-index.sqlite` ≈213MB（后续 250MB） |
| 首次建库耗时 | 256 会话 / ≈194MB → 2–3 分钟；旧壳下建库 24s 内被误杀（`desktop.log` 11:37:53/58、11:38:03 三次探活失败 → killTree → 重启） |
| 桌面壳补丁有效 | 隔离实例实测：强杀服务器 → stderr 落盘 + 退避 3000ms + 恢复前复核（无 EADDRINUSE/重复 spawn）；挂起 50s 未被 kill；补丁版 `--smoke`：`code:0, ok:true, boot:true`（3080 占用时自动换端口 64999） |
| 重启后验收 | `post-restart-check.ps1` → `PASS（FAIL=0，待重启项=0）`；重启后 0 次 `3/3` 判死；无失败 `startup-*.log` |
| 插件清理 | `pnpm -5`；`--dump-config` exit 0，`dsh-token-insights`/`dshmarket` 出现 0 次；catalog 21→12 条 |
| 成本结构 | 固定前缀 ≈12.2k tokens/请求（工具 10.1k + 系统 2.1k）；技能清单 14,950 字符/会话；缓存命中 95.96%；glm-5.3+kimi-k3.1-pro 占 5.6% 调用吃 43% 成本 |
| 文档门有效 | 存量 4 篇打分 47/33/75/59；重排示例 87；输差 SRS v0.1 → 100/100 |
| 追溯门有效 | 输差项目：文档门 100 PASS，追溯门 **FAIL 13**（P0 待口径会 + 部分 P0 为 C + P1 覆盖 50%）——刻意保留的失败结果 |
| 设计能力 | `ui-design-production` 83 字符 description；rubric V1–V12；视觉 QA A/B/C（沙箱不可用已实测） |
| 团队能力 | 原生 Team 探针：设计请求会加载 skill；团队不会自动 spawn（无常驻角色、无配置级路由）；gate-check 探针目录 FAIL 9 项、合规夹具 PASS |
| TeamHarness 不可替代 | `server.py` api_base 默认 `127.0.0.1:8088`，端口 CLOSED；profile 未注册 `dsh-mcp-client` |
| 交接闭环 | 脚本自测：空模板 prepare FAIL（5 项）、填写后 prepare/deliver PASS、结论改回待填 FAIL；`collect-evidence` 失败命令 exit 2 记录真实退出码；非 git 工程 exit 0 + 标注「diff 无法取证」；`open-in-trae` DryRun 解析到 `D:\Trae CN\bin\trae-cn.cmd` |
| 设计 skill 触发 | 探针真实调用 `skill("ui-design-production")`；触发来自 AGENTS.md（自动注入）+ description + rules 三道约束 |
| 商店三层关系（2026-11-13） | 市场插件 README 定位为 SkillHub 浏览/安装端；`panel.json` 实读 `origin=market/manual`、`latestVersion`；SkillHub API `source:"clawhub"`、`upstream_url:"https://clawhub.ai/<user>/<slug>"`、详情 `latestVersion.changelog:"Synced by skillhub pipeline"`；ClawHub 官方 npm README 给出 `clawhub login` / `clawhub skill publish <dir> --slug ...`；本机已装 clawhub skill 有 `_meta.json`（ownerId/slug/version/publishedAt） |

## 3. 未实测 / 受环境限制（不得当事实）

1. **Trae 侧读取行为**：Trae SOLO 是否真读 `AGENTS.md`/`.github/instructions`；技能面板是否显示手工安装的 skill；`-g` 是否精确跳到行（CLI 返回 0，未目视核对）。
2. **浏览器/视觉自动化**：`workspace-write` 下 agent-browser 拉起 Chrome 会因 crashpad `OpenProcess` 被拒失败（exit -36863）——属**进程/权限限制**；`danger-full-access` 下 **Chrome headless `--screenshot` 已实测出图且像素正确**（2026-11-13，1280×720），agent-browser 也能保存截图但 `open` 会挂起（CLI 行为，需后台+超时）。`visual-qa-check.ps1` 把这条判定做成可执行探针：exit 0=A 可用、exit 2=权限受限并**显式提示用户选 A/B/C**（不静默标未实测）。生产默认仍推荐 B（用户终端截图）作对照。
3. **口径类规则**：输差三差率等 R-TL 规则目前多为 B/C 级、待口径会；**P0 规则未签署前，测试追溯门会刻意 FAIL**。
4. **桌面壳补丁与版本强相关**：DSH 升级覆盖 `main.js` 后锚点/哈希会变，必须按新版本重做；源环境补丁只对 2026-11-12 的安装有效。
5. **MCP/异步协作**：未注册/未启用，结论「当前不可用」只代表本机此时状态。
6. **成本数字**随 provider 价格、缓存策略、会话长度变化，只能当量级参考。
7. **商店上架的真实链路**：**已证实** DSH 技能市场只是 SkillHub 客户端（无发布入口）、SkillHub 的 `source=clawhub` 条目由同步管线收录、ClawHub 用 `clawhub` CLI 发布（命令见其官方 npm README）；**未实测** `clawhub login`/`clawhub skill publish` 的真实执行（需 GitHub 授权，且本机 shell 网络不可用：`npm` ETIMEDOUT、`Invoke-WebRequest` TLS 失败）、SkillHub 同步时延、SkillHub 是否有独立上传入口。详见 `95-store-publish.md §6`。

## 4. 如何重新验证

```powershell
# 1) 体检
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.dsh\skills\dsh-capability-loop\scripts\capability-audit.ps1" -Strict
# 2) 环境验收（要重启过桌面版）
powershell -NoProfile -ExecutionPolicy Bypass -File "upgrade\post-restart-check.ps1"
# 3) 检索
#    在 DSH 里调用 session_search("断点清单")，看是否返回真实结果
# 4) 门禁
powershell -NoProfile -ExecutionPolicy Bypass -File "upgrade\team\gate-check.ps1" -TaskDir "<任务目录>" -Kind design
powershell -NoProfile -ExecutionPolicy Bypass -File "upgrade\team\test-traceability.ps1" -TaskDir "<任务目录>"
```

## 5. 版本血缘

- **v1.0.0（2026-11-12）**：首次合并两个源会话，定义五阶段闭环、六组审计指标、四类门禁接线、自迭代协议；scripts 提供 `capability-audit`、`loop-gate`。
- **v2.0.0（2026-11-12）**：按用户 11 问补齐能力（下表）；新增 INTAKE/55 设计前置/GRILL/85 偏好记忆/QUICKSTART；脚本新增 `product-context`、`trae-status`、`skill-status`；audit 扩到九组（含 Trae/版本/漂移）；loop-gate 增加 design-context 硬门与 grill 建议（design 硬门为 breaking）。
- **v2.0.1（2026-11-12）**：独立评审后修 2 P0 + 6 P1（gate-check 编码、grill 语义、交接包误判、更新命令嵌套、分组错位、指标口径）。
- **v2.1.0（2026-11-13）**：按用户 6 条追问补：商店化更新（`skill-status` 读市场记录）/发布打包（`package-skill`）/Trae 工程匹配硬门/接入六问模板/交接链路冒烟（`handoff-smoke`）/三域 grill（设计·需求·测试）+ 浏览器权限实测结论。
- **v2.1.1（2026-11-13）**：独立复验 P2 修复（panel 条目健壮性、占位 handle 提示、时间线/措辞纠正）；六项能力复验 6/6 PASS。
- **v2.1.2（2026-11-13）**：接入问题模板去掉「迁移给同事」选项；新增 `visual-qa-check.ps1`（视觉验收 A 路径探测 + 权限不足时显式提示 A/B/C），`50-design-team.md §3` 增加用户选择话术。
- **v2.2.0（2026-11-13）**：新增 `README.md`（商店/人读概览）与 `references/95-store-publish.md`（ClawHub→SkillHub→DSH 市场上架实操 + 证据 + 未实测项）；`version.json` 登记 `visual-qa-check.ps1` 与发布元数据；修正 P2（视觉探测失败分支证据路径、`package-skill` 发布提示/PUBLISH-NOTES、CHANGELOG 脚本数口径）。
- **v2.2.1（2026-11-13）**：清理 v2.2.0 复核残留（N1–N5/R1/R2）——`95-store-publish.md` 路由清单更正为实读 16 条、`_meta.json` 统一为「安装版实证/发布未实测」、补「市场已安装版本取自 frontmatter `version`」证据与发布版本号未确认项；`version.json.compatibility.node` 改为 22.13+ 口径；`package-skill.ps1` 补 `-ExtraSensitivePaths` 用法注释、本机路径扫描按文件去重、ZIP 结构不合格改 FAIL、新增 frontmatter `version` 一致性校验；`SKILL.md` 声明 `version: 2.2.1`（市场据此显示已安装版本）；`README.md` 版本口径同步（PATCH 允许收紧打包校验、版本号三处一致）。
- **v2.3.0（2026-11-13）**：新增 `scripts/module-preflight.py`（交接前模块/路由预检：扫描 `src/views`、`src/api`、`apps/*/src/{views,api}` 与 router 关键字，其中 `norm()` 去非字母数字再比对；exit 0=NONE / 1=EXISTS / 3=WEAK / 2=参数错误；输出 Markdown 报告，默认落 `<工程>/.tmp/module-preflight/`，可用 `--out` 改路径）；`SKILL.md` 不变式 17、`references/60-handoff.md` 步骤 1.5、`README.md` 脚本表、`QUICKSTART.md §4` 接线；实测（`rmp-frontend`）正例 `输差考核台账`=NONE/0、反例 `资源需求`=EXISTS/1（`apps/web-main/src/views|api/resourceDemand`）、参数错误=2；`--menu-dump` 对 live 菜单接口未实测。
- **v2.4.0–v2.7.0（2026-11-13）**：交接自动化联调记录（`feature-handoff/scripts/send-to-trae-prompt.ps1`：Hotkey→Click+截图哈希校验→指针模式；`trae-cdp.mjs`：CDP 定位/写入/读回）；**脚本本体在 feature-handoff，本 skill 只同步 `references/60-handoff.md` 接线与版本记录**。实测证据见各版本 CHANGELOG（CDP：len=159/head 正确/未发送、找不到输入框 exit 3、端口未开 exit 4）。
- 后续版本差异只查 `CHANGELOG.md`；本文件只在「新增证据/新增未实测项/源会话变化」时更新。

## 6. 能力对照表（用户 11 问 → 本 skill 的落点）

| # | 问题 | 落点 | 实测/验证 |
|---|---|---|---|
| 1 | 具备哪些能力 | `SKILL.md` §0–§7、`QUICKSTART.md`、本表 | — |
| 2 | 是否动态检测技能/插件健康 | audit I 组漂移（快照 `<ws>/.tmp/capability-loop/audit-state.json`）+ 定时跑 `-Strict` | 两次运行出现「无指标变化/变化=…」对比；FAIL=0 |
| 3 | 是否动态关联 Trae | `trae-status.ps1`（CLI/进程/交接包/下一步，只读）+ `open-in-trae.ps1`（真正唤起） | 实测识别 CLI `d:\Trae CN\bin\trae-cn.cmd`、4 个进程、夹具包 PASS |
| 4 | 是否有 skill 更新提示/自动更新 | `skill-status.ps1`（版本/哈希差异 + 手动更新命令；**不自动更新**） | 源 vs 安装版对比；发布后一致 |
| 5 | 是否有首次使用手册 | `QUICKSTART.md`（3 条命令/怎么开口/问题导航） | 已随 skill 分发 |
| 6 | 是否主动问项目并派专家 | `05-intake.md`（≤6 问 + 专家编排表 + `project-profile.md`） | 模板与流程落盘 |
| 7 | 是否深入理解产品设计/业务 | `30-requirement.md` 四源证据 + 业务旅程；`product-context.ps1` 扫工程；`55-design-intake.md` | 对 rmp-frontend 实测识别 ant-design-vue/echarts/vben/tailwind，路由 44/API 1154/mock 32 |
| 8 | 出稿前是否判断现有主题/组件库 | `55-design-intake.md` 硬门 + `design-context.md`；loop-gate design 缺则 FAIL | 夹具 A FAIL(exit1)、B/C PASS |
| 9 | 是否输出 HTML 总览 | `SKILL.md` §2 R11 + 工作区 `tools/build-docs-html.py`（单文件/搜索/双主题/设计稿预览） | 源环境输差项目已产出 194KB 单文件 HTML |
| 10 | 是否有记忆能自我进化 | `80-evolution.md` 分层写回 + `85-ux-memory.md` 偏好账 + `memory/` | 偏好/反馈/度量流程落盘 |
| 11 | 是否对自己产出 grill | `75-grill.md` + `grill-checklist.md`；loop-gate 检查 `grill-*.md`（缺失 WARN） | 夹具记录即 PASS；≥1 个打回要求 |
| 12 | Trae 关联能否支撑设计驱动开发 | `60-handoff.md` §5：交接包带 design-context、UI 任务绑设计依据、视觉 AC、禁止引入新 UI 体系 | 规则落盘；真实交接需用户侧工程与截图（未实测） |

> 诚实边界：第 2/3/4/7/8/10/11 条的**脚本能力**已实测；真正「动态」依赖用户定时触发（script 不常驻）；第 12 条设计驱动交接对真实工程属**未实测**（明日按 `templates/design-handoff-smoke.md` 实测后改为「已实测」）。

## 7. 后续 6 条追问的落点（2026-11-13）

| 追问 | 落点 | 实测/状态 |
|---|---|---|
| 上架商店后按商店逻辑更新 | `skill-status.ps1` 读市场 `panel.json`/`installed.json`（`latestVersion`/`origin`/`directory`），商店优先、源目录仅开发对照；`package-skill.ps1` 生成可上架包（manifest/SHA256/ZIP/PUBLISH-NOTES）；`80-evolution.md §8` 写更新边界 | 本机市场记录识别本 skill 为 `origin=manual`；伪 `latestVersion` 比对逻辑于 v2.1.0 发布前单测；**真实上架版本未验证**（见 §3.7） |
| Trae 工程是否匹配（防改错项目） | `trae-status.ps1` 读 `%APPDATA%\Trae CN\User\globalStorage\storage.json` 的 `windowsState.lastActiveWindow.folder`，与 `-Workspace` 规范化比对；`-RequireMatch` 不匹配 exit 1；`60-handoff.md` 步骤 1 设为硬门 | 本机 `lastActiveWindow` = `<前端仓库>`；用该路径实测应 MATCH，用其它工程应 MISMATCH（本轮实测见回复） |
| 专家编排是否有问题模板 | `templates/intake-questions.md`（可粘贴 6 问 + 追问规则 + 默认/降级 + 反模式）；`05-intake.md` 声明「非全自动：不答则进 D-ID 并暂停依赖步骤」 | 模板已落盘；无自动反问（需 Agent 按模板提问） |
| 设计驱动交接真实项目实测 | `templates/design-handoff-smoke.md`（准备→交接前→实现→验收→结论回写 + 判定标准）；`scripts/handoff-smoke.ps1`（临时工程链路冒烟） | smoke 脚本本轮实测；**真实工程实测待明日**（未实测） |
| 浏览器是否只是权限问题 | `scripts/visual-qa-check.ps1`：探测 Chrome headless 并抽样像素；失败 exit 2 并显式提示 A（切全权限）/B（用户截图）/C（标未实测）；`50-design-team.md §3` 有话术模板 | 2026-11-13 实测：正常探测 exit 0、PNG 9,808 B、像素(16,32,48) 与预期一致；`-SimulateBlocked` exit 2 正确打印三路径提示；指定不存在 Chrome exit 1 |
| 独立评审是否需要修改 | v2.0.1 已由独立 Reviewer 复验 PASS（2 P0 + 4 P1 闭环）；v2.1.0 复验 6/6 PASS（P2 已修） | 已复验（见会话记录） |

## 8. 三域 grill 与 grill-me 的关系

- `grill-me` 是访谈式工具 skill；本 skill 提供**域清单 + 记录模板**：设计（界面+交互，`templates/grill-design.md`）、需求（`grill-requirement.md`）、测试（`grill-testing.md`）。
- 使用顺序：先加载 `grill-me`（若可用）→ 按 `75-grill.md` 对应域逐条问 → 填对应模板 → `loop-gate -RequireGrill` 硬门检查 `grill-*.md`。
- 工具不在 catalog 时，用同一清单自问并注明「未使用访谈式工具」，结论仍有效。
- 商店比对的实测时间线：`skill-status.ps1` 的商店优先逻辑于 **v2.1.0 引入**，并在同版本发布前用伪 `latestVersion` 做过单测（不是 v2.0.1 之前）。
