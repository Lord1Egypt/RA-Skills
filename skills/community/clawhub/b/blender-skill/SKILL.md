---
name: blender-mcp
description: "Blender 工作台：① 连接运行中的 Blender（官方 Lab MCP 插件 + 固定版本服务进程，调场景/截图/渲染/文档工具，或直跑 bpy）；② 美术生产管线（资产命名与 collection 层级、面数/贴图/TD 预算、LOD 与碰撞、UV 与烘焙、材质灯光渲染、绑定动画、几何节点与 FX、引擎导出与 QA），配 asset_qa.py 一键审计、style_presets.py 一键落地 12 套 look。需要实时操控 Blender、做美术资产、转游戏资产、配导出或跑资产验收时使用。"
homepage: https://www.blender.org/lab/mcp-server/
author: taosiuman
version: 4.0.0
metadata:
  octop:
    emoji: "🔌"
    label:
      zh: "Blender 工作台"
      en: "Blender Workbench"
    summary:
      zh: "官方 MCP Server 接入（20+ 工具、bpy 直执行、无头渲染、排障）+ 美术生产管线（规格/预算/导出/QA + 两个可执行工具）。"
      en: "Official MCP server (20+ tools, live bpy, headless) plus art production pipeline with hard specs and two CLI tools."
---

# Blender 工作台（MCP 连接 + 美术生产管线）

Connect to and control a running Blender instance via the official Blender MCP Server, **and** run a spec-driven art production pipeline on top of it.

通过官方 Blender MCP Server 连接和控制运行中的 Blender 实例，**并**在同一套技能里按硬规格做美术资产（建模 → UV → 材质 → 灯光 → 绑定 → GN/FX → 导出 → QA）。

## 两条主线

| 我要… | 走去哪里 |
|---|---|
| 连上 Blender、截图、渲染、直跑 `bpy` | 本文 §Installation / §Tools（`references/{tools,protocol,api,troubleshooting,changelog}.md`） |
| 做一个道具/角色/场景/载具/建筑，要能交付 | `references/art-pipeline.md`（Stage 0–8 与每阶段过关判据） |
| 命名、collection 层级、面数/贴图/TD 预算 | `references/art-standards.md` |
| 建模（硬表面布尔、模块化 kit、载具/建筑/植被、雕刻重拓扑） | `references/art-modeling.md` |
| UV、接缝、texel density、烘焙、ORM 打包 | `references/art-uv-texture.md` |
| 材质与 lookdev、PBR 数值、master material | `references/art-materials-lookdev.md` |
| 灯光、相机、渲染设置、雾与合成 | `references/art-lighting-render.md` |
| 绑定、权重、动画帧数、毛发布料 | `references/art-rig-anim.md` |
| 几何节点、程序化、物理破碎与缓存 | `references/art-gn-vfx-sim.md` |
| LOD、碰撞代理、FBX/GLB/USD、Unity/UE/Godot 差异 | `references/art-optimize-export.md` |
| 交付前验收清单、缺陷分级、verdict 模板 | `references/art-qa.md` |
| 按参考图做，要对得上 | `references/art-reference-match.md` |
| 风格/世界观/情绪（赛博朋克、侘寂、liminal…） | `references/art-style-recipes.md` + `style_presets.py`（12 套可执行 look） |
| 通过 MCP 执行这些片段（批量 payload、超时与后台模式的坑） | `references/art-mcp-execution.md` |
| 覆盖面对照 / 第三方来源与 MIT 许可 | `references/art-coverage-map.md` / `references/art-NOTICE.md` |

### 两个可执行工具（都在 `generated/tools/`）

```bash
RT=C:\Users\haowe\.octop\portable\runtime\python.exe
BL53=generated\blender53\blender-5.3.0-windows-x64\blender.exe

# 资产只读审计（13 类检查、12 档阈值、退出码可接 CI）
"%BL53%" --background asset.blend --python generated\tools\asset_qa.py -- --tier standard --export-gate --json out\qa.json

# 风格一键落地（只建 COL_Lights_Style / COL_Cameras_Style / COL_Style_Fog，不碰几何）
"%BL53%" --background --factory-startup --python generated\tools\style_presets.py -- --look cyberpunk-rain --apply --scale 2 --save out\base.blend --json out\look.json
```

