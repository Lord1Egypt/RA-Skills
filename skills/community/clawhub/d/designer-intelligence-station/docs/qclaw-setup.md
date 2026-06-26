# 设计师情报站 - qclaw 适配指南

## 📋 问题诊断

### 在 qclaw 中效果不佳的原因

1. **依赖 OpenClaw 工具**
   - `web_fetch` 是 OpenClaw 专用工具
   - qclaw 环境可能不可用或权限受限

2. **外部 CLI 工具依赖**
   - mcporter（小红书 MCP）
   - xreach（Twitter）
   - 这些工具在 qclaw 中可能无法调用

3. **浏览器不可用**
   - 某些平台需要浏览器登录
   - qclaw 可能是无头环境

---

## ✅ 解决方案

### 方案一：使用独立抓取器（推荐）

**v1.5.1 新增** - 不依赖 OpenClaw 的独立抓取模式：

```bash
# 安装依赖
pip install -r requirements.txt

# 抓取所有网页源
python tools/web_fetcher_standalone.py fetch-all

# 抓取单个源
python tools/web_fetcher_standalone.py fetch CN001
```

**优点**：
- ✅ 不依赖 OpenClaw 工具
- ✅ 可在任何 Python 环境运行
- ✅ 支持 qclaw、本地、服务器

**缺点**：
- ⚠️ 无法抓取需要登录的平台（小红书、Twitter）
- ⚠️ 反爬较强的网站可能失败

---

### 方案二：修改执行脚本

**修改 `execute_daily.sh`**，使用独立抓取器：

```bash
#!/bin/bash

# 步骤 1: 抓取 RSS
python3 tools/rss_fetcher.py

# 步骤 2: 抓取 API
python3 tools/api_fetcher.py

# 步骤 3: 抓取网页（独立模式）
python3 tools/web_fetcher_standalone.py fetch-all

# 步骤 4: 合并结果
python3 tools/fetch_all.py --merge \
  data/cache/rss_items.json \
  data/cache/api_items.json \
  data/cache/web_items_standalone_*.json \
  --output data/cache/all_items.json

# 步骤 5: 生成报告
# ...（Agent 筛选和格式化）
```

---

### 方案三：使用 web_fetch 工具（如果 qclaw 支持）

如果 qclaw 支持 `web_fetch` 工具，需要在代码中明确调用：

**在 Agent 执行时**：

```python
# 不要这样做（会失败）：
from web_fetcher import call_web_fetch
result = call_web_fetch(url)

# 应该这样做（让 Agent 调用）：
print(f"请调用：web_fetch(url='{url}', extractMode='markdown')")
```

---

## 🔧 qclaw 配置建议

### 1. 安装完整依赖

```bash
cd ~/.qclaw/skills/designer-intelligence-station
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python data/import_sources.py
```

### 3. 测试抓取

```bash
# 测试 RSS 抓取
python tools/rss_fetcher.py

# 测试独立网页抓取
python tools/web_fetcher_standalone.py fetch CN004

# 测试 API 抓取
python tools/api_fetcher.py
```

### 4. 生成日报

```bash
./execute_daily.sh
```

---

## 📊 抓取能力对比

| 抓取方式 | OpenClaw | qclaw（独立） | qclaw（工具） |
|---------|----------|-------------|-------------|
| RSS 源 | ✅ | ✅ | ✅ |
| API 源 | ✅ | ✅ | ✅ |
| 网页（公开） | ✅ | ✅ | ✅ |
| 网页（需登录） | ⚠️ 需配置 | ❌ | ⚠️ 需配置 |
| 社交平台 | ⚠️ 需配置 | ❌ | ⚠️ 需配置 |

---

## 🚀 最佳实践

### 在 qclaw 中使用

**推荐配置**：
1. 使用 `web_fetcher_standalone.py` 抓取公开网页
2. 跳过需要登录的社交平台
3. 重点关注 RSS + API + 公开网页

**执行命令**：
```bash
# 完整流程
python tools/rss_fetcher.py && \
python tools/api_fetcher.py && \
python tools/web_fetcher_standalone.py fetch-all && \
python tools/fetch_all.py --merge ... --output ...
```

### 在 OpenClaw 中使用

**推荐配置**：
1. 使用 Agent 的 `web_fetch` 工具
2. 配置社交平台（Twitter、小红书）
3. 全平台抓取

---

## 🐛 故障排查

### 问题 1：ModuleNotFoundError

```bash
# 安装依赖
pip install requests beautifulsoup4 lxml python-dateutil feedparser
```

### 问题 2：抓取失败（403）

```python
# 添加 User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 ..."
}
```

### 问题 3：解析失败

检查网站结构是否变化，更新解析策略：

```python
def parse_cn004(self, soup, base_url):
    # 爱范儿特定解析逻辑
    items = []
    for article in soup.select('.article-item'):
        title = article.select_one('h2').text
        link = article.select_one('a')['href']
        items.append({...})
    return items
```

---

## 📝 更新日志

### v1.5.1（qclaw 适配版）

- ✅ 新增 `web_fetcher_standalone.py`（独立抓取器）
- ✅ 更新 `requirements.txt`
- ✅ 添加 qclaw 适配指南
- ✅ 优化 User-Agent 轮换
- ✅ 添加请求延迟和随机化

---

*最后更新：2026-03-24 | 设计师情报站 v1.5.1*
