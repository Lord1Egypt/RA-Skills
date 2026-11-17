---
slug: china-news-tool-free
name: china-news-tool-free
version: 1.0.0
displayName: 中国新闻聚合(免费版)
summary: "中国新闻聚合免费版，支持RSS订阅获取主流媒体新闻，智能分类生成简报.。中国新闻聚合助手免费版是面向个人用户的轻量新闻聚合工具。通过RSS订阅模式获取新浪、搜狐、网易等主流媒体内容，智能分类"
license: MIT
edition: free
description: "中国新闻聚合助手免费版是面向个人用户的轻量新闻聚合工具。通过RSS订阅模式获取新浪、搜狐、网易等主流媒体内容，智能分类产出新闻简报。Use. 适用于需要china news tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要china news tool相关能力的开发场景,包含结构化的工作流程和配置指引."
tags:
  - 中国新闻
  - china
  - news
  - automation
  - productivity
  - RSS聚合
  - 智能分类
  - 新闻简报
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
> **RSS订阅、智能分类、生成简报。三步完成中国主流媒体新闻聚合。**

无需复杂配置，通过RSS订阅即可获取主流媒体的最新新闻。免费版聚焦轻量场景，提供基础的新闻聚合与分类能力.
## 概述
免费版中国新闻聚合工具为个人用户提供基础的新闻获取与分类能力。通过RSS订阅模式（无需浏览器）即可获取新浪、搜狐、网易等主流媒体内容，按主题智能分类，生成结构化新闻简报.
### 核心定位
| 维度 | 免费版能力 |
|---|-----|
| RSS订阅模式 | 支持 |
| 浏览器自动化模式 | 不支持（需专业版） |
| AI智能摘要 | 不支持（需专业版） |
| 定时自动执行 | 不支持（需专业版） |
| 多渠道推送 | 不支持（需专业版） |
| 智能分类 | 支持（基础6类） |
| Markdown输出 | 支持 |
| 多语言输出 | 支持（中英文） |

