---
name: corpus-search
description: "语料检索工具，与 corpus-builder 配合使用。支持语义搜索、元数据过滤（场景/情绪/节奏/质量）。Use when: 需要搜索语料库中的小说片段、按场景类型过滤、查找特定情绪/节奏的描写、检索高质量写作素材。"
---

# Corpus Search - 语料检索工具

与 corpus-builder 配合使用的语料检索工具，支持语义搜索和元数据过滤。

## 快速开始

```bash
cd ~/.openclaw/workspace/skills/corpus-search

# 基础搜索
python3 scripts/search_corpus.py -q "紧张的打斗场景" -c xuanhuan-full --limit 10

# 按场景过滤
python3 scripts/search_corpus.py -q "围攻" -c xuanhuan-full --scene 打斗 --limit 5

# 按情绪过滤
python3 scripts/search_corpus.py -q "修炼" -c xuanhuan-full --emotion 紧张 --limit 10

# JSON 输出
python3 scripts/search_corpus.py -q "突破" -c xuanhuan-full --json
```

## 命令行选项

| 选项 | 说明 |
|------|------|
| `-q, --query` | 搜索查询（必填） |
| `-c, --collection` | 语料库名称（必填） |
| `--limit` | 返回数量（默认 10） |
| `--scene` | 场景过滤（打斗/修炼/对话/探险等） |
| `--emotion` | 情绪过滤（紧张/轻松/悲伤/热血等） |
| `--min-quality` | 最低质量分（1-10） |
| `--json` | JSON 格式输出 |
| `--export` | 导出到文件 |
| `--verbose` | 详细输出 |

## 输出示例

```
🔍 搜索结果：紧张的打斗场景
   语料库：xuanhuan-full
   返回数量：5

1. 相似度：87.5%
   场景：打斗
   情绪：紧张，热血
   节奏：快节奏
   来源：没钱修什么仙_第 1-10 章.txt

   内容预览:
   张羽只觉胸口一痛，低头看去，只见一柄长剑已刺入...
```

## 依赖

```bash
pip3 install -r requirements.txt --user
```

## 配置

编辑 `configs/default_config.yml` 修改语料库路径。

## 相关文件

- `scripts/search_corpus.py` - 主程序
- `configs/default_config.yml` - 配置文件

---

**Version**: 1.0.0
