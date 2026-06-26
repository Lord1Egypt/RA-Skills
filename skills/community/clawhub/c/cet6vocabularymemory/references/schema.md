# 数据库表结构

## word_memory_status.csv

用户单词记忆状态表。

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | string | 用户ID |
| word | string | 单词 |
| phonetic | string | 音标 |
| part_of_speech | string | 词性 |
| meaning | string | 中文释义 |
| example_sentence | string | 例句 |
| mastery_level | int | 掌握程度（0-6） |
| next_review_date | date | 下次复习日期 |
| review_count | int | 复习次数 |
| correct_count | int | 正确次数 |
| wrong_count | int | 错误次数 |
| created_at | datetime | 首次学习时间 |
| updated_at | datetime | 最后更新时间 |

## user_schedule.csv

用户学习计划表。

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | string | 用户ID |
| user_name | string | 用户名称 |
| daily_time | string | 每日学习时间 |
| words_per_day | int | 每日学习单词数 |
| is_active | bool | 定时任务是否开启 |
| last_review_date | date | 上次复习日期 |

## CSV 文件格式

- 使用逗号分隔
- 第一行为表头
- 日期格式：YYYY-MM-DD
- 时间格式：HH:MM