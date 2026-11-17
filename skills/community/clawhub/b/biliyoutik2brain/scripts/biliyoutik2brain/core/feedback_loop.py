"""
BiliYouTik2Brain — 反馈闭环 (v4.0)

独立于 corrector_engine 的反馈闭环模块。
收集用户对转录/分析的反馈，回流到知识库和 lessons.md。

闭环路径:
  用户评分/纠错 → 题型模式库 → 高置信追加 lessons.md → 下次修正自动应用
"""

import os, json, time
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from .corrector_engine.feedback import feedback_loop as _engine_feedback


# ═══════════════════════════════════════════════════════════
#  数据模型
# ═══════════════════════════════════════════════════════════

@dataclass
class UserFeedback:
    """用户反馈条目"""
    bvid: str
    video_title: str = ""
    uploader: str = ""
    # 转录评分（1-5）
    transcription_score: Optional[int] = None
    # 分析评分（1-5）
    analysis_score: Optional[int] = None
    # 纠错（用户手动修正）
    corrections: List[Dict] = field(default_factory=list)
    # 自由文本备注
    notes: str = ""
    # 元信息
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class FeedbackStats:
    """反馈统计（跨会话累积）"""
    total_videos: int = 0
    avg_transcription: float = 0.0
    avg_analysis: float = 0.0
    total_corrections: int = 0
    correction_accuracy: float = 0.0  # 用户纠错被采纳的比例


# ═══════════════════════════════════════════════════════════
#  存储路径
# ═══════════════════════════════════════════════════════════

_FEEDBACK_DIR = os.path.expanduser("~/.biliyoutik2brain/feedback")
_STATS_PATH = os.path.join(_FEEDBACK_DIR, "stats.json")


def _ensure_dir():
    os.makedirs(_FEEDBACK_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════
#  用户反馈收集
# ═══════════════════════════════════════════════════════════

def record_user_feedback(fb: UserFeedback):
    """
    记录用户反馈。

    同时触发两个回流:
    1. 题型模式库: 用户纠错 → 下次自动修正
    2. lessons.md: 高置信规则 → 跨会话生效
    """
    _ensure_dir()
    feedback_file = os.path.join(_FEEDBACK_DIR, f"{fb.bvid}.json")

    # 合并已有反馈（同一视频可能多次反馈）
    existing = {}
    if os.path.exists(feedback_file):
        with open(feedback_file, encoding="utf-8") as f:
            existing = json.load(f)

    existing.update({
        "bvid": fb.bvid,
        "video_title": fb.video_title or existing.get("video_title", ""),
        "uploader": fb.uploader or existing.get("uploader", ""),
        "transcription_score": fb.transcription_score or existing.get("transcription_score"),
        "analysis_score": fb.analysis_score or existing.get("analysis_score"),
        "corrections": (existing.get("corrections", []) + fb.corrections)[-100:],
        "notes": fb.notes or existing.get("notes", ""),
        "timestamp": fb.timestamp,
    })

    with open(feedback_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    # 用户纠错 → 回流到正确器引擎的反馈闭环
    if fb.corrections:
        _engine_feedback(fb.corrections, fb.bvid)

    # 更新统计
    _update_stats(fb)


def get_feedback(bvid: str) -> Optional[Dict]:
    """获取某视频的反馈记录"""
    feedback_file = os.path.join(_FEEDBACK_DIR, f"{bvid}.json")
    if not os.path.exists(feedback_file):
        return None
    with open(feedback_file, encoding="utf-8") as f:
        return json.load(f)


def list_all_feedback(limit: int = 50) -> List[Dict]:
    """列出所有反馈记录"""
    _ensure_dir()
    results = []
    for fname in sorted(os.listdir(_FEEDBACK_DIR), reverse=True):
        if not fname.endswith(".json") or fname == "stats.json":
            continue
        with open(os.path.join(_FEEDBACK_DIR, fname), encoding="utf-8") as f:
            results.append(json.load(f))
        if len(results) >= limit:
            break
    return results


# ═══════════════════════════════════════════════════════════
#  统计分析
# ═══════════════════════════════════════════════════════════

def get_stats() -> FeedbackStats:
    """获取累计反馈统计"""
    if not os.path.exists(_STATS_PATH):
        return FeedbackStats()
    with open(_STATS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return FeedbackStats(**data)


def _update_stats(fb: UserFeedback):
    """内部: 更新累计统计"""
    stats = get_stats()

    if fb.transcription_score:
        stats.avg_transcription = (
            (stats.avg_transcription * stats.total_videos + fb.transcription_score)
            / (stats.total_videos + 1)
        )
    if fb.analysis_score:
        stats.avg_analysis = (
            (stats.avg_analysis * stats.total_videos + fb.analysis_score)
            / (stats.total_videos + 1)
        )

    stats.total_corrections += len(fb.corrections)
    if fb.transcription_score or fb.analysis_score:
        stats.total_videos += 1

    _ensure_dir()
    with open(_STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats.__dict__, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
#  质量报告
# ═══════════════════════════════════════════════════════════

def generate_quality_report() -> Dict:
    """生成质量报告（供基准测试和发布使用）"""
    stats = get_stats()
    all_fb = list_all_feedback(limit=200)

    scores_t = [f.get("transcription_score") for f in all_fb if f.get("transcription_score")]
    scores_a = [f.get("analysis_score") for f in all_fb if f.get("analysis_score")]

    return {
        "total_feedback": len(all_fb),
        "avg_transcription": round(stats.avg_transcription, 2),
        "avg_analysis": round(stats.avg_analysis, 2),
        "total_corrections": stats.total_corrections,
        "recent_scores": {
            "transcription": scores_t[:10],
            "analysis": scores_a[:10],
        },
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


# ═══════════════════════════════════════════════════════════
#  管线集成接口
# ═══════════════════════════════════════════════════════════

def on_transcription_complete(bvid: str, original: str, corrected: str, confidence: float):
    """
    转录完成后触发: 记录修正结果到反馈数据库。
    由 enhance_engine / corrector_engine 调用。
    """
    corrections = []

    # 对比原文和修正后的差异
    if original != corrected and confidence >= 0.7:
        import difflib
        orig_words = original.split()
        corr_words = corrected.split()
        differ = list(difflib.unified_diff(orig_words, corr_words, n=0))
        for line in differ:
            if line.startswith("- "):
                word = line[2:].strip()
                corrections.append({
                    "original": word,
                    "corrected": "",
                    "source": "auto_diff",
                    "confidence": confidence,
                })
            elif line.startswith("+ "):
                word = line[2:].strip()
                # 配对最后一个 - 条目
                if corrections and not corrections[-1]["corrected"]:
                    corrections[-1]["corrected"] = word

    if corrections:
        record_user_feedback(UserFeedback(
            bvid=bvid,
            corrections=corrections[:20],
        ))
