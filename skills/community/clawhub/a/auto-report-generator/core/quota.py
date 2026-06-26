"""额度管理模块 - 控制 AI 分析调用次数"""

import json
from pathlib import Path
from datetime import datetime, date
from typing import Literal

# 额度常量
FREE_LIMIT = 5      # 免费版：绝对计数，不清零
STD_LIMIT = 50      # 标准版：50次/月
PRO_LIMIT = 200     # 专业版：200次/月
MAX = float('inf')  # 无限制

# 额度文件路径
QUOTA_FILE = Path.home() / '.auto_report_generator' / 'quota.json'


def check_quota(tier: Literal['free', 'std', 'pro', 'max'], count: int) -> dict:
    """检查当前额度是否足够

    Args:
        tier: 用户等级 ('free', 'std', 'pro', 'max')
        count: 计划使用的次数

    Returns:
        dict: 包含 allowed (bool) 和 message (str)
    """
    current_count = _get_current_count(tier)

    if tier == 'free':
        limit = FREE_LIMIT
        period = '永久'
    elif tier == 'std':
        limit = STD_LIMIT
        period = '本月'
    elif tier == 'pro':
        limit = PRO_LIMIT
        period = '本月'
    elif tier == 'max':
        return {'allowed': True, 'message': '无限额度，无限制使用', 'remaining': '∞', 'limit': '∞'}
    else:
        return {'allowed': False, 'message': f'未知等级: {tier}', 'remaining': 0, 'limit': 0}

    remaining = limit - current_count
    allowed = remaining >= count

    if allowed:
        return {
            'allowed': True,
            'message': f'额度充足。{period}已使用 {current_count}/{limit} 次，剩余 {remaining - count} 次',
            'remaining': remaining - count,
            'limit': limit,
        }
    else:
        return {
            'allowed': False,
            'message': f'额度不足。{period}已使用 {current_count}/{limit} 次，还需 {count} 次',
            'remaining': remaining,
            'limit': limit,
        }


def increment(tier: Literal['free', 'std', 'pro', 'max']) -> int:
    """使用一次额度并返回更新后的计数

    Args:
        tier: 用户等级

    Returns:
        int: 更新后的使用次数
    """
    _ensure_quota_dir()
    quota_data = _load_quota_data()

    today = date.today()
    current_month = today.strftime('%Y-%m')

    if tier == 'free':
        quota_data.setdefault('free', 0)
        quota_data['free'] += 1
        new_count = quota_data['free']
    elif tier in ('std', 'pro'):
        monthly_key = f"{tier}_monthly"
        quota_data.setdefault(monthly_key, {})
        month_data = quota_data[monthly_key]

        if month_data.get('month') != current_month:
            month_data.clear()
            month_data['month'] = current_month
            month_data['count'] = 0

        month_data['count'] = month_data.get('count', 0) + 1
        new_count = month_data['count']
    else:
        return 0

    _save_quota_data(quota_data)
    return new_count


def _get_current_count(tier: str) -> int:
    """获取当前使用次数"""
    if tier == 'free':
        data = _load_quota_data()
        return data.get('free', 0)
    elif tier in ('std', 'pro'):
        data = _load_quota_data()
        monthly_key = f"{tier}_monthly"
        month_data = data.get(monthly_key, {})
        current_month = date.today().strftime('%Y-%m')

        if month_data.get('month') != current_month:
            return 0
        return month_data.get('count', 0)
    return 0


def _ensure_quota_dir():
    """确保额度文件目录存在"""
    QUOTA_FILE.parent.mkdir(parents=True, exist_ok=True)


def _load_quota_data() -> dict:
    """加载额度数据"""
    if not QUOTA_FILE.exists():
        return {}
    try:
        with open(QUOTA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_quota_data(data: dict):
    """保存额度数据"""
    with open(QUOTA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def reset_monthly_quota(tier: Literal['std', 'pro']):
    """手动重置月度额度（用于测试或管理员操作）"""
    data = _load_quota_data()
    monthly_key = f"{tier}_monthly"
    if monthly_key in data:
        del data[monthly_key]
    _save_quota_data(data)
