---
slug: cn-regex-tester
name: 正则表达式测试器
version: "1.2.1"
author: 千策
---

# 正则表达式测试器

输入正则表达式和文本，返回匹配结果。纯Python标准库，无需API Key。

## 功能

- **正则匹配**：查找所有匹配项
- **正则替换**：将匹配内容替换为空（删除匹配）
- **JSON输出**：结构化输出，便于程序处理

## 使用方法

```bash
python3 scripts/regex_tester.py <正则表达式> <文本>
```

## 示例

```bash
# 匹配数字
python3 scripts/regex_tester.py '\d+' 'hello123world456'
# 输出: {"matches": ["123", "456"], "count": 2}

# 匹配单词
python3 scripts/regex_tester.py '[a-z]+' 'Hello World'
# 输出: {"matches": ["ello", "orld"], "count": 2}

# 匹配邮箱
python3 scripts/regex_tester.py '\w+@\w+\.\w+' 'test@example.com'
# 输出: {"matches": ["test@example.com"], "count": 1}

# 替换（删除匹配）
python3 scripts/regex_tester.py '\d+' 'order123 price456'
# 输出: {"result": "order price"}
```

## 输出格式

```json
{
  "matches": ["匹配结果列表"],
  "count": 匹配数量,
  "result": "替换后的文本（替换模式下）"
}
```

## 分类

开发工具

## 关键词

正则, regex, 正则表达式, 测试, tester, match

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
