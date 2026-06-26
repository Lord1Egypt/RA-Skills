# ComfyUI MCP Skill

AI 视频生成技能，基于 ComfyUI 的 MCP 服务

## 功能

- 🎬 **视频生成** - 根据提示词生成 AI 视频
- 📖 **分镜生成** - 创建视频分镜脚本
- 🎞️ **视频合成** - 合并多个视频片段
- 📥 **视频下载** - 下载生成的视频
- 📊 **进度查询** - 查看生成任务进度

## 技术栈

- Python 3.10+
- FastMCP
- ComfyUI API
- Docker (可选)

## 安装

### 方式 1：从 GitHub 安装

```bash
cd /root/.nanobot/workspace/skills
git clone https://github.com/lemnt-ai/comfyui-mcp-server.git comfyui-mcp-skill
cd comfyui-mcp-skill
pip install -r requirements.txt
```

### 方式 2：Docker 部署

```bash
docker-compose up -d
```

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| COMFYUI_HOST | ComfyUI 服务器地址 | localhost |
| COMFYUI_PORT | ComfyUI 端口 | 8188 |
| LOG_LEVEL | 日志级别 | INFO |

### 配置文件

编辑 `config/config.yaml`：

```yaml
comfyui:
  host: localhost
  port: 8188
  timeout: 300

server:
  transport: http
  host: 0.0.0.0
  port: 18060
  path: /mcp
```

## 使用说明

### 启动服务

```bash
# HTTP 模式
python server.py --transport http --host 0.0.0.0 --port 18060

# stdio 模式
python server.py --transport stdio
```

### 工具调用示例

#### 生成视频
```python
generate_video(
    prompt="一个机器人在跳舞",
    duration=5,
    width=512,
    height=512,
    fps=12
)
```

#### 查询进度
```python
check_progress(prompt_id="xxx-xxx-xxx")
```

#### 下载视频
```python
download_video(prompt_id="xxx-xxx-xxx")
```

## 集成到 nanobot

在 nanobot 配置中添加：

```json
{
  "mcpServers": {
    "comfyui": {
      "command": "python",
      "args": ["/root/.nanobot/workspace/skills/comfyui-mcp-skill/server.py"],
      "cwd": "/root/.nanobot/workspace/skills/comfyui-mcp-skill",
      "env": {
        "COMFYUI_HOST": "localhost",
        "COMFYUI_PORT": "8188"
      }
    }
  }
}
```

## 依赖服务

### ComfyUI 安装

```bash
# 克隆 ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 安装依赖
pip install -r requirements.txt

# 启动
python main.py --listen 0.0.0.0 --port 8188
```

### 必要节点

- AnimateDiff
- ControlNet
- IPAdapter

## 工作流文件

工作流配置文件位于 `workflows/` 目录：

| 文件 | 说明 |
|------|------|
| video_workflow.json | 视频生成工作流 |
| storyboard_workflow.json | 分镜生成工作流 |
| compose_workflow.json | 视频合成工作流 |

## 常见问题

### Q: 视频生成失败？
A: 检查 ComfyUI 服务是否正常运行，端口是否正确。

### Q: 生成速度慢？
A: 视频生成依赖 GPU，确保有可用的 GPU 资源。

### Q: 如何自定义工作流？
A: 编辑 `workflows/` 目录下的 JSON 文件。

## 相关链接

- 原项目：https://github.com/lemnt-ai/comfyui-mcp-server
- ComfyUI: https://github.com/comfyanonymous/ComfyUI
- FastMCP: https://github.com/jlowin/fastmcp

## 版本历史

- v1.0.0 - 初始版本
  - 视频生成
  - 分镜生成
  - 视频合成
  - 进度查询

---

*创建时间：2026-03-17*
*版本：v1.0.0*
