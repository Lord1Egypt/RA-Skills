#!/usr/bin/env python3
"""
ADK/Agent Runtime 集成模块
将ADK架构和女娲Agent能力融入全栈架构导师系统
支持接入多种AI平台
"""

import os
import json
import logging
from datetime import datetime

# 导入平台管理器
try:
    from .platform_adapters import PlatformManager
except ImportError:
    # 如果在单独运行时无法导入
    PlatformManager = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentStateMachine:
    """电子宠物状态机"""
    
    STATES = ['sleep', 'listen', 'think', 'ready', 'speak', 'error']
    TRANSITIONS = {
        'sleep': ['listen'],
        'listen': ['think'],
        'think': ['ready', 'error'],
        'ready': ['speak', 'listen'],
        'speak': ['listen', 'sleep'],
        'error': ['listen']
    }
    
    def __init__(self):
        self.current_state = 'sleep'
        self.history = []
    
    def transition(self, new_state):
        """状态转换"""
        if new_state in self.TRANSITIONS.get(self.current_state, []):
            self.history.append({
                'from': self.current_state,
                'to': new_state,
                'timestamp': datetime.now().isoformat()
            })
            self.current_state = new_state
            logger.info(f"状态转换: {self.history[-1]}")
            return True
        else:
            logger.warning(f"无效状态转换: {self.current_state} -> {new_state}")
            return False
    
    def get_state(self):
        """获取当前状态"""
        return {
            'current_state': self.current_state,
            'history': self.history[-5:]
        }

