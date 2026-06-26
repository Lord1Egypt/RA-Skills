# 查询指定日期全市场股票研报（分页）

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 指定日期全市场股票研报 |
| 外部接口 | `/data/api/v1/market/data/announcements/stock-reports`（或项目实际 path） |
| 请求方式 | GET |
| 适用场景 | 获取指定交易日全市场 A 股研报列表，支持分页，含研报标题、作者、发布时间、url_hash 等 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `start_date` | string | 是 | 查询日期，格式 YYYYMMDD，仅支持单日 | `20241231` | - |
| `end_date` | string | 是 | 结束日期，单日查询时与 start_date 相同 | `20241231` | - |
| `type` | string | 是 | 固定为 stock（或接口约定值） | `stock` | - |
| `page` | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| `page_size` | int | 否 | 每页记录数 | `20` | 默认 20 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-reports-all-stocks-specific-date --start-date 20241231 --page 1 --page-size 20
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

返回带分页的 JSON：

```json
{
    "items": [
        {
            "stock_code": "000001.SZ",
            "stock_name": "平安银行",
            "announcement_title": "研报标题示例",
            "announcement_time": "2026-03-11 16:00:00",
            "url_hash": "abc123..."
        }
    ],
    "total_pages": 2,
    "total_items": 20
}
```

### 字段说明（items 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `stock_code` | String | 否 | 股票代码，带市场后缀 | - |
| `stock_name` | String | 否 | 股票名称 | - |
| `announcement_title` | String | 否 | 研报标题 | - |
| `announcement_time` | String | 否 | 发布时间 | - |
| `url_hash` | String | 否 | 用于下载研报 PDF | - |

## 注意事项

- 日期格式为 YYYYMMDD（如 20241231）
- 需要下载研报 PDF 时，使用 `url_hash` 调用 `stock-reports-specific-url-hash`
- 需要全量数据时，循环请求直到 `page > total_pages`
