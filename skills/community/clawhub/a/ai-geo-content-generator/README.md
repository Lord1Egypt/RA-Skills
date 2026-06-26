# AI-GEO Content Generator Skill — README

> **版本**: 0.1.0 (MVP) | **语言**: 中文为主，关键术语保留英文

---

## 🎯 这个 Skill 是什么

**AI-GEO Content Generator Skill**（AI-GEO 内容生成 Skill）是一个内容转化工具。

它读取品牌知识母库（`brand_knowledge_base.json` 或 `brand_knowledge_base.md`），将品牌知识转化为适合大模型、AI 搜索引擎和 AI Agent 理解、总结、引用、推荐的内容资产。

**核心定位**：

```
品牌知识母库 → AI-GEO 内容资产
```

---

## 🔗 与 Knowledge Base Builder 的关系

这两个 Skill 是**并列关系**，通过标准文件格式衔接：

```
Documents/skills/
├── Knowledge Base Builder/    ← 第一步：整理品牌知识，生成母库
└── ai-geo-content-generator/  ← 第二步：读取母库，生成 AI-GEO 内容
```

| 维度 | Knowledge Base Builder | AI-GEO Content Generator |
|---|---|---|
| **作用** | 整理零散品牌资料，建立标准化母库 | 读取母库，生成可被 AI 引用的内容 |
| **输入** | 原始品牌资料（PPT/文档/网页） | `brand_knowledge_base.json/.md` |
| **输出** | `brand_knowledge_base.json/.md/.yaml` | FAQ / 知乎问答 / 头条文章 / llms.txt / 句库 |
| **顺序** | 必须先运行 | 依赖前者的输出才能运行 |
| **耦合** | 无代码耦合 | 无代码耦合 |

---

## 🚀 推荐使用流程

### 第一步：运行 Knowledge Base Builder，生成品牌知识母库

前往 `Documents/skills/Knowledge Base Builder`，将客户原始品牌资料整理成：

- `brand_knowledge_base.json`（优先使用）
- `brand_knowledge_base.md`（备选）
- `brand_knowledge_base.yaml`（备选）

### 第二步：将品牌知识母库作为输入，运行本 Skill

将 `brand_knowledge_base.json` 或 `brand_knowledge_base.md` 作为输入，提供给 AI-GEO Content Generator Skill。

### 第三步：选择要生成的 AI-GEO 内容类型

目前支持以下 5 类输出（可选单项或全部生成）：

- **A. 官网 FAQ 内容** — 适合直接发布到品牌官网帮助中心
- **B. 知乎问答内容** — 适合发布到知乎，包含结构化回答正文
- **C. 今日头条文章** — 适合发布到今日头条、百家号，资讯化写法
- **D. llms.txt 草稿** — 适合放置在网站根目录，供 AI Agent 读取品牌信息
- **E. AI 可引用句库** — 适合在各平台统一品牌表达，提高 AI 引用一致性

---

## 📂 如何准备品牌知识母库

**推荐方式**：使用 `Documents/skills/Knowledge Base Builder` 生成。

**手动准备**：参考 `examples/example_brand_knowledge_base.md`，按照模板格式填写以下核心字段：

| 字段 | 说明 | 是否必填 |
|---|---|---|
| 品牌名称 | 品牌的正式中文名 | ✅ 必填 |
| 公司名称 | 法律注册主体名称 | ✅ 必填 |
| 一句话定义 | 20 字以内的品牌定位 | ✅ 必填 |
| 100 字介绍 | 用于 AI 摘要场景 | ✅ 必填 |
| 目标用户 | 核心用户群体描述 | ✅ 必填 |
| 核心能力 | 产品/服务/技术能力列表 | ✅ 必填 |
| 使用场景 | 至少 2-3 个具体场景 | ✅ 必填 |
| 合规边界 | 能做/不能做/禁用表达 | ✅ 必填 |
| FAQ | 已有的常见问题和回答 | 推荐提供 |
| 标准话术 | 官方认可的品牌表达 | 推荐提供 |
| 品牌关键词 | 核心 SEO/GEO 关键词列表 | 推荐提供 |

---

## 📋 如何选择输出类型

| 你的需求 | 推荐输出类型 |
|---|---|
| 优化官网，让 AI 搜索能准确描述品牌 | 官网 FAQ + llms.txt |
| 在知乎建立权威形象 | 知乎问答 |
| 在今日头条做内容营销 | 今日头条文章 |
| 统一品牌在所有 AI 平台的表达 | AI 可引用句库 |
| 全面铺设 AI-GEO 内容基础 | 全部生成 |

---

## 💬 示例调用

### 聊天界面

