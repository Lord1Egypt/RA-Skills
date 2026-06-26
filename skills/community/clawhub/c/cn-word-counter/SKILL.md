slug: cn-word-counter
name: 中文字数统计
version: "1.0.0"
author: 千策

# 中文字数统计

## 核心功能

统计文本的字数、字符数、行数。

## 使用方式

```bash
python3 scripts/word_counter.py "要统计的文本内容"
```

## 脚本说明

scripts/word_counter.py
- `count_words(text: str)` → `dict`: 返回 {words, chars, lines}

## 输出示例

```json
{
  "words": 125,
  "chars": 256,
  "lines": 8
}
```

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
