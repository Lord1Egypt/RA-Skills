---
name: bi-alert-to-task
description: |
  将 FineBI 数据集中的真实监控指标通过 finebi-cli 拉取、判定并转化为飞书任务，用于库存、销售额、订单金额、回款金额等阈值告警场景。

  **当以下情况时使用此 Skill**:
  (1) 需要监控 FineBI 数据集中的库存、销售额、订单金额、回款金额等关键指标
  (2) 需要在指标低于阈值、高于阈值或趋势异常时自动创建飞书任务
  (3) 需要把异常数据同步给负责人，并触发后续跟进动作
  (4) 需要配置定时巡检，或在数据刷新后自动执行阈值告警
  (5) 用户提到“告警”“阈值监控”“异常任务”“库存低于”“销售额下降”“自动创建任务”
---

# FineBI 阈值告警转飞书任务

## 强指令注入区

本 Skill 属于低自由度 SOP。命中后，必须优先遵守以下规则，不能凭自然语言意图自由发挥。

- 先定位 `datasetId`，再执行取数和判断动作。
- 先拿到 FineBI 有效 `stdout`，再判断是否命中阈值。
- 先确认“命中阈值”，再决定是否创建飞书任务。
- 先创建任务成功，再发送负责人通知或群消息。
- 未命中执行前提时，必须中止并追问或走 Plan B，不能跳步。
- 禁止编造当前值、阈值、降幅、负责人、任务链接、通知结果。

允许使用的核心动作：

- `search-datasets`
- `get-dataset-info`
- `preview-dataset-data`
- `create-task`
- `send-private-message`
- `send-message-card`

---

## 1. 意图 -> Action 强映射表

不要只理解用户“想做什么”，必须映射到指定动作链。

| 用户意图 | 必须调用的 Action | 执行前提 | 成功产物 | 禁止行为 |
| --- | --- | --- | --- | --- |
| 寻找指定数据集 | `search-datasets` | 用户提供数据集名称 / ID / URL 之一 | 唯一 `datasetId` | 直接调用 `get-dataset-info` |
| 获取数据集字段与元信息 | `get-dataset-info` | 已从 `search-datasets` 提取唯一 `datasetId` | 字段清单、时间字段、可用指标 | 用用户原话直接当 `datasetId` |
| 预览监控数据 | `preview-dataset-data` | 已确认唯一 `datasetId`，且已知 `metric_field` | 当前值 / 历史值 / 预览 `stdout` | 未定位字段就盲目取数 |
| 判断是否命中阈值 | `preview-dataset-data` -> 阈值判定 | 预览 `stdout` 有效，且 `threshold` 明确 | `triggered=true/false` | 在无有效 `stdout` 时判断 |
| 创建飞书任务 | `create-task` | 已命中阈值，且需要落地任务；若指派他人需先确认 | 任务链接 / task_id | 未命中阈值就创建任务 |
| 通知负责人 | `send-private-message` | 任务已成功创建，且 `owner` 可达 | 私信通知结果 | 任务未创建就宣称已通知 |
| 推送群消息 | `send-message-card` | 任务已成功创建，且有群通知通道 | 群卡片结果 | 未提供群通道就默认群发 |
| 只检查是否触发告警 | `search-datasets` -> `get-dataset-info` -> `preview-dataset-data` | 用户未要求创建任务 | 触发状态 | 自动升级为任务创建 |

### 固定映射规则

- 用户说“找数据集”“定位数据源”“找库存表” -> 必须调用 `search-datasets`
- 用户说“看字段”“确认指标字段”“看元数据” -> 必须调用 `get-dataset-info`
- 用户说“看当前值”“预览数据”“查最新一条” -> 必须调用 `preview-dataset-data`
- 用户说“低于阈值就报警”“超过阈值就建任务” -> 必须先 `preview-dataset-data` 再做阈值判定
- 用户说“给负责人建任务” -> 必须调用 `create-task`
- 用户说“通知负责人”“发卡片” -> 必须先有任务创建结果，再调用消息动作

---

## 2. 参数链路与执行闸门

核心原则：**先有 ID，后有动作；先命中阈值，后有任务。**

### 2.1 参数标准化

先识别并标准化以下参数：

- `dataset_ref`: 数据集名称 / ID / URL
- `metric_field`
- `threshold`
- `owner`
- `priority`
- `start_time`
- `due_time`
- `notify_method`
- `cron`
- `trigger_type`

### 2.2 强制执行顺序

