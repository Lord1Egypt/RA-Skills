#!/bin/bash
# fetch_emails.sh - 从 macOS 邮件应用数据库检索邮件
# 用法: ./fetch_emails.sh <范围>
# 范围: today | yesterday | unread | all

RANGE="${1:-today}"
DB_PATH="$HOME/Library/Mail/V10/MailData/Envelope Index"

if [ ! -f "$DB_PATH" ]; then
    echo "错误: 邮件数据库未找到: $DB_PATH" >&2
    exit 1
fi

# 获取当前日期（Unix 时间戳，秒）
TODAY_START=$(date -v0H -v0M -v0S +%s)
TODAY_END=$(date -v23H -v59M -v59S +%s)
YESTERDAY_START=$(date -v-1d -v0H -v0M -v0S +%s)

case "$RANGE" in
    today)
        # 今天收到的邮件
        QUERY="SELECT m.ROWID, 
                      datetime(m.date_sent, 'unixepoch') as date_sent, 
                      datetime(m.date_received, 'unixepoch') as date_received, 
                      COALESCE(s.subject, '') as subject, 
                      COALESCE(a.address, '') as sender, 
                      COALESCE(su.summary, '') as summary 
               FROM messages m 
               LEFT JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               LEFT JOIN summaries su ON m.summary = su.ROWID
               WHERE m.date_received >= $TODAY_START AND m.date_received <= $TODAY_END
               ORDER BY m.date_received DESC"
        ;;
    yesterday)
        # 昨天到今天
        QUERY="SELECT m.ROWID, 
                      datetime(m.date_sent, 'unixepoch') as date_sent, 
                      datetime(m.date_received, 'unixepoch') as date_received, 
                      COALESCE(s.subject, '') as subject, 
                      COALESCE(a.address, '') as sender, 
                      COALESCE(su.summary, '') as summary 
               FROM messages m 
               LEFT JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               LEFT JOIN summaries su ON m.summary = su.ROWID
               WHERE m.date_received >= $YESTERDAY_START AND m.date_received <= $TODAY_END
               ORDER BY m.date_received DESC"
        ;;
    unread)
        # 未读邮件
        QUERY="SELECT m.ROWID, 
                      datetime(m.date_sent, 'unixepoch') as date_sent, 
                      datetime(m.date_received, 'unixepoch') as date_received, 
                      COALESCE(s.subject, '') as subject, 
                      COALESCE(a.address, '') as sender, 
                      COALESCE(su.summary, '') as summary 
               FROM messages m 
               LEFT JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               LEFT JOIN summaries su ON m.summary = su.ROWID
               WHERE m.read = 0
               ORDER BY m.date_received DESC"
        ;;
    all)
        # 所有邮件（最近 50 封）
        QUERY="SELECT m.ROWID, 
                      datetime(m.date_sent, 'unixepoch') as date_sent, 
                      datetime(m.date_received, 'unixepoch') as date_received, 
                      COALESCE(s.subject, '') as subject, 
                      COALESCE(a.address, '') as sender, 
                      COALESCE(su.summary, '') as summary 
               FROM messages m 
               LEFT JOIN subjects s ON m.subject = s.ROWID
               LEFT JOIN addresses a ON m.sender = a.ROWID
               LEFT JOIN summaries su ON m.summary = su.ROWID
               ORDER BY m.date_received DESC 
               LIMIT 50"
        ;;
    *)
        echo "错误: 未知范围 '$RANGE'. 使用: today|yesterday|unread|all" >&2
        exit 1
        ;;
esac

# 执行查询并输出 JSON 格式
sqlite3 -json "$DB_PATH" "$QUERY" 2>/dev/null || echo "[]"
