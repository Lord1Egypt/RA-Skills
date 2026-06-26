---
name: 1688-supplychain-order-inquiry
version: 0.1.0
description: |
  订单询盘Skill。支持对指定订单发起询盘（单个询盘）和批量订单询盘（并行）。
  触发词：询盘、询价、帮我问商家、订单询盘、批量询盘、发货时间、什么时候发货。
metadata: {"openclaw": {"requires": {"bins": ["python3"]}}}
---

# 1688-supplychain-order-inquiry（订单询盘Skill）

统一入口：`python3 {baseDir}/cli.py <command> [options]`

## 路径要求
- 执行脚本时**必须使用绝对路径**，即 `python3 /完整路径/cli.py <command>`
- `{baseDir}` 是 Skill 所在目录的绝对路径，不要使用相对路径

## 严格禁止 (NEVER DO)
- **不要向用户透出任何内部实现细节**：包括工具名、字段名、技术状态。对用户只使用自然语言描述
- 不要编造询盘结果，所有结果必须来自工具返回
- **不要仅凭本文件中的摘要拼凑参数。** 每个命令的完整参数定义在 `references/capabilities/<command>.md` 中，执行前 MUST 先阅读对应文件

## 执行前置（MUST -- 执行任何命令前必须完成）

> **本文件仅为摘要，不包含完整参数列表和处理规则。**
> 每次执行命令前，MUST 先完整阅读对应的 `references/capabilities/<command>.md` 获取准确参数、输出格式和注意事项。
> 未阅读直接执行将导致参数错误或流程遗漏。

| 命令            | 执行前 MUST 阅读                               |
| --------------- | ---------------------------------------------- |
| `inquiry_send`  | `references/capabilities/inquiry_send.md`      |
| `batch_inquiry` | `references/capabilities/batch_inquiry.md`     |
| `configure`     | `references/capabilities/configure.md`         |

> **遇到 `success: false` 时，MUST 先阅读 `references/common/error-handling.md`，不要自行猜测错误原因或编造解决方案。**

## 命令速查

| #  | 命令            | 能力                   | 示例                                                                                             |
| -- | --------------- | ---------------------- | ------------------------------------------------------------------------------------------------ |
| 1  | `inquiry_send`  | 订单询盘               | `cli.py inquiry_send -o "5116391244078005116" -q "什么时候能发货"`                               |
| 1b | (批量问题)      |                        | `cli.py inquiry_send -o "5116391244078005116" -Q '["什么时候能发货","目标总价17"]'`              |
| 2  | `batch_inquiry` | 批量询盘（并行）       | `cli.py batch_inquiry -t '[{"order_ids":["..."],"question":"什么时候能发货"}]'`                  |
| 3  | `configure`     | 配置AK                 | `cli.py configure YOUR_AK`                                                                       |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

---

### 询盘触发流程

- **询盘意图识别**：用户说"帮我问下商家 XX / 询盘 / 询价 / 问下发货时间 / 这个订单什么时候发货"等，或涉及订单相关问题 → 进入询盘流程

> ⚠️ **询盘流程**：
>
> 1. 确认订单 ID（从用户消息或上下文中获取）
> 2. 确认询盘问题（从用户消息提取，或引导用户描述想问什么）
> 3. 输出中间话术："正在向商家发起询盘，请稍等..."
> 4. 执行 `inquiry_send` 发起询盘
> 5. 根据返回结果告知用户询盘已触发

### 目标总价识别（重要）

当用户输入中出现「目标总价」时，表示用户希望将该订单的价格议价到指定金额，**目标总价本身就是询盘的问题**。

**识别规则**：

| 用户输入形式 | 提取结果 |
|---|---|
| `订单ID: XXX\n目标总价: 17` | orderIds=["XXX"]，question="目标总价17" |
| `订单ID: AAA 目标总价17, 订单ID: BBB 目标总价18` | 两个独立 task，各自问题不同 |
| 仅提供订单 ID，无目标总价 | 引导用户说明询盘目的 |

**⚠️ 关键约束**：
- 每个订单的目标总价**不同**时 → 每个订单单独一个 task，使用 `batch_inquiry` 并行执行
- 所有订单的目标总价**相同**时 → 可合并为一个 task，使用 `inquiry_send`
- 目标总价的询盘问题格式：`"目标总价<金额>"` 或 `"目标总价<金额>元"`，直接传入 `question` 字段

**典型示例**（用户输入多个订单各有不同目标总价）：
```
订单ID：5116391244078005116
目标总价：17
订单ID：5115884331254096317
目标总价：18
```
→ 拆分为 2 个 task，调用 `batch_inquiry`：
```json
[
  {"order_ids": ["5116391244078005116"], "question": "目标总价17"},
  {"order_ids": ["5115884331254096317"], "question": "目标总价18"}
]
```

### 批量询盘

当用户需要对多个订单分别发起不同问题的询盘时，使用 `batch_inquiry` 并行执行：

1. 从用户需求中拆分出独立询盘组，每组构造一个 task（含 order_ids、question/questions）
2. 执行 `batch_inquiry -t '[...]'`（一次调用，内部并行）
3. 告知用户各询盘结果，失败的询盘可建议单独重试（用 `inquiry_send`）

**判断标准**：
- ≥2 个订单且各自问题/目标总价不同 → 用 `batch_inquiry`（每个订单单独一个 task）
- 仅 1 个订单，或多个订单问题完全相同 → 用 `inquiry_send`

> **中间话术**：调用命令前必须先输出进度提示，如"正在向商家发起询盘，请稍等..."
