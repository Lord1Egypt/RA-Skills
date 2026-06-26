# todoman 配置模板
# 复制到 ~/.config/todoman/config.py

# 提醒事项存储路径 (vdirsyncer 同步目录)
path = "~/.local/share/vdirsyncer/reminders/*"

# 日期时间格式
date_format = "%Y-%m-%d"
time_format = "%H:%M"

# 默认提醒列表 (根据实际情况修改)
default_list = "Reminders"

# 默认截止日期 (0 = 今天, 1 = 明天, None = 无)
default_due = None

# 人性化时间显示
humanize = True

# 默认优先级 (0=无, 1-4=低, 5=中, 6-9=高)
default_priority = 0
