# CHANGELOG — dsh-capability-loop

> **v2.4.0–v2.7.0 归属说明**：这几版记录的是**交接自动化**（`feature-handoff` 的 `send-to-trae-prompt.ps1` / `trae-cdp.mjs`）联调过程；**脚本本体在 `feature-handoff/scripts/`，不在本 skill**，本 skill 只同步 `references/60-handoff.md` 接线文档与版本号。合入时保留原版本编号以保持追溯（按本 skill semver，这类文档同步本应记 PATCH）。以下各条的实测证据均来自该联调会话；v2.7.0 对齐只做文档/版本整理，**未复跑窗口/GUI 操作**，未实测标注保持不变。

## v2.15.0 — 2026-11-19（按 ClawHub 安全审计整改：权限声明 + 干净打包 + 删除边界）

**审计来源**：<https://clawhub.ai/linboomboom/skills/dsh-capability-loop/security-audit>（审计对象是 v2.9.5，共 20 条发现；本版逐条处理，清单见 `SECURITY.md` §5）。

**安全修复**
1. `handoff-smoke.ps1` 不再清空调用方传入的 `-Scratch`：每次创建唯一子目录 `run-<时间戳>-<随机>`，读写与清理只针对该子目录（对应两条 High 的「递归删除调用方目录」）。
2. `visual-qa-check.ps1` 不再自称只读：注释改成「会写探测 HTML/PNG 与临时 Chrome profile」；新增输出目录边界（只允许工作区或 `%TEMP%` 下，`-AllowOutsideOutDir` 显式放行）；只删除自己创建的临时 profile。
3. `package-skill.ps1`：打包排除 `memory/`（个人偏好）、图片/压缩包/私钥、插件夹具；疑似凭证命中从 WARN 改为 **FAIL 阻断**；生成的 PUBLISH-NOTES 改为如实列出排除项与「启发式扫描 + 人工复核」，不再声称「已排除全部敏感材料」。
4. 新增 `SECURITY.md`：读/写/子进程/网络/记忆/删除边界，以及 20 条审计发现的逐条处置与解释。
5. `SKILL.md` frontmatter 增加 `allowed-tools`；正文新增「权限与数据边界」小节。
6. 偏好记忆加隐私护栏：`references/85-ux-memory.md` 要求写入前告知、只记明确偏好、禁记敏感信息、给出删除流程；`memory/user-profile.md` 顶部加隐私提示。
7. 插件卸载步骤提示先备份持久化数据；`references/95-store-publish.md` 声明运行时不联网、发布**打包目录**而不是源码仓库根；playbook 注明浏览器环境变量只对当前进程生效。

**行为变更（非破坏接口）**
- 冒烟脚本产物改为 `<Scratch>/run-<时间戳>-<随机>`；`-Keep` 保留这个子目录，不再保留/删除整个 `-Scratch`。
- 打包产物不再包含 `docs` 图片、插件测试夹具与 `memory/`（条目数会明显下降）。

**验证**
- 夹具 **57/57**；`node --check` 0。
- 打包：排除项生效、凭证扫描正例/反例；条目数记录在发布日志。
- 冒烟：传入含哨兵文件的 `-Scratch`，运行后哨兵仍在、只新增/清理 run 子目录。
- 发布：从干净包目录发布 2.15.0，附带 `--clawscan-note` 说明本地脚本/写入边界/无运行时联网。

**回滚**：`git revert` 本提交；旧版仍可只读使用。

## v2.14.3 — 2026-11-19（真机截图归档：窗口宽 1296 / 768 / 最小 536 像素）

**内容**（无代码变更）
- 面板 v2.14.2 真机截图三张，归档到 `docs/design/`：
  - `panel-1296.png`：窗口宽度 1296 像素（常规桌面）；
  - `panel-768.png`：窗口宽度 768 像素（平板宽度，紧凑排版：指标两列、标签收窄）；
  - `panel-536.png`：窗口最小宽度 536 像素（桌面窗口下限；页面仍可用，动作区按行换行）。
- **375 像素（手机宽度）桌面做不到**：桌面程序窗口下限是 536 像素；需要 375 像素只能用浏览器打开 Web UI 做设备模拟。
- 截图方式：`scripts/ui-shot.ps1` 只 `MoveWindow` + `PrintWindow`，**不注入键盘/鼠标**，截完恢复原尺寸与位置；截图前确认 Harness 在前台（点侧边栏打开面板那一下仍是手动）。

**验证**
- 面板标题确认加载到 v2.14.2（标题下「面板 v2.14.2」）。
- 夹具 57/57；本提交不含代码改动。

**回滚**：删除三张截图即可。

## v2.14.2 — 2026-11-19（面板自报版本 + 澄清桌面版的“刷新”）

**起因**：用户反馈在 Harness 桌面版按 Ctrl+R 没反应，且不知道面板加载的是不是最新代码。

**事实（已核桌面壳源码）**
- 桌面正式版**没有 Ctrl+R 绑定**，也**没有「刷新页面」菜单**：`app.asar/lib/main.js` 里 `reloadPageMenu` 与 `role: "reload"` 只在 `development` 为真时加入菜单。
- 生产版可用：F12（注册了 `toggleDevTools`）→ Console 执行 `location.reload()`；或退出应用重开；或本地 link 安装下等 HMR 后重新点侧边栏。

**改动**
- 面板标题下新增「**面板 v2.14.2**」——版本号没变就说明渲染器仍是旧 `client.js`。
- 插件 README 增加「改了 `client.js` 怎么生效」三条路径与判断方法。
- 新建 `memory/user-profile.md`：记录「不要用代号，要写清楚是什么」等交付偏好（同时补齐体检里一直缺的偏好记忆）。

**验证**
- `node --check` 0；client 夹具 21/21（新增版本号不影响断言）。
- `package-skill` 通过（含 memory/ 新增文件）。

**回滚**：`git revert` 本提交。

## v2.14.1 — 2026-11-19（窄窗口紧凑排版 + 桌面壳最小宽度约束）

**真机截图暴露的问题**
- 桌面窗口 768 宽：KPI 4 列被压扁、阻断文字挤成一大段。
- 桌面壳最小宽度是 **536px**（Electron `minWidth`）：请求 375 时 `MoveWindow` 实际只到 536，**桌面版无法截 375**（375 只能走 Web UI/浏览器）。

**修法**
- `<820px` 进入紧凑排版：KPI 改 2 列、动作区标签 112→72px、页面 padding 22/40→18/16、工程条与卡片头允许换行。
- 阻断 KPI 只显示首条阻断 + 「等 N 项」，避免整段文字撑高。

**验证**
- `node --check` 0；client 夹具 21/21。
- 真机 `ui-shot.ps1`：768×900 成功；请求 375 时实际 536×900（已记录在输出里，脚本会打印实际尺寸）。
- 截图产物：`docs/design/panel-768.png`、`docs/design/panel-375.png`（实际 536 宽，文件名保留请求宽度以便对照）。

**回滚**：`git revert` 本提交（仅样式，无行为变更）。

## v2.14.0 — 2026-11-19（确认框可达性 + 复制 + 双工程接入）

**新增（面板可达性 / 效率）**
- 确认框键盘可达：`Esc` 关闭、`Tab` 在弹窗内循环（焦点陷阱）、打开时焦点自动落到「确认运行」、`aria-labelledby` 指向标题。
- 复制：确认框可复制**完整命令**；结果区可复制**输出**或**命令**；优先 Clipboard API，失败降级 `execCommand`，1.5s 内显示「已复制」/「复制失败」。
- 夹具新增 3 条（Esc 关闭、复制命令、复制输出/命令），React 桩升级为支持 `useEffect` 依赖变化（因此 Esc 可被夹具驱动）。

**接入**
- 「气量平衡月表（管存+罐存）」已执行 `loop-state.ps1 -Action init`（shadow / INTAKE），生成 `.dsh/loop/{project,state}.json` + `.gitignore`。面板现在应列出两个工程，切换按路径记忆；多工程数据路径由 client 夹具覆盖（切换后重读、卡头归属、旧阻断消失）。

**验证**
- 夹具 **57/57**：actions 21 + client 21 + takeover 14 + fallback 1；`node --check` 0。
- `package-skill` → 78 条目、10 脚本 BOM 全 PASS、WARN=0。
- **375/768 真机截图未完成**：当前前台是其他应用，自动点击/按键会打进前台窗口；新增 `scripts/ui-shot.ps1` 只做 resize + PrintWindow（不注入输入），待面板打开后执行。
- 双工程面板真机截图同样待面板打开。

**回滚**：`git revert` 本提交；接入的第二工程可删 `.dsh/loop` 回退。

## v2.13.3 — 2026-11-19（一轮自查：修 6 个真问题 + 4 处体验）

**修的真问题**
1. `taskDir` 含中文/空格时被 `safeToken` 静默丢弃（「气量平衡月表」这类中文目录跑不了门禁/预检）→ 改 `safePath`（允许中文/空格，仍禁 `..` 与开头 `-`）+ 命令值引号解析。
2. `resolveSkillDir` 返回配置原值（可能是相对路径）→ 子进程按错误 cwd 解析脚本；改为返回解析后的绝对路径。
3. 命令 handler 拿不到会话 `cwd` 时回退 `process.cwd()`（应用目录）——会把门禁/打包跑错工程；改为明确报错并提示填 `workspaceRoot`。
4. 门禁没填 `taskDir` 时仍会发命令 → loop-gate 只回「没有可执行的门禁」，像坏了；改为禁用运行键 + 提示，并新增「环境验收」（`run env`）。
5. 动作完成后的 `load()` 可能重排工程列表，按索引选中的工程会跳；改按**工程路径**选中并持久化（刷新回到上次看的工程）。
6. 取消后迟到的命令结果会覆盖「已取消」；`settle` 增加 controller 归属判断后再写结果。

**体验**
- 最近一次运行 / 正在运行 卡片带工程名 chip；确认框显示「名称（路径）」。
- `taskDir` **按工程记忆**（localStorage），切换工程不会带错目录；门禁行支持回车直接弹确认。
- 当前档位按钮禁用（不再弹出“切到当前档位”）；头部「只读」改为「状态只读 · 动作走会话命令」。
- 长阻断文本自动换行，不再挤掉 owner/due；`taskDir` 为空时按钮旁直接给黄色提示。

**工程护栏**
- `capability-audit.ps1` / `package-skill.ps1` 新增 **PowerShell BOM 检查**：`scripts/*.ps1` 缺 UTF-8 BOM 直接 FAIL（PS 5.1 读无 BOM 中文会乱码到脚本解析失败——本轮自查时就复现了一次）。首次运行即抓出 `ui-probe-live.ps1` 缺 BOM，已补。

**验证**
- `node --check`（client / actions / index）→ 0。
- 夹具 **54/54**：actions 21 + client 18 + takeover 14 + fallback 1。
- 真机 `loop-gate -TaskDir "能力 闭环-任务目录"`（中文+空格路径）→ PASS，证明 argv/引号链路可用。
- `package-skill` → 78 条目、10 个脚本 BOM 全 PASS、WARN=0。
- 真机视觉/点击复验仍未做（前台被其他应用占用，未做 UI 自动化）。

**回滚**：`git revert` 本提交。

## v2.13.2 — 2026-11-19（工程归属：每张卡片都标工程名，切换即重读）

**反馈**（用户）：阻断项有了，但看不出是哪个工程的；多个工程切换时内容会不会跟着换？

**修法**
- 新增**工程条**（标题下第一行）：`工程 [下拉] <工程根路径> · 已接入工程 N 个 / 只列已接入工程`；单工程时下拉禁用但仍显示名称与路径。
- 四张卡片（运行中心 / 阶段 / 门禁与证据 / 阻断与下一步）标题后统一加**工程名 chip**，任何一段单独截图都能看出归属。
- 切换工程时 `setSelected + load()`：重读该工程的 `project.json`/`state.json` 再渲染（原来只切索引、用载入时的快照）。
- 面板只列**已接入**工程（有 `.dsh/loop/project.json`）；未接入的工程跑 `loop-state.ps1 -Action init` 后出现。

