#!/usr/bin/env python3
"""
Adaptive Brain — Self-improving agent with pattern detection, adaptation, and evolution.
"""

import sys
import os
import json
import argparse
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter
import re

BRAIN_DIR = Path.home() / '.adaptive-brain'
BRAIN_FILE = BRAIN_DIR / 'brain.json'
LEARNINGS_FILE = BRAIN_DIR / 'learnings.json'
PATTERNS_FILE = BRAIN_DIR / 'patterns.json'
EVOLUTION_FILE = BRAIN_DIR / 'evolution.json'
METRICS_FILE = BRAIN_DIR / 'metrics.json'
PREDICTIONS_FILE = BRAIN_DIR / 'predictions.json'

WORKSPACE = Path.home() / '.openclaw' / 'workspace'
SOUL_FILE = WORKSPACE / 'SOUL.md'
AGENTS_FILE = WORKSPACE / 'AGENTS.md'
TOOLS_FILE = WORKSPACE / 'TOOLS.md'
MEMORY_FILE = WORKSPACE / 'MEMORY.md'

CONFIDENCE_DECAY_DAYS = 30
PATTERN_THRESHOLD = 3  # occurrences to form a pattern
PROMOTE_THRESHOLD = 0.8  # confidence to promote


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_json(path, default=None):
    if default is None:
        default = {}
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def generate_id(prefix, existing):
    """Generate unique ID like LRN-20260331-001."""
    date_str = datetime.now().strftime('%Y%m%d')
    max_num = 0
    for key in existing:
        if key.startswith(f'{prefix}-{date_str}'):
            try:
                num = int(key.split('-')[-1])
                max_num = max(max_num, num)
            except ValueError:
                pass
    return f'{prefix}-{date_str}-{max_num + 1:03d}'


def keyword_extract(text):
    """Extract keywords for pattern matching."""
    stop_words = {'the', 'a', 'an', 'is', 'was', 'are', 'were', 'be', 'been', 'to', 'of', 'in',
                  'for', 'on', 'with', 'at', 'by', 'from', 'it', 'this', 'that', 'and', 'or',
                  'but', 'not', 'if', 'then', 'so', 'as', 'up', 'out', 'no', 'do', 'did', 'has',
                  'have', 'had', 'can', 'will', 'would', 'could', 'should', 'may', 'might'}
    words = re.findall(r'\b[a-z_]{3,}\b', text.lower())
    return [w for w in words if w not in stop_words]


def calculate_confidence(learning):
    """Calculate dynamic confidence based on age, confirmations, contradictions."""
    base = learning.get('confidence', 0.5)

    # Age decay
    try:
        created = datetime.fromisoformat(learning['logged'])
        age_days = (datetime.now(timezone.utc) - created).total_seconds() / 86400
        decay = min(age_days / CONFIDENCE_DECAY_DAYS * 0.1, 0.3)
        base -= decay
    except Exception:
        pass

    # Confirmations boost
    confirmations = learning.get('confirmations', 0)
    base += min(confirmations * 0.15, 0.3)

    # Contradictions hurt
    contradictions = learning.get('contradictions', 0)
    base -= contradictions * 0.3

    return max(0.0, min(1.0, base))


# ─── BRAIN INITIALIZATION ───

def cmd_init(args):
    """Initialize the brain system."""
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)

    if not BRAIN_FILE.exists():
        brain = {
            'version': 1,
            'created': now_iso(),
            'dna': {},
            'total_learnings': 0,
            'total_errors': 0,
            'adaptations_run': 0,
            'evolutions_run': 0,
            'overall_confidence': 0.5
        }
        save_json(BRAIN_FILE, brain)

    for f, default in [
        (LEARNINGS_FILE, {}),
        (PATTERNS_FILE, {'patterns': []}),
        (EVOLUTION_FILE, {'history': []}),
        (METRICS_FILE, {'snapshots': []}),
        (PREDICTIONS_FILE, {'predictions': []}),
    ]:
        if not f.exists():
            save_json(f, default)

    print("\n  🧠 Adaptive Brain initialized.")
    print(f"     Directory: {BRAIN_DIR}")
    print(f"     Files: 6 core files created")


# ─── LEARN ───

