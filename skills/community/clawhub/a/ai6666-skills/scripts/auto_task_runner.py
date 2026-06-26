#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666 自动任务 runner - 配合 cron 使用
每30分钟运行，检查并完成所有新任务

功能：
1. 每日打卡任务 708（每天只做一次）
2. 通知消息接口获取最新红包任务
3. 红包任务列表获取所有红包任务
4. 已完成任务不重复做
"""

import sys
import os
import json
import time
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai6666_skill import AI6666Skill
import ai6666_config as config


def load_completed():
    """加载已完成任务记录"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "completed_tasks.json")
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def load_task_log():
    """加载任务执行日志（供进化系统使用）"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_log.json")
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_task_log(log):
    """保存任务执行日志"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_log.json")
    with open(path, 'w') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def log_task_result(task_id, task_title, task_type, success, message=""):
    """记录单条任务执行结果到日志"""
    log = load_task_log()
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in log:
        log[today] = []
    log[today].append({
        "task_id": task_id,
        "title": task_title[:60] if task_title else "",
        "type": task_type,
        "success": success,
        "message": message,
        "time": datetime.now().isoformat(),
    })
    save_task_log(log)


def save_completed(data):
    """保存已完成任务记录"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "completed_tasks.json")
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_task_titles():
    """加载任务标题记录"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_titles.json")
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_task_title(task_id, title):
    """保存任务标题（方便日志追溯）"""
    titles = load_task_titles()
    titles[str(task_id)] = title
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_titles.json")
    with open(path, 'w') as f:
        json.dump(titles, f, ensure_ascii=False, indent=2)


def is_completed_today(completed, task_id):
    """检查任务是否今天已完成"""
    today = date.today().isoformat()
    if task_id in completed:
        val = completed[task_id]
        if isinstance(val, str) and val.startswith(today):
            return True
        if val == today:
            return True
    return False


def run_daily_checkin(skill, completed):
    """处理每日打卡任务 708"""
    task_id = "708"
    today = date.today().isoformat()
    
    if task_id in completed and completed[task_id] == today:
        print(f"  [跳过] 打卡任务 {task_id} 今日已完成")
        return completed, False
    
    print(f"  [处理] 每日打卡任务 {task_id}...")
    try:
        from auto_poster import AutoPoster
        poster = AutoPoster()
        result = poster.post_once()
        if result.get('success'):
            completed[task_id] = today
            print(f"  [成功] 打卡任务完成")
            return completed, True
        else:
            print(f"  [失败] 发帖未成功")
            return completed, False
    except Exception as e:
        print(f"  [异常] {e}")
        return completed, False


def run_notification_tasks(skill, completed, section, label):
    """从通知消息接口获取任务并完成（通用）"""
    print(f"  [获取] {label}通知任务...")
    tasks = skill.get_notifications(section)
    new_count = 0
    
    for t in tasks:
        tid = t.get("id", "")
        if not tid:
            continue
        if tid in completed:
            print(f"  [跳过] {tid} 已完成")
            continue
        
        title = t.get("title", "")[:60]
        print(f"  [处理] 任务 {tid}: {title}")
        save_task_title(tid, title)
        
        # 获取任务详情
        detail = skill.get_task_detail(tid)
        desc = detail.get("description", "")
        task_title = detail.get("title", "")
        save_task_title(tid, task_title[:60] if task_title else title)
        
        # 生成答案
        answer = skill._generate_task_answer(task_title, desc)
        if not answer:
            print(f"  [跳过] 任务 {tid} 需要外部操作")
            completed[tid] = datetime.now().isoformat()
            save_completed(completed)
            log_task_result(tid, title, section, False, "需要外部操作")
            time.sleep(2)  # 跳过时也稍作停顿
            continue
        
        # 提交答案
        result = skill.submit_task_answer(tid, answer)
        if result.get("success"):
            completed[tid] = datetime.now().isoformat()
            new_count += 1
            print(f"  [成功] 任务 {tid} 完成")
            log_task_result(tid, title, section, True, "答案提交成功")
        else:
            msg = result.get('message', '')
            print(f"  [失败] {msg}")
            log_task_result(tid, title, section, False, msg)
        
        save_completed(completed)
        time.sleep(3)  # 提交后等3秒，避免频率过高触发反爬
    
    return completed, new_count


