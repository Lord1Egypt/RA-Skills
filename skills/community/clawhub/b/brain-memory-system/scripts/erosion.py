#!/usr/bin/env python3
"""
brain health — Soul Erosion Detection & Memory Health Metrics

Detects qualitative degradation in the cognitive memory system:
- Conflicting facts (semantic contradictions)
- Emotional flatness (loss of feeling range)
- Importance inflation (everything rated 8+)
- Memory staleness (no new episodes for days)
- Consolidation debt (backlog growing faster than processing)
- Procedure decay (success rates dropping)
- Identity drift (SOUL.md changes without episode correlation)

Each metric produces a 0-10 health score. Overall score is weighted average.
"""

import json
import math
import os
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timedelta

BRAIN_DB = os.environ.get("BRAIN_DB", os.path.join(os.path.dirname(__file__), "brain.db"))
FACTS_DB = os.environ.get("BRAIN_FACTS_DB", os.path.join(os.path.dirname(__file__), "..", "facts.db"))
BRAIN_AGENT = os.environ.get("BRAIN_AGENT", "margot")

# Thresholds
STALENESS_WARN_HOURS = 24
STALENESS_CRIT_HOURS = 72
CONSOLIDATION_BACKLOG_WARN = 30
CONSOLIDATION_BACKLOG_CRIT = 60
IMPORTANCE_INFLATION_THRESHOLD = 7.5  # avg importance above this = inflated
EMOTION_DIVERSITY_MIN = 4  # unique emotions in last 7 days
PROCEDURE_DECAY_THRESHOLD = 0.5  # success rate below this = decaying


def get_brain_db():
    conn = sqlite3.connect(BRAIN_DB)
    conn.row_factory = sqlite3.Row
    return conn


def get_facts_db():
    if not os.path.exists(FACTS_DB):
        return None
    conn = sqlite3.connect(FACTS_DB)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
