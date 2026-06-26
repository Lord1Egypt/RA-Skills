# Claw Local Knowledge

本地知识库技能，为 AI Agent 提供文档知识管理能力，支持语义搜索与检索。

## 概述

本技能提供两项核心功能：

| 功能 | 说明 |
|------|------|
| **添加知识** | 将用户上传的文档（docx、pdf、xlsx、pptx）转换为 markdown 并存入知识库 |
| **检索知识** | 从知识库中搜索和检索相关文档，辅助决策和回答 |

## 架构

```
.openclaw/workspace/
├── memory/
│   ├── knowledge_base/              # 转换后的 markdown 文档
│   └── knowledge_base_index.json    # 知识库索引（JSON 数组）
└── temp_file/                      # 用户上传文件的临时目录
```

### 文件流程

1. 用户上传文档 → `.openclaw/workspace/temp_file/`
2. Agent 转换为 markdown → `.openclaw/workspace/memory/knowledge_base/`
3. Agent 更新索引 → `.openclaw/workspace/memory/knowledge_base_index.json`

## 初始设置

首次使用前，需初始化所需的目录结构：

### Linux / macOS

```bash
# 创建知识库目录
mkdir -p .openclaw/workspace/memory/knowledge_base

# 创建临时文件目录
mkdir -p .openclaw/workspace/temp_file

# 创建空索引文件
echo '[]' > .openclaw/workspace/memory/knowledge_base_index.json
```

### Windows PowerShell

```powershell
# 创建目录
New-Item -ItemType Directory -Path ".openclaw/workspace/memory/knowledge_base" -Force
New-Item -ItemType Directory -Path ".openclaw/workspace/temp_file" -Force

# 创建空索引文件
Set-Content -Path ".openclaw/workspace/memory/knowledge_base_index.json" -Value "[]"
```

### 配置 SOUL.md

如果 openclaw 工作区中存在 `SOUL.md` 文件，将以下指令以原本 `SOUL.md` 的风格注入以启用主动知识检索：

```plaintext
## Local Knowledge (claw-local-knowledge skill)
Please attempt to load the **claw-local-knowledge skill** when encountering uncertain or specialized knowledge, and retrieve relevant information according to the instructions.

**Retrieval Process:**
1. Read `memory/knowledge_base_index.json` to obtain the file list.
2. Match relevant files based on keywords.
3. Read the corresponding Markdown files from `memory/knowledge_base/`.
4. Integrate the information and reply to the user.

**Note:**
The knowledge base path is `workspace/memory/knowledge_base/`, and the index file is `workspace/memory/knowledge_base_index.json`.
```

此配置确保 Agent 在面对知识盲区时能够主动查询本地知识库。

## 索引文件格式

`knowledge_base_index.json` 为 JSON 数组，每个元素代表一个文档：

```json
{
  "name": "文件名.md",
  "description": "文档内容的简要摘要"
}
```

## 支持的输入格式

| 格式 | 类型 | 扩展名 |
|------|------|--------|
| Word 文档 | Microsoft Word | `.docx` |
| PDF 文档 | 便携式文档格式 | `.pdf` |
| Excel 电子表格 | Microsoft Excel | `.xlsx` |
| PowerPoint 演示文稿 | Microsoft PowerPoint | `.pptx` |

## 使用场景

- 用户上传文档并请求整合到知识库
- Agent 需要领域知识来辅助回答用户问题
- 用户询问知识库已有文档涵盖的主题
- Agent 遇到不确定情况，需参照已存储的文档进行验证

## 工作流程参考

详细工作流程说明请参阅：

- **`references/add_knowledge.md`** — 文档摄入流程：转换、清洗、索引更新
- **`references/retrieval_knowledge.md`** — 知识检索流程：索引查询、内容读取、信息整合