12 套 look：`cyberpunk-rain` `neon-noir` `golden-hour` `nordic-overcast` `liminal-fluorescent` `horror-cold` `cottage-warm` `desert-haze` `moonlit-night` `studio-product` `hd2d-diorama` `post-apoc-dust`

> 三个硬口径：① **雾必须用体积盒**（挂 World Volume 在 EEVEE 下背景全黑，实测亮度 0.0003）；② **导出前先取消集合外所有选择**，只 `use_selection=True` 会把上次选中的对象一起导出；③ **`asset_qa.py` 只读**、`style_presets.py` 只加灯/雾/相机 —— 都不改用户 mesh 数据。

**Version support**: Blender 5.1+（官方 add-on 的硬性要求）；**生产基准 = 5.3（5.3.0，2026-11-10 正式发布）**；**兼容下限 = 5.2 LTS（5.2.4，2026-11-10 发布）**；5.4 仍 Alpha（until 2027-02-03），只用 `hasattr` 兜底 — API compatibility notes included below
**Platform prerequisite**（2026-10-25 核验）: 官方 add-on 要求 **Blender ≥ 5.1**，而 Blender **5.0 起 macOS 只出 Apple Silicon 构建**（Apple Silicon + macOS 13 Ventura 起；`4.5 LTS` 是最后一个支持 Intel Mac 的版本）→ **Intel Mac 上不存在可用的「Blender 5.1+ × 官方 MCP」组合**；Windows / Linux 无此限制（Windows 需 4 核 SSE4.2 + OpenGL 4.3 或 Vulkan 1.3、8 GB RAM）
**Last verified**: **2026-11-18**（**v4.0.0 = 把原独立技能 `blender-art-pipeline` 整体并入本技能**：15 篇美术章节改为 `references/art-*.md`，主文件只加路由与三条硬口径，控制在扫描预算内；`asset_qa.py` 与 `style_presets.py` 均**双构建实测**（5.3.0 `02f0899d78e3` / 5.2.4 `cd5dc428cce1`），12 套 look 在 **EEVEE / Cycles** 各 12/12 通过；文档片段探针（材质骨架 + 先选集合再导出）双构建 PASS。更长的说明在同目录的 `references/`）

---

## ⚠️ Security Warning / 安全警告

**English:**
This skill provides full access to Blender's Python API (`bpy`) through the MCP channel. Code executed via `execute_blender_code` can:
- Read, modify, or delete files on your system
- Execute arbitrary Python code (including network requests)
- Alter or corrupt your Blender project data

**Always review code before execution. Keep backups of important `.blend` files.**

**中文：**
此技能通过 MCP 通道提供对 Blender Python API (`bpy`) 的完全访问。通过 `execute_blender_code` 执行的代码可以：
- 读取、修改或删除系统上的文件
- 执行任意 Python 代码（包括网络请求）
- 更改或损坏 Blender 项目数据

**执行前请始终审查代码。保持重要 `.blend` 文件的备份。**

---

## Architecture Overview

```
┌─────────────┐     TCP Socket      ┌──────────────────     MCP Protocol     ┌──────────────
│  LLM Client │ ◄─────────────────► │  MCP Server      │ ◄──────────────────► │   Blender    │
│  (OpenClaw) │    stdio / HTTP     │  (Python process) │    port 9876         │   (Addon)    │
└─────────────┘                     └──────────────────┘                      └──────────────
```

**Two-component architecture**:
1. **Blender Addon** — runs inside Blender, provides a TCP Socket Server (default `localhost:9876`)
2. **MCP Server** — standalone Python process that bridges the LLM client and the Blender Addon

---

## Installation

### 1. Install the Blender Addon

