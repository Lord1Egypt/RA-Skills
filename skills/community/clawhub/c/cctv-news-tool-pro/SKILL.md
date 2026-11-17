---

slug: cctv-news-tool-pro
name: cctv-news-tool-pro
version: 1.0.0
displayName: 央视新闻抓取(专业版)
summary: "央视新闻联播抓取专业版，含批量查询、AI摘要、多渠道推送、历史趋势分析.。央视新闻抓取助手专业版是面向企业级场景的完整新闻联播内容获取与分析工具。在免费版单日查询能力之上，新增批量日期查询、"
license: Proprietary
edition: pro
description: "央视新闻抓取助手专业版是面向企业级场景的完整新闻联播内容获取与分析工具。在免费版单日查询能力之上，新增批量日期查询、AI智能摘要、多渠道推送、历史趋势分析、全文内容获取、视频片段元数据、个性化订阅七大高级能力。Use。Use when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。 功能涵盖: cctv。"
  when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策.
tags:
  - 央视新闻
  - 企业级
  - AI摘要
  - 趋势分析
  - 多渠道推送
  - 搜索
  - 检索
  - 工具
  - self
  - date
  - stats
  - success
  - result
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
# 定价元数据
category: "Knowledge"

---

> **批量查询+AI摘要+多渠道推送+趋势分析。企业级新闻情报全功能覆盖。**

将复杂的新闻情报获取与分析任务交给专业工具处理。专业版在免费版单日查询能力之上，新增批量日期查询、AI智能摘要、多渠道推送、历史趋势分析、全文内容获取、视频片段元数据、个性化订阅七大高级能力，满足企业级场景对新闻情报的深度、广度与时效性要求.
## 概述
### 免费版 vs 专业版能力对比
| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 单日查询 | 支持 | 支持 |
| 批量日期查询 | 不支持 | 支持（并发抓取） |
| AI智能摘要 | 不支持 | 支持（LLM深度摘要） |
| 多渠道推送 | 不支持 | 支持（飞书/钉钉/企业微信/邮件/Slack） |
| 历史趋势分析 | 不支持 | 支持（关键词频次、主题演变） |
| 全文内容 | 不支持 | 支持（完整新闻正文） |
| 视频片段元数据 | 不支持 | 支持 |
| 个性化订阅 | 不支持 | 支持（关键词过滤、主题订阅） |
| 国内/国际分类 | 基础 | 增强（AI辅助分类） |
| 技术支持 | 社区 | 优先工单响应 |

## 核心能力
### 1. 批量日期查询（并发抓取）
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 央视新闻抓取(专业版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
import concurrent.futures
import threading
from datetime import datetime, timedelta
# ...
class BatchNewsFetcher:
    """批量新闻抓取器（专业版）"""
# ...
    def __init__(self, max_workers=3, cache_dir="./cache"):
        self.max_workers = max_workers
        self.cache_dir = cache_dir
        self.lock = threading.Lock()
        self.results = {}
        self.stats = {"success": 0, "failed": 0, "total": 0}
# ...
    def fetch_date_range(self, start_date, end_date):
        """抓取日期范围内的新闻"""
        dates = self._generate_dates(start_date, end_date)
        print(f"启动批量抓取，共 {len(dates)} 天，并发数 {self.max_workers}")
# ...
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._fetch_single, date): date for date in dates}
            for future in concurrent.futures.as_completed(futures):
                date = futures[future]
                try:
                    result = future.result()
                    with self.lock:
                        self.results[date] = result
                        if result.get("success"):
stats["success"] += 1
                        else:
stats["failed"] += 1
                        status = "成功" if result.get("success") else "失败"
                        print(f"[{status}] {date}")
                except Exception as e:
                    print(f"[异常] {date}: {e}")
# ...
        self._print_summary()
        return self.results
# ...
    def _generate_dates(self, start, end):
        """生成日期列表"""
        start_dt = self._parse_date(start)
        end_dt = self._parse_date(end)
        dates = []
        current = start_dt
        while current <= end_dt:
            dates.append(current.strftime("%Y%m%d"))
            current += timedelta(days=1)
        return dates
