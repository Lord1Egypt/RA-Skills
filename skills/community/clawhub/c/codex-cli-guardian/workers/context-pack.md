# Context Pack 模板

给 worker 提供无法自行推断的上下文时使用。

## 格式

```
Goal: <目标——"完成"是什么意思>
Non-goals: <不做什么>
Constraints: <约束——风格、边界、必须保留、不能改变>
Pointers: <关键文件、目录、文档、链接>
Prior decisions: <之前的决定及原因>
Success check: <如何判断完成——测试、标准、检查清单>
```

## 何时使用

**使用 Context Pack 当：**
- 工作涉及有历史的项目
- 目标不明确
- 约束不明显
- 偏好很重要

**跳过当：**
- 简单查网页
- 小范围孤立编辑
- 简单的一次性任务

## 示例

```
Goal: 爬虫能正确爬取豆瓣 Top250 并保存 CSV
Non-goals: 不做数据清洗、不保存图片
Constraints:
  - 使用 requests + BeautifulSoup（不能用 Scrapy）
  - 每页间隔 2-4 秒随机延迟
  - 输出 UTF-8 CSV
Pointers:
  - 输出文件：douban_top250.py（同目录）
  - 工作目录：~/projects/spider/
Success check:
  - `python douban_top250.py` 无报错
  - 生成 douban_top250.csv 包含 250 条数据
  - CSV 包含列：rank, title, director, score
```

---

*来源：codex-orchestration skill*
