# Corpus Builder - 语料库构建工具

针对中文小说优化的轻量级语料库构建工具,支持场景智能分块、10 维度 AI 标注、ChromaDB 向量存储。

![Version](https://img.shields.io/badge/version-1.0.3-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ 特性

- **智能分块**: 按场景/章节切分,500-2000 字/块
- **10 维度 AI 标注**: 场景类型、情绪、技巧、节奏、视角等
- **向量化存储**: BAAI/bge-small-zh-v1.5 (512 维)
- **混合存储**: YAML (人类可读) + JSON (查询优化)
- **断点续传**: 支持增量处理,避免重复
- **内存监控**: 超 2.5GB 自动释放资源
- **双模式标注**: LLM 模式(高质量)或规则模式(离线)

> 💡 **注意**:语料检索功能已移至 [`corpus-search`](https://github.com/openclaw/openclaw/tree/main/skills/corpus-search) 技能,提供更专业的检索体验。

## 📦 安装

### 方式 1: 使用 pip(推荐)

```bash
cd ~/.openclaw/workspace/skills/corpus-builder
pip3 install -e .
```

### 方式 2: 使用 requirements.txt

```bash
cd ~/.openclaw/workspace/skills/corpus-builder
pip3 install -r requirements.txt --user
```

### 方式 3: 使用 ClawHub

```bash
clawhub install corpus-builder
```

## 🚀 快速开始

### 1. 配置 API Key(LLM 模式)

```bash
# 设置 DashScope API Key(仅 LLM 模式需要)
export DASHSCOPE_API_KEY="sk-xxx"

# 永久生效(可选)
echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.bashrc
source ~/.bashrc
```

### 2. 构建语料库

```bash
cd ~/.openclaw/workspace/skills/corpus-builder

# 批量处理小说文本
python3 scripts/build_corpus.py \
    --source ~/workspace/novels/reference \
    --name 玄幻打斗 \
    --genre 玄幻 \
    --max-chunk-size 2000
```

### 3. 查看统计信息

```bash
python3 scripts/build_corpus.py \
    --stats \
    --collection 玄幻打斗
```

输出示例:
```
📊 语料库统计: 玄幻打斗
生成时间:2026-04-01T10:07:25
总块数:259
文件数:12
题材:玄幻
平均块大小:1661 字
平均质量分:5.0
```

### 4. 导出标注数据

```bash
python3 scripts/build_corpus.py \
    --export json \
    --collection 玄幻打斗 \
    --output results.json
```

输出示例:
```
✅ 标注导出到:results.json
   记录数:259
```

## 📊 标注体系 (10 维度)

| 维度 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| **scene_type** | 多选 | 场景类型 | 打斗/修炼/对话/探险 |
| **emotion** | 多选 | 情绪氛围 | 紧张/轻松/悲伤/热血 |
| **techniques** | 多选 | 写作技巧 | 侧面描写/对比/伏笔 |
| **pace** | 单选 | 节奏 | 快节奏/慢节奏/张弛有度 |
| **pov** | 单选 | 视角 | 第一人称/第三人称 |
| **character_count** | 单选 | 角色数量 | 单人/双人/多人 (3+) |
| **power_level** | 单选 | 实力等级 | 炼气期/筑基期/金丹期 |
| **key_elements** | 多选 | 关键元素 | 围攻,剑法,后发先至 |
| **usage** | 多选 | 适用场景 | 学习打斗描写,学习紧张氛围 |
| **quality_score** | 数值 | 质量评分 | 1-10 分 |

## 📁 输出结构

```
corpus/
├── chroma/                # ChromaDB 向量库
│   └── {collection_name}/
│       ├── chroma.sqlite3
│       └── *.bin
├── annotations/           # 标注数据 (JSON)
│   └── {name}_annotations.json
├── stats/                 # 统计报告 (JSON)
│   └── {name}_stats.json
└── cache/                 # 断点缓存 (JSON)
    └── {name}_checkpoint.json
```

## 🔧 命令行选项

```bash
# 基础选项
--source, -s DIR      源目录(包含 TXT 文件)
--name, -n NAME       语料库名称
--genre, -g GENRE     题材类型

# 处理选项
--max-chunk-size N    最大块大小(默认 2000)
--min-chunk-size N    最小块大小(默认 100)
--overlap N           块重叠(默认 200)
--batch-size N        AI 标注批量大小(默认 5)

# 输出选项
--stats               查看统计信息
--export FORMAT       导出标注 (json/yaml)
--output, -o PATH     输出文件路径
--verbose, -v         详细输出

# 高级选项
--checkpoint FILE     断点文件路径
--memory-limit MB     内存限制(默认 2500)
--no-cache            禁用缓存
```

## 🎯 使用场景

| 场景 | 命令示例 |
|------|----------|
| **构建打斗题材语料库** | `--source ./novels --name 玄幻打斗 --genre 玄幻` |
| **查看语料库统计** | `--stats --collection 玄幻打斗` |
| **导出标注数据** | `--export json --collection 玄幻打斗 --output results.json` |
| **增量更新语料库** | `--source ./new_chapters --name 玄幻打斗 --checkpoint auto` |

> 💡 **需要检索语料？** 请使用 [`corpus-search`](../corpus-search) 技能：
> ```bash
> cd ~/.openclaw/workspace/skills/corpus-search
> python3 scripts/search_corpus.py -q "精彩打斗" -c 玄幻打斗 --scene 打斗 --min-quality 8
> ```

## ⚙️ 配置文件

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

memory:
  limit_mb: 2500
```

## 🐛 故障排除

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

使用规则降级方案,标注结果仍可生成,只是质量得分较低。

```bash
# 无需额外配置,自动降级
python3 scripts/build_corpus.py --source ./novels --name test
```

### ChromaDB 错误

```bash
# 删除向量库重新构建
rm -rf corpus/chroma/{collection_name}
python3 scripts/build_corpus.py --source ./novels --name test
```

### sqlite3 版本过低

```bash
# 使用 pysqlite3 包装器
python3 scripts/run_with_pysqlite3.py scripts/build_corpus.py --source ./novels --name test
```

## 🧪 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行代码质量检查
ruff check scripts/

# 运行测试
pytest tests/
```

## 📝 变更日志

详见 [CHANGELOG.md](CHANGELOG.md)

## 📄 许可证

MIT License

## 👥 作者

OpenClaw Community

## 🔗 相关链接

- [GitHub 仓库](https://github.com/openclaw/openclaw)
- [ClawHub 页面](https://clawhub.ai/yuzhihui886/corpus-builder)
- [问题反馈](https://github.com/openclaw/openclaw/issues)
- [OpenClaw 文档](https://docs.openclaw.ai)
