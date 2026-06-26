"""
业务流程分析模块
分析原型页面之间的业务关系，推断流程流转，生成交互式问题
"""

from typing import List, Dict, Optional
from .models import (
    PageView, MenuItem, ActionButton, FilterField, TableColumn,
    PageAnalysis, OperationAnalysis, FlowHypothesis, StatusTransition,
    AnalysisQuestion, InteractiveAnalysis
)


class BusinessFlowAnalyzer:
    """业务流程分析器 - 从HTML原型推断业务逻辑"""

    def __init__(self, menus: List[MenuItem], page_views: List[PageView]):
        self.menus = menus
        self.page_views = page_views

    def analyze(self) -> InteractiveAnalysis:
        """执行完整分析，返回交互式分析结果"""
        # 1. 分析每个页面
        page_analyses = [self._analyze_page(pv) for pv in self.page_views]

        # 2. 推断流程顺序
        flow_hypothesis = self._infer_flow_sequence(page_analyses)

        # 3. 推断状态流转
        status_transitions = self._infer_status_transitions(page_analyses)

        # 4. 生成问题
        questions = self._generate_questions(page_analyses, flow_hypothesis, status_transitions)

        # 5. 生成分析总结
        summary = self._generate_summary(page_analyses, flow_hypothesis)

        return InteractiveAnalysis(
            system_name="",  # 由调用者填充
            page_analyses=page_analyses,
            flow_hypothesis=flow_hypothesis,
            status_transitions=status_transitions,
            questions=questions,
            analysis_summary=summary
        )

    def _analyze_page(self, pv: PageView) -> PageAnalysis:
        """分析单个页面的业务角色和操作"""
        # 推断页面角色
        role = self._infer_page_role(pv)

        # 分析操作
        operations = self._analyze_operations(pv)

        # 提取关键字段
        key_fields = self._extract_key_fields(pv)

        # 提取状态字段
        status_fields = [f for f in key_fields if '状态' in f or 'status' in f.lower()]

        # 提取筛选维度
        filter_dimensions = [f.name for f in pv.filters]

        # 检查是否有勾选列
        has_checkbox = any(t.has_checkbox for t in pv.tables)

        return PageAnalysis(
            page_name=pv.name,
            view_id=pv.view_id,
            inferred_role=role,
            operations=operations,
            key_fields=key_fields,
            status_fields=status_fields,
            filter_dimensions=filter_dimensions,
            has_checkbox=has_checkbox  # 这里是 PageAnalysis 的属性，不是 PageView 的
        )

    def _infer_page_role(self, pv: PageView) -> str:
        """推断页面角色"""
        # 有大量筛选条件和表格 → 数据查看/处理页面
        if pv.filters and pv.tables:
            # 有创建类按钮 → 处理页面
            create_ops = [b for b in pv.buttons if b.category == 'create']
            if create_ops:
                return '处理页面'
            return '查看页面'

        # 有统计卡片 → 仪表盘/入口页面
        if pv.stat_cards:
            return '入口页面'

        # 有弹窗面板 → 详情/处理页面
        if pv.drawer_panels:
            return '详情页面'

        # 有按钮但无表格 → 操作页面
        if pv.buttons and not pv.tables:
            return '操作页面'

        # 默认
        return '查看页面'

    def _analyze_operations(self, pv: PageView) -> List[OperationAnalysis]:
        """分析页面中的操作"""
        operations = []

        # 从tables中获取has_checkbox
        has_checkbox = any(t.has_checkbox for t in pv.tables)

        for btn in pv.buttons:
            # 跳过基础操作和无效按钮
            if btn.name in ['搜索', '查询', '重置', '清空']:
                continue
            # 跳过无意义的按钮（如纯图标按钮、下拉箭头等）
            if not btn.name or len(btn.name) <= 1 or btn.name in ['▼', '▲', '◀', '▶', '...', '···']:
                continue

            # 推断是否需要勾选
            requires_selection = has_checkbox and btn.location == 'toolbar'

            # 推断可能的执行状态
            possible_states = self._infer_possible_states(btn)

            # 生成描述
            description = self._generate_operation_description(btn)

            operations.append(OperationAnalysis(
                name=btn.name,
                category=btn.category,
                requires_selection=requires_selection,
                possible_states=possible_states,
                description=description
            ))

        return operations

    def _infer_possible_states(self, btn: ActionButton) -> List[str]:
        """推断操作可能的执行状态（基于通用模式，不硬编码）"""
        states = []

        # 根据按钮类别推断
        if btn.category == 'create':
            states.append('任意状态（新建）')
        elif btn.category == 'delete':
            states.append('待处理')
            states.append('可删除状态')
        elif btn.category == 'confirm':
            states.append('待确认')
            states.append('待审核')
        elif btn.category == 'edit':
            states.append('可编辑状态')
        elif btn.category == 'export':
            states.append('任意状态（导出）')

        return states if states else ['待定（需确认）']

    def _generate_operation_description(self, btn: ActionButton) -> str:
        """生成功能描述"""
        category_descriptions = {
            'create': '创建新记录',
            'edit': '编辑现有记录',
            'delete': '删除记录',
            'confirm': '确认/审核操作',
            'export': '导出数据',
            'view': '查看详情',
            'search': '搜索筛选',
            'reset': '重置条件',
        }
        return category_descriptions.get(btn.category, f'执行{btn.name}操作')

    def _extract_key_fields(self, pv: PageView) -> List[str]:
        """提取关键字段"""
        fields = []

        # 从表格列提取
        for table in pv.tables:
            for col in table.columns:
                if col.name and col.name not in ['', '操作', '选择', '全选']:
                    fields.append(col.name)

        return fields

    def _infer_flow_sequence(self, page_analyses: List[PageAnalysis]) -> FlowHypothesis:
        """推断页面流转顺序"""
        if not page_analyses:
            return FlowHypothesis(sequence=[], confidence=0, evidence=[])

        evidence = []

        # 依据1：菜单顺序（最直接的线索）
        menu_order = [pa.page_name for pa in page_analyses if pa.page_name]
        if menu_order:
            evidence.append(f"依据1：菜单排列顺序为 {' → '.join(menu_order[:6])}{'...' if len(menu_order) > 6 else ''}")

        # 依据2：页面角色推断
        entry_pages = [pa.page_name for pa in page_analyses if pa.inferred_role == '入口页面']
        process_pages = [pa.page_name for pa in page_analyses if pa.inferred_role == '处理页面']
        view_pages = [pa.page_name for pa in page_analyses if pa.inferred_role == '查看页面']

        if entry_pages:
            evidence.append(f"依据2：入口页面（有统计卡片）→ {', '.join(entry_pages[:3])}")
        if process_pages:
            evidence.append(f"依据3：处理页面（有创建操作）→ {', '.join(process_pages[:3])}")

        # 依据3：操作关联分析
        create_operations = []
        for pa in page_analyses:
            for op in pa.operations:
                if op.category == 'create':
                    create_operations.append(f"{pa.page_name}的'{op.name}'")

        if create_operations:
            evidence.append(f"依据4：创建类操作 → {', '.join(create_operations[:3])}，可能生成下游记录")

        # 依据4：字段关联分析
        field_connections = self._find_field_connections(page_analyses)
        if field_connections:
            evidence.append(f"依据5：字段关联 → {', '.join(field_connections[:2])}")

        # 计算置信度
        confidence = 0.5  # 基础置信度
        if len(evidence) >= 3:
            confidence += 0.2
        if field_connections:
            confidence += 0.1
        confidence = min(confidence, 0.9)

        return FlowHypothesis(
            sequence=menu_order,
            confidence=confidence,
            evidence=evidence
        )

    def _find_field_connections(self, page_analyses: List[PageAnalysis]) -> List[str]:
        """查找页面之间的字段关联"""
        connections = []

        for i, pa_a in enumerate(page_analyses):
            for j, pa_b in enumerate(page_analyses):
                if i >= j:
                    continue

                # 检查是否有共同字段名
                common_fields = set(pa_a.key_fields) & set(pa_b.key_fields)
                # 排除通用字段
                common_fields -= {'操作', '状态', '时间', '创建时间', '更新时间'}

                if common_fields:
                    connections.append(
                        f"'{pa_a.page_name}' 和 '{pa_b.page_name}' 共享字段：{', '.join(list(common_fields)[:3])}"
                    )

        return connections[:3]  # 最多返回3个

    def _infer_status_transitions(self, page_analyses: List[PageAnalysis]) -> List[StatusTransition]:
        """推断状态流转"""
        transitions = []

        for pa in page_analyses:
            # 从操作推断状态值
            possible_values = []
            transition_rules = []
            evidence = []

            # 根据操作推断状态
            for op in pa.operations:
                if op.category == 'create':
                    possible_values.append('待处理')
                    transition_rules.append('新建 → 待处理')
                elif op.category == 'confirm':
                    possible_values.append('待确认')
                    possible_values.append('已确认')
                    transition_rules.append('待确认 → 已确认')
                elif op.category == 'delete':
                    possible_values.append('已作废')
                    transition_rules.append('任意状态 → 已作废')

            # 从状态Tab提取状态值
            status_tabs = []
            for pv in self.page_views:
                if pv.view_id == pa.view_id:  # 使用view_id匹配更准确
                    status_tabs = pv.status_tabs
                    for tab in pv.status_tabs:
                        if tab.name and tab.name not in possible_values:
                            possible_values.append(tab.name)
                    break

            # 只有有状态值时才添加
            if possible_values:
                # 根据操作生成证据
                op_names = [op.name for op in pa.operations if op.category in ['create', 'confirm', 'delete']]
                if op_names:
                    evidence.append(f"从按钮操作推断：{', '.join(op_names[:3])}")

                if status_tabs:
                    evidence.append(f"从状态筛选Tab推断：{', '.join([t.name for t in status_tabs[:5]])}")

                transitions.append(StatusTransition(
                    page_name=pa.page_name,
                    status_field='状态',
                    possible_values=possible_values,
                    transitions=transition_rules,
                    evidence=evidence
                ))

        return transitions

    def _generate_questions(self, page_analyses: List[PageAnalysis],
                           flow: FlowHypothesis,
                           transitions: List[StatusTransition]) -> List[AnalysisQuestion]:
        """生成需要用户确认的问题"""
        questions = []

        # 问题1：流程顺序确认
        if flow.sequence:
            questions.append(AnalysisQuestion(
                category='flow',
                priority='high',
                question=f"推测的业务流程顺序为：\n{' → '.join(flow.sequence[:8])}{'...' if len(flow.sequence) > 8 else ''}\n\n这个顺序是否正确？",
                context='\n'.join(flow.evidence[:3]),
                options=["顺序正确", "需要调整顺序", "有并行关系", "缺少页面"]
            ))

        # 问题2：页面角色确认
        entry_pages = [pa.page_name for pa in page_analyses if pa.inferred_role == '入口页面']
        process_pages = [pa.page_name for pa in page_analyses if pa.inferred_role == '处理页面']

        if entry_pages or process_pages:
            role_summary = []
            if entry_pages:
                role_summary.append(f"入口页面：{', '.join(entry_pages[:3])}")
            if process_pages:
                role_summary.append(f"处理页面：{', '.join(process_pages[:3])}")

            questions.append(AnalysisQuestion(
                category='flow',
                priority='high',
                question=f"页面角色推断：\n{chr(10).join(role_summary)}\n\n是否正确？",
                context="基于统计卡片、操作按钮等元素推断",
                options=["正确", "需要调整"]
            ))

        # 问题3：状态流转确认
        for trans in transitions[:3]:  # 最多问3个
            if trans.possible_values:
                questions.append(AnalysisQuestion(
                    category='status',
                    priority='high',
                    question=f"【{trans.page_name}】的状态字段「{trans.status_field}」有哪些可选值？",
                    context=f"推测的状态值：{', '.join(trans.possible_values[:5])}",
                    options=trans.possible_values[:5] + ["需要补充"]
                ))

        # 问题4：操作条件确认
        for pa in page_analyses:
            for op in pa.operations:
                if op.category in ['confirm', 'delete'] and op.requires_selection:
                    questions.append(AnalysisQuestion(
                        category='permission',
                        priority='medium',
                        question=f"【{pa.page_name}】的「{op.name}」操作需要什么条件？",
                        context=f"当前推测：{', '.join(op.possible_states)}",
                        options=["需要特定状态", "需要权限", "需要勾选记录", "无限制"]
                    ))

        # 问题5：批量操作确认
        batch_pages = [pa for pa in page_analyses if pa.has_checkbox]
        if batch_pages:
            questions.append(AnalysisQuestion(
                category='operation',
                priority='medium',
                question=f"以下页面支持批量操作（有勾选列）：\n{', '.join([pa.page_name for pa in batch_pages[:3]])}\n\n批量操作有什么限制？",
                context="检测到表格有勾选列",
                options=["无限制", "有数量限制", "需要相同状态", "需要权限"]
            ))

        # 问题6：关键字段确认
        for pa in page_analyses[:3]:
            if pa.key_fields:
                questions.append(AnalysisQuestion(
                    category='field',
                    priority='low',
                    question=f"【{pa.page_name}】的关键字段有哪些需要特别处理？",
                    context=f"检测到字段：{', '.join(pa.key_fields[:5])}{'...' if len(pa.key_fields) > 5 else ''}",
                    options=[]
                ))

        return questions

    def _generate_summary(self, page_analyses: List[PageAnalysis],
                         flow: FlowHypothesis) -> str:
        """生成分析总结"""
        lines = []

        # 统计信息
        total_pages = len(page_analyses)
        total_operations = sum(len(pa.operations) for pa in page_analyses)
        total_fields = sum(len(pa.key_fields) for pa in page_analyses)

        lines.append(f"共分析 {total_pages} 个页面，发现 {total_operations} 个业务操作，{total_fields} 个关键字段。")
        lines.append("")

        # 页面角色分布
        role_counts = {}
        for pa in page_analyses:
            role_counts[pa.inferred_role] = role_counts.get(pa.inferred_role, 0) + 1

        lines.append("页面角色分布：")
        for role, count in role_counts.items():
            lines.append(f"  - {role}：{count}个")

        # 流程推断置信度
        lines.append("")
        lines.append(f"流程推断置信度：{flow.confidence:.0%}")

        if flow.evidence:
            lines.append("")
            lines.append("主要推断依据：")
            for ev in flow.evidence[:3]:
                lines.append(f"  - {ev}")

        return '\n'.join(lines)
