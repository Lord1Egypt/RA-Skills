#!/usr/bin/env python3
"""
Goal Engine — registry and lifecycle management for the autogoal skill.

Combines planning depth (L0-L4), self-improvement learning, session state
tracking, risk guardrails, and strategy outcome tracking.

Usage:
  python3 goal_engine.py create "<goal>" [--channel "<id>"] [--channel-name "<name>"]
  python3 goal_engine.py plan "<goal>" --depth L0|L1|L2|L3|L4 [--strategy sequential|parallel|iterative|spike|checkpoint]
  python3 goal_engine.py list [--status active|paused|completed|abandoned]
  python3 goal_engine.py status <goal-id>
  python3 goal_engine.py update <goal-id> --key <path> --value <json-or-string>
  python3 goal_engine.py log-action <goal-id> --action "<text>" [--result "<text>"]
  python3 goal_engine.py adapt <goal-id> --strategy "<text>"
  python3 goal_engine.py advance <goal-id> --milestone "<text>"
  python3 goal_engine.py close <goal-id> [--status completed|abandoned] [--note "<text>"]
  python3 goal_engine.py set-metrics <goal-id> --json '{"key": "value"}'
  python3 goal_engine.py set-session-state <goal-id> [--objective "<text>"] [--decision "<text>"] [--blocker "<text>"] [--next "<text>"]
  python3 goal_engine.py set-risk-rules <goal-id> --json '{"max_position_size": 100, "max_drawdown": 0.15}'
  python3 goal_engine.py log-outcome <goal-id> --action "<text>" --result "<text>" [--lessons "<text>"]
  python3 goal_engine.py learn <goal-id> --lesson "<text>"
  python3 goal_engine.py report [--status active|paused|completed|abandoned] [--stalled]
  python3 goal_engine.py cron <goal-id>
"""

import json
import os
import sys
import uuid
import argparse
from datetime import datetime, timezone, timedelta

REGISTRY = os.path.join(os.path.dirname(__file__), "..", "goals_registry.json")
REGISTRY = os.path.abspath(REGISTRY)

CRON_TEMPLATE = {
    "schedule": {"kind": "every", "everyMs": 3_600_000, "anchorMs": int(datetime.now(timezone.utc).timestamp() * 1000)},
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
        "kind": "agentTurn",
        "message": "CHECK-IN for goal: <GOAL_RUNTIME_FILL>",
        "model": "opencode/deepseek-v4-flash-free",
        "timeoutSeconds": 300
    },
    "delivery": {"mode": "none"},
    "enabled": True
}

PLAN_DEPTHS = {
    "L0": "Trivial, done before — no plan, just execute",
    "L1": "Simple, low risk — mental checklist, no doc",
    "L2": "Medium complexity — bullet list, share with channel",
    "L3": "Complex, multi-step — detailed plan with milestones",
    "L4": "High stakes, novel — full plan + human validation",
}

PLAN_STRATEGIES = {
    "sequential": "Linear workflow with clear dependencies",
    "parallel": "Independent components running in parallel",
    "iterative": "Draft → feedback → revise cycles",
    "spike": "Timeboxed feasibility proof → decide → full exec",
    "checkpoint": "Milestones with human validation gates",
}


def _load():
    if not os.path.exists(REGISTRY):
        return {"goals": []}
    with open(REGISTRY) as f:
        return json.load(f)


def _save(data):
    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    with open(REGISTRY, "w") as f:
        json.dump(data, f, indent=2, default=str)


def _find(goal_id, data):
    for g in data["goals"]:
        if g["id"] == goal_id:
            return g
    return None


def _goal_script():
    return "cd ~/.openclaw/workspace/skills/autogoal && python3 scripts/goal_engine.py"


def _format_actions(g, n=3):
    actions = g.get("actions_taken", [])
    if not actions:
        return "No actions logged yet."
    recent = actions[-n:]
    lines = []
    for a in recent:
        ts = a.get("timestamp", "?")[:19]
        action = a.get("action", "")
        result = a.get("result", "")
        lines.append(f"  - {ts} | {action} → {result[:60]}")
    return "\n".join(lines)


