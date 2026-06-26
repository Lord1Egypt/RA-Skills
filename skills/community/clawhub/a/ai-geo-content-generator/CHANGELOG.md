# CHANGELOG — AI-GEO Content Generator Skill

---

## [0.1.0] — 2026-05-11

### 🎉 MVP 初始版本发布

#### 新增

- `SKILL.md`：OpenClaw Skill 核心定义文件，包含 11 个章节
- `README.md`：使用说明文档，包含完整的使用流程、注意事项和扩展方向
- `CHANGELOG.md`：版本更新记录（本文件）

#### 提示词（prompts/）

- `intake.md`：信息收集与用户意图确认提示词
- `knowledge_base_reader.md`：品牌知识母库读取与字段提取提示词
- `website_faq.md`：官网 FAQ 内容生成提示词
- `zhihu_answer.md`：知乎问答内容生成提示词
- `toutiao_article.md`：今日头条文章生成提示词
- `llms_txt.md`：llms.txt 草稿生成提示词
- `quote_sentences.md`：AI 可引用句库生成提示词
- `geo_quality_check.md`：AI-GEO 自检提示词（10 条规则）

#### 模板（templates/）

- `website_faq.md`：官网 FAQ 输出格式模板
- `zhihu_answer.md`：知乎问答输出格式模板
- `toutiao_article.md`：今日头条文章输出格式模板
- `llms.txt`：llms.txt 输出格式模板
- `quote_sentence_library.md`：AI 可引用句库输出格式模板

#### 示例（examples/）

- `example_brand_knowledge_base.md`：虚拟品牌"FrameAI"的品牌知识母库输入示例
- `example_website_faq.md`：官网 FAQ 输出示例
- `example_zhihu_answer.md`：知乎问答输出示例
- `example_toutiao_article.md`：今日头条文章输出示例
- `example_llms.txt`：llms.txt 输出示例
- `example_quote_sentence_library.md`：AI 可引用句库输出示例

#### MVP 范围说明

**支持**：
- 读取 brand_knowledge_base.json / .md / .yaml
- 生成官网 FAQ（结构化分类）
- 生成知乎问答（完整回答正文结构）
- 生成今日头条文章（资讯化写法）
- 生成 llms.txt 草稿
- 生成 AI 可引用句库
- AI-GEO 内容自检（10 条规则）

**不支持**（后续版本）：
- 后端系统、数据库、登录系统
- 自动发布、批量任务
- 月度内容监测报告
- 多行业深度定制模板
- 完整咨询报告

---

## [计划中] 后续版本

### [0.2.0] — 计划

- 增加豆包/Doubao GEO 内容优化专项提示词
- 增加 DeepSeek GEO 内容优化专项提示词
- 增加多关键词矩阵覆盖功能

### [0.3.0] — 计划

- 增加知乎内容矩阵（多问题批量生成）
- 增加今日头条内容矩阵（多文章批量生成）

### [0.4.0] — 计划

- 增加月度 GEO 内容健康度维护报告
- 增加官网 GEO 内容包（Schema.org 标注）
