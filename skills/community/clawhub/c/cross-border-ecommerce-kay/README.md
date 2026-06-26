# 🛒 跨境电商选品工具 MVP

一个帮助跨境电商卖家快速分析产品机会的最小可用工具。

## 功能特性

### 1. 关键词分析
- 输入品类关键词，返回搜索量、竞争度、趋势
- 相关关键词推荐
- 建议竞价参考

### 2. 竞品分析
- 抓取亚马逊/eBay同类产品
- 分析价格、评分、销量
- 市场概况统计

### 3. 利润计算器
- 支持 Amazon/eBay 平台
- 多种费用自动计算（佣金、FBA费用等）
- 利润率分析
- 建议售价计算

### 4. AI Listing 生成
- 基于关键词和竞品数据生成优化标题
- 生成5点描述
- 生成完整产品描述
- 推荐关键词标签
- 建议售价

## 技术栈

- **后端**: Python 3.9+ / Flask 3.0
- **数据库**: MySQL / Redis (可选)
- **AI**: OpenAI API (可选，无API Key时使用模拟数据)
- **前端**: HTML5 + CSS3 + Vanilla JS

## 项目结构

```
projects/cross-border-ecommerce/
├── app.py                     # Flask主应用
├── models.py                  # 数据模型
├── services/
│   ├── __init__.py
│   ├── keyword_analyzer.py    # 关键词分析服务
│   ├── competitor_scraper.py  # 竞品爬虫服务
│   ├── profit_calculator.py   # 利润计算器
│   └── ai_listing.py          # AI Listing生成
├── templates/
│   └── index.html             # 前端页面
├── static/
├── requirements.txt
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
cd projects/cross-border-ecommerce
pip install -r requirements.txt
```

### 2. 配置环境变量 (可选)

```bash
# 创建 .env 文件
cat > .env << EOF
FLASK_DEBUG=true
PORT=5000
OPENAI_API_KEY=your_api_key_here  # 可选，不提供则使用模拟数据
EOF
```

### 3. 启动应用

```bash
# 开发模式
python app.py

# 或者使用 gunicorn (生产环境)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 4. 访问应用

打开浏览器访问: http://localhost:5000

## Docker 部署

```bash
# 构建镜像
docker build -t ecommerce-mvp .

# 运行容器
docker run -d -p 5000:5000 --env-file .env ecommerce-mvp
```

## Docker Compose (MySQL + Redis + App)

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_DEBUG=false
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - mysql
      - redis
  
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=ecommerce
  
  redis:
    image: redis:7-alpine
```

运行: `docker-compose up -d`

## API 接口

### 关键词分析

```bash
POST /api/keyword/analyze
Content-Type: application/json

{"keyword": "wireless earbuds"}
```

### 竞品分析

```bash
POST /api/competitor/scrape
Content-Type: application/json

{"keyword": "laptop stand", "platform": "amazon", "limit": 10}
```

### 利润计算

```bash
POST /api/profit/calculate
Content-Type: application/json

{
  "platform": "amazon",
  "product_cost": 10,
  "shipping_cost": 3,
  "selling_price": 35,
  "other_cost": 1,
  "is_fba": true
}
```

### AI 生成 Listing

```bash
POST /api/ai/generate-listing
Content-Type: application/json

{
  "product_name": "Portable Bluetooth Speaker",
  "target_market": "US",
  "include_keyword_analysis": true,
  "include_competitor_analysis": true,
  "platform": "amazon"
}
```

## 数据来源说明

当前版本使用**模拟数据**进行验证：

- 关键词搜索量、竞争度等数据为预设模拟值
- 竞品数据为随机生成的模拟数据
- AI Listing 在无 OpenAI API Key 时生成模拟结果

### 接入真实API

后续可接入以下服务获取真实数据：
- Jungle Scout
- Helium 10
- Rocketmiles
- Keepa
- 亚马逊官方API

## 生产环境优化建议

1. **数据库**: 添加 MySQL 存储分析历史
2. **缓存**: 使用 Redis 缓存频繁查询的数据
3. **爬虫**: 接入代理池，避免IP被封
4. **AI**: 配置 OpenAI API Key 获取真实生成结果
5. **部署**: 使用 Nginx + Gunicorn
6. **监控**: 添加日志和监控告警

## License

MIT License

---

🤖 Built with Python + Flask + AI
