---
name: 1688-bp-inquiry-evaluate
description: |
  1688 商家客服/业务员询盘接待质量评估与改进建议报告。
  能力划分：
  - bp_inquiry_evaluate_summary：店铺业务员整体表现（团队评估指标 / 业务员基础评估列表）。
  - bp_inquiry_evaluate_sales_detail：单个业务员询盘诊断（业务员维度的评估指标列表 / 业务员评估摘要 / 询盘明细列表）。
  触发词：业务员评估、客服评估、团队评估、客服质检、询盘质检、接待报告、能力提升、客服怎么样、团队怎么样、询盘怎么样。
---

# 1688-bp-inquiry-evaluate

## ⚠️ 强制约束

- **数据真实性**：仅展示通过 CLI 命令获取真实数据，禁止编造或改写账号账号/评分/评价/总结,禁止编造或改写账号/评分/总结，可做组件展示与排版优化
- **先执行 CLI 再分析**：必须先通过 `python3 cli.py` 调用获取数据，不得跳过
- **如实标注失败或空数据**：返回 `success=false` 或空数据时标注"数据暂不可用"，不必反复重试
- **可视化要求**：凡是非纯文本的数据展示（指标、列表、卡片），均必须按「组件约束」中的组件渲染，不得使用纯 markdown 表格替代
- **禁止向用户透出内部执行逻辑**，如"按照技能流程"、"不展示明细表格"、"根据指引"等，直接执行并展示结果即可
- **时间参数校验**`：当`startAt`早于今天向前 31 天（即查询区间开始日期 < 设备当前日期 − 31）必须 open_tab，禁止调用接口
- **禁止明文透出用户ID**：严格禁止在报告中明文透出sellerUserId、saleIdentityId

## 前置环境检查

- Skill 使用 `ALI_1688_AK` 环境变量。如有缺失，停止流程并告知用户安装。

## 前置阅读清单（按时机触发）

- 首次执行 `bp_inquiry_evaluate_summary` 前：先完整阅读 `references/capabilities/bp_inquiry_evaluate_summary.md`
- 首次执行 `bp_inquiry_evaluate_sales_detail` 前：先完整阅读 `references/capabilities/bp_inquiry_evaluate_sales_detail.md`

## 命令速查

统一入口：`python3 {baseDir}/cli.py <command> [options]`

| 命令 | 说明 | 示例                                                              |
|------|------|-----------------------------------------------------------------|
| `configure` | 配置 AK | 写入本地配置 |
| `bp_inquiry_evaluate_summary` | 查询店铺业务员整体表现 | `cli.py bp_inquiry_evaluate_summary --startAt "20260504" --endAt "20260510"` |
| `bp_inquiry_evaluate_sales_detail` | 查询单业务员询盘诊断 | `cli.py bp_inquiry_evaluate_sales_detail --saleIdentityId 123123 --startAt "20260501" --endAt "20260510"` |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

## 能力选择决策树

| 用户场景 | 命中命令 | 参数补齐策略 |
|---------|------|-----------|
| 用户问"团队/客服/业务员/询盘/接待整体表现" | bp_inquiry_evaluate_summary | 默认近 7 天 |
| 用户问"看 xxx 业务员的评估摘要/询盘详情/改进建议" | bp_inquiry_evaluate_sales_detail | 仅有姓名 → 先 summary 取 ID |
| 用户问"上周/最近"+ 周期描述 | bp_inquiry_evaluate_summary | 解析为日期区间 |

## 使用流程

1. **解析用户意图**：识别用户意图匹配「能力选择决策树」。
2. **提取参数**（日期默认近 7 天, `startAt` = 设备日期 - 7 天，`endAt` = 设备日期 - 1 天；业务员姓名 → 先 summary 取 ID）。
3. **日期校验**：校验`startAt`是否早于今天-31天，立即触发 **open_tab** 到团队服务评估页面，无需调任何查询接口，也无需解释原因。
4. **执行命令**：根据决策执行相应命令。
5. **结果输出**：可视化输出，按「异常处理」兜底。
6. **追加询问**：结果输出之后，可以继续询问用户是否需要查询其他业务员或者其他周期的评估内容。

### 店铺业务员整体表现使用指引

- 若参数不完整，应先引导用户补齐参数，同时确保参数格式正确，以下格式
  - `startAt` 开始日期，格式：yyyyMMdd，举例: "20260501"
  - `endAt` 结束日期，格式：yyyyMMdd，举例: "20260510"

### 单业务员询盘诊断使用指引

- 若用户只提供姓名，先调用 bp_inquiry_evaluate_summary 获取 saleIdentityId 后再查询
- 若参数不完整，应先引导用户补齐参数，同时确保参数格式正确，以下格式
  - `saleIdentityId` 业务员身份ID
  - `startAt` 开始日期，格式：yyyyMMdd，举例: "20260501"
  - `endAt` 结束日期，格式：yyyyMMdd，举例: "20260510"

### open_tab 团队服务评估

- **触发条件**：1、命中强制约束第 7 条（31 天）；2、后端因范围超限返回错误；3、用户主动请求"打开完整页面"。触发后直接返回此结构，不要附加任何文字解释
- **使用说明**：当命中open_tab时，直接打开页面，不需要输出json

```json
{
  "type": "open_tab",
  "url": "https://air.1688.com/app/bp-boot/a2a-team-newton/index.html",
  "title": "团队服务评估"
}
```

## 输出约束

任何命令输出 `success: true` 时：

1. **若`markdown` 字段有值，直接输出即可**

2. 所有 tool 输出 JSON `{"success", "markdown", "data"}`，**必须完整、逐字、原样输出 `markdown` 字段**（含 `>` 引用块前缀、HTML 注释、空行、表格分隔符）。**禁止** 精简 / 改写 / 提炼 / 合并 / 加开场白 / 从 `data` 重构内容。Agent 的分析或追问必须放在 markdown **之后**。


## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "签名无效" 或 "401" | 提示用户当前发送能力所需鉴权未就绪，请补充有效 AK 或检查鉴权配置后重试 |
| "startAt/endAt 不能为空" | 引导补齐日期 |
| "saleIdentityId 不能为空" | 引导先查 summary |
| 业务员近 7 天可能没有有效询盘 → inquiryCnt=0 或 inquiryDetails=[] | 提示用户该业务员查询周期内无有效询盘 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| "用户不存在" 或 "userId 无效" | 提示用户确认接收人 userId 是否正确 |
| "日期格式不合法" | 提示格式 yyyyMMdd |
| 其他 | 仅输出 markdown 即可 |

3. 当后端因数据范围限制返回错误时，回退到 open_tab 引导用户至团队服务评估页面

## 参数补齐引导话术

**日期缺失追问话术**
> 请提供查询起止日期（格式 yyyyMMdd），或回复"近 7 天"由我自动计算。

**业务员选择话术**
> 请提供业务员的旺旺 ID 或名称；若仅有名称，我将先查询团队列表为您匹配。

**31 天回退提示话术**
> 您查询的日期范围超过 31 天，已为您打开"团队服务评估"完整页面。

## 安全声明

本 skill 全部命令为只读查询，无需用户确认即可执行

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `1688-bp-inquiry-evaluate` | skill 名称 |
| `SKILL_VERSION` | `1.0.0` | skill 版本号 |
| `SKILL_CHANNEL` | `clawhub` | 发布渠道 |

> 已存在的系统环境变量优先级高于 `.env`，CI/CD 注入的变量不会被覆盖。

## 埋点上报

每次 CLI 命令执行时，自动向 skill 网关上报一次调用记录，用于统计 skill 调用次数。

- **实现位置**：`scripts/_tracker.py` → `report_skill_usage()`，在 `cli.py` 的 `main()` 中每次命令执行后自动调用
- **上报接口**：`POST /api/reportSkillsUsage/1.0.0`
- **上报参数**：

  | 参数 | 值来源 | 说明 |
  |------|--------|------|
  | `apiName` | 固定 `null` | 固定传 null |
  | `skillsName` | `.env` `SKILL_NAME` | skill 名称 |
  | `version` | `.env` `SKILL_VERSION` | skill 版本号 |
  | `scene` | 固定 `CLI` | 固定值 |
  | `channel` | `.env` `SKILL_CHANNEL` | 发布渠道 |

- **失败处理**：上报失败静默忽略，不影响主流程