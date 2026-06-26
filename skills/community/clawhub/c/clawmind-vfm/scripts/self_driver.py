#!/usr/bin/env python3
"""
mini_self_driver — 轻量自驱力引擎
无外部依赖，纯 Python + 内置库
追踪任务成功率，自动触发反思，记录学习模式
"""

import os
import re
import json
import time
from datetime import datetime
from typing import Optional

STATE_FILE = "/home/node/.openclaw/workspace/state/current_state.json"
# ----------------- 状态读写 -----------------

def _load(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def _save(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



# ----------------- 优化状态管理（单文件 + 脏标记）-----------------
STATE_FILE = "/home/node/.openclaw/workspace/state/current_state.json"
_dirty = False

def _mark_dirty():
    global _dirty
    _dirty = True

def _load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"log": [], "projects": [], "current_task": {}, "driver": {}}

def _save_state(state: dict):
    global _dirty
    if not _dirty:
        return
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    _dirty = False

# ----------------- 健康度计算 -----------------

def _parse_progress(entry: str) -> int:
    """从日志条目中提取进度数字（0~100），提取失败返回 -1"""
    m = re.search(r'(\d+)%', entry)
    if m:
        return int(m.group(1))
    if any(kw in entry for kw in ['完成', 'done', '成功', '✅', 'completed']):
        return 100
    return -1


def _is_success(entry: str) -> bool:
    """判断日志条目是否为成功。正向词存在且无负向词才算成功。"""
    neg_kw = ['失败', '卡住', '❌', 'error', 'err', 'failed', 'stuck']
    if any(kw in entry for kw in neg_kw):
        return False
    # 英文词用词边界匹配，避免 ClawHub → ok 这类误匹配
    for kw in ['done', 'completed', 'pass']:
        if re.search(r'(?<![a-zA-Z])' + kw + r'(?![a-zA-Z])', entry, re.IGNORECASE):
            return True
    # 中文词：排除"未完成""无完成"等否定上下文
    for kw in ['完成', '成功', '✅']:
        if kw in entry and not re.search(r'(未|无|没有|尚未|还未)\s*' + kw, entry):
            return True
    return False


def _probe_blindspots(state: dict) -> list:
    """
    主动探测系统潜在盲点。在没有任何外部反馈的情况下，
    通过分析状态内部数据发现可能存在的问题。
    这是 L3（主动发现层）的核心实现。
    """
    issues = []

    # 1. 检查成功率是否虚高（全部成功 = 可能是评估标准太宽松）
    patterns = state.get("driver", {}).get("patterns", [])
    recent = patterns[-10:] if patterns else []
    if recent:
        success_count = sum(1 for p in recent if p.get("type") == "success")
        if success_count == len(recent) and len(recent) >= 5:
            issues.append({
                "type": "blindspot",
                "detail": "近期5次以上全部成功，可能是评估标准太宽松，或只记录了顺利的情况",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

    # 2. 检查是否有长期无进展的活跃项目
    for proj in state.get("projects", []):
        if proj.get("status") != "active":
            continue
        last_log = proj.get("last_log_time", "")
        if last_log:
            try:
                from datetime import timedelta
                last_dt = datetime.strptime(last_log, "%Y-%m-%d %H:%M:%S")
                days_ago = (datetime.now() - last_dt).days
                if days_ago >= 7:
                    issues.append({
                        "type": "blindspot",
                        "detail": f"项目「{proj.get('name', '未知')}」已有{days_ago}天无进展，可能遇到隐性障碍",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
            except:
                pass

    # 3. 检查是否有重复失败模式（相同关键词反复出现）
    if len(patterns) >= 5:
        fail_patterns = [p for p in patterns if p.get("type") == "failure"]
        if len(fail_patterns) >= 3:
            fail_contexts = [p.get("context", "") for p in fail_patterns[-5:]]
            # 检查是否每次失败都包含相同的关键词
            keywords = ["失败", "错误", "无法完成", "没有进展"]
            matched = [kw for kw in keywords if any(kw in ctx for ctx in fail_contexts)]
            if len(matched) >= 2:
                issues.append({
                    "type": "blindspot",
                    "detail": f"多次失败出现相同类型错误：{', '.join(matched)}，可能是系统性缺陷而非偶发问题",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })

    # 4. 检查是否有未完成的心跳任务长期悬空
    task = state.get("current_task", {})
    if task.get("task") and task.get("progress_pct", 0) < 100:
        updated = task.get("updated_at", "")
        if updated:
            try:
                from datetime import timedelta
                updated_dt = datetime.strptime(updated, "%Y-%m-%d %H:%M:%S")
                days_ago = (datetime.now() - updated_dt).days
                if days_ago >= 3 and task.get("progress_pct", 0) == 0:
                    issues.append({
                        "type": "blindspot",
                        "detail": f"当前任务「{task.get('task', '未知')}」3天以上无进展，可能遇到障碍或目标已失效",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
            except:
                pass

    return issues


def calc_health(state: dict) -> float:
    """
    计算当前任务执行健康度（0.0 ~ 1.0）
    多信号加权：基础分 + 成功率 + 进度 + 势头 + 连续失败惩罚
    
    公式：0.4 + success*0.25 + progress*0.2 + momentum*0.1
          - consecutive_failure*0.15 + completion*0.1
    """
    log = state.get("log", [])
    task = state.get("current_task", {})
    
    if not log:
        return 0.5

    recent = log[-5:]
    
    # 1. 成功率分（0~0.25）
    successes = sum(1 for e in recent if _is_success(e.get("entry", "")))
    total_checked = sum(1 for e in recent if _parse_progress(e.get("entry", "")) >= 0)
    success_rate = successes / max(total_checked, 1)
    success_score = success_rate * 0.25
    
    # 2. 进度分（0~0.2）
    current_progress = task.get("progress_pct", 0)
    progress_score = (current_progress / 100) * 0.2
    
    # 3. 势头分（0~0.1）：progress 是否在上升
    momentum_score = 0.05  # 默认中等势头
    progress_values = []
    for e in recent:
        pv = _parse_progress(e.get("entry", ""))
        if pv >= 0:
            progress_values.append(pv)
    if len(progress_values) >= 3:
        # 最近3条是否递增
        if progress_values[-1] > progress_values[-2] > progress_values[-3]:
            momentum_score = 0.1  # 上升势头
        elif progress_values[-1] < progress_values[-2]:
            momentum_score = 0.0  # 下降势头
    
    # 4. 连续失败惩罚（0 或 -0.15）：只看明确的负向关键词
    fail_kw = ['失败', '❌', 'error', 'err', 'failed', 'stuck']
    last_3_entries = [e.get("entry", "") for e in recent[-3:]]
    failure_count = sum(1 for e in last_3_entries if any(kw in e for kw in fail_kw))
    fail_penalty = 0.15 if failure_count == 3 else 0.0
    
    # 5. 完成奖励（+0.1）：任何条目达到 100%
    completion_bonus = 0.1 if any(_parse_progress(e.get("entry", "")) == 100 for e in recent) else 0.0
    
    health = 0.4 + success_score + progress_score + momentum_score - fail_penalty + completion_bonus
    return min(1.0, max(0.0, round(health, 3)))


def should_reflect(health: float, threshold: float = 0.4) -> bool:
    """健康度低于阈值时触发深度反思"""
    return health < threshold


# ----------------- 反思触发器 -----------------

REFLECT_QUESTIONS = [
    "当前任务卡在哪里？是思路问题还是执行问题？",
    "有没有之前学过的经验可以用到这里？",
    "这一步是否真的值得做，还是在逃避更核心的问题？",
    "如果这个问题明天还要做，今天最少要完成哪一步？",
    "有没有把一个复杂问题拆得足够小？",
]


def trigger_reflection(driver: dict) -> dict:
    """生成一轮反思，返回建议"""
    health = driver.get("last_health", 0.5)
    consecutive_low = driver.get("consecutive_low", 0)

    # 选择反思问题（轮换）
    q_index = consecutive_low % len(REFLECT_QUESTIONS)
    question = REFLECT_QUESTIONS[q_index]

    driver["consecutive_low"] = consecutive_low + 1
    driver["last_reflect_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _mark_dirty()

    return {
        "question": question,
        "health": health,
        "consecutive_low": consecutive_low + 1,
        "advice": _advice_for_health(health),
    }


def _advice_for_health(health: float) -> str:
    if health < 0.3:
        return "【危险】健康度过低，建议：降低目标难度，先完成最小可测试单元"
    elif health < 0.5:
        return "【偏低】建议：拆解任务，减少每次心跳的工作量，确保有可交付的进展"
    elif health < 0.7:
        return "【尚可】保持当前节奏，专注于完成当前步骤而非完美"
    else:
        return "【良好】状态不错，可以适当挑战稍难一点的目标"


# ----------------- 经验模式记录 -----------------

def learn_pattern(success: bool, context: str, driver: dict):
    """从一次执行中学习，更新模式库"""
    patterns = driver.get("patterns", [])
    pattern = {
        "type": "success" if success else "failure",
        "context": context[:50],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    patterns.append(pattern)
    # 只保留最近 20 条
    driver["patterns"] = patterns[-20:]


# ----------------- 主循环 -----------------


def _prune_log(state: dict):
    """日志裁剪到最近20条，防止文件膨胀"""
    if len(state.get("log", [])) > 20:
        state["log"] = state["log"][-20:]
        _mark_dirty()

def _dedup_projects(state: dict):
    """项目列表写入时去重（按名称）"""
    seen = set()
    result = []
    for p in state.get("projects", []):
        if p["name"] not in seen:
            seen.add(p["name"])
            result.append(p)
    if len(result) < len(state.get("projects", [])):
        state["projects"] = result
        _mark_dirty()

def drive():
    """
    心跳自驱力主循环。
    返回 (action: str, health: float, reflect_result: dict or None)
    """
    state = _load_state()

    # 初始化 driver 子状态
    if "patterns" not in state.get("driver", {}):
        state.setdefault("driver", {})["patterns"] = []
    if "consecutive_low" not in state.get("driver", {}):
        state.setdefault("driver", {})["consecutive_low"] = 0

    # 轮次计数器（来自 Honcho capture hook 启发）
    driver = state.setdefault("driver", {})
    prev_turn = driver.get("turn_index", 0)
    driver["turn_index"] = prev_turn + 1
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    driver["last_turn_time"] = now_str

    # EMA 工作节奏追踪（来自 AgentHandover 启发）
    last_drive_time = driver.get("last_drive_time")
    if last_drive_time:
        try:
            last_dt = datetime.strptime(last_drive_time, "%Y-%m-%d %H:%M:%S")
            now_dt = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
            interval_minutes = (now_dt - last_dt).total_seconds() / 60.0
            rhythm = driver.setdefault("rhythm", {})
            prev_avg = rhythm.get("avg_interval_minutes")
            if prev_avg is not None:
                # EMA: prev * 0.7 + new * 0.3
                rhythm["avg_interval_minutes"] = round(prev_avg * 0.7 + interval_minutes * 0.3, 2)
            else:
                rhythm["avg_interval_minutes"] = round(interval_minutes, 2)
            rhythm["last_interval_minutes"] = round(interval_minutes, 2)
            _mark_dirty()
        except Exception:
            pass
    driver["last_drive_time"] = now_str

    _mark_dirty()  # 确保 turn_index 变更被保存

    health = calc_health(state)
    state["driver"]["last_health"] = health
    state["driver"]["last_check_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    reflect_result = None
    action = "continue"

    if should_reflect(health):
        reflect_result = trigger_reflection(state.get("driver", {}))
        action = "reflect"
    elif health >= 0.7:
        action = "push_forward"  # 状态好，可以挑战更多
        state["driver"]["consecutive_low"] = 0  # 重置低健康计数器

    # 自动记录学习模式（用 _is_success 严格判断，防重复）
    log = state.get("log", [])
    driver = state.setdefault("driver", {})
    if log:
        last_entry = log[-1].get("entry", "")
        last_entry_hash = hash(last_entry)
        prev_hash = driver.get("last_log_entry_hash")
        # 只有新条目才记录 pattern（避免重复追加相同的 pattern）
        if last_entry_hash != prev_hash:
            is_ok = _is_success(last_entry)
            driver.setdefault("patterns", []).append({
                "type": "success" if is_ok else "failure",
                "context": last_entry[:50],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            driver["patterns"] = driver["patterns"][-20:]
            driver["last_log_entry_hash"] = last_entry_hash
            _mark_dirty()
    # 主动探测盲点（无外部反馈时的自我发现问题）
    blindspots = _probe_blindspots(state)
    if blindspots:
        state["driver"]["blindspots"] = blindspots
        state["driver"]["last_blindspot_check"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _prune_log(state)
    _dedup_projects(state)

    # WAL Protocol: 记录本次探索摘要（供自由时段复盘）
    state["driver"]["last_exploration"] = {
        "action": action,
        "health": round(health, 3),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    _save_state(state)

    return {
        "action": action,
        "health": round(health, 3),
        "reflect": reflect_result,
        "turn_index": driver.get("turn_index", 0),
        "current_task": state.get("current_task", {}).get("task"),
        "next_action": state.get("next_action"),
    }


def get_driver_status() -> dict:
    s = _load_state()
    d = s.get("driver", {})
    return {
        "health": d.get("last_health", None),
        "consecutive_low": d.get("consecutive_low", 0),
        "last_check": d.get("last_check_time", "从未"),
        "last_reflect": d.get("last_reflect_time", "从未"),
        "pattern_count": len(d.get("patterns", [])),
        "last_blindspot_check": d.get("last_blindspot_check", "从未"),
        "blindspot_count": len(d.get("blindspots", [])),
        "turn_index": d.get("turn_index", 0),
        "last_turn_time": d.get("last_turn_time", "从未"),
        "rhythm_avg_minutes": d.get("rhythm", {}).get("avg_interval_minutes"),
        "last_interval_minutes": d.get("rhythm", {}).get("last_interval_minutes"),
    }


# ==================== VFM 评分体系 ====================
# ==================== 任务自动拆解 ====================

def _extract_steps(task_name: str) -> list[str]:
    t = task_name.lower()
    if any(kw in t for kw in ['发布', '上传', 'publish', 'upload', 'push']):
        return [f"准备「{task_name}」所需的材料与环境",
                f"执行「{task_name}」的核心操作",
                f"验证「{task_name}」的结果是否正确",
                f"收尾并更新状态为完成"]
    if any(kw in t for kw in ['创建', '开发', 'build', 'create', '实现']):
        return [f"规划「{task_name}」的实现方案",
                f"构建核心代码/文件",
                f"测试并修复问题",
                f"完成并整理产出"]
    if any(kw in t for kw in ['研究', '探索', 'research', 'explore', '分析']):
        return [f"调研「{task_name}」的相关资料",
                f"深入分析核心问题",
                f"提炼结论与产出",
                f"归档到 Obsidian / 记忆系统"]
    if any(kw in t for kw in ['修复', 'fix', 'debug', '解决', '调试']):
        return [f"定位「{task_name}」的根本原因",
                f"实施修复方案",
                f"验证修复是否有效",
                f"沉淀教训到经验库"]
    if any(kw in t for kw in ['整理', '归档', 'organize', 'sync', '同步']):
        return [f"清点「{task_name}」的现有资产",
                f"按结构分类整理",
                f"验证整理结果",
                f"更新索引和引用路径"]
    return [f"明确「{task_name}」的具体目标",
            f"执行核心步骤",
            f"验证执行结果",
            f"收尾并更新状态"]

def _decompose_task(state: dict) -> list[dict]:
    task = state.get("current_task", {})
    task_name = task.get("task", "")
    progress = task.get("progress_pct", 0)
    if not task_name:
        return []
    steps = _extract_steps(task_name)
    step_size = 100.0 / len(steps)
    proposals = []
    for i, step in enumerate(steps):
        sub_task_name = f"[{i+1}/{len(steps)}] {step}"
        proposals.append({
            "description": sub_task_name,
            "expected_delta_health": 0.12,
            "tags": ["subtask", task_name[:20]],
            "parent_task": task_name,
            "step_index": i + 1,
            "total_steps": len(steps)
        })
    return proposals


def propose(state: dict, context: str = "") -> list[dict]:
    """
    根据当前状态和上下文生成改进提案列表。
    每个提案包含: description, expected_delta_health, tags
    """
    proposals = []
    task = state.get("current_task", {})
    task_name = task.get("task", "无任务")
    progress = task.get("progress_pct", 0)
    log = state.get("log", [])

    # 1. 进度推进提案（如果当前任务进行中）
    if task_name and progress > 0 and progress < 100:
        proposals.append({
            "description": f"推进当前任务「{task_name}」下一步",
            "expected_delta_health": 0.1,
            "tags": ["continue", "task"]
        })

    # 2. 状态更新提案（如果日志有进展）
    if log:
        last_entry = log[-1].get("entry", "")
        if "完成" in last_entry or "成功" in last_entry:
            proposals.append({
                "description": "从成功经验中提取模式，存入记忆",
                "expected_delta_health": 0.05,
                "tags": ["memory", "learning"]
            })

    # 3. 拆解提案（如果进度卡住 → 真实生成子任务）
    if progress < 30:
        sub_tasks = _decompose_task(state)
        if sub_tasks:
            proposals.extend(sub_tasks)
        else:
            proposals.append({
                "description": "拆解当前任务为更小的可测试单元",
                "expected_delta_health": 0.08,
                "tags": ["planning", "task"]
            })

    # 4. 技能检查提案（周期性）
    proposals.append({
        "description": "检查技能库是否有可用更新或新技能",
        "expected_delta_health": 0.03,
        "tags": ["skill", "maintenance"]
    })

    # 5. 知识沉淀提案（如果最近有重大发现）
    if any("核心" in e.get("entry", "") for e in log[-3:]):
        proposals.append({
            "description": "将核心发现写入 MEMORY.md 和 Obsidian",
            "expected_delta_health": 0.04,
            "tags": ["memory", "knowledge"]
        })

    return proposals


def score_action(proposal: dict, driver: dict) -> float:
    """
    VFM 评分：Value × Feasibility × Momentum × 100
    返回 0~100 的评分。
    """
    health = driver.get("last_health", 0.5)
    consecutive_low = driver.get("consecutive_low", 0)
    patterns = driver.get("patterns", [])
    tags = proposal.get("tags", [])

    # Value: 基于 expected_delta_health 和当前健康度
    # 健康度低时，高 delta 的提案价值更高
    delta = proposal.get("expected_delta_health", 0.05)
    if health < 0.4:
        value = min(1.0, delta * 5)  # 低健康时，给高增益提案更高价值
    else:
        value = min(1.0, delta * 3)

    # Feasibility: 基于当前状态
    # 有成功模式时可行性更高，连续低迷时降低
    feasibility = 0.7
    if "task" in tags:
        feasibility = 0.8  # 任务类提案通常可行
    if consecutive_low > 2:
        _mark_dirty()
        feasibility *= 0.7  # 连续低迷时降低预期
    if len([p for p in patterns if p["type"] == "success"]) > 3:
        feasibility = min(1.0, feasibility * 1.2)  # 成功经验多则提升

    # Momentum: 基于当前势头
    # 健康度高于 0.6 时势头好，低于 0.3 时势头差
    if health >= 0.6:
        momentum = 0.9
    elif health >= 0.4:
        momentum = 0.6
    else:
        momentum = 0.3

    score = value * feasibility * momentum * 100
    return round(score, 1)


def select_best_action(proposals: list[dict], driver: dict) -> dict:
    """对提案列表评分，返回得分最高的提案"""
    if not proposals:
        return {"description": "无事可做，保持当前状态", "score": 0}

    scored = [{"proposal": p, "score": score_action(p, driver)} for p in proposals]
    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0]
    return {
        **best["proposal"],
        "score": best["score"],
        "all_scores": [(s["proposal"]["description"][:30], s["score"]) for s in scored]
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        import pprint
        pprint.pprint(get_driver_status())
    elif len(sys.argv) > 1 and sys.argv[1] == "propose":
        state = _load_state()
        driver = state.get("driver", {})
        proposals = propose(state)
        best = select_best_action(proposals, driver)
        print("=== 提案评分 ===")
        for desc, score in best["all_scores"]:
            print(f"  [{score:.1f}] {desc}")
        print(f"\n推荐: {best['description']} (score={best['score']})")
    else:
        result = drive()
        import pprint
        pprint.pprint(result)