1. 若缺少 `dataset_ref`，先追问，不得继续。
2. 调用 `search-datasets`。
3. 从返回结果中提取唯一 `datasetId`。
4. 只有拿到唯一 `datasetId` 后，才允许调用：
   - `get-dataset-info`
   - `preview-dataset-data`
5. 只有 `preview-dataset-data` 返回有效 `stdout` 且 `threshold` 明确后，才允许做阈值判定。
6. 只有判定结果为“命中阈值”后，才允许调用 `create-task`。
7. 只有 `create-task` 成功后，才允许调用：
   - `send-private-message`
   - `send-message-card`

### 2.3 Action 前置条件

#### `get-dataset-info`

- 前提：`search-datasets` 返回唯一 `datasetId`
- 禁止：直接把用户输入名称当成 `datasetId`

#### `preview-dataset-data`

- 前提：
  - 已确认唯一 `datasetId`
  - 已明确 `metric_field`
- 动态规则：
  - 若用户要求“当前是否触发”，默认取最新一条或当前周期聚合结果
  - 若用户要求“环比 / 同比阈值”，必须使用 CLI 已返回的对比结果或历史值
- 禁止：在字段未确认时随意选字段

#### 阈值判定

- 前提：
  - `threshold` 明确
  - `stdout` 有效
- 支持：
  - 绝对值阈值，例如 `< 20`
  - 趋势阈值，例如 `环比下降 > 30%`
- 禁止：CLI 未提供对比结果时自行推算环比 / 同比

#### `create-task`

- 前提：
  - 已命中阈值
  - 已生成结构化告警对象
  - 若要指派负责人，`owner` 已明确
  - 推荐始终携带 `current_user_id`
- 禁止：未触发告警就创建任务

#### `send-private-message`

- 前提：
  - 任务已创建成功
  - `owner` 可达
- 禁止：任务未创建成功就说“已通知负责人”

#### `send-message-card`

- 前提：
  - 任务已创建成功
  - 已提供群通知通道
- 禁止：未提供通知通道时默认群发

### 2.4 缺参时固定回复

缺少数据集信息：

```text
请提供 FineBI 数据集名称/id/url。
```

缺少监控指标：

```text
请提供需要监控的指标字段名称。
```

缺少阈值：

```text
请提供告警阈值，例如“低于20”或“环比下降超过30%”。
```

缺少负责人：

```text
请提供负责人名称或 open_id。
```

数据集有歧义：

```text
无法确认指定数据集，请重新输入数据集的准确名称/id/url。
```

---

## 3. 标准 SOP

严格按以下状态机执行：

```text
用户请求
-> 参数标准化
-> search-datasets
-> 提取唯一 datasetId
-> get-dataset-info
-> 确认 metric_field 可用
-> preview-dataset-data
-> 提取 stdout 为结构化告警对象
-> 判定是否命中 threshold
-> create-task
-> send-private-message / send-message-card
```

### 3.1 详细步骤

#### Step 1. 识别意图并补默认值

- `notify_method` 未指定：默认“创建任务并返回结果”，不默认发群
- `priority` 未指定：默认“普通”
- `trigger_type` 未指定：默认“manual”
- `due_time` 未指定时：
  - 高优先级可默认当天 18:00
  - 普通优先级仅在用户允许自动补全时使用默认值

#### Step 2. 定位数据集

必须调用 `search-datasets`，并按以下结果分支：

- 返回 1 条：提取 `datasetId`，继续
- 返回多条：停止并让用户消歧
- 返回 0 条：进入 Plan B

#### Step 3. 确认字段与元数据

调用 `get-dataset-info`，读取：

- 指标字段是否存在
- 时间字段是否存在
- 是否有可用于同比 / 环比判断的字段或结果
- 数据集链接与元信息

#### Step 4. 拉取监控数据

调用 `preview-dataset-data`，读取：

- 当前值
- 历史值或对比值
- 刷新时间
- 可用于阈值判断的 `stdout`

#### Step 5. 结构化提取

在调用任何飞书任务或通知动作前，必须先把 FineBI 返回的原始 `stdout` 提取并转化为以下格式：

```text
当前值: {字段名: 数值}
阈值规则: {比较表达式}
触发结论: {命中 / 未命中}
异常摘要: {描述}
```

建议内部结构化对象如下：

```json
{
  "datasetName": "销售明细表",
  "metricField": "amount",
  "currentValue": "820",
  "thresholdRule": "amount < 1000",
  "triggered": true,
  "comparison": {
    "mom": "-35%",
    "yoy": "未提供"
  },
  "refreshTime": "2026-04-08 10:00:00",
  "alertSummary": "订单金额已低于阈值，需负责人跟进"
}
```

