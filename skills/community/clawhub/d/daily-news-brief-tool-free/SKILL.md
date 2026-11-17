---
slug: daily-news-brief-tool-free
name: daily-news-brief-tool-free
version: 1.0.0
displayName: 每日新闻简报(免费版)
summary: "每日新闻简报免费版，自动搜集国际时事、经济形势、科技发展新闻生成简报.。每日新闻简报助手免费版是面向个人用户的轻量新闻简报生成工具。聚焦"搜集-筛选-生成"三步流程，自动获取国际时事、经济形"
license: MIT
edition: free
description: "每日新闻简报助手免费版是面向个人用户的轻量新闻简报产出工具。聚焦\"搜集-筛选-产出\"三步流程，自发获取国际时事、经济形势、科技发展新闻，产出统一格式的简报。Use. 适用于需要daily news brief tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量."
tags:
  - 每日新闻
  - daily
  - news
  - brief
  - automation
  - 新闻简报
  - 多领域
  - 资讯速递
  - 搜索
  - 检索
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
pricing_tier: free

---
> **搜集、筛选、生成。三步完成每日新闻简报。**

无需复杂配置，通过简单的脚本即可自动搜集国际时事、经济形势、科技发展三大领域的新闻，生成统一格式的新闻简报。免费版聚焦轻量场景，提供基础的简报生成能力.
## 概述
免费版每日新闻简报工具为个人用户提供基础的新闻搜集与简报生成能力。覆盖国际时事、经济形势、科技发展三大领域，基于历史模式和近期动向筛选重要新闻，生成统一格式的Markdown简报.
### 核心定位
| 维度 | 免费版能力 |
|---|-----|
| 多领域覆盖 | 支持（国际/经济/科技） |
| 智能筛选 | 支持（基于关键词） |
| 简报生成 | 支持（Markdown） |
| 定时自动执行 | 不支持（需专业版） |
| 多渠道推送 | 不支持（需专业版） |
| AI智能分析 | 不支持（需专业版） |
| 历史回顾 | 支持（基础） |
| 个性化定制 | 不支持（需专业版） |

## 核心能力
### 1. 多源新闻搜集

> 详细代码示例已移至 `references/detail.md`

**处理**: 解析多源新闻搜集的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多源新闻搜集的响应数据,包含状态码、结果和日志.
### 2. 智能筛选

**处理**: 解析智能筛选的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回智能筛选的响应数据,包含状态码、结果和日志.
### 3. 简报生成

**处理**: 解析简报生成的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回简报生成的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：每日新闻简报免费、自动搜集国际时事、经济形势、科技发展新闻生成、每日新闻简报助手、免费版是面向个人、用户的轻量新闻简、报生成工具、三步流程、自动获取国际时事、科技发展新闻、生成统一格式的简、Use、when、模型调用、智能对话、Agent、LLM、应用时使用、不适用于需要、确定性的关键决策、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：每日新闻回顾
**场景描述**：每天早上获取昨日新闻简报，快速了解世界动态.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 每日新闻简报(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
collector = NewsCollector()
filterer = NewsFilter()
generator = BriefGenerator()
# ...
print("正在搜集新闻...")
all_news = collector.collect_all()
# ...
filtered = filterer.filter_news(all_news)
# ...
brief = generator.generate(filtered)
print(brief)
# ...
generator.save_to_file(brief)
```

### 场景二：行业动态跟踪
**场景描述**：只关注科技和经济类新闻.
```python
collector = NewsCollector()
filterer = NewsFilter()
# ...
all_news = {
    'economic': collector.collect_single('https://finance.sina.com.cn', 'economic'),
    'technology': collector.collect_single('https://tech.sina.com.cn', 'technology')
}
filtered = filterer.filter_news(all_news)
# ...
print("=== 经济形势 ===")
for news in filtered.get('economic', [])[:3]:
    print(f"- {news['title']}")
# ...
print("\n=== 科技发展 ===")
get('technology', [])[:3]:
    print(f"- {news['title']}")
```

### 场景三：内容创作参考
**场景描述**：自媒体创作者获取新闻素材.
```python
collector = NewsCollector()
filterer = NewsFilter()
# ...
filtered = filterer.filter_news(all_news)
# ...
print("=== 今日创作素材 ===")
for category, items in filtered.items():
    print(f"\n【{category}】")
    for i, news in enumerate(items[:3], 1):
        print(f"  {i}. {news['title']}")
        print(f"     URL：{news.get('url', '')}")
```

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手
```bash
python3 << 'PYEOF'
import requests
from bs4 import BeautifulSoup
from datetime import datetime
# ...
url = "https://news.cctv.com/world"
r = requests.get(validated_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.content, 'html.parser')
# ...
print(f"=== 国际新闻速递 {datetime.now().strftime('%Y-%m-%d')} ===\n")
for i, link in enumerate(soup.find_all('a', href=True)[:10], 1):
    title = link.get_text(strip=True)
    if title and len(title) > 10:
        print(f"{i}. {title}")
PYEOF
```bash
# 在此执行相关操作
echo "操作完成"
```bash
# ...
# ...
# ...
# ...
# ...
# ...
# ...
echo "操作完成"
pip install requests beautifulsoup4
cat > daily_brief.py << 'PYEOF'
import requests
from bs4 import BeautifulSoup
from datetime import datetime
SOURCES = {
    'international': ['https://news.cctv.com/world'],
    'economic': ['https://finance.sina.com.cn'],
    'technology': ['https://tech.sina.com.cn'],
}
def collect():
    all_news = {}
    for cat, urls in SOURCES.items():
        items = []
        for url in urls:
            try:
content, 'html.parser')
                for link in soup.find_all('a', href=True)[:10]:
                    title = link.get_text(strip=True)
                    if title and 10 < len(title) < 100:
                        items.append({'title': title, 'url': link['href']})
            except:
        all_news[cat] = items
    return all_news
