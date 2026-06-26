"""
AI前沿哨兵 - 信息分析评分模块
对采集的信息进行智能分析和评分
"""
import json
from datetime import datetime
from pathlib import Path


class InfoAnalyzer:
    """信息分析器"""
    
    # 来源权重配置
    SOURCE_WEIGHTS = {
        "arxiv": 1.5,       # 学术论文权重高
        "github": 1.3,      # 开源项目
        "hackernews": 1.2,  # 技术社区讨论
        "twitter": 1.0,     # 社交媒体
        "blogs": 1.4        # 官方博客
    }
    
    # 热度关键词
    HOT_KEYWORDS = [
        "breaking", "revolutionary", "breakthrough", "new model",
        "launch", "release", "announce", "official",
        "GPT-4", "Claude", "Gemini", "Llama", "Mistral",
        "Sora", "DALL-E", "Stable Diffusion"
    ]
    
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.keywords = self.settings.get("keywords", [])
    
    def analyze(self, raw_data):
        """
        分析采集的原始数据
        
        Args:
            raw_data: 采集的原始数据，包含 sources 字段
        
        Returns:
            dict: 分析后的结构化数据
        """
        sources = raw_data.get("sources", {})
        
        # 合并所有项目
        all_items = []
        for source_name, source_data in sources.items():
            if source_data.get("status") != "success":
                continue
            
            items = source_data.get("items", [])
            for item in items:
                item["_source_name"] = source_name
                item["_weight"] = self.SOURCE_WEIGHTS.get(source_name, 1.0)
                all_items.append(item)
        
        # 计算综合评分
        scored_items = self._calculate_scores(all_items)
        
        # 按类型分类
        categorized = self._categorize(scored_items)
        
        # 提取关键发现
        insights = self._extract_insights(scored_items)
        
        return {
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "total_items": len(all_items),
            "scored_items": scored_items,
            "categorized": categorized,
            "insights": insights,
            "summary": self._generate_summary(categorized, insights)
        }
    
    def _calculate_scores(self, items):
        """
        计算每个项目的综合评分
        
        评分维度:
        1. 原始热度 (stars, score, likes等)
        2. 新鲜度 (越新分数越高)
        3. 来源权重
        4. 关键词匹配
        """
        from datetime import datetime, timedelta
        
        now = datetime.now()
        scored_items = []
        
        for item in items:
            score = 0
            factors = {}
            
            # 1. 热度分数
            if "stars" in item:
                score += min(item["stars"] / 100, 50)  # 最多50分
                factors["stars"] = item["stars"]
            if "score" in item:
                score += min(item["score"] / 10, 30)  # 最多30分
                factors["score"] = item["score"]
            if "likes" in item:
                score += min(item["likes"] / 50, 20)  # 最多20分
                factors["likes"] = item["likes"]
            
            # 2. 新鲜度分数
            time_score = self._calculate_freshness(item, now)
            score += time_score
            factors["freshness"] = time_score
            
            # 3. 来源权重
            weight = item.get("_weight", 1.0)
            score *= weight
            factors["weight"] = weight
            
            # 4. 关键词匹配加分
            keyword_bonus = self._calculate_keyword_bonus(item)
            score += keyword_bonus
            factors["keyword_bonus"] = keyword_bonus
            
            # 5. 热度关键词检测
            if self._contains_hot_keyword(item):
                score *= 1.5
                factors["hot_keyword"] = True
            
            # 存储评分结果
            item["_score"] = round(score, 2)
            item["_factors"] = factors
            scored_items.append(item)
        
        # 按分数排序
        scored_items.sort(key=lambda x: x["_score"], reverse=True)
        
        return scored_items
    
    def _calculate_freshness(self, item, now):
        """计算新鲜度分数"""
        from datetime import datetime
        
        # 尝试从各种字段获取时间
        time_fields = ["created_at", "published", "updated_at", "created", "time"]
        
        for field in time_fields:
            if field in item and item[field]:
                try:
                    time_str = item[field]
                    # 处理ISO格式
                    if "T" in time_str:
                        item_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                    else:
                        item_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    
                    # 计算时间差
                    diff = now - item_time
                    hours = diff.total_seconds() / 3600
                    
                    # 24小时内满分，48小时60%分，7天外10%分
                    if hours < 24:
                        return 30
                    elif hours < 48:
                        return 20
                    elif hours < 72:
                        return 15
                    elif hours < 168:  # 7天
                        return 10
                    else:
                        return 5
                        
                except:
                    continue
        
        return 10  # 默认中等分数
    
    def _calculate_keyword_bonus(self, item):
        """计算关键词匹配加分"""
        if not self.keywords:
            return 0
        
        text = f"{item.get('title', '')} {item.get('description', '')} {item.get('text', '')} {item.get('abstract', '')}"
        text = text.lower()
        
        matches = sum(1 for kw in self.keywords if kw.lower() in text)
        return matches * 5  # 每个匹配加5分
    
    def _contains_hot_keyword(self, item):
        """检测是否包含热度关键词"""
        text = f"{item.get('title', '')} {item.get('description', '')}"
        text = text.lower()
        
        for keyword in self.HOT_KEYWORDS:
            if keyword.lower() in text:
                return True
        
        return False
    
    def _categorize(self, items):
        """按类型分类（自动去重）"""
        categories = {
            "papers": [],      # 学术论文
            "projects": [],    # 开源项目
            "discussions": [], # 社区讨论
            "news": [],        # 新闻动态
            "tweets": []       # 社交动态
        }
        
        # 去重跟踪：使用URL作为唯一标识
        seen_urls = set()
        
        type_mapping = {
            "paper": "papers",
            "repository": "projects",
            "discussion": "discussions",
            "article": "news",
            "tweet": "tweets"
        }
        
        for item in items:
            source_type = item.get("source_type", "")
            category = type_mapping.get(source_type, "news")
            
            # 使用URL去重，如果没有URL则用title+source_type组合
            url = item.get("url") or item.get("hn_url") or item.get("pdf_url") or ""
            dedup_key = f"{url}:{item.get('title', '')}"
            
            if url and dedup_key in seen_urls:
                continue
            
            if url:
                seen_urls.add(dedup_key)
            
            categories[category].append(item)
        
        return categories
    
    def _extract_insights(self, items):
        """提取关键发现"""
        insights = {
            "hot_topics": [],
            "trending_projects": [],
            "important_papers": [],
            "must_read": []
        }
        
        # 热度话题
        title_words = {}
        for item in items[:30]:
            title = item.get("title", "")
            for word in title.split():
                if len(word) > 4:
                    title_words[word] = title_words.get(word, 0) + 1
        
        top_words = sorted(title_words.items(), key=lambda x: x[1], reverse=True)[:5]
        insights["hot_topics"] = [w[0] for w in top_words]
        
        # 热门项目 (Top 5 by score)
        insights["trending_projects"] = [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "score": item.get("_score", 0),
                "stars": item.get("stars", 0)
            }
            for item in items
            if item.get("source_type") == "repository"
        ][:5]
        
        # 重要论文
        insights["important_papers"] = [
            {
                "title": item.get("title", ""),
                "authors": item.get("author_str", ""),
                "url": item.get("url", ""),
                "score": item.get("_score", 0)
            }
            for item in items
            if item.get("source_type") == "paper"
        ][:5]
        
        # 必读内容 (Top 10)
        insights["must_read"] = items[:10]
        
        return insights
    
    def _generate_summary(self, categorized, insights):
        """生成摘要"""
        return {
            "papers_count": len(categorized["papers"]),
            "projects_count": len(categorized["projects"]),
            "discussions_count": len(categorized["discussions"]),
            "news_count": len(categorized["news"]),
            "tweets_count": len(categorized["tweets"]),
            "hot_topics": insights["hot_topics"],
            "top_score": insights["must_read"][0]["_score"] if insights["must_read"] else 0
        }


def load_raw_data(data_dir):
    """加载最新的原始数据"""
    data_dir = Path(data_dir)
    if not data_dir.exists():
        return None
    
    files = list(data_dir.glob("raw_data_*.json"))
    if not files:
        return None
    
    # 获取最新的文件
    latest = max(files, key=lambda f: f.stat().st_mtime)
    
    with open(latest, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI前沿哨兵 - 信息分析工具")
    parser.add_argument("--input", type=str, help="原始数据JSON文件路径")
    parser.add_argument("--output", type=str, help="分析结果输出路径")
    args = parser.parse_args()
    
    data_dir = Path(__file__).parent.parent / "output"
    
    # 加载原始数据
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    else:
        raw_data = load_raw_data(data_dir)
    
    if raw_data:
        analyzer = InfoAnalyzer({"keywords": ["AI", "LLM", "GPT"]})
        result = analyzer.analyze(raw_data)
        
        # 保存结果
        if args.output:
            output_path = Path(args.output)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = data_dir / f"analyzed_{timestamp}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 分析完成，结果已保存到: {output_path}")
    else:
        print("❌ 未找到原始数据文件")
