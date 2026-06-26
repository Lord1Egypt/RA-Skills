---
name: deepsop-tiktokflow
description: TikTok 视频 AI 生成与发布技能（数字员工 Toby）。用户输入自然语言指令，AI 自动拆解任务参数，调用 deepsop 平台接口生成 AI 视频并发布到 TikTok，等待后查询并推送播放/点赞/评论/分享等数据。触发场景：用户说「发 TikTok 视频」「生成视频发布到 TikTok」「抖音国际版发视频」等与 TikTok 视频生成发布相关的指令；或收到包含 [DeepSOP-AutoQuery-Toby] 标记的系统定时事件（cron 回调）。需要提前配置环境变量 DEEPSOP_API_KEY。⚠️ 调用本 SKILL 前必须先完整阅读 SKILL.md。提交 agentSubmitTask **必须**走 scripts/submit_task.py（通过 heredoc 把 body 喂给 stdin），脚本内部串行跑 validate_employee_params.py + UTF-8 安全 HTTP 提交，**禁止**直接写 curl 命令（会因 Windows cp936 代码页导致 taskName/taskDescription 中文乱码）。脚本退出码 0 才算成功；非 0 必须把 summary/errors 原样回给用户后修正重试，禁止绕过校验或假装成功。
---

# TikTok 视频 AI 生成与发布（数字员工 Toby）

## 功能简介

本技能基于 deepsop 平台数字员工 **Toby**，能够：

- **理解自然语言指令**：直接描述需求，如「生成一条库阔 AI 宣传视频发布到 TikTok」
- **AI 视频生成**：调用 Veo3.1 / Sora2 / Wan2.x / Seedance / kling-v3-omni 等多种视频模型生成视频
- **TikTok 自动发布**：根据用户配置的发布参数（数量、开始时间、间隔）自动定时发布到指定 TikTok 账号
- **结果统计**：任务完成后自动查询播放量、点赞、评论、分享、视频明细等数据，并展示 TikTok 链接

> Toby 不依赖客户挖掘（AiWa）等其他员工，可独立执行。如需配合客户挖掘 / 邮件销售 / 电话销售 / 短信销售等多员工协作，请改用 `deepsop-humabot`。

---

## 前置条件：获取 API Key

本技能需要 **API Key 授权**才能调用 DeepSOP 接口。

