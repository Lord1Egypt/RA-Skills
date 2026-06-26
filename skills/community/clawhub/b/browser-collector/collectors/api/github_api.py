#!/usr/bin/env python3
"""
collectors/api/github_api.py - GitHub API适配器

直接调用GitHub REST API获取结构化数据，无需浏览器。

Usage:
    # 基本使用
    from collectors.api.github_api import GitHubAPIAdapter
    api = GitHubAPIAdapter(token=None)  # 无token限制60 req/hr

    # 获取仓库信息
    repo = api.get_repo('microsoft', 'vscode')
    print(f"仓库: {repo.full_name}, 星标: {repo.stars}, 语言: {repo.language}")

    # 获取issues
    issues = api.get_issues('owner', 'repo', state='open', labels=['bug'])

    # 搜索仓库
    results = api.search_repos('playwright', language='python', sort='stars')

    # 获取用户信息
    user = api.get_user('octocat')

    # 获取commit
    commits = api.get_commits('owner', 'repo', since='2024-01-01')

    # 批量获取（自动处理rate limit）
    repos = api.get_multipleRepos([
        ('microsoft', 'vscode'),
        ('openai', 'openai-python'),
        ('facebook', 'react'),
    ])
"""

import time
import math
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from urllib.parse import quote


# ==================== 数据模型 ====================

@dataclass
class GitHubRepo:
    """GitHub仓库数据"""
    full_name: str
    name: str
    owner: str
    description: str
    html_url: str
    stars: int
    forks: int
    language: str
    topics: List[str] = field(default_factory=list)
    open_issues: int = 0
    watchers: int = 0
    created_at: str = ''
    updated_at: str = ''
    pushed_at: str = ''
    license: str = ''
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: Dict) -> 'GitHubRepo':
        return cls(
            full_name=data.get('full_name', ''),
            name=data.get('name', ''),
            owner=data.get('owner', {}).get('login', ''),
            description=data.get('description', '') or '',
            html_url=data.get('html_url', ''),
            stars=data.get('stargazers_count', 0),
            forks=data.get('forks_count', 0),
            language=data.get('language', '') or '',
            topics=data.get('topics', []),
            open_issues=data.get('open_issues_count', 0),
            watchers=data.get('watchers_count', 0),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', ''),
            pushed_at=data.get('pushed_at', ''),
            license=data.get('license', {}).get('name', '') if data.get('license') else '',
            metadata=data,
        )

    def to_item_dict(self) -> Dict:
        """转为dict格式（适配StructuredItem）"""
        return {
            'title': self.full_name,
            'url': self.html_url,
            'platform': 'github.com',
            'author': self.owner,
            'content': f"{self.description}\n\n语言: {self.language}\n星标: {self.stars}\nFork: {self.forks}",
            'tags': self.topics,
            'quality_score': min(1.0, self.stars / 10000),  # 按星标计算质量
        }


@dataclass
class GitHubIssue:
    """GitHub Issue数据"""
    number: int
    title: str
    body: str
    state: str
    html_url: str
    author: str
    labels: List[str] = field(default_factory=list)
    comments: int = 0
    created_at: str = ''
    updated_at: str = ''
    closed_at: str = ''
    repository: str = ''
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: Dict, repo: str = '') -> 'GitHubIssue':
        labels = [l.get('name', '') for l in data.get('labels', [])]
        return cls(
            number=data.get('number', 0),
            title=data.get('title', ''),
            body=data.get('body', '') or '',
            state=data.get('state', 'open'),
            html_url=data.get('html_url', ''),
            author=data.get('user', {}).get('login', ''),
            labels=labels,
            comments=data.get('comments', 0),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', ''),
            closed_at=data.get('closed_at', '') or '',
            repository=repo,
            metadata=data,
        )