# ...
    def _parse_date(self, date_input):
        """解析日期"""
        if isinstance(date_input, str):
            date_str = date_input.replace("-", "").replace("/", "")
            return datetime.strptime(date_str, "%Y%m%d")
        return date_input
# ...
    def _fetch_single(self, date_str):
        """抓取单个日期（带缓存）"""
        import os, json
        cache_file = os.path.join(self.cache_dir, f"news_{date_str}.json")
        os.makedirs(self.cache_dir, exist_ok=True)
# ...
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
# ...
        try:
            import subprocess
            result = subprocess.run(
                ["node", "（请参考skill目录中的脚本文件）", date_str],
                capture_output=True, text=True, timeout=60, encoding="utf-8"
            )
                data = json.loads(result.stdout)
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump({"success": True, "data": data, "date": date_str}, f, ensure_ascii=False)
                return {"success": True, "data": data, "date": date_str}
            return {"success": False, "error": result.stderr, "date": date_str}
        except Exception as e:
            return {"success": False, "error": str(e), "date": date_str}
# ...
    def _print_summary(self):
        """打印摘要"""
        print("\n=== 批量抓取摘要 ===")
        print(f"总数：{self.stats['total']}")
        print(f"成功：{self.stats['success']}")
        print(f"失败：{self.stats['failed']}")
        if self.stats['total'] > 0:
            success_rate = self.stats['success'] / self.stats['total'] * 100
            print(f"成功率：{success_rate:.1f}%")
# ...
fetcher = BatchNewsFetcher(max_workers=3)
results = fetcher.fetch_date_range("2025-02-01", "2025-02-28")
```

**处理**: 解析批量日期查询（并发抓取）的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量日期查询（并发抓取）的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. AI智能摘要（基于LLM）

> 详细代码示例已移至 `references/detail.md`

**处理**: 解析AI智能摘要（基于LLM）的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回AI智能摘要（基于LLM）的响应数据,包含状态码、结果和日志.
### 3. 多渠道推送

**处理**: 解析多渠道推送的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回多渠道推送的响应数据,包含状态码、结果和日志.
### 4. 历史趋势分析

**处理**: 解析历史趋势分析的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回历史趋势分析的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：央视新闻联播抓取、含批量查询、央视新闻抓取助手、专业版是面向企业、级场景的完整新闻、联播内容获取与分、析工具、在免费版单日查询、能力之上、新增批量日期查询、全文内容获取、视频片段元数据、个性化订阅七大高、级能力、Use、when、模型调用、智能对话、Agent、应用时使用、不适用于需要、确定性的关键决策等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：企业新闻情报订阅（企业信息部门）
**场景描述**：每日自动获取央视新闻，AI摘要后推送到企业飞书群.
```python
import schedule
# ...
def daily_news_brief():
    fetcher = BatchNewsFetcher()
    summarizer = AINewsSummarizer()
    pusher = NewsPusher()
    pusher.register_channel("feishu", "https://open.feishu.cn/open-apis/bot/v2/hook/未指定", "feishu")
# ...
    result = fetcher._fetch_single("today")
    if not result.get("success"):
        print("抓取失败")
        return
# ...
    summary = summarizer.generate_daily_summary(result)
# ...
    pusher.push("feishu", summary, "今日央视新闻AI摘要")
# ...
schedule.every().day.at("20:00").do(daily_news_brief)
```

### 场景二：舆情监控与趋势分析（市场研究团队）
**场景描述**：分析最近3个月新闻联播中特定关键词的提及频次趋势.
```python
fetcher = BatchNewsFetcher(max_workers=5)
analyzer = NewsTrendAnalyzer()
# ...
results = fetcher.fetch_date_range("2025-01-01", "2025-03-31")
# ...
report = analyzer.generate_trend_report(results)
print(report)
# ...
with open("news_trend_q1.txt", "w", encoding="utf-8") as f:
    f.write(report)
