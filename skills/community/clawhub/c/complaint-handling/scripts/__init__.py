#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投诉处理技能包
基于《C+基础保障服务手册》第十三章客户投诉处理规程
"""

from .complaint_handler import ComplaintHandler
from .data_manager import ComplaintDataManager
from .reminder_generator import ComplaintReminderGenerator
from .wecom_sender import WecomSender

__version__ = "1.0.0"
__author__ = "Enterprise Service Assistant"

__all__ = [
    'ComplaintHandler',
    'ComplaintDataManager',
    'ComplaintReminderGenerator',
    'WecomSender'
]