"""
SkillQualityAssessor — 技能质量评估器
评估生成技能的质量，给出改进建议
"""

import re
from pathlib import Path
from typing import Dict, List, Optional


class SkillQualityAssessor:
    """技能质量评估器"""
    
    # 质量维度
    QUALITY_DIMENSIONS = {
        'documentation': 0.2,      # 文档完整性
        'structure': 0.2,           # 目录结构
        'executability': 0.3,      # 可执行性
        'trigger_clarity': 0.15,   # 触发条件清晰度
        'error_handling': 0.15,    # 错误处理
    }
    
    def __init__(self):
        self.shared_skills_dir = Path.home() / "SharedSkills"
    
    def assess_skill(self, skill_name: str) -> Dict:
        """
        评估技能质量
        返回详细评分和改建议
        """
        result = {
            'skill_name': skill_name,
            'score': 0.0,
            'grade': '',
            'dimensions': {},
            'issues': [],
            'suggestions': [],
            'passed': False,
        }
        
        skill_path = self.shared_skills_dir / skill_name
        if not skill_path.exists():
            result['issues'].append('技能目录不存在')
            return result
        
        # 检查必需文件
        skill_md = skill_path / 'SKILL.md'
        if not skill_md.exists():
            result['issues'].append('缺少 SKILL.md')
            return result
        
        # 读取 SKILL.md
        try:
            content = skill_md.read_text(encoding='utf-8')
        except:
            result['issues'].append('无法读取 SKILL.md')
            return result
        
        # 各维度评分
        result['dimensions']['documentation'] = self._assess_documentation(content)
        result['dimensions']['structure'] = self._assess_structure(skill_path)
        result['dimensions']['executability'] = self._assess_executability(skill_path)
        result['dimensions']['trigger_clarity'] = self._assess_triggers(content)
        result['dimensions']['error_handling'] = self._assess_error_handling(content, skill_path)
        
        # 计算总分
        total = sum(
            self.QUALITY_DIMENSIONS[dim] * score
            for dim, score in result['dimensions'].items()
        )
        result['score'] = round(total * 100, 1)
        
        # 等级
        result['grade'] = self._score_to_grade(result['score'])
        result['passed'] = result['score'] >= 60
        
        # 生成建议
        result['suggestions'] = self._generate_suggestions(result['dimensions'])
        
        return result
    
    def _assess_documentation(self, content: str) -> float:
        """评估文档完整性"""
        score = 0.0
        
        # 必须包含的元素
        required = ['description', '触发', '能力', '使用']
        for req in required:
            if req in content:
                score += 0.2
        
        # 描述长度
        desc_match = re.search(r'description:\s*"?([^"\n]+)"?', content)
        if desc_match and len(desc_match.group(1)) > 20:
            score += 0.2
        
        return min(1.0, score)
    
    def _assess_structure(self, skill_path: Path) -> float:
        """评估目录结构"""
        score = 0.0
        
        required = ['SKILL.md']
        for f in required:
            if (skill_path / f).exists():
                score += 0.3
        
        scripts_dir = skill_path / 'scripts'
        if scripts_dir.exists() and scripts_dir.is_dir():
            score += 0.2
        
        ref_dir = skill_path / 'references'
        if ref_dir.exists() and ref_dir.is_dir():
            score += 0.2
        
        return min(1.0, score)
    
    def _assess_executability(self, skill_path: Path) -> float:
        """评估可执行性"""
        score = 0.0
        
        scripts_dir = skill_path / 'scripts'
        if scripts_dir.exists():
            scripts = list(scripts_dir.glob('*.py')) + list(scripts_dir.glob('*.sh'))
            if scripts:
                score += 0.6
                # 检查脚本是否有执行权限或 shebang
                for script in scripts[:3]:
                    content = script.read_text(encoding='utf-8', errors='ignore')
                    if script.suffix == '.py' and content.startswith('#!'):
                        score += 0.1
                    elif script.suffix == '.sh' and content.startswith('#!'):
                        score += 0.1
        
        return min(1.0, score)
    
    def _assess_triggers(self, content: str) -> float:
        """评估触发条件清晰度"""
        score = 0.0
        
        if '触发' in content:
            score += 0.3
        
        if '场景' in content:
            score += 0.2
        
        # 检查触发词定义
        trigger_section = re.search(r'触发.*?:(.*?)(?:\n##|\Z)', content, re.DOTALL)
        if trigger_section and len(trigger_section.group(1)) > 20:
            score += 0.3
        
        # 检查是否列举了具体触发条件
        bullet_points = len(re.findall(r'^\s*[\d\*\-]\s', content, re.MULTILINE))
        if bullet_points >= 3:
            score += 0.2
        
        return min(1.0, score)
    
    def _assess_error_handling(self, content: str, skill_path: Path) -> float:
        """评估错误处理"""
        score = 0.5  # 默认中等
        
        error_keywords = ['错误', 'error', '异常', 'exception', '失败', '注意事项']
        for kw in error_keywords:
            if kw in content.lower():
                score += 0.1
        
        return min(1.0, score)
    
    def _score_to_grade(self, score: float) -> str:
        """分数转等级"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _generate_suggestions(self, dimensions: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if dimensions.get('documentation', 0) < 0.8:
            suggestions.append('文档不够完整，建议补充 description、触发场景、能力清单')
        
        if dimensions.get('structure', 0) < 0.6:
            suggestions.append('目录结构不完整，建议添加 scripts/ 目录')
        
        if dimensions.get('executability', 0) < 0.5:
            suggestions.append('缺少可执行脚本，建议在 scripts/ 目录添加核心脚本')
        
        if dimensions.get('trigger_clarity', 0) < 0.7:
            suggestions.append('触发条件不够清晰，建议明确列出触发场景')
        
        if dimensions.get('error_handling', 0) < 0.6:
            suggestions.append('错误处理不够完善，建议添加异常处理和注意事项')
        
        return suggestions
    
    def assess_batch(self, skill_names: List[str]) -> Dict:
        """批量评估技能"""
        results = {}
        for name in skill_names:
            results[name] = self.assess_skill(name)
        return results