def cmd_learn(args):
    """Log a learning with auto-classification."""
    learnings = load_json(LEARNINGS_FILE, {})
    brain = load_json(BRAIN_FILE)

    lid = generate_id('LRN', learnings)
    keywords = keyword_extract(f"{args.summary} {args.context} {args.fix}")

    learning = {
        'id': lid,
        'type': args.type or 'insight',
        'summary': args.summary,
        'context': args.context or '',
        'fix': args.fix or '',
        'area': args.area or 'general',
        'logged': now_iso(),
        'confidence': 0.5,
        'confirmations': 0,
        'contradictions': 0,
        'keywords': keywords,
        'source': args.source or 'user_feedback',
        'status': 'active',
        'promoted_to': None,
        'related': []
    }

    # Check for related existing learnings
    related = find_related_learnings(learning, learnings)
    if related:
        learning['related'] = [r['id'] for r in related[:3]]
        # Boost confidence if related to confirmed learnings
        for r in related:
            if r.get('confirmations', 0) > 0:
                learning['confidence'] += 0.1

    learnings[lid] = learning
    save_json(LEARNINGS_FILE, learnings)

    brain['total_learnings'] = brain.get('total_learnings', 0) + 1
    save_json(BRAIN_FILE, brain)

    print(f"\n  📚 Learning logged: {lid}")
    print(f"     Type: {learning['type']}")
    print(f"     Summary: {args.summary[:80]}")
    if related:
        print(f"     Related: {', '.join(r['id'] for r in related[:3])}")


# ─── ERROR ───

def cmd_error(args):
    """Log an error with automatic pattern detection."""
    learnings = load_json(LEARNINGS_FILE, {})
    patterns = load_json(PATTERNS_FILE, {'patterns': []})
    brain = load_json(BRAIN_FILE)

    lid = generate_id('ERR', learnings)
    cmd_str = ' '.join(args.cmd) if isinstance(args.cmd, list) else args.cmd
    keywords = keyword_extract(f"{cmd_str} {args.error} {args.fix}")

    error = {
        'id': lid,
        'type': 'error',
        'command': cmd_str,
        'error': args.error,
        'fix': args.fix or '',
        'files': args.files.split(',') if args.files else [],
        'logged': now_iso(),
        'confidence': 0.6,
        'confirmations': 0,
        'contradictions': 0,
        'keywords': keywords,
        'source': 'error',
        'status': 'active',
        'area': 'infra',
        'resolved': False
    }

    # Find similar past errors
    similar = find_related_learnings(error, learnings)
    if similar:
        error['related'] = [s['id'] for s in similar[:3]]
        # Check if this forms a pattern
        for s in similar:
            if s.get('type') == 'error':
                check_and_update_pattern(error, s, patterns)

    learnings[lid] = error
    save_json(LEARNINGS_FILE, learnings)
    save_json(PATTERNS_FILE, patterns)

    brain['total_errors'] = brain.get('total_errors', 0) + 1
    save_json(BRAIN_FILE, brain)

    print(f"\n  ❌ Error logged: {lid}")
    print(f"     Command: {cmd_str or 'N/A'}")
    print(f"     Error: {args.error[:80]}")
    if similar:
        print(f"     Similar past errors: {len(similar)}")
        print(f"     ⚠️  This may be a recurring pattern!")


def check_and_update_pattern(new_error, existing_error, patterns):
    """Check if errors form a recurring pattern."""
    new_kw = set(new_error.get('keywords', []))
    old_kw = set(existing_error.get('keywords', []))
    overlap = new_kw & old_kw

    if len(overlap) >= 2:  # At least 2 shared keywords
        # Find existing pattern or create new
        matched_pattern = None
        for p in patterns.get('patterns', []):
            if overlap & set(p.get('keywords', [])):
                matched_pattern = p
                break

        if matched_pattern:
            matched_pattern['count'] = matched_pattern.get('count', 0) + 1
            matched_pattern['last_seen'] = now_iso()
            matched_pattern['keywords'] = list(set(matched_pattern['keywords']) | overlap)
            matched_pattern['confidence'] = min(1.0, matched_pattern.get('confidence', 0.5) + 0.1)
        else:
            pid = f"P{len(patterns.get('patterns', [])) + 1:03d}"
            patterns.setdefault('patterns', []).append({
                'id': pid,
                'name': f"Recurring: {new_error['error'][:50]}",
                'keywords': list(overlap),
                'count': 2,
                'first_seen': now_iso(),
                'last_seen': now_iso(),
                'prevention': new_error.get('fix', ''),
                'confidence': 0.6,
                'errors': [new_error['id'], existing_error['id']]
            })


