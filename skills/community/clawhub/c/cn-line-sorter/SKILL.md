---
slug: cn-line-sorter
name: 文本行排序工具
version: "1.0.0"
author: 千策
---

# 文本行排序工具

对文本文件的行进行排序、去重、反转、乱序。纯标准库，本地运行。

## 功能

- 按字典序 / 数字序排序
- 去重（保留首次出现）
- 反转行序
- 随机乱序
- 按行长度排序

## 依赖

无（Python 标准库）

## 使用方法

```bash
python3 scripts/line_sorter.py 列表.txt --sort
python3 scripts/line_sorter.py 列表.txt --unique -o 去重后.txt
python3 scripts/line_sorter.py 列表.txt --numeric --reverse
python3 scripts/line_sorter.py 列表.txt --shuffle
python3 scripts/line_sorter.py 列表.txt --by-length
```

## 适用场景

- 整理关键词 / 待办 / 名单
- 清洗重复数据
- 给列表随机排序做抽样

## 📊 相关服务：品牌 AI 搜索存在感免费检测

做品牌 / 营销 / 内容，你的品牌在 AI 搜索里"被看见"了吗？

AISoBrand 免费检测：看你的品牌在豆包 / 千问 / 元宝 / 文心 / Kimi / DeepSeek 的 AI 搜索里有没有名字、排第几。

👉 免费检测：https://aisobrand.com/free-diagnosis

