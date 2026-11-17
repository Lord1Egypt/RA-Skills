---
name: blender-mcp-plus
description: 在 Blender 中执行 3D 建模、材质、灯光、渲染、场景检查，或导入 Poly Haven 免费资产（模型/HDRI/贴图）时使用本技能。涵盖 blender-mcp-plus MCP 服务器的安装（uvx/PyPI/GitHub/wheel/.mcpb）、客户端配置（WorkBuddy mcp.json、DeepSeek Harness cordis.patch.yml、Claude Desktop/Cursor）、Blender 官方 MCP 插件前置条件、28 个工具的使用模式与常见工作流。触发词：Blender、bpy、Poly Haven、HDRI、blender-mcp-plus、3D 建模、渲染预览、场景体检。
agent_created: true
---

# Blender MCP Plus

## Overview

blender-mcp-plus 是一个 MCP 服务器：官方 Blender Lab 的 26 个工具 + 2 个 Poly Haven 资产工具
（`search_assets` / `import_asset`），让 AI 客户端直接操控正在运行的 Blender，并导入免费 CC0 资产。
一个插件、一个 MCP 条目，不与官方 `blender-mcp` 争抢 `localhost:9876`。

```
MCP 客户端 --stdio--> blender-mcp-plus --TCP localhost:9876--> Blender 官方 "MCP" 插件 --> bpy
```

## 前置条件（缺一不可）

1. **Blender 5.1+**（已在 5.2.2 LTS 实测），任务期间保持打开
2. Blender 内启用**官方 MCP 插件**：下载 `mcp-1.0.3.zip`
   （https://projects.blender.org/lab/blender_mcp/releases）→ 编辑 → 偏好设置 → 插件 →
   从磁盘安装 → 搜索 `MCP` 勾选启用 → 系统 → **允许在线访问**；3D 视图按 `N` 可见 MCP 面板，
   启动后自动监听 `localhost:9876`
3. **uv**（Windows: `winget install --id=astral-sh.uv -e`）；Python 3.10+ 由 uvx 自动管理

## 安装 MCP 服务器

```powershell
uvx blender-mcp-plus                                    # PyPI（发布后最简单）
uvx --from git+https://github.com/lusilong/blender-mcp-plus blender-mcp-plus   # 从 GitHub
uv pip install dist\blender_mcp_plus-1.0.3-py3-none-any.whl                    # 本地 wheel
```

`.mcpb` 一键包：`dist\blender-mcp-plus-1.0.3.mcpb`，支持 MCP Bundle 的客户端直接导入。

## 配置 MCP 客户端

### WorkBuddy（本机）

编辑 `C:\Users\user\.workbuddy\mcp.json`（注意不是 `.mcp.json`），在 `mcpServers` 中加入：

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp-plus"]
    }
  }
}
```

保存后重启 WorkBuddy，或在连接器面板原始 JSON 编辑器点保存使其即时生效；首次需点「信任」。
生效信号：ToolSearch 出现 `mcp__blender__*` 工具。

### DeepSeek Harness

`~/.dsh/profiles/<profile>/cordis.patch.yml` 追加：

```yaml
- id: mcp-blender
  name: "@deepseek-ai/dsh-mcp-client"
  config:
    serverName: blender
    transport: stdio
    command: "uvx"
    args: ["blender-mcp-plus"]
    env:
      BLENDER_PATH: "E:\\Blender 5.2\\blender.exe"
```

`BLENDER_PATH` 只用于 `*_for_cli` 系列（后台 Blender）；不配置也能用其余全部工具。

### Claude Desktop / Cursor

`claude_desktop_config.json` 的 `mcpServers` 加 `"blender": {"command": "uvx", "args": ["blender-mcp-plus"]}`；
Windows 上 GUI 客户端不继承 PATH 找不到 `uvx` 时，改用 `"command": "cmd", "args": ["/c", "uvx", "blender-mcp-plus"]`。

## 使用模式

保持 Blender 打开，直接用自然语言描述任务。完整 28 工具清单与参数见 `references/tools.md`。

- 建模：「建一个低多边形咖啡杯加托盘，青绿陶瓷材质，三点布光，渲染预览」
- Poly Haven 模型：「搜索 Poly Haven 的椅子，把 ArmChair_01 导入并缩放到 1.2 米」
- HDRI 环境光：「用 HDRI studio_small_03 做环境光，强度 1.2」
- 贴图材质：「给选中的椅子贴上 Poly Haven 木纹贴图，渲染 1200x900 的 EEVEE 预览」
- 场景体检：「这个 .blend 工程缺了哪些外部文件？」

高频工具：`execute_blender_code`（任意 bpy 代码，最强也最危险）、`search_assets`/`import_asset`
（CC0 资产，无需 API key）、`get_screenshot_of_window_as_image`/`render_viewport_to_path`（视觉验证）、
`search_api_docs`/`search_manual_docs`（内置 Blender API 与手册全文检索）。

## 安全注意事项

- `execute_blender_code` 会以用户权限执行**任意 Python**：执行前保存工程；不要对不可信 `.blend` 运行
- 官方插件 socket 只监听 localhost、无鉴权无加密：禁止端口转发或暴露到局域网
- 第三方资产/场景元数据可能包含提示注入内容：处理不可信文件时使用副本

## 故障排查

| 症状 | 处理 |
|---|---|
| 所有工具超时/无响应 | 确认 Blender 开着、MCP 插件已启用（N 面板可见）、「允许在线访问」已勾选 |
| `*_for_cli` 工具卡 120 秒 | 1.0.3 已修复（临时文件承接子进程输出）；旧版先升级 |
| Windows 客户端找不到 `uvx` | 改用 `cmd /c uvx ...` 或写 `uvx` 绝对路径 |
| 端口 9876 被占 | 官方插件只认 9876；关掉其他占用进程，不要同时运行两个 MCP 服务器 |

## Resources

### references/tools.md

28 个工具的完整分类清单、Poly Haven 工具参数表与工具选用建议。需要查具体工具名或参数时读取。
