# 03 时间筛选

## 脚本

```bash
python3 scripts/filter_index.py --date {date} --window 3
```

## 作用

对 `{date}_index.txt` 做时间窗口筛选，过滤掉超出时间范围的旧内容。

## 输入

- `output/raw/{date}_index.txt` — 由 collect_sources_with_opencli.py 生成

## 输出

- `output/raw/{date}_index_filtered.txt` — 筛选后的候选池

## 筛选规则

### 三类条目的处理方式

| 类型 | 判断依据 | 处理 |
|------|---------|------|
| **有时间字段** | `time:` 字段能解析为日期 | 在窗口内保留，超出删除 |
| **无时间字段** | `time:` 字段缺失或无法解析 | **直接过滤** |
| **网站类** | `region: website` | **直接保留**（Google site: 搜索自带 `after:` 过滤） |

### 支持的时间格式

脚本的 `parse_time` 函数支持解析以下格式：

| 格式 | 示例 | 来源 |
|------|------|------|
| Twitter | `Fri Apr 03 14:00:17 +0000 2026` | Twitter search |
| ISO 日期 | `2026-04-03` | 小红书、36氪 |
| ISO 日期时间 | `2026-04-03 14:00:17` | — |
| 无秒 | `2026-04-03 14:00` | Reddit API 转换后 |
| 中文日期 | `2026年4月3日` | — |
| 中文月日 | `04月03日 12:40` | 微博 |
| 今天 | `今天08:04` | 微博 |
| 昨天/前天 | `昨天 17:58` | 微博 |
| 相对时间 | `3小时前` / `2天前` / `12分钟前` | 微博 |
| 英文相对时间 | `2 days ago` / `11 months ago` | YouTube |
| RFC 2822 | `Sat, 04 Apr 2026 12:00:01 GMT` | Google news |
| ISO with TZ | `2026-04-03T14:00:17Z` | — |

### 输出中的标记

每条保留的条目会被标记：

- `time_status: in_window` — 有时间，在窗口内
- `time_status: google_filtered` — 网站类，Google 已过滤
- `time_parsed: 2026-04-05` — 解析后的标准日期

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--date` | 今天 | 目标日期 |
| `--window` | 3 | 时间窗口天数 |
| `--dry-run` | false | 只输出统计，不保存 |

## 多行正文保留

Twitter 推文等多行内容在筛选后完整保留。解析器收集 `[N]` 标题行与字段行之间的所有文本行作为 `content_lines`，输出时写回原位。

```
# 筛选前：
  [4] Wow, this tweet went very viral!
I wanted share a possibly slightly improved version...
So here's the idea in a gist format: https://t.co/...
      author: karpathy

# 筛选后保持完整：
  [4] Wow, this tweet went very viral!
I wanted share a possibly slightly improved version...
So here's the idea in a gist format: https://t.co/...
      author: karpathy
      time_status: in_window
      time_parsed: 2026-04-04
```
