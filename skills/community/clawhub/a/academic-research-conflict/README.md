# academic-research

学术文献检索客户端

## 功能

- search_papers
- get_paper_detail
- search_authors

## 配置

复制 `.env.example` 到 `.env` 并配置参数。

## 使用方法

```python
from academic_client import AcademicResearchClient

client = AcademicResearchClient()
client.initialize()

# 使用功能
result = client.search_papers()
result = client.get_paper_detail()

client.close()
```

## 测试

```bash
python tests/test_client.py
```
