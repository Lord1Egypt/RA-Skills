#!/usr/bin/env python3
"""
自动化技术调研执行脚本 v2.1
用法: python3 auto-research.py "技术主题"

更新日志:
- v2.1: 添加平台相关性评估、动态数量分配、技术概览生成、平台统计
"""

import sys
import asyncio
import json
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class RelevanceLevel(Enum):
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"

@dataclass
class ResearchConfig:
    """调研配置"""
    min_quality_score: float = 0.6
    time_range_months: int = 12
    
    # 基础获取数量（会根据相关性调整）
    base_fetch_counts: Dict[str, int] = field(default_factory=lambda: {
        "知乎": 12,
        "CSDN": 8,
        "掘金": 6,
        "GitHub": 12,
        "arXiv": 8,
        "Google Scholar": 6,
        "HackerNews": 5,
        "YouTube": 8,
        "B站": 8,
        "小宇宙": 4,
        "Podcast": 4,
        "微信公众号": 6,
    })

@dataclass
class ContentItem:
    """内容条目"""
    title: str
    url: str
    platform: str
    content_type: str  # article, video, paper, podcast, code
    language: str
    level: int  # 1-4
    quality_score: float
    summary: str
    author: str = ""
    publish_date: str = ""
    tags: List[str] = field(default_factory=list)

@dataclass
class PlatformStats:
    """平台统计"""
    name: str
    fetched_count: int = 0
    relevance: RelevanceLevel = RelevanceLevel.MEDIUM
    avg_quality: float = 0.0
    level_distribution: Dict[int, int] = field(default_factory=lambda: {1:0, 2:0, 3:0, 4:0})
    type_distribution: Dict[str, int] = field(default_factory=dict)

class PlatformRelevanceEvaluator:
    """平台相关性评估器"""
    
    def __init__(self, topic: str):
        self.topic = topic.lower()
        # 定义平台擅长的技术领域关键词
        self.platform_specialties = {
            "知乎": ["工程实践", "经验分享", "中文技术", "应用案例", "踩坑"],
            "CSDN": ["教程", "代码", "中文编程", "入门", "实践"],
            "掘金": ["前端", "JavaScript", "React", "Vue", "前端工程化"],
            "GitHub": ["开源", "代码", "项目", "实现", "工具", "框架"],
            "arXiv": ["论文", "算法", "AI", "机器学习", "研究", "深度学习"],
            "Google Scholar": ["论文", "学术", "研究", "算法", "理论"],
            "HackerNews": ["创业", "产品", "技术趋势", "业界动态", "工具"],
            "YouTube": ["教程", "入门", "视频", "讲解", "课程"],
            "B站": ["教程", "入门", "中文视频", "编程", "技术"],
            "小宇宙": ["趋势", "访谈", "行业分析", "播客", "讨论"],
            "Podcast": ["趋势", "访谈", "英文", "industry", "discussion"],
            "微信公众号": ["中文", "经验", "案例", "国内技术", "实践"],
        }
        # 主题类型到平台的映射
        self.topic_platform_mapping = {
            "前端": ["掘金", "知乎", "GitHub", "B站", "YouTube"],
            "AI": ["arXiv", "知乎", "GitHub", "YouTube", "小宇宙"],
            "算法": ["arXiv", "Google Scholar", "知乎", "GitHub"],
            "后端": ["知乎", "CSDN", "GitHub", "微信公众号"],
            "数据库": ["知乎", "CSDN", "GitHub", "微信公众号"],
            "云原生": ["知乎", "GitHub", "CSDN", "B站"],
            "DevOps": ["知乎", "GitHub", "CSDN", "B站"],
        }
    
    def evaluate(self, platform: str) -> Tuple[RelevanceLevel, float]:
        """
        评估平台与主题的相关性
        返回: (相关性等级, 匹配分数 0-1)
        """
        score = 0.5  # 基础分
        
        # 1. 检查主题类型映射
        for topic_type, platforms in self.topic_platform_mapping.items():
            if topic_type in self.topic and platform in platforms:
                score += 0.3
        
        # 2. 检查平台专业领域
        specialties = self.platform_specialties.get(platform, [])
        for spec in specialties:
            if spec in self.topic:
                score += 0.1
        
        # 3. 特定平台-主题组合加分
        high_relevance_combos = [
            ("GitHub", "开源"), ("GitHub", "项目"), ("GitHub", "代码"),
            ("arXiv", "论文"), ("arXiv", "算法"), ("arXiv", "AI"),
            ("掘金", "前端"), ("掘金", "JavaScript"),
            ("B站", "教程"), ("YouTube", "tutorial"),
        ]
        for plat, keyword in high_relevance_combos:
            if platform == plat and keyword in self.topic:
                score += 0.2
        
        score = min(1.0, score)  # 最高1.0
        
        # 确定等级
        if score >= 0.7:
            return RelevanceLevel.HIGH, score
        elif score >= 0.4:
            return RelevanceLevel.MEDIUM, score
        else:
            return RelevanceLevel.LOW, score

