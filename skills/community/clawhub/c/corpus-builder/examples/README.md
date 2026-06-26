# 示例语料库数据

本目录包含 Corpus Builder 的示例数据。

## 文件说明

| 文件 | 说明 |
|------|------|
| `example_annotations.json` | 示例标注数据（10 条） |
| `example_stats.json` | 示例统计信息 |
| `sample_text.txt` | 示例文本（用于测试） |

## 示例标注数据结构

```json
{
    "id": "chunk_000001",
    "scene_type": ["打斗"],
    "emotion": ["紧张", "热血"],
    "techniques": ["细节描写", "侧面描写"],
    "pace": "快节奏",
    "pov": "第三人称限知",
    "character_count": "多人 (3+)",
    "power_level": "炼气期",
    "key_elements": ["围攻", "剑法", "后发先至"],
    "usage": ["学习打斗描写", "学习紧张氛围营造"],
    "quality_score": 8,
    "original_text": "张三被五人围攻...",
    "source_file": "没钱修什么仙.txt",
    "embedding": [0.1, 0.2, -0.3, ...]
}
```

## 示例统计信息

```json
{
    "collection_name": "玄幻打斗",
    "genre": "玄幻",
    "total_chunks": 156,
    "total_files": 3,
    "avg_chunk_size": 1523,
    "scene_type_dist": {
        "打斗": 85,
        "对话": 32,
        "修炼": 20,
        "探险": 12,
        "其他": 7
    },
    "emotion_dist": {
        "紧张": 68,
        "热血": 45,
        "中性": 28,
        "轻松": 15
    },
    "avg_quality_score": 7.2,
    "processed_time": "2026-03-28T12:00:00"
}
```

## 使用示例

```bash
# 1. 构建测试语料库
cd ~/.openclaw/workspace/skills/corpus-builder

python3 scripts/build_corpus.py \
    --source examples \
    --name test_corpus \
    --genre test

# 2. 查看统计
python3 scripts/build_corpus.py \
    --stats \
    --collection test_corpus

# 3. 语义搜索
python3 scripts/build_corpus.py \
    --search "紧张的围攻" \
    --collection test_corpus
```

## 数据格式说明

### 标注数据字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一 ID |
| `scene_type` | list | 场景类型（多选） |
| `emotion` | list | 情绪基调（多选） |
| `techniques` | list | 写作手法（多选） |
| `pace` | string | 节奏快慢 |
| `pov` | string | 视角类型 |
| `character_count` | string | 角色数量 |
| `power_level` | string | 力量层级 |
| `key_elements` | list | 关键元素 |
| `usage` | list | 适用场景 |
| `quality_score` | int | 质量评分（1-10） |
| `original_text` | string | 原始文本 |
| `source_file` | string | 来源文件 |
| `embedding` | list | 向量表示 |

### 统计数据字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `collection_name` | string | 语料库名称 |
| `genre` | string | 题材类型 |
| `total_chunks` | int | 总块数 |
| `total_files` | int | 总文件数 |
| `avg_chunk_size` | float | 平均块大小 |
| `scene_type_dist` | dict | 场景类型分布 |
| `emotion_dist` | dict | 情绪分布 |
| `avg_quality_score` | float | 平均质量分 |
| `processed_time` | string | 处理时间 |

---

**Created for OpenClaw** 🦞  
**Version**: 1.0.0  
**Last Updated**: 2026-03-28
