#!/usr/bin/env python3
"""
Boss Auto Greet Script
从 config/filter-rules.json 读取过滤规则，搜索 Java 相关职位，过滤后打招呼
"""

import json
import subprocess
import time
import os
from datetime import date

# ========== 路径配置 ==========
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(WORKSPACE, "config", "filter-rules.json")
LOG_FILE = os.path.join(WORKSPACE, "logs", "boss_greet.log")
TRACK_FILE = os.path.join(WORKSPACE, "logs", "greeted_ids.txt")
TODAY_MARKER = os.path.join(WORKSPACE, "logs", f"greeted_{date.today().isoformat()}.txt")

BOSS_CMD = os.path.expanduser("~/.local/bin/boss")
BOSS_LOGIN_CMD = BOSS_CMD + " login --cookie-source chrome"

# ========== 加载配置 ==========
def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    return cfg

cfg = load_config()

COMPANY_BLACK = set(cfg["company_blacklist"])
JOB_BLACK = set(cfg["job_blacklist"])
KEYWORDS = cfg["search_keywords"]
CITY_PRIORITY = cfg["city_priority"]
MAX_GREET = cfg.get("max_greets_per_day", 50)
SLEEP_BETWEEN_GREET = 1  # 逐个排队，间隔1秒
SLEEP_BETWEEN_SEARCH = 2

# ========== 工具函数 ==========

def log(msg):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def run_boss(args, _retry_login=True):
    """调用 boss 命令，返回 JSON；认证失败时自动尝试 chrome cookie 登录"""
    cmd = [BOSS_CMD] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": result.stdout or result.stderr}

    if not data.get("ok") and ("环境异常" in json.dumps(data) or "登录" in json.dumps(data)):
        log(f"认证过期，尝试 chrome cookie 登录...")
        subprocess.run(BOSS_LOGIN_CMD.split(), capture_output=True, timeout=60)
        if _retry_login:
            return run_boss(args, _retry_login=False)
    return data

def is_already_greeted(sid):
    """检查是否已打过招呼"""
    if os.path.exists(TODAY_MARKER):
        with open(TODAY_MARKER, 'r', encoding='utf-8') as f:
            if sid in f.read().splitlines():
                return True
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, 'r', encoding='utf-8') as f:
            if sid in f.read().splitlines():
                return True
    return False

def mark_greeted(sid):
    """标记为已打招呼"""
    for f in [TRACK_FILE, TODAY_MARKER]:
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, 'a', encoding='utf-8') as fh:
            fh.write(sid + '\n')

def greet(sid, name, brand):
    """单次打招呼"""
    result = run_boss(["greet", sid])
    if result.get("ok"):
        log(f"✅ {name} @ {brand}")
        return True
    else:
        err = json.dumps(result, ensure_ascii=False)
        if "频繁" in err or "限速" in err:
            log(f"⚠️ 限速，等待35秒...")
            time.sleep(35)
            result = run_boss(["greet", sid])
            if result.get("ok"):
                log(f"✅ {name} @ {brand} (重试成功)")
                return True
        log(f"❌ {name} @ {brand}: {str(err)[:100]}")
        return False

def filter_job(brand, job_name, skills_text):
    """过滤黑名单职位"""
    text = (brand + job_name + skills_text).lower()
    for kw in COMPANY_BLACK:
        if kw.lower() in text:
            return False, f"公司黑名单: {kw}"
    for kw in JOB_BLACK:
        if kw.lower() in text:
            return False, f"职位黑名单: {kw}"
    return True, "ok"

def search_and_collect(keyword, city):
    """搜索并收集符合条件的职位"""
    log(f"搜索: {keyword} @ {city}")
    result = run_boss(["search", keyword, "--city", city])
    if not result.get("ok"):
        err_msg = result.get('error', 'unknown')
        if isinstance(err_msg, str):
            err_msg = err_msg[:80]
        else:
            err_msg = str(err_msg)[:80]
        log(f"搜索失败: {err_msg}")
        return []

    jobs = result.get("data", {}).get("jobList", []) or []
    collected = []
    for j in jobs:
        sid = j.get("securityId", "")
        brand = j.get("brandName", "") or ""
        job_name = j.get("jobName", "") or ""
        salary = j.get("salaryDesc", "") or ""
        skills = " ".join(j.get("skills", []) or [])
        job_exp = j.get("jobExperience", "") or ""

        if not sid:
            continue

        ok, reason = filter_job(brand, job_name, skills)
        if not ok:
            continue

        if is_already_greeted(sid):
            continue

        collected.append({
            "sid": sid,
            "name": job_name,
            "brand": brand,
            "salary": salary,
            "exp": job_exp,
            "skills": skills,
            "city": city,
        })
        log(f"  📋 {job_name} @ {brand} ({salary}, {job_exp})")

    return collected

# ========== 主流程 ==========

def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(TRACK_FILE), exist_ok=True)

    log("==== 开始批量打招呼任务 (配置驱动) ====")

    # 先登录
    log("登录...")
    subprocess.run(BOSS_LOGIN_CMD.split(), capture_output=True, timeout=30)

    # 按城市优先级搜索
    all_jobs = {}

    for city in CITY_PRIORITY:
        for kw in KEYWORDS:
            jobs = search_and_collect(kw, city)
            for j in jobs:
                if j["sid"] not in all_jobs:
                    all_jobs[j["sid"]] = j
            time.sleep(SLEEP_BETWEEN_SEARCH)

    count = len(all_jobs)
    log(f"共找到 {count} 个未打招呼的合格职位")

    if count == 0:
        log("无新职位，任务结束")
        return

    # 按城市优先级排序打招呼
    city_rank = {c: i for i, c in enumerate(CITY_PRIORITY)}
    sorted_jobs = sorted(all_jobs.items(), key=lambda x: city_rank.get(x[1]["city"], 99))

    greeted = 0
    for i, (sid, job) in enumerate(sorted_jobs):
        if greeted >= MAX_GREET:
            log(f"已达到每日上限 {MAX_GREET} 个，停止")
            break
        log(f"[{greeted+1}/{MAX_GREET}] 打招呼: {job['name']} @ {job['brand']} [{job['city']}]")
        ok = greet(sid, job["name"], job["brand"])
        if ok:
            mark_greeted(sid)
            greeted += 1
        time.sleep(SLEEP_BETWEEN_GREET)

    log(f"本次打招呼 {greeted} 个")
    log("=== 任务完成 ===")

if __name__ == "__main__":
    main()