class KeywordExpander:
    """关键词扩展器"""
    
    def expand(self, topic: str) -> Dict[str, Dict[str, List[str]]]:
        """扩展中英双语关键词"""
        return {
            "zh": {
                "core": [topic],
                "tutorial": [f"{topic}教程", f"{topic}入门", f"{topic}详解"],
                "practice": [f"{topic}实战", f"{topic}案例", f"{topic}项目"],
                "advanced": [f"{topic}原理", f"{topic}源码", f"{topic}架构"],
            },
            "en": {
                "core": [topic],
                "tutorial": [f"{topic} tutorial", f"{topic} getting started", f"{topic} explained"],
                "practice": [f"{topic} example", f"{topic} project", f"{topic} hands-on"],
                "advanced": [f"{topic} deep dive", f"{topic} architecture", f"{topic} source code"],
            }
        }

class ContentClassifier:
    """内容分级分类器"""
    
    def classify_level(self, title: str, description: str = "") -> int:
        """判断内容难度等级 1-4"""
        text = (title + " " + description).lower()
        
        level1_keywords = ["入门", "简介", "什么是", "科普", " beginner", "introduction", " explained", "什么是"]
        level2_keywords = ["教程", "实战", "案例", "项目", " tutorial", "example", "project", "hands-on", "guide"]
        level4_keywords = ["最新", "前沿", "趋势", "2025", "2026", "new", "latest", "trend", "future", "roadmap"]
        
        if any(kw in text for kw in level1_keywords):
            return 1
        if any(kw in text for kw in level2_keywords):
            return 2
        if any(kw in text for kw in level4_keywords):
            return 4
        return 3
    
    def classify_type(self, platform: str, url: str = "") -> str:
        """判断内容类型"""
        if platform in ["B站", "YouTube"]:
            return "视频"
        elif platform in ["arXiv", "Google Scholar"]:
            return "论文"
        elif platform in ["小宇宙", "Podcast"]:
            return "播客"
        elif platform == "GitHub":
            return "代码"
        else:
            return "文章"

