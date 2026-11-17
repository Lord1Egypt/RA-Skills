# 语言学习卡完整流程（Language Learning Card Workflow）

> **本文件是精简版工作流。**  
> 完整的执行流程请参考：[base-card-workflow.md](base-card-workflow.md)

---

## 快速导航

- **完整执行流程：** [base-card-workflow.md](base-card-workflow.md)
- **领域特定规则：** [domain-configs/language-card-config.md](domain-configs/language-card-config.md)
- **完整版（已归档）：** [legacy/language-card-workflow.md](legacy/language-card-workflow.md)

---

## 领域定位

> **覆盖范围：** 单字、词汇、语法、短语、发音、翻译等语言学习内容。
> 
> **不覆盖：** 数学公式、编程代码、历史时间线等非语言学习内容。

---

## 🔤 术语说明

| 术语 | 层次 | 含义 |
|------|------|------|
| **`language-card`** | 领域层 | 本工作流的定位，指"语言学习域" |
| **`learning-card`** | 模板层 | 共享模板族名称，提供数据契约和渲染模板 |

**类比：**
- `language-card-workflow.md` = 餐饮业务流程手册
- `learning-card` 模板族 = 餐具套装

---

## 适用场景

支持 6 种卡片类型：
- **character-card** - 单字学习卡
- **vocabulary-card** - 词汇卡
- **grammar-card** - 语法卡
- **phrase-card** - 短语卡
- **pronunciation-card** - 发音卡 ⭐
- **translation-card** - 翻译卡 ⭐

---

## 执行流程

### 使用方式

1. **阅读基础流程：** [base-card-workflow.md](base-card-workflow.md) - 阶段 0-9 完整执行流程
2. **查看领域配置：** [domain-configs/language-card-config.md](domain-configs/language-card-config.md) - 语言学习卡特定规则
3. **应用扩展点：** 在基础流程的 9 个扩展点处，应用 language-card 的特定规则

---

## 领域特定要点

### 输入路由（扩展点 #1）
- 单个汉字 → character-card
- 词汇表 → vocabulary-card
- 语法点 → grammar-card
- 短语列表 → phrase-card
- 发音材料 → pronunciation-card
- 翻译文本 → translation-card

### 硬规则（扩展点 #9）
1. **No Unrequested Exam Labels** - 不得添加 HSK/考试标签（除非明确要求）
2. **Example Sentence Appropriateness** - 例句必须适合目标学习者水平
3. **Pronunciation Accuracy** - pronunciation-card 必须有清晰发音指导
4. **Translation Distinction** - translation-card 必须区分字面翻译和意译

### 执行模式偏好（扩展点 #4）
- 单张预览：`direct_image_preview` 可用
- 批量生成：必须 `engineering_rendering`
- 商用场景：必须 `engineering_rendering`

---

## 内容字段速查

详细字段定义见：[domain-configs/language-card-config.md](domain-configs/language-card-config.md) 扩展点 #5

**Character-card：** character, pinyin, tone, stroke_count, radical, words, example_sentence

**Vocabulary-card：** word, phonetic, part_of_speech, definition, synonyms, collocations

**Grammar-card：** grammar_point, structure, usage_rules, common_mistakes

**Phrase-card：** phrase, literal_meaning, idiomatic_meaning, usage_context

**Pronunciation-card：** target_sound, phonemes, minimal_pairs, articulation_guide

**Translation-card：** source_text, literal_translation, idiomatic_translation, cultural_note

---

## 视觉风格

### Character-card（单字卡）
- 风格：童趣、贴纸感、启蒙友好
- 背景：浅黄 #FFF9E6 / 浅蓝 #E8F4F8
- 主色：柔和色调（低饱和度）

### 其他类型
- 风格：简洁专业、信息层级清晰
- 背景：白色 #FFFFFF / 浅灰 #F8F9FA
- 主色：专业蓝、深灰

---

## 批量生成示例

**场景：** 生成 50 个 GRE 词汇卡（付费课程）

1. 完成 Source Lock（词表 + 学习者水平）
2. 路由到 vocabulary-card
3. 检测：批量 + 商用 → 强制 `engineering_rendering`
4. 对每个单词完成 Content Analysis
5. 准备批量渲染数据包（JSON，50 个卡片）
6. 调用 `engineering_rendering` 批量生成
7. 质量检查（准确性 + 一致性）
8. 输出 50 张卡片（1080×1440）

---

## 架构说明

### 为什么采用精简版？

**旧架构问题：**
- 4 个完整 workflow 文件有 85% 内容重复
- 修改通用逻辑需要同步 4 个文件
- 新增域需要复制 500 行代码

**新架构优势：**
- 通用流程只在 base-card-workflow.md 维护
- 领域特定内容只在 domain-config 维护（50 行）
- 修改通用逻辑自动影响所有域
- 新增域只需添加 50 行配置

---

**版本：** 2.0.0（精简版）  
**基于：** base-card-workflow.md v1.0.0  
**配置文件：** language-card-config.md v1.0.0  
**最后更新：** 2026-06-17