**验证**
- `node --check client.js` → 0；`client.test.mjs` → **16/16**（新增：卡头带工程名、多工程切换后重读且内容跟着换、切走后旧阻断消失）。
- 真机视觉复验仍待用户刷新后确认（前台被其他应用占用，未做 UI 自动化）。

**回滚**：`git revert` 本提交。

## v2.13.1 — 2026-11-19（弹窗可读性修复：玻璃皮肤下半透明）

**现象**（用户真机截图）：面板「确认运行」弹窗与背后的运行中心糊在一起——遮罩太淡、面板背景在这套玻璃皮肤下不显实、标题不够抢眼。

**修法**
- 遮罩：`--dsw-alias-bg-mask-3`（48% 黑）+ `backdrop-filter: blur(4px)`，`z-index` 200 → 9999。
- 弹窗面：**两层背景**——主题 `bg-base` 叠在静态深色底（`--dsw-static-neutral-bluish-950`）上；即使皮肤把 alias 调成半透明，也不会透视到下面的文字。再加 24px 模糊、双层阴影、`border-l3` 描边。
- 结构：顶部 3px 品牌色条、标题 16px、命令块加边框与静态底、页脚分隔线、按钮加大到 88/96px。
- 说明文字（工程/命令/后果）统一 12px 行高 1.6。

**验证**
- `node --check client.js` → 0；`client.test.mjs` → 15/15（确认框、取消、未受理等断言不变）。
- **真机截图未复验**：当时前台是其他应用（PUBG），自动点击/发送按键会打到前台窗口，故未做 UI 自动化。补测：Ctrl+R 刷新 → 打开「能力闭环」→ 点任一档位/动作 → 应看到实心弹窗与暗遮罩。

**回滚**：`git revert` 本提交，弹窗回到 v2.13.0 的半透明版本。

## v2.13.0 — 2026-11-19（P2 运行中心：面板可跑门禁/体检/切档位）

**起因**：v2.12.0 的面板只能看不能动，用户要「一步到位跑门禁」；上一轮会话在实现中途被 429 限流打断（actions.js/index.js 已写、client 未接、夹具未跑），本版收尾。

**新增 `plugins/capability-loop/actions.js`（Host 运行中心）**
- 白名单 `ACTIONS`：`audit` / `gate` / `handoff-audit` / `preflight` / `pack` / `visual` / `skill-status` / `sync-shadow` / `mode`；kind 决定解释器（powershell/python/状态脚本）。
- 参数逐个校验：`kind` 枚举、`taskDir/slug/handle` 只允许安全 token 且禁 `..`、不拼 shell；`mode` 只接受 on/shadow/off。
- `runSpawn`：`ctx.subprocess` + 动作级超时 + 5s grace + 输出上限；`AbortSignal` 取消一并中止子进程；结果只回尾部 40 行（≤6000 字）。
- `executeAction(ctx, cfg, rawInput, signal)` 返回 `{ ok, text }`，永不抛错（缺 subprocess / 解释器 / spawn 失败都给一句可读原因）。

**修改 `plugins/capability-loop/index.js`**
- `ctx.inject(['commands'])` 注册会话命令 `capability-loop`（描述 + `input.hint`），handler 用 `agent.session.header.cwd`（缺省 `process.cwd()`）作工程根，调用同一 `executeAction`。
- 命令通道 = 面板与命令行的**同一实现**（`dsh-doc/references/user-actions.md`）。

**修改 `plugins/capability-loop/client.js`（面板动作）**
- `inject` 加 `remote.commands`；`collect` 保留每个工程最近会话的 `sessionId` 作动作凭据。
- 头部加三段档位（接管/影子/关闭）；KPI 下加「运行中心」卡片（门禁 kind+taskDir / 交接体检 slug / 模块预检 keyword+alias / 上架打包 handle / 只读动作）。
- 每个动作先弹**确认框**（工程 + 完整命令 + 说明），确认后 `commands.execute`；运行中显示「正在运行 + 取消」；结果区展示状态/耗时/输出尾部；失败与未受理（命令未注册）分别给可操作提示。

**修改 `scripts/capability-audit.ps1`（体检误报修复）**
- 活动 profile 不再硬编码 `profiles/web`：按 desktop → web → 第一个非 default 目录探测；无 `cordis.patch.yml` 时给 WARN（patch 可选）而不是 FAIL。本机只有 `desktop` profile，旧逻辑每次体检都产生一条假 FAIL。

**夹具**
- 新增 `test/actions.test.mjs` 17 条（白名单/argv/拒绝/失败/abort）。
- `test/client.test.mjs` 9 → 15 条（动作按钮、切档位确认→命令调用、未受理、无 commands、取消 abort）。
- `test/takeover.test.mjs` 10 → 13 条（命令注册 descriptor、空输入/未知动作/缺 subprocess、aborted 信号）。
- 修两个夹具的真实回归：临时沙箱只拷 `index.js` 导致 `./actions.js` `ERR_MODULE_NOT_FOUND`；`ctx.inject` 在夹具里缺失。

**验证（本轮实测）**
- 夹具：逐个文件跑 `node <file>` → **46/46 pass**（沙箱里 `node --test <dir>` 会 spawn EPERM）。
- `node --check client.js` / `index.js` / `actions.js` → 0 错误。
- `loop-gate.ps1 -Environment` → PASS（SKIP=1：本仓库无 `upgrade/post-restart-check.ps1`）；`-TaskDir docs/design -Kind design` → PASS（2 PASS / 1 SKIP）。
- **`on` 档真机实测**：`loop-state.ps1 -Action set-mode -Mode on` → exit 0；本工程真实会话的下一步收到完整契约（阶段/硬约束/门禁/阻断/下一步），D-01 关闭。
- **未实测**：面板运行中心的真机点击——Host 命令需重启应用注册，且当前环境无可操作的桌面窗口；见 `docs/design/grill-p2-actions-20261119.md`。

**新增 `scripts/ui-probe-live.ps1`（可选，Windows）**
- 桌面窗口探针：聚焦 → Ctrl+R 刷新渲染器 → 点侧边栏「能力闭环」→ PrintWindow 截图，供面板真机视觉验收；本机 `.tmp` 不可写时默认输出到 `docs/design/`。

**经验写回**：playbook 增 `ERR-20261119-04`（夹具漏拷新模块）、`ERR-20261119-05`（vm 沙箱缺 AbortController / 跨 realm deepEqual）、`ERR-20261119-06`（Host 命令需重启，client 刷新即可）、`ERR-20261119-07`（工作区 `.tmp` ACL 拒绝写入，改放 `%TEMP%` 或 `docs/`）。

**回滚**：`git revert` 本提交；插件旧版仍可只读面板（`client.js` 不含动作即恢复 v2.12.0 行为）。

## v2.12.0 — 2026-11-19（P2 面板 v1：侧边栏「能力闭环」入口）

**起因**：用户装完 P1 后在桌面版找不到入口。P1 只做了 **host 半**（注入），按设计 P2 才有 UI——但那意味着「装了却看不见」。本版补上 client 半，给出可用的面板 v1。

**新增 `plugins/capability-loop/client.js`（client half）**
- 注册两个 slot：`sidebar.panellist`（id `capability-loop`、`order: 20`、label「能力闭环」、环形箭头图标）与 `main`（同名 key = 面板本体）。
- 面板内容（**只读**）：档位徽标（接管/影子/关闭 + 影子观察进度）、当前阶段 + 7 段轨道、门禁列表（状态徽标 / exit / 时间）、阻断清单、下一步 + 命令、状态源路径。
- 三态：加载中 / 未接入（给接入命令）/ 有工程；多工程时给下拉切换。
- **数据通道**：`GET /api/file?path=<绝对路径>`（已认证 `connection.fetch` + `browserPeer`），先读 `~/.dsh/storages/workspace.json` 找已登记工作区，再逐个试 `<ws>/.dsh/loop/project.json` → `state.json`。**不需要会话**，纯读。
- ctx 由 `apply(ctx)` 闭包注入（不猜 slot props 形状），`fail-open`：读不到就显示未接入，不崩。

**新增**
- `plugins/capability-loop/test/client.test.mjs`（7 条）：注册契约（key/id/order/label/icon）、空态、有工程渲染（档位/阶段/门禁计数/阻断/下一步）、shadow 观察进度、home 未知、fetch 抛错不崩。自带极简 React 桩（hooks + 重渲染）。
- `plugins/capability-loop/locale/{en,zh}.json`（Plugins 页标题/描述/详情）、`docs/DETAIL.md`；`package.json` 加 `./client` 导出、`dsh.client`（`platform: web`、`immediately: true`、四个 inject）。

**修改**
- `SKILL.md`：§1 的 P1 描述改为「注入 + 侧边栏只读面板」，夹具数 18/18，并注明设计稿里 7 Tab 完整版是后续；`version` 2.12.0。
- `version.json`：`bundle` 块加 `clientEntry` / `panel`；breaking_changes 补 v2.12.0。
- 技能包版本 2.11.1 → 2.12.0（MINOR：新增 UI 能力，不装则无变化）。

**验证（本轮实测）**
- 夹具：`node --test plugins/capability-loop/` → **20/20 pass**（host 11 + client 9）。
- `node --check client.js` → 0 错误；`package.json` 可解析。
- profile 解析：`dsh-capability-loop-bundle/client`、`/locale/zh.json`、`/package.json` 均能从 profile 解析到工作区文件。
- `set_plugin include:capability-loop` → `application: applied`；`install_bundle` 依赖仍是 link（junction）。
- 技能包：74 条目、WARN=0。
- **真机（桌面版）**：`Ctrl+R` 重载后左侧出现「能力闭环」，点开读到本仓库真实 `state.json`（影子 2/3、GATE 7/7、设计门 PASS、D-01、下一步、skill v2.12.0），「刷新」可重读。截图见 `.tmp/design-evidence/probe-refresh.png`。

**过程中修掉的两个客户端真缺陷（已记入 70-playbook ERR-20261119-03）**
1. **`ctx.connection.fetch` 在浏览器半边不存在**（只有 Host 侧 Connection 有 `fetch(request, peer)`），且桌面渲染器跑在 `dsh-app://` 源上，`globalThis.fetch('/api/file?path=')` 命中不了 HTTP API → 面板一开始只能显示空态。改为 `remote.session.list({})` 取会话（含 `cwd`）+ `remote.workspaceFiles.read(sessionId, 相对路径)`。
2. **`inject` 要用点号键**：只写 `remote` 时访问 `remote.session` 报 `cannot get property "remote.session" without inject`。改为 `['slots','connection','remote','remote.session','remote.workspaceFiles']`。
3. 顺带：面板空态增加「读取诊断：<具体错误>」——把静默空白换成可定位的一句话。

**未实测 / 已知限制**
- **面板需要刷新页面（Ctrl+R）或重启应用才出现**：渲染器的 client 模块图是启动时建的；本机未跑 `pnpm run dev:web`，`client.js` 改动不会热加载。
- `on` 档真实会话的整段契约仍未实测（本仓库是 `shadow`；切 `on` 即验）。
- Web UI 对 `source.kind='capability-loop'` 的渲染样式当普通用户消息；token 计费差异未测。
- 面板文字中文硬编码（未接 locale 字典）；只读，没有「运行门禁 / 切档位」按钮；只列有会话的工作区。
- 面板背景沿用应用壁纸的透底（与对话区一致），未为可读性单独加不透明底。

**回滚**：`git revert`；或卸载插件；面板随插件行关闭一起消失（不影响 skill 侧脚本）。

## v2.11.1 — 2026-11-19（PATCH：修「装了但没生效」的两个真缺陷）

**起因**：按 v2.11.0 的指引实际安装 P1 插件，`install_bundle` 返回 `exitCode=0` 但 `application: failed`，诊断 `ERR_MODULE_NOT_FOUND: Cannot find package '@deepseek-ai/dsh-llm'`——整行没激活。修好后注入正常，但又发现「注入成功、影子日志没记账」。

