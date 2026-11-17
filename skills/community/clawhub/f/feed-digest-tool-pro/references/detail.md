# 详细参考 - feed-digest-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
from collections import defaultdict

class MultiSourceAggregator:
    """多源聚合器（专业版）"""

    def __init__(self):
        self.fetcher = FeedFetcher()

    def aggregate_by_theme(self, entries):
        """按主题跨源聚合"""
        themes = defaultdict(list)

        for entry in entries:
            theme = self._classify_theme(entry)
            themes[theme].append(entry)

        return dict(themes)

    def aggregate_by_importance(self, entries):
        """按重要程度聚合"""
        importance_levels = {'high': [], 'medium': [], 'low': []}

        for entry in entries:
            level = self._assess_importance(entry)
            importance_levels[level].append(entry)

        return importance_levels

    def find_cross_references(self, entries):
        """发现跨源关联"""
        references = []

        for i, entry1 in enumerate(entries):
            for j, entry2 in enumerate(entries[i+1:], i+1):
                if self._is_related(entry1, entry2):
                    references.append({
                        'entry1': entry1,
                        'entry2': entry2,
                        'relation': self._describe_relation(entry1, entry2)
                    })

        return references

    def _classify_theme(self, entry):
        """分类主题（AI辅助）"""
        title = entry.get('title', '')

        if any(kw in title for kw in ['AI', 'LLM', 'GPT', '大模型']):
            return 'AI与机器学习'
        elif any(kw in title for kw in ['架构', '系统', '分布式', '微服务']):
            return '系统架构'
        elif any(kw in title for kw in ['前端', 'React', 'Vue', 'CSS']):
            return '前端开发'
        elif any(kw in title for kw in ['后端', 'API', '数据库']):
            return '后端开发'
        elif any(kw in title for kw in ['DevOps', 'CI/CD', 'Docker', 'K8s']):
            return 'DevOps'
        else:
            return '其他'

    def _assess_importance(self, entry):
        """评估重要程度"""
        score = entry.get('score', 0)
        if score >= 3:
            return 'high'
        elif score >= 1:
            return 'medium'
        else:
            return 'low'

    def _is_related(self, entry1, entry2):
        """判断是否关联"""
        title1 = entry1.get('title', '')
        title2 = entry2.get('title', '')
        words1 = set(title1.split())
        words2 = set(title2.split())
        common = words1 & words2
        return len(common) >= 2

    def _describe_relation(self, entry1, entry2):
        """描述关联"""
        return f"主题相关：{entry1.get('title', '')} ↔ {entry2.get('title', '')}"

aggregator = MultiSourceAggregator()

themes = aggregator.aggregate_by_theme(filtered_entries)
print("=== 主题聚合 ===")
for theme, items in themes.items():
    print(f"\n【{theme}】({len(items)}条)")
    for item in items[:3]:
        print(f"  - {item['title']}")

references = aggregator.find_cross_references(filtered_entries)
print(f"\n=== 跨源关联 ({len(references)} 对) ===")
for ref in references[:5]:
    print(f"  {ref['relation']}")
```

## 代码示例 (python)

```python
class PersonalizedRecommender:
    """个性化推荐器（专业版）"""

    def __init__(self):
        self.read_history = []
        self.click_history = []
        self.preferences = {}

    def record_read(self, entry):
        """记录阅读"""
        self.read_history.append({
            'entry': entry,
            'read_at': datetime.now().isoformat()
        })

    def record_click(self, entry):
        """记录点击"""
        self.click_history.append({
            'entry': entry,
            'clicked_at': datetime.now().isoformat()
        })

    def update_preferences(self, preferences):
        """更新偏好"""
        self.preferences.update(preferences)

    def recommend(self, all_entries, top_n=10):
        """生成个性化推荐"""
        scored = []

        for entry in all_entries:
            score = self._score_entry(entry)
            if score > 0:
                entry['recommendation_score'] = score
                scored.append(entry)

        scored.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return scored[:top_n]

    def _score_entry(self, entry):
        """计算推荐得分"""
        score = 0
        title = entry.get('title', '')

        preferred_keywords = self.preferences.get('keywords', [])
        for kw in preferred_keywords:
            if kw in title:
                score += 2

        preferred_themes = self.preferences.get('themes', [])
        for theme in preferred_themes:
            if theme in title:
                score += 1

        preferred_feeds = self.preferences.get('feeds', [])
        if entry.get('feed') in preferred_feeds:
            score += 3

        return score

    def analyze_reading_patterns(self):
        """分析阅读模式"""
        if not self.read_history:
            return "暂无阅读历史"

        theme_count = {}
        for record in self.read_history:
            entry = record['entry']
            title = entry.get('title', '')
            if 'AI' in title:
                theme_count['AI'] = theme_count.get('AI', 0) + 1
            if '架构' in title:
                theme_count['架构'] = theme_count.get('架构', 0) + 1

        return {
            'total_reads': len(self.read_history),
            'theme_distribution': theme_count,
            'most_read_theme': max(theme_count, key=theme_count.get) if theme_count else None
        }

recommender = PersonalizedRecommender()
recommender.update_preferences({
    'keywords': ['AI', '架构', '性能优化'],
    'themes': ['AI', '系统设计'],
    'feeds': ['feed_id_1', 'feed_id_2']
})

