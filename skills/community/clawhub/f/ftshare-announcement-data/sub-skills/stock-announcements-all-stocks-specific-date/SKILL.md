# 查询指定日期全市场股票公告（分页）

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 指定日期全市场股票公告 |
| 外部接口 | `/data/api/v1/market/data/announcements/stock-announcements` |
| 请求方式 | GET |
| 适用场景 | 获取指定交易日全市场 A 股公告列表，支持分页，含公告标题、发布时间、url_hash 等 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `start_date` | string | 是 | 查询日期，格式 YYYYMMDD，仅支持单日 | `20241231` | 与 end_date 同值表示单日 |
| `end_date` | string | 是 | 结束日期，单日查询时与 start_date 相同 | `20241231` | - |
| `type` | string | 是 | 固定为 `stock` | `stock` | - |
| `page` | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| `page_size` | int | 否 | 每页记录数 | `20` | 默认 20 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-announcements-all-stocks-specific-date --start-date 20241231 --page 1 --page-size 20
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "items": [
        {
            "stock_code": "000001.SZ",
            "stock_name": "平安银行",
            "announcement_id": "1225004736",
            "announcement_title": "关于股东减持股份计划期间届满暨减持结果的公告",
            "announcement_time": "2026-03-11 16:54:28",
            "column_type": "stock",
            "url_hash": "169f21a0b04aa7291c3a963a8c80542641ea6cd5..."
        }
    ],
    "total_pages": 2,
    "total_items": 31
}
```

### 字段说明（items 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `stock_code` | String | 否 | 股票代码，带 .SZ/.SH/.BJ 后缀 | - |
| `stock_name` | String | 否 | 股票名称 | - |
| `announcement_id` | String | 否 | 公告 ID | - |
| `announcement_title` | String | 否 | 公告标题 | - |
| `announcement_time` | String | 否 | 发布时间 | - |
| `column_type` | String | 否 | 类型，如 stock | - |
| `url_hash` | String | 否 | 用于下载公告 PDF，可调用 stock-announcements-specific-url-hash | - |

## 注意事项

- 日期格式为 YYYYMMDD（如 20241231）
- 需要下载公告 PDF 时，使用 `url_hash` 调用 `stock-announcements-specific-url-hash`
- 需要全量数据时，循环请求直到 `page > total_pages`
