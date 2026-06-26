"""
SkillGenerator — 技能生成器
根据需求全自动生成技能文件
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .templates import SkillTemplates, SkillDirectoryStructure


class SkillGenerator:
    """技能生成器"""
    
    def __init__(self, registry=None):
        self.registry = registry
        self.shared_skills_dir = Path.home() / "SharedSkills"
        self.workspace = Path.home() / ".openclaw" / "workspace"
        self.templates = SkillTemplates()
    
    def generate_skill(self, requirements: Dict, auto_register: bool = True) -> Dict:
        """
        根据需求规格生成技能
        返回生成结果
        """
        result = {
            'success': False,
            'skill_name': '',
            'files': {},
            'errors': [],
            'warnings': [],
        }
        
        skill_name = requirements.get('name', '')
        if not skill_name:
            result['errors'].append('缺少技能名称')
            return result
        
        if not self._validate_name(skill_name):
            result['errors'].append(f'技能名称格式不正确: {skill_name}')
            return result
        
        skill_path = self.shared_skills_dir / skill_name
        if skill_path.exists():
            result['errors'].append(f'技能已存在: {skill_name}')
            return result
        
        try:
            files = self._generate_files(requirements)
            result['files'] = files
            
            for file_path, content in files.items():
                full_path = skill_path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding='utf-8')
            
            result['skill_name'] = skill_name
            result['success'] = True
            
            if auto_register and self.registry:
                self.registry.add_skill(
                    skill_name=skill_name,
                    category=requirements.get('category', 'general'),
                    description=requirements.get('description', ''),
                    auto_created=True,
                )
            
        except Exception as e:
            result['errors'].append(f'生成失败: {str(e)}')
        
        return result
    
    def _validate_name(self, name: str) -> bool:
        """验证技能名称"""
        if not name:
            return False
        import re
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))
    
    def _generate_files(self, requirements: Dict) -> Dict:
        """生成技能文件"""
        files = {}
        
        skill_name = requirements['name']
        description = requirements.get('description', '')
        category = requirements.get('category', 'general')
        triggers = requirements.get('triggers', [])
        capabilities = requirements.get('capabilities', [])
        tags = requirements.get('tags', [category])
        
        skill_md = self.templates.generate_skill_md(
            skill_name=skill_name,
            description=description,
            category=category,
            triggers=triggers,
            capabilities=capabilities,
            tags=tags,
            inputs=requirements.get('inputs', []),
            outputs=requirements.get('outputs', []),
            notes=requirements.get('notes', '无特殊注意事项'),
        )
        files['SKILL.md'] = skill_md
        
        if requirements.get('script_template'):
            script_name = requirements.get('script_name', skill_name)
            files[f'scripts/{script_name}.py'] = requirements['script_template']
        
        return files
    
    def create_from_gap(self, gap: Dict, requirements: Dict) -> Dict:
        """根据缺口分析创建技能"""
        merged = {**requirements}
        merged['name'] = requirements.get('name', gap.get('type', 'unknown'))
        merged['category'] = gap.get('type', 'general')
        return self.generate_skill(merged)
    
    def improve_existing_skill(self, skill_name: str, improvements: Dict) -> Dict:
        """改进现有技能"""
        result = {
            'success': False,
            'skill_name': skill_name,
            'changes': [],
            'errors': [],
        }
        
        skill_path = self.shared_skills_dir / skill_name
        if not skill_path.exists():
            result['errors'].append(f'技能不存在: {skill_name}')
            return result
        
        skill_md_path = skill_path / 'SKILL.md'
        if not skill_md_path.exists():
            result['errors'].append('缺少 SKILL.md')
            return result
        
        try:
            existing = skill_md_path.read_text(encoding='utf-8')
            changelog_entry = f"""

## 更新记录

**日期**: {datetime.now().strftime('%Y-%m-%d')}
**更新内容**: {improvements.get('description', '自动改进')}

{improvements.get('details', '')}
"""
            new_content = existing + changelog_entry
            skill_md_path.write_text(new_content, encoding='utf-8')
            result['success'] = True
            result['changes'].append('SKILL.md')
        except Exception as e:
            result['errors'].append(str(e))
        
        return result
    
    def get_generation_stats(self) -> Dict:
        """获取生成统计"""
        stats = {
            'total_skills': 0,
            'auto_created': 0,
            'categories': {},
        }
        
        if not self.shared_skills_dir.exists():
            return stats
        
        for skill_dir in self.shared_skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            stats['total_skills'] += 1
        
        return stats
