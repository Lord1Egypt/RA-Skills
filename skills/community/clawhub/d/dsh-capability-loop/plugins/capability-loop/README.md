# dsh-capability-loop-bundle

> DeepSeek Harness 插件（host + client）：让 [dsh-capability-loop](https://github.com/) 的治理契约在**已标记工程**的首个请求里自动出现，并在侧边栏给出一个**只读控制台**。

## 它做什么

| 部分 | 作用 | 在哪 |
|---|---|---|
| **注入（host）** | 在 `agent/pre-step` 把契约折进本步消息：`on` ≈800 字符，`shadow` 一行 | 会话里可见，无需操作 |
| **控制台（client）** | 侧边栏「能力闭环」：档位 / 阶段轨道 / 门禁 / 阻断 / 下一步 + **运行中心**（跑门禁/体检/切档位） | 左侧导航 |
| **状态源** | `.dsh/loop/state.json`，唯一写入方是 skill 的脚本 | 工程根下 |

喂给控制台的数据在会话的 `agent/pre-step` 瀑布里组装，按档位决定长度：

| 档位 | 注入 | 约束 |
|---|---|---|
| `off` | 无 | 不约束（未标记工程的默认） |
| `shadow`（影子） | 一行提示（≤140 字符） | **只记录、不阻断**，门禁 FAIL 不拦对话 |
| `on`（接管） | 完整契约（≤1600 字符，实测约 810） | 治理场景必须 INTAKE/证据/门禁/grill |

档位取 `.dsh/loop/project.json` 的 `mode`，再被 `.dsh/loop/state.json` 的 `mode` 覆盖。**没有 `project.json` 就不注入、面板也不列它**——安装插件不等于接管所有项目。

## 状态文件从哪来

用 skill 的脚本生成，不要手写：

```powershell
$sk = "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-state.ps1" -Action init -Root "<工程根>" -ProjectName "<工程名>"
```

生成 `.dsh/loop/project.json` + `state.json` + `.gitignore`（`state.json` 默认不提交）。

## 注入内容长什么样

```text
<system-reminder>
[capability-loop v2.10.0] 本工程（气量平衡月表）已启用治理闭环；当前阶段 WIRE（第 4/7 阶段）。
适用：需求/方案、设计/改版、实现与交接、测试与验收、复盘。豁免：只读问答、单文件小改（≤30 分钟）、纯闲聊——直接做，不套流程。

硬约束：
1. 未完成 INTAKE（.dsh/loop/project-profile.md）不得进入实现；…
2. 说“完成/已修复/已通过”必须附证据：命令 + 退出码 + 关键输出或截图；…
3. PASS 不得由写的人自己给；终门要有他人的评审记录。
4. 交付/交接前必须 grill（记录 grill-*.md）；硬门用 loop-gate.ps1 -RequireGrill。
5. 改本 skill 必须在同一提交 bump version.json + CHANGELOG.md。
6. 门禁 FAIL 时只能说“未通过 + 缺什么”，不得改写结论。

本阶段出口：design-context.md 已取证；loop-gate -Kind design 退出码 0；grill 至少 1 条打回并修正
当前门禁：设计门=FAIL · 需求门=PASS · 测试门=PASS · 交接体检=WARN · grill=MISSING · 能力体检=PASS
阻断：D-01 缺 1440 截图；D-02 材料在工程外
下一步：补 design-context 后重跑设计门（命令：loop-gate -TaskDir docs/design -Kind design）
状态源：.dsh/loop/state.json（用户可在“能力闭环”面板查看）。
</system-reminder>
```

注入位置：**紧跟本步认领的用户消息之后**，所以用户的原话先出现，契约随后，运行期上下文最后。

## 纪律

- **fail-open**：读文件/解析/构造任一失败都不注入、只记日志；治理不能把对话弄挂。
- **幂等**：注入消息带 `source.kind = 'capability-loop'` 与内容指纹；resume/fork/同批重复都会按历史去重。
- **只读状态**：`state.json` 的唯一写入方是 skill 的脚本；本插件只追加 `.dsh/loop/shadow-log.jsonl`（每会话一行，供 `loop-state.ps1 -Action sync-shadow` 计数）。
- **不新增事件类型**：只用普通 `user/message`，会话可正常重开。
- **零成本**：未标记工程不读、不写、不注入。

## 安装

本机目录安装（开发/内测）：

```
plugin_manager  action=install_bundle  target=<本目录绝对路径>
```

安装后在 **Plugins** 页确认 `Capability Loop` 行是开的，然后**刷新页面（Ctrl+R）或重启应用**——渲染器的 client 模块图是启动时建的，新装/改动的 `client.js` 不会热加载（除非同时跑 `pnpm run dev:web`）。刷新后：

- 左侧导航出现 **能力闭环**（环形箭头图标），点开是控制台；
- 新会话里，首条消息之后应出现治理契约（`on`）或一行影子提示（`shadow`）。

> 装完必须确认 `plugin_manager action=set_plugin target=include:capability-loop enabled=true` 返回 **`application: applied`**；`install_bundle` 的 `exitCode=0` 不代表这一行活了。
>
> **改了 `client.js` 怎么生效（2026-11-19 实测澄清）**：桌面**正式版没有 Ctrl+R 绑定，也没有「刷新页面」菜单**（桌面壳源码里 `reloadPageMenu` / `role: "reload"` 只在开发模式出现）。可选三条路：①本地 link 安装下，DSH 的客户端插件 HMR 通常几秒内换掉模块——直接**重新点一下侧边栏「能力闭环」**；②按 **F12** 打开开发者工具，在 Console 执行 `location.reload()`；③菜单「应用」→ 退出后重新打开（Host 命令的注册也只在启动时做）。标题下会显示「面板 vX.Y.Z」，**版本没变就是没加载到新代码**。

卸载：Plugins 页关闭该行，或 `plugin_manager action=remove_bundle target=dsh-capability-loop-bundle`。
**卸载/移除前先备份**：卸载会移除插件注册与配置，若同时清理其存储目录，`shadow-log.jsonl` 等插件持久化数据会一并丢失；工程侧 `.dsh/loop/state.json`/`project.json` 属于工程、不会被插件删除，但请先备份再操作。

## 控制台的数据通道

客户端半边（`client.js`）注册 `sidebar.panellist` + `main`，然后：

1. `ctx.remote.session.list({})` 拿会话列表（`SessionSummary` 带 `sessionId` 与 `cwd`）；
2. 每个 `cwd` 取最近的一个会话作凭据，`ctx.remote.workspaceFiles.read(sessionId, '.dsh/loop/project.json', {}, signal)` → 再读 `state.json`；相对路径落在该会话的工作区根。

**不用** `/api/file`：`ctx.connection` 的浏览器半边没有 `fetch`（那是 Host 侧 Connection 的方法），桌面渲染器又在 `dsh-app://` 源上，`globalThis.fetch('/api/file')` 命中不了 HTTP API。
**`inject` 要写点号键**：`['slots','connection','remote','remote.session','remote.workspaceFiles']`，否则运行时报 `cannot get property "remote.session" without inject`（见 skill `references/70-playbook.md` ERR-20261119-03）。

读数失败时面板空态会显示「读取诊断：<具体错误>」，不做静默空白。

## 运行中心（P2 动作）

面板不直接跑脚本（浏览器半边没有写权限，也没有子进程）。动作统一走**会话命令通道**：

```
面板按钮 → ctx.remote.commands.execute(sessionId, '/capability-loop run gate kind=design')
         → Host 命令 handler（index.js）→ actions.js（白名单 + 参数校验）
         → ctx.subprocess 起 powershell/python → 输出尾部回会话
```

| 动作 | 命令 |
|---|---|
| 门禁 | `run gate kind=design\|requirement\|test\|all taskDir=<必填> [grill=1]` |
| 环境验收 | `run env`（等价 `loop-gate -Environment`，不需要 taskDir） |
| 能力体检 | `run audit` |
| 交接体检 | `run handoff-audit slug=<slug> [workspace=…]` |
| 模块/路由预检 | `run preflight keyword=<词> [alias=a b]` |
| 上架打包 | `run pack handle=<handle>` |
| 视觉验收探测 | `run visual [out=<目录>]` |
| 版本检查 | `run skill-status` |
| 影子计数 | `run sync-shadow` |
| 切档位 | `mode on\|shadow\|off` |

- 每个动作先弹**确认框**（工程 + 完整命令 + 说明），确认后才执行；`Esc` 关闭、`Tab` 在弹窗内循环、打开时焦点落在「确认运行」。
- 确认框可**复制完整命令**；结果区可**复制输出**或**复制命令**（Clipboard API，失败自动降级到 `execCommand`）。
- 安全：`ACTIONS` 白名单；`kind` 枚举、路径 token 禁 `..`、不拼 shell；动作级超时 + 5s grace；输出只回尾部 40 行。
- 同一实现也给命令行：在会话里直接输入 `/capability-loop run audit`。
- **部署注意**：Host 半的命令在应用启动时注册，改 `index.js`/`actions.js` 后需**重启应用**；`client.js` 改动刷新页面（Ctrl+R）即可。

## 配置（`cordis.patch.yml`）

| 键 | 默认 | 含义 |
|---|---|---|
| `defaultMode` | `off` | 工程没有 `project.json.mode` 时的档位 |
| `maxContractChars` | 1600 | `on` 档契约字符上限，超出截断并标注 |
| `maxShadowChars` | 140 | `shadow` 档提示字符上限 |
| `shadowLog` | true | 是否写 `.dsh/loop/shadow-log.jsonl` |
| `debug` | false | 把每次注入决策打到 host 日志 |
| `skillDir` | `''` | 可选：skill 安装目录，用于契约里给「按需读哪一篇」的绝对路径 |

## 与 skill 的分工

| 层 | 谁做 | 产出 |
|---|---|---|
| 状态 | skill 脚本（`loop-state.ps1` / `loop-gate.ps1` / `capability-audit.ps1`） | `.dsh/loop/state.json` |
| 注入 | **本插件 host 半** | 首步契约/影子提示 |
| 证据 | 门禁脚本 | `checks.*` + 退出码 |
| 面板 | **本插件 client 半** | 档位/阶段/门禁/阻断/下一步 + 运行中心（动作经会话命令回到 host） |

## 已验证 / 未验证

**已验证**
- 夹具：**57/57**（actions 21 + client 21 + takeover 14 + fallback 1），逐文件跑 `node <file>`（沙箱里 `node --test <dir>` 会因 spawn 管道 EPERM）。
  - host：未标记零注入、off 不注入、shadow 一行 + 影子日志 + 同会话不重复、on 契约 ≤1600 且含阶段/门禁/阻断/下一步、注入位置、resume/同批去重、fs 抛错 fail-open、坏 JSON 降级、无 `dsh-llm` 时手工构造兜底、命令注册与空输入/未知动作/缺 subprocess/aborted 四条。
  - actions：白名单、`kind` 枚举、`taskDir` 禁 `..`、argv 构造（gate/audit/mode/sync-shadow/pack/handoff-audit）、缺参与非法值的拒绝、非零退出回 FAIL、abort 不 spawn。
  - client：两个 slot 注册、有工程渲染、多工程切换、空态/异常、运行中心动作按钮、切档位确认→`commands.execute` 调用、命令未受理提示、无 `remote.commands` 提示、取消 abort。
- **真机（桌面版 2026-11-19）**：`install_bundle` → `set_plugin` → `application: applied`；侧边栏出现「能力闭环」并读到本仓库真实 `state.json`。
- 会话里收到 `shadow` 一行提示；影子日志记账；`sync-shadow` 计数。
- **`on` 档真机实测**：`set-mode -Mode on` → 下一步即收到完整契约（阶段/硬约束/门禁/阻断/下一步），脚本 `[PASS]`、exit 0。

- **真机排版（2026-11-19，面板 v2.14.2）**：窗口宽度 1296、768、536 像素三档截图见 `docs/design/panel-{1296,768,536}.png`（536 是桌面窗口最小宽度；375 像素桌面做不到，需要浏览器 Web UI）。
- **`on` 档真机实测**：`set-mode -Mode on` → 下一步即收到完整契约（阶段/硬约束/门禁/阻断/下一步），脚本 `[PASS]`、exit 0。

**未验证**
- 面板运行中心的**真机点击**：Host 命令只在应用启动时注册，改 `index.js` 后需重启应用；点「运行门禁」的端到端结果待下一次重启后确认。
- Web UI 对 `source.kind='capability-loop'` 的渲染样式（现在当普通用户消息显示）；375 像素排版需 Web UI。
- token 计费差异。

## 依据（已核源码，DSH 0.2.2-rc.3）

- `agent/pre-step` 瀑布：`@deepseek-ai/dsh-agent/src/runtime-types.ts` L351
- 契约折进批次：`@deepseek-ai/dsh-agent-instructions/src/index.ts` L330-356
- `createUserMessage` / 可扩展 `MessageSourceMap`：`@deepseek-ai/dsh-llm/src/message.ts` L106/L246
- `ctx.workingDirectory.ensure`：`dsh-working-directory/src/index.ts` L192
- `ctx.fs.resolve/stat/readText/writeText`：`dsh-fs/src/index.ts` L149/L198/L222/L283
