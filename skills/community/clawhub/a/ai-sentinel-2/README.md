# 🔭 AI前沿哨兵 (AI Sentinel)

> 你的AI情报指挥中心，自动采集、分析与报告AI领域最新动态

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/xiaopengs/ai-sentinel?style=social)](https://github.com/xiaopengs/ai-sentinel)

---

## 🚀 一分钟快速开始

```bash
# 1. 克隆项目
git clone https://github.com/xiaopengs/ai-sentinel.git
cd ai-sentinel

# 2. 安装依赖
pip install requests feedparser pyyaml jinja2

# 3. 创建输出目录
mkdir -p output

# 4. 运行采集（采集所有信息源）
python scripts/collect.py --all

# 5. 生成报告
python scripts/reporter.py --type morning
```

> 💡 **提示**：使用 WebUI 可以更直观地管理信息源和查看报告

```bash
cd webui && python -m http.server 8080
# 然后浏览器打开 http://localhost:8080
```

---

## 👤 适合谁用？

| 人群 | 使用场景 |
|------|----------|
| **AI 研究者** | 追踪最新论文和开源项目，不错过重要研究进展 |
| **开发者** | 发现热门AI项目和最佳实践，紧跟技术趋势 |
| **投资人** | 了解AI行业最新动态，发现潜在投资机会 |
| **产品经理** | 关注AI产品更新和行业新闻，启发产品灵感 |
| **技术爱好者** | 保持对AI领域的了解，学习新技术 |

---

## ✨ 功能特性

### 🔍 多源信息采集

| 信息源 | 说明 | 内置 |
|--------|------|------|
| **GitHub Trending** | 追踪AI开源项目热度，发现新兴项目 | ✅ |
| **arXiv 论文** | 获取最新学术研究成果 | ✅ |
| **HackerNews** | 捕捉开发者社区热点讨论 | ✅ |
| **Twitter/X** | 追踪AI大咖和机构动态 (需配置API) | ✅ |
| **RSS 订阅** | 支持任意博客/新闻源 | ✅ |
| **官方博客** | Anthropic、OpenAI、Google AI、DeepMind等 | ✅ (快速模板) |

### ⏰ 智能定时调度

- **晨报** - 每天早8点推送，隔夜重要动态
- **晚报** - 每天晚8点推送，全天热点汇总
- **即时采集** - 手动触发，按需获取

### 📊 智能分析评分

- **热度评分** - 基于star、fork、评论数
- **新鲜度权重** - 越新权重越高
- **来源可信度** - 不同来源不同权重
- **关键词匹配** - 自定义关注领域

### 📄 自动化报告

- 结构化 Markdown 格式
- 分类清晰：论文、项目、讨论、新闻
- 摘要+链接，可直接跳转阅读

### 🎛️ WebUI 管理面板

- 信息源配置与管理
- 实时采集状态监控
- 报告预览与导出
- 设置调整即时生效

---

## 📖 快速开始

### 环境要求

- Python 3.9+
- 网络连接

### 安装

```bash
# 克隆项目
git clone https://github.com/xiaopengs/ai-sentinel.git
cd ai-sentinel

# 安装依赖
pip install requests feedparser pyyaml jinja2

# 创建输出目录
mkdir -p output
```

### 基本使用

#### 命令行采集

```bash
# 采集所有信息源
python scripts/collect.py --all

# 仅采集 GitHub
python scripts/collect.py --source github

# 仅采集 arXiv 论文
python scripts/collect.py --source arxiv

# 查看采集状态
python scripts/collect.py --status
```

#### 生成报告

```bash
# 生成晨报
python scripts/reporter.py --type morning

# 生成晚报
python scripts/reporter.py --type evening
```

#### 启动 WebUI

```bash
cd webui && python -m http.server 8080
```

然后在浏览器打开 `http://localhost:8080`

#### 定时任务 (Linux/Mac)

```bash
# 编辑 crontab
crontab -e

# 添加以下内容
0 8 * * * cd /path/to/ai-sentinel && python scripts/collect.py --all && python scripts/reporter.py --type morning
0 20 * * * cd /path/to/ai-sentinel && python scripts/collect.py --all && python scripts/reporter.py --type evening
```

---

## 🔗 如何添加信息源

### 使用 WebUI 添加（推荐）

1. 打开 WebUI，点击左侧菜单的 **「信息源」**
2. 点击右上角的 **「添加信息源」** 按钮
3. 你可以使用两种方式添加：

#### 方式一：快速添加（一键添加常用博客）

在弹窗中的「快速添加」区域，我们提供了常用的AI博客模板：

| 博客 | 说明 |
|------|------|
| OpenAI 官方博客 | GPT模型更新、研究论文 |
| Anthropic 官方博客 | Claude、 Constitutional AI |
| Google AI Blog | Google在AI领域的研究 |
| DeepMind 研究 | 前沿AI研究成果 |
| Hugging Face Blog | 开源LLM和模型库动态 |
| Machine Learning Mastery | 实用的机器学习教程 |

点击「添加」按钮即可一键订阅！

#### 方式二：手动添加自定义源

如果想添加其他博客，需要获取该博客的 **RSS 订阅地址**：

1. 打开目标博客网站
2. 找页面底部的 **RSS** 或 **Feed** 图标
3. 点击后复制浏览器地址栏的URL
4. 回到 WebUI，填写：
   - **名称**：博客的名字（如「机器之心」）
   - **RSS订阅地址**：刚才复制的URL
   - **描述**：简短描述（可选）

### 命令行添加 RSS 源

编辑 `config/sources.yaml`：

```yaml
custom_rss:
  - name: "机器之心"
    url: "https://feed.jiqizhixin.com/rss"
    enabled: true
  - name: "量子位"
    url: "https://www.qbitai.com/feed"
    enabled: true
```

### 常见博客 RSS 地址

| 博客 | RSS 地址 |
|------|----------|
| 机器之心 | `https://feed.jiqizhixin.com/rss` |
| 量子位 | `https://www.qbitai.com/feed` |
| 知乎专栏-AI | `https://zhuanlan.zhihu.com/feed/` |
| Medium-AI | `https://medium.com/feed/tag/artificial-intelligence` |
| OpenAI Blog | `https://openai.com/blog/rss.xml` |
| Anthropic Blog | `https://www.anthropic.com/news/rss` |

---

## ⚙️ 信息源配置说明

### GitHub

```yaml
github:
  enabled: true
  language: python        # 编程语言
  date_range: weekly      # daily/weekly/monthly
  limit: 20
  keywords:              # 可选关键词过滤
    - AI
    - machine-learning
    - LLM
```

### arXiv

```yaml
arxiv:
  enabled: true
  categories:            # 论文分类
    - cs.AI              # Artificial Intelligence
    - cs.LG              # Machine Learning
    - cs.CL              # Computation and Language
  max_results: 20
```

### HackerNews

```yaml
hackernews:
  enabled: true
  item_type: top         # top/new/best/ask/show
  limit: 20
  keywords:              # AI相关关键词过滤
    - AI
    - machine learning
    - LLM
```

### Twitter/X

```yaml
twitter:
  enabled: true
  bearer_token: "your-twitter-bearer-token"  # 必需
  keywords:              # 关注关键词
    - AI
    - GPT
    - LLM
```

**获取 Bearer Token 步骤：**

1. 访问 [Twitter Developer Portal](https://developer.twitter.com)
2. 注册开发者账号（需要审核，通常1-2天）
3. 创建项目和应用
4. 在应用设置中生成 Bearer Token
5. 复制 Token 到 `config/settings.yaml` 或 WebUI 配置页

**推荐的 AI 大咖账号：**
- `@sama` - Sam Altman (OpenAI CEO)
- `@ylecun` - Yann LeCun (Meta AI 首席科学家)
- `@karpathy` - Andrej Karpathy (前OpenAI)
- `@AndrewYNg` - Andrew Ng (DeepLearning.AI)

### RSS 自定义源

```yaml
rss:
  enabled: true
  sources:
    - name: "OpenAI Blog"
      url: "https://openai.com/blog/rss.xml"
      update_interval: 3600    # 更新间隔（秒）
```

---

## 📁 项目结构

```
ai-sentinel/
├── config/                 # 配置文件目录
│   ├── sources.yaml        # 信息源配置
│   ├── settings.yaml       # 系统设置
│   └── schedule.yaml       # 定时任务配置
├── scripts/                # 脚本目录
│   ├── collect.py          # 主采集脚本
│   ├── reporter.py         # 报告生成脚本
│   └── parsers/            # 各信息源解析器
│       ├── github_trending.py
│       ├── arxiv.py
│       ├── hackernews.py
│       ├── twitter_x.py
│       └── blog_rss.py
├── templates/              # 报告模板
├── webui/                  # Web 管理界面
│   ├── index.html         # 主页面
│   ├── app.js             # 前端逻辑
│   └── style.css          # 样式文件
├── output/                 # 采集结果输出目录
├── SKILL.md                # 详细技术文档
├── LICENSE                 # MIT License
└── README.md               # 本文档
```

---

## ❓ 常见问题 (FAQ)

### Q: 如何添加 Twitter 信息源？

1. 访问 [Twitter Developer Portal](https://developer.twitter.com)
2. 创建开发者账号（需要审核，通常1-2天）
3. 创建 App 并生成 Bearer Token
4. 在 WebUI 的「配置」页面或 `config/settings.yaml` 填入 Token

> ⚠️ 需要Twitter开发者账号，审核通过后即可使用

### Q: 如何获取 Twitter Bearer Token？

1. 访问 [Twitter Developer Portal](https://developer.twitter.com)
2. 创建一个开发者账号（需要审核）
3. 创建 App 并申请 Bearer Token
4. 在 WebUI 的「配置」页面填入 Token

> ⚠️ 注意：Twitter API 有访问限制和配额，请合理使用

### Q: RSS 订阅不生效怎么办？

1. 确认 RSS 地址正确（可以在浏览器直接访问测试）
2. 有些网站使用 Atom 格式，尝试 `/atom.xml` 或 `/feed/atom`
3. 检查是否需要认证

### Q: 采集的数据在哪里？

- **原始数据**：`output/raw_data_YYYYMMDD_HHMMSS.json`
- **处理后数据**：`output/processed_data.json`
- **报告文件**：`output/reports/morning_YYYYMMDD.md` 或 `evening_`

### Q: 如何自定义报告模板？

编辑 `templates/report_template.md`，使用 Jinja2 语法。

### Q: 采集频率怎么调整？

修改定时任务或使用 crontab：

```bash
# 每6小时采集一次
0 */6 * * * cd /path/to/ai-sentinel && python scripts/collect.py --all
```

### Q: 支持哪些 RSS 格式？

支持标准的 RSS 2.0 和 Atom 格式。

---

## 📝 示例输出

采集结果示例 (`output/raw_data_*.json`)：

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "sources": {
    "github": {
      "status": "success",
      "count": 15,
      "items": [
        {
          "title": "user/repo-name",
          "description": "项目描述",
          "url": "https://github.com/user/repo-name",
          "stars": 12500,
          "forks": 1200,
          "language": "Python",
          "source": "github"
        }
      ]
    }
  }
}
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

本项目采用 [MIT License](LICENSE) 开源。

---

⭐ **如果这个项目对你有帮助，请给它一个星！**
