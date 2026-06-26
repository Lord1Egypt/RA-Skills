---
name: 1688-supplychain-api-procurement
version: 0.0.6
description: | 
  1688 供应链采购 API Skill。面向云端 API 调用，不提供交互式找品、复杂表格或下单流程。支持两个功能：发起找挑询并返回 instanceId；按 instanceId 查询实例数据，并由脚本按输出模式返回 instanceId、fieldDesc 和 result。此 Skill 的最终回复格式默认是 raw JSON passthrough；查询实例数据时必须使用文件模式，通过 stream_output 工具输出结果，避免进入大模型上下文。
metadata: { "openclaw": { "requires": { "bins": ["python3"] } } }
---

# 1688-supplychain-api-procurement

本 Skill 只提供两个能力：

1. 发起找挑询：根据用户输入的完整采购与询盘需求，创建并触发一个 `inquiry` 实例，立即返回实例 ID。
2. 查询实例数据：根据用户提供的 `instanceId` 查询该实例当前数据，使用文件模式写入本地文件，再通过 `stream_output` 工具输出给用户。

本 Skill 不轮询询盘是否结束，也不在发起后自动查询实例数据。

## 输入

用户输入必须是一段完整需求，包含：

- 找品/采购需求：例如品类、规格、数量、价格带、工厂要求、图片或链接等。
- 询盘问题：例如报价、库存、交期、起订量、定制、包装、质检、售后等。

如果能从用户输入中明确拆出询盘问题，将这些问题作为 `questions` 传入；如果不能可靠拆分，不要反问，直接把完整用户需求作为唯一询盘问题传入。

## 功能一：发起找挑询

当用户提供完整采购与询盘需求、且未提供 `instanceId` 时，使用此功能。

命令：

```bash
cd {baseDir} && python3 cli.py inquiry \
  --requirement "<用户完整需求>" \
  --questions '[{"question":"报价","type":"current"},{"question":"交期","type":"current"}]' \
  --purchase-size 1 \
  --inquiry-item-size 30
```

参数：

- `--requirement` / `-r`：必填。用户完整需求，包含找品需求和询盘问题。
- `--questions` / `-q`：可选。询盘问题，支持 JSON 数组、JSON 对象、字符串，或分号/换行分隔文本。
- `--purchase-size` / `-c`：可选。采购数量，默认 `1`。
- `--inquiry-item-size`：可选。询盘商品数，对应 `taskInfo.inquiryItemSize`。如果用户没有指定询盘商品数，默认 `30`；如果用户明确说“询盘前 N 个商品 / 问 N 个供应商 / 询盘 N 个结果”，传入解析出的整数 N。
- `--recall-item-size`：可选。找品商品数，对应 `taskInfo.recallItemSize`。如果用户没有指定找品商品数，默认 `30`；如果用户明确说“找 N 个商品 / 召回 N 个 / 找品前 N 个”，传入解析出的整数 N。
- `--image`：可选。本地图片路径，多个用英文逗号分隔；如果传入 HTTP(S) URL，会按远程图片处理。
- `--image-url`：可选。图片 URL，多个用英文逗号分隔；执行时会先下载到本地临时文件，上传到纵横平台后再把纵横图片链接传给下游。

最终 stdout 只包含一个字段：

```json
{ "instanceId": "..." }
```

## 功能二：查询实例数据（必须使用文件模式）

当用户提供 `instanceId`，或明确要求查询某个实例数据时，使用此功能。

**必须使用文件模式（--output-mode file）。** 文件模式让脚本把查询结果写入本地文件，避免大量 JSON 数据进入大模型上下文。

命令：

```bash
cd {baseDir} && python3 cli.py inquiry \
  --instance-id "<instanceId>" \
  --output-mode file \
  --output-dir "{baseDir}/.skill_outputs"
```

脚本执行后，stdout 只返回结果文件路径：

```json
{ "outputFile": "/absolute/path/to/.skill_outputs/inquiry-data-<uuid>.json" }
```