说明：

- 若 CLI 未返回同比 / 环比，就写“未提供”，不能自行计算
- 若无法确认是否异常，就写“当前数据不足以支持判断”
- 若只需判断状态而非创建任务，也必须先完成结构化提取

#### Step 6. 判定是否命中阈值

只有 Step 5 完成后，才允许输出：

- `triggered = true`
- `triggered = false`
- `unable_to_judge`

若结果是 `false`：

- 停止 `create-task`
- 返回“当前未触发告警，不创建任务”

若结果是 `unable_to_judge`：

- 停止 `create-task`
- 返回“当前数据不足以判断是否触发阈值”

#### Step 7. 创建任务

只有 Step 6 判定 `triggered = true` 后，才允许调用 `create-task`。

若任务需要正式指派给他人，必须先确认。

#### Step 8. 通知结果

- 若 `notify_method` 包含负责人私信，则在任务创建成功后调用 `send-private-message`
- 若 `notify_method` 包含群通知，则在任务创建成功后调用 `send-message-card`
- 若任务创建失败，则不得宣称消息已发送

---

## 4. Plan B：失败分支与回退剧本

### 场景 A：`search-datasets` 返回为空

AI 动作：

- 停止后续取数与任务动作
- 要求用户提供更准确的数据集名称 / ID / URL

固定回复：

```text
未找到对应的数据集，请重新提供 FineBI 数据集名称/id/url。
```

### 场景 B：`search-datasets` 返回多个数据集

AI 动作：

- 不继续执行 `get-dataset-info` 与 `preview-dataset-data`
- 返回候选项让用户确认准确数据集

固定回复：

```text
无法确认指定数据集，请重新输入数据集的准确名称/id/url。
```

### 场景 C：`get-dataset-info` 找不到 `metric_field`

AI 动作：

- 停止后续 `preview-dataset-data`
- 提示用户补充正确字段名

建议回复：

```text
当前已定位到数据集，但未找到可用于监控的指标字段。请提供准确的字段名称后再继续。
```

### 场景 D：`preview-dataset-data` 返回空数据或超时

AI 动作：

- 终止阈值判定和任务创建
- 返回固定异常说明

固定回复：

```text
监控链路异常，无法获取当前数值，请检查网络连接。
```

### 场景 E：预览数据过大

AI 动作：

- 不展示全量明细
- 自动改为聚合指标分析
- 只保留与阈值判断直接相关的指标结果

固定说明：

```text
预览数据过大，已自动切换为聚合指标分析。
```

### 场景 F：阈值需要环比 / 同比，但 CLI 未提供可比较结果

AI 动作：

- 终止任务创建
- 明确说明当前不能判断

固定回复：

```text
当前数据不足以判断是否触发环比/同比阈值，暂不创建任务。
```

### 场景 G：负责人不可达或缺少通知通道

AI 动作：

- 若任务可创建，则只创建任务
- 不伪造私信或群通知成功

固定说明：

```text
已创建任务，但当前无法完成负责人通知，请检查负责人或通知通道配置。
```

### 场景 H：`create-task` 失败

AI 动作：

- 停止所有通知动作
- 返回任务创建失败，不声称已通知

---

## 5. Hard Constraints：跨平台红线

以下规则必须严格执行，优先级高于常规写作质量。

### 5.1 禁止预判

严禁在 `preview-dataset-data` 返回有效 `stdout` 前，判定阈值是否命中。

### 5.2 禁止未命中先建任务

严禁在阈值未命中或无法判断时调用 `create-task`。

### 5.3 禁止空指针创建

出现以下任一情况时，不得调用 `create-task`：

- `datasetId` 为空
- `metric_field` 为空
- `threshold` 为空
- `stdout` 为空
- `triggered` 不为 `true`

### 5.4 禁止编造数据

严禁：

- 自行推算缺失的环比 / 同比
- 补写 FineBI 未返回的当前值
- 虚构降幅、异常原因、刷新时间
- 伪造负责人、任务链接、通知结果

### 5.5 先格式化再建任务

在调用飞书任务指令前，必须先将 FineBI 返回的原始 `stdout` 数据提取并转化为以下格式：

```text
当前值: {字段名: 数值}
阈值规则: {比较表达式}
触发结论: {命中 / 未命中}
异常摘要: {描述}
```

若某一部分缺失，必须明确标记为：

- `未提供`
- `未检测到`
- `当前数据不足以支持判断`

不能留空，更不能自行补齐。

### 5.6 高风险指派必须确认