# ─── ADAPT ───

def cmd_adapt(args):
    """Run adaptation cycle — detect patterns, update DNA, generate rules."""
    brain = load_json(BRAIN_FILE)
    learnings = load_json(LEARNINGS_FILE, {})
    patterns = load_json(PATTERNS_FILE, {'patterns': []})

    print("\n  🔄 Running adaptation cycle...\n")

    adaptations = 0

    # 1. Update confidence scores
    for lid, learning in learnings.items():
        old_conf = learning.get('confidence', 0.5)
        new_conf = calculate_confidence(learning)
        if abs(new_conf - old_conf) > 0.05:
            learning['confidence'] = round(new_conf, 3)
            adaptations += 1

    # 2. Detect new patterns from keyword clustering
    all_keywords = Counter()
    for l in learnings.values():
        if l.get('type') == 'error' and l.get('status') == 'active':
            for kw in l.get('keywords', []):
                all_keywords[kw] += 1

    hot_keywords = {kw for kw, count in all_keywords.items() if count >= 2}
    print(f"  📊 Hot keywords (2+ errors): {', '.join(list(hot_keywords)[:10])}")

    # 3. Auto-generate prevention rules for high-confidence patterns
    new_rules = []
    for p in patterns.get('patterns', []):
        if p.get('count', 0) >= PATTERN_THRESHOLD and p.get('confidence', 0) >= 0.7:
            rule = p.get('prevention', '')
            if rule:
                new_rules.append((p['id'], rule, p['confidence']))

    if new_rules:
        print(f"\n  🛡️  Prevention rules ready to promote:")
        for pid, rule, conf in new_rules:
            print(f"     [{pid}] {rule} (confidence: {conf:.0%})")

    # 4. Update DNA
    dna = brain.get('dna', {})
    for lid, learning in learnings.items():
        if learning.get('confidence', 0) >= PROMOTE_THRESHOLD and learning.get('fix'):
            # Convert learning to DNA gene
            gene_key = re.sub(r'[^a-z0-9_]', '_', learning['fix'].lower())[:30]
            if gene_key not in dna:
                dna[gene_key] = {
                    'value': True,
                    'reason': learning['summary'],
                    'source_learning': lid,
                    'established': now_iso(),
                    'confidence': learning['confidence']
                }
                print(f"  🧬 New DNA gene: {gene_key}")
                adaptations += 1

    brain['dna'] = dna
    brain['adaptations_run'] = brain.get('adaptations_run', 0) + 1
    save_json(BRAIN_FILE, brain)
    save_json(LEARNINGS_FILE, learnings)

    # 5. Record metrics snapshot
    record_metrics(brain, learnings, patterns)

    print(f"\n  ✅ Adaptation complete: {adaptations} changes made")
    print(f"     DNA genes: {len(dna)}")
    print(f"     Active patterns: {len(patterns.get('patterns', []))}")


# ─── PREDICT ───

def cmd_predict(args):
    """Predict failure risk for a task based on past learnings."""
    learnings = load_json(LEARNINGS_FILE, {})
    patterns = load_json(PATTERNS_FILE, {'patterns': []})

    task_keywords = keyword_extract(args.task)
    print(f"\n  🔮 Predicting risk for: \"{args.task}\"\n")

    # Find related errors
    risk_factors = []
    for l in learnings.values():
        if l.get('type') == 'error' and l.get('status') == 'active':
            l_keywords = set(l.get('keywords', []))
            overlap = set(task_keywords) & l_keywords
            if overlap:
                risk_factors.append({
                    'error': l['error'][:60],
                    'keywords': list(overlap),
                    'confidence': l.get('confidence', 0.5)
                })

    # Calculate risk score
    if risk_factors:
        avg_confidence = sum(r['confidence'] for r in risk_factors) / len(risk_factors)
        risk_score = min(1.0, len(risk_factors) * 0.15 + avg_confidence * 0.3)
    else:
        risk_score = 0.1  # baseline low risk

    # Risk level
    if risk_score < 0.3:
        level = 'LOW'
        emoji = '🟢'
    elif risk_score < 0.5:
        level = 'MEDIUM'
        emoji = '🟡'
    elif risk_score < 0.7:
        level = 'HIGH'
        emoji = '🟠'
    else:
        level = 'CRITICAL'
        emoji = '🔴'

    print(f"  {emoji} Risk Level: {level} ({risk_score:.0%})")

    if risk_factors:
        print(f"\n  ⚠️  Risk factors ({len(risk_factors)}):")
        for rf in risk_factors[:5]:
            print(f"     • {rf['error']} (keywords: {', '.join(rf['keywords'][:3])})")

    # Find prevention rules
    preventions = []
    for p in patterns.get('patterns', []):
        p_kw = set(p.get('keywords', []))
        if set(task_keywords) & p_kw and p.get('prevention'):
            preventions.append(p['prevention'])

    if preventions:
        print(f"\n  🛡️  Recommended precautions:")
        for prev in list(set(preventions))[:3]:
            print(f"     • {prev}")

    # Save prediction
    predictions = load_json(PREDICTIONS_FILE, {'predictions': []})
    predictions.setdefault('predictions', []).append({
        'task': args.task,
        'risk_score': risk_score,
        'risk_level': level,
        'risk_factors': len(risk_factors),
        'predicted_at': now_iso(),
        'outcome': None  # filled in later when task completes
    })
    save_json(PREDICTIONS_FILE, predictions)

    print(f"\n  {'═'*50}")


