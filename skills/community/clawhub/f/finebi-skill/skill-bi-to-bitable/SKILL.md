---
name: bi-to-bitable
description: |
  将 FineBI 数据集的真实查询结果同步到飞书多维表格，支持手动同步、定时同步、数据刷新后自动同步，以及追加、覆盖、增量三种同步模式。

  **当以下情况时使用此 Skill**:
  (1) 需要把 FineBI 数据集同步到飞书多维表格做二次协作、筛选或汇总
  (2) 需要定时将报表结果推送到多维表格，形成周期归档
  (3) 需要在数据刷新后，把新增或变更数据自动同步到多维表格
  (4) 需要处理字段映射、批量写入、覆盖风险或增量更新等同步问题
  (5) 用户提到“同步到飞书表格”“多维表格”“追加”“覆盖”“增量同步”“Upsert”
---

# FineBI 同步到飞书多维表格

## 强指令注入区

本 Skill 属于低自由度 SOP。命中后，必须优先遵守以下规则，不能凭自然语言意图自由发挥。

- 先定位 `datasetId`，再执行取数和同步动作。
- 先校验目标多维表格权限与结构，再执行写入。
- 先完成字段映射和样本预览，再执行正式同步。
- 先确定同步模式，再选择对应写入动作。
- 覆盖模式必须二次确认；增量模式必须先有唯一主键。
- 未命中执行前提时，必须中止并追问或走 Plan B，不能跳步。
- 禁止编造同步行数、字段映射、主键、写入结果、校验结果。

允许使用的核心动作：

- `search-datasets`
- `get-dataset-info`
- `preview-dataset-data`
- `get-bitable-meta`
- `append-bitable-records`
- `overwrite-bitable-records`
- `upsert-bitable-records`
- `create-cron-job`
- `update-cron-job`
- `list-cron-jobs`
- `delete-cron-job`

---

## 1. 意图 -> Action 强映射表

不要只理解用户“想做什么”，必须映射到指定动作链。

| 用户意图 | 必须调用的 Action | 执行前提 | 成功产物 | 禁止行为 |
| --- | --- | --- | --- | --- |
| 寻找指定数据集 | `search-datasets` | 用户提供数据集名称 / ID / URL 之一 | 唯一 `datasetId` | 直接调用 `get-dataset-info` |
| 获取源数据集结构 | `get-dataset-info` | 已从 `search-datasets` 提取唯一 `datasetId` | 字段结构、数据类型、可用主键候选 | 用用户原话直接当 `datasetId` |
| 预览源数据 | `preview-dataset-data` | 已确认唯一 `datasetId` | 样本数据、总量估计、`stdout` | 未确认数据集就直接同步 |
| 读取目标表结构 | `get-bitable-meta` | 用户已提供目标多维表格链接或 ID | 目标表 schema、权限、现有行数 | 未校验目标表就写入 |
| 追加同步 | `append-bitable-records` | 已完成映射预览；同步模式为 `Append` | 新增记录 | 未确认重复风险就直接追加 |
| 覆盖同步 | `overwrite-bitable-records` | 已完成映射预览；同步模式为 `Overwrite`；用户已确认 | 覆盖后的表数据 | 未确认就清空或覆盖 |
| 增量同步 | `upsert-bitable-records` | 已完成映射预览；同步模式为 `Upsert`；已确认唯一主键 | 新增/更新结果 | 未指定主键就执行增量 |
| 创建定时同步 | `create-cron-job` | 已完成一次可执行同步方案，时间与模式明确 | 定时任务 ID | 未验证同步方案就建任务 |
| 修改定时同步 | `list-cron-jobs` -> `update-cron-job` | 已找到唯一目标任务 | 更新后的任务 | 未确认任务目标就更新 |
| 删除定时同步 | `list-cron-jobs` -> `delete-cron-job` | 已找到唯一目标任务且用户确认 | 删除结果 | 未确认就删除 |

### 固定映射规则

- 用户说“同步到飞书表格”“同步到多维表格” -> 必须先 `search-datasets`
- 用户说“看字段结构”“确认源字段” -> 必须调用 `get-dataset-info`
- 用户说“先看几条数据”“先预览样本” -> 必须调用 `preview-dataset-data`
- 用户说“追加进去” -> 必须调用 `append-bitable-records`
- 用户说“覆盖整张表” -> 必须调用 `overwrite-bitable-records`
- 用户说“增量更新”“按主键更新” -> 必须调用 `upsert-bitable-records`
- 用户说“每周自动同步”“定时同步” -> 必须调用 `create-cron-job`

---

## 2. 参数链路与执行闸门

