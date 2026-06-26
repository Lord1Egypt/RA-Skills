# 巨潮资讯网 (CNINFO) API 参考

巨潮资讯网 (cninfo.com.cn) 是中国证监会指定的上市公司信息披露网站，覆盖深交所(主板+创业板)、上交所(主板+科创板)全部A股公告。

## 基础信息

- **网站**: http://www.cninfo.com.cn
- **状态**: 2026-05 可达 (HTTP 200, ~0.3s)
- **限流**: 无明显限流，但建议 ≥1s/次

## API 端点

### 1. 全文搜索 (推荐 — 最通用)

```
POST http://www.cninfo.com.cn/new/fulltextSearch/full
Content-Type: application/x-www-form-urlencoded
```

**参数**:

| 参数 | 说明 | 示例 |
|------|------|------|
| `searchkey` | 搜索关键词 (股票代码/名称/关键字) | `000001` |
| `sdate` | 开始日期 (YYYY-MM-DD) | `2026-01-01` |
| `edate` | 结束日期 | `2026-05-14` |
| `isfulltext` | 是否全文搜索 | `false` |
| `sortName` | 排序字段 | `pubdate` |
| `sortType` | 排序方向 | `desc` |
| `pageNum` | 页码 | `1` |
| `pageSize` | 每页条数 | `20` |

**响应字段**:

| 字段 | 说明 |
|------|------|
| `announcements[]` | 公告列表 |
| `.announcementId` | 公告ID (用于详情页) |
| `.announcementTitle` | 标题 (含 `<em>` 高亮标签) |
| `.announcementTime` | 时间戳(毫秒) |
| `.adjunctUrl` | PDF路径 (相对路径) |
| `.secCode` | 股票代码 |
| `.secName` | 股票名称 |
| `.orgId` | 机构ID (格式 `gssz0000001`) |

**bash 示例**:

```bash
curl -s "http://www.cninfo.com.cn/new/fulltextSearch/full" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "searchkey=000001&pageNum=1&pageSize=5&sortName=pubdate&sortType=desc"
```

### 2. 全市场最新公告

```
POST http://www.cninfo.com.cn/new/hisAnnouncement/query
Content-Type: application/x-www-form-urlencoded
```

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `column` | 板块 | `szse` (深交所) — **当前唯一有效的值** |
| `plate` | 板块代码 | `sze` |
| `tabName` | 标签 | `fulltext` |
| `stockType` | 股票类型 | `stock` |
| `pageNum` | 页码 | `1` |
| `pageSize` | 每页条数 | `10` |
| `seDate` | 日期范围 | `2026-05-12~2026-05-14` |

**注意**: `stock=000001,sze` 参数**已失效** (返回0条)。个股查询请用全文搜索API。`column=shse`(沪市)/`column=gem`(创业板) 等**均失效**。

### 3. 公告详情页

```
GET http://www.cninfo.com.cn/new/disclosure/detail
  ?stockCode=000001
  &announcementId=1225188743
  &orgId=gssz0000001
```

返回HTML页面，含公告全文。

### 4. PDF下载 (旧格式 — 已失效)

```
GET http://www.cninfo.com.cn/finalpage/2026-04-25/1225188743.PDF
```
返回 **HTTP 404**。建议通过 iFinD HTTP API (如有token) 或从详情页提取正文。

## 与 iFinD / Tushare Pro 对比

| 能力 | CNINFO | iFinD HTTP | Tushare Pro |
|------|--------|------------|-------------|
| 关键词搜索 | 灵活 | 需精确条件 | 需精确条件 |
| 全文PDF | 404 | 可下载 | 仅链接 |
| 公告正文 | 详情页HTML | 可配 | 无 |
| 限流风险 | 极低 | 周配额1万条 | 积分制 |
| 无需Key | 是 | 需token | 需token |

## 历史变更

- **2026-05**: `stock=xxx` 个股查询参数失效；`column=shse/gem` 等失效；PDF直链404；全文搜索API仍然稳定可用。
