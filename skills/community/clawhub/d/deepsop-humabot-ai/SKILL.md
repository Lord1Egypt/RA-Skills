---
name: deepsop-humabot
description: 人机协作台技能。用户输入自然语言销售指令，AI自动分析拆解任务参数，调用 deepsop 平台接口提交任务，等待后查询结果并推送。触发场景：用户说「帮我找客户」「挖掘XXX行业客户」「找XXX个客户」「提交任务」等与客户挖掘、销售任务相关的指令；或用户说「创建电话场景」「新建外呼话术」「新建电话机器人」「提交场景审核」「我要做一个外呼场景」等与场景创建/审核相关的指令；或收到包含 [DeepSOP-AutoQuery] 标记的系统定时事件（cron 回调，用于自动查询并推送任务结果）。需要提前配置环境变量 DEEPSOP_API_KEY。⚠️ 调用本 SKILL 前必须先完整阅读 SKILL.md。提交 agentSubmitTask **必须**走 scripts/submit_task.py、创建/审核场景 **必须**走 scripts/submit_script_review.py（均通过 heredoc 把 body 喂给 stdin），脚本内部串行跑参数校验 + UTF-8 安全 HTTP 提交，**禁止**直接写 curl 命令（会因 Windows cp936 代码页导致中文字段乱码）。脚本退出码 0 才算成功；非 0 必须把 summary/errors 原样回给用户后修正重试，禁止绕过校验或假装成功。
---

# 人机协作台（Human-AI Collaboration）

## 功能简介

人机协作台是基于 deepsop 平台的智能销售任务助手，能够：

- **理解自然语言指令**：直接描述需求，如「帮我找50个美国做服装的客户」
- **智能任务拆解**：自动识别目标数量、行业、地区、执行周期等参数
- **多员工协作**：根据任务类型自动分配对应职能员工
  - **AiWa**：客户挖掘（找客户、行业客户等）
  - **Frank**：邮件销售
  - **Fran**：电话销售
  - **Lisa**：短信销售
- **自动提交任务**：调用 deepsop API 提交任务，后台异步执行
- **定时查询结果**：任务提交后询问用户期望等待时长，按用户指定时间自动查询并推送结果（默认 8 分钟）
- **生成 xlsx 报表**：AiWa 客户数据自动生成带样式的 Excel 文件返回
- **Frank 邮件统计**：查询邮件发送总数、成功数、已读数、回复数、点击数，并展示发送详情（可与 AiWa 搭配，或在无 AiWa 协同时通过客户来源选择 xlsx 上传 / 公司搜索 指定客户）
- **Fran 电话销售**：自动查询号码池与场景库，由用户选择后提交电话销售任务（可与 AiWa 搭配，或在无 AiWa 协同时通过客户来源选择 xlsx 上传 / 公司搜索 指定客户）
- **Lisa 短信统计**：查询短信发送总数、成功数、失败数，并展示发送详情（可与 AiWa 搭配，或在无 AiWa 协同时通过客户来源选择指定客户）
- **电话场景创建/审核**：用户可主动说「创建电话场景」「新建外呼话术」直接走 Step 1.7 子流程，也可在 Fran 提交时若无可用场景库时被引导即时创建并提交阿里云审核（场景+TTS+机器人 prompt 三合一）

---

## 前置条件：获取 API Key

本技能需要 **API Key 授权**才能调用 DeepSOP 接口。请按以下步骤获取：

