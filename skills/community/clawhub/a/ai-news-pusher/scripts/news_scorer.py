#!/usr/bin/env python3
"""
新闻价值评分模块 - 基于 LLM 的产品价值打分系统
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class NewsScorer:
    """新闻价值评分器"""
    
    # Few-shot 学习样例
    FEW_SHOT_EXAMPLES = [
        {
            "news": {
                "title": "GPT-5 Technical Report: Multimodal Reasoning at Scale",
                "content": "OpenAI今日发布GPT-5技术报告，新增1T参数MoE架构，在MMLU上达到95.2%准确率...",
                "source": "openai_blog",
                "source_weight": 10,
                "published_date": (datetime.now() - timedelta(hours=2)).isoformat()
            },
            "expected_score": 95,
            "rationale": "OpenAI官方发布，24小时内首发，技术细节丰富，产业影响重大"
        },
        {
            "news": {
                "title": "RAG技术在企业知识库中的应用实践",
                "content": "本文详细介绍了检索增强生成在企业级知识库中的部署方案，包括向量数据库选型、提示词优化等...",
                "source": "huggingface_blog",
                "source_weight": 9,
                "published_date": (datetime.now() - timedelta(days=1)).isoformat()
            },
            "expected_score": 82,
            "rationale": "高质量社区来源，技术实践干货，有落地场景，信息增量大"
        },
        {
            "news": {
                "title": "AI创业公司获1000万美元种子轮融资",
                "content": "某AI创业公司今日宣布完成1000万美元种子轮融资，投资方包括多家知名VC...",
                "source": "techcrunch_ai",
                "source_weight": 8,
                "published_date": (datetime.now() - timedelta(hours=12)).isoformat()
            },
            "expected_score": 75,
            "rationale": "知名科技媒体，时效性强，有融资信息，但技术深度有限"
        }
    ]
    
    # 评分阈值
    AUTO_PUSH_THRESHOLD = 80
    GRAY_ZONE_MIN = 60
    GRAY_ZONE_MAX = 80
    
    def __init__(self, llm_provider: str = "openai"):
        """
        初始化评分器
        
        Args:
            llm_provider: LLM 提供商 (openai, anthropic, etc.)
        """
        self.llm_provider = llm_provider
        self.api_key = self._get_api_key()
        self.few_shot_examples = self.FEW_SHOT_EXAMPLES.copy()
        self.feedback_data: List[Dict] = []
        
    def _get_api_key(self) -> Optional[str]:
        """获取 API Key"""
        if self.llm_provider == "openai":
            return os.environ.get('OPENAI_API_KEY')
        elif self.llm_provider == "anthropic":
            return os.environ.get('ANTHROPIC_API_KEY')
        return None
    
    def _calculate_source_bonus(self, source_weight: int, source_category: str) -> int:
        """计算信源加分"""
        bonus = 0
        if source_weight >= 9:
            bonus += 15
        elif source_weight >= 7:
            bonus += 10
        elif source_weight >= 5:
            bonus += 5
        
        if source_category == 'official':
            bonus += 10
        elif source_category == 'academic':
            bonus += 8
        
        return min(bonus, 25)
    
    def _calculate_recency_score(self, published_date_str: str) -> int:
        """计算时效性得分"""
        try:
            if not published_date_str:
                return 0
            
            published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
            now = datetime.now()
            hours_diff = (now - published_date).total_seconds() / 3600
            
            if hours_diff <= 6:
                return 25
            elif hours_diff <= 12:
                return 20
            elif hours_diff <= 24:
                return 15
            elif hours_diff <= 48:
                return 10
            elif hours_diff <= 72:
                return 5
            return 0
        except:
            return 0
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取技术关键词"""
        tech_keywords = [
            'transformer', 'moe', 'rag', 'fine-tuning', 'pretrain',
            'llama', 'gpt', 'claude', 'mistral', 'gemma',
            'mmlu', 'humaneval', 'benchmark', 'token', 'context window',
            'quantization', 'inference', 'training', 'dataset',
            'api', 'sdk', 'framework', 'model', 'architecture'
        ]
        content_lower = content.lower()
        found = [kw for kw in tech_keywords if kw in content_lower]
        return found
    
    def _build_scoring_prompt(self, news: Dict) -> str:
        """构建评分提示词"""
        few_shot_text = ""
        for i, example in enumerate(self.few_shot_examples, 1):
            few_shot_text += f"""
示例 {i}:
新闻标题: {example['news']['title']}
新闻内容: {example['news']['content'][:200]}...
信源: {example['news']['source']}
发布时间: {example['news']['published_date']}
预期得分: {example['expected_score']}
评分理由: {example['rationale']}
"""
        
        return f"""你是一位专业的AI行业资讯分析师，请为以下AI新闻进行"产品价值"打分（0-100分）。

评分维度：
1. 时效性 (25%) - 是否为24小时内首发消息
2. 源头权重 (25%) - 来自官方/学术机构还是普通媒体
3. 产业关联度 (25%) - 是底层技术突破还是应用层八卦
4. 信息增量 (25%) - 是否提供新参数/融资额/落地场景

{few_shot_text}

请评估以下新闻，只返回JSON格式，包含"score"（0-100整数）和"rationale"（评分理由）字段：

新闻标题: {news.get('title', '')}
新闻内容: {news.get('content', '')}
信源: {news.get('source', 'unknown')}
信源权重: {news.get('source_weight', 5)}
信源分类: {news.get('source_category', 'unknown')}
发布时间: {news.get('published_date', '')}
链接: {news.get('url', '')}
"""
    
    def _score_with_llm(self, news: Dict) -> Tuple[int, str]:
        """使用 LLM 评分"""
        if not self.api_key:
            return self._score_with_rules(news)
        
        try:
            prompt = self._build_scoring_prompt(news)
            
            if self.llm_provider == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是一位专业的AI行业资讯分析师，只返回JSON格式。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                result_text = response.choices[0].message.content.strip()
            
            elif self.llm_provider == "anthropic":
                import anthropic
                client = anthropic.Anthropic(api_key=self.api_key)
                response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=500,
                    temperature=0.3,
                    messages=[{"role": "user", "content": prompt}]
                )
                result_text = response.content[0].text.strip()
            
            else:
                return self._score_with_rules(news)
            
            try:
                result = json.loads(result_text)
                score = max(0, min(100, int(result.get('score', 50))))
                rationale = result.get('rationale', '')
                return score, rationale
            except:
                return self._score_with_rules(news)
                
        except Exception as e:
            print(f"LLM 评分失败，使用规则评分: {e}")
            return self._score_with_rules(news)
    
    def _score_with_rules(self, news: Dict) -> Tuple[int, str]:
        """基于规则的备用评分方法"""
        score = 50
        rationale_parts = []
        
        recency_score = self._calculate_recency_score(news.get('published_date', ''))
        score += recency_score
        if recency_score > 0:
            rationale_parts.append(f"时效性+{recency_score}")
        
        source_bonus = self._calculate_source_bonus(
            news.get('source_weight', 5),
            news.get('source_category', 'unknown')
        )
        score += source_bonus
        if source_bonus > 0:
            rationale_parts.append(f"信源+{source_bonus}")
        
        keywords = self._extract_keywords(news.get('content', '') + news.get('title', ''))
        keyword_bonus = min(len(keywords) * 3, 15)
        score += keyword_bonus
        if keyword_bonus > 0:
            rationale_parts.append(f"技术关键词+{keyword_bonus}")
        
        score = max(0, min(100, score))
        rationale = " | ".join(rationale_parts) if rationale_parts else "规则评分"
        
        return score, rationale
    
    def score_news(self, news: Dict) -> Dict:
        """
        对单条新闻进行评分
        
        Args:
            news: 新闻字典
        
        Returns:
            包含评分信息的新闻字典
        """
        score, rationale = self._score_with_llm(news)
        
        category = self._classify_by_score(score)
        
        return {
            **news,
            'score': score,
            'rationale': rationale,
            'category': category,
            'scored_at': datetime.now().isoformat()
        }
    
    def _classify_by_score(self, score: int) -> str:
        """根据分数分类"""
        if score >= self.AUTO_PUSH_THRESHOLD:
            return 'auto_push'
        elif self.GRAY_ZONE_MIN <= score < self.GRAY_ZONE_MAX:
            return 'gray_zone'
        else:
            return 'filtered'
    
    def score_batch(self, news_list: List[Dict]) -> Dict[str, List[Dict]]:
        """
        批量评分并分类
        
        Args:
            news_list: 新闻列表
        
        Returns:
            分类后的新闻字典
        """
        auto_push = []
        gray_zone = []
        filtered = []
        
        for news in news_list:
            scored_news = self.score_news(news)
            category = scored_news['category']
            
            if category == 'auto_push':
                auto_push.append(scored_news)
            elif category == 'gray_zone':
                gray_zone.append(scored_news)
            else:
                filtered.append(scored_news)
        
        return {
            'auto_push': auto_push,
            'gray_zone': gray_zone,
            'filtered': filtered
        }
    
    def add_feedback(self, news_id: str, original_score: int, manual_score: int, notes: str = ""):
        """
        添加人工反馈，用于后续迭代
        
        Args:
            news_id: 新闻ID（可用URL）
            original_score: 原始评分
            manual_score: 人工评分
            notes: 备注
        """
        self.feedback_data.append({
            'news_id': news_id,
            'original_score': original_score,
            'manual_score': manual_score,
            'notes': notes,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_few_shot_example(self, news: Dict, score: int, rationale: str):
        """
        添加新的 Few-shot 示例
        
        Args:
            news: 新闻内容
            score: 评分
            rationale: 理由
        """
        self.few_shot_examples.append({
            'news': news,
            'expected_score': score,
            'rationale': rationale
        })
    
    def analyze_feedback(self) -> Dict:
        """分析反馈数据，找出优化方向"""
        if not self.feedback_data:
            return {'status': 'no_feedback'}
        
        total_diff = 0
        over_estimates = 0
        under_estimates = 0
        
        for fb in self.feedback_data:
            diff = fb['manual_score'] - fb['original_score']
            total_diff += diff
            if diff > 10:
                under_estimates += 1
            elif diff < -10:
                over_estimates += 1
        
        avg_diff = total_diff / len(self.feedback_data)
        
        return {
            'total_feedback': len(self.feedback_data),
            'avg_score_diff': avg_diff,
            'over_estimates': over_estimates,
            'under_estimates': under_estimates,
            'recommendation': self._generate_recommendation(avg_diff, over_estimates, under_estimates)
        }
    
    def _generate_recommendation(self, avg_diff: float, over: int, under: int) -> str:
        """生成优化建议"""
        if abs(avg_diff) < 5:
            return "评分系统表现良好，继续保持"
        elif avg_diff > 10:
            return "建议：模型评分偏保守，可增加正向Few-shot示例"
        elif avg_diff < -10:
            return "建议：模型评分偏宽松，可增加负向Few-shot示例"
        elif over > under:
            return "建议：存在较多高估，检查信源权重或提示词"
        elif under > over:
            return "建议：存在较多低估，扩充技术关键词库"
        return "持续收集更多反馈数据"
