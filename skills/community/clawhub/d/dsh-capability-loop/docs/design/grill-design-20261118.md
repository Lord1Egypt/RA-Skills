# Grill 记录 · 设计域（界面 + 交互）— 能力闭环面板 / 2026-11-18

> 依据 `references/75-grill.md` §2。先核 `design-context.md`，再逐条逼问。
> 记录要求：问题具体、答案有证据、至少 1 个打回并修正；未解决项进 D-ID。
> **评审独立性声明**：本轮为**设计者自问**（lead）；实现者尚未指定，独立 Reviewer/Lead 复核待补。按 `75-grill.md` §1.4，自问记录不得单独作为 PASS 依据。

## 1. 对象

| 项 | 内容 |
|---|---|
| 页面/模块 | Harness Web GUI · 全局主面板「能力闭环」v0.1 → **v0.2（7 Tab 全量控制台）** |
| 设计稿/原型路径 | `docs/design/panel-mockup.html`（7 Tab × 4 态 × 明暗）；预览 `panel-overview-dark.png`、`panel-project-dark.png`、`panel-health-dark.png`、`panel-skills-dark.png`、`panel-handoff-dark.png`、`panel-memory-dark.png`、`panel-runs-dark.png`、`panel-shadow-dark.png`、`panel-overview-light.png`、`panel-empty-dark.png`、`panel-error-dark.png` |
| design-context.md | `docs/design/design-context.md`（PARTIAL，缺 Plugins 页运行截图） |
| 评审人（不得是实现者） | lead（自问）；独立复核待补 |
| 工具 | 本清单（`grill-me` 不在本会话 catalog） |

## 2. 十二问

| # | 攻击问题 | 答案/结论 | 证据 | 打回？ |
|---|---|---|---|---|
| D1 | 层级/主次/关键动作是否清楚？ | 页头（身份+开关）→ 4 指标（先看状态）→ 阶段轨道（看进度）→ 本阶段出口（看缺什么）→ 门禁清单（看证据）；唯一主行动「复制命令」固定在右栏「下一步」。主按钮 `rgb(65,118,230)` 白字，次按钮描边，不同权重。 | `panel-overview-dark.png` | 否 |
| D2 | 空/加载/失败/部分失败/超长？ | 空态（未接管）、失败（JSON 坏）已出图；**部分失败**（gate 已跑但证据文件读不到）未单独出图；**加载骨架**只在文档描述。 | mockup 四态；`2026-11-18-capability-loop-panel.md` §4.4 | 是（P1，见 D-06） |
| D3 | 375/768/1440 与触控尺寸？ | 1440 已出图（1440×900）；1024/768/375 未渲染（设计规则已写：≥1280 双栏、1024–1279 单栏、768–1023 指标 2×2、<768 轨道纵向）。门禁行当前 38px，**低于 44px 触控目标**（桌面鼠标可用，触屏不达标）。 | mockup；§4.6 | 是（P1，见 D-05） |
| D4 | 暗色/对比度 ≥4.5:1？ | 暗/亮各出图。**发现真实缺陷**：初版 PASS/WARN/FAIL 徽标文字直接用 `state-success/warn/error` 色，绿色 `#22C55E` 与琥珀 `#F59E0B` 在白底上约 2.1–2.3:1，**不达 4.5:1**。已改为：徽标文字用 `label-primary`，语义色只放在 5px 圆点与 10% 底色上；颜色不再是唯一信息载体（同时有 PASS/WARN/FAIL 文字）。 | 修正前失败值按 token 手算；修正后见 `panel-overview-light.png` 徽标区 | **是（P0，已修正）** |
| D5 | 键盘/focus/ESC？ | 设计写了 focus ring 2px + `aria-expanded` + Esc 还焦；**mockup 未画 focus 态、未做键盘实测**。 | §4.7 | 未解决，D-06 |
| D6 | 与现有组件库/主题一致？差异说明？ | 颜色/圆角/阴影/字体全部取自 `design-platform.css`、`base.css`；页宽 960、页头 28px、Tab 34px 沿用 Plugins 页。新增 stepper、KPI 块两处已登记差异（D1/D2）。不自造色值、不引入组件库。 | `design-context.md` §3、§6 | 否 |
| D7 | 数字精度/单位/时区/排序统一？ | 计数用「项/次/字」；时间用相对时间 + 具体时刻（今天 14:02 / 昨天 16:40 / 前天 09:00），同一页不混用 UTC；百分比 67% 与「样本 9 次」同屏。注入量写「1,412 字符」不写 token 估数。 | mockup 指标区、脚注 | 否 |
| D8 | 图表是否误导？ | 只有 6 格结果信号条（3 绿/1 琥珀/1 红/1 未运行），无坐标轴、无缺失值当 0；未运行用虚线而不是绿色。 | `panel-overview-dark.png` 门禁 KPI | 否 |
| D9 | 危险操作确认/撤销/审计？ | 「关闭」会停止注入与阻断，属危险操作：设计稿要求二次确认（说明后果：不再自动接管，已有 state 保留）。**mockup 未画确认弹窗**。 | §4.3 H 行 | 是（P2，见 D-07） |
| D10 | 文案可执行（谁/做什么/后果）？ | **打回**：空态原第二个按钮「打开状态文件」在未接管时**没有文件可打开**，是死动作。已改为「查看接入示例」，并在下方给出「跑 05-intake 六问」的可执行路径。 | 修正前 `panel-empty-dark.png` 旧版；修正后同名新图 | **是（P0，已修正）** |
| D11 | 性能：骨架/大列表/抖动？ | 打开读一次 + 无轮询（P2 才上 watch）；门禁最多 7 行，无虚拟列表需求；展开是局部重排，不做整页跳动。**骨架未出图**。 | §4.8 | 未解决，D-06 |
| D12 | 能否用现有组件实现（不引入新 UI 体系）？ | 纯 div/CSS + `sidebar.panellist` + `main` slot；图标为 16px 自绘 SVG；无 iframe、无第三方组件库。stepper 是 CSS 网格，不是新组件包。 | mockup 源码；`design-context.md` §2 | 否 |

