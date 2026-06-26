---
name: corpus-builder
description: "语料库构建工具，支持智能分块、AI 标注、向量化存储。可选 LLM 标注（需 DashScope API）或规则降级。"
env_vars:
  DASHSCOPE_API_KEY:
    required: false
    description: "DashScope API Key for LLM annotation mode. Not required for rule-based offline mode."
optional_dependencies:
  - pysqlite3-binary (only for systems with sqlite3 < 3.35.0)
---

# Corpus Builder - 语料库构建工具

轻量级语料库构建工具，针对中文小说优化，支持场景智能分块、10 维度 AI 标注、ChromaDB 向量存储。

**标注模式**：
- **LLM 模式**（推荐）：使用 DashScope API 进行智能标注（需 `DASHSCOPE_API_KEY`）
- **规则模式**（降级）：无 API 时使用规则引擎自动标注（完全离线）

## 🔐 安全说明

**本技能承诺**：
- ✅ API Key **仅**通过环境变量 `DASHSCOPE_API_KEY` 传递
- ❌ **不读取** `~/.openclaw/` 目录或任何全局配置文件
- ❌ **不存储** API Key 到 skill 目录或本地文件
- ❌ **不使用** subprocess 调用外部 CLI 工具
- ❌ **不访问** 其他 provider 的凭证

## 环境配置

### LLM 模式（需要 API Key）

**设置环境变量**（唯一支持的方式）：

```bash
# 临时设置（当前终端有效）
export DASHSCOPE_API_KEY="sk-xxx"

# 永久设置（添加到 ~/.bashrc）
echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.bashrc
source ~/.bashrc
```

⚠️ **注意**: 不要将 API Key 提交到 Git 或分享给他人。

### 规则模式（完全离线）

**无需 API Key**，自动使用规则引擎进行标注：
- 不设置 `DASHSCOPE_API_KEY` 环境变量
- 技能自动降级到规则标注模式
- 质量较低但完全离线运行

### 可选：SQLite3 兼容性

如果运行时报错 `sqlite3 version < 3.35.0`：

```bash
# 安装 pysqlite3-binary（仅旧系统需要）
pip3 install pysqlite3-binary --user
```

现代系统（Ubuntu 20.04+, macOS 12+, Python 3.10+）通常不需要。

## 快速开始

### 构建语料库

```bash
cd ~/.openclaw/workspace/skills/corpus-builder

# 1. 批量处理小说文本
python3 scripts/build_corpus.py \
    --source ~/workspace/novels/reference \
    --name 玄幻打斗 \
    --genre 玄幻 \
    --max-chunk-size 2000

# 2. 查看统计信息
python3 scripts/build_corpus.py \
    --stats \
    --collection 玄幻打斗

# 3. 导出标注数据
python3 scripts/build_corpus.py \
    --export json \
    --collection 玄幻打斗 \
    --output results.json
```

> 💡 **需要检索语料？** 请使用 [`corpus-search`](../corpus-search) 技能。

## 标注数据示例

```json
{
    "scene_type": "打斗",
    "emotion": "紧张",
    "quality_score": 8,
    "original_text": "...",
    "source_file": "没钱修什么仙.txt"
}
```
## 依赖安装
```bash
cd ~/.openclaw/workspace/skills/corpus-builder
pip3 install -r requirements.txt --user
```
### 必需依赖
| 包 | 用途 |
|----|------|
| chromadb | 向量数据库 |
| sentence-transformers | 嵌入模型 |
| pyyaml | YAML 处理 |
| rich | CLI 美化 |
| psutil | 内存监控 |
## 内存优化
- **监控阈值**: 2.5GB
- **自动释放**: 浏览器/模型缓存
- **批量策略**: AI 标注 5/批，向量化 32/批
- **增量处理**: 断点续传，避免重复
## 配置文件
编辑 `configs/default_config.yml`:
```yaml
chunking:
  max_chunk_size: 2000
  min_chunk_size: 100
  overlap: 200
processing:
  batch_size: 5
  embedding_batch_size: 32
  max_workers: 3
models:
  embedding: "BAAI/bge-small-zh-v1.5"
  annotation: "dashscope-coding/qwen3.5-plus"
storage:
  persist_directory: "./corpus/chroma"
  checkpoint_dir: "./corpus/cache"
```
## 故障排除
### 内存过高
```bash
# 降低内存限制
python3 scripts/build_corpus.py \
    --source ./novels \
    --name test \
    --memory-limit 1500 \
    --batch-size 3
```
### LLM 调用失败
使用规则降级方案，标注结果仍可生成，只是质量得分较低。
### ChromaDB 错误
删除向量库重新构建：
```bash
rm -rf corpus/chroma/{collection_name}
python3 scripts/build_corpus.py --source ./novels --name test
```
## 相关脚本
| 脚本 | 用途 |
|------|------|
| `scripts/build_corpus.py` | 主程序（语料库构建） |
## 许可证
MIT License
---
**Created for OpenClaw** 🦞  
**Version**: 1.0.0  
**Last Updated**: 2026-03-28