recommendations = recommender.recommend(all_entries, top_n=10)
print("=== 个性化推荐 ===")
for i, entry in enumerate(recommendations, 1):
    print(f"{i}. {entry['title']} (score: {entry['recommendation_score']})")
```

## 代码示例 (python)

```python
class AIDigestGenerator:
    """AI深度摘要生成器（专业版）"""

    def __init__(self):
        self.llm_available = True  # 由Agent平台内置提供
    def generate_digest(self, entries):
        """生成AI深度摘要"""
        entries_text = self._prepare_input(entries)

        prompt = f"""请基于以下订阅条目生成深度AI摘要：

{entries_text}

要求：
1. 提取3-5个核心主题
2. 每个主题下整理2-3条相关条目
3. 标注重要程度（高/中/低）
4. 分析条目间的关联性
5. 生成200字整体概述
6. 推荐今日必读的Top 3
"""
        return self._call_llm(prompt)

    def generate_topic_summary(self, entries, topic):
        """生成特定主题的深度摘要"""
        filtered = [e for e in entries if topic.lower() in e.get('title', '').lower()]

        if not filtered:
            return f"未找到与'{topic}'相关的条目"

        prompt = f"""请基于以下关于'{topic}'的订阅条目生成专题摘要：

{self._format_entries(filtered)}

要求：
1. 主题背景介绍
2. 核心观点整理
3. 不同视角对比
4. 趋势分析
5. 推荐进一步阅读的条目
"""
        return self._call_llm(prompt)

    def generate_weekly_digest(self, weekly_entries):
        """生成每周AI摘要"""
        prompt = f"""请基于本周订阅条目生成周报：

{self._format_weekly(weekly_entries)}

要求：
1. 本周核心主题（3-5个）
2. 重要事件时间线
3. 趋势分析与走向预测
4. 下周关注重点
5. 300字周报概述
"""
        return self._call_llm(prompt)

    def _prepare_input(self, entries):
        lines = []
        for i, entry in enumerate(entries[:20], 1):
            lines.append(f"{i}. {entry.get('title', '')}")
            if entry.get('summary'):
                lines.append(f"   摘要：{entry['summary'][:100]}")
        return "\n".join(lines)

    def _format_entries(self, entries):
        lines = []
        for i, entry in enumerate(entries, 1):
            lines.append(f"{i}. {entry.get('title', '')}")
        return "\n".join(lines)

    def _format_weekly(self, weekly):
        lines = []
        for day, entries in weekly.items():
            lines.append(f"\n{day}:")
            for e in entries[:5]:
                lines.append(f"  - {e.get('title', '')}")
        return "\n".join(lines)

    def _call_llm(self, prompt):
        """调用LLM"""
        return f"[AI摘要] 基于输入生成（{len(prompt)}字符）"

ai_generator = AIDigestGenerator()
digest = ai_generator.generate_digest(filtered_entries)
print(digest)
```

## 代码示例 (python)

```python
import schedule
import time
from datetime import datetime

class ScheduledDigestPusher:
    """定时摘要推送器（专业版）"""

    def __init__(self):
        self.fetcher = FeedFetcher()
        self.filterer = FeedFilter()
        self.ai_generator = AIDigestGenerator()
        self.pusher = NewsPusher()
        self.running = False

    def setup_schedule(self):
        """配置定时任务"""
        schedule.every().day.at("08:00").do(self.daily_digest)
        schedule.every().day.at("12:00").do(self.noon_express)
        schedule.every().monday.at("09:00").do(self.weekly_digest)

        print("定时任务已配置：")
        print("  - 每天 08:00 每日AI摘要")
        print("  - 每天 12:00 午间快讯")
        print("  - 每周一 09:00 周报")

    def daily_digest(self):
        """每日AI摘要"""
        print(f"\n[{datetime.now()}] 执行每日AI摘要...")

        self.fetcher.fetch()

        entries_text = self.fetcher.get_entries(limit=50)
        entries = self._parse_entries(entries_text)

        filtered = self.filterer.filter_entries(entries_text)

        digest = self.ai_generator.generate_digest(filtered)

        self.pusher.push_all(digest, "每日订阅AI摘要")

        manager = ReadStatusManager()
        manager.mark_read([e['id'] for e in filtered])

    def noon_express(self):
        """午间快讯"""
        print(f"\n[{datetime.now()}] 执行午间快讯...")
        entries_text = self.fetcher.get_entries(limit=20)
        filtered = self.filterer.filter_entries(entries_text)[:5]

        express = "\n".join([
            f"- [{e.get('feed', '')}] {e['title']}"
            for e in filtered
        ])
        self.pusher.push_all(express, "午间订阅快讯")

    def weekly_digest(self):
        """周报"""
        print(f"\n[{datetime.now()}] 执行周报...")
        pass

    def start(self):
        """启动定时任务"""
        self.running = True
        self.setup_schedule()
        print("\n定时摘要推送器已启动...")
        while self.running:
            schedule.run_pending()
            time.sleep(60)

    def _parse_entries(self, text):
        """解析条目"""
        return []

scheduler = ScheduledDigestPusher()
scheduler.pusher.register("feishu", "https://open.feishu.cn/open-apis/bot/v2/hook/xxx", "feishu")
scheduler.pusher.register("slack", "REDACTED-SECRET", "slack")
```

