---
name: ai-news-website-generator
description: AI资讯网站生成器 - 一键构建智能内容聚合平台
version: 1.0.0
author: 爱马仕
license: MIT
metadata:
  hermes:
    tags: [ai-news, rss, website-generator, nextjs, fastapi, docker, fullstack, automation]
    related_skills: [multi-agent-coordination, architecture-diagram]
---

# AI资讯网站生成器

一键生成完整的AI资讯聚合网站！包含Next.js前端、FastAPI后端、Docker容器化部署、以及自动定时刷新功能。不仅适用于AI新闻，也适用于任何RSS源的内容聚合。

## 核心特性

- ✅ **一键生成** - 完整的项目结构，开箱即用
- ✅ **多源RSS聚合** - 支持配置任意RSS源
- ✅ **自动去重** - 基于内容哈希的智能去重
- ✅ **定时刷新** - 内置APScheduler，可配置刷新间隔
- ✅ **Docker部署** - 一键启动，跨平台兼容
- ✅ **响应式设计** - 支持移动端和桌面端
- ✅ **分类筛选** - 按来源和类别筛选内容
- ✅ **无限滚动** - 流畅的浏览体验

## 技术栈

| 层级 | 技术选型 |
|------|----------|
| **前端** | Next.js 15 + React 19 + TypeScript + Tailwind CSS |
| **后端** | Python + FastAPI + feedparser + APScheduler |
| **部署** | Docker + Docker Compose |

## 快速开始

### 1. 生成项目（30秒搞定！）

```bash
# 运行项目生成脚本
python ~/.hermes/skills/productivity/ai-news-website-generator/scripts/generate-project.py

# 或者指定项目目录
python ~/.hermes/skills/productivity/ai-news-website-generator/scripts/generate-project.py my-news-site
```

脚本会自动创建完整的项目结构，包含：
- ✅ Next.js 前端（带漂亮的深色主题）
- ✅ FastAPI 后端（含自动刷新）
- ✅ Docker 配置（一键部署）
- ✅ 启动脚本（本地/Docker双模式）

### 2. 配置RSS源

编辑 `backend/main.py` 中的 `RSS_FEEDS`：

```python
RSS_FEEDS = [
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "category": "AI"},
    {"name": "你的RSS源", "url": "https://example.com/rss.xml", "category": "科技"},
]
```

### 3. 启动项目

```bash
cd ai-news-website
docker-compose up -d
```

### 4. 访问网站

- 前端：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

## 项目结构

```
ai-news-website/
├── frontend/                 # Next.js 前端
│   ├── app/
│   │   ├── page.tsx         # 首页
│   │   ├── layout.tsx       # 布局
│   │   └── globals.css      # 全局样式
│   ├── components/
│   │   ├── NewsList.tsx     # 新闻列表
│   │   └── NewsCard.tsx     # 新闻卡片
│   ├── Dockerfile
│   └── package.json
├── backend/                  # FastAPI 后端
│   ├── main.py              # 主应用（含定时任务）
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml        # Docker编排
├── start.sh                  # 一键启动脚本
├── README.md                 # 详细文档
└── PROJECT_SUMMARY.md        # 项目总结
```

## 自定义配置

### 修改刷新频率

编辑 `backend/main.py`：

```python
# 每6小时刷新
scheduler.add_job(refresh_articles, 'interval', hours=6, id='refresh_rss')

# 改为每小时刷新
scheduler.add_job(refresh_articles, 'interval', hours=1, id='refresh_rss')

# 改为每30分钟刷新
scheduler.add_job(refresh_articles, 'interval', minutes=30, id='refresh_rss')
```

### 修改端口

编辑 `docker-compose.yml`：

```yaml
services:
  frontend:
    ports:
      - "3000:3000"  # 改为 "8080:3000"
  
  backend:
    ports:
      - "8000:8000"  # 改为 "8081:8000"
```

## API接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/articles` | 获取文章列表 |
| GET | `/api/articles/{id}` | 获取单篇文章 |
| POST | `/api/refresh` | 手动刷新所有RSS源 |
| GET | `/api/health` | 健康检查 |

### 查询参数

```
GET /api/articles?page=1&limit=20&source=OpenAI&category=AI
```

## 使用场景

### 1. AI资讯门户网站

配置AI相关的RSS源（OpenAI、Google AI、MIT AI等），快速搭建AI资讯门户。

### 2. 技术博客聚合

聚合你喜欢的技术博客，打造个人技术阅读中心。

### 3. 行业资讯平台

为特定行业（区块链、生物医药、金融科技等）聚合专业资讯。

### 4. 团队知识门户

聚合团队内部博客和外部行业资讯，作为团队知识库。

## 部署建议

### 生产环境部署

1. **使用Nginx反向代理**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

2. **配置HTTPS（Let's Encrypt）**

```bash
certbot --nginx -d your-domain.com
```

3. **数据持久化**

当前版本使用内存存储，生产环境建议：
- 添加SQLite/PostgreSQL数据库
- 使用Redis缓存
- 添加文章搜索功能

## 扩展功能建议

### 第二阶段功能

- [ ] 用户账户系统
- [ ] 文章收藏和点赞
- [ ] 邮件订阅推送
- [ ] 社交媒体分享
- [ ] 文章搜索功能

### 第三阶段功能

- [ ] 个性化推荐
- [ ] AI摘要生成
- [ ] 多语言支持
- [ ] 数据分析面板
- [ ] 移动端App

## 实战案例

### 案例：创建区块链资讯站

1. 配置区块链相关RSS源
2. 修改前端主题色为区块链风格
3. 部署到服务器
4. 配置域名和HTTPS
5. 启动！

### 案例：团队内部技术周报

1. 配置团队博客和技术媒体RSS
2. 每周一定期刷新
3. 团队成员通过内网访问
4. 作为每周技术分享的素材库

## 常见问题

### Q: 如何添加更多RSS源？

A: 编辑 `backend/main.py` 中的 `RSS_FEEDS` 列表，添加新的源即可。

### Q: 刷新失败怎么办？

A: 检查网络连接，确认RSS源URL可访问。查看后端日志：`docker-compose logs backend`

### Q: 如何修改前端样式？

A: 编辑 `frontend/app/globals.css` 和组件文件，使用Tailwind CSS类。

### Q: 可以不使用Docker吗？

A: 可以！使用 `start.sh` 脚本选择本地启动模式，或参考README中的手动启动步骤。

## 商业价值

### 作为SaaS服务

- 提供在线网站生成器，按站点数收费
- 提供托管服务，按月订阅
- 提供高级功能（自定义域名、数据分析等）

### 作为技术解决方案

- 为企业定制内部资讯门户
- 为媒体客户提供内容聚合方案
- 作为开发者工具包销售

### 开源社区价值

- 成为热门开源项目
- 建立开发者社区
- 吸引贡献者共同维护

## 相关资源

- [Next.js 文档](https://nextjs.org/docs)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Docker 文档](https://docs.docker.com/)
- [Tailwind CSS](https://tailwindcss.com/)

## 许可证

MIT License - 可自由使用、修改和分发。

---

**使用此Skill，你可以在5分钟内从0到1搭建一个专业的资讯聚合网站！** 🚀
