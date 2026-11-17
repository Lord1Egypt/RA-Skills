# 小递查查快递查询 API 参考（xdccy.com）

> 来源：小递查查《快递物流查询 API 接口文档》V1.0（2026-05-02）
> 接口地址：`https://api.xdccy.com/IsvApi/GetXdccTrackInfoV2`
> 本技能在客户端层做「批量单号」并发批处理，底层仍是该单号接口。

## 1. 基本信息

| 项目 | 说明 |
|---|---|
| 报文格式 | JSON，UTF-8 |
| Content-Type | `application/x-www-form-urlencoded;charset=utf-8` |
| 请求方式 | POST |
| 平均响应 | 200ms |
| 请求超时 | 8000ms |
| 频率限制 | **无限制**（故本技能默认并发 5，可上调） |
| 通信协议 | HTTPS |

## 2. 安全机制（签名）

采用 **IP 认证 + 签名** 双重机制，防篡改 + 身份认证。

### 2.1 POST 必传参数

| 参数 | 说明 |
|---|---|
| `PlatformID` | 平台 ID（客服分配） |
| `RequestData` | 业务请求数据（JSON，**需 URL 编码**，UTF-8） |
| `DataSign` | 数据签名（见下） |

### 2.2 DataSign 生成步骤

1. 拼接原始字符串：`未URL编码的RequestData` + `APIKey`
2. 对拼接串做 **MD5**（32 位小写 hex）
3. 对 MD5 结果做 **Base64 编码**（⚠️ 编码的是 hex 字符串本身，非 16 字节）
4. 对 Base64 结果做 **URL（UTF-8）编码** → 最终 `DataSign`

```
原始 = {"MemberID":"123","Tel":"8789","No":"118954907573","ReturnFormat":"JSON"} + APIKey
MD5  = 42e8b3d72bc5036697443df68362f8ba
B64  = NDJlOGIzZDcyYmM1MDM2Njk3NDQzZGY2ODM2MmY4YmE=
Sign = NDJlOGIzZDcyYmM1MDM2Njk3NDQzZGY2ODM2MmY4YmE%3d
```

校验逻辑（服务端）：用 PlatformID 取对应 APIKey，对 RequestData 重算摘要，与收到的
DataSign（解码后）比对，一致则通过。

## 3. 请求参数

| 名称 | 类型(长度) | 必填 | 说明 |
|---|---|---|---|
| PlatformID | String | 是 | 平台 ID |
| DataSign | String | 是 | 签名 |
| RequestData | String | 是 | 业务数据（URL 编码） |
| MemberID | String(20) | 是 | 会员唯一 ID（内嵌 RequestData） |
| Tel | String(15) | 条件选填 | **顺丰、中通必填**，发/收件人手机号后四位（内嵌 RequestData） |
| ReturnFormat | String | 否 | 默认返回字符串；传 `JSON` 返回 JSON 对象 |
| No | String | 是 | 运单号（内嵌 RequestData） |

### RequestData 示例（URL 编码前）

```json
{"MemberID":"123","Tel":"8789","No":"118954907573","ReturnFormat":"JSON"}
```

### 最终 POST 体示例

```
PlatformID=123&RequestData=%7b%27MemberID%27%3a%27123%27%2c%27Tel%27%3a%278789%27%2c%27No%27%3a%27118954907573%27%2c%27ReturnFormat%27%3a%27JSON%27%7d&DataSign=NDJlOGIzZDcyYmM1MDM2Njk3NDQzZGY2ODM2MmY4YmE%3d
```

## 4. 整体报文结构

| 节点 | 类型 | 说明 |
|---|---|---|
| Code | Integer | 状态码，200=成功 |
| Message | String | 状态描述 |
| DebugMsg | String | 调试信息（同 Message） |
| Data | Object | 物流核心数据（见下） |

> 实战注意：当单号无轨迹时，Data 返回**精简对象**（含 `result`/`message`/`ShipperCode`
> /`LogisticCode`/`ExpressName`/`Count` 等，`State`/`StateDesc` 为 `null`）。本技能对此做了
> 容错：状态显示「未知」并附 `message` 说明，不视为失败（仍 Code=200）。

