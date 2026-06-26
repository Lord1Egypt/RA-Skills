"""
SkillLearner — 技能学习器
通过研究现有技能、分析工作日志，自主学习如何开发新技能
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class SkillLearner:
    """技能学习器"""
    
    def __init__(self, skill_scores: Dict, skill_registry: Dict):
        """
        初始化学习器
        skill_scores: 技能评分数据
        skill_registry: 技能注册表
        """
        self.skill_scores = skill_scores
        self.skill_registry = skill_registry
        self.shared_skills_dir = Path.home() / "SharedSkills"
    
    def study_existing_skills(self, count: int = 5) -> List[Dict]:
        """
        研究现有技能的结构和模式
        返回高质量技能的元数据分析
        """
        studies = []
        
        # 获取评分最高的技能
        top_skills = sorted(
            self.skill_scores.items(),
            key=lambda x: x[1].get('score', 0),
            reverse=True
        )[:count]
        
        for skill_name, score_data in top_skills:
            skill_path = self.shared_skills_dir / skill_name
            if not skill_path.exists():
                continue
            
            study = {
                'name': skill_name,
                'score': score_data.get('score', 0),
                'calls': score_data.get('calls', 0),
                'files': [],
                'structure': {},
            }
            
            # 分析技能结构
            for file_path in skill_path.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    rel_path = file_path.relative_to(skill_path)
                    study['files'].append(str(rel_path))
                    
                    # 统计代码行数
                    if file_path.suffix in ['.py', '.js', '.sh']:
                        try:
                            lines = len(file_path.read_text(encoding='utf-8', errors='ignore').splitlines())
                            study['structure'][str(rel_path)] = lines
                        except:
                            pass
            
            studies.append(study)
        
        return studies
    
    def learn_skill_patterns(self) -> Dict:
        """
        学习技能开发模式
        从现有技能中提取通用模式
        """
        patterns = {
            'common_files': [],      # 常见文件
            'common_patterns': [],    # 代码模式
            'trigger_patterns': [],    # 触发词模式
            'structure_hints': [],    # 结构建议
        }
        
        # 统计常见文件
        file_count = {}
        
        for skill_dir in self.shared_skills_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue
            
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    rel_path = file_path.relative_to(skill_dir)
                    file_count[str(rel_path)] = file_count.get(str(rel_path), 0) + 1
        
        # 取最常见的文件
        patterns['common_files'] = [
            {'file': f, 'count': c}
            for f, c in sorted(file_count.items(), key=lambda x: -x[1])[:10]
        ]
        
        # 生成结构提示
        patterns['structure_hints'] = [
            "SKILL.md 是必需的，包含技能的描述和使用方式",
            "scripts/ 目录放置核心脚本",
            "references/ 目录放置参考文档",
            "技能需要定义触发场景 (trigger conditions)",
            "技能应该有输入输出规范",
        ]
        
        return patterns
    
    def generate_skill_requirements(self, gap_type: str, context: str) -> Dict:
        """
        根据技能缺口和上下文生成技能需求规格
        """
        requirements = {
            'name': '',
            'description': '',
            'category': gap_type,
            'triggers': [],
            'capabilities': [],
            'inputs': [],
            'outputs': [],
            'dependencies': [],
            'quality_criteria': [],
        }
        
        # 基于缺口类型生成规格
        gap_specs = {
            'research': {
                'triggers': ['搜索', '查找', '查询', '研究'],
                'capabilities': ['网络搜索', '内容提取', '信息整理'],
                'inputs': ['查询关键词'],
                'outputs': ['搜索结果列表', '关键信息摘要'],
            },
            'code': {
                'triggers': ['写代码', '开发', '编程', '代码问题'],
                'capabilities': ['代码生成', '代码审查', '调试辅助'],
                'inputs': ['需求描述', '编程语言'],
                'outputs': ['代码片段', '解决方案'],
            },
            'data': {
                'triggers': ['分析', '统计数据', '处理数据'],
                'capabilities': ['数据分析', '可视化', '报表生成'],
                'inputs': ['数据源', '分析目标'],
                'outputs': ['分析报告', '图表'],
            },
            'media': {
                'triggers': ['处理图片', '处理视频', '音频处理'],
                'capabilities': ['格式转换', '内容提取', '媒体编辑'],
                'inputs': ['媒体文件'],
                'outputs': ['处理后的媒体'],
            },
            'devops': {
                'triggers': ['部署', '服务器', '运维'],
                'capabilities': ['自动化部署', '监控告警', '日志分析'],
                'inputs': ['部署配置'],
                'outputs': ['部署状态'],
            },
        }
        
        spec = gap_specs.get(gap_type, {})
        for key in ['triggers', 'capabilities', 'inputs', 'outputs']:
            if key in spec:
                requirements[key] = spec[key]
        
        # 生成技能名称
        requirements['name'] = f"auto-{gap_type}-{datetime.now().strftime('%m%d')}"
        requirements['description'] = f"自动开发的{gap_type}类技能，用于{context[:50]}"
        
        # 通用质量标准
        requirements['quality_criteria'] = [
            '有清晰的 SKILL.md 文档',
            '有具体可执行的脚本',
            '触发条件明确',
            '错误处理完善',
            '有使用示例',
        ]
        
        return requirements
    
    def validate_skill_idea(self, skill_name: str, requirements: Dict) -> Dict:
        """
        验证技能想法的可行性
        """
        validation = {
            'feasible': True,
            'issues': [],
            'suggestions': [],
            'estimated_complexity': 'medium',
        }
        
        # 检查是否已存在同名技能
        if skill_name in self.skill_scores:
            validation['feasible'] = False
            validation['issues'].append(f"技能 {skill_name} 已存在")
        
        # 检查名称格式
        if not skill_name.replace('-', '').replace('_', '').isalnum():
            validation['issues'].append("技能名称只能包含字母、数字、-和_")
        
        # 检查描述是否完整
        if not requirements.get('description'):
            validation['issues'].append("缺少技能描述")
        
        if not requirements.get('triggers'):
            validation['feasible'] = False
            validation['issues'].append("缺少触发条件定义")
        
        if not requirements.get('capabilities'):
            validation['feasible'] = False
            validation['issues'].append("缺少能力定义")
        
        # 复杂度评估
        if len(requirements.get('capabilities', [])) > 5:
            validation['estimated_complexity'] = 'high'
            validation['suggestions'].append("技能能力过多，建议拆分")
        
        return validation
