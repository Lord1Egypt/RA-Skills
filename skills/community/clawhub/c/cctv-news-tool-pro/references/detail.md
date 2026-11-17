# 详细参考 - cctv-news-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
from collections import Counter, defaultdict
from datetime import datetime

class NewsTrendAnalyzer:
    """新闻趋势分析器（专业版）"""

    def __init__(self):
        self.keyword_timeline = defaultdict(list)

    def analyze_keywords(self, news_data_dict, top_n=20):
        """分析关键词频次趋势"""
        all_news = []
        for date, data in news_data_dict.items():
            if data.get("success"):
                news_list = data["data"].get("news", [])
                for news in news_list:
                    news["date"] = date
                    all_news.append(news)

        keyword_freq = Counter()
        keyword_dates = defaultdict(list)

        for news in all_news:
            title = news.get("title", "")
            keywords = self._extract_keywords(title)
            for kw in keywords:
                keyword_freq[kw] += 1
                keyword_dates[kw].append(news["date"])

        top_keywords = keyword_freq.most_common(top_n)
        return {
            "top_keywords": top_keywords,
            "keyword_timeline": {kw: keyword_dates[kw] for kw, _ in top_keywords},
            "total_news": len(all_news)
        }

    def analyze_themes(self, news_data_dict):
        """分析主题演变"""
        theme_timeline = defaultdict(lambda: defaultdict(int))

        for date, data in news_data_dict.items():
            if not data.get("success"):
                continue
            news_list = data["data"].get("news", [])
            for news in news_list:
                theme = self._classify_theme(news.get("title", ""))
                theme_timeline[theme][date] += 1

        return dict(theme_timeline)

    def generate_trend_report(self, news_data_dict):
        """生成趋势报告"""
        keyword_analysis = self.analyze_keywords(news_data_dict)
        theme_analysis = self.analyze_themes(news_data_dict)

        report = []
        report.append("=" * 60)
        report.append("  央视新闻联播趋势分析报告")
        report.append("=" * 60)
        report.append("")

        report.append("【关键词Top 10】")
        for kw, count in keyword_analysis["top_keywords"][:10]:
            dates = keyword_analysis["keyword_timeline"].get(kw, [])
            date_range = f"{min(dates)} 至 {max(dates)}" if dates else ""
            report.append(f"  {kw}: {count}次 ({date_range})")

        report.append("")
        report.append("【主题分布】")
        for theme, dates in theme_analysis.items():
            total = sum(dates.values())
            report.append(f"  {theme}: {total}条")

        report.append("")
        report.append(f"【统计】总新闻数：{keyword_analysis['total_news']}")

        return "\n".join(report)

    def _extract_keywords(self, text):
        """提取关键词（简化版）"""
        keywords = []
        important_words = ["经济", "科技", "改革", "外交", "主席", "总理",
                          "美国", "俄罗斯", "日本", "AI", "芯片", "新能源"]
        for word in important_words:
            if word in text:
                keywords.append(word)
        return keywords

    def _classify_theme(self, title):
        """分类主题"""
        if any(kw in title for kw in ["主席", "总理", "外交", "访问"]):
            return "政治外交"
        elif any(kw in title for kw in ["经济", "发展", "改革", "市场"]):
            return "经济发展"
        elif any(kw in title for kw in ["科技", "AI", "芯片", "创新"]):
            return "科技创新"
        elif any(kw in title for kw in ["民生", "教育", "医疗"]):
            return "民生社会"
        elif any(kw in title for kw in ["美国", "俄罗斯", "国际"]):
            return "国际事务"
        else:
            return "其他"

analyzer = NewsTrendAnalyzer()
report = analyzer.generate_trend_report(results)
print(report)
```

## 代码示例 (python)

```python
import requests
import json

class NewsPusher:
    """新闻推送器（专业版）"""

    def __init__(self):
        self.channels = {}

    def register_channel(self, name, webhook_url, channel_type="generic"):
        """注册推送渠道"""
        self.channels[name] = {
            "url": webhook_url,
            "type": channel_type
        }
        print(f"已注册渠道：{name}（{channel_type}）")

    def push(self, channel_name, content, title="央视新闻简报"):
        """推送新闻到指定渠道"""
        if channel_name not in self.channels:
            print(f"渠道 {channel_name} 未注册")
            return False

        channel = self.channels[channel_name]
        try:
            if channel["type"] == "feishu":
                return self._push_feishu(channel["url"], title, content)
            elif channel["type"] == "dingtalk":
                return self._push_dingtalk(channel["url"], title, content)
            elif channel["type"] == "wechat":
                return self._push_wechat(channel["url"], title, content)
            elif channel["type"] == "email":
                return self._push_email(channel["url"], title, content)
            elif channel["type"] == "slack":
                return self._push_slack(channel["url"], title, content)
            else:
                return self._push_generic(channel["url"], title, content)
        except Exception as e:
            print(f"推送失败：{e}")
            return False

    def push_all(self, content, title="央视新闻简报"):
        """推送到所有已注册渠道"""
        results = {}
        for name in self.channels:
            results[name] = self.push(name, content, title)
        return results

    def _push_feishu(self, url, title, content):
        """飞书推送"""
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {"title": {"tag": "plain_text", "content": title}},
                "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": content}}]
            }
        }
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _push_dingtalk(self, url, title, content):
        """钉钉推送"""
        payload = {
            "msgtype": "markdown",
            "markdown": {"title": title, "text": f"## {title}\n\n{content}"}
        }
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _push_wechat(self, url, title, content):
        """企业微信推送"""
        payload = {
            "msgtype": "markdown",
            "markdown": {"content": f"## {title}\n{content}"}
        }
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _push_email(self, url, title, content):
        """邮件推送"""
        payload = {"subject": title, "body": content, "format": "markdown"}
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _push_slack(self, url, title, content):
        """Slack推送"""
        payload = {"text": f"*{title}*\n{content}"}
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

    def _push_generic(self, url, title, content):
        """通用推送"""
        payload = {"title": title, "content": content}
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200

