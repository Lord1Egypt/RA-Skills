#!/usr/bin/env python3
"""
ClawHub Auto Publisher - 自动上架 skills 到 ClawHub
"""
import os
import re
import json
import yaml
from datetime import datetime
from pathlib import Path

class ClawHubPublisher:
    def __init__(self):
        self.skills_dir = Path("~/.openclaw/workspace/skills").expanduser()
        self.api_key = os.getenv("CLAWHUB_API_KEY")
        
    def scan_skills(self):
        """扫描本地所有 skills"""
        skills = []
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    skill = self._parse_skill(skill_dir)
                    if skill:
                        skills.append(skill)
        return skills
    
    def _parse_skill(self, skill_dir):
        """解析 skill 元数据"""
        skill_file = skill_dir / "SKILL.md"
        with open(skill_file) as f:
            content = f.read()
        
        # 提取 frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
        
        try:
            metadata = yaml.safe_load(match.group(1))
        except:
            return None
        
        # 计算价格
        suggested_price = self._suggest_price(content, metadata)
        
        return {
            'name': skill_dir.name,
            'metadata': metadata,
            'description': metadata.get('description', ''),
            'suggested_price': suggested_price,
            'path': str(skill_dir),
            'ready': self._check_ready(skill_dir)
        }
    
    def _suggest_price(self, content, metadata):
        """智能定价建议"""
        base_price = 300
        
        # 根据功能复杂度调整
        if 'auto' in content.lower() or 'automatic' in content.lower():
            base_price += 100
        
        # 根据类别调整
        category = metadata.get('metadata', {}).get('openclaw', {}).get('category', '')
        if category == 'earner':
            base_price += 200
        elif category == 'productivity':
            base_price += 100
        
        # 根据代码量调整
        code_files = list(Path(metadata.get('path', '')).glob('*.py')) if metadata.get('path') else []
        base_price += len(code_files) * 50
        
        return min(base_price, 1000)  # 上限 1000
    
    def _check_ready(self, skill_dir):
        """检查 skill 是否准备好上架"""
        required_files = ['SKILL.md']
        optional_files = ['README.md', 'requirements.txt', '*.py']
        
        has_required = all((skill_dir / f).exists() for f in required_files)
        has_code = any(len(list(skill_dir.glob(f))) > 0 for f in optional_files[2:])
        
        return has_required and has_code
    
    def publish(self, skill_name=None, dry_run=False):
        """上架 skill"""
        skills = self.scan_skills()
        
        if skill_name:
            skills = [s for s in skills if s['name'] == skill_name]
        
        print(f"Found {len(skills)} skills")
        print("=" * 60)
        
        for skill in skills:
            status = "✅ Ready" if skill['ready'] else "⏳ Draft"
            print(f"\n{status} | {skill['name']}")
            print(f"  Description: {skill['description'][:60]}...")
            print(f"  Suggested Price: {skill['suggested_price']} credits")
            
            if skill['ready'] and not dry_run:
                self._upload_to_clawhub(skill)
    
    def _upload_to_clawhub(self, skill):
        """上传到 ClawHub"""
        # TODO: 实现实际的 ClawHub API 调用
        print(f"  🚀 Uploading {skill['name']} to ClawHub...")
        return True

def main():
    publisher = ClawHubPublisher()
    
    import sys
    dry_run = '--dry-run' in sys.argv
    
    publisher.publish(dry_run=dry_run)

if __name__ == "__main__":
    main()