@dataclass
class GitHubUser:
    """GitHub用户数据"""
    login: str
    name: str
    bio: str
    html_url: str
    avatar_url: str
    public_repos: int = 0
    followers: int = 0
    following: int = 0
    location: str = ''
    company: str = ''
    blog: str = ''
    email: str = ''
    hireable: bool = False
    created_at: str = ''
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: Dict) -> 'GitHubUser':
        return cls(
            login=data.get('login', ''),
            name=data.get('name', '') or '',
            bio=data.get('bio', '') or '',
            html_url=data.get('html_url', ''),
            avatar_url=data.get('avatar_url', ''),
            public_repos=data.get('public_repos', 0),
            followers=data.get('followers', 0),
            following=data.get('following', 0),
            location=data.get('location', '') or '',
            company=data.get('company', '') or '',
            blog=data.get('blog', '') or '',
            email=data.get('email', '') or '',
            hireable=data.get('hireable', False),
            created_at=data.get('created_at', ''),
            metadata=data,
        )


@dataclass
class GitHubCommit:
    """GitHub提交记录"""
    sha: str
    message: str
    author: str
    author_date: str
    committer: str
    commit_date: str
    html_url: str
    repository: str = ''
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: Dict, repo: str = '') -> 'GitHubCommit':
        commit = data.get('commit', {})
        author_info = commit.get('author', {})
        committer_info = commit.get('committer', {})
        return cls(
            sha=data.get('sha', ''),
            message=commit.get('message', '').split('\n')[0],  # 第一行
            author=author_info.get('name', ''),
            author_date=author_info.get('date', ''),
            committer=committer_info.get('name', ''),
            commit_date=committer_info.get('date', ''),
            html_url=data.get('html_url', ''),
            repository=repo,
            metadata=data,
        )


# ==================== GitHub API适配器 ====================

