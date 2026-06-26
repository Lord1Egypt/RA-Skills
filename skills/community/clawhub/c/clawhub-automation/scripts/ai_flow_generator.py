"""
AI Flow Generator - AI流程智能生成器
根据自然语言指令自动生成自动化流程
"""

import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .workflow_engine import Workflow, WorkflowNode, NodeType


@dataclass
class IntentParseResult:
    """意图解析结果"""
    intent: str
    trigger: Dict[str, Any]
    actions: List[Dict[str, Any]]
    conditions: List[Dict[str, Any]]
    confidence: float


class AIFlowGenerator:
    """
    AI流程智能生成器
    
    Features:
    - 自然语言指令识别
    - 自动流程生成
    - 流程优化建议
    - 中文语义理解
    """
    
    def __init__(self):
        """初始化AI生成器"""
        self.platform_keywords = {
            '微信': 'wechat',
            'wechat': 'wechat',
            '钉钉': 'dingtalk',
            'dingtalk': 'dingtalk',
            '飞书': 'feishu',
            'feishu': 'feishu',
            'lark': 'feishu',
            'WPS': 'wps',
            'wps': 'wps',
            '腾讯文档': 'tencent_doc',
            'tencent_doc': 'tencent_doc',
            '阿里云盘': 'aliyun_drive',
            'aliyun': 'aliyun_drive',
            '云盘': 'aliyun_drive'
        }
        
        self.action_keywords = {
            '发送': 'send_message',
            '发': 'send_message',
            '同步': 'sync_file',
            '上传': 'upload_file',
            '下载': 'download_file',
            '创建': 'create_document',
            '生成': 'create_document',
            '通知': 'send_notification',
            '提醒': 'send_notification',
            '收到': 'receive_message',
            '接收': 'receive_message',
            '整理': 'organize',
            '备份': 'backup',
            '转存': 'sync_file'
        }
        
        self.trigger_keywords = {
            '收到': 'message_received',
            '接收': 'message_received',
            '当': 'trigger',
            '每当': 'trigger',
            '自动': 'auto_trigger',
            '定时': 'schedule_trigger',
            '每天': 'schedule_trigger',
            '每周': 'schedule_trigger'
        }
    
    def generate(self, instruction: str, workflow_name: str = None) -> Workflow:
        """
        根据自然语言指令生成流程
        
        Args:
            instruction: 自然语言指令
            workflow_name: 流程名称（可选）
            
        Returns:
            Workflow: 生成的工作流
        """
        # 解析意图
        intent = self._parse_intent(instruction)
        
        # 生成流程名称
        if not workflow_name:
            workflow_name = self._generate_name(instruction)
        
        # 创建工作流
        from .workflow_engine import WorkflowEngine
        engine = WorkflowEngine()
        workflow = engine.create_workflow(
            name=workflow_name,
            description=instruction
        )
        
        # 添加触发节点
        if intent.trigger:
            trigger_node_id = engine.add_node(
                workflow_id=workflow.id,
                name="触发条件",
                node_type=NodeType.TRIGGER,
                platform=intent.trigger.get('platform', 'system'),
                action=intent.trigger.get('action', 'trigger'),
                params=intent.trigger.get('params', {})
            )
        
        # 添加动作节点
        prev_node_id = trigger_node_id if intent.trigger else None
        
        for i, action in enumerate(intent.actions):
            node_name = action.get('name', f"操作{i+1}")
            node_id = engine.add_node(
                workflow_id=workflow.id,
                name=node_name,
                node_type=NodeType.ACTION,
                platform=action.get('platform', 'system'),
                action=action.get('action', 'action'),
                params=action.get('params', {}),
                is_critical=action.get('is_critical', True)
            )
            
            # 连接节点
            if prev_node_id:
                engine.connect_nodes(workflow.id, prev_node_id, node_id)
            
            prev_node_id = node_id
        
        # 添加分支条件（如果有）
        for condition in intent.conditions:
            condition_node_id = engine.add_node(
                workflow_id=workflow.id,
                name=condition.get('name', '条件判断'),
                node_type=NodeType.CONDITION,
                platform='system',
                action='condition',
                condition=condition.get('expression', '')
            )
            
            if prev_node_id:
                engine.connect_nodes(workflow.id, prev_node_id, condition_node_id)
        
        # 更新引擎中的工作流
        engine.workflows[workflow.id] = workflow
        
        return workflow
    
    def _parse_intent(self, instruction: str) -> IntentParseResult:
        """
        解析用户意图
        
        Args:
            instruction: 自然语言指令
            
        Returns:
            IntentParseResult: 解析结果
        """
        instruction = instruction.lower()
        
        # 识别平台
        platforms = self._extract_platforms(instruction)
        
        # 识别触发条件
        trigger = self._extract_trigger(instruction, platforms)
        
        # 识别动作
        actions = self._extract_actions(instruction, platforms)
        
        # 识别条件
        conditions = self._extract_conditions(instruction)
        
        # 计算置信度
        confidence = self._calculate_confidence(trigger, actions)
        
        return IntentParseResult(
            intent=instruction,
            trigger=trigger,
            actions=actions,
            conditions=conditions,
            confidence=confidence
        )
    
    def _extract_platforms(self, instruction: str) -> List[str]:
        """提取涉及的平台"""
        platforms = []
        for keyword, platform in self.platform_keywords.items():
            if keyword in instruction:
                if platform not in platforms:
                    platforms.append(platform)
        return platforms
    
    def _extract_trigger(self, instruction: str, platforms: List[str]) -> Optional[Dict]:
        """提取触发条件"""
        # 检测触发关键词
        for keyword, trigger_type in self.trigger_keywords.items():
            if keyword in instruction:
                # 文件相关触发
                if '文件' in instruction or '文档' in instruction:
                    return {
                        'platform': platforms[0] if platforms else 'system',
                        'action': 'file_received',
                        'params': {
                            'file_types': ['*'],
                            'path': '/incoming'
                        }
                    }
                
                # 消息相关触发
                if '消息' in instruction or '消息' in instruction:
                    return {
                        'platform': platforms[0] if platforms else 'system',
                        'action': 'message_received',
                        'params': {
                            'message_types': ['text', 'file']
                        }
                    }
                
                # 定时触发
                if '定时' in instruction or '每天' in instruction or '每周' in instruction:
                    schedule = '0 9 * * *'  # 默认每天9点
                    if '每天' in instruction:
                        schedule = '0 9 * * *'
                    elif '每周' in instruction:
                        schedule = '0 9 * * 1'
                    
                    return {
                        'platform': 'system',
                        'action': 'schedule_trigger',
                        'params': {
                            'schedule': schedule
                        }
                    }
        
        # 默认触发
        return {
            'platform': platforms[0] if platforms else 'system',
            'action': 'manual_trigger',
            'params': {}
        }
    
    def _extract_actions(self, instruction: str, platforms: List[str]) -> List[Dict]:
        """提取操作动作"""
        actions = []
        
        # 同步/转存操作
        if any(kw in instruction for kw in ['同步', '转存', '上传', '备份']):
            if len(platforms) >= 2:
                actions.append({
                    'name': f"同步文件到{platforms[1]}",
                    'platform': platforms[1],
                    'action': 'sync_file',
                    'params': {
                        'from_platform': platforms[0],
                        'to_platform': platforms[1]
                    },
                    'is_critical': True
                })
        
        # 发送通知
        if any(kw in instruction for kw in ['通知', '提醒', '发送']):
            target_platform = platforms[-1] if platforms else 'system'
            actions.append({
                'name': f"发送通知到{target_platform}",
                'platform': target_platform,
                'action': 'send_notification',
                'params': {
                    'title': '自动化流程执行通知',
                    'body': '流程已完成执行'
                },
                'is_critical': False
            })
        
        # 创建文档
        if any(kw in instruction for kw in ['创建', '生成', '整理']):
            doc_platform = None
            for p in platforms:
                if p in ['wps', 'tencent_doc', 'feishu']:
                    doc_platform = p
                    break
            
            if doc_platform:
                actions.append({
                    'name': f"创建{doc_platform}文档",
                    'platform': doc_platform,
                    'action': 'create_document',
                    'params': {
                        'title': '自动生成的文档',
                        'template': 'blank'
                    },
                    'is_critical': False
                })
        
        # 如果没有识别到具体动作，添加一个通用动作
        if not actions:
            actions.append({
                'name': '执行操作',
                'platform': platforms[0] if platforms else 'system',
                'action': 'execute',
                'params': {},
                'is_critical': True
            })
        
        return actions
    
    def _extract_conditions(self, instruction: str) -> List[Dict]:
        """提取分支条件"""
        conditions = []
        
        # 如果/那么条件
        if '如果' in instruction and '那么' in instruction:
            conditions.append({
                'name': '条件判断',
                'expression': 'condition_check',
                'params': {}
            })
        
        return conditions
    
    def _calculate_confidence(self, trigger: Dict, actions: List[Dict]) -> float:
        """计算生成置信度"""
        confidence = 0.5  # 基础置信度
        
        if trigger:
            confidence += 0.2
        
        if actions:
            confidence += 0.2
        
        if len(actions) >= 2:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _generate_name(self, instruction: str) -> str:
        """生成流程名称"""
        # 提取前10个字符作为名称
        name = instruction[:15] if len(instruction) <= 15 else instruction[:15] + "..."
        return f"AI生成: {name}"
    
    def suggest_optimization(self, workflow: Workflow) -> List[Dict]:
        """
        提供流程优化建议
        
        Args:
            workflow: 工作流
            
        Returns:
            List[Dict]: 优化建议列表
        """
        suggestions = []
        
        nodes = list(workflow.nodes.values())
        
        # 检查是否有冗余节点
        platforms_used = set()
        for node in nodes:
            if node.platform in platforms_used and node.node_type == NodeType.ACTION:
                suggestions.append({
                    'type': 'redundancy',
                    'message': f"节点 '{node.name}' 可能与前面的同平台操作重复，建议合并",
                    'node_id': node.id
                })
            platforms_used.add(node.platform)
        
        # 检查节点顺序
        trigger_nodes = [n for n in nodes if n.node_type == NodeType.TRIGGER]
        if len(trigger_nodes) > 1:
            suggestions.append({
                'type': 'order',
                'message': '检测到多个触发条件，建议只保留一个触发节点'
            })
        
        # 检查是否有缺少错误处理的节点
        for node in nodes:
            if node.is_critical and node.node_type == NodeType.ACTION:
                suggestions.append({
                    'type': 'error_handling',
                    'message': f"核心节点 '{node.name}' 建议添加错误处理或降级策略",
                    'node_id': node.id
                })
        
        return suggestions
    
    def validate_instruction(self, instruction: str) -> Dict[str, Any]:
        """
        验证指令是否清晰
        
        Args:
            instruction: 自然语言指令
            
        Returns:
            Dict: 验证结果
        """
        result = {
            'valid': True,
            'missing_info': [],
            'suggestions': []
        }
        
        # 检查是否包含平台信息
        platforms = self._extract_platforms(instruction)
        if len(platforms) < 2:
            result['valid'] = False
            result['missing_info'].append('缺少目标平台信息（需要至少两个平台）')
            result['suggestions'].append('请说明文件要从哪个平台同步到哪个平台')
        
        # 检查是否包含动作
        has_action = False
        for keyword in self.action_keywords.keys():
            if keyword in instruction:
                has_action = True
                break
        
        if not has_action:
            result['valid'] = False
            result['missing_info'].append('缺少具体操作描述')
            result['suggestions'].append('请说明要执行什么操作（如：同步、发送、创建等）')
        
        # 检查是否包含触发条件
        has_trigger = False
        for keyword in self.trigger_keywords.keys():
            if keyword in instruction:
                has_trigger = True
                break
        
        if not has_trigger:
            result['suggestions'].append('建议添加触发条件（如：当收到文件时、每天定时等）')
        
        return result