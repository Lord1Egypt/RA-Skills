#!/usr/bin/env python3
"""
memory_core — memory-skill 的核心实现
数据库路径：/home/node/.openclaw/workspace/my_memory_core/memory.db
（与 skill 目录分离，实现持久化）
"""

import sqlite3
import re
import os
import json
from datetime import datetime
from typing import Optional, List

DB_PATH = "/home/node/.openclaw/workspace/my_memory_core/memory.db"

# SQLite 连接超时（秒），防止并发写入时报 "database is locked"
_SQLITE_TIMEOUT = 10.0

# ---------------------------------------------------------------------------
# 数据库初始化
# ---------------------------------------------------------------------------

def init_db():
    with sqlite3.connect(DB_PATH, timeout=_SQLITE_TIMEOUT) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS conversation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_text TEXT NOT NULL, source TEXT DEFAULT '',
            logged_at TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS experiences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_intent TEXT NOT NULL,
            approach TEXT NOT NULL,
            key_insight TEXT NOT NULL,
            raw_log_id INTEGER,
            tags TEXT DEFAULT '[]',
            times_used INTEGER DEFAULT 0,
            times_triggered INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            last_accessed TEXT,
            FOREIGN KEY (raw_log_id) REFERENCES conversation_log(id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_tag TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            frequency INTEGER DEFAULT 1,
            last_seen TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS experience_tags (
            experience_id INTEGER, tag TEXT,
            PRIMARY KEY (experience_id, tag),
            FOREIGN KEY (experience_id) REFERENCES experiences(id))""")
        c.execute("CREATE INDEX IF NOT EXISTS idx_exp_intent ON experiences(task_intent)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_exp_approach ON experiences(approach)")
        conn.commit()
    return DB_PATH


# ---------------------------------------------------------------------------
# 经验提取引擎（纯规则）
# ---------------------------------------------------------------------------

INTENT_PATTERNS = [
    (r"(?:修复|解决|排查|debug|fix)[：:\s]*(?P<target>[^，。\n]{3,50})", "problem_fixing"),
    (r"(?:搭建|部署|安装|配置|deploy|install|configure)[：:\s]*(?P<target>[^，。\n]{3,50})", "setup_deploy"),
    (r"(?:研究|调研|搜索|调查|search|research)[：:\s]*(?P<target>[^，。\n]{3,50})", "research"),
    (r"(?:编写|写|创建|制作|build|write|create|make)[：:\s]*(?P<target>[^，。\n]{3,50})", "creation"),
    (r"(?:优化|改进|提升|improve|optimize|enhance)[：:\s]*(?P<target>[^，。\n]{3,50})", "optimization"),
    (r"(?:自动化|automat)[：:\s]*(?P<target>[^，。\n]{3,50})", "automation"),
    (r"(?:连接|访问|获取|fetch|connect|access)[：:\s]*(?P<target>[^，。\n]{3,50})", "data_access"),
]

OUTCOME_PATTERNS = [
    (r"成功|完成|ok|done|solved|fixed|resolved|works?|通了|✅", True),
    (r"失败|错误|error|fail|blocked|cannot|timeout|❌", False),
]

INSIGHT_HINTS = [
    (r"原来|实际上|其实|才发现|turns out|realized", "breakthrough"),
    (r"注意|提醒|关键|important|key|critical|must|教训", "caution"),
    (r"更好的|最优|最佳|better|best|optimal|改进", "improvement"),
    (r"没想到|意外|unexpected|surprising|surprise", "surprise"),
    (r"经验|教训|takeaway|learned|lesson|insight", "lesson"),
]

APPROACH_TAGS = {
    "api": "API 调用", "rest": "REST API", "curl": "HTTP 请求",
    "python": "Python 脚本", "sqlite": "SQLite 数据库", "json": "JSON 处理",
    "正则": "正则表达式", "regex": "正则表达式", "cron": "定时任务",
    "daemon": "守护进程", "webdav": "WebDAV", "网页抓取": "网页抓取",
    "搜索": "网络搜索", "fallback": "降级方案", "重试": "重试机制",
    "并发": "并发控制", "锁": "锁机制", "缓存": "缓存策略",
    "环境变量": "环境变量", "配置文件": "配置文件",
    "docker": "Docker", "容器": "容器", "linux": "Linux",
    "服务器": "服务器", "飞书": "飞书", "obsidian": "笔记",
    "github api": "GitHub API", "algolia": "Algolia API",
    "firebase": "Firebase API", "browser": "浏览器自动化",
    "bridge": "Docker 网络", "docker network": "Docker 网络",
    "子网": "网络规划", "subnet": "网络规划",
    "ping": "连通性测试", "iptables": "防火墙规则",
}


def extract_task_intent(text: str) -> str:
    for pattern, kind in INTENT_PATTERNS:
        m = re.search(pattern, text.lower())
        if m:
            target = m.group("target").strip()[:40]
            return f"[{kind}] {target}"
    clean = re.sub(r"[^\w\u4e00-\u9fff]", " ", text)
    return clean[:60].strip()


def extract_approach(text: str) -> str:
    found = set()
    for kw, label in APPROACH_TAGS.items():
        if kw.lower() in text.lower():
            found.add(label)
    return " + ".join(sorted(found)) if found else "常规方法"


def detect_outcome(text: str) -> Optional[bool]:
    for pattern, result in OUTCOME_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return result
    return None


def extract_key_insight(text: str) -> str:
    lines = text.split("\n")
    insights = []
    for line in lines:
        for pattern, _ in INSIGHT_HINTS:
            if re.search(pattern, line, re.IGNORECASE):
                clean = re.sub(r"^[\s\-\*›•]+", "", line).strip()
                if 10 < len(clean) < 200:
                    insights.append(clean)
    if insights:
        return max(insights, key=len)
    sol_lines = [l.strip() for l in lines if any(
        k in l.lower() for k in ["解决", "成功", "通了", "works", "solved", "fixed"]
    ) and 15 < len(l) < 150]
    if sol_lines:
        return max(sol_lines, key=len)
    if len(lines) > 2:
        return lines[len(lines)//2].strip()[:120]
    return text[:120]


def extract_tags(text: str) -> list:
    tag_set = set()
    text_lower = text.lower()
    for kw, label in APPROACH_TAGS.items():
        if kw.lower() in text_lower:
            tag_set.add(label)
    extra = {
        "网络": "网络", "docker": "Docker", "容器": "容器",
        "linux": "Linux", "服务器": "服务器", "飞书": "飞书",
        "obsidian": "笔记", "权限": "权限", "认证": "认证",
        "api": "API", "llm": "LLM", "ai": "AI",
        "github": "GitHub", "hacker news": "HN",
        "简报": "自动化", "skill": "Skill",
    }
    for kw, tag in extra.items():
        if kw in text_lower:
            tag_set.add(tag)
    return sorted(tag_set)


def extract_experience(raw_log: str, source: str = "") -> dict:
    return {
        "task_intent": extract_task_intent(raw_log),
        "approach": extract_approach(raw_log),
        "key_insight": extract_key_insight(raw_log),
        "outcome": detect_outcome(raw_log),
        "tags": extract_tags(raw_log),
        "raw_log": raw_log,
        "source": source,
        "logged_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ---------------------------------------------------------------------------
# 数据库操作
# ---------------------------------------------------------------------------

def store_experience(exp: dict) -> int:
    init_db()
    with sqlite3.connect(DB_PATH, timeout=_SQLITE_TIMEOUT) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO conversation_log (raw_text, source, logged_at) VALUES (?, ?, ?)",
                  (exp["raw_log"], exp["source"], exp["logged_at"]))
        log_id = c.lastrowid
        c.execute("""INSERT INTO experiences
            (task_intent, approach, key_insight, raw_log_id, tags,
             times_used, times_triggered, created_at, last_accessed)
            VALUES (?, ?, ?, ?, ?, 0, 0, ?, ?)""",
                  (exp["task_intent"], exp["approach"], exp["key_insight"],
                   log_id, json.dumps(exp["tags"], ensure_ascii=False),
                   exp["logged_at"], exp["logged_at"]))
        exp_id = c.lastrowid
        for tag in exp["tags"]:
            c.execute("INSERT OR IGNORE INTO experience_tags (experience_id, tag) VALUES (?, ?)",
                      (exp_id, tag))
            c.execute("""INSERT INTO patterns (pattern_tag, description, frequency, last_seen)
                VALUES (?, ?, 1, ?) ON CONFLICT(pattern_tag) DO UPDATE SET
                frequency = frequency + 1, last_seen = excluded.last_seen""",
                      (tag, f"标签 {tag} 相关经验", exp["logged_at"]))
        conn.commit()
        return exp_id


def recall(keyword: str = "", tags: list = None, limit: int = 5) -> List[dict]:
    init_db()
    # limit 默认 2，防止长经验撑爆上下文窗口；可根据需要调大
    with sqlite3.connect(DB_PATH, timeout=_SQLITE_TIMEOUT) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        query = "SELECT * FROM experiences WHERE 1=1"
        params = []
        if keyword:
            query += " AND (task_intent LIKE ? OR approach LIKE ? OR key_insight LIKE ?)"
            kw = f"%{keyword}%"
            params += [kw, kw, kw]
        if tags:
            placeholders = ",".join("?" * len(tags))
            query += f" AND id IN (SELECT experience_id FROM experience_tags WHERE tag IN ({placeholders}))"
            params += tags
        query += " ORDER BY times_triggered DESC, created_at DESC LIMIT ?"
        params.append(limit)
        c.execute(query, params)
        rows = c.fetchall()
        results = []
        for row in rows:
            c.execute("UPDATE experiences SET times_triggered = times_triggered + 1, last_accessed = ? WHERE id = ?",
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), row["id"]))
            conn.commit()
            results.append({
                "id": row["id"],
                "task_intent": row["task_intent"],
                "approach": row["approach"],
                "key_insight": row["key_insight"],
                "tags": json.loads(row["tags"]),
                "times_triggered": row["times_triggered"],
                "created_at": row["created_at"],
            })
        return results


def get_patterns():
    init_db()
    with sqlite3.connect(DB_PATH, timeout=_SQLITE_TIMEOUT) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM patterns ORDER BY frequency DESC")
        return [dict(r) for r in c.fetchall()]


# ---------------------------------------------------------------------------
# 技能接口函数（供 remember/recall 命令调用）
# ---------------------------------------------------------------------------

def remember(context: str, source: str = "") -> dict:
    """接收任意文本，提取经验并存库。"""
    init_db()
    exp = extract_experience(context, source=source)
    exp_id = store_experience(exp)
    return {"id": exp_id, **exp}


def recall_experiences(query: str = "", tags: list = None, limit: int = 2) -> List[dict]:
    """根据关键词或标签检索相关经验。

    limit 默认为 2，防止长经验撑爆上下文窗口。
    """
    init_db()
    return recall(keyword=query, tags=tags, limit=limit)
