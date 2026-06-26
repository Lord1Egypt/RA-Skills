# 查询单只股票所有公告（分页）

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 单只股票公告历史 |
| 外部接口 | `/data/api/v1/market/data/announcements/stock-announcements` |
| 请求方式 | GET |
| 适用场景 | 获取单只 A 股股票的公告历史列表，支持分页，含公告标题、发布时间、url_hash 等 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `stock_code` | string | 是 | 股票代码，含市场后缀 | `000001.SZ` | 6 位数字 + .SZ/.SH/.BJ |
| `page` | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| `page_size` | int | 否 | 每页记录数 | `20` | 默认 20 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-announcements-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 20
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

返回带分页的 JSON，结构同「指定日期全市场公告」：

```json
{
    "items": [
        {
            "stock_code": "000001.SZ",
            "stock_name": "平安银行",
            "announcement_id": "1225004736",
            "announcement_title": "公告标题示例",
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
| `stock_code` | String | 否 | 股票代码，带市场后缀 | - |
| `stock_name` | String | 否 | 股票名称 | - |
| `announcement_id` | String | 否 | 公告 ID | - |
| `announcement_title` | String | 否 | 公告标题 | - |
| `announcement_time` | String | 否 | 发布时间 | - |
| `column_type` | String | 否 | 类型，如 stock | - |
| `url_hash` | String | 否 | 用于下载公告 PDF | - |

## 注意事项

- 股票代码格式：6 位数字 + 市场后缀（SH/SZ/BJ）
- 需要下载公告 PDF 时，使用 `url_hash` 调用 `stock-announcements-specific-url-hash`
