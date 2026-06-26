---
name: skill-generator
description: 自然语言描述需求，AI自动生成可复用的Skill。用于：(1)根据需求创建新Skill (2)生成Skill结构 (3)批量生成Skill模板。触发词：创建skill、生成skill、做一个skill
---

# Skill生成器

将自然语言需求转换为标准Skill结构。

## 核心功能

- **需求解析**: 理解用户描述的功能需求
- **结构生成**: 自动生成Skill的name、description、body
- **预览编辑**: 生成后可预览和修改
- **一键保存**: 确认后保存到Skill库
- **自动发布**: 一键发布到ClawHub和GitHub

## 使用方法

### 基本用法

直接告诉SC你想要创建的Skill，例如：

- "帮我创建一个查天气的skill"
- "生成一个可以自动写代码注释的skill"
- "做一个管理提醒事项的skill"
- "创建一个skill：自动总结YouTube视频"

### 生成流程

1. **描述需求**: 用自然语言描述你想要的功能
2. **LLM解析**: 系统分析需求，提取关键信息
3. **生成结构**: 自动生成Skill的name、description、body
4. **预览确认**: 展示生成的Skill供你预览
5. **保存部署**: 确认后保存到Skill库
6. **发布分享**: 可选 - 发布到ClawHub和GitHub

### Skill结构说明

每个Skill包含:

| 字段 | 说明 | 示例 |
|------|------|------|
| **name** | 英文名称(kebab-case) | `weather-query` |
| **description** | 功能描述和触发场景 | "查询天气..." |
| **triggers** | 触发关键词列表 | ["查天气", "weather"] |
| **body** | Markdown使用说明 | 详细功能描述 |

## 发布流程（自动）

当Skill保存后，可以选择发布：

1. **发布到ClawHub**: `clawhub publish <skill-name>`
2. **发布到GitHub**: 自动创建仓库并推送
3. **生成抖音宣传**: 自动创建宣传文案

### 抖音宣传内容模板

发布后自动生成：

```
🎉 新Skill发布！
【Skill名称】
📦 下载: ClawHub/GitHub链接
💡 功能说明
📖 使用方法
#AI #OpenClaw #Skill名称
```

---

## 示例

**用户输入:**
> "我需要一个查天气的skill"

**生成的Skill:**
```yaml
---
name: weather-query
description: 查询全球城市天气和预报。使用场景：(1)了解当前天气 (2)查看未来预报 (3)比较不同城市天气
triggers: ["查天气", "天气怎么样", "weather"]
---

# Weather Query

## 功能
- 查询当前天气
- 查看3-7天预报
- 多城市对比

## 使用方式
直接告诉SC:"查北京天气"或"上海明天天气怎么样"
```

---

## 底层实现

如需直接调用生成器:

```bash
python ~/.openclaw/workspace/skills/skill-generator/scripts/generate.py "用户需求"
```

生成器会:
1. 调用LLM解析需求
2. 生成标准JSON结构
3. 转换为SKILL.md格式
4. 保存到 skills/ 目录
5. 可选：发布到ClawHub和GitHub
