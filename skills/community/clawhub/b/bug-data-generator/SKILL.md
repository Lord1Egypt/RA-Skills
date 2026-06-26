---
name: bug-data-generator
description: 根据 BUG 描述生成对应的工具名和用户指令列表，供用户审核确认后再调用 data-generator 生成完整 JSONL 训练数据。触发场景：(1) 输入 BUG 描述，获取应调用的工具和触发指令列表；(2) 确认指令后自动调用 data-generator；(3) BUG 数据生成的中间步骤。
---

# Bug Data Generator

将 BUG 描述转换为可用的训练指令序列。

## 工作流

```
用户: BUG描述 + 错误原因
        ↓
Agent: 分析 BUG → 确定工具 + 生成用户指令列表
        ↓
用户: 审核指令列表（可修改/补充/删除）
        ↓
用户: 确认 "没问题，生成数据"
        ↓
调用 data-generator → 输出 JSONL（新格式）
```

## 第一步：分析 BUG

输入以下信息，自动推断：

| 字段 | 说明 | 示例 |
|------|------|------|
| BUG 描述 | 用户的实际指令 + 系统的错误行为 | "用户说X分钟后开空调，系统却立即执行" |
| 错误原因 | 为什么错 + 正确工具 | "调用了 dev_control 而应该调用 scene_generator" |

## 第二步：生成指令列表

输出内容：

```
工具: scene_generator

用户指令列表:
  1. 5分钟后打开空调
  2. 3分钟后关灯
  3. 10分钟后开启空气净化器
  ...（共 N 条）
```

**发送给用户确认，等待回复。**

## 第三步：用户修改指令

用户可直接回复修改意见：
- "把第3条改成 `20分钟后打开加湿器`"
- "删除第5条"
- "补充5条延时类指令"
- "指令没问题，生成数据"

## 第四步：调用 data-generator

收到确认后，使用最终版指令列表，调用 data-generator v2.0.0（**新格式**）：

**输入参数：**
```
tool_name: scene_generator
user_instructions: [确认后的完整列表]
```

**输出 JSONL（新格式）：**
```json
{
  "conversations": [
    {"from": "human", "value": "<当前用户指令>5分钟后打开空调</当前用户指令>\n<本地设备>舒享家(空调)</本地设备>\n<当前时间>2026-03-21 20:00:00</当前时间>\n<用户场景列表>[...]</用户场景列表>\n<用户设备列表>{...}</用户设备列表>"},
    {"from": "assistant", "value": "<tool_call>{\"tool_name\":\"scene_generator\",\"query\":\"...\"}</tool_call>"},
    {"from": "observation", "value": "<tool_response>场景创建成功。</tool_response>"},
    {"from": "assistant", "value": "好的，5分钟后准时执行~"}
  ],
  "system": "",
  "history": []
}
```

## 格式规则（新格式）

1. `conversations[0].value` = 完整上下文（`<当前用户指令>` + `<本地设备>` + `<当前时间>` + `<用户场景列表>` + `<用户设备列表>`）
2. `conversations[1].value` = tool_call，**无垫音前缀**
3. `conversations[2].value` = `<tool_response>...</tool_response>`
4. `conversations[3].value` = 终接回复，**无垫音前缀**
5. `system = ""`，`history = []`

## 指令模板参考

生成时可参考以下模板类型：

| 类型 | 模板示例 |
|------|---------|
| 延时-分钟 | `{N}分钟后打开{D}` |
| 延时-秒 | `{N}秒后关闭{D}` |
| 延时-小时 | `{H}小时后开{D}` |
| 定时-今天 | `今天{H}点打开{D}` |
| 定时-明天 | `明天{H}点关{D}` |
| 循环-每天 | `每天{H}点打开{D}` |
| 设备开关 | `打开{D}`、`把{D}关闭` |

## 输出格式（第一步）

```json
{
  "tool_name": "scene_generator",
  "instruction_count": 20,
  "instructions": [
    {"id": 1, "text": "5分钟后打开空调", "type": "延时-分钟"},
    {"id": 2, "text": "3分钟后关灯", "type": "延时-分钟"}
  ],
  "note": "以上为由 AI 根据 BUG 分析生成的指令列表，请审核或修改后确认，确认后调用 data-generator 生成 JSONL。"
}
```

## 注意

- **不依赖 data-generator 内部实现**：仅输出中间产物（工具名 + 指令列表）
- **可迭代**：用户可多轮修改指令，直到满意再生成
- data-generator 升级时，bug-data-generator 无需更新
