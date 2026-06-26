# DG-LAB（郊狼）控制器

OpenClaw Skill — 通过 WebSocket 协议控制 DG-LAB Coyote 3.0 郊狼脉冲设备。

## 功能

- 设备配对（二维码扫描）
- A/B 双通道强度调节（0-200）
- 16 种内置波形预设 + 自定义波形生成
- 安全机制：强度上限、速率限制、紧急停止
- 完整的启动引导流程（环境检查 → 安装 → 配对 → 安全确认）

## 架构

```
AI Agent --HTTP--> ws_client.py --WebSocket--> 中继服务器 --WS--> DG-LAB APP --BLE--> 郊狼 3.0
```

`ws_client.py` 作为常驻后台进程，同时维护与中继服务器的 WebSocket 连接和面向 AI Agent 的本地 HTTP API（`127.0.0.1:8899`）。

## 前置依赖

- Python 3.10+
- Node.js 18+
- [DG-LAB 官方中继服务器](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE)

## 安装

```bash
# 安装 Python 依赖
pip install -r scripts/requirements.txt

# 克隆并安装中继服务器
git clone https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE.git ~/DG-LAB-OPENSOURCE
cd ~/DG-LAB-OPENSOURCE/socket/v2/backend && npm install
```

## 使用

通过 OpenClaw 加载后，AI Agent 会自动按照 `SKILL.md` 中定义的工作流引导用户完成环境检查、服务启动、设备配对和安全确认。

手动启动：

```bash
# 1. 启动中继服务器
cd ~/DG-LAB-OPENSOURCE/socket/v2/backend && npm start

# 2. 启动控制器
python scripts/ws_client.py --ws-url ws://localhost:9999 --strength-limit 50
```

## 项目结构

```
DG-LAB/
├── SKILL.md              # Skill 定义（元数据 + AI 指令）
├── README.md             # 本文件
├── .gitignore
├── scripts/
│   ├── ws_client.py      # WebSocket 客户端 + HTTP API 控制器
│   ├── waveform.py       # 波形生成 / 验证工具
│   ├── presets.json       # 16 种内置波形预设数据
│   └── requirements.txt   # Python 依赖
└── references/
    ├── protocol.md        # WebSocket 协议参考
    └── waveform-format.md # V3 波形 HEX 编码参考
```

## 安全说明

- 所有控制通信在本机完成（HTTP API 仅监听 `127.0.0.1`，WebSocket 连接本地中继服务器）
- 不收集、不上传任何用户数据
- 唯一的外部网络访问：首次安装时从 GitHub 克隆中继服务器仓库
- 设备控制包含强度上限、速率限制和紧急停止等多重安全机制
- 使用前强制进行电极安全确认

## License

MIT