> **Requirements (official)**: **Blender 5.1 or newer**（官方 Lab 页原文）；官方 add-on 当前版本 **v1.0.3**（2026-10-11 复核，与 10-09 / 10-10 一致）。

**Option A: From ZIP** (official release / 官方发布)
1. Download addon ZIP: `https://projects.blender.org/lab/blender_mcp/releases/download/v1.0.3/mcp-1.0.3.zip`
   （或从官方落地页 `https://www.blender.org/lab/mcp-server/` 取最新链接）
2. Blender → Edit → Preferences → Add-ons → Install from Disk
3. Enable the MCP addon (listed as **MCP**, maintained by Blender Lab)
4. Confirm Host/Port in addon settings (default `localhost:9876`)
5. **Optional: Enable "Auto Start"** — ⚠️ 只在 **Blender 启动时**触发；刚装完状态仍是 "Server is stopped"，需手动点一次 **Start MCP Bridge Server**

**Option B: Drag & Drop**
- Drag the install link/ZIP into the Blender window **twice**: first drop adds the **Blender Lab repository**, second installs the addon
- 好处：之后能收到 add-on 更新通知

**Option C: From Source**
- Source code locations: `mcp/blmcp/` and `addon/blender_mcp_addon/`

**Option D: Quick Install via uvx** (Simplest / 最简单)
```bash
# Install uv first (safe method / 安全方法)
# Download installer and verify before running / 下载并验证后再运行
# Windows: download a release build from https://github.com/astral-sh/uv/releases
#          and review it before running.
# macOS/Linux: download a release build from https://github.com/astral-sh/uv/releases
#            and review it before running. Do not pipe an installer into a shell.

# Start MCP server with pinned version (auto-downloads dependencies)
uvx blender-mcp==1.0.0
```

> ⚠️ **别把两个版本号搞混**（真实高频困惑）：
> - **Blender add-on**（官方 Lab 发布，装在 Blender 里）：当前 **v1.0.3** —— 见上面 Option A 链接
> - **MCP Server 包**（`uvx`/`pip` 装的 Python 进程）：本文档 pin 在 **1.0.0**（PyPI 包 `blender-mcp`）
> 两者版本号各自独立；排障时先确认「哪一半」出问题。

> ⚠️ **分发渠道（2026-11-07 补，官方 issue #71）**：官方 `lab/blender_mcp` **没有发布到 PyPI** —— 官方只走两条渠道：
> ① **Blender Extensions / `.mcpb`**（`releases/download/v1.0.3/mcp-1.0.3.zip`，见 Option A/B）；
> ② **Git 源码**（`mcp/blmcp/` 直接用 `uv`/`pip install -e` 装）。
> PyPI 上的包名 `blender-mcp` 是**第三方实现**（同样用 TCP 9876 桥接，但代码基线不同），**不是 Blender 官方包**；
> 企业 MCP 注册表（Azure API Center 等）要登记官方实现时，请引用 **MCPB release URL**，别引用 PyPI 包名。
> Option D 的 `uvx blender-mcp==1.0.0` 命中的是 PyPI 那个第三方包 —— **要官方实现请走 Option A/B**。

### 2. Start the Blender MCP Server

```bash
# Install dependencies with pinned versions
cd path/to/blender_mcp
pip install mcp==1.8.0 pyyaml==6.0.2 starlette==0.45.0

# Start MCP Server (stdio mode)
python -m blmcp --transport stdio

# Or HTTP mode (default 127.0.0.1:8000)
python -m blmcp --transport http --host 127.0.0.1 --port 8000
```

### 3. Configure mcporter

```bash
# Add Blender MCP Server config
mcporter config add blender-mcp --transport stdio --command "python -m blmcp --transport stdio"

# Or use HTTP mode
mcporter config add blender-mcp --transport http --url "http://127.0.0.1:8000"

# Verify connection
mcporter list blender-mcp --schema
```

---

## Usage

### Method 1: Via mcporter (recommended)

