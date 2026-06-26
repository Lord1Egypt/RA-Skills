"""Builder Agent 헬스체크"""

import subprocess
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict

logger = logging.getLogger('builder-agent.health')


def check_health() -> Dict:
    """Discovery 시스템 헬스체크"""
    health = {
        'status': 'healthy',
        'checks': {}
    }

    # 1. agent-browser 확인
    try:
        result = subprocess.run(
            ['agent-browser', '--version'],
            capture_output=True, text=True, timeout=5
        )
        health['checks']['agent_browser'] = 'ok' if result.returncode == 0 else 'unavailable'
    except (subprocess.TimeoutExpired, FileNotFoundError):
        health['checks']['agent_browser'] = 'unavailable'
        health['status'] = 'degraded'

    # 2. NVD API 확인
    try:
        req = urllib.request.Request(
            'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1'
        )
        req.add_header('User-Agent', 'Builder-Agent-HealthCheck/1.0')
        with urllib.request.urlopen(req, timeout=10) as response:
            health['checks']['nvd_api'] = 'ok' if response.status == 200 else 'error'
    except Exception:
        health['checks']['nvd_api'] = 'unreachable'
        health['status'] = 'degraded'

    # 3. Notion API 토큰 확인
    env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
    has_notion_token = False
    if env_file.exists():
        content = env_file.read_text()
        has_notion_token = 'NOTION_API_KEY=' in content
    health['checks']['notion_token'] = 'ok' if has_notion_token else 'missing'
    if not has_notion_token:
        health['status'] = 'degraded'

    # 4. 캐시 디렉토리 확인
    cache_dir = Path('/tmp/builder-discovery/cache')
    health['checks']['cache_dir'] = 'ok' if cache_dir.exists() else 'not_created'

    # 5. brave-search 확인
    brave_search = Path.home() / '.openclaw' / 'workspace' / 'skills' / 'brave-search' / 'search.js'
    health['checks']['brave_search'] = 'ok' if brave_search.exists() else 'missing'

    return health


def log_health_report(health: Dict):
    """헬스체크 결과 로깅"""
    status = health['status']
    checks = health['checks']

    if status == 'healthy':
        logger.info("Health check: ALL OK")
    else:
        logger.warning("Health check: %s", status.upper())
        for component, result in checks.items():
            if result != 'ok':
                logger.warning("  %s: %s", component, result)

    return status == 'healthy'


if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("="*70)
    print("BUILDER AGENT HEALTH CHECK")
    print("="*70)
    
    health = check_health()
    
    print(f"\nOverall Status: {health['status'].upper()}")
    print("\nComponent Status:")
    for component, status in health['checks'].items():
        icon = "✅" if status == "ok" else "⚠️" if status in ["not_created", "missing"] else "❌"
        print(f"  {icon} {component}: {status}")
    
    print("="*70)
    
    if health['status'] == 'healthy':
        print("✅ All systems operational")
        exit(0)
    else:
        print("⚠️ Some issues detected, check logs for details")
        exit(1)
