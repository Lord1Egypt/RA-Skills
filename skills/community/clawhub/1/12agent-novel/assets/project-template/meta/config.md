# 模型分工与项目配置

> ⚠️ **格式要求：** 模型值必须使用 `provider/model-id` 格式（如 `anthropic/claude-opus-4-6`、`openai/gpt-4o`）。自然语言名称不能直接写入配置文件。

## 模型分配

| 角色 | 模型 | 职责 |
|------|------|------|
| 主控/协调 | （当前会话模型，无需填写） | 整体调度、存档管理、用户汇报 |
| 世界观 | {{worldbuilder_model}} | 世界观构建 |
| 角色设计 | {{characterDesigner_model}} | 角色圣经与关系网设计 |
| 全书大纲 | {{outlinePlanner_model}} | 三幕结构与主支线规划 |
| 章节细纲 | {{chapterOutliner_model}} | 章节细纲规划 |
| 主笔/初稿 | {{mainWriter_model}} | 完成章节初稿 |
| 润色/氛围 | {{mainWriter_model}} | 优化语言、氛围、感官细节 |
| OOC守护 | {{oocGuardian_model}} | 一致性检查（常规章节抽样+条件触发） |
| 战斗/动作 | {{battleAgent_model}} | **仅高强度/复杂战斗，详见战斗调用条件** |
| 终稿三审 | {{finalReviewer_model}} | 逻辑/情感/节奏/语言终审 |
| 读者模拟 | {{readerSimulator_model}} | 读者视角反馈 |
| 风格锚定 | {{styleAnchorGenerator_model}} | 风格锚定生成 |
| 滚动摘要 | {{rollingSummarizer_model}} | 滚动摘要压缩 |

## 关键章节配置（动态生成）

| 字段 | 内容 |
|------|------|
| key_chapters | {{key_chapters}} |
| act_boundaries | {{act_boundaries}} |
| total_chapters | {{total_chapters}} |
| batch_mode | false |

## 自动推进配置（默认）

| 字段 | 默认值 | 说明 |
|------|--------|------|
| auto_advance_chapters | 4 | 一次自动写4章 |
| write_interval_seconds | 6 | API缓冲 + 阅读思考时间 |
| auto_confirm | false | 保留手动安全感 |

## 备选模型配置（回退链）

> 当主模型拒绝/故障/超时时，Coordinator 按此回退链切换。详见 `references/model-fallback-strategy.md`。

| Agent | 主模型 | 备选模型 |
|-------|--------|----------|
| MainWriter | {{mainWriter_model}} | （填写备选 provider/model-id，如无则留空） |
| FinalReviewer | {{finalReviewer_model}} | {{oocGuardian_model}}（自动回退到 OOCGuardian 模型） |
| OOCGuardian | {{oocGuardian_model}} | Coordinator 自行处理 |
| ReaderSimulator | {{readerSimulator_model}} | 跳过（不阻断） |
| RollingSummarizer | {{rollingSummarizer_model}} | Coordinator 自行处理 |

> **提示：** Phase 0 初始化后，请在 MainWriter 一行填入备选模型，避免写作中途因模型故障中断。

---

## 战斗Agent调用条件

满足以下任一条件时调用战斗Agent：
- 细纲/本章规划标注"高强度/复杂/多方战斗"
- 需要专业动作/物理/兵器描写
- 大规模战役场景

不满足上述条件时，战斗描写由主笔完成。
