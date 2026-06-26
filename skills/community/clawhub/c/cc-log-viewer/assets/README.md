# cc-log-viewer

实时查看 Claude Code 终端输出的 Web 工具。

## 快速开始

```bash
# 安装依赖
cd cc-log-viewer && npm install

# 启动（含CC进程，默认端口18798）
bash start-all.sh

# 打开浏览器访问
# http://localhost:18798/
```

更多说明见 [SKILL.md](SKILL.md)

## 文件说明

| 文件 | 说明 |
|------|------|
| `log-streamer.js` | 后端服务：HTTP + WebSocket + CC进程管理 |
| `index.html` | 前端页面：xterm.js 终端渲染 |
| `start-all.sh` | 一键启动脚本 |
| `package.json` | npm 依赖配置 |


