# Eyes Cron 安装命令模板
# cron message 仅引用SKILL.md，行为由SKILL.md驱动，更新SKILL.md即更新行为
# 安装时请替换 CHANNEL 和 TARGET 为实际值：
#   openclaw directory  # 获取当前渠道和目标，或从会话上下文读取
#   CHANNEL = feishu / discord / telegram 等
#   TARGET = ou_xxx / channel_id / chat_id 等

# 1. 早8点开盘前瞻
openclaw cron add \
  --name eyes-morning \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --message "【引用SKILL.md执行】\n按 eyes SKILL.md 中\"早8点开盘前瞻\"流程执行。规格见\"通用分段推送（全渠道）\"和\"推送格式\"章节。\n\n要点：搜索12h事件→合并3-5段→每段加粗排版→openclaw message send逐段发，段间sleep 1.5。严禁输出思考过程。" \
  --timeout-seconds 600 \
  --channel CHANNEL \
  --to TARGET \
  --session isolated \
  --no-deliver

# 2. 整点扫描（9:00~19:00）
openclaw cron add \
  --name eyes-hourly \
  --cron "0 9-19 * * *" \
  --tz "Asia/Shanghai" \
  --message "【引用SKILL.md执行】\n按 eyes SKILL.md 中\"整点扫描\"流程执行。无新事件不推送。推送规则见\"通用分段推送\"章节。\n\n要点：搜索1h事件→合并分段→加粗排版→openclaw message send发送，段间sleep 1.5。" \
  --timeout-seconds 600 \
  --channel CHANNEL \
  --to TARGET \
  --session isolated \
  --no-deliver

# 3. 晚8点收盘复盘
openclaw cron add \
  --name eyes-evening \
  --cron "0 20 * * *" \
  --tz "Asia/Shanghai" \
  --message "【引用SKILL.md执行】\n按 eyes SKILL.md 中\"晚8点收盘复盘\"流程执行。规格见\"通用分段推送\"和\"推送格式\"章节。\n\n要点：搜索12h事件+A股分析+明日关注→合并3-5段→加粗排版→openclaw message send逐段发，段间sleep 1.5→末段加互动语。严禁输出长内容。" \
  --timeout-seconds 600 \
  --channel CHANNEL \
  --to TARGET \
  --session isolated \
  --no-deliver