```bash
# List all available tools
mcporter list blender-mcp --schema

# Call a specific tool
mcporter call blender-mcp.execute_blender_code code='import bpy; result = {"objects": [o.name for o in bpy.data.objects]}'

mcporter call blender-mcp.get_objects_summary
mcporter call blender-mcp.get_object_detail_summary object_name="Cube"

# Search API docs
mcporter call blender-mcp.search_api_docs query="bpy.ops.object.delete"

# Search user manual
mcporter call blender-mcp.search_manual_docs query="Geometry Nodes"

# Screenshot
mcporter call blender-mcp.get_screenshot_of_window_as_image

# Render viewport
mcporter call blender-mcp.render_viewport_to_path output_path="C:\\render.png"
```

### Method 2: Direct TCP Socket to Blender Addon (lightweight)

⚠️ **Warning**: This mode sends caller-supplied code directly to Blender with no guardrails. Review code before execution.

```python
import socket
import json

def send_to_blender(code: str, host="localhost", port=9876, timeout=30.0) -> dict:
    """Send Python code directly to Blender Addon for execution."""
    request = json.dumps({
        "type": "execute",
        "code": code,
        "strict_json": False,
    }) + "\0"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.sendall(request.encode("utf-8"))

        buf = bytearray()
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            buf.extend(chunk)
            if b"\0" in buf:
                break

    line, _, _ = buf.partition(b"\0")
    return json.loads(line.decode("utf-8"))

# Example: get all object names in the scene
response = send_to_blender(
    'import bpy\nresult = {"objects": [o.name for o in bpy.data.objects]}'
)
print(response)
# {"status": "ok", "result": {"objects": ["Cube", "Camera", "Light"]}}
```

### Method 3: Blender Background Mode (headless rendering / batch)

```bash
# Start Blender background MCP Server
blender --background myscene.blend --command blender_mcp --host localhost --port 9876

# Or execute code via CLI
blender --background myscene.blend --python-expr "
import bpy
# your code
result = {'count': len(bpy.data.objects)}
print('__BLMCP_RESULT__' + str(result))
"
```

---

## Built-in tools

The 20 official tools and their parameters are listed in [references/tools.md](references/tools.md).


## Communication protocol

TCP 9876 message shape and the two code examples are in [references/protocol.md](references/protocol.md). `result` must be a dict.


## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BLENDER_MCP_HOST` | `localhost` | Blender Addon host address |
| `BLENDER_MCP_PORT` | `9876` | Blender Addon port |
| `BLENDER_PATH` | `blender` | Path to Blender executable |
| `DISABLE_TELEMETRY` | `false` | Set to `true` to disable anonymous usage telemetry. **English:** Anonymous telemetry may be collected by default. Set to `true` to opt out. **中文：** 默认情况下可能会收集匿名遥测数据。设置为 `true` 可退出。 |

---

## Security Notes

⚠️ **Official security warning**: The MCP Server executes LLM-generated code with **no sandboxing**.

**Built-in weak sandbox** (`WeakSandboxForLLM`):
- Blocks `sys.exit()` calls
- Blocks dangerous operators: `wm.quit_blender`, `wm.read_factory_settings`, `wm.read_factory_userpref`, `wm.read_userpref`

### Security Best Practices

1. **Keep server local only** — Always use `localhost` / `127.0.0.1`; never bind to `0.0.0.0`
2. **Review code before execution** — Prefer scoped built-in tools over raw `execute_blender_code`
3. **Protect your projects** — Keep backups of important `.blend` files
4. **Verify external dependencies** — Download addon only from official Blender Lab sources

---

## Troubleshooting

The full error table (connection, SAC, TLS, port reuse, return type) is in [references/troubleshooting.md](references/troubleshooting.md).


## API compatibility notes

Breaking changes and version guards for Blender 5.1, 5.2 LTS (compatibility floor) and 5.3 (production baseline) live in [references/api.md](references/api.md). Read that file before writing version-sensitive `bpy` code.


## OpenClaw Integration

