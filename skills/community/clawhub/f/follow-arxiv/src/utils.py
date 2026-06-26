"""工具函数模块"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from pathlib import Path


def get_config_dir() -> str:
    """获取用户配置目录"""
    config_dir = os.path.expanduser("~/.arxiv-search")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_config_path() -> str:
    """获取用户配置文件路径"""
    return os.path.join(get_config_dir(), "config.json")


def get_default_config() -> Dict[str, Any]:
    """获取默认配置"""
    return {
        "max_results": 10,
        "time_window_hours": 24,
        "default_query": "AI Agent",
        "search_categories": ["cs.AI", "cs.CL", "cs.LG"],
        "request_delay": 3,
        "pdf_download_dir": "~/.arxiv-search/pdfs",
        "max_retries": 3,
        "language": "zh",
        "onboarding_complete": False
    }


def load_config() -> Dict[str, Any]:
    """加载配置文件，如果不存在则返回默认配置"""
    config_path = get_config_path()

    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 合并默认配置中缺失的字段
            default_config = get_default_config()
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    else:
        # 返回默认配置
        return get_default_config()


def save_config(config: Dict[str, Any]) -> None:
    """保存配置文件到用户目录"""
    config_path = get_config_path()
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_prompts_dir() -> str:
    """获取用户提示词目录"""
    prompts_dir = os.path.join(get_config_dir(), "prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    return prompts_dir


def load_prompt(prompt_name: str) -> str:
    """
    加载提示词模板
    优先从用户目录加载，如果不存在则从项目目录加载默认模板
    """
    # 先尝试加载用户自定义提示词
    user_prompt_path = os.path.join(get_prompts_dir(), f"{prompt_name}.md")
    if os.path.exists(user_prompt_path):
        with open(user_prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    # 否则加载项目默认提示词
    default_prompt_path = os.path.join("prompts", f"{prompt_name}.md")
    if os.path.exists(default_prompt_path):
        with open(default_prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    raise FileNotFoundError(f"提示词模板 {prompt_name} 不存在")


def save_prompt(prompt_name: str, content: str) -> None:
    """保存提示词模板到用户目录"""
    prompts_dir = get_prompts_dir()
    prompt_path = os.path.join(prompts_dir, f"{prompt_name}.md")
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_time_range(hours: int = 24) -> tuple[datetime, datetime]:
    """获取时间范围"""
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    return start_time, end_time


def ensure_dir(dir_path: str) -> None:
    """确保目录存在"""
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def format_paper_metadata(papers: List[Dict[str, Any]]) -> str:
    """格式化论文元数据为可读文本"""
    formatted = []
    for i, paper in enumerate(papers, 1):
        formatted.append(f"""
### 论文 {i}: {paper['title']}
- **Arxiv ID**: {paper['arxiv_id']}
- **作者**: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}
- **发布日期**: {paper['published']}
- **分类**: {', '.join(paper['categories'])}
- **摘要**: {paper['summary'][:300]}...
""")
    return '\n'.join(formatted)