# ─── EVOLVE ───

def cmd_evolve(args):
    """Auto-evolve: review learnings, generate SKILL.md patches, track evolution."""
    brain = load_json(BRAIN_FILE)
    learnings = load_json(LEARNINGS_FILE, {})
    patterns = load_json(PATTERNS_FILE, {'patterns': []})
    evolution = load_json(EVOLUTION_FILE, {'history': []})

    print("\n  🧬 Running evolution cycle...\n")

    mutations = []

    # 1. Identify high-confidence learnings for promotion
    promotable = []
    for lid, l in learnings.items():
        if (l.get('confidence', 0) >= PROMOTE_THRESHOLD and
            l.get('status') == 'active' and
            l.get('fix') and
            not l.get('promoted_to')):
            promotable.append((lid, l))

    if promotable:
        print(f"  📈 {len(promotable)} learnings ready for promotion:")
        for lid, l in promotable[:5]:
            target = suggest_promotion_target(l)
            print(f"     [{lid}] → {target}: {l['summary'][:60]}")

    # 2. Generate DNA mutations
    dna = brain.get('dna', {})
    for lid, l in promotable:
        gene_key = re.sub(r'[^a-z0-9_]', '_', l['fix'].lower())[:30]
        if gene_key not in dna:
            dna[gene_key] = {
                'value': True,
                'reason': l['summary'],
                'source_learning': lid,
                'established': now_iso(),
                'confidence': l['confidence']
            }
            mutations.append({
                'gene': gene_key,
                'reason': l['summary'],
                'source': lid,
                'timestamp': now_iso()
            })
            l['promoted_to'] = 'dna'
            l['status'] = 'promoted'

    # 3. Auto-promote to workspace files
    promoted_count = 0
    for lid, l in promotable:
        target = suggest_promotion_target(l)
        rule = l.get('fix', '')
        if rule and target:
            success = append_to_workspace_file(target, rule, l['summary'])
            if success:
                l['promoted_to'] = target
                l['status'] = 'promoted'
                promoted_count += 1
                mutations.append({
                    'gene': f'promote_{lid}',
                    'reason': f'Promoted to {target}',
                    'source': lid,
                    'timestamp': now_iso()
                })

    brain['dna'] = dna
    brain['evolutions_run'] = brain.get('evolutions_run', 0) + 1
    save_json(BRAIN_FILE, brain)
    save_json(LEARNINGS_FILE, learnings)

    # 4. Record evolution
    if mutations:
        evolution['history'].append({
            'timestamp': now_iso(),
            'mutations': mutations,
            'dna_size': len(dna),
            'evolution_number': len(evolution['history']) + 1
        })
        save_json(EVOLUTION_FILE, evolution)

    print(f"\n  ✅ Evolution complete:")
    print(f"     Mutations: {len(mutations)}")
    print(f"     Promoted to workspace: {promoted_count}")
    print(f"     Total DNA genes: {len(dna)}")


def suggest_promotion_target(learning):
    """Suggest which workspace file to promote a learning to."""
    area = learning.get('area', '')
    ltype = learning.get('type', '')
    summary = learning.get('summary', '').lower()

    if 'tool' in summary or 'command' in summary or area == 'infra':
        return 'TOOLS.md'
    elif 'behavior' in summary or 'always' in summary or 'never' in summary or ltype == 'correction':
        return 'SOUL.md'
    elif 'workflow' in summary or 'process' in summary or 'steps' in summary:
        return 'AGENTS.md'
    else:
        return 'MEMORY.md'