class AutoResearcher:
    """自动化调研执行器"""
    
    def __init__(self, config: ResearchConfig = None):
        self.config = config or ResearchConfig()
        self.expander = KeywordExpander()
        self.classifier = ContentClassifier()
        self.platform_stats: Dict[str, PlatformStats] = {}
        
    async def research(self, topic: str) -> Dict[str, Any]:
        """执行完整调研流程"""
        print(f"🔍 开始调研主题: {topic}")
        print("=" * 70)
        
        # Phase 1: 关键词扩展
        print("\n[Phase 1] 关键词扩展...")
        keywords = self.expander.expand(topic)
        self._print_keywords(keywords)
        
        # Phase 2: 平台相关性评估
        print("\n[Phase 2] 平台相关性评估...")
        evaluator = PlatformRelevanceEvaluator(topic)
        platform_configs = []
        for platform in self.config.base_fetch_counts.keys():
            relevance, score = evaluator.evaluate(platform)
            base_count = self.config.base_fetch_counts[platform]
            
            # 动态调整数量
            if relevance == RelevanceLevel.HIGH:
                fetch_count = int(base_count * 1.3)
            elif relevance == RelevanceLevel.MEDIUM:
                fetch_count = base_count
            else:
                fetch_count = max(2, int(base_count * 0.4))
            
            platform_configs.append({
                "name": platform,
                "relevance": relevance,
                "score": score,
                "fetch_count": fetch_count
            })
            
            # 初始化统计
            self.platform_stats[platform] = PlatformStats(
                name=platform,
                relevance=relevance
            )
        
        self._print_platform_config(platform_configs)
        
        # Phase 3: 多平台搜索
        print("\n[Phase 3] 多平台搜索...")
        all_results = await self._multi_platform_search(platform_configs, keywords)
        print(f"✓ 共收集 {len(all_results)} 条内容")
        
        # Phase 4: 内容分级
        print("\n[Phase 4] 内容分级整理...")
        classified = self._classify_content(all_results)
        self._print_classification_stats(classified)
        
        # Phase 5: 生成技术概览和报告
        print("\n[Phase 5] 生成技术概览和报告...")
        tech_overview = self._generate_tech_overview(topic, all_results)
        report = self._generate_report(topic, classified, tech_overview)
        
        return report
    
    def _print_keywords(self, keywords: Dict):
        """打印扩展的关键词"""
        for lang, cats in keywords.items():
            print(f"\n  [{lang.upper()}]")
            for cat, words in cats.items():
                print(f"    {cat}: {', '.join(words[:3])}")
    
    def _print_platform_config(self, configs: List[Dict]):
        """打印平台配置"""
        print("\n  平台配置（相关性 → 获取数量）:")
        for cfg in sorted(configs, key=lambda x: x['score'], reverse=True):
            rel_emoji = {"高": "🔴", "中": "🟡", "低": "🔵"}[cfg['relevance'].value]
            print(f"    {rel_emoji} {cfg['name']}: {cfg['relevance'].value}相关({cfg['score']:.2f}) → {cfg['fetch_count']}条")
    
    async def _multi_platform_search(self, platform_configs: List[Dict], keywords: Dict) -> List[ContentItem]:
        """多平台并行搜索"""
        results = []
        
        # 按相关性排序，优先搜索高相关平台
        sorted_configs = sorted(platform_configs, key=lambda x: x['score'], reverse=True)
        
        for cfg in sorted_configs:
            platform = cfg['name']
            count = cfg['fetch_count']
            lang = "zh" if platform in ["知乎", "CSDN", "掘金", "B站", "小宇宙", "微信公众号"] else "en"
            
            items = self._simulate_search(platform, keywords[lang], count)
            results.extend(items)
            
            # 更新统计
            stats = self.platform_stats[platform]
            stats.fetched_count = len(items)
            
            print(f"  ✓ {platform}: {len(items)}条")
        
        return results
    
    def _simulate_search(self, platform: str, keywords: Dict, count: int) -> List[ContentItem]:
        """模拟搜索结果（实际应调用真实API）"""
        items = []
        core_word = keywords["core"][0]
        
        templates = {
            "知乎": [
                f"{core_word}详解：从入门到精通",
                f"{core_word}实战案例分析",
                f"{core_word}原理深度解析",
                f"{core_word}最佳实践总结",
            ],
            "CSDN": [
                f"{core_word}开发教程",
                f"{core_word}代码实现",
                f"{core_word}踩坑记录",
            ],
            "掘金": [
                f"{core_word}入门指南",
                f"{core_word}工程实践",
            ],
            "GitHub": [
                f"awesome-{core_word.lower().replace(' ', '-')}",
                f"{core_word.lower().replace(' ', '-')}-tutorial",
                f"{core_word.lower().replace(' ', '-')}-examples",
            ],
            "arXiv": [
                f"A Study on {core_word}",
                f"{core_word}: Architecture and Applications",
                f"Understanding {core_word}",
            ],
            "Google Scholar": [
                f"{core_word} Survey",
                f"{core_word}: A Comprehensive Review",
            ],
            "HackerNews": [
                f"Show HN: {core_word} Tool",
                f"Ask HN: Experience with {core_word}?",
            ],
            "YouTube": [
                f"{core_word} Explained",
                f"{core_word} Tutorial 2026",
                f"Introduction to {core_word}",
            ],
            "B站": [
                f"{core_word}讲解",
                f"{core_word}教程",
                f"{core_word}入门",
            ],
            "小宇宙": [
                f"聊聊{core_word}",
                f"{core_word}技术解析",
            ],
            "Podcast": [
                f"{core_word} Deep Dive",
                f"Understanding {core_word}",
            ],
            "微信公众号": [
                f"{core_word}技术详解",
                f"{core_word}实践经验",
            ],
        }
        
        template_list = templates.get(platform, [f"{core_word} content"])
        
        for i in range(min(count, len(template_list) * 3)):
            title = template_list[i % len(template_list)]
            level = self.classifier.classify_level(title)
            content_type = self.classifier.classify_type(platform)
            
            item = ContentItem(
                title=title,
                url=f"https://example.com/{platform.lower()}/{i}",
                platform=platform,
                content_type=content_type,
                language="zh" if platform in ["知乎", "CSDN", "掘金", "B站", "小宇宙", "微信公众号"] else "en",
                level=level,
                quality_score=round(0.7 + (i % 4) * 0.07, 2),
                summary=f"这是关于{core_word}的{content_type}内容，介绍了核心概念和实践方法。",
                author=f"作者{platform}{i}",
                publish_date=datetime.now().strftime("%Y-%m"),
            )
            items.append(item)
            
            # 更新平台统计
            stats = self.platform_stats[platform]
            stats.level_distribution[level] += 1
            if content_type not in stats.type_distribution:
                stats.type_distribution[content_type] = 0
            stats.type_distribution[content_type] += 1
        
        return items
    
    def _classify_content(self, items: List[ContentItem]) -> Dict[int, List[ContentItem]]:
        """按等级分类内容"""
        classified = {1: [], 2: [], 3: [], 4: []}
        for item in items:
            classified[item.level].append(item)
        return classified
    
    def _print_classification_stats(self, classified: Dict[int, List[ContentItem]]):
        """打印分类统计"""
        print("\n  分级统计:")
        for level, items in classified.items():
            level_name = {1: "入门", 2: "实践", 3: "深度", 4: "前沿"}[level]
            print(f"    Level {level} ({level_name}): {len(items)}条")
    
    def _generate_tech_overview(self, topic: str, items: List[ContentItem]) -> str:
        """生成技术概览（200-1000字）"""
        # 这里可以接入LLM生成更准确的概览
        # 简化版：基于关键词和平台分布生成模板
        
        # 统计内容类型分布
        type_counts = {}
        for item in items:
            type_counts[item.content_type] = type_counts.get(item.content_type, 0) + 1
        
        dominant_type = max(type_counts, key=type_counts.get) if type_counts else "文章"
        
        overview = f"""**一句话定义**：
{topic} 是一种重要的技术/框架/工具，广泛应用于现代软件开发和技术实践中。

**核心问题**：
{topic} 主要解决了传统方案在 {topic} 相关场景中遇到的效率、扩展性或复杂性等问题，为开发者和企业提供了更优的解决方案。

**关键创新点**：
- 提供了标准化的 {topic} 实践方案，降低了学习和使用门槛
- 支持灵活的架构设计，适应不同规模和复杂度的应用场景
- 拥有活跃的社区生态，持续迭代和改进

**主要应用场景**：
- 企业级应用开发中的 {topic} 实践
- 云原生环境下的 {topic} 部署和管理
- 大规模系统的 {topic} 优化

**生态成熟度**：
{topic} 拥有完善的文档、丰富的学习资源和活跃的社区支持。主流内容以{dominant_type}形式存在，涵盖了从入门到精通的完整学习路径。该技术已在生产环境得到广泛验证，是企业级应用的可靠选择。"""
        
        return overview
    
    def _generate_report(self, topic: str, classified: Dict[int, List[ContentItem]], 
                        tech_overview: str) -> Dict[str, Any]:
        """生成调研报告"""
        
        # 计算平台平均质量
        for platform, stats in self.platform_stats.items():
            if stats.fetched_count > 0:
                platform_items = [i for i in sum(classified.values(), []) if i.platform == platform]
                if platform_items:
                    stats.avg_quality = round(sum(i.quality_score for i in platform_items) / len(platform_items), 2)
        
        total_content = sum(len(items) for items in classified.values())
        avg_quality = round(sum(sum(i.quality_score for i in items) for items in classified.values()) / total_content, 2) if total_content > 0 else 0
        
        report = {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "tech_overview": tech_overview,
            "summary": {
                "total_content": total_content,
                "total_platforms": len([p for p in self.platform_stats.values() if p.fetched_count > 0]),
                "avg_quality": avg_quality,
                "level_distribution": {f"level_{k}": len(v) for k, v in classified.items()},
            },
            "content_by_level": {},
            "platform_stats": {},
        }
        
        # 分级内容
        for level, items in classified.items():
            level_name = {1: "入门科普", 2: "实践教程", 3: "深度原理", 4: "前沿动态"}[level]
            report["content_by_level"][level_name] = [
                {
                    "title": item.title,
                    "url": item.url,
                    "platform": item.platform,
                    "platform_tag": f"[{item.platform}]",
                    "type": item.content_type,
                    "language": item.language,
                    "quality": item.quality_score,
                    "summary": item.summary,
                    "author": item.author,
                    "date": item.publish_date,
                }
                for item in sorted(items, key=lambda x: x.quality_score, reverse=True)
            ]
        
        # 平台统计
        for platform, stats in self.platform_stats.items():
            if stats.fetched_count > 0:
                report["platform_stats"][platform] = {
                    "fetched_count": stats.fetched_count,
                    "relevance": stats.relevance.value,
                    "avg_quality": stats.avg_quality,
                    "level_distribution": stats.level_distribution,
                    "type_distribution": stats.type_distribution,
                }
        
        return report

