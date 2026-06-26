# -*- coding: utf-8 -*-
"""
AutoClaw v1.0 - 自动化脚本工具箱
功能：健康检查 + 自动备份 + 进程守护
"""
import os
import sys
import shutil
import json
import subprocess
from datetime import datetime

class AutoClaw:
    def __init__(self, workspace_path):
        self.workspace = workspace_path
        self.backup_dir = os.path.join(workspace_path, 'backups')
        self.log_file = os.path.join(workspace_path, 'logs', 'autoclaw.log')
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # 配置
        self.config = {
            'max_backups': 10,  # 最多保留 10 个备份
            'check_interval': 30,  # 检查间隔 (分钟)
            'auto_restart': True,  # 自动重启进程
        }
        
        # 监控的进程
        self.monitored_processes = [
            {
                'name': 'OKX Trading',
                'script': 'quant-bot-v2/ai-multi-coin.js',
                'check_cmd': 'node',
                'start_cmd': 'node quant-bot-v2/ai-multi-coin.js'
            }
        ]
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # 同时输出到控制台
        print(log_entry.strip())
    
    def health_check(self):
        """健康检查"""
        self.log("=" * 50)
        self.log("AutoClaw 健康检查")
        self.log("=" * 50)
        
        results = {
            'config': self._check_file('config.json'),
            'lessons': self._check_file('docs/lessons-learned.md'),
            'okx_setup': self._check_file('docs/okx-setup.md'),
            'memory_db': self._check_file('memory_data/ai_memory.db'),
            'tasks_dir': self._check_dir('tasks'),
        }
        
        # 统计
        ok_count = sum(1 for v in results.values() if v)
        total = len(results)
        
        self.log(f"检查结果：{ok_count}/{total} 正常")
        
        if ok_count == total:
            self.log("[OK] 系统健康")
            return True
        else:
            self.log("[WARN] 部分文件缺失")
            return False
    
    def _check_file(self, relative_path):
        """检查文件是否存在"""
        path = os.path.join(self.workspace, relative_path)
        exists = os.path.exists(path)
        status = "[OK]" if exists else "[MISSING]"
        self.log(f"  {status} {relative_path}")
        return exists
    
    def _check_dir(self, relative_path):
        """检查目录是否存在"""
        path = os.path.join(self.workspace, relative_path)
        exists = os.path.exists(path) and os.path.isdir(path)
        status = "[OK]" if exists else "[MISSING]"
        self.log(f"  {status} {relative_path}/")
        return exists
    
    def auto_backup(self):
        """自动备份"""
        self.log("\n" + "=" * 50)
        self.log("AutoClaw 自动备份")
        self.log("=" * 50)
        
        # 生成备份文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        # 要备份的文件
        files_to_backup = [
            'config.json',
            'MEMORY.md',
            'docs/lessons-learned.md',
            'memory_data/ai_memory.db',
        ]
        
        # 执行备份
        backed_up = 0
        for file in files_to_backup:
            src = os.path.join(self.workspace, file)
            if os.path.exists(src):
                # 创建子目录
                dest_dir = os.path.join(backup_path, os.path.dirname(file))
                os.makedirs(dest_dir, exist_ok=True)
                
                # 复制文件
                shutil.copy2(src, os.path.join(backup_path, file))
                backed_up += 1
                self.log(f"  [OK] {file}")
            else:
                self.log(f"  [WARN] {file} (不存在)")
        
        # 清理旧备份
        self._cleanup_old_backups()
        
        self.log(f"\n[OK] 备份完成：{backed_up} 个文件")
        self.log(f"备份位置：{backup_path}")
        
        return backup_path
    
    def _cleanup_old_backups(self):
        """清理旧备份"""
        try:
            backups = sorted([
                os.path.join(self.backup_dir, d) 
                for d in os.listdir(self.backup_dir) 
                if d.startswith('backup_') and os.path.isdir(os.path.join(self.backup_dir, d))
            ])
            
            while len(backups) > self.config['max_backups']:
                oldest = backups.pop(0)
                shutil.rmtree(oldest)
                self.log(f"[CLEANUP] 删除旧备份：{oldest}")
        except Exception as e:
            self.log(f"[ERROR] 清理备份失败：{e}")
    
    def check_processes(self):
        """检查进程状态"""
        self.log("\n" + "=" * 50)
        self.log("进程守护检查")
        self.log("=" * 50)
        
        for proc in self.monitored_processes:
            self.log(f"检查：{proc['name']}")
            
            # 简化版：检查脚本文件是否存在
            script_path = os.path.join(self.workspace, proc['script'])
            if os.path.exists(script_path):
                self.log(f"  [OK] 脚本存在")
            else:
                self.log(f"  [MISSING] 脚本不存在")
        
        self.log("[OK] 进程检查完成")
    
    def run(self):
        """运行完整流程"""
        self.log("\n" + "=" * 50)
        self.log("AutoClaw v1.0 启动")
        self.log("=" * 50)
        
        try:
            # 健康检查
            health_ok = self.health_check()
            
            # 自动备份
            self.auto_backup()
            
            # 进程检查
            self.check_processes()
            
            self.log("\n" + "=" * 50)
            self.log("AutoClaw 运行完成")
            self.log("=" * 50)
            
            return health_ok
        except Exception as e:
            self.log(f"[ERROR] 运行失败：{e}")
            return False

if __name__ == '__main__':
    workspace = "C:\\Users\\Administrator\\.openclaw\\workspace"
    autoclaw = AutoClaw(workspace)
    autoclaw.run()
