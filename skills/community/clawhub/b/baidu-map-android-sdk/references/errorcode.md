# 错误码对照表

检索、路线等接口返回结果中带 error/errorCode 时，可参考下表。更多可查官方错误码文档。

| 状态码 | 含义 |
|--------|------|
| 0 | 正常 |
| 1 | 服务器内部错误（超时或系统错误） |
| 10 | 上传内容超过 8M |
| 101 | AK 参数不存在 |
| 102 | mcode 参数不存在（Mobile 类型必需 Mcode） |
| 200 | APP 不存在，AK 有误 |
| 201 | APP 被用户禁用 |
| 202 | APP 被管理员删除 |
| 203 | APP 类型错误（Server/Mobile/Browser 等） |
| 210 | APP IP 校验失败 |
| 211 | APP SN 校验失败 |
| 220 | APP Referer 校验失败 |
| 230 | APP Mcode 校验失败 |
| 240 | APP 服务被禁用 |
| 250 | 用户不存在 |
| 251 | 用户被自己删除 |
| 252 | 用户被管理员删除 |
| 260 | 服务不存在 |
| 261 | 服务被禁用 |
| 301 | 永久配额超限 |
| 302 | 天配额超限 |
| 401 | 并发量超过约定并发配额 |
| 402 | 并发超限且总并发也超总配额 |

检索/路线结果判断：结果类（如 PoiResult、DrivingRouteResult）有 **result.error** 字段，类型为 **SearchResult.ERRORNO**（枚举）。成功：`result.error == SearchResult.ERRORNO.NO_ERROR`。

### 路线规划常用 ERRORNO

| 枚举值 | 含义 |
|--------|------|
| NO_ERROR | 成功 |
| RESULT_NOT_FOUND | 未找到路线 |
| AMBIGUOUS_ROURE_ADDR | 起终点或途经点地址歧义，可 result.getSuggestAddrInfo() |

### POI 检索常用 ERRORNO

| 枚举值 | 含义 |
|--------|------|
| NO_ERROR | 成功 |
| RESULT_NOT_FOUND | 未找到 |
| AMBIGUOUS_KEYWORD | 关键字在本市无、其他城市有，可 result.getSuggestCityList() |
