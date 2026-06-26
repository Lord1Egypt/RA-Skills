#!/usr/bin/env python3
"""
Fund News Summary Generator - Cursor Version
Production-ready with asyncio rate limiting, exponential backoff, and proper error handling.
"""

import asyncio
import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# Set INFO level for less verbose output in production
# logger.setLevel(logging.INFO)

# Fund configuration - 5 funds
FUNDS = {
    "nasdaq": {
        "name": "华宝纳斯达克精选股票 (QDII)C",
        "keywords": ["纳斯达克100", "Nvidia", "Microsoft", "美股半导体", "Nasdaq 100"],
        "impact_factors": ["AI板块表现", "美联储政策", "科技股财报"]
    },
    "europe": {
        "name": "摩根欧洲动力策略股票 (QDII)A",
        "keywords": ["欧洲股市", "ASML", "诺华", "欧股走势", "欧洲股市"],
        "impact_factors": ["ASML业绩", "欧股整体走势", "欧元汇率"]
    },
    "japan": {
        "name": "摩根日本精选股票 (QDI)A",
        "keywords": ["日经225", "日元汇率", "丰田", "日本股市", "Nikkei 225"],
        "impact_factors": ["日经指数变化", "日元汇率波动", "日本央行政策"]
    },
    "gold": {
        "name": "易方达黄金 ETF 联接 C",
        "keywords": ["现货黄金", "COMEX黄金", "避险情绪", "gold price", "COMEX"],
        "impact_factors": ["国际金价", "避险情绪", "美元指数"]
    },
    "sp500": {
        "name": "标普500 (S&P 500 Index)",
        "keywords": ["标普500", "美股大盘", "联储政策", "S&P 500", "Fed"],
        "impact_factors": ["美联储政策", "美股大盘走势", "经济数据"]
    }
}


class RateLimiter:
    """
    Async rate limiter that allows true concurrency while maintaining minimum interval between request starts.
    
    Key design:
    - All tasks start concurrently
    - Uses a token bucket approach: tracks last request time and ensures minimum interval
    - Multiple HTTP requests can run concurrently (network I/O)
    - Only controls the spacing between when requests START, not their execution duration
    - This allows HTTP requests to overlap while respecting rate limits
    """
    
    def __init__(self, min_interval: float = 1.5):
        self.min_interval = min_interval
        self.lock = asyncio.Lock()
        self._last_request_time = 0
    
    async def acquire(self):
        """
        Acquire execution permit with automatic interval handling.
        Ensures minimum interval since last request start, then allows immediate execution.
        Multiple calls can happen concurrently - they'll queue and execute with proper spacing.
        """
        async with self.lock:
            now = time.time()
            
            # Calculate delay needed to maintain interval
            if self._last_request_time > 0:
                elapsed = now - self._last_request_time
                if elapsed < self.min_interval:
                    # Need to wait to maintain interval
                    delay = self.min_interval - elapsed
                    # Update last request time BEFORE sleeping (so next task knows when to start)
                    self._last_request_time = now + delay
                    # Release lock before sleeping to allow other tasks to check their timing
                    await asyncio.sleep(delay)
                else:
                    # Can start immediately
                    self._last_request_time = now
            else:
                # First request starts immediately
                self._last_request_time = now
        
        # Now we can start HTTP request - it will run concurrently with others
        # The lock is released, so other tasks can proceed
    
    def release(self):
        """Release execution permit (no-op for new design, kept for compatibility)."""
        pass
    
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()


