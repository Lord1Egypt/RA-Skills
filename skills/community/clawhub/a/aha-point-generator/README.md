# AhaPoint Generator Skill v1.0

按 **AhaPoints Protocol v1.0 (APS v1.0)** 标准，自动生成带确权元数据的独立 AhaPoint 报告。

---

## 快速开始

### 基础用法

```
"帮我生成一个关于减肥的 aha point"
"挖掘远程办公领域的痛点"
"找 3 个教育领域的妙点"
"按 APS v1.0 标准生成一个关于 XXX 的报告"
```

### 指定类型

```
"帮我找一个减肥领域的痛点🔴"
"有什么 AI+ 健身的妙点🟢"
"来点好玩的乐点🟡"
```

### 格式化已有想法

```
"把这个想法转成 AhaPoint 格式：
  我每次点外卖都不知道多少热量，太难了"
```

### 批量生成

```
"生成减肥领域的 3 个 aha points（痛点 + 妙点 + 乐点）"
"挖掘远程办公领域的 5 个痛点"
```

---

## 输出示例

### 生成的文件

```
ahapoints-protocol/points/
├── 20260305-1600-PAIN-打工人外卖热量盲区.md
├── 20260305-1605-INNO-AI 拍小票估算热量.md
└── 20260305-1610-FUN-外卖热量吐槽大会.md
```

### 报告内容

每个报告包含：
1. **APS v1.0 元数据块**（YAML 格式）
   - 唯一 ID: `ap-{domain}-{YYYYMMDD}-{HHMMSS}-{random4}`
   - 时间戳（ISO 8601 + 时区）
   - SHA-256 内容哈希
   - 作者信息
   - 版本历史
   - 引用关系
2. **7 部分标准模板**
   - 点类型（🔴/🟢/🟡）
   - 一句话描述
   - 场景故事（200-500 字）
   - 为什么重要
   - 潜在方案方向
   - 验证方法（可执行）
   - 元数据表
3. **Mermaid 知识图谱**
4. **优先权声明**

---

## APS v1.0 确权标准

### 元数据字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 全局唯一标识 | `ap-diet-20260305-160000-p1a2` |
| `type` | 点类型 | `PAIN` / `INNO` / `FUN` |
| `timestamps` | 时间戳组 | created/published/updated |
| `hash` | SHA-256 哈希 | 64 位十六进制 |
| `author` | 作者信息 | name/identifier/contact |
| `version` | 版本追踪 | 语义化版本 (1.0.0) |
| `relations` | 引用关系 | supersedes/related_to 等 |

### 文件命名

```
YYYYMMDD-HHMM-[TYPE]-[标题].md

示例:
20260305-1600-PAIN-打工人外卖热量盲区.md
20260305-1605-INNO-AI 拍小票估算热量.md
20260305-1610-FUN-外卖热量吐槽大会.md
```

---

## 三种模式

### 模式 A: 单点深度生成（默认）

聚焦 1 个点，深入调研，完整 APS v1.0 元数据。

**适用场景**:
- 有明确想探索的具体问题
- 需要高质量、可确权的报告
- 准备认真验证和跟进

**示例**:
```
"帮我深入分析一下外卖热量估算这个问题"
```

### 模式 B: 多点批量生成

某领域生成 3-5 个点，快速探索。

**适用场景**:
- 刚进入新领域，想快速了解
- 头脑风暴，寻找方向
- 积累点子库

**示例**:
```
"挖掘减肥领域的 5 个 aha points"
```

### 模式 C: 用户输入转标准

用户提供零散想法，整理成标准 APS v1.0 格式。

**适用场景**:
- 已有洞察，需要规范化
- 快速记录，避免遗忘
- 团队协作，统一格式

**示例**:
```
"把这个转成 AhaPoint：
  减肥餐太难吃了，坚持不了一周"
```

---

## 工作流程

```
1. 确认需求（领域/类型/模式）
   ↓
2. 网络调研（browser 搜索）
   ↓
3. 生成 APS v1.0 元数据
   - 唯一 ID
   - 时间戳
   - SHA-256 哈希
   - 作者信息
   - 版本和关系
   ↓
4. 填充 7 部分模板
   ↓
5. 生成 Mermaid 知识图谱
   ↓
6. 保存文件 + 更新注册表
   ↓
7. 质量复核 + 用户确认
```

---

## 依赖工具

- **必需**: `browser` 工具（用于网络调研）
- **必需**: `ahapoints-protocol` 目录（用于存储输出）
- **可选**: Git（用于版本控制和增强确权）

无需 API key，使用 browser 工具直接搜索。

---

## 与 painpoint-discovery 的区别

| 维度 | painpoint-discovery | aha-point-generator |
|------|---------------------|---------------------|
| **输出** | 综合分析报告 | 独立 AhaPoint 报告 |
| **格式** | 自定义结构 | AhaPoints Protocol v1.0 |
| **类型** | 仅痛点 | 痛点 + 妙点 + 乐点 |
| **确权** | 无 | APS v1.0 完整元数据 |
| **图谱** | 无 | Mermaid 知识图谱 |
| **用途** | 创业方向调研 | 点子记录 + 优先权确权 |
| **文件** | 1 份综合报告 | 多个独立报告 |

**选择建议**:
- 想快速了解某领域 → `painpoint-discovery`
- 想记录具体洞察并确权 → `aha-point-generator`
- 两者可以配合使用

---

## 最佳实践

### ✅ 好的 AhaPoint

- **具体场景**: 有明确的人物、时间、地点
- **真实问题**: 来自真实抱怨，不是臆想
- **可验证**: 验证方法可立即执行
- **清晰简洁**: 一句话描述 20 字以内
- **完整元数据**: APS v1.0 所有字段齐全

### ❌ 避免

- 泛泛而谈："XX 领域很大"
- 伪需求："用户想要更好的体验"
- 不可验证："需要市场调研"
- 过于复杂：模板填不完
- 元数据缺失：缺少哈希、时间戳等

---

## 发布到 ClawHub

```bash
cd /Users/olivia/.openclaw/workspace/skills/aha-point-generator
clawhub publish . --slug aha-point-generator --name "AhaPoint 生成专家" --version 1.0.0
```

---

## 版本历史

### v1.0.0 (2026-03-05)
- 完整实现 APS v1.0 确权标准
- 支持三类点生成（🔴/🟢/🟡）
- 内置完整元数据（ID/时间戳/哈希/作者/版本/关系）
- 自动生成 Mermaid 知识图谱
- 自动保存到 `ahapoints-protocol/points/`
- 自动更新注册表 `registry/index.json`
- 三种输出模式（单点/批量/格式化）
- Browser 工作流（无需 API）

---

## 相关链接

- [AhaPoints Protocol v1.0](../../ahapoints-protocol/AHAPOINTS-PROTOCOL-v1.0.md)
- [示例报告](../../ahapoints-protocol/points/)
- [知识图谱](../../ahapoints-protocol/graphs/)
- [注册表](../../ahapoints-protocol/registry/index.json)
- [Painpoint Discovery Skill](../painpoint-discovery/)

---

*Skill 遵循 CC-BY-4.0 许可，欢迎 Fork 和贡献。*
