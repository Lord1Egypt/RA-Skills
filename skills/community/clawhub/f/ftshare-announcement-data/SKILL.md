---
name: FTShare-ashare-announcement-data
description: A 股公告与研报数据技能集。覆盖指定日期全市场公告/研报、单只股票公告/研报历史、通过 url_hash 下载公告/研报 PDF（market.ft.tech）。用户询问某天公告列表、某只股票公告或研报、下载公告/研报时使用。
---

# FT A-share 公告与研报数据 Skills

本 skill 是 `FTShare-ashare-announcement-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> 所有接口均以 `https://market.ft.tech` 为基础域名，使用 HTTP GET。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-announcements-all-stocks-specific-date --start-date 20241231 --page 1 --page-size 20
python <RUN_PY> stock-announcements-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 20
python <RUN_PY> stock-announcements-specific-url-hash --url-hash <hash> --output announcement.pdf
python <RUN_PY> stock-reports-all-stocks-specific-date --start-date 20241231 --page 1 --page-size 20
python <RUN_PY> stock-reports-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 20
python <RUN_PY> stock-reports-specific-url-hash --url-hash <hash> --output report.pdf
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 公告

- **`stock-announcements-all-stocks-specific-date`**：指定日期全市场股票公告列表（分页）。必填参数：`--start-date`（YYYYMMDD）；可选 `--page`、`--page-size`。

- **`stock-announcements-single-stock-all-periods`**：单只股票公告历史（分页）。必填参数：`--stock-code`（带市场后缀，如 `000001.SZ`）；可选 `--page`、`--page-size`。

- **`stock-announcements-specific-url-hash`**：通过 url_hash 查询/下载单条公告 PDF。必填参数：`--url-hash`；可选 `--output`（保存文件名）。

### 2. 研报

- **`stock-reports-all-stocks-specific-date`**：指定日期全市场股票研报列表（分页）。必填参数：`--start-date`（YYYYMMDD）；可选 `--page`、`--page-size`。

- **`stock-reports-single-stock-all-periods`**：单只股票研报历史（分页）。必填参数：`--stock-code`（带市场后缀）；可选 `--page`、`--page-size`。

- **`stock-reports-specific-url-hash`**：通过 url_hash 查询/下载单条研报 PDF。必填参数：`--url-hash`；可选 `--output`（保存文件名）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配对应子 skill 名称。
3. （可选）读取 `<RUN_PY>` 同级目录 `sub-skills/<子skill名>/SKILL.md` 了解接口详情与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|---|---|
| 「今天/某天的公告列表」 | `stock-announcements-all-stocks-specific-date` |
| 「指定日期全市场公告」 | `stock-announcements-all-stocks-specific-date` |
| 「某只股票的历史公告」 | `stock-announcements-single-stock-all-periods` |
| 「下载某条公告 PDF」 | `stock-announcements-specific-url-hash` |
| 「今天/某天的研报列表」 | `stock-reports-all-stocks-specific-date` |
| 「指定日期全市场研报」 | `stock-reports-all-stocks-specific-date` |
| 「某只股票的历史研报」 | `stock-reports-single-stock-all-periods` |
| 「下载某条研报 PDF」 | `stock-reports-specific-url-hash` |