class PersonalityDistiller:
    """女娲风格的人物性格蒸馏器"""
    
    def __init__(self):
        self.personalities = {}
        self.load_personalities()
    
    def load_personalities(self):
        """加载已蒸馏的人物性格"""
        personalities_path = os.path.join(os.path.dirname(__file__), 'personalities.json')
        if os.path.exists(personalities_path):
            try:
                with open(personalities_path, 'r', encoding='utf-8') as f:
                    self.personalities = json.load(f)
                logger.info(f"加载了 {len(self.personalities)} 个人物性格")
            except Exception as e:
                logger.error(f"加载人物性格失败: {str(e)}")
    
    def distill_personality(self, name, materials):
        """蒸馏人物性格
        
        Args:
            name: 人物名称
            materials: 素材（著作、演讲、访谈、决策记录等）
            
        Returns:
            personality: 蒸馏出的人物性格
        """
        personality = {
            'name': name,
            'created_at': datetime.now().isoformat(),
            'expression_dna': self._extract_expression_dna(materials),
            'decision_framework': self._extract_decision_framework(materials),
            'value_orientation': self._extract_value_orientation(materials),
            'style_preferences': self._extract_style_preferences(materials)
        }
        
        self.personalities[name] = personality
        self._save_personalities()
        logger.info(f"成功蒸馏人物性格: {name}")
        return personality
    
    def _extract_expression_dna(self, materials):
        """提取表达DNA"""
        return {
            'tone': '专业严谨',
            'rhythm': '清晰有条理',
            'wording_preference': ['技术术语', '逻辑分析', '数据驱动'],
            'communication_style': '结构化表达'
        }
    
    def _extract_decision_framework(self, materials):
        """提取决策框架"""
        return {
            'analysis_method': '系统化分析',
            'decision_criteria': ['可行性', '效益', '风险', '可扩展性'],
            'prioritization_strategy': '价值驱动'
        }
    
    def _extract_value_orientation(self, materials):
        """提取价值取向"""
        return {
            'core_values': ['创新', '质量', '效率', '用户体验'],
            'principles': ['简洁至上', '持续改进', '数据驱动']
        }
    
    def _extract_style_preferences(self, materials):
        """提取风格偏好"""
        return {
            'response_length': '中等',
            'formality': '正式',
            'use_of_examples': True,
            'visual_aid_preference': '流程图、架构图'
        }
    
    def _save_personalities(self):
        """保存人物性格"""
        personalities_path = os.path.join(os.path.dirname(__file__), 'personalities.json')
        try:
            with open(personalities_path, 'w', encoding='utf-8') as f:
                json.dump(self.personalities, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存人物性格失败: {str(e)}")
    
    def get_personality(self, name):
        """获取人物性格"""
        return self.personalities.get(name, None)
    
    def list_personalities(self):
        """列出所有人物性格"""
        return list(self.personalities.keys())

class OrchestratorAgent:
    """ADK Orchestrator Agent - 协调多个子Agent"""
    
    def __init__(self):
        self.agents = {}
        self.state_machine = AgentStateMachine()
        self.personality_distiller = PersonalityDistiller()
    
    def register_agent(self, agent_name, agent):
        """注册子Agent"""
        self.agents[agent_name] = agent
        logger.info(f"注册Agent: {agent_name}")
    
    def unregister_agent(self, agent_name):
        """注销子Agent"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            logger.info(f"注销Agent: {agent_name}")
    
    def list_agents(self):
        """列出所有注册的Agent"""
        return list(self.agents.keys())
    
    def orchestrate(self, task, context=None):
        """协调执行任务"""
        self.state_machine.transition('listen')
        
        # 分析任务
        self.state_machine.transition('think')
        
        try:
            # 根据任务类型选择合适的Agent
            result = self._dispatch_task(task, context)
            self.state_machine.transition('ready')
            
            # 生成响应
            response = self._generate_response(result, context)
            self.state_machine.transition('speak')
            
            return response
        except Exception as e:
            self.state_machine.transition('error')
            logger.error(f"任务执行失败: {str(e)}")
            return f"执行失败: {str(e)}"
    
    def _dispatch_task(self, task, context):
        """任务分发"""
        task_type = self._classify_task(task)
        
        if task_type == 'code_generation':
            return self._handle_code_generation(task, context)
        elif task_type == 'prd_generation':
            return self._handle_prd_generation(task, context)
        elif task_type == 'tech_recommendation':
            return self._handle_tech_recommendation(task, context)
        elif task_type == 'knowledge_query':
            return self._handle_knowledge_query(task, context)
        else:
            return self._handle_default(task, context)
    
    def _classify_task(self, task):
        """任务分类"""
        task_lower = task.lower()
        if any(keyword in task_lower for keyword in ['代码', '编程', 'function', 'code']):
            return 'code_generation'
        elif any(keyword in task_lower for keyword in ['prd', '产品', '需求']):
            return 'prd_generation'
        elif any(keyword in task_lower for keyword in ['技术栈', '推荐', '架构']):
            return 'tech_recommendation'
        elif any(keyword in task_lower for keyword in ['知识', '查询', '解释']):
            return 'knowledge_query'
        else:
            return 'default'
    
    def _handle_code_generation(self, task, context):
        """处理代码生成任务"""
        return {"type": "code_generation", "content": f"代码生成任务: {task}"}
    
    def _handle_prd_generation(self, task, context):
        """处理PRD生成任务"""
        return {"type": "prd_generation", "content": f"PRD生成任务: {task}"}
    
    def _handle_tech_recommendation(self, task, context):
        """处理技术推荐任务"""
        return {"type": "tech_recommendation", "content": f"技术推荐任务: {task}"}
    
    def _handle_knowledge_query(self, task, context):
        """处理知识查询任务"""
        return {"type": "knowledge_query", "content": f"知识查询任务: {task}"}
    
    def _handle_default(self, task, context):
        """处理默认任务"""
        return {"type": "default", "content": f"通用任务: {task}"}
    
    def _generate_response(self, result, context):
        """生成响应"""
        personality_name = context.get('personality', 'default')
        personality = self.personality_distiller.get_personality(personality_name)
        
        if personality:
            style = personality.get('style_preferences', {})
            response = f"【{personality_name}风格】\n"
        else:
            response = ""
        
        response += f"任务类型: {result['type']}\n"
        response += f"任务内容: {result['content']}\n"
        response += f"状态: {self.state_machine.get_state()['current_state']}"
        
        return response

class ADKIntegration:
    """ADK/Agent Runtime 集成主类"""
    
    def __init__(self, platform_manager=None):
        self.orchestrator = OrchestratorAgent()
        self.personality_distiller = PersonalityDistiller()
        self.state_machine = AgentStateMachine()
        
        # 处理平台管理器
        if platform_manager:
            self.platform_manager = platform_manager
        elif PlatformManager:
            self.platform_manager = PlatformManager()
        else:
            self.platform_manager = None
            logger.warning("平台管理器不可用，将使用内置功能")
        
        self._register_core_agents()
    
    def _register_core_agents(self):
        """注册核心Agent"""
        # 视觉Agent
        self.orchestrator.register_agent('visual_agent', VisualAgent())
        self.orchestrator.register_agent('diagram_agent', DiagramAgent())
        self.orchestrator.register_agent('ascii_artist_agent', ASCIIArtistAgent())
        
        # 语言Agent
        self.orchestrator.register_agent('vocal_agent', VocalAgent())
        self.orchestrator.register_agent('talk_agent', TalkAgent())
        
        # 专业Agent
        self.orchestrator.register_agent('code_agent', CodeAgent())
        self.orchestrator.register_agent('prd_agent', PRDAgent())
        self.orchestrator.register_agent('tech_agent', TechAgent())
    
    def process(self, task, context=None):
        """处理任务"""
        return self.orchestrator.orchestrate(task, context)
    
    def add_personality(self, name, materials):
        """添加人物性格"""
        return self.personality_distiller.distill_personality(name, materials)
    
    def get_personality(self, name):
        """获取人物性格"""
        return self.personality_distiller.get_personality(name)
    
    def list_personalities(self):
        """列出所有人物性格"""
        return self.personality_distiller.list_personalities()
    
    def get_state(self):
        """获取系统状态"""
        return {
            'state_machine': self.state_machine.get_state(),
            'registered_agents': self.orchestrator.list_agents(),
            'personalities': self.personality_distiller.list_personalities()
        }

# 子Agent定义
class VisualAgent:
    def execute(self, task):
        return f"视觉处理: {task}"

class DiagramAgent:
    def execute(self, task):
        return f"图表生成: {task}"

class ASCIIArtistAgent:
    def execute(self, task):
        return f"ASCII艺术生成: {task}"

class VocalAgent:
    def execute(self, task):
        return f"语音处理: {task}"

class TalkAgent:
    def execute(self, task):
        return f"对话处理: {task}"

class CodeAgent:
    def execute(self, task):
        return f"代码生成: {task}"

class PRDAgent:
    def execute(self, task):
        return f"PRD生成: {task}"

class TechAgent:
    def execute(self, task):
        return f"技术推荐: {task}"

if __name__ == "__main__":
    # 测试集成
    adk = ADKIntegration()
    
    print("系统状态:")
    print(adk.get_state())
    print()
    
    # 添加人物性格
    print("添加人物性格 - 乔布斯:")
    materials = ["乔布斯演讲", "苹果产品发布会", "访谈记录"]
    adk.add_personality("乔布斯", materials)
    print(adk.get_personality("乔布斯"))
    print()
    
    # 处理任务
    print("处理任务:")
    result = adk.process("帮我生成一个电商平台的PRD文档", {"personality": "乔布斯"})
    print(result)
    print()
    
    # 测试状态机
    print("状态机测试:")
    print(adk.get_state()['state_machine'])