def append_to_workspace_file(target, rule, summary):
    """Append a rule to a workspace file."""
    target_path = WORKSPACE / target
    if not target_path.exists():
        return False

    try:
        with open(target_path, 'a') as f:
            f.write(f"\n- {rule} *(learned: {datetime.now().strftime('%Y-%m-%d')})*")
        return True
    except Exception:
        return False


# ─── DASHBOARD ───

def cmd_dashboard(args):
    """Show learning metrics and improvement trends."""
    brain = load_json(BRAIN_FILE)
    learnings = load_json(LEARNINGS_FILE, {})
    patterns = load_json(PATTERNS_FILE, {'patterns': []})
    evolution = load_json(EVOLUTION_FILE, {'history': []})
    metrics = load_json(METRICS_FILE, {'snapshots': []})

    # Calculate stats
    total = len(learnings)
    by_type = Counter(l.get('type', 'unknown') for l in learnings.values())
    by_status = Counter(l.get('status', 'active') for l in learnings.values())
    avg_confidence = sum(calculate_confidence(l) for l in learnings.values()) / max(total, 1)

    active_errors = sum(1 for l in learnings.values() if l.get('type') == 'error' and not l.get('resolved'))
    promoted = sum(1 for l in learnings.values() if l.get('status') == 'promoted')
    pattern_count = len(patterns.get('patterns', []))
    dna_size = len(brain.get('dna', {}))

    # Confidence distribution
    high_conf = sum(1 for l in learnings.values() if calculate_confidence(l) >= 0.8)
    med_conf = sum(1 for l in learnings.values() if 0.5 <= calculate_confidence(l) < 0.8)
    low_conf = sum(1 for l in learnings.values() if calculate_confidence(l) < 0.5)

    print(f"\n{'═'*55}")
    print(f"  🧠 ADAPTIVE BRAIN DASHBOARD")
    print(f"{'═'*55}")
    print(f"")
    print(f"  📚 Total Learnings:    {total}")
    print(f"  🧬 DNA Genes:          {dna_size}")
    print(f"  🔄 Adaptations Run:    {brain.get('adaptations_run', 0)}")
    print(f"  🧬 Evolutions Run:     {brain.get('evolutions_run', 0)}")
    print(f"")
    print(f"  ── By Type ──")
    for t, count in by_type.most_common():
        print(f"     {t:20s}  {count}")
    print(f"")
    print(f"  ── Status ──")
    print(f"     Active:    {by_status.get('active', 0)}")
    print(f"     Promoted:  {promoted}")
    print(f"     Resolved:  {by_status.get('resolved', 0)}")
    print(f"")
    print(f"  ── Confidence Distribution ──")
    print(f"     🟢 High (≥0.8):   {high_conf}")
    print(f"     🟡 Med (0.5-0.8): {med_conf}")
    print(f"     🔴 Low (<0.5):    {low_conf}")
    print(f"     📊 Average:       {avg_confidence:.2f}")
    print(f"")
    print(f"  ── Patterns ──")
    print(f"     Detected:  {pattern_count}")
    if patterns.get('patterns'):
        for p in patterns['patterns'][:3]:
            print(f"     • {p.get('name', 'N/A')} ({p.get('count', 0)}x)")
    print(f"")
    print(f"  ── Active Issues ──")
    print(f"     Unresolved errors: {active_errors}")
    print(f"")
    print(f"  ── Recent Evolutions ({len(evolution.get('history', []))}) ──")
    for e in evolution.get('history', [])[-3:]:
        ts = e.get('timestamp', '?')[:10]
        mut_count = len(e.get('mutations', []))
        print(f"     {ts}: {mut_count} mutations")
    print(f"{'═'*55}")


# ─── ROLLBACK ───

def cmd_rollback(args):
    """Rollback to a previous evolution state."""
    evolution = load_json(EVOLUTION_FILE, {'history': []})
    history = evolution.get('history', [])

    target = int(args.to) if args.to else len(history) - 1

    if target < 1 or target > len(history):
        print(f"\n  ❌ Invalid evolution number. Available: 1-{len(history)}")
        return

    state = history[target - 1]
    print(f"\n  ⏪ Rolling back to evolution #{target}")
    print(f"     Timestamp: {state.get('timestamp', '?')}")
    print(f"     Mutations: {len(state.get('mutations', []))}")

    # Truncate history
    evolution['history'] = history[:target]
    save_json(EVOLUTION_FILE, evolution)

    print(f"\n  ✅ Rolled back. {len(history) - target} evolution(s) reverted.")


