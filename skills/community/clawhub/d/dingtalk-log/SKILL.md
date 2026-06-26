# 调用钉钉日志列表接口技能说明
## 技能名称
调用钉钉topapi/report/list接口获取用户日志列表

## 技能描述
该技能用于调用钉钉开放平台的`topapi/report/list`接口，获取企业/员工的日志列表（含日志创建人、创建时间、模板名称等），支持按模板名称、员工ID、时间范围等条件筛选查询。

## 前置条件
1. 应用权限：仅支持**企业内部应用/第三方企业应用**调用，需提前为应用申请「查询企业员工日志权限」；第三方个人应用不支持。
2. AccessToken准备：调用接口前必须先获取对应应用的access_token：
   - 接口地址：`https://api.dingtalk.com/v1.0/oauth2/accessToken`
   - 请求方式：POST
   - 请求体参数：
     | 名称      | 类型   | 必填 | 说明                     |
     |-----------|--------|------|--------------------------|
     | appKey    | String | 是   | 企业内部应用的Cilent ID  |
     | appSecret | String | 是   | 企业内部应用的Cilent Secret |
   - AccessToken规则：有效期7200秒（2小时），需缓存避免频繁调用；重复获取会续期，过期返回新值。

## 接口核心信息
### 1. 基础调用信息
- 请求方式：POST
- 请求地址：`https://oapi.dingtalk.com/topapi/report/list`
- 字符编码：UTF-8

### 2. 请求参数
#### （1）Query参数（URL拼接）
| 名称         | 类型   | 必填 | 示例值     | 描述                                  |
|--------------|--------|------|------------|---------------------------------------|
| access_token | String | 是   | 6d1bxxxx   | 应用凭证（从前置步骤获取）|

#### （2）Body参数（JSON格式）
| 名称                | 类型   | 必填 | 示例值          | 描述                                                                 |
|---------------------|--------|------|-----------------|----------------------------------------------------------------------|
| start_time          | Number | 是   | 1507564800000   | 日志创建开始时间（Unix毫秒级时间戳）|
| end_time            | Number | 是   | 1507564800000   | 日志创建结束时间（Unix毫秒级时间戳）；与start_time间隔≤180天          |
| template_name       | String | 否   | 周报            | 日志模板名称（传值则筛选该模板的日志）|
| userid              | String | 否   | user123         | 员工userId（传值则筛选该员工的日志）|
| cursor              | Number | 是   | 0               | 查询游标（初始传0，后续从返回值取next_cursor）|
| size                | Number | 是   | 10              | 每页数据量（最大值20）|
| modified_start_time | Number | 否   | 1507564800000   | 日志修改开始时间（Unix毫秒级时间戳）|
| modified_end_time   | Number | 否   | 1507564800000   | 日志修改结束时间（Unix毫秒级时间戳）|

### 3. 参数传递规则（核心）
- 查指定模板+时间段日志：传`template_name`，`userId`为空；
- 查指定员工+时间段日志：传`userId`，`template_name`为空；
- 查企业所有日志：`template_name`和`userId`均为空；
- 分页查询：首次`cursor=0`，若返回`has_more=true`，则用`next_cursor`作为新游标继续调用。

## 返回结果解析
### 1. 返回参数结构
| 名称      | 类型      | 说明                     |
|-----------|-----------|--------------------------|
| errcode   | Number    | 返回码（0=成功）|
| errmsg    | String    | 返回描述（ok=成功）|
| result    | PageVo    | 核心结果集               |
| request_id| String    | 请求ID（用于排查问题）|

#### result子参数
| 名称        | 类型           | 说明                     |
|-------------|----------------|--------------------------|
| data_list   | ReportOapiVo[] | 日志列表（核心数据）|
| size        | Number         | 实际返回数据量           |
| next_cursor | Number         | 下一页游标               |
| has_more    | Boolean        | 是否有下一页（true=有）|

#### data_list子参数（单条日志）
| 名称          | 类型   | 说明                     |
|---------------|--------|--------------------------|
| create_time   | Number | 日志创建时间（毫秒时间戳） |
| creator_id    | String | 日志创建人userId         |
| creator_name  | String | 日志创建人姓名           |
| template_name | String | 日志模板名称             |
| contents      | Array  | 日志具体内容（key-value） |
| report_id     | String | 日志唯一ID               |

### 2. 返回示例
```json
{
    "errcode": 0,
    "errmsg":"ok",
    "result": {
        "data_list": [
            {
                "contents": [
                    {
                        "key": "今日完成工作",
                        "sort": "0",
                        "type": "1",
                        "value": "今天已经完成的工作"
                    }
                ],
                "create_time": 1605680704000,
                "creator_id": "user123",
                "creator_name": "测试同学",
                "template_name": "日报"
            }
        ],
        "has_more": false,
        "next_cursor": 2862455276,
        "size": 10
    },
    "request_id": "5c8q6ic6wyah"
}
```

## 调用步骤（标准化流程）
1. 调用`/v1.0/oauth2/accessToken`获取access_token，缓存该值（避免重复调用）；
2. 构造日志查询的Body参数（必填：start_time、end_time、cursor、size；可选：template_name、userId等）；
3. 发送POST请求到`https://oapi.dingtalk.com/topapi/report/list?access_token=xxx`，传入Body参数；
4. 解析返回结果：
   - 若`errcode=0`，提取`result.data_list`获取日志数据；
   - 若`has_more=true`，用`next_cursor`作为新游标重复步骤3，直到`has_more=false`；
5. 异常处理：若`errcode≠0`，根据`errmsg`排查权限/参数问题（如access_token过期、时间范围超限等）。

## 注意事项
1. 时间参数：所有时间戳均为**毫秒级Unix时间戳**，start_time与end_time间隔不超过180天；
2. 频率限制：禁止频繁调用gettoken接口，否则会被拦截；
3. 权限校验：调用前务必确认应用已添加「查询企业员工日志权限」。

### 总结
1. 调用核心：先获取access_token，再按条件（模板/员工/全量）传参调用日志列表接口，支持分页；
2. 参数规则：start_time/end_time/cursor/size为必填，template_name和userId按需传值（均空则查全量）；
3. 关键限制：时间范围≤180天、每页size≤20、access_token需缓存且有效期2小时。