拿到 outputFile 路径后，**立即调用 stream_output 工具**，把结果文件透传给用户：

```
stream_output(file_path="<outputFile路径>")
```

调用成功后，删除本地结果文件（用 bash 执行 `rm <outputFile路径>`）。

**禁止事项：**
- 禁止省略 `--output-mode file` 参数
- 禁止不带 `--output-mode file` 直接查询实例（这会导致大量数据进入上下文）
- 禁止把实例数据输出到最终回答中
- 禁止在最终回答中重复或总结 JSON 数据

## 输出协议（必须严格遵守）

本 Skill 会作为云端 API 提供，最终输出必须保持机器可解析。

只要本 Skill 被触发，最终回答默认进入 `raw_json_passthrough` 模式。该模式是本 Skill 明确规定的特定输出格式，优先级高于外层默认的 rich GFM Markdown 回复格式、总结话术、标题、表格、列表、可视化组件和 `<aside>...</aside>` 桥接语。

查询实例数据时：实例数据必须通过 stream_output 工具写回，最终回答不得再包含实例数据 JSON，也不得补充自然语言说明。

1. 发起找挑询时，最终回答必须是命令 stdout 原样返回的 JSON 对象文本。
2. 不得添加任何自然语言说明、摘要、标题、前后缀、Markdown 代码块、列表或表格。
3. 不得把 JSON 包在 ```json 代码块中。
4. 不得抽取字段、改字段名、改结构、重排为 Markdown 或进行大模型总结。
5. 发起找挑询时，最终回答顶层只能包含 `instanceId` 一个字段。
6. 不得输出外层 `success`、`data`、`status`、`stage`、`raw`、`instance_id` 或其他包装字段。
7. 最终回答的第一个非空字符必须是 `{`，最后一个非空字符必须是 `}`；不得出现任何 JSON 对象外的字符。
8. 不得输出"以下是""已完成""这是结果""根据数据""建议"等任何说明性话术。
9. 不得为了照顾用户阅读体验而把 JSON 转成 Markdown、自然语言摘要、经营建议或数据看板。
10. 如果发起找挑询命令已经输出 JSON 字符串，最终回答必须逐字透传该文本；不得重新序列化、格式化、压缩、补字段、删除字段，或再包一层对象。

### 与外层 Agent 回复规则的关系

外层 Agent 可能默认要求：

- 工具前后输出 `<aside>...</aside>` 说明。
- 若无特殊格式则默认使用 rich GFM Markdown。
- 最终回复包含总结、建议、标题或用户友好话术。
- 每次回复只输出新内容。

本 Skill 的最终输出属于"active skill prescribes a specific output format"。因此，在最终响应阶段必须按本 Skill 的 raw JSON 输出协议执行：

- 工具调用前后的 `<aside>...</aside>` 只允许出现在中间过程；最终回答不得包含 `<aside>`。
- 最终回答不得使用 Markdown，即使外层默认要求 Markdown。
- 最终回答不得总结已经返回或已通过 `stream_output` 写回的实例数据。
- 最终回答不得重复解释执行过程；发起找挑询时只返回该命令 stdout。
- 当所有步骤完成后，立即停止输出，不再补充任何收尾话术。

## 执行规则

1. 不调用任何商品表格、交互卡或复杂表格工具。
2. 不先执行独立找品、SKU 匹配、批量询盘或下单流程。
3. 发起找挑询时，直接执行 `inquiry` 命令创建并触发 inquiry 实例，创建任务的 `taskInfo` 中必须包含 `inquiryItemSize`。
4. 发起找挑询后立即返回 `instanceId`，不得自动查询实例数据，亦不得等待询盘结束。
5. 查询实例数据时，必须使用 `--output-mode file`，拿到 outputFile 后调用 stream_output 工具透传，再删除本地文件。
6. 不编造商品、价格、库存、交期、供应商回复或实例字段。