**修 1：本地目录安装的 bundle 顶层 import dsh 包会整行不激活**
- 根因：本地目录安装走 pnpm **link（junction）**，插件真实路径在工作区；Node 从真实路径向上找 `node_modules`，到不了 profile 的 `node_modules`（dsh 自带包在那里）。只有从 npm/Git 装进 profile 的包才能顶层直接 import。
- 修法：`index.js` 去掉顶层 `import '@deepseek-ai/dsh-llm'`，改**运行时动态解析 + 手工构造兜底**——能解析就用官方 `createUserMessage`，解析不到就按 `dsh-session/src/repair.ts` L168 的同款形状手工 `Object.freeze`。
- 回归：新增 `test/fallback.test.mjs`（沙箱里**不放桩**，强制走兜底），断言仍注入 + 消息形状正确 + 记录降级日志。

**修 2：`ctx.fs.writeText` 未传 per-call 策略时按部署默认 `read-only` 被拒，异常被静默吞掉**
- 根因：`dsh-fs-sandbox` 的 `checkedTarget` 是 `policy = sandboxPolicy ?? ctx.sandboxPolicy.resolve()`；不传就用**部署默认**（fail-safe `read-only`）→ `FS_SANDBOX_DENIED`；插件原实现在 `catch {}` 里静默吞掉，表现为「注入成功但影子日志不增长」。
- 修法：写入时传**本会话自己的**策略 `ctx.sandboxPolicy.resolve({ session })` 作为第 5 参；失败改为 `logger.warn`（不再静默）。只读会话里写入被拒是正确行为——尊重用户沙箱，降级不阻断。
- 证据：修前影子日志只有夹具的 `e2e-1`；修后真机追加 `session-056a88a3-…`，`sync-shadow` 计数 1 → **2/3**。

**文档**
- `references/70-playbook.md` 新增 `ERR-20261119-01`（link 安装 + 顶层 import dsh 包）与 `ERR-20261119-02`（插件写文件静默失败），含根因、修法、验证方式。
- `SKILL.md`：P1 状态改为「已在本机 profile 安装并实测注入成功」；版本 2.11.1。

**验证（本轮实测）**
- `install_bundle` → `application: failed`（复现）；改后 `set_plugin include:capability-loop` → **`application: applied`**。
- 真机会话里收到影子一行提示（86 字符，`mode: shadow`）；影子日志追加当前 session id；`sync-shadow` 显示「已观察 2 / 3 个会话」。
- 夹具：`node --test` → **11/11 pass**（含无桩兜底用例）；`node --check` 0 错误。

**未实测**：`on` 档在真实会话里的整段契约（本仓库当前是 `shadow`；把 `.dsh/loop/state.json` 切 `on` 即可验）；Web UI 对 `source.kind='capability-loop'` 的渲染样式；token 计费差异。

**回滚**：`git revert`；或 `plugin_manager action=remove_bundle target=dsh-capability-loop-bundle`；或 `loop-state.ps1 -Action set-mode -Mode off` 单工程关闭。

## v2.11.0 — 2026-11-18（P1 宿主接管插件：契约自动进首步，不再等模型自觉）

**起因**：v2.10.0 的 P0 是软接管——`AGENTS.md` 链一定注入，但「读 `state.json`」仍靠模型自觉，实测里模型会跳过那次 `read`。要确定性，必须由宿主在首步把契约折进消息。

**新增 `plugins/capability-loop/`（host bundle，不装则行为与 v2.10.0 完全一致）**
- `index.js`：`agent/pre-step` 瀑布钩子，先 `await next()`，再按档位决定是否把契约折进 `decision.messages`（**紧跟本步认领的用户消息之后**，用户原话先出现）。
  - `on`：完整契约 ≤1600 字符（实测约 810），含阶段/本阶段出口/当前门禁/阻断/下一步/状态源路径；
  - `shadow`：一行 ≤140 字符提示，只记录不阻断；并追加 `.dsh/loop/shadow-log.jsonl`（每会话一行）；
  - `off` / 未标记工程：0 注入、0 读写。
- 档位优先级：`project.json.mode` → 被 `state.json.mode` 覆盖 → 缺省 `defaultMode`（`off`）。**安装插件 ≠ 接管所有项目**。
- 纪律：**fail-open**（读/解析/构造任一失败只记日志、不注入）；**幂等**（消息带 `source.kind='capability-loop'` + 内容指纹，同批/会话历史/resume/fork 都判重）；**只读 `state.json`**（唯一写入方仍是脚本）；**不新增 Session 事件类型**（只用普通 `user/message`，会话可正常重开）。
- `cordis.patch.yml`：`insert` 行 + 六个可配键（`defaultMode` / `maxContractChars` / `maxShadowChars` / `shadowLog` / `debug` / `skillDir`）。
- `README.md`（含契约样张、安装、配置、已验证/未验证）、`icon.svg`、`package.json`（`dsh.bundle.patch` + `test` 脚本）。
- `test/takeover.test.mjs`：**10 条夹具**，自带沙箱（临时目录 + `@deepseek-ai/dsh-llm` 桩，等价真实解析路径），`node --test` 全绿。覆盖：未标记零注入 / off 不注入 / shadow 一行+日志+同会话只记一次 / on 契约内容与长度 / 注入位置 / resume 去重 / 同批去重 / fs 抛错 fail-open / state 坏 JSON 降级 / `defaultMode=on` 但未标记仍不注入。

**修改**
- `scripts/loop-state.ps1`：新增 `-Action sync-shadow`（读影子日志 → `shadowSessions` + `shadow{sessions,target,canUpgrade,at}`；不覆盖已有 `next.label`）与 `-ShadowTarget`（默认 3）；`status` 增加「影子：已观察 N/M 个会话 —— 可升级」一行。
- `scripts/loop-state.ps1`（补）：`init` 生成的 `.dsh/loop/.gitignore` 追加 `shadow-log.jsonl`；默认 `-SkillVersion` 跟到 2.11.0。
- 插件影子提示超预算时**丢「下一步」尾句并保句号收尾**，不再截成半句（夹具加了两条断言）。
- `references/02-takeover.md`：P1 从「未实现」改为「已实现 + 夹具验证」，补 §2.1（入口/钩子/档位/注入/去重/影子计数/安装/夹具）、`sync-shadow` 命令与回归行；已知限制改写为真实未实测项。
- `SKILL.md`：§1 的 P1 描述更新；§8 文件地图补 `plugins/capability-loop/`；`version` 2.11.0。
- `version.json`：新增 `bundle` 块（dir/name/kind/entry/hook/install/test/verified/unverified），breaking_changes 补 v2.11.0。

**验证（本轮实测）**
- 夹具：`node --test plugins/capability-loop/test/takeover.test.mjs` → **10/10 pass**。
- `node --check index.js` → 0 错误；`package.json` / `cordis.patch.yml` 可解析。
- 契约样张实测：813 字符、注入位置索引 1（用户消息 0）、`digest=cl2ff7ab3d-330`。
- `sync-shadow`：无日志 → exit 1 + 提示；3 条不同会话（含 1 条重复）→ `shadowSessions=3`、`canUpgrade=true`、`status` 打印升级提示。
- 9 个 `.ps1` 解析 0 错误 + BOM 完好；`package-skill.ps1` 打包 WARN=0。

**未实测**
- **真实 Cordis 加载**：`install_bundle` 后该行是否按预期激活（本轮只做夹具，未改用户 profile）。
- 自定义 `source.kind='capability-loop'` 在 Web UI 的渲染表现（可能显示为普通用户消息；`MessageSourceMap` 文档称消费者对未知 kind 降级）。
- 真实会话的 token 计费差异；多工作区切换时的读取时序。
- `shadow-log.jsonl` 每会话读全量再重写的成本（日志是每会话一行，预期很小，未做长跑压测）。
- **影子日志已写进本仓库 dogfood**（`.dsh/loop/shadow-log.jsonl`，已被 `.gitignore` 忽略），`sync-shadow` 实测计数 1/3。

**回滚**：`git revert` 本提交；或仅卸载插件（`plugin_manager action=remove_bundle target=dsh-capability-loop-bundle`）——skill 侧行为不受影响。`v2.10.0` 的 P0 路径仍完整可用。

## v2.10.0 — 2026-11-18（接管协议：让闭环自动生效，而不是等模型想起）

**起因**：用户实测反馈「装了 skill 但真实项目里不接管」——没有 INTAKE、没有门禁、没有证据收口，必须手动 `/dsh-capability-loop` 才动。根因不是 description 写得不够好，而是缺**确定性的触发、会话内的状态、用户可证的可视性**三层机制：skill 正文只有在模型主动调 `skill` 或用户打 `/name` 时才注入（catalog 只有摘要）；七阶段没有状态载体，跨会话不保留；门禁输出只在终端滚过。

**新增**
- `references/02-takeover.md`：接管协议——三档（`off` / `shadow` 影子 / `on` 接管）八维对照、状态源 schema、`<system-reminder>` 注入逐字稿（on ≈1,450 字符 ≈350–400 token；shadow ≈90 字符）、注入纪律（首步一次 / digest 增量 / fail-open / 不写 system prompt / 不新增 Session event 类型）、P0（AGENTS 片段软接管，今天可用）→ P1（宿主插件 `agent/pre-step` 折入契约，硬接管）→ P2（Web 面板）路线、正反例回归基线、已知限制。
- `scripts/loop-state.ps1`：接管状态源唯一写入方。`init`（生成 `.dsh/loop/project.json` + `state.json` + `.gitignore`，默认 `shadow`）/ `status`（只读，未接入 exit 3，支持 `-Json`）/ `set-mode` / `set-stage` / `set-next` / `record-check` / `add-blocker`（自动 D-ID）/ `resolve-blocker` / `sync-audit`。写 `digest`（mode+stage+checks+blockers 指纹）供 P1 判断增量注入。
- `templates/agents-loop-fragment.md`：AGENTS.md 12 行接管片段（标记行 `<!-- dsh-capability-loop:on -->` + 先读 state + 适用/豁免 + 证据 + 门禁 + 自审不顶门 + 写回），含「为什么是这几行」与「不要把整包贴进去」。
- `templates/loop-project.json`：接管声明模板。

**修改**
- `scripts/loop-gate.ps1`：新增可选 `-StateFile`；在「单一类别（design/requirement/test）或 `-Environment`」且「给了 `-StateFile` 或工程有 `.dsh/loop/project.json`」时，调用 `loop-state.ps1 -Action record-check` 写回 `checks.<类别>`。**未标记工程零变化**；退出码语义不变。
- `scripts/package-skill.ps1`：**修复打包会把 `.tmp` 打进去**的缺陷（此前 1003 条目 → 现 62 条目）。新增排除目录 `.tmp/.git/.dsh/dist/out/__pycache__/node_modules` 与 `.DS_Store/Thumbs.db`（`.dsh/` 是工程级接管状态，含本机路径，属于工程而非技能）；副作用是「本机路径」扫描不再命中 `.tmp` 里的历史评审记录（本次由 WARN 4 处变 PASS）。
- `scripts/capability-audit.ps1`：写快照后，若工程已标记，自动 `sync-audit`（同步 metrics）并记 `checks.environment-audit`（PASS/WARN/FAIL + exit）。未标记工程零变化。
- `SKILL.md`：新增 §1「接管」（三档表 + 一行接入命令 + 状态源 + P0/P1/P2），章节整体后移重编号；§5 快速命令加接管命令；§8 文件地图补 `02-takeover.md` / `loop-state.ps1` / 两个新模板。frontmatter `version` 2.9.6 → 2.10.0；`description` 的【配套】加「项目接管（三档+状态源）」，字符数 188 → **199**（仍 ≤200 的「不偏贵」线，catalog 增加约 11 字符）。
- `version.json`：版本、references/templates/scripts 清单、breaking_changes 同步。

