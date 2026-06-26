---
name: FTShare-news-data
description: 新闻语义搜索技能集（market.ft.tech）。根据搜索文字进行语义搜索，返回相关新闻列表。用户询问语义搜新闻、按关键词搜新闻时使用。数据仅支持当年、最近半个月。
---

# FT 新闻数据 Skills

本 skill 是 `FTShare-news-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」或「询问方式与子 skill 对应表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，本技能集子 skill 无需额外请求头。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> semantic-search-news --query 人工智能
python <RUN_PY> semantic-search-news --query 人工智能 --limit 10 --year 2026
python <RUN_PY> semantic-search-news --query 人工智能 --limit 10 --year 2026 --start_time 2026-03-01T00:00:00+08:00 --end_time 2026-03-15T23:59:59+08:00
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 新闻 — 询问方式与子 skill 对应表

| 询问方式（用户常说的词） | 子 skill |
|------------------------|----------|
| **语义搜索新闻**、**按关键词搜新闻**、**搜索相关新闻** | `semantic-search-news` |

---

## 能力总览

- **`semantic-search-news`**：根据搜索文字进行语义搜索，返回相关新闻列表。数据仅支持**当年**、**最近半个月**内的新闻。必填：`--query`（搜索文字）；可选：`--limit`（返回条数，默认 10）、`--year`（年份，仅支持当年）。展示时需包含来源（source_site）与文章链接（article_url），并提示用户数据仅半个月内。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「询问方式与子 skill 对应表」或「能力总览」匹配子 skill 名称。
3. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：按子 skill 要求展示来源、链接，并提示「以下结果仅展示当年、最近半个月以内的新闻。」
