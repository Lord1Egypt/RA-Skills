"""
招聘搜索技能包
支持BOSS直聘、智联招聘、前程无忧三大平台
"""

__version__ = "1.0.0"
__author__ = "OpenClaw"
__description__ = "招聘网站岗位搜索技能"

from .job_searcher import JobSearcher, Job
from .openclaw_integration import JobSearchSkill

__all__ = [
    'JobSearcher',
    'Job', 
    'JobSearchSkill'
]