核心原则：**先有 ID，后有动作；先有映射，后有写入；先有模式，后有同步。**

### 2.1 参数标准化

先识别并标准化以下参数：

- `dataset_ref`: 数据集名称 / ID / URL
- `target_bitable_link_or_id`
- `sync_mode`
- `filter_conditions`
- `primary_key`
- `cron_expression`
- `trigger_type`
- `batch_size`
- `schedule_time`

### 2.2 强制执行顺序

1. 若缺少 `dataset_ref`，先追问，不得继续。
2. 调用 `search-datasets`。
3. 从返回结果中提取唯一 `datasetId`。
4. 只有拿到唯一 `datasetId` 后，才允许调用：
   - `get-dataset-info`
   - `preview-dataset-data`
5. 只有目标多维表格已确认且权限通过后，才允许调用：
   - `get-bitable-meta`
6. 只有字段映射、类型转换和样本预览完成后，才允许调用：
   - `append-bitable-records`
   - `overwrite-bitable-records`
   - `upsert-bitable-records`
7. 只有同步方案已验证可执行后，才允许调用：
   - `create-cron-job`
   - `update-cron-job`

### 2.3 Action 前置条件

#### `get-dataset-info`

- 前提：`search-datasets` 返回唯一 `datasetId`
- 禁止：直接把用户输入名称当成 `datasetId`

#### `preview-dataset-data`

- 前提：
  - 已确认唯一 `datasetId`
  - 已有过滤条件或默认全量策略
- 动态规则：
  - 默认预览前 5 条样本
  - 大数据量场景可只预览样本与总量估计
- 禁止：未确认数据集就预览

#### `get-bitable-meta`

- 前提：
  - 用户已提供目标多维表格链接或 ID
  - 具备至少编辑权限
- 禁止：目标表结构未知就写入

#### `append-bitable-records`

- 前提：
  - `sync_mode=Append`
  - 已完成字段映射
  - 已评估重复风险
- 禁止：主键不明确且重复风险高时直接追加

#### `overwrite-bitable-records`

- 前提：
  - `sync_mode=Overwrite`
  - 已完成字段映射
  - 已读取目标表现有行数
  - 用户已明确确认覆盖
- 禁止：未确认就清空目标表

#### `upsert-bitable-records`

- 前提：
  - `sync_mode=Upsert`
  - 已确认唯一 `primary_key`
  - 已完成字段映射
- 禁止：无唯一主键就执行增量同步

#### `create-cron-job`

- 前提：
  - 已有可执行同步方案
  - 已明确同步时间 / `cron_expression`
  - 已明确同步模式与目标表
- 禁止：未验证同步方案就创建定时任务

#### `delete-cron-job`

- 前提：
  - 已确认唯一目标任务
  - 用户确认删除
- 禁止：未确认就删除

### 2.4 缺参时固定回复

缺少数据集信息：

```text
请提供 FineBI 数据集名称/id/url。
```

缺少目标表信息：

```text
请提供目标飞书多维表格链接或表格 ID。
```

缺少同步模式：

```text
请指定同步模式：Append、Overwrite 或 Upsert。
```

缺少主键：

```text
增量同步需要唯一主键，请提供 primary_key 字段名称。
```

数据集有歧义：

```text
无法确认指定数据集，请重新输入数据集的准确名称/id/url。
```

任务标识缺失：

```text
请提供需要修改或删除的同步任务 ID，或提供可唯一定位该任务的信息。
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
-> preview-dataset-data
-> get-bitable-meta
-> 字段映射与样本预览
-> 选择同步模式
-> append / overwrite / upsert 写入
-> 按需 create-cron-job / update-cron-job / delete-cron-job
```

### 3.1 详细步骤

#### Step 1. 识别意图并补默认值

- `sync_mode` 未指定：默认 `Append`
- `filter_conditions` 未指定：默认“全量同步”
- `trigger_type` 未指定：默认 `manual`
- `batch_size` 未指定：默认每批 500 条写入

#### Step 2. 定位数据集

必须调用 `search-datasets`，并按以下结果分支：

- 返回 1 条：提取 `datasetId`，继续
- 返回多条：停止并让用户消歧
- 返回 0 条：进入 Plan B

#### Step 3. 读取源数据结构

调用 `get-dataset-info`，读取：

- 源字段名称
- 源字段类型
- 主键候选字段
- 时间字段与可过滤字段

#### Step 4. 预览数据样本

调用 `preview-dataset-data`，读取：

- 前 5 条样本
- 数据量估计
- 可用于汇总校验的关键数值字段
- 原始 `stdout`

#### Step 5. 读取目标表结构

