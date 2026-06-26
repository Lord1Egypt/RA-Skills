#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fallback_handler.py - Fallback mechanism for ChinaTour Skill

Handles graceful degradation when API is unavailable:
1. Try API first
2. Fall back to local data
3. Provide meaningful error messages

Usage:
    from fallback_handler import FallbackHandler

    handler = FallbackHandler()
    result = handler.ask("故宫开放时间?")
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Handle Windows console encoding
if sys.platform == 'win32':
    import io
    if not isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Import API client
try:
    from api_client import ChinaTourClient, AskResult, HealthResult
    API_CLIENT_AVAILABLE = True
except ImportError:
    API_CLIENT_AVAILABLE = False

# Import local data loader
try:
    from recommend_route import load_attraction_data, SUPPORTED_ATTRACTIONS
    LOCAL_DATA_AVAILABLE = True
except ImportError:
    LOCAL_DATA_AVAILABLE = False


# ============== Configuration ==============

DEFAULT_API_URL = os.environ.get('CHINATOUR_API_URL', 'http://localhost:3000')
DEFAULT_TIMEOUT = int(os.environ.get('CHINATOUR_API_TIMEOUT', '90'))
FALLBACK_ENABLED = os.environ.get('CHINATOUR_FALLBACK', 'true').lower() == 'true'


# ============== Data Classes ==============

@dataclass
class FallbackResult:
    """Result from fallback handler"""
    success: bool
    answer: str
    source: str  # 'api', 'local', 'error'
    error: Optional[str] = None
    from_cache: bool = False


# ============== Fallback Handler ==============

class FallbackHandler:
    """
    Handles fallback from API to local data

    Example:
        handler = FallbackHandler()
        result = handler.ask("故宫开放时间?")
        print(f"Source: {result.source}")
        print(f"Answer: {result.answer}")
    """

    def __init__(
        self,
        api_url: str = DEFAULT_API_URL,
        timeout: int = DEFAULT_TIMEOUT,
        enable_fallback: bool = FALLBACK_ENABLED,
        debug: bool = False
    ):
        self.api_url = api_url
        self.timeout = timeout
        self.enable_fallback = enable_fallback
        self.debug = debug

        # Initialize API client if available
        self.api_client = None
        if API_CLIENT_AVAILABLE:
            self.api_client = ChinaTourClient(
                api_url=api_url,
                timeout=timeout,
                debug=debug
            )

        # Track API health
        self.api_healthy = None
        self.last_health_check = 0
        self.health_check_interval = 60  # seconds

    def _log(self, message: str) -> None:
        """Debug logging"""
        if self.debug:
            print(f"[FallbackHandler] {message}")

    def _should_check_health(self) -> bool:
        """Check if we should run a health check"""
        return (
            self.api_healthy is None or
            time.time() - self.last_health_check > self.health_check_interval
        )

    def check_api_health(self) -> bool:
        """
        Check if API is healthy

        Returns:
            True if API is healthy, False otherwise
        """
        if not self.api_client:
            self._log("API client not available")
            return False

        try:
            result = self.api_client.health_check()
            self.api_healthy = result.success
            self.last_health_check = time.time()
            self._log(f"API health: {'healthy' if result.success else 'unhealthy'}")
            return result.success
        except Exception as e:
            self._log(f"Health check error: {e}")
            self.api_healthy = False
            self.last_health_check = time.time()
            return False

    def _try_api(self, question: str, **kwargs) -> Optional[FallbackResult]:
        """Try to get answer from API"""
        if not self.api_client:
            return None

        # Check health if needed
        if self._should_check_health():
            if not self.check_api_health():
                return None

        try:
            result = self.api_client.ask(question, **kwargs)

            if result.success:
                return FallbackResult(
                    success=True,
                    answer=result.answer,
                    source='api',
                    from_cache=result.from_cache
                )
            else:
                self._log(f"API error: {result.error}")
                return None

        except Exception as e:
            self._log(f"API exception: {e}")
            self.api_healthy = False
            return None

    def _try_local(self, question: str) -> Optional[FallbackResult]:
        """Try to get answer from local data"""
        if not LOCAL_DATA_AVAILABLE:
            return None

        # Try to identify attraction from question
        attraction = self._identify_attraction(question)
        if not attraction:
            return None

        # Load local data
        data = load_attraction_data(attraction)
        if not data:
            return None

        # Generate answer from local data
        answer = self._generate_local_answer(question, data)
        if answer:
            return FallbackResult(
                success=True,
                answer=answer,
                source='local'
            )

        return None

    def _identify_attraction(self, question: str) -> Optional[str]:
        """Identify attraction from question text"""
        # Map of keywords to attraction IDs
        attraction_keywords = {
            'forbidden-city': ['故宫', '紫禁城', 'Forbidden City', '故宫博物院'],
            'great-wall': ['长城', '万里长城', 'Great Wall', '八达岭', '慕田峪'],
            'summer-palace': ['颐和园', 'Summer Palace'],
            'temple-of-heaven': ['天坛', 'Temple of Heaven'],
            'terracotta-army': ['兵马俑', '秦始皇陵', 'Terracotta', '兵马俑博物馆'],
            'west-lake': ['西湖', 'West Lake', '杭州西湖'],
            'yellow-mountain': ['黄山', 'Yellow Mountain', '黄山风景区'],
            'jiuzhaigou': ['九寨沟', 'Jiuzhaigou', '九寨沟风景区'],
            'potala-palace': ['布达拉宫', 'Potala Palace'],
            'lijiang-old-town': ['丽江', 'Lijiang', '丽江古城'],
            'wulingyuan': ['张家界', 'Zhangjiajie', '武陵源'],
            'dunhuang-mogao-caves': ['敦煌', 'Dunhuang', '莫高窟', 'Mogao'],
        }

        question_lower = question.lower()
        for attraction_id, keywords in attraction_keywords.items():
            for keyword in keywords:
                if keyword.lower() in question_lower:
                    return attraction_id

        return None

    def _generate_local_answer(self, question: str, data: Dict) -> Optional[str]:
        """Generate answer from local data"""
        name = data.get('name', '景区')
        spots = data.get('spots', [])

        # Check for different question types
        question_lower = question.lower()

        # Opening hours question
        if any(k in question_lower for k in ['开放时间', '几点', '开门', 'closing', 'open']):
            return f"""📍 {name} 开放时间

由于 API 服务暂时不可用，以下是参考信息：

**旺季 (4-10月)**: 08:00 - 18:00
**淡季 (11-3月)**: 08:00 - 17:30

⚠️ 注意：此为参考信息，实际开放时间请以官方公告为准。

建议：
1. 提前在官方平台预约门票
2. 节假日可能调整开放时间
3. 恢复在线服务后可获取最新信息
"""
        # Main attractions question
        if any(k in question_lower for k in ['景点', '看什么', 'what to see', 'attractions']):
            if spots:
                spots_list = '\n'.join([f"  • {s.get('name', '景点')} - {s.get('highlight', '亮点')}" for s in spots[:5]])
                return f"""📍 {name} 主要景点

{spots_list}

⚠️ 注意：此为离线参考信息，建议恢复在线服务后获取完整导览。
"""

        # Route question
        if any(k in question_lower for k in ['路线', '怎么逛', '怎么走', 'route', 'how to visit']):
            if spots:
                route = ' → '.join([s.get('name', '景点') for s in spots[:5]])
                return f"""📍 {name} 推荐路线

推荐游览顺序：
{route}

⚠️ 注意：此为离线参考信息，建议恢复在线服务后获取个性化路线推荐。
"""

        # Default answer
        if spots:
            return f"""📍 {name}

主要景点：
{chr(10).join([f"  • {s.get('name', '景点')}" for s in spots[:5]])}

⚠️ API 服务暂时不可用，此为离线参考信息。
恢复在线服务后可获取完整 AI 导览服务。
"""

        return None

    def _generate_error_message(self, question: str) -> str:
        """Generate error message when no data available"""
        return """⚠️ 服务暂时不可用

很抱歉，AI 导游服务暂时不可用。请稍后重试或尝试以下方式：

1. **检查网络连接** - 确保网络正常
2. **稍后重试** - 服务可能正在维护
3. **查看官方信息** - 访问景区官方网站获取最新信息

如有紧急问题，请联系景区客服。
"""

    def ask(self, question: str, **kwargs) -> FallbackResult:
        """
        Ask a question with fallback support

        Args:
            question: User question
            **kwargs: Additional arguments for API

        Returns:
            FallbackResult with answer and source info
        """
        self._log(f"Processing question: {question[:50]}...")

        # Try API first
        if self.api_client:
            result = self._try_api(question, **kwargs)
            if result:
                self._log(f"Got answer from API (cache={result.from_cache})")
                return result

        # Fall back to local data
        if self.enable_fallback:
            result = self._try_local(question)
            if result:
                self._log("Got answer from local data")
                return result

        # No answer available
        self._log("No answer available")
        return FallbackResult(
            success=False,
            answer=self._generate_error_message(question),
            source='error',
            error='Service unavailable'
        )

    def get_status(self) -> Dict[str, Any]:
        """Get current status of fallback handler"""
        return {
            'api_client_available': API_CLIENT_AVAILABLE,
            'local_data_available': LOCAL_DATA_AVAILABLE,
            'api_healthy': self.api_healthy,
            'fallback_enabled': self.enable_fallback,
            'last_health_check': self.last_health_check,
        }


