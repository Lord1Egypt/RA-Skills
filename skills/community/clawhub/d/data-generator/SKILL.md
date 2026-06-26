---
name: data-generator
description: 训练数据生成技能。根据传入的工具名和用户指令列表，生成多轮对话格式的 JSONL 训练数据。触发场景：(1) 传入工具名和用户指令列表，生成完整训练数据；(2) 批量生成指定工具的标注数据；(3) 给定指令列表，输出 JSONL 对话样本。
---

# Data Generator

将用户指令列表转换为标准 JSONL 训练数据。

## 输入

两个必填参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| `tool_name` | string | 工具名，如 `dev_control`、`scene_generator`、`weather` |
| `user_instructions` | string[] | 用户指令列表，如 `["5分钟后打开空调", "3分钟后关灯"]` |

## 输出 JSONL 格式

```json
{"conversations":[
  {"from":"human","value":"<当前用户指令>打开客厅空调</当前用户指令>\n<本地设备>格力冷静王(空调)</本地设备>\n<当前时间>2026-03-15 14:22:47</当前时间>\n<用户场景列表>[{\"scene_id\":1001,\"scene_name\":\"回家模式\",\"room_name\":\"全屋\"},{\"scene_id\":1002,\"scene_name\":\"睡眠模式\",\"room_name\":\"主卧\"}]</用户场景列表>\n<用户设备列表>{\"客厅\":[\"格力冷静王(空调)\",\"洗碗机A1(洗碗机)\"],\"主卧\":[\"美的舒省风(空调)\"]}</用户设备列表>"},
  {"from":"assistant","value":"<tool_call>{\"tool_name\":\"dev_control\",\"query\":\"打开客厅空调\"}</tool_call>"},
  {"from":"observation","value":"<tool_response>客厅空调已打开</tool_response>"},
  {"from":"assistant","value":"好的，客厅空调已经打开啦~"}
],"system":"","history":[]}
```

## 格式规则

1. **human value** = 完整上下文，格式固定：
   ```
   <当前用户指令>用户原始指令</当前用户指令>
   <本地设备>设备名(类型)</本地设备>
   <当前时间>YYYY-MM-DD HH:mm:ss</当前时间>
   <用户场景列表>[{"scene_id":xxx,"scene_name":"场景名","room_name":"房间名"},...]</用户场景列表>
   <用户设备列表>{"房间":["设备名(类型)",...]}</用户设备列表>
   ```
2. **assistant tool_call** = 直接输出 tool_call 标签，**无垫音前缀**
3. **observation** = `<tool_response>...</tool_response>` 或 `<tool_call>{...}</tool_call>`（dev_info/weather 等工具）
4. **assistant 终接回复** = 直接回复内容，**无垫音前缀**
5. **system = ""**，**history = []**

## 工作流

```
1. 接收 tool_name + user_instructions[]
         ↓
2. 加载提示词：通用要求 + 工具特定要求（references/tools/{tool}.txt）
         ↓
3. 将 user_instructions 注入提示词
         ↓
4. 生成 JSONL（每条独立）
         ↓
5. 输出 .jsonl 文件
```

## 提示词拼接

拼接规则：
```
[通用要求]
# ═══════════════════════════════════════════════════════════════════
# 【工具特定要求】
# 本次只调用：{TOOL_NAME}
# ────────────────────────────────────────────────────────────────
[references/tools/{TOOL_NAME}.txt 内容]
```

拼接脚本：`scripts/build_prompt.py`

## 工具与文件对照

| 工具 | 要求文件 |
|------|---------|
| `dev_control` | `references/tools/dev_control.txt` |
| `scene_generator` | `references/tools/scene_generator.txt` |
| `alarm_remind` | `references/tools/alarm_remind.txt` |
| `weather` | `references/tools/weather.txt` |
| `scene_control` | `references/tools/scene_control.txt` |
| `dev_info` | `references/tools/dev_info.txt` |
| `exit_dialog` | `references/tools/exit_dialog.txt` |
| `GreeQA` | `references/tools/GreeQA.txt` |
| `scene_guide` | `references/tools/scene_guide.txt` |
| `chat` | `references/tools/chat.txt` |

## 使用示例

**输入：**
```
tool_name: "dev_info"
user_instructions: ["家里空调数量", "有几个空调"]
```

**输出字段说明：**

| 字段 | 说明 |
|------|------|
| `conversations[0].value` | 含 `<当前用户指令>` + 完整上下文 |
| `conversations[1].value` | `<tool_call>{"tool_name":"dev_info"}</tool_call>` |
| `conversations[2].value` | dev_info 返回结果（设备列表） |
| `conversations[3].value` | 文字终接回复 |
| `system` | 空字符串 `""` |
| `history` | 空数组 `[]` |

## BUG 修复数据

当传入 `tool_name` 为修复后的正确工具时，生成的数据应体现：
- 工具调用格式正确（符合工具要求文件）
- query 字段格式正确（如延时类指令含 `timing` 字段）
- 文字回复符合预期（含延时时间描述）

具体格式参考：`references/tools/scene_generator.txt`。
