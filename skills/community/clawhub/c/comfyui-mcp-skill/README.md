# 🎬 ComfyUI MCP Skill

> AI 视频生成技能 - 让 AI 帮你创作视频内容

[![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)](https://clawhub.ai)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)

---

## ✨ 功能特性

- 🎬 **文生视频** - 输入提示词，自动生成 AI 视频
- 📖 **分镜生成** - 自动创建视频分镜脚本
- 🎞️ **视频合成** - 合并多个视频片段
- 📥 **视频下载** - 一键下载生成的视频
- 📊 **进度查询** - 实时查看生成进度

---

## 🚀 快速开始

### 前置要求

1. Python 3.10+
2. ComfyUI 服务（本地运行）
3. Node.js 18+（用于 ClawHub CLI）

### 安装

```bash
# 1. 克隆技能
cd /root/.nanobot/workspace/skills
git clone https://github.com/lemnt-ai/comfyui-mcp-server.git comfyui-mcp-skill

# 2. 安装依赖
cd comfyui-mcp-skill
pip install -r requirements.txt

# 3. 配置 ComfyUI
# 编辑 config/config.yaml，设置 ComfyUI 地址
```

### 启动

```bash
# HTTP 模式（推荐）
python server.py --transport http --host 0.0.0.0 --port 18060

# stdio 模式
python server.py --transport stdio
```

### 集成到 nanobot

在 nanobot 配置中添加：

```json
{
  "mcpServers": {
    "comfyui": {
      "command": "python",
      "args": ["server.py", "--transport", "http", "--port", "18060"],
      "cwd": "/root/.nanobot/workspace/skills/comfyui-mcp-skill"
    }
  }
}
```

---

## 📖 使用示例

### 生成视频

```
帮我生成一个视频：一个机器人在跳舞，时长 5 秒
```

### 查询进度

```
查看视频生成进度，prompt_id 是 xxx
```

### 下载视频

```
下载生成的视频，prompt_id 是 xxx
```

---

## 🔧 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `COMFYUI_HOST` | ComfyUI 服务器地址 | `localhost` |
| `COMFYUI_PORT` | ComfyUI 端口 | `8188` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

### 配置文件

`config/config.yaml`:

```yaml
comfyui:
  host: localhost
  port: 8188
  timeout: 300

server:
  transport: http
  host: 0.0.0.0
  port: 18060
```

---

## 📦 工具列表

| 工具 | 描述 | 参数 |
|------|------|------|
| `generate_video` | 生成 AI 视频 | prompt, duration, width, height, fps |
| `generate_storyboard` | 生成分镜 | prompt, scenes |
| `compose_video` | 合成视频 | video_list, output_name |
| `download_video` | 下载视频 | prompt_id |
| `check_progress` | 查询进度 | prompt_id |

---

## 🐳 Docker 部署

```bash
# 使用 docker-compose
docker-compose up -d

# 查看日志
docker-compose logs -f
```

---

## ❓ 常见问题

### Q: 视频生成失败？
**A:** 检查 ComfyUI 服务是否正常运行，端口是否正确。

### Q: 生成速度慢？
**A:** 视频生成依赖 GPU，确保有可用的 GPU 资源。

### Q: 如何自定义工作流？
**A:** 编辑 `workflows/` 目录下的 JSON 文件。

---

## 🔗 相关链接

- [原项目](https://github.com/lemnt-ai/comfyui-mcp-server)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [ClawHub](https://clawhub.ai)

---

## 📄 许可证

MIT License

---

*创建时间：2026-03-17*
*版本：v1.0.0*
