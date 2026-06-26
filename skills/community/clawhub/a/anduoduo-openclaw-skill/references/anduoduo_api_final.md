# 安多多平台 API 文档

> 本文档仅描述接口能力、请求方式、数据结构和字段语义，不指定具体使用方。所有示例地址、API Key、业务标识均为占位值或脱敏值。

## 1. 文档概览

- **基础地址**：`{{BASE_URL}}`
- **接口前缀**：`/api/openclaw/v1`
- **认证方式**：请求头 `Authorization: {{API_KEY}}`
- **Content-Type**：除 GET/HEAD 外，默认使用 `application/json`
- **状态判定**：请同时检查 HTTP 状态码与响应体中的 `code` 字段；`HTTP 200` 不一定代表业务成功。

### 1.1 通用请求头

| 头名称 | 是否必填 | 类型 | 说明 | 示例值 |
| --- | --- | --- | --- | --- |
| Authorization | 是 | string | API Key，直接作为请求头值传入 | `{{API_KEY}}` |
| Accept | 否 | string | 建议声明可接收 JSON | `application/json` |
| Content-Type | 条件必填 | string | 请求体为 JSON 时使用 | `application/json` |

### 1.2 统一响应结构

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 业务状态码；通常 `200` 表示业务成功 |
| msg | string/null | 业务消息；失败时通常包含可读错误信息 |
| data | object/array/null | 业务数据主体 |
| requestId | string | 请求链路标识 |
| timestamp | long | 服务端时间戳（毫秒） |