**验证（本轮实测，PowerShell 5.1）**
- 8 个 `.ps1` 全部 Parser 0 错误 + UTF-8 BOM（编辑后逐个人工补 BOM）。
- `loop-state.ps1`：`init`（临时目录）→ `state.json`/`project.json`/`.gitignore` 三件生成；`status` 未接入 exit 3；`record-check`/`set-stage`/`add-blocker`×2（自动 D-01/D-02）/`resolve-blocker`/`set-mode on`/`sync-audit` 全部 PASS，`project.json.mode` 与 `state.mode` 同步。
- `loop-gate.ps1` 状态写回：正例（有 design-context+grill）→ PASS + `checks.design=PASS`；反例（缺 design-context）→ exit 1 + `checks.design=FAIL`；**未标记工程不创建 `.dsh/`**（实测 state exists=False）；标记工程自动写回（不传 `-StateFile`）。
- `next.label` 不被 FAIL 覆盖：先 `set-next` 再有 FAIL，`status` 仍显示用户设定的下一步。
- `capability-audit.ps1` 在标记工程上自动 `sync-audit` + 记 `environment-audit`（PASS=19 WARN=10 FAIL=2 SKIP=1 的临时目录样本）。

**未实测**
- P1 宿主插件注入（`agent/pre-step` 折入契约、resume/fork 去重、`shadowSessions` 计数）——设计稿 `docs/design/2026-11-18-capability-loop-panel.md` 已给逐字稿与验收判据，尚未实现。
- P2 面板（`sidebar.panellist` + `main`、7 Tab、运行中心）——只有设计稿与 mockup，无真实插件渲染。
- `loop-gate -Kind all` 不写回（设计如此，未跑 all 场景验证）。
- 设计自审的 P2 打磨项（当前阶段强调色、记忆返工趋势、活动条数）未做。

**回滚**：`git revert` 本提交即可（新增文件全部为新增，`loop-gate`/`capability-audit` 的新增逻辑均在 try/catch 内且默认不触发——未标记工程行为完全不变）；旧工程若已生成 `.dsh/loop/`，删除该目录即恢复到未接管。

## v2.9.6 — 2026-11-15（SKILL 描述改主次结构：重点功能 / 配套功能）

**起因**：v2.9.5 的 frontmatter `description` 是一条平铺的能力链（审计→修复→串接→门禁→写回）加一串触发词，主次不分——核心（体检/修复 DSH 自身）与配套（项目接入、需求/设计/测试、交接、grill、迁移/上架）混在同一句，技能市场里也不容易看出「这个 skill 到底主打什么」。

**修正**
- `SKILL.md` frontmatter `description` 重排为显式主次结构：`【重点】` = 体检/修复 DSH 自身（九组审计→检索/桌面壳/Token 死重量修复→门禁验收→经验写回）+ 适用触发；`【配套】` = 项目接入六问、需求/设计/测试串接、Trae 交接体检（含网关前缀）、grill 自对抗、迁移与上架；保留尾部排除句（单点需求/设计/测试走各自规范）。
- **触发词集合与触发边界不变**（升级/优化/体检 DSH、治理插件与技能、修会话检索或进程退出、降 Token、迭代本 skill、迁移/上架等原词全部保留），只调整呈现顺序与分段；字符数 195 → 188（catalog 成本不增长）。
- `version.json`：2.9.5 → 2.9.6（PATCH：未改脚本行为、门禁口径、退出码语义与触发边界）；`released` 2026-11-15。

**验证（本轮实测）**
- `package-skill.ps1`：EXIT=0，description 长度 PASS（188 字符 ≤200），ZIP 40 条目/单顶层/全 `/`，`SHA256SUMS` 40/40。
- 反例：frontmatter 与 `version.json` 版本不一致 → EXIT=1（校验未回归）。
- 文档规模：`SKILL.md` 208 行（<300）；8/8 `.ps1` BOM + Parser 不变。
- 新 ZIP：由 `package-skill.ps1` 生成 40 条目/单顶层/全 `/`（`dsh-capability-loop-v2.9.6.zip`，具体字节数与 SHA256 见发布记录，避免写进包内造成自引用）。

**未实测**：技能市场/ClawHub 对 `【重点】/【配套】` 这类结构化描述的实际选择效果（需真实触发样本观察；市场端按 description 语义匹配，本地无法判定）。

**回滚**：把 `SKILL.md` 的 `description` 还原为 v2.9.5 原文（见下一条目），`version.json` 回 2.9.5；无脚本行为回滚。

## v2.9.5 — 2026-11-13（F 组反向指令改位置序判定）

**起因**：v2.9.4 去掉顿号切分后出现**双刃**：`不要写 /api、/png 前缀` 能抓了，但「网关前缀 /png 必写、host 不写」
「路径含 /png 前缀、不含 host」被误报（否定义在 `/png…前缀` 之后）。靠「切/不切顿号」无法同时满足两个方向。

**修正**
- 反向指令改**位置序判定**：去掉 `**`/反引号装饰、剥离不含 `/png` 的括号说明后，**只按 `。；` 切句**；
  在句内定位「`/png` … 前缀/硬编码/硬写」短语，**只有否定词出现在该短语之前**才判 FAIL。
  - `不要写 /api、/png 前缀` / `**不要**写 host，**也不要**写 `/api` 或 `/png` 前缀` → FAIL（否定在前）
  - `网关前缀 /png 必写、host 不写` / `含 /png 前缀、不含 host` / `含 /png 网关前缀（不写 host；/png 由常量给出）` → 不误报（否定在后）
  - 仍保留：「不得漏写」正向豁免；`不是/而非/≠` 对比豁免；历史行豁免；`不需要写` 属否定词。
- **全 weak 不再静默**：`if api_prefixes or weak_prefixes:`——工程里每个前缀只出现 1 次时，
  出 `F-prefix-weak` **WARN** 提示人工确认；缺陷路径仍按 FAIL 处理（不再落 F-skip）。
- 测试文件排除改**精确后缀 + 目录**（`*.test.*`/`*.spec.*`/`/__tests__/`/`/fixtures/`/`/mocks/`/`/stubs/`），
  不再用子串（原来 `special.ts` 会因含 `spec` 被误排除）。
- 口径同步 `SKILL.md` 19 与 `60-handoff.md` 1.9（改为位置序描述，删除「必写/必须/必含 不误报」的旧规则）。

**验证（本轮实测）**
- 正向不误报：`网关前缀 /png 必写、host 不写`、`路径含 /png 前缀、不含 host`、`含 /png 网关前缀（不写 host；/png 由常量给出）`、`不得漏写 /png 前缀` → **forbid 0 命中**。
- 反向命中：`不要写 /api、/png 前缀`、`**不要**写 /api 或 /png 前缀`、`不要写 /png 前缀（不是 /api）` → **F-forbid FAIL**。
- `/api` 事故形态仍 FAIL；真实包 `EXIT=1`、FAIL=5、F PASS；合规正例 EXIT=0。
- 全 weak 夹具：缺陷路径 → FAIL；正确路径 → `F-prefix-weak` WARN。

**未实测**：工程网关前缀恰为 `/api` 的约定差异（当前一律把 `api` 视作 baseURL 段）；非 `src/api` 结构工程会落 F-skip。

## v2.9.4 — 2026-11-13（F 组边界收口：/api 形态、括号与顿号写法）

**起因**：v2.9.3 复核发现 3 项边界：
① 真实工程里 `apps/web-main/src/api/ai-assistant/index.test.ts` 的 `'/api/…'` 让 `api` 进了前缀集合 → 把真实包全量替换成 `/api/annualResourceDemand/*` 时 **F 组仍 PASS**（事故文档形态被放行）；proxy 来源同理（声明 `'/api'` 会放行）。
② 括号同分句：「不要写 `/png` 前缀（不是 /api）」因同分句含「不是」被豁免 → 漏报；「含 `/png` 前缀（不写 host）」被误报。
③ 新增分句符 `、` 的双向副作用：`不要写 `/api`、`/png` 前缀` 被切开漏报。

**修正**
- 前缀集合：只取 API 目录、**排除 test/spec/mock/stub/fixture 文件**、**排除 `api` 段**（baseURL 不是网关前缀）；**取消 proxy/vite-config 来源**；出现 **1 次**的段不再算确定前缀，而记入 `weak` → `F-prefix-weak` **WARN** 提示人工确认（避免「仅 1 次就整项静默关闭」）。
- 括号处理：不含 `/png` 的括号视为说明**剥离**（`（不写 host）`）；含 `/png` 的括号**保留内容**（事故原文就在括号里）。
- 分句符**去掉 `、`**（`，,。；;` 才切分）；否定词补 **`不需要写`**。
- 口径同步 `SKILL.md` 不变式 19 / `60-handoff.md` 1.9（明确「不得漏写」是正向、判分句规则、前缀集合规则）。

**验证（本轮实测）**
- 事故原文 **7 变体全部 F-forbid FAIL**（含 `**不要**写 /api 或 /png 前缀`、`不要写 /api 或者 /png 前缀`、`**不要**写 host，**也不要**写 /api 或 /png 前缀`、`不要写 host 和 /png 前缀`、`不写 host、不写 /png 前缀`）。
- 正确措辞 **0 误报**：`含 /png 网关前缀；host 不写`、`不得漏写 /png 前缀`、`网关前缀 /png 必写；不含 host、不含 /api`、`含 /png 网关前缀（不写 host）`。
- **`/api/annualResourceDemand/list` 形态（v2.9.3 会放行）→ F-prefix FAIL**；括号反向 `不要写 /png 前缀（不是 /api）` → FAIL；顿号反向 `不要写 /api、/png 前缀` → FAIL（v2.9.3 漏报）。
- 真实包：`EXIT=1`、FAIL=5、**F PASS「9 处」**（前缀集合已无 `api`、无 test 文件污染）；路由父级假绿夹具仍 FAIL；合规正例 EXIT=0。

**未实测**：proxy/网关前缀在他工程命名结构下的覆盖（本版已改为不依赖 proxy）；仅校验首段前缀。

## v2.9.3 — 2026-11-13（F 组反向指令改分句判定，修掉事故原文漏检回归）