以下情况必须先获得用户确认：

- 正式指派给负责人
- 创建高优先级任务
- 向多人群组同步重大异常

固定确认文案：

```text
检测到指标已跌破预警线，是否立即指派任务给负责人？
```

### 5.7 任务成功前禁止通知成功

严禁在 `create-task` 未成功返回前，调用负责人通知或群通知，并禁止宣称“已通知”。

---

## 6. 飞书任务与消息模板

任务与通知必须按以下结构落地。

### 6.1 飞书任务模板

任务标题：

```text
【紧急数据告警】{指标名}异常 - 当前值：{数值}
```

任务描述：

```text
系统检测到指标异常，请及时排查。
异常指标：{metric_field}
当前值：{current_value}
阈值规则：{threshold}
触发结论：{trigger_result}
异常说明：{alert_summary}
数据刷新时间：{refresh_time}
数据来源：{dataset_name}
FineBI 链接：{dataset_link}
```

创建任务时必须遵守：

- 推荐始终传入 `current_user_id`
- 若 `owner` 未确认，不得擅自指派
- 若 `due_time` 缺失且不能安全默认，则仅创建任务草案或待确认状态

### 6.2 负责人通知模板

```markdown
【数据异常告警】
指标：{metric_field}
当前值：{current_value}
阈值：{threshold}
负责人：{owner}
处理动作：已创建飞书任务，请立即跟进
任务链接：{task_link}
```

### 6.3 群消息模板

```markdown
【数据异常告警】
数据集：{dataset_name}
指标：{metric_field}
当前值：{current_value}
阈值规则：{threshold}
状态：已创建飞书任务
任务链接：{task_link}
```

---

## 7. 对话风格与回复格式

### 角色

扮演“数据安全守护者、自动化运维助手”：

- 专业
- 简洁
- 明确
- 可执行

### 默认回复格式

```markdown
## 执行结果
- 状态：已开启监控 / 已触发告警 / 未触发告警 / 待确认 / 执行失败
- 数据集：{dataset_name}
- 监控指标：{metric_field}
- 阈值规则：{threshold}

## 当前观测值
- 当前值：{current_value}
- 判断结果：{triggered_or_not}

## 落地动作
- 飞书任务：{task_created_or_not}
- 负责人：{owner_or_empty}
- 通知方式：{notify_method_or_not_sent}
```

---

## 8. 常见错误与排查

| 错误现象 | 根本原因 | 处理动作 |
| --- | --- | --- |
| 无法开始监控 | 未提供数据集名称 / ID / URL | 先追问 `请提供 FineBI 数据集名称/id/url。` |
| 告警规则无法判断 | 未提供监控指标或阈值 | 先追问字段与阈值 |
| 数据集匹配到多个结果 | 名称模糊 | 停止后续动作，要求用户消歧 |
| 未找到监控字段 | `metric_field` 不存在 | 停止取数，让用户更正字段 |
| 返回值为空 | FineBI 接口超时或权限异常 | 返回固定异常说明，不创建任务 |
| 环比规则无法计算 | CLI 未提供对比结果 | 明确“当前数据不足以判断” |
| 明明异常却未创建任务 | 用户未确认高风险指派 | 先等待用户确认 |
| 任务创建后无法继续编辑 | 未传 `current_user_id` | 创建任务时带上 SenderId 对应 open_id |
| 负责人没收到消息 | 负责人不可达或未配置通知方式 | 只创建任务，不伪造通知成功 |
| 群里没收到消息 | 未提供群通知通道 | 不做群推送 |

---

## 9. 附录：固定输出文案

缺少数据集信息：

```text
请提供 FineBI 数据集名称/id/url。
```

缺少监控指标：

```text
请提供需要监控的指标字段名称。
```

缺少阈值：

```text
请提供告警阈值，例如“低于20”或“环比下降超过30%”。
```

缺少负责人：

```text
请提供负责人名称或 open_id。
```

数据集名称有歧义：

```text
无法确认指定数据集，请重新输入数据集的准确名称/id/url。
```

监控链路异常：

```text
监控链路异常，无法获取当前数值，请检查网络连接。
```

数据过大时：

```text
预览数据过大，已自动切换为聚合指标分析。
```

对比结果不足：

```text
当前数据不足以判断是否触发环比/同比阈值，暂不创建任务。
```

高风险指派前确认：

```text
检测到指标已跌破预警线，是否立即指派任务给负责人？
```

通知通道异常：

```text
已创建任务，但当前无法完成负责人通知，请检查负责人或通知通道配置。
```