统一响应示例：
```json
{
  "code": 200,
  "msg": null,
  "data": {},
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

### 1.3 实测校验结论（节选）

- 本阶段标准化测试共 **28** 项，全部通过，其中 reachability 为 **23** 项，HTTP semantics 为 **2** 项，invariants 为 **3** 项。
- 实测未观察到 `Bearer {API_KEY}` 兼容性，建议仅使用 `Authorization: {{API_KEY}}`。
- 对分页类接口，建议显式传入分页参数；其中风险分页接口建议至少传入 `page=1`。

## 2. 接口目录

- **扫描任务**：`POST /api/openclaw/v1/scans`、`GET /api/openclaw/v1/scans/{taskId}`
- **资产与风险**：`POST /api/openclaw/v1/assets/list`、`POST /api/openclaw/v1/cloud-instance/category/node`、`POST /api/openclaw/v1/risks/list`、`GET /api/openclaw/v1/risks/{riskId}`、`GET /api/openclaw/v1/riskSeverity/list`、`GET /api/openclaw/v1/ruleType/list`
- **风险聚合**：`POST /api/openclaw/v1/group-by/rule-type`、`POST /api/openclaw/v1/group-by/instance-type`、`POST /api/openclaw/v1/group-by/basic-reason`、`POST /api/openclaw/v1/group-by/severity`、`POST /api/openclaw/v1/group-by/rule-label`、`POST /api/openclaw/v1/group-by/rule-id`、`POST /api/openclaw/v1/group-by/account-id`
- **合规与报告**：`POST /api/openclaw/v1/ruleStandardsAndRegulation/list`、`POST /api/openclaw/v1/compliance/summary`、`POST /api/openclaw/v1/reports/compliance`、`GET /api/openclaw/v1/reports/{reportId}`
- **云账号与云厂商**：`GET /api/openclaw/v1/cloudAccounts/list`、`GET /api/openclaw/v1/cloudType/list`
- **规则**：`POST /api/openclaw/v1/rules/list`
- **云账号扩展能力**：`POST /api/openclaw/v1/cloudAccounts/add`

## 3. 扫描任务

### 发起实例扫描任务

- **方法与路径**：`POST /api/openclaw/v1/scans`
- **能力说明**：发起实例扫描任务。服务端会强制设置：`taskType=INSTANCE_SCAN`、`taskName=instance_scan_task`、`scope=FULL`。
- **实测补充说明**：
  - 鉴权方式实测为请求头 `Authorization: {{API_KEY}}`，未观察到 Bearer 兼容。
  - 请求体中的 `cloudAccountIds` 与 `cloudTypes` 至少提供一类更稳妥；不同云账号状态下返回结果可能不同。
  - 实测中：有效且空闲账号可返回任务数组；无效账号可能返回空数组；存在同步任务时可能返回业务错误 `exist sync task`。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| cloudAccountIds | 否 | array<string> | 云账号 ID 列表；为空时按 `cloudTypes` 自动补齐当前用户账号 | `["ca-001"]` |
| cloudTypes | 否 | array<string> | 云厂商类型列表 | `["tencent"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].id | string | 任务 ID | `ct-001` |
| data[].cloudAccountId | string | 云账号 ID | `ca-001` |
| data[].taskType | string | 任务类型 | `INSTANCE_SCAN` |
| data[].scope | string | 扫描范围 | `FULL` |
| data[].taskName | string | 任务名称 | `instance_scan_task` |
| data[].executeType | string | 执行类型 | `MANUAL` |
| data[].rules | string | 扫描规则（JSON 字符串） | `["rule-001"]` |
| data[].regions | string | 地域（JSON 字符串） | `{"ap-beijing":"beijing"}` |
| data[].instanceTypes | string | 实例类型（JSON 字符串） | `["CVM"]` |
| data[].instances | string | 实例（JSON 字符串） | `["ins-001"]` |
| data[].status | string | 任务状态 | `RUNNING` |
| data[].creator | string | 创建人 | `u-001` |
| data[].createdTime | string | 创建时间 | `null` |
| data[].modifiedTime | string | 修改时间 | `null` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/scans" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"cloudAccountIds": ["ca-001"],"cloudTypes": ["aliyun"]}'
```

#### 成功响应示例
```json
{
  "code": 200,
  "msg": null,
  "data": [
    {
      "id": "ct-001",
      "cloudAccountId": "ca-001",
      "taskType": "INSTANCE_SCAN",
      "scope": "FULL",
      "taskName": "instance_scan_task",
      "executeType": "MANUAL",
      "rules": "",
      "regions": "",
      "instanceTypes": "",
      "instances": "",
      "status": "RUNNING",
      "creator": "SYSTEM",
      "createdTime": null,
      "modifiedTime": null
    }
  ],
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

#### 常见业务错误示例
```json
{
  "code": 500,
  "msg": "exist sync task",
  "data": null,
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

### 查询扫描任务详情

- **方法与路径**：`GET /api/openclaw/v1/scans/{taskId}`
- **能力说明**：查询扫描任务详情、任务步骤、同步统计、扫描统计。
- **实测补充说明**：
  - `taskId` 应为扫描任务 ID。
  - 该接口用于查询扫描任务详情、步骤以及同步/扫描统计信息。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| taskId | 是 | string | 扫描任务 ID | `ct-001` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.detail.id | string | 任务 ID | `ct-001` |
| data.detail.status | string | 任务状态 | `RUNNING` |
| data.cloudInstanceVersion | string | 实例版本号 | `v-001` |
| data.taskSteps[].id | string | 步骤 ID | `step-1` |
| data.taskSteps[].cloudTaskId | string | 任务 ID | `ct-001` |
| data.taskSteps[].stepName | string | 步骤名称 | `sync` |
| data.taskSteps[].stepType | string | 步骤类型 | `SYNC` |
| data.taskSteps[].status | string | 步骤状态 | `SUCCESS` |
| data.taskSteps[].orderNum | integer | 排序 | `1` |
| data.taskSteps[].extend | string | 扩展字段 | `{}` |
| data.syncTask[].instanceType | string | 同步实例类型 | `CVM` |
| data.syncTask[].status | string | 同步状态 | `SUCCESS` |
| data.syncTask[].count | integer | 数量 | `3` |
| data.scanTask[].instanceType | string | 扫描实例类型 | `CVM` |
| data.scanTask[].status | string | 扫描状态 | `SUCCESS` |
| data.scanTask[].count | integer | 数量 | `3` |

#### 请求示例
```bash
curl -X GET "{{BASE_URL}}/api/openclaw/v1/scans/ct-001" \
  -H "Authorization: {{API_KEY}}" \
```

#### 成功响应示例
```json
{
  "code": 200,
  "msg": null,
  "data": {
    "detail": {
      "id": "ct-001",
      "status": "RUNNING"
    },
    "cloudInstanceVersion": "v-001",
    "taskSteps": [
      {
        "id": "cts-001",
        "cloudTaskId": "ct-001",
        "stepName": "SYNC",
        "stepType": "SYNC",
        "status": "SUCCESS",
        "orderNum": 1,
        "extend": "{}"
      }
    ],
    "syncTask": [
      {
        "instanceType": "CVM",
        "status": "SUCCESS",
        "count": 3
      }
    ],
    "scanTask": [
      {
        "instanceType": "CVM",
        "status": "RUNNING",
        "count": 3
      }
    ]
  },
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

## 4. 资产与风险

### 资产分页查询

- **方法与路径**：`POST /api/openclaw/v1/assets/list`
- **能力说明**：分页查询资产信息。
- **实测补充说明**：
  - 分页参数 `page`、`pageSize` 在实现上具有一定容忍度，但建议显式传入。
  - 返回体是分页对象，核心记录位于 `data.records`。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| page | 否 | integer | 页码（默认 1） | `1` |
| pageSize | 否 | integer | 每页条数（默认 20） | `20` |
| id | 否 | string | 资产 ID | `ci-001` |
| ids | 否 | array<string> | 资产 ID 列表 | `["ci-001"]` |
| name | 否 | string | 名称模糊检索（匹配 name/instanceId） | `web` |
| instanceId | 否 | string | 云平台实例 ID | `ins-001` |
| cloudAccountId | 否 | array<string> | 云账号 ID 列表 | `["ca-001"]` |
| instanceType | 否 | array<string> | 实例类型列表 | `["CVM"]` |
| cloudInstanceTags | 否 | array<string> | 实例标签列表 | `["env:prod"]` |
| cloudType | 否 | array<string> | 云厂商类型 | `["tencent"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.records[].id | string | 资产 ID | `ci-001` |
| data.records[].instanceId | string | 云平台实例 ID | `ins-001` |
| data.records[].cloudAccountId | string | 云账号 ID | `ca-001` |
| data.records[].instanceHashId | string | 实例 Hash ID | `hash-001` |
| data.records[].name | string | 实例名称 | `web-01` |
| data.records[].cloudType | string | 云厂商类型 | `tencent` |
| data.records[].instanceType | string | 实例类型 | `CVM` |
| data.records[].category | string | 分类 | `compute` |
| data.records[].graphCategory | string | 图分类 | `compute` |
| data.records[].osName | string | 操作系统 | `Linux` |
| data.records[].region | string | 地域编码 | `ap-beijing` |
| data.records[].regionName | string | 地域名称 | `Beijing` |
| data.records[].status | string | 状态 | `enable` |
| data.records[].info | string | 实例详情 JSON | `{"cpu":4}` |
| data.records[].extend | string | 扩展字段 JSON | `{"env":"prod"}` |
| data.records[].version | string | 版本 | `v-001` |
| data.records[].cloudUniqueId | string | 云账号唯一标识 | `uin-001` |
| data.records[].cloudAccountName | string | 云账号名称 | `MainAccount` |
| data.records[].displayInstanceType | string | 展示实例类型 | `CVM(S5)` |
| data.records[].description | string | 实例类型描述 | `S5` |
| data.records[].categoryName | string | 分类中文名 | `Compute` |
| data.records[].graphCategoryName | string | 图分类中文名 | `Compute` |
| data.total | integer | 总记录数 | `1` |
| data.size | integer | 每页大小 | `20` |
| data.current | integer | 当前页 | `1` |
| data.pages | integer | 总页数 | `1` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/assets/list" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"page": 1,"pageSize": 20}'
```

### 资产类型树节点查询

- **方法与路径**：`POST /api/openclaw/v1/cloud-instance/category/node`
- **能力说明**：按分类树返回资产数量统计，可用于资产分类面板/图谱面板。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| instanceType | 否 | array<string> | 实例类型 | `["CVM"]` |
| cloudAccountIds | 否 | array<string> | 云账号 ID 列表 | `["ca-001"]` |
| cloudTypes | 否 | array<string> | 云厂商类型列表 | `["tencent"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].categoryId | string | 分类 ID | `cat-root` |
| data[].category | string | 分类编码 | `root` |
| data[].categoryNameCn | string | 分类中文名 | `Root` |
| data[].categoryDescription | string | 分类描述 | `Root category` |
| data[].assetCount | integer | 分类资产总数 | `10` |
| data[].assetTypeCount | long | 分类资产类型数 | `2` |
| data[].sortBy | integer | 排序值 | `1` |
| data[].instanceTypeCount[].cloudType | string | 云厂商类型 | `tencent` |
| data[].instanceTypeCount[].instanceType | string | 实例类型 | `CVM` |
| data[].instanceTypeCount[].description | string | 实例类型描述 | `Compute` |
| data[].instanceTypeCount[].displayName | string | 实例类型展示名 | `CVM` |
| data[].instanceTypeCount[].assetCount | integer | 该类型资产数 | `5` |
| data[].instanceTypeCount[].commonField | boolean | 是否公共类型 | `false` |
| data[].subAssetCategoryCount[] | array | 子分类节点 | `[...]` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/cloud-instance/category/node" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 风险分页查询

- **方法与路径**：`POST /api/openclaw/v1/risks/list`
- **能力说明**：分页查询风险记录。
- **实测补充说明**：
  - 建议至少传入 `page=1`；实测中完全空请求体可能出现超时。
  - 返回体是分页对象，核心记录位于 `data.records`。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| page | 否 | integer | 页码（默认 1） | `1` |
| pageSize | 否 | integer | 每页条数（默认 20） | `20` |
| cloudInstanceId | 否 | string | 云实例 ID | `ci-001` |
| name | 否 | string | 风险规则名称 | `Open Port` |
| status | 否 | array<string> | 风险状态列表 | `["OPEN"]` |
| ruleId | 否 | string | 规则 ID | `rule-uuid-001` |
| instanceHashId | 否 | string | 实例 Hash ID | `hash-001` |
| instanceType | 否 | string | 实例类型 | `CVM` |
| cloudTypes | 否 | array<string> | 云厂商类型列表 | `["tencent"]` |
| severities | 否 | array<string> | 严重度列表 | `["高"]` |
| ruleTypes | 否 | array<string> | 规则类型列表 | `["MisConfig"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.records[].platformType | string | 外部工单平台类型 | `jira` |
| data.records[].ticketUrl | string | 工单链接 | `https://jira.example.com/browse/RISK-1` |
| data.records[].instanceInfo.id | string | 资产 ID | `ci-001` |
| data.records[].instanceInfo.instanceId | string | 云实例 ID | `ins-001` |
| data.records[].instanceInfo.cloudAccountId | string | 云账号 ID | `ca-001` |
| data.records[].instanceInfo.instanceHashId | string | 实例 Hash ID | `hash-001` |
| data.records[].instanceInfo.name | string | 资产名称 | `web-01` |
| data.records[].instanceInfo.cloudType | string | 云厂商类型 | `tencent` |
| data.records[].instanceInfo.instanceType | string | 实例类型 | `CVM` |
| data.records[].instanceInfo.category | string | 分类 | `compute` |
| data.records[].instanceInfo.graphCategory | string | 图分类 | `compute` |
| data.records[].instanceInfo.region | string | 地域 | `ap-beijing` |
| data.records[].instanceInfo.regionName | string | 地域名 | `Beijing` |
| data.records[].instanceInfo.status | string | 状态 | `enable` |
| data.records[].instanceInfo.version | string | 版本 | `v-001` |
| data.records[].instanceInfo.cloudUniqueId | string | 云账号唯一标识 | `uin-001` |
| data.records[].instanceInfo.cloudAccountName | string | 云账号名称 | `MainAccount` |
| data.records[].instanceInfo.displayInstanceType | string | 展示实例类型 | `CVM(S5)` |
| data.records[].rule.id | string | 规则 ID | `rule-001` |
| data.records[].rule.uuid | string | 规则业务 ID | `rule-uuid-001` |
| data.records[].rule.name | string | 规则名称 | `Open Port` |
| data.records[].rule.type | string | 规则类型 | `MisConfig` |
| data.records[].rule.version | string | 规则版本 | `v1` |
| data.records[].rule.status | string | 启用状态 | `enable` |
| data.records[].rule.description | string | 规则描述 | `Port open to internet` |
| data.records[].rule.impact | string | 影响 | `May expose service` |
| data.records[].rule.severity | string | 严重度 | `高` |
| data.records[].rule.categories[] | array<KV> | 分类列表 | `[{"key":"cat-001","value":"Network"}]` |
| data.records[].rule.providers[] | array<string> | 云厂商列表 | `["tencent"]` |
| data.records[].rule.basicReasons[] | array<KV> | 根因列表 | `[{"key":"reason-001","value":"SecurityGroup"}]` |
| data.records[].rule.standardsAndRegulations[] | array<KV> | 合规框架列表 | `[{"key":"sr-001","value":"Baseline"}]` |
| data.records[].rule.labels[] | array<KV> | 标签列表 | `[{"key":"label-001","value":"public-network"}]` |
| data.records[].riskMapping.id | string | 风险映射 ID | `rm-001` |
| data.records[].riskMapping.cloudTaskId | string | 任务 ID | `ct-001` |
| data.records[].riskMapping.cloudInstanceVersion | string | 实例版本 | `v-001` |
| data.records[].riskMapping.cloudAccountId | string | 云账号 ID | `ca-001` |
| data.records[].riskMapping.cloudInstanceId | string | 云实例 ID | `ci-001` |
| data.records[].riskMapping.instanceHashId | string | 实例 Hash ID | `hash-001` |
| data.records[].riskMapping.ruleId | string | 规则业务 ID | `rule-uuid-001` |
| data.records[].riskMapping.cloudType | string | 云厂商类型 | `tencent` |
| data.records[].riskMapping.instanceType | string | 实例类型 | `CVM` |
| data.records[].riskMapping.status | string | 风险状态 | `OPEN` |
| data.records[].riskMapping.message | string | 风险消息 | `22 is open` |
| data.records[].riskMapping.version | long | 版本号 | `1` |
| data.records[].riskMapping.creator | string | 创建人 | `u-001` |
| data.total | integer | 总记录数 | `1` |
| data.size | integer | 每页大小 | `20` |
| data.current | integer | 当前页 | `1` |
| data.pages | integer | 总页数 | `1` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/risks/list" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"page": 1,"pageSize": 20}'
```

### 风险详情

- **方法与路径**：`GET /api/openclaw/v1/risks/{riskId}`
- **能力说明**：查询单条风险详情。
- **实测补充说明**：
  - `riskId` 实测对应风险映射 ID，而非风险列表中任意其它 ID 字段。
  - 传入错误类型的 ID 时，服务端可能返回业务错误 `风险映射不存在!`。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| riskId | 是 | string | 风险映射 ID | `rm-001` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.platformType | string | 外部平台类型 | `jira` |
| data.ticketUrl | string | 工单链接 | `https://jira.example.com/browse/RISK-1` |
| data.instanceInfo.* | object | 资产信息 | 见上节 |
| data.rule.* | object | 规则信息 | 见上节 |
| data.riskMapping.* | object | 风险映射信息 | 见上节 |

#### 请求示例
```bash
curl -X GET "{{BASE_URL}}/api/openclaw/v1/risks/rm-001" \
  -H "Authorization: {{API_KEY}}" \
```

#### 常见业务错误示例
```json
{
  "code": 500,
  "msg": "风险映射不存在!",
  "data": null,
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

### 风险等级枚举

- **方法与路径**：`GET /api/openclaw/v1/riskSeverity/list`
- **能力说明**：返回风险严重度枚举列表。

#### 输入参数

该接口无独立业务参数，仅依赖认证信息。

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].code | string | 枚举编码 | `严重` |
| data[].label | string | 枚举显示名 | `严重` |

#### 请求示例
```bash
curl -X GET "{{BASE_URL}}/api/openclaw/v1/riskSeverity/list" \
  -H "Authorization: {{API_KEY}}" \
```

### 规则类型枚举

- **方法与路径**：`GET /api/openclaw/v1/ruleType/list`
- **能力说明**：返回规则类型枚举列表。

#### 输入参数

该接口无独立业务参数，仅依赖认证信息。

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].code | string | 枚举编码 | `Vulnerability` |
| data[].label | string | 枚举显示名 | `Vulnerability` |

#### 请求示例
```bash
curl -X GET "{{BASE_URL}}/api/openclaw/v1/ruleType/list" \
  -H "Authorization: {{API_KEY}}" \
```

## 5. 风险聚合

### 按规则类型聚合

- **方法与路径**：`POST /api/openclaw/v1/group-by/rule-type`
- **能力说明**：按规则类型聚合风险数量。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| cloudAccountIds | 否 | set<string> | 云账号 ID 集合（为空时按当前用户账号） | `["ca-001"]` |
| cloudTypes | 否 | set<string> | 云厂商类型集合 | `["tencent"]` |
| ruleTypes | 否 | set<string> | 规则类型集合 | `["MisConfig"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].type | string | 规则类型 | `MisConfig` |
| data[].count | long | 数量 | `12` |
| data[].severity | string | 严重度 | `高` |
| data[].cloudType | string | 云厂商类型 | `tencent` |
| data[].displayType | string | 展示名称 | `MisConfig` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/group-by/rule-type" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 按实例类型聚合

- **方法与路径**：`POST /api/openclaw/v1/group-by/instance-type`
- **能力说明**：按实例类型聚合风险数量。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| cloudAccountIds | 否 | set<string> | 云账号 ID 集合 | `["ca-001"]` |
| cloudTypes | 否 | set<string> | 云厂商类型集合 | `["tencent"]` |
| instanceTypes | 否 | set<string> | 实例类型集合 | `["CVM"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].type | string | 实例类型 | `CVM` |
| data[].count | long | 数量 | `8` |
| data[].severity | string | 严重度 | `中` |
| data[].cloudType | string | 云厂商类型 | `tencent` |
| data[].displayType | string | 展示名称 | `Cloud Virtual Machine` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/group-by/instance-type" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 按基础原因聚合

- **方法与路径**：`POST /api/openclaw/v1/group-by/basic-reason`
- **能力说明**：按基础原因聚合风险数量。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| cloudAccountIds | 否 | set<string> | 云账号 ID 集合 | `["ca-001"]` |
| cloudTypes | 否 | set<string> | 云厂商类型集合 | `["tencent"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].basicReason | string | 基础原因 | `SecurityGroup` |
| data[].count | long | 数量 | `5` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/group-by/basic-reason" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 按风险等级聚合

- **方法与路径**：`POST /api/openclaw/v1/group-by/severity`
- **能力说明**：按严重度维度返回风险统计汇总。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| cloudAccountIds | 否 | set<string> | 云账号 ID 集合 | `["ca-001"]` |
| cloudTypes | 否 | set<string> | 云厂商类型集合 | `["tencent"]` |
| severities | 否 | set<string> | 严重度过滤集合 | `["高"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.createTime | string | 统计版本时间 | `2026-03-11` |
| data.criticalRiskCount | integer | 严重风险数 | `1` |
| data.highRiskCount | integer | 高风险数 | `2` |
| data.mediumRiskCount | integer | 中风险数 | `3` |
| data.lowRiskCount | integer | 低风险数 | `4` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/group-by/severity" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 按规则标签聚合

- **方法与路径**：`POST /api/openclaw/v1/group-by/rule-label`
- **能力说明**：按规则标签聚合风险数量。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| cloudAccountIds | 否 | set<string> | 云账号 ID 集合 | `["ca-001"]` |
| cloudTypes | 否 | set<string> | 云厂商类型集合 | `["tencent"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].label | string | 标签 | `public-network` |
| data[].labelCount | integer | 数量 | `9` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/group-by/rule-label" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 按规则 ID 聚合

- **方法与路径**：`POST /api/openclaw/v1/group-by/rule-id`
- **能力说明**：按规则 ID 聚合风险数量。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| cloudAccountIds | 否 | set<string> | 云账号 ID 集合 | `["ca-001"]` |
| cloudTypes | 否 | set<string> | 云厂商类型集合 | `["tencent"]` |
| ruleIds | 否 | set<string> | 规则 ID 集合 | `["rule-001"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].ruleId | string | 规则 ID | `rule-001` |
| data[].ruleName | string | 规则名称 | `Open Port` |
| data[].severity | string | 严重度 | `高` |
| data[].count | long | 数量 | `7` |
| data[].cloudAccountId | string | 云账号 ID | `ca-001` |
| data[].instanceType | string | 实例类型 | `CVM` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/group-by/rule-id" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 按云账号 ID 聚合

- **方法与路径**：`POST /api/openclaw/v1/group-by/account-id`
- **能力说明**：按云账号维度聚合风险数量。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| cloudAccountIds | 否 | set<string> | 云账号 ID 集合 | `["ca-001"]` |
| cloudTypes | 否 | set<string> | 云厂商类型集合 | `["tencent"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].cloudAccountId | string | 云账号 ID | `ca-001` |
| data[].count | long | 数量 | `13` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/group-by/account-id" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 6. 合规与报告

### 合规框架列表

- **方法与路径**：`POST /api/openclaw/v1/ruleStandardsAndRegulation/list`
- **能力说明**：查询合规框架列表。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| name | 否 | string | 合规框架名称模糊匹配 | `Baseline` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].id | string | 框架 ID | `ruleStandardsAndRegulations-001` |
| data[].name | string | 框架名称 | `Baseline` |
| data[].sortBy | integer | 排序值 | `1` |
| data[].description | string | 描述 | `Security baseline` |
| data[].categories | map<string,string> | 关联分类映射 | `{"cat-001":"Network"}` |
| data[].creator | string | 创建人 | `admin` |
| data[].createdTime | string | 创建时间 | `null` |
| data[].modifiedTime | string | 修改时间 | `null` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/ruleStandardsAndRegulation/list" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'
```

### 合规摘要（多框架）

- **方法与路径**：`POST /api/openclaw/v1/compliance/summary`
- **能力说明**：返回多个合规框架摘要信息（服务端固定 `projectIds=["ALL"]`）。
- **实测补充说明**：
  - `standardAndRegulationsIds` 必须为非空数组。
  - 该接口返回多框架的合规摘要列表。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| standardAndRegulationsIds | 是 | array<string> | 合规框架 ID 列表 | `["ruleStandardsAndRegulations-001"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].projectId | string | 项目 ID | `ALL` |
| data[].projectName | string | 项目名称 | `All` |
| data[].standardAndRegulationsId | string | 框架 ID | `ruleStandardsAndRegulations-001` |
| data[].standardAndRegulationsName | string | 框架名称 | `Baseline` |
| data[].allRuleCount | long | 规则总数 | `100` |
| data[].passedRuleCount | long | 通过规则数 | `80` |
| data[].naRuleCount | long | 不适用规则数 | `10` |
| data[].passedPercent | double | 通过率 | `80.0` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/compliance/summary" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"standardAndRegulationsIds": ["ruleStandardsAndRegulations-001"]}'
```

#### 常见业务错误示例
```json
{
  "code": 500,
  "msg": "请选择合规框架",
  "data": null,
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

### 导出合规报告（多框架）

- **方法与路径**：`POST /api/openclaw/v1/reports/compliance`
- **能力说明**：发起多框架合规报告导出任务，返回报告 ID 和轮询地址。
- **实测补充说明**：
  - `standardAndRegulationsIds` 必须为非空数组。
  - 成功后返回 `reportId` 与 `pollingUrl`，需结合报告详情接口轮询状态。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| standardAndRegulationsIds | 是 | array<string> | 合规框架 ID 列表 | `["ruleStandardsAndRegulations-001"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.reportId | string | 报告 ID | `cp-001` |
| data.pollingUrl | string | 轮询路径 | `/api/平台/v1/reports/cp-001` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/reports/compliance" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"standardAndRegulationsIds": ["ruleStandardsAndRegulations-001"]}'
```

#### 成功响应示例
```json
{
  "code": 200,
  "msg": null,
  "data": {
    "reportId": "cp-001",
    "pollingUrl": "/api/openclaw/v1/reports/cp-001"
  },
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

#### 常见业务错误示例
```json
{
  "code": 500,
  "msg": "请选择合规框架！",
  "data": null,
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

### 报告详情/下载链接

- **方法与路径**：`GET /api/openclaw/v1/reports/{reportId}`
- **能力说明**：查询报告详情与下载链接。
- **实测补充说明**：
  - 实测观察到状态会从 `WAIT` 进入 `SUCCESS`。
  - `reportDownloadUrl` 属于环境运行时数据，新文档仅保留字段语义，不保留真实链接。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| reportId | 是 | string | 报告 ID | `cp-001` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.id | string | 报告 ID | `cp-001` |
| data.userId | string | 用户 ID | `u-001` |
| data.reportType | string | 报告类型 | `multi_compliance` |
| data.reportName | string | 报告名称 | `report.pdf` |
| data.reportDownloadUrl | string | 下载链接 | `https://download.example.com/report.pdf` |
| data.message | string | 状态消息 | `SUCCESS` |
| data.extend | string | 扩展字段 | `null` |
| data.status | string | 报告状态 | `SUCCESS` |
| data.expiredTime | string | 下载过期时间 | `null` |
| data.createdTime | string | 创建时间 | `null` |
| data.modifiedTime | string | 修改时间 | `null` |

#### 请求示例
```bash
curl -X GET "{{BASE_URL}}/api/openclaw/v1/reports/cp-001" \
  -H "Authorization: {{API_KEY}}" \
```

#### 成功响应示例
```json
{
  "code": 200,
  "msg": null,
  "data": {
    "id": "cp-001",
    "userId": "SYSTEM",
    "reportType": "multi_compliance",
    "reportName": "compliance_report.pdf",
    "reportDownloadUrl": "https://example.com/download/report.pdf",
    "message": "",
    "extend": "{\"projectIds\":[\"ALL\"],\"standardAndRegulationsIds\":[\"ruleStandardsAndRegulations-001\"]}",
    "status": "SUCCESS",
    "expiredTime": "2026-03-17T17:18:38",
    "createdTime": "2026-03-16T17:18:31",
    "modifiedTime": "2026-03-16T17:18:38"
  },
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

## 7. 云账号与云厂商

### 云账号列表

- **方法与路径**：`GET /api/openclaw/v1/cloudAccounts/list`
- **能力说明**：查询当前 API Key 绑定用户下的云账号列表。
- **实测补充说明**：
  - 实测列表中可见 `VALID` 与 `INVALID` 两类账号状态。
  - 真实返回可能包含账号名称等业务信息，新文档仅保留字段语义。

#### 输入参数

该接口无独立业务参数，仅依赖认证信息。

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].id | string | 云账号 ID | `ca-001` |
| data[].name | string | 云账号名称 | `MainAccount` |
| data[].cloudId | string | 云插件 ID | `cloud-001` |
| data[].cloudType | string | 云厂商类型 | `tencent` |
| data[].cloudUniqueId | string | 云账号唯一标识 | `uin-001` |
| data[].accessType | string | 接入方式 | `AKSK` |
| data[].status | string | 账号状态 | `enable` |

#### 请求示例
```bash
curl -X GET "{{BASE_URL}}/api/openclaw/v1/cloudAccounts/list" \
  -H "Authorization: {{API_KEY}}" \
```

### 云厂商列表

- **方法与路径**：`GET /api/openclaw/v1/cloudType/list`
- **能力说明**：查询系统支持的云厂商类型列表（按 `orderNum` 排序）。
- **实测补充说明**：
  - 适合作为接入连通性探针接口。
  - HEAD 请求无响应体，符合本阶段语义检查结果。

#### 输入参数

该接口无独立业务参数，仅依赖认证信息。

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data[].id | string | 云厂商 ID | `cloud-002` |
| data[].name | string | 云厂商名称 | `AWS` |
| data[].type | string | 云厂商类型 | `aws` |
| data[].description | string | 描述 | `Amazon cloud` |

#### 请求示例
```bash
curl -X GET "{{BASE_URL}}/api/openclaw/v1/cloudType/list" \
  -H "Authorization: {{API_KEY}}" \
```

### 云账号添加

### 通过 AK/SK 添加云账号

- **方法与路径**：`POST /api/openclaw/v1/cloudAccounts/add`
- **能力说明**：提交云账号名称与云平台凭证，服务端校验凭证有效后创建云账号。
- **实测观察**：已验证名称必填校验与云凭证有效性校验；未使用真实有效凭证验证成功创建流程。

#### 请求体参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| name | 是 | string | 云账号显示名称 | `cloud-account-demo` |
| ak | 是 | string | 云平台访问密钥 AK | `AK_EXAMPLE` |
| sk | 是 | string | 云平台访问密钥 SK | `SK_EXAMPLE` |

#### 成功响应数据

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.accountId | string | 新创建的云账号 ID | `ca-001` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/cloudAccounts/add" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"name":"cloud-account-demo","ak":"AK_EXAMPLE","sk":"SK_EXAMPLE"}'
```

#### 成功响应示例（接口规格样例）
```json
{
  "code": 200,
  "msg": null,
  "data": {
    "accountId": "ca-001"
  },
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

#### 常见业务错误示例（本阶段实测）
```json
{
  "code": 500,
  "msg": "name不能为空",
  "data": null,
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```

```json
{
  "code": 500,
  "msg": "cloud account valid fail",
  "data": null,
  "requestId": "req-001",
  "timestamp": 1773648920888
}
```


## 8. 规则

### 规则列表查询

- **方法与路径**：`POST /api/openclaw/v1/rules/list`
- **能力说明**：分页查询规则列表。
- **实测补充说明**：
  - 分页参数建议显式传入；实测对空请求体有一定容忍度。
  - 返回体是分页对象，核心记录位于 `data.records`。

#### 输入参数

| 参数名 | 是否必选 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| page | 否 | integer | 页码（默认 1） | `1` |
| pageSize | 否 | integer | 每页条数（默认 20） | `20` |
| name | 否 | string | 规则名称模糊匹配 | `Open` |
| types | 否 | array<string> | 规则类型列表 | `["MisConfig"]` |
| severities | 否 | array<string> | 严重度列表 | `["高"]` |

#### 关键响应字段

| 字段名 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| data.records[].id | string | 规则 ID | `rule-001` |
| data.records[].uuid | string | 规则业务 ID | `rule-uuid-001` |
| data.records[].name | string | 规则名称 | `Open Port` |
| data.records[].type | string | 规则类型 | `MisConfig` |
| data.records[].version | string | 规则版本 | `v1` |
| data.records[].status | string | 规则状态 | `enable` |
| data.records[].description | string | 规则描述 | `null` |
| data.records[].impact | string | 影响描述 | `null` |
| data.records[].severity | string | 严重度 | `高` |
| data.records[].categories[] | array<KV> | 分类列表 | `[{"key":"cat-001","value":"Network"}]` |
| data.records[].providers[] | array<string> | 云厂商列表 | `["tencent"]` |
| data.records[].basicReasons[] | array<KV> | 根因列表 | `[{"key":"reason-001","value":"SecurityGroup"}]` |
| data.records[].standardsAndRegulations[] | array<KV> | 合规框架列表 | `[{"key":"sr-001","value":"Baseline"}]` |
| data.records[].labels[] | array<KV> | 标签列表 | `[{"key":"label-001","value":"public-network"}]` |
| data.records[].belongServices[] | array<string> | 归属产品类型列表 | `[]` |
| data.records[].belongServiceInfos[] | array<object> | 归属产品明细 | `[]` |
| data.records[].ruleInfo | string | 扫描语句 | `null` |
| data.records[].creator | string | 创建人 | `null` |
| data.records[].attackPath | string | 攻击路径 | `null` |
| data.records[].fixManualRecommendations | string | 人工修复建议 | `null` |
| data.records[].fixIacDocs | string | IaC 修复文档 | `null` |
| data.records[].referenceDocs | string | 参考文档 | `null` |
| data.records[].queryCondition | string | 查询条件 | `null` |
| data.records[].createdTime | string | 创建时间 | `null` |
| data.records[].modifiedTime | string | 修改时间 | `null` |
| data.total | integer | 总记录数 | `1` |
| data.size | integer | 每页大小 | `20` |
| data.current | integer | 当前页 | `1` |
| data.pages | integer | 总页数 | `1` |

#### 请求示例
```bash
curl -X POST "{{BASE_URL}}/api/openclaw/v1/rules/list" \
  -H "Authorization: {{API_KEY}}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"page": 1,"pageSize": 20}'
```

## 9. 文档说明

- 本文档已去除旧域名、旧环境说明、真实业务样例、真实下载链接和真实账号/项目标识。
- 路径中的 `/api/openclaw/v1` 为接口实际路径前缀，保留用于正确调用；文档标题与能力描述未再绑定特定使用方。
- 如需批量执行命令，请配合单独提供的 curl 文件。