pusher = NewsPusher()
pusher.register_channel("feishu", "https://open.feishu.cn/open-apis/bot/v2/hook/xxx", "feishu")
pusher.register_channel("dingtalk", "https://oapi.dingtalk.com/robot/send?access_token=xxx", "dingtalk")
pusher.register_channel("wechat", "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx", "wechat")

pusher.push("feishu", "今日新闻联播要点：\n1. xxx\n2. xxx", "2025年2月10日新闻简报")
```

## 代码示例 (python)

```python
class AINewsSummarizer:
    """AI新闻摘要生成器（专业版）"""

    def __init__(self, llm_router=None):
        self.llm_router = llm_router  # 由Agent平台内置LLM提供
    def generate_daily_summary(self, news_data):
        """生成每日新闻AI摘要"""
        news_list = news_data.get("data", {}).get("news", [])
        if not news_list:
            return "无新闻内容"

        news_text = "\n".join([
            f"{i+1}. {news.get('title', '')}: {news.get('content', '')[:200]}"
            for i, news in enumerate(news_list)
        ])

        prompt = f"""请基于以下新闻联播内容，生成一份结构化的AI摘要：

{news_text}

要求：
1. 提取当日3-5个核心要点
2. 分析新闻主题（如政治、经济、科技、外交等）
3. 标注重要程度（高/中/低）
4. 生成100字以内的整体概述
"""
        summary = self._call_llm(prompt)
        return summary

    def generate_weekly_digest(self, weekly_data):
        """生成每周新闻摘要"""
        all_news = []
        for date, data in weekly_data.items():
            if data.get("success"):
                news_list = data["data"].get("news", [])
                for news in news_list:
                    news["date"] = date
                    all_news.append(news)

        themes = self._cluster_by_theme(all_news)

        prompt = f"""请基于以下一周新闻联播内容，生成一份周报：

主题聚类：
{self._format_themes(themes)}

要求：
1. 按主题分类总结
2. 标注本周最重要的3个事件
3. 分析新闻趋势与走向
4. 生成200字以内的周报概述
"""
        return self._call_llm(prompt)

    def _cluster_by_theme(self, news_list):
        """按主题聚类"""
        themes = {
            "政治外交": [],
            "经济发展": [],
            "科技创新": [],
            "民生社会": [],
            "国际事务": [],
            "其他": []
        }
        for news in news_list:
            title = news.get("title", "")
            if any(kw in title for kw in ["主席", "总理", "外交", "访问", "会见"]):
                themes["政治外交"].append(news)
            elif any(kw in title for kw in ["经济", "发展", "改革", "市场", "金融"]):
                themes["经济发展"].append(news)
            elif any(kw in title for kw in ["科技", "AI", "芯片", "创新", "技术"]):
                themes["科技创新"].append(news)
            elif any(kw in title for kw in ["民生", "教育", "医疗", "就业", "社保"]):
                themes["民生社会"].append(news)
            elif any(kw in title for kw in ["美国", "俄罗斯", "日本", "国际", "联合国"]):
                themes["国际事务"].append(news)
            else:
                themes["其他"].append(news)
        return themes

    def _format_themes(self, themes):
        """格式化主题"""
        lines = []
        for theme, news_list in themes.items():
            if news_list:
                lines.append(f"\n{theme}（{len(news_list)}条）:")
                for news in news_list[:3]:
                    lines.append(f"  - {news.get('title', '')}")
        return "\n".join(lines)

    def _call_llm(self, prompt):
        """调用LLM（由Agent平台内置）"""
        return f"[LLM摘要结果] 基于提示词生成的内容（{len(prompt)}字符输入）"

summarizer = AINewsSummarizer()
daily_summary = summarizer.generate_daily_summary(results.get("20250210", {}))
print(daily_summary)
```