def _format_metrics(g):
    metrics = g.get("metrics", {})
    if not metrics:
        return "No metrics recorded."
    return ", ".join(f"{k}={v}" for k, v in sorted(metrics.items()) if v is not None)


def _is_stalled(g):
    actions = g.get("actions_taken", [])
    if len(actions) < 3:
        return False
    recent = actions[-3:]
    stagnant = 0
    for a in recent:
        result = (a.get("result") or "").strip().lower()
        if not result or result in ("none", "no change", "no action needed", "no progress", "-"):
            stagnant += 1
    return stagnant >= 3


def _strategy_tip(g):
    """Return a relevant tip from the auto-trading-strategy skill for financial goals."""
    statement = (g.get("statement") or "").lower()
    
    trading_tips = [
        "💡 **Tip**: Never risk more than 2% per trade. Max loss = 2% of total capital (Risk Management Rule 1).",
        "💡 **Tip**: Cut losses quickly, let winners run. Use a 2R take-profit target then trail the remainder (Trend Follow Rule 3).",
        "💡 **Tip**: Track R-multiple, not just win rate. A 40% win rate with 1.5R avg win beats 60% with 0.8R avg win (Risk Management Rule 3).",
        "💡 **Tip**: Wait for trend confirmation before entering. ADX > 25 with stacked MAs = strong trend (Trend Follow entry filter).",
        "💡 **Tip**: Use Kelly Criterion: position = (win_rate * avg_win - avg_loss) / avg_win. Then use half-Kelly for safety.",
        "💡 **Tip**: Max 20% in a single position, max 50% in one category, keep 20% cash for opportunities (Portfolio Management).",
        "💡 **Tip**: If drawdown hits 10%, halve position sizes. At 15%, stop new trades entirely. Recover before risking more.",
        "💡 **Tip**: To recover a X% loss, you need Y% = X / (1 - X/100). A 50% loss needs 100% gain — don't let losses compound!",
        "💡 **Tip**: Set stop-loss at 2x ATR for volatility-adaptive exits. Fixed 20% is simpler but may get caught on noise.",
        "💡 **Tip**: No revenge trading, no FOMO, no averaging down, no overleveraging. Run the checklist before every trade (Psychology Rules).",
        "💡 **Tip**: Max 20 trades/day, max 6% daily loss, max 15% weekly drawdown. Stick to these hard limits.",
        "💡 **Tip**: Trend follow entry: price crosses above 20-MA + volume > 1.5x avg + RSI < 70. Never chase a move that's >20% from entry.",
    ]
    
    kalshi_tips = [
        "💡 **Tip**: When modeling YES at 15¢ but market is 10¢, that's 5¢ edge. Check volatility — narrow markets converge faster.",
        "💡 **Tip**: For binary prediction markets, keep position small when the category is new (unknown drift/edge). Scale up with track record.",
        "💡 **Tip**: Watch for correlated bets (same underlying event, different thresholds). If one leg is mispriced, check the ladder.",
        "💡 **Tip**: Time decay accelerates in last 48h. Enter earlier when edge is clear; wait for volume when edge is marginal.",
        "💡 **Tip**: Consider combo orders on event ladders — mispriced thresholds create risk-free or near-risk-free spreads.",
    ]
    
    crypto_tips = [
        "💡 **Tip**: Track whale wallets for accumulation patterns. Small buys every 15-30m = strong accumulation signal (Whale Tracking Type 1).",
        "💡 **Tip**: When 3+ whales move in the same direction, signal strength is high. Follow, but only if entry is within 20% of theirs.",
        "💡 **Tip**: RSI mean reversion works in range-bound markets. In trending markets, use ADX to identify direction, not reversals.",
        "💡 **Tip**: Crypto correlates heavily — if BTC moves, altcoins follow. Don't over-allocate correlated positions.",
    ]
    
    # Pick tips based on goal category
    tips = []
    if "kalshi" in statement or "prediction" in statement or "market" in statement:
        tips.extend(kalshi_tips)
    if "crypto" in statement or "coin" in statement:
        tips.extend(crypto_tips)
    if "profit" in statement or "trade" in statement or "trading" in statement or "swing" in statement or "stock" in statement or "alpaca" in statement:
        tips.extend(trading_tips)
    
    # If we have risk rules, use those to narrow relevant tips
    rr = g.get("risk_rules", {})
    if rr:
        relevant = []
        for t in tips:
            if "position" in t and rr.get("max_position_size"):
                relevant.append(t)
            elif "drawdown" in t and rr.get("max_drawdown"):
                relevant.append(t)
            elif "trade" in t.lower() and rr.get("max_daily_trades"):
                relevant.append(t)
        if relevant:
            return relevant[0]  # Most relevant tip
    
    # Default: rotate through tips deterministically by goal id hash
    if not tips:
        return None
    idx = sum(ord(c) for c in g.get("id", "")) % len(tips)
    return tips[idx]


