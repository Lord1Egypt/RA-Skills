"""
Wikiquote Fetcher 测试用例 (v2 - 符合 12 条标准)

测试覆盖:
1. API 200 + valid parse（成功）
2. API 200 但无 parse（NotFound）
3. API timeout/retry（NetworkError）
4. HTML 有 quotes section（提取成功）
5. HTML 无 quotes section（ParseError）
6. fallback 到 local db（成功）
"""

import json
import os
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

from anime_character_loader.extractors.wikiquote import (
    Quote, QuoteCollection, CacheManager, WikiquoteFetcher,
    WikiquoteError, CharacterNotFoundError, NetworkError, ParseError
)

class TestWikiquoteFetcherStandard:
    """符合 12 条标准的测试类"""
    
    @pytest.fixture
    def fetcher(self, tmp_path):
        return WikiquoteFetcher(cache_dir=str(tmp_path))

    def test_api_200_valid_parse_success(self, fetcher):
        """测试 API 200 + 有效解析 (成功)"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "parse": {
                "title": "Megumi Katou",
                "text": {"*": "<h2>Quotes</h2><blockquote>Hello, world!</blockquote>"}
            }
        }
        
        with patch.object(requests.Session, 'get', return_value=mock_response):
            result = fetcher.fetch("加藤惠", use_cache=False)
            assert result.character == "Megumi Katou"
            assert len(result.quotes) > 0
            assert result.quotes[0].text == "Hello, world!"
            assert result.source_type == "api"

    def test_api_200_no_parse_notfound(self, fetcher):
        """测试 API 200 但无 parse (NotFound)"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": {"code": "missingtitle", "info": "The page you specified doesn't exist."}
        }
        
        # 确保 local db 也不包含此人，从而抛出异常
        with patch("anime_character_loader.extractors.wikiquote.WikiquoteFetcher._load_from_local_db", return_value=None):
            with patch.object(requests.Session, 'get', return_value=mock_response):
                with pytest.raises(CharacterNotFoundError):
                    fetcher.fetch("UnknownCharacter", use_cache=False)

    def test_api_timeout_network_error(self, fetcher):
        """测试 API 超时 (NetworkError)"""
        with patch("anime_character_loader.extractors.wikiquote.WikiquoteFetcher._load_from_local_db", return_value=None):
            with patch.object(requests.Session, 'get', side_effect=requests.exceptions.Timeout):
                with pytest.raises(NetworkError):
                    fetcher.fetch("加藤惠", use_cache=False)

    def test_html_has_quotes_section_success(self, fetcher):
        """测试 HTML 有 quotes section (提取成功)"""
        # 注意: 使用 BeautifulSoup 的 next_siblings 时，空白字符会被视为 NavigableString
        html = "<h2>台词</h2><blockquote>这是台词</blockquote>"
        parse_data = {
            "title": "Test",
            "text": {"*": html}
        }
        quotes = fetcher._extract_quotes(parse_data, "Test")
        assert len(quotes) == 1
        assert quotes[0].text == "这是台词"
        assert quotes[0].section == "台词"
        assert quotes[0].quote_id is not None

    def test_html_no_quotes_section_parse_error(self, fetcher):
        """测试 HTML 无 quotes section (ParseError)"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "parse": {
                "title": "EmptyPage",
                "text": {"*": "<div>仅有介绍，无台词</div>"}
            }
        }
        
        with patch("anime_character_loader.extractors.wikiquote.WikiquoteFetcher._load_from_local_db", return_value=None):
            with patch.object(requests.Session, 'get', return_value=mock_response):
                # API 正常但解析不出台词
                with pytest.raises(ParseError):
                    fetcher.fetch("EmptyPage", use_cache=False)

    def test_fallback_to_local_db_success(self, fetcher, tmp_path):
        """测试 API 失败时 fallback 到本地数据库 (成功)"""
        # 模拟 API 404
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": {"code": "missingtitle"}}
        
        # 准备本地数据库文件
        local_db_dir = tmp_path / "data"
        local_db_dir.mkdir()
        local_db_file = local_db_dir / "quotes_database.json"
        local_db_content = {
            "MockCharacter": {
                "character": "MockCharacter",
                "quotes": [{"text": "本地台词", "context": "local"}]
            }
        }
        local_db_file.write_text(json.dumps(local_db_content), encoding="utf-8")
        
        # 修改 fetcher 使其能找到这个模拟的 data 目录
        with patch("anime_character_loader.extractors.wikiquote.Path.cwd", return_value=tmp_path):
            with patch.object(requests.Session, 'get', return_value=mock_response):
                result = fetcher.fetch("MockCharacter", use_cache=False)
                assert result.source_type == "local"
                assert result.quotes[0].text == "本地台词"

class TestDataStructure:
    """测试数据结构是否包含要求的字段"""
    
    def test_quote_fields(self):
        q = Quote(text="T", section="S", quote_id="ID", source_url="URL")
        assert q.section == "S"
        assert q.quote_id == "ID"
        assert q.source_url == "URL"

    def test_collection_source_type(self):
        c = QuoteCollection(character="C", source_type="api")
        assert c.source_type == "api"
        d = c.to_dict()
        assert d["source_type"] == "api"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
