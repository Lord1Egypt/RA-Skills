# OpenClaw Browser Relay 配置指南

## 概述

OpenClaw Browser Relay 是一个浏览器中转服务，用于解决以下问题：
1. **字体加密**：浏览器端可以正确渲染加密字体
2. **地区选择**：支持一次性选择多个地区
3. **实时验证**：可以直观看到采集过程

## 部署 Browser Relay 服务

### 方式1：使用 Docker（推荐）

```bash
# 拉取镜像
docker pull openclaw/browser-relay:latest

# 启动服务
docker run -d \
  --name browser-relay \
  -p 8080:8080 \
  -v /tmp/browser-data:/data \
  openclaw/browser-relay:latest
```

### 方式2：使用 Docker Compose

```yaml
version: '3.8'
services:
  browser-relay:
    image: openclaw/browser-relay:latest
    container_name: browser-relay
    ports:
      - "8080:8080"
    volumes:
      - /tmp/browser-data:/data
    environment:
      - HEADLESS=true
      - MAX_SESSIONS=5
```

### 方式3：本地运行（开发环境）

```bash
# 安装依赖
npm install -g @openclaw/browser-relay

# 启动服务
browser-relay --port 8080
```

## 服务接口

### 1. 执行命令

```bash
POST /execute
Content-Type: application/json

{
  "action": "goto|click|evaluate|screenshot",
  "url": "页面URL",  // goto 需要
  "selector": "CSS选择器",  // click 需要
  "script": "JavaScript代码",  // evaluate 需要
  "waitUntil": "load|networkidle"
}
```

### 2. 查看会话状态

```bash
GET /sessions
```

### 3. 关闭会话

```bash
DELETE /sessions/:sessionId
```

## 使用示例

### 基础使用

```python
from scripts.sufu_crawler_openclaw import SufuCrawlerOpenClaw

# 创建采集器
crawler = SufuCrawlerOpenClaw(relay_url="http://localhost:8080")

# 采集数据（一次性选择多个地区）
results = crawler.collect_sufu(regions=["盐南高新区", "经开区"])

# 处理结果
if results:
    for project in results:
        print(f"{project['project_name']} - {project['region']}")
```

### 集成到主采集器

```python
from scripts.crawler import SufuCrawler

class SufuCrawler(BaseCrawler):
    def crawl(self, region=None, days=None):
        # 使用 Browser Relay 方式采集
        from scripts.sufu_crawler_openclaw import SufuCrawlerOpenClaw

        crawler = SufuCrawlerOpenClaw()
        results = crawler.collect_sufu(regions=["盐南高新区", "经开区"])

        # 保存到数据库
        for project in results:
            self.db.save_project(project)

        return results
```

## 优势

1. **解决字体加密**：浏览器端渲染，无需处理加密字体
2. **支持多地区选择**：一次性选择多个地区，提高效率
3. **实时可见**：可以查看采集过程，便于调试
4. **易于扩展**：支持自定义JavaScript脚本
5. **无头模式**：支持无头浏览器，适合服务器环境

## 注意事项

1. **服务依赖**：需要先启动 Browser Relay 服务
2. **端口占用**：确保8080端口未被占用
3. **资源消耗**：浏览器实例会占用较多内存
4. **超时设置**：合理设置超时时间，避免长时间等待
5. **错误处理**：注意处理网络异常和服务不可用的情况

## 故障排查

### 问题1：无法连接到 Browser Relay 服务

**解决方案**：
- 检查服务是否启动：`docker ps | grep browser-relay`
- 检查端口是否开放：`netstat -an | grep 8080`
- 检查防火墙设置

### 问题2：字体仍然显示乱码

**解决方案**：
- 确保浏览器版本支持字体渲染
- 检查字体文件是否加载成功
- 尝试使用有头模式查看实际效果

### 问题3：地区选择不生效

**解决方案**：
- 查看浏览器截图确认选择是否成功
- 检查选择器是否正确
- 尝试增加等待时间

## 性能优化

1. **会话复用**：复用浏览器会话，减少启动开销
2. **并发限制**：限制并发会话数量，避免资源耗尽
3. **缓存策略**：对不频繁变化的数据使用缓存
4. **超时控制**：合理设置超时，避免长时间等待
