# 钉钉日志API规范

## 目录
1. [获取access_token](#1-获取access_token)
2. [用户详情](#2-用户详情)
3. [获取模板](#3-获取模板)
4. [创建日志](#4-创建日志)
5. [查询日志](#5-查询日志)
6. [搜索用户工号](#6-搜索用户工号)

---

## 1. 获取access_token

**接口地址**：`https://oapi.dingtalk.com/gettoken`  
**请求方式**：GET  
**用途**：获取企业内部应用的access_token，用于后续API调用鉴权

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| appkey | String | 是 | 应用的唯一标识 |
| appsecret | String | 是 | 应用的密钥 |

### 返回示例

```json
{
  "errcode": 0,
  "access_token": "96fc7a7axxx",
  "errmsg": "ok",
  "expires_in": 7200
}
```

### 返回参数说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| errcode | Number | 错误码，0表示成功 |
| access_token | String | 生成的access_token |
| errmsg | String | 错误信息 |
| expires_in | Number | access_token的过期时间，单位秒（默认7200秒，2小时） |

### 注意事项
- access_token有效期为2小时，建议缓存复用
- 不要频繁调用，每天有调用次数限制

---

## 2. 用户详情

**接口地址**：`https://oapi.dingtalk.com/topapi/v2/user/get`  
**请求方式**：POST  
**用途**：获取用户详细信息（姓名、职位、工号等）

### Query参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | String | 是 | 接口调用凭证 |

### Body参数

```json
{
  "userid": "2021",
  "language": "zh_CN"
}
```

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | String | 是 | 用户的工号 |
| language | String | 否 | 语言，默认zh_CN |

### 返回示例

```json
{
  "errcode": 0,
  "result": {
    "name": "开发",
    "userid": "2021",
    "title": "",
    "job_number": "",
    "unionid": "",
    "dept_id_list": [],
    "active": true,
    "admin": true
  },
  "errmsg": "ok"
}
```

---

## 3. 获取模板

**接口地址**：`https://oapi.dingtalk.com/topapi/report/template/getbyname`  
**请求方式**：POST  
**用途**：根据模板名称获取模板详情（模板ID、字段列表）

### Query参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | String | 是 | 接口调用凭证 |

### Body参数

```json
{
  "userid": "2021",
  "template_name": "日报"
}
```

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | String | 是 | 用户工号 |
| template_name | String | 是 | 模板名称，目前支持：日报、周报 |

### 返回示例

```json
{
  "errcode": 0,
  "result": {
    "name": "日报",
    "id": "17956cc991da45dee70cb79433a8a757",
    "fields": [
      {
        "sort": 0,
        "type": 1,
        "field_name": "今日完成工作"
      },
      {
        "sort": 1,
        "type": 1,
        "field_name": "未完成工作"
      },
      {
        "sort": 2,
        "type": 1,
        "field_name": "需协调工作"
      }
    ],
    "userid": "2021"
  },
  "errmsg": "ok"
}
```

### 字段说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | String | 模板ID，用于创建日志 |
| fields | Array | 模板字段列表 |
| fields[].sort | Number | 字段排序序号（创建日志时需要） |
| fields[].type | Number | 字段类型，1表示文本 |
| fields[].field_name | String | 字段名称 |

---

## 4. 创建日志

**接口地址**：`https://oapi.dingtalk.com/topapi/report/create`  
**请求方式**：POST  
**用途**：创建并发送日报/周报

### Query参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | String | 是 | 接口调用凭证 |

### Body参数

```json
{
  "create_report_param": {
    "contents": [
      {
        "content_type": "markdown",
        "sort": "0",
        "type": "1",
        "content": "完成项目文档编写",
        "key": "今日完成工作"
      },
      {
        "content_type": "markdown",
        "sort": "1",
        "type": "1",
        "content": "继续优化性能",
        "key": "未完成工作"
      },
      {
        "content_type": "markdown",
        "sort": "2",
        "type": "1",
        "content": "无",
        "key": "需协调工作"
      }
    ],
    "template_id": "17956cc991da45dee70cb79433a8a757",
    "userid": "2021",
    "to_chat": true,
    "to_userids": ["user123", "user456"]
  }
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| contents | Array | 是 | 日志内容数组 |
| contents[].content_type | String | 是 | 内容类型，固定为"markdown" |
| contents[].sort | String | 是 | 字段序号（从模板获取） |
| contents[].type | String | 是 | 字段类型，固定为"1" |
| contents[].content | String | 是 | 日志内容，支持Markdown，不超过1000字符 |
| contents[].key | String | 是 | 字段名称 |
| template_id | String | 是 | 模板ID |
| userid | String | 是 | 创建者工号 |
| to_userids | Array | 否 | 接收人工号列表 |
| to_chat | Boolean | 否 | 是否发送消息通知，默认false |
| to_cids | String | 否 | 发送到的群ID |

### 返回示例

```json
{
  "errcode": 0,
  "result": "1734xxxxxxe08500e",
  "request_id": "5kaikoe9uc8i"
}
```

### 注意事项
- content内容支持Markdown语法
- 单个字段内容不超过1000字符
- sort值必须与模板字段的sort对应

---

## 5. 查询日志

**接口地址**：`https://oapi.dingtalk.com/topapi/report/list`  
**请求方式**：POST  
**用途**：查询用户发送的日报/周报列表

### Query参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| access_token | String | 是 | 接口调用凭证 |

### Body参数

```json
{
  "userid": "2021",
  "template_name": "日报",
  "start_time": 1774800128000,
  "end_time": 1774882928000,
  "cursor": 0,
  "size": 10
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userid | String | 是 | 查询用户的工号 |
| template_name | String | 是 | 模板名称（日报、周报） |
| start_time | Number | 是 | 查询开始时间，Unix时间戳（毫秒） |
| end_time | Number | 是 | 查询结束时间，Unix时间戳（毫秒） |
| cursor | Number | 否 | 分页游标，默认0 |
| size | Number | 否 | 每页数量，默认10 |

### 返回示例

```json
{
  "errcode": 0,
  "result": {
    "data_list": [
      {
        "report_id": "19d3e827cfe7b500369eb14429c8cd18",
        "template_name": "日报",
        "creator_id": "2021",
        "creator_name": "",
        "dept_name": "",
        "create_time": 1774870232000,
        "modified_time": 1774870232000,
        "contents": [
          {
            "sort": "0",
            "type": "1",
            "key": "今日完成工作",
            "value": "无"
          },
          {
            "sort": "1",
            "type": "1",
            "key": "未完成工作",
            "value": "无"
          },
          {
            "sort": "2",
            "type": "1",
            "key": "需协调工作",
            "value": "无"
          }
        ]
      }
    ],
    "has_more": false,
    "next_cursor": 6902435413,
    "size": 10
  },
  "errmsg": "ok"
}
```

### 注意事项
- 时间跨度不能超过180天
- 时间参数为Unix时间戳，单位为毫秒
- has_more为true时表示还有更多数据，可使用next_cursor继续查询

---


## 6. 搜索用户工号

**接口地址**：`https://api.dingtalk.com/v1.0/contact/users/search`  
**请求方式**：POST  
**用途**：搜索用户工号获取userid

### Query参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| query-word | String | 是 | 搜索关键词（用户姓名） |
| offset | String | 是 | 分页偏移量（可选，默认 0） |
| size | String | 是 | 每页数量（可选，默认 10） |
| full-match | String | 是 | 是否完全匹配（可选，1=完全匹配，0=模糊匹配，默认 1） |

### Body参数

```json
{
    "queryWord": "小红",
    "offset": 0,
    "size": 10,
    "fullMatchField": 1
}
```

### 返回参数说明

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| list | Array |  | 查询用户的工号 |
### 返回示例

```json
{
  "list": ["2021100111"],
  "hasMore": false,
  "totalCount": 3
}
```

### 注意事项
- 时间跨度不能超过180天
- 时间参数为Unix时间戳，单位为毫秒
- has_more为true时表示还有更多数据，可使用next_cursor继续查询

---

## 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| 40014 | 不合法的access_token | 检查AppKey和AppSecret是否正确 |
| 40035 | 不合法的参数 | 检查参数格式和必填项 |
| 60011 | 没有调用该接口的权限 | 联系管理员开通接口权限 |
| 60012 | 不允许调用该接口 | 检查应用是否有相关权限 |

## 时间戳转换示例

### JavaScript
```javascript
// 获取当前时间戳（毫秒）
const now = Date.now();

// 获取指定日期的时间戳
const timestamp = new Date('2025-01-15').getTime();

// 时间戳转日期
const date = new Date(1774870232000);
```

### Node.js
```javascript
// 获取本周开始时间（周一 00:00:00）
function getWeekStart() {
  const now = new Date();
  const day = now.getDay() || 7;
  now.setDate(now.getDate() - day + 1);
  now.setHours(0, 0, 0, 0);
  return now.getTime();
}

// 获取本月开始时间（1日 00:00:00）
function getMonthStart() {
  const now = new Date();
  now.setDate(1);
  now.setHours(0, 0, 0, 0);
  return now.getTime();
}
```
