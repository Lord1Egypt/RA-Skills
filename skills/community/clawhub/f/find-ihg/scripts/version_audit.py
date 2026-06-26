#!/usr/bin/env python3
"""
IHG技能版本审计脚本
用于检查技能版本状态、文件完整性、变更历史
"""

import os
import json
import hashlib
import datetime
from pathlib import Path

class SkillAuditor:
    def __init__(self, skill_dir):
        self.skill_dir = Path(skill_dir)
        self.results = {
            "audit_time": datetime.datetime.now().isoformat(),
            "skill_name": "ihg-monitor",
            "status": "PASS",
            "checks": [],
            "warnings": [],
            "errors": []
        }
    
    def check_file_exists(self, file_path, description):
        """检查文件是否存在"""
        full_path = self.skill_dir / file_path
        exists = full_path.exists()
        
        check = {
            "check": f"文件存在性: {description}",
            "file": str(file_path),
            "status": "PASS" if exists else "FAIL",
            "details": f"文件{'存在' if exists else '不存在'}"
        }
        
        self.results["checks"].append(check)
        
        if not exists:
            self.results["warnings"].append(f"缺失文件: {file_path} - {description}")
        
        return exists
    
    def get_file_hash(self, file_path):
        """获取文件哈希值"""
        full_path = self.skill_dir / file_path
        
        if not full_path.exists():
            return None
        
        with open(full_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    
    def check_version_consistency(self):
        """检查版本一致性"""
        # 从SKILL.md提取版本
        skill_md_path = self.skill_dir / "SKILL.md"
        version_skills = "unknown"
        
        if skill_md_path.exists():
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                import re
                match = re.search(r'版本\s*[vV]?(\d+\.\d+\.\d+)', content)
                if match:
                    version_skills = match.group(1)
        
        # 从CHANGELOG.md获取最新版本
        changelog_path = self.skill_dir / "references" / "CHANGELOG.md"
        version_changelog = "unknown"
        
        if changelog_path.exists():
            with open(changelog_path, 'r', encoding='utf-8') as f:
                content = f.read()
                import re
                match = re.search(r'## v(\d+\.\d+\.\d+)', content)
                if match:
                    version_changelog = match.group(1)
        
        check = {
            "check": "版本一致性检查",
            "status": "PASS" if version_skills == version_changelog else "WARN",
            "details": f"SKILL.md: v{version_skills}, CHANGELOG.md: v{version_changelog}"
        }
        
        self.results["checks"].append(check)
        
        if version_skills != version_changelog:
            self.results["warnings"].append(f"版本不一致: SKILL.md(v{version_skills}) ≠ CHANGELOG.md(v{version_changelog})")
    
    def check_skill_json(self):
        """检查skills.json配置"""
        json_path = self.skill_dir / "skills.json"
        
        if not json_path.exists():
            self.results["errors"].append("skills.json文件不存在")
            return
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            skill = data.get("skills", [{}])[0]
            
            check = {
                "check": "skills.json配置验证",
                "status": "PASS",
                "details": f"技能ID: {skill.get('id')}, 名称: {skill.get('name')}"
            }
            
            self.results["checks"].append(check)
            
            # 检查执行命令
            exec_cmd = skill.get('exec', '')
            if 'query.py' not in exec_cmd:
                self.results["warnings"].append(f"执行命令可能不正确: {exec_cmd}")
                
        except Exception as e:
            self.results["errors"].append(f"skills.json解析错误: {str(e)}")
    
    def scan_directory_structure(self):
        """扫描目录结构"""
        file_tree = {}
        
        for root, dirs, files in os.walk(self.skill_dir):
            rel_root = Path(root).relative_to(self.skill_dir)
            
            # 跳过隐藏文件和目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            
            if str(rel_root) == '.':
                rel_root_str = "根目录"
            else:
                rel_root_str = str(rel_root)
            
            file_tree[rel_root_str] = {
                "directories": dirs,
                "files": files,
                "file_count": len(files)
            }
            
            # 记录文件哈希
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.skill_dir)
                file_hash = self.get_file_hash(rel_path)
                
                if file_hash:
                    key = f"{rel_root_str}/{file}" if rel_root_str != "根目录" else file
                    file_tree[rel_root_str].setdefault("file_hashes", {})[key] = file_hash
        
        check = {
            "check": "目录结构扫描",
            "status": "PASS",
            "details": f"共扫描 {len(file_tree)} 个目录"
        }
        
        self.results["checks"].append(check)
        self.results["directory_structure"] = file_tree
    
    def generate_report(self):
        """生成审计报告"""
        # 更新总体状态
        if self.results["errors"]:
            self.results["status"] = "FAIL"
        elif self.results["warnings"]:
            self.results["status"] = "WARN"
        
        # 统计
        self.results["summary"] = {
            "total_checks": len(self.results["checks"]),
            "passed_checks": len([c for c in self.results["checks"] if c["status"] == "PASS"]),
            "warn_checks": len([c for c in self.results["checks"] if c["status"] == "WARN"]),
            "fail_checks": len([c for c in self.results["checks"] if c["status"] == "FAIL"]),
            "warning_count": len(self.results["warnings"]),
            "error_count": len(self.results["errors"])
        }
        
        return self.results
    
    def run_full_audit(self):
        """运行完整审计"""
        print("🔍 开始IHG技能版本审计...")
        
        # 检查核心文件
        self.check_file_exists("SKILL.md", "技能主文档")
        self.check_file_exists("skills.json", "技能配置文件")
        self.check_file_exists("GOGO_INSTRUCTIONS.md", "Gogo调用指南")
        self.check_file_exists("references/CHANGELOG.md", "变更日志")
        
        # 检查脚本文件 (如果存在)
        self.check_file_exists("scripts/version_audit.py", "版本审计脚本")
        
        # 执行各项检查
        self.check_version_consistency()
        self.check_skill_json()
        self.scan_directory_structure()
        
        # 生成报告
        report = self.generate_report()
        
        print(f"✅ 审计完成 - 状态: {report['status']}")
        print(f"   检查项: {report['summary']['total_checks']}个")
        print(f"   通过: {report['summary']['passed_checks']}个")
        
        if report['warnings']:
            print(f"\n⚠️  警告 ({len(report['warnings'])}个):")
            for warning in report['warnings']:
                print(f"   - {warning}")
        
        if report['errors']:
            print(f"\n❌ 错误 ({len(report['errors'])}个):")
            for error in report['errors']:
                print(f"   - {error}")
        
        return report

def main():
    """主函数"""
    # 获取技能目录
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    
    # 创建审计器并运行
    auditor = SkillAuditor(skill_dir)
    report = auditor.run_full_audit()
    
    # 保存报告到JSON文件
    report_file = skill_dir / "references" / "audit_report.json"
    
    import json
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 详细报告已保存至: {report_file.relative_to(skill_dir)}")
    
    # 返回状态码
    return 0 if report['status'] != 'FAIL' else 1

if __name__ == "__main__":
    exit(main())