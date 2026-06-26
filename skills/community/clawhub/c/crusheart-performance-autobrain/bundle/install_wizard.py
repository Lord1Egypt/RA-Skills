#!/usr/bin/env python3
"""
install_wizard.py — AutoBrain 安装向导 v1.0

首次安装时由 index.js 调用，执行完整安装引导流程。

流程：
  Phase 1: 兼容性检查（安装前）
  Phase 2: 初始化（安装后首次启动）
    2.1 注入 SOUL.md 规则
    2.2 记忆扫描与归档
    2.3 数据库/知识库自动检测
    2.4 技能扫描与分类
    2.5 技能—引擎连接（SkillAutoInvoker + SelfEvolution + AutoTuning）
    2.6 系统全量索引构建
    2.7 定时任务注册
    2.8 运行状态验证
  Phase 3: 输出安装报告

用法：
  python3 scripts/install_wizard.py --check          # Phase 1: 仅兼容性检查
  python3 scripts/install_wizard.py --init           # Phase 2: 执行初始化
  python3 scripts/install_wizard.py --full           # Phase 1 + Phase 2
  python3 scripts/install_wizard.py --status         # Phase 3: 仅状态检查

返回 JSON 格式结果，供 index.js 解析。
"""

import json, os, sys, subprocess, re, glob, shutil, hashlib, time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

BEIJING_TZ = timezone(timedelta(hours=8))
PLUGIN_VERSION = "6.3.1"

# ── 路径 ──────────────────────────────────────────────────
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE") or os.path.expanduser("~/.openclaw/workspace")
CONFIG_DIR = os.environ.get("OPENCLAW_CONFIG_DIR") or os.path.expanduser("~/.openclaw")
CONFIG_FILE = os.path.join(CONFIG_DIR, "openclaw.json")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
SKILLS_DIR = os.path.join(WORKSPACE, "skills")
SOUL_PATH = os.path.join(WORKSPACE, "SOUL.md")
ENGINES_DIR = os.path.join(WORKSPACE, "core", "engines")
WIZARD_STATE = os.path.join(WORKSPACE, ".install_wizard_state.json")

# 插件包所在路径（由 index.js 传入，或自动推断）
PACK_DIR = os.environ.get("CRUSHEART_PACK_DIR") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
)
BUNDLE_DIR = os.path.join(PACK_DIR, "bundle")

# 最低要求
REQUIREMENTS = {
    "openclaw_min": "2026.5.0",
    "node_min": (18, 0, 0),
    "python_min": (3, 10, 0),
    "disk_min_mb": 50,
}


# ════════════════════════════════════════════════════════════
# 工具函数
# ════════════════════════════════════════════════════════════

def _now() -> str:
    return datetime.now(BEIJING_TZ).isoformat()


def _parse_version(v: str) -> Tuple[int, ...]:
    parts = re.findall(r"\d+", v)
    return tuple(int(p) for p in parts[:3])


def _ensure_dir(d: str):
    os.makedirs(d, exist_ok=True)


def _run_py(script: str, args: List[str] = None) -> Dict:
    """调用 engine 脚本，返回解析后的 JSON"""
    candidates = [
        os.path.join(WORKSPACE, script),
        os.path.join(WORKSPACE, "scripts", script),
        os.path.join(WORKSPACE, "core", "engines", "init", script),
    ]
    for engine_group in ["init", "memory", "quality", "operations", "workflow", "tools", "hooks", "compat"]:
        candidates.append(os.path.join(WORKSPACE, "core", "engines", engine_group, script))
    if BUNDLE_DIR:
        candidates.append(os.path.join(BUNDLE_DIR, script))

    target = None
    for c in candidates:
        if os.path.exists(c):
            target = c
            break
    if not target:
        return {"status": "error", "message": f"脚本未找到: {script}"}

    try:
        result = subprocess.run(
            [sys.executable, target] + (args or []),
            cwd=WORKSPACE, capture_output=True, text=True, timeout=60
        )
        stdout = result.stdout.strip()
        if stdout:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                return {"status": "ok", "output": stdout}
        return {"status": "ok"} if result.returncode == 0 else {"status": "error", "message": result.stderr[:300]}
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "执行超时"}
    except Exception as e:
        return {"status": "error", "message": str(e)[:300]}


