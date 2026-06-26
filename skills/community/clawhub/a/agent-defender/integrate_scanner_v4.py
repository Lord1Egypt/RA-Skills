#!/usr/bin/env python3
"""
🔄 agent-security-skill-scanner v4.1.0 → agent-defender 集成脚本
============================================================
功能：
- 同步最新检测规则 (optimized_rules)
- 同步 DLP 规则
- 同步 Runtime 规则
- 备份旧规则
- 生成集成报告
- 更新 SKILL.md

版本：v4.1.0 (2026-04-07)
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class ScannerToIntegrator:
    """Scanner v4.1.0 → agent-defender 集成器"""
    
    def __init__(self):
        # 源目录 (直接使用 skills/agent-security-skill-scanner)
        self.scanner_base = Path(__file__).parent.parent / "agent-security-skill-scanner"
        self.scanner_expert = self.scanner_base / "expert_mode"
        self.scanner_output = self.scanner_expert / "output"
        
        # 目标目录 (agent-defender)
        self.agent_defender = Path(__file__).parent
        self.defender_rules = self.agent_defender / "rules"
        self.defender_dlp = self.agent_defender / "dlp"
        self.defender_runtime = self.agent_defender / "runtime"
        self.backup_dir = self.agent_defender / "rules_backup"
        
        self.sync_log = []
        self.stats = {
            "rules_synced": 0,
            "dlp_synced": 0,
            "runtime_synced": 0,
            "backup_created": False,
            "errors": []
        }
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.sync_log.append(log_entry)
        print(log_entry)
    
    def backup_current_rules(self) -> str:
        """备份当前规则"""
        self.log("📦 开始备份当前规则...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        
        rules_dir = self.agent_defender / "rules"
        if rules_dir.exists() and any(rules_dir.iterdir()):
            shutil.copytree(rules_dir, backup_path)
            self.log(f"✅ 备份规则到：{backup_path}")
            self.stats["backup_created"] = True
            return str(backup_path)
        else:
            self.log("ℹ️ 无规则需要备份", "INFO")
            return None
    
    def sync_optimized_rules(self) -> int:
        """同步优化规则 (optimized_rules)"""
        self.log("📋 开始同步检测规则...")
        
        optimized_rules_dir = self.scanner_expert / "optimized_rules"
        
        if not optimized_rules_dir.exists():
            self.log("⚠️ 未找到 optimized_rules 目录", "ERROR")
            self.stats["errors"].append("optimized_rules 目录不存在")
            return 0
        
        # 确保目标目录存在
        self.defender_rules.mkdir(exist_ok=True)
        
        synced_count = 0
        
        for rule_file in optimized_rules_dir.glob("*.json"):
            dest = self.defender_rules / rule_file.name
            
            # 读取新规则
            try:
                with open(rule_file, 'r', encoding='utf-8') as f:
                    new_rules = json.load(f)
                
                # 检查是否需要更新
                if dest.exists():
                    with open(dest, 'r', encoding='utf-8') as f:
                        old_rules = json.load(f)
                    
                    # 简单比较：如果规则数量相同且内容一样，跳过
                    if old_rules == new_rules:
                        self.log(f"⏭️  跳过 (未变更): {rule_file.name}")
                        continue
                
                # 复制规则
                shutil.copy2(rule_file, dest)
                rule_count = len(new_rules) if isinstance(new_rules, list) else 1
                self.log(f"✅ 同步：{rule_file.name} ({rule_count} 条规则)")
                synced_count += 1
                
            except Exception as e:
                self.log(f"❌ 同步失败 {rule_file.name}: {e}", "ERROR")
                self.stats["errors"].append(f"{rule_file.name}: {str(e)}")
        
        self.stats["rules_synced"] = synced_count
        return synced_count
    
    def sync_dlp_rules(self) -> int:
        """同步 DLP 规则"""
        self.log("🛡️  开始同步 DLP 规则...")
        
        # 查找 DLP 规则文件
        dlp_candidates = [
            self.scanner_output / "dlp_rules.json",
            self.scanner_base / "dlp" / "custom_rules.json"
        ]
        
        dlp_file = None
        for candidate in dlp_candidates:
            if candidate.exists():
                dlp_file = candidate
                break
        
        if not dlp_file:
            self.log("ℹ️ 未找到 DLP 规则文件", "INFO")
            return 0
        
        # 确保目标目录存在
        self.defender_dlp.mkdir(exist_ok=True)
        dest = self.defender_dlp / "custom_rules.json"
        
        try:
            with open(dlp_file, 'r', encoding='utf-8') as f:
                new_rules = json.load(f)
            
            # 如果已有规则，合并
            if dest.exists():
                with open(dest, 'r', encoding='utf-8') as f:
                    existing_rules = json.load(f)
                
                # 基于 ID 去重
                existing_ids = {rule.get('id') for rule in existing_rules if isinstance(rule, dict)}
                merged = existing_rules.copy()
                
                for rule in new_rules:
                    if isinstance(rule, dict) and rule.get('id') not in existing_ids:
                        merged.append(rule)
                        self.log(f"✅ 添加 DLP 规则：{rule.get('id')}")
                
                # 保存合并后的规则
                with open(dest, 'w', encoding='utf-8') as f:
                    json.dump(merged, f, indent=2, ensure_ascii=False)
                
                self.stats["dlp_synced"] = len(new_rules)
                return len(new_rules)
            else:
                # 直接保存
                with open(dest, 'w', encoding='utf-8') as f:
                    json.dump(new_rules, f, indent=2, ensure_ascii=False)
                
                self.log(f"✅ 创建 DLP 规则文件：{dest.name}")
                self.stats["dlp_synced"] = len(new_rules)
                return len(new_rules)
                
        except Exception as e:
            self.log(f"❌ DLP 规则同步失败：{e}", "ERROR")
            self.stats["errors"].append(f"DLP: {str(e)}")
            return 0
    
    def sync_runtime_rules(self) -> int:
        """同步 Runtime 监控规则"""
        self.log("⚡ 开始同步 Runtime 规则...")
        
        # 查找 Runtime 规则文件
        runtime_candidates = [
            self.scanner_output / "runtime_rules.py",
            self.scanner_base / "runtime" / "custom_rules.py"
        ]
        
        runtime_file = None
        for candidate in runtime_candidates:
            if candidate.exists():
                runtime_file = candidate
                break
        
        if not runtime_file:
            self.log("ℹ️ 未找到 Runtime 规则文件", "INFO")
            return 0
        
        # 确保目标目录存在
        self.defender_runtime.mkdir(exist_ok=True)
        dest = self.defender_runtime / "custom_rules.py"
        
        try:
            shutil.copy2(runtime_file, dest)
            self.log(f"✅ 同步 Runtime 规则：{dest.name}")
            self.stats["runtime_synced"] = 1
            return 1
        except Exception as e:
            self.log(f"❌ Runtime 规则同步失败：{e}", "ERROR")
            self.stats["errors"].append(f"Runtime: {str(e)}")
            return 0
    
    def update_skill_md(self):
        """更新 SKILL.md 文档"""
        self.log("📝 更新 SKILL.md...")
        
        skill_file = self.agent_defender / "SKILL.md"
        
        if not skill_file.exists():
            self.log("⚠️ 未找到 SKILL.md", "WARN")
            return False
        
        try:
            # 统计规则总数
            total_rules = 0
            if self.defender_rules.exists():
                for rule_file in self.defender_rules.glob("*.json"):
                    try:
                        with open(rule_file, 'r', encoding='utf-8') as f:
                            rules = json.load(f)
                            if isinstance(rules, list):
                                total_rules += len(rules)
                            else:
                                total_rules += 1
                    except:
                        pass
            
            content = skill_file.read_text(encoding='utf-8')
            
            # 更新规则数量
            import re
            updated_content = re.sub(
                r'\*\*检测规则数量\*\*: \d+',
                f"**检测规则数量**: {total_rules}",
                content
            )
            
            if updated_content != content:
                skill_file.write_text(updated_content, encoding='utf-8')
                self.log(f"✅ 更新 SKILL.md: 规则数 → {total_rules}")
                return True
            else:
                self.log("ℹ️ SKILL.md 无需更新")
                return False
                
        except Exception as e:
            self.log(f"❌ 更新 SKILL.md 失败：{e}", "ERROR")
            self.stats["errors"].append(f"SKILL.md: {str(e)}")
            return False
    
    def generate_integration_report(self, backup_path: str) -> str:
        """生成集成报告"""
        self.log("📊 生成集成报告...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取 scanner 版本信息
        scanner_version = "v4.1.0"
        try:
            import subprocess
            result = subprocess.run(
                ["git", "describe", "--tags", "--always"],
                cwd=self.scanner_base,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                scanner_version = result.stdout.strip()
        except:
            pass
        
        report = f"""# 🔄 agent-defender 集成报告