1. 获取 API Key 入口：
   - **已有账号** → 前往 [https://ai.deepsop.com/login?source=3](https://ai.deepsop.com/login?source=3) 登录获取
   - **没有账号** → 前往 [https://ai.deepsop.com/register?source=3](https://ai.deepsop.com/register?source=3) 注册后获取
2. 登录后进入「设置」或「API 管理」页面
3. 新建 API Key，复制以 `sk-` 开头的密钥
4. 在 OpenClaw 中配置环境变量：

```
DEEPSOP_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
```

> 所有 API 请求头需携带：`x-api-key: $DEEPSOP_API_KEY`
> API Base URL：`https://ai.deepsop.com/prod-api/`

---

## ⛔ 接口路径强约束（最高优先级，所有 HTTP 请求必须遵守）

> 🔒 **核心规则：** 调用任何接口时，**必须严格使用本文档对应步骤标注的完整 URL**，不得做任何形式的改写、简化、猜测或自创。
>
> **请求前自检流程（每一次 HTTP 请求都必须执行）：**
> 1. 在下方「**API 路径权威清单**」中找到对应步骤的接口；
> 2. 将即将发出的完整 URL（含 host、path、query key 名与顺序、`pageNum`/`pageSize`/`platform` 等参数值）与清单中的 `Path` 列**逐字符比对**；
> 3. 完全一致才允许发出请求；任何偏差立即停止，按清单中的路径修正后再重试；
> 4. 若某接口未在清单中列出 → **绝对禁止**自行编造路径，必须先向用户确认。
>
> **禁止行为：**
> - ❌ 把 `prod-api` 改成 `api` / `v1` / `prod` / `prodApi`
> - ❌ 把 camelCase 改成 snake_case 或全小写（如 `presetEmployee` ≠ `preset_employee` ≠ `presetemployee`）
> - ❌ 把 `outBound` 写成 `outbound`、`emailconfig` 写成 `emailConfig`、`authaccount` 写成 `authAccount`（这三个偏偏就是全小写，特别注意）
> - ❌ 用同义词替换路径段（`getCustomerPoolDetail` ≠ `customerPoolDetail` / `getCustomerDetail`；`collaborationCallResult` ≠ `callResult`）
> - ❌ 漏写或私自补加 query 参数（如漏 `platform=1` / `status=1`，或私自加 `pageSize=20` 改成 `pageSize=10`）
> - ❌ 凭"上一次调用记得"或"经验"猜测路径，不回到本文档对照
>
> **路径错误是最常见、最可避免、影响最大的事故，必须零容忍。**

### 📋 API 路径权威清单（Base URL: `https://ai.deepsop.com/prod-api`）

| # | 步骤 | 方法 | Path（不含 Base URL） |
|---|---|---|---|
| 1 | Step 1.5 数字员工可用性 | `GET` | `/ai/presetEmployee/list` |
| 1.1 | Step 1.5.1① 签约套餐列表 | `GET` | `/ai/setting/list?packageType=3` |
| 1.2 | Step 1.5.1② 人民币→K币汇率 | `GET` | `/system/config/configKey/CNY_TO_KCOIN` |
| 1.3 | Step 1.5.1③ K币余额查询 | `GET` | `/ai/vip/balance?userId={userId}` |
| 1.4 | Step 1.5.1④ 提交签约（扣K币） | `POST` | `/ai/order/purchaseIndependentPackageByKToken` |
| 2 | Step 3 提交任务 | `POST` | `/ai/presetEmployee/submitTask` |
| 3 | Step 3 前置 A-0 外呼实例 | `GET` | `/ai/outBound/describeInstance` |
| 4 | Step 3 前置 A-1 号码池 | `GET` | `/ai/outBound/callerNumber/list` |
| 5 | Step 3 前置 A-2 场景库 | `POST` | `/ai/outBound/listScripts` |
| 5.1 | Step 1.7 / 前置 A-2 兜底 创建+审核场景 | `POST` | `/ai/outBound/createOrModifyScriptAndSubmitScriptReview` |
| 5.2 | Step 1.7 轮询场景审核状态 | `POST` | `/ai/outBound/describeScript` |
| 5.3 | Step 1.7 修改场景时回填机器人设定 | `POST` | `/ai/outBound/getAgentProfile` |
| 5.4 | Step 1.7 辅 单独重新提交场景审核 | `POST` | `/ai/outBound/submitScriptReview` |
| 5.5 | Step 1.7 辅 撤销场景审核 | `POST` | `/ai/outBound/withdrawScriptReview` |
| 6 | Step 3 前置 B0 邮箱绑定检查 | `GET` | `/ai/emailconfig/list?pageSize=1000&pageNum=1&status=1` |
| 7 | Step 3 前置 B 用户 Profile | `GET` | `/ai/user/profile` |
| 8 | Step 3 前置 D-1 短信模板列表 | `GET` | `/ai/sms/querySmsTemplateList?pageNum=1&pageSize=20&pageNumber=1` |
| 12 | Step 5-A AiWa 客户池详情 | `POST` | `/ai/presetEmployee/getCustomerPoolDetail?pageNum=1&pageSize=10` |
| 13 | Step 5-B-1 Frank 邮件统计 | `GET` | `/ai/email/getTaskEmailCount?taskId={frankDagTaskId}` |
| 14 | Step 5-B-2 Frank 邮件列表 | `GET` | `/ai/email/taskList?pageNum=1&pageSize=2000&taskId={frankDagTaskId}` |
| 15 | Step 5-C-1 Fran 电话统计 | `GET` | `/ai/presetEmployee/collaborationTaskStatistics?taskId={franDagTaskId}&customerPoolId={franCustomerPoolId}` |
| 16 | Step 5-C-2 Fran 电话详情 | `POST` | `/ai/presetEmployee/collaborationCallResult?pageNum=1&pageSize=10` |
| 17 | Step 5-D-1 Lisa 短信统计 | `POST` | `/ai/sms/getTaskSmsCount` |
| 18 | Step 5-D-2 Lisa 短信详情 | `POST` | `/ai/sms/getSmsResultList?pageNum=1&pageSize=10` |
| 21 | Step 1.6 途径B 客户搜索（无 AiWa 销售任务） | `POST` | `/ai/customer/customerList?pageNum={pageNum}&pageSize=10` |
| 22 | Step 1.6 途径A xlsx 上传到 OSS | `POST` | `/system/fileUpload/upload`（multipart/form-data, 字段名 `file`） |
| 23 | Step 1.6 途径A 下载「公司导入」模板 | `POST` | `/ai/customer/template`（application/x-www-form-urlencoded, 空 body, 响应 blob） |
| 24 | Step 1.6 途径A 下载「地址簿导入」模板 | `POST` | `/ai/customer/contactImportTemplate`（application/x-www-form-urlencoded, 空 body, 响应 blob） |

> 🔁 **本清单与下文各 Step 中"接口："标注的路径完全一致**。如发现两处不一致，**以下文 Step 中的标注为准**（本清单仅为快速比对索引），同时立即向用户报告该不一致以便修正。

### 🛡️ 双轨强约束（本文档 + 代码）

> 上述清单同时存在于 `scripts/api_paths.py`，构成"双轨强约束"：
>
> - **LLM 直接发请求时（curl/工具调用）：** 必须对照本文档清单逐字符比对路径。
> - **脚本调用 API 时（如 `submit_task.py`）：** 严禁脚本内硬编码 URL，必须从 `api_paths.py` 通过 `build_url("xxx")` 获取，并配合 `assert_url_matches()` 自检。
> - **新增/修改接口的强制流程：** 先改 SKILL.md 这张表 → 再改 `api_paths.py` → 然后才能在脚本里使用；遗漏任一步即视为 bug。
> - **漂移检测：** 运行 `python scripts/api_paths.py` 会扫描本文件中所有 `https://ai.deepsop.com/prod-api/...` 路径，若有未在 `api_paths.py` 登记的项目则非零退出。该命令应在每次修改路径后执行一次自检。

---

## 完整执行流程

### Step 0：触发类型判断（每次进入技能必须首先执行）

检查当前输入内容是否包含 `[DeepSOP-AutoQuery]` 标记：

- **包含该标记**：这是 cron 定时回调。**不得询问用户是否继续，不得等待确认，不得说「我将开始查询」。立即从输入文本中解析变量（`taskId`、`aiwaDagTaskId`、`aiwaCustomerPoolId`、`frankDagTaskId`、`franDagTaskId`、`franCustomerPoolId`、`lisaDagTaskId`、`lisaCustomerPoolId`、`taskName`、`totalTarget`、`employeeList`、`feishuChatId`），跳过 Step 1～4 直接执行 Step 5 的全部内容（查询接口 → 生成 xlsx → 发送文件 → 回复文字摘要），直到所有参与员工的结果都处理完毕。
- **不包含该标记**：这是用户主动指令，继续执行 Step 1。

---

### Step 1：第一轮 AI 分析（任务拆解 + 意图分流）

> 🔀 **意图分流前置（在跑下方拆解 prompt 之前先判断）：**
>
> 如果用户输入**明确**包含以下关键词之一且**不**带销售目标数量（如「找 N 个客户」「发邮件」「打电话推销」），判定为「场景创建意图」：
> - 「创建电话场景」「新建外呼话术」「新建电话机器人」「新建场景」「做一个外呼场景」
> - 「场景审核」「提交场景审核」「话术审核」「让阿里云审一下」
> - 「修改场景 / 修改话术 / 改一下场景库」（带或不带 scriptId）
> - 「撤销场景审核 / 撤回场景审核 / 取消场景审核」 → 走 [Step 1.7.6 辅助操作](#step-176场景审核辅助操作用户已有草稿审核中场景) 中的 `withdrawScriptReview` 分支
> - 「重新提交场景审核 / 重审已有场景」（用户明确说明是已有 scriptId、不要改内容） → 走 [Step 1.7.6 辅助操作](#step-176场景审核辅助操作用户已有草稿审核中场景) 中的 `submitScriptReview` 分支
>
> 命中此意图 → **跳过下方 Step 1 任务拆解 prompt + Step 1.5/1.6/2/3/3.5/4/5 的销售流程**，直接进入 [Step 1.7：电话场景创建/审核子流程](#step-17电话场景创建审核子流程独立入口)。
>
> 若用户句子里**同时**有销售意图（如「先建一个外呼场景，再用它给我打 50 个家纺客户的电话」），按以下顺序处理：
>   1. 先走 Step 1.7 完成场景创建+审核，拿到 `scriptId / agentProfileId`；
>   2. 再回到下方 Step 1 拆解销售意图，进入 Step 1.5/1.6/2/3 流程；
>   3. 进入 Step 3 前置 A-2 时，把 Step 1.7 拿到的 `scriptId / agentProfileId` 作为已选场景直接复用，**不要**再调 `listScripts` 让用户选。
>
> 未命中场景创建关键词 → 进入下方常规销售任务拆解。

用以下 prompt 分析用户指令，严格返回 JSON，不含任何额外文字：

```
根据【指令】描述，Json格式返回数据
不需要多余的描述，不要过度解读，没有提及的内容请不要擅自理解，识别结果除了Json数据其他文字不要出现
规则如下：{
  "taskName": "根据描述总结出一个简洁的任务名称"
  "executionMode": "判断描述中是否明确提及每日/每天/周期性，如果提及则返回周期性任务，未提及则返回定额任务"
  "totalTarget": "提取描述中提及的数量（无单位纯数字）"
  "employeeList": "首先将描述按逗号、顿号等分隔符拆分成多个子任务，然后为每个子任务匹配对应员工：
    - 挖掘客户职能（AiWa）：匹配任何包含“找”、“开发”、“行业”、“客户”等与客户挖掘相关的描述，以及没有明确匹配其他职能的单子任务
    - 邮件销售职能（Frank）：匹配包含“邮件”、“发邮件”等关键词的描述
    - 电话销售职能（Fran）：匹配包含“电话”、“打电话”、“电话销售”等关键词的描述
    - 短信销售职能（Lisa）：匹配包含“短信”、“发短信”等关键词的描述
    - 生产视频职能（Jack）：匹配包含“视频”、“生产视频”等关键词的描述
    - 智能SEO优化职能（Sophia）：匹配包含“SEO”、“优化”、“搜索引擎”等关键词的描述
    - AI剪辑师职能（Alex）：匹配包含“剪辑”、“视频剪辑”等关键词的描述
    - 独立站客服职能（Leo）：匹配包含“客服”、“客户服务”、“咨询”等关键词的描述
    如果拆分后只有一个子任务且没有匹配上员工，则默认匹配挖掘客户职能（AiWa）
    最后汇总所有匹配到的员工名称组成一个,拼接的字符串并返回（去重）",
  "language": "判断描述中是否明确提及国家或地区，若提及了国家或地区但和中国没有关联则返回'英文'其他情况返回'中文'",
}
```

解析结果字段（**注意：这些只是 SKILL 内部用的解析变量，不要原样塞到最终 API 请求体里**）：
- `totalTarget`：目标数量（数字）— 仅作为 `employeeParams.AiWa.totalTarget` 的值来源，**不得**作为根级字段
- `employeeList`：参与员工逗号字符串，如 `"AiWa"` 或 `"AiWa,Frank"` — **仅本 SKILL 内部用于决定要构造哪些 `employeeParams.{Name}` 子对象，绝不允许出现在最终请求体的任何层级**
- `language`：`"中文"` 或 `"英文"` — **仅作为 `employeeParams.Frank.language` 的值，不得挂到根级或其他员工子对象**
- `taskName`：任务名称（→ `collaborationSubmitTaskParam.taskName`）
- `executionMode`：中文字符串 `"定额任务"` 或 `"周期性任务"` — **这是 LLM 返回的内部变量，提交请求体时必须转换为数字**：
  - 后端枚举：`"周期性任务" = 0`，`"定额任务" = 1`
  - 🔒 **当前阶段强制规则：无论 LLM 识别结果是定额还是周期性，提交请求体时 `executionMode` 一律硬编码为数字 `1`（即按定额任务下达）**。
  - **绝不允许**把中文字符串直接塞进请求体（如 `"executionMode": "定额任务"`），会被后端 schema 校验拒绝；也不得写成 `"1"`（带引号字符串）、`true`、`null`。

**员工组合校验：**

1. **不支持的员工拦截**：当 `employeeList` 包含 `Jack`、`Leo`、`Sophia`、`Alex` 中的任意一个时，**终止任务**，回复：
   > ⚠️ 数字员工「{员工名}」尚未接入人机协作台，当前支持的员工为：AiWa、Frank、Fran、Lisa。请调整指令后重试。

2. **销售员工无 AiWa 协同时必须指定客户来源**：当 `employeeList` 包含 `Frank`、`Fran`、`Lisa` 中的任意一个或多个，且**不包含** `AiWa` 时，**不再终止任务**；改为进入「Step 1.6 客户来源选择」流程，由用户通过「上传 xlsx 文件」或「搜索选择公司」两种方式指定要执行销售动作的客户来源，待客户来源确认完成（`fileList` / `addressFileList` / `suppurIds` 三者中至少一个非空）后再继续后续步骤。
   - 若用户最终未提供任何客户来源（取消、放弃或多次留空），则终止任务并回复：
     > ⚠️ 未指定任何客户来源，无法执行销售动作。请上传客户 / 地址簿 xlsx 文件，或搜索并选择目标公司后重试。
     > （Frank / Fran / Lisa 三位销售员工均支持单独下任务，无需强制搭配 AiWa；如果你本来就想顺带做客户挖掘，也可以在指令里追加「找 N 个 XX 客户」让 AiWa 协同。）


---

### Step 1.5：数字员工可用性校验（Step 1 完成后立即执行，所有任务均须）

**接口：** `GET https://ai.deepsop.com/prod-api/ai/presetEmployee/list`

**请求头：** `x-api-key: $DEEPSOP_API_KEY`

响应 `data` 数组中每条记录关键字段：
- `name`：员工名称（与 employeeList 中的名称对应，如 `AiWa`、`Frank`、`Fran`、`Lisa`）
- `status`：启用状态，`0` = 启用，`1` = 禁用
- `remainingDays`：剩余可用天数（可为 null）

**逐一检查 employeeList 中每个员工，规则如下：**

1. **禁用状态（status = 1）→ 终止任务**，回复：
   > ⚠️ 数字员工「{name}」当前处于禁用状态，无法执行任务。请联系管理员启用后再试。

2. **未开通 / 已过期（status = 0 且 `remainingDays` 为 `null` 或 `remainingDays ≤ 0`）→ 进入签约流程（见下方 Step 1.5.1）**。签约完成后重新拉取 `/ai/presetEmployee/list` 校验，通过后继续；用户放弃或余额不足则终止任务。

3. **剩余天数不足（status = 0 且 remainingDays > 0 且 remainingDays ≤ 7）→ 提醒用户，但允许继续**：
   > ⚡ 提示：数字员工「{name}」剩余可用天数仅剩 **{remainingDays} 天**，建议尽快前往 https://ai.deepsop.com 续费，以免中断服务。

4. **正常（status = 0 且 remainingDays > 7）→ 继续流程**

**所有员工均通过校验后，方可继续后续步骤。任一员工触发规则 1 立即停止；规则 2 必须走完签约流程且成功后才能继续。**

---

#### Step 1.5.1：数字员工签约流程（仅在规则 2 触发时执行）

按顺序执行，**每一步失败或用户放弃均立即终止任务**。

**① 拉取套餐列表**

接口：`GET https://ai.deepsop.com/prod-api/ai/setting/list?packageType=3`
请求头：`x-api-key: $DEEPSOP_API_KEY`

响应 `data` 为数组，每项结构：
```
{
  presetEmployeeId,          // 关联员工 ID，用于匹配当前待签约员工
  packageOptions: [
    {
      id,                    // optionId（提交签约用）
      packageId,             // 套餐 ID（提交签约用）
      description,           // 套餐名称文案（如"月度套餐"）
      purchaseMonths,        // 1 | 3 | 6 | 12
      actualPrice,           // 人民币实价（元）
      discountRate,          // 折扣率，100 = 无折扣
      giftKToken             // 赠送 K 币数量
    }
  ]
}
```

根据当前待签约员工的 `id` 匹配对应条目，取其 `packageOptions`。

**② 展示套餐让用户选择**

先获取人民币→K币汇率：
接口：`GET https://ai.deepsop.com/prod-api/system/config/configKey/CNY_TO_KCOIN`
响应 `msg` 即为汇率（记为 `rate`）。

每个套餐的**应付 K 币**计算公式：
```
priceKCoin = actualPrice × (discountRate / 100) × rate
```

向用户展示（格式示例）：
```
数字员工「{name}」尚未开通，请选择签约套餐（回复序号）：
1. {description}（{purchaseMonths}个月） — {priceKCoin} K币{折扣率≠100 时追加"（{discountRate/10}折）"}{giftKToken>0 时追加"，赠送 {giftKToken} K币"}
2. ...

回复「取消」放弃签约。
```

**等待用户回复序号**。用户选"取消"或无响应 → 终止任务并回复：
> 已取消签约，任务终止。

**③ K 币余额校验**

接口：`GET https://ai.deepsop.com/prod-api/ai/vip/balance?userId={userId}`
请求头：`x-api-key: $DEEPSOP_API_KEY`

其中 `userId` 取自 Step 3 前置 B `/ai/user/profile` 返回的 `data.userId`（若此前未调用则先调用获取）。响应 `data` 即为当前 K 币余额。

> 🔒 **强制实时查询规则（极其重要，避免使用缓存余额）：**
> - 每次进入本步骤 ③ 都**必须**重新调用一次 `/ai/vip/balance` 接口，**严禁**复用本会话中任何先前一次查询到的 `balance` 值。
> - 典型踩坑场景：一次任务里有多个员工需要连续签约（例如先给 AiWa 签约扣了 K 币，紧接着又要给 Frank 签约）；或同一员工首次提示余额不足、用户充值后让你重试 —— 此时上一轮的 `balance` 已经过时，**必须**重新发请求拿最新值，**不得**沿用记忆里的旧数字做判断或在话术中展示。
> - 同样地，在 ④ 提交签约扣款成功之后，如果还有下一个员工要走签约流程，回到本步骤 ③ 时也**必须**重新查询余额，不得用「旧余额 - priceKCoin」自行推算。
> - 用户口头告知"我已经充值了/余额已经够了"也**不能**作为跳过本接口的理由，必须以接口实时返回为准。

取余额 `balance`（**本次接口调用的最新返回值**），与所选套餐的 `priceKCoin` 比较：

- **`balance < priceKCoin` → 余额不足，终止任务**，回复：
  > ❌ 余额不足，签约失败。当前余额：**{balance} K币**，所需：**{priceKCoin} K币**。
  > 请前往 https://ai.deepsop.com 登录后充值 K 币，充值完成后重新下达任务。

  **不要**尝试任何充值接口，直接终止流程。

- **`balance ≥ priceKCoin` → 进入 ④**

**④ 提交签约（扣 K 币）**

接口：`POST https://ai.deepsop.com/prod-api/ai/order/purchaseIndependentPackageByKToken`
请求头：`x-api-key: $DEEPSOP_API_KEY`
请求体：
```json
{
  "packageId": "<选中套餐的 packageId>",
  "optionId": "<选中套餐的 id>"
}
```

- 成功 → 回复：
  > ✅ 「{name}」签约成功！套餐：{description}，扣除 {priceKCoin} K币。
- 失败（含后端返回余额不足错误码）→ 按"余额不足"文案回复并终止。

**⑤ 回到 Step 1.5 重新拉取 `/ai/presetEmployee/list` 校验**，该员工状态正常后继续剩余流程。

> ⚠️ 如果剩余 employeeList 中还有其他员工需要走签约流程，回到 Step 1.5.1 处理下一个员工时，**步骤 ③ 必须重新调用 `/ai/vip/balance` 拉取最新余额**（因为本员工的 ④ 已经扣过 K 币，旧余额已失效）。**禁止**用「上一员工查到的 balance − 上一员工 priceKCoin」自行推算结果作为下一员工的余额判断依据。

---

### Step 1.6：客户来源选择（仅当 employeeList 含 Frank/Fran/Lisa 但**不含** AiWa 时执行）

本步骤用于在没有 AiWa 协同的销售任务里，由用户直接指定本次销售动作要面向的客户池。所有数据最终写入 `collaborationSubmitTaskParam.sourceSettings` 对象（结构见本步骤末尾「最终装配规则」）。

**触发条件回顾：** `employeeList` 不含 `AiWa`，且至少含 `Frank` / `Fran` / `Lisa` 之一。`employeeList` 含 `AiWa`（无论是否还含销售员工）时，**跳过本步骤**。

**首次提问：让用户在两种来源中二选一（也可两者并用、累加生效）：**

```
🧭 检测到本次任务无 AiWa 客户挖掘协同，请选择客户来源（可二选一，也可两种叠加）：

1. 上传 xlsx 文件
   - 客户管理（公司导入）模板：调用 API 清单 #23 `POST /ai/customer/template` 下载（详见下方「模板下载接口」小节）
   - 地址簿（地址簿导入）模板：调用 API 清单 #24 `POST /ai/customer/contactImportTemplate` 下载（详见下方「模板下载接口」小节）
   你可以直接上传 xlsx 文件，也可以以文字形式按模板格式提供客户/地址簿信息，由我代为整理成对应 xlsx 后上传。

2. 搜索选择公司
   通过关键词搜索系统内已存在的公司（客户），由你勾选若干条，对应的客户 ID 会进入 suppurIds。

请回复「1」「2」或「1+2」，并附上你的具体输入。
```

#### 途径 A：上传 xlsx 文件

##### 模板下载接口（API 清单 #23 / #24）

两个模板**不再**从写死的 OSS 链接获取，必须改为调用后端接口实时下载（与前端 Vue 项目 `handleDownloadTemplate` / 通用 `download(url, params, filename)` 行为一致）。

**接口：**
```
POST https://ai.deepsop.com/prod-api/ai/customer/template            # 公司导入模板（uploadType === 'fileList'）
POST https://ai.deepsop.com/prod-api/ai/customer/contactImportTemplate  # 地址簿导入模板（uploadType !== 'fileList'）
```

**请求头：**
- `x-api-key: $DEEPSOP_API_KEY`
- `Content-Type: application/x-www-form-urlencoded`

**请求体：** 空 form（`params = {}`，序列化后为空字符串），**不要**带 JSON body。

**响应：** `responseType: 'blob'`，二进制 xlsx 流。客户端按 `导入模板_${Date.now()}.xlsx` 命名保存即可。

**Blob 校验规则（与前端 `blobValidate(data)` 一致）：**
- 若返回的 Blob 是真实 xlsx 二进制（首字节为 `PK..` zip 头）→ 视为成功，直接 `saveAs(blob, filename)`。
- 若 Blob 实为 JSON 文本（被错误包装成 blob 的错误响应）→ 读取 text 后 `JSON.parse`，把 `msg` 原样回给用户，**不要**当成 xlsx 保存。

等价 curl（用于排查/手工取模板）：
```bash
curl --location --request POST 'https://ai.deepsop.com/prod-api/ai/customer/template' \
     --header 'x-api-key: $DEEPSOP_API_KEY' \
     --header 'Content-Type: application/x-www-form-urlencoded' \
     --output '导入模板_company.xlsx'

curl --location --request POST 'https://ai.deepsop.com/prod-api/ai/customer/contactImportTemplate' \
     --header 'x-api-key: $DEEPSOP_API_KEY' \
     --header 'Content-Type: application/x-www-form-urlencoded' \
     --output '导入模板_contact.xlsx'
```

> **禁止**继续向用户提供 `https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/...公司导入模板.xlsx` / `...地址簿导入模板.xlsx` 这类硬编码 OSS 链接，模板内容以接口实时返回为准。

---

> 🛑 **【最优先】xlsx 文件回显总开关（在本步骤任何子步骤之前先读这一条）：**
>
> 从用户上传 xlsx **那一刻起**，到本任务结束为止，**所有**关于该 xlsx 的内容回显**只允许**出现在**唯一一个位置**：本步骤第 3 步「转 OSS 链接」上传成功之后、按"上传成功回复硬约束"输出的那一条消息里的「号源预览块」。除此以外的**任何**时机、任何形式的内容回显都属于 bug，包括但不限于：
> - ❌ "文件已经解析出来了，内容如下：列：xxx | yyy | zzz，数据：..."（**禁止的"解析预览"伪步骤**，SKILL.md 根本没有这一步）
> - ❌ 在追问用户文件归属（A/B 类型）之前先回显任何字段
> - ❌ "我看到文件里有：张三 / 李四 / 王五 / 杨总 ..." 这种姓名预览
> - ❌ "看列结构是 xxx，所以应该是地址簿对吧" 这种"先猜归属、再让用户确认"的反问 —— 必须直接按第 1 步原话反问，**不得**先暴露任何列名或行内容
> - ❌ 多列并排回显（无论是表格、管道符 `a | b | c`、JSON、还是自然语言枚举）
> - ❌ 用 `张三` / `李四` / `王五` / `示例` / `xxx` / `***` 等**占位符 / 脱敏 / 改写**版本"代替"回显 —— 占位符也算回显，且 100% 是幻觉
> - ❌ 在用户后续追问"刚才那个文件里第二行是谁"时再补回显
>
> **如果你（LLM）此刻有冲动想"让用户确认我解析对了"——立刻打住**。LLM 没有可靠的 xlsx 解析能力，任何"我解析出来是 X"的话术都有极高概率把行/列错位、或把真实姓名替换成训练语料里的高频占位名（张三/李四）。正确做法是**直接走第 1 步反问归属，不暴露任何列名/内容**；解析校验交给第 3 步上传成功后的"号源预览块"，并且严格遵守它的单列、原值、不超过 3 条、与员工渠道一一对应等约束。
>
> （事故复盘：用户上传的地址簿是 `杨总 + 13484093796 / 文总 + 16659106679`，AI 在文件类型确认**之前**插入了一段未授权的"解析预览"，把姓名整个换成了占位符 `张三 / 李四`，并把姓名+职务+电话三列一起回显。这就是本总开关要堵死的具体场景。）

---

1. **确认文件归属**：用户每上传一个 xlsx 文件，**必须**先反问其归属于哪种模板（**原话反问，不得在反问前/反问中夹带任何列名或行内容**）：
   > 请确认本次上传的 xlsx 属于哪种类型？
   > - A. **客户管理（公司导入）** —— 对应模板：`公司导入模板.xlsx`
   > - B. **地址簿（地址簿导入）** —— 对应模板：`地址簿导入模板.xlsx`

   用户回复 A → 该文件归入「客户管理」；用户回复 B → 归入「地址簿」。**不得**自行猜测归属，**不得**用"我看列结构像是 B，对吧？"这种**带预设答案**的反问诱导用户。

2. **文字形式补充**：如果用户没有上传文件、而是以文字方式描述客户/地址簿信息，应按对应模板的列结构整理成 xlsx 文件，再走相同的上传 / 归属确认流程。整理时遵循模板列顺序与字段名，**禁止**自行新增列或合并列。

3. **转 OSS 链接**：调用 DeepSOP 的统一文件上传接口（API 清单 #22），后端会把文件落到阿里云 OSS 并返回公网可访问的 `https://...aliyuncs.com/...` 链接。

   **接口：**
   ```
   POST https://ai.deepsop.com/prod-api/system/fileUpload/upload
   ```

   请求头：
   - `x-api-key: $DEEPSOP_API_KEY`
   - `Content-Type: multipart/form-data`（让 HTTP 客户端自动带 boundary，不要手填）

   请求体（form-data）：
   - `file`：xlsx 文件本身（**字段名严格为 `file`，不得改成 `upload` / `xlsx` / `attachment`**）

   等价 curl：
   ```bash
   curl --location --request POST 'https://ai.deepsop.com/prod-api/system/fileUpload/upload' \
        --header 'x-api-key: $DEEPSOP_API_KEY' \
        --form 'file=@"<本地 xlsx 绝对路径>"'
   ```

   **成功响应示例：**
   ```json
   {
     "msg": "操作成功",
     "code": 200,
     "fileName": "公司导入.xlsx",
     "url": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/material/100/xxx.xlsx"
   }
   ```

   **响应解析规则：**
   - 当且仅当 `code === 200` 视为成功；其它 `code` 一律按上传失败处理，把 `msg` 原样回给用户并要求重试，**不得**继续。
   - 取顶层 `url`（**不是** `data.url`，本接口的成功结构是平铺字段）作为 OSS 链接。
   - 该 URL 必须满足：`https://` 开头 + 域名含 `aliyuncs.com`。不满足则视为上传失败，**不得**写入 `fileList` / `addressFileList`。

   > 🛑 **上传成功回复硬约束（强制，违反即视为 bug）：**
   >
   > 用户上传 xlsx 成功后，**只能**给用户回以下格式的话（基础句式 + 可选号源预览）：
   >
   > > ✅ 文件 `{fileName}` 上传成功，本次共导入 **{N}** 条{公司 / 联系人}数据。
   >
   > - `{N}` = 本地 xlsx 的**数据行数**（不含表头行）；如果当前运行环境无法读取本地 xlsx，就只回「文件上传成功」，**不要**自己编一个数字。
   > - 类型 A（公司导入）→ 后缀「条公司数据」；类型 B（地址簿导入）→ 后缀「条联系人数据」。
   >
   > **号源预览规则（按下任务员工展示对应渠道字段）：**
   >
   > 在能可靠解析本地 xlsx 的前提下（如运行环境提供了 xlsx 解析能力，且能确定地读出表头列名），按本次任务的**销售执行员工**追加号源预览片段，**只展示与该员工渠道对应的那一列**前 3 条非空值，不展示其他任何字段：
   >
   > | 任务员工 | 展示列 | 列名匹配（命中任一即可，大小写不敏感） |
   > |---|---|---|
   > | **Frank**（邮件销售） | 邮箱 | `email` / `邮箱` / `邮件` |
   > | **Fran**（电话销售） | 电话 | `phone` / `mobile` / `tel` / `电话` / `手机` / `手机号` |
   > | **Lisa**（短信销售） | 电话 | 同上 |
   >
   > 命中后追加格式（注意：每条单独一行，前后用反引号包住，不带姓名/公司/序号以外的任何字段）：
   >
   > > 号源预览（仅展示 {Frank → 邮箱 / Fran/Lisa → 电话} 列前 3 条，供你核对，不代表全部）：
   > > 1. `{value_1}`
   > > 2. `{value_2}`
   > > 3. `{value_3}`
   >
   > **强约束（违反即视为 bug，全部并列生效）：**
   > - **只准展示当前员工对应的那一列**：Frank 不展示电话列，Fran/Lisa 不展示邮箱列；**绝对禁止**把同一行的姓名、公司、地址、岗位、行业、备注等其他字段拼进来。
   > - **必须**严格按 xlsx 中该列的原始顺序取前 3 条非空值，**不得**重排、去重、改写、脱敏、截断或"美化"为占位符。
   > - 同一任务命中多个销售员工（例如 Fran + Lisa）时，电话列只输出**一次**预览块；如果同时有 Frank 和 Fran/Lisa，则分别输出邮箱预览块与电话预览块（仍然各自只取该列前 3 条）。
   > - **任何**无法可靠解析的情况一律退化为"只回文件名 + 条数"基础句式，**不得**输出号源预览块。包括但不限于：运行环境读不到本地 xlsx；找不到匹配的列名；该列前 3 行全部为空；列内容看起来与渠道不符（如声称是邮箱列但值里没有 `@`、声称是电话列但值里全是非数字字符）。
   > - **绝对禁止**凭记忆 / 凭印象 / 凭用户聊天里提过的样例**编造**号码或邮箱。哪怕只多写一个数字、改一个字母，也按 bug 处理。
   > - **绝对禁止**在号源预览块里出现**任何**人物姓名、公司名、阶段标签、星级、地区、备注；如果用户后续追问"这是谁的号码 / 哪个公司的邮箱"，统一回："导入的明细以 DeepSOP 后台为准，提交任务后可在客户管理 / 地址簿模块查看，本助手只对你核对的渠道列（电话/邮箱）做有限回显，不关联到具体人物或公司，以免错位。"
   >
   > **历史事故复盘（必读）：** 早期实现里 AI 在"上传成功"提示里把内容回显成了 `C 公司 + A 电话 / D 公司 + B 电话` 这种**行/列错位**结果（用户原文件其实是 `A 公司 + A 电话 / B 公司 + B 电话`），导致用户去删数据 / 重传 / 改任务。**根本原因**：LLM 没有可靠的跨字段对齐能力，只要同时回显 ≥2 个字段就有概率串行。所以本规则刻意**只允许单列回显、且是与当前员工渠道一一对应的那一列**——既能让用户核对号源到底有没有传对，又把 LLM 的错位风险压到最低。

4. **落位规则**：
   - 类型 A（客户管理 / 公司导入）→ 把上传接口返回的 `{ name, url }` **对象**追加到 `sourceSettings.fileList` 数组中。
   - 类型 B（地址簿 / 地址簿导入）→ 把上传接口返回的 `{ name, url }` **对象**追加到 `sourceSettings.addressFileList` 数组中。
   - 同一类型可累加多个文件，按上传顺序追加。

   > 🛑 **类型强约束（最常见、最高危错误）**：`fileList` / `addressFileList` 的元素**必须是 `ExcelFile` 对象**，对应后端 Java POJO：
   >
   > ```java
   > public static class ExcelFile {
   >     String name;   // 文件名（含 .xlsx 后缀），如 "公司导入.xlsx"
   >     String url;    // 阿里云 OSS 公网 URL（来自上传接口顶层 url 字段）
   > }
   > ```
   >
   > 整体类型是 `ExcelFile[]`（即 `Array<{name: string, url: string}>`）。两字段约束完全对称，**任一**写错都会导致后端解析失败或客户来源丢失。
   >
   > **元素装配规则：** 上传接口 `/system/fileUpload/upload` 成功响应的顶层字段：
   > - `fileName` → 装到 ExcelFile 的 **`name`** 字段（注意：上传响应叫 `fileName`，但 ExcelFile 的字段叫 `name`，需要重命名）
   > - `url` → 装到 ExcelFile 的 `url` 字段
   >
   > **`addressFileList`（地址簿 / 地址簿导入）**
   >
   > **正确：**
   > ```json
   > "addressFileList": [
   >   { "name": "地址簿导入.xlsx", "url": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/material/100/xxx.xlsx" }
   > ]
   > ```
   >
   > **错误：**
   > - ❌ `"addressFileList": ["https://..."]`（裸 URL 字符串数组 — 后端反序列化为 ExcelFile 失败）
   > - ❌ `"addressFileList": [{ "url": "https://..." }]`（漏 `name`）
   > - ❌ `"addressFileList": [{ "name": "...", "url": "...", "fileName": "..." }]`（多余 `fileName` 键 — 用 `name`，不要再带 `fileName`）
   > - ❌ `"addressFileList": [{ "fileName": "...", "url": "..." }]`（key 写成 `fileName` — 必须是 `name`）
   > - ❌ `"addressFileList": {}`（空对象 — 类型必须是数组）
   > - ❌ `"addressFileList": [{}]`（空对象元素）
   > - ❌ `"addressFileList": null` / 省略字段（无地址簿文件时写成空数组 `[]`，**不能**为 `null` 或缺省）
   >
   > **`fileList`（客户管理 / 公司导入）**
   >
   > **正确：**
   > ```json
   > "fileList": [
   >   { "name": "公司导入.xlsx", "url": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/material/100/yyy.xlsx" }
   > ]
   > ```
   >
   > **错误：** 错误模式与 `addressFileList` 完全对称（裸字符串、漏 `name`、key 写成 `fileName`、`{}` / `null` / 缺省、空对象元素等），不再赘述。此外：
   > - ❌ 把已经成功上传的 xlsx 文件 "忘了"放进去（最终请求体里 `fileList: []`，导致前端选了文件但后端实际收不到客户来源）
   >
   > **统一规则**：用户每上传一个 xlsx 并由其确认归属后，对应的 `{ name, url }` 对象（`name` 来自上传响应的 `fileName`，`url` 来自顶层 `url`）必须作为 ExcelFile 元素 push 进对应数组（A 类→`fileList`，B 类→`addressFileList`），并在最终提交前肉眼核对 `sourceSettings` 中两字段的元素数量与已确认归属的文件数一致。**禁止**在最终请求体里把已成功上传的文件丢失为 `[]`，更**禁止**把字段写成 `{}` / `null` / 字符串数组 / 漏 `name` 或 `url` 任一键。

5. **`updateSupport`（仅 `fileList` 非空时生效）**：
   - 含义：xlsx 中存在与系统内已有客户**公司名完全相同**时，是否覆盖更新已有客户信息。
   - 取值：`1` = 更新（默认）；`0` = 不更新。
   - 用户未明确说明时使用默认值 `1`；用户表达「不要覆盖 / 保留原数据 / 不要更新已有客户」等含义时改为 `0`。

#### 途径 B：搜索选择公司（`sourceType === 'search'`）

此途径对应前端 Vue 项目的「客户搜索栏」逻辑（`sourceType === 'search'` 分支），与前端共用同一个客户列表接口。

**接口（API 清单 #21）：**
```
POST https://ai.deepsop.com/prod-api/ai/customer/customerList?pageNum={pageNum}&pageSize=10
```

请求头：`x-api-key: $DEEPSOP_API_KEY`

**Query 参数（与 body 中同名字段冗余传递，与前端 Vue 的 `params` 对齐）：**
- `pageNum`：从 `1` 开始的页码
- `pageSize`：**固定为 `10`，禁止改写**

**Body（JSON）：**
```json
{
  "pageNum": <同上>,
  "pageSize": 10,
  "name": "<公司名搜索关键词，无关键词时填空字符串 \"\">",
  "searchSort": "<排序字段：\"\" | \"email\" | \"phone\">",
  "type": 0
}
```

> 🔒 **Body 字段硬约束：**
> 1. `type` **恒为数字 `0`**（不是字符串、不是 `1`），来自前端 `getCustomerList` 中 `{ ...customerQueryParams, type: 0 }` 的硬编码。
> 2. `searchSort` 仅允许三种值：`""`（默认不排序）、`"email"`（按邮箱排序）、`"phone"`（按电话排序）。任何其他值都属于编造。
> 3. `name` 为空时必须显式传 `""`，**不要**省略键也不要传 `null`。
> 4. 同一次会话中，每次发起搜索都需把上述 5 个键全部带上，缺键属于错误。

**响应字段：**
- `total`：搜索到的总条数（数字）
- `rows`：当前页的客户数组，每条至少含：
  - `id`：客户唯一 ID（用于装入 `suppurIds`）
  - `name`：公司名
  - `countryName` / `countryValue`：国家中文名 / 国家代码（如 `cn`、`us`，前端用作国旗图片名）
  - `email` / `phone`：联系邮箱 / 电话（可能为空，空时取 `aiCustomers[0]` 的对应字段）
  - `stageLabel`：客户阶段对象 `{ stageLabel, backgroundColor, color }`（可空）
  - `groupName` / `groupId`：客户分组（可空）
  - `level`：客户星级（0–5）
  - `aiSuppurLabels`：客户标签数组 `[{labelName, backgroundColor, color}, ...]`
  - `aiCustomers`：联系人数组；当 `email` / `phone` 为空时，前端会取 `aiCustomers[0].email` / `aiCustomers[0].phone` 兜底（对齐 Vue 的 `handlePropLabel`）。
  - `aiDynamics` / `aiEmails` / `aiPhoneCalls`：跟进动态 / 邮件 / 电话数组，**后端原始返回**，前端 `calculateLastFollowInfo` 用它们衍生出 `lastFollowInfo` 字段。

> ℹ️ **`lastFollowInfo` 不是后端返回字段**，是前端纯展示衍生数据。SKILL 侧只需要 `id` 用于 `suppurIds`，无需复刻 `calculateLastFollowInfo` 的衍生逻辑；如需在对话里展示"最近动态"，可参考 Vue `calculateLastFollowInfo`：从 `aiDynamics` / `aiEmails`(`emailSubject` 当 content、`createTime` 当 time) / `aiPhoneCalls`(解析 `describeJobJson.body.job.contacts[0].phoneNumber + tasks[0].status`) 三个列表中各取最新一条，再按 `time` 取最大者作为该客户的"最近动态"。

**交互流程：**

1. **首次进入搜索**：用户选择途径 2 后，先以默认参数 `{ pageNum: 1, pageSize: 10, name: "", searchSort: "", type: 0 }` 拉取一次列表（与 Vue `watch.sourceType` 中 `if (newVal === 'search' && !this.customerTableData.length)` 行为一致），再让用户输入关键词。

2. **关键词搜索**：用户给出公司名 / 关键词时，把它作为 `name` 重发请求，并把 `pageNum` 重置为 `1`（对齐 Vue 的 `handleCustomerQuery`）。

3. **结果展示**：每次返回向用户输出：
   > 共搜到 **{total}** 条数据，当前为第 **{pageNum}** 页 / 共 **{Math.ceil(total/10)}** 页（每页 10 条）。
   >
   > 1. {name} | {countryName} | {email or phone} | 阶段：{stageLabel?.stageLabel || '—'} | 等级：{level}星
   > 2. ...
   >
   > 回复「页码 N」切换分页；回复「{name 关键词}」重新搜索；回复要选中的条目序号（多个用逗号分隔，如 `1,3,5`）或「全选当前页」加入选择；回复「清空选中」可重置已选；回复「确认」结束选择。

4. **翻页**：用户回复「页码 N」时，保持 `name` / `searchSort` 不变，仅更新 `pageNum = N` 后重新调用接口。`N` 必须 ∈ `[1, ceil(total/10)]`，越界则回复并要求重输。

5. **排序切换（可选）**：当用户表达"按邮箱排序" / "按电话排序"时，把 `searchSort` 设为 `"email"` / `"phone"`，否则保持 `""`（对齐 Vue 的 `handleCustomerSortChange`：再次点击同一列时回到 `""`）。

6. **勾选 / 全选 / 清空**（对齐 Vue 的 `handleCustomerSelect` / `handleCustomerSelectAll` / `handleClearCustomerSelection`）：
   - 单选：`selection` 数组中存在该 `id` 则移除，否则追加。
   - 全选当前页：把当前 `rows` 中尚未在 `selection` 内的全部加进去；取消全选则把当前 `rows` 中已选的从 `selection` 移除（**只影响当前页**，不清掉其他页已选）。
   - 清空：`selection` 置空。
   - 翻页或重新搜索时**不要清空 `selection`**（Vue 中 `getCustomerList(false)` 的 `clearSelectionFlag=false` 路径），需要在新页面里把已勾选过的行用接口返回的 `id` 集合**回显**为已选。

7. **同步到 `sourceSettings.suppurIds`**（对齐 Vue 的 `syncCustomerIds`）：每次 `selection` 变更立即执行：
   ```
   sourceSettings.suppurIds = selection.map(item => item.id)
   ```
   **字段名是 `suppurIds`（拼写：`suppur` 非 `supplier`），不得改写为 `supplierIds` / `customerIds`。** `id` 类型保持接口返回原样（数字或字符串），不做 toString / parseInt 转换。

8. **结束选择**：用户回复「确认」（或表达完成选择的等价语义）后退出途径 B。**未确认前**不进入 Step 2/3。

#### 最终装配规则

完成客户来源选择后，本步骤产出的 `sourceSettings` **必须**严格采用以下结构（键集与示例一致，键序不限）：

```json
{
  "groupId": [],
  "stageId": [],
  "labelId": [],
  "level": [],
  "seasGroupIds": [],
  "addressId": [],
  "fileList": [],
  "updateSupport": 1,
  "addressFileList": [],
  "suppurIds": []
}
```

字段说明（仅 `fileList` / `updateSupport` / `addressFileList` / `suppurIds` 由本步骤填充，其余固定为空数组）：

| 字段 | 类型 | 来源 | 说明 |
|---|---|---|---|
| `groupId` / `stageId` / `labelId` / `level` / `seasGroupIds` / `addressId` | `array` | 固定空数组 `[]` | 当前 SKILL 不暴露这些维度的选择，恒为 `[]` |
| `fileList` | `ExcelFile[]` | 途径 A 类型 A | 客户管理（公司导入）xlsx 文件对象列表，元素结构 `{ "name": "<文件名>", "url": "<OSS URL>" }` |
| `updateSupport` | `0 \| 1` | 途径 A 用户确认 | 公司同名是否覆盖更新，默认 `1` |
| `addressFileList` | `ExcelFile[]` | 途径 A 类型 B | 地址簿（地址簿导入）xlsx 文件对象列表，元素结构同 `fileList` |
| `suppurIds` | `(string\|number)[]` | 途径 B | 用户搜索选中的客户 ID 列表 |

**最终硬校验（继续后续步骤前必过）**：
- `fileList.length > 0` **或** `addressFileList.length > 0` **或** `suppurIds.length > 0`，三者**至少一个**非空。
- 若三者全空，回到本步骤开头重新询问用户；连续 2 次询问仍全空，按 Step 1「员工组合校验」第 2 条的终止文案结束任务。

> 🔒 **本步骤产出的 `sourceSettings` 优先级最高**：当 `employeeList` 不含 AiWa 但含销售员工时，最终提交请求体中的 `sourceSettings` 必须是本步骤产出的对象，**禁止**使用 AiWa 联合场景下含 `cascader` / `aiMining` / `customerMining` / `seasMining` / `uploadMining` / `countryId` / `addressMining` 的旧版结构。

---

### Step 1.7：电话场景创建/审核子流程（独立入口）

> 触发方式（**任一**）：
> - **A. 用户主动触发**：Step 1 意图分流命中"场景创建"关键词。
> - **B. Fran 流程兜底**：Step 3 前置 A-2 的 `listScripts` 返回空、或全部场景 `status` 都不是 `PUBLISHED`，且用户回复"创建/我自己建/帮我建一个"。
>
> 出口：拿到 `scriptId` + `agentProfileId`（场景已 PUBLISHED）。
> - 触发方式 A 完成后：直接回复用户"场景已发布，可用于后续电话销售任务"，**不再**自动进入销售流程；
> - 触发方式 B 完成后：把 `scriptId` / `agentProfileId` 当作前置 A-2 的选定结果，继续 Step 3 前置 B / D / 最终提交流程。

#### Step 1.7.0：环境前置自检

进入子流程前，先校验外呼实例可用性（与 Step 3 前置 A-0 同接口）：

接口：`GET https://ai.deepsop.com/prod-api/ai/outBound/describeInstance`，请求头 `x-api-key: $DEEPSOP_API_KEY`。

- 实例并发数为 0：终止子流程，回复用户"外呼实例并发数为 0，请联系管理员开通后再尝试创建场景"；
- 实例可用：继续。

#### Step 1.7.1：澄清场景基础信息

向用户依次询问以下槽位。**每一轮只问 1～2 个槽位**，等用户回复后才追问下一组。**所有 `promptJson.*` 字段名与上限均与前端 Vue 表单严格对齐，超长会被后端拒绝或截断**：

| 槽位 | 必填 | 默认 | 上限（字符） | 说明（与 Vue 表单 label 一致） |
|---|---|---|---|---|
| `industry` | 否 | `"通用"` | — | 行业（scriptParams.industry） |
| `scene` | 否 | `"通用"` | — | 场景（scriptParams.scene） |
| `scriptName` | 是 | — | ≤30 | 场景库名称（scriptParams.scriptName） |
| `promptJson.openingPrompt` 👋 开场白 | **是** | — | **200** | 开场白原文，直接对客户读出来的话 |
| `promptJson.goals` 🚩 目标 | **是** | — | **1000** | 此次呼叫的目的，如「调研上次服务的满意度情况」 |
| `promptJson.background` 📌 背景 | 否 | `""` | 2000 | 呼叫背景，活动信息、FAQ 等 |
| `promptJson.skills` 🛠️ 技能 | 否 | `""` | 1000 | 机器人能执行的具体事项（多条用编号） |
| `promptJson.workflow` 🧰 流程 | 否 | `""` | 4000 | 与客户交流的过程骨架 |
| `promptJson.constraint` 📦 约束 | 否 | `""` | 3000 | 对话约束/异常话术（专业用语、情绪识别等） |

> ⛔ **禁止 LLM 自己脑补 `openingPrompt` 与 `goals`**：必须由用户至少给出大致内容；若用户说"你帮我编一个"，先草拟一版**展示给用户确认**，等待用户回复"确认/就这个"才能继续。
>
> ⛔ **禁止超长**：每个字段提交前自检 `len(value) ≤ 上限`；接近上限时（≥80%）主动提醒用户精简，避免脚本 pre-flight 校验报 `TOO_LONG`。
>
> ⛔ **不要再向用户索要 Vue 表单未暴露的字段**（如 `name` / `gender` / `age` / `role` / `communicationStyle` / `output` / `aiHangupOutput` / `aiSilenceTimeoutOutput`）。这些字段在 schema 里存在，但 Vue UI 不让用户填，本 SKILL 同样**统一以空字符串占位**，由后端使用其默认行为。

线索字段（`agentForm.labelsJson`，对应 Vue 底部「线索收集管理」表格，非必填，可多次追加）：
让用户列出"这通电话需要收集的客户信息"，每条 3 列：
- **线索名称**（`name`）：要收集的字段名，如「客户兴趣」「能否到访」
- **线索描述**（`description`）：用于让机器人正确判定该线索的解释
- **线索关键词**（`valueList`）：候选取值数组（Vue UI 是"+ 关键词"逐个加 tag），如 `["有兴趣","没兴趣","待跟进"]`；用户可以不填，留空数组 `[]` 表示开放收集

> 装配时 `valueList` 必须**先转成 JSON 字符串**（如 `"[\"有兴趣\",\"没兴趣\"]"`），这是阿里云 Chatbot 的格式硬要求；脚本内 `validate_script_params.py` 会强校验此点。

变量字段（`agentForm.variablesJson`，非必填）：通话过程中需要替换的占位变量名（如 `customerName`），每条 `{name, description}`，最终也是 JSON 字符串。

#### Step 1.7.2：TTS 音色配置

向用户提供以下默认值，并允许用户调整：

```
默认 TTS 配置：
- 发音人：CosyVoice:longcheng（女声 / 通用）
- 引擎：ali（阿里云标准 TTS）
- 音量：50（0–100）
- 语速：0（-500 ~ +500）
- 语调：0（-500 ~ +500）
- 全局可打断：开
- 服务类型：Managed
```

用户可单点或整体替换；若选择克隆音色，引擎须改为 `bailian`。**禁止**让用户自由输入 `nlsServiceType` / `nluEngine` / `nluAccessType`，全部按下方"参数固定值"装配。

#### Step 1.7.3：装配请求体（两段 JSON 字符串）

待全部槽位收齐，按以下结构装配。**严格对齐 Vue 数据模型**：`promptJson` 内部包含全部 14 个 schema 字段，但只有 6 个用户可填字段会有值，其余字段统一使用空字符串占位。

`agentParams.promptJson` / `labelsJson` / `variablesJson` / `scriptParams.ttsConfig` 都是**先建对象/数组再 `JSON.stringify` 一次**得到的字符串；其中 `labelsJson[*].valueList` 还要再 `JSON.stringify` 一次（**二次 stringify**）。

构建步骤建议（按顺序，避免 LLM 拼错引号）：

1. 先构造 promptJson 的 **对象**：
   ```json
   {
     "name": "", "gender": "", "age": "", "role": "", "communicationStyle": "",
     "openingPrompt": "您好，我是XX公司客服助理...",
     "goals":         "邀约客户参加 4 月 20 日新品发布会",
     "background":    "",
     "skills":        "",
     "workflow":      "",
     "constraint":    "",
     "output": "", "aiHangupOutput": "", "aiSilenceTimeoutOutput": ""
   }
   ```
   再 `JSON.stringify` 一次得到 `agentParams.promptJson` 字符串。

2. 构造 labelsJson 的 **数组**（用户每条线索）：
   ```json
   [
     { "name": "客户兴趣", "description": "客户对产品是否有兴趣的判断", "valueList": ["有兴趣", "没兴趣", "待跟进"] }
   ]
   ```
   **遍历**对每个元素的 `valueList` 单独 `JSON.stringify`：
   ```json
   [
     { "name": "客户兴趣", "description": "客户对产品是否有兴趣的判断", "valueList": "[\"有兴趣\",\"没兴趣\",\"待跟进\"]" }
   ]
   ```
   再对整个数组 `JSON.stringify` 一次得到 `agentParams.labelsJson`。

3. 构造 ttsConfig 的 **对象**，再整体 `JSON.stringify` 得到 `scriptParams.ttsConfig`：
   ```json
   {
     "voice": "CosyVoice:longcheng",
     "voiceShow": [0, "CosyVoice:longcheng"],
     "volume": 50,
     "speechRate": 0,
     "pitchRate": 0,
     "globalInterruptible": true,
     "engine": "ali",
     "nlsServiceType": "Managed"
   }
   ```

4. 最终请求体（与 Vue `getProcessData()` 输出 1:1 对齐）：
   ```json
   {
     "agentParams": {
       "model": "model_001",
       "agentProfileId": "",
       "promptJson":     "<上方第 1 步 stringify 后的字符串>",
       "labelsJson":     "<上方第 2 步 stringify 后的字符串>",
       "variablesJson":  "[]"
     },
     "scriptParams": {
       "scriptId": "",
       "scriptName": "4月新品发布邀约",
       "industry": "通用",
       "scene": "通用",
       "nluEngine": "Prompts",
       "nluAccessType": "Managed",
       "ttsConfig": "<上方第 3 步 stringify 后的字符串>"
     }
   }
   ```

> 🔒 **字段名零改写规则同样适用于本步骤**（参见 Step 3 总规约「字段名零改写规则」）：
> - `agentParams` ≠ `agent_params` / `AgentParams`；`scriptParams` ≠ `script_params`
> - `promptJson` / `labelsJson` / `variablesJson` 必须是 **JSON 字符串**（外层套引号、内层用 `\"`），**不得**直接放对象/数组
> - `ttsConfig` 同上，是 JSON 字符串而不是对象
> - `labelsJson` 元素里的 `valueList` 是**二次 stringify 过的字符串**（如 `"[\"v1\",\"v2\"]"`），不是数组
> - **修改场景**（Fran 流程兜底外的「编辑现有草稿」入口）需在 `agentParams.agentProfileId` 与 `scriptParams.scriptId` 填入既有值；新建场景这两个字段一律为空字符串 `""`，**禁止省略键名**

> 🔡 **UTF-8 传输强约束**（这是脚本存在的核心理由）：
> - LLM 在 Windows 终端**禁止**直接用 `curl` / `Invoke-RestMethod` 提交以上请求体——cp936 代码页会把 `openingPrompt` / `goals` / `background` 等中文字段静默转码导致后端审核拒绝
> - **必须**通过 `python3 scripts/submit_script_review.py <<'SCRIPT_BODY_EOF' ... SCRIPT_BODY_EOF` 走脚本，脚本内部以 `bytes = json.dumps(body, ensure_ascii=False).encode("utf-8")` + `Content-Type: application/json; charset=utf-8` 显式发送字节，已和 `submit_task.py` 同级别强约束

#### Step 1.7.4：提交并轮询审核

把装配好的 body 通过 stdin 喂给 `scripts/submit_script_review.py`，**禁止**写 curl：

```bash
python3 scripts/submit_script_review.py <<'SCRIPT_BODY_EOF'
{
  "agentParams":  { ... },
  "scriptParams": { ... }
}
SCRIPT_BODY_EOF
```

脚本内部串行执行：
1. UTF-8 解码 stdin；
2. 跑 `validate_script_params.py` 做结构/取值层 pre-flight 校验；
3. POST `/ai/outBound/createOrModifyScriptAndSubmitScriptReview` 提交场景+TTS+机器人设定；
4. 拿到返回中的 `scriptId` / `agentProfileId`；
5. 每 10s 轮询一次 `/ai/outBound/describeScript` 直到 `data.body.script.status === "PUBLISHED"` 或超时（默认 600s）。

可选参数：
- `--no-poll`：提交完立即返回（不等审核），用于"先入库再异步等"的场景。
- `--max-wait-seconds N`：自定义最长等待时长（秒）。
- `--dry-run`：只跑校验，不发任何 HTTP。

输出（stdout 单行 JSON）：
- 成功：`{"ok":true,"stage":"done","scriptId":"...","agentProfileId":"...","status":"PUBLISHED","elapsed_seconds":47}`
- 校验失败：`{"ok":false,"stage":"validate","summary":"...","errors":[{path,code,msg,suggestion}]}`
- 网络/服务端非 2xx：`stage` 为 `http`，含 `response`
- 审核未在超时内完成：`stage` 为 `polling`，含 `scriptId` 与最后一次 `status`
- 审核被驳回（status ∈ {`FAIL_REVIEW`,`REJECT`,`FAILED`}）：`ok:false`，须把错误信息原样回给用户后让其调整 prompt 后重试

> ⛔ **退出码 0 才算成功**；非 0 必须把 `summary` / `errors` 原样回报用户，**禁止**绕过校验或假装成功。

#### Step 1.7.5：审核完成后的处理

- **触发方式 A**（用户主动）：回复
  > ✅ 场景"{scriptName}"已通过阿里云审核（scriptId=`...`，agentProfileId=`...`），后续提交 Fran 电话任务时可直接选用。

- **触发方式 B**（Fran 兜底）：把 `{scriptId, agentProfileId}` 当作前置 A-2 的最终选定结果，**不再**回调 `listScripts`，直接进入 Step 3 前置 B（若需要）或最终装配。在装配 Fran 子对象时：
  - `scriptId` ← 本步骤拿到的字符串原值（不得改名、不得二次包裹引号）
  - `agentProfileId` ← 本步骤拿到的字符串原值（不得改名为 `agentId` / `chatbotId` / `profileId`）

#### Step 1.7.6：场景审核辅助操作（用户已有草稿/审核中场景）

当用户**不是**要新建/编辑场景内容，而是想：

- **重新提交既有草稿/已发布场景进入审核**（如已存在 `DRAFTED` / `ROLLBACK_FAILED` / `PUBLISH_FAILED` / 已 `PUBLISHED` 但想重审的场景）→ 用 5.4 `submitScriptReview`
- **撤销正在审核中的场景**（`TO_BE_REVIEWED` 等）→ 用 5.5 `withdrawScriptReview`

**前置确认**（必须先做，禁止直接发请求）：
1. 调用 5 `listScripts`（请求体 `{"pageNumber":1,"pageSize":20,"scriptName":"<可选关键词>"}`）拿到列表；
2. 将 `scriptName + status + 创建时间` 渲染给用户挑选；
3. 等用户明确选定后才取出对应 `scriptId`。

**请求体**（两个接口结构一致）：

```json
{
  "scriptId": "<上一步选定>",
  "description": "提交审核"
}
```

> 与 `submit_script_review.py` 不同，本步骤**不**走 pre-flight 校验（请求体足够简单），可以直接发送，但仍需通过 `python -c "import urllib.request,json; ..."` 或临时小脚本以 **UTF-8 字节路径**发出，**禁止** PowerShell 原生 `Invoke-RestMethod`（避免 cp936 影响 `description` 字段，虽然此处通常是固定文案）。

成功后**必须**调用 `describeScript` 复查一次 `status` 再回复用户实际状态变化（如 `DRAFTED → TO_BE_REVIEWED`），不要凭返回 `code:200` 就声称"已通过审核"。

---

### Step 2：第二轮 AI 分析（仅当 employeeList 包含 AiWa）

用以下 prompt 对同一用户指令做第二轮分析，严格返回 JSON。**该 prompt 的 JSON 字段名、结构、取值类型不得改写**——下游 `validate_employee_params.py` 与 `addressObjList` 的 `type=1/0` 构建逻辑都依赖此契约。

```
根据【指令】描述，Json格式返回数据，其中所有数值部分一律以字符串输出（如 "50"，禁止输出数字 50），未提及的字段一律返回空字符串 ""（数组类字段除外，按字段说明处理）。

【全局原则】
1. 只识别描述中明确出现的信息，禁止过度解读、补全、推断未提及的内容；不确定时一律返回空字符串。
2. 输出必须是合法 JSON，且除 JSON 外不得出现任何说明文字、Markdown 代码块标记、注释。
3. 字段顺序、键名、类型必须严格与下方"规则"完全一致。

【数值区间通用规则（员工/门店等所有 RangeStart / RangeEnd 字段统一适用）】
- 仅当描述中明确出现"<对象>X<量词><比较词>"形态时才提取，三种比较词分别处理：
  - "X以上"      → Start = "X"，End = ""
  - "X以下"      → Start = ""，End = "X"
  - "X左右"      → Start = "X"，End = "X"
  - "X到Y" / "X-Y" / "X至Y" → Start = "X"，End = "Y"
- 未出现比较词或仅出现单一具体数字（如"员工50人"无以上/以下/左右）→ Start/End 均为 ""。
- 描述中"找X家门店""开发X个客户""挖掘X家"等是**任务目标数量**，**不**写入 storeNumberRange* / employeeNumberRange*；任务目标已在 Step 1 的 totalTarget 处理，本步骤不重复提取。

【国家 vs 七大洲互斥规则】
- 如果描述中提到任何具体国家（如"中国"、"英国"、"美国"），则 continent 必须为 ""，仅在 country / countryCodeList 中输出。
- 仅当描述中只提到大洲（如"亚洲眼镜店"）而未提到任何国家时，才在 continent 输出对应大洲名，country / countryCodeList 留空（country = ""，countryCodeList = ""）。
- 七大洲取值集合限定为：亚洲、欧洲、非洲、北美洲、南美洲、大洋洲、南极洲。

【地址提取规则（addressObjList）】
- 第一步：识别并**排除**所有出现在公司名称、品牌名、企业全称、组织机构名、店铺名中的地理位置——例：【巨龙光学（福建）有限公司】中的"福建"、【XX上海分公司】中的"上海"、【杭州佬大食品】中的"杭州"，均不参与提取。
- 第二步：在剩余描述里提取明确出现的、国家层级之下的地理位置；中国地址按"一级（省/直辖市/自治区）→二级（市）→三级（区/县/镇）"拆分，**多级用英文逗号 `,` 拼接到同一字符串**（如"浙江宁波鄞州区" → "浙江,宁波,鄞州区"）。
- 第三步：非中国地址（英文国家/地区下的地理位置）一律以英文原文整段输出，不做层级拆分（如"London, UK" → "London, UK"）。
- 多个互不归属的地址：用英文分号 `;` 分隔多组（如"浙江宁波;广东深圳" → "浙江,宁波;广东,深圳"；"London, UK; Paris, France" → "London, UK; Paris, France"）。下游会按 `;` 切分为多个对象，再按是否含中文拆分到 `type=1`（结构化省市县）或 `type=0`（自由文本 address）。
- 如排除公司名后**无其他地理位置**，返回 ""（下游会构造占位 `type=1` 空对象，禁止你输出任何编造地址）。

【关键词提取规则（keywordList）】
- 优先识别"客户挖掘"语义片段（包含"找/开发/挖掘/拓展/寻找/获客/开拓/对接"等动词），仅从该片段提取核心名词。
- 若整段描述无客户挖掘语义（如纯品牌运营/内容生产指令），则从整段提取核心业务名词。
- 必须**排除**所有地理位置词（省、市、区、县、镇、国家、大洲、城市/地区名），它们不属于关键词。
- 必须**排除**已写入 employeeNumberRange* / storeNumberRange* / industryList 等其他字段的纯量词、人数、家数。
- 提取后为每个核心名词补全中文同义词与对应英文翻译，最终用英文逗号 `,` 拼接（如"眼镜店" → "眼镜店,optical shop,眼镜零售,eyewear store"）；同义词去重，禁止保留分隔符前后空格。

【行业推断规则（industryList）】
- 根据 keywordList 的核心业务语义推断 1~3 个一级行业标签，用英文逗号 `,` 拼接（如：服装、数码、家居、餐饮、美妆、医疗、教育、汽车、建材、机械、化工、能源、金融、物流、农业、零售、家纺）。
- 不可纯凭地理位置/数量推断行业；若 keywordList 完全无法确定行业，返回 ""。

规则如下（**键名/顺序不可改**）：{
  "keywordList": "按【关键词提取规则】产出的英文逗号分隔字符串。例：眼镜店,optical shop,眼镜零售,eyewear store",
  "continent": "按【国家 vs 七大洲互斥规则】产出。仅在描述只提到大洲、未提到任何国家时才填；提到国家则必须为 \"\"。例：亚洲",
  "country": "明确提及的国家，多个用英文逗号分隔。例：中国,英国",
  "countryCodeList": "对应国家的 ISO 3166-1 alpha-2 代码，顺序与 country 一一对应，多个用英文逗号分隔。例：CN,GB",
  "addressObjList": "按【地址提取规则】产出的字符串：单个地址内用 `,` 拼接层级，多个不同地址用 `;` 分隔；非中国地址保留英文原文不拆层级；无地址时为 \"\"。例：浙江,宁波;London, UK",
  "employeeNumberRangeStart": "按【数值区间通用规则】仅在描述明确包含 '员工X人以上/以下/左右/到/至' 时提取最小值；否则为 \"\"。",
  "employeeNumberRangeEnd": "按【数值区间通用规则】仅在描述明确包含 '员工X人以上/以下/左右/到/至' 时提取最大值；否则为 \"\"。",
  "storeNumberRangeStart": "按【数值区间通用规则】仅在描述明确包含 '门店X家以上/以下/左右/到/至' 或 'X家门店以上/以下/左右' 时提取最小值；否则为 \"\"。'找X家门店' 不属于此字段。",
  "storeNumberRangeEnd": "按【数值区间通用规则】仅在描述明确包含 '门店X家以上/以下/左右/到/至' 或 'X家门店以上/以下/左右' 时提取最大值；否则为 \"\"。'找X家门店' 不属于此字段。",
  "industryList": "按【行业推断规则】产出，多个用英文逗号分隔。例：服装,数码,家居"
}
```

> 📌 **`addressObjList` 字段升级说明**：本版本约定多个地址使用英文分号 `;` 分隔多组，组内用英文逗号 `,` 分级。下游 AiWa 参数构建规则（见后文「AiWa 参数构建规则」中 `addressObjList` 一节）将该字符串先按 `;` 切多个原子地址，再对每个原子地址按"是否包含中文"决定 `type=1`（中文结构化）或 `type=0`（英文自由文本）；空字符串仍走占位对象。

---

### Step 3：构建并提交任务

> 🧷 **下任务参数总规约（最高优先级，所有员工通用）**
>
> 提交任务时 `collaborationSubmitTaskParam` 对象**有且仅有以下 5 个根级键**，键名、类型、取值规则严格如下：
>
> ```ts
> {
>   "taskName":        String,   // AI 总结出的任务名称（来自 Step 1 的 taskName，非空字符串）
>   "currentModule":   "content",// 字符串字面量，永远是 "content"（不分员工组合，无任何例外）
>   "executionMode":   Number,   // 永远写数字 1（当前阶段一律按定额任务下达；后端枚举：周期性=0、定额=1）
>   "employeeParams":  Object,   // 见下方规约
>   "taskDescription": String    // 用户最初下达的原始任务描述，原文透传，不要改写/精简/翻译
> }
> ```
>
> 同时与 `collaborationSubmitTaskParam` **同级**必须再带：
> - `completed`: `true`（布尔字面量）
> - `sourceSettings`: 见下方「员工组合 → sourceSettings 对照表」（含 Fran/Lisa 时为完整对象，否则为 `null`）
>
> **`employeeParams` 规约：**
> - 是一个对象，key 为参与员工的 PascalCase 名称（`AiWa` / `Frank` / `Fran` / `Lisa`），value 为该员工自己的参数对象。
> - **包含哪些员工**由 Step 1 解析出的 `taskDescription` + `employeeList` 共同决定：任务里识别出几个员工，`employeeParams` 就有几个对应的 key，**多一个、少一个、错一个都不允许**。
> - 例：任务里同时有 AiWa 和 Frank → `employeeParams: { "AiWa": {...}, "Frank": {...} }`，两个员工的参数都是各自独立的对象，不得混合到同一个对象里，也不得只挂一个员工的参数。
>
> **每个员工子对象内部参数清单（按员工查阅下文「{员工} 参数构建规则」与「{员工} 结构强约束」获取必填键、固定值、示例）：**
> - `AiWa`: `totalTarget` / `incrementalTarget` / `upperLimitTarget` / `keywordList` / `continent` / `country` / `countryCodeList` / `addressObjList` / `industryList`（外加可选范围字段 `employeeNumberRangeStart` / `employeeNumberRangeEnd` / `storeNumberRangeStart` / `storeNumberRangeEnd`，仅当 Step 2 提取到值时才放入）。
> - `Frank`: `incrementalTarget` / `upperLimitTarget` / `senderEmail` / `language` / `templateId` / `emailPlanList`（`emailPlanList` 元素含 `delayDay` / `emailSubject` / `emailText` / `loading`）。
> - `Fran`: `priority` / `scriptId` / `callingNumber` / `agentProfileId` / `minConcurrency` / `ringingDuration` / `incrementalTarget` / `upperLimitTarget`。
> - `Lisa`: `signName` / `templateCode` / `templateType` / `templateContent` / `incrementalTarget` / `upperLimitTarget` / `qualificationName` / `templateParamList`。
>
> **必须遵守的硬规则（违反任意一条，后端立即拒绝）：**
> 1. `currentModule` 永远等于字符串 `"content"`，禁止写 `"analysis"` / `"Content"` / `null` / 省略。
> 2. `executionMode` 永远等于数字 `1`，禁止写 `0` / `2` / `"1"` / `true` / `"定额任务"` / `"周期性任务"`。
> 3. `taskDescription` 透传用户原始指令文本，禁止改写为 AI 总结后的简短描述（那是 `taskName` 的活儿）。
> 4. `employeeParams` 子键必须是 PascalCase 原样（`AiWa` / `Frank` / `Fran` / `Lisa`），不得改成 `aiwa` / `aiwaParam` / `aiwaParams` 等任何变体。
> 5. Step 1/Step 2 的内部解析变量（`employeeList` / `language` / 根级 `totalTarget`）一律不得出现在最终请求体中——它们只能流到对应员工子对象内的指定字段。
>
> **下方各员工的"参数构建规则"、"结构强约束"、"请求体示例"是上述规约的展开细节，构建请求体时必须先按本规约确定整体形状，再按对应员工的小节填充值。**

**接口：** `POST https://ai.deepsop.com/prod-api/ai/presetEmployee/submitTask`

**请求头：**
```
Content-Type: application/json; charset=utf-8
x-api-key: $DEEPSOP_API_KEY
```

> ⚠️ **强制规则：** 请求体根级必须包含 `"completed": true`（布尔字面量）。**严禁省略、写成 `null`、`"true"` 字符串或 `false`**，否则后端会直接返回 500。该字段与 `collaborationSubmitTaskParam` 同级，不在其内部。

> 🔒 **强制使用 `submit_task.py` 提交，禁止直接 `curl`：**
>
> ```bash
> python3 scripts/submit_task.py <<'TASK_BODY_EOF'
> {
>   "completed": true,
>   "collaborationSubmitTaskParam": { ...完整请求体... }
> }
> TASK_BODY_EOF
> ```
>
> 原因：直接在 bash 命令行写 `curl -d '{"taskName":"家纺..."}'` 会触发 Windows ANSI 代码页（cp936）与 UTF-8 之间的转码歧义，导致 `taskName` / `taskDescription` 含中文时**间歇性提交为乱码**。`submit_task.py` 通过 stdin 字节流 + 显式 UTF-8 解码 + `Content-Type: application/json; charset=utf-8` 显式声明，**彻底闭合编码链路**，并内置两层 pre-flight 校验（`validate_employee_params.py` + `validate_sms_template_params.py`），校验未过自动阻塞 HTTP 提交。
>
> 行为约束：
> - **必须**通过 heredoc（`<<'TASK_BODY_EOF'` ... `TASK_BODY_EOF`）把请求体喂给 stdin；**禁止**用 argv 传 JSON（如 `python3 submit_task.py "$(echo {...})"`），argv 仍受 shell 编码影响。
> - heredoc 定界符**必须用单引号包裹**（`'TASK_BODY_EOF'` 而不是 `TASK_BODY_EOF`），否则 bash 会做变量展开，破坏 JSON 中的 `$` 字符。
> - 若运行时不支持 heredoc（极少见），退路：用 `python3 -c` 把 body 写到 UTF-8 文件，再 `python3 scripts/submit_task.py --file /tmp/task_body.json`。
> - 脚本输出单行 JSON：`{ok, stage, status, summary, response, body_preview, errors?}`；退出码 `0`=成功、`1`=校验失败、`2`=网络失败、`3`=服务端非 2xx、`4`=输入格式错误。
> - 退出码 ≠ 0 时，**必须**把 `summary` + `errors`/`response` 原样回复给用户，不得直接重试或假装成功。

> ⛔ **字段名零改写规则（极高优先级，违反必返回 500）：**
> 后端通过精确字段名解析参数，**所有键名必须与本文档示例 JSON 中的拼写完全一致（大小写、连写、单复数都不能改）**。在生成请求体时：
>
> 1. **不得做大小写转换**：`scriptId` ≠ `scriptID` ≠ `ScriptId` ≠ `script_id`；`agentProfileId` ≠ `agentProfileID` ≠ `AgentProfileId`。
> 2. **不得做命名风格转换**：禁止把 camelCase 改成 snake_case 或 kebab-case。
>    - ❌ `template_param_list` / `template-param-list` → ✅ `templateParamList`
>    - ❌ `email_plan_list` → ✅ `emailPlanList`
>    - ❌ `country_code_list` → ✅ `countryCodeList`
>    - ❌ `address_obj_list` → ✅ `addressObjList`
>    - ❌ `industry_list` / `keyword_list` → ✅ `industryList` / `keywordList`
>    - ❌ `account_config_list` → ✅ `accountConfigList`
>    - ❌ `publish_templates` → ✅ `publishTemplates`
>    - ❌ `current_module` → ✅ `currentModule`
>    - ❌ `execution_mode` → ✅ `executionMode`
>    - ❌ `task_name` / `task_description` → ✅ `taskName` / `taskDescription`
>    - ❌ `source_settings` / `employee_params` → ✅ `sourceSettings` / `employeeParams`
>    - ❌ `total_target` / `incremental_target` / `upper_limit_target` → ✅ `totalTarget` / `incrementalTarget` / `upperLimitTarget`
>    - ❌ `sender_email` → ✅ `senderEmail`
>    - ❌ `calling_number` / `ringing_duration` / `min_concurrency` → ✅ `callingNumber` / `ringingDuration` / `minConcurrency`
>    - ❌ `template_code` / `template_content` / `template_type` / `sign_name` / `qualification_name` → ✅ `templateCode` / `templateContent` / `templateType` / `signName` / `qualificationName`
>    - ❌ `variable_label` / `variable_attribute` / `variable_value` → ✅ `variableLabel` / `variableAttribute` / `variableValue`
>    - ❌ `method_type` / `image_url_list` / `first_image_url` / `last_image_url` / `keep_original_sound` / `generate_audio` / `enhance_prompt` / `negative_prompt` / `prompt_extend` / `shot_type` / `duration_switch` / `person_generation` / `resize_mode` → 全部保持 camelCase
>    - ❌ `account_id` / `privacy_level` / `comment_disabled` / `duet_disabled` / `stitch_disabled` / `disable_comment` / `disable_duet` / `disable_stitch` / `is_public_account` / `brand_content_toggle` / `brand_organic_toggle` → 全部保持 camelCase
>    - ❌ `release_type` / `time_zone` / `interval_type` / `start_time` / `publish_count` / `publish_interval` → 全部保持 camelCase
>    - ❌ `delay_day` / `email_subject` / `email_text` → ✅ `delayDay` / `emailSubject` / `emailText`
>    - ❌ `country_id` / `address_id` / `file_list` / `update_support` / `seas_group_ids` / `group_id` / `stage_id` / `label_id` / `address_file_list` / `suppur_ids` → 全部保持 camelCase（`groupId` / `stageId` / `labelId` / `seasGroupIds` / `fileList` / `updateSupport` / `addressId` / `countryId` / `addressFileList` / `suppurIds`）。**注意：`suppurIds` 不是 `supplierIds` / `customerIds`，保持原拼写不得"修正"。**
>    - ❌ `staff_id` / `video_items` → ✅ `staffId` / `videoItems`
> 3. **不得做单复数改造**：复数字段必须保留 `List` / 复数后缀，单数字段不得加 `s`。
>    - `emailPlanList` 不得写成 `emailPlans` / `emailPlan`
>    - `callingNumber` 不得写成 `callingNumbers`
>    - `publishTemplates` 不得写成 `publishTemplate` / `publishTemplateList`
>    - `accountConfigList` 不得写成 `accountConfigs`
>    - `templateParamList` 不得写成 `templateParams`
> 4. **不得做语义改名**：禁止用同义词替换字段名。
>    - `agentProfileId` ≠ `agentId` / `chatbotId` / `profileId` / `botId`
>    - `senderEmail` ≠ `fromEmail` / `mailFrom` / `email`
>    - `callingNumber` ≠ `callerNumber` / `phone` / `outboundNumber`
>    - `templateCode` ≠ `smsTemplateCode` / `code`
>    - `signName` ≠ `signature` / `signatureName`（注意：模板列表返回的字段叫 `signatureName`，但**提交时的字段名必须是 `signName`**）
>    - `qualificationName` ≠ `qualification` / `qualifications`
>    - `taskName` / `taskDescription` ≠ `name` / `description` / `title`
> 5. **校验流程**：构建完请求体后，**必须把 JSON 字符串与本文档对应的示例 JSON 逐字段对位检查一遍**——示例里有的键，请求体必须有；示例里键名怎么拼，请求体就照样拼；任何一个键名拼错都视为构建失败，重新构建后再提交。
>
> 不允许"我觉得 snake_case 更规范所以转一下"或"复数加 s 更自然"这类自作主张。

**参数构建规则：**

**前置 A：Fran 号码池与场景库查询（当 employeeList 包含 Fran 时必须先执行）**

**0. 检查外呼实例可用性**

接口：`GET https://ai.deepsop.com/prod-api/ai/outBound/describeInstance`

请求头：`x-api-key: $DEEPSOP_API_KEY`

检查 `data.body.instance.maxConcurrentConversation`：
- 大于 0：继续执行步骤 1（查询号码池）
- 等于 0：**终止任务**，回复用户：
  > ⚠️ 当前外呼账号并发数为 0，无法提交电话销售任务，请联系管理员开通并发资源后再试。

**1. 查询号码池**

接口：`GET https://ai.deepsop.com/prod-api/ai/outBound/callerNumber/list`

请求头：`x-api-key: $DEEPSOP_API_KEY`

返回示例：
```json
{
  "total": 1,
  "rows": [
    {
      "id": 7,
      "callNumber": "30350903",
      "nickName": "Kocgo"
    }
  ],
  "code": 200,
  "msg": "查询成功"
}
```

处理规则：
- `rows` 为空（`total=0`）：**终止任务**，回复用户：
  > ⚠️ 当前账号下没有可用的外呼号码，无法提交电话销售任务，请联系管理员开通号码后再试。
- `rows` 只有 1 条：自动选用该 `callNumber`，无需用户确认。
- `rows` 有多条：列出所有号码供用户选择（支持多选），格式：
  ```
  检测到多个可用外呼号码，请选择本次任务要使用的号码（可多选，用逗号分隔序号）：
  1. {callNumber}（{nickName}）
  2. {callNumber}（{nickName}）
  ...
  ```
  **等待用户回复后**，解析出被选中的 `callNumber` 列表（数组形式），赋值给 `callingNumber`。未收到选择不得继续。

**2. 查询场景库**

> 🛑 **强制实时拉取规则（反幻觉硬约束，违反即视为 bug）：**
>
> 当 Fran 流程进入"号码池已选定 + 客户来源已确认（含 AiWa 协同 / xlsx / 公司搜索任一通道）"这一步，**必须**真实调用 `POST /ai/outBound/listScripts` 接口拿到当前账号下的场景库列表后，**用接口返回的真实 `scriptName / industry / scene / status` 渲染**给用户挑选。
>
> **绝对禁止**：
> - ❌ 不调接口、直接凭"上次记忆 / 训练语料 / 用户聊天里提过的关键词"编造一份候选场景列表（典型幻觉如：脑补出"家纺外贸开发场景 / 服装清仓促销场景"等并标记为 `PUBLISHED`）。
> - ❌ 在接口返回**全部非 PUBLISHED** 的情况下，自行把某条 `TO_BE_REVIEWED` / `REJECTED` / 草稿场景"美化"成 `PUBLISHED` 让用户选用 —— 即使 status 是 `TO_BE_REVIEWED`、`REVIEWING` 也**不得**当作可用项；用户若不想等审核中的场景，必须按"无可用场景"分支引导他走 [Step 1.7](#step-17电话场景创建审核子流程独立入口) **创建 + 审核 + 发布**完整流程，审核通过（变 `PUBLISHED`）后再继续下任务。
> - ❌ 把 Step 1.7 中刚拿到的 `scriptId` 用作"列表里的一项"伪装成接口返回。Step 1.7 出口走的是上文的"已选定场景"分支（直接复用 `scriptId / agentProfileId`，**跳过本步骤**），不要二次列表。
>
> 只有接口真的返回了 `status === "PUBLISHED"` 的条目，才允许进入下方"列出供用户选择"分支；否则一律走"无可用场景 → 引导创建/取消"分支。

接口：`POST https://ai.deepsop.com/prod-api/ai/outBound/listScripts`

请求头：
```
Content-Type: application/json
x-api-key: $DEEPSOP_API_KEY
```

请求体：
```json
{"pageNumber": 1, "pageSize": 20, "scriptName": ""}
```

返回结构（重点字段）：
- `data.body.scripts.list[]`：场景库列表
  - `scriptId`：场景库 ID
  - `scriptName`：场景库名称
  - `industry` / `scene`：行业 / 场景
  - `status`：状态，**必须为 `PUBLISHED` 才可用**
- `data.chatbotIdList[]`：与场景库配套的 chatbot id 列表，取第一个作为 `agentProfileId`

处理规则：
- `list` 为空，或过滤后无 `status === "PUBLISHED"` 的场景：**不再立即终止**。改为向用户提供「即时创建」与「自行去后台创建」两个选项，格式：
  ```
  ⚠️ 当前账号下没有可用（已发布）的场景库。可以二选一：
  1. 我现在引导您创建一个外呼场景（回复"创建"）— 含场景信息 + TTS 音色 + 机器人 prompt + 阿里云审核（约 1～5 分钟）
  2. 前往 https://ai.deepsop.com 自行创建并发布场景后重试（回复"取消"）
  ```
  - 用户回复"创建/我自己建/帮我建一个" → **暂存当前 Fran 流程上下文**，跳转到 [Step 1.7：电话场景创建/审核子流程](#step-17电话场景创建审核子流程独立入口)；待 Step 1.7 拿到 `scriptId / agentProfileId` 后**回到本步骤的"已选定场景"分支**，直接使用，**不再重查** `listScripts`。
  - 用户回复"取消/不创建" → 按原文案终止任务。
  - 用户多轮不明确回复（≥2 次） → 默认按"取消"终止任务，提示同上。
- 仅 1 条 `PUBLISHED` 场景：**不得自动选用**，必须列出并等待用户明确确认，格式：
  ```
  检测到以下可用场景库，请确认是否使用（回复「确认」即可）：
  1. {scriptName}（行业：{industry}，场景：{scene}）
  ```
  **等待用户明确回复「确认」后**，取对应 `scriptId`。未收到确认不得继续。
- 多条 `PUBLISHED` 场景：列出供用户**单选**，格式：
  ```
  请选择本次电话销售任务要使用的场景库（回复序号）：
  1. {scriptName}（行业：{industry}，场景：{scene}）
  2. ...
  ```
  **等待用户回复后**，取对应 `scriptId`。未收到选择不得继续。
- `agentProfileId` 统一取 `data.chatbotIdList[0]`（若为空数组则终止并提示联系管理员）。

**前置 B0：Frank 邮箱绑定检查（当 employeeList 包含 Frank 时必须先执行）**

接口：`GET https://ai.deepsop.com/prod-api/ai/emailconfig/list?pageSize=1000&pageNum=1&status=1`

请求头：`x-api-key: $DEEPSOP_API_KEY`

检查 `rows` 列表：
- `rows` 不为空（至少 1 条）：继续执行前置 B（获取用户 Profile）
- `rows` 为空（`total=0`）：**终止任务**，回复用户：
  > ⚠️ 当前账号未绑定可用邮箱，无法提交邮件销售任务，请先登录 https://ai.deepsop.com 前往「邮件配置」绑定邮箱后再试。

**前置 B：获取用户 Profile（当 employeeList 包含 Frank 时必须先执行）**

```bash
curl -s -H "x-api-key: $DEEPSOP_API_KEY" 'https://ai.deepsop.com/prod-api/ai/user/profile'
```

提取以下字段用于邮件署名：
- `nickName`：发件人姓名
- `position`：职位（可能为空，直接取 profile 中的 `position` 字段）
- `dept.deptName`：公司名称
- `phonenumber`：电话（注意字段名全小写）
- `email`：邮箱（作为 `senderEmail`）

**前置 C：AI 生成邮件内容（当 employeeList 包含 Frank 时必须先执行）**

根据用户指令和 profile 信息，用 LLM 生成邮件主题和正文，严格返回 JSON 数组：

```
生成对应语言【{language}】的内容，请直接输出纯净的JSON数组，不包含任何额外文本、代码标记、说明或包装。
输出示例：[{"emailSubject": "邮件主题", "emailText": "邮件内容"}]

邮件生成规则：
1. 开头：使用标准问候语（中文："尊敬的先生/女士："）
2. 正文：根据【{taskDescription}】生成开发信，必须至少包含以下一项：
   - 产品关键词：从 taskDescription 中提取
   - 价值主张：包含「功能+场景+风格」三要素（如：【防风防水】男士户外工装夹克 春秋季通勤休闲外套）
   - 痛点：具体描述需求未被满足的场景
   - 解决方案：突出技术/设计优势与使用场景
   - 行动呼吁：包含「稀缺性+权益+行动指令」（如：区域独家授权：仅开放3个地区代理名额！签约即享首单5%折扣→ 立即WhatsApp发送需求）
   - 证明点：包含「原始痛点+解决方案+量化结果」的客户案例
   - 服务吸引物：分点列出，覆盖供应链/物流/市场支持/售后/定制化5大类
3. 结尾：自然添加对应语言祝福语
4. 署名（每项另起一行，共4行）：
   {nickName}（{position}）
   {companyName}（若 nickName 与 companyName 相同则省略此行）
   {phoneNumber}
   {email}
5. 风格：专业、直接、有帮助且富有亲和力；避免使用「免费」「优惠」「限时」等推销词汇
6. 主题：简洁引人入胜，避免垃圾邮件词汇
7. 禁止出现 [Name] 等变量占位符
```

生成结果提取 `emailSubject` 和 `emailText` 用于 Frank 参数。

**前置 D：Lisa 短信模板查询与变量填写（当 employeeList 包含 Lisa 时必须先执行）**

**1. 查询短信模板列表**

接口：`GET https://ai.deepsop.com/prod-api/ai/sms/querySmsTemplateList?pageNum=1&pageSize=20&pageNumber=1`

请求头：`x-api-key: $DEEPSOP_API_KEY`

关键字段：
- `data.smsTemplateList[]`：模板列表
  - `auditStatus`：必须为 `AUDIT_STATE_PASS` 才可用
  - `templateCode`：模板编码
  - `templateName`：模板名称
  - `templateContent`：模板内容（含 `${xxx}` 占位符）
  - `signatureName`：签名名称
  - `templateType`：模板类型（0=通知, 1=推广, 2=验证码）
  - `outerTemplateType`：提交时使用的模板类型参数

处理规则：
- 过滤后无 `auditStatus === "AUDIT_STATE_PASS"` 的模板：**终止任务**，回复用户：
  > ⚠️ 当前账号下没有已审核通过的短信模板，请先登录 https://ai.deepsop.com 创建并审核通过短信模板（状态需为 `AUDIT_STATE_PASS`）后再试。
- 仅 1 条 `AUDIT_STATE_PASS` 模板：**不得自动选用**，必须列出并等待用户明确确认，格式：
  ```
  检测到以下可用短信模板，请确认是否使用（回复「确认」即可）：
  1. {templateName}（类型：{templateType中文}）
     内容：{templateContent}
  ```
  **等待用户明确回复「确认」后**，取该模板。未收到确认不得继续。
- 多条 `AUDIT_STATE_PASS` 模板：列出供用户**单选**，格式：
  ```
  请选择本次短信销售要使用的模板（回复序号）：
  1. {templateName}（类型：{templateType中文}）
     内容：{templateContent}
  2. ...
  ```

**2. 模板变量填写**

选定模板后，解析 `templateContent` 中的 `${xxx}` 占位符，就每个变量告知用户并求其填写。如模板无变量，跳过此步。

根据 `templateType` 匹配对应变量规则集并告知用户填写要求：

| templateType | 模板类型 | 应用变量规则集 |
|---|---|---|
| 2 | 验证码短信 | verify（验证码类规则） |
| 0 | 通知短信 | notify（通知类规则） |
| 1 | 推广短信 | market（推广类规则） |

**主要变量类型与校验规则：**

| 变量类型名 | code | 适用范围 | 校验规则 |
|---|---|---|---|
| 仅数字（验证码） | numberCaptcha | verify | 纯数字4–6位 |
| 数字+字母组合或仅字母 | characterWithNumber2 | verify | 长度4–6位 |
| 验证码时间（1–2位数字） | verifyTime | verify | 1–99的整数 |
| 时间/日期 | time | notify/market | YYYY-MM-DD、hh:mm、上午/下午等标准时间格式 |
| 金额/数量 | money | notify/market | 纯数字或小数，不含单位符号 |
| 用户昵称 | user_nick | notify/market | 不超过20个字符，不含表情/QQ/微信号 |
| 个人姓名 | name | notify/market | 2–5个简体中文 |
| 企业/组织名称 | unit_name | notify | 仅中文，不超过20字符 |
| 地址 | address | notify | 不超过30字符，不含 QQ/微信号 |
| 车牌号 | license_plate_number | notify | 省份简称+字母+数字组合，不超过10字符 |
| 快递单号 | tracking_number | notify | 8–16位数字，或字母开头+数字字母 |
| 取件码 | pick_up_code | notify | 4–8位数字/短横线/下划线 |
| 其他号码 | other_number2 | notify | 不超过35字符字母数字组合 |
| 电话号码 | phone_number2 | notify | 3–12位纯数字，每模板最多2个号码变量 |
| 链接参数 | link_param | notify/market | 1–8位英文数字，不含完整链接/IP |
| 邮筱地址 | email_address | notify | 7–30字符，包含@ |
| 其他 | others | notify/market | 不超过35字符，不含 QQ/微信/手机/网址 |

**变量匹配逻辑：**
1. 根据变量名（如 `conference`、`address`、`time`）在对应规则集中按变量类型名称匹配：
   - `time`/`date`/`day`/`year`/`month` 类 → `time`
   - `money`/`price`/`amount` 类 → `money`
   - `phone`/`tel`/`mobile` 类 → `phone_number2`
   - `address`/`addr`/`location` 类 → `address`
   - `name`/姓名类 → `name`
   - `user_nick`/昵称类 → `user_nick`
   - `conference`/`unit`/组织类 → `unit_name`
   - 其他 → `others`
2. 求用户为每个变量填写具体值。**必须**同时给出"✅ 正确示例"和"❌ 错误示例"，让用户一眼看到雷区。格式：
   > 模板内容为：「{templateContent}」
   > 包含以下变量需要填写（请严格按格式，否则短信会全部发送失败）：
   > - `${conference}`：企业/组织名称（仅中文，不超过20字符）
   >   - ✅ 例：`库阔数字科技`
   >   - ❌ 例：`Kocgo Tech`（含英文）、`库阔数字科技股份有限公司（杭州）`（超长）
   > - `${address}`：地址（不超过30字符）
   >   - ✅ 例：`杭州萧山万豪酒店三楼`
   >   - ❌ 例：`https://maps.example.com/...`（含网址）
   > - `${time}`：时间（仅允许 `YYYY-MM-DD`、`hh:mm`、`上午/下午X点` 等标准格式）
   >   - ✅ 例：`2026-05-15 14:00`、`5月15日 下午2点`
   >   - ❌ 例：`2026年5月15日 14:00`（含中文"年月日"会被运营商网关拒绝）
   > 请为每个变量填写具体内容。
3. 🔒 **强制变量校验（pre-flight gate，违反任意一条都不得继续）：**

   ✅ **首选方式：调用本 SKILL 自带的校验脚本**（代码级校验，结果机器可读，比 LLM 自查可靠）：

   ```bash
   python3 scripts/validate_sms_template_params.py '<templateParamList JSON 字符串>'
   ```

   - 入参：和最终请求体里的 `templateParamList` 同形状的 JSON 数组（仅含 `variableLabel` / `variableAttribute` / `variableValue` 三键）。
   - stdout 输出单行 JSON：`{ok, summary, results: [{label, attribute, value, status, reason, suggestion?}]}`。
   - 退出码：`0` 全 PASS、`1` 至少一项 FAIL、`2` 输入格式错误。
   - 行为约束：
     - 退出码 ≠ 0 时，**禁止**继续；必须把 `results` 中每条 FAIL 的 `reason` + `suggestion` 原样回复给用户，要求其重新填写后再次构建 `templateParamList` 并**重新调用本脚本**。
     - 退出码 = 0 时才进入第 4 步。
     - **不得**自己规整后跳过脚本（例如把 `2026年5月15日` 改成 `2026-05-15` 然后直接提交），必须让用户确认修改后的值再走一次校验。

   ⚠️ **退路：脚本调用失败时（极少见，例如 python3 不可用）**，按下列规则人工逐个变量校验，规则与脚本完全一致：

   a. 按变量的 `variableAttribute`（即上一步匹配到的 `code`）查上方"主要变量类型与校验规则"表，取出"校验规则"列。
   b. 用规则对值做逐字符校验，**必须**判定是 PASS 还是 FAIL。不得"差不多就算过"，不得"用户写得清楚就提交"。
   c. **任意一个变量 FAIL** → 立即向用户回复不合规的变量、违反的具体规则、合法示例，并要求重新填写。**不得**：
      - 调用提交任务接口（`agentSubmitTask`）
      - 自己擅自规整格式（如把 `2026年5月15日` 改写成 `2026-05-15` 后偷偷提交——必须让用户确认）
      - 把"用户写得很明确"作为跳过校验的理由
   d. **全部 PASS** 才能进入第 4 步构建 `templateParamList` 并继续后续提交流程。

   **🚨 高频错误案例（已发生过真实事故，每次提交前必须自查）：**

   | 变量类型 | 用户实际填写 | AI 错误处理 | 后果 | 正确处理 |
   |---|---|---|---|---|
   | `time` | `2026年5月15日 14:00` | 直接提交 | 短信网关拒绝，13 条全部失败 | 提醒用户改成 `2026-05-15 14:00` 后再提交 |
   | `unit_name` | `Kocgo Tech` | 直接提交 | 模板审核为"仅中文"被拒 | 提醒用户改成中文名称 |
   | `phone_number2` | `+86 138-1234-5678` | 直接提交 | 含非数字字符被拒 | 提醒用户改成 `13812345678` |

4. 校验通过后，构建 `templateParamList`：
   ```json
   [
     {"variableLabel": "conference", "variableAttribute": "unit_name", "variableValue": "用户填写的值"},
     {"variableLabel": "address",    "variableAttribute": "address",   "variableValue": "用户填写的值"},
     {"variableLabel": "time",       "variableAttribute": "time",      "variableValue": "用户填写的值"}
   ]
   ```
   其中 `variableLabel` = 占位符名（不含 `${}`），`variableAttribute` = 匹配到的 code。

**AiWa 参数构建规则：**
- `totalTarget`：定额模式下填 Step 1 的 totalTarget，周期模式下为 null
- `incrementalTarget`：必填，固定填 5000（不可为 null）
- `upperLimitTarget`：固定填 5000
- `keywordList`：Step 2 的 keywordList **必须用 `.split(",")` 拆分成数组**（绝不可保留为逗号字符串）
- `continent`：Step 2 的 continent，**无则填 `null`，不得填 `""`**
- `country`：Step 2 的 country，**无则填 `null`，不得填 `""`**
- `countryCodeList`：Step 2 的 countryCodeList **必须用 `.split(",")` 拆分成数组**，无则填 `[]`（**不得填 `""` 或 `null`**）
- `addressObjList`：根据 Step 2 的 `addressObjList` 字符串构建数组。**先按英文分号 `;` 切成多个原子地址**，再对每个原子地址按下面规则各自构造一个对象：
  - **情况 1（整体为空字符串 `""`）**：Step 2 未识别到任何地址。必须填占位 `[{"type":1,"province":"","city":"","county":"","address":""}]`，**不得填 `[]`**。
  - **情况 2（原子地址包含中文）**：判定为中文结构化地址，按英文逗号 `,` 切分得到层级数组（最多三段：省/市/县），不足三段后续位补 `""`。填 `type=1`、`address=""`：
    - `"浙江,宁波"` → `{"type":1,"province":"浙江","city":"宁波","county":"","address":""}`
    - `"浙江,宁波,鄞州区"` → `{"type":1,"province":"浙江","city":"宁波","county":"鄞州区","address":""}`
    - `"上海"` → `{"type":1,"province":"上海","city":"","county":"","address":""}`
  - **情况 3（原子地址不含中文 / 为英文自由文本）**：填 `type=0`、`province/city/county=""`、`address` 放原子原文：
    - `"London, UK"` → `{"type":0,"province":"","city":"","county":"","address":"London, UK"}`
  - **多个原子地址**：按 `;` 切完后，每个原子单独走情况 2 或情况 3，最终多对象并列在数组里：
    - `"浙江,宁波;London, UK"` → `[{"type":1,"province":"浙江","city":"宁波","county":"","address":""},{"type":0,"province":"","city":"","county":"","address":"London, UK"}]`
  - **`type` 取值语义**：`1` = 中文结构化拆分地址（仅填 `province/city/county`）；`0` = 自由文本地址（仅填 `address`）。**禁止两者同时填**（`type=1` 时 `address` 必须为 `""`；`type=0` 时 `province/city/county` 必须全为 `""`），违反 `validate_employee_params.py` 会以 `TYPE_ADDRESS_CONFLICT` 拦截。
- `industryList`：Step 2 的 industryList **必须用 `.split(",")` 拆分成数组**

> ⛔ **AiWa 结构强约束（违反必返回 500 / 后端识别不到参数）：**
>
> 1. AiWa 子对象的 key 是 **`AiWa`**（**P**ascal**C**ase 三个字母原样），不是 `aiwa` / `Aiwa` / `aiWa` / `aiwaParam` / `aiWaParams`。
> 2. AiWa 子对象**必须**嵌在 `collaborationSubmitTaskParam.employeeParams.AiWa` 之下，**绝对禁止**直接挂到 `collaborationSubmitTaskParam.aiwaParam` / `collaborationSubmitTaskParam.AiWa` 这种少一层的位置。
> 3. **以下来自 Step 1/Step 2 的"内部解析变量"是给本 SKILL 内部流程用的，绝不允许出现在最终请求体的任何层级**：
>    - `employeeList`（Step 1 用来分发员工，请求体只关心 `employeeParams` 里的子键）
>    - `language`（仅在 `employeeParams.Frank` 子对象内部使用，禁止挂到根级或 AiWa 子对象内）
>    - `totalTarget`（**只能**作为 `employeeParams.AiWa.totalTarget`，**不得**挂到 `collaborationSubmitTaskParam` 根级）
> 4. AiWa 必填的 9 个键：`totalTarget` / `incrementalTarget` / `upperLimitTarget` / `keywordList` / `continent` / `country` / `countryCodeList` / `addressObjList` / `industryList`，**一个都不能漏**。
> 5. `currentModule` 必须在 `collaborationSubmitTaskParam` 内，**值固定为 `"content"`**（任何员工组合下都不得写 `"analysis"`）。

**AiWa 任务请求体示例（仅 AiWa 单独执行 — 直接对照拷贝，不要自由发挥）：**

```json
{
  "collaborationSubmitTaskParam": {
    "taskName": "家纺客户挖掘",
    "taskDescription": "帮我找10个做家纺的客户",
    "executionMode": 1,
    "employeeParams": {
      "AiWa": {
        "totalTarget": 10,
        "incrementalTarget": 5000,
        "upperLimitTarget": 5000,
        "keywordList": ["家纺", "纺织", "床上用品", "毛巾", "窗帘", "home textile", "bedding"],
        "continent": null,
        "country": null,
        "countryCodeList": [],
        "addressObjList": [{"type": 1, "province": "", "city": "", "county": "", "address": ""}],
        "industryList": ["家纺", "纺织"]
      }
    },
    "sourceSettings": null,
    "currentModule": "content"
  },
  "completed": true
}
```

> 🚫 **错误示例（曾经真实出现过的错传，禁止再生成此种结构）：**
>
> ```json
> {
>   "completed": true,
>   "collaborationSubmitTaskParam": {
>     "taskName": "家纺客户挖掘",
>     "executionMode": 1,
>     "totalTarget": 10,                       // ❌ 不应在根级
>     "employeeList": "AiWa",                  // ❌ Step 1 内部变量，不应出现
>     "language": "中文",                       // ❌ Step 1 内部变量，不应出现
>     "aiwaParam": {                           // ❌ 应是 employeeParams.AiWa
>       "keywordList": "家纺,纺织,床上用品,毛巾,窗帘",  // ❌ 应是数组
>       "industryList": "家纺,纺织",              // ❌ 应是数组
>       "continent": "",                         // ❌ 应是 null
>       "country": "",                           // ❌ 应是 null
>       "countryCodeList": "",                   // ❌ 应是 []
>       "addressObjList": []                     // ❌ 必须放占位对象
>     }
>     // ❌ 缺 employeeParams 包装层
>     // ❌ 缺 incrementalTarget / upperLimitTarget
>     // ❌ 缺 currentModule / sourceSettings
>   }
> }
> ```
>
> 上面这个错例犯了 7 项错误，**任何一项都会让后端识别不到参数**。生成请求体前请把上面的"正确示例"拷过来再替换具体值，不要从头自由编写。

**Frank 参数构建规则：**
- `incrementalTarget`：固定填 1000
- `upperLimitTarget`：固定填 1000
- `senderEmail`：来自 profile 的 `email`
- `language`：来自 Step 1 的 `language`（`"中文"` 或 `"英文"`）
- `templateId`：固定为 null
- `emailPlanList`：包含一个对象，字段：
  - `delayDay`：0
  - `emailSubject`：AI 生成的邮件主题
  - `emailText`：AI 生成的邮件正文（HTML 格式）
  - `loading`：0

> ⛔ **Frank 结构强约束：**
> 1. 子对象 key 必须是 **`Frank`**（首字母大写），不是 `frank` / `FRANK` / `frankParam` / `frankParams`。
> 2. 必须嵌在 `collaborationSubmitTaskParam.employeeParams.Frank` 之下。
> 3. `language` **只能**作为 `employeeParams.Frank.language`，**不得**挂到根级或其他员工子对象。
> 4. `emailPlanList` 必须是**长度为 1 的数组**，元素是对象，且对象内 4 个键 `delayDay` / `emailSubject` / `emailText` / `loading` 一个都不能漏。**不得**写成 `emailPlan`（单数）或 `emailPlans`（错误复数）或直接把对象本身赋给 `emailPlanList`（少一层数组）。
> 5. `senderEmail` 必须是字符串，不得写成对象 `{email: "..."}`，也不得改名为 `email` / `fromEmail` / `mailFrom`。
> 6. 必填 6 个键：`incrementalTarget` / `upperLimitTarget` / `senderEmail` / `language` / `templateId` / `emailPlanList`，一个都不能漏。

**Fran 参数构建规则：**
- `ringingDuration`：固定填 25
- `incrementalTarget`：固定填 1000
- `upperLimitTarget`：固定填 1000
- `minConcurrency`：固定填 1
- `priority`：固定填 `"Daily"`
- `callingNumber`：前置 A 第 1 步用户选定的号码**数组**（如 `["30350903"]`），**单号码也必须是数组形式**
- `scriptId`：前置 A 第 2 步用户选定的场景库 `scriptId`
- `agentProfileId`：前置 A 第 2 步 `data.chatbotIdList[0]`

> ⛔ **Fran 结构强约束：**
> 1. 子对象 key 必须是 **`Fran`**（首字母大写、4 个字母原样），不是 `fran` / `FRAN` / `franParam` / `franParams`。
> 2. 必须嵌在 `collaborationSubmitTaskParam.employeeParams.Fran` 之下。
> 3. `callingNumber` **必须是数组**（`["30350903"]`），即使只有一个号码也不得写成裸字符串 `"30350903"`，也不得改名为 `callingNumbers` / `callerNumber` / `phone` / `outboundNumber`。
> 4. `scriptId` 与 `agentProfileId` 必须是 **接口返回的字符串原值**（保留原始大小写如 `"chatbot-cn-RYRmV3jjzb"`），不得自行拼接、改名、加引号包裹两次。`agentProfileId` ≠ `agentId` / `chatbotId` / `profileId`。
> 5. `priority` 是字符串 `"Daily"`（**首字母大写**），不是 `"daily"` / `"DAILY"` / 整数。
> 6. 必填 8 个键：`ringingDuration` / `incrementalTarget` / `upperLimitTarget` / `minConcurrency` / `priority` / `callingNumber` / `scriptId` / `agentProfileId`，一个都不能漏。

**Fran 任务请求体示例（AiWa + Fran 联合任务）：**
```json
{
  "collaborationSubmitTaskParam": {
    "taskName": "启动财务课程电话销售",
    "taskDescription": "帮我找客户并启动电话销售",
    "executionMode": 1,
    "employeeParams": {
      "AiWa": { "...": "同上" },
      "Fran": {
        "ringingDuration": 25,
        "incrementalTarget": 1000,
        "upperLimitTarget": 1000,
        "callingNumber": ["30350903"],
        "minConcurrency": 1,
        "priority": "Daily",
        "scriptId": "c92d016f-03c8-47a3-95d9-61d75e192181",
        "agentProfileId": "chatbot-cn-RYRmV3jjzb"
      }
    },
    "sourceSettings": {
      "groupId": [], "stageId": [], "labelId": [], "level": [],
      "seasGroupIds": [], "addressId": [], "fileList": [],
      "updateSupport": 1, "cascader": null, "aiMining": null,
      "customerMining": null, "seasMining": null, "uploadMining": null,
      "countryId": null, "addressMining": null
    },
    "currentModule": "content"
  },
  "completed": true
}
```

> ⚠️ 当 `employeeList` **同时包含 `AiWa` 与 `Fran`/`Lisa`** 时，`sourceSettings` 必须按上述完整对象填充（不能为 `null`），且 `currentModule` 固定为 `"content"`。
>
> ⚠️ 若 `employeeList` 含 `Fran`/`Lisa` 但**不含 `AiWa`**，`sourceSettings` 改用 Step 1.6 产出的客户来源对象（结构是 `groupId / stageId / labelId / level / seasGroupIds / addressId / fileList / updateSupport / addressFileList / suppurIds`），**不要**沿用上面这份带 `cascader / aiMining / customerMining / seasMining / uploadMining / countryId / addressMining` 的旧版结构。

**Lisa 参数构建规则：**
- `incrementalTarget`：固定填 100
- `upperLimitTarget`：固定填 100
- `signName`：选定模板的 `signatureName`（**接口返回字段叫 `signatureName`，但请求体提交时必须叫 `signName`，自行改名**）
- `qualificationName`：同 `signName`（如两者不同由用户确认）
- `templateCode`：选定模板的 `templateCode`
- `templateContent`：选定模板的 `templateContent`
- `templateType`：选定模板的 `outerTemplateType`（注意：值取自模板对象的 `outerTemplateType` 字段，但请求体的键名仍叫 `templateType`）
- `templateParamList`：前置 D 第 2 步构建的变量数组（无变量则为 `[]`）

> ⛔ **Lisa 结构强约束：**
> 1. 子对象 key 必须是 **`Lisa`**（首字母大写、4 个字母原样），不是 `lisa` / `LISA` / `lisaParam` / `lisaParams`。
> 2. 必须嵌在 `collaborationSubmitTaskParam.employeeParams.Lisa` 之下。
> 3. `templateParamList` **必须是数组**，每个元素是含 **`variableLabel` / `variableAttribute` / `variableValue`** 三个键的对象。**禁止**改成键值映射形式（如 `{conference: "库阔科技", address: "杭州"}`）；**禁止**漏 `variableAttribute`（即使值与 `variableLabel` 同名也必须显式写出）。无变量时填 `[]`，**不要省略此键**。
> 4. `signName` ≠ `signatureName`（提交字段名）；`signName` 不得改名为 `signature` / `sign`。
> 5. `templateCode` 必须保留接口返回的原值（如 `"SMS_500460013"`），不得改名为 `code` / `smsTemplateCode`。
> 6. `templateType` 是数字（取自 `outerTemplateType`），不是字符串。
> 7. 必填 8 个键：`incrementalTarget` / `upperLimitTarget` / `signName` / `qualificationName` / `templateCode` / `templateContent` / `templateType` / `templateParamList`，一个都不能漏。

**Lisa 任务请求体示例（AiWa + Lisa 联合任务）：**
```json
{
  "collaborationSubmitTaskParam": {
    "taskName": "双十一老客户短信推广",
    "taskDescription": "帮我找客户并给老客户发短信",
    "executionMode": 1,
    "employeeParams": {
      "AiWa": { "...": "同上" },
      "Lisa": {
        "incrementalTarget": 100,
        "upperLimitTarget": 100,
        "qualificationName": "杭州库阔数字科技",
        "signName": "杭州库阔数字科技",
        "templateCode": "SMS_500460013",
        "templateParamList": [
          {"variableLabel": "conference", "variableAttribute": "unit_name", "variableValue": "库阔科技"},
          {"variableLabel": "address",    "variableAttribute": "address",   "variableValue": "杭州"},
          {"variableLabel": "time",       "variableAttribute": "time",      "variableValue": "2026-04-20"}
        ],
        "templateType": 1,
        "templateContent": "温馨提醒：${conference}会议将在${address}地点，于${time}时间开始，请您准时参加。"
      }
    },
    "sourceSettings": {
      "groupId": [], "stageId": [], "labelId": [], "level": [],
      "seasGroupIds": [], "addressId": [], "fileList": [],
      "updateSupport": 1
    },
    "currentModule": "content"
  },
  "completed": true
}
```

---

**📋 员工组合 → `currentModule` / `sourceSettings` 对照表**

构建请求体前，按本次任务实际包含的员工组合从下表查 `currentModule` 与 `sourceSettings` 的取值，**严禁自行推断**：

> 🔒 **`currentModule` 全局固定为 `"content"`**：无论员工组合是哪种、是否含销售员工，`currentModule` 字段都是字符串字面量 `"content"`，**不得**写成 `"analysis"` / `"Content"` / `"CONTENT"` / `null` / 省略。

| 员工组合 | `currentModule` | `sourceSettings` | 备注 |
|---|---|---|---|
| 仅 AiWa | `"content"` | `null` | 单纯客户挖掘 |
| AiWa + Frank | `"content"` | `null` | 挖客户 + 邮件销售 |
| AiWa + Fran | `"content"` | 完整 sourceSettings 对象（见 Fran 示例） | 挖客户 + 电话销售 |
| AiWa + Lisa | `"content"` | 完整 sourceSettings 对象（见 Lisa 示例） | 挖客户 + 短信销售 |
| AiWa + Frank + Fran | `"content"` | 完整 sourceSettings 对象 | 多通道销售 |
| AiWa + Frank + Lisa | `"content"` | 完整 sourceSettings 对象 | 多通道销售 |
| AiWa + Fran + Lisa | `"content"` | 完整 sourceSettings 对象 | 多通道销售 |
| AiWa + Frank + Fran + Lisa | `"content"` | 完整 sourceSettings 对象 | 全通道销售 |
| 仅 Frank（无 AiWa） | `"content"` | Step 1.6 产出的客户来源对象 | 仅邮件销售，客户来源由用户指定 |
| 仅 Fran（无 AiWa） | `"content"` | Step 1.6 产出的客户来源对象 | 仅电话销售，客户来源由用户指定 |
| 仅 Lisa（无 AiWa） | `"content"` | Step 1.6 产出的客户来源对象 | 仅短信销售，客户来源由用户指定 |
| Frank/Fran/Lisa 任意组合（无 AiWa） | `"content"` | Step 1.6 产出的客户来源对象 | 多通道销售但无 AiWa 协同 |

> 🔍 **快速判定规则**：
> - `currentModule` 始终为 `"content"`（无任何例外分支）。
> - **含 AiWa**：含 `Fran` 或 `Lisa` → `sourceSettings` 为完整对象（含 `cascader` / `aiMining` 等键，见 Fran/Lisa 示例）；其他子组合 → `sourceSettings` 为 `null`。
> - **不含 AiWa 且含 `Frank`/`Fran`/`Lisa` 任一**：`sourceSettings` **必须**为 Step 1.6 产出的客户来源对象（含 `fileList` / `addressFileList` / `suppurIds` 等键，**不要**带 `cascader` / `aiMining` 等 AiWa 联合场景的旧键），且 `fileList` / `addressFileList` / `suppurIds` 三者至少一个非空。
> - **既不含 AiWa 也不含 `Frank`/`Fran`/`Lisa`**：`sourceSettings` 为 `null`。

> 🚫 **组合场景常见错例：**
>
> 1. 仅 AiWa 任务把 `currentModule` 写成 `"analysis"`：错。**任何组合**都必须 `"content"`。
> 2. AiWa+Fran 联合任务把 `sourceSettings` 写成 `null`：错。含 Fran 必须填完整对象。
> 4. 多员工组合时把不同员工塞进同一个员工 key（如 `employeeParams.AiWaFrank: {...}`）：错。每个员工是 `employeeParams` 下独立的同级 key。
> 5. 多员工组合时漏掉某个员工的子对象（仅在 `employeeList` 字符串里出现，但 `employeeParams` 里没有对应键）：错。`employeeList` 里写了的员工，`employeeParams` 必须有对应子对象。

---

**⚠️ 提交前必须执行参数完整性校验（缺少任意一项禁止提交）**

> 🔒 **第 0 步（前置硬闸）：字段名逐键对位检查**
> 把刚构建好的 `body` JSON 字符串和本文件对应员工的示例 JSON 并排放置，**逐键比对拼写**：
> 1. 示例里出现的每一个键名（含 `taskName`、`taskDescription`、`executionMode`、`employeeParams`、`sourceSettings`、`currentModule`、`completed`，以及各员工子对象内部的全部 key），在 body 中必须**原样存在**，不得改写大小写、不得改 snake_case、不得改单复数、不得换同义词。
> 2. 任何键名只要与示例不一致（哪怕只差一个字母大小写），立即停止提交，回头修正后再走本清单。
> 3. 这一步在所有员工字段值校验之前完成，因为字段名错了，值再对也没用。

根据本次任务包含的员工，逐项对照以下清单检查构建好的请求体，确认每个字段都存在且有合法值：

**根结构（必须）：**
- `collaborationSubmitTaskParam.taskName`：非空字符串
- `collaborationSubmitTaskParam.taskDescription`：非空字符串
- `collaborationSubmitTaskParam.executionMode`：**当前阶段一律硬编码为数字 `1`**（即使 Step 1 识别为周期性任务也写 1；不得写 `0` / `2` / `"1"` / `"定额任务"`）
- `collaborationSubmitTaskParam.employeeParams`：对象，包含至少一个员工
- `collaborationSubmitTaskParam.sourceSettings`：取值严格按上文「员工组合 → `currentModule` / `sourceSettings` 对照表」填（**不要在这里推断**）。快速规则：含 `Fran` 或 `Lisa` → 完整对象；不含 `Fran` 也不含 `Lisa` → `null`
- `collaborationSubmitTaskParam.currentModule`：**全局固定为字符串 `"content"`**，无任何例外（不得写 `"analysis"` / `"Content"` / `null`）
- `completed`：**必传**，布尔字面量 `true`，与 `collaborationSubmitTaskParam` 同级；不得为 `null`、缺省、字符串 `"true"` 或 `false`，否则接口返回 500

**AiWa（当 employeeList 包含 AiWa 时）：**
- `totalTarget`：用户指定的目标数量（正整数）
- `incrementalTarget`：`5000`
- `upperLimitTarget`：`5000`
- `keywordList`：非空数组
- `continent`：字符串或 `null`
- `country`：字符串或 `null`
- `countryCodeList`：数组（可为空数组 `[]`）
- `addressObjList`：包含至少一个对象，每个对象含 `type`/`province`/`city`/`county`/`address` 五个字段
- `industryList`：非空数组

**Frank（当 employeeList 包含 Frank 时）：**
- `incrementalTarget`：`1000`
- `upperLimitTarget`：`1000`
- `senderEmail`：来自 profile 的 email，非空字符串
- `language`：`"中文"` 或 `"英文"`
- `templateId`：`null`
- `emailPlanList`：包含一个对象，该对象必须含以下四个字段：
  - `delayDay`：`0`
  - `emailSubject`：AI 生成的主题，非空字符串
  - `emailText`：AI 生成的正文 HTML，非空字符串
  - `loading`：`0`

**Fran（当 employeeList 包含 Fran 时）：**
- `ringingDuration`：`25`
- `incrementalTarget`：`1000`
- `upperLimitTarget`：`1000`
- `minConcurrency`：`1`
- `priority`：`"Daily"`
- `callingNumber`：非空数组，来自号码池选择
- `scriptId`：非空字符串，来自场景库选择
- `agentProfileId`：非空字符串，来自 `data.chatbotIdList[0]`

**Lisa（当 employeeList 包含 Lisa 时）：**
- `incrementalTarget`：`100`
- `upperLimitTarget`：`100`
- `signName`：非空字符串，来自模板 `signatureName`
- `qualificationName`：非空字符串，与 `signName` 相同
- `templateCode`：非空字符串，来自模板 `templateCode`
- `templateContent`：非空字符串，来自模板 `templateContent`
- `templateType`：数字，来自模板 `outerTemplateType`
- `templateParamList`：数组（无变量时为 `[]`，不可缺少此字段）

> ⚠️ **`sourceSettings` 与 `currentModule` 是根级字段，取值取决于本次任务的员工组合，请查阅上文「员工组合 → `currentModule` / `sourceSettings` 对照表」，请勿一律写成 `null`/`"analysis"`。**例如 `AiWa+Lisa` 时，`sourceSettings` 必须是完整对象、`currentModule` 为 `"content"`。

**发现任何字段缺失或值不合法时，停止提交，先补全后再执行提交。**

**🔒 强制提交：直接走 `scripts/submit_task.py`（一站式：校验 + UTF-8 安全 HTTP）**

`submit_task.py` 已串联以下三件事，**LLM 只需调一次**即可完成"校验 + 提交"，不需要再单独调 `validate_employee_params.py` 或 `validate_sms_template_params.py`：

1. 内部调用 `validate_employee_params.py`（结构 + 取值，覆盖 AiWa/Frank/Fran/Lisa 全员）
2. 含 Lisa 模板变量时，自动调用 `validate_sms_template_params.py` 做内容校验
3. 任一步校验失败立即退出（退出码 1），**不会**触发 HTTP 提交
4. 校验全过才以 `Content-Type: application/json; charset=utf-8` POST 到 `/ai/presetEmployee/submitTask`

```bash
python3 scripts/submit_task.py <<'TASK_BODY_EOF'
{
  "completed": true,
  "collaborationSubmitTaskParam": { ...完整请求体... }
}
TASK_BODY_EOF
```

**校验覆盖范围**（详见 `validate_employee_params.py` / `validate_sms_template_params.py` 源码）：
- Step 1/2 内部变量（`employeeList` / `language` / 根级 `totalTarget`）泄漏到根或 `collaborationSubmitTaskParam` 层
- 员工 key 大小写错（`aiwa` / `aiwaParam` / `franParam` 等都会被纠错为 PascalCase）
- `executionMode` 必须是数字 `1`（拦截 `"1"` / `true` / `"定额任务"` 等）
- `currentModule` 必须固定为 `"content"`；含 `Fran`/`Lisa` 时 `sourceSettings` 必须是完整对象
- 各员工必填键、固定值（如 AiWa.incrementalTarget=5000、Frank.upperLimitTarget=1000、Fran.priority="Daily"、Lisa.incrementalTarget=100）
- 数组类字段类型（`keywordList` / `industryList` / `countryCodeList` / `callingNumber` / `templateParamList` / `publishTemplates` / `accountConfigList`）
- AiWa.addressObjList 占位规则与 `type=0/1` 与 `address` / `province/city/county` 的互斥
- Frank.emailPlanList 长度恰为 1 与子键完整
- Lisa.templateParamList 数组结构 + 每项三键齐全 + 变量内容合规（如 `time` 类禁止含中文"年"）

**行为约束：**
- **必须**用 heredoc + 单引号定界符（`<<'TASK_BODY_EOF'`），不能用 argv 传 JSON。
- 脚本输出单行 JSON（含 `summary` / `errors` / `body_preview` / `response`）。
- 退出码：`0` 提交成功 / `1` 校验失败 / `2` 网络失败 / `3` HTTP 非 2xx / `4` 输入格式错误或 API key 缺失。
- 退出码 ≠ 0 时，**必须**把 `summary`、`errors`/`response` 原样回给用户，按提示修正请求体再重跑；**不允许**跳过校验、不允许"我这次写得很标准"为由绕过。

> ℹ️ 仅在排查时可先用 `python3 scripts/submit_task.py --dry-run <<'TASK_BODY_EOF' ...` 跑校验而不发 HTTP；正式提交禁止 `--dry-run`。

**用户确认清单（以下各项必须已获得用户明确确认，缺一不可提交）：**
- Fran 参与时：✅ `callingNumber` 非空（多号码时用户已选择）
- Fran 参与时：✅ 用户已选择/确认场景库（`scriptId` 非空，且用户有明确回复确认）
- Lisa 参与时：✅ 用户已选择/确认短信模板（`templateCode` 非空，且用户有明确回复确认）
- Lisa 参与时（模板含变量）：✅ 已通过 `scripts/submit_task.py` 完成提交（脚本内部已串行跑过 `validate_employee_params.py` + `validate_sms_template_params.py`）；脚本退出码 ≠ 0 时禁止重试，必须把脚本返回的 `summary`/`errors` 原样回给用户、修正后再重跑。**禁止**绕过 `submit_task.py` 自己拼 curl。**特别注意 `time` 类变量**——值中**不得**出现中文"年"，脚本会直接拒绝
- Frank 参与时：✅ 用户 profile 已获取（`senderEmail` 非空），邮件内容已 AI 生成

**若上述任一项未完成，禁止调用提交接口。**

---

**请求体示例（AiWa + Frank 联合任务）：**
```json
{
  "collaborationSubmitTaskParam": {
    "taskName": "找服装客户并发邮件",
    "taskDescription": "帮我找10个做服装的客户并发邮件",
    "executionMode": 1,
    "employeeParams": {
      "AiWa": {
        "totalTarget": 10,
        "incrementalTarget": 5000,
        "upperLimitTarget": 5000,
        "keywordList": ["服装", "clothing"],
        "continent": null,
        "country": null,
        "countryCodeList": [],
        "addressObjList": [{"type": 1, "province": "", "city": "", "county": "", "address": ""}],
        "industryList": ["服装"]
      },
      "Frank": {
        "incrementalTarget": 1000,
        "upperLimitTarget": 1000,
        "senderEmail": "{profile.email}",
        "language": "中文",
        "templateId": null,
        "emailPlanList": [{
          "delayDay": 0,
          "emailSubject": "{AI生成的邮件主题}",
          "emailText": "{AI生成的邮件正文HTML}",
          "loading": 0
        }]
      }
    },
    "sourceSettings": null,
    "currentModule": "content"
  },
  "completed": true
}
```

**成功响应：**
```json
{
  "msg": "操作成功",
  "code": 200,
  "data": {
    "employeeList": [
      {
        "dagTaskId": "<frankDagTaskId>",
        "nodeType": "FRANK",
        "customerPoolId": 1065
      },
      {
        "dagTaskId": "<aiwaDagTaskId>",
        "nodeType": "AIWA",
        "customerPoolId": 1066
      }
    ],
    "taskId": "<taskId>"
  }
}
```

**响应字段提取规则：**
- `taskId`：取 `data.taskId`
- `aiwaDagTaskId`：遍历 `data.employeeList`，找到 `nodeType === "AIWA"` 的条目，取其 `dagTaskId`，用于 **AiWa** 客户查询；无则为 null
- `aiwaCustomerPoolId`：遍历 `data.employeeList`，找到 `nodeType === "AIWA"` 的条目，取其 `customerPoolId`，用于 **AiWa** 客户查询；无则为 null
- `frankDagTaskId`：遍历 `data.employeeList`，找到 `nodeType === "FRANK"` 的条目，取其 `dagTaskId`，用于 **Frank** 邮件查询；无则为 null
- `franDagTaskId`：遍历 `data.employeeList`，找到 `nodeType === "FRAN"` 的条目，取其 `dagTaskId`，用于 **Fran** 电话查询；无则为 null
- `franCustomerPoolId`：遍历 `data.employeeList`，找到 `nodeType === "FRAN"` 的条目，取其 `customerPoolId`，用于 **Fran** 电话统计/详情查询；无则为 null
- `lisaDagTaskId`：遍历 `data.employeeList`，找到 `nodeType === "LISA"` 的条目，取其 `dagTaskId`，用于 **Lisa** 短信查询；无则为 null
- `lisaCustomerPoolId`：遍历 `data.employeeList`，找到 `nodeType === "LISA"` 的条目，取其 `customerPoolId`，用于 **Lisa** 短信统计/详情查询；无则为 null

> ⚠️ **`nodeType` 大写统一**：后端返回的 `nodeType` 是**全大写**（`AIWA` / `FRANK` / `FRAN` / `LISA`），不是 PascalCase 的 `AiWa` / `Frank` 。上面 4 条提取规则里的字符串只能是大写形式。如果某次调用发现某个员工总拿不到 `dagTaskId`，优先检查是不是这里的大写写错了。

提交成功后，告知用户并询问等待时间：
> 任务已提交！任务名：{taskName}，目标数量：{totalTarget}，任务ID：{taskId}。
>
> 后台正在执行，**你希望多久后查询结果并推送给你？**（直接告诉我时间，例如「8分钟」「半小时」「20分钟后」，直接回复「好」或不填则默认8分钟）

---

### Step 3.5：解析用户指定的等待时间

等待用户回复后，解析其意图为秒数：

| 用户说 | 解析为秒数 |
|--------|----------|
| N分钟 / N分 | N × 60 |
| N小时 | N × 3600 |
| 半小时 | 1800 |
| 一刻钟 | 900 |
| 好 / 默认 / ok / 回车 / 不填 | 480（8分钟）|
| 无法识别 | 再询问一次，若仍无效则使用 480 |

解析成功后，回复确认：
> 好的，将在 {用户指定时间描述}（约 {N} 分钟）后为你查询结果，请稍候 ☕

---

### Step 4：按用户指定时间设置自动查询

根据 Step 3.5 解析出的秒数（变量：`waitSeconds`），使用 `cron` 工具设置一次性定时任务：

```json
{
  "action": "add",
  "job": {
    "name": "aiwa-query-{taskId前8位}",
    "schedule": { "kind": "at", "at": "{当前时间 + waitSeconds 的ISO8601字符串，如2026-03-19T15:00:00+08:00}" },
    "sessionTarget": "main",
    "wakeMode": "now",
    "payload": {
      "kind": "systemEvent",
      "text": "[DeepSOP-AutoQuery] 人机协作台定时结果推送，请立即跳转 Step 5 执行结果查询并主动推送，不要等待用户提问，不要执行 Step 1-4。taskId={taskId}，aiwaDagTaskId={aiwaDagTaskId}，aiwaCustomerPoolId={aiwaCustomerPoolId}，frankDagTaskId={frankDagTaskId}，franDagTaskId={franDagTaskId}，franCustomerPoolId={franCustomerPoolId}，lisaDagTaskId={lisaDagTaskId}，lisaCustomerPoolId={lisaCustomerPoolId}，任务名：{taskName}，目标数量：{totalTarget}，参与员工：{employeeList}，feishuChatId={feishuChatId}。【AiWa部分，仅当employeeList包含AiWa时执行】1. 调用 POST https://ai.deepsop.com/prod-api/ai/presetEmployee/getCustomerPoolDetail?pageNum=1&pageSize=10 查询结果，参数 {"taskId":"{aiwaDagTaskId}","customerPoolId":{aiwaCustomerPoolId},"startTime":null,"endTime":null}；2. 将完整响应JSON传给脚本生成xlsx：python3 ~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_customers.py '<JSON>' '/tmp/aiwa_{aiwaDagTaskId前8位}.xlsx'；3. 执行 cp /tmp/aiwa_{aiwaDagTaskId前8位}.xlsx ~/.openclaw/workspace/aiwa_{aiwaDagTaskId前8位}.xlsx 并执行 openclaw message send --channel feishu --target {feishuChatId} --media ~/.openclaw/workspace/aiwa_{aiwaDagTaskId前8位}.xlsx --message 'AiWa 客户挖掘完成，共找到客户数据，详见附件' 将文件发送到飞书群；4. 同时在当前会话回复前5条客户摘要。【Frank部分，仅当employeeList包含Frank且frankDagTaskId不为null时执行】1. 调用 GET https://ai.deepsop.com/prod-api/ai/email/getTaskEmailCount?taskId={frankDagTaskId} 查询邮件统计（使用frankDagTaskId）；2. 调用 GET https://ai.deepsop.com/prod-api/ai/email/taskList?pageNum=1&pageSize=2000&taskId={frankDagTaskId} 查询邮件列表（使用frankDagTaskId）；3. 生成xlsx：python3 ~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_emails.py '<JSON>' '/tmp/frank_{frankDagTaskId前8位}.xlsx'；4. 执行 cp /tmp/frank_{frankDagTaskId前8位}.xlsx ~/.openclaw/workspace/frank_{frankDagTaskId前8位}.xlsx 并执行 openclaw message send --channel feishu --target {feishuChatId} --media ~/.openclaw/workspace/frank_{frankDagTaskId前8位}.xlsx --message 'Frank 邮件发送完成，详见附件' 将文件发送到飞书群；5. 同时在当前会话回复邮件统计摘要和前5条详情。【Lisa部分，仅当employeeList包含Lisa且lisaCustomerPoolId不为null时执行】1. 调用 POST https://ai.deepsop.com/prod-api/ai/sms/getTaskSmsCount 查询短信统计，参数 {"taskId":"{taskId}","customerPoolId":{lisaCustomerPoolId}}；2. 调用 POST https://ai.deepsop.com/prod-api/ai/sms/getSmsResultList?pageNum=1&pageSize=10 查询短信列表，参数 {"taskId":"{taskId}","customerPoolId":{lisaCustomerPoolId},"success":null,"startTime":null,"endTime":null}；3. 生成xlsx：python3 ~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_sms.py '<JSON>' '/tmp/lisa_{taskId前8位}.xlsx'；4. 发送文件并在当前会话展示短信统计摘要和前5条短信详情。"
    },
    "deleteAfterRun": true
  }
}
```

`schedule.at` = 当前时间 + `waitSeconds`，ISO8601 格式，含时区（如 `+08:00`）。

cron 设置成功后，回复用户确认并进入等待状态：
> ✅ 定时任务已设置！将在 **{N} 分钟后**（{schedule.at}）自动查询结果并推送，请安心等候 ⏰
> 如需提前查询，可说「现在就查结果」，我会立即执行。

> ⚠️ **等待期间处理规则**：
> - cron 设置完成到 [DeepSOP-AutoQuery] 到达之前，**不得主动执行 Step 5**。
> - 如果用户在等待期间间起其他话题，正常回应，但**不要提前查询结果**。
> - 如果用户说「现在就查结果」或「提前查」，立即执行 Step 5（此为唯一允许的提前触发方式）。

---

### Step 5：查询结果并返回给用户

> � **触发锁定：Step 5 只允许在以下两种情况下执行，其他任何情况一律不执行：**
> 1. 收到含 `[DeepSOP-AutoQuery]` 标记的 systemEvent（cron 自动触发）
> 2. 用户在等待期间明确说「现在就查结果」或「提前查」
>
> 🚨 **强制执行规则：执行 Step 5 时，以下规则一条都不得违反：**
> 1. **立即开始执行，不得发出任何询问或确认语句（如「要开始查询了吗」「是否需要推送」）**
> 2. **必须完成全流程：调接口 → 生成 xlsx → 发送文件 → 文字摘要，缺任一不算完成**
> 3. **文件必须透过 `openclaw message send` 主动发送到对应 channel，不得只告知文件路径**
> 4. **发送完成后在当前会话回复结果摘要，让用户对当前分话框也能看到结果**
> 5. **每个参与员工的结果必须按顺序全部处理，不得跳过任一员工**

根据 employeeList 包含的员工依次执行对应的 Step 5-A / 5-B / 5-C / 5-D / 5-E。

---

#### Step 5-A：AiWa 结果处理（仅当 employeeList 包含 AiWa）

> ⚠️ AiWa 查询接口使用 `aiwaDagTaskId`（`nodeType=AIWA` 的 `dagTaskId`）+ `aiwaCustomerPoolId`（同条目的 `customerPoolId`）。

**接口：** `POST https://ai.deepsop.com/prod-api/ai/presetEmployee/getCustomerPoolDetail?pageNum=1&pageSize=10`

**请求头：** `Content-Type: application/json`、`x-api-key: $DEEPSOP_API_KEY`

**请求体：**
```json
{"taskId": "{aiwaDagTaskId}", "customerPoolId": {aiwaCustomerPoolId}, "startTime": null, "endTime": null}
```

**响应关键字段：**
- `total`：总条数
- `rows[]`：客户列表（根层）
  - `personName` / `position`：联系人 / 职位
  - `companyName`：公司名称
  - `systemIndustryName`：标准化行业名称
  - `phone` / `email`：电话 / 邮筱（多个用逗号分隔）
  - `countryName`：国家（如 `中国/China`）
  - `whatsapp` / `linkedin` / `facebook` 等社媒字段
  - `url`：公司网址

**情况一：有数据（rows 非空）**

1. 将完整 API 响应 JSON 传给脚本生成 xlsx 文件：

```bash
python3 ~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_customers.py '<完整响应JSON>' '/tmp/aiwa_{aiwaDagTaskId前8位}.xlsx'
```

2. 根据当前 channel 决定如何返回文件：

**飞书（feishu）：** 必须执行，不得跳过
```bash
cp /tmp/aiwa_{aiwaDagTaskId前8位}.xlsx ~/.openclaw/workspace/aiwa_{aiwaDagTaskId前8位}.xlsx
openclaw message send --channel feishu --target {feishuChatId} --media ~/.openclaw/workspace/aiwa_{aiwaDagTaskId前8位}.xlsx --message 'AiWa 客户挖掘完成！任务「{taskName}」共找到 {total} 位客户，详情见附件。'
```

**Telegram / WhatsApp：** 必须执行，不得跳过
```
openclaw message send --channel telegram --target {chat_id} --media ~/.openclaw/workspace/aiwa_{aiwaDagTaskId前8位}.xlsx --message 'AiWa 客户挖掘完成！任务「{taskName}」共找到 {total} 位客户，详情见附件。'
```

**webchat 或其他不支持文件的 channel：**
> ✅ xlsx 文件已生成：`/tmp/aiwa_{aiwaDagTaskId前8位}.xlsx`，共 {total} 位客户。请从服务器下载该文件。

3. 同时以文字形式展示前5条客户预览：

```
序号. 👤 {personName}（{position}）
   🏢 公司：{companyName}
   🏭 行业：{systemIndustryName}
   🌍 国家：{countryName}
   📧 邮筱：{email}
   📱 手机：{phone}
   💬 WhatsApp：{whatsapp}
   🔗 LinkedIn：{linkedin}
```

社媒字段若为 null 则整行不显示。超过5条附上：`...共 {N} 位，完整数据见 xlsx 文件`

**情况二：rows 为空或 code 非 200**

> 已到查询时间，暂未获取到客户数据，任务可能仍在执行中。
> aiwaDagTaskId：{aiwaDagTaskId}，aiwaCustomerPoolId：{aiwaCustomerPoolId}
> 你可以告诉我「再查一次」，我会立即重新查询。

---

#### Step 5-C：Fran 结果处理（仅当 employeeList 包含 Fran 且 franDagTaskId 不为 null）

> ⚠️ Fran 的两个查询接口均使用 `franDagTaskId`（来自 `data.employeeList` 中 `nodeType=Fran` 的 `dagTaskId`）+ `franCustomerPoolId`（同条目的 `customerPoolId`）。

**第一步：查询电话任务统计**

接口：`GET https://ai.deepsop.com/prod-api/ai/presetEmployee/collaborationTaskStatistics?taskId={franDagTaskId}&customerPoolId={franCustomerPoolId}`

请求头：`x-api-key: $DEEPSOP_API_KEY`

返回字段说明：
- `taskCallPhoneCount`：总呼叫数
- `taskSuccessCallPhoneCount`：总通话数（接通并成功完成的数量）
- `taskAnswerCount`：总回复数

**第二步：查询电话任务详情列表**

接口：`POST https://ai.deepsop.com/prod-api/ai/presetEmployee/collaborationCallResult?pageNum=1&pageSize=10`

请求头：
```
Content-Type: application/json
x-api-key: $DEEPSOP_API_KEY
```

请求体（默认拉全部呼叫，`status` 可根据需求切换）：
```json
{
  "taskId": "{franDagTaskId}",
  "customerPoolId": {franCustomerPoolId},
  "status": "All",
  "startTime": "",
  "endTime": ""
}
```

`status` 可选值：
- `All`：全部呼叫（默认，对应 `taskCallPhoneCount`）
- `Succeeded`：通话成功记录（对应 `taskSuccessCallPhoneCount`）
- `Answer`：有回复记录（对应 `taskAnswerCount`）

响应关键字段：
- `rows[].jobStatus`：呼叫任务状态（如 `Succeeded`、`Failed`）
- `rows[].jobTaskStatus`：任务执行细分状态（如 `SucceededFinish`）
- `rows[].companyName` / `personName` / `phoneNumber` / `userName`：客户信息（可能为 null）
- `rows[].createTime` / `updateTime`：创建/更新时间
- `rows[].describeJobJson`：完整通话详情 JSON（字符串，需二次解析），关键内容在 `body.job.tasks[]`：
  - `contact.contactName` / `phoneNumber`：联系人与号码
  - `calledNumber` / `callingNumber`：被呼号 / 呼出号
  - `duration` / `realRingingDuration`：通话时长毫秒 / 实际振铃秒
  - `endReason`：挂断原因（如 `FINISHED`）
  - `conversation[]`：对话明细（`speaker`=`Robot`/`Contact`，`script`=话术内容）

**第三步：生成 xlsx 文件**

```bash
curl 结果存 /tmp/fran_{franDagTaskId前8位}_raw.json
python3 ~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_calls.py "$(cat /tmp/fran_{franDagTaskId前8位}_raw.json)" '/tmp/fran_{franDagTaskId前8位}.xlsx'
```

根据当前 channel 必须发送文件，不得跳过：
- **飞书**：必须执行 `cp /tmp/fran_{franDagTaskId前8位}.xlsx ~/.openclaw/workspace/fran_{franDagTaskId前8位}.xlsx`，再用 `openclaw message send --channel feishu --target {feishuChatId} --media ~/.openclaw/workspace/fran_{franDagTaskId前8位}.xlsx --message 'Fran 电话销售完成！任务「{taskName}」共呼叫 {taskCallPhoneCount} 人，详情见附件。'`
- **Telegram / WhatsApp**：必须执行，media 路径用 workspace 路径，message 同上
- **webchat**：输出文字摘要和文件路径 `/tmp/fran_{franDagTaskId前8位}.xlsx`

**第四步：展示结果**

先展示统计摘要：
```
☎️ Fran 电话销售任务结果 — {taskName}

📊 呼叫统计：
   📞 总呼叫数：{taskCallPhoneCount}
   ✅ 总通话数：{taskSuccessCallPhoneCount}
   💬 总回复数：{taskAnswerCount}
```

再展示列表中前 5 条呼叫详情（从 `rows[].describeJobJson` 解析）：
```
序号. 👤 {contactName}（{contactPhone}）
   🔄 状态：{jobStatus} / {endReason}
   ⏱ 通话时长：{duration_s}s（振铃 {realRingingDuration}s）
   📞 呼出号码：{callingNumber}
   📝 对话摘要：取 conversation 中第一条 Robot 的 script 前80字
```

超过 5 条附上：`...共 {total} 条通话记录，完整数据见 xlsx 文件`。

**情况：统计接口全为 0 或列表为空**

> Fran 电话任务数据暂未就绪，可能仍在拨号或已呼叫但未接通。
> franDagTaskId：{franDagTaskId}，franCustomerPoolId：{franCustomerPoolId}
> 你可以告诉我「再查Fran结果」，我会立即重新查询。

---

#### Step 5-D：Lisa 结果处理（仅当 employeeList 包含 Lisa 且 lisaDagTaskId 不为 null）

> ⚠️ Lisa 的两个查询接口均使用 `lisaDagTaskId`（来自 `data.employeeList` 中 `nodeType=Lisa` 的 `dagTaskId`）+ `lisaCustomerPoolId`（同条目的 `customerPoolId`）。

**第一步：查询短信任务统计**

接口：`POST https://ai.deepsop.com/prod-api/ai/sms/getTaskSmsCount`

请求头：`Content-Type: application/json`、`x-api-key: $DEEPSOP_API_KEY`

请求体：
```json
{"taskId": "{lisaDagTaskId}", "customerPoolId": {lisaCustomerPoolId}}
```

返回字段说明：
- `totalCount`：已发送短信数
- `successCount`：触达短信数（发送成功）
- `failCount`：失败短信数

**第二步：查询短信详情列表**

接口：`POST https://ai.deepsop.com/prod-api/ai/sms/getSmsResultList?pageNum=1&pageSize=10`

请求头：
```
Content-Type: application/json
x-api-key: $DEEPSOP_API_KEY
```

请求体：
```json
{"taskId": "{lisaDagTaskId}", "customerPoolId": {lisaCustomerPoolId}, "success": null, "startTime": null, "endTime": null}
```

关键字段：
- `data.total`：总条数
- `data.rows[].phoneNumber`：手机号码
- `data.rows[].success`：1=发送成功，0=发送失败
- `data.rows[].errMsg`：状态描述（如「用户接收成功」）
- `data.rows[].errCode`：状态码（如 `DELIVERED`）
- `data.rows[].content`：实际发送的短信内容
- `data.rows[].smsSize`：短信条数
- `data.rows[].sendTime`：发送时间
- `data.rows[].reportTime`：回执时间

**第三步：生成 xlsx 文件**

```bash
curl 结果存 /tmp/lisa_{lisaDagTaskId前8位}_raw.json
python3 ~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_sms.py "$(cat /tmp/lisa_{lisaDagTaskId前8位}_raw.json)" '/tmp/lisa_{lisaDagTaskId前8位}.xlsx'
```

根据当前 channel 必须发送文件，不得跳过：
- **飞书**：必须执行 `cp /tmp/lisa_{lisaDagTaskId前8位}.xlsx ~/.openclaw/workspace/lisa_{lisaDagTaskId前8位}.xlsx`，再用 `openclaw message send --channel feishu --target {feishuChatId} --media ~/.openclaw/workspace/lisa_{lisaDagTaskId前8位}.xlsx --message 'Lisa 短信发送完成！任务「{taskName}」共发送 {totalCount} 条，详情见附件。'`
- **Telegram / WhatsApp**：必须执行，media 路径用 workspace 路径，message 同上
- **webchat**：输出文字摘要和文件路径 `/tmp/lisa_{lisaDagTaskId前8位}.xlsx`

**第四步：展示结果**

先展示统计摘要：
```
📱 Lisa 短信销售任务结果 — {taskName}

📊 发送统计：
   📨 总发送：{totalCount} 条
   ✅ 触达成功：{successCount} 条
   ❌ 发送失败：{failCount} 条
```

再展示列表中前 5 条短信详情：
```
序号. 📱 {phoneNumber}
   🔄 状态：{success中文} / {errCode}
   📝 内容：{content前60字}
   📅 发送：{sendTime}（回执 {reportTime}）
```

超过 5 条附上：`...共 {total} 条短信记录，完整数据见 xlsx 文件`。

**情况：统计接口全为 0 或列表为空**

> Lisa 短信任务数据暂未就绪，可能仍在发送中或等待运营商回执。
> lisaDagTaskId：{lisaDagTaskId}，lisaCustomerPoolId：{lisaCustomerPoolId}
> 你可以告诉我「再查Lisa结果」，我会立即重新查询。

---

#### Step 5-B：Frank 结果处理（仅当 employeeList 包含 Frank 且 frankDagTaskId 不为 null）

> ⚠️ Frank 的两个查询接口均使用 `frankDagTaskId`（来自提交响应 `data.employeeList` 中 `nodeType=FRANK` 的 `dagTaskId`），**不是** `taskId`。

**第一步：查询邮件统计**

接口：`GET https://ai.deepsop.com/prod-api/ai/email/getTaskEmailCount?taskId={frankDagTaskId}`

请求头：`x-api-key: $DEEPSOP_API_KEY`

返回字段说明：
- `taskSendEmailCount`：任务发送邮件总数
- `taskSuccessEmailCount`：发送成功数量
- `taskOpenEmailCount`：已读数量
- `taskReceiveEmailCount`：收到回复数量
- `taskClickEmailCount`：点击链接数量

**第二步：查询邮件列表**

接口：`GET https://ai.deepsop.com/prod-api/ai/email/taskList?pageNum=1&pageSize=2000&taskId={frankDagTaskId}`

请求头：`x-api-key: $DEEPSOP_API_KEY`

关键字段：
- `rows[].recipientEmailAddress`：收件人邮箱
- `rows[].companyName`：公司名称
- `rows[].personName`：联系人姓名
- `rows[].position`：职位
- `rows[].emailSubject`：邮件主题
- `rows[].sendTime`：发送时间
- `rows[].emailStatus`：发送状态（0=未发送，1=发送失败，2=发送成功）
- `rows[].round`：轮次

**第三步：生成 xlsx 文件**

将邮件列表 JSON 传给脚本生成 xlsx：
```bash
curl 结果存 /tmp/frank_{frankDagTaskId前8位}_raw.json
python3 ~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_emails.py "$(cat /tmp/frank_{frankDagTaskId前8位}_raw.json)" '/tmp/frank_{frankDagTaskId前8位}.xlsx'
```

根据当前 channel 必须发送文件，不得跳过：
- **飞书**：必须执行 `cp /tmp/frank_{frankDagTaskId前8位}.xlsx ~/.openclaw/workspace/frank_{frankDagTaskId前8位}.xlsx`，再用 `openclaw message send --channel feishu --target {feishuChatId} --media ~/.openclaw/workspace/frank_{frankDagTaskId前8位}.xlsx --message 'Frank 邮件发送完成！任务「{taskName}」共发送 {taskSendEmailCount} 封，详情见附件。'`
- **Telegram / WhatsApp**：必须执行，media 路径用 workspace 路径，message 同上
- **webchat**：输出文字摘要和文件路径 `/tmp/frank_{frankDagTaskId前8位}.xlsx`

**第四步：展示结果**

先展示统计摘要：
```
📧 Frank 邮件任务结果 — {taskName}

📊 发送统计：
   📤 总发送：{taskSendEmailCount} 封
   ✅ 发送成功：{taskSuccessEmailCount} 封（emailStatus=2）
   ❌ 发送失败：{taskSendEmailCount - taskSuccessEmailCount} 封（emailStatus=1）
   👁 已读：{taskOpenEmailCount} 封
   💬 收到回复：{taskReceiveEmailCount} 封
   🔗 点击链接：{taskClickEmailCount} 封
```

再展示前5条邮件发送详情：
```
序号. 📧 {emailSubject}
   👤 收件人：{personName}（{position}）
   🏢 公司：{companyName}
   📮 邮箱：{recipientEmailAddress}
   📅 发送时间：{sendTime}
   状态：✅ 成功 / ❌ 失败
```

超过5条附上：`...共 {total} 封，如需完整列表请告知`

**情况：统计接口或列表接口返回非 200 / data 为空**

> Frank 邮件任务数据暂未就绪，可能仍在发送中。
> 任务ID：{taskId}
> 你可以告诉我「再查Frank结果」，我会立即重新查询。


---

## 实现方式

- **AI 分析**：直接在当前对话中用 LLM 完成，分析时告知用户正在处理
- **HTTP 请求**：使用 `exec` 工具调用 `curl`
- **定时等待**：使用 `cron(action=add)` 设置 8 分钟后触发的 systemEvent
- **xlsx 生成**：使用 `exec` 调用 Python 脚本

---

## 依赖

- Python 3（系统自带）
- openpyxl：`python3 -m pip install openpyxl --user --break-system-packages`
- AiWa 生成脚本：`~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_customers.py`
- Frank 生成脚本：`~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_emails.py`
- Fran 生成脚本：`~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_calls.py`
- Lisa 生成脚本：`~/.openclaw/workspace/skills/deepsop-humabot/scripts/format_sms.py`

---

## 错误处理

- `DEEPSOP_API_KEY` 未设置：提示用户**需要 API Key 授权**才能使用本技能：
  - **已有账号** → 前往 [https://ai.deepsop.com/login?source=3](https://ai.deepsop.com/login?source=3) 登录获取
  - **没有账号** → 前往 [https://ai.deepsop.com/register?source=3](https://ai.deepsop.com/register?source=3) 注册获取
  
  登录后在控制台新建 API Key（`sk-` 开头），配置 `DEEPSOP_API_KEY` 环境变量后再重试
- POST 接口返回非 200：展示错误信息，提示检查参数或稍后重试
- AiWa GET 接口 data 为空：提示任务可能仍在执行，给出 taskId 供用户告知「再查一次」
- Frank 邮件统计/列表接口异常：提示邮件任务可能仍在发送中，给出 taskId 供用户告知「再查Frank结果」
- Frank / Fran / Lisa 单独出现（未与 AiWa 搭配）：终止任务，提示用户补充客户挖掘需求
- Fran 外呼实例并发数为 0：终止任务，提示用户联系管理员开通并发资源
- Fran 号码池为空：终止任务，提示用户联系管理员开通外呼号码
- Frank 邮箱未绑定：终止任务，提示用户登录 https://ai.deepsop.com 前往「邮件配置」绑定邮箱
- Fran 场景库为空或无 `PUBLISHED` 状态：终止任务，提示用户前往 https://ai.deepsop.com 创建并发布场景库
- Lisa 短信模板为空或无 `AUDIT_STATE_PASS` 状态：终止任务，提示用户前往 https://ai.deepsop.com 创建并提交审核短信模板
- Lisa 变量校验失败：明确告知用户不符合的具体规则并要求重新填写，不中断整个流程
- Lisa 统计/详情接口异常或计数全为 0：提示短信任务可能仍在发送中，给出 taskId 和 lisaCustomerPoolId 供用户告知「再查Lisa结果」
- Fran 统计/详情接口异常或计数全为 0：提示电话任务可能仍在拨号中，给出 taskId 和 franCustomerPoolId 供用户告知「再查Fran结果」
- Python 脚本执行失败：直接以文字列表格式返回客户数据，不中断流程
- 数字员工禁用（status=1）：终止任务，提示联系管理员启用该员工
- 数字员工使用天数耗尽（remainingDays≤0）：终止任务，提示前往 https://ai.deepsop.com 购买/续费
- 不支持的员工（Jack/Leo/Sophia/Alex）：终止任务，提示当前仅支持 AiWa、Frank、Fran、Lisa
- TikTok 视频生成与发布（Toby）：本技能不再支持，请改用 `deepsop-tiktokflow` 技能
- 网络请求失败：展示 curl 错误信息
