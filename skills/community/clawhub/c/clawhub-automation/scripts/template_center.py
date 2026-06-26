"""
Template Center - 模板中心
提供预设的自动化流程模板
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from .workflow_engine import Workflow, WorkflowNode, NodeType


@dataclass
class WorkflowTemplate:
    """工作流模板"""
    id: str
    name: str
    description: str
    category: str          # 分类: personal, business, enterprise
    tags: List[str]
    platforms: List[str]   # 涉及平台
    nodes: List[Dict]      # 节点配置
    params: Dict[str, Any] = field(default_factory=dict)
    usage_count: int = 0
    rating: float = 5.0
    author: str = "system"
    is_official: bool = True
    is_public: bool = True


class TemplateCenter:
    """
    模板中心
    
    Features:
    - 预设模板管理
    - 模板分类与搜索
    - 模板复用与自定义
    """
    
    def __init__(self):
        """初始化模板中心"""
        self.templates: Dict[str, WorkflowTemplate] = {}
        self.user_templates: Dict[str, List[WorkflowTemplate]] = {}
        
        # 注册默认模板
        self._register_default_templates()
    
    def _register_default_templates(self):
        """注册默认模板"""
        # 个人场景模板
        self._register_personal_templates()
        # 小微企业场景模板
        self._register_business_templates()
        # 企业级场景模板
        self._register_enterprise_templates()
    
    def _register_personal_templates(self):
        """注册个人场景模板"""
        templates = [
            WorkflowTemplate(
                id="tpl_wechat_to_aliyun",
                name="微信文件自动同步到阿里云盘",
                description="微信收到文件后自动备份到阿里云盘，再也不怕文件过期",
                category="personal",
                tags=["文件同步", "微信", "阿里云盘", "备份"],
                platforms=["wechat", "aliyun_drive"],
                nodes=[
                    {
                        'name': '微信收到文件',
                        'type': 'trigger',
                        'platform': 'wechat',
                        'action': 'file_received'
                    },
                    {
                        'name': '同步到阿里云盘',
                        'type': 'action',
                        'platform': 'aliyun_drive',
                        'action': 'upload_file'
                    },
                    {
                        'name': '发送确认通知',
                        'type': 'action',
                        'platform': 'wechat',
                        'action': 'send_message',
                        'is_critical': False
                    }
                ]
            ),
            WorkflowTemplate(
                id="tpl_chat_backup",
                name="聊天记录自动整理备份",
                description="自动整理微信/钉钉聊天记录并保存到文档",
                category="personal",
                tags=["聊天记录", "整理", "备份", "文档"],
                platforms=["wechat", "tencent_doc"],
                nodes=[
                    {
                        'name': '定时触发',
                        'type': 'trigger',
                        'platform': 'system',
                        'action': 'schedule_trigger',
                        'params': {'schedule': '0 22 * * *'}
                    },
                    {
                        'name': '整理聊天记录',
                        'type': 'action',
                        'platform': 'wechat',
                        'action': 'organize_chats'
                    },
                    {
                        'name': '生成文档',
                        'type': 'action',
                        'platform': 'tencent_doc',
                        'action': 'create_document'
                    }
                ]
            ),
            WorkflowTemplate(
                id="tpl_expense_tracker",
                name="消费记录自动记账",
                description="自动识别微信/支付宝消费通知并记录到表格",
                category="personal",
                tags=["记账", "消费", "表格", "财务"],
                platforms=["wechat", "tencent_doc"],
                nodes=[
                    {
                        'name': '收到消费通知',
                        'type': 'trigger',
                        'platform': 'wechat',
                        'action': 'message_received'
                    },
                    {
                        'name': '识别金额',
                        'type': 'action',
                        'platform': 'system',
                        'action': 'extract_amount'
                    },
                    {
                        'name': '记录到表格',
                        'type': 'action',
                        'platform': 'tencent_doc',
                        'action': 'update_spreadsheet'
                    }
                ]
            ),
            WorkflowTemplate(
                id="tpl_daily_reminder",
                name="每日定时提醒",
                description="每天定时发送提醒通知（喝水、休息、日程等）",
                category="personal",
                tags=["提醒", "定时", "健康", "日程"],
                platforms=["wechat"],
                nodes=[
                    {
                        'name': '定时触发',
                        'type': 'trigger',
                        'platform': 'system',
                        'action': 'schedule_trigger',
                        'params': {'schedule': '0 9,14,18 * * *'}
                    },
                    {
                        'name': '发送提醒',
                        'type': 'action',
                        'platform': 'wechat',
                        'action': 'send_message'
                    }
                ]
            )
        ]
        
        for template in templates:
            self.templates[template.id] = template
    
    def _register_business_templates(self):
        """注册小微企业场景模板"""
        templates = [
            WorkflowTemplate(
                id="tpl_order_to_sheet",
                name="微信订单自动同步到腾讯文档",
                description="微信收到客户订单后自动录入到腾讯文档表格",
                category="business",
                tags=["订单", "同步", "腾讯文档", "销售"],
                platforms=["wechat", "tencent_doc"],
                nodes=[
                    {
                        'name': '收到订单消息',
                        'type': 'trigger',
                        'platform': 'wechat',
                        'action': 'message_received'
                    },
                    {
                        'name': '解析订单信息',
                        'type': 'action',
                        'platform': 'system',
                        'action': 'parse_order'
                    },
                    {
                        'name': '录入表格',
                        'type': 'action',
                        'platform': 'tencent_doc',
                        'action': 'update_spreadsheet'
                    },
                    {
                        'name': '发送确认',
                        'type': 'action',
                        'platform': 'wechat',
                        'action': 'send_message',
                        'is_critical': False
                    }
                ]
            ),
            WorkflowTemplate(
                id="tpl_approval_archive",
                name="钉钉审批自动归档",
                description="钉钉审批完成后自动归档到云盘并通知相关人员",
                category="business",
                tags=["审批", "钉钉", "归档", "通知"],
                platforms=["dingtalk", "aliyun_drive"],
                nodes=[
                    {
                        'name': '审批完成',
                        'type': 'trigger',
                        'platform': 'dingtalk',
                        'action': 'approval_completed'
                    },
                    {
                        'name': '导出审批单',
                        'type': 'action',
                        'platform': 'dingtalk',
                        'action': 'export_approval'
                    },
                    {
                        'name': '归档到云盘',
                        'type': 'action',
                        'platform': 'aliyun_drive',
                        'action': 'upload_file'
                    },
                    {
                        'name': '通知申请人',
                        'type': 'action',
                        'platform': 'dingtalk',
                        'action': 'send_work_notice',
                        'is_critical': False
                    }
                ]
            ),
            WorkflowTemplate(
                id="tpl_invoice_organize",
                name="发票自动整理",
                description="自动收集发票图片并整理到指定文件夹",
                category="business",
                tags=["发票", "财务", "整理", "归档"],
                platforms=["wechat", "aliyun_drive"],
                nodes=[
                    {
                        'name': '收到发票图片',
                        'type': 'trigger',
                        'platform': 'wechat',
                        'action': 'file_received'
                    },
                    {
                        'name': '识别发票信息',
                        'type': 'action',
                        'platform': 'system',
                        'action': 'recognize_invoice'
                    },
                    {
                        'name': '分类存储',
                        'type': 'action',
                        'platform': 'aliyun_drive',
                        'action': 'upload_file'
                    }
                ]
            ),
            WorkflowTemplate(
                id="tpl_employee_notify",
                name="员工通知自动推送",
                description="定时向员工推送通知、公告、日报提醒",
                category="business",
                tags=["通知", "员工", "定时", "公告"],
                platforms=["dingtalk"],
                nodes=[
                    {
                        'name': '定时触发',
                        'type': 'trigger',
                        'platform': 'system',
                        'action': 'schedule_trigger',
                        'params': {'schedule': '0 9 * * 1'}
                    },
                    {
                        'name': '发送群通知',
                        'type': 'action',
                        'platform': 'dingtalk',
                        'action': 'send_work_notice'
                    }
                ]
            )
        ]
        
        for template in templates:
            self.templates[template.id] = template
    
    def _register_enterprise_templates(self):
        """注册企业级场景模板"""
        templates = [
            WorkflowTemplate(
                id="tpl_cross_platform_sync",
                name="飞书任务同步到钉钉通知",
                description="飞书任务状态变更时自动通知钉钉群",
                category="enterprise",
                tags=["跨平台", "飞书", "钉钉", "任务同步"],
                platforms=["feishu", "dingtalk"],
                nodes=[
                    {
                        'name': '飞书任务更新',
                        'type': 'trigger',
                        'platform': 'feishu',
                        'action': 'task_updated'
                    },
                    {
                        'name': '同步到钉钉',
                        'type': 'action',
                        'platform': 'dingtalk',
                        'action': 'send_work_notice'
                    }
                ]
            ),
            WorkflowTemplate(
                id="tpl_data_summary",
                name="跨办公软件数据汇总",
                description="自动汇总各平台数据生成报表",
                category="enterprise",
                tags=["数据汇总", "报表", "跨平台", "自动化"],
                platforms=["feishu", "dingtalk", "tencent_doc"],
                nodes=[
                    {
                        'name': '定时触发',
                        'type': 'trigger',
                        'platform': 'system',
                        'action': 'schedule_trigger',
                        'params': {'schedule': '0 18 * * 5'}
                    },
                    {
                        'name': '收集飞书数据',
                        'type': 'action',
                        'platform': 'feishu',
                        'action': 'export_data'
                    },
                    {
                        'name': '收集钉钉数据',
                        'type': 'action',
                        'platform': 'dingtalk',
                        'action': 'export_data'
                    },
                    {
                        'name': '生成汇总报表',
                        'type': 'action',
                        'platform': 'tencent_doc',
                        'action': 'create_spreadsheet'
                    }
                ]
            ),
            WorkflowTemplate(
                id="tpl_onboarding",
                name="员工入职流程自动化",
                description="自动化处理新员工入职各项流程",
                category="enterprise",
                tags=["入职", "HR", "自动化", "流程"],
                platforms=["dingtalk", "feishu"],
                nodes=[
                    {
                        'name': '收到入职申请',
                        'type': 'trigger',
                        'platform': 'dingtalk',
                        'action': 'approval_completed'
                    },
                    {
                        'name': '创建账号',
                        'type': 'action',
                        'platform': 'feishu',
                        'action': 'create_user'
                    },
                    {
                        'name': '发送欢迎通知',
                        'type': 'action',
                        'platform': 'dingtalk',
                        'action': 'send_work_notice',
                        'is_critical': False
                    }
                ]
            )
        ]
        
        for template in templates:
            self.templates[template.id] = template
    
    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """获取模板"""
        return self.templates.get(template_id)
    
    def list_templates(
        self,
        category: str = None,
        platforms: List[str] = None,
        tags: List[str] = None
    ) -> List[WorkflowTemplate]:
        """
        列出模板
        
        Args:
            category: 分类筛选
            platforms: 平台筛选
            tags: 标签筛选
            
        Returns:
            List[WorkflowTemplate]: 模板列表
        """
        templates = list(self.templates.values())
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        if platforms:
            templates = [
                t for t in templates
                if any(p in t.platforms for p in platforms)
            ]
        
        if tags:
            templates = [
                t for t in templates
                if any(tag in t.tags for tag in tags)
            ]
        
        return templates
    
    def search_templates(self, keyword: str) -> List[WorkflowTemplate]:
        """
        搜索模板
        
        Args:
            keyword: 关键词
            
        Returns:
            List[WorkflowTemplate]: 匹配的模板
        """
        keyword = keyword.lower()
        results = []
        
        for template in self.templates.values():
            if (keyword in template.name.lower() or
                keyword in template.description.lower() or
                any(keyword in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return results
    
    def create_workflow_from_template(
        self,
        template_id: str,
        workflow_engine,
        custom_params: Dict = None
    ) -> Optional[Workflow]:
        """
        从模板创建工作流
        
        Args:
            template_id: 模板ID
            workflow_engine: 工作流引擎
            custom_params: 自定义参数
            
        Returns:
            Workflow or None
        """
        template = self.get_template(template_id)
        if not template:
            return None
        
        # 创建工作流
        workflow = workflow_engine.create_workflow(
            name=template.name,
            description=template.description
        )
        
        # 添加节点
        prev_node_id = None
        for node_config in template.nodes:
            node_id = workflow_engine.add_node(
                workflow_id=workflow.id,
                name=node_config['name'],
                node_type=NodeType[node_config['type'].upper()],
                platform=node_config['platform'],
                action=node_config['action'],
                params=node_config.get('params', {}),
                is_critical=node_config.get('is_critical', True)
            )
            
            # 连接节点
            if prev_node_id:
                workflow_engine.connect_nodes(workflow.id, prev_node_id, node_id)
            
            prev_node_id = node_id
        
        # 更新模板使用统计
        template.usage_count += 1
        
        return workflow
    
    def add_user_template(self, user_id: str, template: WorkflowTemplate):
        """
        添加用户自定义模板
        
        Args:
            user_id: 用户ID
            template: 模板
        """
        if user_id not in self.user_templates:
            self.user_templates[user_id] = []
        
        template.is_official = False
        self.user_templates[user_id].append(template)
    
    def get_user_templates(self, user_id: str) -> List[WorkflowTemplate]:
        """获取用户自定义模板"""
        return self.user_templates.get(user_id, [])
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(set(t.category for t in self.templates.values()))
    
    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        tags = set()
        for template in self.templates.values():
            tags.update(template.tags)
        return list(tags)