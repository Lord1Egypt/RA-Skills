# Grill 记录 · 设计/实现域 — P2 运行中心（面板动作 + 命令通道 / 2026-11-19）

> 依据 `references/75-grill.md`。自问 + 实测，记录会被打回的问题；未解决项进 D-ID。
> 实现者：本会话（lead）；**终门 PASS 需非实现者复核，本表不自判 PASS**。

## 1. 对象

| 项 | 内容 |
|---|---|
| 页面/模块 | 侧边栏「能力闭环」→ 运行中心（门禁/体检/交接体检/预检/打包/视觉探测/版本检查/影子计数）+ 三段档位 |
| 代码 | `plugins/capability-loop/{client.js,actions.js,index.js}` |
| 设计依据 | `docs/design/2026-11-18-capability-loop-panel.md` §4.5（运行中心）、`docs/design/design-context.md` D6 |
| 状态源 | `.dsh/loop/state.json`（脚本唯一写入） |
| 评审人（不得是实现者） | 待指派；本表为自问，Lead 终门需他人复核 |

## 2. 十二问

| # | 攻击问题 | 答案/结论 | 证据 | 打回？ |
|---|---|---|---|---|
| D1 | 关键动作是否清楚？ | 门禁是主按钮（primary），危险/写操作（打包、切档位）都进确认框；档位在头部 | 面板「运行中心」3 行；`client.test.mjs` 动作按钮用例 | 否 |
| D2 | 空/加载/失败/部分失败/超长？ | 无会话 → 动作禁用并说明；命令未受理 / 通道失败 / 脚本 FAIL / 输出超长（尾部 40 行）分别有文案 | 夹具：未受理、无 commands、FAIL、取消 | 否（首版曾只有「失败」一种文案 → 已拆） |
| D3 | 375/768/1440 与触控？ | 行动区 `flexWrap`，输入最小 90px；**未实测** 375/768 真机排版 | 无截图（当前无桌面窗口） | **是（P1，未解决 D-01）** |
| D4 | 暗色/对比度？ | 只用主题 token（`--dsw-alias-*`），未新增色值；确认框遮罩 rgba(.42) | 代码；旧版截图 `panel-*-dark.png` | 否 |
| D5 | 键盘/focus/ESC？ | 确认框没有 focus trap / ESC 关闭；按钮可用 Tab 到达 | 代码审查 | **是（P2，未解决 D-02）** |
| D6 | 与现有组件库/主题一致？ | 复用 v2.12.0 的 token 与卡片/徽标；新增 input/seg/pre 样式都基于既有 token | `client.js` S 表 | 否 |
| D7 | 数字/时间/单位一致？ | 结果区耗时 0.1s 精度、时间 `YYYY-MM-DD HH:mm`；门禁 exit 原样显示 | `stampNow` / ResultPanel | 否 |
| D8 | 图表误导？ | 无图表 | — | 否 |
| D9 | 危险操作确认/撤销/审计？ | 全部动作先确认；`mode`/`pack` 明确写「会写什么」；取消用 AbortSignal 中止子进程；运行结果留在面板 | `client.test.mjs` 确认/取消用例；`actions.test.mjs` abort | 否（首版取消只改 UI、不中止子进程 → 已打回修正） |
| D10 | 文案可执行？ | 每条说明「跑什么/影响什么/失败怎么办」；未受理提示直接给「重启应用」 | 面板文案 | 否 |
| D11 | 性能/抖动？ | 单动作串行（有 running 态）；输出截断；无轮询 | — | 否 |
| D12 | 能否用现有组件实现？ | 全部用基础元素 + 主题 token；命令通道复用 DSH `commands` 服务，没有自造 Remote | `dsh-doc/references/user-actions.md` | 否 |

## 3. 打回与修正

