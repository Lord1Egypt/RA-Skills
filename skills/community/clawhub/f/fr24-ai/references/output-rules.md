# 输出规则（对用户展示与下载）

脚本 stdout 含 **`userView`**（给用户）与 **`agentOnly`**（仅 Agent 内部续跑）。  
**对用户聊天、表格、附件、导出文件时，只使用 `userView` 与顶层 `message`，禁止引用 `agentOnly` 或整段原始 stdout。**

## 查价 parse 后（未搜索）

- 用表格确认：`userView` 中的行程、日期、人数、舱位（`intentSummary` / `legs`）
- **禁止**向用户展示：`payload`、`payloadFile`、本机路径、Python 命令行

## 搜索 search 成功后

- 用表格或分条列出 **直飞最低**、**中转最低**（有则展示）
- 每条包含：航线、航班号、**人均成人价**（注明测试环境演示价）、**退票/改期摘要**、**行李摘要**、**报价ID**（`quoteId`，便于用户后续确认和排查）
- 可展示 **今日剩余搜索次数**（`remainingQuota` / `dailyLimit`）
- 多条可订时，请用户选择「直飞」或「中转」

## 用户要改航司 / 起飞时间

- 须 **refine → 再 search**（见 SKILL.md），不要只复述旧报价
- 可展示 `searchFilters` / 筛选条件摘要；无匹配时说明「未找到符合条件」并建议放宽

## 演示配额用尽（307901）

- 使用 `userView.message` / 顶层 `message`（引导至 [航路官网](https://www.flightroutes24.com/) 开通 API 采购并本机配置 APPKEY，**不要**只提示「明日再试」）
- 可展示 `registerPortalUrl` 链接
- 用户问具体配置步骤时，按 [user-appkey-config.md](./user-appkey-config.md) 回答

## 预订

- **parse-passengers**：只展示 `passengerDisplay`、`contactDisplay` 与确认话术
- **verify / order**：展示 `orderPreview`（行程、退改、乘客回显）、**报价ID**（`quoteId`）及订单号等业务字段
- **禁止**向用户展示：证件明文 API 结构、`passengerRawMappings`、`contactRaw`

## 禁止写入用户下载 / 对外展示

| 类别 | 示例 |
|------|------|
| 链路调试 | `traceId`、`processingTime` |
| 内部状态 | `code`、`searchMode`、`workflowSteps`、`workflowStep` |
| 密钥与路径 | `clientKey`、`payloadFile`、`.cache/` 路径、完整 `payload` |
| 原始 API | 完整 `ApiSearchRs`、`data.offers` 全量列表 |
| 预订内部 ID | `verifyOfferId`、`offerId`（用 `quoteId` 报价ID 代替，用户可看到） |
| 内部测试与维护材料 | 测试报告、维护文档全文、非生产网关说明 |
| 环境变量名 | 勿向用户列出采购/网关相关的系统变量名 |
| 示例姓名 | 对用户说明时使用 **张三**（儿童示例可用 **张小三**） |

## Agent 内部（可读 `agentOnly`）

- 续跑命令所需：`payload`、`offerId`、`verifyOfferId`、`passengers` 等见 `agentOnly` 或 `.cache/`
- 排障：将 `agentOnly.traceId` 提供给运维时**勿**粘贴到用户可见文档

## 用户问配置 appkey / 采购密钥

- **只**按 [user-appkey-config.md](./user-appkey-config.md) 回答
- **禁止**：说明内部联调、跳过校验/白名单等非用户配置项
- **禁止**：让用户在聊天里提交密钥明文，或代用户在对话中执行环境变量配置命令

## 流程禁止

- 未确认意图就 `search`（扣配额）
- 未确认乘客就 `verify`
- 未确认就 `order`
- 把脚本 stdout 整段保存为用户「下载文件」