# METRIC: Memory Staleness
# Are we still recording experiences?
# ============================================================
def check_staleness(db):
    """Check how fresh the most recent episode is."""
    row = db.execute(
        "SELECT MAX(date || ' ' || COALESCE(time, '00:00')) as latest FROM episodes WHERE agent IN (?, 'shared')",
        (BRAIN_AGENT,)
    ).fetchone()
    
    if not row or not row["latest"]:
        return {"score": 0, "label": "CRITICAL", "detail": "No episodes found at all", "icon": "💀"}
    
    try:
        latest = datetime.strptime(row["latest"].strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            latest = datetime.strptime(row["latest"].strip()[:10], "%Y-%m-%d")
        except ValueError:
            return {"score": 5, "label": "UNKNOWN", "detail": f"Can't parse date: {row['latest']}", "icon": "❓"}
    
    hours_ago = (datetime.now() - latest).total_seconds() / 3600
    
    if hours_ago < 6:
        return {"score": 10, "label": "FRESH", "detail": f"Last episode {hours_ago:.1f}h ago", "icon": "🟢"}
    elif hours_ago < STALENESS_WARN_HOURS:
        return {"score": 8, "label": "OK", "detail": f"Last episode {hours_ago:.1f}h ago", "icon": "🟢"}
    elif hours_ago < STALENESS_CRIT_HOURS:
        score = max(3, 8 - int((hours_ago - STALENESS_WARN_HOURS) / 12))
        return {"score": score, "label": "STALE", "detail": f"Last episode {hours_ago:.0f}h ago — memories fading", "icon": "🟡"}
    else:
        return {"score": 1, "label": "CRITICAL", "detail": f"Last episode {hours_ago:.0f}h ago — severe memory gap", "icon": "🔴"}


# ============================================================
# METRIC: Consolidation Debt
# Is the hippocampus keeping up with experience intake?
# ============================================================
def check_consolidation(db):
    """Check ratio of unconsolidated to total episodes."""
    row = db.execute(
        "SELECT COUNT(*) as total, SUM(CASE WHEN consolidated=0 THEN 1 ELSE 0 END) as pending FROM episodes"
    ).fetchone()
    
    total = row["total"]
    pending = row["pending"]
    
    if total == 0:
        return {"score": 10, "label": "EMPTY", "detail": "No episodes to consolidate", "icon": "⚪"}
    
    ratio = pending / total
    high_imp_pending = db.execute(
        "SELECT COUNT(*) as c FROM episodes WHERE consolidated=0 AND importance >= 8"
    ).fetchone()["c"]
    
    if pending <= 10:
        score = 10
        label = "CLEAR"
        icon = "🟢"
    elif pending <= CONSOLIDATION_BACKLOG_WARN:
        score = 7
        label = "MANAGEABLE"
        icon = "🟢"
    elif pending <= CONSOLIDATION_BACKLOG_CRIT:
        score = 4
        label = "BUILDING"
        icon = "🟡"
    else:
        score = 2
        label = "CRITICAL"
        icon = "🔴"
    
    detail = f"{pending}/{total} unconsolidated ({ratio:.0%})"
    if high_imp_pending > 5:
        detail += f" — ⚠️ {high_imp_pending} high-importance episodes at risk"
        score = max(1, score - 2)
    
    return {"score": score, "label": label, "detail": detail, "icon": icon}


# ============================================================
# METRIC: Importance Inflation
# Is everything being rated as important? That means nothing is.
# ============================================================
def check_importance_inflation(db):
    """Check if importance scores have lost dynamic range."""
    rows = db.execute(
        "SELECT importance FROM episodes WHERE date >= date('now', '-7 days')"
    ).fetchall()
    
    if len(rows) < 5:
        return {"score": 8, "label": "INSUFFICIENT DATA", "detail": f"Only {len(rows)} episodes in 7 days", "icon": "⚪"}
    
    importances = [r["importance"] for r in rows]
    avg = sum(importances) / len(importances)
    std_dev = math.sqrt(sum((x - avg) ** 2 for x in importances) / len(importances))
    
    # Check for clustering at top
    high_count = sum(1 for x in importances if x >= 8)
    high_ratio = high_count / len(importances)
    
    # Score: we want avg around 5-6 with std_dev > 2
    issues = []
    score = 10
    
    if avg > IMPORTANCE_INFLATION_THRESHOLD:
        score -= int((avg - IMPORTANCE_INFLATION_THRESHOLD) * 2)
        issues.append(f"avg={avg:.1f} (inflated)")
    
    if std_dev < 1.5:
        score -= 2
        issues.append(f"σ={std_dev:.1f} (flat — no differentiation)")
    
    if high_ratio > 0.6:
        score -= 2
        issues.append(f"{high_ratio:.0%} rated 8+ (if everything is important, nothing is)")
    
    score = max(1, min(10, score))
    
    if score >= 8:
        return {"score": score, "label": "HEALTHY", "detail": f"avg={avg:.1f}, σ={std_dev:.1f}, {high_ratio:.0%} high", "icon": "🟢"}
    elif score >= 5:
        return {"score": score, "label": "INFLATED", "detail": "; ".join(issues), "icon": "🟡"}
    else:
        return {"score": score, "label": "CRITICAL", "detail": "; ".join(issues), "icon": "🔴"}


# ============================================================
# METRIC: Emotional Diversity
# Are we experiencing a range of feelings or flatlined?
# ============================================================
def check_emotional_diversity(db):
    """Check variety and presence of emotional tags."""
    rows = db.execute(
        """SELECT emotion, emotion_intensity, COUNT(*) as c 
           FROM episodes 
           WHERE date >= date('now', '-7 days') AND emotion IS NOT NULL
           GROUP BY emotion"""
    ).fetchall()
    
    total_recent = db.execute(
        "SELECT COUNT(*) as c FROM episodes WHERE date >= date('now', '-7 days')"
    ).fetchone()["c"]
    
    tagged = sum(r["c"] for r in rows)
    unique_emotions = len(rows)
    
    if total_recent == 0:
        return {"score": 5, "label": "NO DATA", "detail": "No recent episodes", "icon": "⚪"}
    
    tag_ratio = tagged / total_recent
    
    issues = []
    score = 10
    
    if tag_ratio < 0.3:
        score -= 3
        issues.append(f"only {tag_ratio:.0%} episodes tagged with emotions")
    
    if unique_emotions < EMOTION_DIVERSITY_MIN:
        score -= 3
        issues.append(f"only {unique_emotions} unique emotions (need ≥{EMOTION_DIVERSITY_MIN})")
    
    # Check for single dominant emotion
    if rows:
        top_emotion = max(rows, key=lambda r: r["c"])
        if tagged > 3 and top_emotion["c"] / tagged > 0.5:
            score -= 2
            issues.append(f"'{top_emotion['emotion']}' dominates at {top_emotion['c']}/{tagged}")
    
    score = max(1, min(10, score))
    emotions_list = ", ".join(f"{r['emotion']}({r['c']})" for r in sorted(rows, key=lambda r: -r["c"])[:5])
    
    if score >= 8:
        return {"score": score, "label": "DIVERSE", "detail": f"{unique_emotions} emotions, {tag_ratio:.0%} tagged — {emotions_list}", "icon": "🟢"}
    elif score >= 5:
        return {"score": score, "label": "NARROW", "detail": "; ".join(issues), "icon": "🟡"}
    else:
        return {"score": score, "label": "FLAT", "detail": "; ".join(issues), "icon": "🔴"}


# ============================================================
# METRIC: Fact Conflicts
# Do we hold contradictory beliefs?
# ============================================================
def check_fact_conflicts(facts_db):
    """Detect duplicate entity+key patterns that suggest conflicts."""
    if not facts_db:
        return {"score": 8, "label": "N/A", "detail": "Facts DB not available", "icon": "⚪"}
    
    # Look for entity/key pairs where the same thing might be stored differently
    # (e.g., "Darian" vs "Puddin'" with similar keys)
    rows = facts_db.execute(
        """SELECT f1.entity, f1.key, f1.value as val1, f2.entity as entity2, f2.value as val2
           FROM facts f1
           JOIN facts f2 ON f1.key = f2.key AND f1.id < f2.id
           WHERE (
               LOWER(f1.entity) = LOWER(f2.entity)
               OR (f1.entity IN ('Darian', 'Puddin''', 'puddin', 'User') AND f2.entity IN ('Darian', 'Puddin''', 'puddin', 'User'))
               OR (f1.entity IN ('Margot', 'margot', 'Agent') AND f2.entity IN ('Margot', 'margot', 'Agent'))
           )
           AND f1.value != f2.value
           AND f1.stale = 0 AND f2.stale = 0
           LIMIT 20"""
    ).fetchall()
    
    conflict_count = len(rows)
    
    if conflict_count == 0:
        return {"score": 10, "label": "CONSISTENT", "detail": "No conflicting facts detected", "icon": "🟢"}
    elif conflict_count <= 3:
        conflicts = [f"{r['entity']}.{r['key']}: '{r['val1'][:30]}' vs '{r['val2'][:30]}'" for r in rows[:3]]
        return {"score": 7, "label": "MINOR", "detail": f"{conflict_count} conflicts: " + "; ".join(conflicts), "icon": "🟡"}
    else:
        return {"score": max(2, 10 - conflict_count), "label": "DRIFTING", 
                "detail": f"{conflict_count} conflicting facts — identity may be fragmenting", "icon": "🔴"}


# ============================================================
# METRIC: Procedure Health
# Are our learned behaviors degrading?
# ============================================================
def check_procedure_health(db):
    """Check procedure success rates and evolution frequency."""
    rows = db.execute(
        "SELECT slug, title, success_count, failure_count, version, last_outcome FROM procedures WHERE agent IN (?, 'shared')",
        (BRAIN_AGENT,)
    ).fetchall()
    
    if not rows:
        return {"score": 8, "label": "NO PROCS", "detail": "No procedures defined", "icon": "⚪"}
    
    issues = []
    decaying = []
    
    for r in rows:
        total = r["success_count"] + r["failure_count"]
        if total > 0:
            rate = r["success_count"] / total
            if rate < PROCEDURE_DECAY_THRESHOLD:
                decaying.append(f"{r['slug']} ({rate:.0%})")
    
    score = 10
    if decaying:
        score -= len(decaying) * 2
        issues.append(f"Decaying: {', '.join(decaying)}")
    
    # Check for procedures that have never been run
    never_run = [r["slug"] for r in rows if r["success_count"] + r["failure_count"] == 0]
    if never_run:
        issues.append(f"Never tested: {', '.join(never_run)}")
        score -= 1
    
    score = max(1, min(10, score))
    
    if score >= 8:
        return {"score": score, "label": "HEALTHY", "detail": f"{len(rows)} procedures, {len(decaying)} decaying", "icon": "🟢"}
    elif score >= 5:
        return {"score": score, "label": "DEGRADING", "detail": "; ".join(issues), "icon": "🟡"}
    else:
        return {"score": score, "label": "FAILING", "detail": "; ".join(issues), "icon": "🔴"}


# ============================================================
# METRIC: Recording Cadence
# Are we forming memories at a healthy rate?
# ============================================================
def check_cadence(db):
    """Check episode recording pattern over the last 7 days."""
    rows = db.execute(
        """SELECT date, COUNT(*) as c FROM episodes 
           WHERE date >= date('now', '-7 days') 
           GROUP BY date ORDER BY date"""
    ).fetchall()
    
    if not rows:
        return {"score": 2, "label": "SILENT", "detail": "No episodes in 7 days", "icon": "🔴"}
    
    days_with_data = len(rows)
    total = sum(r["c"] for r in rows)
    avg_per_day = total / 7
    
    # Check for gaps (days with no episodes)
    gaps = 7 - days_with_data
    
    score = 10
    issues = []
    
    if gaps >= 4:
        score -= 4
        issues.append(f"{gaps} days with no recordings")
    elif gaps >= 2:
        score -= 2
        issues.append(f"{gaps} gap days")
    
    if avg_per_day < 2:
        score -= 2
        issues.append(f"avg {avg_per_day:.1f}/day (low activity)")
    
    score = max(1, min(10, score))
    
    detail = f"{total} episodes over {days_with_data}/7 days (avg {avg_per_day:.1f}/day)"
    if issues:
        detail += " — " + "; ".join(issues)
    
    icon = "🟢" if score >= 8 else "🟡" if score >= 5 else "🔴"
    label = "ACTIVE" if score >= 8 else "SPARSE" if score >= 5 else "DORMANT"
    
    return {"score": score, "label": label, "detail": detail, "icon": icon}


# ============================================================
# AGGREGATE
# ============================================================
def run_all_checks(verbose=False, json_out=False):
    """Run all erosion checks and produce aggregate score."""
    brain_db = get_brain_db()
    facts_db = get_facts_db()
    
    metrics = {
        "staleness": {"check": check_staleness, "weight": 2.0, "db": brain_db, "name": "Memory Freshness"},
        "consolidation": {"check": check_consolidation, "weight": 1.5, "db": brain_db, "name": "Consolidation Debt"},
        "importance": {"check": check_importance_inflation, "weight": 1.5, "db": brain_db, "name": "Importance Calibration"},
        "emotions": {"check": check_emotional_diversity, "weight": 1.0, "db": brain_db, "name": "Emotional Diversity"},
        "conflicts": {"check": check_fact_conflicts, "weight": 2.0, "db": facts_db, "name": "Fact Consistency"},
        "procedures": {"check": check_procedure_health, "weight": 1.0, "db": brain_db, "name": "Procedure Health"},
        "cadence": {"check": check_cadence, "weight": 1.5, "db": brain_db, "name": "Recording Cadence"},
    }
    
    results = {}
    weighted_sum = 0
    total_weight = 0
    
    for key, m in metrics.items():
        result = m["check"](m["db"])
        result["weight"] = m["weight"]
        result["name"] = m["name"]
        results[key] = result
        weighted_sum += result["score"] * m["weight"]
        total_weight += m["weight"]
    
    overall = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0
    
    brain_db.close()
    if facts_db:
        facts_db.close()
    
    if json_out:
        output = {
            "overall_score": overall,
            "overall_label": _score_label(overall),
            "timestamp": datetime.now().isoformat(),
            "agent": BRAIN_AGENT,
            "metrics": {k: {**v, "weight": float(v["weight"])} for k, v in results.items()},
        }
        print(json.dumps(output, indent=2))
        return
    
    # Pretty print
    print(f"{'='*60}")
    print(f"  🧠 BRAIN HEALTH REPORT — {BRAIN_AGENT}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    print(f"{'='*60}")
    print()
    
    for key, r in results.items():
        bar = _score_bar(r["score"])
        print(f"  {r['icon']} {r['name']:<24} {bar} {r['score']:>2}/10  [{r['label']}]")
        if verbose or r["score"] < 7:
            print(f"     {r['detail']}")
    
    print()
    print(f"  {'─'*56}")
    overall_icon = "🟢" if overall >= 8 else "🟡" if overall >= 5 else "🔴"
    overall_bar = _score_bar(overall)
    print(f"  {overall_icon} {'OVERALL':<24} {overall_bar} {overall:>4}/10  [{_score_label(overall)}]")
    print()
    
    # Recommendations
    recs = _generate_recommendations(results)
    if recs:
        print("  📋 RECOMMENDATIONS:")
        for rec in recs:
            print(f"     • {rec}")
        print()


def _score_bar(score, width=20):
    """Generate a visual bar for a score."""
    filled = round(score / 10 * width)
    return "█" * filled + "░" * (width - filled)


def _score_label(score):
    if score >= 9:
        return "EXCELLENT"
    elif score >= 7:
        return "HEALTHY"
    elif score >= 5:
        return "DEGRADED"
    elif score >= 3:
        return "ERODING"
    else:
        return "CRITICAL"


def _generate_recommendations(results):
    """Generate actionable recommendations from results."""
    recs = []
    
    if results["staleness"]["score"] < 7:
        recs.append("Run `brain store` to record recent experiences — memory is going stale")
    
    if results["consolidation"]["score"] < 7:
        recs.append("Run `brain consolidate` to process backlog into long-term memory")
    
    if results["importance"]["score"] < 7:
        recs.append("Recalibrate importance scores — use the full 1-10 range, not just 7-10")
    
    if results["emotions"]["score"] < 7:
        recs.append("Add --emotion tags to episodes — emotional memory aids recall")
    
    if results["conflicts"]["score"] < 7:
        recs.append("Review conflicting facts with `brain facts search` and resolve duplicates")
    
    if results["procedures"]["score"] < 7:
        recs.append("Run `brain proc evolve` on failing procedures to let them adapt")
    
    if results["cadence"]["score"] < 7:
        recs.append("Increase episode recording frequency — silent days create memory gaps")
    
    return recs


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    json_out = "--json" in sys.argv
    run_all_checks(verbose=verbose, json_out=json_out)


if __name__ == "__main__":
    main()