def _make_checkin_message(g):
    script = _goal_script()
    pd = g.get("plan_depth", "")
    ps = g.get("plan_strategy", "")
    ss = g.get("session_state", {})
    rr = g.get("risk_rules", {})

    # Header
    msg = (
        f"## Goal Check-In\n\n"
        f"**Goal**: {g['statement']}\n"
        f"**Goal ID**: {g['id']}\n"
        f"**Status**: {g['status']}\n"
        f"**Current Strategy**: {g.get('current_strategy', 'Not defined')}\n"
    )

    # Plan depth
    if pd:
        desc = PLAN_DEPTHS.get(pd, "")
        msg += f"**Plan Level**: {pd}" + (f" — {desc}" if desc else "") + "\n"
    if ps:
        sdesc = PLAN_STRATEGIES.get(ps, "")
        msg += f"**Plan Strategy**: {ps}" + (f" — {sdesc}" if sdesc else "") + "\n"

    # Session state
    if ss.get("current_objective"):
        msg += f"**Session Objective**: {ss['current_objective']}\n"
    if ss.get("blocker"):
        msg += f"**⚠️ Blocker**: {ss['blocker']}\n"
    if ss.get("next_move"):
        msg += f"**Next Move**: {ss['next_move']}\n"

    # Risk rules
    if rr:
        risk_parts = []
        for k, v in sorted(rr.items()):
            k_display = k.replace("_", " ").title()
            risk_parts.append(f"{k_display}={v}")
        msg += f"**Risk Rules**: {', '.join(risk_parts)}\n"

    # Strategy tip
    tip = _strategy_tip(g)
    if tip:
        msg += f"{tip}\n"

    # Metrics
    metrics = g.get("metrics", {})
    if metrics:
        msg += f"**Metrics**: {_format_metrics(g)}\n"

    # Recent actions
    actions = g.get("actions_taken", [])
    if actions:
        msg += f"\n**Recent Actions**:\n{_format_actions(g, 3)}\n"

    # Stalled warning
    if _is_stalled(g):
        msg += f"\n**⚠️ Stalled**: No meaningful progress in last 3 check-ins.\n"

    # Check-in steps
    msg += (
        f"\n1. Evaluate progress. What has changed since the last check?\n"
        f"2. Take action to move closer to the goal using available tools and skills.\n"
        f"3. Update session state (objective/blocker/next move):\n"
        f"   `{script} set-session-state {g['id']} --objective \"...\" --blocker \"...\" --next \"...\"`\n"
        f"4. Log your action with optional lessons:\n"
        f"   `{script} log-action {g['id']} --action \"<what you did>\" --result \"<outcome>\"`\n"
        f"5. Update metrics if tracking:\n"
        f"   `{script} set-metrics {g['id']} --json '{{\"pnl\": value, \"win_rate\": value}}'`\n"
        f"6. Record outcome for self-improvement:\n"
        f"   `{script} log-outcome {g['id']} --action \"<action>\" --result \"<result>\" --lessons \"<lessons>\"`\n"
        f"7. If the current strategy isn't working, adapt it:\n"
        f"   `{script} adapt {g['id']} --strategy \"<new approach>\"`\n"
        f"8. If the goal is achieved, close it:\n"
        f"   `{script} close {g['id']} --status completed`\n"
        f"9. If blocked, explain what you need.\n\n"
        f"Report back concisely."
    )
    return msg


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_create(args):
    data = _load()
    goal = {
        "id": "goal-" + uuid.uuid4().hex[:12],
        "statement": args.statement,
        "channel": args.channel or "",
        "channel_name": args.channel_name or "",
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_check": None,
        "current_strategy": args.strategy or "",
        "plan_depth": None,
        "plan_strategy": None,
        "session_state": {},
        "risk_rules": {},
        "metrics": {},
        "milestones": [],
        "actions_taken": [],
        "outcomes": [],
        "learnings": [],
        "notes": ""
    }
    data["goals"].append(goal)
    _save(data)
    print(json.dumps({"id": goal["id"], "statement": goal["statement"], "status": "created", "path": REGISTRY}))
    return goal