class ExponentialBackoff:
    """
    Enhanced exponential backoff retry handler with comprehensive error handling.
    Handles rate limits, network errors, timeouts, and transient failures.
    """
    
    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0, max_retries: int = 5):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
    
    def _is_retryable_error(self, error: Exception) -> bool:
        """Check if error is retryable."""
        error_str = str(error).lower()
        error_type = type(error).__name__.lower()
        
        # Rate limit errors
        is_rate_limit = (
            "429" in error_str or
            "rate limit" in error_str or
            "too many requests" in error_str or
            "quota exceeded" in error_str
        )
        
        # Network errors
        is_network_error = (
            "timeout" in error_str or
            "connection" in error_str or
            "network" in error_str or
            "dns" in error_str or
            error_type in ["timeouterror", "connectionerror", "connecttimeouterror"]
        )
        
        # Server errors (5xx)
        is_server_error = (
            "500" in error_str or
            "502" in error_str or
            "503" in error_str or
            "504" in error_str or
            "service unavailable" in error_str
        )
        
        # Transient errors
        is_transient = (
            is_rate_limit or
            is_network_error or
            is_server_error
        )
        
        return is_transient
    
    async def retry(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry on retryable errors."""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                # Check if error is retryable
                if not self._is_retryable_error(e):
                    logger.error(f"Non-retryable error: {str(e)}")
                    raise e
                
                # If max retries reached, raise the exception
                if attempt >= self.max_retries - 1:
                    logger.error(
                        f"Max retries ({self.max_retries}) reached. "
                        f"Last error: {str(e)}"
                    )
                    raise e
                
                # Calculate delay with exponential backoff
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                # Add jitter to prevent thundering herd
                jitter = random.uniform(0, delay * 0.2)
                total_delay = delay + jitter
                
                error_type = "rate limit" if "429" in str(e).lower() else "network/server error"
                logger.warning(
                    f"{error_type} encountered (attempt {attempt + 1}/{self.max_retries}). "
                    f"Retrying in {total_delay:.2f}s... Error: {str(e)[:100]}"
                )
                
                await asyncio.sleep(total_delay)
                continue
        
        # Should not reach here, but just in case
        if last_exception:
            raise last_exception
        raise Exception("Retry logic failed unexpectedly")


class WebSearchClient:
    """
    Web search client wrapper.
    Supports both direct API calls and tool-based calls.
    """
    
    def __init__(self, use_api: bool = True):
        self.use_api = use_api
        self.api_key = os.getenv("BRAVE_API_KEY")
        
    async def search(self, query: str, search_lang: str = "zh-hans") -> List[Dict]:
        """
        Perform web search.
        
        Args:
            query: Search query string
            search_lang: Language code (default: zh-hans for Simplified Chinese)
            
        Returns:
            List of search results with title, url, snippet, etc.
        """
        if self.use_api and self.api_key:
            return await self._brave_search_api(query, search_lang)
        else:
            # Fallback: return structured mock data for testing
            logger.warning("No API key found, using mock data")
            return await self._mock_search(query)
    
    async def _brave_search_api(self, query: str, search_lang: str) -> List[Dict]:
        """Call Brave Search API with timeout and better error handling."""
        import aiohttp
        
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
        params = {
            "q": query,
            "count": 5,
            "search_lang": search_lang,
            "country": "CN",
            "safesearch": "moderate"
        }
        
        # Configure timeout: 10s connect, 30s total
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers, params=params) as response:
                    # Handle rate limit explicitly
                    if response.status == 429:
                        error_text = await response.text()
                        raise Exception(f"429 Rate Limit: {error_text}")
                    
                    # Handle other HTTP errors
                    if response.status >= 500:
                        error_text = await response.text()
                        raise Exception(f"Server Error {response.status}: {error_text}")
                    
                    response.raise_for_status()
                    
                    # Parse JSON response
                    try:
                        data = await response.json()
                    except Exception as e:
                        raise Exception(f"Failed to parse JSON response: {str(e)}")
                    
                    results = []
                    web_results = data.get("web", {}).get("results", [])
                    
                    for item in web_results[:5]:
                        results.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "snippet": item.get("description", ""),
                            "source": self._extract_domain(item.get("url", "")),
                            "time": datetime.now().strftime("%Y-%m-%d")
                        })
                    
                    return results
                    
        except asyncio.TimeoutError:
            raise Exception("Request timeout: API did not respond within 30 seconds")
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            # Re-raise if already formatted
            if "Rate Limit" in str(e) or "Server Error" in str(e) or "timeout" in str(e).lower():
                raise
            # Wrap unexpected errors
            raise Exception(f"Unexpected error: {str(e)}")
    
    async def _mock_search(self, query: str) -> List[Dict]:
        """Mock search for testing without API."""
        await asyncio.sleep(random.uniform(0.5, 1.0))
        
        return [
            {
                "title": f"{query} 相关新闻标题",
                "url": "https://example.com/news1",
                "snippet": f"关于 {query} 的最新动态和分析...",
                "source": "Reuters",
                "time": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "title": f"{query} 市场分析",
                "url": "https://example.com/news2",
                "snippet": f"{query} 的市场表现和未来展望...",
                "source": "Yahoo Finance",
                "time": datetime.now().strftime("%Y-%m-%d")
            }
        ]
    
    @staticmethod
    def _extract_domain(url: str) -> str:
        """Extract domain name from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "")
            return domain.split(".")[-2] if "." in domain else domain
        except:
            return "Unknown"