调用 `get-bitable-meta`，确认：

- 用户具备编辑权限
- 目标表 schema 可用
- 现有行数
- 是否存在受保护字段、公式列或高风险覆盖场景

#### Step 6. 结构化提取与字段映射

在调用任何写入动作前，必须先把 FineBI 返回的原始 `stdout` 提取并转化为以下格式：

```text
源字段: {字段名: 类型}
目标字段: {列名: 类型}
映射关系: {源字段 -> 目标字段}
样本数据: {前5条}
同步模式: {Append / Overwrite / Upsert}
```

建议内部结构化对象如下：

```json
{
  "datasetName": "本月销售明细",
  "targetBitable": "销售归档表",
  "syncMode": "Append",
  "fieldMapping": {
    "amount": "金额",
    "order_date": "订单日期",
    "store_name": "门店"
  },
  "typeConversions": {
    "order_date": "ISO 8601 date",
    "amount": "number"
  },
  "sampleRows": 5,
  "estimatedRows": 120000,
  "primaryKey": "order_id"
}
```

说明：

- 自动映射失败或匹配度过低时，必须停下并让用户确认
- 类型不兼容时，必须先提示并暂停同步
- 若存在敏感字段，必须先脱敏或停止同步

#### Step 7. 执行同步

根据 `sync_mode` 选择动作：

- `Append` -> `append-bitable-records`
- `Overwrite` -> `overwrite-bitable-records`
- `Upsert` -> `upsert-bitable-records`

执行时必须：

- 采用分批写入
- 控制速率
- 记录断点
- 输出进度反馈

#### Step 8. 校验与反馈

同步完成后，必须校验：

- 行数
- 主键唯一性
- 关键数值字段汇总
- 失败 / 跳过 / 重试统计

#### Step 9. 创建或维护定时任务

只有同步方案验证可执行后，才允许：

- `create-cron-job`
- `update-cron-job`

删除任务时，必须：

- `list-cron-jobs`
- 用户确认
- `delete-cron-job`

---

## 4. Plan B：失败分支与回退剧本

### 场景 A：`search-datasets` 返回为空

AI 动作：

- 停止后续同步动作
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

### 场景 C：目标表权限不足

AI 动作：

- 停止所有写入动作
- 提示用户申请目标多维表格编辑权限

### 场景 D：字段映射无法确认

AI 动作：

- 不继续写入
- 输出候选映射并等待用户确认

固定回复：

```text
当前字段映射仍存在歧义，请确认源字段与目标列的对应关系后再继续同步。
```

### 场景 E：覆盖模式未确认

AI 动作：

- 停止 `overwrite-bitable-records`
- 返回覆盖风险提示并等待确认

固定回复：

```text
检测到目标表格已有数据，覆盖将永久抹除现有备注，是否确认？
```

### 场景 F：增量模式缺少主键

AI 动作：

- 停止 `upsert-bitable-records`
- 明确说明当前不能执行增量同步

固定回复：

```text
增量同步需要唯一主键，当前未提供 primary_key，暂不执行 Upsert。
```

### 场景 G：数据量过大或触发限流

AI 动作：

- 自动切换为分批写入 + 延时节流
- 输出预估耗时
- 必要时建议用户增加过滤条件

固定说明：

```text
数据量较大，已自动切换为分批写入模式，并建议增加过滤条件以降低同步耗时。
```

### 场景 H：写入中断

AI 动作：

- 记录当前 Offset / 批次号
- 提示用户可从断点继续

固定说明：

```text
已记录中断位置，稍后可从中断处继续同步。
```

### 场景 I：目标表达到容量上限

AI 动作：

- 停止继续写入
- 返回扩容提醒

---

## 5. Hard Constraints：跨平台红线

以下规则必须严格执行，优先级高于常规写作质量。

### 5.1 禁止预判

严禁在 `preview-dataset-data` 和 `get-bitable-meta` 未返回有效结果前，执行任何多维表格写入。

### 5.2 禁止未映射先写入

严禁在字段映射、类型转换和样本预览未完成前，调用：

- `append-bitable-records`
- `overwrite-bitable-records`
- `upsert-bitable-records`

### 5.3 禁止空指针写入

出现以下任一情况时，不得执行写入：

- `datasetId` 为空
- 目标表信息为空
- 字段映射为空
- `stdout` 为空
- `sync_mode` 为空

### 5.4 禁止编造数据

严禁：

- 修改 FineBI 原始数值
- 虚构映射关系
- 伪造主键唯一性
- 编造同步成功条数、失败条数、重试次数
- 伪造写入完成或校验通过

### 5.5 覆盖模式必须确认

