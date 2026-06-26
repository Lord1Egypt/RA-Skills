"""
任务路由器 - 识别用户意图并分发到对应子技能
"""

from enum import Enum
from typing import Dict, Any, Optional
import re


class SkillType(Enum):
    """子技能类型枚举"""
    ML_STRUCT = "ml_struct"
    DL_DAMAGE = "dl_damage"
    DIGITAL_TWIN = "digital_twin"
    SMART_MONITOR = "smart_monitor"
    UNKNOWN = "unknown"


class TaskRouter:
    """
    任务路由器
    
    功能：
    1. 识别用户意图
    2. 提取参数
    3. 分发到对应子技能
    4. 整合返回结果
    """
    
    def __init__(self):
        """初始化路由器"""
        self.skills = {}
        self._register_keywords()
    
    def _register_keywords(self):
        """注册关键词映射"""
        self.keywords = {
            SkillType.ML_STRUCT: [
                "机器学习", "预测", "回归", "结构响应", "ml",
                "gpr", "神经网络", "xgboost", "代理模型"
            ],
            SkillType.DL_DAMAGE: [
                "损伤", "裂缝", "识别", "检测", "图像", "图片",
                "深度学习", "cnn", "yolo", "视觉"
            ],
            SkillType.DIGITAL_TWIN: [
                "数字孪生", "孪生", "实时", "在线", "仿真",
                "rom", "降阶", "模型更新"
            ],
            SkillType.SMART_MONITOR: [
                "监测", "传感器", "模态", "频域", "异常",
                "加速度", "位移", "应变", "信号处理"
            ]
        }
    
    def route(self, intent: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        路由任务到对应子技能
        
        Args:
            intent: 用户意图描述
            params: 参数字典
            
        Returns:
            执行结果
        """
        if params is None:
            params = {}
        
        # 识别意图
        skill_type = self._classify_intent(intent)
        
        if skill_type == SkillType.UNKNOWN:
            return {
                "status": "error",
                "message": "无法识别任务类型，请明确说明需求",
                "suggestions": [
                    "机器学习预测结构响应",
                    "损伤识别",
                    "数字孪生建模",
                    "监测数据分析"
                ]
            }
        
        # 获取对应技能
        skill = self.skills.get(skill_type.value)
        if skill is None:
            return {
                "status": "error",
                "message": f"技能 {skill_type.value} 未加载"
            }
        
        # 执行技能
        try:
            result = skill.execute(params)
            result["skill_type"] = skill_type.value
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "skill_type": skill_type.value
            }
    
    def _classify_intent(self, intent: str) -> SkillType:
        """
        分类用户意图
        
        Args:
            intent: 用户输入
            
        Returns:
            技能类型
        """
        scores = {skill: 0 for skill in SkillType}
        
        for skill_type, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword.lower() in intent.lower():
                    scores[skill_type] += 1
        
        # 返回得分最高的技能
        best_skill = max(scores, key=scores.get)
        if scores[best_skill] > 0:
            return best_skill
        
        return SkillType.UNKNOWN
    
    def register_skill(self, skill_type: str, skill_instance):
        """
        注册子技能
        
        Args:
            skill_type: 技能类型名称
            skill_instance: 技能实例
        """
        self.skills[skill_type] = skill_instance
