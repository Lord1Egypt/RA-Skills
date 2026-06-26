# doc-first

**任何外部工具、服务、API 的配置或问题，第一时间查官方文档，力求精准解决。**

## 触发条件

遇到以下情况时自动触发：
- 不确定某个工具/服务的正确配置格式
- 不确定某个命令的用法或选项
- 遇到权限、授权、认证相关问题
- 遇到错误不知道原因
- 任何不确定的操作
- 配置 openclaw.json / 环境变量 / CLI 参数时

## 执行原则

### 第一原则：查官方文档
- 优先查官方文档/官方 API 文档
- 用 `web_fetch` 抓取官方页面
- **英文文档为主，中文文档用于辅助确认**（中文翻译常有滞后或不完整）
- **查完官方文档仍无解** → 按序尝试：GitHub Issue → Stack Overflow → 开发者社区搜索
- **每次查文档须说明依据**：告诉用户查了哪篇文档、哪个版本（URL + 日期或版本号），方便用户核实

### 第二原则：精准解决
- 不确定答案时，宁可说"我不确定"也不瞎猜
- 遇到奇怪报错，先查文档再尝试修复
- 配置文件动手前，先确认正确格式和路径

### 第三原则：如实告知
- 官方文档没有 → 直接说明，不编造
- 找不到解决方案 → 说清楚，而不是给可能错误的答案
- 不确定的地方 → 提出最可能的猜测，但标注不确定

### 第四原则：验证步骤
改了配置之后，**重新对比官方文档**，确认格式/路径/选项都匹配，再继续下一步。不匹配就修正，不确定就停下来如实告知用户。

### 第五原则：版本意识
查文档时**先确认版本号或服务版本**，尤其是 Discord API 这类有大版本变化的（v10 → v14 格式完全不同）。不确定用哪个版本时，优先用最新版文档，并在回答中注明版本依据。

## 常见误区

- 以为配置格式和旧版本一样（实际上经常变）
- 记错选项名（比如 `--force` 写成 `--forced`）
- 混用不同 API 版本（v1 和 v2 格式完全不同）
- 用错误的路径（比如把 user 配置放进 system 配置）

## 常用文档入口

| 服务 | 文档地址 |
|------|----------|
| OpenClaw | https://docs.openclaw.ai/llms.txt |
| OpenAI | https://platform.openai.com/docs |
| Anthropic | https://docs.anthropic.com/ |
| GLM (智谱) | https://open.bigmodel.cn/dev/api |
| MiniMax | https://www.minimaxi.com/document/Guide |
| 阿里云通义千问 (DashScope) | https://qianwen-api.aliyun.com/ |
| 百度文心一言 (千帆) | https://qianfan.cloud.baidu.com/ |
| 讯飞星火认知大模型 | https://www.xfyun.cn/doc/spark/ |
| 月之暗面 Kimi (Moonshot) | https://platform.moonshot.cn/ |
| 昆仑万维天工AI | https://www.tiangong.cn/ |
| 字节扣子 (Coze) | https://www.coze.cn/docs/ |
| 微信小程序 | https://developers.weixin.qq.com/miniprogram/dev/framework/ |
| Telegram Bot API | https://core.telegram.org/bots/api |
| DeepSeek | https://api.deepseek.com/docs |
| Slack API | https://api.slack.com/ |
| Discord API | https://discord.com/developers/docs |
| GitHub API | https://docs.github.com/rest |
| Notion API | https://developers.notion.com/docs/getting-started |
| GMAIL API | https://developers.google.com/gmail/api |

## 规则

**不查官方文档不开口。找不到就直说，不编答案。**
