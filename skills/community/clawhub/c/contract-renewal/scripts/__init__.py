#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合同续租管理技能包
基于《园区运营项目客户服务标准指引》续扩租管理章节
"""

from .contract_renewal import ContractRenewalManager
from .data_manager import ContractRenewalDataManager
from .reminder_generator import ContractRenewalReminderGenerator
from .wecom_sender import WecomSender

__version__ = "1.0.0"
__author__ = "Enterprise Service Assistant"

__all__ = [
    'ContractRenewalManager',
    'ContractRenewalDataManager',
    'ContractRenewalReminderGenerator',
    'WecomSender'
]