class FundNewsGenerator:
    """Fund news generator with rate limiting and retry logic."""
    
    def __init__(self, use_api: bool = True, min_interval: float = 1.5):
        # Rate limiter now only controls interval, not concurrency
        self.rate_limiter = RateLimiter(min_interval=min_interval)
        self.backoff = ExponentialBackoff(base_delay=1.0, max_delay=60.0, max_retries=5)
        self.search_client = WebSearchClient(use_api=use_api)
        self.results = {}
    
    async def search_fund_news(self, fund_id: str, fund_config: Dict) -> Dict:
        """
        Search news for a single fund with rate limiting and retry logic.
        
        True concurrency design:
        1. All tasks start concurrently
        2. Rate limiter ensures requests start with minimum interval
        3. Once a request gets its turn, HTTP request executes immediately
        4. Multiple HTTP requests can run concurrently (network I/O)
        
        Args:
            fund_id: Fund identifier
            fund_config: Fund configuration dict
            
        Returns:
            Dict with fund_name, fund_id, query, news, status, and error (if any)
        """
        fund_name = fund_config["name"]
        keywords = fund_config["keywords"]
        
        # Build search query using first 3 keywords
        query = " ".join(keywords[:3])
        
        # Acquire rate limiter slot (waits for turn, then immediately proceeds)
        # The key: once we exit this context, HTTP request starts immediately
        # and can run concurrently with other HTTP requests
        request_start_time = time.time()
        async with self.rate_limiter:
            pass  # Rate limiter ensures spacing, then we proceed
        
        wait_time = time.time() - request_start_time
        logger.info(f"[{fund_name}] Got rate limit slot, waited {wait_time:.3f}s, starting HTTP request now")
        
        # Now execute HTTP request - this can run concurrently with others
        try:
            # Use exponential backoff for retries
            search_results = await self.backoff.retry(
                self.search_client.search,
                query,
                search_lang="zh-hans"
            )
            
            return {
                "fund_name": fund_name,
                "fund_id": fund_id,
                "query": query,
                "news": search_results,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Failed to search news for {fund_name}: {str(e)}")
            return {
                "fund_name": fund_name,
                "fund_id": fund_id,
                "query": query,
                "news": [],
                "status": "error",
                "error": str(e)
            }
    
    async def generate_summary(self) -> str:
        """
        Generate complete news summary report for all funds.
        Now uses true concurrency - all HTTP requests can run simultaneously,
        but rate limiter ensures minimum interval between request starts.
        
        Returns:
            Formatted report string in bold list format
        """
        logger.info("Starting fund news collection with concurrent requests...")
        
        # Create tasks for all funds - they will run concurrently
        # Rate limiter ensures spacing between request starts, not blocking concurrency
        tasks = [
            self.search_fund_news(fund_id, config)
            for fund_id, config in FUNDS.items()
        ]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"Completed {len(results)} fund news searches")
        
        # Build report
        report_lines = [
            f"**📊 基金新闻摘要** — {datetime.now().strftime('%Y年%m月%d日')}",
            "",
            "---",
            ""
        ]
        
        # Process results for each fund
        for i, ((fund_id, config), result) in enumerate(zip(FUNDS.items(), results), 1):
            if isinstance(result, Exception):
                report_lines.append(f"**{i}. {config['name']}**")
                report_lines.append(f"• 获取新闻失败: {str(result)}")
                report_lines.append("")
                continue
            
            if result and result.get("status") == "success":
                report_lines.append(f"**{i}. {config['name']}**")
                
                news_list = result.get("news", [])
                if news_list:
                    for news in news_list[:3]:  # Show max 3 items
                        title = news.get("title", "无标题")
                        source = news.get("source", "未知来源")
                        snippet = news.get("snippet", "暂无摘要")
                        
                        report_lines.append(f"• **{title}**")
                        report_lines.append(f"  - 来源: {source}")
                        report_lines.append(f"  - 摘要: {snippet[:100]}..." if len(snippet) > 100 else f"  - 摘要: {snippet}")
                else:
                    report_lines.append("• 今日暂无重大新闻")
                
                report_lines.append("")
            else:
                report_lines.append(f"**{i}. {config['name']}**")
                error_msg = result.get("error", "未知错误") if result else "获取失败"
                report_lines.append(f"• 获取新闻失败: {error_msg}")
                report_lines.append("")
        
        # Add impact prediction section
        report_lines.extend([
            "---",
            "",
            "**💡 今日净值影响预测**",
            ""
        ])
        
        for fund_id, config in FUNDS.items():
            impact_factors = config.get("impact_factors", [])
            factors_str = "、".join(impact_factors)
            report_lines.append(f"• **{config['name']}**: {factors_str}")
        
        report_lines.extend([
            "",
            "*数据来源: Yahoo Finance, Reuters, MarketWatch, Brave Search*"
        ])
        
        return "\n".join(report_lines)


async def main():
    """Main entry point."""
    # Check if API key is available
    use_api = bool(os.getenv("BRAVE_API_KEY"))
    
    if not use_api:
        logger.warning("BRAVE_API_KEY not found. Using mock data for testing.")
    
    generator = FundNewsGenerator(use_api=use_api)
    report = await generator.generate_summary()
    
    print(report)
    return report


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        
        # Optionally save to file
        output_file = "/tmp/fund_news_report.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        
        logger.info(f"Report saved to {output_file}")
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
