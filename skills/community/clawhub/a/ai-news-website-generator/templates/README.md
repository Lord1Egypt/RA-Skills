# AI资讯网站生成器

一键生成完整的AI资讯聚合网站！

## 快速开始

### Docker部署（推荐）

```bash
docker-compose up -d --build
```

### 本地部署

```bash
chmod +x start.sh
./start.sh
```

## 访问地址

- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 配置RSS源

编辑 `backend/main.py` 中的 `RSS_FEEDS`：

```python
RSS_FEEDS = [
    {"name": "你的RSS源", "url": "https://example.com/rss.xml", "category": "分类"},
]
```

## 修改刷新频率

编辑 `backend/main.py`：

```python
# 每6小时刷新
scheduler.add_job(refresh_articles, 'interval', hours=6, id='refresh_rss')

# 改为每小时刷新
scheduler.add_job(refresh_articles, 'interval', hours=1, id='refresh_rss')
```

## 技术栈

- **前端**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **后端**: Python + FastAPI + feedparser + APScheduler
- **部署**: Docker + Docker Compose

## 项目结构

```
ai-news-website/
├── frontend/                 # Next.js 前端
│   ├── app/
│   │   ├── page.tsx         # 首页
│   │   └── layout.tsx       # 布局
│   ├── Dockerfile
│   └── package.json
├── backend/                  # FastAPI 后端
│   ├── main.py              # 主应用
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── start.sh
└── README.md
```

## API接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/articles` | 获取文章列表 |
| GET | `/api/articles/{id}` | 获取单篇文章 |
| POST | `/api/refresh` | 手动刷新 |
| GET | `/api/sources` | 获取来源列表 |
| GET | `/api/categories` | 获取分类列表 |
| GET | `/api/health` | 健康检查 |

## 常用命令

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 重新构建
docker-compose up -d --build
```

## 许可证

MIT License