**集成时间**: {timestamp}  
**来源**: agent-security-skill-scanner ({scanner_version})  
**备份位置**: {backup_path or '无'}

---

## 📊 集成统计

| 模块 | 同步数量 | 状态 |
|------|----------|------|
| 检测规则 | {self.stats['rules_synced']} 条 | {'✅' if self.stats['rules_synced'] > 0 else 'ℹ️'} |
| DLP 规则 | {self.stats['dlp_synced']} 条 | {'✅' if self.stats['dlp_synced'] > 0 else 'ℹ️'} |
| Runtime 规则 | {self.stats['runtime_synced']} 条 | {'✅' if self.stats['runtime_synced'] > 0 else 'ℹ️'} |
| 备份创建 | {'是' if self.stats['backup_created'] else '否'} | {'✅' if self.stats['backup_created'] else 'ℹ️'} |

---

## 📝 变更日志

"""
        
        for log_entry in self.sync_log:
            report += f"- {log_entry}\n"
        
        if self.stats["errors"]:
            report += f"\n## ⚠️ 错误\n\n"
            for error in self.stats["errors"]:
                report += f"- {error}\n"
        
        report += f"""
---

## ✅ 集成完成

**总同步规则数**: {self.stats['rules_synced'] + self.stats['dlp_synced'] + self.stats['runtime_synced']} 条

