---
name: diary-agent-control
description: 安全连接超级日记，供 WorkBuddy、OpenClaw、Codex、Claude 等 Agent 查询记录、趋势、总结与记录旅程；只在用户明确确认时新增记录。
version: 0.6.1
metadata:
  openclaw:
    install:
      - kind: node
        package: https://github.com/super21-bat/diary-agent-control/archive/refs/heads/main.tar.gz
        bins:
          - diary
          - diary-mcp
    homepage: https://github.com/super21-bat/diary-agent-control
---

# 超级日记 Agent Control

如果系统中没有 `diary` 命令，先自动执行 `npm install -g https://github.com/super21-bat/diary-agent-control/archive/refs/heads/main.tar.gz` 并检查 `diary --version`；不要把安装命令转交给用户手动执行。

使用前先运行 `diary doctor`。若未配置，向用户索取小程序“我的 → 记录与连接 → 自动化接入”生成的一次性专属钥匙；不要让用户把钥匙发到群聊、代码仓库、截图或公开日志。

## 产品边界

- 小程序是日常记录、今日回顾和基础统计的主入口。
- Agent 的价值是跨应用归集（聊天、收据、运动等）、跨周/月追问、批量整理和用户明确安排的提醒。
- 不要为了展示能力重复生成应用内已有的基础统计。
- 默认只读。新增日记前复述内容、时间和共享状态并取得本次明确确认。
- `diary_create_note` 必须传 `confirm: true`；成功后必须立即读取返回的记录，向用户报告实际保存结果。
- 不修改、不删除历史记录；当前公开 MCP 也不提供删除工具。

## 常用流程

1. `diary doctor` 检查账户与工具。
2. `diary tools` 查看服务端当前能力，不猜测参数。
3. 使用 `diary call diary_list_notes '{"page":1,"pageSize":20}'` 查询。
4. 需要长期分析时，先缩小日期或关键词范围，再读取必要记录，避免过度暴露私人内容。
5. 用户确认写入后调用：`diary call diary_create_note '{"content":"...","createdAt":"ISO 8601","isShared":false,"confirm":true}'`，然后按返回 ID 回读。

原生支持 Streamable HTTP MCP 的客户端可直接连接配置中的 URL，并以专属钥匙作为 Bearer Token。
若客户端只支持 stdio，使用 `diary-mcp` 作为 command；它读取 `~/.super-diary/config.json`，不要在客户端配置中重复明文保存钥匙。安装完成不能只检查版本，必须以 `diary doctor` 的实际读取结果作为连接成功标准。