def run_redpacket_notification_tasks(skill, completed):
    """从通知消息接口获取红包任务并完成"""
    return run_notification_tasks(skill, completed, "redpacket", "红包")


def run_list_tasks(skill, completed, bounty, label):
    """从任务列表获取任务并完成（通用）"""
    print(f"  [获取] {label}任务列表...")
    try:
        tasks = skill.get_tasks(bounty=bounty)
    except Exception as e:
        print(f"  [异常] 获取{label}任务列表失败: {e}")
        return completed, 0
    
    new_count = 0
    for t in tasks:
        tid = t.get("id", "")
        if not tid or tid in completed:
            continue
        
        title = t.get("title", "")[:60]
        print(f"  [处理] 任务 {tid}: {title}")
        save_task_title(tid, title)
        
        # 获取详情
        detail = skill.get_task_detail(tid)
        desc = detail.get("description", "")
        task_title = detail.get("title", "")
        save_task_title(tid, task_title[:60] if task_title else title)
        
        # 生成答案
        answer = skill._generate_task_answer(task_title, desc)
        if not answer:
            print(f"  [跳过] 任务 {tid} 需要外部操作")
            completed[tid] = datetime.now().isoformat()
            save_completed(completed)
            log_task_result(tid, title, bounty, False, "需要外部操作")
            time.sleep(2)  # 跳过时也稍作停顿
            continue
        
        # 提交
        result = skill.submit_task_answer(tid, answer)
        if result.get("success"):
            completed[tid] = datetime.now().isoformat()
            new_count += 1
            print(f"  [成功] 任务 {tid} 完成")
            log_task_result(tid, title, bounty, True, "答案提交成功")
        else:
            msg = result.get('message', '')
            print(f"  [失败] {msg}")
            log_task_result(tid, title, bounty, False, msg)
        
        save_completed(completed)
        time.sleep(3)  # 提交后等3秒，避免频率过高触发反爬
    
    return completed, new_count


def run_redpacket_list_tasks(skill, completed):
    """从红包任务列表获取任务并完成"""
    return run_list_tasks(skill, completed, "redpacket", "红包")


def main():
    print(f"\n{'='*60}")
    print(f"AI6666 自动任务 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)
    
    # 加载已完成记录
    completed = load_completed()
    print(f"已加载 {len(completed)} 条已完成记录")
    
    # 初始化
    skill = AI6666Skill(
        username=config.USERNAME,
        password=config.PASSWORD
    )
    
    if not skill.is_logged_in():
        print("[错误] 登录失败，退出")
        return
    
    total_new = 0
    
    # 1. 每日打卡
    completed, ok = run_daily_checkin(skill, completed)
    if ok:
        total_new += 1
    save_completed(completed)
    
    # 2. 红包通知任务
    completed, cnt = run_redpacket_notification_tasks(skill, completed)
    total_new += cnt
    
    # 3. 红包任务列表
    completed, cnt = run_redpacket_list_tasks(skill, completed)
    total_new += cnt
    
    # 4. Nothing 积分任务（通知接口）
    completed, cnt = run_notification_tasks(skill, completed, "nothing", "Nothing积分")
    total_new += cnt
    
    # 5. Nothing 积分任务（列表接口）
    completed, cnt = run_list_tasks(skill, completed, "nothing", "Nothing积分")
    total_new += cnt
    
    # 6. 普通任务（通知接口）
    completed, cnt = run_notification_tasks(skill, completed, "task", "普通")
    total_new += cnt
    
    # 最终保存
    save_completed(completed)
    
    # 报告
    balance = skill.get_balance()
    print(f"\n{'='*60}")
    print(f"执行完成")
    print(f"  本次新增: {total_new} 个")
    print(f"  累计完成: {len(completed)} 个")
    print(f"  RMB余额: {balance.get('rmb', 0)}")
    print(f"  Nothing: {balance.get('nothing', 0)}")
    print('='*60)
    
    # 进化分析（每次任务执行后自动触发）
    print(f"\n[进化] 运行技能进化分析...")
    try:
        import subprocess
        result = subprocess.run(
            ["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "auto_evolution.py")],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"  进化分析完成")
        else:
            print(f"  进化分析异常: {result.stderr[:100]}")
    except Exception as e:
        print(f"  进化分析跳过: {e}")


if __name__ == "__main__":
    main()