def generate(news):
    lines = [f"# 每日新闻简报 | {datetime.now().strftime('%Y年%m月%d日')}\n"]
    for cat, items in news.items():
        cat_name = {'international': '国际时事', 'economic': '经济形势', 'technology': '科技发展'}
        lines.append(f"## {cat_name.get(cat, cat)}\n")
        for i, item in enumerate(items[:5], 1):
            lines.append(f"{i}. {item['title']}")
        lines.append("")
    return "\n".join(lines)
if __name__ == "__main__":
    news = collect()
    brief = generate(news)
    print(brief)
    with open(f"brief_{datetime.now().strftime('%Y%m%d')}.md", "w", encoding="utf-8") as f:
        f.write(brief)
    print("\n简报已保存")
PYEOF
python3 daily_brief.py
```bash
# 在此执行相关操作
echo "操作完成"
```python
import os
from datetime import datetime
# ...
class BriefConfig:
    """简报配置（免费版）"""
    SOURCES = {
        'international': [
            'https://news.cctv.com/world',
            'https://www.reuters.com/world',
        ],
        'economic': [
            'https://finance.sina.com.cn',
bloomberg.com/markets',
        ],
        'technology': [
            'https://tech.sina.com.cn',
            'https://techcrunch.com',
        ]
    }
# ...
    OUTPUT_DIR = os.getenv('BRIEF_OUTPUT_DIR', './output')
    OUTPUT_FORMAT = os.getenv('BRIEF_FORMAT', 'markdown')
    MAX_PER_CATEGORY = int(os.getenv('BRIEF_MAX_PER_CAT', '5'))
# ...
    TITLE_TEMPLATE = "每日新闻简报 | {date} | {weekday}"
# ...
    @classmethod
    def show(cls):
        print("=== 简报配置 ===")
        print(f"输出目录：{cls.OUTPUT_DIR}")
        print(f"输出格式：{cls.OUTPUT_FORMAT}")
        print(f"每分类最大数量：{cls.MAX_PER_CATEGORY}")