def cmd_plan(args):
    """Create a goal with planning depth and strategy upfront."""
    if args.depth not in PLAN_DEPTHS:
        print(f"Invalid depth {args.depth}. Choose from: {', '.join(PLAN_DEPTHS.keys())}", file=sys.stderr)
        sys.exit(1)
    if args.strategy and args.strategy not in PLAN_STRATEGIES:
        print(f"Invalid strategy {args.strategy}. Choose from: {', '.join(PLAN_STRATEGIES.keys())}", file=sys.stderr)
        sys.exit(1)

    data = _load()
    goal = {
        "id": "goal-" + uuid.uuid4().hex[:12],
        "statement": args.statement,
        "channel": args.channel or "",
        "channel_name": args.channel_name or "",
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_check": None,
        "current_strategy": args.strategy_desc or "",
        "plan_depth": args.depth,
        "plan_strategy": args.strategy,
        "session_state": {},
        "risk_rules": {},
        "metrics": {},
        "milestones": [],
        "actions_taken": [],
        "outcomes": [],
        "learnings": [],
        "notes": ""
    }
    data["goals"].append(goal)
    _save(data)
    depth_desc = PLAN_DEPTHS.get(args.depth, "")
    strat_desc = PLAN_STRATEGIES.get(args.strategy, "") if args.strategy else "none"
    print(f"Planned goal: {goal['id']}")
    print(f"  Statement: {args.statement}")
    print(f"  Depth: {args.depth} — {depth_desc}")
    print(f"  Strategy: {args.strategy or 'default'} — {strat_desc}")
    return goal