1. 获取 API Key 入口：
   - **已有账号** → [https://ai.deepsop.com/login?source=5](https://ai.deepsop.com/login?source=5)
   - **没有账号** → [https://ai.deepsop.com/register?source=5](https://ai.deepsop.com/register?source=5)
2. 登录后进入「设置」/「API 管理」页面，新建以 `sk-` 开头的 API Key。
3. 配置环境变量：

```
DEEPSOP_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
```

> 所有 API 请求头需携带：`x-api-key: $DEEPSOP_API_KEY`
> API Base URL：`https://ai.deepsop.com/prod-api/`

---

## ⛔ 接口路径强约束（最高优先级）

> 🔒 调用任何接口时，**必须严格使用本文档对应步骤标注的完整 URL**，不得做任何形式的改写、简化、猜测或自创。
>
> 请求前自检流程：
> 1. 在下方「**API 路径权威清单**」中找到对应步骤的接口；
> 2. 将即将发出的完整 URL（含 host、path、query key 名与顺序、`platform=1` / `pageSize` 等）与清单中的 `Path` 列**逐字符比对**；
> 3. 完全一致才允许发出；任何偏差立即停止。
>
> 禁止行为：
> - ❌ 把 `prod-api` 改成 `api` / `v1` / `prod`
> - ❌ 把 camelCase 改成 snake_case 或全小写（`presetEmployee` ≠ `preset_employee` ≠ `presetemployee`）
> - ❌ `authaccount` 偏偏是全小写，不得改成 `authAccount`
> - ❌ 漏写或私自补加 query 参数（如漏 `platform=1` / `status=1`）
> - ❌ 凭"经验/记忆"猜测路径，不回到本文档对照

### 📋 API 路径权威清单（Base URL: `https://ai.deepsop.com/prod-api`）

| # | 步骤 | 方法 | Path（不含 Base URL） |
|---|---|---|---|
| 1 | Step 1.5 数字员工可用性 | `GET` | `/ai/presetEmployee/list` |
| 1.1 | Step 1.5.1① 签约套餐列表 | `GET` | `/ai/setting/list?packageType=3` |
| 1.2 | Step 1.5.1② 人民币→K币汇率 | `GET` | `/system/config/configKey/CNY_TO_KCOIN` |
| 1.3 | Step 1.5.1③ K币余额查询 | `GET` | `/ai/vip/balance?userId={userId}` |
| 1.4 | Step 1.5.1④ 提交签约（扣K币） | `POST` | `/ai/order/purchaseIndependentPackageByKToken` |
| 1.5 | Step 1.5.1③ 用户 Profile（取 userId） | `GET` | `/ai/user/profile` |
| 2 | Step 3 提交任务 | `POST` | `/ai/presetEmployee/submitTask` |
| 3 | Step 3 前置 E-1 TikTok 账号列表 | `GET` | `/ai/authaccount/list?pageNum=1&pageSize=999&platform=1&status=1` |
| 4 | Step 3 前置 E-2 TikTok 账号权限 | `GET` | `/ai/auth/tiktok/getCreatorInfo?authAccountId={id}` |
| 5 | Step 3 前置 E-3 视频模型列表 | `POST` | `/ai/consumeSource/list?pageNum=1&pageSize=999` |
| 6 | Step 5-1 视频统计 | `GET` | `/ai/data/count?taskId={tobyDagTaskId}&customerPoolId={tobyCustomerPoolId}&platform=1` |
| 7 | Step 5-2 视频列表 | `GET` | `/ai/data/list?pageNum=1&pageSize=10&taskId={tobyDagTaskId}&customerPoolId={tobyCustomerPoolId}&platform=1` |

### 🛡️ 双轨强约束（本文档 + 代码）

> 上述清单同时存在于 `scripts/api_paths.py`：
>
> - **LLM 直接发请求时：** 必须对照本文档清单逐字符比对路径。
> - **脚本调用 API 时：** 严禁脚本内硬编码 URL，必须从 `api_paths.py` 通过 `build_url("xxx")` 获取，并配合 `assert_url_matches()` 自检。
> - 漂移检测：运行 `python scripts/api_paths.py` 会扫描本文件中所有 `https://ai.deepsop.com/prod-api/...` 路径，未在 `api_paths.py` 登记则非零退出。

---

## 完整执行流程

### Step 0：触发类型判断（每次进入技能必须首先执行）

检查输入是否包含 `[DeepSOP-AutoQuery-Toby]` 标记：

- **包含**：cron 定时回调。**不得询问用户、不得等待确认**。立即从输入中解析 `taskId` / `tobyDagTaskId` / `tobyCustomerPoolId` / `taskName` / `feishuChatId`，跳过 Step 1～4 直接执行 Step 5。
- **不包含**：用户主动指令，继续 Step 1。

---

### Step 1：AI 分析（任务拆解）

用以下 prompt 分析用户指令，严格返回 JSON：

```
根据【指令】描述，Json格式返回数据
不需要多余的描述，不要过度解读，没有提及的内容请不要擅自理解，识别结果除了Json数据其他文字不要出现
规则如下：{
  "taskName": "根据描述总结出一个简洁的任务名称",
  "totalTarget": "提取描述中提及的视频数量（无单位纯数字）；未提及则填 1",
  "tiktokContent": "根据描述总结出一个 TikTok 内容发布的内容主题"
}
```

解析结果字段（**注意：内部解析变量，不要原样塞到最终 API 请求体**）：
- `taskName` → `collaborationSubmitTaskParam.taskName`
- `totalTarget` → `employeeParams.Toby.totalTarget`（不得作为根级字段）
- `tiktokContent` → `employeeParams.Toby.content` 与 `employeeParams.Toby.param.text`（不得作为独立字段出现）

**`executionMode` 当前阶段强制规则：** 提交请求体时一律硬编码为数字 `1`（定额任务）。后端枚举：`周期性任务 = 0`，`定额任务 = 1`。**绝不允许**写中文字符串、`"1"` 字符串、`true`、`null`。

---

### Step 1.5：数字员工 Toby 可用性校验（Step 1 完成后立即执行）

**接口：** `GET https://ai.deepsop.com/prod-api/ai/presetEmployee/list`

**请求头：** `x-api-key: $DEEPSOP_API_KEY`

响应 `data` 数组中找到 `name === "Toby"` 的条目，检查：
- `status`：`0` = 启用，`1` = 禁用
- `remainingDays`：剩余可用天数（可为 null）

规则：

1. **禁用（status=1）→ 终止任务：**
   > ⚠️ 数字员工「Toby」当前处于禁用状态，无法执行任务。请联系管理员启用后再试。

2. **未开通 / 已过期（status=0 且 `remainingDays` 为 null 或 ≤ 0）→ 进入签约流程（Step 1.5.1）**。完成后重新拉 `/ai/presetEmployee/list` 校验通过后继续；用户放弃或余额不足则终止。

3. **剩余 ≤ 7 天 → 提示但允许继续：**
   > ⚡ 提示：数字员工「Toby」剩余可用天数仅剩 **{remainingDays} 天**，建议尽快前往 https://ai.deepsop.com 续费。

4. **正常（status=0 且 remainingDays > 7）→ 继续**

#### Step 1.5.1：Toby 签约流程（仅规则 2 触发时执行）

**① 拉取套餐列表**

接口：`GET https://ai.deepsop.com/prod-api/ai/setting/list?packageType=3`

响应 `data` 中按 `presetEmployeeId` 匹配 Toby 对应条目，取其 `packageOptions`：

```
{
  presetEmployeeId,
  packageOptions: [
    { id, packageId, description, purchaseMonths, actualPrice, discountRate, giftKToken }
  ]
}
```

**② 展示套餐**

获取人民币→K币汇率：
接口：`GET https://ai.deepsop.com/prod-api/system/config/configKey/CNY_TO_KCOIN`
响应 `msg` 即为汇率（`rate`）。

应付 K 币计算：
```
priceKCoin = actualPrice × (discountRate / 100) × rate
```

向用户展示并等待用户回复序号。用户「取消」→ 终止：
> 已取消签约，任务终止。

**③ K 币余额校验**

> 🔒 **强制实时查询规则：每次进入本步骤都必须重新调用 `/ai/vip/balance`，严禁复用先前查询到的 balance 值。**

先获取 `userId`：`GET https://ai.deepsop.com/prod-api/ai/user/profile` 响应 `data.userId`。

接口：`GET https://ai.deepsop.com/prod-api/ai/vip/balance?userId={userId}`

响应 `data` 即为余额。

- `balance < priceKCoin` → 终止：
  > ❌ 余额不足，签约失败。当前余额：**{balance} K币**，所需：**{priceKCoin} K币**。
  > 请前往 https://ai.deepsop.com 充值后重新下达任务。

- `balance ≥ priceKCoin` → 进入 ④

**④ 提交签约**

接口：`POST https://ai.deepsop.com/prod-api/ai/order/purchaseIndependentPackageByKToken`
请求体：
```json
{ "packageId": "<packageId>", "optionId": "<id>" }
```

成功 → 回复成功并回到 Step 1.5 校验后继续；失败 → 终止。

---

### Step 2：Toby TikTok 账号与发布参数配置（Step 3 前置）

**E-1：查询 TikTok 绑定账号**

接口：`GET https://ai.deepsop.com/prod-api/ai/authaccount/list?pageNum=1&pageSize=999&platform=1&status=1`

请求头：`x-api-key: $DEEPSOP_API_KEY`

关键字段：
- `rows[].id`、`rows[].account`、`rows[].fansNum`、`rows[].groupNames`、`rows[].expiredTime`

处理：
- `rows` 为空 → 终止：
  > ⚠️ 当前账号未绑定任何 TikTok 授权账号，请先登录 https://ai.deepsop.com 添加 TikTok 授权账号后再试。
- 1 条 → 列出并等用户回复「确认」：
  ```
  检测到以下 TikTok 账号，请确认是否使用（回复「确认」即可）：
  1. @{account}（粉丝：{fansNum}，分组：{groupNames}）
  ```
- 多条 → 列出供用户多选（逗号分隔序号）。

**等待用户确认/选择**后，将选中账号的 `id` 列表记为 `selectedAccountIds`。

**E-2：获取账号权限信息**

针对第一个选中账号：
接口：`GET https://ai.deepsop.com/prod-api/ai/auth/tiktok/getCreatorInfo?authAccountId={selectedAccountIds[0]}`

提取：
- `data.privacyLevelOptions[]`：可用隐私级别
- `data.commentDisabled` / `data.duetDisabled` / `data.stitchDisabled`

`privacyLevelOptions` 多个时让用户选择隐私级别：
```
请选择该账号的视频隐私设置（回复序号）：
1. PUBLIC_TO_EVERYONE — 全公开
2. MUTUAL_FOLLOW_FRIENDS — 互关好友
3. SELF_ONLY — 仅自己可见
```

**E-3：AI 视频生成模型（默认）**

`param.methodType` **默认固定为 `"3"`**（Veo3.1 Fast Lite），无需用户选择。如需查看全部模型，可调：

接口：`POST https://ai.deepsop.com/prod-api/ai/consumeSource/list?pageNum=1&pageSize=999`
请求体：`{"sourceTypeList":["VIDEO_MODEL"],"hiddenState":"0"}`

默认 methodType=`"3"` 下其他视频参数默认：
- `resolution`: `720p`，`ratio`: `16:9`，`duration`: `8`（methodType=3 唯一允许值）
- `generationType`: `"FIRST&LAST"`，`shotType`: `"single"`，`mode`: `"pro"`
- `keepOriginalSound`: `"yes"`，`personGeneration`: `"allow_adult"`，`resizeMode`: `"pad"`
- `n`: `1`，`generateAudio`: `true`
- `enhancePrompt` / `promptExtend` / `multiShot`: `false`，`durationSwitch`: `"1"`

> 若用户切换其他模型（Veo3.1 Pro / Sora2 Pro / kling-v3-omni 等），先调 `consumeSource/list` 拿 `sourceValue`，再据此 methodType 去下方「methodType → 取值约束表」校正各依赖字段，**不得**沿用默认值。

**E-4：视频生成提示词确认（必问，禁止跳过）**

以 Step 1 解析出的 `tiktokContent` 作为默认提示词，强制询问：

```
当前 AI 视频生成提示词为：「{tiktokContent}」
是否需要修改？（回复「不用」直接使用，或直接输入新的提示词）
```

- 「不用」/类似否定 → 保持 `tiktokContent` 不变
- 输入新提示词 → 替换 `content` 与 `param.text`

**未收到用户回复不得继续。**

**E-5：发布参数配置（必须由用户指定，禁止自动填充）**

针对每个选中账号依次询问：
```
请为账号 @{account} 配置发布参数：
- 每天发布视频数（publishCount，如 3）：
- 定时发布开始时间（startTime，HH:mm 格式，如 09:30）：
- 视频发布间隔（publishInterval，分钟，如 60）：
```

**等待所有账号回复完毕**后，构建 `publishTemplates`。

---

### Step 3：构建并提交任务

> 🧷 **请求体总规约（最高优先级）**
>
> `collaborationSubmitTaskParam` **有且仅有以下 5 个根级键**：
>
> ```ts
> {
>   "taskName":        String,   // Step 1 的 taskName，非空
>   "currentModule":   "content",// 字符串字面量，永远是 "content"
>   "executionMode":   1,        // 永远写数字 1
>   "employeeParams":  { "Toby": {...} },
>   "taskDescription": String    // 用户原始指令，原文透传
> }
> ```
>
> 与其同级必须再带：
> - `completed`: `true`（布尔字面量）
> - `sourceSettings`: `null`（Toby 单独执行时永远为 null）
>
> **硬规则：**
> 1. `currentModule` 永远 `"content"`；`executionMode` 永远 `1`。
> 2. `taskDescription` 透传用户原文，禁止改写为 AI 总结。
> 3. `employeeParams` 子键必须是 PascalCase `Toby`，不得 `toby` / `TOBY` / `tobyParam`。
> 4. Step 1 内部解析变量（`tiktokContent` / 根级 `totalTarget`）一律不得出现在请求体中——只能流到 `employeeParams.Toby` 内的指定字段。

**接口：** `POST https://ai.deepsop.com/prod-api/ai/presetEmployee/submitTask`

**请求头：**
```
Content-Type: application/json; charset=utf-8
x-api-key: $DEEPSOP_API_KEY
```

> 🔒 **强制使用 `submit_task.py` 提交，禁止直接 curl：**
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
> 原因：直接 `curl -d '{中文 JSON}'` 会触发 Windows cp936 与 UTF-8 转码歧义，导致 taskName/taskDescription 中文乱码。`submit_task.py` 通过 stdin 字节流 + 显式 UTF-8 + `Content-Type: application/json; charset=utf-8` 闭合编码链路，并内置 `validate_employee_params.py` pre-flight 校验。
>
> 行为约束：
> - 必须 heredoc 单引号定界符（`<<'TASK_BODY_EOF'`），禁止 argv 传 JSON。
> - 退路：`python3 scripts/submit_task.py --file /tmp/task_body.json`。
> - 退出码：`0` 成功 / `1` 校验失败 / `2` 网络失败 / `3` 服务端非 2xx / `4` 输入格式错误。
> - 退出码 ≠ 0 时，**必须**把 `summary` + `errors`/`response` 原样回给用户，不得跳过或假装成功。

> ⛔ **字段名零改写规则：** 所有键名严格保持 camelCase，不得改 snake_case / kebab-case / 同义词。`accountConfigList` ≠ `account_config_list`，`publishTemplates` ≠ `publish_templates`，`staffId` ≠ `staff_id`，`videoItems` ≠ `video_items`，等等。

**Toby 参数构建规则：**

- `totalTarget`：定额模式下填 Step 1 的 totalTarget，周期模式下为 null
- `incrementalTarget`：周期模式下填用户指定的每天发布数，定额模式下固定填 10
- `upperLimitTarget`：固定 10
- `content`：来自 Step 1 的 `tiktokContent`（E-4 确认后的最终值）
- `staffId`：固定为空字符串 `""`
- `param`：嵌套对象，**有且仅有以下 27 个键**，必须按官方默认模板的键集构建（`text` 取自 E-4 确认后的最终提示词；`methodType` 默认 `"3"`）。**注意：当前 methodType 下 UI 不显的字段也必须传默认值，禁止裁剪 key**：

  | 字段 | 默认值 | 类型 | 说明 |
  |---|---|---|---|
  | `methodType` | `"3"` | string | 视频生成模型，默认 Veo3.1 Fast Lite |
  | `multiShot` | `false` | boolean | 是否多镜头（仅 methodType=`"10"` 实际生效） |
  | `generationType` | `"FIRST&LAST"` | string | 生成类型；可选值受 methodType 约束 |
  | `text` | E-4 提示词 | string | 视频生成提示词，与 `Toby.content` 相同 |
  | `multiPrompt` | `[]` | string[] | 多镜头分镜（仅 `shotType="customize"` 时填） |
  | `negativePrompt` | `""` | string | 反向提示词 |
  | `imageUrlList` | `[]` | string[] | 参考图（仅 `generationType` ∈ {REFERENCE,EDIT,FEATURE} 时填） |
  | `firstImageUrl` | `null` | string\|null | 首帧图（仅 `generationType="FIRST&LAST"` 时填） |
  | `lastImageUrl` | `null` | string\|null | 尾帧图（除 methodType ∈ {auto,1,8,11,12} 外） |
  | `firstClipUrl` | `null` | string\|null | 续写/编辑/参考视频（仅 methodType ∈ {10,14}） |
  | `elementList` | `[]` | array | 参考主体（仅 methodType=`"10"` 时填） |
  | `videoUrlList` | `[]` | string[] | 参考视频（methodType ∈ {9,16,17,18}） |
  | `audioUrl` | `null` | string\|null | 参考音频（methodType ∈ {7,8,14,15,16}） |
  | `keepOriginalSound` | `"yes"` | string | 保留视频原声（仅 methodType=`"10"` 实际生效） |
  | `durationList` | `[]` | array | 多段时长配置 |
  | `mode` | `"pro"` | string | 生成模式（仅 methodType=`"10"` 实际生效） |
  | `resolution` | `"720p"` | string | 分辨率；可选值受 methodType 约束 |
  | `ratio` | `"16:9"` | string | 画面比例；可选值受 methodType 约束 |
  | `generateAudio` | `true` | boolean | 是否生成声音（methodType ∈ {2,5,6,10,17,18} 生效） |
  | `enhancePrompt` | `false` | boolean | 翻译为英文（methodType ∈ {3,4,5,6} 生效） |
  | `n` | `1` | number | 生成数量（methodType ∈ {5,6} 生效） |
  | `personGeneration` | `"allow_adult"` | string | 是否允许人物（methodType ∈ {5,6} 生效） |
  | `resizeMode` | `"pad"` | string | 图像缩放（methodType ∈ {5,6} 生效） |
  | `promptExtend` | `false` | boolean | 智能改写（methodType ∈ {7,8,9,14,15,16} 生效） |
  | `shotType` | `"single"` | string | 镜头模式；可选值受 methodType 约束 |
  | `durationSwitch` | `"1"` | string | 生成时长模式（methodType ∈ {2,17,18} 生效） |
  | `duration` | `8`（methodType=`"3"`） | number | 视频时长（秒）；范围与默认值受 methodType 约束 |

- `videoItems`：固定 `[]`
- `publishTemplates`：每个选中账号一条：
  - `publishCount`：用户指定（字符串）
  - `releaseType`：固定 `"1"`
  - `timeZone`：固定 `"1"`
  - `intervalType`：固定 `"1"`
  - `startTime`：用户指定（HH:mm）
  - `accountId`：对应账号 `id`（字符串）
  - `publishInterval`：用户指定（整数，分钟）
- `accountConfigList`：仅一条，取 E-2 中第一个选中账号：
  - `accountId`：`selectedAccountIds[0]`（字符串）
  - `privacyLevel`：用户选定值
  - `disableDuet`：来自 `data.duetDisabled`（布尔转字符串）
  - `disableStitch`：来自 `data.stitchDisabled`
  - `disableComment`：来自 `data.commentDisabled`
  - `expand`：固定 `false`
  - `brandContentToggle`：固定 `"false"`
  - `brandOrganicToggle`：固定 `"false"`
  - `isPublicAccount`：固定 `true`
  - `commentDisabled`：同 `data.commentDisabled`（布尔转字符串）
  - `duetDisabled`：同 `data.duetDisabled`
  - `stitchDisabled`：同 `data.stitchDisabled`

> ⛔ **Toby 结构强约束：**
> 1. 子对象 key 必须 **`Toby`**，不得 `toby` / `TOBY` / `tobyParam` / `tobyParams`。
> 2. 必须嵌在 `collaborationSubmitTaskParam.employeeParams.Toby` 下。
> 3. **`param` 必须保持嵌套对象**：所有视频生成参数都是 `param` 内部键，**禁止**提升到 Toby 根部（错例：`Toby.methodType`、`Toby.text`）。
> 4. `tiktokContent` **不是请求体字段**，其值落到 `Toby.content` 与 `Toby.param.text`，但不得自己再加 `tiktokContent` 键。
> 5. `publishTemplates` 数组每条必填 7 键。
> 6. `accountConfigList` 数组（仅一条）必填 12 键。
> 7. `staffId` 必填，空字符串 `""` 也得给。
> 8. `videoItems` 必填，空数组 `[]` 也得给。
> 9. Toby 根部必填 9 键：`totalTarget` / `incrementalTarget` / `upperLimitTarget` / `content` / `staffId` / `param` / `videoItems` / `publishTemplates` / `accountConfigList`。
> 10. **`param` 27 键全量传**：即使当前 methodType 隐藏了某些字段，请求体仍按表中默认值传值，不得裁剪 key。

**📐 methodType → 取值约束表：**

| methodType | 模型 | `generationType` 可选 | `resolution` 可选 | `ratio` 可选 | `duration`（步长/最小/最大/默认） | `shotType` 可选 |
|---|---|---|---|---|---|---|
| `"auto"` | Auto | `FIRST&LAST` | `720p` | `16:9`,`9:16` | 由模型自动决定 (键保留默认 `8`) | `single` |
| `"1"` | Sora2 BetaMax | `TEXT`,`FIRST&LAST` | `720p` | `16:9`,`9:16` | step=5, 10–15, 默认 `10` | `single` |
| `"2"` | Seedance1.5 Pro | `TEXT`,`FIRST&LAST` | `480p`,`720p`,`1080p` | `adaptive`,`1:1`,`3:4`,`4:3`,`16:9`,`9:16`,`21:9` | step=1, 4–12, 默认 `4` | `single` |
| `"3"`（**默认**） | Veo3.1 Fast Lite | `TEXT`,`FIRST&LAST`,`REFERENCE` | `720p`,`1080p`,`4K` | `adaptive`,`16:9`,`9:16` | step=1, 8–8, 默认 `8`（**唯一允许 8**） | `single` |
| `"4"` | Veo3.1 Pro Lite | `TEXT`,`FIRST&LAST` | `720p`,`1080p`,`4K` | `adaptive`,`16:9`,`9:16` | step=1, 8–8, 默认 `8` | `single` |
| `"5"` | Veo3.1 Fast | `TEXT`,`FIRST&LAST` | `720p`,`1080p`,`4K` | `adaptive`,`16:9`,`9:16` | step=2, 4–8, 默认 `4` | `single` |
| `"6"` | Veo3.1 Pro | `TEXT`,`FIRST&LAST` | `720p`,`1080p`,`4K` | `adaptive`,`16:9`,`9:16` | step=2, 4–8, 默认 `4` | `single` |
| `"7"` | Wan2.6 t2v | `TEXT` | `720p`,`1080p` | `1:1`,`3:4`,`4:3`,`16:9`,`9:16` | step=1, 3–15, 默认 `3` | `single`,`multi` |
| `"8"` | Wan2.6 i2v | `FIRST&LAST` | `720p`,`1080p` | **不传 `ratio`** | step=1, 3–15, 默认 `3` | `single`,`multi` |
| `"9"` | Wan2.6 r2v | `REFERENCE` | `720p`,`1080p` | `1:1`,`3:4`,`4:3`,`16:9`,`9:16` | step=1, 3–10, 默认 `3` | `single`,`multi` |
| `"10"` | kling-v3-omni | `TEXT`,`FIRST&LAST`,`REFERENCE`,`EDIT`,`FEATURE` | **不传 `resolution`** | `1:1`,`16:9`,`9:16` | step=1, 3–15, 默认 `3` | `single`,`multi`,`customize` |
| `"11"` | Sora2 | `TEXT`,`FIRST&LAST` | `720p` | `16:9`,`9:16` | step=4, 4–12, 默认 `4` | `single` |
| `"12"` | Sora2 Pro | `TEXT`,`FIRST&LAST` | `720p`,`2K` | `16:9`,`9:16`,`7:4`,`4:7` | step=4, 4–12, 默认 `4` | `single` |
| `"14"` | Wan2.7 i2v | `FIRST&LAST`,`CONTINUATION` | `720p`,`1080p` | **不传 `ratio`** | step=1, 3–15, 默认 `3` | `single` |
| `"15"` | Wan2.7 t2v | `TEXT` | `720p`,`1080p` | `1:1`,`3:4`,`4:3`,`16:9`,`9:16` | step=1, 3–15, 默认 `3` | `single` |
| `"16"` | Wan2.7 r2v | `REFERENCE` | `720p`,`1080p` | `1:1`,`3:4`,`4:3`,`16:9`,`9:16` | 有 videoUrlList 时 step=1, 3–10；否则 3–15；默认 `3` | `single` |
| `"17"` | Seedance2.0 | `TEXT`,`FIRST&LAST`,`REFERENCE` | `480p`,`720p`,`1080p` | `adaptive`,`1:1`,`3:4`,`4:3`,`16:9`,`9:16`,`21:9` | step=1, 4–15, 默认 `4` | `single` |
| `"18"` | Seedance2.0 Fast | `TEXT`,`FIRST&LAST`,`REFERENCE` | `480p`,`720p` | `adaptive`,`1:1`,`3:4`,`4:3`,`16:9`,`9:16`,`21:9` | step=1, 4–15, 默认 `4` | `single` |

> 🔒 **填值硬规则：**
> 1. `generationType` / `resolution` / `ratio` / `shotType` 必须从该 methodType 行内"可选值"中取。
> 2. `duration` 必须落在该行 [最小, 最大] 闭区间内，且 `(duration - 最小) % 步长 === 0`。methodType=`"3"` 时只能是 `8`。
> 3. methodType=`"8"` / `"14"` 时**不传 `ratio`**（键保留、值给默认 `"16:9"`，后端忽略）；methodType=`"10"` 时**不传 `resolution`**（键保留、值给默认 `"720p"`）；methodType=`"auto"` 时 duration 由后端决定（键保留默认 `8`）。
> 4. 字段间依赖：
>    - `generationType="FIRST&LAST"` → `firstImageUrl` 必填、`lastImageUrl` 必填（除 methodType ∈ {auto,1,8,11,12} 留 `null`）
>    - `generationType ∈ {REFERENCE, EDIT, FEATURE}` → `imageUrlList` ≥ 1 项
>    - `generationType ∈ {CONTINUATION, EDIT, FEATURE}` → `firstClipUrl` 必填（仅 methodType ∈ {10,14} 支持）
>    - `shotType="customize"` → `multiPrompt` ≥ 1 项；`text` 可留空
> 5. 默认 methodType=`"3"` 下，合法 `param` 默认快照：`generationType="FIRST&LAST"`、`resolution="720p"`、`ratio="16:9"`、`duration=8`、`shotType="single"`、`enhancePrompt=false`，其他依赖字段保持空值（`null` 或 `[]`）。

**Toby 任务请求体示例：**
```json
{
  "collaborationSubmitTaskParam": {
    "taskName": "AI宣传视频TikTok分发",
    "taskDescription": "生成库阔AI宣传视频分发到tiktok",
    "executionMode": 1,
    "employeeParams": {
      "Toby": {
        "totalTarget": 1,
        "incrementalTarget": 10,
        "upperLimitTarget": 10,
        "content": "库阔AI宣传视频",
        "staffId": "",
        "param": {
          "methodType": "3",
          "multiShot": false,
          "generationType": "FIRST&LAST",
          "text": "库阔AI宣传视频",
          "multiPrompt": [],
          "negativePrompt": "",
          "imageUrlList": [],
          "firstImageUrl": null,
          "lastImageUrl": null,
          "firstClipUrl": null,
          "elementList": [],
          "videoUrlList": [],
          "audioUrl": null,
          "keepOriginalSound": "yes",
          "durationList": [],
          "mode": "pro",
          "resolution": "720p",
          "ratio": "16:9",
          "generateAudio": true,
          "enhancePrompt": false,
          "n": 1,
          "personGeneration": "allow_adult",
          "resizeMode": "pad",
          "promptExtend": false,
          "shotType": "single",
          "durationSwitch": "1",
          "duration": 8
        },
        "videoItems": [],
        "publishTemplates": [
          {
            "publishCount": "1",
            "releaseType": "1",
            "timeZone": "1",
            "intervalType": "1",
            "startTime": "15:10",
            "accountId": "130",
            "publishInterval": 60
          }
        ],
        "accountConfigList": [
          {
            "accountId": "130",
            "privacyLevel": "PUBLIC_TO_EVERYONE",
            "disableDuet": "false",
            "disableStitch": "false",
            "disableComment": "false",
            "expand": false,
            "brandContentToggle": "false",
            "brandOrganicToggle": "false",
            "isPublicAccount": true,
            "commentDisabled": "false",
            "duetDisabled": "false",
            "stitchDisabled": "false"
          }
        ]
      }
    },
    "sourceSettings": null,
    "currentModule": "content"
  },
  "completed": true
}
```

**用户确认清单（缺一不可提交）：**
- ✅ 用户已选择/确认 TikTok 账号（`selectedAccountIds` 非空）
- ✅ 用户已确认或修改视频生成提示词（`content` 已确定）
- ✅ 用户已为每个账号填写 `publishCount`、`startTime`、`publishInterval`
- ✅ 用户已选择隐私级别（`privacyLevel` 非空）

**成功响应：**
```json
{
  "msg": "操作成功",
  "code": 200,
  "data": {
    "employeeList": [
      { "dagTaskId": "<tobyDagTaskId>", "nodeType": "TOBY", "customerPoolId": 1066 }
    ],
    "taskId": "<taskId>"
  }
}
```

**响应字段提取：**
- `taskId` = `data.taskId`
- `tobyDagTaskId`：遍历 `data.employeeList` 找 `nodeType === "TOBY"` 取 `dagTaskId`
- `tobyCustomerPoolId`：同条目的 `customerPoolId`

> ⚠️ `nodeType` 后端返回**全大写** `"TOBY"`，不是 PascalCase `Toby`。

提交成功后，告知用户并询问等待时间：
> 任务已提交！任务名：{taskName}，目标视频数：{totalTarget}，任务ID：{taskId}。
>
> 后台正在生成与发布，**你希望多久后查询结果并推送给你？**（直接告诉我时间，例如「8 分钟」「半小时」「20 分钟后」，直接回复「好」或不填则默认 8 分钟）

---

### Step 3.5：解析用户指定的等待时间

| 用户说 | 解析为秒数 |
|--------|----------|
| N分钟 / N分 | N × 60 |
| N小时 | N × 3600 |
| 半小时 | 1800 |
| 一刻钟 | 900 |
| 好 / 默认 / ok / 回车 / 不填 | 480（8分钟）|
| 无法识别 | 再询问一次，仍无效则用 480 |

回复确认：
> 好的，将在 {用户指定时间描述}（约 {N} 分钟）后为你查询结果，请稍候 ☕

---

### Step 4：按用户指定时间设置自动查询

使用 `cron` 工具设置一次性定时任务：

```json
{
  "action": "add",
  "job": {
    "name": "toby-query-{taskId前8位}",
    "schedule": { "kind": "at", "at": "{当前时间 + waitSeconds 的 ISO8601 字符串，如 2026-03-19T15:00:00+08:00}" },
    "sessionTarget": "main",
    "wakeMode": "now",
    "payload": {
      "kind": "systemEvent",
      "text": "[DeepSOP-AutoQuery-Toby] TikTok 视频任务定时结果推送，请立即跳转 Step 5 执行结果查询并主动推送，不要等待用户提问，不要执行 Step 1-4。taskId={taskId}，tobyDagTaskId={tobyDagTaskId}，tobyCustomerPoolId={tobyCustomerPoolId}，任务名：{taskName}，feishuChatId={feishuChatId}。1. 调用 GET https://ai.deepsop.com/prod-api/ai/data/count?taskId={tobyDagTaskId}&customerPoolId={tobyCustomerPoolId}&platform=1 查询统计；2. 调用 GET https://ai.deepsop.com/prod-api/ai/data/list?pageNum=1&pageSize=10&taskId={tobyDagTaskId}&customerPoolId={tobyCustomerPoolId}&platform=1 查询视频列表；3. 展示统计数据（播放、点赞、评论、分享、发布总数）并列出每条视频的标题、播放、点赞、评论、转发、发布时间、TikTok 链接。"
    },
    "deleteAfterRun": true
  }
}
```

cron 设置成功后回复：
> ✅ 定时任务已设置！将在 **{N} 分钟后**（{schedule.at}）自动查询结果并推送，请安心等候 ⏰
> 如需提前查询，可说「现在就查结果」，我会立即执行。

> ⚠️ **等待期间处理规则：**
> - cron 设置完成到 [DeepSOP-AutoQuery-Toby] 到达之前，不得主动执行 Step 5。
> - 用户在等待期间问其他话题，正常回应，但不要提前查询。
> - 用户说「现在就查结果」/「提前查」→ 立即执行 Step 5。

---

### Step 5：查询结果并返回给用户

> 🚨 **触发锁定：Step 5 只允许在以下两种情况下执行：**
> 1. 收到含 `[DeepSOP-AutoQuery-Toby]` 标记的 systemEvent
> 2. 用户明确说「现在就查结果」/「提前查」

**5-1：查询统计数据**

接口：`GET https://ai.deepsop.com/prod-api/ai/data/count?taskId={tobyDagTaskId}&customerPoolId={tobyCustomerPoolId}&platform=1`

请求头：`x-api-key: $DEEPSOP_API_KEY`

关键字段：
- `data.playCount`：总播放量
- `data.likeCount`：总点赞数
- `data.commentCount`：总评论数
- `data.shareCount`：总分享数
- `data.totalTiktokCount`：已发布视频数

**5-2：查询视频列表**

接口：`GET https://ai.deepsop.com/prod-api/ai/data/list?pageNum=1&pageSize=10&taskId={tobyDagTaskId}&customerPoolId={tobyCustomerPoolId}&platform=1`

请求头：`x-api-key: $DEEPSOP_API_KEY`

关键字段：
- `rows[].titleName`：视频标题
- `rows[].platformUrl`：TikTok 链接
- `rows[].url`：视频文件地址
- `rows[].playNum` / `likesNum` / `commentNum` / `transmitNum`
- `rows[].displayCreateTime`：发布时间
- `total`：列表总数

**5-3：回复结果摘要**

```
🎥 Toby TikTok 视频发布结果
任务：{taskName}

📊 数据概览：
   发布视频数：{totalTiktokCount}
   总播放量：{playCount}
   总点赞数：{likeCount}
   总评论数：{commentCount}
   总分享数：{shareCount}

📋 视频明细（共 {total} 条）：
1. 《{titleName}》
   播放：{playNum} | 点赞：{likesNum} | 评论：{commentNum} | 转发：{transmitNum}
   发布时间：{displayCreateTime}
   TikTok 链接：{platformUrl}
2. ...
```

**情况：两个接口均返回非 200 或 data 为空**

> Toby TikTok 视频任务数据暂未就绪，可能仍在生成/发布中。
> 任务ID：{tobyDagTaskId}
> 你可以告诉我「再查 Toby 结果」，我会立即重新查询。

---

## 实现方式

- **AI 分析**：直接在当前对话中用 LLM 完成
- **HTTP 请求**：使用 `exec` 工具调用 `curl`（仅 GET 接口；POST submitTask **必须**走 `submit_task.py`）
- **定时等待**：使用 `cron(action=add)` 设置一次性 systemEvent

---

## 依赖

- Python 3（系统自带）
- 仅 Python 标准库（urllib），无第三方依赖

---

## 错误处理

- `DEEPSOP_API_KEY` 未设置：提示用户**需要 API Key 授权**
  - 已有账号 → [https://ai.deepsop.com/login?source=5](https://ai.deepsop.com/login?source=5)
  - 没有账号 → [https://ai.deepsop.com/register?source=5](https://ai.deepsop.com/register?source=5)
- POST 接口返回非 200：展示错误信息，提示检查参数或稍后重试
- TikTok 账号为空：终止任务，提示用户登录 https://ai.deepsop.com 添加 TikTok 授权账号
- 视频模型列表为空：终止任务，提示用户联系管理员开通视频生成权限
- 获取账号权限失败：提示用户重新授权该 TikTok 账号
- 统计/列表接口异常或数据为空：提示视频任务可能仍在生成/发布中，给出 tobyDagTaskId 供用户告知「再查 Toby 结果」
- 数字员工 Toby 禁用（status=1）：终止任务，提示联系管理员启用
- Toby 使用天数耗尽（remainingDays≤0）：进入 Step 1.5.1 签约流程；用户放弃或余额不足则终止
- 网络请求失败：展示 curl 错误信息
