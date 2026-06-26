#!/usr/bin/env python3
"""
逻辑对齐验证工具
对比优化前后的 skill，确保功能完整性
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Set


class SkillValidator:
    def __init__(self, original_path: Path, optimized_path: Path):
        self.original_path = original_path
        self.optimized_path = optimized_path
        self.issues = []
        
    def load_skill_md(self, path: Path) -> Dict[str, str]:
        """加载 SKILL.md 并解析 frontmatter 和 body"""
        skill_md = path / "SKILL.md"
        if not skill_md.exists():
            return {'frontmatter': '', 'body': ''}
        
        content = skill_md.read_text(encoding='utf-8')
        
        # 解析 frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if frontmatter_match:
            return {
                'frontmatter': frontmatter_match.group(1),
                'body': frontmatter_match.group(2)
            }
        return {'frontmatter': '', 'body': content}
    
    def extract_keywords(self, text: str) -> Set[str]:
        """提取关键词（中英文）"""
        # 简单的关键词提取：移除常见停用词
        stop_words = {'的', '了', '是', '在', '有', '和', '与', '或', '但', 'the', 'a', 'an', 'and', 'or', 'but'}
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text.lower())
        return set(w for w in words if len(w) > 1 and w not in stop_words)
    
    def validate_description_coverage(self) -> bool:
        """验证 description 的覆盖度"""
        original = self.load_skill_md(self.original_path)
        optimized = self.load_skill_md(self.optimized_path)
        
        # 提取 description
        orig_desc_match = re.search(r'description:\s*(.+?)(?:\n[a-z]+:|$)', original['frontmatter'], re.DOTALL)
        opt_desc_match = re.search(r'description:\s*(.+?)(?:\n[a-z]+:|$)', optimized['frontmatter'], re.DOTALL)
        
        if not orig_desc_match or not opt_desc_match:
            self.issues.append({
                'type': 'warning',
                'message': '无法提取 description，跳过覆盖度检查'
            })
            return True
        
        orig_desc = orig_desc_match.group(1).strip()
        opt_desc = opt_desc_match.group(1).strip()
        
        # 提取关键词
        orig_keywords = self.extract_keywords(orig_desc)
        opt_keywords = self.extract_keywords(opt_desc)
        
        # 检查是否有重要关键词丢失
        missing_keywords = orig_keywords - opt_keywords
        
        if missing_keywords:
            # 过滤掉一些不重要的词
            important_missing = [w for w in missing_keywords if len(w) > 2]
            if important_missing:
                self.issues.append({
                    'type': 'error',
                    'message': f'description 丢失了重要关键词：{", ".join(important_missing)}'
                })
                return False
        
        return True
    
    def validate_function_preservation(self) -> bool:
        """验证功能入口是否保留"""
        original = self.load_skill_md(self.original_path)
        optimized = self.load_skill_md(self.optimized_path)
        
        # 查找功能列表或标题
        orig_headers = re.findall(r'^#{1,6}\s+(.+)$', original['body'], re.MULTILINE)
        opt_headers = re.findall(r'^#{1,6}\s+(.+)$', optimized['body'], re.MULTILINE)
        
        orig_header_set = set(h.strip().lower() for h in orig_headers)
        opt_header_set = set(h.strip().lower() for h in opt_headers)
        
        # 检查是否有重要章节消失
        missing_headers = orig_header_set - opt_header_set
        
        if missing_headers:
            # 允许一些常见的优化（如 "使用示例" -> "示例"）
            fuzzy_match = []
            for mh in missing_headers:
                if not any(mh in oh or oh in mh for oh in opt_header_set):
                    fuzzy_match.append(mh)
            
            if fuzzy_match:
                self.issues.append({
                    'type': 'warning',
                    'message': f'以下章节可能被删除：{", ".join(fuzzy_match)}'
                })
        
        return True
    
    def validate_file_references(self) -> bool:
        """验证文件引用完整性"""
        original = self.load_skill_md(self.original_path)
        optimized = self.load_skill_md(self.optimized_path)
        
        # 查找文件引用（markdown 链接和代码中的路径）
        orig_refs = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', original['body'])
        orig_refs += re.findall(r'`([^`]*(?:scripts|references|assets)/[^`]+)`', original['body'])
        
        opt_refs = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', optimized['body'])
        opt_refs += re.findall(r'`([^`]*(?:scripts|references|assets)/[^`]+)`', optimized['body'])
        
        # 提取文件路径
        orig_files = set()
        for ref in orig_refs:
            path = ref[1] if isinstance(ref, tuple) else ref
            if '/' in path and not path.startswith('http'):
                orig_files.add(path)
        
        opt_files = set()
        for ref in opt_refs:
            path = ref[1] if isinstance(ref, tuple) else ref
            if '/' in path and not path.startswith('http'):
                opt_files.add(path)
        
        missing_files = orig_files - opt_files
        
        if missing_files:
            self.issues.append({
                'type': 'error',
                'message': f'以下文件引用可能丢失：{", ".join(missing_files)}'
            })
            return False
        
        return True
    
    def validate_scripts_correspondence(self) -> bool:
        """验证 scripts/ 调用是否对应原有逻辑"""
        original = self.load_skill_md(self.original_path)
        optimized = self.load_skill_md(self.optimized_path)
        
        # 查找新增的脚本调用
        opt_scripts = re.findall(r'scripts/([a-zA-Z0-9_-]+\.py)', optimized['body'])
        orig_scripts = re.findall(r'scripts/([a-zA-Z0-9_-]+\.py)', original['body'])
        
        new_scripts = set(opt_scripts) - set(orig_scripts)
        
        if new_scripts:
            # 检查脚本是否真的存在
            for script in new_scripts:
                script_path = self.optimized_path / "scripts" / script
                if not script_path.exists():
                    self.issues.append({
                        'type': 'error',
                        'message': f'引用的脚本不存在：scripts/{script}'
                    })
                    return False
        
        return True
    
    def run_validation(self) -> Dict:
        """运行所有验证"""
        results = {
            'description_coverage': self.validate_description_coverage(),
            'function_preservation': self.validate_function_preservation(),
            'file_references': self.validate_file_references(),
            'scripts_correspondence': self.validate_scripts_correspondence()
        }
        
        return {
            'passed': all(results.values()),
            'results': results,
            'issues': self.issues
        }


def main():
    if len(sys.argv) < 3:
        print("用法: python validate_logic.py --original <path> --optimized <path>")
        sys.exit(1)
    
    args = {}
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i].startswith('--'):
            args[sys.argv[i][2:]] = sys.argv[i+1]
    
    original_path = Path(args.get('original', ''))
    optimized_path = Path(args.get('optimized', ''))
    
    if not original_path.exists() or not optimized_path.exists():
        print("❌ 错误：路径不存在")
        sys.exit(1)
    
    validator = SkillValidator(original_path, optimized_path)
    result = validator.run_validation()
    
    print("\n" + "="*60)
    print("逻辑对齐验证报告")
    print("="*60)
    
    for check, passed in result['results'].items():
        status = "✅ 通过" if passed else "❌ 失败"
        check_name = {
            'description_coverage': 'Description 覆盖度',
            'function_preservation': '功能入口保留',
            'file_references': '文件引用完整性',
            'scripts_correspondence': 'Scripts 对应性'
        }.get(check, check)
        print(f"{status} {check_name}")
    
    if result['issues']:
        print("\n" + "-"*60)
        print("发现的问题：")
        print("-"*60)
        for issue in result['issues']:
            emoji = "🔴" if issue['type'] == 'error' else "⚠️"
            print(f"{emoji} [{issue['type'].upper()}] {issue['message']}")
    
    print("\n" + "="*60)
    if result['passed']:
        print("✅ 验证通过！优化后的 skill 保留了原有功能。")
        sys.exit(0)
    else:
        print("⚠️ 验证未通过，请检查上述问题。")
        sys.exit(1)


if __name__ == "__main__":
    main()
