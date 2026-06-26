---
name: book-translator
description: 使用平台内置文本翻译技能，对整本书或长文本进行自动分段翻译
metadata:
  clawdbot:
    emoji: "📚"
    category: "translation"
---

# 📚 全书翻译 (Book Translator)

这个 Skill 可以将 **整本书或长文本内容自动拆分并翻译**。

由于大模型存在 token 限制，本技能会：

1. 读取整本书文本  
2. 自动拆分为多个小段  
3. 调用平台内置 **文本翻译 Skill**  
4. 将所有翻译结果合并  
5. 输出完整译文  

适用于：

- PDF 书籍  
- TXT 文本  
- 长文章  
- 电子书内容  
- 长报告  

---

# 工作流程

完整流程如下：

## 1 读取书籍内容

Agent 获取用户提供的文本或文件内容。

---

## 2 自动拆分文本

为了避免超过模型 Token 限制，系统会将文本拆分为多个片段。

示例：

原始文本

↓

Chunk 1  
Chunk 2  
Chunk 3  
Chunk 4  

---

## 3 调用平台内置翻译 Skill

对每个片段调用：

text_translate

示例调用：

text_translate(
  text=chunk,
  target_language="Chinese"
)

---

## 4 合并翻译结果

所有翻译片段将被合并为完整译文：

translated_chunk1  
translated_chunk2  
translated_chunk3  

最终输出：

完整翻译文本

---

# 使用方式

用户可以直接对 Agent 说：

请把这本书翻译成中文

或者：

translate this book to Chinese

如果用户提供文本：

把下面这本书翻译成中文：
[书籍内容]

Agent 会自动执行：

1. 读取文本  
2. 自动拆分  
3. 调用翻译  
4. 合并结果  

---

# 支持的文件类型

本 Skill 可以处理：

TXT  
PDF  
Markdown  
长文本  

如果是 PDF：

Agent 需要先提取文本，再执行翻译。

---

# 分段翻译策略

为了保证稳定性，本 Skill 使用 **自动分段翻译策略**。

推荐分段大小：

1000 - 2000 字符

流程示例：

长文本  
↓  
拆分  
↓  
chunk1  
chunk2  
chunk3  
↓  
逐段翻译  
↓  
合并  

这样可以：

- 防止 Token 超限  
- 提高翻译稳定性  
- 降低失败概率  

---

# 翻译规则

调用翻译 Skill 时，遵循以下规则：

1. 保留原文段落结构  
2. 不省略内容  
3. 不总结  
4. 忠实翻译原文  
5. 保留专有名词  

---

# 示例流程

输入：

Translate this book into Chinese.

Agent 执行流程：

读取文本  
↓  
拆分文本  
↓  
调用 text_translate  
↓  
翻译 chunk1  
翻译 chunk2  
翻译 chunk3  
↓  
合并译文  
↓  
输出完整翻译  

---

# 示例输出

第一章：人工智能的起源  

人工智能的概念最早可以追溯到……  

第二章：机器学习的发展  

随着计算能力的提升……

---

# 推荐使用场景

这个 Skill 适用于：

- 翻译整本书  
- 翻译研究论文  
- 翻译技术文档  
- 翻译课程资料  
- 翻译长报告  

---

# 注意事项

1. 如果文本过长，系统会自动拆分。  
2. 如果翻译中断，可以重新继续。  
3. 翻译质量取决于所调用的大模型。  

