#!/usr/bin/env python3
"""
Discovery Layer for Builder Agent
GitHub Trending, CVE Database, Security News에서 프로젝트 아이디어 발굴
"""

import json
import subprocess
import time
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import urllib.error
import urllib.parse
import logging

logger = logging.getLogger('builder-agent.discovery')


class DiscoveryCache:
    """소스별 캐시 관리"""

    def __init__(self, cache_dir: Path, ttl_seconds: int = 3600):
        self.cache_dir = cache_dir
        self.ttl = ttl_seconds
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, source: str) -> Optional[List[Dict]]:
        cache_file = self.cache_dir / f"{source}_cache.json"
        if not cache_file.exists():
            return None
        try:
            data = json.loads(cache_file.read_text())
            if time.time() - data.get('timestamp', 0) > self.ttl:
                return None
            logger.info("Cache hit for %s (%d ideas)", source, len(data['ideas']))
            return data['ideas']
        except (json.JSONDecodeError, KeyError):
            return None

    def set(self, source: str, ideas: List[Dict]):
        cache_file = self.cache_dir / f"{source}_cache.json"
        cache_file.write_text(json.dumps({
            'timestamp': time.time(),
            'ideas': ideas
        }, ensure_ascii=False, indent=2))


class DiscoveryLayer:
    """프로젝트 아이디어 발굴 시스템"""

    def __init__(self, output_dir: str = "/tmp/builder-discovery", cache_ttl: int = 3600):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 캐시
        self.cache = DiscoveryCache(self.output_dir / "cache", ttl_seconds=cache_ttl)

        # 발견된 아이디어 저장소
        self.ideas_file = self.output_dir / "discovered_ideas.json"
        self.ideas = self._load_ideas()
    
    def discover_all(self) -> List[Dict]:
        """모든 소스에서 병렬로 아이디어 발굴"""

        logger.info("Starting discovery process...")

        all_ideas = []

        sources = {
            'GitHub Trending': self.discover_from_github_trending,
            'CVE Database': self.discover_from_cve_database,
            'Security News': self.discover_from_security_news,
        }

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(func): name
                for name, func in sources.items()
            }

            for future in as_completed(futures, timeout=60):
                source_name = futures[future]
                try:
                    ideas = future.result(timeout=30)
                    all_ideas.extend(ideas)
                    self.ideas.extend(ideas)
                    logger.info("%s: %d ideas found", source_name, len(ideas))
                except Exception as e:
                    logger.warning("%s failed: %s", source_name, e)

        # 중복 제거
        unique_ideas = self._remove_duplicates(all_ideas)

        # 저장
        self._save_ideas(unique_ideas)

        logger.info("Discovery complete: %d unique ideas found", len(unique_ideas))
        
        return unique_ideas
    
    def discover_from_github_trending(self) -> List[Dict]:
        """GitHub Trending에서 아이디어 발굴"""

        cached = self.cache.get('github_trending')
        if cached is not None:
            return cached

        ideas = []

        try:
            # agent-browser로 GitHub Trending 접근
            result = subprocess.run([
                'agent-browser', 'open', 
                'https://github.com/trending/python?since=daily'
            ], capture_output=True, text=True, timeout=30)
            
            time.sleep(2)  # 페이지 로드 대기
            
            # 스냅샷 가져오기
            result = subprocess.run([
                'agent-browser', 'snapshot', '-c'
            ], capture_output=True, text=True, timeout=10)
            
            snapshot = result.stdout
            
            # 레포지토리 정보 추출 (간단한 파싱)
            # 실제로는 더 정교한 파싱 필요
            repo_pattern = r'([\w-]+/[\w-]+)'
            repos = re.findall(repo_pattern, snapshot)[:5]
            
            for repo in repos:
                ideas.append({
                    'title': f"Clone/Improve: {repo}",
                    'description': f"Based on trending GitHub repo: {repo}",
                    'source': 'github_trending',
                    'url': f"https://github.com/{repo}",
                    'complexity': 'medium',
                    'priority': 'medium',
                    'discovered_at': datetime.now().isoformat()
                })
            
            # 브라우저 닫기
            subprocess.run(['agent-browser', 'close'], capture_output=True, timeout=5)
            
        except subprocess.TimeoutExpired:
            logger.warning("Timeout while accessing GitHub Trending")
        except Exception as e:
            logger.warning("GitHub Trending error: %s", e)

        if ideas:
            self.cache.set('github_trending', ideas)
        return ideas

    def discover_from_cve_database(self) -> List[Dict]:
        """CVE Database에서 아이디어 발굴 (NVD API 사용)"""

        cached = self.cache.get('cve_database')
        if cached is not None:
            return cached

        ideas = []

        try:
            # NVD API 사용 (HTTP) - 최근 7일 고위험 CVE만 조회
            url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=7)

            params = urllib.parse.urlencode({
                'resultsPerPage': 20,
                'pubStartDate': start_date.strftime('%Y-%m-%dT00:00:00.000'),
                'pubEndDate': end_date.strftime('%Y-%m-%dT23:59:59.999'),
                'cvssV3Severity': 'HIGH',
            })

            req = urllib.request.Request(f"{url}?{params}")
            req.add_header('User-Agent', 'Builder-Agent-Discovery/1.0')

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
            
            # CVE 데이터 파싱
            for vuln in data.get('vulnerabilities', [])[:20]:
                cve = vuln['cve']
                cve_id = cve.get('id', 'Unknown')
                
                # 설명 가져오기
                descriptions = cve.get('descriptions', [])
                description = next(
                    (d['value'] for d in descriptions if d.get('lang') == 'en'),
                    descriptions[0].get('value', 'No description') if descriptions else 'No description'
                )
                
                # CVSS 점수 확인
                metrics = cve.get('metrics', {})
                severity = 'Unknown'
                score = 0.0
                
                if 'cvssMetricV31' in metrics:
                    cvss_data = metrics['cvssMetricV31'][0].get('cvssData', {})
                    severity = cvss_data.get('baseSeverity', 'Unknown')
                    score = cvss_data.get('baseScore', 0.0)
                elif 'cvssMetricV2' in metrics:
                    cvss_data = metrics['cvssMetricV2'][0].get('cvssData', {})
                    score = cvss_data.get('baseScore', 0.0)
                    severity = 'HIGH' if score >= 7.0 else 'MEDIUM' if score >= 4.0 else 'LOW'
                
                # 심각한 취약점만 선택 (score >= 7.0)
                if score >= 7.0:
                    ideas.append({
                        'title': f"CVE Scanner: {cve_id}",
                        'description': f"Scanner for {description[:150]}",
                        'source': 'cve_database',
                        'cve_id': cve_id,
                        'severity': severity,
                        'score': score,
                        'url': f"https://nvd.nist.gov/vuln/detail/{cve_id}",
                        'complexity': 'medium',
                        'priority': 'high' if severity == 'CRITICAL' else 'medium',
                        'discovered_at': datetime.now().isoformat()
                    })
        
        except urllib.error.HTTPError as e:
            logger.warning("CVE API HTTP Error %d: %s", e.code, e.reason)
        except urllib.error.URLError as e:
            logger.warning("CVE API Network Error: %s", e.reason)
        except json.JSONDecodeError as e:
            logger.warning("CVE API JSON Decode Error: %s", e)
        except Exception as e:
            logger.warning("CVE API error: %s", e)

        if ideas:
            self.cache.set('cve_database', ideas)
        return ideas

    def discover_from_security_news(self) -> List[Dict]:
        """Security News에서 아이디어 발굴 (RSS/HTTP 사용)"""

        cached = self.cache.get('security_news')
        if cached is not None:
            return cached

        ideas = []

        # 보안 뉴스 소스들 (RSS 피드가 있다면 사용)
        news_sources = [
            {
                'name': 'KRCERT',
                'url': 'https://www.krcert.or.kr',
                'type': 'web'
            }
        ]

        try:
            for source in news_sources:
                try:
                    req = urllib.request.Request(source['url'])
                    req.add_header('User-Agent', 'Builder-Agent-Discovery/1.0')

                    with urllib.request.urlopen(req, timeout=5) as response:
                        # TODO: Sprint 3에서 brave-search 기반 실제 구현으로 교체
                        pass

                except Exception:
                    pass

            # 키워드 기반 아이디어 생성 (Sprint 3에서 brave-search로 대체 예정)
            keywords = ['ransomware', 'vulnerability', 'malware', 'phishing',
                        'zero-day', 'supply-chain']

            for keyword in keywords:
                ideas.append({
                    'title': f"Security Tool: {keyword.title()} Detector",
                    'description': f"Tool to detect and analyze {keyword} threats",
                    'source': 'security_news',
                    'keyword': keyword,
                    'complexity': 'medium',
                    'priority': 'medium',
                    'discovered_at': datetime.now().isoformat()
                })

        except Exception as e:
            logger.warning("Security News error: %s", e)

        if ideas:
            self.cache.set('security_news', ideas)
        return ideas
    
    def queue_to_notion(self, ideas: List[Dict], database_id: str) -> int:
        """Notion 큐에 아이디어 등록"""
        
        notion_token = self._get_notion_token()
        if not notion_token:
            logger.warning("Notion API token not found")
            return 0
        
        queued_count = 0
        
        for idea in ideas[:10]:  # 최대 10개만 큐에 등록
            try:
                # Notion API 호출 - 실제 DB 구조에 맞게 수정
                data = {
                    "parent": {"database_id": database_id},
                    "properties": {
                        "내용": {
                            "title": [{"text": {"content": idea['title']}}]
                        },
                        "상태": {"status": {"name": "아이디어"}},
                        "카테고리": {"select": {"name": "AI-Agent"}},  # 기본값
                        "테그": {"multi_select": [{"name": "아이디어"}]}
                    }
                }
                
                # 설명 추가 (있는 경우)
                if idea.get('description'):
                    data["properties"]["도구 설명"] = {
                        "rich_text": [{"text": {"content": idea['description'][:2000]}}]
                    }
                
                # URL 추가 (있는 경우)
                if idea.get('url'):
                    data["properties"]["URL"] = {"url": idea['url']}
                
                req = urllib.request.Request(
                    'https://api.notion.com/v1/pages',
                    data=json.dumps(data).encode('utf-8'),
                    headers={
                        'Authorization': f'Bearer {notion_token}',
                        'Content-Type': 'application/json',
                        'Notion-Version': '2022-06-28'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        queued_count += 1
                        logger.info("Queued: %s", idea['title'][:50])

                time.sleep(0.5)  # Rate limit 회피

            except Exception as e:
                logger.warning("Failed to queue %s: %s", idea['title'][:30], e)
        
        return queued_count
    
    def _load_ideas(self) -> List[Dict]:
        """저장된 아이디어 로드"""
        
        if self.ideas_file.exists():
            try:
                with open(self.ideas_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_ideas(self, ideas: List[Dict]):
        """아이디어 저장"""
        
        with open(self.ideas_file, 'w') as f:
            json.dump(ideas, f, indent=2, ensure_ascii=False)
        
        logger.info("Saved %d ideas to %s", len(ideas), self.ideas_file)
    
    def _remove_duplicates(self, ideas: List[Dict]) -> List[Dict]:
        """중복 제거"""
        
        seen = set()
        unique = []
        
        for idea in ideas:
            # 제목 기준 중복 체크
            key = idea['title'].lower()
            
            if key not in seen:
                seen.add(key)
                unique.append(idea)
        
        return unique
    
    def _get_notion_token(self) -> Optional[str]:
        """Notion API 토큰 가져오기"""
        
        # .env 파일에서 읽기
        import os
        _workspace = os.getenv("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace"))
        env_file = Path(_workspace) / ".env"
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('NOTION_API_KEY='):
                        return line.split('=', 1)[1].strip()
        
        return None
    
    def get_stats(self) -> Dict:
        """발견 통계"""
        
        return {
            'total_ideas': len(self.ideas),
            'by_source': {
                'github_trending': len([i for i in self.ideas if i.get('source') == 'github_trending']),
                'cve_database': len([i for i in self.ideas if i.get('source') == 'cve_database']),
                'security_news': len([i for i in self.ideas if i.get('source') == 'security_news'])
            },
            'by_priority': {
                'high': len([i for i in self.ideas if i.get('priority') == 'high']),
                'medium': len([i for i in self.ideas if i.get('priority') == 'medium']),
                'low': len([i for i in self.ideas if i.get('priority') == 'low'])
            }
        }


if __name__ == "__main__":
    # 직접 실행 시 기본 로깅 설정
    logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(message)s')

    discovery = DiscoveryLayer()
    ideas = discovery.discover_all()

    for i, idea in enumerate(ideas[:10], 1):
        print(f"{i}. [{idea['source']}] {idea['title']} (priority: {idea.get('priority', 'N/A')})")

    stats = discovery.get_stats()
    print(f"\nTotal: {stats['total_ideas']} | "
          f"GitHub: {stats['by_source']['github_trending']} | "
          f"CVE: {stats['by_source']['cve_database']} | "
          f"News: {stats['by_source']['security_news']}")
