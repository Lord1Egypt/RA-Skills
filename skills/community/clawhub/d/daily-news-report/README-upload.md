# Daily News Brief - OpenClaw Skill

## 文件说明

这个技能包已经准备好上传到 OpenClaw。以下是文件位置：

### 主要文件
1. **技能包文件**: `/Users/lezi/skills/daily-news-brief.tar.gz`
   - 这是上传到 OpenClaw 的主要文件

2. **技能源代码目录**: `/Users/lezi/skills/daily-news-brief/`
   - 包含所有源代码文件

### 上传步骤

1. **下载技能包**
   ```bash
   cp /Users/lezi/skills/daily-news-brief.tar.gz ~/Downloads/
   ```

2. **在 OpenClaw 中上传**
   - 将 `daily-news-brief.tar.gz` 上传到 OpenClaw
   - 或者解压到 OpenClaw 的 skills 目录

3. **安装和配置**
   ```bash
   # 进入 OpenClaw
   cd /path/to/your/openclaw

   # 解压技能包
   tar -xzf daily-news-brief.tar.gz

   # 注册技能
   /skills/daily-news-brief/register

   # 配置 Telegram
   set config.telegram_chat_id "YOUR_CHAT_ID"
   set config.telegram_bot_token "YOUR_BOT_TOKEN"

   # 测试
   daily-news-brief test
   ```

### 技能功能
- ✅ 定时抓取新闻（08:00, 17:30, 22:30）
- ✅ 智能去重和分类
- ✅ 一句话新闻改写
- ✅ Telegram 推送
- ✅ 支持全量和重点领域模式
- ✅ 支持 3 个主要新闻源（财联社、IT之家、36氪）

### 注意事项
- 需要在使用前配置自己的 Telegram 配置
- 如果 Telegram 发送失败，请确认 Chat ID 是真实的用户 ID，而不是另一个 bot
- 测试模式会显示完整报告，不会发送到 Telegram
- 实际模式会发送报告到 Telegram