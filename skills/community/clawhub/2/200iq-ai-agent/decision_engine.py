from roi_monitor import evaluate_roi
from logger import log_journal

def rank_tasks(tasks, min_roi=1.0):
    """Ranks tasks based on expected ROI"""
    ranked = sorted(tasks, key=lambda t: evaluate_roi(t), reverse=True)
    high_roi = [t for t in ranked if evaluate_roi(t) >= min_roi]
    log_journal(f"Ranked tasks: {[t['name'] for t in high_roi]}")
    return high_roi
