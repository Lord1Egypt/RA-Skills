# 能力闭环（Capability Loop）

> 给 DeepSeek Harness 加一条「工程治理」轨道：被标记的工程在**每个会话首步**自动拿到一段短契约（阶段 / 当前门禁 / 阻断 / 下一步），侧边栏同时给出一个控制台：**看状态 + 跑门禁/体检/切档位**。

## 它做什么

| 部分 | 作用 | 在哪 |
|---|---|---|
| **注入（host）** | 在 `agent/pre-step` 把契约折进本步消息：`on` 档 ≈800 字符，`shadow` 档一行 | 会话里可见，无需操作 |
| **控制台（client）** | 侧边栏「能力闭环」面板：档位 / 阶段轨道 / 门禁列表 / 阻断 / 下一步 + **运行中心** | 左侧导航 |
| **动作（host 命令）** | `/capability-loop` 会话命令：门禁/体检/交接体检/预检/打包/视觉探测/版本检查/影子计数/切档位；面板按钮走同一实现 | 面板或命令行 |
| **状态源** | `.dsh/loop/state.json`，唯一写入方是 skill 的脚本 | 工程根下 |

三档：`off`（不注入）/ `shadow` 影子（只记录、不阻断）/ `on` 接管（治理场景必须 INTAKE/证据/门禁/grill）。档位取 `.dsh/loop/project.json` 的 `mode`，再被 `state.json` 覆盖。**没有 `project.json` 就不接管、面板也不会列它。**

## 看见面板

1. 安装后在 **Plugins** 页确认 `Capability Loop` 那一行是开的；
2. 左侧导航出现 **能力闭环**（图标是环形箭头）；
3. 点开就是控制台；没有已接入工程时显示接入命令。

面板数据经 `ctx.remote.session.list` 找会话（含 `cwd`），再用 `ctx.remote.workspaceFiles.read(sessionId, '.dsh/loop/…')` 读状态，**只读**。动作则走会话命令通道（见下）。

## 运行中心（面板动作）

面板 → `ctx.remote.commands.execute(sessionId, '/capability-loop …')` → Host 命令 handler → `actions.js`（白名单 + 参数校验）→ 子进程。

- 动作：`run gate kind=… taskDir=…` / `run audit` / `run handoff-audit slug=…` / `run preflight keyword=…` / `run pack handle=…` / `run visual` / `run skill-status` / `run sync-shadow` / `mode on|shadow|off`。
- 每个动作先确认（工程 + 完整命令 + 说明）；`Esc` 关闭、`Tab` 焦点循环；确认框与结果区都能复制命令/输出；运行中可取消（中止子进程）；输出只回尾部 40 行。
- **Host 命令在应用启动时注册**：改 `index.js`/`actions.js` 后需重启应用；改 `client.js` 刷新页面即可。

## 接入一个工程

```powershell
$sk = "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-state.ps1" -Action init -Root "<工程根>" -ProjectName "<工程名>"
```

生成 `.dsh/loop/project.json` + `state.json` + `.gitignore`，默认 `shadow`。切换档位：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-state.ps1" -Action set-mode -Root "<工程根>" -Mode on
```

## 配置（`cordis.patch.yml`）

| 键 | 默认 | 含义 |
|---|---|---|
| `defaultMode` | `off` | 工程缺少 `project.json.mode` 时的档位 |
| `maxContractChars` | 1600 | `on` 档契约字符上限（实测约 800） |
| `maxShadowChars` | 140 | `shadow` 档提示字符上限 |
| `shadowLog` | true | 是否写 `.dsh/loop/shadow-log.jsonl`（供 `sync-shadow` 计数） |
| `debug` | false | 把每次注入决策打进 host 日志 |
| `skillDir` | `''` | 可选：skill 目录，用于契约里「按需读哪一篇」的绝对路径 |

## 纪律

- **fail-open**：读文件/解析/构造任一失败都不注入，只记日志——治理不能把对话弄挂。
- **幂等**：注入消息带 `source.kind='capability-loop'` + 内容指纹，同批/历史/resume 都判重。
- **只读状态**：`state.json` 只由脚本写；插件只追加 `shadow-log.jsonl`。
- **面板只读**：不提供运行门禁、不改档位（这些后续版本再做）。

## 已验证 / 未验证

**已验证**
- 本机安装：`install_bundle`（pnpm link）→ `set_plugin` → `application: applied`。
- 真机会话收到 `shadow` 一行提示；影子日志记账；`sync-shadow` 计数。
- 夹具 `node --test`：11/11（三档、注入位置、resume/同批去重、fail-open、坏 JSON、无 dsh-llm 兜底）。

**未验证**
- 控制台在桌面版/浏览器里的实际渲染（首次装好后需要刷新页面让 client 半加载）。
- `on` 档在真实会话里的整段契约。
- Web UI 对 `source.kind='capability-loop'` 的渲染样式。
- 多工程切换时的面板选择状态。

## 已知限制

- 面板文字目前为中文硬编码（未接 locale 字典）。
- 面板只能读到 `~/.dsh/storages/workspace.json` 里登记过的工程；临时目录工程需手动加工作区。
- 只读：没有「运行门禁」「切档位」按钮。
