# egatee-chat-summary

用于通过 Notify 开放接口（`getChatHistoryByApiKey`，`X-API-Key` 鉴权）拉取绑定 IM 账号近 1~7 天聊天记录，并输出 `meta` 与 `peer_summaries`。

## 目录

- `SKILL.md`: Skill 元数据与使用说明
- `tool.py`: 调用与汇总脚本
- `requirements.txt`: Python 依赖
- `run.sh`: 一键运行脚本

## 快速开始

1. 安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

2. 配置环境变量（见 `SKILL.md`「依赖环境变量」；本地可自建 `.env` 并由 `run.sh` 加载）

3. 运行：

```bash
python3 tool.py --day 7 --timeout 60
# 或
./run.sh 7
```

