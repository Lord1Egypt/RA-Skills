---
name: douyin-automation
description: 抖音内容自动化运营技能。跨平台（Windows/macOS/Linux），一键安装，自动 clone 后端代码并配置，流水线执行：抓取AI量化视频→AI改写→发布长图文→自动回复评论。支持 Cron 定时任务。
---

# Douyin-Automation 抖音自动化运营

## 🚀 一键安装（2条命令）

```bash
# 1. 安装 skill（自动安装所有依赖）
clawhub install douyin-auto-hnc

# 2. 全自动引导（自动 clone 后端 + 配置路径 + 健康检查）
python ~/.qclaw/skills/douyin-automation/scripts/setup.py
```

> **macOS/Linux 用户**：路径为 `~/.qclaw/skills/douyin-automation/scripts/setup.py`

---

## 完整流程

```
安装 skill → setup.py (自动 clone 后端) → start-backend.py (启动服务)
                                                        ↓
                                                 run-pipeline.py (执行发布)
```

### 第1步：安装
```bash
clawhub install douyin-auto-hnc
```

### 第2步：运行 setup.py（全自动）
```bash
python ~/.qclaw/skills/douyin-automation/scripts/setup.py
```

setup.py 自动完成：
- 从 GitHub clone `douyin-agent-master` 后端代码到 `~/douyin/`
- 复制 creator-tools 到 `~/.openclaw/douyin-creator-tools/`
- 安装 Python 依赖（requests, playwright 等）
- 交互式确认端口和路径配置
- 生成 `CONFIG.md`
- 运行健康检查

### 第3步：启动服务（一键）
```bash
python ~/.qclaw/skills/douyin-automation/scripts/start-backend.py
```

- 自动启动 Chrome（带 `--remote-debugging-port`）
- 自动启动 FastAPI 后端（端口 8080）
- 如果端口已被占用则跳过（已运行）

### 第4步：执行流水线
```bash
# 正式运行
python ~/.qclaw/skills/douyin-automation/scripts/run-pipeline.py

# 试运行（不实际发布）
python ~/.qclaw/skills/douyin-automation/scripts/run-pipeline.py --dry-run

# 禁用 AI 优化（直接发布原始内容）
python ~/.qclaw/skills/douyin-automation/scripts/run-pipeline.py --no-ai
```

### 第5步：配置定时任务（可选）
```bash
# 抖音运营流水线，每 6 小时执行
openclaw cron add "DOUYIN-PIPELINE-6H" \
  --cron "0 */6 * * *" \
  --message "执行: python ~/.qclaw/skills/douyin-automation/scripts/run-pipeline.py"

# 抖音评论回复，每 30 分钟执行
openclaw cron add "DOUYIN-COMMENTS-30M" \
  --cron "*/30 * * * *" \
  --message "执行: python ~/.qclaw/skills/douyin-automation/scripts/run-pipeline.py --comments-only"
```

---

## 系统架构

```
GitHub: HNC87/douyin-agent-master
  ↓ clone 到 ~/douyin/
  ↓
douyin-agent-master/backend/    (FastAPI :8080)
douyin-agent-master/orchestrator/douyin_full_orchestrator.py
  ↓
douyin-creator-tools/
  publish-douyin-article.mjs   → 发布到抖音
  export-douyin-comments.mjs   → 导出未回复评论
  reply-douyin-comments.mjs    → 自动回复
  ↓
OpenClaw Gateway (http://127.0.0.1:28789)
  → AI 改写内容（openclaw/default 模型）
```

---

## 手动前提条件

**必须提前准备（setup.py 无法自动化）：**

1. **Chrome 浏览器**（已安装）
2. **抖音账号已登录 Chrome**（首次运行 setup.py 后，用 Chrome 手动扫码登录一次）
3. **OpenClaw Gateway 运行中**（AI 改写需要）

**可选（提高自动化程度）：**
- Python 3.11+
- Node.js（用于 creator-tools 脚本）

---

## 配置说明

所有路径集中在 `~/.qclaw/skills/douyin-automation/CONFIG.md`：

| 键 | 默认值 | 说明 |
|---|---|---|
| `chrome_cdp_port` | `9222` | Chrome 调试端口 |
| `agent_port` | `8080` | FastAPI 后端端口 |
| `openclaw_gateway` | `http://127.0.0.1:28789` | AI 网关地址 |
| `douyin_home` | `~/douyin` | 项目根目录 |

重新配置：
```bash
python ~/.qclaw/skills/douyin-automation/scripts/setup.py
```

---

## 详细内容

- [发布规则与安全过滤](references/publishing.md)
- [评论导出与自动回复](references/comment-reply.md)
- [Qenda AI 封面生成](references/cover-ai.md)
- [编排器参数配置](references/config-reference.md)

---

## 常见问题

| 问题 | 解决 |
|------|------|
| "No items to publish" | 确认 douyin-agent 已抓取并改写视频内容到 DB |
| "CONFIG.md not found" | 运行 `python scripts/setup.py` |
| Chrome CDP 连接失败 | 确保 Chrome 已退出，重新运行 `start-backend.py` |
| AI 改写失败 | 检查 OpenClaw Gateway 是否运行 |
| 登录态失效 | 重新用 Chrome 扫码登录 creator.douyin.com |

---

## 更新 skill

```bash
clawhub update douyin-auto-hnc
```
