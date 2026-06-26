# 查询单只股票所有研报（分页）

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 单只股票研报历史 |
| 外部接口 | `/data/api/v1/market/data/announcements/stock-reports`（或项目实际 path） |
| 请求方式 | GET |
| 适用场景 | 获取单只 A 股股票的研报历史列表，支持分页，含研报标题、作者、发布时间、url_hash 等 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `stock_code` | string | 是 | 股票代码，含市场后缀 | `000001.SZ` | 6 位数字 + .SZ/.SH/.BJ |
| `page` | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| `page_size` | int | 否 | 每页记录数 | `20` | 默认 20 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-reports-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 20
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

返回带分页的 JSON，结构同「指定日期全市场研报」：`items` 数组、`total_pages`、`total_items`。items 每项含 `stock_code`、`stock_name`、研报标题、发布时间、`url_hash` 等，字段说明参见 `stock-reports-all-stocks-specific-date`。

## 注意事项

- 股票代码格式：6 位数字 + 市场后缀（SH/SZ/BJ）
- 需要下载研报 PDF 时，使用 `url_hash` 调用 `stock-reports-specific-url-hash`
