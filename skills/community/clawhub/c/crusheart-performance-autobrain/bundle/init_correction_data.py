#!/usr/bin/env python3
"""
init_correction_data.py — 自纠错数据链路初始化 v1.0

打通 JudgeEngine 需要的数据文件：
  - .verified_memories.jsonl — 已验证记忆
  - .reflexions.jsonl — 反思记录（失败模式三元组）
  - .replay_buffer/ — 纠正信号重放缓冲区

功能：
  1. 创建必需的数据目录和文件
  2. 集成到 scan_memory 体系，让数据链路完整可用

用法：
  python3 scripts/init_correction_data.py            # 初始化+验证
  python3 scripts/init_correction_data.py --force     # 强制重建
  python3 scripts/init_correction_data.py --status    # 查看状态
"""

import json, os, sys, time, gzip
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from pathlib import Path

BEIJING_TZ = timezone(timedelta(hours=8))
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")

# JudgeEngine 引用的数据文件路径（对应 core/engines/quality/judge_engine.py）
DATA_PATHS = {
    "verified_memories": os.path.join(WORKSPACE, ".verified_memories.jsonl"),
    "reflexions": os.path.join(WORKSPACE, ".reflexions.jsonl"),
    "replay_buffer_records": os.path.join(WORKSPACE, ".replay_buffer", "records.jsonl"),
    "replay_buffer_distilled": os.path.join(WORKSPACE, ".replay_buffer", "distilled.jsonl"),
    "evolution_log": os.path.join(WORKSPACE, ".evolution_log.json"),
    "tuning_log": os.path.join(WORKSPACE, ".tuning_log.json"),
}

# 补充 auto_tuning.py 引用的目录
SKILL_CONFIG_DIR = os.path.join(WORKSPACE, "skills", "Crusheart-Performance-AutoBrain")


def ensure_data_files(force: bool = False) -> Dict:
    """
    确保所有必需的数据文件存在。
    - 如果文件不存在，创建空的
    - 如果文件存在且 force=True，重新创建
    """
    stats = {"created": [], "skipped": [], "errors": []}

    # 1. 顶层数据文件
    for name, path in DATA_PATHS.items():
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if os.path.exists(path) and not force:
                stats["skipped"].append(f"{name} (已存在)")
                continue
            if path.endswith(".jsonl") or path.endswith(".json"):
                with open(path, "w", encoding="utf-8") as f:
                    if path.endswith(".json"):
                        if name == "evolution_log":
                            json.dump({"experiences": [], "learnings": [], "stats": {}}, f)
                        elif name == "tuning_log":
                            json.dump({"history": [], "stats": {}}, f)
                        else:
                            json.dump({}, f)
                    else:
                        f.write("")  # 空的 jsonl
                stats["created"].append(name)
        except Exception as e:
            stats["errors"].append(f"{name}: {e}")

    # 2. auto_tuning.py 的 config.json
    try:
        os.makedirs(SKILL_CONFIG_DIR, exist_ok=True)
        config_path = os.path.join(SKILL_CONFIG_DIR, "config.json")
        if not os.path.exists(config_path) or force:
            default_config = {
                "anti_fake": {"risk_threshold": "high", "authority_domains": [".gov.cn", ".gov", ".edu.cn", ".edu", "arxiv.org", "reuters.com", "xinhuanet.com"]},
                "dual_mode": {"default_mode": "fast", "auto_switch": True, "fast_keyword_weight": 10, "agent_keyword_weight": 8, "multi_tool_weight": 15, "text_length_threshold": 120},
                "lazy_load": {"search_interval_ms": 500, "max_searches_per_task": 5, "cache_ttl_seconds": 1800},
                "mutex": {"task_timeout_seconds": 180, "max_retry": 3},
                "self_evolution": {"enabled": True, "require_confirmation": True},
                "memory_layer": {"l2_retention_days": 7, "decay_start_days": 30, "decay_end_days": 90, "decay_min_weight": 0.5}
            }
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
            stats["created"].append("auto_tuning_config")
    except Exception as e:
        stats["errors"].append(f"auto_tuning_config: {e}")

    # 3. self_evolution_v3.py 引用的目录
    evo_tracker_dir = os.path.join(WORKSPACE, ".evolution_tracker")
    try:
        os.makedirs(evo_tracker_dir, exist_ok=True)
        rules_file = os.path.join(evo_tracker_dir, "registered_rules.json")
        if not os.path.exists(rules_file) or force:
            with open(rules_file, "w", encoding="utf-8") as f:
                json.dump({}, f)
            stats["created"].append("evolution_tracker_rules")
    except Exception as e:
        stats["errors"].append(f"evolution_tracker: {e}")

    return stats