def find_related_learnings(new_learning, all_learnings):
    """Find related learnings by keyword overlap."""
    new_kw = set(new_learning.get('keywords', []))
    if not new_kw:
        return []

    related = []
    for lid, l in all_learnings.items():
        if lid == new_learning.get('id'):
            continue
        l_kw = set(l.get('keywords', []))
        overlap = new_kw & l_kw
        if len(overlap) >= 2:
            related.append({'id': lid, 'overlap': len(overlap), **l})

    related.sort(key=lambda x: x['overlap'], reverse=True)
    return related[:5]


def cmd_outcome(args):
    """Record outcome of a prediction to improve future predictions."""
    predictions = load_json(PREDICTIONS_FILE, {'predictions': []})
    learnings = load_json(LEARNINGS_FILE, {})
    brain = load_json(BRAIN_FILE)

    task = ' '.join(args.task) if isinstance(args.task, list) else args.task
    success = args.success == 'yes'
    task_keywords = keyword_extract(task)

    # Find matching prediction
    matched = False
    for pred in reversed(predictions.get('predictions', [])):
        if pred.get('outcome') is None:
            pred_kw = set(keyword_extract(pred.get('task', '')))
            if pred_kw & set(task_keywords):
                pred['outcome'] = 'success' if success else 'failure'
                pred['outcome_notes'] = args.notes
                pred['outcome_at'] = now_iso()
                matched = True
                break

    # Update confidence of related learnings
    for lid, l in learnings.items():
        l_kw = set(l.get('keywords', []))
        if l_kw & set(task_keywords):
            if success:
                l['confirmations'] = l.get('confirmations', 0) + 1
            else:
                l['contradictions'] = l.get('contradictions', 0) + 1

    save_json(PREDICTIONS_FILE, predictions)
    save_json(LEARNINGS_FILE, learnings)

    result = 'confirmed' if success else 'contradicted'
    print(f"\n  {'✅' if success else '❌'} Outcome recorded: {result}")
    print(f"     Task: {task[:80]}")
    if matched:
        print(f"     Matched prediction updated")
    print(f"     Related learnings updated ({'+' if success else '-'}confidence)")


def cmd_report(args):
    """Generate improvement report over time period."""
    learnings = load_json(LEARNINGS_FILE, {})
    predictions = load_json(PREDICTIONS_FILE, {'predictions': []})
    metrics = load_json(METRICS_FILE, {'snapshots': []})

    cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()

    # Recent learnings
    recent = {lid: l for lid, l in learnings.items() if l.get('logged', '') >= cutoff}
    recent_errors = sum(1 for l in recent.values() if l.get('type') == 'error')
    recent_promoted = sum(1 for l in recent.values() if l.get('status') == 'promoted')

    # Prediction accuracy
    preds = [p for p in predictions.get('predictions', []) if p.get('predicted_at', '') >= cutoff]
    resolved = [p for p in preds if p.get('outcome')]
    accurate = sum(1 for p in resolved if (p.get('risk_level') in ('HIGH', 'CRITICAL')) == (p.get('outcome') == 'failure'))
    accuracy = (accurate / len(resolved) * 100) if resolved else 0

    # Confidence trend
    snapshots = [s for s in metrics.get('snapshots', []) if s.get('timestamp', '') >= cutoff]
    conf_trend = 'stable'
    if len(snapshots) >= 2:
        first_conf = snapshots[0].get('avg_confidence', 0.5)
        last_conf = snapshots[-1].get('avg_confidence', 0.5)
        if last_conf > first_conf + 0.05:
            conf_trend = '↑ improving'
        elif last_conf < first_conf - 0.05:
            conf_trend = '↓ declining'

    print(f"\n{'═'*55}")
    print(f"  📈 IMPROVEMENT REPORT — Last {args.days} days")
    print(f"{'═'*55}")
    print(f"")
    print(f"  📚 New learnings:    {len(recent)}")
    print(f"  ❌ New errors:       {recent_errors}")
    print(f"  🟢 Promoted:         {recent_promoted}")
    print(f"")
    print(f"  🔮 Predictions:      {len(preds)} total, {len(resolved)} resolved")
    print(f"  🎯 Accuracy:         {accuracy:.0f}%")
    print(f"  📊 Confidence trend: {conf_trend}")
    print(f"{'═'*55}")


