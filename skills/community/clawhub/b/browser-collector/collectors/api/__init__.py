"""
collectors/api/ - API适配器

提供直接调用外部API的数据采集器，不依赖浏览器。

当前支持:
- github_api.py: GitHub REST API
"""

from collectors.api.github_api import (
    GitHubAPIAdapter,
    GitHubRepo,
    GitHubIssue,
    GitHubUser,
    GitHubCommit,
    get_repo_info,
    search_repos,
    get_user_profile,
)

__all__ = [
    'GitHubAPIAdapter',
    'GitHubRepo',
    'GitHubIssue',
    'GitHubUser',
    'GitHubCommit',
    'get_repo_info',
    'search_repos',
    'get_user_profile',
]