**起因**：v2.9.2 为消除「正确措辞被误报」，把反向指令改成「否定词与 `/png` 相邻 ≤12 字符」+ `STRIP_NEG` 剥离宾语。
复核证伪发现**回归**：事故原文 `**不要**写 /api 或 /png 前缀`（`**` 装饰使距离 >12）、`不要写 /api 或者 /png 前缀`、
`**不要**写 host，**也不要**写 /api 或 /png 前缀 → **全部漏检**（把真实包 T-08 还原成事故原文，v2.9.2 脚本无任何 F FAIL）。

**修正**
- 判定改为**分句**：先去掉 `**`/`_`/反引号装饰，再按 `，,、。；;` 切分；**同一分句内**同时出现 `/png` + 前缀/硬编码/硬写 + 否定词 → FAIL。
  - 「不得漏写 `/png` 前缀」= 正向要求，豁免；
  - 「不写 host」「不含 `/api`」所在分句不含 `/png`，天然不触发；
  - 「`/api` 与 `/png` 不是同一前缀」属解释性对比（含 不是/而非/≠），豁免；
  - 历史行（原写/已修/根因/事故/变更记录/早期）豁免。
- 路径收集的分句符补 `，,、`（同分句逗号里的否定也不再吞掉路径校验）。
- 前缀集合补充取 **proxy / vite-config** 里声明的前缀（避免某前缀只在配置里出现 1 次时 F 项被静默关闭）。
- 口径同步：`SKILL.md` 不变式 19、`60-handoff.md` 1.9（写明「按分句判定」与三类不误报情形）。

**验证（本轮实测，7 个事故变体 + 3 个正确措辞 + 3 类反例）**
- 事故原文 7 变体（含 `**不要**写 /api 或 /png 前缀`、`不要写 /api 或者 /png 前缀`、`**不要**写 host，**也不要**写 /api 或 /png 前缀`、
  `不要写 host 和 /png 前缀`、`不写 host、不写 /png 前缀`、`不要写 /png 前缀`）→ **全部 F-forbid-prefix FAIL**。
- 正确措辞 3 种（「含 `/png` 网关前缀；host 不写」「不得漏写 `/png` 前缀」「网关前缀 `/png` 必写；不含 host、不含 `/api`」）→ **0 误报**。
- 真实包：`EXIT=1`、FAIL=5、**F PASS「9 处一致」**（前缀集合因补 proxy 增到 9 条有效路径）；路由子路径假绿夹具仍 FAIL；合规正例 `EXIT=0`。

**未实测**：其他工程结构下 proxy 前缀来源的覆盖度；仅校验首段前缀。

## v2.9.2 — 2026-11-13（F 组两处修正：路由豁免/否定误报）

**起因**：v2.9.1 复核发现新引入 1 处假绿 + 1 类误报：
① 页面路由豁免用了 `startswith(route + "/")` —— 当路由表里有 `/annualResourceDemand` 时，契约里漏写 `/png` 的
`/annualResourceDemand/list`、`/export` 整支被豁免 → **EXIT=0 假绿**；
② 反向指令判定只要「有 `/png` + 前缀 + 否定词且无必写」就 FAIL —— 正确写法「路径常量**含** `/png` 网关前缀；host **不写**」、
「**不得漏写** `/png` 前缀」被判成反向指令 → **误报挡住正确包**。

**修正**
- 路由豁免改为**精确匹配**（`path.rstrip("/") in page_routes`）：只豁免与页面路由完全相同的路径，其子路径仍按 API 校验。
- 反向指令改为：先剥离「不写 host / 不含 /api / 不得写域名」这类正确指引（`STRIP_NEG`），再要求否定词与 `/png` **相邻**（≤12 字符）才判 FAIL；
  「必写/必须/必含/**漏写**」一律视为正向。
- 前缀阈值 `≥2` → **`≥1`**：避免某前缀只出现 1 次时整个 F 项被 `F-skip` 静默关闭。
- 通过计数改为 `checked - page_hits`（不再把页面路由算进「N 处一致」）。
- 文档口径：`SKILL.md`「查四件事」→「查六组（A–F）」、文件地图补 F 组、`60-handoff.md` 1.8 列全 A–F、`README` 环境要求补 `handoff-audit.py`。

**验证（本轮实测）**
- 真实包：`EXIT=1`、FAIL=5、**F PASS「8 处 API 路径一致」**（12 处中 4 处为页面路由，正确排除）。
- **v2.9.1 假绿复现夹具**（`src/router` 有 `/annualResourceDemand`、契约写 `/annualResourceDemand/list|export`）→ **F-prefix FAIL**。
- 正确措辞夹具（「含 `/png` 前缀；host 不写」「不得漏写 `/png` 前缀」）→ **不再误报**（F 组 PASS）。
- 真反向指令夹具（「**不要写** `/png` 前缀」）→ **F-forbid-prefix FAIL**。
- 合规正例：`EXIT=0`（PASS=13 / WARN=0）；`py_compile` 通过。

**未实测**：其他工程结构下的路由/前缀覆盖度；仅校验首段前缀，不校验版本号/超时等约定。

## v2.9.1 — 2026-11-13（F 组口径修正：前缀集合/路由排除/反向指令）

**起因**：v2.9.0 的 F 组在复核中被证实**存在假绿**——①前缀集合实际扫的是 `apps/` 下全部 `ts/js/vue`（含 `public/tinymce.min.js` 的 `skins/langs`、`src/router/routes/local.ts` 的 `resourceDemand`），与文档写的「只取 `src/api/**`」不符，构造「路由段出现 ≥5 次」即可让漏前缀缺陷放行；②反向指令只认「不要|禁止 … `/png`」一种句式，真实残留的「**不含** `/api` 或 `/png` 硬编码」「业务代码**不写死**」不报；③`/api` 曾被列入豁免段，恰好放过事故形态。

**修正**
- 前缀集合只统计 **`src/api/**`（含 `apps/<app>/src/api/**`）**，阈值降到「出现 ≥2 次」即算既有前缀。
- 新增**页面路由排除**：从 `src/router/**` 收集 path 常量（如 `/resourceDemand/monthly`），契约里出现的路由路径不再被误判为 API。
- 反向指令识别扩为「`/png` + 前缀/硬编码/硬写 + 否定词（不要|禁止|不写|不含|不写死|不得|严禁）」，
  覆盖 **brief/tasks/acceptance/record/PROMPT 五个文档**；「必写/必须/必含」的正向措辞与描述旧缺陷的历史行（原写/已修/根因/事故）不误报。
- 反向指令检查移出「有 `src/api` 才执行」的分支（无 `src/api` 的工程同样会查）。
- `NON_API_SEGMENTS` 移除 `api`（`/api/...` 不再整体豁免，前缀不对就会被查出）。
- 报告计数改为**去重后的路径数**（原先用命中行数，出现「报 3 处只列 2 个」）。
- 同步口径：`README` 脚本表、`SKILL.md` 不变式 19、`60-handoff.md` 1.9、`version.json` 脚本描述。

**验证（本轮实测）**
- 真实包 `resource-demand`：`EXIT=1`、FAIL=5（B/C/D-nobatch/D-prompt-batch/E-noctx-file）、**F 组 PASS**「12 处 API 路径均与既有前缀一致（api/auth/callback/finance/ige/inventory…）」，路由 `/resourceDemand/*` 未被误判。
- 反例①（路由污染：`src/router` 里 `/annualResourceDemand`×5、契约去掉 `/png`）→ **F-prefix FAIL**（v2.9.0 会假绿）。
- 反例②（`acceptance.md` 写「API 常量不含 `/api` 或 `/png` 硬编码」）→ **F-forbid-prefix FAIL**。
- 反例③（旧缺陷 tasks.md：`/annualResourceDemand/list` 无前缀）→ F-prefix FAIL 点名。
- 合规正例 → `EXIT=0`（PASS=13 / WARN=0）；`py_compile` 通过。

**未实测**：前缀阈值（≥2）在其他工程结构下的适用性；仅校验首段前缀，不校验版本号/超时等约定。

## v2.9.0 — 2026-11-13（真实事故驱动：接口网关前缀校验 F 组）

**起因（真实事故）**：`rmp-frontend` 年度接口联调 404 —— 月度契约写的是 `/png/monthlyResourceDemand/*`（正确），
而 `07-年度接口规格` 的公共约定写成 `Base /api/annualResourceDemand`，交接包 `tasks.md` T-08 更写了「**不要**写 `/api` 或 `/png` 前缀」
→ 实现按契约写成 `/annualResourceDemand/list`，被网关 404。**接口文档与交接契约都没把「网关前缀」当硬约定**，这是流程缺陷。

**新增**
- `scripts/handoff-audit.py` **F 组「API 路径前缀一致性」**：
  - 从工程 `src/api/**`（含 `apps/*/src/api`）统计既有 API 前缀集合（出现 ≥5 次的第一段，如 `png`/`sales`）；
  - 扫 `brief/tasks/acceptance/record/PROMPT` 里以 `/` 开头的整段路径与 `GET|POST … /path`，首段不在集合内 → **FAIL**（提示「多半漏写网关前缀」）；
  - 出现「不要/禁止 … /png 前缀」这类反向指令 → **FAIL `F-forbid-prefix`**；
  - 否定语境行（禁止/不新增/不要/不得/已废弃）自动跳过，避免误报「不新增 /annualResourceDemand/companies」；
  - 工程无 `src/api` 时 `F-skip` 按 OK 处理（不适用）。
- `references/60-handoff.md` 新增步骤 1.9「接口契约核对」：网关前缀写全、host 不写、`/api` ≠ 网关前缀、方法/响应包装/错误码一并核。
- `SKILL.md` 新增不变式 19（接口契约必须写全网关前缀；反向指令视为缺陷）。

**验证（本轮实测）**
- 修复后的真实包：F 组 **PASS**「12 处 API 路径均与工程既有网关前缀一致」；总 `EXIT=1`、FAIL=5（B-missing / C-missing / D-nobatch / D-prompt-batch / E-noctx-file）。
- **反例（把 `/png/annualResourceDemand` 改回无前缀，复现旧缺陷）：`EXIT=1`，`F-prefix` 命中 7 处**，输出直接点名 `/annualResourceDemand/list`、`/export`。
- 合规正例：`EXIT=0`（PASS=13 / WARN=0）。
- `py_compile` 通过；F 组对 `![]()`/evidence 路径无误报（只认以 `/` 开头的整段）。

**未实测**：前缀集合阈值（≥5 次）在其他工程结构的适用性；F 组只覆盖「首段前缀」，不校验版本号/超时等约定。

## v2.8.1 — 2026-11-13（v2.8.0 复核修订：脚本边界 + 文档口径）

**修正（复核 P2/P3，均为收紧或纠错，无新功能）**
- `scripts/handoff-audit.py`：
  - 新增 **D-batch-size**：解析「## 批次」表，某批任务数 > `--batch-max-tasks`（默认 3）→ **FAIL**（原只查段是否存在，塞 12 个任务也放行）；批次文件数 > `--batch-max-files` → WARN；任务未归入任何批次 → WARN。
  - 引用收集扩展到 **markdown 链接/图片 `![]()`**（原来只认反引号，图片引用会漏）；扩展名白名单加 webp/gif/svg/pdf/log/yaml/xml 等。
  - `evidence/` 改为**递归**统计（子目录不再误报 `C-empty`）；证据匹配同时认相对名与 basename；任务 ID 正则放宽到 `A1/B1/T-01` 等非 `T-NN` 写法（原来会静默跳过 D/E 三项）。
  - **默认不再落盘**：原默认把 `audit-report.md` 写进被体检的工程（只读工具污染工作区），现默认只打印，`--out` 才写。
  - 报告体积用 **UTF-8 字节数**（原来把字符数当 KB，`resource-demand` 实际 59 KB 被报成 39 KB）。
  - `E-noctx-file` 从 WARN 提升为 **FAIL**（既有系统却没有 `design-context.md` 属于「风格没固化」，不该放行）。
- `references/60-handoff.md`：退出码文案纠正为「`0` 无 FAIL 且无 WARN；`3` 仅 WARN」；体检报告默认不落盘、留档用 `--out`；Trae 版本口径统一为 3.4.18。
- `SKILL.md`：不变式 17（模块预检）与 18（交接体检）顺序纠正（原 18 排在 17 前）。
- `README.md`：脚本一览补 `handoff-audit.py`。
- `CHANGELOG`：本机工程绝对路径改为 `<工程根>`；「9 张截图」更正为「8 张截图 + 1 个 README.md」；补「敏感扫描不覆盖普通盘符项目路径、用 `-ExtraSensitivePaths`」的已知边界。

**验证（本轮实测）**
- 真实包 `resource-demand`：EXIT=1，**FAIL=5**（`B-missing` 59 / `C-missing` 35 / `D-nobatch` / `D-prompt-batch` / `E-noctx-file`）+ WARN=1（`C-orphan` 8 个 jpg）。
- 自建合规包：**EXIT=0**（PASS=12 / WARN=0）。
- 反例：批次塞 12 个任务 → `D-batch-size` FAIL、EXIT=1；`evidence/` 子目录文件不再触发 `C-empty`。
- `py_compile` 通过；退出码 0/1/3/2 均已覆盖。

**未实测**：缩写表解析仅在本项目包验证；`materials/` 随行后 Trae 实读效果未实测。

## v2.8.0 — 2026-11-13（复盘驱动：交接包体检 + 材料随行 + 批次纪律）

**起因**：真实项目复盘（`rmp-frontend` / `docs/handoff/resource-demand`）暴露 4 个问题：①设计稿与规格在**另一个工作区**（`文档工作区（与本机工程不同盘符）`），实现者读不到；②`acceptance`/`record` 引用的 **35 个证据文件全部不存在**，实际 8 张截图（+1 个 README.md）无人引用；③12 个任务一次交付（tasks.md 39 KB）→ 实现者上下文被压缩；④无 `design-context`，既有系统风格没被固化，设计稿先出、规范后补。

**新增**
- `scripts/handoff-audit.py`：交接包体检。A 包完整性（四件套+PROMPT）/ B 材料可达性（工程内相对路径解析 + 缩写表解析 + 跨工作区判定）/ C 证据对账（acceptance+record 的 `evidence/` 引用 vs 实际文件，含 `*` 通配、孤儿文件）/ D 批次与粒度（批次段、PROMPT 本批、单任务 ≤3 文件）/ E 设计依据（brief 段 + `design-context*.md` + 每任务「设计依据」）。退出码 `0/1/3/2`；报告写 `<包>/audit-report.md`。
- `references/60-handoff.md`：新增步骤 1.6 材料随行（跨工作区必须拷到 `docs/handoff/<slug>/materials/`）、1.7 批次划分（一批 ≤3 任务/≤8 文件/≤1 页面）、1.8 交接包体检（门禁命令与退出码）；新增 §5.1 设计前置可执行要求（系统已有→遵循既有 token/组件，禁止自造；新项目→先固化 token）。
- `SKILL.md`：不变式 18（交接前必须 audit 通过、材料必须在工程内、必须分批）、命令区、文件地图登记新脚本。
- `version.json`：`scripts` 增至 10（含 `handoff-audit.py`）。

**验证（本轮实测，`rmp-frontend` 真实包）**
- `python scripts/handoff-audit.py --workspace <工程根> --slug resource-demand`：EXIT=1，PASS=7 / WARN=2 / FAIL=4 —— FAIL 恰为四项：`B-missing` 61 处引用在工程内找不到、`C-missing` 35 个证据引用不存在、`D-nobatch`/`D-prompt-batch` 无批次且 PROMPT 未指本批；WARN 为 `C-orphan` 8 个截图未被引用、`E-noctx-file` 无 design-context。**该 4+2 项与用户复盘提出的 4 个问题一一对应**。
- 正例：`py_compile` 通过；`--json` 输出结构化结果；工程/包路径不存在时 EXIT=2；空 evidence 目录 → `C-empty` FAIL。

**未实测**：`handoff-audit.py` 的缩写表解析仅在 `resource-demand` 包上验证（其它包的 brief 结构可能不同）；`materials/` 随行后的 Trae 实读效果未实测（需下一次真实交接验证）。

**已知边界**：`package-skill.ps1` 的敏感扫描只覆盖「用户目录」（`%USERPROFILE%`/`%LOCALAPPDATA%` + 通用用户目录正则），**不覆盖普通盘符项目路径**（如 `D:\某项目`）——给特定项目打标时请显式传 `-ExtraSensitivePaths`；本 CHANGELOG 里原先的工程绝对路径已改为 `<工程根>`。

**回滚**：删 `scripts/handoff-audit.py`，回退 60-handoff/SKILL/version.json 至 v2.7.1。

## v2.7.1 — 2026-11-13（对齐复核 P3 文档打磨）

**修正（不涉及脚本）**：CHANGELOG v2.4.0 条目笔误 `features-handoff`→`feature-handoff`；归属说明补「实测证据来自联调会话、v2.7.0 对齐未复跑 GUI」；`references/60-handoff.md` 的 v2.4.0–v2.7.0 条目统一加「脚本在 `feature-handoff/scripts/`」指路；`version.json.compatibility` 的 node/python 口径与当前脚本构成一致；`README.md` 脚本表 `module-preflight.py` 退出码列改为「0 / 1 / 3（参数错误 2）」，与「参数/路径错误统一 exit 2」约定一致。
**验证**：`package-skill.ps1` EXIT=0（WARN=0），ZIP 39 条目/单顶层/全 `/`，`SHA256SUMS` 39/39；`capability-audit.ps1 -Strict` FAIL=0；8/8 `.ps1` BOM+Parser；文档规模与相对链接通过。来源：`.tmp/capability-review/review-v2.7.0-20261113.md` 的 P3 清单。
**回滚**：用 v2.7.0 目录覆盖。

## v2.7.0 — 2026-11-13（交接自动化 CDP 加固）

**新增 CDP 加固**：`feature-handoff/scripts/trae-cdp.mjs` + 包装脚本 `-Mode Cdp`。重启 Trae 加 `--remote-debugging-port=9333`，通过 `/json/list` 定位 workbench，按“右侧+下半区+面积”打分命中 `DIV.chat-input-v2-input-box-editable`，真实点击聚焦后用 `Input.insertText` 写入，读回 `len/head` 校验；清空用 `Ctrl+A`+`Backspace` 键事件（execCommand 在该编辑器无效）。
**实测**：测试串 ABCDE → len=5/head=ABCDE；真实 159 字符指针提示词 → len=159、head 正确、`sent=false`；找不到输入框 exit 3（自动尝试 Ctrl+U 后重试一次），端口未开且无 -Restart 时 exit 4。
**取舍**：CDP 优先（可验证），Click 坐标法保留作未重启兜底，Hotkey 仅调试。
**未实测**：`-AutoSend`（点击发送按钮）在多轮生成中的行为；多显示器下 Click 坐标。

## v2.6.1 — 2026-11-13（对话面板检测比例校准）

**校准**：对话面板检测的发送键探针比例从 (0.972,0.889) 修正为 **(0.964,0.934)**（原值偏低 40px，导致“面板已开仍判 closed”）。
**实测**：打开时 green=132 / 关闭时 green=0；`Ctrl+U` 仅在编辑器聚焦时打开面板（脚本已先点编辑器）；完整链路 检测→点击输入框→粘贴→前后截图哈希校验 全部 PASS，且不自动发送。
**证据**：sig `80A1AE…:22824` → `7ACC70…:23437`；测试文本 Ctrl+Z 撤销后 open=True；仓库零污染，tasks.md 55,268B。

## v2.6.0 — 2026-11-13（对话面板状态检测 + 自动开启）

**新增**：`send-to-trae-prompt.ps1` 增加**对话面板状态检测 + 自动开启**流程（检测发送按钮绿色像素 → 未打开则点编辑器并发送 `-ChatChord` → 复检 → 仍失败 exit 3 不盲发；支持 `-OpenClickXRatio/Y` 坐标兜底）。
**实测**：检测准确（关闭 green=0、阈值 20）；本机该布局 `Ctrl+U`、`Ctrl+Alt+B` 均**未能打开**对话面板（复检 green=10），脚本正确拒绝输入。
**结论/待办**：自动开启需真实入口（用户提供快捷键或面板开关坐标）或改用 CDP；已登记为待配置项。
**回归**：测试文案未污染仓库（命中 0），`tasks.md` 55,268B 完好。

## v2.5.1 — 2026-11-13（Click 坐标边界登记）

**修正/限制登记**：Click 模式回归测试暴露真实边界——当 TU 对话面板关闭、右下角变成终端时，固定比例坐标会点到终端，粘贴文本与 `^Z/^U` 被终端字面接收（未污染仓库文件；tasks.md 55,268B 完好）。
**结论**：坐标自动化必须「先截图确认目标区域」；布局不明时禁用 Hotkey 模式（`^Z` 会挂起前台进程）。脚本的哈希校验已正确 FAIL(exit 2)、未发送。
**写回**：`feature-handoff/SKILL.md` 增「已知限制（v2.5.1）」；`60-handoff.md` 增限制条目。
**后续**：CDP 方案（`--remote-debugging-port` + DOM 设值）列为该能力的稳健替代，未实测。

## v2.5.0 — 2026-11-13（Click 模式 + 截图哈希校验）

**新增**：`feature-handoff/scripts/send-to-trae-prompt.ps1` 的 **Click 模式**（默认）——用窗口相对坐标点对话输入框 → 粘贴 → **前后截图哈希校验** → 默认不发送（`-AutoSend` 才点发送）。同时 `-VerifyOnly`、`-Inline`、`-Mode Hotkey` 保留。
**为什么**：实测 Trae CN 3.4.18 的 `Ctrl+U` 只开面板不聚焦输入框；Electron DOM 对 UIA 不可见（`edit count=0`）。旧实现 `^U→^A→^V` 盲发导致 `^A` 落到编辑器、覆盖 `tasks.md`（已 Ctrl+Z + Ctrl+S 恢复 55,268B）。
**安全纪律**：脚本永不发送 `^A`/`^S`；校验失败 exit 2 且不发送。
**实测证据**：窗口 1440×900@371,102；点击 1611,912；before sig `9183E0C4332E7FC6:16535` → after `424CBDE7FF055A86:17847`（差异即落点证据）；最终对话区截图确认指针提示词在位、测试文本已 Ctrl+Z 清除。
**接线**：`feature-handoff/SKILL.md` 附节「自动填指令（Click 模式）」；本文件步骤 5。
**回滚**：`-Mode Hotkey` 可回旧路径（需自行保证焦点）；删除脚本则回到纯人工粘贴。
**未实测**：非 1440×900 分辨率/多显示器下的比例坐标；`-AutoSend` 发送按钮坐标。

## v2.4.1 — 2026-11-13（指针模式省 token）

**改进**：`send-to-trae-prompt.ps1` 默认改为**指针模式**（约 160 字符 / ~100 token），只发“按 PROMPT.md 执行 + 必读三件套 + 禁止改契约 + 回填 record”；`-Inline` 保留全文粘贴模式。
**为什么**：纯文本粘贴把已在文件里的契约重复灌进对话（629 字符/次，多轮与多任务累积），且 tasks.md 50KB+ 绝不应进对话；路径引用让 Trae 按需读文件，token 与上下文都更省。
**实测**：dry-run 指针模式 `chars=159`（inline 为 629）。
**接线**：`feature-handoff/SKILL.md` 附节新增「Token 取舍」；本文件步骤 5 补 v2.4.1 说明。
**回滚**：恢复脚本默认 `$Inline=$true` 即回到全文粘贴。

## v2.4.0 — 2026-11-13（自动填指令首版）

**新增**：`feature-handoff/scripts/send-to-trae-prompt.ps1`——唤起 Trae 后自动把 `PROMPT.md` 填入 AI 对话输入框，默认不发送，开发者按 Enter 确认开工。
**为什么**：`trae-cn.exe --help` 无 chat/prompt 参数；本机实测 Trae CN 对话快捷键 `Ctrl+U`（SendKeys `^u`），可用「窗口激活 + 快捷键 + 剪贴板」实现。
**实测**：激活 pid 11868（tasks.md - rmp-frontend - TRAE CN）→ `^u` → `^v`，629 字符提示词已填入输入框（未发送）。
**接线**：`feature-handoff/SKILL.md` 附节；本文件步骤 5 补充。
**回滚**：删除脚本并回退两处文档至 v2.3.0。
**未实测**：多窗口/失焦时粘贴目标；`-AutoSend` 自动发送（默认关闭）。

## v2.3.0 — 2026-11-13（交接前模块/路由预检）

**新增**：`scripts/module-preflight.py` —— 交接前置「模块/路由预检」（Python3，输出 Markdown 报告；exit 0=NONE / 1=EXISTS / 3=WEAK / 2=参数错误）。
**为什么**：真实工程 `rmp-frontend` 已存在 `apps/web-main/src/views/resourceDemand` 与 `/resourceDemand` 路由，但交接前无检查，容易把已有模块当新模块重写、或新建路由与既有菜单冲突。
**怎么用**：`python scripts/module-preflight.py --project <工程根> --keyword "<中文模块名>" --alias <英文别名...> [--menu-dump <菜单导出.json>]`；0=NONE、1=EXISTS、3=WEAK、2=参数错误。
**接线**：SKILL.md 不变式 17、`references/60-handoff.md` 步骤 1.5、`README.md` 脚本表、`QUICKSTART.md §4`。
**验证（2026-11-13 复跑）**：正例 `输差考核台账` → NONE / exit 0；反例 `资源需求` → EXISTS（`view|resourceDemand` + `api|resourceDemand`）/ exit 1；`--project D:\nope` → exit 2。
**回滚**：删 `scripts/module-preflight.py`，回退 SKILL.md/60-handoff.md/version.json/README/QUICKSTART 至 v2.2.1。
**未实测**：`--menu-dump` 对 live 菜单接口的覆盖（当前用菜单导出 JSON 代替）。

## v2.2.1 — 2026-11-13（复核残留清理：N1–N5 / R1 / R2）

**起因**：v2.2.0 复核 2 判「可交付」，但留 4 项新增（N1–N4）、2 项残留（R1、R2）与 1 项未实测风险（N5）。本版只做文档口径与 `package-skill.ps1` 校验收紧：`loop-gate`/`capability-audit`/`skill-status`/`visual-qa-check` 的退出码语义不变，`package-skill` 仅对结构不合格的 ZIP 由 WARN 改为 FAIL + exit 1。

**修正**
- **N1** `references/95-store-publish.md §2`：「路由仅 5 个」更正为插件 `lib/index.js` 实读的 **16 个路由**；结论不变——**没有向 SkillHub/ClawHub 发布或上传的路由**，唯一上传是本地导入 `POST /skill-market/api/import`。
- **R1** `95 §2`：`_meta.json` 一行改为「ClawHub **安装版**目录内可见；**发布是否同写未实测**」，与 §4 降级口径一致。
- **R2** `version.json.compatibility.node`：改为「22.13+ 或 24+（clawhub CLI，engines `^22.13.0 || >=24`）；仓库内 `.mjs` 工具 22+」，不再以 `>=22` 起头。
- **N2** `scripts/package-skill.ps1` 用法注释补 `-ExtraSensitivePaths`。
- **N3** `package-skill.ps1` 本机路径扫描按文件去重：`%LOCALAPPDATA%` 位于 `%USERPROFILE%` 下时，同一处不再记多条 WARN（每个文件的本机路径命中合并为 1 条）。
- **N4** `package-skill.ps1` ZIP 结构校验由 WARN 改 **FAIL + exit 1**：0 条目、含 `\` 分隔符、非单一顶层目录都判为不可用包（市场本地导入会失败）。
- **N5** `SKILL.md` frontmatter 新增 `version: 2.2.1`：技能市场 `declaredVersionOf` 读该字段显示「已安装版本」（v2.2.0 本地导入实测版本为空）；`package-skill.ps1` 新增一致性校验（frontmatter 缺失 WARN、与 `version.json` 不一致 FAIL）。
- **文档联动（复核 P3 顺手修）**：`README.md` 补「版本号三处一致」与 PATCH/MINOR 口径并收紧既有脚本内校验，`SKILL.md` 版本规则同步对齐（PATCH=既有脚本内修正/收紧；MINOR=新增脚本/章节/模板）+ 版本纪律补 frontmatter `version`，`references/90-provenance.md` 追加 v2.2.1 条目，`95 §6` 补「新增 frontmatter `version` 键的接受度」未实测/部分实测项；`references/80-evolution.md §3` 版本表与发布纪律同步（消除第二口径，冲突以 `SKILL.md` 为准）。

**验证（本轮实测）**
- `package-skill.ps1` 正例：EXIT=0；38 文件；frontmatter version PASS；本机路径扫描 0 命中；ZIP 38 条目、单顶层、路径全 `/`；`SHA256SUMS` 38/38 一致。
- 本地导入（插件导出函数，隔离 `DSH_HOME`）：`IMPORT OK files=38`、`version=2.2.1`（v2.2.0 为 `version=` 空，见 N5）。
- 反例：坏 name EXIT=1；frontmatter `version` 与 `version.json` 不一致 EXIT=1；本机路径夹具每个文件只记 1 条 WARN。
- `capability-audit.ps1 -Strict`：FAIL=0、EXIT=0；8/8 脚本 BOM + `Parser::ParseFile` 通过；文档规模与相对链接无死链。
- 独立复核：`.tmp/capability-review/review-v2.2.1-20261113.md`（非实现者，结论见该报告）。

**未实测**：`clawhub login` / `clawhub skill publish` 真实执行、SkillHub 同步时延、ClawHub 发布时的版本号解析（N5 只解决**市场本地导入**版本号）；详见 `95-store-publish.md §6`。

**回滚**：用 v2.2.0 目录覆盖安装版；本次无脚本行为回退（ZIP 校验只对不合格包更严格）。

## v2.2.0 — 2026-11-13（README + 商店上架实操 + P2 修正）

**起因**：用户要上架技能商店，并追问「当前 skill 的 README 是否写好」；v2.1.2 独立复验留下 3 个不阻塞 P2。

**新增**
- `README.md`：商店/人读概览（能力边界、两种安装方式、快速开始、目录结构、脚本表、版本与更新、环境要求、安全边界、许可证）。
- `references/95-store-publish.md`：上架实操——三层关系（ClawHub 发布 → SkillHub 同步 → DSH 市场安装）、2026-11-13 证据表、`clawhub login`/`clawhub skill publish` 命令、首次/更新/验证/回滚、未实测清单、一页检查单。
- `SKILL.md`：文件地图登记 `README.md` 与 `95-store-publish.md`；§5/§6/命令区补「上架 = ClawHub publish」；`QUICKSTART.md` 新增 §4.2。

**修正（P2）**
- `version.json`：登记 `visual-qa-check.ps1`；新增 `publish_registry`/`publish_tool`/`publish_doc`；lineage 追加本会话。
- `visual-qa-check.ps1`：失败分支仅在 PNG 真实存在时打印「探测证据：」，否则明确「未生成截图」。
- `package-skill.ps1`：`README.md` 缺失记 WARN；收尾提示与 `PUBLISH-NOTES.md` 改为真实上架路径（ClawHub publish；ZIP 仅供本地导入/留档）；修正 here-string 内 `v$version:` 的变量插值风险（改为 `${version}`）；ZIP 改为手工写条目，**条目路径统一 `/`** 并自动校验（PS5.1 `CreateFromDirectory` 会写成 `\`，不符合 ZIP 规范）。
- `references/80-evolution.md §8`、`90-provenance.md`（§2 证据 / §3.7 / §5 血缘）：同步商店机制与新证据。

**修正（独立复核 P1/P2，2026-11-13）**
- **P1-1 ZIP 本地导入**：`package-skill.ps1` 的 ZIP 只收录 `$pkgSkillDir`（**单一顶层 `<name>/`，38 条目**），manifest/SHA256SUMS/PUBLISH-NOTES 留在包目录留档、不进 ZIP；新增「路径全 `/` + 单一顶层」双断言。修后插件导出函数实测 `IMPORT OK`（参照复核报告）。
- **P1-2 敏感扫描**：`package-skill.ps1` 去掉硬编码的本机用户目录/本机项目目录（原为脚本内写死），改为运行时推导（`$env:USERPROFILE`/`$env:LOCALAPPDATA` + 通用用户目录正则 + `-ExtraSensitivePaths`）；**删除对 `package-skill.ps1` 自身的扫描豁免**，不再假 PASS。
- **P2-1** `95-store-publish.md §2`：证据改为「无发布路由；唯一上传是本地导入 `POST /skill-market/api/import`（`apiUpload`）」。
- **P2-2** 本 CHANGELOG 增加「独立复核」小节（原文悬空引用已修复）。
- **P2-3** `README.md` 脚本表补「参数/路径错误统一 exit 2」，并注明 `skill-status.ps1` 应从安装版目录运行。
- **P2-4** `95-store-publish.md §4`：`_meta.json` 从「发布成功后出现」降级为「安装版可见 + 发布是否同写未实测」。
- **P2-5** `README.md`/`version.json`：Node 口径统一为「22.13+ 或 24+」（clawhub `engines`）。
- **P2-6** `capability-audit.ps1`：去掉默认 `D:\DeepSeek Harness\resources\app\src` 硬编码，改为 `$env:DSH_APP_SRC` / 运行中 DSH 进程反推 / ProgramFiles / LocalAppData 探测，缺失记 WARN 不猜测。
- **P2-7** `skill-status.ps1`：检测到从源目录运行时打印「源 vs 源」提示，指引改用安装版脚本。

**验证（本轮实测）**
- 8/8 脚本 UTF-8 BOM + `Parser::ParseFile` 通过。
- `package-skill.ps1`：EXIT=0，38 文件，manifest version=2.2.0，SHA256SUMS 38/38 一致，ZIP **38 条目、单一顶层 `dsh-capability-loop/`、路径分隔符全部 `/`**（`dist/skill-store/dsh-capability-loop-v2.2.0.zip`）；坏 name 夹具 EXIT=1 不打包；缺 README 夹具 WARN 但 EXIT=0。
- ZIP 本地导入：用插件导出函数（隔离 `DSH_HOME`）实测 `IMPORT OK`（files=38）；修复前 41 条目/4 顶层对照为 `IMPORT FAIL`（见复核报告 P1-1）。
- `visual-qa-check.ps1`：danger-full-access 真实运行 exit 0（PNG 9,808 B、像素 16/32/48）；workspace-write 受限 exit 2 且提示语正确；`-SimulateBlocked` exit 2；无效 Chrome 路径 exit 1。
- `skill-status.ps1`：从安装版运行 exit 0，安装版=源=2.2.0、差异 0；从源目录运行会打印「源 vs 源」提示；商店记录 `origin=manual`（未上架）。
- `capability-audit.ps1 -Strict`：FAIL=0，exit 0（桌面壳检查改为进程/环境推导后仍 PASS）。
- 独立 Reviewer 复核：见下方「独立复核」小节（非实现者）。

**未实测**：`clawhub login` / `clawhub skill publish` 真实执行、SkillHub 同步时延、SkillHub 是否有独立上传入口（本机 shell 网络不可用 + 需 GitHub 授权）；详见 `95-store-publish.md §6`。

**回滚**：用 v2.1.2 目录覆盖安装版；商店安装版在市场「版本历史」回退。README/95 为增量文档，删除不影响脚本行为。

**独立复核（2026-11-13，Reviewer 未参与编写）**
- 报告：`.tmp/capability-review/review-v2.2.0-20261113.md`（逐项命令/退出码/文件:行号）。
- 复核 1 结论：8 项中 **6 PASS / 1 WARN / 1 FAIL**；**P0=0、P1=2、P2=7**；一句话「需修改后再交付」。
- 本版已闭环两个 P1（ZIP 单顶层可导入；敏感扫描去硬编码+去自豁免）与全部 P2；修复后复验见同目录 `review-v2.2.0-recheck-*.md`。
- 诚实性：`clawhub login/publish`、SkillHub 同步时延/独立上传入口、市场 UI 安装均**未实测**，本版未写成已通过。

## v2.1.2 — 2026-11-13（接入模板精简 + 视觉验收权限显式提示）

- `templates/intake-questions.md` / `05-intake.md`：交付形态去掉「迁移给同事」选项（迁移能力仍在 skill 的「交付与迁移」章节，不作为项目接入的交付形态）。
- 新增 `scripts/visual-qa-check.ps1`：探测 Chrome headless 截图是否可用（A 路径），校验 PNG 大小与像素；成功 exit 0；**权限/渲染受限 exit 2 并显式提示用户选 A（切 danger-full-access）/ B（用户截图 + read_image）/ C（标未实测 + 补测）**；Chrome 缺失/参数错 exit 1；`-SimulateBlocked` 仅用于验证提示话术。
- `50-design-team.md §3`：视觉 QA 前先跑探测脚本；补充「权限不足时必须显式提示用户」的 `ask_user_question` 话术模板；`SKILL.md` R6、命令区、文件地图同步。
- 验证：正常探测 exit 0（PNG 9,808 B、像素 16/32/48 与预期一致）；`-SimulateBlocked` exit 2 打印三路径提示；无效 Chrome 路径 exit 1；8 个脚本 BOM+Parser 通过。

## v2.1.1 — 2026-11-13（独立复验 P2 修复）

- `skill-status.ps1`：panel.json 的 installed 条目改为「逐条 try + PSObject.Properties 判空」，缺字段不再让整轮扫描静默中断。
- `package-skill.ps1` 的 PUBLISH-NOTES：明确「store.id 若仍为占位 handle，正式上架前用真实 `-Handle` 重打包」。
- `90-provenance.md §7` 时间线纠正（商店优先逻辑于 v2.1.0 引入并同版单测）。
- `CHANGELOG` 措辞纠正（R6/R13 改写、R15/R16 新增，不是「新增 4 条」）。
- 验证：独立 Reviewer v2.1.0 6/6 PASS；本版修复后重跑 `skill-status`/`package-skill` 与安装一致性检查。

## v2.1.0 — 2026-11-13（商店化更新 · Trae 工程匹配 · 接入模板 · 交接冒烟 · 三域 grill）

**起因**：用户将把 skill 上架技能商店，并追问 6 项：商店更新逻辑、Trae 工程匹配、专家问题模板、真实工程实测准备、浏览器权限结论、grill-me 三域覆盖。

**新增/变更**
- **商店化更新**：`skill-status.ps1` 重写为「商店优先」——读技能市场 `panel.json` 的 `installed[].name/version/latestVersion/origin/directory` 与 `installed.json`，与安装版 `version.json` 比对；`origin=manual` 说明「上架后由商店接管」；源目录对比仅开发机使用；新增 `-MarketData` 参数；**不自动更新、不覆盖商店安装版**。`version.json` 增加 `store` 元数据块。
- **发布打包**：新增 `scripts/package-skill.ps1`——校验 frontmatter name/description、version semver、CHANGELOG 条目、敏感信息/本机路径；生成 `manifest.json` + `SHA256SUMS.txt` + ZIP + `PUBLISH-NOTES.md`（含商店目录 `<handle>--<slug>` 约定）。
- **Trae 工程匹配**：`trae-status.ps1` 读取 `%APPDATA%\Trae CN\User\globalStorage\storage.json` 的 `windowsState.lastActiveWindow.folder` 与 `backupWorkspaces`，规范化比对 `-Workspace`；输出 `MATCH/MISMATCH/UNKNOWN`；新增 `-RequireMatch`（不匹配 exit 1）；`60-handoff.md` 步骤 1 设为硬门。
- **接入问题模板**：新增 `templates/intake-questions.md`（可粘贴 6 问 + 追问规则 + 默认/降级 + 反模式）；`05-intake.md` 明确「非全自动：不答进 D-ID」。
- **交接链路冒烟**：新增 `scripts/handoff-smoke.ps1`——在临时工程验证 new-handoff/空模板拦截/合规包 prepare+deliver/取证/DryRun 唤起/工程匹配；不碰真实项目。
- **真实工程实测清单**：新增 `templates/design-handoff-smoke.md`（明日按此把「设计驱动交接」从规则升级为已实测）。
- **三域 grill**：`75-grill.md` 扩为设计（界面+交互）/需求分析/自动化测试三套 12 问清单与接线；新增 `templates/grill-design.md`、`grill-requirement.md`、`grill-testing.md`；`grill-me` 在三域均优先加载。
- **浏览器权限结论**：`50-design-team.md` 更新——`workspace-write` 失败是 crashpad 权限/进程限制；`danger-full-access` 下 Chrome headless `--screenshot` 实测出图（1280×720，像素正确）；agent-browser 可截图但 `open` 挂起（后台+超时）。
- `SKILL.md` 不变式更新：新增「交接前工程匹配」「发布物可校验」，改写「浏览器路径」「商店更新边界」（R6/R13 改写，R15/R16 新增），文件地图/命令更新。

**验证（v2.1.0）**
- 7 个脚本 BOM + Parser 通过；`handoff-smoke.ps1` 在临时工程全链路 PASS（结束后清理）。
- `trae-status.ps1`：本机 `lastActiveWindow = <前端仓库>` → 对该路径 MATCH；对其它工程 MISMATCH（`-RequireMatch` exit 1）。
- `skill-status.ps1`：商店记录识别本 skill（`origin=manual`）；伪 `latestVersion` 比对逻辑单测；无源目录时正常降级。
- `package-skill.ps1`：源目录打包 → 校验通过、ZIP 生成、manifest/SHA256 齐全。
- Chrome headless：exit 0、PNG 7,494 B、页面背景/标题像素与预期一致。
- 独立 Reviewer 复验（v2.0.1 P0/P1 修复）PASS；v2.1.0 新增能力待其复验。

**回滚**
- 商店安装版：用商店「版本历史」回滚旧版本；手工版回退到 v2.0.1 副本。
- 新版仅增量能力，无破坏性变更。

## v2.0.1 — 2026-11-12（独立评审后的 P0/P1 修复）

**起因**：独立 Reviewer（未参与编写）按 11 项能力逐条实测，报 2 个 P0 + 6 个 P1；本版修复。

**P0 修复**
- **gate-check 编码误判**：`upgrade/team/gate-check.ps1` 的 `Read-Text` 由 `Get-Content`（PS5.1 默认 ANSI）改为 `[System.IO.File]::ReadAllText(..., UTF8)`；无 BOM 的 UTF-8 中文文档不再被误判为缺小节/缺评审/缺证据。
- **grill 口径矛盾**：`SKILL.md` 的「GRILL 未记录不 GATE」改为与实现一致——默认 WARN，交付前硬门用 `loop-gate.ps1 -RequireGrill`（缺失即 FAIL）；同时明确 `gate-check.ps1` 不校验 grill 内容，grill 由 loop-gate 负责。

**P1 修复**
- `skill-status.ps1` 更新命令：从「把源目录拷进安装目录」（嵌套复制）改为 `Copy-Item "$Source\*" -Destination $installed -Recurse -Force`，并加注释提醒。
- `10-audit.md` 九组字母与脚本一致（A 运行时 / B Skills / C 角色 / D profile / E 记忆 / F 桌面壳 / G 资产 / H 版本 / I 漂移）。
- `loop-gate.ps1` auto 识别：排除 `docs\handoff\`、不再把单独的 `brief.md` 判成 design（交接包不再被误判）。
- `capability-audit.ps1`：description 总字符 >5000 → WARN；用户偏好账 >120 天未更新 → WARN。
- 指标口径修正：catalog「14,950→3,673 −43%」措辞纠正为「磁盘 6,419→3,673（−43%）；catalog 注入估算 21 条约 14,950 → 12 条约 6k」。
- HTML 总览规则补充：`tools/build-docs-html.py` 是项目专用模板（改 PROJ/DOCS/标题 3 处常量），换项目必须改配置或写等价脚本。
- 新增 `templates/design-driven-acceptance.md`（UI 交接视觉 AC 六条 + 判定口径），`60-handoff.md §5` 引用。
- 文档一致性：QUICKSTART「六组」→「九组」；`60-handoff` 重复 §6 重编为 §7；`trae-status` 下一步措辞改为「brief/tasks/acceptance（record 验收后填）」。

**验证（v2.0.1）**
- 无 BOM 设计夹具：修 gate-check 后 PASS（此前误判 4 项 FAIL）。
- `loop-gate.ps1 -RequireGrill`：无 grill → FAIL(exit 1)；有 grill → PASS。
- `loop-gate.ps1` auto 对 `docs/handoff` 夹具：不再误判 design（SKIP）。
- `capability-audit.ps1 -Strict`：FAIL=0；用户偏好/字符阈值告警生效。
- `skill-status.ps1`：更新命令为不嵌套复制；安装版=源=2.0.1。

## v2.0.0 — 2026-11-12（能力补全：接入/上下文/grill/动态健康/更新提示）

**起因**：用户按 11 项能力逐条拷问「是否具备」，补齐缺口（见 `references/90-provenance.md` §6）。

**新增能力**
- **INTAKE 项目接入**：`references/05-intake.md` + `templates/project-profile.md`；≤6 问一次问完，产出项目画像并编排专家（能源叠加 `energy-pm-framework`、评审员、Designer/Reviewer、QA、Trae、grill）。
- **产品/设计上下文**：`scripts/product-context.ps1`（扫描框架/组件库/主题线索/页面接口规模）+ `references/55-design-intake.md` + `templates/design-context.md`；**出设计稿前强制**：先读现有系统主题/组件库/状态/样本页，再出稿；与现有体系冲突必须写差异。
- **自对抗评审 GRILL**：`references/75-grill.md` + `templates/grill-checklist.md`；优先加载 `grill-me`，12 问攻击清单 + 退出条件（≥1 个打回并修正）。
- **动态健康检测**：`capability-audit.ps1` 新增 G（Trae 关联）/H（版本与更新）/I（与上次快照漂移）三组，快照写 `<ws>\.tmp\capability-loop\audit-state.json`，下次自动对比 skills/字符/索引/补丁/检索/Trae/会话数变化。
- **更新提示**：`scripts/skill-status.ps1` 对比安装版与源目录版本/哈希，输出 `SOURCE-NEWER` 与手动更新命令；**不自动更新、不推送**。
- **Trae 关联可视化**：`scripts/trae-status.ps1` 报告 CLI/进程/交接包进度（brief/tasks/acceptance/evidence/record/结论）与下一步；只读，不自动唤起。
- **设计驱动开发**：`references/60-handoff.md` 新增 §5——UI 类交接必须带 `design-context.md`、UI 任务绑定设计依据、验收含视觉 AC、禁止引入新 UI 体系。
- **用户偏好记忆**：`references/85-ux-memory.md`；偏好写工作区 `memory/user-profile.md`，任务前读取，度量纠正/返工次数。
- **首次使用手册**：`QUICKSTART.md`（3 条命令、怎么开口、任务类型表、出问题看哪里）。
- **HTML 总览强制**：文档集交付必须生成单文件 HTML（搜索/目录/明暗双主题/打印/设计稿预览位）。

**行为变更（BREAKING）**
- `loop-gate.ps1` 的 **design 类别默认要求 `design-context*.md`**，缺失即 FAIL；确实不需要时用 `-AllowMissingDesignContext` 显式跳过并写理由。
- design/requirement/test 三类门禁均新增 `grill-*.md` 检查（缺失为 WARN，不阻断，但需在交付说明中解释）。
- `capability-audit.ps1` 组别由 6 组扩展到 9 组；`-Strict` 语义不变（有 FAIL → exit 1）。

**验证（v2.0.0 发布前）**
- 5 个脚本：UTF-8 BOM + `Parser::ParseFile` 通过；空跑不崩溃。
- `capability-audit.ps1`：源环境与安装版均 PASS=48 / WARN=10 / FAIL=0（`-Strict` exit 0）；第二次运行出现「I 漂移」对比（无指标变化）。
- `loop-gate.ps1`：design 缺 `design-context` → FAIL(exit 1)；补齐后 PASS；加 grill 记录后 grill 项 PASS；requirement/test 正反例通过。
- `product-context.ps1`：对真实前端仓库识别出 ant-design-vue / echarts / vben / tailwind，路由 44 / API 1154 / mock 32。
- `trae-status.ps1`：识别 Trae CLI `d:\Trae CN\bin\trae-cn.cmd`、4 个运行中进程、夹具交接包 PASS。
- `skill-status.ps1`：安装版=源=2.0.0 → UP-TO-DATE（-Strict exit 0）。
- `loop-gate.ps1 -Environment`：`post-restart-check` PASS（exit 0）。

**回滚**
- 本版为新增能力，回退到 v1.0.0 副本即可；`design-context` 硬门可用 `-AllowMissingDesignContext` 立即绕过。

## v1.0.0 — 2026-11-12（基线）

**来源（合并）**
- session-0d908c48：DSH 安装面审计 + P0 修复（检索/桌面壳）+ 插件与 skill 清理 + 生产级 UI 设计与团队契约 + 需求规格标准 + 系统证据驱动重建 + 实际示例（输差管理）+ 迁移交付包 v1.0。
- session-3ef140c9：DSH↔Trae 分工交接（`feature-handoff` skill + 四脚本 + 四模板 + prepare/deliver 门禁）。

**新增**
- 五阶段闭环（AUDIT → FIX → WIRE → HANDOFF → GATE）与 8 条不变式。
- 六组审计指标与度量口径。
- 需求、测试、设计团队、交接四套方法的接线。
- `references/70-playbook.md`：23 条已复现或高概率复现的坑。
- 自迭代协议（分层写回、semver、回归清单、健康度指标、拆分/淘汰、月度维护）。
- 脚本：`capability-audit.ps1`、`loop-gate.ps1`；模板：`templates/retro.md`；`references/90-provenance.md`。