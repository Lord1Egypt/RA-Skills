# 知识库字段说明

本文件供助手在**本地待填项回填**时查阅。推荐流程：
1. 先用 `python3 scripts/zcm.py knowledge-base` 查看可用分类；
2. 再按需查询某一类，例如 `python3 scripts/zcm.py knowledge-base qualifications`；
3. 本地模型根据下列字段含义匹配待填项；
4. **没有把握的字段宁可保留待填项，不要臆造。**

> 开放范围仅含：`company_profile`、`qualifications`、`performances`、`financial_reports`。
> 明确不含：历史标书库、标书模板库。
> 明确不返回：任何附件地址、文件流、base64、附件布尔标记。

## 一、company_profile（企业信息）

| field_key | 字段名 | 说明 | 是否可直接回填 |
|---|---|---|---|
| `company_name` | 公司名称 | 企业全称/投标人名称 | 是 |
| `enterprise_type` | 企业类型 | 单位性质/企业性质 | 是 |
| `business_term` | 营业期限 | 营业执照中的经营期限 | 是 |
| `credit_code` | 统一社会信用编码 | 企业统一社会信用代码 | 是 |
| `registered_address` | 注册地址 | 营业执照注册地址 | 是 |
| `office_address` | 办公地址 | 企业办公/联系地址 | 是 |
| `legal_representative` | 法人名称 | 法定代表人姓名 | 是 |
| `legal_rep_position` | 职务 | 法定代表人职务 | 是 |
| `legal_rep_phone` | 法人联系方式 | 法定代表人联系电话 | 仅模板明确要求时回填 |

## 二、qualifications（企业资质）

| field_key | 字段名 | 说明 | 是否可直接回填 |
|---|---|---|---|
| `qualification_name` | 资质名称 | 资质/证书名称 | 是 |
| `certificate_number` | 证书编号 | 资质证书编号 | 是 |
| `valid_period` | 有效期限 | 统一按“起始日期 至 截止日期/长期”返回 | 是 |

> 资质是**多条记录**。回填前先判断模板要的是哪类资质，再选对应记录，不要默认取第一条。

## 三、performances（企业业绩）

| field_key | 字段名 | 说明 | 是否可直接回填 |
|---|---|---|---|
| `contract_name` | 合同名称 | 业绩对应的合同或项目名称 | 是 |
| `client_name` | 客户名称 | 甲方/客户名称 | 是 |
| `contract_amount` | 合同金额 | 合同金额原值 | 是 |
| `completion_date` | 完成时间 | 竣工/验收/完成日期 | 是 |

> 业绩同样是**多条记录**。需要按项目名称、客户、金额或时间要求筛选最匹配的一条或几条，不能把多条业绩混成一条。

## 四、financial_reports（财务报告）

当前仅开放**分类入口**，暂不开放具体字段。

这意味着：
- 可以知道当前租户存在该类资料；
- 不能通过本接口取出财务报告的正文、附件或明细字段；
- 本地模型不要自行假设或补写财务数据。

## 使用边界

- 没值：保留待填项，不要自行生成。
- 多条记录：资质、业绩都要先选记录，再回填字段。
- 附件资料：本接口不返回任何附件相关信息，不能据此推断附件内容。
- 租户隔离：只能查询当前 Api Key 所属租户的数据，不能跨租户取数。