# ============== Convenience Functions ==============

_handler: Optional[FallbackHandler] = None


def get_handler(**kwargs) -> FallbackHandler:
    """Get or create singleton handler"""
    global _handler
    if _handler is None:
        _handler = FallbackHandler(**kwargs)
    return _handler


def ask_with_fallback(question: str, **kwargs) -> FallbackResult:
    """Convenience function for asking questions with fallback"""
    return get_handler().ask(question, **kwargs)


# ============== CLI Interface ==============

def main():
    """CLI interface for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='ChinaTour Fallback Handler')
    parser.add_argument('question', nargs='?', help='Question to ask')
    parser.add_argument('--api-url', default=DEFAULT_API_URL, help='API URL')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='Timeout in seconds')
    parser.add_argument('--no-fallback', action='store_true', help='Disable fallback')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--status', action='store_true', help='Show handler status')

    args = parser.parse_args()

    handler = FallbackHandler(
        api_url=args.api_url,
        timeout=args.timeout,
        enable_fallback=not args.no_fallback,
        debug=args.debug
    )

    if args.status:
        status = handler.get_status()
        print(json.dumps(status, indent=2))
        return

    if not args.question:
        parser.print_help()
        return

    result = handler.ask(args.question)

    print(f"\n{'='*50}")
    print(f"Source: {result.source}")
    print(f"Success: {result.success}")
    if result.from_cache:
        print(f"From cache: {result.from_cache}")
    print(f"{'='*50}")
    print(result.answer)
    if result.error:
        print(f"\nError: {result.error}")


if __name__ == '__main__':
    main()