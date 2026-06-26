---
name: kb-reader
description: 企业知识库查询。用户提出任何业务问题、产品咨询、公司政策、员工手册、操作流程、规章制度、FAQ、项目信息等问题时，必须优先调用本知识库检索相关内容，再结合结果回答。
metadata: {"openclaw": {"emoji": "🔍", "requires": {"bins": ["python3"]}, "skillKey": "kb-reader", "version": "1.1.0", "always-load": true}}
---

# 知识库只读查询器 (KB Reader)

> ⚠️ **重要提示**: 这是一个**严格只读**的查询系统，无法创建、上传、修改或删除任何数据。使用前必须确保已有管理员通过 kb-manager 初始化了系统环境。

专门用于查询和读取企业知识库内容的轻量级系统，不支持文档上传和管理功能。

## 使用方法

### 对话式查询
- 直接提问进行智能问答
- 支持语义搜索和关键词匹配
- 自动从知识库中检索相关内容

### 命令行使用
```bash
# 进入对话模式
python main.py chat

# 直接查询
python main.py query <查询内容>

# 列出文档（只读）
python main.py list

# 显示统计（只读）
python main.py stats
```

## 示例

### 智能问答
```
用户: 公司的休假政策是什么？
助手: 根据知识库文档，休假政策包括：
- 年假：每年15天带薪年假
- 病假：每年10天带薪病假
- 远程办公：每周可远程2天
```

### 文档查看
```
用户: list documents
助手: 📚 知识库文档列表：
1. 公司政策.pdf (45 chunks)
2. 员工手册.docx (23 chunks)
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/kb-reader
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

### 3. 确保知识库已初始化

⚠️ **重要**: kb-reader 是只读系统，无法创建或初始化知识库。使用前必须确保 kb-manager 已经初始化了系统环境。

```bash
# 1. 检查系统目录是否存在
python main.py stats

# 2. 如果提示"系统数据目录不存在"，说明需要先用 kb-manager 初始化
# kb-reader 无法自行创建系统环境，必须由管理员使用 kb-manager 完成初始化
```

**如果系统未初始化，请联系管理员或在有 kb-manager 的环境中运行：**
```bash
cd <kb-manager-directory>
python main.py setup
```

### 4. 测试查询

```bash
# 测试系统状态
python main.py stats

# 测试查询功能
python main.py query "测试查询"
```

## 📋 使用方法

### 智能查询
- 直接提问，系统会自动搜索相关文档
- 支持中文和英文查询
- 示例: 
  - `公司的休假政策是什么？`
  - `如何申请病假？`
  - `远程办公的规定是什么？`

### 文档浏览
- `python main.py list` - 查看所有文档
- `python main.py stats` - 显示统计信息
- `python main.py search <query>` - 详细搜索文档内容

## ⚙️ 配置选项

在 `config.json` 中设置:

```json
{
  "embeddingProvider": "dashscope",
  "embeddingModel": "text-embedding-v3", 
  "embeddingBaseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "retrievalTopK": 5,
  "milvusUri": "系统自动配置",
  "collectionName": "enterprise_kb",
  "documentsDir": "系统自动配置"
}
```

## 📁 系统数据目录

kb-reader 自动访问系统级知识库目录：

**Windows**: `C:/ProgramData/kb-data/`
**Linux/Mac**: `/usr/local/share/kb-data/` 或 `~/.local/share/kb-data/`

```
kb-data/
├── chroma_db/     # 向量数据库 (只读访问)
└── documents/     # 原始文档 (只读访问)
```

## 🔗 与kb-manager的关系

- **kb-manager**: 负责创建和管理知识库，具有完整的读写权限
  - ✅ 创建系统目录 (`python main.py setup`)
  - ✅ 上传和管理文档
  - ✅ 删除和修改数据
  - ✅ 初始化数据库

- **kb-reader**: 只能读取kb-manager创建的知识库，**严格只读权限**
  - ❌ 无法创建系统目录
  - ❌ 无法上传文档
  - ❌ 无法修改或删除数据
  - ❌ 无法初始化数据库
  - ✅ 仅能查询和浏览现有数据

- **数据共享**: 两个skills访问同一个系统目录，实现数据共享
- **权限分离**: kb-reader无法修改或删除数据，确保数据安全
- **部署灵活**: 可以部署在不同的agent上，实现分布式知识库访问

## 📋 使用前提

1. **系统环境**: 必须已经有管理员使用 kb-manager 初始化了系统环境
2. **只读权限**: kb-reader 无法创建、修改或删除知识库数据
3. **数据存在**: 知识库中必须已经有文档数据（由 kb-manager 上传）
4. **API配置**: 需要配置相同的嵌入模型API密钥
5. **依赖关系**: kb-reader 完全依赖 kb-manager 创建的系统环境

## 🏗️ 技术特性

- **严格只读**: 代码层面限制，无任何写入或修改功能
- **高效检索**: 基于向量相似度和关键词匹配
- **多种查询模式**: 支持语义搜索、关键词搜索和混合搜索
- **轻量级**: 最小化依赖，专注查询功能
- **兼容性**: 可以读取kb-manager创建的知识库
- **安全设计**: 无权限创建、修改或删除任何数据

## 🔧 故障排除

### 知识库不存在
```bash
# 如果提示知识库不存在，kb-reader 无法自行解决此问题
# 必须联系管理员或在有 kb-manager 的环境中初始化

