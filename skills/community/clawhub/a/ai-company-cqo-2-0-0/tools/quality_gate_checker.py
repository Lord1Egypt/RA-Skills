#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quality Gate Checker - Skill质量门禁检查器
CQO-001 共享工具

功能：自动检查Skill是否符合质量门禁标准
检查项：
1. SKILL.md 格式规范
2. meta.json 完整性和版本号合规
3. 无恶意代码特征
4. 无敏感信息泄露
5. 描述清晰度

使用：python quality_gate_checker.py <skill_path>
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

class QualityGateChecker:
    """Skill质量门禁检查器"""
    
    # 质量门禁标准
    GATES = {
        'G0': '必备文件检查',
        'G1': 'SKILL.md格式规范',
        'G2': 'meta.json完整性',
        'G3': '安全合规检查',
        'G4': '描述质量评估'
    }
    
    # 敏感信息模式
    SENSITIVE_PATTERNS = [
        r'api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{16,}',
        r'password["\']?\s*[:=]\s*["\']?[^\s"\']+',
        r'secret["\']?\s*[:=]\s*["\']?[^\s"\']+',
        r'token["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
        r'private[_-]?key["\']?\s*[:=]',
        r'AKIA[0-9A-Z]{16}',  # AWS Access Key
        r'ghp_[a-zA-Z0-9]{36}',  # GitHub Personal Token
    ]
    
    # 恶意代码特征
    DANGEROUS_PATTERNS = [
        r'eval\s*\(',
        r'exec\s*\(',
        r'subprocess\.call\s*\([^)]*shell\s*=\s*True',
        r'os\.system\s*\(',
        r'__import__\s*\(',
        r'compile\s*\(',
    ]
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.results: Dict[str, List[str]] = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.score = 0
        self.max_score = 100
        
    def check(self) -> Tuple[bool, Dict]:
        """执行全部门禁检查"""
        print(f"🔍 开始质量门禁检查: {self.skill_path}")
        print("=" * 60)
        
        # G0: 必备文件检查
        self._check_g0_required_files()
        
        # G1: SKILL.md格式规范
        self._check_g1_skill_md_format()
        
        # G2: meta.json完整性
        self._check_g2_meta_json()
        
        # G3: 安全合规检查
        self._check_g3_security()
        
        # G4: 描述质量评估
        self._check_g4_description_quality()
        
        # 计算总分
        self.score = len(self.results['passed']) * 20
        
        print("=" * 60)
        print(f"📊 检查完成 - 得分: {self.score}/{self.max_score}")
        
        passed_all = len(self.results['failed']) == 0
        
        return passed_all, {
            'score': self.score,
            'passed': self.results['passed'],
            'failed': self.results['failed'],
            'warnings': self.results['warnings']
        }
    
    def _check_g0_required_files(self):
        """G0: 检查必备文件"""
        print("\n🚪 G0: 必备文件检查")
        
        required_files = ['SKILL.md', 'meta.json']
        all_exist = True
        
        for file in required_files:
            file_path = self.skill_path / file
            if file_path.exists():
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} - 缺失")
                self.results['failed'].append(f'G0: 缺少 {file}')
                all_exist = False
        
        if all_exist:
            self.results['passed'].append('G0: 所有必备文件存在')
    
    def _check_g1_skill_md_format(self):
        """G1: 检查SKILL.md格式"""
        print("\n📄 G1: SKILL.md格式规范")
        
        skill_md_path = self.skill_path / 'SKILL.md'
        if not skill_md_path.exists():
            self.results['failed'].append('G1: SKILL.md不存在')
            return
        
        try:
            content = skill_md_path.read_text(encoding='utf-8')
        except Exception as e:
            self.results['failed'].append(f'G1: 读取SKILL.md失败 - {e}')
            return
        
        checks = {
            '标题': r'^#\s+.+',
            '描述': r'##?\s*描述|##?\s*Description|##?\s*简介',
            '触发条件': r'##?\s*触发|##?\s*Trigger|##?\s*使用场景',
            '执行流程': r'##?\s*流程|##?\s*Workflow|##?\s*执行步骤',
        }
        
        passed_checks = 0
        for check_name, pattern in checks.items():
            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                print(f"  ✅ 包含{check_name}")
                passed_checks += 1
            else:
                print(f"  ⚠️  缺少{check_name}部分")
                self.results['warnings'].append(f'G1: SKILL.md缺少{check_name}')
        
        if passed_checks >= 3:
            self.results['passed'].append(f'G1: SKILL.md格式规范 ({passed_checks}/4)')
        else:
            self.results['failed'].append(f'G1: SKILL.md格式不完整 ({passed_checks}/4)')
    
    def _check_g2_meta_json(self):
        """G2: 检查meta.json完整性"""
        print("\n📋 G2: meta.json完整性")
        
        meta_path = self.skill_path / 'meta.json'
        if not meta_path.exists():
            self.results['failed'].append('G2: meta.json不存在')
            return
        
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
        except json.JSONDecodeError as e:
            self.results['failed'].append(f'G2: meta.json格式错误 - {e}')
            return
        except Exception as e:
            self.results['failed'].append(f'G2: 读取meta.json失败 - {e}')
            return
        
        required_fields = ['name', 'version', 'description', 'author']
        missing_fields = []
        
        for field in required_fields:
            if field not in meta or not meta[field]:
                missing_fields.append(field)
        
        # 版本号格式检查
        version_valid = True
        if 'version' in meta:
            version_pattern = r'^\d+\.\d+\.\d+$'
            if not re.match(version_pattern, meta['version']):
                print(f"  ⚠️  版本号格式不规范: {meta.get('version')}")
                self.results['warnings'].append('G2: 版本号应使用语义化版本(x.y.z)')
                version_valid = False
        
        if not missing_fields and version_valid:
            self.results['passed'].append('G2: meta.json完整且版本号合规')
        elif not missing_fields:
            self.results['passed'].append('G2: meta.json完整')
        else:
            self.results['failed'].append(f'G2: meta.json缺少字段: {", ".join(missing_fields)}')
    
    def _check_g3_security(self):
        """G3: 安全合规检查"""
        print("\n🔒 G3: 安全合规检查")
        
        # 扫描所有文件
        all_files = list(self.skill_path.rglob('*'))
        text_files = [f for f in all_files if f.is_file() and f.suffix in ['.md', '.json', '.py', '.js', '.ts', '.txt', '.yaml', '.yml']]
        
        sensitive_found = []
        dangerous_found = []
        
        for file_path in text_files:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                rel_path = file_path.relative_to(self.skill_path)
                
                # 检查敏感信息
                for pattern in self.SENSITIVE_PATTERNS:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        sensitive_found.append(f"{rel_path}: {match.group()[:30]}...")
                
                # 检查危险代码
                for pattern in self.DANGEROUS_PATTERNS:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        dangerous_found.append(f"{rel_path}: {match.group()}")
                        
            except Exception:
                continue
        
        if sensitive_found:
            print(f"  ⚠️  发现 {len(sensitive_found)} 处潜在敏感信息")
            for item in sensitive_found[:3]:  # 只显示前3个
                print(f"     - {item}")
            self.results['warnings'].append(f'G3: 发现{len(sensitive_found)}处潜在敏感信息')
        else:
            print("  ✅ 未发现敏感信息")
        
        if dangerous_found:
            print(f"  ❌ 发现 {len(dangerous_found)} 处危险代码模式")
            for item in dangerous_found[:3]:
                print(f"     - {item}")
            self.results['failed'].append(f'G3: 发现{len(dangerous_found)}处危险代码')
        else:
            print("  ✅ 未发现危险代码")
        
        if not sensitive_found and not dangerous_found:
            self.results['passed'].append('G3: 安全合规检查通过')
        elif not dangerous_found:
            self.results['passed'].append('G3: 无危险代码')
    
    def _check_g4_description_quality(self):
        """G4: 描述质量评估"""
        print("\n✨ G4: 描述质量评估")
        
        skill_md_path = self.skill_path / 'SKILL.md'
        meta_path = self.skill_path / 'meta.json'
        
        quality_score = 0
        
        # 检查SKILL.md长度
        if skill_md_path.exists():
            content = skill_md_path.read_text(encoding='utf-8')
            if len(content) > 500:
                print("  ✅ SKILL.md内容充实")
                quality_score += 1
            else:
                print("  ⚠️  SKILL.md内容较短")
                self.results['warnings'].append('G4: SKILL.md内容较短')
        
        # 检查meta.json描述
        if meta_path.exists():
            try:
                with open(meta_path, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                desc = meta.get('description', '')
                if len(desc) > 20:
                    print("  ✅ meta.json描述清晰")
                    quality_score += 1
                else:
                    print("  ⚠️  meta.json描述较短")
                    self.results['warnings'].append('G4: meta.json描述不够清晰')
            except:
                pass
        
        if quality_score >= 2:
            self.results['passed'].append('G4: 描述质量良好')
        else:
            self.results['failed'].append('G4: 描述质量需改进')
    
    def generate_report(self) -> str:
        """生成检查报告"""
        report = []
        report.append("# Skill质量门禁检查报告")
        report.append(f"\n**检查对象**: {self.skill_path}")
        report.append(f"**检查时间**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**总得分**: {self.score}/{self.max_score}")
        report.append(f"**检查结果**: {'✅ 通过' if self.score >= 80 else '❌ 未通过'}")
        
        report.append("\n## 详细结果\n")
        
        if self.results['passed']:
            report.append("### ✅ 通过项\n")
            for item in self.results['passed']:
                report.append(f"- {item}")
            report.append("")
        
        if self.results['failed']:
            report.append("### ❌ 失败项\n")
            for item in self.results['failed']:
                report.append(f"- {item}")
            report.append("")
        
        if self.results['warnings']:
            report.append("### ⚠️ 警告项\n")
            for item in self.results['warnings']:
                report.append(f"- {item}")
            report.append("")
        
        report.append("\n---\n*Generated by Quality Gate Checker v1.0*")
        
        return '\n'.join(report)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python quality_gate_checker.py <skill_path>")
        print("示例: python quality_gate_checker.py ./my-skill")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    if not os.path.exists(skill_path):
        print(f"❌ 错误: 路径不存在 {skill_path}")
        sys.exit(1)
    
    checker = QualityGateChecker(skill_path)
    passed, results = checker.check()
    
    # 保存报告
    report = checker.generate_report()
    report_path = Path(skill_path) / 'quality-gate-report.md'
    report_path.write_text(report, encoding='utf-8')
    print(f"\n📝 报告已保存: {report_path}")
    
    sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
