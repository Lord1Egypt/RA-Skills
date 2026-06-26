# 🇨🇳 cn-ai-search - 中文AI Agent聚合搜索Skill

专为中文AI Agent/OpenClaw优化的多平台聚合搜索工具，一次查询覆盖全网主流中文平台，自动去重过滤广告，支持Tavily AI自动总结。

## ✨ 特性

- 📦 **开箱即用**：基础功能无需API密钥，安装就能用
- 🌏 **中文全覆盖**：百度、微信公众号、知乎、B站、微博、头条、360、搜狗全覆盖
- 🧹 **自动净化**：过滤广告、SEO垃圾、重复内容，结果干净直接喂大模型
- 🤖 **AI自动总结**：基于Tavily AI，自动汇总多平台搜索结果为结构化答案
- 🔧 **灵活配置**：支持指定平台、结果数量、排序方式

## 📖 支持平台

| 平台 | 状态 | 配置要求 |
|------|------|----------|
| 百度 | ✅ 可用 | 无需配置 |
| 必应中国 | ✅ 可用 | 无需配置 |
| 360搜索 | ✅ 可用 | 无需配置 |
| 搜狗 | ✅ 可用 | 无需配置 |
| 微信公众号 | ✅ 可用 | 无需配置 |
| 头条 | ✅ 可用 | 无需配置 |
| 知乎 | ✅ 可用 | 无需配置 |
| B站 | ✅ 可用 | 无需配置 |
| 微博 | ✅ 可用 | 无需配置 |
| 小红书 | ✅ 可用 | 需要配置mcporter + Docker |
| 抖音 | ✅ 可用 | 需要配置mcporter |

## 🚀 安装

```bash
# 克隆仓库
git clone https://github.com/[你的用户名]/cn-ai-search-skill.git
cd cn-ai-search-skill

# 安装依赖
pip install -r requirements.txt

# 创建命令链接
ln -s $(pwd)/index.py /usr/local/bin/cn-ai-search
chmod +x /usr/local/bin/cn-ai-search
```

## 💡 使用示例

```bash
# 基础搜索（默认百度+微信公众号+知乎+B站）
cn-ai-search "你的搜索关键词"

# 指定多个平台
cn-ai-search "OpenClaw skill 变现" --platforms baidu,weixin,zhihu,bilibili

# 开启AI自动总结（需要配置TAVILY_API_KEY）
cn-ai-search "OpenClaw skill 变现" --summarize

# 控制结果数量
cn-ai-search "AI 创业 2026" --count 20 --count-per-platform 5

# 按热度排序
cn-ai-search "热点事件" --sort hot
```

## ⚙️ 配置

在`config.py`中填入你的API密钥（Tavily和Jina可选配置）：

```python
# Tavily AI搜索（开启AI总结需要）
TAVILY_API_KEY = "你的tavily api key"

# Jina Reader API（网页抓取，可选配置，解决限流）
JINA_API_KEY = "你的jina api key"
```

## 💎 版本说明

| 版本 | 价格 | 功能 |
|------|------|------|
| 社区版 | 免费 | 支持百度/微信/知乎/B站/微博等基础平台，最多20条结果 |
| 专业版 | **$9.99 一次性授权** | 全平台支持（含小红书/抖音），无限结果，AI总结功能，终身更新，技术支持 |

**获取专业版：** 扫描下方二维码购买，购买后获取完整安装包和授权。

## 🎯 适用场景

- AI Agent需要获取实时中文信息
- 商业情报搜集、商机挖掘
- 多平台内容聚合调研
- 市场分析、竞品分析
- 新闻热点追踪

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 💖 赞助

如果这个项目对你有帮助，欢迎star支持，也可以购买专业版支持我们继续开发！

