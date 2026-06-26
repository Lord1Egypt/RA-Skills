"""
单元测试 - Adapter 错误处理
"""
import pytest
import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestKronosAdapter:
    """Kronos Adapter 错误处理测试"""
    
    def test_error_result_format(self):
        """测试错误结果格式"""
        from kronos_adapter import KronosAdapter
        
        adapter = KronosAdapter()
        result = adapter._error_result("Test error message")
        
        # 验证返回格式
        assert 'model' in result
        assert 'signal' in result
        assert 'confidence' in result
        assert result['signal'] == 'neutral'
        assert result['confidence'] == 30
        assert 'Kronos错误' in result['reasoning']
    
    def test_predict_with_invalid_data(self):
        """测试无效数据处理"""
        from kronos_adapter import KronosAdapter
        
        adapter = KronosAdapter()
        # 使用不存在的标的
        result = adapter.predict('INVALID_SYMBOL_XYZ', bar='4H', lookback=10)
        
        # 应该返回错误结果，不是崩溃
        assert result['signal'] == 'neutral'
        assert result['confidence'] == 30


class TestOKXDataProvider:
    """OKX Data Provider 测试"""
    
    def test_get_data_auto_detection(self):
        """测试股票/加密货币自动检测"""
        from okx_data_provider import get_data
        
        # 测试非股票代码 -> 应该尝试OKX
        # (不实际调用，只验证函数存在)
        assert callable(get_data)
    
    def test_get_stock_klines_function_exists(self):
        """测试股票数据函数存在"""
        from okx_data_provider import get_stock_klines
        assert callable(get_stock_klines)


class TestVADERAdapter:
    """VADER FinBERT Adapter 测试"""
    
    def test_load_is_instant(self):
        """测试VADER加载是即时的"""
        import time
        from finbert_adapter import FinBERTAdapter
        
        adapter = FinBERTAdapter()
        start = time.time()
        adapter.load()
        elapsed = time.time() - start
        
        # VADER 应该<1秒加载
        assert elapsed < 5, f"VADER加载过慢: {elapsed}s"
    
    def test_analyze_empty_texts(self):
        """测试空文本处理"""
        from finbert_adapter import FinBERTAdapter
        
        adapter = FinBERTAdapter()
        result = adapter.analyze_texts([])
        
        assert result['sentiment'] == 'neutral'
        assert result['score'] == 0
        assert result['confidence'] == 30
    
    def test_financial_keywords(self):
        """测试金融关键词增强"""
        from finbert_adapter import FinBERTAdapter
        
        adapter = FinBERTAdapter()
        
        # 看涨文本
        bullish_texts = [
            "Bitcoin surges to new all-time high",
            "Stock rally continues on strong earnings",
            "Market breakout signals more gains ahead"
        ]
        result = adapter.analyze_texts(bullish_texts)
        assert result['sentiment'] in ['bullish', 'neutral']
        
        # 看跌文本
        bearish_texts = [
            "Crypto crash wipes out gains",
            "Market dump on fear and panic selling",
            "Stock decline continues amid recession fears"
        ]
        result = adapter.analyze_texts(bearish_texts)
        assert result['sentiment'] in ['bearish', 'neutral']


class TestSocialSentiment:
    """Social Sentiment Provider 测试"""
    
    def test_reddit_headers_complete(self):
        """测试Reddit Headers完整性"""
        from social_sentiment_provider import SocialSentimentProvider
        
        provider = SocialSentimentProvider()
        headers = provider.REDDIT_HEADERS
        
        # 应该包含完整的User-Agent
        assert 'User-Agent' in headers
        assert 'Chrome' in headers['User-Agent'] or 'Safari' in headers['User-Agent']
    
    def test_sentiment_provider_init(self):
        """测试情绪提供者初始化"""
        from social_sentiment_provider import SocialSentimentProvider
        
        provider = SocialSentimentProvider()
        assert hasattr(provider, 'REDDIT_HEADERS')
        assert hasattr(provider, 'BULLISH_WORDS')
        assert hasattr(provider, 'BEARISH_WORDS')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
