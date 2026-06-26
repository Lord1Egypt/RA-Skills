---
name: Core Vocabulary for CET-4
description: Randomly generates one or more words from a curated database of 300 must-know College English Test Band 4 (CET-4) vocabulary.
metadata: { "openclaw": { "emoji": "🚀",  "requires": { "bins": ["shell"] } } }
---

# Core Vocabulary for CET-4(300)
从本地词库word.txt中读取单词返回给用户，本地词库的获取不消费token，请放心使用
## Usage
根据用户对话提取单词个数N，从word.txt文件中随机读取N条，返回给用户。
# Examples
读取一条数据为[curriculum#/kəˈrɪkjələm/#n. 课程#The school curriculum includes math and science.#学校课程包括数学和科学。]
使用#进行切分返回级用户下面信息：
word: "curriculum",
phonetic: "/kəˈrɪkjələm/",
meaning": "n. 课程",
sentence_en: "The school curriculum includes math and science.",
sentence_cn: "学校课程包括数学和科学。"
## Current Status

Fully functional.
