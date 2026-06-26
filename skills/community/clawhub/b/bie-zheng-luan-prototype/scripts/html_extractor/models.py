"""
数据结构定义模块
定义HTML解析结果的数据结构（@dataclass）
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class MenuItem:
    """菜单项"""
    group: str               # 分组名（如"系统管理"）
    name: str                # 菜单名（如"用户列表"）
    icon: str                # SVG图标精确描述
    icon_svg: str            # SVG原始代码（用于前端还原）
    page_id: str             # 页面标识（data-scm-page）
    href: str                # 链接地址
    is_active: bool          # 是否当前激活


@dataclass
class UserInfo:
    """用户信息"""
    avatar_text: str         # 头像文字（如"A"）
    name: str                # 用户姓名（如"张三"）
    role: str                # 用户角色（如"管理员"）


@dataclass
class SidebarInfo:
    """侧边栏信息"""
    has_toggle: bool         # 是否有折叠按钮
    toggle_button_id: str    # 折叠按钮ID
    user_info: UserInfo      # 用户信息


@dataclass
class PageTab:
    """页面标签"""
    name: str                # 标签名称
    is_active: bool          # 是否当前激活
    has_close: bool          # 是否有关闭按钮


@dataclass
class SubPill:
    """子标签（工作台切换）"""
    name: str                # 标签名称
    pill_id: str             # 标签ID
    is_active: bool          # 是否当前激活
    target_panel: str        # 目标面板ID


@dataclass
class FilterField:
    """筛选字段"""
    name: str                # 字段名（如"分类"）
    type: str                # 类型：select/input/text/date
    options: List[str]       # 下拉选项（如["全部", "选项A", "选项B"]）
    placeholder: str         # 占位符（input类型）
    filter_id: str           # 筛选器ID（如"filter-1")
    default_value: str       # 默认值


@dataclass
class TableColumn:
    """表格列"""
    name: str                # 列名（如"单号"）
    data_type: str           # 数据类型推断：text/link/number/badge/progress/date/image/currency/percentage
    sortable: bool           # 是否可排序
    table_index: int         # 所属表格索引（用于区分多个表格）
    is_detail: bool          # 是否是明细子表列


@dataclass
class ActionButton:
    """操作按钮"""
    name: str                # 按钮名
    category: str            # 分类：search/action/export/edit/delete/create/confirm/view/reset/other
    style: str               # 样式：primary/default/danger/warning
    button_id: str           # 按钮ID
    icon: str                # 按钮图标描述（如果有）
    location: str            # 按钮位置：toolbar/filter/table/modal


@dataclass
class StatCard:
    """统计卡片"""
    title: str               # 卡片标题（如"待处理事项"）
    value: str               # 数值
    subtitle: str            # 子标题/说明
    color_type: str          # 颜色类型：blue/orange/purple/red/yellow/pink
    icon_svg: str            # SVG图标代码


@dataclass
class MessageCard:
    """消息通知卡片"""
    dot_visible: bool        # 是否有未读标记点
    headline: str            # 标题
    content: str             # 正文内容
    time: str                # 时间
    participants: int        # 参与人数
    comments: int            # 评论数
    action_button: str       # 操作按钮
    action_button_style: str # 按钮样式


@dataclass
class StaffCard:
    """人员工作进度卡片"""
    avatar: str              # 头像（可能是图片或文字）
    name: str                # 姓名
    tag: str                 # 标签
    tag_color: str           # 标签颜色
    stats: Dict[str, str]    # 统计数据
    overdue_count: int       # 已逾期数量
    action_buttons: List[str] # 操作按钮列表


@dataclass
class StatusTab:
    """状态筛选Tab"""
    name: str                # 状态名称
    count: int               # 数量
    color_type: str          # 颜色类型：default/orange/green/red/pink
    is_active: bool          # 是否当前激活
    filter_key: str          # 筛选键


@dataclass
class ProgressItem:
    """进度条组件"""
    status_dot_color: str    # 状态点颜色（blue/orange/green/red）
    name: str                # 名称
    detail: str              # 详情
    status_label: str        # 状态标签
    status_label_color: str  # 状态标签颜色
    date: str                # 日期


@dataclass
class DrawerAnchorLink:
    """弹窗锚点导航链接"""
    name: str                # 锚点名称
    anchor_key: str          # 锚点键（data-anchor）
    is_active: bool          # 是否当前激活


@dataclass
class DrawerFormField:
    """弹窗内表单字段"""
    name: str                # 字段名
    type: str                # 类型：select/input/textarea
    is_required: bool        # 是否必填
    options: List[str]       # 下拉选项（select类型）
    placeholder: str         # 占位符（input/textarea类型）
    field_id: str            # 字段ID
    is_full_width: bool      # 是否占整行


@dataclass
class DrawerStatistics:
    """弹窗内统计信息"""
    name: str                # 统计项名称（如"事项"）
    value: str               # 数值
    color_type: str          # 颜色类型


@dataclass
class DrawerPanel:
    """弹窗/抽屉面板"""
    panel_id: str            # 弹窗ID（如"drawer-detail"）
    title: str               # 弹窗标题（如"详情查看"）
    title_icon: str          # 标题图标描述
    status_badge_id: str     # 状态badge元素ID
    no_element_id: str       # 单号元素ID
    anchor_links: List[DrawerAnchorLink]  # 锚点导航
    form_fields: List[DrawerFormField]    # 表单字段
    statistics: List[DrawerStatistics]    # 统计信息
    inner_buttons: List[ActionButton]     # 弹窗内按钮
    has_search_box: bool     # 是否有搜索框
    search_placeholder: str  # 搜索框占位符
    has_timeline: bool       # 是否有操作日志时间线


@dataclass
class TableInfo:
    """表格信息"""
    table_index: int         # 表格索引
    table_class: str         # 表格class
    is_main_table: bool      # 是否主表
    columns: List[TableColumn]  # 列信息
    has_checkbox: bool       # 是否有勾选列


@dataclass
class PageView:
    """页面视图"""
    view_id: str             # 页面视图ID（如"view-user-list"）
    name: str                # 页面名称推断
    filters: List[FilterField] = field(default_factory=list)
    tables: List[TableInfo] = field(default_factory=list)
    buttons: List[ActionButton] = field(default_factory=list)
    stat_cards: List[StatCard] = field(default_factory=list)
    message_cards: List[MessageCard] = field(default_factory=list)
    staff_cards: List[StaffCard] = field(default_factory=list)
    sub_pills: List[SubPill] = field(default_factory=list)
    status_tabs: List[StatusTab] = field(default_factory=list)
    progress_items: List[ProgressItem] = field(default_factory=list)
    drawer_panels: List[DrawerPanel] = field(default_factory=list)


@dataclass
class APIEndpoint:
    """API接口端点"""
    path: str               # 接口路径
    method: str             # HTTP方法（GET/POST/PUT/DELETE）
    name: str               # 接口名称
    description: str        # 接口描述
    params: List[str]       # 参数列表
    resource: str           # 资源名称
    action_type: str        # 操作类型


@dataclass
class DatabaseTable:
    """数据库表设计"""
    table_name: str         # 表名
    entity_name: str        # 实体名称
    columns: List[Dict[str, str]]  # 列定义
    indexes: List[str]      # 索引列表
    foreign_keys: List[Dict[str, str]]  # 外键关系
    status_enum: Optional[str]  # 状态枚举定义（如有）
    is_main_entity: bool    # 是否主实体


@dataclass
class EntityRelation:
    """实体关系"""
    from_entity: str        # 源实体
    to_entity: str          # 目标实体
    relation_type: str      # 关系类型（one_to_many/many_to_many/one_to_one）
    description: str        # 关系描述


@dataclass
class TechImplementation:
    """技术实现建议"""
    routes: List[Dict[str, str]]     # 路由配置
    api_endpoints: List[APIEndpoint] # API接口列表
    database_tables: List[DatabaseTable]  # 数据库表列表
    entity_relations: List[EntityRelation]  # 实体关系
    status_enums: Dict[str, List[str]]  # 状态枚举映射


@dataclass
class PrototypeAnalysis:
    """原型分析结果"""
    system_name: str         # 系统名称
    title: str               # 页面标题
    menus: List[MenuItem]    # 菜单结构
    sidebar: SidebarInfo     # 侧边栏信息
    page_tabs: List[PageTab] # 页面标签栏
    page_views: List[PageView]  # 页面视图列表
    total_filters: int       # 总筛选字段数
    total_columns: int       # 总表格列数
    total_buttons: int       # 总按钮数
    analysis_time: str       # 分析时间
    tech_implementation: Optional[TechImplementation] = None  # 技术实现建议


# ==================== 业务流程分析相关数据结构 ====================

@dataclass
class OperationAnalysis:
    """操作分析结果"""
    name: str                # 操作名称
    category: str            # 操作类别
    requires_selection: bool # 是否需要勾选记录
    possible_states: List[str]  # 推断的可执行状态
    description: str         # 功能描述

@dataclass
class PageAnalysis:
    """单个页面的业务分析结果"""
    page_name: str           # 页面名称
    view_id: str             # 视图ID
    inferred_role: str       # 推断的页面角色（入口/处理/查看/配置）
    operations: List[OperationAnalysis]  # 操作列表
    key_fields: List[str]    # 关键字段
    status_fields: List[str] # 状态相关字段
    filter_dimensions: List[str]  # 筛选维度
    has_checkbox: bool       # 是否有勾选列（支持批量操作）

@dataclass
class FlowHypothesis:
    """流程假设"""
    sequence: List[str]          # 页面流转顺序
    confidence: float            # 置信度（0-1）
    evidence: List[str]          # 推断依据

@dataclass
class StatusTransition:
    """状态流转假设"""
    page_name: str               # 页面名称
    status_field: str            # 状态字段名
    possible_values: List[str]   # 可能的状态值
    transitions: List[str]       # 推断的流转规则
    evidence: List[str]          # 推断依据

@dataclass
class AnalysisQuestion:
    """生成的问题"""
    category: str      # 问题类别（flow/status/permission/field/operation）
    priority: str      # 优先级（high/medium/low）
    question: str      # 问题内容
    context: str       # 问题上下文/推断依据
    options: List[str] # 建议选项（如果有）

@dataclass
class InteractiveAnalysis:
    """交互式分析结果"""
    system_name: str
    page_analyses: List[PageAnalysis]
    flow_hypothesis: FlowHypothesis
    status_transitions: List[StatusTransition]
    questions: List[AnalysisQuestion]
    analysis_summary: str  # 分析总结