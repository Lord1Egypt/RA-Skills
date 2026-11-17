# MCP / Agent 接口

本技能为 Agent/上层应用提供三种稳定方式：**CLI JSON（无服务模式）**、**stdio MCP**、**Web UI/API**。
凭据一律不出口：系统凭据库密码、Cookie、Token 不会出现在任何 JSON/text 输出里。

配置优先级：`CLI 参数 > 环境变量 > config.json > 内置默认值`。
示例统一使用 `<api-url>`、`<download-dir>`、`<port>`、`<pan-root>`。

## 1. CLI JSON：无服务模式

不需要 Web UI 或 MCP 时，Agent 直接调用：

```bash
python3 <pan-root>/scripts/pan.py doctor --json
python3 <pan-root>/scripts/pan.py detect "<链接>"
python3 <pan-root>/scripts/pan.py get "<链接>" --dry-run --json
python3 <pan-root>/scripts/pan.py get "<链接>" --to <download-dir>
```

| 子命令 | 说明 |
|---|---|
| `pan.py doctor --json` | 环境与依赖检查 |
| `pan.py detect <url> [--json]` | 识别网盘（默认即 JSON） |
| `pan.py dirs --json` | 默认下载目录 |
| `pan.py secret check --json` | 凭据引用状态 |
| `pan.py secret list --json` | 配置中的凭据引用清单 |
| `pan.py get <url> --dry-run --json` | 下载计划（只读） |
| `pan.py get <url> --events` | 实际下载时逐步 JSON 事件流 |

## 2. stdio MCP 服务器

脚本：`scripts/pan_mcp.py`（纯 Python，无第三方依赖）。

暴露工具：

- `pan_get`：执行下载；默认 `dry_run=true`，只有在显式关闭 dry-run 时才实际落盘。
- `pan_task`：`list / pause / resume / cancel` 任务。
- `pan_get_plan`：只读生成 dry-run 计划，不读取凭据明文。

### Codex 配置

写入 `<codex-home>/config.toml`：

```toml
[mcp_servers.pan-cloud-drive]
command = "python3"
args = ["<pan-root>/scripts/pan_mcp.py"]
enabled = true
```

重启 Codex 后生效。

### 通用 MCP 客户端配置

```json
{
  "mcpServers": {
    "pan-cloud-drive": {
      "command": "python3",
      "args": ["<pan-root>/scripts/pan_mcp.py"]
    }
  }
}
```

一键查看本机路径：`python3 <pan-root>/scripts/pan.py mcp guide --json`。

## 3. 安全边界

- `pan_get_plan` 只生成计划，不执行下载、不读取系统凭据明文。
- `--events` 输出步骤参数全部打码；`content` 内不含密码/Token/Cookie。
- 参数中的 `pwd` 是分享提取码（非账号密码），仍按最小必要原则传递。
- MCP 不做上传、不做转发；实际执行发生在 Agent 运行环境或用户指定的本机/远端引擎。

## 4. Web UI / API

- 本机模式：`python3 <pan-root>/scripts/pan.py serve --host 127.0.0.1 --port <port>`，访问 `http://127.0.0.1:<port>`。
- NAS 模式：`http://<nas>:<port>`。
- 服务器模式：`http://<server>:<port>`。
- 公网或局域网暴露前确认防火墙、反代与访问控制；默认监听 127.0.0.1。
