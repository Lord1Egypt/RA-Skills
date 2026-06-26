---
name: kb-manager
description: 企业知识库管理。用户需要上传文档、添加知识、更新资料、删除文档、管理知识库、初始化系统时调用。同时支持业务问答：当用户提出业务问题、公司政策、流程规范等问题时，优先检索知识库后回答。
metadata: {"openclaw": {"emoji": "📚", "requires": {"bins": ["python3"]}, "skillKey": "kb-manager", "version": "1.1.0", "always-load": true}}
---

# 知识库管理系统 (KB Manager)

基于ChromaDB的本地知识库管理系统，支持多种文档格式的上传、管理和智能问答。

## 使用方法

### 对话式交互
- 发送文件并添加说明: **"upload to kb"** 或 **"上传到知识库"**
- 直接提问进行智能问答
- 支持格式: PDF, DOCX, TXT, MD

### 命令行使用
```bash
# 进入对话模式
python main.py chat

# 上传文档
python main.py upload <文件路径> [文档名称]

# 查询知识库
python main.py query <查询内容>

# 列出文档
python main.py list

# 显示统计
python main.py stats
```

## 示例

### 上传文档
```
用户: [附件: 公司政策.pdf] 上传到知识库
助手: ✅ 文档上传成功！已处理 公司政策.pdf，创建了 45 个文档块。
```

### 智能问答
```
用户: 公司的休假政策是什么？
助手: 根据公司政策文档，休假政策包括：
- 年假：每年15天带薪年假
- 病假：每年10天带薪病假
- 远程办公：每周可远程2天
```

### 文档管理
```
用户: list kb documents
助手: 📚 知识库文档列表：
1. 公司政策.pdf (45 chunks)
2. 员工手册.docx (23 chunks)
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/kb-manager
pip install -r requirements.txt
```

### 2. 配置API密钥

**方式一：环境变量**
```powershell
# DashScope (阿里云千问) - 推荐
$env:DASHSCOPE_API_KEY='your-dashscope-key'

# 或者 OpenAI
$env:OPENAI_API_KEY='your-openai-key'
```

**方式二：OpenClaw配置文件**
编辑 `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "kb-manager": {
        "enabled": true,
        "env": {
          "DASHSCOPE_API_KEY": "your-dashscope-key"
        },
        "config": {
          "embeddingProvider": "dashscope",
          "embeddingModel": "text-embedding-v3",
          "chunkSize": 500,
          "retrievalTopK": 5
        }
      }
    }
  }
}
```

### 3. 初始化系统环境

```bash
# 首次使用时，初始化系统环境
python main.py setup
```

这个命令会：
- 创建系统级数据目录
- 初始化ChromaDB数据库
- 设置正确的权限
- 验证系统配置

### 4. 测试系统

```bash
# 测试系统状态
python main.py stats

# 测试查询功能
python main.py query "测试查询"
```

## 📋 使用方法

### 上传文档
- 发送文件并添加说明: **"upload to kb"** 或 **"上传到知识库"**
- 支持格式: PDF, DOCX, TXT, MD
- 示例: `[附件: 公司政策.pdf] 上传到知识库`

### 智能问答
- 直接提问，系统会自动搜索相关文档
- 示例: 
  - `公司的休假政策是什么？`
  - `如何申请病假？`
  - `远程办公的规定是什么？`

### 文档管理
- `python main.py list` - 查看所有文档
- `python main.py stats` - 显示统计信息
- `python main.py delete <文档ID>` - 删除文档
- `python main.py setup` - 初始化系统环境

## ⚙️ 配置选项

在 `config.json` 或 OpenClaw 配置中设置:

```json
{
  "embeddingProvider": "dashscope",
  "embeddingModel": "text-embedding-v3", 
  "embeddingBaseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "chunkSize": 500,
  "chunkOverlap": 50,
  "retrievalTopK": 5,
  "collectionName": "enterprise_kb",
  "vectorDimension": 1024
}
```

**注意**: 数据库路径和文档目录由系统自动管理，无需手动配置。

## 🏗️ 技术架构

- **向量数据库**: ChromaDB (本地存储，无需Docker)
- **文档存储**: 系统级目录 (自动配置)
- **向量存储**: 系统级目录 (自动配置)
- **嵌入模型**: DashScope text-embedding-v3 (1024维) 或 OpenAI
- **支持格式**: PDF, DOCX, TXT, Markdown
- **分块策略**: 可配置大小和重叠度
- **搜索算法**: 余弦相似度