class GitHubAPIAdapter:
    """
    GitHub API适配器

    功能：
    - 仓库信息查询
    - Issues/PR查询
    - 用户信息查询
    - 代码搜索
    - 自动处理Rate Limit
    - 分页处理

    Rate Limit说明：
    - 无token: 60 req/hr
    - 有token: 5000 req/hr

    Attributes:
        token: GitHub Personal Access Token
        base_url: API基础URL
        per_page: 每页数量
    """

    BASE_URL = 'https://api.github.com'
    DEFAULT_HEADERS = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'BrowserCollector/1.0',
    }

    def __init__(self, token: str = None, per_page: int = 30):
        """
        Args:
            token: GitHub Personal Access Token（可选）
            per_page: 每页数量（最大100）
        """
        self.token = token
        self.per_page = min(per_page, 100)
        self._rate_limit_remaining = None
        self._rate_limit_reset = None
        self._last_request_time = 0

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = self.DEFAULT_HEADERS.copy()
        if self.token:
            headers['Authorization'] = f'token {self.token}'
        return headers

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        通用请求方法

        Args:
            method: HTTP方法 (GET, POST, etc.)
            endpoint: API端点
            **kwargs: 传递给requests的参数

        Returns:
            API响应的dict
        """
        import urllib.request
        import json

        # 请求限速（避免触发rate limit）
        self._throttle()

        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()

        # 添加分页参数
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['per_page'] = self.per_page

        # 构建URL（带查询参数）
        if kwargs.get('params'):
            query = '&'.join(f"{k}={quote(str(v))}" for k, v in kwargs['params'].items() if v)
            if query:
                url = f"{url}?{query}"

        req = urllib.request.Request(url, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                self._update_rate_limit(resp)
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 403:
                # Rate limit
                self._handle_rate_limit(e)
                raise Exception(f"Rate limit exceeded. Resets at: {self._rate_limit_reset}")
            elif e.code == 404:
                raise Exception(f"Not found: {url}")
            else:
                raise Exception(f"HTTP {e.code}: {e.reason}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")

    def _throttle(self):
        """请求限速（每秒不超过10个请求）"""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < 0.1:  # 至少100ms间隔
            time.sleep(0.1 - elapsed)
        self._last_request_time = time.time()

    def _update_rate_limit(self, response):
        """从响应头更新rate limit信息"""
        self._rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        self._rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))

    def _handle_rate_limit(self, error):
        """处理rate limit（等待到重置时间）"""
        if self._rate_limit_reset:
            wait_seconds = max(1, self._rate_limit_reset - time.time() + 5)
            print(f"[GitHubAPI] Rate limit reached. Waiting {wait_seconds:.0f}s...")
            time.sleep(wait_seconds)

    def _get_paginated(self, endpoint: str, max_pages: int = 5, **kwargs) -> List[Dict]:
        """
        分页获取数据

        Args:
            endpoint: API端点
            max_pages: 最大页数
            **kwargs: 其他参数

        Returns:
            所有页的数据合并列表
        """
        all_data = []
        page = 1

        while page <= max_pages:
            kwargs['params']['page'] = page
            try:
                data = self._request('GET', endpoint, params=kwargs.pop('params', {}))
                if isinstance(data, list):
                    all_data.extend(data)
                    if len(data) < self.per_page:
                        break  # 最后一页
                else:
                    break
                page += 1
            except Exception as e:
                print(f"[GitHubAPI] Page {page} failed: {e}")
                break

        return all_data

    # ---- 仓库操作 ----

    def get_repo(self, owner: str, repo: str) -> GitHubRepo:
        """
        获取仓库信息

        Args:
            owner: 仓库所有者
            repo: 仓库名

        Returns:
            GitHubRepo对象
        """
        data = self._request('GET', f'/repos/{owner}/{repo}')
        return GitHubRepo.from_api(data)

    def get_repos(self, owner: str) -> List[GitHubRepo]:
        """
        获取用户的仓库列表

        Args:
            owner: 用户/组织名

        Returns:
            GitHubRepo列表
        """
        data = self._get_paginated(f'/users/{owner}/repos', max_pages=3)
        return [GitHubRepo.from_api(d) for d in data]

    def get_multipleRepos(self, repo_specs: List[Tuple[str, str]]) -> List[GitHubRepo]:
        """
        批量获取多个仓库信息

        Args:
            repo_specs: [(owner, repo), ...] 列表

        Returns:
            GitHubRepo列表
        """
        repos = []
        for owner, repo in repo_specs:
            try:
                r = self.get_repo(owner, repo)
                repos.append(r)
            except Exception as e:
                print(f"[GitHubAPI] Failed to get {owner}/{repo}: {e}")
        return repos

    def get_repo_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """获取仓库语言统计"""
        data = self._request('GET', f'/repos/{owner}/{repo}/languages')
        return data

    def get_repo_topics(self, owner: str, repo: str) -> List[str]:
        """获取仓库topics"""
        data = self._request('GET', f'/repos/{owner}/{repo}/topics')
        return data.get('names', [])

    # ---- Issues操作 ----

    def get_issues(self, owner: str, repo: str, state: str = 'open',
                   labels: str = None, since: str = None, sort: str = 'created') -> List[GitHubIssue]:
        """
        获取仓库的issues

        Args:
            owner: 仓库所有者
            repo: 仓库名
            state: open/closed/all
            labels: 逗号分隔的标签
            since: ISO格式日期（只返回此日期后的）
            sort: created/updated/comments

        Returns:
            GitHubIssue列表
        """
        params = {'state': state, 'sort': sort}
        if labels:
            params['labels'] = labels
        if since:
            params['since'] = since

        data = self._get_paginated(f'/repos/{owner}/{repo}/issues', max_pages=3, params=params)
        return [GitHubIssue.from_api(d, f"{owner}/{repo}") for d in data if d.get('pull_request') is None]  # 过滤PR

    def get_issue_comments(self, owner: str, repo: str, issue_number: int) -> List[Dict]:
        """获取issue的评论"""
        data = self._get_paginated(f'/repos/{owner}/{repo}/issues/{issue_number}/comments', max_pages=2)
        return data

    def create_issue(self, owner: str, repo: str, title: str, body: str = '', labels: List[str] = None) -> GitHubIssue:
        """创建issue（需要token）"""
        payload = {'title': title, 'body': body}
        if labels:
            payload['labels'] = labels

        import json
        data = self._request('POST', f'/repos/{owner}/{repo}/issues', params={}, **{
            'body': json.dumps(payload)
        })
        return GitHubIssue.from_api(data, f"{owner}/{repo}")

    # ---- 用户操作 ----

    def get_user(self, username: str) -> GitHubUser:
        """
        获取用户信息

        Args:
            username: GitHub用户名

        Returns:
            GitHubUser对象
        """
        data = self._request('GET', f'/users/{username}')
        return GitHubUser.from_api(data)

    def get_user_repos(self, username: str, sort: str = 'pushed') -> List[GitHubRepo]:
        """
        获取用户的仓库列表

        Args:
            username: 用户名
            sort: updated/pushed/created/full_name

        Returns:
            GitHubRepo列表
        """
        data = self._get_paginated(f'/users/{username}/repos', max_pages=3, params={'sort': sort})
        return [GitHubRepo.from_api(d) for d in data]

    # ---- 搜索操作 ----

    def search_repos(self, query: str, language: str = None, sort: str = 'stars',
                     order: str = 'desc', per_page: int = 30) -> List[GitHubRepo]:
        """
        搜索仓库

        Args:
            query: 搜索关键词
            language: 语言筛选（如 python, javascript）
            sort: stars/forks/updated
            order: desc/asc

        Returns:
            GitHubRepo列表
        """
        q = query
        if language:
            q = f"{query} language:{language}"

        params = {'q': q, 'sort': sort, 'order': order, 'per_page': per_page}
        data = self._request('GET', '/search/repositories', params=params)

        items = data.get('items', [])
        return [GitHubRepo.from_api(item) for item in items]

    def search_issues(self, query: str, state: str = 'open', sort: str = 'created',
                      labels: str = None) -> List[GitHubIssue]:
        """
        搜索issues

        Args:
            query: 搜索关键词
            state: open/closed/all
            sort: created/updated/comments
            labels: 逗号分隔的标签

        Returns:
            GitHubIssue列表
        """
        q = query
        if labels:
            q = f"{query} labels:{labels}"

        params = {'q': q, 'state': state, 'sort': sort}
        data = self._request('GET', '/search/issues', params=params)

        items = data.get('items', [])
        return [GitHubIssue.from_api(item) for item in items]

    # ---- Commits操作 ----

    def get_commits(self, owner: str, repo: str, path: str = None,
                    since: str = None, until: str = None,
                    author: str = None) -> List[GitHubCommit]:
        """
        获取提交记录

        Args:
            owner: 仓库所有者
            repo: 仓库名
            path: 文件路径筛选
            since: 起始日期
            until: 结束日期
            author: 作者筛选

        Returns:
            GitHubCommit列表
        """
        params = {}
        if path:
            params['path'] = path
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        if author:
            params['author'] = author

        full_repo = f"{owner}/{repo}"
        data = self._get_paginated(f'/repos/{owner}/{repo}/commits', max_pages=5, params=params)
        return [GitHubCommit.from_api(d, full_repo) for d in data]

    # ---- 速率限制查询 ----

    def get_rate_limit(self) -> Dict[str, Any]:
        """获取当前rate limit状态"""
        data = self._request('GET', '/rate_limit')
        return data.get('rate', {})

    def wait_if_needed(self, min_remaining: int = 10):
        """如果剩余请求数不足，等待"""
        if self._rate_limit_remaining is not None and self._rate_limit_remaining < min_remaining:
            if self._rate_limit_reset:
                wait = max(1, self._rate_limit_reset - time.time() + 5)
                print(f"[GitHubAPI] Low rate limit ({self._rate_limit_remaining}). Waiting {wait:.0f}s...")
                time.sleep(wait)


# ==================== 便捷函数 ====================

def get_repo_info(owner: str, repo: str, token: str = None) -> Dict:
    """快速获取仓库信息（返回dict）"""
    api = GitHubAPIAdapter(token=token)
    repo_obj = api.get_repo(owner, repo)
    return repo_obj.to_item_dict()


def search_repos(keyword: str, language: str = None, top: int = 10) -> List[Dict]:
    """快速搜索仓库（返回dict列表）"""
    api = GitHubAPIAdapter()
    repos = api.search_repos(keyword, language=language)
    return [r.to_item_dict() for r in repos[:top]]


def get_user_profile(username: str, token: str = None) -> Dict:
    """快速获取用户信息"""
    api = GitHubAPIAdapter(token=token)
    user = api.get_user(username)
    return {
        'login': user.login,
        'name': user.name,
        'bio': user.bio,
        'followers': user.followers,
        'public_repos': user.public_repos,
        'location': user.location,
    }