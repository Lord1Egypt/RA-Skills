#!/usr/bin/env python3
"""
技术文档生成器
将页面分析结果转换为详细的技术规格文档
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import argparse

class SpecGenerator:
    """技术文档生成器"""
    
    def __init__(self, template_file: str = None):
        self.template = self._load_template(template_file)
        # 加载参考文件内容
        self._load_references()
    
    def _load_references(self):
        """加载参考文件内容，用于填充文档章节"""
        # 脚本所在目录的上级目录下的 references/
        script_dir = Path(__file__).resolve().parent
        ref_dir = script_dir.parent / 'references'
        
        self.ref_template_spec = self._read_ref_file(ref_dir / 'template-spec.md')
        self.ref_api_design = self._read_ref_file(ref_dir / 'api-design.md')
        self.ref_component_catalog = self._read_ref_file(ref_dir / 'component-catalog.md')
    
    def _read_ref_file(self, filepath: Path) -> str:
        """安全读取参考文件内容"""
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception:
            pass
        return None
    
    def _load_template(self, template_file: str = None) -> str:
        """加载文档模板"""
        if template_file and Path(template_file).exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        
        # 默认模板
        return """# 产品原型技术分析文档

## 文档信息
- **原型来源**: {url}
- **分析时间**: {analysis_time}
- **文档版本**: v1.0
- **技能版本**: bie-zheng-luan-prototype v1.1.0

## 1. 系统概览

### 1.1 产品简介
{product_intro}

### 1.2 技术栈建议
{tech_stack}

### 1.3 核心业务流程
{core_workflow}

## 2. 页面结构分析

### 2.1 整体布局
{layout_analysis}

### 2.2 导航菜单结构
{navigation_structure}

### 2.3 功能模块清单
{module_list}

## 3. 前端实现方案

### 3.1 页面路由规划
{routing_plan}

### 3.2 组件清单
{component_list}

### 3.3 样式规范
{style_spec}

### 3.4 交互细节
{interaction_details}

## 4. 后端实现方案

### 4.1 API接口设计
{api_design}

### 4.2 服务层设计
{service_design}

### 4.3 第三方服务集成
{third_party_integration}

## 5. 数据库设计

### 5.1 数据库表清单
{database_tables}

### 5.2 实体关系图
{entity_relationship}

## 6. 部署与运维

### 6.1 环境配置
{environment_config}

### 6.2 监控指标
{monitoring_metrics}

### 6.3 备份策略
{backup_strategy}

## 7. 测试要点

### 7.1 单元测试
{unit_tests}

### 7.2 集成测试
{integration_tests}

### 7.3 性能测试
{performance_tests}

## 8. 开发注意事项

### 8.1 安全性
{security_considerations}

### 8.2 性能优化
{performance_optimization}

### 8.3 可维护性
{maintainability}

---

## 文档生成信息
- **生成工具**: bie-zheng-luan-prototype v1.1.0
- **生成时间**: {generation_time}
- **置信度评估**: {confidence_level}
- **建议复核**: {review_suggestion}

