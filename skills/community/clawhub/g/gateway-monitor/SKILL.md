# Gateway Monitor - OpenClaw 监控面板

实时监控 OpenClaw Gateway 状态、日志检索、服务健康检查的一站式监控面板。

## 功能特性

- **实时监控**：Gateway 运行状态、资源使用、会话上下文
- **日志检索**：错误/警告高亮，支持关键字搜索和过滤
- **服务状态**：launchd 服务、LiteLLM、oMLX、acpx
- **LiteLLM 按需唤起**：默认可保持停止，支持自动唤起或手动唤起/停止
- **告警系统**：基于错误频率、资源消耗的自动告警
- **一键还原**：配置出错时可从备份恢复
- **皮肤主题**：深色 / 浅色 / 跟随系统，响应式布局

## 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/yes999zc/gateway-monitor.git
cd gateway-monitor

# 无需依赖，直接运行
node server.js

# 浏览器访问
open http://127.0.0.1:18990
```

### 环境变量配置

```bash
# 可选配置
export PORT=18990                      # 服务端口（默认 18990）
export OMLX_MODELS_URL=http://127.0.0.1:9981/v1/models  # oMLX 模型端点
export OMLX_API_KEY=8888               # oMLX API 密钥
export LITELLM_BASE_URL=http://127.0.0.1:4000  # LiteLLM 端点
export LITELLM_CONTAINER_NAME=litellm-omlx  # LiteLLM docker 容器名
export LITELLM_AUTO_WAKE_DEFAULT=0     # 是否默认自动唤起（0/1）
```

## API 端点

- `GET /` - 仪表盘页面
- `GET /api/summary` - 聚合状态快照
- `GET /api/logs` - 日志列表
- `GET /api/gateway-status` - Gateway 状态
- `GET /api/launchd-status` - launchd 服务状态
- `GET /api/restore-config?confirm=true` - 恢复配置
- `GET /api/gateway-restart?confirm=true` - 重启 Gateway
- `GET /api/litellm-status?autoWake=1` - LiteLLM 状态（可自动唤起）
- `GET /api/litellm-control?action=wake|start|stop|restart&confirm=true` - 控制 LiteLLM 容器
- `GET /api/omlx-capabilities` - oMLX 能力检测（模型/VLM/Embedding/Rerank）
- `GET /api/litellm-wake` - LiteLLM 按需唤起
- `GET /api/omlx-update?check=1` - 检查 oMLX 更新

## 监控面板截图

![Dashboard](https://raw.githubusercontent.com/yes999zc/gateway-monitor/main/screenshots/dashboard.png)

## 使用场景

1. **Gateway 健康检查**：实时监控 Gateway 运行状态、token 使用情况
2. **日志排查**：快速定位错误日志，支持关键字搜索
3. **配置恢复**：配置出错时一键从备份恢复
4. **服务管理**：LiteLLM、oMLX 等服务状态监控与控制

## 安全说明

- 密钥脱敏显示：API key 首尾保留，中间用 `***` 填充
- 恢复配置需要二次确认（前端弹窗 + URL 参数）
- 重启 Gateway 需要二次确认

## 后台运行

```bash
# 使用 launchd 托管（推荐）
cp bin/ai.openclaw.gateway-monitor.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway-monitor.plist

# 手动后台运行
nohup node server.js > gateway-monitor.log 2>&1 &
```

## 更新日志

### v1.0.1
- 改进 UI 界面设计
- 新增快照捕获功能
- 增强监控能力检测

### v1.0.0
- 初始发布
- Gateway 状态监控
- 日志检索与告警系统
- 一键配置恢复

## 许可证

MIT License

## 贡献

欢迎提 Issue 和 PR！
