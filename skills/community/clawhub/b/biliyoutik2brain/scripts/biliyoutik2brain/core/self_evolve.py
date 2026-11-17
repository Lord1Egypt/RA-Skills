"""
技能自进化系统 (v1.0)

每次管线运行后记录指标，累积分析后自动调优参数。

进化维度:
  - 模型选择: tiny/base/small 根据历史质量/速度自动选择
  - 置信度阈值: 根据历史低置信率动态调整
  - 分块大小: 根据LLM token消耗调整
  - 错误模式: 检测重复失败 → 推荐修复策略

日志存储: ~/.biliyoutik2brain/evolution_log.json
"""

import os, json, time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════
#  日志记录
# ═══════════════════════════════════════════════════════════════

LOG_FILE = os.path.expanduser("~/.biliyoutik2brain/evolution_log.json")


def log_run(
    video_id: str,
    uploader: str,
    duration_s: int,
    asr_engine: str,
    asr_model: str,
    chars: int,
    confidence: float,
    low_conf_ratio: float,
    llm_backend: str,
    llm_calls: int,
    llm_tokens: int,
    chunks: int,
    elapsed_s: float,
    asr_elapsed_s: float = 0,
    error: str = "",
):
    """记录一次管线运行"""
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "video_id": video_id,
        "uploader": uploader,
        "duration_s": duration_s,
        "asr_engine": asr_engine,
        "asr_model": asr_model,
        "chars": chars,
        "confidence": confidence,
        "low_conf_ratio": low_conf_ratio,
        "llm_backend": llm_backend,
        "llm_calls": llm_calls,
        "llm_tokens": llm_tokens,
        "chunks": chunks,
        "elapsed_s": elapsed_s,
        "asr_elapsed_s": asr_elapsed_s,
        "error": error,
        # 计算指标
        "speed_factor": round(duration_s / max(elapsed_s, 0.1), 2),  # >1 = 快于实时
        "chars_per_second": round(chars / max(elapsed_s - asr_elapsed_s, 0.1), 1),
        "cost_estimate": round(llm_tokens * 0.000001, 6) if llm_tokens > 0 else 0,
    }

    _append_log(entry)
    print(f"  [进化] 📊 已记录运行 #{len(_load_logs())}")


def _append_log(entry: Dict):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    logs = _load_logs()
    logs.append(entry)
    logs = logs[-200:]  # 保留最近200条
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def _load_logs() -> List[Dict]:
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE) as f:
            return json.load(f)
    except Exception:
        return []


# ═══════════════════════════════════════════════════════════════
#  自我分析
# ═══════════════════════════════════════════════════════════════

def analyze() -> Dict:
    """分析历史日志，输出建议"""
    logs = _load_logs()
    if not logs:
        return {"status": "no_data", "message": "尚无运行记录"}

    recent = logs[-20:]  # 最近20次
    total = len(logs)

    # 基础统计
    successful = [l for l in recent if not l.get("error")]
    failed = [l for l in recent if l.get("error")]

    analysis = {
        "status": "ok",
        "total_runs": total,
        "recent_runs": len(recent),
        "success_rate": f"{len(successful)}/{len(recent)}" + (f"({len(successful)/max(len(recent),1)*100:.0f}%)" if recent else ""),
        "failures": len(failed),
    }

    if successful:
        avg_speed = sum(l["speed_factor"] for l in successful) / len(successful)
        avg_conf = sum(l["confidence"] for l in successful) / len(successful)
        avg_chars = sum(l["chars"] for l in successful) / len(successful)
        total_cost = sum(l.get("cost_estimate", 0) for l in successful)
        total_tokens = sum(l.get("llm_tokens", 0) for l in successful)

        analysis.update({
            "avg_speed": f"{avg_speed:.2f}x实时",
            "avg_confidence": round(avg_conf, 3),
            "avg_chars": round(avg_chars, 0),
            "total_cost": f"¥{total_cost:.6f}",
            "total_llm_tokens": total_tokens,
        })

    # 模型对比
    model_stats = {}
    for l in successful:
        key = f"{l.get('asr_model', '?')}/{l.get('llm_backend', '?')}"
        if key not in model_stats:
            model_stats[key] = {"runs": 0, "total_speed": 0, "total_conf": 0}
        model_stats[key]["runs"] += 1
        model_stats[key]["total_speed"] += l["speed_factor"]
        model_stats[key]["total_conf"] += l["confidence"]

    for key, stats in model_stats.items():
        stats["avg_speed"] = round(stats["total_speed"] / stats["runs"], 2)
        stats["avg_conf"] = round(stats["total_conf"] / stats["runs"], 3)

    analysis["model_comparison"] = model_stats

    # 错误模式
    error_patterns = {}
    for l in failed:
        err = l.get("error", "unknown")
        error_patterns[err] = error_patterns.get(err, 0) + 1
    if error_patterns:
        analysis["error_patterns"] = error_patterns

    return analysis