## 5. Data 核心字段

### 5.1 基础信息

| 字段 | 类型 | 说明 |
|---|---|---|
| Create_Time | String | 接口请求生成时间 YYYY-MM-DD HH:MM:SS |
| Pickup_Time | String | 揽收时间 |
| FirstIssue_Time | String | 首次发出时间 |
| FirstArrival_Time | String | 首次到达转运中心时间 |
| LeaveDistributionCenter_Time | String | 离开首个转运中心时间 |
| Dispatch_Time | String | 派件开始时间 |
| SignFor_Time | String | 签收时间 |
| LastUpdate_Time | String | 物流最后更新时间 |
| LastRequest_Time | String | 本次请求时间 |
| Pickup_Courier | String | 揽收快递员/网点 |
| Pickup_Courier_Phone | String? | 揽收员电话（可空） |
| Pickup_Network | String? | 揽收网点（可空） |
| Pickup_City | String | 揽收城市 |
| Delivery_Network | String? | 派送网点（可空） |
| Delivery_City | String | 派送城市 |
| Delivery_Courier | String | 派送快递员 |
| Delivery_Courier_Phone | String | 派送员电话 |
| FirstArrival_Name | String | 首次到达转运中心名称 |
| ShipperCode | String | 快递公司编码（ZTO=中通） |
| LogisticCode | String | 快递单号 |
| ExpressName | String | 快递公司名称 |
| State | Integer | 状态码（3=已签收） |
| StateDesc | String | 状态描述 |
| LastTrace | String | 最后一条轨迹（精简） |
| Count | Integer | 轨迹总条数 |

### 5.2 时效时长字段（单位：分钟）

| 字段 | 说明 |
|---|---|
| FirstIssue_TimeSpan | 揽收→首次发出 |
| FirstArrival_TimeSpan | 揽收→首次到达转运 |
| LeaveDistributionCenter_TimeSpan | 揽收→离开首个转运 |
| HalfwayStagnation_TimeSpan | 中途停滞 |
| Dispatch_TimeSpan | 揽收→开始派件 |
| SignFor_TimeSpan | 揽收→完成签收 |

### 5.3 超时标记字段（0=未超时，1=超时）

| 字段 | 说明 |
|---|---|
| Pickup_TimeOut | 揽收超时 |
| FirstIssue_TimeOut | 首次发出超时 |
| FirstArrival_TimeOut | 首次到达转运超时 |
| LeaveDistributionCenter_TimeOut | 离开转运超时 |
| HalfwayStagnation_TimeOut | 中途停滞超时 |
| Dispatch_TimeOut | 派件超时 |
| SignFor_TimeOut | 签收超时 |

### 5.4 物流轨迹列表 TraceList

JSON 数组，元素字段：

| 字段 | 说明 |
|---|---|
| time | 轨迹时间 YYYY-MM-DD HH:MM:SS |
| desc | 轨迹描述 |

> 轨迹**倒序**排列（最新在前）。

## 6. 状态码

| 码 | 说明 |
|---|---|
| 200 | 成功 |
| 400 | 参数错误（查单号格式 / 缺 Tel） |
| 401 | 签名校验失败 / 身份认证失败 |
| 500 | 服务器异常 |

> 网络层异常本技能映射为 Code -1（网络错误）/-2（请求异常）/-3（响应非 JSON）。

## 7. 注意事项

- 所有时间字段均为东八区（GMT+8）`YYYY-MM-DD HH:MM:SS`。
- 超时标记 1=超时，0=未超时，判定规则结合业务场景。
- TraceList 按时间**倒序**（最新在前）。
- 签名严格遵循「原始RequestData+APIKey → MD5 → Base64 → URL 编码」，编码统一 UTF-8。
- 部分字段（如 Pickup_Courier_Phone、Pickup_Network）可能为空，需做非空判断。
- 顺丰、中通查询**必须**传 Tel（手机号后四位），否则返回 400。
