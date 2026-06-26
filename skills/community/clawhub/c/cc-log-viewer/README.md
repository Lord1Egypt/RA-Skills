# cc-log-viewer

实时捕获 Claude Code 终端输出，通过 WebSocket 推送到 xterm.js 浏览器页面。

## 功能

- 实时显示 CC 终端输出，毫秒级 WebSocket 推送
- 在手机/平板上观察 CC 执行任务
- 通过 HTTP API 向 CC 发命令、查状态、重启
- 嵌入模式 `?embed=1` 可集成到监控面板
- 知识图谱 API — 扫描 Obsidian vault 结构并输出图谱数据
- 零外部 CDN 依赖，xterm.js 自托管

## 安装

```bash
openclaw skills install cc-log-viewer
cd ~/.openclaw/workspace/skills/cc-log-viewer
cd assets && npm install && cd ..
bash assets/start-all.sh
```

浏览器打开 `http://localhost:18798/`

## 更多

详见 `SKILL.md`。