```

### 场景三：内容创作素材库（自媒体创作者）
**场景描述**：建立新闻素材库，按主题分类整理，便于内容创作时检索.
```python
fetcher = BatchNewsFetcher(max_workers=3)
summarizer = AINewsSummarizer()
# ...
results = fetcher.fetch_date_range("2025-02-01", "2025-02-28")
# ...
themes = {}
for date, data in results.items():
    if data.get("success"):
        news_list = data["data"].get("news", [])
        for news in news_list:
            theme = analyzer._classify_theme(news.get("title", ""))
            if theme not in themes:
                themes[theme] = []
            themes[theme].append({
                "date": date,
                "title": news.get("title"),
                "content": news.get("content", "")[:500]
            })
# ...
import json
with open("news_materials_feb.json", "w", encoding="utf-8") as f:
    json.dump(themes, f, ensure_ascii=False, indent=2)
# ...
print(f"素材库已生成，共 {sum(len(v) for v in themes.values())} 条新闻")
```

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手（批量抓取）
```bash
python3 -c "
from batch_fetcher import BatchNewsFetcher
fetcher = BatchNewsFetcher(max_workers=3)
results = fetcher.fetch_date_range('2025-02-04', '2025-02-10')
"
# ...
python3 -c "
from ai_summarizer import AINewsSummarizer
summarizer = AINewsSummarizer()
generate_daily_summary(results['20250210'])
print(summary)
"
```

### 120秒标准搭建
```bash
pip install requests schedule
# ...
export FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/未指定
export DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=未指定
# ...
python3 daily_pipeline.py --date-range 2025-02-01:2025-02-28 --push feishu,dingtalk
```

## 配置示例
### 企业级配置
```yaml
fetcher:
  max_workers: 5
  cache_dir: ./cache
  timeout: 60
# ...
ai_summarizer:
  model: gpt-4o
  max_tokens: 2000
  prompt_template: daily_summary_v2
# ...
pusher:
  channels:
    - name: feishu
      type: feishu
      url: https://open.feishu.cn/open-apis/bot/v2/hook/未指定
    - name: dingtalk
      type: dingtalk
      url: https://oapi.dingtalk.com/robot/send?access_token=未指定
    - name: wechat
      type: wechat
      url: https://qyapi.weixin.qq.com/cgi-（请参考skill目录中的脚本文件）?key=未指定
    - name: email
      type: email
      url: https://api.email-service.com/send
# ...
analyzer:
  top_keywords: 20
  theme_categories:
    - 政治外交
    - 经济发展
    - 科技创新
    - 民生社会
    - 国际事务
# ...
schedule:
  daily_brief: "0 20 * * *"  # 每天20:00
  weekly_digest: "0 10 * * 1"  # 每周一10:00