> **注意**: 本文档为技术分析结果，实际开发前应与产品经理确认需求细节。
"""
    
    def generate_from_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """从分析数据生成文档"""
        
        # 准备模板变量
        template_vars = {
            'url': analysis_data.get('url', '未知URL'),
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'product_intro': self._generate_product_intro(analysis_data),
            'tech_stack': self._generate_tech_stack(analysis_data),
            'core_workflow': self._generate_core_workflow(analysis_data),
            'layout_analysis': self._generate_layout_analysis(analysis_data),
            'navigation_structure': self._generate_navigation_structure(analysis_data),
            'module_list': self._generate_module_list(analysis_data),
            'routing_plan': self._generate_routing_plan(analysis_data),
            'component_list': self._generate_component_list(analysis_data),
            'style_spec': self._generate_style_spec(analysis_data),
            'interaction_details': self._generate_interaction_details(analysis_data),
            'api_design': self._generate_api_design(analysis_data),
            'service_design': self._generate_service_design(analysis_data),
            'third_party_integration': self._generate_third_party_integration(analysis_data),
            'database_tables': self._generate_database_tables(analysis_data),
            'entity_relationship': self._generate_entity_relationship(analysis_data),
            'environment_config': self._generate_environment_config(analysis_data),
            'monitoring_metrics': self._generate_monitoring_metrics(analysis_data),
            'backup_strategy': self._generate_backup_strategy(analysis_data),
            'unit_tests': self._generate_unit_tests(analysis_data),
            'integration_tests': self._generate_integration_tests(analysis_data),
            'performance_tests': self._generate_performance_tests(analysis_data),
            'security_considerations': self._generate_security_considerations(analysis_data),
            'performance_optimization': self._generate_performance_optimization(analysis_data),
            'maintainability': self._generate_maintainability(analysis_data),
            'confidence_level': self._assess_confidence(analysis_data),
            'review_suggestion': self._get_review_suggestion(analysis_data),
        }
        
        # 应用模板
        document = self.template
        for key, value in template_vars.items():
            placeholder = '{' + key + '}'
            document = document.replace(placeholder, value)
        
        return document
    
    def _generate_product_intro(self, analysis_data: Dict[str, Any]) -> str:
        """生成产品简介"""
        title = analysis_data.get('title', '')
        
        # 基于页面标题和元素推断产品类型
        if any(word in title.lower() for word in ['dashboard', '控制台', '后台']):
            product_type = "管理后台系统"
        elif any(word in title.lower() for word in ['shop', 'store', '商城', '电商']):
            product_type = "电子商务平台"
        elif any(word in title.lower() for word in ['blog', 'news', '内容', '文章']):
            product_type = "内容管理系统"
        elif any(word in title.lower() for word in ['user', '用户', 'member', '会员']):
            product_type = "用户管理系统"
        else:
            product_type = "业务管理系统"
        
        intro = f"{product_type}，基于分析的原型页面，主要功能包括：\n\n"
        
        # 基于交互元素推断功能
        interactive_elements = analysis_data.get('interactive_elements', [])
        forms = analysis_data.get('forms', [])
        
        if interactive_elements:
            button_texts = [e.get('text', '') for e in interactive_elements if e.get('type') == 'button']
            unique_buttons = list(set([bt for bt in button_texts if bt]))[:5]
            
            if unique_buttons:
                intro += "**主要操作**:\n"
                for btn in unique_buttons:
                    intro += f"- {btn}\n"
                intro += "\n"
        
        if forms:
            intro += f"**数据管理**:\n"
            intro += f"- 包含 {len(forms)} 个表单，用于数据录入和编辑\n"
            
            total_fields = sum(len(form.get('fields', [])) for form in forms)
            intro += f"- 共计 {total_fields} 个数据字段需要管理\n\n"
        
        intro += "**目标用户**: 系统管理员、普通用户、访客等\n"
        
        return intro
    
    def _generate_tech_stack(self, analysis_data: Dict[str, Any]) -> str:
        """生成技术栈建议"""
        tech_stack = """
- **前端框架**: React 18 + TypeScript（组件化开发，类型安全）
- **UI组件库**: Ant Design 5.x（企业级设计系统，组件丰富）
- **状态管理**: Redux Toolkit + React Query（数据流管理，API缓存）
- **构建工具**: Vite 5.x（快速构建，开发体验优秀）
- **样式方案**: Tailwind CSS + CSS Modules（原子化CSS，样式隔离）
- **路由管理**: React Router 6.x（声明式路由，嵌套路由支持）

- **后端框架**: Node.js + Express 或 .NET Core 6（根据团队技术栈选择）
- **数据库**: PostgreSQL 15（关系型数据库，JSON支持）
- **ORM框架**: Prisma 或 TypeORM（类型安全的数据访问层）
- **API文档**: Swagger/OpenAPI 3.0（自动生成API文档）
- **认证授权**: JWT + Refresh Token（无状态认证，安全可靠）
- **缓存层**: Redis 7.x（会话缓存，数据缓存）

