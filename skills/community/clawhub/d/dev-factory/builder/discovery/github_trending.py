"""GitHub Trending 발굴 (GitHub API)

Phase 1: 기본 검색
Phase 2: 실제 메트릭 수집 (stars, forks, issues)
"""

import json
import logging
import subprocess
import re
from datetime import datetime
from typing import List, Dict, Optional

from builder.discovery.base import DiscoverySource
from builder.models import DiscoverySource as DS

logger = logging.getLogger('builder-agent.discovery.github')


class GitHubTrendingSource(DiscoverySource):
    """GitHub Trending/인기 repo 발굴"""

    def __init__(self, config=None):
        super().__init__(config)
        self.language = config.language if config else "python"
        self.max_results = config.max_results if config else 5
        self.method = config.method if config else "api"  # "api" | "browser"

    def discover(self) -> List[Dict]:
        """GitHub에서 인기 Python repo 발굴"""
        if not self.enabled:
            return []

        if self.method == "api":
            return self._discover_via_api()
        else:
            return self._discover_via_browser()

    def _discover_via_api(self) -> List[Dict]:
        """GitHub Search API 사용 (실제 메트릭 수집)"""
        ideas = []

        try:
            # gh CLI로 최근 인기 Python repo 검색
            result = subprocess.run([
                'gh', 'api',
                '/search/repositories',
                '-q', '.items[] | {name, full_name, description, stargazers_count, forks_count, open_issues_count, language, subscribers_count}',
                '-f', f'q=language:{self.language} stars:>10 pushed:>2026-01-01',
                '-f', 'sort=stars',
                '-f', 'order=desc',
                '-f', 'per_page=' + str(self.max_results)
            ], capture_output=True, text=True, timeout=15)

            if result.returncode != 0:
                logger.warning("GitHub API failed: %s", result.stderr)
                return self._discover_via_browser()

            # JSON 파싱
            repos = json.loads(result.stdout)

            for repo in repos[:self.max_results]:
                name = repo.get('name', '')
                full_name = repo.get('full_name', '')
                description = repo.get('description', '')
                stars = repo.get('stargazers_count', 0)
                forks = repo.get('forks_count', 0)
                issues = repo.get('open_issues_count', 0)
                subscribers = repo.get('subscribers_count', 0)

                # /pricing, /sponsors 등 비-repo 경로 필터링
                if '/' in name and not full_name.startswith(name):
                    continue

                # 실제 메트릭을 포함한 아이디어 생성
                ideas.append({
                    'title': f"GitHub: {full_name}",
                    'description': description or f"Popular Python repo with {stars} stars",
                    'source': DS.GITHUB_TRENDING.value,
                    'url': f"https://github.com/{full_name}",
                    'complexity': 'medium',
                    'priority': 'high' if stars > 1000 else 'medium',
                    'tech_stack': ['python'],
                    'discovered_at': datetime.now().isoformat(),
                    # 실제 메트릭 (AdaptiveIdeaScorer에서 사용)
                    'github_metrics': {
                        'stars': stars,
                        'forks': forks,
                        'issues': issues,
                        'subscribers': subscribers
                    }
                })

            logger.info("GitHub API: %d ideas found (with metrics)", len(ideas))

        except subprocess.TimeoutExpired:
            logger.warning("GitHub API timeout")
        except FileNotFoundError:
            logger.warning("gh CLI not found, falling back to browser")
            return self._discover_via_browser()
        except Exception as e:
            logger.warning("GitHub API error: %s", e)

        return ideas

    def _discover_via_browser(self) -> List[Dict]:
        """agent-browser로 GitHub Trending 접근 (fallback)"""
        ideas = []

        try:
            # agent-browser로 GitHub Trending 접근
            subprocess.run([
                'agent-browser', 'open',
                f'https://github.com/trending/{self.language}?since=daily'
            ], capture_output=True, timeout=30, check=False)

            import time
            time.sleep(2)

            # 스냅샷
            result = subprocess.run([
                'agent-browser', 'snapshot', '-c'
            ], capture_output=True, text=True, timeout=10)

            snapshot = result.stdout

            # repo 패턴 추출 (개선된 regex)
            repo_pattern = r'github\.com/([\w-]+/[\w-]+)'
            repos = re.findall(repo_pattern, snapshot)

            # 비-repo 경로 필터
            excluded = {'pricing', 'sponsors', 'explore', 'marketplace',
                        'features', 'security', 'team', 'enterprise'}

            seen = set()
            for repo in repos:
                owner, name = repo.split('/', 1)

                # 필터링
                if name in excluded or owner in excluded:
                    continue
                if repo in seen:
                    continue

                seen.add(repo)
                ideas.append({
                    'title': f"GitHub Trending: {repo}",
                    'description': f"Trending Python repository: {repo}",
                    'source': DS.GITHUB_TRENDING.value,
                    'url': f"https://github.com/{repo}",
                    'complexity': 'medium',
                    'priority': 'medium',
                    'tech_stack': ['python'],
                    'discovered_at': datetime.now().isoformat()
                })

                if len(ideas) >= self.max_results:
                    break

            # 브라우저 정리
            subprocess.run(['agent-browser', 'close'],
                          capture_output=True, timeout=5)

            logger.info("GitHub Browser: %d ideas found", len(ideas))

        except subprocess.TimeoutExpired:
            logger.warning("GitHub Trending timeout")
        except FileNotFoundError:
            logger.warning("agent-browser not found")
        except Exception as e:
            logger.warning("GitHub Trending error: %s", e)

        return ideas