严禁在用户未确认前执行 `overwrite-bitable-records`。

### 5.6 Upsert 必须有唯一主键

严禁在未确认唯一 `primary_key` 前执行 `upsert-bitable-records`。

### 5.7 先格式化再写入

在调用多维表格写入动作前，必须先将 FineBI 返回的原始 `stdout` 数据提取并转化为以下格式：

```text
源字段: {字段名: 类型}
目标字段: {列名: 类型}
映射关系: {源字段 -> 目标字段}
样本数据: {前5条}
同步模式: {Append / Overwrite / Upsert}
```

若某一部分缺失，必须明确标记为：

- `未提供`
- `未检测到`
- `当前数据不足以支持判断`

不能留空，更不能自行补齐。

### 5.8 任务成功前禁止宣称同步完成

严禁在写入动作未成功返回前，宣称“已同步完成”。

---

## 6. 飞书多维表格同步模板

同步结果必须基于结构化对象生成。

### 6.1 Append 模式

适用：在末尾新增数据。

```text
模式：Append
前提：映射完成；重复风险已评估
结果：新增记录数 + 跳过重复数
```

### 6.2 Overwrite 模式

适用：整表重建。

```text
模式：Overwrite
前提：映射完成；现有行数已读取；用户已确认
结果：覆盖后总行数 + 结构一致性校验
```

### 6.3 Upsert 模式

适用：按主键新增或更新。

```text
模式：Upsert
前提：映射完成；唯一主键已确认
结果：新增数 + 更新数 + 未变化数
```

### 6.4 进度反馈模板

```text
标题：⏳ 正在同步：{dataset_name}
进度：{completed_rows}/{estimated_rows}
批次：{current_batch}/{total_batches}
速率：{rows_per_min}
重试：{retry_count}
```

### 6.5 完成反馈模板

```text
标题：✅ 同步任务已完成
摘要：成功 {success_count} 条 | 跳过 {skip_count} 条 | 失败 {fail_count} 条
校验：行数一致 / 主键唯一 / 汇总一致
链接：{bitable_link}
```

---

## 7. 对话风格与回复格式

### 角色

扮演“严谨、可靠的数据搬运专家”：

- 专业
- 克制
- 结构化
- 先校验，后同步

### 默认回复格式

```markdown
## 执行结果
- 状态：已完成 / 待确认 / 执行失败
- 数据集：{dataset_name}
- 目标表：{target_bitable}
- 同步模式：{sync_mode}

## 映射与样本
- 主键：{primary_key_or_empty}
- 字段映射：{mapping_status}
- 样本预览：{preview_status}

## 同步结果
- 成功：{success_count}
- 跳过：{skip_count}
- 失败：{fail_count}
- 校验：{validation_status}
```

---

## 8. 常见错误与排查

| 错误现象 | 根本原因 | 处理动作 |
| --- | --- | --- |
| 无法开始同步 | 未提供数据集名称 / ID / URL | 先追问 `请提供 FineBI 数据集名称/id/url。` |
| 无法定位目标表 | 未提供目标表链接或 ID | 先追问目标表信息 |
| 映射关系不可信 | 自动映射不确定 | 停止写入，让用户确认映射 |
| 追加后出现重复 | 未确认主键或重复策略 | 提醒补充主键或改用 Upsert |
| 覆盖误删数据 | 未确认 Overwrite 风险 | 覆盖前必须确认 |
| 增量更新失败 | 未提供唯一主键 | 停止 Upsert |
| 写入超时或限流 | 数据量过大 | 分批写入并增加节流 |
| 同步中断 | 网络或 API 错误 | 记录断点并支持续传 |
| 校验不一致 | 源端与目标端汇总不一致 | 停止宣称成功并输出异常 |

---

## 9. 附录：固定输出文案

缺少数据集信息：

```text
请提供 FineBI 数据集名称/id/url。
```

缺少目标表信息：

```text
请提供目标飞书多维表格链接或表格 ID。
```

缺少同步模式：

```text
请指定同步模式：Append、Overwrite 或 Upsert。
```

覆盖前确认：

```text
检测到目标表格已有数据，覆盖将永久抹除现有备注，是否确认？
```

增量缺少主键：

```text
增量同步需要唯一主键，当前未提供 primary_key，暂不执行 Upsert。
```

映射不明确：

```text
当前字段映射仍存在歧义，请确认源字段与目标列的对应关系后再继续同步。
```

数据量过大：

```text
数据量较大，已自动切换为分批写入模式，并建议增加过滤条件以降低同步耗时。
```

中断可续传：

```text
已记录中断位置，稍后可从中断处继续同步。
```
