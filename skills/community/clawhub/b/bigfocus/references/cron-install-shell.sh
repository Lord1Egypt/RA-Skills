# BigFocus Cron 安装命令模板
# cron message 引用 SKILL.md，行为由 SKILL.md 驱动
# 安装时请替换 CHANNEL 和 TARGET 为实际值：
#   openclaw directory  # 获取当前渠道和目标，或从会话上下文读取
#   CHANNEL = feishu / discord / telegram 等
#   TARGET = ou_xxx / channel_id / chat_id 等

# 定时扫描（每整点）
openclaw cron add \
  --name bigfocus-scan \
  --cron "0 * * * *" \
  --tz "Asia/Shanghai" \
  --message "🎯 BigFocus 定时扫描。
按 bigfocus SKILL.md 中「定时扫描」流程执行。

要点：
1. 调 bigfocus.py scan 获取到期项
2. 对 need_ai 项做 web_search
3. 调 bigfocus.py record 记录结果
4. 有变化则按「定时汇报模板」推送（openclaw message send）
5. 无变化不推送，不输出任何内容
6. 严禁输出思考过程和调试信息" \
  --timeout-seconds 300 \
  --channel CHANNEL \
  --to TARGET \
  --session isolated \
  --no-deliver
