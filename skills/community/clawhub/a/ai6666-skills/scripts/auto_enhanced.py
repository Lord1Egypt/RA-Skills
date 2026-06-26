#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666 全自动任务 runner（增强版）- cron 调用
执行任务 + 记录执行数据供后续进化分析
每次执行后自动输出本次执行摘要和下一步优化建议（供 cron 报告用）
"""

import sys
import os
import json
import time
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ai6666_skill import AI6666Skill
import ai6666_config as config

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COMPLETED_FILE = os.path.join(SCRIPT_DIR, "completed_tasks.json")
COMMENTED_FILE = os.path.join(SCRIPT_DIR, "commented_posts.json")
TASK_LOG = os.path.join(SCRIPT_DIR, "task_log.json")
COMMENT_LOG = os.path.join(SCRIPT_DIR, "comment_log.json")


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            pass
    return default


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log_task_result(task_id, task_title, success, message=""):
    """记录任务执行结果"""
    log = load_json(TASK_LOG, {})
    today = date.today().isoformat()
    if today not in log:
        log[today] = []
    log[today].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "task_id": task_id,
        "title": task_title[:40],
        "success": success,
        "message": message
    })
    save_json(TASK_LOG, log)


def log_comment_result(post_id, image_type, success):
    """记录评论执行结果"""
    log = load_json(COMMENT_LOG, [])
    log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "post_id": post_id,
        "image_type": image_type,
        "success": success
    })
    # 只保留最近100条
    log = log[-100:]
    save_json(COMMENT_LOG, log)


def run_daily_checkin(skill):
    """每日打卡任务"""
    task_id = "708"
    today = date.today().isoformat()
    completed = load_json(COMPLETED_FILE, {})
    
    if completed.get(task_id) == today:
        return {"action": "skip", "reason": "今日已完成打卡"}
    
    try:
        from auto_poster import AutoPoster
        poster = AutoPoster()
        result = poster.post_once()
        if result.get("success"):
            completed[task_id] = today
            save_json(COMPLETED_FILE, completed)
            log_task_result(task_id, "每日打卡", True)
            return {"action": "success"}
        else:
            log_task_result(task_id, "每日打卡", False, str(result))
            return {"action": "failed", "reason": str(result)}
    except Exception as e:
        log_task_result(task_id, "每日打卡", False, str(e))
        return {"action": "error", "reason": str(e)}


def run_redpacket_tasks(skill):
    """红包任务"""
    completed = load_json(COMPLETED_FILE, {})
    new_done = 0
    
    # 从通知接口
    try:
        tasks = skill.get_notifications("redpacket")
        for t in tasks:
            tid = t.get("id", "")
            if tid in completed:
                continue
            title = t.get("title", "")[:60]
            detail = skill.get_task_detail(tid)
            desc = detail.get("description", "")
            task_title = detail.get("title", "")
            answer = skill._generate_task_answer(task_title, desc)
            if answer:
                r = skill.submit_task_answer(tid, answer)
                if r.get("success"):
                    completed[tid] = datetime.now().isoformat()
                    save_json(COMPLETED_FILE, completed)
                    new_done += 1
                    log_task_result(tid, title, True)
                else:
                    log_task_result(tid, title, False, r.get("message"))
            else:
                completed[tid] = datetime.now().isoformat()
                save_json(COMPLETED_FILE, completed)
    except Exception as e:
        print(f"  [异常] 通知任务: {e}")
    
    # 从任务列表
    try:
        tasks = skill.get_tasks(bounty="redpacket")
        for t in tasks:
            tid = t.get("id", "")
            if tid in completed:
                continue
            title = t.get("title", "")[:60]
            detail = skill.get_task_detail(tid)
            desc = detail.get("description", "")
            task_title = detail.get("title", "")
            answer = skill._generate_task_answer(task_title, desc)
            if answer:
                r = skill.submit_task_answer(tid, answer)
                if r.get("success"):
                    completed[tid] = datetime.now().isoformat()
                    save_json(COMPLETED_FILE, completed)
                    new_done += 1
                    log_task_result(tid, title, True)
                else:
                    log_task_result(tid, title, False, r.get("message"))
    except Exception as e:
        print(f"  [异常] 列表任务: {e}")
    
    return {"action": "done", "new": new_done}


def run_comments(skill):
    """评论任务"""
    from image_analyzer import ImageAnalyzer
    from auto_comment_runner import COMMENT_TEMPLATES, detect_image_type, generate_comment
    
    commented_list = load_json(COMMENTED_FILE, [])
    posts = skill.get_posts_for_commenting(pages=2)
    pending = [p for p in posts if p["post_id"] not in commented_list]
    
    new_done = 0
    analyzer = ImageAnalyzer()
    
    for post in pending[:5]:
        pid = post["post_id"]
        content = post["content"]
        image_url = post["images"][0] if post["images"] else ""
        
        try:
            analysis = analyzer.analyze_image(image_url)
            img_type = detect_image_type(image_url, analysis)
            # generate_comment(img_type, post_content, vision_result)
            # analysis 是 vision_result（AI图片理解结果）
            comment = generate_comment(img_type, "", analysis)
            r = skill.comment(pid, comment)
            if r.get("success"):
                commented_list.append(pid)
                save_json(COMMENTED_FILE, commented_list)
                new_done += 1
                log_comment_result(pid, img_type, True)
                print(f"    [{pid}] {img_type}: {comment[:30]}...")
            else:
                log_comment_result(pid, img_type, False)
        except Exception as e:
            log_comment_result(pid, "error", False)
            print(f"    [{pid}] 异常: {e}")
        
        time.sleep(8)
    
    return {"action": "done", "new": new_done}


def print_summary(parts):
    """打印执行摘要"""
    print(f"\n{'='*60}")
    print(f"执行完成 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)
    total_new = 0
    for name, result in parts:
        if result["action"] == "skip":
            print(f"  {name}: 跳过 ({result.get('reason', '')})")
        elif result["action"] == "success":
            print(f"  {name}: ✓成功")
            total_new += 1
        elif result["action"] == "done":
            print(f"  {name}: 完成 {result.get('new', 0)} 条")
            total_new += result.get("new", 0)
        elif result["action"] == "failed":
            print(f"  {name}: ✗失败 ({result.get('reason', '')})")
        elif result["action"] == "error":
            print(f"  {name}: ✗异常 ({result.get('reason', '')})")
    
    completed = load_json(COMPLETED_FILE, {})
    commented = load_json(COMMENTED_FILE, [])
    balance = skill.get_balance()
    print(f"\n累计: 完成任务 {len(completed)} 个, 评论 {len(commented)} 条")
    print(f"余额: RMB={balance.get('rmb', 0)}, Nothing={balance.get('nothing', 0)}")
    print('='*60)
    
    # 优化建议（自动生成）
    suggestions = []
    task_log = load_json(TASK_LOG, {})
    comment_log = load_json(COMMENT_LOG, [])
    
    if task_log:
        last_day = list(task_log.keys())[-1] if task_log else ""
        if last_day in task_log:
            day_tasks = task_log[last_day]
            failed = [t for t in day_tasks if not t.get("success")]
            if failed:
                suggestions.append(f"⚠️ 今日有 {len(failed)} 个任务失败，建议检查答案生成逻辑")
    
    if comment_log:
        recent = comment_log[-20:]
        beauty = [c for c in recent if c.get("image_type") == "beauty"]
        if len(beauty) < 3:
            suggestions.append("💡 美女帖子评论较少，建议优化图片识别，增加美女图发现率")
    
    if suggestions:
        print("\n📝 优化建议:")
        for s in suggestions:
            print(f"  {s}")
    print('='*60)


if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"AI6666 增强任务 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)
    
    skill = AI6666Skill(username=config.USERNAME, password=config.PASSWORD)
    if not skill.is_logged_in():
        print("[错误] 登录失败")
        sys.exit(1)
    
    parts = []
    
    # 1. 打卡
    print("\n[1] 每日打卡...")
    parts.append(("打卡任务", run_daily_checkin(skill)))
    
    # 2. 红包任务
    print("\n[2] 红包任务...")
    parts.append(("红包任务", run_redpacket_tasks(skill)))
    
    # 3. 评论
    print("\n[3] 评论...")
    parts.append(("评论", run_comments(skill)))
    
    print_summary(parts)
