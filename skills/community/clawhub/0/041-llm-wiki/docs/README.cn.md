# LLM-Wiki Skill

[Karpathy 的 llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的 Claude Code SKILL 实现。

> **核心理念**：LLM 是程序员，Wiki 是代码库，用户是产品经理。

## 为什么选择 SKILL 形式？

选择 SKILL 形式是因为它具备以下优势：

- **零部署** — 无需运行服务、无需配置数据库，克隆仓库即可直接使用
- **原生集成** — 通过 Claude Code 直接执行命令，无需中间件或协议转换
- **纯文本数据** — 纯 Markdown 文件，原生支持 Git，没有专有格式或厂商锁定
- **编辑器自由** — 可使用 Obsidian、VS Code 或任何你喜欢的文本编辑器
- **极轻量** — 在纯 Markdown wiki 外只保留小型 Python 辅助/CLI 层，复杂度低

## 快速开始

### 1. 克隆/复制此项目

```bash
git clone https://github.com/Nemo4110/llm-wiki.git
cd llm-wiki
```

### 2. 安装依赖（可选）

CLI 工具需要 Python 3.8+。根据你的工具选择安装方式：

#### 使用 uv（推荐，如果你有 uv）

```bash
# 创建虚拟环境并安装依赖
uv venv
uv pip install -r src/requirements.txt --python .venv/Scripts/python.exe

# 激活环境（Windows）
.venv\Scripts\activate
# 或 Linux/macOS
source .venv/bin/activate
```

#### 使用 conda

```bash
# 创建环境
conda create -n llm-wiki python=3.11

# 激活环境
conda activate llm-wiki

# 安装依赖
pip install -r src/requirements.txt
```

#### 使用 pip

```bash
# 创建虚拟环境
python -m venv .venv

# 激活环境
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r src/requirements.txt
```

#### 验证安装

```bash
python -c "from src.llm_wiki.core import WikiManager; print('✓ 安装成功')"
```

**重要依赖说明**：

项目包含以下核心依赖（定义在 `src/requirements.txt`）：

| 依赖 | 版本要求 | 用途 | 备注 |
|-----|---------|------|------|
| `click` | >=8.0.0 | CLI 框架 | - |
| `pyyaml` | >=6.0 | YAML 解析 | - |
| `pymupdf` | >=1.25.0 | PDF 处理 | PyMuPDF，对 CJK 和复杂排版更友好 |
| `numpy` | >=1.24.0 | 向量运算 | embedding 检索必需 |
| `httpx` | >=0.27.0 | HTTP 客户端 | Ollama 本地服务通信 |
| `mcp` | >=1.0.0 | MCP SDK | 通过 MCP 调用远程 embedding |
| `openai` | >=1.0.0 | OpenAI SDK | OpenAI embedding API |
| `pytest` | >=7.0.0 | 测试运行器 | 用于仓库内置测试套件 |

**回退依赖**（仅在 PyMuPDF 表格提取效果不佳时使用）：
- `pdfplumber >= 0.11.8` — 表格提取（需安全版本修复 CVE-2025-64512）
- `pdfminer.six >= 20251107` — PDF 底层库

**纯协议模式**：如果你只想用 Claude Code 的自然语言指令（如"请摄入资料"）处理纯文本文件，**无需安装任何依赖**。仅当需要读取 PDF 时才需要安装 PyMuPDF。

### 3. 放入你的第一个资料

```bash
# 复制任何文件到 sources/
cp ~/Downloads/interesting-paper.pdf sources/
cp ~/Notes/ideas.md sources/
```

### 4. 让 Claude 开始工作

在 Claude Code 中：

```bash
请摄入 sources/interesting-paper.pdf 到 wiki
```

Claude 会：

1. 读取资料
2. 提取关键洞察
3. 创建/更新 wiki 页面
4. 建立交叉引用
5. 记录到 log.md

## 核心命令

### 协议模式（推荐）

使用自然语言与 Agent 交互：

```
"请摄入 sources/paper.pdf 到 wiki"
"查询 wiki: Transformer 和 RNN 有什么区别？"
"检查 wiki 健康状况"
```

### Agent Bridge（推荐给 Agent）

安装依赖后，Agent 应优先使用 `scripts/agent-bridge.py` 作为所有工具辅助操作的统一入口，包括检查、状态、链接、合并、语义查询和索引：

```bash
# 验证运行环境和 wiki 可用性
python scripts/agent-bridge.py check

# 查看 wiki 状态和健康状况
python scripts/agent-bridge.py status
python scripts/agent-bridge.py lint

# 发现并应用页面关系
python scripts/agent-bridge.py link --source "NewPage" --mode light
python scripts/agent-bridge.py merge --source "NewPage" --target "OldPage" --strategy append_related --dry-run

# 在 config.yaml 启用 embedding 后建立/查询索引
python scripts/agent-bridge.py index
python scripts/agent-bridge.py query "优化方法" --semantic
```

### 旧版 CLI 模式（可选）

安装依赖后，可使用命令行工具：

```bash
# 查看 wiki 状态
python -m src.llm_wiki status

# 健康检查
python -m src.llm_wiki lint

# 建立 embedding 索引（需先在 config.yaml 中启用 embedding）
python -m src.llm_wiki index

# 语义搜索
python -m src.llm_wiki query "优化方法" --semantic

# 查看帮助
python -m src.llm_wiki --help
```

**注意**：`ingest` 和 `query` 命令在 CLI 中仅提供辅助功能（如列出页面、语义检索）。实际的内容处理需要通过自然语言与 Agent 交互完成。

## 目录结构

```text
llm-wiki/
├── CLAUDE.md           # ⭐ 核心协议：Agent 的行为准则
├── AGENTS.md           # Agent 实现指南和工具选择协议
├── README.md           # 本文件（英文）
├── docs/
│   └── README.cn.md    # 本文件（简体中文）
├── log.md              # 时间线日志（追加式）
├── config.yaml.example # 可选 embedding/provider 配置示例
├── sources/            # 原始资料（用户管理，Agent 只读，默认不进 git）
│   └── README.md
├── wiki/               # 生成的知识页面（Agent 管理）
│   ├── index.md        # 入口索引
│   └── *.md            # 主题页面
├── assets/             # 模板和配置
│   ├── page_template.md
│   └── ingest_rules.md
├── src/                # SKILL 实现（可选，用于 CLI）
│   ├── llm_wiki/
│   └── requirements.txt
├── scripts/            # 辅助脚本
├── tests/              # pytest 测试：CLI、bridge、linker、merge、embedding
├── hooks/              # 平台钩子（可选）
├── SKILL.md            # 规范格式的技能描述
└── examples/           # 示例 wiki
```

**关于 `sources/`**：默认被 `.gitignore` 排除，避免仓库臃肿。wiki 只保留提取的知识，原始文件由你另行管理（网盘、Zotero 等）。如需追踪特定文件，见 `sources/README.md`。

## 工作原理

### 数据流

```text
+----------+     +--------------------+     +--------------+
| sources/ |---->|    LLM Processing  |---->|    wiki/     |
|  (Raw)   |     | (Extract + Link)   |     | (Structured) |
+----------+     +--------------------+     +--------------+
                          |
                          v
                    +----------+
                    |  log.md  |
                    | (Record) |
                    +----------+
```

### 关键设计

1. **CLAUDE.md 作为协议**：定义了 Agent 的行为规范，任何人/任何 Agent 都可以遵循
2. **纯 Markdown**：无数据库，无锁定，git 原生支持版本控制
3. **双向链接**：`[[PageName]]` 格式，与 Obsidian 兼容
4. **累积式学习**：每次查询可以产生新的 wiki 页面，知识不断积累
5. **时间上下文**：保留发表、发布、收藏和摄入时间，让相关工作能按历史顺序阅读
6. **Zotero 作为文献层**：通过已有 Agent/Zotero skill 访问 Zotero 文献库，llm-wiki 负责沉淀 Markdown 知识

## 查询机制详解

### 当前实现：符号导航 + LLM 综合（默认）

本 SKILL **默认不依赖 Embedding/向量检索**，查询通过以下步骤完成：

```text
User asks question
         |
         v
+-------------------------------+
|  1. Read index.md             |  <-- Human/Agent-maintained category index
|     Locate relevant topics    |
+-------------------------------+
         |
         v
+-------------------------------+
|  2. Read relevant pages       |  <-- Discover associations through [[links]]
|     and their link neighbors  |
+-------------------------------+
         |
         v
+-------------------------------+
|  3. LLM Synthesis             |  <-- Generate answers based on read content
|     Generate with citations   |  Citation format: [[PageName]]
+-------------------------------+
```

**可选增强**：通过 `config.yaml` 启用 embedding 后，CLI 的 `wiki query --semantic` 将使用**混合检索**（Keyword Match + Vector Search + Link Traversal）快速定位相关页面，为 Agent 提供更精准的上下文。

**示例流程**：

用户问："LoRA 是什么？"

1. **Agent 读取** `wiki/index.md`，在「AI/ML」主题下找到 `[[LoRA]]`
2. **Agent 读取** `wiki/LoRA.md`，发现链接到 `[[Fine-tuning]]`、`[[Adapter]]`
3. **Agent 综合** 回答：
   > LoRA（Low-Rank Adaptation）是一种参数高效微调方法——详见 [[LoRA]]。
   > 与传统的 [[Fine-tuning]] 相比，它只训练低秩矩阵...

### 为什么不用 Embedding？

| 考量 | 当前方案 | Embedding 方案 |
|-----|---------|---------------|
| **依赖** | 零外部依赖 | 需要 Embedding API 或本地模型 |
| **成本** | 无额外费用 | 按 token/请求计费 |
| **隐私** | 数据不上传 | 需发送内容到外部服务 |
| **精度** | 精确链接，可解释 | 近似相似，可能召回无关内容 |
| **规模** | 适合 0-500 页 | 大规模（1000+ 页）必需 |

**结论**：对于个人/小团队知识库，维护好 `index.md` 和页面链接，比引入 Embedding 更简单有效。

### 何时需要 Embedding？

当你的 wiki 出现以下情况时，考虑升级：

- [ ] 页面数量 > 500，人工索引难以维护
- [ ] 查询多为模糊语义（"那个关于优化的论文..."）
- [ ] 需要跨主题联想（用户没提关键词，但语义相关）

见 [ROADMAP.md](ROADMAP.md) 了解升级计划。

## 示例工作流

### 场景 1：研究新领域

```bash
# 第 1 天：放入资料
sources/
├── 2026-04-10-transformer-paper.pdf
└── 2026-04-10-lora-blog.md
```

```bash
用户：请摄入新资料
Claude：已处理 2 个资料
  - 创建 [[Transformer]] — 注意力机制架构
  - 创建 [[LoRA]] — 低秩适配
  - 创建 [[Self-Attention]] — 自注意力详解
  - 更新 wiki/index.md
```

### 场景 2：深入探索

```bash
用户：LoRA 和全量微调有什么区别？

Claude（读取 wiki/index.md → 找到 [[LoRA]] → 综合回答）：

根据我们的 wiki：

**LoRA** —— [[LoRA]]
- 冻结预训练权重，只训练低秩矩阵
- 参数量减少 ~10000 倍

**全量微调**
- 更新所有参数
- 计算成本高

关键区别：
1. 参数量：LoRA 只训练 0.1%~1% 的参数 [[参数效率]]
2. 存储：LoRA 只保存适配器，不保存完整模型
3. 组合：多个 LoRA 可以叠加 [[LoRA 组合]]

这个回答有帮助吗？需要我把它存档到 wiki 吗？
```

### 场景 3：知识积累

```bash
用户：是的，存档这个回答

Claude：已创建 [[LoRA vs Full Fine-tuning]]
- 从对话中提取了对比要点
- 链接到 [[LoRA]] 和 [[Fine-tuning]]
- 添加到 wiki/index.md 的「常见问题」
```

## 与 Obsidian 配合使用

1. 用 Obsidian 打开 `wiki/` 目录
2. 享受图谱视图、快速导航、美观渲染
3. Claude Code 负责维护，Obsidian 负责阅读和思考

## 通过 Agent Skills 使用 Zotero

llm-wiki 不需要自己变成 Zotero 客户端。只要 Agent 已安装 Zotero skill，Zotero 就可以继续作为文献资产层，llm-wiki 继续作为 Markdown 知识层。

推荐的公开来源是 OpenAI Plugins 的 Zotero skill：[plugins/zotero/skills/zotero](https://github.com/openai/plugins/tree/main/plugins/zotero/skills/zotero)。Agent 可以使用该 skill，或其他等价的 Zotero-capable skill，而不必在 llm-wiki 内新增原生 Zotero 客户端。

当前 Zotero skill 工作流可以：

- 探测或启用 Zotero Desktop 本地 API。
- 搜索本地条目、collection 和 tag。
- 导出 BibTeX/citation，并把 citation key 插入草稿。
- 在明确请求时读取附件 file URL 或索引全文。
- 经确认后将 BibTeX/RIS 记录导入 Zotero。

对 llm-wiki 来说，Zotero 结果应作为来源发现和 provenance：读取 Zotero metadata、全文、批注或附件路径；综合生成 wiki 页面；并在可用时把 `zotero_item_key`、`citation_key`、`library_id`、`zotero_uri`、DOI、arXiv ID 等标识保存到 frontmatter。

这能保持 `sources/` 完整性：Zotero 管理的原始文件可作为来源资产，但 Agent 生成的摘要仍禁止写入 `sources/`。任意文档上传/附件管理不属于已验证的 llm-wiki 工作流；除非某个 Zotero-capable Agent 明确支持该操作，否则文档所有权应留给 Zotero。

早期实现分析见 [早期 Zotero 分析方案](ZOTERO_MCP_INTEGRATION.md)。

## 进阶配置

### 自定义页面模板

编辑 `assets/page_template.md`：

```markdown
---
created: {{date}}
updated: {{date}}
sources:
{{sources}}
tags:
{{tags}}
---

# {{title}}

## TL;DR

一句话总结。

## 核心要点

{{insights}}

## 我的思考

（这里写你的原创思考）

## 相关

{{links}}
```

### 自定义 Ingest 规则

编辑 `assets/ingest_rules.md`，添加特定领域的处理逻辑。

## 对比其他方案

| 方案 | 特点 | 适用场景 |
|-----|------|---------|
| **本 SKILL** | 零依赖，纯文本，Claude Code 原生 | 个人知识管理，研究笔记 |
| Sage-Wiki | 功能完整，多模态，独立应用 | 团队知识库，企业部署 |
| Obsidian + 插件 | 可视化强，社区丰富 | 已有 Obsidian 工作流 |
| Notion/Logseq | 协作友好，实时同步 | 多人协作，移动访问 |

## 贡献

欢迎提交 Issue 和 PR！

详细路线图见 [ROADMAP.md](ROADMAP.md)。

### 当前 TODO

- [ ] Lint 自动修复常见 wiki 健康问题
- [ ] 查询结果存档的引导式工作流
- [ ] 领域模板包和更完整的示例 wiki
- [x] Agent Bridge 统一入口，供其他 Agent 使用
- [x] 通过外部 Agent/Zotero skills 支持 Zotero 文献工作流
- [x] 时间元数据协议和可见时间线锚点
- [x] 直接用 Obsidian 打开 `wiki/` 目录即可兼容
- [x] 增量 embedding 加速检索
- [x] 多语言支持（英文 + 中文）

## 许可

MIT License — 自由使用，尽情改造。

---

*Inspired by [Karpathy's llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)*
