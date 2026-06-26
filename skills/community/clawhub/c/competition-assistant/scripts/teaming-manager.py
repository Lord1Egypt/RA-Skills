#!/usr/bin/env python3
"""
组队需求管理脚本
用于管理跨会话持久化的组队需求
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "teaming-requests.json"


def ensure_data_file():
    """确保数据文件存在"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        initial_data = {
            "version": "1.0",
            "lastUpdated": datetime.now().isoformat(),
            "requests": []
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
    return DATA_FILE


def load_data() -> dict:
    """加载数据"""
    ensure_data_file()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data: dict):
    """保存数据"""
    data["lastUpdated"] = datetime.now().isoformat()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def mask_contact(contact: str) -> str:
    """遮蔽联系方式"""
    # 手机号
    if re.match(r'^1[3-9]\d{9}$', contact):
        return contact[:3] + '****' + contact[-4:]
    
    # QQ号
    if re.match(r'^\d{5,11}$', contact):
        if len(contact) <= 5:
            return contact[:2] + '***'
        return contact[:3] + '***' + contact[-2:]
    
    # 邮箱
    if '@' in contact:
        parts = contact.split('@')
        local = parts[0]
        domain = parts[1]
        if len(local) <= 2:
            masked_local = local + '***'
        else:
            masked_local = local[:2] + '***'
        return masked_local + '@' + domain
    
    # 微信号或其他
    if len(contact) <= 3:
        return contact[:1] + '***'
    if len(contact) <= 6:
        return contact[:2] + '***' + contact[-1:]
    return contact[:3] + '***' + contact[-3:]


def generate_id() -> str:
    """生成唯一ID"""
    import random
    import string
    chars = string.ascii_lowercase + string.digits
    return 'req_' + ''.join(random.choices(chars, k=8))


def add_request(
    user_id: str,
    user_name: str,
    competition_name: str,
    competition_category: str,
    role: str,
    skills: list,
    skills_needed: list,
    free_time: str,
    contact: str,
    team_current: int = 1,
    team_target: int = 3,
    deadline: str = None,
    notes: str = ""
) -> dict:
    """添加组队需求"""
    data = load_data()
    
    # 默认截止日期：报名截止前3天（这里简化为30天后）
    if not deadline:
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    request = {
        "id": generate_id(),
        "createdAt": datetime.now().isoformat(),
        "userId": user_id,
        "userName": user_name,
        "competition": {
            "name": competition_name,
            "category": competition_category or "其他"
        },
        "role": role,
        "skills": skills,
        "skillsNeeded": skills_needed,
        "freeTime": free_time,
        "contact": contact,
        "contactMasked": mask_contact(contact),
        "teamSize": {
            "current": team_current,
            "target": team_target
        },
        "deadline": deadline,
        "status": "active",
        "notes": notes
    }
    
    data["requests"].append(request)
    save_data(data)
    return request


def list_requests(status: str = "active", competition: str = None) -> list:
    """列出组队需求"""
    data = load_data()
    requests = data.get("requests", [])
    
    # 过滤状态
    if status:
        requests = [r for r in requests if r.get("status") == status]
    
    # 过滤比赛
    if competition:
        requests = [r for r in requests if competition in r.get("competition", {}).get("name", "")]
    
    # 过滤过期
    today = datetime.now().date()
    requests = [r for r in requests if datetime.strptime(r.get("deadline", "2099-12-31"), "%Y-%m-%d").date() >= today]
    
    return requests


def calculate_match_score(req1: dict, req2: dict) -> int:
    """计算两个需求的匹配分数"""
    score = 0
    
    # 比赛匹配（必须）
    if req1["competition"]["name"] != req2["competition"]["name"]:
        return 0
    score += 50
    
    # 技能互补
    skills1 = set(req1.get("skills", []))
    skills_needed1 = set(req1.get("skillsNeeded", []))
    skills2 = set(req2.get("skills", []))
    skills_needed2 = set(req2.get("skillsNeeded", []))
    
    # 我需要的 = 对方有的
    match1 = skills_needed1 & skills2
    # 对方需要的 = 我有的
    match2 = skills_needed2 & skills1
    
    skill_score = len(match1) * 10 + len(match2) * 10
    score += min(skill_score, 30)
    
    # 时间匹配（简化判断）
    if req1.get("freeTime") and req2.get("freeTime"):
        # 关键词匹配
        time_keywords = ["周末", "晚间", "下午", "上午", "全天"]
        time1 = req1.get("freeTime", "")
        time2 = req2.get("freeTime", "")
        common = sum(1 for kw in time_keywords if kw in time1 and kw in time2)
        if common >= 2:
            score += 20
        elif common >= 1:
            score += 10
    
    return score


def find_matches(user_id: str, competition: str = None, limit: int = 2) -> list:
    """为用户寻找匹配的队友"""
    data = load_data()
    requests = data.get("requests", [])
    
    # 找到用户自己的需求
    user_requests = [r for r in requests if r.get("userId") == user_id and r.get("status") == "active"]
    if not user_requests:
        return []
    
    user_req = user_requests[0]
    
    # 找其他人的需求
    other_requests = [r for r in requests if r.get("userId") != user_id and r.get("status") == "active"]
    
    # 计算匹配分数
    matches = []
    for other in other_requests:
        score = calculate_match_score(user_req, other)
        if score >= 30:
            matches.append({
                "request": other,
                "score": score
            })
    
    # 排序并返回前N个
    matches.sort(key=lambda x: (-x["score"], x["request"]["createdAt"]))
    return matches[:limit]


def update_status(request_id: str, status: str):
    """更新需求状态"""
    data = load_data()
    for req in data["requests"]:
        if req.get("id") == request_id:
            req["status"] = status
            save_data(data)
            return True
    return False


def delete_request(request_id: str):
    """删除需求"""
    data = load_data()
    data["requests"] = [r for r in data["requests"] if r.get("id") != request_id]
    save_data(data)


# CLI接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: teaming-manager.py <command> [args]")
        print("命令: add, list, match, update, delete")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        reqs = list_requests()
        print(json.dumps(reqs, ensure_ascii=False, indent=2))
    
    elif cmd == "match":
        if len(sys.argv) < 3:
            print("用法: teaming-manager.py match <user_id>")
            sys.exit(1)
        matches = find_matches(sys.argv[2])
        print(json.dumps(matches, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {cmd}")
