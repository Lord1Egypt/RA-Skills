# 04 深抓正文

## 脚本

```bash
python3 scripts/collect_detail.py --date {date}
```

## 作用

从筛选后的候选池中，对网站类条目用 `opencli web read` 深抓正文。平台类条目已有完整内容，直接保留。

## 输入

- `output/raw/{date}_index_filtered.txt` — 由 filter_index.py 生成

## 输出

- `output/raw/{date}_detail.txt` — 包含完整内容的候选详情

## 处理逻辑

### 两类条目

| 类型 | 判断依据 | 处理 |
|------|---------|------|
| **平台类** | `time_status: in_window` | 已有完整内容（title/text），直接复制到 detail |
| **网站类** | `time_status: google_filtered` | 只有标题+URL，需要 `opencli web read --url` 抓正文 |

### 网站类深抓流程

1. 提取所有网站类条目的 URL
2. 按 URL 去重（同一 URL 不重复抓取）
3. 逐个执行 `opencli web read --url "{url}"`
4. 每次请求间隔 3 秒
5. 正文截取前 2000 字符保存（避免文件过大）
6. 标记 `fetch_status: success / FAILED`

## 输出格式

```
# ━━ 第一部分：平台类条目（已有完整内容）━━

--- [微博] (cn) ---
type: platform
keyword: 大模型
title: 标题内容...
author: xxx
time: 04月05日 12:30
url: https://weibo.com/...

# ━━ 第二部分：网站类条目（深抓正文）━━

--- [量子位] (website) ---
type: website_detail
keyword: 大模型
title: 文章标题...
url: https://www.qbitai.com/...
fetch_status: success
fetched_content:
  （正文 Markdown，最多 2000 字符）
```

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--date` | 今天 | 目标日期 |
| `--max-fetch` | 0 | 最多深抓多少个 URL，0=不限 |
| `--dry-run` | false | 只输出要抓的 URL 列表 |
| `--no-save` | false | 不保存到文件 |

## 多行正文保留

与 filter_index.py 一样，解析器保留 `[N]` 标题行与字段行之间的所有多行正文（如 Twitter 推文），输出到 detail.txt 时完整写回。

## 超时和间隔

- 单次请求超时：**60 秒**（部分网站如 The Verge 单次需要 15-20 秒，连续请求时更慢）
- 请求间隔：**5 秒**（给浏览器释放资源时间）
- 实测 36 个 URL 全部成功（之前 30s 超时时 20 个失败）

## 常见失败原因

- 超时（浏览器资源占满）→ 已通过加大超时和间隔解决
- 部分网站有反爬（少数情况）→ 失败条目保留在 detail.txt 中标记 `fetch_status: FAILED`，不影响后续流程
