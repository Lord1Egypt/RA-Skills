"""
UI框架配置模块
定义多种UI框架的CSS选择器模式，用于HTML元素定位
"""

from typing import Dict, List, Any


# ============ UI框架适配配置 ============
# 支持多种UI框架的类名映射，自动识别并适配

UI_FRAMEWORK_CONFIGS: Dict[str, Dict[str, Any]] = {
    # 企业后台系统风格（通用配置）
    'enterprise_backend': {
        'sidebar': {
            'container': ['aside.sider', 'div.sidebar'],
            'nav': ['nav.sider__nav', 'nav'],
            'group': ['div.sider__group'],
            'group_label': ['div.sider__group-label'],
            'item': ['a.sider__item', 'div.nav-item'],
            'item_text': ['span.sider__item-text'],
            'item_icon': ['span.sider__item-icon'],
            'user_container': ['div.sider__user'],
            'avatar': ['div.sider__avatar'],
            'user_name': ['div.sider__user-name'],
            'user_role': ['div.sider__user-role'],
            'toggle_btn': ['button.sider__toggle-btn'],
            'page_id_attr': 'data-scm-page',
        },
        'filter': {
            'container': ['span.pr-filter-item', 'div.filter-item', 'div.search-field'],
            'label': ['span.pr-filter-item__label', 'label'],
            'select': ['select.pr-select', 'select'],
            'input': ['input'],
        },
        'stat_card': {
            'container': ['div.stat-card'],
            'title': ['div.stat-card__title'],
            'value': ['div.stat-card__num'],
            'subtitle': ['div.stat-card__sub'],
            'icon': ['div.stat-card__icon'],
            'color_classes': {
                'blue': ['stat-card--blue', 'blue'],
                'orange': ['stat-card--orange', 'orange'],
                'purple': ['stat-card--purple', 'purple'],
                'red': ['stat-card--red', 'red'],
                'yellow': ['stat-card--yellow', 'yellow'],
                'pink': ['stat-card--pink', 'pink'],
                'green': ['stat-card--green', 'green'],
            },
        },
        'page_view': {
            'container': ['div.view', 'div.page-view', 'div.main-wrap', 'div.scm-view', 'div[data-view]', 'div[data-page]'],
        },
        'modal': {
            'container': ['div.drawer-panel', 'div.modal-overlay'],
            'header': ['div.drawer-panel__header', 'div.modal-header'],
            'title': ['span[id*="title"]', 'h2'],
            'anchor_bar': ['div.drawer-anchor-bar'],
            'anchor_link': ['a.drawer-anchor-link'],
            'body': ['div.drawer-panel__body', 'div.modal-body'],
            'footer': ['div.drawer-panel__footer', 'div.modal-footer'],
            'form_item': ['div.drawer-info-item'],
            'form_label': ['span.drawer-info-label'],
            'form_select': ['select.drawer-info-select'],
            'form_input': ['input.drawer-info-input'],
            'form_textarea': ['textarea.drawer-info-textarea'],
        },
        'status_tab': {
            'container': ['div.pr-status-group'],
            'chip': ['span.pr-status-chip'],
        },
    },

    # 通用后台系统风格（标准配置）
    'standard_backend': {
        'sidebar': {
            'container': ['aside.sidebar', 'div.sidebar'],
            'nav': ['nav'],
            'group': ['div.nav-section'],
            'group_label': ['div.nav-label'],
            'item': ['div.nav-item'],
            'item_text': ['span'],
            'item_badge': ['span.badge'],
            'toggle_btn': [],
            'user_container': [],
            'page_id_attr': 'data-view',
        },
        'filter': {
            'container': ['div.filters', 'div.plan-filter-bar', 'div.plan-filter-fields'],
            'item': ['label.plan-filter-field', 'span.plan-filter-field', 'div.warning-time-filter'],
            'label': ['span.plan-filter-label'],
            'select': ['select'],
            'input': ['input.plan-filter-inp', 'input[type="text"]', 'input[type="search"]', 'input[type="date"]'],
            'search_container': ['div.search-wrap'],
        },
        'stat_card': {
            'container': ['div.wb-overview', 'div.plan-stats', 'div.ship-stat-cards', 'div.stat-card'],
            'title': ['span', 'div.stat-title', 'div.stat-label'],
            'value': ['strong', 'span.stat-value', 'div.stat-num'],
            'subtitle': ['small', 'div.stat-sub'],
            'icon': [],
            'color_classes': {
                'blue': ['blue', 'primary'],
                'orange': ['orange', 'warning'],
                'red': ['red', 'danger'],
                'green': ['green', 'success'],
            },
        },
        'page_view': {
            'container': ['div.view', 'div[data-view]', 'div.plan-body', 'div.ship-body'],
            'id_prefix': 'view',
        },
        'modal': {
            'container': ['div.modal-overlay'],
            'header': ['div.modal-header'],
            'title': ['h2'],
            'body': ['div.modal-body'],
            'footer': ['div.modal-footer'],
            'close_btn': ['button.btn-close'],
        },
        'status_tab': {
            'container': ['div.plan-stats'],
            'chip': ['span'],
        },
    },

    # 通用移动端H5风格
    'mobile_h5': {
        'sidebar': {
            'container': [],
            'nav': ['nav.navbar', 'div.navbar'],
            'item': ['a.nav-item', 'button.nav-item'],
            'item_text': ['span'],
        },
        'filter': {
            'container': ['div.search-bar', 'div.filter-bar'],
            'label': ['span', 'label'],
            'select': ['select'],
            'input': ['input'],
        },
        'stat_card': {
            'container': ['div.card', 'div.stat-card'],
            'title': ['div.card-title', 'div.stat-title'],
            'value': ['div.card-value', 'span.stat-value'],
            'subtitle': ['div.card-subtitle'],
            'icon': [],
            'color_classes': {
                'blue': ['card-blue', 'primary'],
                'orange': ['card-orange', 'warning'],
                'red': ['card-red', 'danger'],
                'green': ['card-green', 'success'],
            },
        },
        'page_view': {
            'container': ['div.page-body', 'div.content', 'div[data-page]'],
        },
        'modal': {
            'container': ['div.modal', 'div.popup'],
            'header': ['div.modal-header', 'div.header'],
            'body': ['div.modal-body', 'div.body'],
            'footer': ['div.modal-footer', 'div.footer'],
        },
    },
}


def get_framework_config(framework_name: str) -> Dict[str, Any]:
    """获取指定框架的配置"""
    return UI_FRAMEWORK_CONFIGS.get(framework_name, UI_FRAMEWORK_CONFIGS['enterprise_backend'])


def get_all_framework_names() -> List[str]:
    """获取所有支持的框架名称"""
    return list(UI_FRAMEWORK_CONFIGS.keys())