#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto-accounting - 自动记账 Skill
Copyright (c) 2026 摇摇

本软件受著作权法保护。虽然采用 MIT-0 许可证允许商用，
但必须保留原始版权声明。

禁止：
- 移除或修改版权声明
- 声称为自己开发
- 在非授权环境使用

官方环境：小艺 Claw + 一日记账 APP
联系方式：QQ 2756077825
"""

"""
用户偏好配置管理
管理用户的记账偏好设置
"""

import json
import os
from typing import Dict, Any, Optional


class UserPreferences:
    """用户记账偏好管理"""
    
    DEFAULT_PREFERENCES = {
        "default_payment_method": "微信支付",
        "confirm_before_save": False,
        "custom_categories": {},
        "excluded_keywords": ["测试", "demo", "test"],
        "large_amount_threshold": 1000,
        "auto_categorize": True,
        "save_history": True,
        "notification_enabled": True
    }
    
    def __init__(self, preferences_path: Optional[str] = None):
        """
        初始化用户偏好
        
        Args:
            preferences_path: 偏好配置文件路径
        """
        self.preferences_path = preferences_path
        self.preferences = self._load_preferences()
    
    def _load_preferences(self) -> Dict[str, Any]:
        """加载用户偏好"""
        if self.preferences_path and os.path.exists(self.preferences_path):
            try:
                with open(self.preferences_path, 'r', encoding='utf-8') as f:
                    user_prefs = json.load(f)
                    # 合并默认偏好
                    return {**self.DEFAULT_PREFERENCES, **user_prefs}
            except (json.JSONDecodeError, IOError):
                pass
        return self.DEFAULT_PREFERENCES.copy()
    
    def save_preferences(self) -> bool:
        """保存用户偏好"""
        if not self.preferences_path:
            return False
        try:
            os.makedirs(os.path.dirname(self.preferences_path), exist_ok=True)
            with open(self.preferences_path, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取偏好设置"""
        return self.preferences.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置偏好"""
        self.preferences[key] = value
    
    def get_default_payment_method(self) -> str:
        """获取默认支付方式"""
        return self.get("default_payment_method", "微信支付")
    
    def should_confirm_before_save(self, amount: float) -> bool:
        """
        判断是否需要在保存前确认
        
        Args:
            amount: 金额
            
        Returns:
            是否需要确认
        """
        # 如果设置了始终确认
        if self.get("confirm_before_save", False):
            return True
        # 如果金额超过大额阈值
        threshold = self.get("large_amount_threshold", 1000)
        return amount >= threshold
    
    def get_custom_category(self, keyword: str) -> Optional[str]:
        """
        获取自定义分类
        
        Args:
            keyword: 关键词
            
        Returns:
            分类名称或 None
        """
        custom_categories = self.get("custom_categories", {})
        for category, keywords in custom_categories.items():
            if keyword in keywords:
                return category
        return None
    
    def is_excluded(self, keyword: str) -> bool:
        """
        判断关键词是否被排除
        
        Args:
            keyword: 关键词
            
        Returns:
            是否排除
        """
        excluded = self.get("excluded_keywords", [])
        return keyword.lower() in [k.lower() for k in excluded]
    
    def add_custom_category(self, category: str, keywords: list) -> None:
        """
        添加自定义分类
        
        Args:
            category: 分类名称
            keywords: 关键词列表
        """
        custom_categories = self.get("custom_categories", {})
        custom_categories[category] = keywords
        self.set("custom_categories", custom_categories)
    
    def add_excluded_keyword(self, keyword: str) -> None:
        """
        添加排除关键词
        
        Args:
            keyword: 关键词
        """
        excluded = self.get("excluded_keywords", [])
        if keyword not in excluded:
            excluded.append(keyword)
            self.set("excluded_keywords", excluded)
    
    def reset_to_default(self) -> None:
        """重置为默认偏好"""
        self.preferences = self.DEFAULT_PREFERENCES.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.preferences.copy()


# 全局偏好实例
_preferences_instance: Optional[UserPreferences] = None


def get_preferences() -> UserPreferences:
    """获取全局偏好实例"""
    global _preferences_instance
    if _preferences_instance is None:
        _preferences_instance = UserPreferences()
    return _preferences_instance


def init_preferences(preferences_path: Optional[str] = None) -> UserPreferences:
    """
    初始化全局偏好
    
    Args:
        preferences_path: 偏好配置文件路径
        
    Returns:
        UserPreferences 实例
    """
    global _preferences_instance
    _preferences_instance = UserPreferences(preferences_path)
    return _preferences_instance
