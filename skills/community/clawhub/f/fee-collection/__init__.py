#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
费用催缴管理技能包
基于《C+基础保障服务手册》第十一章费用收缴管理规程
"""

__version__ = '1.0.0'
__author__ = '企服助手'
__description__ = '费用催缴管理技能 - 智能分级催缴、个性化话术、能耗欠费合并计算'

from .fee_collection import FeeCollectionManager

__all__ = ['FeeCollectionManager']