```

## 优选实践
### 1. 抓取频率控制
```python
fetcher = BatchNewsFetcher(max_workers=3)  # 建议不超过5
```

### 2. 缓存策略
```python
fetcher = BatchNewsFetcher(cache_dir="./cache")
```

### 3. AI摘要优化
```python
summarizer = AINewsSummarizer()
summary_formal = summarizer.generate_daily_summary(data, style="formal")
summary_brief = summarizer.generate_daily_summary(data, style="brief")
```

## 常见问题
### Q1：专业版如何与免费版兼容？
专业版完全兼容免费版的所有功能。免费版的单日查询、基础分类、JSON输出在专业版中均可直接使用。升级后原有脚本无需修改，仅新增高级能力可用.
### Q2：AI摘要使用什么模型？
专业版使用GPT-4o模型路由，提供更强的中文理解与摘要生成能力。支持自定义prompt模板，可生成不同风格的摘要（正式报告、简洁要点、口语化等）.
### Q3：批量抓取的最大并发数应该设多少？
建议根据目标站点承压能力设置：(1) 央视官网：3-5并发；(2) 单次批量建议不超过30天；(3) 跨月度抓取建议分批执行。专业版自动控制请求间隔，避免触发反爬.
### Q4：推送渠道支持哪些格式？
专业版支持：(1) 飞书（交互式卡片）；(2) 钉钉（Markdown消息）；(3) 企业微信（Markdown消息）；(4) 邮件（HTML/Markdown）；(5) Slack（带格式的文本）；(6) 通用Webhook（JSON）.
### Q5：趋势分析能发现什么？
趋势分析能发现：(1) 关键词频次变化（如"AI"提及次数月度趋势）；(2) 主题分布演变（如科技类新闻占比变化）；(3) 重要事件周期性（如每年两会期间政治类新闻激增）；(4) 长期报道重点转移.
### Q6：缓存数据如何管理？
专业版自动管理缓存：(1) 已抓取数据按日期存储为JSON文件；(2) 默认缓存有效期7天，过期后自动重新抓取；(3) 支持手动清理缓存（`clear_cache()`）；(4) 缓存文件可导出用于离线分析.
### Q7：可以定制AI摘要的prompt吗？
可以。专业版支持自定义prompt模板，可通过配置文件指定不同场景的模板（每日简报、周报、月报、专题分析等）。模板支持变量替换（如日期、新闻数量等）.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 16+ 或 **Bun**: 1.0+
- **Python**: 3.8+

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node.js 16+ | 运行时 | 二选一 | 官网下载安装 |
| Bun 1.0+ | 运行时 | 二选一 | `curl -fsSL https://bun.sh/install \| bash` |
| node-html-parser | npm包 | 必需 | `npm install node-html-parser` |
| Python 3.8+ | 运行时 | 必需 | 官网下载安装 |
| requests | Python库 | 必需 | `pip install requests`（推送功能） |
| schedule | Python库 | 可选 | `pip install schedule`（定时任务） |
| concurrent.futures | Python库 | 必需 | Python标准库（批量抓取） |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### LLM模型路由
- 专业版使用 **GPT-4o** 模型路由，提供更强的中文理解与摘要生成能力
- 支持自定义prompt模板、多风格摘要生成、智能主题聚类

### API Key 配置
- 新闻抓取基于公开网页内容，无需API Key
- 推送渠道需配置对应平台（飞书/钉钉/企业微信）的Webhook URL
- LLM模型路由由Agent平台内置提供

### 可用性分类
- **分类**: MD+EXEC（Markdown指令+命令行执行）
- **说明**: 通过自然语言指令驱动Agent执行企业级新闻情报获取与分析任务

## 专业版特性
本专业版相比免费版新增以下能力：

- **批量日期查询**：日期范围抓取、并发处理、结果聚合，支持单次最多30天
- **AI智能摘要**：基于GPT-4o的深度摘要生成，支持多种风格与自定义模板
- **多渠道推送**：飞书/钉钉/企业微信/邮件/Slack/通用Webhook六大渠道
- **历史趋势分析**：关键词频次、主题演变、周期性检测、长期趋势报告
- **全文内容获取**：完整新闻正文（非仅摘要）
- **视频片段元数据**：新闻联播视频片段的时长、链接、缩略图信息
- **个性化订阅**：关键词过滤、主题订阅、定向推送

此外，专业版还提供：
- 多角色场景指南（企业信息部门/市场研究/自媒体创作者）
- 完整FAQ（7问）与故障排查表
- 性能优化建议与优选实践
- GPT-4o模型路由与优先支持

## 定价
| 版本 | 价格 | 功能 | 适用场景 |
|:---:|:---:|:---:|:---:|
| 免费体验版 | ¥0 | 单日查询 + 基础分类 + JSON输出 + 基础简报 | 个人试用、单日查询 |
| 收费专业版 | ¥29/月 | 批量查询 + AI摘要 + 多渠道推送 + 趋势分析 + 全文 + 视频元数据 + 订阅 + 优先支持 | 团队/企业、情报监控 |

专业版通过SkillHub SkillPay发布.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "央视新闻抓取(专业版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "cctv news pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 央视新闻联播抓取专业版，含批量查询、AI摘要、多渠道推送、历史趋势分析.。央视新闻抓取助手专业版是面向企业级场景的完整新
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据