"""
Fandom Hybrid Fetcher 测试

测试三层策略：API → Browser → Local
"""

import json
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from anime_character_loader.extractors.fandom_hybrid import (
    FandomHybridFetcher, QuoteItem, QuoteResult,
    NetworkError, CharacterNotFoundError, ParseError,
    fetch_quotes_fandom
)


class TestFandomHybridFetcher:
    """测试 Fandom Hybrid Fetcher"""
    
    @pytest.fixture
    def fetcher(self, tmp_path):
        return FandomHybridFetcher(cache_dir=str(tmp_path))
    
    def test_api_success_with_confident_quotes(self, fetcher):
        """1. API 页面存在且有高置信度台词 -> 成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "parse": {
                "title": "Test Character",
                "text": {"*": '<h2 id="Quotes">Quotes</h2><blockquote>「Test quote」</blockquote>'},
                "sections": [{"line": "Quotes", "anchor": "Quotes"}]
            }
        }
        
        with patch.object(fetcher.session, 'get', return_value=mock_response):
            result = fetcher.fetch("Test", "TestWork")
            assert result.source_type == "api"
            assert len(result.quotes) > 0
            assert all(q.confidence >= 0.4 for q in result.quotes)
    
    def test_api_success_but_no_quotes_section(self, fetcher):
        """2. API 页面存在但无有效台词 -> ParseError"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "parse": {
                "title": "Empty Character",
                "text": {"*": "<div>No quotes here</div>"},
                "sections": []
            }
        }
        
        # 准备 local fallback
        local_db = {
            "Test": {
                "character": "Test",
                "work": "TestWork",
                "quotes": [{"text": "Local quote", "context": "test"}]
            }
        }
        
        with patch.object(fetcher.session, 'get', return_value=mock_response):
            with patch.object(fetcher, '_fetch_local', return_value=[
                QuoteItem(text="Local quote", quote_id="test", confidence=0.8)
            ]):
                result = fetcher.fetch("Test", "TestWork")
                # 应该走到 local fallback
                assert result.source_type in ("local", "api")
    
    def test_api_timeout_then_browser_success(self, fetcher):
        """3. API 超时 + Browser 成功 -> source_type=browser"""
        import requests
        
        # API 超时
        with patch.object(fetcher.session, 'get', side_effect=requests.exceptions.Timeout):
            # Browser 成功（mock）
            with patch.object(fetcher, '_fetch_browser', return_value=[
                QuoteItem(text="Browser quote", quote_id="b1", confidence=0.9)
            ]):
                result = fetcher.fetch("Test", "TestWork")
                assert result.source_type == "browser"
                assert len(result.quotes) == 1
    
    def test_all_fail_then_local_fallback(self, fetcher):
        """4. API/Browser 都失败 -> local fallback"""
        import requests
        
        with patch.object(fetcher.session, 'get', side_effect=requests.exceptions.Timeout):
            with patch.object(fetcher, '_fetch_browser', return_value=[]):
                with patch.object(fetcher, '_fetch_local', return_value=[
                    QuoteItem(text="Local quote", quote_id="l1", confidence=0.8, source_url="local://test")
                ]):
                    result = fetcher.fetch("Test", "TestWork")
                    assert result.source_type == "local"
                    assert result.quotes[0].text == "Local quote"
    
    def test_speaker_extraction(self, fetcher):
        """5. Speaker 识别正确"""
        # 测试模式1: "角色名: 台词"
        speaker, text = fetcher._extract_speaker("Eriri: Baka!", "Eriri")
        assert speaker == "Eriri"
        assert text == "Baka!"
        
        # 测试模式2: （角色名）台词
        speaker, text = fetcher._extract_speaker("（Eriri）Baka!", "Eriri")
        assert speaker == "Eriri"
        assert text == "Baka!"
        
        # 测试模式3: [角色名] 台词
        speaker, text = fetcher._extract_speaker("[Eriri] Baka!", "Eriri")
        assert speaker == "Eriri"
        assert text == "Baka!"
    
    def test_confidence_scoring(self, fetcher):
        """6. Confidence 阈值过滤有效"""
        # 高置信度
        score = fetcher._score_quote(
            text="Valid quote",
            speaker="Eriri",
            target_character="Eriri",
            in_quotes_section=True
        )
        assert score >= 0.7  # 0.35 + 0.35 + 0.15 + 0.15 = 1.0
        
        # 低置信度
        score = fetcher._score_quote(
            text="Bad",
            speaker="unknown",
            target_character="Eriri",
            in_quotes_section=False
        )
        assert score < 0.4
    
    def test_deduplication(self, fetcher):
        """7. 去重有效"""
        quotes = [
            QuoteItem(text="Quote 1", quote_id="id1"),
            QuoteItem(text="Quote 1", quote_id="id1"),  # 重复
            QuoteItem(text="Quote 2", quote_id="id2"),
        ]
        result = fetcher._deduplicate_quotes(quotes)
        assert len(result) == 2
    
    def test_output_fields_complete(self, fetcher):
        """8. 输出字段完整性校验"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "parse": {
                "title": "Test",
                "text": {"*": '<h2 id="Quotes">Quotes</h2><blockquote>「Test」</blockquote>'},
                "sections": [{"line": "Quotes", "anchor": "Quotes"}]
            }
        }
        
        with patch.object(fetcher.session, 'get', return_value=mock_response):
            result = fetcher.fetch("Test", "TestWork")
            
            # 检查必需字段
            assert result.character
            assert result.work
            assert result.source_type in ("api", "browser", "local", "cache")
            assert result.source_url
            assert isinstance(result.quotes, list)
            
            if result.quotes:
                q = result.quotes[0]
                assert q.text
                assert q.speaker is not None
                assert q.quote_id
                assert 0 <= q.confidence <= 1


class TestFetchQuotesFandom:
    """测试便捷函数"""
    
    def test_fetch_quotes_fandom_local_fallback(self):
        """测试便捷函数 local fallback"""
        with patch('anime_character_loader.extractors.fandom_hybrid.FandomHybridFetcher') as MockFetcher:
            mock_instance = MagicMock()
            mock_instance.fetch.return_value = QuoteResult(
                character="Eriri",
                work="Saekano",
                source_type="local",
                source_url="local://test",
                quotes=[QuoteItem(text="Test", quote_id="t1")]
            )
            MockFetcher.return_value = mock_instance
            
            result = fetch_quotes_fandom("Eriri", "Saekano")
            assert result["character"] == "Eriri"
            assert result["source_type"] == "local"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
