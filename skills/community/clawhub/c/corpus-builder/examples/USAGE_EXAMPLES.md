# Corpus Builder - 使用示例

本目录包含 Corpus Builder 的使用示例。

## 示例 1: 构建语料库

```bash
# 1. 准备源文件（TXT 格式）
mkdir -p ~/novels/reference
cp /path/to/your/novels/*.txt ~/novels/reference/

# 2. 构建语料库
cd ~/.openclaw/workspace/skills/corpus-builder

python3 scripts/build_corpus.py \
    --source ~/novels/reference \
    --name 玄幻打斗 \
    --genre 玄幻 \
    --verbose
```

## 示例 2: 查看统计信息

```bash
python3 scripts/build_corpus.py \
    --stats \
    --collection 玄幻打斗
```

## 示例 3: 语义搜索

```bash
# 搜索高质量打斗场景
python3 scripts/build_corpus.py \
    --search "紧张的围攻场景" \
    --collection 玄幻打斗 \
    --filter "scene_type=打斗,emotion=紧张,quality_score>=8" \
    --limit 10
```

## 示例 4: 导出标注

```bash
# 导出为 JSON
python3 scripts/build_corpus.py \
    --export json \
    --collection 玄幻打斗 \
    --output ./annotations.json

# 导出为 YAML
python3 scripts/build_corpus.py \
    --export yaml \
    --collection 玄幻打斗 \
    --output ./annotations.yaml
```

## 示例 5: 增量更新

```bash
# 添加新文件到现有语料库
python3 scripts/build_corpus.py \
    --source ~/novels/new_files \
    --name 玄幻打斗 \
    --checkpoint ./corpus/cache/last_checkpoint.json
```

## 示例 6: 自定义配置

```bash
# 创建自定义配置文件
cat > my_config.yml << 'EOF'
chunking:
  max_chunk_size: 1500
  min_chunk_size: 50
  overlap: 100

processing:
  batch_size: 10

memory:
  limit_mb: 2000
EOF

# 使用自定义配置
python3 scripts/build_corpus.py \
    --source ~/novels/reference \
    --name 玄幻打斗 \
    --config my_config.yml
```

## 输出结构

构建完成后，语料库将包含：

```
corpus/
├── chroma/                    # ChromaDB 向量库
│   └── 玄幻打斗/
│       ├── chroma.sqlite3
│       └── *.bin
├── annotations/               # 标注数据 (JSON)
│   ├── 玄幻打斗_annotations.json
│   └── 玄幻打斗_stats.json
├── cache/                     # 断点缓存 (JSON)
│   └── 玄幻打斗_cache.json
└── default_config.yml         # 默认配置
```

## 高级用法

### 自定义过滤条件

```bash
# 搜索慢节奏的修炼场景
python3 scripts/build_corpus.py \
    --search "突破瓶颈" \
    --collection 玄幻打斗 \
    --filter "scene_type=修炼,pace=慢节奏" \
    --limit 5

# 搜索多人对话场景
python3 scripts/build_corpus.py \
    --search "激烈争论" \
    --collection 玄幻打斗 \
    --filter "scene_type=对话,character_count=多人" \
    --limit 10
```

### 批量处理多个语料库

```bash
#!/bin/bash
# build_all.sh

# 构建打斗语料库
python3 scripts/build_corpus.py \
    --source ~/novels/reference \
    --name 玄幻打斗 \
    --genre 玄幻

# 构建修炼语料库
python3 scripts/build_corpus.py \
    --source ~/novels/reference修炼 \
    --name 玄幻修炼 \
    --genre 玄幻

# 构建对话语料库
python3 scripts/build_corpus.py \
    --source ~/novels/reference对话 \
    --name 玄幻对话 \
    --genre 玄幻
```

## 故障排除

### 1. 内存不足

```bash
# 降低内存限制
python3 scripts/build_corpus.py \
    --source ~/novels/reference \
    --name test \
    --memory-limit 1500 \
    --batch-size 3
```

### 2. LLM 调用失败

系统会自动降级为规则标注，标注结果仍可生成，只是质量得分较低。

### 3. ChromaDB 错误

```bash
# 删除向量库重新构建
rm -rf corpus/chroma/{collection_name}
python3 scripts/build_corpus.py --source ~/novels/reference --name test
```

### 4. JSON 解析失败

重试次数达到上限后，系统自动降级为规则标注。

## 性能优化

### 批量大小调整

```bash
# 更大的批量（更快，但需要更多内存）
python3 scripts/build_corpus.py \
    --source ~/novels/reference \
    --name test \
    --batch-size 10 \
    --memory-limit 3000

# 更小的批量（更慢，但更稳定）
python3 scripts/build_corpus.py \
    --source ~/novels/reference \
    --name test \
    --batch-size 3 \
    --memory-limit 1500
```

### 块大小调整

```bash
# 更小的块（更多块，更精细）
python3 scripts/build_corpus.py \
    --source ~/novels/reference \
    --name test \
    --max-chunk-size 1000 \
    --overlap 100

# 更大的块（更少块，更粗略）
python3 scripts/build_corpus.py \
    --source ~/novels/reference \
    --name test \
    --max-chunk-size 3000 \
    --overlap 300
```

## 下一步

- 查看 `corpus/annotations/` 中的标注数据
- 使用 `--search` 进行语义检索
- 根据检索结果优化标注
- 定期导出和备份标注数据

---

**Created for OpenClaw** 🦞  
**Version**: 1.0.0  
**Last Updated**: 2026-03-28
