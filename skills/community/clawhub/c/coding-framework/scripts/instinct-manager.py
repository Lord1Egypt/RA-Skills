#!/usr/bin/env python3
"""
instinct-manager.py — 本能学习系统

管理编码本能（instincts）的记录、查询、衰减和晋升。
借鉴 ECC 的 instinct-cli.py 设计，适配 OpenClaw 平台。

核心概念：
  - Instinct: 从编码实践中学习到的模式/规则
  - Confidence: 置信度（0.0-1.0），基于观察次数和一致性
  - Scope: global（全局）或 project（项目级）
  - Domain: 领域标签（code-style, error-handling, performance 等）

置信度演化：
  - 初始：1-2次观察=0.3，3-5次=0.5，6-10次=0.7，11+=0.85
  - 增强：每次确认 +0.05（上限1.0）
  - 衰减：每次矛盾 -0.1，每周不使用 -0.02

晋升机制：
  - 同一 instinct 在 2+ 项目中 confidence >= 0.8 → 自动晋升为 global

用法：
  python instinct-manager.py record --trigger "..." --action "..." --domain "code-style"
  python instinct-manager.py query --domain "code-style" --min-confidence 0.6
  python instinct-manager.py decay
  python instinct-manager.py promote --id "instinct-xxx"
  python instinct-manager.py list --all
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ─── 常量 ───────────────────────────────────────────────────────────────────

INSTINCTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "instincts")
GLOBAL_DIR = os.path.join(INSTINCTS_DIR, "global")
PROJECTS_DIR = os.path.join(INSTINCTS_DIR, "projects")

# 置信度阈值
CONFIDENCE_INITIAL = {
    (1, 2): 0.3,
    (3, 5): 0.5,
    (6, 10): 0.7,
    (11, 999999): 0.85,
}

CONFIDENCE_BOOST = 0.05  # 每次确认增强
CONFIDENCE_PENALTY = 0.1  # 每次矛盾惩罚
DECAY_RATE_PER_WEEK = 0.02  # 每周衰减

PROMOTE_THRESHOLD = 0.8  # 晋升阈值
PROMOTE_MIN_PROJECTS = 2  # 最少项目数


# ─── 工具函数 ────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs():
    """确保目录存在。"""
    os.makedirs(GLOBAL_DIR, exist_ok=True)
    os.makedirs(PROJECTS_DIR, exist_ok=True)


def detect_project() -> Optional[str]:
    """检测当前项目，返回 project_id（基于 git remote hash）。"""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5, cwd=os.getcwd()
        )
        if result.returncode == 0:
            remote = result.stdout.strip()
            return hashlib.sha256(remote.encode()).hexdigest()[:12]
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    return None


def get_project_dir(project_id: Optional[str]) -> str:
    """获取项目级 instinct 目录。"""
    if project_id:
        return os.path.join(PROJECTS_DIR, project_id)
    return GLOBAL_DIR


def load_instinct(path: str) -> dict:
    """加载 instinct 文件。"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_instinct(path: str, data: dict):
    """保存 instinct 文件。"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def calculate_confidence(observations: int, confirmations: int, contradictions: int) -> float:
    """计算置信度。"""
    # 基础置信度（基于观察次数）
    base = 0.3
    for (low, high), value in CONFIDENCE_INITIAL.items():
        if low <= observations <= high:
            base = value
            break
    
    # 增强（确认）
    boost = confirmations * CONFIDENCE_BOOST
    
    # 惩罚（矛盾）
    penalty = contradictions * CONFIDENCE_PENALTY
    
    # 最终置信度（0.0-1.0）
    return max(0.0, min(1.0, base + boost - penalty))


def apply_decay(instinct: dict) -> dict:
    """应用衰减。"""
    last_used = instinct.get("last_used", instinct.get("created_at", ""))
    if not last_used:
        return instinct
    
    try:
        last_dt = datetime.fromisoformat(last_used)
        now = datetime.now(timezone.utc)
        weeks_elapsed = (now - last_dt).total_seconds() / (7 * 24 * 3600)
        
        if weeks_elapsed > 0:
            decay_amount = weeks_elapsed * DECAY_RATE_PER_WEEK
            instinct["confidence"] = max(0.0, instinct["confidence"] - decay_amount)
            instinct["decay_applied"] = decay_amount
    except ValueError:
        pass
    
    return instinct


# ─── 子命令实现 ──────────────────────────────────────────────────────────────

def cmd_record(args: argparse.Namespace) -> None:
    """记录一个新的本能观察。"""
    ensure_dirs()
    
    # 检测项目
    project_id = detect_project() if not args.global_mode else None
    project_dir = get_project_dir(project_id)
    os.makedirs(project_dir, exist_ok=True)
    
    # 生成 instinct ID
    trigger_hash = hashlib.sha256(args.trigger.encode()).hexdigest()[:8]
    instinct_id = f"instinct-{trigger_hash}"
    instinct_path = os.path.join(project_dir, f"{instinct_id}.json")
    
    # 加载或创建 instinct
    if os.path.exists(instinct_path):
        instinct = load_instinct(instinct_path)
        instinct["observations"] += 1
        if args.confirm:
            instinct["confirmations"] += 1
        if args.contradict:
            instinct["contradictions"] += 1
    else:
        instinct = {
            "id": instinct_id,
            "trigger": args.trigger,
            "action": args.action,
            "domain": args.domain,
            "scope": "global" if args.global_mode else "project",
            "project_id": project_id,
            "observations": 1,
            "confirmations": 1 if args.confirm else 0,
            "contradictions": 1 if args.contradict else 0,
            "confidence": 0.3,
            "created_at": now_iso(),
            "last_used": now_iso(),
            "tags": args.tags.split(",") if args.tags else [],
        }
    
    # 重新计算置信度
    instinct["confidence"] = calculate_confidence(
        instinct["observations"],
        instinct["confirmations"],
        instinct["contradictions"]
    )
    instinct["last_used"] = now_iso()
    instinct["updated_at"] = now_iso()
    
    # 保存
    save_instinct(instinct_path, instinct)
    
    print(json.dumps({
        "success": True,
        "action": "record",
        "instinct_id": instinct_id,
        "confidence": instinct["confidence"],
        "observations": instinct["observations"],
        "scope": instinct["scope"],
        "message": f"已记录本能: {instinct_id} (置信度: {instinct['confidence']:.2f})"
    }, ensure_ascii=False, indent=2))


def cmd_query(args: argparse.Namespace) -> None:
    """查询当前可用的本能。"""
    ensure_dirs()
    
    project_id = detect_project() if not args.global_mode else None
    
    # 收集所有 instinct
    results = []
    
    # 全局 instinct
    if os.path.exists(GLOBAL_DIR):
        for f in Path(GLOBAL_DIR).glob("*.json"):
            instinct = load_instinct(str(f))
            instinct = apply_decay(instinct)
            if instinct["confidence"] >= args.min_confidence:
                if not args.domain or instinct.get("domain") == args.domain:
                    results.append(instinct)
    
    # 项目级 instinct
    if project_id:
        project_dir = get_project_dir(project_id)
        if os.path.exists(project_dir):
            for f in Path(project_dir).glob("*.json"):
                instinct = load_instinct(str(f))
                instinct = apply_decay(instinct)
                if instinct["confidence"] >= args.min_confidence:
                    if not args.domain or instinct.get("domain") == args.domain:
                        results.append(instinct)
    
    # 按置信度排序
    results.sort(key=lambda x: x["confidence"], reverse=True)
    
    print(json.dumps({
        "success": True,
        "action": "query",
        "count": len(results),
        "instincts": results[:args.limit],
        "message": f"找到 {len(results)} 个本能"
    }, ensure_ascii=False, indent=2))


def cmd_decay(args: argparse.Namespace) -> None:
    """衰减长期未使用的本能。"""
    ensure_dirs()
    
    decayed_count = 0
    
    # 遍历所有 instinct
    for dir_path in [GLOBAL_DIR, PROJECTS_DIR]:
        if not os.path.exists(dir_path):
            continue
        for f in Path(dir_path).rglob("*.json"):
            instinct = load_instinct(str(f))
            old_confidence = instinct["confidence"]
            instinct = apply_decay(instinct)
            
            if instinct["confidence"] < old_confidence:
                save_instinct(str(f), instinct)
                decayed_count += 1
    
    print(json.dumps({
        "success": True,
        "action": "decay",
        "decayed_count": decayed_count,
        "message": f"已衰减 {decayed_count} 个本能"
    }, ensure_ascii=False, indent=2))


def cmd_promote(args: argparse.Namespace) -> None:
    """晋升项目本能到全局。"""
    ensure_dirs()
    
    instinct_id = args.id
    if not instinct_id.endswith(".json"):
        instinct_id = f"{instinct_id}.json"
    
    # 查找 instinct
    found = False
    for project_dir in Path(PROJECTS_DIR).iterdir():
        if not project_dir.is_dir():
            continue
        instinct_path = project_dir / instinct_id
        if instinct_path.exists():
            instinct = load_instinct(str(instinct_path))
            
            # 检查晋升条件
            if instinct["confidence"] < PROMOTE_THRESHOLD:
                print(json.dumps({
                    "success": False,
                    "message": f"置信度不足: {instinct['confidence']:.2f} < {PROMOTE_THRESHOLD}"
                }, ensure_ascii=False))
                return
            
            # 检查是否在多个项目中存在
            project_count = 0
            for pd in Path(PROJECTS_DIR).iterdir():
                if pd.is_dir() and (pd / instinct_id).exists():
                    other_instinct = load_instinct(str(pd / instinct_id))
                    if other_instinct["confidence"] >= PROMOTE_THRESHOLD:
                        project_count += 1
            
            if project_count < PROMOTE_MIN_PROJECTS:
                print(json.dumps({
                    "success": False,
                    "message": f"项目数不足: {project_count} < {PROMOTE_MIN_PROJECTS}"
                }, ensure_ascii=False))
                return
            
            # 晋升：复制到 global
            global_path = os.path.join(GLOBAL_DIR, instinct_id)
            instinct["scope"] = "global"
            instinct["promoted_at"] = now_iso()
            save_instinct(global_path, instinct)
            
            found = True
            print(json.dumps({
                "success": True,
                "action": "promote",
                "instinct_id": instinct["id"],
                "from": "project",
                "to": "global",
                "message": f"已晋升本能: {instinct['id']} 到全局"
            }, ensure_ascii=False, indent=2))
            break
    
    if not found:
        print(json.dumps({
            "success": False,
            "message": f"未找到本能: {args.id}"
        }, ensure_ascii=False))


def cmd_list(args: argparse.Namespace) -> None:
    """列出所有本能。"""
    ensure_dirs()
    
    results = []
    
    # 全局
    if os.path.exists(GLOBAL_DIR):
        for f in Path(GLOBAL_DIR).glob("*.json"):
            instinct = load_instinct(str(f))
            results.append(instinct)
    
    # 项目级
    if os.path.exists(PROJECTS_DIR):
        for f in Path(PROJECTS_DIR).rglob("*.json"):
            instinct = load_instinct(str(f))
            results.append(instinct)
    
    # 按置信度排序
    results.sort(key=lambda x: x["confidence"], reverse=True)
    
    if not args.all:
        results = [r for r in results if r["confidence"] >= 0.5]
    
    print(json.dumps({
        "success": True,
        "action": "list",
        "count": len(results),
        "instincts": results,
    }, ensure_ascii=False, indent=2))


# ─── 参数解析 ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="本能学习系统 — 管理编码本能的记录、查询、衰减和晋升",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # record
    p_record = subparsers.add_parser("record", help="记录一个新的本能观察")
    p_record.add_argument("--trigger", required=True, help="触发条件描述")
    p_record.add_argument("--action", required=True, help="推荐动作")
    p_record.add_argument("--domain", required=True, help="领域标签（code-style, error-handling, performance 等）")
    p_record.add_argument("--tags", help="标签（逗号分隔）")
    p_record.add_argument("--confirm", action="store_true", help="确认观察（增强置信度）")
    p_record.add_argument("--contradict", action="store_true", help="矛盾观察（降低置信度）")
    p_record.add_argument("--global", dest="global_mode", action="store_true", help="记录为全局本能")
    
    # query
    p_query = subparsers.add_parser("query", help="查询当前可用的本能")
    p_query.add_argument("--domain", help="领域过滤")
    p_query.add_argument("--min-confidence", type=float, default=0.5, help="最低置信度（默认 0.5）")
    p_query.add_argument("--limit", type=int, default=10, help="返回数量限制（默认 10）")
    p_query.add_argument("--global", dest="global_mode", action="store_true", help="仅查询全局本能")
    
    # decay
    p_decay = subparsers.add_parser("decay", help="衰减长期未使用的本能")
    
    # promote
    p_promote = subparsers.add_parser("promote", help="晋升项目本能到全局")
    p_promote.add_argument("--id", required=True, help="本能 ID")
    
    # list
    p_list = subparsers.add_parser("list", help="列出所有本能")
    p_list.add_argument("--all", action="store_true", help="包括低置信度本能")
    
    return parser


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    commands = {
        "record": cmd_record,
        "query": cmd_query,
        "decay": cmd_decay,
        "promote": cmd_promote,
        "list": cmd_list,
    }
    
    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
