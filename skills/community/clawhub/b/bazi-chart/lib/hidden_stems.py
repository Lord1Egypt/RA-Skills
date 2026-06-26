"""
藏干模块
查询地支中的藏干（本气、中气、余气）
"""

from .constants import HIDDEN_STEMS


def get_hidden_stems(branch):
    """
    获取地支的藏干列表
    
    Args:
        branch: 地支（如"子"、"丑"）
    
    Returns:
        list: 藏干列表，去掉 None 值（如 ["壬", "甲"]）
    """
    stems = HIDDEN_STEMS.get(branch, [])
    return [s for s in stems if s is not None]


def get_hidden_stems_with_weight(branch):
    """
    获取地支的藏干及其权重
    
    Returns:
        list of (stem, weight): 如 [("壬", 0.7), ("甲", 0.3)]
    """
    raw = HIDDEN_STEMS.get(branch, [])
    stems = [s for s in raw if s is not None]
    count = len(stems)
    
    from .constants import HIDDEN_STEM_WEIGHTS
    weights = HIDDEN_STEM_WEIGHTS.get(count, [1.0])
    
    return list(zip(stems, weights))