### 下一步

1. 验证规则：`python3 test_integrated_rules.py`
2. 启动守护进程：`./defenderctl.sh start`
3. 查看状态：`./defenderctl.sh status`

---

**集成版本**: v4.1.0  
**创建时间**: {timestamp}
"""
        
        # 保存报告
        reports_dir = self.agent_defender / "sync_reports"
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        return str(report_file)
    
    def run_integration(self):
        """执行完整集成"""
        print("=" * 70)
        print("🔄 agent-security-skill-scanner v4.1.0 → agent-defender 集成")
        print("=" * 70)
        print()
        
        # 步骤 1: 备份
        print("📦 步骤 1: 备份当前规则...")
        backup_path = self.backup_current_rules()
        print()
        
        # 步骤 2: 同步检测规则
        print("📋 步骤 2: 同步检测规则 (optimized_rules)...")
        self.sync_optimized_rules()
        print()
        
        # 步骤 3: 同步 DLP 规则
        print("🛡️  步骤 3: 同步 DLP 规则...")
        self.sync_dlp_rules()
        print()
        
        # 步骤 4: 同步 Runtime 规则
        print("⚡ 步骤 4: 同步 Runtime 规则...")
        self.sync_runtime_rules()
        print()
        
        # 步骤 5: 更新文档
        print("📝 步骤 5: 更新 SKILL.md...")
        self.update_skill_md()
        print()
        
        # 步骤 6: 生成报告
        print("📊 步骤 6: 生成集成报告...")
        report_file = self.generate_integration_report(backup_path)
        print(f"✅ 报告已保存：{report_file}")
        print()
        
        print("=" * 70)
        total = self.stats['rules_synced'] + self.stats['dlp_synced'] + self.stats['runtime_synced']
        print(f"✅ 集成完成！总同步规则数：{total}")
        print("=" * 70)
        
        if self.stats["errors"]:
            print(f"\n⚠️  发生 {len(self.stats['errors'])} 个错误，请查看日志")
            return 1
        return 0


def main():
    integrator = ScannerToIntegrator()
    exit_code = integrator.run_integration()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