def verify_linkage() -> Dict:
    """验证调用链路完整性（铁律十）"""
    issues = []

    # 1. 检查数据文件是否可读写
    for name, path in DATA_PATHS.items():
        if not os.path.exists(path):
            issues.append(f"{name}: 文件不存在")
            continue
        try:
            with open(path, mode="r" if path.endswith(".jsonl") else "r", encoding="utf-8") as f:
                if path.endswith(".json"):
                    json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            issues.append(f"{name}: 无法读取 - {str(e)[:50]}")

    # 2. 检查 judge_engine 是否可以 import 并实例化
    sys.path.insert(0, WORKSPACE)
    try:
        from core.engines.quality.judge_engine import JudgeEngine
        je = JudgeEngine()
        assert je.verified_path == DATA_PATHS["verified_memories"], "verified_path mismatch"
    except Exception as e:
        issues.append(f"JudgeEngine 实例化失败: {str(e)[:80]}")

    # 3. 检查 auto_memory 是否可用
    try:
        from core.engines.memory.auto_memory import AutoMemory
        am = AutoMemory()
        mem_stats = am.stats()
        assert isinstance(mem_stats, dict), "stats() 返回值类型异常"
    except Exception as e:
        issues.append(f"AutoMemory 检查失败: {str(e)[:80]}")

    # 4. 检查 read_config 是否可读取
    try:
        import importlib
        rc = importlib.import_module("scripts.read_config")
        result = rc.read()
        assert result.get("status") == "ok", "read_config 读取失败"
    except Exception as e:
        issues.append(f"read_config 检查失败: {str(e)[:80]}")

    # 5. 检查 scan_skills 是否可用
    try:
        import importlib
        ss = importlib.import_module("scripts.scan_skills")
        # 只是测试 import，不跑全量扫描
    except Exception as e:
        issues.append(f"scan_skills 导入失败: {str(e)[:80]}")

    return {
        "status": "ok" if not issues else "issues_found",
        "issues": issues,
        "files_checked": list(DATA_PATHS.keys()),
        "judge_engine_available": "JudgeEngine" in dir() if "JudgeEngine" in dir() else False,
    }


def run_init(force: bool = False) -> Dict:
    """统一初始化入口"""
    print("🔧 自纠错数据链路初始化...")
    
    print("  [步骤1/3] 创建数据文件...")
    stats = ensure_data_files(force=force)
    print(f"    创建: {len(stats['created'])} 个, 跳过: {len(stats['skipped'])} 个")
    if stats["errors"]:
        print(f"    ❌ 错误: {stats['errors']}")
    
    print("  [步骤2/3] 验证链路完整性...")
    linkage = verify_linkage()
    if linkage["issues"]:
        print(f"    ⚠️ 发现 {len(linkage['issues'])} 个问题:")
        for i in linkage["issues"]:
            print(f"      - {i}")
    else:
        print("    ✅ 链路完整")
    
    print("  [步骤3/3] 首次扫描...")
    try:
        import importlib
        sm = importlib.import_module("scripts.scan_memory")
        result = sm.scan_directory()
        print(f"    → 扫描完成")
    except Exception as e:
        print(f"    ⚠️ 记忆扫描跳过: {str(e)[:50]}")
    
    print(f"\n{'✅ 初始化完成' if not linkage['issues'] else '⚠️ 初始化完成（有需处理的问题）'}")
    
    return {
        "data_files": stats,
        "linkage": linkage,
        "initialized_at": datetime.now(BEIJING_TZ).isoformat(),
    }


if __name__ == "__main__":
    force = "--force" in sys.argv
    
    if "--status" in sys.argv:
        linkage = verify_linkage()
        print(f"📋 自纠错数据链路状态")
        print(f"  状态: {'✅ 正常' if not linkage['issues'] else '⚠️ 有问题'}")
        if linkage["issues"]:
            print(f"  问题:")
            for i in linkage["issues"]:
                print(f"    - {i}")
        else:
            # 显示文件大小
            for name, path in DATA_PATHS.items():
                if os.path.exists(path):
                    size = os.path.getsize(path)
                    print(f"  {name}: {size} bytes")
        sys.exit(0)
    
    if "--force" in sys.argv:
        run_init(force=True)
    else:
        run_init(force=False)
