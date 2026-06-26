"""
核心HTML解析器模块
深度解析HTML原型，提取菜单、筛选、表格、按钮等完整信息
"""

import io
import sys
import json
import re
from datetime import datetime
from dataclasses import asdict
from typing import List, Dict, Any

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("错误: 需要安装BeautifulSoup4")
    print("请运行: pip install beautifulsoup4 lxml html5lib")
    sys.exit(1)

from .config import UI_FRAMEWORK_CONFIGS
from .detector import UIFrameworkDetector
from .utils import find_by_patterns
from .models import (
    MenuItem, UserInfo, SidebarInfo, PageTab, SubPill,
    FilterField, TableColumn, ActionButton, StatCard,
    MessageCard, StaffCard, StatusTab, ProgressItem,
    DrawerAnchorLink, DrawerFormField, DrawerStatistics,
    DrawerPanel, TableInfo, PageView, PrototypeAnalysis,
    APIEndpoint, DatabaseTable, EntityRelation, TechImplementation,
    InteractiveAnalysis
)
from .analyzer import BusinessFlowAnalyzer

# 设置标准输出编码为UTF-8（仅在直接运行时）
def _setup_utf8_output():
    """设置UTF-8输出编码（仅在需要时调用）"""
    try:
        if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass


class EnhancedHTMLExtractor:
    """通用HTML提取器 v2.8.0 - 支持多种UI框架自动适配，增强技术实现推断"""

    def __init__(self, html_content: str, url: str = ""):
        self.soup = BeautifulSoup(html_content, 'lxml')
        self.url = url
        # 自动检测UI框架类型
        self.detector = UIFrameworkDetector(self.soup)
        self.framework = self.detector.detect_framework()
        self.config = self.detector.get_config(self.framework)

    def extract_full_structure(self) -> PrototypeAnalysis:

        # 1. 系统名称
        title = self.soup.title.string if self.soup.title else ""
        system_name = self._extract_system_name(title)

        # 2. 菜单结构
        menus = self._extract_sidebar_menu()

        # 3. 侧边栏信息
        sidebar = self._extract_sidebar_info()

        # 4. 页面标签栏
        page_tabs = self._extract_page_tabs()

        # 5. 页面视图（传入菜单用于名称匹配）
        page_views = self._extract_all_page_views(menus)

        # 6. 统计
        total_filters = sum(len(pv.filters) for pv in page_views)
        total_columns = sum(sum(len(t.columns) for t in pv.tables) for pv in page_views)
        total_buttons = sum(len(pv.buttons) for pv in page_views)

        # 7. 生成技术实现建议（增强版）
        tech_implementation = self._generate_tech_implementation(menus, page_views)

        return PrototypeAnalysis(
            system_name=system_name,
            title=title,
            menus=menus,
            sidebar=sidebar,
            page_tabs=page_tabs,
            page_views=page_views,
            total_filters=total_filters,
            total_columns=total_columns,
            total_buttons=total_buttons,
            analysis_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tech_implementation=tech_implementation
        )

    def extract_interactive_analysis(self) -> InteractiveAnalysis:
        """
        提取交互式分析结果
        分析业务流程，推断状态流转，生成问题让用户确认
        """
        # 1. 获取基础结构
        analysis = self.extract_full_structure()

        # 2. 使用业务流程分析器
        analyzer = BusinessFlowAnalyzer(analysis.menus, analysis.page_views)
        interactive = analyzer.analyze()

        # 3. 填充系统名称
        interactive.system_name = analysis.system_name

        return interactive

    def to_interactive_markdown(self, interactive: InteractiveAnalysis) -> str:
        """
        将交互式分析结果转换为Markdown格式
        """
        md_lines = []

        # 标题
        md_lines.append("# 原型业务分析报告")
        md_lines.append("")
        md_lines.append(f"**系统名称**: {interactive.system_name}")
        md_lines.append("")

        # 分析总结
        md_lines.append("## 一、分析总结")
        md_lines.append("")
        md_lines.append(interactive.analysis_summary)
        md_lines.append("")

        # 流程假设
        md_lines.append("## 二、业务流程假设")
        md_lines.append("")

        if interactive.flow_hypothesis.sequence:
            md_lines.append("### 流程顺序")
            md_lines.append("")
            md_lines.append("```")
            md_lines.append(" → ".join(interactive.flow_hypothesis.sequence[:10]))
            if len(interactive.flow_hypothesis.sequence) > 10:
                md_lines.append(" → ...")
            md_lines.append("```")
            md_lines.append("")
            md_lines.append(f"**置信度**: {interactive.flow_hypothesis.confidence:.0%}")
            md_lines.append("")

            md_lines.append("**推断依据**:")
            md_lines.append("")
            for ev in interactive.flow_hypothesis.evidence:
                md_lines.append(f"- {ev}")
            md_lines.append("")

        # 页面功能分析
        md_lines.append("## 三、页面功能分析")
        md_lines.append("")

        for pa in interactive.page_analyses:
            md_lines.append(f"### {pa.page_name}")
            md_lines.append("")
            md_lines.append(f"- **页面角色**: {pa.inferred_role}")
            md_lines.append(f"- **视图ID**: `{pa.view_id}`")

            if pa.has_checkbox:
                md_lines.append(f"- **支持批量操作**: 是")

            md_lines.append("")

            # 操作列表
            if pa.operations:
                md_lines.append("**可执行操作**:")
                md_lines.append("")
                md_lines.append("| 操作 | 类别 | 需要勾选 | 可能状态 |")
                md_lines.append("|-----|------|---------|---------|")
                for op in pa.operations:
                    states_str = ", ".join(op.possible_states[:2])
                    selection_str = "✓" if op.requires_selection else "-"
                    md_lines.append(f"| {op.name} | {op.category} | {selection_str} | {states_str} |")
                md_lines.append("")

            # 关键字段
            if pa.key_fields:
                md_lines.append(f"**关键字段**: {', '.join(pa.key_fields[:8])}{'...' if len(pa.key_fields) > 8 else ''}")
                md_lines.append("")

            # 筛选维度
            if pa.filter_dimensions:
                md_lines.append(f"**筛选维度**: {', '.join(pa.filter_dimensions[:5])}{'...' if len(pa.filter_dimensions) > 5 else ''}")
                md_lines.append("")

            md_lines.append("---")
            md_lines.append("")

        # 状态流转
        if interactive.status_transitions:
            md_lines.append("## 四、状态流转假设")
            md_lines.append("")

            for trans in interactive.status_transitions:
                md_lines.append(f"### {trans.page_name} - {trans.status_field}")
                md_lines.append("")

                if trans.possible_values:
                    md_lines.append(f"**可能的状态值**: {', '.join(trans.possible_values)}")
                    md_lines.append("")

                if trans.transitions:
                    md_lines.append("**推断的流转规则**:")
                    md_lines.append("")
                    for rule in trans.transitions:
                        md_lines.append(f"- {rule}")
                    md_lines.append("")

                md_lines.append("---")
                md_lines.append("")

        # 需要确认的问题
        md_lines.append("## 五、需要确认的问题")
        md_lines.append("")

        # 按优先级分组
        high_questions = [q for q in interactive.questions if q.priority == 'high']
        medium_questions = [q for q in interactive.questions if q.priority == 'medium']
        low_questions = [q for q in interactive.questions if q.priority == 'low']

        if high_questions:
            md_lines.append("### 高优先级（流程和状态相关）")
            md_lines.append("")
            for i, q in enumerate(high_questions, 1):
                md_lines.append(f"**Q{i}: {q.question}**")
                md_lines.append("")
                if q.context:
                    md_lines.append(f"> 推断依据：{q.context}")
                    md_lines.append("")
                if q.options:
                    md_lines.append("建议选项：")
                    for opt in q.options:
                        md_lines.append(f"- [ ] {opt}")
                    md_lines.append("")
                md_lines.append("您的回答：_____")
                md_lines.append("")
                md_lines.append("---")
                md_lines.append("")

        if medium_questions:
            md_lines.append("### 中优先级（操作和权限相关）")
            md_lines.append("")
            for i, q in enumerate(medium_questions, 1):
                md_lines.append(f"**Q{i}: {q.question}**")
                md_lines.append("")
                if q.context:
                    md_lines.append(f"> 推断依据：{q.context}")
                    md_lines.append("")
                if q.options:
                    md_lines.append("建议选项：")
                    for opt in q.options:
                        md_lines.append(f"- [ ] {opt}")
                    md_lines.append("")
                md_lines.append("您的回答：_____")
                md_lines.append("")
                md_lines.append("---")
                md_lines.append("")

        if low_questions:
            md_lines.append("### 低优先级（字段细节）")
            md_lines.append("")
            for i, q in enumerate(low_questions, 1):
                md_lines.append(f"**Q{i}: {q.question}**")
                md_lines.append("")
                if q.context:
                    md_lines.append(f"> 推断依据：{q.context}")
                    md_lines.append("")
                md_lines.append("您的回答：_____")
                md_lines.append("")

        # 结尾
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("*请根据以上分析结果，确认或修正AI的推断。*")
        md_lines.append("*对于标记为高优先级的问题，请优先回答。*")

        return "\n".join(md_lines)

    def _extract_system_name(self, title: str) -> str:
        """从标题提取系统名称"""
        if ' - ' in title:
            return title.split(' - ')[0]
        return title

    def _extract_sidebar_menu(self) -> List[MenuItem]:
        """提取侧边栏菜单结构（通用版 - 支持多种UI框架）"""
        menus = []
        sidebar_config = self.config.get('sidebar', {})

        # 根据配置查找侧边栏容器
        container_patterns = sidebar_config.get('container', ['aside.sider', 'div.sidebar', 'aside.sidebar'])
        nav_patterns = sidebar_config.get('nav', ['nav.sider__nav', 'nav'])
        group_patterns = sidebar_config.get('group', ['div.sider__group', 'div.nav-section'])
        group_label_patterns = sidebar_config.get('group_label', ['div.sider__group-label', 'div.nav-label'])
        item_patterns = sidebar_config.get('item', ['a.sider__item', 'div.nav-item'])
        item_text_patterns = sidebar_config.get('item_text', ['span.sider__item-text', 'span'])
        item_icon_patterns = sidebar_config.get('item_icon', ['span.sider__item-icon'])
        page_id_attr = sidebar_config.get('page_id_attr', 'data-scm-page')

        # 查找侧边栏容器
        sidebar_container = find_by_patterns(self.soup, container_patterns)
        if not sidebar_container:
            return menus

        # 查找导航区域
        nav_area = find_by_patterns(sidebar_container, nav_patterns) if sidebar_container else None
        if not nav_area:
            nav_area = sidebar_container

        # 查找菜单分组
        groups = find_by_patterns(nav_area, group_patterns, find_all=True)
        if not groups:
            # 如果没有分组，直接查找菜单项
            items = find_by_patterns(nav_area, item_patterns, find_all=True)
            if items:
                for item in items:
                    self._add_menu_item(menus, item, "默认菜单", item_text_patterns, item_icon_patterns, page_id_attr)
            return menus

        # 遍历分组提取菜单项
        for group in groups:
            # 获取分组名称
            group_label = find_by_patterns(group, group_label_patterns)
            group_name = group_label.get_text(strip=True) if group_label else "未分组"

            # 获取菜单项
            items = find_by_patterns(group, item_patterns, find_all=True)
            for item in items:
                self._add_menu_item(menus, item, group_name, item_text_patterns, item_icon_patterns, page_id_attr)

        return menus

    def _add_menu_item(self, menus, item, group_name, text_patterns, icon_patterns, page_id_attr):
        """添加菜单项到列表"""
        # 获取菜单文本
        item_text = find_by_patterns(item, text_patterns)
        menu_name = item_text.get_text(strip=True) if item_text else ""
        if not menu_name:
            menu_name = item.get_text(strip=True)

        if not menu_name:
            return

        # 提取SVG图标代码
        icon_desc = ""
        icon_svg = ""
        if icon_patterns:
            item_icon = find_by_patterns(item, icon_patterns)
            if item_icon:
                svg = item_icon.find('svg')
                if svg:
                    icon_svg = str(svg)
                    icon_desc = self._infer_icon_from_svg(svg)

        # 获取页面标识
        page_id = item.get(page_id_attr, '') or item.get('data-view', '') or item.get('href', '')
        href = item.get('href', '')
        is_active = 'is-active' in item.get('class', []) or 'active' in item.get('class', [])

        menus.append(MenuItem(
            group=group_name,
            name=menu_name,
            icon=icon_desc,
            icon_svg=icon_svg,
            page_id=page_id,
            href=href,
            is_active=is_active
        ))

    def _extract_sidebar_info(self) -> SidebarInfo:
        """提取侧边栏信息（使用可配置模式）"""
        has_toggle = False
        toggle_button_id = ""
        user_info = UserInfo(avatar_text="", name="", role="")

        sidebar_config = self.config.get('sidebar', {})
        container_patterns = sidebar_config.get('container', ['aside.sider', 'div.sidebar'])

        sider = find_by_patterns(self.soup, container_patterns)

        if sider:
            # 折叠按钮
            toggle_patterns = sidebar_config.get('toggle_btn', ['button.sider__toggle-btn', 'button.sidebar-toggle'])
            toggle_btn = find_by_patterns(sider, toggle_patterns)
            if toggle_btn:
                has_toggle = True
                toggle_button_id = toggle_btn.get('id', 'sider-toggle-btn')

            # 用户信息
            user_patterns = sidebar_config.get('user_container', ['div.sider__user', 'div.user-info'])
            user_elem = find_by_patterns(sider, user_patterns)
            if user_elem:
                avatar_patterns = sidebar_config.get('avatar', ['div.sider__avatar', 'div.avatar'])
                avatar = find_by_patterns(user_elem, avatar_patterns)
                avatar_text = avatar.get_text(strip=True) if avatar else ""

                name_patterns = sidebar_config.get('user_name', ['div.sider__user-name', 'div.user-name'])
                name_elem = find_by_patterns(user_elem, name_patterns)
                name = name_elem.get_text(strip=True) if name_elem else ""

                role_patterns = sidebar_config.get('user_role', ['div.sider__user-role', 'div.user-role'])
                role_elem = find_by_patterns(user_elem, role_patterns)
                role = role_elem.get_text(strip=True) if role_elem else ""

                user_info = UserInfo(avatar_text=avatar_text, name=name, role=role)

        return SidebarInfo(has_toggle=has_toggle, toggle_button_id=toggle_button_id, user_info=user_info)

    def _extract_page_tabs(self) -> list:
        """提取页面标签栏"""
        tabs = []

        tabs_bar = self.soup.find('div', class_='page-tabs-bar')
        if not tabs_bar:
            return tabs

        page_tabs_container = tabs_bar.find('div', class_='page-tabs')
        if not page_tabs_container:
            return tabs

        tab_elems = page_tabs_container.find_all('div', class_='page-tab')
        for tab in tab_elems:
            tab_name = tab.get_text(strip=True)
            # 移除关闭按钮的SVG内容
            close_svg = tab.find('svg', class_='page-tab__close')
            if close_svg:
                close_svg_text = close_svg.get_text(strip=True)
                tab_name = tab_name.replace(close_svg_text, '').strip()

            is_active = 'page-tab--active' in tab.get('class', [])
            has_close = close_svg is not None

            tabs.append(PageTab(name=tab_name, is_active=is_active, has_close=has_close))

        return tabs

    def _infer_icon_from_svg(self, svg) -> str:
        """从SVG精确推断图标类型（优化版）"""
        svg_str = str(svg)

        icon_patterns = {
            '工作台图标': ['rect x="3" y="3"', 'width="7" height="9"', 'rect x="14" y="3"'],
            '收件箱图标': ['M22 12h-6', 'M9 12h6', 'inbox'],
            '文档图标': ['M9 12h6m-6 4h6', 'M7 2h5.586', 'document'],
            '编辑图标': ['M11 5H6a2 2 0 00-2 2v11', 'M11.828 15H9', 'edit'],
            '功能图标': ['rect x="3" y="4" width="18" height="16"', 'M7 8h10'],
            '日历图标': ['rect x="3" y="4" width="18" height="18"', 'M16 2v4M8 2v4', 'calendar'],
            '银行卡图标': ['rect x="2" y="5" width="20" height="14"', 'M2 10h20', 'payment'],
            '下载图标': ['M4 16v2a2 2 0 002 2h12', 'M8 12l4 4 4-4m-4-4v8', 'download', 'upload'],
            '验证图标': ['M9 12l2 2 4-4m6 2a9 9 0 11-18 0', 'check', 'verify'],
            '警告图标': ['circle cx="12" cy="12" r="10"', 'M12 8v4M12 16h.01', 'warning'],
            '时钟图标': ['circle cx="12" cy="12" r="10"', 'M12 6v6l4 2', 'clock', 'time'],
            '禁止图标': ['circle cx="12" cy="12" r="10"', 'M4.5 4.5l15 15', 'forbidden', 'ban'],
            '消息图标': ['M21 15a4 4 0 01-4 4H7', 'M21 11.5a8.38', 'message'],
            '用户图标': ['M17 21v-2a4 4 0 00-4-4H5', 'circle cx="9" cy="7" r="4"', 'user', 'avatar'],
            '搜索图标': ['circle cx="11" cy="11" r="8"', 'M21 21l-4.35-4.35', 'search'],
            '设置图标': ['circle cx="12" cy="12" r="3"', 'gear', 'settings'],
            '文件夹图标': ['M22 19a2 2 0 01-2 2H4a2', 'folder'],
        }

        for icon_name, patterns in icon_patterns.items():
            for pattern in patterns:
                if pattern in svg_str:
                    return icon_name

        aria_label = svg.get('aria-label', '')
        if aria_label:
            return f"{aria_label}图标"

        return "功能图标"

    def _extract_all_page_views(self, menus: list = None) -> list:
        """提取所有页面视图（使用可配置模式）"""
        # 构建 view_id → 菜单名称 的映射
        menu_name_map = {}
        if menus:
            for menu in menus:
                if menu.page_id:
                    menu_name_map[menu.page_id.lower()] = menu.name
        page_views = []

        view_config = self.config.get('page_view', {})
        view_patterns = view_config.get('container', ['div.view', 'div.page-view', 'div.main-wrap', 'div[data-view]', 'div[data-page]'])

        view_containers = find_by_patterns(self.soup, view_patterns, find_all=True)

        if not view_containers:
            data_view_elements = self.soup.find_all(attrs={'data-view': True})
            view_containers.extend(data_view_elements)
            data_page_elements = self.soup.find_all(attrs={'data-page': True})
            view_containers.extend(data_page_elements)

        # 过滤无效的视图容器
        invalid_view_patterns = ['nav-item', 'nav-', 'menu-', 'sidebar', 'sider']

        for container in view_containers:
            view_id = container.get('id', '')
            if not view_id:
                classes = container.get('class', [])
                if isinstance(classes, list) and classes:
                    view_id = classes[0]

            # 过滤无效的视图ID
            if not view_id or any(pattern in view_id for pattern in invalid_view_patterns):
                continue

            # 检查容器是否包含实际内容
            has_content = container.find('table') or container.find('button') or container.find('form') or container.find('input')
            if not has_content and not container.find('div', class_=lambda x: x and ('stat' in x or 'card' in x or 'overview' in x) if x else False):
                continue

            view_name = self._infer_page_name(view_id, container)

            # 使用菜单名称覆盖（如果匹配到）
            if menu_name_map:
                # view_id 如 "viewWarning" 或 "scm-view-purchase-booking" → 提取关键部分匹配 menu page_id
                id_part = view_id
                for prefix in ['scm-view-', 'view-', 'view', 'page-', 'page']:
                    if id_part.lower().startswith(prefix):
                        id_part = id_part[len(prefix):]
                        break
                id_key = id_part.lower().replace('-', '').replace('_', '')
                # 同时标准化 menu key（去掉连字符）
                normalized_map = {k.replace('-', '').replace('_', ''): v for k, v in menu_name_map.items()}
                if id_key in normalized_map:
                    view_name = normalized_map[id_key]

            # 跳过加载指示器等无效页面
            if view_name in ['加载中…', '加载中...', 'Loading', 'loading']:
                continue

            # 提取各组件
            sub_pills = self._extract_sub_pills(container)
            filters = self._extract_filter_fields(container)
            tables = self._extract_tables(container)
            buttons = self._extract_buttons(container)
            stat_cards = self._extract_stat_cards(container)
            message_cards = self._extract_message_cards(container)
            staff_cards = self._extract_staff_cards(container)
            status_tabs = self._extract_status_tabs(container)
            progress_items = self._extract_progress_items(container)
            drawer_panels = self._extract_drawer_panels(container)

            page_views.append(PageView(
                view_id=view_id,
                name=view_name,
                filters=filters,
                tables=tables,
                buttons=buttons,
                stat_cards=stat_cards,
                message_cards=message_cards,
                staff_cards=staff_cards,
                sub_pills=sub_pills,
                status_tabs=status_tabs,
                progress_items=progress_items,
                drawer_panels=drawer_panels
            ))

        # 如果没有找到明确的视图容器
        if not page_views:
            tables = self.soup.find_all('table')
            if tables:
                filters = self._extract_filter_fields(self.soup)
                tables_info = self._extract_tables(self.soup)
                buttons = self._extract_buttons(self.soup)
                stat_cards = self._extract_stat_cards(self.soup)
                message_cards = self._extract_message_cards(self.soup)
                staff_cards = self._extract_staff_cards(self.soup)
                status_tabs = self._extract_status_tabs(self.soup)
                progress_items = self._extract_progress_items(self.soup)
                drawer_panels = self._extract_drawer_panels(self.soup)

                page_views.append(PageView(
                    view_id='main-content',
                    name='主页面',
                    filters=filters,
                    tables=tables_info,
                    buttons=buttons,
                    stat_cards=stat_cards,
                    message_cards=message_cards,
                    staff_cards=staff_cards,
                    sub_pills=[],
                    status_tabs=status_tabs,
                    progress_items=progress_items,
                    drawer_panels=drawer_panels
                ))

        return page_views

    def _extract_sub_pills(self, container) -> list:
        """提取子标签"""
        pills = []

        sub_pills_container = container.find('div', class_='sub-pills')
        if sub_pills_container:
            pill_elems = sub_pills_container.find_all('button', class_='sub-pill')
            for pill in pill_elems:
                pill_name = pill.get_text(strip=True)
                pill_id = pill.get('id', '')
                is_active = 'sub-pill--active' in pill.get('class', [])
                target_panel = pill.get('data-workbench', '')

                pills.append(SubPill(
                    name=pill_name,
                    pill_id=pill_id,
                    is_active=is_active,
                    target_panel=target_panel
                ))

        return pills

    def _infer_page_name(self, view_id: str, container) -> str:
        """推断页面名称"""
        title_elem = container.find(['h1', 'h2', 'h3'])
        if title_elem:
            text = title_elem.get_text(strip=True)
            if text and text not in ['加载中…', '加载中...', 'Loading']:
                return text

        page_title = container.find('title')
        if page_title:
            return page_title.get_text(strip=True)

        if container.get('data-title'):
            return container.get('data-title')
        if container.get('aria-label'):
            return container.get('aria-label')

        if view_id:
            # 去掉常见前缀
            clean_id = view_id
            for prefix in ['view-', 'view', 'page-', 'page']:
                if clean_id.lower().startswith(prefix):
                    clean_id = clean_id[len(prefix):]
                    break
            # camelCase 拆分
            words = re.sub(r'([a-z])([A-Z])', r'\1 \2', clean_id).replace('-', ' ').replace('_', ' ').split()
            if words:
                return ' '.join(word.capitalize() for word in words)
            return view_id

        return '未命名页面'

    def _extract_filter_fields(self, container) -> list:
        """提取筛选条件（使用可配置模式）"""
        filters = []

        filter_config = self.config.get('filter', {})
        item_patterns = filter_config.get('item', ['span.pr-filter-item', 'div.filter-item', 'div.search-field'])
        label_patterns = filter_config.get('label', ['span.pr-filter-item__label', 'label'])

        filter_items = find_by_patterns(container, item_patterns, find_all=True)

        for item in filter_items:
            label_elem = find_by_patterns(item, label_patterns)
            field_name = label_elem.get_text(strip=True) if label_elem else ""

            if not field_name:
                continue

            filter_id = item.get('data-filter-id', '') or item.get('id', '')

            select_elem = item.find('select')
            input_elem = item.find('input')

            if select_elem:
                options = []
                default_value = ""
                for opt in select_elem.find_all('option'):
                    opt_text = opt.get_text(strip=True)
                    if opt_text:
                        options.append(opt_text)
                    if opt.get('selected'):
                        default_value = opt_text

                filters.append(FilterField(
                    name=field_name,
                    type='select',
                    options=options,
                    placeholder='',
                    filter_id=filter_id,
                    default_value=default_value
                ))

            elif input_elem:
                input_type = input_elem.get('type', 'text')
                placeholder = input_elem.get('placeholder', '')
                default_value = input_elem.get('value', '')

                filters.append(FilterField(
                    name=field_name,
                    type=input_type,
                    options=[],
                    placeholder=placeholder,
                    filter_id=filter_id,
                    default_value=default_value
                ))

            else:
                filters.append(FilterField(
                    name=field_name,
                    type='unknown',
                    options=[],
                    placeholder='',
                    filter_id=filter_id,
                    default_value=''
                ))

        return filters

    def _extract_tables(self, container) -> list:
        """提取表格信息"""
        tables_info = []

        tables = container.find_all('table')
        for idx, table in enumerate(tables):
            table_class = ' '.join(table.get('class', []))

            is_main_table = idx == 0
            if 'detail' in table_class.lower() or 'sub' in table_class.lower():
                is_main_table = False
            if 'main' in table_class.lower():
                is_main_table = True

            columns = []
            has_checkbox = False

            thead = table.find('thead')
            tbody = table.find('tbody')

            if thead:
                header_cells = thead.find_all('th')
                col_names = []
                for th in header_cells:
                    col_name = th.get_text(strip=True)
                    col_names.append(col_name)

                if col_names and col_names[0] in ['', '全选', '选择', '□']:
                    has_checkbox = True

                col_types = []
                if tbody:
                    first_data_row = tbody.find('tr')
                    if first_data_row:
                        data_cells = first_data_row.find_all('td')
                        for i, td in enumerate(data_cells):
                            col_types.append(self._infer_cell_type(td, col_names[i] if i < len(col_names) else ''))
                    else:
                        col_types = ['text'] * len(col_names)
                else:
                    col_types = ['text'] * len(col_names)

                for i, col_name in enumerate(col_names):
                    if col_name in ['', '全选', '选择', '□']:
                        continue

                    data_type = col_types[i] if i < len(col_types) else 'text'
                    columns.append(TableColumn(
                        name=col_name,
                        data_type=data_type,
                        sortable=False,
                        table_index=idx,
                        is_detail=not is_main_table
                    ))

            tables_info.append(TableInfo(
                table_index=idx,
                table_class=table_class,
                is_main_table=is_main_table,
                columns=columns,
                has_checkbox=has_checkbox
            ))

        return tables_info

    def _infer_cell_type(self, cell, col_name: str = '') -> str:
        """从单元格内容和列名推断数据类型"""
        col_name_lower = col_name.lower()
        if any(kw in col_name_lower for kw in ['单号', '编号', '编码', '账号']):
            return 'link'
        if any(kw in col_name_lower for kw in ['日期', '时间', '创建时间', '审核时间']):
            return 'date'
        if any(kw in col_name_lower for kw in ['数量', '金额', '单价', '总价', '合计']):
            return 'number'
        if any(kw in col_name_lower for kw in ['价格', '金额', '单价']) and '¥' in cell.get_text():
            return 'currency'
        if any(kw in col_name_lower for kw in ['率', '百分比', '占比']):
            return 'percentage'
        if any(kw in col_name_lower for kw in ['状态', '进度', '审核状态', '确认状态']):
            return 'badge'
        if any(kw in col_name_lower for kw in ['图片', '照片', '缩略图', '头像']):
            return 'image'

        # 基于class推断
        cell_classes = cell.get('class', [])
        if isinstance(cell_classes, str):
            cell_classes = [cell_classes]

        if any('num' in str(cls).lower() for cls in cell_classes):
            return 'number'
        if any('thumb' in str(cls).lower() or 'img' in str(cls).lower() for cls in cell_classes):
            return 'image'
        if any('badge' in str(cls).lower() or 'tag' in str(cls).lower() for cls in cell_classes):
            return 'badge'

        # 基于内容推断
        cell_text = cell.get_text(strip=True)

        if not cell_text or cell_text in ['—', '-', '']:
            return 'empty'

        if re.match(r'\d{4}-\d{2}-\d{2}', cell_text) or re.match(r'\d{2}:\d{2}', cell_text):
            return 'date'

        if re.match(r'^[\d,.\-¥￥%]+$', cell_text) and cell_text:
            if '%' in cell_text:
                return 'percentage'
            if '¥' in cell_text or '￥' in cell_text:
                return 'currency'
            if re.match(r'^\d+[,.]?\d*$', cell_text):
                return 'number'

        link = cell.find('a') or cell.find('span', class_='pr-num-link')
        if link:
            return 'link'

        img = cell.find('img')
        if img:
            return 'image'

        badge = cell.find('span', class_=lambda x: x and ('badge' in x or 'tag' in x) if x else False)
        if badge:
            return 'badge'

        progress = cell.find('div', class_=lambda x: x and 'progress' in x if x else False)
        if progress:
            return 'progress'

        return 'text'

    def _extract_buttons(self, container) -> list:
        """提取按钮（增强版 - 改进位置识别）"""
        buttons = []

        button_elements = container.find_all('button')
        for btn in button_elements:
            btn_text = btn.get_text(strip=True)
            if not btn_text:
                btn_text = btn.get('aria-label', '')
            if not btn_text:
                btn_text = btn.get('title', '')

            if not btn_text:
                continue

            # 跳过无意义的按钮（纯图标按钮、下拉箭头等）
            if len(btn_text) <= 1 or btn_text in ['▼', '▲', '◀', '▶', '...', '···', '…']:
                continue

            btn_id = btn.get('id', '')

            # 推断按钮位置（增强版 - 多层级父元素检查）
            location = self._infer_button_location(btn)

            category = self._infer_button_category(btn_text, btn)

            btn_classes = btn.get('class', [])
            if isinstance(btn_classes, str):
                btn_classes = [btn_classes]

            style = 'default'
            if 'primary' in btn_classes or 'btn-primary' in btn_classes:
                style = 'primary'
            elif 'danger' in btn_classes:
                style = 'danger'
            elif 'warning' in btn_classes:
                style = 'warning'
            elif 'outline' in btn_classes or 'btn-outline' in btn_classes:
                style = 'outline'
            elif 'link' in btn_classes:
                style = 'link'

            icon = ""
            svg = btn.find('svg')
            if svg:
                icon = self._infer_icon_from_svg(svg)

            buttons.append(ActionButton(
                name=btn_text,
                category=category,
                style=style,
                button_id=btn_id,
                icon=icon,
                location=location
            ))

        # 去重：同名同位置的按钮只保留一个
        seen = set()
        unique_buttons = []
        for btn in buttons:
            key = (btn.name, btn.location)
            if key not in seen:
                seen.add(key)
                unique_buttons.append(btn)

        return unique_buttons

    def _infer_button_location(self, btn) -> str:
        """推断按钮位置（增强版 - 多层级检查）"""
        # 定义位置识别模式（通用，不写死具体业务名称）
        location_patterns = {
            'toolbar': [
                'toolbar', 'actions-bar', 'action-bar', 'btn-bar', 'button-bar',
                'filter-actions', 'secondary-actions', 'pr-toolbar', 'pa-toolbar',
                'po-toolbar', 'bk-toolbar', 'pi-toolbar', 'qc-toolbar'
            ],
            'filter': [
                'filter-row', 'filter-bar', 'search-bar', 'filter-item',
                'filter-actions', 'toolbar__filter', 'pr-filter-row'
            ],
            'modal': [
                'modal', 'drawer', 'dialog', 'popup', 'panel',
                'modal-footer', 'drawer-footer', 'drawer-panel', 'modal_toolbar',
                'drawer-panel__footer', 'por-detail-toolbar'
            ],
            'message': [
                'msg-card', 'message-card', 'notification', 'alert', 'toast'
            ],
            'stat': [
                'stat-card', 'stat-row', 'overview', 'dashboard'
            ],
            'buyer': [
                'buyer-card', 'user-card', 'staff-card', 'worker-card'
            ],
            'table': [
                'table', 'datagrid', 'data-table', 'row-actions', 'cell-action'
            ],
            'header': [
                'header', 'navbar', 'topbar', 'page-header'
            ],
            'sidebar': [
                'sidebar', 'sider', 'nav', 'menu'
            ],
            'pagination': [
                'pagination', 'pager', 'page-nav'
            ],
        }

        # 向上遍历最多5层父元素
        current = btn.parent
        depth = 0
        max_depth = 5

        while current and depth < max_depth:
            # 获取父元素的class
            parent_classes = current.get('class', [])
            if isinstance(parent_classes, str):
                parent_classes = [parent_classes]
            parent_class_str = ' '.join(parent_classes).lower()

            # 获取父元素的id
            parent_id = current.get('id', '').lower()

            # 检查每个位置模式
            for location, patterns in location_patterns.items():
                for pattern in patterns:
                    if pattern in parent_class_str or pattern in parent_id:
                        return location

            # 检查父元素标签类型
            parent_tag = current.name
            if parent_tag == 'tfoot':
                return 'table_footer'
            if parent_tag == 'thead':
                return 'table_header'

            # 向上一层
            current = current.parent
            depth += 1

        # 最后尝试从按钮自身的class推断
        btn_classes = btn.get('class', [])
        if isinstance(btn_classes, str):
            btn_classes = [btn_classes]
        btn_class_str = ' '.join(btn_classes).lower()

        for location, patterns in location_patterns.items():
            for pattern in patterns:
                if pattern in btn_class_str:
                    return location

        return 'unknown'

    def _infer_button_category(self, text: str, btn) -> str:
        """推断按钮分类（通用版 - 不依赖业务词汇）"""
        text_lower = text.lower()

        # 通用操作关键词（跨业务领域通用）
        if any(kw in text_lower for kw in ['搜索', '查询', '筛选', '查找', '检索', 'search', 'filter']):
            return 'search'
        if any(kw in text_lower for kw in ['导出', '下载', 'export', 'download']):
            return 'export'
        if any(kw in text_lower for kw in ['编辑', '修改', '更新', 'edit', 'update', 'modify']):
            return 'edit'
        if any(kw in text_lower for kw in ['删除', '移除', 'delete', 'remove']):
            return 'delete'
        if any(kw in text_lower for kw in ['新增', '添加', '创建', '新建', 'add', 'create', 'new']):
            return 'create'
        if any(kw in text_lower for kw in ['确认', '提交', '审核', '批准', 'confirm', 'submit', 'approve', 'audit']):
            return 'confirm'
        if any(kw in text_lower for kw in ['重置', '清空', 'reset', 'clear']):
            return 'reset'
        if any(kw in text_lower for kw in ['查看', '详情', '日志', '记录', 'view', 'detail', 'log']):
            return 'view'

        # 根据按钮样式推断
        btn_classes = btn.get('class', [])
        if isinstance(btn_classes, str):
            btn_classes = [btn_classes]
        if 'danger' in btn_classes:
            return 'delete'
        if 'success' in btn_classes or 'primary' in btn_classes:
            return 'confirm'

        return 'action'

    def _extract_stat_cards(self, container) -> list:
        """提取统计卡片"""
        cards = []

        stat_config = self.config.get('stat_card', {})
        card_patterns = stat_config.get('container', ['div.stat-card', 'div.wb-overview', 'div.stat-item'])
        title_patterns = stat_config.get('title', ['div.stat-card__title', 'div.stat-title', 'span.stat-label'])
        value_patterns = stat_config.get('value', ['div.stat-card__num', 'div.stat-num', 'span.stat-value'])
        sub_patterns = stat_config.get('subtitle', ['div.stat-card__sub', 'div.stat-sub'])
        icon_patterns = stat_config.get('icon', ['div.stat-card__icon', 'div.stat-icon'])

        stat_cards = find_by_patterns(container, card_patterns, find_all=True)

        for card in stat_cards:
            title_elem = find_by_patterns(card, title_patterns)
            title = title_elem.get_text(strip=True) if title_elem else ""

            value_elem = find_by_patterns(card, value_patterns)
            value = value_elem.get_text(strip=True) if value_elem else ""

            sub_elem = find_by_patterns(card, sub_patterns)
            subtitle = sub_elem.get_text(strip=True) if sub_elem else ""

            if 'wb-overview' in card.get('class', []):
                spans = card.find_all('span')
                if len(spans) >= 2:
                    title = spans[0].get_text(strip=True) if spans[0] else ""
                    value = spans[1].get_text(strip=True) if spans[1] else ""

            if not title:
                continue

            icon_elem = find_by_patterns(card, icon_patterns)
            icon_svg = ""
            if icon_elem:
                svg = icon_elem.find('svg')
                if svg:
                    icon_svg = str(svg)

            card_classes = card.get('class', [])
            if isinstance(card_classes, str):
                card_classes = [card_classes]

            color_type = 'default'
            color_patterns = stat_config.get('color_classes', {})
            for cls in card_classes:
                for color_name, color_patterns_list in color_patterns.items():
                    if any(pattern in cls for pattern in color_patterns_list):
                        color_type = color_name
                        break

            cards.append(StatCard(
                title=title,
                value=value,
                subtitle=subtitle,
                color_type=color_type,
                icon_svg=icon_svg
            ))

        return cards

    def _extract_message_cards(self, container) -> list:
        """提取消息通知卡片"""
        cards = []

        msg_cards = container.find_all('div', class_='msg-card')
        for card in msg_cards:
            dot_elem = card.find('div', class_='msg-card__dot')
            dot_visible = dot_elem is not None

            headline_elem = card.find('div', class_='msg-card__headline')
            headline = headline_elem.get_text(strip=True) if headline_elem else ""

            body_elem = card.find('div', class_='msg-card__body')
            content = ""
            if body_elem:
                text_elem = body_elem.find('p', class_='msg-card__text')
                if text_elem:
                    content = text_elem.get_text(strip=True)

            time = ""
            participants = 0
            comments = 0
            meta_elem = card.find('div', class_='msg-card__meta')
            if meta_elem:
                spans = meta_elem.find_all('span')
                for span in spans:
                    span_text = span.get_text(strip=True)
                    if re.match(r'\d{1,2}:\d{2}', span_text):
                        time = span_text
                    try:
                        num = int(span_text)
                        icon = span.find('svg')
                        if icon:
                            icon_str = str(icon)
                            if 'circle cx="9" cy="7"' in icon_str or 'user' in icon_str.lower():
                                participants = num
                            elif 'path d="M21 15' in icon_str or 'message' in icon_str.lower():
                                comments = num
                    except:
                        pass

            action_button = ""
            action_button_style = ""
            btn_elem = card.find('button')
            if btn_elem:
                action_button = btn_elem.get_text(strip=True)
                btn_classes = btn_elem.get('class', [])
                if 'btn-primary' in btn_classes or 'primary' in btn_classes:
                    action_button_style = 'primary'
                elif 'btn-default' in btn_classes:
                    action_button_style = 'default'

            cards.append(MessageCard(
                dot_visible=dot_visible,
                headline=headline,
                content=content,
                time=time,
                participants=participants,
                comments=comments,
                action_button=action_button,
                action_button_style=action_button_style
            ))

        return cards

    def _extract_staff_cards(self, container) -> list:
        """提取用户工作进度卡片"""
        cards = []

        staff_cards = container.find_all('div', class_='buyer-card')
        for card in staff_cards:
            avatar_elem = card.find('div', class_='avatar')
            avatar = ""
            if avatar_elem:
                img = avatar_elem.find('img')
                if img:
                    avatar = img.get('src', '')
                else:
                    avatar = avatar_elem.get_text(strip=True)

            name_elem = card.find('div', class_='buyer-card__name')
            name = name_elem.get_text(strip=True) if name_elem else ""

            tag = ""
            tag_color = ""
            tag_elem = card.find('span', class_=lambda x: x and 'tag' in x if x else False)
            if tag_elem:
                tag = tag_elem.get_text(strip=True)
                tag_classes = tag_elem.get('class', [])
                if 'tag-blue' in tag_classes:
                    tag_color = 'blue'
                elif 'tag-orange' in tag_classes:
                    tag_color = 'orange'
                elif 'tag-green' in tag_classes:
                    tag_color = 'green'
                elif 'tag-red' in tag_classes:
                    tag_color = 'red'

            stats = {}
            overdue_count = 0
            stats_elem = card.find('div', class_='buyer-card__stats')
            if stats_elem:
                spans = stats_elem.find_all('span')
                for span in spans:
                    span_text = span.get_text(strip=True)
                    match = re.match(r'(.+?)\s+(\d+)个', span_text)
                    if match:
                        stat_name = match.group(1)
                        stat_value = match.group(2) + '个'
                        stats[stat_name] = stat_value

                        if '逾期' in stat_name:
                            overdue_count = int(match.group(2))
                    else:
                        overdue_span = span.find('span', class_='overdue')
                        if overdue_span:
                            overdue_text = overdue_span.get_text(strip=True)
                            try:
                                overdue_count = int(overdue_text)
                            except:
                                pass

            action_buttons = []
            btn_elems = card.find_all('button')
            for btn in btn_elems:
                btn_text = btn.get_text(strip=True)
                if btn_text:
                    action_buttons.append(btn_text)

            cards.append(StaffCard(
                avatar=avatar,
                name=name,
                tag=tag,
                tag_color=tag_color,
                stats=stats,
                overdue_count=overdue_count,
                action_buttons=action_buttons
            ))

        return cards

    def _extract_status_tabs(self, container) -> list:
        """提取状态筛选Tab"""
        tabs = []

        status_groups = container.find_all('div', class_='pr-status-group')
        for group in status_groups:
            chips = group.find_all('span', class_='pr-status-chip')
            for chip in chips:
                chip_text = chip.get_text(strip=True)
                # 匹配 "状态名7670" 或 "状态名 7670" 格式（名称+数量）
                match = re.match(r'^(.+?)(\d+)$', chip_text)
                if match:
                    name = match.group(1).strip()
                    try:
                        count = int(match.group(2))
                    except:
                        count = 0
                        name = chip_text
                else:
                    name = chip_text
                    count = 0

                chip_classes = chip.get('class', [])
                color_type = 'default'
                for cls in chip_classes:
                    if 'pr-status-chip--orange' in cls:
                        color_type = 'orange'
                    elif 'pr-status-chip--green' in cls:
                        color_type = 'green'
                    elif 'pr-status-chip--red' in cls:
                        color_type = 'red'
                    elif 'pr-status-chip--pink' in cls:
                        color_type = 'pink'

                is_active = 'is-active' in chip_classes

                filter_key = chip.get('data-paa-status-filter', '') or chip.get('data-pr-status-filter', '') or chip.get('data-por-status-filter', '')

                tabs.append(StatusTab(
                    name=name,
                    count=count,
                    color_type=color_type,
                    is_active=is_active,
                    filter_key=filter_key
                ))

        return tabs

    def _extract_progress_items(self, container) -> list:
        """提取进度条组件"""
        items = []

        progress_items = container.find_all('div', class_='progress-item')
        for item in progress_items:
            dot_elem = item.find('span', class_='status-dot')
            dot_color = ''
            if dot_elem:
                dot_classes = dot_elem.get('class', [])
                for cls in dot_classes:
                    if 'status-dot--blue' in cls:
                        dot_color = 'blue'
                    elif 'status-dot--orange' in cls:
                        dot_color = 'orange'
                    elif 'status-dot--green' in cls:
                        dot_color = 'green'
                    elif 'status-dot--red' in cls:
                        dot_color = 'red'

            name_elem = item.find('div', class_='progress-item__name')
            name = name_elem.get_text(strip=True) if name_elem else ""

            detail_elem = item.find('div', class_='progress-item__detail')
            detail = detail_elem.get_text(strip=True) if detail_elem else ""

            status_elem = item.find('div', class_='status-pill')
            status_label = status_elem.get_text(strip=True) if status_elem else ""
            status_label_color = ''
            if status_elem:
                status_classes = status_elem.get('class', [])
                for cls in status_classes:
                    if 'status-pill--blue' in cls:
                        status_label_color = 'blue'
                    elif 'status-pill--orange' in cls:
                        status_label_color = 'orange'
                    elif 'status-pill--green' in cls:
                        status_label_color = 'green'
                    elif 'status-pill--red' in cls:
                        status_label_color = 'red'

            date_elem = item.find('div', class_='progress-item__date')
            date = date_elem.get_text(strip=True) if date_elem else ""

            items.append(ProgressItem(
                status_dot_color=dot_color,
                name=name,
                detail=detail,
                status_label=status_label,
                status_label_color=status_label_color,
                date=date
            ))

        return items

    def _extract_drawer_panels(self, container) -> list:
        """提取弹窗/抽屉面板"""
        panels = []

        drawer_panels = container.find_all('div', class_='drawer-panel')
        for panel in drawer_panels:
            panel_id = panel.get('id', '')

            title_elem = panel.find('span', id=lambda x: x and 'title' in x if x else False)
            title = title_elem.get_text(strip=True) if title_elem else ""
            if not title_elem:
                title_container = panel.find('div', class_='drawer-panel__title')
                if title_container:
                    title = title_container.get_text(strip=True)

            title_icon = ""
            icon_elem = panel.find('div', class_='drawer-panel__title-icon')
            if icon_elem:
                svg = icon_elem.find('svg')
                if svg:
                    title_icon = self._infer_icon_from_svg(svg)

            status_badge_id = ""
            badge_elem = panel.find('span', class_='pr-badge', id=True)
            if badge_elem:
                status_badge_id = badge_elem.get('id', '')

            no_element_id = ""
            no_elem = panel.find('span', class_=lambda x: x and 'no' in x if x else False, id=True)
            if no_elem:
                no_element_id = no_elem.get('id', '')

            # 锚点导航
            anchor_links = []
            anchor_bar = panel.find('div', class_='drawer-anchor-bar')
            if anchor_bar:
                links = anchor_bar.find_all('a', class_='drawer-anchor-link')
                for link in links:
                    link_name = link.get_text(strip=True)
                    anchor_key = link.get('data-anchor', '')
                    is_active = 'is-active' in link.get('class', [])
                    anchor_links.append(DrawerAnchorLink(
                        name=link_name,
                        anchor_key=anchor_key,
                        is_active=is_active
                    ))

            # 表单字段
            form_fields = []
            info_items = panel.find_all('div', class_='drawer-info-item')
            for item in info_items:
                label_elem = item.find('span', class_='drawer-info-label')
                field_name = label_elem.get_text(strip=True) if label_elem else ""
                is_required = item.find('span', class_='req') is not None

                select_elem = item.find('select', class_='drawer-info-select')
                textarea_elem = item.find('textarea', class_='drawer-info-textarea')
                input_elem = item.find('input', class_='drawer-info-input')

                field_type = 'unknown'
                options = []
                placeholder = ''
                field_id = ''

                if select_elem:
                    field_type = 'select'
                    field_id = select_elem.get('id', '')
                    for opt in select_elem.find_all('option'):
                        opt_text = opt.get_text(strip=True)
                        if opt_text and opt_text != '请选择':
                            options.append(opt_text)
                elif textarea_elem:
                    field_type = 'textarea'
                    field_id = textarea_elem.get('id', '')
                    placeholder = textarea_elem.get('placeholder', '')
                elif input_elem:
                    field_type = input_elem.get('type', 'input')
                    field_id = input_elem.get('id', '')
                    placeholder = input_elem.get('placeholder', '')

                is_full_width = 'drawer-info-item--full' in item.get('class', [])

                if field_name:
                    form_fields.append(DrawerFormField(
                        name=field_name,
                        type=field_type,
                        is_required=is_required,
                        options=options,
                        placeholder=placeholder,
                        field_id=field_id,
                        is_full_width=is_full_width
                    ))

            # 统计信息
            statistics = []
            stat_elems = panel.find_all('span', class_='por-demand-stat-inline__item')
            for stat in stat_elems:
                stat_text = stat.get_text(strip=True)
                match = re.match(r'(.+?)(\d+)', stat_text)
                if match:
                    stat_name = match.group(1)
                    stat_value = match.group(2)
                    stat_classes = stat.get('class', [])
                    color_type = 'default'
                    for cls in stat_classes:
                        if 'por-demand-stat-inline__item--total' in cls:
                            color_type = 'total'
                        elif 'por-demand-stat-inline__item--split' in cls:
                            color_type = 'split'
                        elif 'por-demand-stat-inline__item--unsplit' in cls:
                            color_type = 'unsplit'
                    statistics.append(DrawerStatistics(
                        name=stat_name,
                        value=stat_value,
                        color_type=color_type
                    ))

            # 弹窗内按钮
            inner_buttons = []
            footer = panel.find('div', class_='drawer-panel__footer')
            if footer:
                btns = footer.find_all('button')
                for btn in btns:
                    btn_text = btn.get_text(strip=True)
                    if btn_text:
                        btn_id = btn.get('id', '')
                        btn_classes = btn.get('class', [])
                        style = 'default'
                        if 'scm-btn--primary' in btn_classes or 'pr-btn--primary' in btn_classes:
                            style = 'primary'
                        elif 'scm-btn--danger' in btn_classes:
                            style = 'danger'
                        inner_buttons.append(ActionButton(
                            name=btn_text,
                            category=self._infer_button_category(btn_text, btn),
                            style=style,
                            button_id=btn_id,
                            icon='',
                            location='modal_footer'
                        ))
            # 工具栏按钮
            toolbar_right = panel.find('div', class_='por-detail-toolbar-right')
            if toolbar_right:
                btns = toolbar_right.find_all('button')
                for btn in btns:
                    btn_text = btn.get_text(strip=True)
                    if btn_text:
                        btn_id = btn.get('id', '')
                        inner_buttons.append(ActionButton(
                            name=btn_text,
                            category=self._infer_button_category(btn_text, btn),
                            style='outline',
                            button_id=btn_id,
                            icon='',
                            location='modal_toolbar'
                        ))

            has_search_box = panel.find('input', class_='por-detail-search__input') is not None
            search_placeholder = ''
            search_input = panel.find('input', class_='por-detail-search__input')
            if search_input:
                search_placeholder = search_input.get('placeholder', '')

            has_timeline = panel.find('div', class_='drawer-timeline') is not None

            panels.append(DrawerPanel(
                panel_id=panel_id,
                title=title,
                title_icon=title_icon,
                status_badge_id=status_badge_id,
                no_element_id=no_element_id,
                anchor_links=anchor_links,
                form_fields=form_fields,
                statistics=statistics,
                inner_buttons=inner_buttons,
                has_search_box=has_search_box,
                search_placeholder=search_placeholder,
                has_timeline=has_timeline
            ))

        return panels

    def to_markdown(self, analysis: PrototypeAnalysis) -> str:
        """转换为Markdown格式"""
        md_lines = []

        # 标题
        md_lines.append(f"# 原型分析报告")
        md_lines.append("")
        md_lines.append(f"**分析时间**: {analysis.analysis_time}")
        md_lines.append(f"**HTML来源**: {self.url}")
        md_lines.append("")

        # 系统概览
        md_lines.append("## 系统概览")
        md_lines.append("")
        md_lines.append(f"| 属性 | 值 |")
        md_lines.append(f"|-----|-----|")
        md_lines.append(f"| 系统名称 | {analysis.system_name} |")
        md_lines.append(f"| 页面标题 | {analysis.title} |")
        md_lines.append(f"| 菜单数量 | {len(analysis.menus)} |")
        md_lines.append(f"| 页面视图数量 | {len(analysis.page_views)} |")
        md_lines.append(f"| 筛选字段总数 | {analysis.total_filters} |")
        md_lines.append(f"| 表格列总数 | {analysis.total_columns} |")
        md_lines.append(f"| 操作按钮总数 | {analysis.total_buttons} |")
        md_lines.append("")

        # 侧边栏信息
        md_lines.append("## 侧边栏信息")
        md_lines.append("")
        md_lines.append(f"| 属性 | 值 |")
        md_lines.append(f"|-----|-----|")
        md_lines.append(f"| 是否有折叠按钮 | {analysis.sidebar.has_toggle} |")
        md_lines.append(f"| 折叠按钮ID | {analysis.sidebar.toggle_button_id or '-'} |")
        md_lines.append(f"| 用户头像文字 | {analysis.sidebar.user_info.avatar_text or '-'} |")
        md_lines.append(f"| 用户姓名 | {analysis.sidebar.user_info.name or '-'} |")
        md_lines.append(f"| 用户角色 | {analysis.sidebar.user_info.role or '-'} |")
        md_lines.append("")

        # 页面标签栏
        if analysis.page_tabs:
            md_lines.append("## 页面标签栏")
            md_lines.append("")
            md_lines.append(f"| 标签名称 | 是否激活 | 是否有关闭按钮 |")
            md_lines.append(f"|---------|---------|---------------|")
            for tab in analysis.page_tabs:
                md_lines.append(f"| {tab.name} | {tab.is_active} | {tab.has_close} |")
            md_lines.append("")

        # 菜单结构
        md_lines.append("## 菜单结构")
        md_lines.append("")

        menu_groups = {}
        for menu in analysis.menus:
            if menu.group not in menu_groups:
                menu_groups[menu.group] = []
            menu_groups[menu.group].append(menu)

        for group_name, group_menus in menu_groups.items():
            md_lines.append(f"### {group_name}")
            md_lines.append("")
            md_lines.append(f"| 菜单名称 | 图标描述 | 页面标识 | 是否激活 |")
            md_lines.append(f"|---------|---------|----------|---------|")
            for menu in group_menus:
                md_lines.append(f"| {menu.name} | {menu.icon} | {menu.page_id or '-'} | {menu.is_active} |")
            md_lines.append("")

        # 页面详情
        md_lines.append("## 页面详情")
        md_lines.append("")

        for page_view in analysis.page_views:
            md_lines.append(f"### 页面：{page_view.name}")
            md_lines.append(f"- 视图ID: `{page_view.view_id}`")
            md_lines.append("")

            # 子标签
            if page_view.sub_pills:
                md_lines.append("#### 子标签切换")
                md_lines.append("")
                md_lines.append(f"| 标签名称 | 标签ID | 是否激活 | 目标面板 |")
                md_lines.append(f"|---------|--------|---------|---------|")
                for pill in page_view.sub_pills:
                    md_lines.append(f"| {pill.name} | {pill.pill_id} | {pill.is_active} | {pill.target_panel} |")
                md_lines.append("")

            # 统计卡片
            if page_view.stat_cards:
                md_lines.append("#### 统计卡片")
                md_lines.append("")
                md_lines.append(f"| 卡片标题 | 数值 | 说明 | 颜色类型 |")
                md_lines.append(f"|---------|------|------|---------|")
                for card in page_view.stat_cards:
                    md_lines.append(f"| {card.title} | {card.value} | {card.subtitle} | {card.color_type} |")
                md_lines.append("")

            # 消息通知卡片
            if page_view.message_cards:
                md_lines.append("#### 消息通知")
                md_lines.append("")
                md_lines.append(f"| 标题 | 正文 | 时间 | 参与人数 | 评论数 | 操作按钮 |")
                md_lines.append(f"|-----|------|------|---------|-------|---------|")
                for card in page_view.message_cards:
                    md_lines.append(f"| {card.headline} | {card.content[:50]}... | {card.time} | {card.participants} | {card.comments} | {card.action_button} |")
                md_lines.append("")

            # 用户工作进度卡片
            if page_view.staff_cards:
                md_lines.append("#### 用户工作进度概览")
                md_lines.append("")
                md_lines.append(f"| 姓名 | 标签 | 统计数据 | 已逾期 | 操作按钮 |")
                md_lines.append(f"|-----|------|---------|-------|---------|")
                for card in page_view.staff_cards:
                    stats_str = '; '.join([f"{k}: {v}" for k, v in card.stats.items()])
                    buttons_str = ', '.join(card.action_buttons)
                    md_lines.append(f"| {card.name} | {card.tag}({card.tag_color}) | {stats_str} | {card.overdue_count}个 | {buttons_str} |")
                md_lines.append("")

            # 状态筛选Tab
            if page_view.status_tabs:
                md_lines.append("#### 状态筛选Tab")
                md_lines.append("")
                md_lines.append(f"| 状态名称 | 数量 | 颜色类型 | 是否激活 | 筛选键 |")
                md_lines.append(f"|---------|------|---------|---------|--------|")
                for tab in page_view.status_tabs:
                    md_lines.append(f"| {tab.name} | {tab.count} | {tab.color_type} | {tab.is_active} | {tab.filter_key or '-'} |")
                md_lines.append("")

            # 进度条组件
            if page_view.progress_items:
                md_lines.append("#### 进度条组件")
                md_lines.append("")
                md_lines.append(f"| 名称 | 详情 | 状态标签 | 状态颜色 | 日期 |")
                md_lines.append(f"|-----|------|---------|---------|------|")
                for item in page_view.progress_items:
                    md_lines.append(f"| {item.name} | {item.detail} | {item.status_label} | {item.status_label_color} | {item.date} |")
                md_lines.append("")

            # 弹窗面板
            if page_view.drawer_panels:
                md_lines.append("#### 弹窗/抽屉面板")
                md_lines.append("")
                for panel in page_view.drawer_panels:
                    md_lines.append(f"**弹窗ID**: `{panel.panel_id}`")
                    md_lines.append("")
                    md_lines.append(f"- **标题**: {panel.title} ({panel.title_icon})")
                    md_lines.append(f"- **是否有搜索框**: {panel.has_search_box}")
                    if panel.has_search_box:
                        md_lines.append(f"- **搜索框占位符**: {panel.search_placeholder}")
                    md_lines.append(f"- **是否有操作日志时间线**: {panel.has_timeline}")
                    md_lines.append("")

                    if panel.anchor_links:
                        md_lines.append(f"- **锚点导航**: {', '.join([link.name for link in panel.anchor_links])}")
                        md_lines.append("")

                    if panel.form_fields:
                        md_lines.append("**弹窗内表单字段**:")
                        md_lines.append("")
                        md_lines.append(f"| 字段名 | 类型 | 是否必填 | 选项 | 占位符 |")
                        md_lines.append(f"|-------|------|---------|------|--------|")
                        for field in panel.form_fields:
                            required_str = "✅" if field.is_required else "-"
                            options_str = ', '.join(field.options[:5]) if field.options else "-"
                            md_lines.append(f"| {field.name} | {field.type} | {required_str} | {options_str} | {field.placeholder or '-'} |")
                        md_lines.append("")

                    if panel.statistics:
                        md_lines.append("**弹窗内统计信息**:")
                        md_lines.append("")
                        stats_str = ' | '.join([f"{s.name}{s.value}" for s in panel.statistics])
                        md_lines.append(f"| {stats_str} |")
                        md_lines.append("")

                    if panel.inner_buttons:
                        md_lines.append("**弹窗内按钮**:")
                        md_lines.append("")
                        md_lines.append(f"| 按钮名称 | 分类 | 样式 | 位置 |")
                        md_lines.append(f"|---------|------|------|------|")
                        for btn in panel.inner_buttons:
                            md_lines.append(f"| {btn.name} | {btn.category} | {btn.style} | {btn.location} |")
                        md_lines.append("")

                    md_lines.append("---")
                    md_lines.append("")

            # 筛选条件
            if page_view.filters:
                md_lines.append("#### 筛选条件")
                md_lines.append("")
                md_lines.append(f"| 字段名 | 类型 | 选项/占位符 | 默认值 | 筛选器ID |")
                md_lines.append(f"|-------|------|------------|-------|----------|")
                for filter_field in page_view.filters:
                    if filter_field.type == 'select':
                        options_str = ', '.join(filter_field.options[:10])
                        if len(filter_field.options) > 10:
                            options_str += '...'
                        md_lines.append(f"| {filter_field.name} | select | {options_str} | {filter_field.default_value or '全部'} | {filter_field.filter_id} |")
                    elif filter_field.type in ['text', 'input']:
                        md_lines.append(f"| {filter_field.name} | {filter_field.type} | {filter_field.placeholder} | {filter_field.default_value or '-'} | {filter_field.filter_id} |")
                    else:
                        md_lines.append(f"| {filter_field.name} | {filter_field.type} | - | {filter_field.default_value or '-'} | {filter_field.filter_id} |")
                md_lines.append("")

            # 操作按钮
            if page_view.buttons:
                md_lines.append("#### 操作按钮")
                md_lines.append("")
                md_lines.append(f"| 按钮名称 | 分类 | 样式 | 位置 | 按钮ID |")
                md_lines.append(f"|---------|------|------|------|--------|")
                for btn in page_view.buttons:
                    md_lines.append(f"| {btn.name} | {btn.category} | {btn.style} | {btn.location} | {btn.button_id or '-'} |")
                md_lines.append("")

            # 表格信息
            if page_view.tables:
                for table_info in page_view.tables:
                    table_label = "主表" if table_info.is_main_table else "明细子表"
                    md_lines.append(f"#### {table_label}（表格索引: {table_info.table_index})")
                    md_lines.append("")
                    if table_info.columns:
                        md_lines.append(f"| 字段名 | 数据类型 | 是否明细列 |")
                        md_lines.append(f"|-------|---------|----------|")
                        for col in table_info.columns:
                            md_lines.append(f"| {col.name} | {col.data_type} | {col.is_detail} |")
                        md_lines.append("")
                    md_lines.append(f"- 是否有勾选列: {table_info.has_checkbox}")
                    md_lines.append("")

            md_lines.append("---")
            md_lines.append("")

        # 技术实现建议（增强版）
        md_lines.append("## 技术实现建议")
        md_lines.append("")

        if analysis.tech_implementation:
            tech = analysis.tech_implementation

            # 前端路由规划
            md_lines.append("### 前端路由规划")
            md_lines.append("")
            md_lines.append("```typescript")
            md_lines.append("const routes = [")
            for route in tech.routes:
                meta_str = f"icon: '{route['meta']['icon']}'" if route['meta'].get('icon') else ""
                md_lines.append(f"  {{ path: '{route['path']}', name: '{route['name']}', component: () => import('{route['component']}'), meta: {{ {meta_str} }} }},")
            md_lines.append("];")
            md_lines.append("```")
            md_lines.append("")

            # API接口规划（增强版）
            md_lines.append("### API接口规划")
            md_lines.append("")
            md_lines.append("```yaml")
            md_lines.append("# 建议的API接口结构（含业务操作接口）")

            # 按资源分组
            resource_groups = {}
            for endpoint in tech.api_endpoints:
                if endpoint.resource not in resource_groups:
                    resource_groups[endpoint.resource] = []
                resource_groups[endpoint.resource].append(endpoint)

            for resource, endpoints in resource_groups.items():
                md_lines.append(f"\n{resource}:")
                for ep in endpoints:
                    params_str = ', '.join(ep.params) if ep.params else ''
                    md_lines.append(f"  {ep.action_type}: {ep.method} {ep.path}")
                    md_lines.append(f"    # {ep.name}")
                    if params_str:
                        md_lines.append(f"    # 参数: {params_str}")
            md_lines.append("```")
            md_lines.append("")

            # 数据库表设计（增强版）
            md_lines.append("### 数据库表设计")
            md_lines.append("")
            md_lines.append("```sql")
            md_lines.append("-- 基于原型分析推断的数据表结构")

            for table in tech.database_tables:
                md_lines.append(f"\n-- {table.entity_name}表 ({table.table_name})")
                md_lines.append(f"CREATE TABLE {table.table_name} (")

                for col in table.columns:
                    constraint = col.get('constraint', '')
                    constraint_str = f" {constraint}" if constraint else ""
                    comment = col.get('comment', '')
                    comment_str = f" COMMENT '{comment}'" if comment else ""
                    md_lines.append(f"    {col['name']} {col['type']}{constraint_str}{comment_str},")

                # 状态枚举
                if table.status_enum:
                    md_lines.append(f"    status {table.status_enum} COMMENT '状态',")

                md_lines.append(");")

                # 索引
                if table.indexes:
                    for idx in table.indexes:
                        md_lines.append(f"CREATE INDEX idx_{table.table_name}_{idx} ON {table.table_name}({idx});")

            md_lines.append("```")
            md_lines.append("")

            # 实体关系
            if tech.entity_relations:
                md_lines.append("### 实体关系")
                md_lines.append("")
                md_lines.append("```mermaid")
                md_lines.append("erDiagram")
                for rel in tech.entity_relations:
                    arrow = "||--o{" if rel.relation_type == 'one_to_many' else "||--||"
                    md_lines.append(f"    {rel.from_entity} {arrow} {rel.to_entity} : \"{rel.description}\"")
                md_lines.append("```")
                md_lines.append("")

            # 状态枚举
            if tech.status_enums:
                md_lines.append("### 状态枚举定义")
                md_lines.append("")
                md_lines.append("```typescript")
                for enum_name, values in tech.status_enums.items():
                    md_lines.append(f"// {enum_name}")
                    md_lines.append(f"enum {enum_name.upper()} {{")
                    for v in values:
                        enum_value = v.upper().replace(' ', '_').replace('-', '_')
                        md_lines.append(f"  {enum_value} = '{v}',")
                    md_lines.append("}")
                md_lines.append("```")
                md_lines.append("")
        else:
            # 兼容旧版输出（如果没有 tech_implementation）
            md_lines.append("### 前端路由规划")
            md_lines.append("")
            md_lines.append("```typescript")
            md_lines.append("const routes = [")
            for menu in analysis.menus:
                if menu.page_id:
                    route_path = menu.page_id.replace('-', '/')
                    md_lines.append(f"  {{ path: '/{route_path}', name: '{menu.name}', component: () => import('@/views/{menu.page_id}/index.vue') }},")
            md_lines.append("];")
            md_lines.append("```")
            md_lines.append("")

            md_lines.append("### API接口规划")
            md_lines.append("")
            md_lines.append("```yaml")
            md_lines.append("# 建议的API接口结构")
            for page_view in analysis.page_views[:5]:
                md_lines.append(f"{page_view.view_id}:")
                api_name = page_view.view_id.replace('view-', '').replace('-view', '').replace('page-', '')
                md_lines.append(f"  list: GET /api/{api_name}/list")
                md_lines.append(f"  detail: GET /api/{api_name}/:id")
                md_lines.append(f"  create: POST /api/{api_name}")
                md_lines.append(f"  update: PUT /api/{api_name}/:id")
                md_lines.append(f"  delete: DELETE /api/{api_name}/:id")
            md_lines.append("```")
            md_lines.append("")

            md_lines.append("### 数据库表设计建议")
            md_lines.append("")
            md_lines.append("```sql")
            md_lines.append("-- 基于筛选条件和表格列推断的数据表结构")
            for page_view in analysis.page_views[:3]:
                main_table = None
                for t in page_view.tables:
                    if t.is_main_table:
                        main_table = t
                        break
                if main_table and main_table.columns:
                    table_name = page_view.view_id.replace('view-', '').replace('-view', '').replace('page-', '').replace('-', '_')
                    md_lines.append(f"-- {page_view.name}表")
                    md_lines.append(f"CREATE TABLE {table_name} (")
                    md_lines.append(f"    id VARCHAR(36) PRIMARY KEY,")
                    for col in main_table.columns[:15]:
                        col_name = col.name.lower().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')
                        if col.data_type == 'number':
                            md_lines.append(f"    {col_name} DECIMAL(10,2),")
                        elif col.data_type == 'date':
                            md_lines.append(f"    {col_name} DATE,")
                        elif col.data_type in ['link', 'currency']:
                            md_lines.append(f"    {col_name} VARCHAR(100),")
                        else:
                            md_lines.append(f"    {col_name} VARCHAR(200),")
                    md_lines.append(f"    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,")
                    md_lines.append(f"    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                    md_lines.append(f");")
                    md_lines.append("")
            md_lines.append("```")
            md_lines.append("")

        md_lines.append("---")
        md_lines.append("*生成工具: bie-zheng-luan-prototype技能 v2.9.1*")
        md_lines.append("*注意: 本分析基于HTML结构，实际业务逻辑需与产品经理确认*")

        return "\n".join(md_lines)

    def to_json(self, analysis: PrototypeAnalysis) -> str:
        """转换为JSON格式"""
        return json.dumps(asdict(analysis), ensure_ascii=False, indent=2)

    # ==================== 增强的技术实现推断方法 ====================

    def _generate_tech_implementation(self, menus: List[MenuItem], page_views: List[PageView]) -> TechImplementation:
        """生成完整的技术实现建议"""
        routes = self._generate_routes(menus, page_views)
        api_endpoints = self._generate_api_endpoints(menus, page_views)
        database_tables = self._generate_database_tables(menus, page_views)
        entity_relations = self._generate_entity_relations(database_tables)
        status_enums = self._extract_status_enums(page_views)

        return TechImplementation(
            routes=routes,
            api_endpoints=api_endpoints,
            database_tables=database_tables,
            entity_relations=entity_relations,
            status_enums=status_enums
        )

    def _generate_routes(self, menus: List[MenuItem], page_views: List[PageView]) -> List[Dict[str, str]]:
        """生成前端路由配置（增强版 - 处理特殊href）"""
        routes = []

        for menu in menus:
            route_path = self._infer_route_path(menu)
            component_path = self._infer_component_path(menu)

            routes.append({
                'path': route_path,
                'name': menu.name,
                'component': component_path,
                'meta': {
                    'icon': menu.icon,
                    'group': menu.group
                }
            })

        # 添加页面视图的路由（排除已存在的）
        existing_paths = set(r['path'] for r in routes)
        for pv in page_views:
            if pv.view_id:
                view_path = '/' + pv.view_id.replace('-', '/')
                if view_path not in existing_paths:
                    routes.append({
                        'path': view_path,
                        'name': pv.name,
                        'component': f"@/views/{pv.view_id}/index.vue",
                        'meta': {'hidden': True}
                    })

        return routes

    def _infer_route_path(self, menu: MenuItem) -> str:
        """推断路由路径（增强版 - 处理 javascript:void(0) 等特殊值）"""
        # 处理特殊 href 值
        href = menu.href or ''
        page_id = menu.page_id or ''

        # 无效模式列表
        invalid_patterns = [
            'javascript:void(0)',
            'javascript:;',
            '#',
            '',
            'void(0)',
        ]

        # 检查 href 是否无效
        href_invalid = href in invalid_patterns or href.startswith('javascript:')
        # 检查 page_id 是否无效
        page_id_invalid = page_id in invalid_patterns or page_id.startswith('javascript:') if page_id else True

        # 如果 href 无效，检查 page_id
        if href_invalid:
            if page_id and not page_id_invalid:
                # page_id 格式: purchase-order-req -> /purchase/order/req
                return '/' + page_id.replace('-', '/')
            else:
                # 使用菜单名称生成路由（通用处理）
                menu_name = menu.name.lower()
                if menu_name:
                    # 使用 kebab-case 格式，将中文转为拼音或使用通用路径
                    # 对于常见的工作台菜单，使用通用名称
                    # 注意：这里只处理最通用的UI概念，不涉及任何业务词汇
                    # "我的"通常是系统级的个人视图
                    if '我的' in menu_name or '我' in menu_name:
                        return '/my-view'
                    # 使用 URL 安全的名称
                    safe_name = menu_name.replace(' ', '-').replace('/', '-')
                    return '/' + safe_name
                return '/unknown'

            # href 有效，直接使用
            if href.startswith('/'):
                return href
            if href.startswith('http'):
                # 外部链接，不适合作为路由，使用菜单名称
                menu_name = menu.name.lower().replace(' ', '-')
                return '/' + menu_name

            # 其他情况，检查 page_id
            if page_id and not page_id_invalid:
                return '/' + page_id.replace('-', '/')

            # 最后使用菜单名称
            return '/' + menu.name.lower().replace(' ', '-').replace('/', '-')

    def _infer_component_path(self, menu: MenuItem) -> str:
        """推断组件路径"""
        page_id = menu.page_id or ''

        # 无效模式列表
        invalid_patterns = [
            'javascript:void(0)',
            'javascript:;',
            '#',
            '',
            'void(0)',
        ]

        # 检查 page_id 是否无效
        page_id_invalid = page_id in invalid_patterns or page_id.startswith('javascript:') if page_id else True

        if page_id and not page_id_invalid:
            return f"@/views/{page_id}/index.vue"

        # 使用菜单名称生成组件路径
        # 对于包含"我的"的菜单，使用通用路径
        menu_name = menu.name
        if '我的' in menu_name:
            return "@/views/my-view/index.vue"

        # 使用 URL 安全的名称
        # 注意：这里不硬编码任何业务词汇，只是生成路径
        safe_name = menu_name.lower().replace(' ', '-').replace('/', '-')
        return f"@/views/{safe_name}/index.vue"

    def _generate_api_endpoints(self, menus: List[MenuItem], page_views: List[PageView]) -> List[APIEndpoint]:
        """生成API接口列表（增强版 - 包含业务操作接口）"""
        endpoints = []

        # 根据菜单和页面视图推断基础CRUD接口
        for menu in menus:
            resource = self._infer_resource_name(menu)
            if resource:
                # 基础CRUD接口
                endpoints.extend(self._generate_crud_endpoints(resource, menu.name))

        # 根据页面视图中的按钮推断业务接口
        for pv in page_views:
            resource = self._infer_resource_from_view(pv)
            if resource:
                # 根据按钮推断业务操作接口
                endpoints.extend(self._infer_business_endpoints_from_buttons(resource, pv.buttons))

        # 去重
        seen = set()
        unique_endpoints = []
        for ep in endpoints:
            key = f"{ep.method}:{ep.path}"
            if key not in seen:
                seen.add(key)
                unique_endpoints.append(ep)

        return unique_endpoints

    def _infer_resource_name(self, menu: MenuItem) -> str:
        """从菜单推断资源名称（通用版 - 优先使用page_id）"""
        page_id = menu.page_id or ''

        # 无效模式列表
        invalid_patterns = [
            'javascript:void(0)',
            'javascript:;',
            '#',
            '',
            'void(0)',
        ]

        # 检查 page_id 是否有效
        page_id_invalid = page_id in invalid_patterns or page_id.startswith('javascript:') if page_id else True

        if page_id and not page_id_invalid:
            # purchase-order-req -> purchase_order_req
            return page_id.replace('-', '_')

        # 使用菜单名称生成资源名（纯通用处理）
        # 1. 尝试使用英文翻译常见UI概念
        menu_name = menu.name

        # 注意：这里只处理UI层面的通用概念，不涉及任何业务词汇
        # "我的"通常是系统级的个人视图
        if '我的' in menu_name:
            return 'my_view'

        # "管理"、"列表"、"详情"是UI展示概念，不是业务词汇
        # 对于包含这些词的菜单，使用page_id或菜单名称处理
        if '管理' in menu_name or '列表' in menu_name or '详情' in menu_name:
            # 尝试提取实体部分
            base = menu_name.replace('管理', '').replace('列表', '').replace('详情', '').strip()
            if base:
                return self._to_english_name(base) or 'resource'
            return 'resource'

        # 最后使用通用名称
        return self._to_english_name(menu_name) or 'generic_resource'

    def _to_english_name(self, chinese_name: str) -> str:
        """将中文名称转换为英文名称（通用处理）"""
        # 这是一个辅助方法，用于处理纯中文名称
        # 使用拼音或通用名称
        name = chinese_name.lower().strip()

        # 如果名称为空或只有空格
        if not name:
            return 'resource'

        # 使用URL安全的名称（仅ASCII字符）
        # 对于纯中文，返回空字符串让调用者使用备用方案
        import re
        safe_name = re.sub(r'[^\w]', '_', name)
        ascii_only = re.sub(r'[^\x00-\x7F]', '', safe_name)

        if ascii_only and ascii_only.replace('_', ''):
            return ascii_only.lower()

        # 纯中文名称，返回空让调用者使用备用方案
        return ''

    def _infer_resource_from_view(self, pv: PageView) -> str:
        """从页面视图推断资源名称"""
        view_id = pv.view_id or ''

        if view_id:
            # main-supply -> supply, purchase-req -> purchase_req
            parts = view_id.split('-')
            if len(parts) > 1:
                # 去掉常见前缀
                prefixes = ['main', 'view', 'page', 'panel']
                resource_parts = [p for p in parts if p not in prefixes]
                return '_'.join(resource_parts)
            return view_id

        return pv.name.lower().replace(' ', '_').replace('-', '_')

    def _generate_crud_endpoints(self, resource: str, entity_name: str) -> List[APIEndpoint]:
        """生成基础CRUD接口"""
        return [
            APIEndpoint(
                path=f"/api/{resource}/list",
                method="GET",
                name=f"获取{entity_name}列表",
                description=f"查询{entity_name}列表，支持分页和筛选",
                params=["page", "size", "filters"],
                resource=resource,
                action_type="list"
            ),
            APIEndpoint(
                path=f"/api/{resource}/:id",
                method="GET",
                name=f"获取{entity_name}详情",
                description=f"根据ID获取{entity_name}详细信息",
                params=["id"],
                resource=resource,
                action_type="detail"
            ),
            APIEndpoint(
                path=f"/api/{resource}",
                method="POST",
                name=f"创建{entity_name}",
                description=f"创建新的{entity_name}记录",
                params=["body"],
                resource=resource,
                action_type="create"
            ),
            APIEndpoint(
                path=f"/api/{resource}/:id",
                method="PUT",
                name=f"更新{entity_name}",
                description=f"更新{entity_name}信息",
                params=["id", "body"],
                resource=resource,
                action_type="update"
            ),
            APIEndpoint(
                path=f"/api/{resource}/:id",
                method="DELETE",
                name=f"删除{entity_name}",
                description=f"删除{entity_name}记录",
                params=["id"],
                resource=resource,
                action_type="delete"
            ),
        ]

    def _infer_business_endpoints_from_buttons(self, resource: str, buttons: List[ActionButton]) -> List[APIEndpoint]:
        """从按钮推断业务操作接口（通用版 - 动态生成，不硬编码业务词汇）"""
        endpoints = []

        # 已处理的按钮名（避免重复）
        processed = set()

        for btn in buttons:
            btn_name = btn.name

            # 跳过已处理的按钮
            if btn_name in processed:
                continue
            processed.add(btn_name)

            # 跳过基础CRUD按钮（已经在CRUD端点中处理）
            basic_buttons = ['搜索', '查询', '重置', '清空', '新增', '添加', '创建', '删除', '移除',
                             '编辑', '修改', '查看', '详情']
            if btn_name in basic_buttons:
                continue

            # 根据按钮名称动态生成接口
            # 1. 生成英文动作名
            action_name = self._button_name_to_action(btn_name)

            if action_name:
                # 推断HTTP方法（默认POST用于操作按钮）
                method = 'POST'
                if btn.category in ['view', 'search']:
                    method = 'GET'
                elif btn.category == 'export':
                    method = 'GET'

                endpoints.append(APIEndpoint(
                    path=f"/api/{resource}/{action_name}",
                    method=method,
                    name=btn_name,
                    description=f"{btn_name}操作",
                    params=['ids'] if method == 'POST' else [],
                    resource=resource,
                    action_type='action'
                ))

        return endpoints

    def _button_name_to_action(self, btn_name: str) -> str:
        """将按钮名称转换为接口动作名（通用版 - 动态转换）"""
        name = btn_name.lower()

        # 通用动作词转换（跨领域通用）
        common_actions = {
            '确认': 'confirm',
            '取消': 'cancel',
            '提交': 'submit',
            '审核': 'audit',
            '批准': 'approve',
            '作废': 'void',
            '撤回': 'withdraw',
            '刷新': 'refresh',
            '导出': 'export',
            '导入': 'import',
            '打印': 'print',
            '分配': 'assign',
            '处理': 'process',
            '退回': 'return',
            '推送': 'push',
            '生成': 'generate',
        }

        for chinese, english in common_actions.items():
            if chinese in name:
                return english

        # 如果包含"申请"或"预约"，使用apply
        if '申请' in name or '预约' in name:
            return 'apply'

        # 对于其他按钮名称，尝试生成英文动作
        # 使用按钮名称的URL安全版本
        import re
        safe_name = re.sub(r'[^\w]', '_', name)
        ascii_only = re.sub(r'[^\x00-\x7F]', '', safe_name)

        if ascii_only and ascii_only.replace('_', ''):
            return ascii_only.lower().replace('_', '-')

        # 无法转换的中文按钮名，返回空（跳过）
        return ''

    def _generate_database_tables(self, menus: List[MenuItem], page_views: List[PageView]) -> List[DatabaseTable]:
        """生成数据库表设计（增强版 - 根据页面结构推断完整表结构）"""
        tables = []

        # 根据菜单推断主实体表
        for menu in menus:
            if menu.page_id and 'javascript' not in menu.page_id.lower():
                entity_name = menu.name
                table_name = self._infer_table_name(menu)
                if table_name:
                    # 查找对应的页面视图获取列信息
                    matching_view = None
                    for pv in page_views:
                        if pv.view_id and menu.page_id in pv.view_id:
                            matching_view = pv
                            break

                    columns = []
                    status_enum = None

                    if matching_view:
                        # 从表格列提取字段
                        columns = self._extract_columns_from_view(matching_view)
                        # 从状态Tab提取状态枚举
                        status_enum = self._extract_status_enum_from_tabs(matching_view.status_tabs)

                    tables.append(DatabaseTable(
                        table_name=table_name,
                        entity_name=entity_name,
                        columns=columns,
                        indexes=[],
                        foreign_keys=[],
                        status_enum=status_enum,
                        is_main_entity=True
                    ))

        # 根据页面视图中的明细表推断子表
        for pv in page_views:
            for table_info in pv.tables:
                if not table_info.is_main_table and table_info.columns:
                    detail_table_name = f"{pv.view_id.replace('-', '_')}_detail_{table_info.table_index}"
                    columns = self._convert_table_columns_to_db_columns(table_info.columns)

                    tables.append(DatabaseTable(
                        table_name=detail_table_name,
                        entity_name=f"{pv.name}明细{table_info.table_index}",
                        columns=columns,
                        indexes=[],
                        foreign_keys=[{
                            'column': 'parent_id',
                            'ref_table': pv.view_id.replace('-', '_'),
                            'ref_column': 'id'
                        }],
                        status_enum=None,
                        is_main_entity=False
                    ))

        # 添加基础数据表（通用推断）
        base_tables = self._infer_base_tables_from_filters(page_views)
        tables.extend(base_tables)

        return tables

    def _infer_table_name(self, menu: MenuItem) -> str:
        """推断表名"""
        page_id = menu.page_id or ''

        if page_id:
            return page_id.replace('-', '_')

        return menu.name.lower().replace(' ', '_').replace('-', '_')

    def _extract_columns_from_view(self, pv: PageView) -> List[Dict[str, str]]:
        """从页面视图提取数据库列定义"""
        columns = []

        # 主键
        columns.append({
            'name': 'id',
            'type': 'VARCHAR(36)',
            'constraint': 'PRIMARY KEY',
            'comment': '主键ID'
        })

        # 从筛选字段提取
        for filter_field in pv.filters:
            col_name = filter_field.name.lower().replace(' ', '_').replace('/', '_')
            col_type = self._infer_column_type_from_filter(filter_field)
            columns.append({
                'name': col_name,
                'type': col_type,
                'constraint': '',
                'comment': filter_field.name
            })

        # 从主表列提取
        for table_info in pv.tables:
            if table_info.is_main_table:
                for col in table_info.columns:
                    col_name = col.name.lower().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')
                    col_type = self._infer_column_type_from_table_column(col)
                    columns.append({
                        'name': col_name,
                        'type': col_type,
                        'constraint': '',
                        'comment': col.name
                    })
                break

        # 标准字段
        columns.extend([
            {'name': 'created_at', 'type': 'TIMESTAMP', 'constraint': 'DEFAULT CURRENT_TIMESTAMP', 'comment': '创建时间'},
            {'name': 'updated_at', 'type': 'TIMESTAMP', 'constraint': 'DEFAULT CURRENT_TIMESTAMP', 'comment': '更新时间'},
            {'name': 'created_by', 'type': 'VARCHAR(50)', 'constraint': '', 'comment': '创建人'},
            {'name': 'updated_by', 'type': 'VARCHAR(50)', 'constraint': '', 'comment': '更新人'},
        ])

        return columns

    def _infer_column_type_from_filter(self, filter_field: FilterField) -> str:
        """从筛选字段推断列类型"""
        if filter_field.type == 'select':
            return 'VARCHAR(100)'
        if filter_field.type in ['text', 'input']:
            return 'VARCHAR(200)'
        if filter_field.type == 'date':
            return 'DATE'
        if filter_field.type == 'number':
            return 'DECIMAL(10,2)'
        return 'VARCHAR(200)'

    def _infer_column_type_from_table_column(self, col: TableColumn) -> str:
        """从表格列推断数据库列类型"""
        type_mapping = {
            'text': 'VARCHAR(200)',
            'link': 'VARCHAR(100)',
            'number': 'DECIMAL(10,2)',
            'currency': 'DECIMAL(10,2)',
            'percentage': 'DECIMAL(5,2)',
            'date': 'DATE',
            'badge': 'VARCHAR(50)',
            'image': 'VARCHAR(500)',
            'progress': 'VARCHAR(50)',
            'empty': 'VARCHAR(200)',
        }
        return type_mapping.get(col.data_type, 'VARCHAR(200)')

    def _convert_table_columns_to_db_columns(self, columns: List[TableColumn]) -> List[Dict[str, str]]:
        """将表格列转换为数据库列定义"""
        db_columns = []

        # 主键和外键
        db_columns.append({
            'name': 'id',
            'type': 'VARCHAR(36)',
            'constraint': 'PRIMARY KEY',
            'comment': '明细ID'
        })
        db_columns.append({
            'name': 'parent_id',
            'type': 'VARCHAR(36)',
            'constraint': 'NOT NULL',
            'comment': '父记录ID'
        })

        for col in columns:
            col_name = col.name.lower().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')
            col_type = self._infer_column_type_from_table_column(col)
            db_columns.append({
                'name': col_name,
                'type': col_type,
                'constraint': '',
                'comment': col.name
            })

        return db_columns

    def _extract_status_enum_from_tabs(self, status_tabs: List[StatusTab]) -> str:
        """从状态Tab提取状态枚举定义"""
        if not status_tabs:
            return None

        status_values = [tab.name for tab in status_tabs if tab.name]
        if status_values:
            quoted_values = [f"'{s}'" for s in status_values]
            return f"ENUM({', '.join(quoted_values)})"
        return None

    def _infer_base_tables_from_filters(self, page_views: List[PageView]) -> List[DatabaseTable]:
        """从筛选字段的下拉选项推断基础数据表（通用版 - 动态推断）"""
        base_tables = []
        seen_entities = set()

        for pv in page_views:
            for filter_field in pv.filters:
                if filter_field.type == 'select' and filter_field.options:
                    # 从字段名推断实体（通用处理）
                    field_name = filter_field.name

                    # 跳过无效的字段名
                    if field_name in ['', '全部', '类型', '状态']:
                        continue

                    # 跳过状态类型的筛选（通常不需要单独的基础表）
                    if '状态' in field_name or '进度' in field_name or '溢价' in field_name:
                        continue

                    # 动态生成表名
                    # 使用字段名的英文转换
                    table_name = self._field_name_to_table_name(field_name)

                    if table_name and table_name not in seen_entities:
                        seen_entities.add(table_name)

                        # 生成基础表结构
                        columns = [
                            {'name': 'id', 'type': 'VARCHAR(36)', 'constraint': 'PRIMARY KEY', 'comment': '主键'},
                            {'name': 'name', 'type': 'VARCHAR(100)', 'constraint': 'NOT NULL', 'comment': '名称'},
                            {'name': 'code', 'type': 'VARCHAR(50)', 'constraint': '', 'comment': '编码'},
                            {'name': 'status', 'type': 'VARCHAR(20)', 'constraint': 'DEFAULT "active"', 'comment': '状态'},
                            {'name': 'sort_order', 'type': 'INT', 'constraint': 'DEFAULT 0', 'comment': '排序'},
                            {'name': 'created_at', 'type': 'TIMESTAMP', 'constraint': 'DEFAULT CURRENT_TIMESTAMP', 'comment': '创建时间'},
                        ]

                        base_tables.append(DatabaseTable(
                            table_name=table_name,
                            entity_name=field_name,
                            columns=columns,
                            indexes=['name'],
                            foreign_keys=[],
                            status_enum=None,
                            is_main_entity=False
                        ))

        return base_tables

    def _field_name_to_table_name(self, field_name: str) -> str:
        """将字段名转换为表名（通用版 - 动态推断）"""
        name = field_name.lower()

        # 跳过明显不是独立实体的筛选字段
        skip_keywords = ['状态', '进度', '时间', '日期', '范围', '溢价', '打标', '标签', '备注']
        for kw in skip_keywords:
            if kw in field_name:
                return ''

        # 根据字段名后缀推断表名（跨领域通用的命名模式）
        # 注意：这些是命名模式，不是业务词汇
        suffix_patterns = {
            '人': 'persons',      # 任何系统的"人"相关实体
            '员': 'persons',      # 任何系统的"员"相关实体
            '公司': 'companies',  # 任何系统的公司相关
            '主体': 'companies',  # 任何系统的主体相关
            '仓': 'warehouses',   # 任何系统的仓库相关（仓储、ERP等）
            '库': 'warehouses',   # 任何系统的库相关
            '品牌': 'brands',     # 任何系统的品牌相关
            '分类': 'categories', # 任何系统的分类相关
            '类型': 'types',      # 任何系统的类型相关
            '部门': 'departments', # 任何系统的部门相关
            '角色': 'roles',      # 任何系统的角色相关
            '渠道': 'channels',   # 任何系统的渠道相关
        }

        for chinese, english in suffix_patterns.items():
            if chinese in name:
                return english

        # 尝试将中文转换为英文（使用字段ID中的信息）
        # 如果有英文信息在字段名中，使用它
        import re
        ascii_parts = re.findall(r'[a-zA-Z]+', field_name)
        if ascii_parts:
            return ascii_parts[0].lower()

        # 对于其他字段名，尝试生成合理的表名
        # 使用字段名的URL安全版本作为表名
        safe_name = re.sub(r'[^\w]', '_', name)
        ascii_only = re.sub(r'[^\x00-\x7F]', '', safe_name)

        if ascii_only and ascii_only.replace('_', ''):
            return ascii_only.lower()

        # 无法推断的，返回空（跳过）
        return ''

    def _generate_entity_relations(self, tables: List[DatabaseTable]) -> List[EntityRelation]:
        """生成实体关系"""
        relations = []

        # 主表与明细表的关系
        main_tables = [t for t in tables if t.is_main_entity]
        detail_tables = [t for t in tables if not t.is_main_entity]

        for main in main_tables:
            for detail in detail_tables:
                # 检查是否有外键指向主表
                for fk in detail.foreign_keys:
                    if fk['ref_table'] == main.table_name:
                        relations.append(EntityRelation(
                            from_entity=main.table_name,
                            to_entity=detail.table_name,
                            relation_type='one_to_many',
                            description=f"{main.entity_name}包含多条{detail.entity_name}"
                        ))

        # 基础表与主表的关系
        base_tables = [t for t in tables if not t.is_main_entity and 'detail' not in t.table_name]
        for main in main_tables:
            for base in base_tables:
                # 检查主表是否有指向基础表的字段
                for col in main.columns:
                    if base.table_name.rstrip('s') in col['name'].lower():
                        relations.append(EntityRelation(
                            from_entity=main.table_name,
                            to_entity=base.table_name,
                            relation_type='many_to_one',
                            description=f"{main.entity_name}关联{base.entity_name}"
                        ))

        return relations

    def _extract_status_enums(self, page_views: List[PageView]) -> Dict[str, List[str]]:
        """提取所有状态枚举"""
        enums = {}

        for pv in page_views:
            for tab in pv.status_tabs:
                # 根据状态Tab所在区域推断枚举名称
                enum_name = f"{pv.view_id}_status"
                if enum_name not in enums:
                    enums[enum_name] = []
                if tab.name and tab.name not in enums[enum_name]:
                    enums[enum_name].append(tab.name)

        return enums