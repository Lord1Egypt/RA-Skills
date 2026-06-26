#!/usr/bin/env python3
"""
持续学习套件 - 定时任务安装脚本（跨平台）

支持Windows/Linux/Mac
"""
import subprocess
import sys
import platform
from pathlib import Path

WORKSPACE = Path.cwd()
SYNC_SCRIPT = WORKSPACE / "skills/continuous-learning/sync/sync_notification.py"
DREAM_SCRIPT = WORKSPACE / "skills/continuous-learning/dream/dream_cycle.py"


def is_windows():
    """检测是否为Windows"""
    return platform.system() == 'Windows'


def get_existing_windows_tasks():
    """获取Windows现有任务"""
    try:
        result = subprocess.run(
            ['schtasks', '/query', '/fo', 'LIST', '/v'],
            capture_output=True,
            text=True,
            shell=True
        )
        return result.stdout if result.returncode == 0 else ''
    except:
        return ''


def install_windows_tasks():
    """安装Windows定时任务"""
    print("\n检测到Windows系统，将创建任务计划程序任务...")

    # 删除旧任务
    for task_name in ['OpenClaw-ContinuousSync', 'OpenClaw-ContinuousDream']:
        try:
            subprocess.run(
                ['schtasks', '/delete', '/tn', task_name, '/f'],
                capture_output=True,
                shell=True
            )
            print(f"  删除旧任务: {task_name}")
        except:
            pass

    # 创建新任务
    tasks = [
        {
            'name': 'OpenClaw-ContinuousSync',
            'script': str(SYNC_SCRIPT),
            'time': '23:00'
        },
        {
            'name': 'OpenClaw-ContinuousDream',
            'script': str(DREAM_SCRIPT),
            'time': '02:00'
        }
    ]

    success = True
    for task in tasks:
        try:
            result = subprocess.run(
                [
                    'schtasks', '/create',
                    '/tn', task['name'],
                    '/tr', f'python "{task["script"]}"',
                    '/sc', 'daily',
                    '/st', task['time'],
                    '/f'
                ],
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode == 0:
                print(f"  ✅ 创建任务: {task['name']} ({task['time']})")
            else:
                print(f"  ❌ 创建任务失败: {task['name']}")
                print(f"     错误: {result.stderr}")
                success = False
        except Exception as e:
            print(f"  ❌ 创建任务异常: {task['name']} - {e}")
            success = False

    return success


def get_cron_jobs():
    """获取现有cron任务（Linux/Mac）"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        return result.stdout.split('\n') if result.returncode == 0 else []
    except:
        return []


def install_cron_jobs():
    """安装cron任务（Linux/Mac）"""
    print("\n检测到Linux/Mac系统，将创建cron任务...")

    existing_jobs = get_cron_jobs()

    # 过滤掉我们的旧任务
    filtered_jobs = [
        job for job in existing_jobs
        if 'ContinuousSync' not in job and 'ContinuousDream' not in job
    ]

    # 添加新任务
    new_jobs = filtered_jobs.copy()

    sync_cron = f"0 23 * * * cd {WORKSPACE} && python {SYNC_SCRIPT} >> /tmp/openclaw_sync.log 2>&1"
    dream_cron = f"0 2 * * * cd {WORKSPACE} && python {DREAM_SCRIPT} >> /tmp/openclaw_dream.log 2>&1"

    new_jobs.append(sync_cron)
    new_jobs.append(dream_cron)

    # 写入crontab
    crontab_content = '\n'.join(new_jobs)

    process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
    process.communicate(input=crontab_content)

    return process.returncode == 0


def main():
    print("\n持续学习套件 - 定时任务安装")
    print("=" * 60)

    print("将添加以下定时任务：")
    print(f"  23:00 - 同步聊天 ({SYNC_SCRIPT})")
    print(f"  02:00 - 做梦分析 ({DREAM_SCRIPT})")
    print()

    # 检查操作系统
    if is_windows():
        print(f"检测到系统: {platform.system()} {platform.release()}")
        print()
        response = input("继续安装Windows任务计划程序任务？ [y/N]: ")
    else:
        print(f"检测到系统: {platform.system()} {platform.release()}")
        print()
        response = input("继续安装cron任务？ [y/N]: ")

    if response.lower() != 'y':
        print("已取消")
        sys.exit(0)

    # 安装任务
    if is_windows():
        success = install_windows_tasks()

        if success:
            print("\n✅ 任务计划程序任务安装成功！")
            print("\n查看任务：")
            print("  打开“任务计划程序”（taskschd.msc）")
            print("  查找任务名：OpenClaw-ContinuousSync, OpenClaw-ContinuousDream")
            print("\n查看状态：")
            print("  schtasks /query /tn \"OpenClaw-ContinuousSync\"")
        else:
            print("\n❌ 安装失败")
            print("\n提示：可能需要管理员权限")
            sys.exit(1)
    else:
        if install_cron_jobs():
            print("\n✅ cron任务安装成功！")
            print("\n查看任务：")
            print("  crontab -l")
            print("\n日志文件：")
            print("  /tmp/openclaw_sync.log")
            print("  /tmp/openclaw_dream.log")
        else:
            print("\n❌ 安装失败")
            sys.exit(1)


if __name__ == '__main__':
    main()