```
我已经用 Knowledge Base Builder 生成了品牌知识母库，这是 brand_knowledge_base.json 文件内容：

[粘贴内容]

请帮我生成：
1. 官网 FAQ（至少 20 个问题）
2. llms.txt 草稿

重点关键词：AI内容生成、品牌GEO优化、知识库
```

### API 调用

```json
{
  "skill": "ai-geo-content-generator",
  "action": "generate",
  "payload": {
    "knowledge_base_file": "brand_knowledge_base.json",
    "output_types": ["website_faq", "llms_txt"],
    "keywords": ["AI内容生成", "品牌知识库", "GEO优化"]
  }
}
```

---

## ⚠️ 注意事项

1. **必须先有品牌知识母库**：本 Skill 不能在没有母库的情况下运行。
2. **输出为草稿**：所有输出内容都是初稿，正式发布前必须经过人工审核。
3. **不编造事实**：本 Skill 不会自行补充品牌不具备的资质、案例或价格信息，缺失字段会标注 `[待确认]`。
4. **敏感行业需额外审核**：医疗、金融、法律行业的内容需专业人士复核后方可使用。
5. **内容基于母库生成**：如品牌知识母库信息不完整，输出质量可能受限，建议先完善母库。
6. **不自动发布**：MVP 版本不支持自动发布到任何平台，内容输出后需手动复制使用。

---

## 📦 MVP 版本范围

### ✅ 当前 MVP 支持

- 读取 `brand_knowledge_base.json / .md / .yaml`
- 生成官网 FAQ（分类结构化）
- 生成知乎问答（含回答正文结构）
- 生成今日头条文章（资讯化写法）
- 生成 `llms.txt` 草稿
- 生成 AI 可引用句库
- AI-GEO 自检（10 条规则）

### ❌ 当前 MVP 不支持

- 后端系统
- 数据库存储
- 登录/账号系统
- 付费计费系统
- 自动发布到平台
- 批量任务队列
- 月度内容健康度监测
- 多行业深度定制模板
- 完整咨询报告生成

---

## 🔭 后续可扩展方向

| 扩展模块 | 说明 |
|---|---|
| Doubao GEO Content Generator | 专为豆包/今日头条生态优化 |
| DeepSeek GEO Content Generator | 专为 DeepSeek 问答生态优化 |
| 官网 GEO 内容包 | 含元描述、结构化数据、Schema.org 标注 |
| 知乎内容矩阵 | 多问题批量生成 |
| 今日头条内容矩阵 | 多文章批量生成 |
| 月度 GEO 维护报告 | 内容健康度追踪 |
| 多语言 GEO 内容 | 英文、日文等国际版本 |

---

## 📁 文件结构

```
Documents/skills/ai-geo-content-generator/
├── SKILL.md                          ← Skill 核心定义（OpenClaw 读取）
├── README.md                         ← 本文件：使用说明
├── CHANGELOG.md                      ← 版本更新记录
├── prompts/                          ← AI 执行提示词
│   ├── intake.md                     ← 信息收集提示词
│   ├── knowledge_base_reader.md      ← 母库读取提示词
│   ├── website_faq.md                ← 官网 FAQ 生成提示词
│   ├── zhihu_answer.md               ← 知乎问答生成提示词
│   ├── toutiao_article.md            ← 今日头条文章生成提示词
│   ├── llms_txt.md                   ← llms.txt 生成提示词
│   ├── quote_sentences.md            ← AI 可引用句库生成提示词
│   └── geo_quality_check.md          ← AI-GEO 自检提示词
├── templates/                        ← 输出格式模板
│   ├── website_faq.md
│   ├── zhihu_answer.md
│   ├── toutiao_article.md
│   ├── llms.txt
│   └── quote_sentence_library.md
└── examples/                         ← 示例文件（虚拟品牌）
    ├── example_brand_knowledge_base.md
    ├── example_website_faq.md
    ├── example_zhihu_answer.md
    ├── example_toutiao_article.md
    ├── example_llms.txt
    └── example_quote_sentence_library.md
```

---

## 🔒 Security & Privacy（安全与隐私声明）

1. 本 Skill 是文本生成与内容结构化 Skill；
2. 本 Skill 不包含可执行脚本；
3. 本 Skill 不会主动读取用户本地文件；
4. 本 Skill 只处理用户主动提供的品牌资料；
5. 本 Skill 不会收集、上传或外传用户数据；
6. 请勿输入密码、私钥、API Key、cookie、token、个人身份证件、银行卡信息等敏感信息；
7. 生成内容仅供品牌内容建设参考；
8. 涉及医疗、金融、法律、教育等行业时，需要由专业人士审核；
9. 本 Skill 不承诺 AI 搜索排名、模型引用或推荐结果；
10. 用户应在发布前人工审核所有生成内容。
