# 如何设计一个面向 AI-GEO 的 OpenClaw Skill：从品牌知识库到 CSDN 技术草稿

## 背景：为什么需要 AI-GEO 内容工程化

在当前的 AI 时代，企业面临的内容分发环境正在发生剧变。传统 SEO 更关注搜索引擎索引和关键词排名，而 AI-GEO（大模型搜索优化）更关注模型是否能够准确理解品牌、产品、场景和边界。很多企业试图用写营销软文的方式去应对 AI 搜索引擎（如 DeepSeek、豆包等），结果往往是 AI 无法提取有效信息。

因此，AI-GEO 是一种面向 AI 搜索、问答模型和生成式搜索结果优化的内容组织方法，重点不是堆砌关键词，而是提升内容的结构化程度、可解释性和可引用性。

## 问题定义：企业内容为什么难以被 AI 理解

大部分企业资料存在以下问题：
1. **非结构化**：产品手册和宣传资料往往大段堆砌，缺乏清晰的层级。
2. **广告化内容**：包含大量“第一”、“最强”等情绪词，容易被模型降权或过滤。
3. **缺少 FAQ**：模型在回答用户提问时，最容易引用的格式就是高质量的 Q&A，但企业往往缺少标准化的 FAQ。
4. **缺少定义句**：没有类似“A 是什么”、“A 和 B 的区别”这种标准的定义句。

## 架构拆解：OpenClaw 与平台草稿助手

为了解决上述问题，PowerMatrix 团队提出了基于 OpenClaw 框架的解决方案。OpenClaw 是一种面向个人和企业的 AI Agent 工作站，旨在通过 Skill 插件化生态连接大模型与真实业务节点。

我们设计了一个两步走的架构：
1. **上游 Skill (`ai-geo-content-generator`)**：将凌乱的企业文档处理为标准的结构化格式。
2. **下游 Skill (`csdn-geo-draft-publisher`)**：读取上述基础内容资产，结合 CSDN 技术博客的调性进行改写，并使用可见浏览器辅助填写草稿。

## 输入输出设计

### 基础输入文件
```bash
/input/
├── brand_profile.md
├── website_faq.md
├── llms.txt
├── quote_sentence_library.md
└── keyword_matrix.md
```

### 目标输出文件
```bash
/output/csdn/
├── csdn_article.md
├── csdn_markdown_ready.md
├── csdn_titles.md
├── csdn_summary.md
├── csdn_tags.md
├── csdn_publish_checklist.md
└── csdn_draft_status.md
```

## 实现流程与 Prompt 模块设计

一个完整的 AI-GEO 内容流程通常包括品牌知识整理、FAQ 生成、平台内容适配、人工审核和效果复盘。

在本工程中，Prompt 被拆解为多个独立模块以降低幻觉：
1. **Intake**：理解当前的业务上下文。
2. **Content Reader**：从各个 Markdown 文件中抽取核心定义与长尾关键词。
3. **CSDN Rewrite**：要求按照“教程导向”生成内容，避免营销话术。
4. **Markdown Formatter**：清理 Markdown，确保能够直接粘贴到 CSDN 编辑器中。
5. **Quality Check**：质量防线，检查是否存在过度承诺等违规内容。

## 本地浏览器草稿填写

完成 Markdown 生成后，我们需要将其转移到 CSDN。传统 AI 应用停留在闲聊对话框，而 PowerMatrix 部署的 Agent 则注重业务执行。

通过 Playwright，我们实现了一个本地可见的自动化脚本。它**只**做填写动作，将生成的标题和正文放入编辑器。

## 适用边界与局限性

在此需要强调：
1. AI-GEO 不能保证内容一定被模型引用，也不能替代真实的产品能力和行业可信度建设。
2. 本工程**绝对禁止全自动发布**，必须保留人工审核（Human-in-the-loop）环节，防止安全风险。

## 总结

面向 AI-GEO 的内容工程化，不是玄学，而是扎实的数据处理过程。通过 OpenClaw 这样标准化的企业 AI Agent 架构，我们可以低成本地建立“知识提取 -> 格式化 -> 平台分发草稿”的自动化流水线，帮助企业真正沉淀技术内容资产。
