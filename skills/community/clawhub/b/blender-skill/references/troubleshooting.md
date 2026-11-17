# Troubleshooting

Error table for the official Blender MCP add-on (v1.0.3) — last updated 2026-11-12 (skill v3.7.3) and the pinned server package. Issue numbers refer to https://projects.blender.org/lab/blender_mcp.

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `ConnectionRefusedError` | Blender not running or Addon not started | Start Blender, enable MCP Addon, click "Start Server" |
| `ConnectionRefusedError`（Blender 开着也没反应） | **Auto Start 只在 Blender 启动时触发** —— 刚装完 add-on 时状态仍是 "Server is stopped" | 手动点一次 **Start MCP Bridge Server**（之后 Auto Start 才会生效） |
| 端口被占 / 连上却不是自己的 Blender | **两个 MCP add-on 不能同时启用**（官方 Lab add-on 与社区 `blender-mcp` 都监听 **9876**） | 只留一个：Preferences → Add-ons 里禁用另一个；或改端口并同步 `BLENDER_MCP_PORT` |
| `Online access must be enabled in the system preferences` | Blender 的全局联网开关（官方 add-on 遵守该开关） | Preferences → **System → Network → Allow Online Access** |
| 装完在 Add-ons 里找不到 | 拖拽安装**需要拖两次**（第一次只加了 Blender Lab 仓库） | 再拖一次；或改用 Install from Disk |
| `ConnectionError: Empty response` | Network timeout or Addon crashed | Check Blender console output, verify port |
| `result is not JSON-serializable` | Returned a Blender object | Use `strict_json=False` or manually convert to dict |
| `Blender executable not found` | Blender command not found | Set `BLENDER_PATH` environment variable |
| `Deferred responses not supported` | Background mode doesn't support deferred responses | Use synchronous code or switch to GUI mode |
| **`*_for_cli` 工具在 Windows + stdio 下 120s 超时挂死** | `run_blender_cli()` 调 `subprocess.run()` 未传 `stdin` → 子进程继承 MCP 的 stdio 管道，Windows 上死锁（官方 issue **#58** / **#60**，修复 PR **#48 未合并**） | 仍有问题：给该处补 `stdin=subprocess.DEVNULL`（本地打补丁），或改用非 `*_for_cli` 的交互工具 |
| **`*_for_cli` 恒报 `Blender CLI timed out after 120s`，且一执行就打断正在跑的交互 Blender** | **另一套根因（官方 issue #72，2026-11-09，报告者推断、官方未确认）**：MCP add-on **在 background 模式也会启动 server**，与占用 **9876** 的交互实例**抢端口**，且**留非守护线程**使子进程跑完不退出。对照实验：`blender -b` 普通偏好 → 打印结果但**进程不退出**；`--factory-startup` → **≈1.8 s 正常退出**；`--factory-startup` + 约 55 个其他 add-on（不含 MCP）→ **≈5 s 正常**；`--factory-startup` + `bl_ext.lab_blender_org.mcp` 且交互实例占 9876 → **挂住 + 打断交互实例**。⚠️ 与 #58/#60（`stdin` 未传）、#69（Store 版 launcher 丢 stdout）**是三套不同根因，别混判** | ① 先**停掉交互 Blender 的 MCP server**（或临时禁用 MCP add-on / 改端口）再跑 `*_for_cli`；② 能不用 `*_for_cli` 就用交互式 `execute_blender_code`；③ `*_for_cli` **无法传 `--factory-startup`** → 要干净环境得自己起 `blender -b --factory-startup --python <script>` |
| `NameError: name 'bpy' is not defined` / 上次的变量不见了 | **`execute_blender_code` 每次调用都是全新 Python 命名空间**（`bpy` 不预导入、局部变量不跨调用保留；官方 issue **#55**/#53） | 每次调用**都写 `import bpy`**；需要跨调用状态就显式写回 `bpy` 数据或文件 |
| `get_objects_summary` 把上下文撑爆 | 输出随场景复杂度递归增长（1670 对象 ≈ 904 KB ≈ 15.5k+ tokens；官方 issue **#54**） | 大场景先用更轻的检查方式；必要时按集合分批查询 |
| 缩略图 / 渲染产物**不是**想要的分辨率或不在指定路径 | `render_thumbnail_to_path` 交互模式会用原分辨率渲染（issue **#46**/**#61**）。**根因（官方 PR #66，2026-10-22，未合并）**：上下文管理器在 `INVOKE_DEFAULT` job **返回时就恢复了设置**，而 job 真正执行在后面 → job 读到的是用户原设置；另 EEVEE 引擎标识未匹配 `BLENDER_EEVEE`。作者实测 main 1920×1080 / 1.6 MB / ~9 s → 打补丁 320×180 / 50 KB / 0.8~1.3 s。两个 `*_to_path` 工具**只取文件名的 basename**，实际写进 MCP 临时目录（issue #53） | 用工具返回的 `filepath` 读产物；要确定的分辨率就自己在 `execute_blender_code` 里设渲染参数并阻塞式渲染（**PR #66 合并前这是唯一可靠做法**） |
| `get_python_api_docs` 查成员文档查不到（`bpy.types.Object.location`） | 成员解析需要**重复类名**（官方 issue **#62**，2026-10-10） | 用 `bpy.types.Object.Object.location`；`bpy.ops.*` 和整类查询正常 |
| macOS 上 `.mcpb` 装不上（"Operation not permitted"） | Claude Desktop 的 `.mcpb` 安装助手与 uv cache 权限冲突（官方 issue **#57**） | macOS 走 **add-on + `uvx`** 路线，别依赖 `.mcpb` |
| Windows 上 `blender-mcp.exe` 被拦（`os error 4551` / Claude Desktop "MCP Blender: Server disconnected"） | **Smart App Control（SAC）enforcement 模式只放行「被 Microsoft 应用智能服务识别」或「受信任 CA 签名」的二进制**（Microsoft Learn 原文）→ **未签名的 `blender-mcp.exe` 必被拦**。⚠️ **2026-10-19 起确认：换成官方 MCPB 扩展也躲不过** —— 扩展自带 `.venv\Scripts\blender-mcp.exe` 同样 `NotSigned`、同样触发 Code Integrity event 3077（官方 issue **#56** 走 uv 安装 / **#65** 走官方扩展，两者同因） | **旧建议「改用官方 add-on / MCPB 通道」已被 #65 证伪，不要再用**。可行路径：① 先 `Get-AuthenticodeSignature .venv\Scripts\blender-mcp.exe` 确认是否 `NotSigned`（SAC 场景 100% 是）；② 让用户在 **SAC 状态**（设置 → 隐私和安全性 → Windows 安全中心 → 应用和浏览器控制）上做决定 —— 关闭 SAC 属高风险改动、企业域策略下不要动，**先确认再谈**；③ ⚠️ 待核验：SAC 是否支持「为单个应用加白名单」（据本机观察没有该入口，需查 Microsoft 文档确认后写死） |
| **扩展/服务器起不来，日志里是 `Failed to download <pkg>` + `invalid peer certificate: UnknownIssuer`** | **比 #56/#65 更早一层**：`uv` 建 venv 时要拉 wheel（`rpds-py` / `pydantic-core` / `pyyaml` 等，来自 `files.pythonhosted.org`），**本机 TLS 信任链被中间人拦截**（企业代理 / 杀软 HTTPS 扫描 / 自签 CA）→ 依赖装不上 → 表面现象仍是 "MCP Blender: Server disconnected"（官方 issue **#67**，2026-10-25） | **判据**：在客户端日志里搜 `invalid peer certificate: UnknownIssuer` 或 `Failed to download`，命中即属本类，**不要按 SAC 路径排查**。处置三选一：① 让 uv 走系统信任库 `UV_NATIVE_TLS=1`；② 指定企业根证书 `SSL_CERT_FILE=<ca.pem>`（uv 亦认 `REQUESTS_CA_BUNDLE` 同值）；③ 让代理/杀软对该域名关闭 HTTPS 解密，或临时直连。修完重跑一次 `uvx blender-mcp==1.0.3` 验证依赖可下载 |
| **Windows 多开 Blender：服务显示"已启动"、客户端却连到别的实例**（改了没反应 / 操作落到另一个窗口） | `mcp_to_blender_server.py` 在 `bind()` **之前**设了 `SO_REUSEADDR`；Windows 语义允许**第二个 socket 绑定已监听端口** → 第二个实例不报错，客户端始终连第一个（官方 issue **#63**，Win11 + Blender 5.2.2 LTS + blender_mcp 1.0.2 实测 20/20 复现；建议官方改用 `SO_EXCLUSIVEADDRUSE`） | **只开一个 Blender 实例**再启服务；或先关掉旧实例再 Start；排查时看端口占用（`netstat -ano \| findstr 9876`）而非只看按钮状态 |
| `The result variable must be a dict, not list. Wrap your return value: result = {"key": value}` | add-on **只接受 dict**；官方 server instructions / `prompts.yml` L48 声称可返回 "dicts, lists" 属**文案与实现不一致**（官方 issue **#64**） | 返回值**一律包成 dict**：`result = {"items": [...]}`；别按 instructions 返回裸 list |

> **查官方动态的正确姿势（2026-10-13 起，绕开 HTML 403）**：`projects.blender.org` 的**网页**长期 403，但**同一站点的 Gitea REST API 可用**：
>
> ```bash
> # 仓库 / 发布 / issue / PR（实测 2026-10-13 全部 200）
> https://projects.blender.org/api/v1/repos/lab/blender_mcp
> https://projects.blender.org/api/v1/repos/lab/blender_mcp/releases?limit=10
> https://projects.blender.org/api/v1/repos/lab/blender_mcp/issues?state=open&sort=recentupdate&limit=20
> https://projects.blender.org/api/v1/repos/lab/blender_mcp/pulls?state=open&limit=10
> ```
>
> 官方落地页 `https://www.blender.org/lab/mcp-server/` 一般可访问（给 add-on 版本号与安装要求）。
> ⚠️ **不要**用搜索摘要代替官方源：本工作区曾据此写下**不存在的 issue 号**（#344/#345/#348 实测 404），已作废。

---
