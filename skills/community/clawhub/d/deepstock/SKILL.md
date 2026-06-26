---
name: deepstock
description: A股量化投研助手 | 免费提供K线数据 · 技术指标 · 股东人数 · 官方公告解析。
---
# DeepStock API
HTTP HOST: http://60.205.179.76:8000
## 接口清单

### 股票基础信息


#### `GET /api/stock/basic/name/{name}`
根据名称查询股票基础信息, 可以获取到`ts_code`等。

```bash
GET /api/stock/basic/name/贵州茅台
```

---

#### `GET /api/stock/search`
搜索股票(代码、名称、行业)。

| 参数 | 类型 | 说明 |
|------|------|------|
| q | string | 搜索关键词(必填) |

```bash
GET /api/stock/search?q=茅台
```

---

### 日线数据

#### `GET /api/stock/daily/{ts_code}`
获取股票日线数据(前复权)，包含价格、均线、市盈率(pe)、市净率(pb)等指标

| 参数 | 类型 | 说明 |
|------|------|------|
| start_date | string | 开始日期 YYYYMMDD(可选) |
| end_date | string | 结束日期 YYYYMMDD(可选) |
| limit | int | 返回条数(默认100，最大5000) |

```bash
# 获取最近30天日线
GET /api/stock/daily/600519.SH?limit=30

# 获取指定日期范围
GET /api/stock/daily/600519.SH?start_date=20250101&end_date=20250328
```

---

### 股东人数

#### `GET /api/stock/holder/{ts_code}`
获取股东人数变化历史。

| 参数 | 类型 | 说明 |
|------|------|------|
| limit | int | 返回条数(默认10，最大100) |

```bash
GET /api/stock/holder/600519.SH?limit=10
```

返回: `[{"ts_code": "600519.SH", "ann_date": "20250813", "holder_num": 220658, ...}, ...]`
ann_date: 公告发布时间
holder_num: 股东人数

---

### 公告搜索

#### `GET /api/ann/recent/{stock_name}`
获取股票公告列表，会自动下载 PDF 到本地。

| 参数 | 类型 | 说明 |
|------|------|------|
| days | int | 天数(可选，不传则获取所有历史) |
| max_pages | int | 最多获取页数(每页30条，默认3，最大100) |

```bash
# 获取最近30天公告
GET /api/ann/recent/贵州茅台?days=30

# 获取所有历史公告(最多90条)
GET /api/ann/recent/贵州茅台
```

返回:
```json
{
  "success": true,
  "data": [
    {
      "title": "贵州茅台关于高级管理人员被实施留置的公告",
      "time": 1773417600000,
      "date": "2026-03-14",
      "sec_name": "贵州茅台",
      "announcement_id": "1225009431",
      "pdf_path": "/path/to/xxx.pdf"
    }
  ]
}
```

---

#### `GET /api/ann/search`
搜索股票公告(支持关键词)。

| 参数 | 类型 | 说明 |
|------|------|------|
| stock_name | string | 股票名称或代码(必填) |
| keyword | string | 公告关键词(可选，如"年报"、"季报") |
| days | int | 天数(可选，不传则获取所有历史) |
| max_pages | int | 最多获取页数(默认10) |

```bash
# 搜索年报
GET /api/ann/search?stock_name=贵州茅台&keyword=年报

# 搜索所有历史季报
GET /api/ann/search?stock_name=贵州茅台&keyword=季报
```

---

#### `GET /api/ann/content`
读取公告 PDF 正文内容。

| 参数 | 类型 | 说明 |
|------|------|------|
| pdf_path | string | PDF文件路径(必填)，使用公告接口返回的 `pdf_path` |

```bash
GET /api/ann/content?pdf_path=/path/to/贵州茅台_关于xxx的公告_1225009431.pdf
```

返回:
```json
{
  "success": true,
  "data": [
    {
      "success": true,
      "file_path": "/path/to/xxx.pdf",
      "file_name": "xxx.pdf",
      "file_size": 71386,
      "page_count": 1,
      "text_content": "证券代码：600519 证券简称：贵州茅台...",
      "error_message": ""
    }
  ]
}
```

---


## 股票代码格式

- 上海证券交易所: `XXXXXX.SH` (如 `600519.SH`)
- 深圳证券交易所: `XXXXXX.SZ` (如 `000001.SZ`)

## 日期格式

所有日期参数使用 `YYYYMMDD` 格式，如 `20250328`。

## 公告 PDF 保存位置

默认保存在 `$STOCK_HOME/run/ann_downloads/` 目录下，按股票名称和日期组织。
