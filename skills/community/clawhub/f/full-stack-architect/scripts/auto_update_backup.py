#!/usr/bin/env python3
"""
全栈架构导师自动更新和备份脚本

功能：
1. 运行知识整理脚本，更新知识库索引
2. 创建压缩包备份
3. 保存到工作区根目录
4. 记录备份日志

使用方法：
- 手动运行：python auto_update_backup.py
- 定时运行：设置cron任务或系统定时任务
"""

import os
import sys
import subprocess
import datetime
import logging

# 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = BASE_DIR
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
UPDATE_DIR = os.path.join(ROOT_DIR, '更新')
ARCHITECT_DIR = os.path.join(UPDATE_DIR, '全栈架构师')

# 确保目录存在
os.makedirs(ARCHITECT_DIR, exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(ARCHITECT_DIR, 'update_backup.log')),
        logging.StreamHandler()
    ]
)

def run_command(command, cwd=None):
    """运行命令并返回结果"""
    logging.info(f"执行命令: {command}")
    try:
        # 使用shell=True时，命令会被正确处理，包括包含空格的路径
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        logging.info(f"命令执行成功: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"命令执行失败: {e.stderr.strip()}")
        return False

def update_knowledge_base():
    """更新知识库"""
    logging.info("开始更新知识库...")
    script_path = os.path.join(SKILL_DIR, 'scripts', 'knowledge_organizer.py')
    if os.path.exists(script_path):
        # 直接在 scripts 目录中运行，避免路径问题
        return run_command('python3 knowledge_organizer.py', cwd=os.path.join(SKILL_DIR, 'scripts'))
    else:
        logging.error(f"知识整理脚本不存在: {script_path}")
        return False

def create_backup():
    """创建备份压缩包"""
    logging.info("开始创建备份...")
    
    # 生成备份文件名
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'full-stack-architect-backup_{timestamp}.tar.gz'
    backup_path = os.path.join(ARCHITECT_DIR, backup_filename)
    
    # 确保路径中的空格被正确处理
    backup_path_escaped = backup_path.replace(' ', '\\ ')
    
    # 创建压缩包
    command = f'tar -czf {backup_path_escaped} full-stack-architect'
    if run_command(command, cwd=os.path.join(BASE_DIR, '..')):
        logging.info(f"备份成功创建: {backup_path}")
        return backup_path
    else:
        logging.error("备份创建失败")
        return None

def main():
    """主函数"""
    logging.info("===== 全栈架构导师自动更新和备份 ====")
    
    # 更新知识库
    if update_knowledge_base():
        # 创建备份
        backup_path = create_backup()
        if backup_path:
            logging.info(f"更新和备份完成！备份文件: {backup_path}")
        else:
            logging.error("备份失败")
    else:
        logging.error("知识库更新失败")
    
    logging.info("===== 任务完成 =====")

if __name__ == "__main__":
    main()
