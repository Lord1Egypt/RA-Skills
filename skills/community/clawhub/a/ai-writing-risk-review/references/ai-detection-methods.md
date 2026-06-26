# AI 写稿检测方法速览

## 方法谱系

### 统计与语言模型特征

常见指标包括 perplexity、entropy、token rank、log probability、burstiness、词汇多样性、句长分布和标点分布。思路是：模型生成文本往往更平滑、更接近高概率 token，句式节奏也可能更稳定。

典型代表：

- GLTR：用 token 概率排名、分布熵等可视化特征辅助人类判断。
- 零样本 log-likelihood / log-rank 检测：比较文本在语言模型下的平均概率或排名。

局限：

- 新模型、强提示词、人类轻度改写、翻译和领域迁移都会削弱效果。
- 正式公文、教科书、说明书、低错别字文本容易被误判。

### 曲率与扰动检测

DetectGPT 类方法会改写或扰动原文，比较原文和扰动文本在语言模型下的概率变化。核心假设是：模型生成文本更可能落在模型概率函数的特定曲率区域。

局限：

- 需要访问合适的语言模型或替代模型。
- 对短文本、跨模型文本、经过人类编辑的文本不稳定。
- 成本和实现复杂度高于简单统计检测。

### 监督分类器

训练 BERT、RoBERTa、DeBERTa 或其它分类模型，输入文本后输出 AI/人类标签或分数。商业 AI detector 常混合使用监督分类器、统计特征和内部语料。

局限：

- 训练集、生成模型、语言、体裁和时间变化会造成 domain shift。
- 公开准确率通常不能直接迁移到用户手上的文本。
- 低 false positive 场景更难，尤其不能用于单独处罚。

### 风格计量与作者基线

比较目标文本与作者历史文本的风格差异，包括功能词、常用短语、句法长度、错别字、标点、段落节奏、观点表达、引用习惯和材料来源。

适合：

- 用户提供同一作者的多篇历史文本。
- 需要判断“是否不像这个人写的”，而不仅是“是否像 AI”。

局限：

- 作者换题材、被编辑润色、模仿他人风格或多人协作时会偏移。
- 只能说明风格异常，不能单独证明 AI 生成。

### 水印与来源证明

水印方法会在生成阶段影响 token 选择或嵌入统计签名，检测时再验证签名。SynthID-Text、green-list/red-list 类方法属于这一方向。C2PA、平台元数据、文档修订历史和生成日志属于更广义的来源证明。

优势：

- 若生成端和检测端都可信，水印/来源证明比纯文本猜测更强。

局限：

- 必须由生成系统预先嵌入或保留来源信息。
- 深度改写、翻译、拼接、多模型接力可能破坏信号。
- 开源模型、未接入水印的模型和人工转写通常无法验证。

### 多工具交叉验证

可以把多个检测器作为参考，但要记录工具名称、版本、日期、文本长度、阈值和结果差异。多个工具同意不等于真相；多个工具分歧通常说明证据不足或文本处于边界。

## 常见强弱信号

强信号：

- 有可信生成日志、水印命中、平台溯源或文档历史证明。
- 长文本中多段呈现高度一致的机器化结构，同时明显偏离作者历史文本。
- 大量伪引用、伪数据、无法追溯的具体事实，并符合模型幻觉模式。

中信号：

- 段落结构和连接词高度模板化。
- 信息密度均匀但缺少真实经历、具体约束、取舍和例外。
- 多个检测方法给出相近风险，但无外部证据。

弱信号：

- “首先、其次、最后”“综上所述”等套话。
- 过于流畅、语法正确、很少错别字。
- 标题党、营销话术、教科书腔、公文腔。

## 使用边界

AI 检测尤其容易在以下场景失效：

- 文本很短。
- 文本被翻译、改写、摘要、润色或混写。
- 作者是非母语写作者。
- 体裁本身高度模板化。
- 用户需要做纪律处分、录用拒绝、法律判断或版权归责。

遇到高风险场景，建议把 AI 检测作为线索，并要求补充写作过程、草稿版本、引用来源、口头答辩或人工复核。

## 研究依据关键词

需要进一步查证时，优先搜索这些关键词：

- `GLTR statistical detection generated text token rank entropy`
- `DetectGPT probability curvature machine generated text`
- `AI-generated text detection survey watermarking statistical stylistic machine learning classification`
- `AI text detector false positives reliability`
- `SynthID-Text watermarking LLM outputs`

## 代表资料

- OpenAI, `New AI classifier for indicating AI-written text`：说明 AI classifier 已因准确率低下线，并列出短文本、非英语、可预测文本、改写规避和训练分布外校准等限制。
- Gehrmann, Strobelt, Rush, `GLTR: Statistical Detection and Visualization of Generated Text`：用 token rank、概率和熵等统计特征辅助人类识别生成文本。
- Mitchell et al., `DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature`：用语言模型 log probability 曲率和扰动文本做零样本检测。
- Dathathri et al., `Scalable watermarking for identifying large language model outputs`：SynthID-Text 类水印方法，代表生成端嵌入、检测端验证的来源证明路线。
- Kirchenbauer et al., `A Watermark for Large Language Models`：green-list/red-list token 水印思路，展示在生成时嵌入可算法检测的隐藏信号。
