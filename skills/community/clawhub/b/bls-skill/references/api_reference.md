# BLS API Reference

## Service Endpoints

| Region | Endpoint| Protocol |
| --- | --- | --- |
|  华北-北京| bls-log.bj.baidubce.com | HTTP/HTTPS |
|  华南-广州| bls-log.gz.baidubce.com | HTTP/HTTPS |
|  华东-苏州| bls-log.su.baidubce.com | HTTP/HTTPS |
|  华北-保定| bls-log.bd.baidubce.com | HTTP/HTTPS |
|  金融华中-武汉| bls-log.fwh.baidubce.com | HTTP/HTTPS |
|  华北-阳泉| bls-log.yq.baidubce.com | HTTP/HTTPS |
|  华北-南京| bls-log.nj.baidubce.com| HTTP/HTTPS |
|  西南-成都| bls-log.cd.baidubce.com | HTTP/HTTPS |
|  中国香港| bls-log.hkg.baidubce.com | HTTP/HTTPS |

## Authentication

BCE auth header: `bce-auth-v1/{accessKeyId}/{timestamp}/{expirationPeriodInSeconds}/{signedHeaders}/{signature}`

Details: https://cloud.baidu.com/doc/Reference/s/Njwvz1wot

---

## 1. ListProject - 获取日志组列表

```
GET /v1/project?name={name}&pageNo={pageNo}&pageSize={pageSize}
Host: <Endpoint>
```

Response:
```json
{
  "result": [{"name": "default", "description": "my project"}],
  "pageNo": 1, "pageSize": 10, "totalCount": 1
}
```

---

## 2. ListLogStore - 获取日志集列表

```
GET /v1/logstore?project={project}&logStoreName={logStoreName}&pageNo={pageNo}&pageSize={pageSize}
Host: <Endpoint>
```

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| project | String | No | 日志组名称 |
| logStoreName | String | No | 日志集名称关键字过滤 |
| order | String | No | asc/desc, 默认 desc |
| orderBy | String | No | 排序字段, 默认 creationDateTime |
| pageNo | Int | No | 页码, 默认 1 |
| pageSize | Int | No | 每页数量, 默认 10 |

Response:
```json
{
  "result": [
    {
      "creationDateTime": "2019-09-10T15:30:20Z",
      "lastModifiedTime": "2019-09-10T15:30:20Z",
      "project": "default",
      "logStoreName": "demo",
      "retention": 7
    }
  ],
  "orderBy": "creationDateTime",
  "order": "desc",
  "pageNo": 1, "pageSize": 10, "totalCount": 1
}
```

---

## 3. DescribeLogStore - 获取日志集详情

```
GET /v1/logstore/{logStoreName}?project={project}
Host: <Endpoint>
```

Response:
```json
{
  "creationDateTime": "2019-09-10T15:30:20Z",
  "lastModifiedTime": "2019-09-10T15:30:20Z",
  "project": "default",
  "logStoreName": "demo",
  "retention": 7
}
```

---

## 4. DescribeIndex - 获取索引详情

```
GET /v1/logstore/{logStoreName}/index?project={project}
Host: <Endpoint>
```

Response contains `fulltext` (bool) and `fields` (object with field name -> type/stored mapping).

---

## 5. QueryLogRecord - 检索分析日志

```
GET /v1/logstore/{logStoreName}/logrecord?project={project}&query={query}&startDateTime={start}&endDateTime={end}
Host: <Endpoint>
```

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| project | String | No | 日志组名称 |
| logStoreName | String | Yes | 日志集名称 (Path) |
| logStreamName | String | No | 日志流名称 |
| query | String | Yes | Query语句 |
| startDateTime | DateTime | Yes | 起始时间 (UTC ISO8601, 如 2020-01-10T13:23:34Z) |
| endDateTime | DateTime | Yes | 结束时间 (UTC ISO8601) |
| marker | String | No | 检索翻页标记 |
| limit | Int | No | 返回条数, 0-1000, 默认 100 |
| sort | String | No | desc(默认)/asc |
| pageNo | Int | No | 分页页码 |
| pageSize | Int | No | 分页大小 |

### Query Syntax (3 formats)

1. **match 检索**: `match method:GET and status >= 400` (需开启索引)
2. **SQL 分析**: `select * limit 10` (无需 FROM 子句)
3. **match + SQL**: `match method:GET and status >= 400 | select host, count() group by host`

### Response (SQL)
```json
{
  "resultSet": {
    "queryType": "sql",
    "columns": ["level", "count()"],
    "columnTypes": ["string", "int"],
    "rows": [["DEBUG", 32], ["INFO", 1]]
  },
  "datasetScanInfo": {"processedRows": 100, "processedBytes": 1024}
}
```

### Response (match)
```json
{
  "resultSet": {
    "queryType": "match",
    "columns": ["@timestamp", "@seq", "@stream", "@raw"],
    "columnTypes": ["int", "int", "string", "string"],
    "rows": [[1567374000000, 1, "stream1", "log content..."]]
  },
  "nextMarker": "CN3W3Z-BMxD6gde_g6eFMyAD",
  "datasetScanInfo": {"isTruncated": false}
}
```