## 3. 结论

- **必须修改（P0，已关闭）**：
  1. D4 徽标对比度：文字改 `label-primary`，语义色只做圆点/底色；已重渲染 5 张预览。
  2. D10 空态死动作：`打开状态文件` → `查看接入示例`；已重渲染 `panel-empty-dark.png`。
- **可排期（P1）**：D2 部分失败态与骨架、D3 触控目标（<768 时行高 44px + 三档截图）、D5 focus 态、D11 骨架。
- **可排期（P2）**：D9 关闭确认弹窗、P3 动作执行。
- **未解决 D-ID**：
  - D-05 375/768/1024 三档真实渲染（owner：实现者，P2 验收前）
  - D-06 加载/部分失败/focus 三态出图（owner：设计者，P1 出稿前）
  - D-07 关闭档位确认弹窗文案与焦点（owner：设计者，P2 前）
  - D-08 独立 Reviewer 复核本 grill（owner：lead，指派非实现者）
  - D-09 面板读通道在真实会话中的授权与降级（owner：实现者，P2 前）
- **修正证据**：mockup 两个 P0 修正均落在 `docs/design/panel-mockup.html`；重渲染命令见下；预览图 sha256 变化可复核。
- **判定**：**有条件交付（设计评审用）**。作为设计稿可评审；进入实现前必须先关 D-05/D-06，并补独立复核。不得据此宣称「设计已通过」。

## 4. 复核

| 角色 | 结论 | 日期 |
|---|---|---|
| Designer（lead，自问） | 有条件交付；2 个 P0 已修 | 2026-11-18 |
| Reviewer（待指派，不得是实现者） | 待复核 | — |

## 5. 评审后修正（2026-11-18 晚）

- **读通道**：原设计 `capabilityLoop.status` 自定义 Remote → 经 `dsh-api-remotes` README §Known Limitations 核实**不可行**（capability set 由构建期显式 import 固定，Client 不发现运行时新增 Remote）。改为现有 `workspaceFiles.read(sessionId, '.dsh/loop/state.json')`；P3 动作走 `commands.execute`。影响：面板需要当前会话授权，无会话时显示空态（D-09）。
- **交付判定不变**：仍为「有条件交付」；该修正在设计稿 §3 架构图与 §4.8 已同步。

## 6. 复跑方式

```powershell
# 渲染一个 Tab（本机 Chrome headless；路径含空格需引号）
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --disable-gpu --hide-scrollbars `
  --window-size=1440,900 --virtual-time-budget=2500 `
  --screenshot "docs\design\panel-overview-dark.png" `
  "file:///<repo>/docs/design/panel-mockup.html#shot=1&state=ready&view=overview&theme=dark"
