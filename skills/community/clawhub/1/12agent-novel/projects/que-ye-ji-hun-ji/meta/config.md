# 模型分工与项目配置

> ⚠️ **格式要求：** 模型值必须使用 `provider/model-id` 格式。

## 模型分配

| 角色 | 模型 | 职责 |
|------|------|------|
| 主控/协调 | （当前会话模型，无需填写） | 整体调度、存档管理、用户汇报 |
| 主笔/初稿 | infini-ai/deepseek-v3.2 | 完成章节初稿 |
| 润色/氛围 | infini-ai/deepseek-v3.2 | 优化语言、氛围、感官细节 |
| OOC守护 | qwencode/qwen3.5-plus | 一致性检查 |
| 战斗/动作 | qwencode/qwen3-max-2026-01-23 | 仅高强度/复杂战斗 |
| 终稿三审 | xinkentao/claude-opus-4-6 | 逻辑/情感/节奏/语言终审 |
| 读者模拟 | infini-ai/deepseek-v3.2-thinking | 读者视角反馈 |
| 风格锚定 | xinkentao/claude-opus-4-6 | 风格锚定生成 |
| 章节细纲 | qwencode/kimi-k2.5 | 章节细纲规划 |
| 世界观 | xinkentao/claude-opus-4-6 | 世界观构建 |
| 角色设计 | xinkentao/claude-opus-4-6 | 角色设计 |
| 大纲规划 | xinkentao/claude-opus-4-6 | 大纲规划 |
| 滚动摘要 | minimax/MiniMax-M2.7-highspeed | 滚动摘要压缩 |

## 关键章节配置（动态生成）

| 字段 | 内容 |
|------|------|
| key_chapters | [1, 10, 11, 25, 26, 38] |
| act_boundaries | { "第一幕": [1, 10], "第二幕": [11, 25], "第三幕": [26, 38] } |
| total_chapters | 38 |
| batch_mode | false |

## 备选模型配置（回退链）

> 当主模型拒绝/故障/超时时，Coordinator 按此回退链切换。详见 `references/model-fallback-strategy.md`。

| Agent | 主模型 | 备选模型 |
|-------|--------|----------|
| MainWriter | infini-ai/deepseek-v3.2 | qwencode/kimi-k2.5 |
| FinalReviewer | xinkentao/claude-opus-4-6 | qwencode/qwen3.5-plus（自动回退到 OOCGuardian 模型） |
| OOCGuardian | qwencode/qwen3.5-plus | Coordinator 自行处理 |
| ReaderSimulator | infini-ai/deepseek-v3.2-thinking | 跳过（不阻断） |
| RollingSummarizer | minimax/MiniMax-M2.7-highspeed | Coordinator 自行处理 |

> **提示：** Phase 0 初始化后，请在 MainWriter 一行填入备选模型，避免写作中途因模型故障中断。

## 自动推进配置（默认）

| 字段 | 默认值 | 说明 |
|------|--------|------|
| auto_advance_chapters | 4 | 一次自动写4章 |
| write_interval_seconds | 6 | API缓冲 + 阅读思考时间 |
| auto_confirm | false | 保留手动安全感 |

## 战斗Agent调用条件

满足以下任一条件时调用战斗Agent：
- 细纲/本章规划标注"高强度/复杂/多方战斗"
- 需要专业动作/物理/兵器描写
- 大规模战役场景

不满足上述条件时，战斗描写由主笔完成。