def record_metrics(brain, learnings, patterns):
    """Record a metrics snapshot."""
    metrics = load_json(METRICS_FILE, {'snapshots': []})

    snapshot = {
        'timestamp': now_iso(),
        'total_learnings': len(learnings),
        'total_errors': sum(1 for l in learnings.values() if l.get('type') == 'error'),
        'avg_confidence': sum(calculate_confidence(l) for l in learnings.values()) / max(len(learnings), 1),
        'dna_size': len(brain.get('dna', {})),
        'pattern_count': len(patterns.get('patterns', [])),
        'promoted_count': sum(1 for l in learnings.values() if l.get('status') == 'promoted')
    }

    metrics['snapshots'].append(snapshot)
    # Keep last 100 snapshots
    metrics['snapshots'] = metrics['snapshots'][-100:]
    save_json(METRICS_FILE, metrics)


# ─── LIST ───

def cmd_list(args):
    """List learnings with filters."""
    learnings = load_json(LEARNINGS_FILE, {})

    items = list(learnings.values())

    if args.type:
        items = [l for l in items if l.get('type') == args.type]
    if args.status:
        items = [l for l in items if l.get('status') == args.status]

    items.sort(key=lambda x: x.get('logged', ''), reverse=True)
    items = items[:args.limit or 10]

    if not items:
        print("\n  📭 No learnings found.")
        return

    print(f"\n  📚 Learnings ({len(items)} shown):")
    for l in items:
        conf = calculate_confidence(l)
        conf_bar = '█' * int(conf * 5) + '░' * (5 - int(conf * 5))
        status_emoji = {'active': '🔵', 'promoted': '🟢', 'resolved': '✅'}.get(l.get('status'), '⚪')
        print(f"  {status_emoji} [{l['id']}] {l.get('type', '?'):12s} | {conf_bar} {conf:.0%} | {l.get('summary', '')[:60]}")


# ─── MAIN ───

def main():
    parser = argparse.ArgumentParser(description='Adaptive Brain — Self-Improving Agent')
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('init', help='Initialize brain system')

    p = sub.add_parser('learn', help='Log a learning')
    p.add_argument('--type', choices=['correction', 'insight', 'knowledge_gap', 'best_practice'])
    p.add_argument('--summary', required=True)
    p.add_argument('--context', default='')
    p.add_argument('--fix', default='')
    p.add_argument('--area', default='general')
    p.add_argument('--source', default='user_feedback')

    p = sub.add_parser('error', help='Log an error')
    p.add_argument('--cmd', nargs='*', default=[], help='Command that failed')
    p.add_argument('--error', required=True)
    p.add_argument('--fix', default='')
    p.add_argument('--files', default='')

    sub.add_parser('adapt', help='Run adaptation cycle')
    sub.add_parser('evolve', help='Run evolution cycle')
    sub.add_parser('dashboard', help='Show metrics dashboard')

    p = sub.add_parser('predict', help='Predict failure risk')
    p.add_argument('task', nargs='+')

    p = sub.add_parser('rollback', help='Rollback evolution')
    p.add_argument('--to', required=True)

    p = sub.add_parser('list', help='List learnings')
    p.add_argument('--type')
    p.add_argument('--status')
    p.add_argument('--limit', type=int, default=10)

    p = sub.add_parser('outcome', help='Record prediction outcome')
    p.add_argument('--task', required=True, nargs='+')
    p.add_argument('--success', required=True, choices=['yes', 'no'])
    p.add_argument('--notes', default='')

    p = sub.add_parser('report', help='Generate improvement report')
    p.add_argument('--days', type=int, default=7)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'predict':
        args.task = ' '.join(args.task)
    if args.command == 'outcome':
        args.task = args.task if isinstance(args.task, list) else [args.task]

    handlers = {
        'init': cmd_init,
        'learn': cmd_learn,
        'error': cmd_error,
        'adapt': cmd_adapt,
        'evolve': cmd_evolve,
        'dashboard': cmd_dashboard,
        'predict': cmd_predict,
        'rollback': cmd_rollback,
        'list': cmd_list,
        'outcome': cmd_outcome,
        'report': cmd_report,
    }

    handler = handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