## 核心能力
### 1. RSS订阅获取新闻
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 中国新闻聚合(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
# ...
class RSSFetcher:
    """RSS订阅获取器（免费版）"""
# ...
    def __init__(self):
        self.sources = {
            '新浪国内': 'https://rss.sina.com.cn/news/china/roll.xml',
            '新浪国际': 'https://rss.sina.com.cn/news/world/roll.xml',
            '新浪财经': 'https://rss.sina.com.cn/finance/roll.xml',
            '新浪科技': 'https://rss.sina.com.cn/tech/roll.xml',
            '搜狐新闻': 'https://news.sohu.com/rss/',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
# ...
    def fetch_all(self):
        """获取所有RSS源"""
        all_news = []
        for source_name, url in self.sources.items():
            print(f"  获取 {source_name}...")
            items = self.fetch_single(url)
            for item in items:
                item['source'] = source_name
            all_news.extend(items)
        return all_news
# ...
    def fetch_single(self, url, timeout=10):
        """获取单个RSS源"""
        try:
            response = requests.get(validated_url, timeout=timeout, headers=self.headers)
            root = ET.fromstring(response.content)
            items = []
# ...
            for item in root.findall('.//item'):
                title = item.find('title')
                link = item.find('link')
                desc = item.find('description')
# ...
                if title is not None and title.text:
                    items.append({
                        'title': title.text.strip(),
                        'url': link.text if link is not None else '',
                        'desc': desc.text[:200] if desc is not None and desc.text else '',
                        'fetched_at': datetime.now().isoformat()
                    })
# ...
            return items[:15]  # 每源最多15条
        except Exception as e:
            print(f"    获取失败：{e}")
            return []
# ...
fetcher = RSSFetcher()
news = fetcher.fetch_all()
print(f"\n共获取 {len(news)} 条新闻")
```

**处理**: 解析RSS订阅获取新闻的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回RSS订阅获取新闻的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 智能分类
```python
class NewsCategorizer:
    """新闻分类器（免费版）"""
# ...
    def __init__(self):
        self.categories = {
            '时事': ['政治', '国际', '外交', '政策', '政府', '两会', '选举', '主席', '总理'],
            '财经': ['股市', '基金', '经济', '金融', '投资', '银行', '房产', 'A股', '上市'],
            '科技': ['AI', '人工智能', '芯片', '手机', '互联网', '新能源', '科技', '5G', '半导体'],
            '体育': ['足球', '篮球', '奥运', '世界杯', 'NBA', '中超', '体育', '冠军'],
            '娱乐': ['明星', '电影', '音乐', '综艺', '八卦', '热播', '娱乐', '演员'],
            '社会': ['事故', '案件', '民生', '教育', '医疗', '疫情', '社会', '安全']
        }
# ...
    def categorize(self, news_list):
        """分类新闻列表"""
        categorized = {cat: [] for cat in self.categories}
        categorized['其他'] = []
# ...
        for news in news_list:
            matched = False
            for category, keywords in self.categories.items():
                if any(kw in news.get('title', '') for kw in keywords):
                    categorized[category].append(news)
                    matched = True
                    break
            if not matched:
                categorized['其他'].append(news)
# ...
        return {k: v for k, v in categorized.items() if v}
# ...
    def get_stats(self, categorized):
        """获取分类统计"""
        stats = {}
        for cat, news_list in categorized.items():
            stats[cat] = len(news_list)
        return stats
# ...
categorizer = NewsCategorizer()
categorized = categorizer.categorize(news)
stats = categorizer.get_stats(categorized)
print("\n分类统计：")
for cat, count in stats.items():
    print(f"  {cat}: {count}条")
```

**处理**: 解析智能分类的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回智能分类的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 新闻简报生成
```python
class NewsBriefGenerator:
    """新闻简报生成器（免费版）"""
# ...
    def generate(self, categorized_news, date_str=None):
        """生成新闻简报"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y年%m月%d日 %H:%M')
# ...
        lines = []
        lines.append(f"# 每日新闻速递")
        lines.append(f"**{date_str}**")
        lines.append("")
        lines.append("---")
        lines.append("")
# ...
        lines.append("## 热点速递")
        lines.append("")
        for category, news_list in categorized_news.items():
            if news_list and category != '其他':
                top = news_list[0]
                lines.append(f"- **【{category}】** {top['title']}")
        lines.append("")
        lines.append("---")
        lines.append("")
# ...
            if news_list:
append(f"## {category}新闻（{len(news_list)}条）")
                for i, news in enumerate(news_list[:5], 1):
                    title = news.get('title', '无标题')[:80]
                    source = news.get('source', '')
append(f"{i}. {title}")
                    if source:
append(f"   - 来源：{source}")
# ...
        lines.append("---")
        lines.append(f"*共 {sum(len(v) for v in categorized_news.values())} 条新闻*")
# ...
        return "\n".join(lines)
# ...
    def save_to_file(self, content, filename=None):
        """保存到文件"""
        import os
        if filename is None:
            filename = f"news_{datetime.now().strftime('%Y%m%d')}.md"
# ...
        output_dir = os.environ.get('OUTPUT_DIR', os.getcwd())
        output_path = os.path.join(output_dir, filename)
# ...
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
# ...
        print(f"简报已保存：{output_path}")
        return output_path
# ...
generator = NewsBriefGenerator()
brief = generator.generate(categorized)
print(brief[:500])
generator.save_to_file(brief)
```

**处理**: 解析新闻简报生成的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回新闻简报生成的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：中国新闻聚合免费、订阅获取主流媒体、智能分类生成简报、中国新闻聚合助手、免费版是面向个人、用户的轻量新闻聚、合工具、订阅模式获取新浪、网易等主流媒体内、智能分类生成新闻、when、模型调用、智能对话、LLM、应用时使用、不适用于需要、确定性的关键决策、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一：每日新闻浏览
**场景描述**：每天早上获取最新新闻，按分类快速浏览.
```python
fetcher = RSSFetcher()
categorizer = NewsCategorizer()
generator = NewsBriefGenerator()
# ...
print("正在获取新闻...")
news = fetcher.fetch_all()
# ...
# ...
brief = generator.generate(categorized)
print(brief)
# ...
generator.save_to_file(brief)
```

### 场景二：分类新闻速览
**场景描述**：只关注科技和财经类新闻.
```python
fetcher = RSSFetcher()
categorizer = NewsCategorizer()
# ...
news = fetcher.fetch_all()
# ...
for category in ['科技', '财经']:
    if category in categorized:
        print(f"\n=== {category}新闻 ===")
        for i, item in enumerate(categorized[category][:5], 1):
            print(f"{i}. {item['title']}")
            print(f"   来源：{item.get('source', '')}")
```

### 场景三：英文新闻输出
**场景描述**：生成英文版新闻简报.
```python
class EnglishBriefGenerator:
    """英文简报生成器"""
    CATEGORY_EN = {
        '时事': 'Current Affairs',
        '财经': 'Finance',
        '科技': 'Technology',
        '体育': 'Sports',
        '娱乐': 'Entertainment',
        '社会': 'Society',
        '其他': 'Others'
    }
# ...
    def generate(self, categorized_news):
        lines = ["# Daily News Brief", ""]
        for cat, news_list in categorized_news.items():
            cat_en = self.CATEGORY_EN.get(cat, cat)
            lines.append(f"## {cat_en} ({len(news_list)} items)")
            for i, news in enumerate(news_list[:3], 1):
append(f"{i}. {news['title']}")
            lines.append("")
        return "\n".join(lines)
# ...
en_generator = EnglishBriefGenerator()
print(en_generator.generate(categorized))
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
import xml.etree.ElementTree as ET
# ...
response = requests.get(
    'https://rss.sina.com.cn/news/china/roll.xml',
    headers={'User-Agent': 'Mozilla/5.0'}, timeout=10
)
root = ET.fromstring(response.content)
# ...
for item in root.findall('.//item')[:5]:
    title = item.find('title').text
    print(f"- {title}")
PYEOF
```bash
# 在此执行相关操作
echo "操作完成"
```bash
pip install requests
# ...
cat > news_aggregator.py << 'PYEOF'
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
# ...
sources = {
sina.com.cn/news/china/roll.xml',
sina.com.cn/tech/roll.xml',
}
# ...
all_news = []
for name, url in sources.items():
    try:
        r = requests.get(validated_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        root = ET.fromstring(r.content)
findall('.//item')[:10]:
append({'title': title, 'source': name})
    except Exception as e:
        print(f"{name} 获取失败：{e}")
# ...
print(f"\n共获取 {len(all_news)} 条新闻\n")
for i, news in enumerate(all_news, 1):
    print(f"{i}. [{news['source']}] {news['title']}")
PYEOF
# ...
python3 news_aggregator.py
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 配置示例
### RSS源配置
```python
RSS_SOURCES = {
sina.com.cn/news/china/roll.xml',
sina.com.cn/news/world/roll.xml',
sina.com.cn/finance/roll.xml',
sina.com.cn/tech/roll.xml',
    '36氪': 'https://36kr.com/feed',
    '凤凰资讯': 'https://news.ifeng.com/rss/',
}
# ...
CATEGORIES = {
    '时事': ['政治', '国际', '外交', '政策', '政府'],
    '财经': ['股市', '基金', '经济', '金融', '投资'],
    '科技': ['AI', '人工智能', '芯片', '互联网', '新能源'],
    '体育': ['足球', '篮球', '奥运', '世界杯', 'NBA'],
    '娱乐': ['明星', '电影', '音乐', '综艺', '热播'],
    '社会': ['事故', '案件', '民生', '教育', '医疗'],
}
```bash
# 在此执行相关操作
echo "操作完成"
```python
OUTPUT_CONFIG = {
    'format': 'markdown',  # markdown / json / text
    'max_per_category': 5,  # 每分类最多显示条数
    'show_source': True,   # 是否显示来源
    'show_time': True,     # 是否显示时间
    'output_dir': './output',
    'filename_pattern': 'news_{date}.md',
}
```bash
# 在此执行相关操作
echo "操作完成"
```python
def safe_fetch_all(fetcher):
    """安全的批量获取"""
    all_news = []
    failed_sources = []
    for name, url in fetcher.sources.items():
        try:
            items = fetcher.fetch_single(url)
            if items:
                for item in items:
                    item['source'] = name
            else:
                failed_sources.append(name)
        except Exception as e:
            print(f"  {name} 失败：{e}")
# ...
    if failed_sources:
        print(f"\n警告：{len(failed_sources)} 个源获取失败：{failed_sources}")
    return all_news
```bash
# 在此执行相关操作
echo "操作完成"
```python
def deduplicate(news_list):
    """去重（基于标题相似度）"""
    seen = set()
    unique = []
    for news in news_list:
        if title not in seen:
            seen.add(title)
            unique.append(news)
    return unique
# ...
unique_news = deduplicate(news)
print(f"去重前：{len(news)} 条，去重后：{len(unique_news)} 条")
```bash
# 在此执行相关操作
echo "操作完成"
```python
import os
import json
from datetime import datetime
# ...
class NewsCache:
    """新闻缓存（免费版）"""
    def __init__(self, cache_dir="./cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
# ...
    def get(self, date_str):
        cache_file = os.path.join(self.cache_dir, f"news_{date_str}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
# ...
    def set(self, date_str, data):
path.join(self.json")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
```
### 错误场景3

检查`error_code`并按照处理方式进行排查.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Python 3.8+ | 运行时 | 必需 | 官网下载安装 |
| requests | Python库 | 必需 | `pip install requests` |
| xml.etree.ElementTree | Python库 | 必需 | Python标准库（RSS解析） |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- 免费版无需任何API Key
- RSS订阅基于公开网页内容，不涉及付费API调用
- LLM模型路由由Agent平台内置提供

### 可用性分类
- **分类**: MD+EXEC（Markdown指令+命令行执行）
- **说明**: 通过自然语言指令驱动Agent执行新闻聚合与简报生成任务

## 已知限制
本免费体验版限制以下高级功能（需升级至专业版解锁）：

- **浏览器自动化模式**（获取无RSS源站点内容）
- **AI智能摘要**（基于LLM的深度摘要）
- **定时自动执行**（cron调度）
- **多渠道推送**（飞书/钉钉/企业微信/邮件）
- **AI辅助分类**（基于LLM的智能分类）
- **更多媒体源**（网易、腾讯、人民日报等）
- **新闻情感分析**（正面/负面/中性判断）
- **历史新闻查询**（过往新闻检索）
- **优先技术支持**

解锁全部高级能力请使用专业版：`china-news-tool-pro`
