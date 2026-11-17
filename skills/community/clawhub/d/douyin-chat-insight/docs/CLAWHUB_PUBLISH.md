# ClawHub 发布说明

- slug: `douyin-chat-insight`
- version: `0.2.0`
- homepage: https://github.com/tars1230/douyin-chat-insight

## clawscan 边界说明

本 skill 仅读取用户显式传入的本地聊天导出文件，在本地生成 HTML/Markdown/JSON 报告。
不登录任何 IM，不采集 cookie 或会话凭据，不强制网络请求，不强制阿里云/百炼 Key。
可选环境变量 DASHSCOPE_API_KEY 仅用于状态探测与文档中的可选转写指导，核心 run 路径不调用云 ASR。
输出目录默认在工作区内；报告路径会脱敏。

## 命令示例

```bash
clawhub skill publish "$(pwd)" \
  --slug douyin-chat-insight \
  --name "Douyin Chat Insight 抖音聊天转知识库" \
  --version 0.2.0 \
  --changelog "首个公开稳定版：本地会话四块报告、doctor 体检、可选抖音链接 ASR 端口（不强制 Key）" \
  --clawscan-note "本地读取用户指定导出；无 IM 登录；无强制网络；无强制云 Key" \
  --tags latest
```