## 📁 系统数据目录

知识库数据存储在系统级固定目录中，所有skills自动共享：

**Windows**: `C:/ProgramData/kb-data/`
**Linux/Mac**: `/usr/local/share/kb-data/` 或 `~/.local/share/kb-data/`

```
kb-data/
├── chroma_db/     # 向量数据库
└── documents/     # 原始文档
```

这种设计的优势：
- **固定路径**: 所有agent自动使用相同路径
- **无需配置**: 不需要环境变量或符号链接  
- **系统标准**: 遵循操作系统标准目录结构
- **自动权限**: 智能处理权限问题

## 🔧 故障排除

### API密钥问题
```bash
# 检查环境变量 (Windows)
echo $env:DASHSCOPE_API_KEY

# 检查环境变量 (Linux/Mac)  
echo $DASHSCOPE_API_KEY

# 设置API密钥 (Windows)
$env:DASHSCOPE_API_KEY='your-api-key'

# 设置API密钥 (Linux/Mac)
export DASHSCOPE_API_KEY='your-api-key'

# 测试API连接
python -c "import os; print('API Key:', os.getenv('DASHSCOPE_API_KEY', 'Not Set'))"
```

### 依赖安装问题
```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 如果遇到grpcio问题，ChromaDB已默认配置无需Docker
pip install chromadb --upgrade
```

### 系统环境问题
```bash
# 初始化系统环境
python main.py setup

# 检查系统状态和路径
python main.py stats

# 验证系统目录权限
python -c "from src.system_config import print_system_info; print_system_info()"
```

### 数据库问题
```bash
# 系统会自动管理数据库，如需重置：
# 1. 备份重要文档
# 2. 删除系统目录 (需要管理员权限)
# 3. 重新初始化
python main.py setup

# 检查ChromaDB状态
python -c "from src.chroma_client import ChromaVectorDB; db = ChromaVectorDB(); print('DB Status:', db.get_collection_info())"
```

### 权限问题
```bash
# Windows: 确保对 C:/ProgramData/ 有写权限
# Linux/Mac: 如果 /usr/local/share/ 无权限，会自动使用 ~/.local/share/

# 检查当前使用的路径
python -c "from src.system_config import get_system_kb_path; print('KB Path:', get_system_kb_path())"
```

## 📊 性能指标

- **处理速度**: ~100页/分钟 (PDF)
- **搜索延迟**: <500ms (本地向量搜索)
- **存储效率**: ~1MB/1000页文档
- **支持规模**: 10万+文档块

## 🌐 多Agent部署

### 部署架构
```
Agent A (管理员)          Agent B (用户)           Agent C (用户)
├── kb-manager           ├── kb-reader            ├── kb-reader  
│   ├── 上传文档          │   ├── 查询知识库        │   ├── 查询知识库
│   ├── 管理知识库        │   └── 浏览文档          │   └── 浏览文档
│   └── 系统维护          └── 只读访问              └── 只读访问
└── 系统级数据目录 ←──────────────┴─────────────────────┘
    C:/ProgramData/kb-data/ (Windows)
    /usr/local/share/kb-data/ (Linux/Mac)
```

### 部署步骤

1. **管理员Agent设置**
```bash
# 在管理员Agent上安装kb-manager
cd agent-admin/skills/
git clone <kb-manager-repo>
cd kb-manager
pip install -r requirements.txt

# 初始化系统环境
python main.py setup

# 上传初始文档
python main.py upload company-docs.pdf
```

2. **用户Agent设置**
```bash
# 在用户Agent上安装kb-reader
cd agent-user/skills/
git clone <kb-reader-repo>
cd kb-reader
pip install -r requirements.txt

# 测试连接
python main.py stats
python main.py query "测试查询"
```

### 权限管理
- **kb-manager**: 完整权限，可创建、修改、删除
- **kb-reader**: 只读权限，仅能查询和浏览
- **系统目录**: 自动权限管理，确保数据安全

## 🔒 安全特性

- **本地存储**: 所有数据保存在本地，不上传云端
- **API安全**: 支持多种API提供商，密钥加密存储
- **访问控制**: 基于OpenClaw的用户权限管理
- **数据隔离**: 每个技能实例独立的数据存储
- **权限分离**: 管理和查询权限分离，防止误操作

