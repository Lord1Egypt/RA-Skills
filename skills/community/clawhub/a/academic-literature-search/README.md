# 学术文献检索技能

一个专注于文献检索的 OpenClaw 技能，提供快速、准确、全面的学术文献检索服务。

## 功能特性

- **多数据库集成**: Semantic Scholar、Crossref、PubMed、arXiv
- **高级检索**: 布尔搜索、字段限定、范围搜索
- **智能处理**: 去重、排序、过滤、结果丰富
- **多格式输出**: Markdown、JSON、CSV、BibTeX、RIS、Excel
- **性能优化**: 并发检索、智能缓存、渐进式加载

## 安装

### 方法一：通过 OpenClaw 安装

```bash
openclaw skill install academic-literature-search
```

### 方法二：手动安装

1. 克隆仓库：

```bash
git clone https://github.com/jibeilindong/academic-literature-search.git
cd academic-literature-search
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置环境变量（可选但推荐）：

```bash
export SEMANTIC_SCHOLAR_API_KEY="your_email@example.com"
export CROSSREF_API_EMAIL="your_email@example.com"
export PUBMED_API_KEY="your_api_key"
```

4. 复制配置文件：

```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml 进行配置
```

## 使用方法

### Python API

```python
import asyncio
from agent import AcademicLiteratureSearchSkill

async def main():
    skill = AcademicLiteratureSearchSkill()
    
    params = {
        "query": "large language models in healthcare",
        "databases": ["semantic_scholar", "crossref"],
        "max_results": 50,
        "year_range": "2020-2024"
    }
    
    result = await skill.execute(params)
    print(result["results"])

asyncio.run(main())
```

### 作为库使用

```python
import asyncio
from agent import LiteratureSearchEngine

async def search():
    async with LiteratureSearchEngine() as engine:
        papers = await engine.search(
            query="reinforcement learning",
            databases=["semantic_scholar", "arxiv"],
            max_results=20
        )
        for paper in papers:
            print(f"{paper.title} - {paper.citation_count} citations")

asyncio.run(search())
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | string | 必需 | 检索查询字符串 |
| databases | array | ["semantic_scholar", "crossref"] | 使用的数据库 |
| max_results | integer | 50 | 最大返回数量 |
| year_range | string | - | 年份范围，如 "2020-2024" |
| sort_by | string | "relevance" | 排序方式 (relevance, citations, year) |
| sort_order | string | "desc" | 排序顺序 (asc, desc) |
| open_access_only | boolean | false | 仅开放获取 |
| min_citations | integer | - | 最小引用数 |
| output_format | string | "markdown" | 输出格式 |
| output_file | string | - | 输出文件路径 |
| interactive | boolean | false | 交互式模式 |
| cache | boolean | true | 启用缓存 |

## 支持的数据库

| 数据库 | 数据量 | 优势领域 | 速率限制 |
|--------|--------|----------|----------|
| Semantic Scholar | 2.33亿+ | AI、计算机科学 | 100请求/5分钟（无认证） |
| Crossref | 1.4亿+ | 期刊文章、DOI | 无限制（礼貌使用） |
| arXiv | 220万+ | 预印本 | 无限制 |
| PubMed | 3500万+ | 生物医学 | 10请求/秒 |

## 输出格式示例

### Markdown

```markdown
# 文献检索结果

**检索词**: deep learning in medical imaging
**检索时间**: 2024-01-15 14:30:00
**结果数量**: 20篇

## 检索结果

### 1. Deep Learning for Medical Image Analysis
- **作者**: Geert Litjens, Thijs Kooi, et al.
- **出版信息**: 2017年 | Medical Image Analysis
- **引用数**: 4231
- **标识符**: DOI: 10.1016/j.media.2017.07.005
- **访问**: [原文链接](url) | 🔓 开放获取
```

### BibTeX

```bibtex
@article{Litjens_2017,
  title = {Deep Learning for Medical Image Analysis},
  author = {Geert Litjens and Thijs Kooi},
  year = {2017},
  journal = {Medical Image Analysis},
  doi = {10.1016/j.media.2017.07.005}
}
```

## 高级功能

### 1. 缓存系统

- 内存缓存：5分钟 TTL
- 磁盘缓存：1小时 TTL
- 智能缓存键生成

### 2. 并发检索

- 并行查询多个数据库
- 智能请求调度
- 速率限制处理

### 3. 错误处理

- 自动重试机制
- 优雅降级
- 详细的错误信息

## 配置

### 环境变量

```bash
# API 密钥
SEMANTIC_SCHOLAR_API_KEY    # Semantic Scholar API
CROSSREF_API_EMAIL          # Crossref 邮箱
PUBMED_API_KEY              # PubMed API

# 网络配置
HTTP_PROXY
HTTPS_PROXY
LITERATURE_SEARCH_TIMEOUT

# 缓存配置
LITERATURE_SEARCH_CACHE_ENABLED
LITERATURE_SEARCH_CACHE_DIR
```

### 配置文件

编辑 `config.yaml`：

```yaml
search:
  default_max_results: 100
  default_databases: ["semantic_scholar", "crossref", "pubmed"]

cache:
  enabled: true
  memory_cache_ttl: 600  # 10分钟

output:
  default_format: "json"
  auto_save: true
```

## 故障排除

### 常见问题

1. **API 速率限制**
   - 申请 Semantic Scholar API 密钥
   - 提供 Crossref 邮箱
   - 启用缓存减少请求

2. **网络问题**
   - 检查网络连接
   - 配置代理服务器
   - 增加超时时间

3. **无结果**
   - 检查查询语法
   - 尝试英文关键词
   - 扩大检索范围

### 调试模式

```bash
export LITERATURE_SEARCH_LOG_LEVEL=DEBUG
```

## 项目结构

```
academic-literature-search/
├── SKILL.md              # 技能描述
├── agent.py              # 主执行逻辑
├── skill.json            # 技能元信息
├── requirements.txt     # Python 依赖
├── config.example.yaml  # 配置示例
├── tests/                # 测试文件
└── README.md             # 使用说明
```

## 运行测试

```bash
pip install pytest pytest-asyncio
pytest tests/
```

## 许可证

MIT License

## 支持

- 问题报告: [GitHub Issues](https://github.com/openclaw/skills/issues)
- 文档: [OpenClaw Docs](https://docs.openclaw.dev)
- 社区: [Discord](https://discord.gg/openclaw)