- **部署环境**: Docker + Docker Compose（容器化部署）
- **反向代理**: Nginx 1.24（静态资源，负载均衡）
- **监控日志**: Prometheus + Grafana + ELK Stack（系统监控，日志分析）
- **CI/CD**: GitHub Actions 或 GitLab CI（自动化部署）
"""
        return tech_stack
    
    def _generate_core_workflow(self, analysis_data: Dict[str, Any]) -> str:
        """生成核心业务流程"""
        # 基于表单和交互元素推断流程
        forms = analysis_data.get('forms', [])
        
        if forms:
            workflow = "```mermaid\ngraph TD\n    A[用户访问] --> B[身份验证]\n"
            
            for i, form in enumerate(forms[:3]):  # 最多显示3个表单流程
                form_name = form.get('id', f'表单{i+1}')
                action = form.get('action', '')
                
                if action:
                    workflow += f"    B --> C{ i }[填写{form_name}]\n"
                    workflow += f"    C{ i } --> D{ i }[提交数据]\n"
                    workflow += f"    D{ i } --> E{ i }[数据验证]\n"
                    workflow += f"    E{ i } --> F{ i }[保存到数据库]\n"
                    workflow += f"    F{ i } --> G{ i }[显示结果]\n"
                    
                    if i < len(forms) - 1:
                        workflow += f"    G{ i } --> C{ i+1 }\n"
            
            workflow += "    G2 --> H[完成操作]\n```"
        else:
            workflow = "```\n1. 用户访问系统\n2. 浏览页面内容\n3. 进行交互操作\n4. 获取反馈结果\n```"
        
        return workflow
    
    def _generate_layout_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """生成布局分析"""
        layout_elements = analysis_data.get('layout_elements', [])
        
        if not layout_elements:
            return "基于标准网页布局分析：\n- 头部：Logo、导航菜单\n- 侧边栏：功能菜单（可选）\n- 主内容区：核心功能模块\n- 底部：版权信息、辅助链接"
        
        layout_analysis = "| 区域 | 位置 | 包含内容 | 宽度占比 | 固定/滚动 |\n|------|------|----------|----------|-----------|\n"
        
        # 识别常见的布局区域
        regions = {
            'header': ['header', '头部', '顶部'],
            'sidebar': ['sidebar', '侧边栏', '左边栏', '右边栏'],
            'main': ['main', '内容区', '主体'],
            'footer': ['footer', '底部', '页脚']
        }
        
        identified_regions = set()
        
        for layout in layout_elements[:10]:  # 限制数量
            selector = layout.get('selector', '')
            tag = layout.get('tag', '')
            classes = layout.get('classes', [])
            text_preview = layout.get('text_preview', '')[:50]
            
            # 判断区域类型
            region_type = '其他'
            for reg_name, keywords in regions.items():
                if any(keyword in selector.lower() or 
                       any(keyword in cls.lower() for cls in classes if isinstance(cls, str)) 
                       for keyword in keywords):
                    region_type = reg_name
                    break
            
            if region_type not in identified_regions:
                identified_regions.add(region_type)
                
                # 确定宽度占比和固定性
                width_percent = '100%' if region_type in ['header', 'footer'] else '15-20%' if region_type == 'sidebar' else '剩余宽度'
                fixed_scroll = '固定' if region_type in ['header', 'sidebar', 'footer'] else '滚动'
                
                content_desc = {
                    'header': '品牌Logo、导航菜单、用户信息',
                    'sidebar': '功能菜单、快捷操作、筛选器',
                    'main': '数据展示、功能模块、操作区域',
                    'footer': '版权信息、备案号、辅助链接',
                    '其他': text_preview or '功能模块'
                }
                
                layout_analysis += f"| {region_type} | {'顶部' if region_type == 'header' else '左侧' if region_type == 'sidebar' else '中间' if region_type == 'main' else '底部'} | {content_desc[region_type]} | {width_percent} | {fixed_scroll} |\n"
        
        return layout_analysis
    
    def _generate_navigation_structure(self, analysis_data: Dict[str, Any]) -> str:
        """生成导航菜单结构"""
        navigation = analysis_data.get('navigation', [])
        
        if not navigation:
            return "```yaml\n# 基于标准管理后台的导航结构\n一级菜单:\n  - 仪表盘:\n      icon: Dashboard\n      path: /dashboard\n      无子菜单\n  \n  - 数据管理:\n      icon: Database\n      path: /data\n      二级菜单:\n        - 用户管理: /data/users\n        - 产品管理: /data/products\n        \n  - 系统设置:\n      icon: Settings\n      path: /settings\n      二级菜单:\n        - 参数配置: /settings/config\n        - 日志查看: /settings/logs\n```"
        
        yaml_structure = "```yaml\n"
        
        for i, nav in enumerate(navigation[:3]):  # 限制数量
            nav_type = nav.get('type', 'nav')
            items = nav.get('items', [])
            
            yaml_structure += f"{nav_type}:\n"
            
            # 分组菜单项（假设相似的文本属于同一菜单）
            menu_items = {}
            for item in items:
                text = item.get('text', '')
                if text:
                    # 简单分组：按第一个词分组
                    first_word = text.split()[0] if ' ' in text else text[:10]
                    if first_word not in menu_items:
                        menu_items[first_word] = []
                    menu_items[first_word].append(item)
            
            for menu_name, sub_items in list(menu_items.items())[:5]:  # 限制数量
                yaml_structure += f"  - {menu_name}:\n"
                yaml_structure += f"      icon: {self._get_icon_for_menu(menu_name)}\n"
                yaml_structure += f"      path: /{menu_name.lower().replace(' ', '-')}\n"
                
                if len(sub_items) > 1:
                    yaml_structure += f"      二级菜单:\n"
                    for sub_item in sub_items[:5]:  # 限制数量
                        sub_text = sub_item.get('text', '')
                        sub_href = sub_item.get('href', '')
                        if sub_text:
                            path = sub_href if sub_href and not sub_href.startswith('#') else f"/{menu_name.lower()}/{sub_text.lower().replace(' ', '-')}"
                            yaml_structure += f"        - {sub_text}: {path}\n"
                else:
                    yaml_structure += f"      无子菜单\n"
            
            if i < len(navigation) - 1:
                yaml_structure += "\n"
        
        yaml_structure += "```"
        return yaml_structure
    
    def _get_icon_for_menu(self, menu_name: str) -> str:
        """根据菜单名称获取图标"""
        icon_map = {
            '用户': 'User',
            '产品': 'Product',
            '单据': 'FileText',
            '设置': 'Settings',
            '仪表盘': 'Dashboard',
            '数据': 'Database',
            '文件': 'File',
            '消息': 'Message',
            '通知': 'Bell',
            '帮助': 'HelpCircle',
            '首页': 'Home',
            '搜索': 'Search',
            '添加': 'Plus',
            '编辑': 'Edit',
            '删除': 'Trash',
            '查看': 'Eye',
            '下载': 'Download',
            '上传': 'Upload',
            '导出': 'Export',
            '导入': 'Import',
        }
        
        for key, icon in icon_map.items():
            if key in menu_name:
                return icon
        
        return 'Folder'  # 默认图标
    
    def _generate_module_list(self, analysis_data: Dict[str, Any]) -> str:
        """生成功能模块清单"""
        interactive_elements = analysis_data.get('interactive_elements', [])
        forms = analysis_data.get('forms', [])
        components = analysis_data.get('identified_components', [])
        
        module_list = "| 模块名称 | 所在页面 | 位置坐标 | 主要功能 | 数据来源 |\n|----------|----------|----------|----------|----------|\n"
        
        # 从按钮推断模块
        buttons = [e for e in interactive_elements if e.get('type') == 'button']
        for i, btn in enumerate(buttons[:10]):  # 限制数量
            btn_text = btn.get('text', f'按钮{i+1}')
            module_list += f"| {btn_text}模块 | 主页面 | 顶部工具栏 | {btn_text}操作 | 后端API |\n"
        
        # 从表单推断模块
        for i, form in enumerate(forms[:5]):  # 限制数量
            form_id = form.get('id', f'表单{i+1}')
            field_count = len(form.get('fields', []))
            module_list += f"| {form_id}管理 | 数据管理页 | 主内容区 | 数据录入和编辑 | 后端API + 数据库 |\n"
        
        # 从组件推断模块
        component_types = {}
        for comp in components:
            comp_type = comp.get('type', '')
            if comp_type:
                if comp_type not in component_types:
                    component_types[comp_type] = 0
                component_types[comp_type] += 1
        
        for comp_type, count in list(component_types.items())[:5]:  # 限制数量
            module_list += f"| {comp_type}组件 | 各相关页面 | 内容区域 | {comp_type}功能展示 | {'后端API' if comp_type in ['datatable', 'chart'] else '前端状态'} |\n"
        
        if not buttons and not forms and not component_types:
            module_list += "| 用户管理 | /users | 主内容区 | 用户信息管理 | 后端API |\n"
            module_list += "| 数据展示 | /dashboard | 主内容区 | 数据可视化展示 | 后端API |\n"
            module_list += "| 系统设置 | /settings | 侧边栏 | 系统参数配置 | 后端API + 数据库 |\n"
        
        return module_list
    
    def _generate_routing_plan(self, analysis_data: Dict[str, Any]) -> str:
        """生成页面路由规划"""
        return """```typescript
// src/routes/index.tsx
const routes = [
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: 'dashboard', element: <Dashboard /> },
      {
        path: 'users',
        children: [
          { index: true, element: <UserList /> },
          { path: ':id', element: <UserDetail /> },
          { path: ':id/edit', element: <UserEdit /> },
          { path: 'create', element: <UserCreate /> },
        ],
      },
      {
        path: 'data',
        children: [
          { path: 'list', element: <DataList /> },
          { path: 'detail/:id', element: <DataDetail /> },
        ],
      },
      {
        path: 'settings',
        children: [
          { path: 'general', element: <GeneralSettings /> },
          { path: 'security', element: <SecuritySettings /> },
          { path: 'logs', element: <SystemLogs /> },
        ],
      },
    ],
  },
  { path: '/login', element: <Login /> },
  { path: '/register', element: <Register /> },
  { path: '/forgot-password', element: <ForgotPassword /> },
  { path: '*', element: <NotFound /> },
];
```"""
    
    def _generate_component_list(self, analysis_data: Dict[str, Any]) -> str:
        """生成组件清单"""
        components = analysis_data.get('identified_components', [])
        
        if not components:
            return "#### 3.2.1 布局组件\n**组件名**: `MainLayout`\n- **位置**: 根组件\n- **Props**: `children`, `title`\n- **状态**: `collapsed`, `userInfo`\n- **交互逻辑**: 侧边栏折叠/展开，用户菜单\n\n#### 3.2.2 业务组件\n**组件名**: `DataTable`\n- **位置**: 数据列表页面\n- **Props**: `dataSource`, `columns`, `loading`\n- **状态**: `selectedRows`, `pagination`\n- **交互逻辑**: 排序、筛选、分页、行选择"
        
        component_list = ""
        
        # 按类型分组
        by_type = {}
        for comp in components:
            comp_type = comp.get('type', '其他')
            if comp_type not in by_type:
                by_type[comp_type] = []
            by_type[comp_type].append(comp)
        
        for comp_type, type_components in by_type.items():
            component_list += f"#### 3.2.{len(component_list.split('####'))} {comp_type}组件\n"
            
            for i, comp in enumerate(type_components[:3]):  # 每个类型最多3个
                comp_name = f"{comp_type.title()}{i+1}"
                element = comp.get('element', 'div')
                
                component_list += f"**组件名**: `{comp_name}`\n"
                component_list += f"- **元素类型**: {element}\n"
                
                comp_id = comp.get('id', '')
                if comp_id:
                    component_list += f"- **ID**: {comp_id}\n"
                
                comp_classes = comp.get('classes', [])
                if comp_classes:
                    component_list += f"- **类名**: {', '.join(comp_classes[:3])}\n"
                
                text_preview = comp.get('text_preview', '')
                if text_preview:
                    component_list += f"- **内容预览**: {text_preview}\n"
                
                component_list += f"- **Props**: `data`, `onChange`, `disabled`\n"
                component_list += f"- **状态**: `value`, `error`, `loading`\n"
                component_list += f"- **交互逻辑**: 用户输入处理，数据验证，状态反馈\n\n"
        
        return component_list
    
    def _generate_style_spec(self, analysis_data: Dict[str, Any]) -> str:
        """生成样式规范"""
        return """```css
/* 设计令牌 */
:root {
  /* 主色调 */
  --primary-color: #1890ff;
  --primary-hover: #40a9ff;
  --primary-active: #096dd9;
  
  /* 功能色 */
  --success-color: #52c41a;
  --warning-color: #faad14;
  --error-color: #f5222d;
  --info-color: #1890ff;
  
  /* 中性色 */
  --text-color: rgba(0, 0, 0, 0.85);
  --text-color-secondary: rgba(0, 0, 0, 0.45);
  --text-color-disabled: rgba(0, 0, 0, 0.25);
  --border-color: #d9d9d9;
  --border-color-split: #f0f0f0;
  --background-color: #f5f5f5;
  --background-color-light: #fafafa;
  --background-color-hover: rgba(0, 0, 0, 0.025);
  
  /* 尺寸 */
  --font-size-base: 14px;
  --font-size-lg: 16px;
  --font-size-sm: 12px;
  
  --border-radius-base: 6px;
  --border-radius-sm: 4px;
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 48px;
  
  /* 阴影 */
  --shadow-1: 0 1px 2px -2px rgba(0, 0, 0, 0.16);
  --shadow-2: 0 3px 6px -4px rgba(0, 0, 0, 0.12);
  --shadow-3: 0 6px 16px 0 rgba(0, 0, 0, 0.08);
  --shadow-4: 0 9px 28px 8px rgba(0, 0, 0, 0.05);
}

/* 响应式断点 */
@media (max-width: 576px) {
  :root { --container-padding: var(--spacing-sm); }
}

@media (min-width: 577px) and (max-width: 768px) {
  :root { --container-padding: var(--spacing-md); }
}

@media (min-width: 769px) and (max-width: 992px) {
  :root { --container-padding: var(--spacing-lg); }
}

@media (min-width: 993px) and (max-width: 1200px) {
  :root { --container-padding: var(--spacing-xl); }
}

@media (min-width: 1201px) {
  :root { --container-padding: var(--spacing-xxl); }
}
```"""
    
    def _generate_interaction_details(self, analysis_data: Dict[str, Any]) -> str:
        """生成交互细节"""
        interactive_elements = analysis_data.get('interactive_elements', [])
        
        if not interactive_elements:
            return "#### 按钮交互示例\n**按钮**: \"提交\"\n- **位置**: 表单底部\n- **样式**: 主按钮（蓝色背景）\n- **点击行为**: 验证表单，提交数据，显示结果\n- **成功反馈**: 显示成功提示，跳转页面\n- **失败反馈**: 显示错误信息，高亮错误字段"
        
        interaction_details = ""
        
        # 按钮交互
        buttons = [e for e in interactive_elements if e.get('type') == 'button']
        for i, btn in enumerate(buttons[:5]):  # 限制数量
            btn_text = btn.get('text', f'按钮{i+1}')
            
            interaction_details += f"#### 按钮交互示例{i+1}\n"
            interaction_details += f"**按钮**: \"{btn_text}\"\n"
            interaction_details += f"- **位置**: {btn.get('element_type', 'button')}元素"
            
            btn_id = btn.get('id', '')
            if btn_id:
                interaction_details += f"，ID: {btn_id}"
            
            btn_classes = btn.get('classes', [])
            if btn_classes:
                interaction_details += f"，类名: {', '.join(btn_classes[:3])}"
            
            interaction_details += "\n"
            interaction_details += f"- **样式**: {'主按钮' if 'primary' in str(btn_classes).lower() else '次按钮'}\n"
            
            onclick = btn.get('onclick', '')
            if onclick:
                interaction_details += f"- **点击行为**: {onclick[:100]}...\n"
            else:
                interaction_details += f"- **点击行为**: 触发{btn_text}操作，调用对应API\n"
            
            interaction_details += f"- **成功反馈**: 显示\"{btn_text}成功\"提示，更新界面状态\n"
            interaction_details += f"- **失败反馈**: 显示错误信息，保持当前状态\n\n"
        
        return interaction_details
    
    def _extract_ref_section(self, ref_content: Optional[str], section_title: str) -> Optional[str]:
        """从参考文件中提取指定章节的内容"""
        if not ref_content:
            return None
        lines = ref_content.split('\n')
        in_section = False
        section_lines = []
        depth = 0
        target_depth = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                # 计算标题层级
                level = len(stripped.split()[0])
                title_text = stripped.lstrip('#').strip()
                if title_text == section_title:
                    in_section = True
                    target_depth = level
                    continue
                if in_section and level <= target_depth:
                    break
            if in_section:
                section_lines.append(line)
        if section_lines:
            return '\n'.join(section_lines).rstrip()
        return None
    
    def _generate_api_design(self, analysis_data: Dict[str, Any]) -> str:
        """生成API接口设计章节"""
        output = []
        # 从api-design.md提取完整内容
        if self.ref_api_design:
            output.append("### API设计规范")
            output.append("")
            # 跳过第1行标题，直接输出内容
            lines = self.ref_api_design.split('\n')
            for line in lines:
                if line.startswith('# '):
                    continue
                output.append(line)
            output.append("")
            output.append("---")
            output.append("")
            output.append("### API接口示例（用户管理）")
            output.append("")
        # 从template-spec.md提取API接口示例
        if self.ref_template_spec:
            lines = self.ref_template_spec.split('\n')
            in_section = False
            for line in lines:
                if 'API接口设计' in line and line.startswith('#'):
                    in_section = True
                    continue
                if in_section:
                    if '服务层设计' in line and line.startswith('#'):
                        break
                    output.append(line)
        return '\n'.join(output).rstrip()
    
    def _generate_service_design(self, analysis_data: Dict[str, Any]) -> str:
        """生成服务层设计章节"""
        if self.ref_template_spec:
            lines = self.ref_template_spec.split('\n')
            output = []
            in_section = False
            for line in lines:
                if '服务层设计' in line and line.startswith('#'):
                    in_section = True
                    continue
                if in_section:
                    if '第三方服务集成' in line and line.startswith('#'):
                        break
                    output.append(line)
            if output:
                return '\n'.join(output).rstrip()
        return "参考 `references/template-spec.md` 中的服务层设计示例"
    
    def _generate_third_party_integration(self, analysis_data: Dict[str, Any]) -> str:
        """生成第三方服务集成章节"""
        if self.ref_template_spec:
            lines = self.ref_template_spec.split('\n')
            output = []
            in_section = False
            for line in lines:
                if '第三方服务集成' in line and line.startswith('#'):
                    in_section = True
                    continue
                if in_section:
                    if '数据库设计' in line and line.startswith('#'):
                        break
                    output.append(line)
            if output:
                return '\n'.join(output).rstrip()
        return "- **短信服务**: 用户验证码发送\n- **邮件服务**: 通知邮件发送\n- **文件存储**: 用户上传文件存储\n- **支付服务**: 在线支付功能（如需要）"
    
    def _generate_database_tables(self, analysis_data: Dict[str, Any]) -> str:
        """生成数据库表设计章节"""
        if self.ref_template_spec:
            lines = self.ref_template_spec.split('\n')
            output = []
            in_section = False
            for line in lines:
                if '数据库表清单' in line and line.startswith('#'):
                    in_section = True
                    continue
                if in_section:
                    if '实体关系图' in line and line.startswith('#'):
                        break
                    output.append(line)
            if output:
                return '\n'.join(output).rstrip()
        return "参考 `references/template-spec.md` 中的数据库表设计示例"
    
    def _generate_entity_relationship(self, analysis_data: Dict[str, Any]) -> str:
        """生成实体关系图章节"""
        if self.ref_template_spec:
            lines = self.ref_template_spec.split('\n')
            output = []
            in_section = False
            for line in lines:
                if '实体关系图' in line and line.startswith('#'):
                    in_section = True
                    continue
                if in_section:
                    if '部署与运维' in line and line.startswith('#'):
                        break
                    output.append(line)
            if output:
                return '\n'.join(output).rstrip()
        return "```mermaid\nerDiagram\n    USERS ||--o{ ORDERS : places\n    ORDERS ||--o{ ORDER_ITEMS : contains\n    PRODUCTS ||--o{ ORDER_ITEMS : includes\n```"
    
    def _generate_environment_config(self, analysis_data: Dict[str, Any]) -> str:
        """生成环境配置章节"""
        if self.ref_template_spec:
            lines = self.ref_template_spec.split('\n')
            output = []
            in_section = False
            for line in lines:
                if '环境配置' in line and line.startswith('#'):
                    in_section = True
                    continue
                if in_section:
                    if '监控指标' in line and line.startswith('#'):
                        break
                    output.append(line)
            if output:
                return '\n'.join(output).rstrip()
        return "参考 `references/template-spec.md` 中的Docker Compose配置示例"
    
    def _generate_monitoring_metrics(self, analysis_data: Dict[str, Any]) -> str:
        return "- API响应时间P95 < 500ms\n- 错误率 < 0.1%\n- 系统可用性 > 99.9%\n- 数据库连接池使用率 < 80%"
    
    def _generate_backup_strategy(self, analysis_data: Dict[str, Any]) -> str:
        return "- 数据库每日全量备份，保留30天\n- 增量备份每4小时一次\n- 备份文件加密存储，异地容灾"
    
    def _generate_unit_tests(self, analysis_data: Dict[str, Any]) -> str:
        return "- 工具函数单元测试\n- 组件渲染测试\n- 表单验证测试\n- 业务逻辑测试"
    
    def _generate_integration_tests(self, analysis_data: Dict[str, Any]) -> str:
        return "- API接口端到端测试\n- 用户流程集成测试\n- 数据库操作测试\n- 第三方服务集成测试"
    
    def _generate_performance_tests(self, analysis_data: Dict[str, Any]) -> str:
        return "- 并发用户压力测试\n- API响应时间测试\n- 数据库查询性能测试\n- 内存泄漏测试"
    
    def _generate_security_considerations(self, analysis_data: Dict[str, Any]) -> str:
        return "- 所有用户输入验证和过滤\n- SQL注入防护\n- XSS攻击防护\n- CSRF令牌验证\n- 密码加密存储\n- API速率限制"
    
    def _generate_performance_optimization(self, analysis_data: Dict[str, Any]) -> str:
        return "- 数据库查询优化（索引）\n- 缓存策略（Redis）\n- 代码分割和懒加载\n- 图片和资源优化\n- CDN加速"
    
    def _generate_maintainability(self, analysis_data: Dict[str, Any]) -> str:
        return "- 统一代码规范\n- 组件化和模块化\n- 完整文档\n- 自动化测试\n- 持续集成"
    
    def _assess_confidence(self, analysis_data: Dict[str, Any]) -> str:
        """评估置信度"""
        stats = analysis_data.get('statistics', {})
        total_elements = stats.get('total_elements', 0)
        
        if total_elements > 100:
            return "高（页面结构完整，元素丰富）"
        elif total_elements > 50:
            return "中（页面结构清晰，关键元素可识别）"
        else:
            return "低（页面内容较少，需要更多上下文）"
    
    def _get_review_suggestion(self, analysis_data: Dict[str, Any]) -> str:
        """获取复核建议"""
        forms = analysis_data.get('forms', [])
        
        if forms:
            return "需要与产品经理确认表单字段的业务逻辑和验证规则"
        else:
            return "建议与产品经理确认核心业务流程和用户交互细节"

def main():
    parser = argparse.ArgumentParser(description='生成技术规格文档')
    parser.add_argument('output_file', help='输出文件路径')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='输出格式')
    parser.add_argument('--template', help='自定义模板文件')
    parser.add_argument('--input-json', help='从JSON文件读取分析数据（替代stdin）')
    
    args = parser.parse_args()
    
    # 从JSON文件或标准输入读取分析数据
    import sys
    if args.input_json:
        try:
            with open(args.input_json, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"错误: 读取JSON文件失败: {e}", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        analysis_json = sys.stdin.read()
        try:
            analysis_data = json.loads(analysis_json)
        except json.JSONDecodeError:
            print("错误: 输入不是有效的JSON格式", file=sys.stderr)
            sys.exit(1)
    else:
        # 如果没有输入，使用示例数据
        print("警告: 未提供分析数据，使用示例数据", file=sys.stderr)
        analysis_data = {
            'url': 'https://example.com/prototype',
            'title': '用户管理系统原型',
            'statistics': {'total_elements': 150},
            'interactive_elements': [],
            'forms': [],
            'navigation': [],
            'identified_components': []
        }
    
    # 生成文档
    generator = SpecGenerator(args.template)
    document = generator.generate_from_analysis(analysis_data)
    
    # 输出到文件
    try:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(document)
        print(f"文档已生成: {args.output_file}")
    except Exception as e:
        print(f"写入文件失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()