# ═══════════════════════════════════════════════════════════════
#  自动调优
# ═══════════════════════════════════════════════════════════════

def auto_tune(base_model: str = "base", base_threshold: float = 0.6) -> Tuple[str, float]:
    """基于历史数据自动调优参数

    返回: (推荐模型, 推荐置信度阈值)
    """
    logs = _load_logs()
    recent = logs[-20:]

    if len(recent) < 3:
        return base_model, base_threshold  # 数据不够, 用默认

    successful = [l for l in recent if not l.get("error")]
    if len(successful) < 3:
        return base_model, base_threshold

    # 模型选择: 如果 base 模型的 speed_factor < 0.5 (太慢), 降级到 tiny
    base_runs = [l for l in successful if l.get("asr_model") == "base"]
    if base_runs:
        avg_base_speed = sum(l["speed_factor"] for l in base_runs) / len(base_runs)
        if avg_base_speed < 0.5:
            base_model = "tiny"
            print(f"  [进化/调优] base模型太慢({avg_base_speed:.2f}x), 降级到tiny")
        elif avg_base_speed > 2.0:
            base_model = "small"
            print(f"  [进化/调优] base模型有余力({avg_base_speed:.2f}x), 升级到small")

    # 置信度阈值: 如果历史低置信率 < 5%, 可以提高阈值来减少LLM调用
    avg_low_conf = sum(l.get("low_conf_ratio", 0) for l in successful) / len(successful)
    if avg_low_conf < 0.03:
        base_threshold = 0.5  # 更宽松
        print(f"  [进化/调优] 低置信率仅{avg_low_conf:.1%}, 阈值调至0.5(省LLM)")
    elif avg_low_conf > 0.1:
        base_threshold = 0.7  # 更严格
        print(f"  [进化/调优] 低置信率{avg_low_conf:.1%}, 阈值调至0.7(更安全)")

    return base_model, base_threshold


# ═══════════════════════════════════════════════════════════════
#  诊断报告
# ═══════════════════════════════════════════════════════════════

def report() -> str:
    """生成自进化报告"""
    analysis = analyze()
    model, threshold = auto_tune()

    lines = ["自进化报告", "=" * 45]

    if analysis.get("status") == "no_data":
        lines.append("尚无运行记录，3次运行后开始进化。")
        return "\n".join(lines)

    lines.append(f"总运行: {analysis['total_runs']}次")
    lines.append(f"成功率: {analysis['success_rate']}")
    lines.append(f"平均速度: {analysis.get('avg_speed', 'N/A')}")
    lines.append(f"平均置信度: {analysis.get('avg_confidence', 'N/A')}")
    lines.append(f"累计LLM费用: {analysis.get('total_cost', 'N/A')}")
    lines.append(f"累计Tokens: {analysis.get('total_llm_tokens', 0)}")

    if analysis.get("error_patterns"):
        lines.append(f"\n错误模式:")
        for err, count in analysis["error_patterns"].items():
            lines.append(f"  {err}: {count}次")

    if analysis.get("model_comparison"):
        lines.append(f"\n模型对比:")
        for key, stats in analysis["model_comparison"].items():
            lines.append(f"  {key}: {stats['runs']}次, 速度{stats['avg_speed']}x, 置信{stats['avg_conf']}")

    lines.append(f"\n推荐参数: ASR={model}, 阈值={threshold}")
    return "\n".join(lines)