### Configure openclaw.json

```json
{
  "plugins": {
    "entries": {
      "mcp": {
        "servers": {
          "blender-mcp": {
            "command": "python",
            "args": ["-m", "blmcp", "--transport", "stdio"],
            "cwd": "path/to/blender_mcp",
            "env": {
              "BLENDER_MCP_HOST": "localhost",
              "BLENDER_MCP_PORT": "9876"
            }
          }
        }
      }
    }
  }
}
```

### Via mcporter CLI

```bash
# List tools
mcporter call blender-mcp.get_objects_summary

# Execute code
mcporter call blender-mcp.execute_blender_code code='import bpy; result = {"count": len(bpy.data.objects)}'
```

---

## Geometry Nodes MCP Integration

The official Blender MCP Server supports advanced Geometry Nodes inspection and debugging capabilities (Blender 5.2+):

### Querying Data Relations
```bash
# Find which objects use a specific material
mcporter call blender-mcp.execute_blender_code code='
import bpy
material_name = "pebbles"
users = [obj.name for obj in bpy.data.objects if obj.active_material and obj.active_material.name == material_name]
result = {"material": material_name, "users": users, "count": len(users)}
'
```

### Scene Debugging
```bash
# Find highest poly-count object in scene
mcporter call blender-mcp.execute_blender_code code='
import bpy
mesh_objects = [(obj.name, len(obj.data.polygons)) for obj in bpy.data.objects if obj.type == "MESH"]
if mesh_objects:
    highest = max(mesh_objects, key=lambda x: x[1])
    result = {"object": highest[0], "faces": highest[1]}
else:
    result = {"error": "No mesh objects found"}
'
```

### Geometry Node Tree Inspection
```bash
# Inspect Geometry Nodes modifier connections
mcporter call blender-mcp.execute_blender_code code='
import bpy
obj = bpy.data.objects["GEO-pebble"]
if obj.modifiers:
    mod = obj.modifiers[0]
    if mod.type == "NODES":
        node_tree = mod.node_group
        nodes_info = [{"name": n.name, "type": n.type, "inputs": [i.name for i in n.inputs]} for n in node_tree.nodes]
        result = {"modifier": mod.name, "node_tree": node_tree.name, "nodes": nodes_info}
    else:
        result = {"error": "Not a Geometry Nodes modifier"}
else:
    result = {"error": "No modifiers found"}
'
```

### Common Geometry Nodes MCP Patterns

| Task | Example Query |
|------|---------------|
| Find material users | `"Which objects use the material: [name]"` |
| Scene density analysis | `"Analyze mesh density distribution in this scene"` |
| Debug missing data | `"What is the object with the highest poly-count?"` |
| Node tree structure | `"Show me the Geometry Nodes connections for [object]"` |

---

## Gemini CLI Integration

Blender MCP can be used with Google Gemini CLI (in addition to Claude):

```bash
# Install Gemini CLI
npm install -g @google/gemini-cli

# Configure MCP via Gemini CLI's built-in command
gemini mcp add blender --transport stdio --command "uvx blender-mcp==1.0.0" --env BLENDER_MCP_HOST=localhost --env BLENDER_MCP_PORT=9876

# Start Gemini CLI with Blender MCP
gemini
```

**Security Note / 安全说明**: The `gemini mcp add` command automatically creates the configuration in the appropriate location. No manual file editing is required.

---

## Quick Start Checklist

- [ ] Blender 5.1+ installed
- [ ] MCP Addon installed and enabled
- [ ] **Auto Start enabled** (optional, recommended)
- [ ] MCP Server started (`python -m blmcp --transport stdio` or `uvx blender-mcp==1.0.0`)
- [ ] mcporter installed (`npm install -g mcporter`)
- [ ] Port 9876 available (default)
- [ ] `BLENDER_PATH` environment variable set (if needed)
- [ ] `DISABLE_TELEMETRY=true` (optional, for privacy)

---

## Changelog

Full history: [references/changelog.md](references/changelog.md).