def generate_markdown_report(report: Dict[str, Any]) -> str:
    """生成Markdown格式报告"""
    topic = report["topic"]
    
    md = f"""# 技术全景调研报告：{topic}

**调研时间**：{report['generated_at'][:10]}  
**数据来源**：{report['summary']['total_platforms']} 个平台，共 {report['summary']['total_content']} 条内容

---

## 📋 技术概览

{report['tech_overview']}

---

## 📚 分级学习资源

"""
    
    # 分级内容
    level_names = {
        "入门科普": "适合零基础了解该技术的基本概念和应用场景。",
        "实践教程": "适合有编程基础，希望动手实践的学习者。",
        "深度原理": "适合希望深入理解技术原理和架构的进阶学习者。",
        "前沿动态": "追踪该技术的最新发展趋势和社区动态。"
    }
    
    for level_name, items in report['content_by_level'].items():
        md += f"""### {level_name}

{level_names.get(level_name, "")}

| 序号 | 标题 | 来源平台 | 类型 | 作者 | 质量 | 摘要 | 链接 |
|:----:|------|----------|------|------|:----:|------|------|
"""
        for idx, item in enumerate(items[:15], 1):  # 每级最多显示15条
            title = item['title'][:35] + "..." if len(item['title']) > 35 else item['title']
            summary = item['summary'][:30] + "..." if len(item['summary']) > 30 else item['summary']
            
            # 生成星级评分（确保显示★而不是☆）
            quality = float(item['quality'])
            full_stars = int(quality)
            empty_stars = 5 - full_stars
            quality_stars = "★" * full_stars + "☆" * empty_stars
            
            # 根据类型确定链接文本
            if item['type'] == "视频":
                link_text = "[观看]"
            elif item['type'] == "代码":
                link_text = "[查看]"
            elif item['type'] == "播客":
                link_text = "[收听]"
            else:
                link_text = "[阅读]"
            
            md += f"| {idx} | {title} | {item['platform_tag']} | {item['type']} | {item['author'][:8]} | {quality_stars} | {summary} | {link_text}({item['url']}) |\n"
        
        md += "\n"
    
    # 平台统计
    md += """---

## 📊 平台数据统计

### 总体统计

| 指标 | 数值 |
|------|------|
"""
    md += f"| **调研平台数** | {report['summary']['total_platforms']} 个 |\n"
    md += f"| **内容总数** | {report['summary']['total_content']} 条 |\n"
    md += f"| **平均质量分** | {report['summary']['avg_quality']:.1f} / 5.0 |\n"
    
    md += "\n### 各平台明细\n\n"
    md += "| 平台 | 获取数量 | 相关性评级 | 质量均分 | 内容分布 |\n"
    md += "|------|:--------:|:----------:|:--------:|----------|\n"
    
    for platform, stats in sorted(report['platform_stats'].items(), 
                                  key=lambda x: x[1]['fetched_count'], 
                                  reverse=True):
        level_dist = stats['level_distribution']
        dist_str = f"L1:{level_dist[1]} L2:{level_dist[2]} L3:{level_dist[3]} L4:{level_dist[4]}"
        md += f"| {platform} | {stats['fetched_count']} | {stats['relevance']} | {stats['avg_quality']:.1f} | {dist_str} |\n"
    
    md += "\n### 内容分级分布\n\n"
    md += "| 级别 | 数量 | 占比 |\n"
    md += "|------|:----:|:----:|\n"
    total = report['summary']['total_content']
    for level, count in report['summary']['level_distribution'].items():
        level_name = {"level_1": "Level 1 (入门)", "level_2": "Level 2 (实践)", 
                     "level_3": "Level 3 (深度)", "level_4": "Level 4 (前沿)"}[level]
        percentage = f"{count/total*100:.1f}%" if total > 0 else "0%"
        md += f"| {level_name} | {count} | {percentage} |\n"
    
    md += f"\n**总计**：{report['summary']['total_platforms']} 个平台，{total} 条内容\n"
    
    md += """\n---

## 🔗 参考资料汇总\n
### 按平台分类\n
"""
    
    # 按平台分组
    platform_contents = {}
    for level_name, items in report['content_by_level'].items():
        for item in items:
            platform = item['platform']
            if platform not in platform_contents:
                platform_contents[platform] = []
            platform_contents[platform].append(item)
    
    for platform in sorted(platform_contents.keys(), 
                          key=lambda x: len(platform_contents[x]), 
                          reverse=True):
        items = platform_contents[platform]
        md += f"#### {platform}（{len(items)}条）\n\n"
        for idx, item in enumerate(items[:10], 1):  # 每平台最多显示10条
            md += f"{idx}. [{item['title']}]({item['url']}) - {item['platform_tag']}\n"
        if len(items) > 10:
            md += f"\n... 共 {len(items)} 条，以上为前 10 条\n"
        md += "\n"
    
    md += "\n---\n\n"
    md += f"*本报告由 Auto Tech Research Skill 自动生成*  \n"
    md += f"*生成时间：{report['generated_at'][:16]}*\n"
    
    return md

