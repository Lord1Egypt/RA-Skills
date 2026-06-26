---
name: cn-trends-ai
version: "1.3.0"
description: "获取知乎、微博、百度、B站实时热搜榜单。"
---

# 中文热搜聚合

获取4大平台实时热搜。

## 功能
- 知乎热榜
- 微博热搜
- 百度热搜
- B站排行榜
- 统一格式输出、关键词过滤

## 用法
python3 scripts/fetch_all_trends.py --all
python3 scripts/fetch_all_trends.py --platform zhihu --limit 10
python3 scripts/fetch_all_trends.py --all --keyword "AI" --json

## 依赖
- Python 3.7+
- certifi（SSL证书验证）

## 数据来源
所有数据来自公开接口，无需登录，无需API Key。

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