# 其余：view=project/health/skills/handoff/memory/runs；state=shadow/empty/error；theme=light
```

## 7. v0.2 复审（2026-11-18 晚，按用户反馈重做）

> 用户反馈：「面板的功能对当前 skill 并没有全量容纳，只是突出了项目进度」；「影子是什么模式看不到」；面板位置/动作/状态目录已确认。

| # | 攻击问题 | 答案/结论 | 证据 | 打回？ |
|---|---|---|---|---|
| V1 | 「全量容纳」是真全量还是换个说法的进度页？ | 初版只有项目进度，**确是缺项**。v0.2 增加 §4.2 **32 行能力覆盖矩阵**（接入/阶段 9、体检/运行时 4、技能/插件 5、交接/交付 8、记忆/迭代/运行 6），并落成 7 Tab；每行给「面板位置 + 数据源 + 状态口径」。 | 设计稿 §4.2；mockup 7 个 Tab | **是（P0，已修正）** |
| V2 | 32 项能力会不会变成信息过载？ | 总览只放 12 张能力卡 + 下钻；每 Tab 首屏 ≤5 块；7 Tab 横向可滚。能力地图是唯一「全量」视图，其余是分区细节。 | `panel-overview-dark.png`；设计稿 §4.3 | 否（P1 观察） |
| V3 | 影子模式「看不到是什么」——它到底做什么、和关闭/接管差在哪？ | 初版只有一句档位名，**不可判定**。v0.2 给 **8 维对照表**（注入/约束/面板/门禁后果/切换）+ 独立 banner + KPI「影子 shadow · 未阻断 1 次」+ **首启 3 会话观察期** + 「升级为接管」动作。 | 设计稿 §3.1；`panel-shadow-dark.png` | **是（P0，已修正）** |
| V4 | 「一步到位跑门禁」= 面板能 exec 任意命令吗？ | 初版只写「可运行」，**没有白名单/确认/超时/取消/写回**。v0.2 给 7 个白名单动作、参数校验、「将写」清单、确认弹窗、输出尾部、取消进程树、串行限制、`allowRun` 开关。 | 设计稿 §4.5；`panel-runs-dark.png` | **是（P0，已修正）** |
| V5 | 7 个 Tab 在 960/768 会不会溢出？ | 960 下 7×4 字可容纳（mockup 实测 1440 外壳）；更窄横向滚动。未在 768/375 实测。 | 设计稿 §4.1/§4.7 | 未解决（D-10） |
| V6 | 读状态需要会话，全局页没有会话怎么办？ | 已确认不能自造 Remote；`workspaceFiles` 需要 sessionId。无会话显示「先打开一个会话」空态，不伪造数据。 | 设计稿 §4.9；`dsh-api-workspace-files` README | 未解决（D-09） |
| V7 | 运行结果会不会和命令行不一致？ | 设计规则：面板动作与工具调用同一个 Host 方法；输出/exit/写回同一份；P2 逐动作对比验收。 | 设计稿 §4.5/§5 | 未实测（D-10） |
| V8 | 版本落后（装 2.9.5 / 源 2.9.6）面板会怎样？ | 只读 + 「落后 1 个 PATCH，按商店更新」；不自动覆盖。 | `panel-skills-dark.png` | 否 |

**v0.2 结论**：3 个 P0 打回并修正（V1 全量覆盖、V3 影子可见、V4 运行安全）。新增 D-ID：

- D-09 读通道授权/无会话空态（实现者，P2 前）
- D-10 7 Tab 在 375/768/1024 的真实渲染 + 运行中心逐动作对账（实现者，P2 验收前）
- D-11 32 行能力矩阵的完整性由 skill 维护者复核（lead，P1 前）
- D-12 独立 Reviewer 复核 v0.2（lead，指派非实现者）

**判定**：仍为**有条件交付（设计评审用）**；不得据此宣称「设计已通过」。

## 8. 设计者自审（2026-11-18 晚，v0.2 定稿后）

见 [review-20261118-self.md](review-20261118-self.md)。要点：

- **P0 4 项已修**：副标题「只读状态」与可跑门禁矛盾；门禁 KPI 计数与 6 行列表不一致；guard 状态恒绿（异常/未接管也显示运行中）；960/1000 页宽不一致。
- **P1 7 项已在 v0.3 收敛**：总览 6 卡 + 32 项抽屉；门禁合并为一个列表；单一主「运行门禁」；补确认模态；Tab 12px/去常量计数；L3 标「仅复制」；异常态禁用档位（见 review §7）。
- **P2 剩余打磨**：当前阶段强调色、记忆返工趋势、活动补到 6 条；不影响进入 P2 实现门。
- **结构判定**：v0.3 可进入 P2 实现；仍需 375/768/1024 真机截图与独立 Reviewer（D-12 仍开放）。
- 自审不替代独立 Reviewer。


