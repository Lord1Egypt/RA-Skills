# cn-emoji-tool

中文Emoji翻译与搜索工具。支持Emoji含义查询、关键词搜索Emoji、中文描述转Emoji。

## 使用场景

- 想知道某个Emoji的中文含义
- 用中文关键词搜索对应Emoji
- 批量转换文本中的关键词为Emoji

## 功能

1. **含义查询**：输入Emoji，返回中英文含义、分类
2. **关键词搜索**：输入中文关键词，返回匹配的Emoji列表
3. **文本Emoji化**：将文本中的关键词自动替换为对应Emoji

## 使用方法

```bash
# 查询Emoji含义
python3 scripts/emoji_tool.py --query "🔥"

# 关键词搜索Emoji
python3 scripts/emoji_tool.py --search "开心"

# 文本Emoji化
python3 scripts/emoji_tool.py --text "今天天气真好"
```

## 依赖

纯Python标准库，无需额外安装。

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
