#!/usr/bin/env python3
"""
安全实验改进闭环 - 安全可控的自我改进
设计原则：隔离实验 → 测试验证 → 人工审批 → 确认合并 → 自动回滚
绝对不直接改生产，必须用户批准才会生效
"""

import os
import sys
import shutil
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

EXPERIMENT_ROOT = "/app/working/memory/experiments/"
BACKUP_ROOT = "/app/working/memory/experiment-backups/"

class SafeExperiment:
    """安全实验管理器"""
    
    def __init__(self):
        os.makedirs(EXPERIMENT_ROOT, exist_ok=True)
        os.makedirs(BACKUP_ROOT, exist_ok=True)
    
    def create_experiment(self, experiment_name: str, description: str) -> str:
        """创建新实验，返回实验ID"""
        experiment_id = f"{datetime.now().strftime('%Y%m%d-%H%M')}-{experiment_name.replace(' ', '-')}"
        experiment_dir = os.path.join(EXPERIMENT_ROOT, experiment_id)
        os.makedirs(experiment_dir, exist_ok=True)
        
        # 创建实验信息文件
        info = {
            "id": experiment_id,
            "name": experiment_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "experimenting",
            "files_modified": [],
        }
        
        with open(os.path.join(experiment_dir, "experiment.json"), "w", encoding='utf-8') as f:
            json.dump(info, f, indent=2)
        
        print(f"✅ 创建实验成功: {experiment_id}")
        print(f"📁 实验目录: {experiment_dir}")
        return experiment_id
    
    def backup_original(self, file_path: str) -> str:
        """备份原文件到备份目录，返回备份路径"""
        if not os.path.exists(file_path):
            return ""
        
        # 创建备份
        rel_path = file_path.replace("/app/working/", "").replace("/", "_")
        backup_name = f"{datetime.now().strftime('%Y%m%d-%H%M')}_{rel_path}"
        backup_path = os.path.join(BACKUP_ROOT, backup_name)
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(file_path, backup_path)
        print(f"💾 已备份原文件: {file_path} → {backup_path}")
        return backup_path
    
    def add_experiment_file(self, experiment_id: str, target_path: str, new_content: str) -> bool:
        """添加修改文件到实验"""
        experiment_dir = os.path.join(EXPERIMENT_ROOT, experiment_id)
        if not os.path.exists(experiment_dir):
            print(f"❌ 实验不存在: {experiment_id}")
            return False
        
        # 备份原文件
        if os.path.exists(target_path):
            self.backup_original(target_path)
        
        # 保存实验版本
        rel_target = target_path.replace("/app/working/", "")
        experiment_file_path = os.path.join(experiment_dir, rel_target)
        os.makedirs(os.path.dirname(experiment_file_path), exist_ok=True)
        
        with open(experiment_file_path, "w", encoding='utf-8') as f:
            f.write(new_content)
        
        # 更新实验信息
        info_path = os.path.join(experiment_dir, "experiment.json")
        with open(info_path, "r", encoding='utf-8') as f:
            info = json.load(f)
        
        if rel_target not in info["files_modified"]:
            info["files_modified"].append(rel_target)
        
        with open(info_path, "w", encoding='utf-8') as f:
            json.dump(info, f, indent=2)
        
        print(f"✅ 已保存实验修改: {rel_target}")
        return True
    
    def diff_experiment(self, experiment_id: str) -> List[Dict]:
        """生成实验diff报告"""
        experiment_dir = os.path.join(EXPERIMENT_ROOT, experiment_id)
        info_path = os.path.join(experiment_dir, "experiment.json")
        
        with open(info_path, "r", encoding='utf-8') as f:
            info = json.load(f)
        
        diffs = []
        for rel_file in info["files_modified"]:
            target_path = os.path.join("/app/working", rel_file)
            experiment_path = os.path.join(experiment_dir, rel_file)
            
            if os.path.exists(target_path):
                with open(target_path, "r", encoding='utf-8') as f:
                    original = f.read()
                with open(experiment_path, "r", encoding='utf-8') as f:
                    modified = f.read()
                
                if original != modified:
                    lines_original = len(original.split('\n'))
                    lines_modified = len(modified.split('\n'))
                    diffs.append({
                        "file": rel_file,
                        "original_lines": lines_original,
                        "modified_lines": lines_modified,
                        "changed": True
                    })
                else:
                    diffs.append({
                        "file": rel_file,
                        "changed": False
                    })
            else:
                # 新增文件
                with open(experiment_path, "r", encoding='utf-8') as f:
                    modified = f.read()
                diffs.append({
                    "file": rel_file,
                    "original_lines": 0,
                    "modified_lines": len(modified.split('\n')),
                    "changed": True,
                    "new_file": True
                })
        
        return diffs
    
    def generate_report(self, experiment_id: str) -> str:
        """生成实验报告"""
        experiment_dir = os.path.join(EXPERIMENT_ROOT, experiment_id)
        info_path = os.path.join(experiment_dir, "experiment.json")
        
        with open(info_path, "r", encoding='utf-8') as f:
            info = json.load(f)
        
        diffs = self.diff_experiment(experiment_id)
        
        report = f"# 🧪 实验改进报告 - {info['name']} ({experiment_id})\n\n"
        report += f"**描述**: {info['description']}\n\n"
        report += f"**创建时间**: {info['created_at']}\n"
        report += f"**状态**: {info['status']}\n\n"
        
        report += "## 📝 修改文件\n\n"
        report += "| 文件 | 原行数 | 新行数 | 变更 |\n"
        report += "|------|--------|--------|------|\n"
        
        changed_count = 0
        for d in diffs:
            if not d["changed"]:
                continue
            changed_count += 1
            if d.get("new_file"):
                change_str = "✨ 新增"
            else:
                change_str = "✏️ 修改"
            report += f"| `{d['file']}` | {d['original_lines']} | {d['modified_lines']} | {change_str} |\n"
        
        report += f"\n**总计**: {changed_count} 个文件变更\n\n"
        report += "## 🔍 测试结果\n\n*(请在实验中测试后填写结果)*\n\n"
        report += "- [ ] 功能正常\n- [ ] 没有 regression\n- [ ] 性能提升\n\n"
        report += "## 🚀 审批\n\n"
        report += "- ⏳ 等待审批\n- 👉 批准请回复: **`批准合并实验 " + experiment_id + "`**\n"
        report += "- ❌ 不批准请回复: **`删除实验 " + experiment_id + "`**\n\n"
        report += "---\n*安全实验闭环，隔离测试，必须人工审批才会合并到生产*\n"
        
        return report
    
    def approve_and_merge(self, experiment_id: str) -> Tuple[bool, str]:
        """批准实验，合并到生产环境"""
        experiment_dir = os.path.join(EXPERIMENT_ROOT, experiment_id)
        info_path = os.path.join(experiment_dir, "experiment.json")
        
        if not os.path.exists(experiment_dir):
            return False, f"❌ 实验不存在: {experiment_id}"
        
        # 检查核心文件，要二次确认
        with open(info_path, "r", encoding='utf-8') as f:
            info = json.load(f)
        
        # 检查是否修改核心配置
        core_files = ["jobs.json", "config.json", "chats.json", "copaw_file_metadata.json", "MEMORY.md"]
        is_core_modified = any(cf in f for f in info["files_modified"] for cf in core_files)
        
        if is_core_modified:
            return False, f"⚠️ 实验修改了核心配置文件 {[f for f in info['files_modified'] if any(cf in f for cf in core_files)]}，需要二次手动确认才能合并"
        
        # 合并修改
        merged = []
        for rel_file in info["files_modified"]:
            experiment_path = os.path.join(experiment_dir, rel_file)
            target_path = os.path.join("/app/working", rel_file)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # 复制实验版本到生产
            shutil.copy2(experiment_path, target_path)
            merged.append(rel_file)
            print(f"✅ 已合并: {rel_file}")
        
        # 更新状态
        info["status"] = "merged"
        with open(info_path, "w", encoding='utf-8') as f:
            json.dump(info, f, indent=2)
        
        return True, f"✅ 合并完成，共合并 {len(merged)} 个文件"
    
    def delete_experiment(self, experiment_id: str) -> Tuple[bool, str]:
        """删除实验，不合并"""
        experiment_dir = os.path.join(EXPERIMENT_ROOT, experiment_id)
        
        if not os.path.exists(experiment_dir):
            return False, f"❌ 实验不存在: {experiment_id}"
        
        shutil.rmtree(experiment_dir)
        return True, f"✅ 实验已删除: {experiment_id}"
    
    def list_experiments(self) -> List[Dict]:
        """列出所有实验"""
        experiments = []
        for d in os.listdir(EXPERIMENT_ROOT):
            exp_dir = os.path.join(EXPERIMENT_ROOT, d)
            info_path = os.path.join(exp_dir, "experiment.json")
            if os.path.exists(info_path):
                with open(info_path, "r", encoding='utf-8') as f:
                    info = json.load(f)
                    experiments.append(info)
        
        return sorted(experiments, key=lambda x: x["created_at"], reverse=True)

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python safe-experiment.py list              - 列出所有实验")
        print("  python safe-experiment.py create <name> <desc>  - 创建新实验")
        print("  python safe-experiment.py approve <id>        - 批准合并实验")
        print("  python safe-experiment.py delete <id>         - 删除实验")
        sys.exit(1)
    
    cmd = sys.argv[1]
    exp = SafeExperiment()
    
    if cmd == "list":
        exps = exp.list_experiments()
        print("\n📋 所有实验:")
        for e in exps:
            print(f"  [{e['status']}] {e['id']} - {e['name']}")
        sys.exit(0)
    
    elif cmd == "create":
        if len(sys.argv) < 4:
            print("❌ 需要实验名称和描述")
            sys.exit(1)
        name = sys.argv[2]
        desc = " ".join(sys.argv[3:])
        exp.create_experiment(name, desc)
        sys.exit(0)
    
    elif cmd == "approve":
        if len(sys.argv) < 3:
            print("❌ 需要实验ID")
            sys.exit(1)
        exp_id = sys.argv[2]
        success, msg = exp.approve_and_merge(exp_id)
        print(msg)
        if not success:
            sys.exit(1)
        sys.exit(0)
    
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("❌ 需要实验ID")
            sys.exit(1)
        exp_id = sys.argv[2]
        success, msg = exp.delete_experiment(exp_id)
        print(msg)
        if not success:
            sys.exit(1)
        sys.exit(0)
    
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
