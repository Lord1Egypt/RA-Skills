"""
html_extractor 包
HTML原型深度解析工具，支持多种UI框架自动适配
"""

from .config import UI_FRAMEWORK_CONFIGS, get_framework_config, get_all_framework_names
from .models import (
    MenuItem, UserInfo, SidebarInfo, PageTab, SubPill,
    FilterField, TableColumn, ActionButton, StatCard,
    MessageCard, StaffCard, StatusTab, ProgressItem,
    DrawerAnchorLink, DrawerFormField, DrawerStatistics,
    DrawerPanel, TableInfo, PageView, PrototypeAnalysis,
    APIEndpoint, DatabaseTable, EntityRelation, TechImplementation,
    PageAnalysis, OperationAnalysis, FlowHypothesis, StatusTransition,
    AnalysisQuestion, InteractiveAnalysis
)
from .detector import UIFrameworkDetector
from .utils import find_by_patterns
from .extractor import EnhancedHTMLExtractor, _setup_utf8_output
from .analyzer import BusinessFlowAnalyzer
from .main import main

__all__ = [
    # 配置
    'UI_FRAMEWORK_CONFIGS',
    'get_framework_config',
    'get_all_framework_names',
    # 模型
    'MenuItem',
    'UserInfo',
    'SidebarInfo',
    'PageTab',
    'SubPill',
    'FilterField',
    'TableColumn',
    'ActionButton',
    'StatCard',
    'MessageCard',
    'StaffCard',
    'StatusTab',
    'ProgressItem',
    'DrawerAnchorLink',
    'DrawerFormField',
    'DrawerStatistics',
    'DrawerPanel',
    'TableInfo',
    'PageView',
    'PrototypeAnalysis',
    # 技术实现模型
    'APIEndpoint',
    'DatabaseTable',
    'EntityRelation',
    'TechImplementation',
    # 业务分析模型
    'PageAnalysis',
    'OperationAnalysis',
    'FlowHypothesis',
    'StatusTransition',
    'AnalysisQuestion',
    'InteractiveAnalysis',
    # 检测器
    'UIFrameworkDetector',
    # 分析器
    'BusinessFlowAnalyzer',
    # 工具
    'find_by_patterns',
    # 解析器
    'EnhancedHTMLExtractor',
    # 入口
    'main',
]

__version__ = '3.1.0'