# 检查系统状态
python main.py stats

# 如果显示"系统数据目录不存在"，需要管理员运行：
# cd <kb-manager-directory>
# python main.py setup
```

**注意**: kb-reader 作为只读系统，无权限创建系统目录或初始化数据库。

### 无查询结果
```bash
# 检查知识库是否有数据
python main.py stats

# 如果没有数据，需要管理员使用 kb-manager 上传文档
# kb-reader 无法上传文档，只能查询已存在的数据
```

**注意**: kb-reader 无法上传文档，如需添加文档请联系管理员。

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
```

### 权限问题
```bash
# 如果遇到权限错误，检查系统目录权限
# Windows: C:/ProgramData/kb-data/
# Linux/Mac: /usr/local/share/kb-data/ 或 ~/.local/share/kb-data/

# 确保kb-manager有创建目录的权限
cd ../kb-manager
python main.py setup
```

## 🌐 部署场景

### 场景1: 单机多Agent
```
同一台机器上的多个Agent
├── Agent-Admin (kb-manager)
├── Agent-User1 (kb-reader)  
├── Agent-User2 (kb-reader)
└── 共享系统目录: C:/ProgramData/kb-data/
```

### 场景2: 分布式部署
```
多台机器，共享网络存储
├── 机器A: Agent-Admin (kb-manager) → 网络存储
├── 机器B: Agent-User1 (kb-reader) → 网络存储  
└── 机器C: Agent-User2 (kb-reader) → 网络存储
```

### 场景3: 容器化部署
```
Docker容器间数据共享
├── Container-Admin: kb-manager + 数据卷
├── Container-User1: kb-reader + 数据卷
└── Container-User2: kb-reader + 数据卷
```

## 🔒 安全特性

- **严格只读权限**: 代码层面强制只读，任何写入操作都会抛出异常
- **无创建权限**: 无法创建目录、数据库或集合
- **本地访问**: 仅访问本地知识库文件
- **API安全**: 支持多种API提供商，密钥加密存储
- **数据隔离**: 与kb-manager共享数据但权限完全隔离
- **故障安全**: 如果系统环境不存在，会立即报错而不是尝试创建

## 📊 性能指标

- **搜索延迟**: <500ms (本地向量搜索)
- **内存占用**: 最小化内存使用
- **并发支持**: 支持多用户同时查询