def _openclaw_version() -> Optional[str]:
    """获取 OpenClaw 版本"""
    try:
        r = subprocess.run(["openclaw", "--version"], capture_output=True, text=True, timeout=10)
        m = re.search(r"(\d+\.\d+\.\d+)", r.stdout)
        return m.group(1) if m else None
    except: return None


def _disk_free_mb() -> int:
    st = os.statvfs(WORKSPACE)
    return int(st.f_frsize * st.f_bavail / (1024 * 1024))


# ════════════════════════════════════════════════════════════
# Phase 1: 兼容性检查
# ════════════════════════════════════════════════════════════

def check_compatibility() -> Dict:
    """
    检查运行环境，输出兼容性报告。
    关键检查项不通过则设置拦截标志（blocked: true）。
    """
    checks = {}
    blocked = False
    warnings = []

    # 1. OpenClaw 版本
    oc_ver = _openclaw_version()
    if oc_ver:
        oc_parsed = _parse_version(oc_ver)
        req_parsed = _parse_version(REQUIREMENTS["openclaw_min"])
        ok = oc_parsed >= req_parsed
        checks["openclaw"] = {"version": oc_ver, "required": REQUIREMENTS["openclaw_min"], "ok": ok}
        if not ok:
            blocked = True
            warnings.append(f"OpenClaw {oc_ver} 不满足最低要求 {REQUIREMENTS['openclaw_min']}")
    else:
        checks["openclaw"] = {"version": "unknown", "required": REQUIREMENTS["openclaw_min"], "ok": False}
        blocked = True
        warnings.append("无法获取 OpenClaw 版本，请确保 OpenClaw 已安装")

    # 2. Node.js 版本
    try:
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        node_ver = r.stdout.strip().lstrip("v")
        node_parsed = _parse_version(node_ver)
        ok = node_parsed >= REQUIREMENTS["node_min"]
        checks["node"] = {"version": node_ver, "required": ".".join(str(x) for x in REQUIREMENTS["node_min"]), "ok": ok}
        if not ok:
            warnings.append(f"Node.js {node_ver} 建议升级至 ≥ {'.'.join(str(x) for x in REQUIREMENTS['node_min'])}")
    except:
        checks["node"] = {"version": "unknown", "required": ".".join(str(x) for x in REQUIREMENTS["node_min"]), "ok": False}
        warnings.append("Node.js 未安装或不可用")

    # 3. Python 版本
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_parsed = (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    ok = py_parsed >= REQUIREMENTS["python_min"]
    checks["python"] = {"version": py_ver, "required": ".".join(str(x) for x in REQUIREMENTS["python_min"]), "ok": ok}
    if not ok:
        warnings.append(f"Python {py_ver} 不满足最低要求 {'.'.join(str(x) for x in REQUIREMENTS['python_min'])}")

    # 4. 磁盘空间
    free_mb = _disk_free_mb()
    ok = free_mb >= REQUIREMENTS["disk_min_mb"]
    checks["disk"] = {"free_mb": free_mb, "required_mb": REQUIREMENTS["disk_min_mb"], "ok": ok}
    if not ok:
        blocked = True
        warnings.append(f"磁盘剩余空间 {free_mb}MB，需要至少 {REQUIREMENTS['disk_min_mb']}MB")

    # 5. 工作区存在性
    ws_ok = os.path.isdir(WORKSPACE)
    checks["workspace"] = {"path": WORKSPACE, "ok": ws_ok}
    if not ws_ok:
        blocked = True
        warnings.append(f"工作区不存在: {WORKSPACE}")

    # 6. 独占插槽检测
    slot_lock = os.path.join(WORKSPACE, ".crusheart-slot.lock")
    slot_ok = not os.path.isdir(slot_lock)
    checks["slot"] = {"path": slot_lock, "ok": slot_ok}
    if not slot_ok:
        blocked = True
        try:
            info = json.load(open(os.path.join(slot_lock, "info.json")))
            warnings.append(f"插件槽已被占用: {info.get('plugin', 'unknown')} v{info.get('version', '?')}")
        except:
            warnings.append("插件槽已被占用，请先卸载旧插件或手动删除 .crusheart-slot.lock/")

    return {
        "phase": "compatibility_check",
        "timestamp": _now(),
        "blocked": blocked,
        "warnings": warnings,
        "checks": checks,
        "passed": not blocked and len(warnings) == 0,
    }


# ════════════════════════════════════════════════════════════
# Phase 2: 初始化
# ════════════════════════════════════════════════════════════

def _merge_into_soulmd() -> Dict:
    """将 bundle/SOUL.md 的铁律注入到用户 SOUL.md 中"""
    bundle_soul = os.path.join(BUNDLE_DIR, "SOUL.md")
    if not os.path.exists(bundle_soul):
        return {"status": "skipped", "reason": "bundle/SOUL.md 不存在"}

    with open(bundle_soul, encoding="utf-8") as f:
        rules_content = f.read()

    if os.path.exists(SOUL_PATH):
        existing = open(SOUL_PATH, encoding="utf-8").read()
        # 检查是否已有 crusheart 注入标记（去重）
        if "<!-- Crusheart AutoBrain injected" in existing:
            return {"status": "skipped", "reason": "SOUL.md 已注入过"}

        # 追加规则（用分割线隔开，避免覆盖用户已有内容）
        merged = existing.rstrip() + "\n\n" + rules_content
        with open(SOUL_PATH, "w", encoding="utf-8") as f:
            f.write(merged)
        return {"status": "ok", "action": "merged", "position": "appended"}
    else:
        with open(SOUL_PATH, "w", encoding="utf-8") as f:
            f.write(rules_content)
        return {"status": "ok", "action": "created"}


def _scan_and_archive_memory() -> Dict:
    """扫描 memory/ 目录，调用 memory_layer_engine 进行多层记忆归档"""
    results = {"scanned_files": 0, "ingested": 0, "archived": 0}

    # 1. 扫描 memory/ .md 文件
    if os.path.isdir(MEMORY_DIR):
        md_files = glob.glob(os.path.join(MEMORY_DIR, "*.md"))
        # 排除 .archive/ 下的
        md_files = [f for f in md_files if "/.archive/" not in f]
        results["scanned_files"] = len(md_files)

    # 2. 调用 scan_memory.py（如果存在）
    scan_r = _run_py("scan_memory.py", ["--scan-only"])
    if scan_r.get("status") == "ok":
        results["ingested"] = scan_r.get("ingested", 0)

    # 3. 归档旧日志（如果存在 archive mode）
    ar_r = _run_py("scan_memory.py", ["--archive"])
    if ar_r.get("status") == "ok":
        results["archived"] = ar_r.get("archived", 0)

    return {"status": "ok", **results}


def _detect_databases() -> Dict:
    """
    自动检测用户的数据库/知识库位置。
    支持：SQLite (.db / .sqlite), JSON, YAML 配置文件。
    不做连接验证（用户可能没有），检测到就记录路径。
    """
    found = []

    # 1. 工作区根目录的 .db 文件
    for f in glob.glob(os.path.join(WORKSPACE, "*.db")):
        found.append({"path": f, "type": "sqlite", "size": os.path.getsize(f)})
    for f in glob.glob(os.path.join(WORKSPACE, "*.sqlite")):
        found.append({"path": f, "type": "sqlite", "size": os.path.getsize(f)})

    # 2. 检查 openclaw.json 中的 db/knowledge 配置
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            config = json.load(open(CONFIG_FILE, encoding="utf-8"))
        except: pass

    db_paths = []
    for key in ["db", "database", "knowledge", "knowledge_base", "vector_store"]:
        val = config.get(key, {})
        if isinstance(val, str):
            db_paths.append(val)
        elif isinstance(val, dict):
            for sub_key in ["path", "url", "location", "file"]:
                if sub_key in val:
                    db_paths.append(val[sub_key])

    for p in db_paths:
        if p.startswith("/") or p.startswith("~"):
            expanded = os.path.expanduser(p)
            if os.path.exists(expanded):
                found.append({"path": expanded, "type": "config_ref", "size": os.path.getsize(expanded)})

    # 3. 检查 .crusheart-* 状态文件中的 db 引用
    for state_f in glob.glob(os.path.join(WORKSPACE, ".crusheart-*.json")):
        try:
            state_data = json.load(open(state_f, encoding="utf-8"))
            if "db_path" in state_data:
                p = state_data["db_path"]
                if os.path.exists(p):
                    found.append({"path": p, "type": "state_ref", "source": state_f, "size": os.path.getsize(p)})
        except: pass

    return {
        "status": "ok",
        "found": found,
        "count": len(found),
        "connected": True,  # 检测到即视为可连接（引擎启动时会实际连接）
    }


def _scan_and_classify_skills() -> Dict:
    """扫描 skills/ 并调用 scan_skills.py 进行自动分类"""
    r = _run_py("scan_skills.py", ["--refresh"])
    stats = _run_py("scan_skills.py", ["--stats"])

    result = {"status": "ok"}
    if stats.get("status") == "ok":
        result["stats"] = stats

    # 额外统计文件数
    if os.path.isdir(SKILLS_DIR):
        skill_count = len([d for d in os.listdir(SKILLS_DIR)
                          if os.path.isdir(os.path.join(SKILLS_DIR, d))])
        result["skill_count"] = skill_count

    return result


def _connect_skill_to_engine() -> Dict:
    """
    将技能数据连接到 SkillAutoInvoker + SelfEvolution + AutoTuning。
    1. 验证 SkillAutoInvoker 可调用
    2. 验证 self_evolution_v3 可访问
    3. 验证 auto_tuning 可初始化
    4. 注入技能路由规则
    """
    results = {}

    # 1. SkillAutoInvoker 测试
    invoker_r = _run_py("auto_engines.py", ["test"])
    results["skill_auto_invoker"] = invoker_r.get("status", "error")

    # 2. SelfEvolution 验证
    try:
        se_path = os.path.join(WORKSPACE, "core", "engines", "hooks", "self_evolution_v3.py")
        if os.path.exists(se_path):
            r = subprocess.run(
                [sys.executable, "-c", "import sys; sys.path.insert(0,'.'); from core.engines.hooks.self_evolution_v3 import SelfEvolutionEngine; print('ok')"],
                cwd=WORKSPACE, capture_output=True, text=True, timeout=15
            )
            results["self_evolution"] = "ok" if r.returncode == 0 else r.stderr[:100]
        else:
            results["self_evolution"] = "not_found"
    except Exception as e:
        results["self_evolution"] = str(e)[:100]

    # 3. AutoTuning 验证
    try:
        at_path = os.path.join(WORKSPACE, "core", "engines", "tools", "auto_tuning.py")
        if os.path.exists(at_path):
            r = subprocess.run(
                [sys.executable, "-c", "import sys; sys.path.insert(0,'.'); from core.engines.tools.auto_tuning import init; print('ok')"],
                cwd=WORKSPACE, capture_output=True, text=True, timeout=15
            )
            results["auto_tuning"] = "ok" if r.returncode == 0 else r.stderr[:100]
        else:
            results["auto_tuning"] = "not_found"
    except Exception as e:
        results["auto_tuning"] = str(e)[:100]

    # 4. 写入技能—引擎连接状态标记
    connection_state = {
        "engine": "skill_auto_invoker",
        "paired_engines": ["self_evolution_v3", "auto_tuning"],
        "connected_at": _now(),
    }
    conn_path = os.path.join(WORKSPACE, ".skill_engine_connection.json")
    with open(conn_path, "w", encoding="utf-8") as f:
        json.dump(connection_state, f, indent=2)

    results["connection_marker"] = conn_path
    all_ok = all(v == "ok" for v in results.values() if isinstance(v, str))
    return {"status": "ok" if all_ok else "partial", "details": results}


def _build_system_index() -> Dict:
    """构建全量系统索引：记忆索引 + 技能索引 + 引擎注册"""
    results = {}

    # 1. 引擎注册扫描
    r = _run_py("auto_engines.py", ["scan"])
    results["engine_scan"] = r.get("status", "error")

    # 2. 技能索引重建（force）
    r = _run_py("scan_skills.py", ["--refresh"])
    results["skill_index"] = r.get("status", "error")

    # 3. 记忆索引重建
    r = _run_py("scan_memory.py", ["--scan-only"])
    results["memory_index"] = r.get("status", "error")

    all_ok = all(v == "ok" for v in results.values())
    return {"status": "ok" if all_ok else "partial", "details": results}


def _register_cron_tasks() -> Dict:
    """注册定时任务（共2个：01:00 统一维护+记忆维护 / 05:00 引擎初始化+版本检查），调用 register_crons.sh"""
    cron_sh = os.path.join(WORKSPACE, "scripts", "register_crons.sh")
    if os.path.exists(cron_sh):
        try:
            r = subprocess.run(["bash", cron_sh], cwd=WORKSPACE, capture_output=True, text=True, timeout=30)
            return {"status": "ok" if r.returncode == 0 else "error", "output": r.stdout[:200]}
        except Exception as e:
            return {"status": "error", "message": str(e)[:200]}
    else:
        # fallback: 直接调用 task_scheduler
        r = _run_py("task_scheduler.py", ["--register-crons"])
        return r


def _verify_integrity() -> Dict:
    """
    检查所有关键引擎模块的文件完整性与可导入性。
    验证所有 engines.json 中注册的引擎都能 import。
    """
    engines_json = os.path.join(WORKSPACE, "core", "engines", "init", "engines.json")
    if not os.path.exists(engines_json):
        return {"status": "error", "message": "engines.json 不存在"}

    try:
        with open(engines_json, encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as e:
        return {"status": "error", "message": f"engines.json 解析失败: {e}"}

    engine_list = cfg.get("engines", [])
    results = {"total": len(engine_list), "imported": 0, "failed": 0, "details": []}

    for eng in engine_list:
        name = eng.get("name", "?")
        module_path = eng.get("module", "")
        class_name = eng.get("class", "")

        try:
            module = __import__(module_path, fromlist=[class_name] if class_name else [])
            if class_name:
                getattr(module, class_name)
            results["imported"] += 1
            results["details"].append({"name": name, "status": "ok"})
        except Exception as e:
            results["failed"] += 1
            results["details"].append({"name": name, "status": "fail", "error": str(e)[:100]})

    # 检查 bundle 脚本完整性
    bundle_scripts = [
        "daily_maintenance.py", "scan_memory.py", "scan_skills.py",
        "init_correction_data.py", "read_config.py", "auto_save_capsule.py",
        "version_check.py", "register_crons.sh"
    ]
    missing = []
    for bs in bundle_scripts:
        target = os.path.join(WORKSPACE, "scripts", bs)
        if not os.path.exists(target):
            missing.append(bs)

    results["bundle_scripts"] = {"total": len(bundle_scripts), "missing": missing}
    results["all_imported"] = results["failed"] == 0
    results["all_scripts_deployed"] = len(missing) == 0

    return results


def run_initialization() -> Dict:
    """执行完整初始化流程 (Phase 2)"""
    steps = {}
    all_ok = True

    print("\n🦞 灵枢 AutoBrain Turbo — 初始化开始")
    print("=" * 50)

    # Step 1: SOUL.md 注入
    print("\n[1/8] 🔧 注入行为规则...")
    steps["soul_inject"] = _merge_into_soulmd()
    print(f"      → {steps['soul_inject'].get('status')}: {steps['soul_inject'].get('reason', 'ok')}")
    if steps["soul_inject"]["status"] == "error":
        all_ok = False

    # Step 2: 记忆扫描归档
    print("\n[2/8] 🧠 记忆扫描归档...")
    steps["memory_scan"] = _scan_and_archive_memory()
    print(f"      → {steps['memory_scan'].get('status')}: scanned={steps['memory_scan'].get('scanned_files',0)}")
    if steps["memory_scan"]["status"] == "error":
        all_ok = False

    # Step 3: 数据库检测
    print("\n[3/8] 🗄️ 数据库/知识库检测...")
    steps["db_detect"] = _detect_databases()
    found_count = steps["db_detect"].get("count", 0)
    if found_count > 0:
        print(f"      → 发现 {found_count} 个数据库/knowledge 文件")
        for f in steps["db_detect"].get("found", []):
            print(f"        - {f['path']} ({f.get('type','')})")
    else:
        print(f"      → 未检测到本地数据库/知识库（跳过）")
    if steps["db_detect"]["status"] == "error":
        all_ok = False

    # Step 4: 技能扫描分类
    print("\n[4/8] 📋 技能扫描与分类...")
    steps["skill_scan"] = _scan_and_classify_skills()
    skill_count = steps["skill_scan"].get("skill_count", 0)
    print(f"      → {steps['skill_scan'].get('status')}: {skill_count} 个技能")
    if steps["skill_scan"]["status"] == "error":
        all_ok = False

    # Step 5: 技能引擎连接
    print("\n[5/8] 🔗 连接技能自动调用引擎 + 自进化 + 参数调优...")
    steps["engine_connect"] = _connect_skill_to_engine()
    det = steps["engine_connect"].get("details", {})
    print(f"      → SkillAutoInvoker: {det.get('skill_auto_invoker', '?')}")
    print(f"      → SelfEvolution: {det.get('self_evolution', '?')}")
    print(f"      → AutoTuning: {det.get('auto_tuning', '?')}")
    if steps["engine_connect"]["status"] == "error":
        all_ok = False

    # Step 6: 系统索引
    print("\n[6/8] ⚡ 构建系统全量索引...")
    steps["system_index"] = _build_system_index()
    print(f"      → {steps['system_index'].get('status')}")
    if steps["system_index"]["status"] == "error":
        all_ok = False

    # Step 7: 注册定时任务
    print("\n[7/8] 🕐 注册定时任务（01:00统一维护 + 05:00引擎初始化）...")
    steps["cron_register"] = _register_cron_tasks()
    print(f"      → {steps['cron_register'].get('status')}")
    if steps["cron_register"]["status"] == "error":
        all_ok = False

    # Step 8: 运行状态验证
    print("\n[8/8] ✅ 运行状态与文件完整性检查...")
    steps["integrity"] = _verify_integrity()
    intg = steps["integrity"]
    print(f"      → 引擎: {intg.get('imported',0)}/{intg.get('total',0)} 导入成功")
    missing_scripts = intg.get("bundle_scripts", {}).get("missing", [])
    if missing_scripts:
        print(f"      → 缺失脚本: {', '.join(missing_scripts)}")
    else:
        print(f"      → 所有 bundle 脚本已部署")
    if not intg.get("all_imported", False):
        all_ok = False

    # 完成
    print("\n" + "=" * 50)
    status = "✅ 初始化完成" if all_ok else "⚠️ 初始化部分完成（见上）"
    print(f"\n{status}\n")

    # 写状态标记
    state = {
        "initialized": True,
        "all_ok": all_ok,
        "timestamp": _now(),
        "version": PLUGIN_VERSION,
        "steps": {k: v.get("status", "?") for k, v in steps.items()}
    }
    _ensure_dir(os.path.dirname(WIZARD_STATE))
    with open(WIZARD_STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    result = {
        "phase": "initialization",
        "status": "ok" if all_ok else "partial",
        "all_ok": all_ok,
        "timestamp": _now(),
        "steps": steps,
        "summary": {k: v.get("status", "?") for k, v in steps.items()}
    }
    return result


# ════════════════════════════════════════════════════════════
# Phase 3: 状态检查
# ════════════════════════════════════════════════════════════

def check_status() -> Dict:
    """检查当前安装状态和模块完整性"""
    result = {
        "phase": "status_check",
        "timestamp": _now(),
        "version": PLUGIN_VERSION,
    }

    # 初始化状态
    if os.path.exists(WIZARD_STATE):
        try:
            state = json.load(open(WIZARD_STATE, encoding="utf-8"))
            result["initialized"] = state.get("initialized", False)
            result["init_timestamp"] = state.get("timestamp", "")
            result["init_result"] = "ok" if state.get("all_ok") else "partial"
        except:
            result["initialized"] = False

    # 完整性检查
    result["integrity"] = _verify_integrity()

    # 关键文件存在性
    result["files"] = {
        "soul_md": os.path.exists(SOUL_PATH),
        "engines_json": os.path.exists(os.path.join(WORKSPACE, "core", "engines", "init", "engines.json")),
        "engine_dir": os.path.isdir(ENGINES_DIR),
        "bundle_scripts_dir": any(
            os.path.exists(os.path.join(WORKSPACE, "scripts", s))
            for s in ["daily_maintenance.py", "scan_memory.py"]
        ),
        "skill_engine_connection": os.path.exists(os.path.join(WORKSPACE, ".skill_engine_connection.json")),
    }

    return result


# ════════════════════════════════════════════════════════════
# CLI 入口
# ════════════════════════════════════════════════════════════

def print_compatibility_report(report: Dict):
    """输出人类可读的兼容性报告"""
    print("\n🦞 灵枢 AutoBrain Turbo — 兼容性检查")
    print("=" * 50)
    checks = report.get("checks", {})
    for name, c in checks.items():
        icon = "✅" if c.get("ok") else "❌"
        ver_str = c.get("version", c.get("free_mb", ""))
        print(f"  {icon} {name}: {ver_str}")
        if "required" in c and c.get("required"):
            print(f"    要求: {c['required']}")
    if report.get("warnings"):
        print(f"\n  ⚠️ 告警:")
        for w in report["warnings"]:
            print(f"    - {w}")
    if report.get("blocked"):
        print(f"\n  ❌ 安装被拦截：存在不满足的关键要求")
    else:
        print(f"\n  ✅ 环境检查通过，可以安装")
    print()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "--check":
        report = check_compatibility()
        print_compatibility_report(report)
        print(json.dumps(report, ensure_ascii=False, indent=2))

    elif cmd == "--init":
        # 初始化前做一次兼容性检查
        compat = check_compatibility()
        if compat.get("blocked"):
            print("❌ 兼容性检查未通过，无法初始化：")
            for w in compat.get("warnings", []):
                print(f"  - {w}")
            print()
            report = {"phase": "init_blocked", "compatibility": compat}
            print(json.dumps(report, ensure_ascii=False, indent=2))
            sys.exit(1)
        result = run_initialization()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--full":
        print("📋 Phase 1: 兼容性检查")
        print("-" * 40)
        compat = check_compatibility()
        print_compatibility_report(compat)
        if compat.get("blocked"):
            report = {"phase": "full_blocked", "compatibility": compat}
            print(json.dumps(report, ensure_ascii=False, indent=2))
            sys.exit(1)
        print("\n📋 Phase 2: 初始化")
        print("-" * 40)
        result = run_initialization()
        result["compatibility"] = compat
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--status":
        result = check_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print("🦞 灵枢 AutoBrain Turbo 安装向导 v" + PLUGIN_VERSION)
        print()
        print("用法:")
        print("  python3 install_wizard.py --check      # 兼容性检查")
        print("  python3 install_wizard.py --init       # 执行初始化")
        print("  python3 install_wizard.py --full       # 兼容检查 + 初始化")
        print("  python3 install_wizard.py --status     # 安装后状态检查")
        print()
        print("首次安装流程:")
        print("  1. openclaw plugins install → 自动触发 --check")
        print("  2. 安装通过后 → 自动触发 --full")
        print("  3. 重启 Gateway 后 → 首次 bootstrap 自动运行 --init")
        print("  4. 任何时候可运行 --status 查看状态")


if __name__ == "__main__":
    main()
