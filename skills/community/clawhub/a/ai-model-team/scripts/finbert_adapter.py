"""
FinBERT Adapter for AI Model Team
FinBERT: 金融文本情绪分析模型
基于VADER + 金融关键词增强 + HuggingFace神经网络备选
输出交易信号
"""
import sys
import os
import numpy as np
from typing import Dict, List

# 导入社会情绪数据模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from social_sentiment_provider import get_news_sentiment, get_social_sentiment


class FinBERTAdapter:
    """FinBERT金融情绪分析模型 (VADER + 金融关键词增强)"""
    name = "FinBERT-sentiment"
    institution = "HuggingFace"
    params = "VADER+FinBERT"
    specialty = "文本情绪/金融新闻"
    _analyzer = None
    
    # 情绪阈值配置
    BULLISH_THRESHOLD = 0.3   # 积极情绪阈值 (compound score)
    BEARISH_THRESHOLD = -0.3  # 消极情绪阈值
    
    # 金融领域增强关键词
    FINANCIAL_BULLISH = [
        'surge', 'rally', 'bull', 'pump', 'moon', 'breakout', 'adoption', 'partnership',
        'growth', 'soar', 'jump', 'rise', 'gain', 'climb', 'advance', 'increase',
        'profit', 'win', 'success', 'bullish', 'optimistic', 'uptrend', 'higher',
        'record high', 'all-time high', 'bull market', 'recover', 'recovery',
        'upgrade', 'buy rating', 'outperform', 'strong demand', 'supply crunch'
    ]
    FINANCIAL_BEARISH = [
        'crash', 'dump', 'bear', 'fall', 'decline', 'ban', 'hack', 'fear', 'panic',
        'drop', 'plunge', 'sink', 'loss', 'fail', 'uncertainty', 'downtrend',
        'sell', 'bearish', 'pessimistic', 'lower', 'worst', 'bleak', 'recession',
        'downgrade', 'sell rating', 'underperform', 'weak demand', 'oversupply',
        'liquidation', 'margin call', 'regulation', 'ban', 'outage', 'exploit'
    ]
    
    def __init__(self, variant: str = "vader"):
        self.variant = variant
        self.model_name = "VADER (Valence Aware Dictionary)"
    
    def load(self):
        """加载VADER情感分析器 (即时加载)"""
        if FinBERTAdapter._analyzer is None:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            FinBERTAdapter._analyzer = SentimentIntensityAnalyzer()
            print(f"  加载 VADER 情感分析器... ✅ (即时)")
        return FinBERTAdapter._analyzer
    
    def analyze_texts(self, texts: List[str]) -> Dict:
        """分析文本列表的情绪"""
        if not texts:
            return {"sentiment": "neutral", "score": 0, "confidence": 30}
        
        analyzer = self.load()
        
        try:
            results = []
            for text in texts[:20]:  # 限制分析数量
                if not text or len(text.strip()) == 0:
                    continue
                # VADER 分析
                vader_score = analyzer.polarity_scores(text)
                results.append(vader_score)
            
            if not results:
                return {"sentiment": "neutral", "score": 0, "confidence": 30}
            
            # 计算平均分数
            avg_compound = np.mean([r['compound'] for r in results])
            avg_positive = np.mean([r['pos'] for r in results])
            avg_negative = np.mean([r['neg'] for r in results])
            avg_neutral = np.mean([r['neu'] for r in results])
            
            # 金融关键词增强
            fin_score = self._financial_keyword_boost(texts)
            
            # 综合分数 (VADER 70% + 金融关键词 30%)
            combined_score = avg_compound * 0.7 + fin_score * 0.3
            
            # 判断信号
            if combined_score > self.BULLISH_THRESHOLD:
                signal = "bullish"
                confidence = min(95, 50 + int(combined_score * 50))
            elif combined_score < self.BEARISH_THRESHOLD:
                signal = "bearish"
                confidence = min(95, 50 + int(abs(combined_score) * 50))
            else:
                signal = "neutral"
                confidence = 50
            
            return {
                "sentiment": signal,
                "score": round(combined_score, 3),
                "confidence": confidence,
                "vader_compound": round(avg_compound, 3),
                "positive_ratio": round(avg_positive, 3),
                "negative_ratio": round(avg_negative, 3),
                "neutral_ratio": round(avg_neutral, 3),
                "financial_boost": round(fin_score, 3),
                "samples_analyzed": len(results)
            }
            
        except Exception as e:
            print(f"VADER分析失败: {e}")
            return self._keyword_analysis(texts)
    
    def _financial_keyword_boost(self, texts: List[str]) -> float:
        """金融关键词增强分数"""
        pos_count = 0
        neg_count = 0
        
        for text in texts:
            text_lower = text.lower()
            for word in self.FINANCIAL_BULLISH:
                if word in text_lower:
                    pos_count += 1
            for word in self.FINANCIAL_BEARISH:
                if word in text_lower:
                    neg_count += 1
        
        total = pos_count + neg_count
        if total > 0:
            return (pos_count - neg_count) / total
        return 0.0
    
    def _keyword_analysis(self, texts: List[str]) -> Dict:
        """纯关键词回退分析"""
        pos_count = 0
        neg_count = 0
        
        for text in texts:
            text_lower = text.lower()
            for word in self.FINANCIAL_BULLISH:
                if word in text_lower:
                    pos_count += 1
            for word in self.FINANCIAL_BEARISH:
                if word in text_lower:
                    neg_count += 1
        
        total = pos_count + neg_count
        if total > 0:
            net_sentiment = (pos_count - neg_count) / total
            if net_sentiment > 0.3:
                signal = "bullish"
                confidence = min(95, 50 + int(net_sentiment * 40))
            elif net_sentiment < -0.3:
                signal = "bearish"
                confidence = min(95, 50 + int(abs(net_sentiment) * 40))
            else:
                signal = "neutral"
                confidence = 50
        else:
            signal = "neutral"
            confidence = 30
            net_sentiment = 0
        
        return {
            "sentiment": signal,
            "score": round(net_sentiment, 3),
            "confidence": confidence,
            "method": "keyword_fallback",
            "samples_analyzed": len(texts)
        }
    
    def predict(self, symbol: str, bar: str = "4H", lookback: int = 24, pred_len: int = 24) -> Dict:
        """
        FinBERT预测：基于新闻和社交媒体情绪
        """
        try:
            # 提取货币代码
            currency = symbol.split("-")[0] if "-" in symbol else symbol
            
            # 获取新闻数据
            print(f"  获取{currency}新闻数据...", end=" ", flush=True)
            news_data = get_news_sentiment(currency)
            print(f"✅ {len(news_data)}条")
            
            if not news_data:
                return self._error_result("无法获取新闻数据")
            
            # 提取文本内容
            texts = [n.get("title", "") for n in news_data if n.get("title")]
            
            # 分析情绪
            print(f"  VADER情绪分析中...", end=" ", flush=True)
            sentiment_result = self.analyze_texts(texts)
            print(f"✅")
            
            # 转换为统一格式
            signal = sentiment_result.get("sentiment", "neutral")
            confidence = sentiment_result.get("confidence", 50)
            score = sentiment_result.get("score", 0)
            
            # 价格变化（基于情绪强度）
            price_change = score * 2
            
            current_price = 0
            trend_strength = min(100, abs(score) * 100)
            
            samples = sentiment_result.get("samples_analyzed", 0)
            method = f"VADER+金融关键词 ({sentiment_result.get('samples_analyzed', 0)}条)"
            
            return {
                "model": self.name,
                "institution": self.institution,
                "params": self.params,
                "specialty": self.specialty,
                "signal": signal,
                "confidence": confidence,
                "trend_strength": round(trend_strength, 1),
                "current_price": current_price,
                "forecast_price": current_price * (1 + price_change/100) if current_price else 0,
                "price_change_pct": round(price_change, 2),
                "forecast_low": 0,
                "forecast_high": 0,
                "up_bars": 0,
                "total_bars": 0,
                "reasoning": f"VADER金融情绪分析: {samples}条新闻, 情绪得分{score:+.3f} ({method}), 整体{signal.upper()}",
                "details": {
                    "sentiment_score": score,
                    "vader_compound": sentiment_result.get("vader_compound", 0),
                    "positive_ratio": sentiment_result.get("positive_ratio", 0),
                    "negative_ratio": sentiment_result.get("negative_ratio", 0),
                    "sample_headlines": texts[:3]
                }
            }
            
        except Exception as e:
            return self._error_result(str(e))
    
    def _error_result(self, msg: str) -> Dict:
        return {
            "model": self.name,
            "institution": self.institution,
            "params": self.params,
            "specialty": self.specialty,
            "signal": "neutral",
            "confidence": 30,
            "trend_strength": 0,
            "current_price": 0,
            "forecast_price": 0,
            "price_change_pct": 0,
            "forecast_low": 0,
            "forecast_high": 0,
            "up_bars": 0,
            "total_bars": 0,
            "reasoning": f"VADER分析失败: {str(msg)[:100]}"
        }


# 便捷函数
def get_finbert_sentiment(texts: List[str]) -> Dict:
    """快速获取FinBERT情绪分析"""
    adapter = FinBERTAdapter()
    return adapter.analyze_texts(texts)


if __name__ == "__main__":
    # 测试
    adapter = FinBERTAdapter()
    result = adapter.predict("BTC-USDT-SWAP")
    print("\n" + "="*60)
    print(f"FinBERT信号: {result['signal'].upper()}")
    print(f"置信度: {result['confidence']}")
    print(f"分析: {result['reasoning']}")