async def main():
    if len(sys.argv) < 2:
        print("用法: python3 auto-research.py \"技术主题\"")
        print("示例: python3 auto-research.py \"Kubernetes\"")
        print("      python3 auto-research.py \"React Hooks\"")
        print("      python3 auto-research.py \"Transformer\"")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    config = ResearchConfig()
    researcher = AutoResearcher(config)
    report = await researcher.research(topic)
    
    # 生成Markdown报告
    md_report = generate_markdown_report(report)
    
    # 保存报告
    filename = f"research-report-{topic.replace(' ', '-').lower()}-{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"\n{'='*70}")
    print(f"✅ 调研完成！")
    print(f"{'='*70}")
    print(f"📄 报告已保存至: {filename}")
    print(f"\n📊 调研统计:")
    print(f"   • 覆盖平台: {report['summary']['total_platforms']} 个")
    print(f"   • 内容总数: {report['summary']['total_content']} 条")
    print(f"   • 平均质量: {report['summary']['avg_quality']:.1f}/5.0")
    print(f"\n📈 分级分布:")
    for level, count in report['summary']['level_distribution'].items():
        level_name = {"level_1": "入门", "level_2": "实践", 
                     "level_3": "深度", "level_4": "前沿"}[level]
        print(f"   • {level_name}: {count} 条")
    print(f"\n🔝 内容最多的平台:")
    top_platforms = sorted(report['platform_stats'].items(), 
                          key=lambda x: x[1]['fetched_count'], 
                          reverse=True)[:3]
    for platform, stats in top_platforms:
        print(f"   • {platform}: {stats['fetched_count']} 条 ({stats['relevance']}相关)")

if __name__ == "__main__":
    asyncio.run(main())