| # | 打回项 | 根因 | 修正 | 证据 |
|---|---|---|---|---|
| R1 | 夹具全红（takeover/fallback 11 条） | 临时沙箱只拷 `index.js`，新 `actions.js` 没拷 | 两个夹具补拷 `actions.js` | `node <file>` → takeover 13/13、fallback 1/1 |
| R2 | 「取消运行」是假取消 | `executeAction` 只检查信号，没有把 signal 传进 `spawn` | `runSpawn` 合并 AbortController，abort 一并中止子进程；夹具断言 signal 已 abort | `actions.test.mjs` 17/17；`client.test.mjs` 取消用例 |
| R3 | client 夹具 5 条 ReferenceError | vm 沙箱没有 `AbortController` | 沙箱显式注入 | client 15/15 |
| R4 | 面板 patch 后语法错（样式块多一个 `}`、`PanelIcon` 头重复） | 大段替换脚本锚点不严 | 修正脚本按插入块长度截断旧函数体；`node --check` 卡口 | `node --check client.js` → 0 |
| R5 | 弹窗在真机上「糊在页面上」：遮罩太淡、面板背景在这套玻璃皮肤下不透视也像透视、标题不抢眼（用户截图） | 只用单个 alias 背景（皮肤里可能是半透明）；遮罩 42% 偏轻；z-index 200 偏低 | 遮罩改 `bg-mask-3` + 4px 模糊 + z-index 9999；弹窗改「主题色叠静态深色底」两层背景 + 24px 模糊 + 双层阴影；加顶部色条/页脚分隔线/更大按钮 | `node --check` 0；client 15/15；**真机视觉复验待用户刷新后点一次**（前台被其他应用占用，自动点击会打到前台，未做） |
| R6 | 阻断/门禁看不出属于哪个工程；多工程时不确定切换是否换内容（用户反馈） | 工程名只在页头副标题出现一次；卡片标题无归属；切换只改索引、用的是载入时的快照 | 工程条（下拉 + 路径 + 数量）；四张卡片统一工程名 chip；切换时 `setSelected + load()` 重读 | client 16/16（卡头归属、切换后重读、旧阻断消失） |
| R7 | 自查：中文/空格 taskDir 被静默丢弃；无会话 cwd 回退应用目录会跑错工程；门禁空 taskDir 只回 WARN；动作后工程重排导致选中跳；取消后迟到结果覆盖；PS 脚本缺 BOM（本轮真复现） | `safeToken` 限 ASCII；`cwdOf` 回退 `process.cwd()`；面板没校验 taskDir；选中用索引；取消只清空 controller；编辑剥掉 BOM | `safePath`+引号解析；handler 无 cwd 明确报错；门禁禁用+env 动作；按路径选中并持久化；settle 归属判断；审计/打包新增 BOM 硬门 | actions 21、client 18、takeover 14、fallback 1（54/54）；中文+空格路径真机 PASS；package BOM 10/10 |
| R8 | 可达性缺口：确认框无 ESC/焦点陷阱（D5 一直挂）；结果只能看不能带走（命令/输出不可复制） | 组件无 hooks 设计导致没做键盘逻辑；没有复制入口 | 页级 useEffect：Esc 关闭 + Tab 循环 + 初始焦点；复制按钮（Clipboard API + 降级 + 已复制反馈）；React 桩支持 deps 以测 Esc | client 21/21（含 Esc、复制命令/输出）；`node --check` 0 |
| R9 | 768 宽截图：KPI 4 列压扁、阻断文字挤成一段；请求 375 实际只到 536（桌面壳 minWidth） | 固定 4 列 KPI / 112px 标签 / 40px padding；Electron 窗口最小宽度 536 | `<820px` 紧凑排版（KPI 2 列、标签 72、padding 18/16、卡头换行、阻断 KPI 只显示首条）；截图脚本打印**实际**尺寸并标注 375 需 Web UI | `panel-768.png` 真机截图；`panel-375.png` 实际 536×900；client 21/21 |

## 4. 结论

- 必须修改（P0）：R1–R4 已修。
- 可排期（P1/P2）：D3 响应式截图、D5 键盘/ESC。
- 未解决 D-ID：
  - **D-01（P1）**：面板 375/768/1440 真机截图缺失（当前环境无可见桌面窗口；补测：打开 GUI → 侧边栏能力闭环 → 截图）。
  - **D-02（P2）**：确认框无 focus trap/ESC。
- 判定：**有条件交付**（代码与夹具可交付；真机点击与视觉验收待重启应用后补）。
- 修正证据：`node <file>` 46/46；`node --check` 三文件 0；`loop-gate -Environment` PASS；`on` 档注入真机实测。

## 5. 复核

| 角色 | 结论 | 日期 |
|---|---|---|
| 实现者（自问） | 有条件交付；R1–R4 已修 | 2026-11-19 |
| Reviewer（待指派，不得是实现者） | 待复核 | — |
