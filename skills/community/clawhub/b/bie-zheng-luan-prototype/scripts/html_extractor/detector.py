"""
UI框架检测器模块
自动检测HTML使用的UI框架类型
"""

from typing import Dict, Any

from .config import UI_FRAMEWORK_CONFIGS


class UIFrameworkDetector:
    """UI框架自动检测器"""

    def __init__(self, soup):
        self.soup = soup
        self.detected_framework = None

    def detect_framework(self) -> str:
        """自动检测HTML使用的UI框架类型"""
        html_str = str(self.soup)

        # 检测企业后台系统特征
        if 'sider__nav' in html_str or 'sider__item' in html_str or 'pr-filter-item' in html_str:
            return 'enterprise_backend'

        # 检测通用后台系统特征
        if 'nav-item' in html_str and 'data-view' in html_str:
            if 'plan-filter-field' in html_str or 'warning-toolbar' in html_str or 'wb-overview' in html_str:
                return 'standard_backend'

        # 检测移动端H5特征
        if 'navbar' in html_str and 'viewport' in html_str:
            return 'mobile_h5'

        # 默认使用企业后台配置
        return 'enterprise_backend'

    def get_config(self, framework: str = None) -> Dict[str, Any]:
        """获取指定框架的配置"""
        if framework is None:
            framework = self.detect_framework()
        return UI_FRAMEWORK_CONFIGS.get(framework, UI_FRAMEWORK_CONFIGS['enterprise_backend'])