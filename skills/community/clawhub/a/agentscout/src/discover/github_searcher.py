"""GitHub API 搜索 + 过滤"""

import base64
from datetime import datetime, timedelta
from typing import Optional
from github import Github, GithubException

from src.config import GitHubConfig
from src.storage.models import Project
from src.storage.database import Database


class GitHubSearcher:
    """GitHub 项目搜索器"""

    def __init__(self, config: GitHubConfig, db: Database):
        self.github = Github(config.token) if config.token else Github()
        self.config = config
        self.db = db

    def search(self) -> list[Project]:
        """执行搜索，返回新发现的项目列表"""
        candidates = []

        # 策略1: 关键词搜索
        for query in self.config.search_queries:
            results = self._search_by_query(query)
            candidates.extend(results)

        # 策略2: 组织监控
        for org in self.config.watch_orgs:
            results = self._search_by_org(org)
            candidates.extend(results)

        # 去重（同一轮搜索内）
        seen = set()
        unique = []
        for p in candidates:
            if p.repo_full_name not in seen:
                seen.add(p.repo_full_name)
                unique.append(p)

        return unique

    def _search_by_query(self, query: str) -> list[Project]:
        """按关键词搜索"""
        projects = []
        try:
            repos = self.github.search_repositories(
                query=query,
                sort="updated",
                order="desc",
            )
            count = 0
            for repo in repos:
                if count >= self.config.max_results_per_query:
                    break
                # 跳过已存在的项目
                if self.db.project_exists(repo.full_name):
                    count += 1
                    continue
                project = self._repo_to_project(repo, source="search")
                if project:
                    projects.append(project)
                count += 1
        except GithubException as e:
            print(f"[GitHubSearcher] 搜索失败 ({query}): {e}")
        return projects

    def _search_by_org(self, org_name: str) -> list[Project]:
        """监控组织最近更新的 repo"""
        projects = []
        cutoff = datetime.now() - timedelta(days=self.config.recent_days)
        try:
            org = self.github.get_organization(org_name)
            for repo in org.get_repos(sort="updated", direction="desc"):
                if repo.updated_at and repo.updated_at < cutoff:
                    break
                if self.db.project_exists(repo.full_name):
                    continue
                project = self._repo_to_project(repo, source="org_watch")
                if project:
                    projects.append(project)
        except GithubException as e:
            print(f"[GitHubSearcher] 组织监控失败 ({org_name}): {e}")
        return projects

    def _repo_to_project(self, repo, source: str) -> Optional[Project]:
        """将 GitHub repo 对象转为 Project 模型"""
        try:
            readme_excerpt = self._get_readme_excerpt(repo)
            return Project(
                repo_full_name=repo.full_name,
                repo_url=repo.html_url,
                name=repo.name,
                description=repo.description or "",
                language=repo.language or "",
                stars=repo.stargazers_count,
                forks=repo.forks_count,
                open_issues=repo.open_issues_count,
                last_updated=repo.updated_at.isoformat() if repo.updated_at else "",
                created_at=repo.created_at.isoformat() if repo.created_at else "",
                owner_type=repo.owner.type if repo.owner else "",
                topics=repo.get_topics(),
                readme_excerpt=readme_excerpt,
                source=source,
            )
        except Exception as e:
            print(f"[GitHubSearcher] 解析 repo 失败 ({repo.full_name}): {e}")
            return None

    def _get_readme_excerpt(self, repo, max_chars: int = 500) -> str:
        """获取 README 前 N 个字符"""
        try:
            readme = repo.get_readme()
            content = base64.b64decode(readme.content).decode("utf-8", errors="replace")
            return content[:max_chars]
        except Exception:
            return ""