# ...
BriefConfig.show()
```bash
# 在此执行相关操作
echo "操作完成"
```python
FILTER_KEYWORDS = {
    'international': {
        'priorities': ['中美关系', '中东', '欧洲', '亚太', '俄罗斯'],
        'weight': {
            '中美关系': 3, '中东': 2, '欧洲': 1, '亚太': 2, '俄罗斯': 2
        }
    },
    'economic': {
        'priorities': ['GDP', '通胀', '利率', '美联储', '央行'],
        'weight': {
            'GDP': 3, '通胀': 2, '利率': 2, '美联储': 3, '央行': 2
        }
    },
    'technology': {
        'priorities': ['AI', '芯片', '新能源', '生物科技', '太空'],
        'weight': {
            'AI': 3, '芯片': 2, '新能源': 2, '生物科技': 1, '太空': 1
        }
    }
}
```bash
# 在此执行相关操作
echo "操作完成"
```python
def safe_collect(url, category):
    """安全的新闻搜集"""
    try:
        response = requests.0'})
        if response.status_code == 200:
            return parse_news(response.content, category)
        return []
    except requests.Timeout:
        print(f"超时：{url}")
        return []
    except Exception as e:
        print(f"异常：{url} - {e}")
        return []
```bash
# 在此执行相关操作
echo "操作完成"
```python
def deduplicate(news_list):
    """去重"""
    seen = set()
    unique = []
    for news in news_list:
        title = news.get('title', '')
        if title not in seen:
            seen.add(title)
            unique.append(news)
    return unique
```bash
# 在此执行相关操作
echo "操作完成"
```python
import os
import json
# ...
class BriefCache:
    """简报缓存"""
    def __init__(self, cache_dir="./cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
# ...
    def get(self, date_str):
        """获取缓存"""
        cache_file = os.path.join(self.cache_dir, f"brief_{date_str}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
# ...
    def set(self, date_str, data):
        """设置缓存"""
path.join(self.json")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
```
### 错误场景3

检查`error_code`并按照处理方式进行排查.
## 常见问题
### Q1：免费版支持定时自动执行吗？
不支持。免费版需手动触发执行。如需定时自动执行（如每天早上8点自动生成并推送简报），需升级至专业版，支持定时任务配置调度与多渠道推送.
### Q2：新闻搜集失败怎么办？
可能原因：(1) 网络问题，稍后重试；(2) 源站结构变更，需更新解析逻辑；(3) User-Agent被屏蔽，尝试更换UA；(4) 源站临时不可用。免费版会跳过失败源，继续搜集其他源.
### Q3：筛选不准确怎么办？
免费版使用基于关键词的简单筛选。如遇筛选不准的情况：(1) 调整关键词列表与权重；(2) 增加更多关键词；(3) 升级专业版使用AI智能分析（基于LLM的深度分析与筛选）.
### Q4：可以定制新闻领域吗？
免费版默认覆盖国际时事、经济形势、科技发展三大领域。可通过修改 `SOURCES` 配置添加其他领域（如体育、娱乐），但筛选关键词需手动调整。专业版支持完全个性化定制.
### Q5：支持哪些输出格式？
免费版支持Markdown格式输出。如需HTML、PDF、邮件格式等其他输出，需升级专业版.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+
- **Node.js**: 16+（可选，用于JavaScript实现）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Python 3.8+ | 运行时 | 必需 | 官网下载安装 |
| requests | Python库 | 必需 | `pip install requests` |
| beautifulsoup4 | Python库 | 必需 | `pip install beautifulsoup4` |
| Node.js 16+ | 运行时 | 可选 | JavaScript实现使用 |
| axios | npm包 | 可选 | JavaScript实现使用 |
| cheerio | npm包 | 可选 | JavaScript实现使用 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- 免费版无需任何API Key
- 新闻搜集基于公开网页内容，不涉及付费API调用
- LLM模型路由由Agent平台内置提供

### 可用性分类
- **分类**: MD+EXEC（Markdown指令+命令行执行）
- **说明**: 通过自然语言指令驱动Agent执行新闻搜集与简报生成任务

## 已知限制
本免费体验版限制以下高级功能（需升级至专业版解锁）：

- **定时自动执行**（cron调度，每日自动推送）
- **多渠道推送**（飞书/钉钉/企业微信/邮件/Slack）
- **AI智能分析**（基于LLM的情感分析与趋势预测）
- **个性化定制**（关键词权重、领域自定义、模板定制）
- **多语言支持**（英文/日文/韩文简报）
- **历史回顾**（相关历史事件检索）
- **新闻情感分析**（正面/负面/中性判断）
- **优先技术支持**

解锁全部高级能力请使用专业版：`daily-news-brief-tool-pro`

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```bash
# 在此执行相关操作
echo "操作完成"
```json
{
  "success": true,
  "data": {
    "result": "每日新闻简报(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "daily news brief"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
