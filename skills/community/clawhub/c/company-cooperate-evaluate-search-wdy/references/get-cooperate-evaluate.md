# fget-cooperate-evaluate - 企业合作评估信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orgId | Long | 是 | `fuzzy-search-org`返回的orgId |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| orgInfo | object | 企业基本信息 |
| abnormalInfo | object | 经营异常信息 |
| caseAdPunish | object | 行政处罚信息 |
| caseExecDish | object | 失信被执行人信息 |
| orgRiskOverview | list\<object\> | 风险信息 |

### orgInfo - 企业基本信息

| 字段 | 类型 | 说明 |
|------|------|------|
| orgName | string | 企业名称 |
| legalName | string | 法定代表人名称 |
| legalRelOrgCount | int | 法定代表人关联企业数 |
| regStatus | string | 登记状态 |
| regCapBd | bigdecimal | 注册资本 |
| regCap | string | 注册资本（带单位） |
| incDate | date | 成立日期 |
| actCap | string | 实缴资本（带单位） |
| sipCount | int | 参保人数 |
| sipSource | string | 参保人数来源 |
| staffSize | string | 人员规模 |
| industryCode | string | 国标行业编码 |
| industry | string | 国标行业 |
| usCreditCode | string | 统一社会信用代码 |
| orgCode | string | 组织机构代码 |
| regNo | string | 工商注册号 |
| taxpayerNumber | string | 纳税人识别号 |
| taxQualification | string | 纳税人资质 |
| apprDate | date | 核准日期 |
| regInstitute | string | 登记机关 |
| orgCategory | string | 企业类型 |
| businessStartTime | date | 经营开始日期 |
| businessEndTime | date | 经营截止日期 |
| region | string | 所属地区 |
| nameEn | string | 英文名 |
| nameHis | list\<object\> | 曾用名 |
| businessScope | string | 经营范围 |
| phone | string | 电话 |
| samePhoneCount | int | 同电话企业数 |
| addrReg | string | 注册地址 |
| sameAddrCount | int | 同注册地址企业数 |
| addrBusiness | string | 经营地址 |
| sameAddrBusinessCount | int | 同经营地址企业数 |
| addrContact | string | 通信地址 |
| sameAddrContactCount | int | 同通信地址企业数 |
| website | string | 官网 |
| ipcFlag | boolean | 官网是否IPC |
| email | string | 邮箱 |
| scale | string | 企业规模 |
| category | string | 机构类型 |

#### nameHis - 曾用名

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 名称 |
| startDate | date | 开始时间 |
| endDate | date | 结束时间 |
| phoneCount | int | 更多电话数 |

### abnormalInfo - 经营异常信息

| 字段 | 类型 | 说明 |
|------|------|------|
| count | long | 总记录数 |
| list | list\<object\> | 前5条数据 |

#### list - 前5条数据

| 字段 | 类型 | 说明 |
|------|------|------|
| orgId | long | 企业ID |
| abnormalReason | int | 列入原因 |
| abnormalReasonDesc | string | 列入原因描述 |
| department | string | 列入部门 |
| abnormalDate | date | 列入日期 |
| removeReason | string | 移出原因 |
| removeDate | date | 移出日期 |
| removeDepartment | string | 移出部门 |

### caseAdPunish - 行政处罚信息

| 字段 | 类型 | 说明 |
|------|------|------|
| caseNo | string | 案号 |
| punishNo | string | 行政处罚决定文书号 |
| punishTime | date | 处罚日期 |
| releaseTime | date | 发布日期 |
| punishAmountYuan | string | 处罚金额（元） |
| seizeAmountYuan | string | 没收金额（元） |
| illegalFact | string | 违法事实 |
| illegalType | string | 违法行为类型 |
| punishResult | string | 处罚结果 |
| punishAccord | string | 处罚依据 |
| punishType | string | 处罚类型 |
| punishTypeCode | string | 处罚类型编码 |
| punishArea | string | 地区 |
| entityName | string | 实体名称 |
| entityRole | string | 实体身份 |
| entityRoleCode | string | 实体身份编码 |

### caseExecDish - 失信被执行人信息

| 字段 | 类型 | 说明 |
|------|------|------|
| caseNo | string | 案号 |
| executeAccordNo | string | 执行依据文号 |
| registerTime | date | 立案时间 |
| releaseTime | date | 发布日期 |
| caseAmountYuan | string | 涉案金额（元） |
| executeAmountYuan | string | 执行标的（元） |
| executeCourtName | string | 执行法院名称 |
| performStatus | string | 被执行人履行情况 |
| performDate | date | 履行日期 |
| dishonestySituation | string | 失信被执行人行为具体情形 |
| legalPapersDuty | string | 生效法律文书确定的义务 |
| entityName | string | 实体名称 |
| entityRole | string | 实体身份 |
| entityRoleCode | string | 实体身份编码 |

### orgRiskOverview - 风险信息

| 字段 | 类型 | 说明 |
|------|------|------|
| itemType | int | 风险大类 |
| itemId | string | 风险类型编码 |
| itemName | string | 风险类型名称 |
| currentRiskCnt | int | 当前风险数量 |
| historyRiskCnt | int | 历史风险数量 |
| highRiskCnt | int | 高风险数量 |
| middleRiskCnt | int | 中风险数量 |
| lowRiskCnt | int | 低风险数量 |
| tipRiskCnt | int | 提示风险数量 |
| pendingCaseCnt | int | 在审案件数量 |
| judgedCaseCnt | int | 已判决案件数量 |
| casePlaintiffCnt | int | 原告案件数量 |
| caseDefendantCnt | int | 被告案件数量 |
| caseOtherCnt | int | 其他角色案件数量 |

