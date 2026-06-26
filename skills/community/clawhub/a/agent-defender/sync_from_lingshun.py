#!/usr/bin/env python3
"""
🔄 灵顺 V5 → agent-defender 持续集成脚本
=========================================
功能：
- 自动同步检测规则
- 更新 DLP 规则
- 更新 Runtime 监控规则
- 生成变更报告
- 备份旧规则
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class DefenderIntegrator:
    """agent-defender 集成器"""
    
    def __init__(self):
        self.expert_mode = Path(__file__).parent.parent / "agent-security-skill-scanner" / "expert_mode"
        self.agent_defender = Path(__file__).parent
        self.backup_dir = self.agent_defender / "rules_backup"
        self.sync_log = []
    
    def backup_current_rules(self) -> str:
        """备份当前规则"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        
        rules_dir = self.agent_defender / "rules"
        if rules_dir.exists():
            shutil.copytree(rules_dir, backup_path)
            self.log(f"✅ 备份规则到：{backup_path}")
            return str(backup_path)
        else:
            self.log("ℹ️ 无规则需要备份")
            return None
    
    def sync_detection_rules(self) -> int:
        """同步检测规则"""
        optimized_rules = self.expert_mode / "optimized_rules"
        defender_rules = self.agent_defender / "rules"
        
        defender_rules.mkdir(exist_ok=True)
        
        synced_count = 0
        
        if optimized_rules.exists():
            for rule_file in optimized_rules.glob("*.json"):
                dest = defender_rules / rule_file.name
                
                # 检查是否需要更新
                if dest.exists():
                    old_content = dest.read_text()
                    new_content = rule_file.read_text()
                    
                    if old_content == new_content:
                        self.log(f"⏭️  跳过 (未变更): {rule_file.name}")
                        continue
                
                # 复制规则
                shutil.copy2(rule_file, dest)
                self.log(f"✅ 同步：{rule_file.name}")
                synced_count += 1
        else:
            self.log("⚠️ 未找到优化规则目录")
        
        return synced_count
    
    def sync_dlp_rules(self) -> int:
        """同步 DLP 规则"""
        dlp_rules_file = self.expert_mode / "output" / "dlp_rules.json"
        dlp_dir = self.agent_defender / "dlp"
        
        if not dlp_rules_file.exists():
            self.log("ℹ️ 无 DLP 规则文件")
            return 0
        
        dlp_dir.mkdir(exist_ok=True)
        dest = dlp_dir / "custom_rules.json"
        
        # 读取并合并规则
        with open(dlp_rules_file, 'r', encoding='utf-8') as f:
            new_rules = json.load(f)
        
        # 如果已有规则，合并
        if dest.exists():
            with open(dest, 'r', encoding='utf-8') as f:
                existing_rules = json.load(f)
            
            # 基于 ID 去重
            existing_ids = {rule['id'] for rule in existing_rules}
            for rule in new_rules:
                if rule['id'] not in existing_ids:
                    existing_rules.append(rule)
                    self.log(f"✅ 添加 DLP 规则：{rule['id']}")
            
            # 保存合并后的规则
            with open(dest, 'w', encoding='utf-8') as f:
                json.dump(existing_rules, f, indent=2, ensure_ascii=False)
            
            return len(new_rules)
        else:
            # 直接保存
            with open(dest, 'w', encoding='utf-8') as f:
                json.dump(new_rules, f, indent=2, ensure_ascii=False)
            
            self.log(f"✅ 创建 DLP 规则文件：{dest.name}")
            return len(new_rules)
    
    def sync_runtime_rules(self) -> int:
        """同步 Runtime 监控规则"""
        runtime_rules_file = self.expert_mode / "output" / "runtime_rules.py"
        runtime_dir = self.agent_defender / "runtime"
        
        if not runtime_rules_file.exists():
            self.log("ℹ️ 无 Runtime 规则文件")
            return 0
        
        runtime_dir.mkdir(exist_ok=True)
        dest = runtime_dir / "custom_rules.py"
        
        # 复制规则
        shutil.copy2(runtime_rules_file, dest)
        self.log(f"✅ 同步 Runtime 规则：{dest.name}")
        
        return 1
    
    def update_skill_md(self) -> bool:
        """更新 SKILL.md 文档"""
        skill_file = self.agent_defender / "SKILL.md"
        
        if not skill_file.exists():
            self.log("⚠️ 未找到 SKILL.md")
            return False
        
        content = skill_file.read_text(encoding='utf-8')
        
        # 更新规则数量
        rules_dir = self.agent_defender / "rules"
        total_rules = 0
        
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.json"):
                with open(rule_file, 'r', encoding='utf-8') as f:
                    rules = json.load(f)
                    total_rules += len(rules)
        
        # 查找并更新规则数量行
        old_line = f"- **检测规则数量**: \\d+"
        new_line = f"- **检测规则数量**: {total_rules}"
        
        import re
        updated_content = re.sub(
            r'\*\*检测规则数量\*\*: \d+',
            new_line,
            content
        )
        
        if updated_content != content:
            skill_file.write_text(updated_content, encoding='utf-8')
            self.log(f"✅ 更新 SKILL.md: 规则数 → {total_rules}")
            return True
        else:
            self.log("ℹ️ SKILL.md 无需更新")
            return False
    
    def generate_sync_report(self, synced_rules: int, synced_dlp: int, 
                            synced_runtime: int, backup_path: str) -> str:
        """生成同步报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 🔄 agent-defender 同步报告

**同步时间**: {timestamp}  
**备份位置**: {backup_path or '无'}

---

## 📊 同步统计

| 模块 | 同步数量 | 状态 |
|------|----------|------|
| 检测规则 | {synced_rules} 条 | {'✅' if synced_rules > 0 else 'ℹ️'} |
| DLP 规则 | {synced_dlp} 条 | {'✅' if synced_dlp > 0 else 'ℹ️'} |
| Runtime 规则 | {synced_runtime} 条 | {'✅' if synced_runtime > 0 else 'ℹ️'} |

---

## 📝 变更日志

"""
        
        for log_entry in self.sync_log:
            report += f"- {log_entry}\n"
        
        report += f"""
---

## ✅ 同步完成

**总同步规则数**: {synced_rules + synced_dlp + synced_runtime} 条

"""
        
        # 保存报告
        reports_dir = self.agent_defender / "sync_reports"
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        return str(report_file)
    
    def log(self, message: str):
        """记录日志"""
        self.sync_log.append(message)
        print(message)
    
    def run_sync(self):
        """执行完整同步"""
        print("=" * 60)
        print("🔄 灵顺 V5 → agent-defender 同步")
        print("=" * 60)
        print()
        
        # 步骤 1: 备份
        print("📦 步骤 1: 备份当前规则...")
        backup_path = self.backup_current_rules()
        print()
        
        # 步骤 2: 同步检测规则
        print("📋 步骤 2: 同步检测规则...")
        synced_rules = self.sync_detection_rules()
        print()
        
        # 步骤 3: 同步 DLP 规则
        print("🛡️  步骤 3: 同步 DLP 规则...")
        synced_dlp = self.sync_dlp_rules()
        print()
        
        # 步骤 4: 同步 Runtime 规则
        print("⚡ 步骤 4: 同步 Runtime 规则...")
        synced_runtime = self.sync_runtime_rules()
        print()
        
        # 步骤 5: 更新文档
        print("📝 步骤 5: 更新 SKILL.md...")
        self.update_skill_md()
        print()
        
        # 步骤 6: 生成报告
        print("📊 步骤 6: 生成同步报告...")
        report_file = self.generate_sync_report(
            synced_rules, synced_dlp, synced_runtime, backup_path
        )
        print(f"✅ 报告已保存：{report_file}")
        print()
        
        print("=" * 60)
        print(f"✅ 同步完成！总规则数：{synced_rules + synced_dlp + synced_runtime}")
        print("=" * 60)


def main():
    integrator = DefenderIntegrator()
    integrator.run_sync()


if __name__ == "__main__":
    main()