def cmd_set_session_state(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    ss = g.setdefault("session_state", {})
    if args.objective is not None:
        ss["current_objective"] = args.objective
    if args.decision is not None:
        ss["last_decision"] = args.decision
    if args.blocker is not None:
        ss["blocker"] = args.blocker
    if args.next is not None:
        ss["next_move"] = args.next
    g["last_check"] = datetime.now(timezone.utc).isoformat()
    _save(data)
    updated = [k for k in ["current_objective", "last_decision", "blocker", "next_move"] if k in ss]
    print(f"Session state updated for {args.goal_id}: {', '.join(updated)}")


def cmd_set_risk_rules(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    try:
        updates = json.loads(args.json)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(updates, dict):
        print("Risk rules must be a JSON object", file=sys.stderr)
        sys.exit(1)
    g.setdefault("risk_rules", {}).update(updates)
    _save(data)
    keys = list(updates.keys())
    print(f"Risk rules updated for {args.goal_id}: {', '.join(keys)}")


def cmd_log_outcome(args):
    """Log a check-in outcome with lessons for self-improvement."""
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    outcome = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": args.action,
        "result": args.result,
        "lessons": args.lessons or "",
        "plan_depth": g.get("plan_depth"),
        "plan_strategy": g.get("plan_strategy"),
    }
    g.setdefault("outcomes", []).append(outcome)
    g["last_check"] = datetime.now(timezone.utc).isoformat()
    _save(data)
    print(f"Outcome logged for {args.goal_id}")


def cmd_learn(args):
    """Record a learning that can be promoted for self-improvement."""
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    learning = {
        "lesson": args.lesson,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repetitions": 0,
        "promoted_to_hot": False,
    }
    # Check for duplicate lesson
    existing = g.setdefault("learnings", [])
    for l in existing:
        if l["lesson"].lower() == args.lesson.lower():
            l["repetitions"] += 1
            l["created_at"] = datetime.now(timezone.utc).isoformat()
            if l["repetitions"] >= 3:
                l["promoted_to_hot"] = True
                print(f"Learning reinforced ({l['repetitions']}x) and promoted to HOT for {args.goal_id}")
            else:
                print(f"Learning reinforced ({l['repetitions']}x) for {args.goal_id}")
            _save(data)
            return
    existing.append(learning)
    _save(data)
    print(f"Lesson recorded for {args.goal_id}")


def cmd_set_metrics(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    try:
        updates = json.loads(args.json)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(updates, dict):
        print("Metrics must be a JSON object", file=sys.stderr)
        sys.exit(1)
    g.setdefault("metrics", {}).update(updates)
    _save(data)
    keys = list(updates.keys())
    print(f"Metrics updated for {args.goal_id}: {', '.join(keys)}")


def cmd_list(args):
    data = _load()
    if not data["goals"]:
        print("No goals found. Create one with `create` or `plan`.")
        return
    for g in data["goals"]:
        if args.status and g["status"] != args.status:
            continue
        pd = g.get("plan_depth", "").ljust(3) if g.get("plan_depth") else "   "
        mv = g.get("metrics", {}).get("current_value")
        metric_str = ""
        if mv is not None:
            tv = g.get("metrics", {}).get("target_value")
            metric_str = f"  [{mv}" + (f"/{tv}" if tv is not None else "") + "]"
        print(f"{g['id']:30s} [{g['status']:12s}] {pd}  {g['statement'][:60]}{metric_str}")


def cmd_status(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(g, indent=2, default=str))


def cmd_update(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    try:
        parsed = json.loads(args.value)
    except (json.JSONDecodeError, TypeError):
        parsed = args.value
    parts = args.key.split(".")
    target = g
    for p in parts[:-1]:
        if p not in target or not isinstance(target[p], dict):
            target[p] = {}
        target = target[p]
    target[parts[-1]] = parsed
    _save(data)
    print(f"Updated {args.key} = {json.dumps(parsed)}")


def cmd_log_action(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    action = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": args.action or "",
        "result": args.result or ""
    }
    g.setdefault("actions_taken", []).append(action)
    g["last_check"] = datetime.now(timezone.utc).isoformat()
    _save(data)
    print(f"Logged action for {args.goal_id}")


def cmd_adapt(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    g["current_strategy"] = args.strategy or ""
    g["strategy_updated_at"] = datetime.now(timezone.utc).isoformat()
    _save(data)
    print(f"Strategy updated for {args.goal_id}")


def cmd_advance(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    desc = args.milestone or ""
    found = False
    for m in g.setdefault("milestones", []):
        if m["description"] == desc:
            m["achieved"] = True
            m["achieved_at"] = datetime.now(timezone.utc).isoformat()
            found = True
            break
    if not found:
        g["milestones"].append({"description": desc, "achieved": True, "achieved_at": datetime.now(timezone.utc).isoformat()})
    _save(data)
    print(f"Milestone advanced: {desc} [{args.goal_id}]")


def cmd_close(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    g["status"] = args.status or "completed"
    g["closed_at"] = datetime.now(timezone.utc).isoformat()
    if args.note:
        g["notes"] = args.note
    _save(data)
    print(f"Goal {args.goal_id} closed as {g['status']}")


def cmd_report(args):
    data = _load()
    goals = data.get("goals", [])
    if args.status:
        goals = [g for g in goals if g["status"] == args.status]
    if args.stalled:
        goals = [g for g in goals if _is_stalled(g)]
    if not goals:
        print("No goals found matching criteria.")
        return
    print(f"# Goal Report — {len(goals)} goal(s)\n")
    for i, g in enumerate(goals):
        stalled = _is_stalled(g)
        actions = g.get("actions_taken", [])
        outcomes = g.get("outcomes", [])
        learnings = g.get("learnings", [])
        metrics = _format_metrics(g)
        last_check = (g.get("last_check") or "-")[:19]
        status_icon = {"active": "🟢", "paused": "🟡", "completed": "✅", "abandoned": "❌"}.get(g["status"], "⚪")
        stalled_mark = " ⚠️ STALLED" if stalled else ""
        pd = g.get("plan_depth", "")
        ps = g.get("plan_strategy", "")
        ss = g.get("session_state", {})
        rr = g.get("risk_rules", {})

        print(f"### {status_icon} {g['statement']}{stalled_mark}")
        print(f"  **ID**: {g['id']} | **Status**: {g['status']} | **Last check**: {last_check}")
        if pd:
            print(f"  **Plan**: {pd} / {ps or 'default'}")
        if ss.get("blocker"):
            print(f"  **⚠️ Blocker**: {ss['blocker']}")
        if ss.get("next_move"):
            print(f"  **Next**: {ss['next_move']}")
        if rr:
            print(f"  **Risk**: {', '.join(f'{k}={v}' for k,v in sorted(rr.items()))}")
        print(f"  **Actions**: {len(actions)} | **Outcomes**: {len(outcomes)} | **Learnings**: {len(learnings)}")
        if metrics:
            print(f"  **Metrics**: {metrics}")
        if stalled:
            print(f"  **⚠️ Stalled**: No meaningful progress in last 3 check-ins.")
        if i < len(goals) - 1:
            print()


def cmd_cron(args):
    data = _load()
    g = _find(args.goal_id, data)
    if not g:
        print(f"No goal with id: {args.goal_id}", file=sys.stderr)
        sys.exit(1)
    cron = dict(CRON_TEMPLATE)
    cron["name"] = f"goal-check-{g['id']}"
    cron["description"] = f"Goal check-in: {g['statement'][:80]}"
    cron["payload"]["message"] = _make_checkin_message(g)
    print(json.dumps(cron, indent=2, default=str))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="autogoal — Goal Engine")
    sub = parser.add_subparsers(dest="cmd")

    # create
    p_create = sub.add_parser("create")
    p_create.add_argument("statement", help="Goal statement")
    p_create.add_argument("--channel", help="Discord/source channel ID")
    p_create.add_argument("--channel-name", help="Human channel name")
    p_create.add_argument("--strategy", help="Initial strategy")

    # plan
    p_plan = sub.add_parser("plan")
    p_plan.add_argument("statement", help="Goal statement")
    p_plan.add_argument("--depth", choices=list(PLAN_DEPTHS.keys()), required=True,
                        help=f"Planning depth: {', '.join(f'{k}={v}' for k,v in PLAN_DEPTHS.items())}")
    p_plan.add_argument("--strategy", choices=list(PLAN_STRATEGIES.keys()),
                        help=f"Strategy template: {', '.join(PLAN_STRATEGIES.keys())}")
    p_plan.add_argument("--channel", help="Discord/source channel ID")
    p_plan.add_argument("--channel-name", help="Human channel name")
    p_plan.add_argument("--strategy-desc", help="Free-text strategy description")

    # list
    p_list = sub.add_parser("list")
    p_list.add_argument("--status", choices=["active", "paused", "completed", "abandoned"], help="Filter by status")

    # status
    p_status = sub.add_parser("status")
    p_status.add_argument("goal_id", help="Goal ID")

    # update
    p_update = sub.add_parser("update")
    p_update.add_argument("goal_id", help="Goal ID")
    p_update.add_argument("--key", required=True, help="Dot-separated key path (e.g. metrics.current_value)")
    p_update.add_argument("--value", required=True, help="Value (JSON or plain string)")

    # log-action
    p_log = sub.add_parser("log-action")
    p_log.add_argument("goal_id", help="Goal ID")
    p_log.add_argument("--action", required=True, help="What was done")
    p_log.add_argument("--result", default="", help="Outcome")

    # adapt
    p_adapt = sub.add_parser("adapt")
    p_adapt.add_argument("goal_id", help="Goal ID")
    p_adapt.add_argument("--strategy", required=True, help="New strategy text")

    # advance
    p_advance = sub.add_parser("advance")
    p_advance.add_argument("goal_id", help="Goal ID")
    p_advance.add_argument("--milestone", required=True, help="Milestone description")

    # close
    p_close = sub.add_parser("close")
    p_close.add_argument("goal_id", help="Goal ID")
    p_close.add_argument("--status", choices=["completed", "abandoned", "paused"], default="completed")
    p_close.add_argument("--note", default="", help="Closing note")

    # set-metrics
    p_sm = sub.add_parser("set-metrics")
    p_sm.add_argument("goal_id", help="Goal ID")
    p_sm.add_argument("--json", required=True, help='JSON object to merge into metrics, e.g. {"pnl": 14.17}')

    # set-session-state
    p_ss = sub.add_parser("set-session-state")
    p_ss.add_argument("goal_id", help="Goal ID")
    p_ss.add_argument("--objective", help="Current objective for this check-in")
    p_ss.add_argument("--decision", help="Last confirmed decision")
    p_ss.add_argument("--blocker", help="Blocker or open question")
    p_ss.add_argument("--next", help="Next useful move")

    # set-risk-rules
    p_rr = sub.add_parser("set-risk-rules")
    p_rr.add_argument("goal_id", help="Goal ID")
    p_rr.add_argument("--json", required=True,
                      help='Risk parameters JSON, e.g. {"max_position_size": 100, "max_drawdown": 0.15}')

    # log-outcome
    p_lo = sub.add_parser("log-outcome")
    p_lo.add_argument("goal_id", help="Goal ID")
    p_lo.add_argument("--action", required=True, help="What was done")
    p_lo.add_argument("--result", required=True, help="Outcome (success/partial/failure)")
    p_lo.add_argument("--lessons", default="", help="Lessons learned")

    # learn
    p_lrn = sub.add_parser("learn")
    p_lrn.add_argument("goal_id", help="Goal ID")
    p_lrn.add_argument("--lesson", required=True, help="Lesson or insight to record")
    p_lrn.add_argument("--reinforce", action="store_true", help="Increment repetition count")

    # report
    p_rep = sub.add_parser("report")
    p_rep.add_argument("--status", choices=["active", "paused", "completed", "abandoned"], help="Filter by status")
    p_rep.add_argument("--stalled", action="store_true", help="Show only stalled goals")

    # cron
    p_cron = sub.add_parser("cron")
    p_cron.add_argument("goal_id", help="Goal ID")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "create": cmd_create,
        "plan": cmd_plan,
        "list": cmd_list,
        "status": cmd_status,
        "update": cmd_update,
        "log-action": cmd_log_action,
        "adapt": cmd_adapt,
        "advance": cmd_advance,
        "close": cmd_close,
        "set-metrics": cmd_set_metrics,
        "set-session-state": cmd_set_session_state,
        "set-risk-rules": cmd_set_risk_rules,
        "log-outcome": cmd_log_outcome,
        "learn": cmd_learn,
        "report": cmd_report,
        "cron": cmd_cron,
    }

    handlers[args.cmd](args)
