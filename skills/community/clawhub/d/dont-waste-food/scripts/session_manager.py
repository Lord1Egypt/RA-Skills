#!/usr/bin/env python3
"""
Dont Waste Food — Session Manager
Saves cooking sessions, maintains history, and computes stats.
"""
import json
import os
import uuid
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.qclaw-oversea/workspace/dont-waste-food")
SESSIONS_DIR = f"{WORKSPACE}/sessions"
HISTORY_FILE = f"{WORKSPACE}/history.json"


def ensure_dirs():
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"sessions": [], "stats": default_stats()}, f, ensure_ascii=False, indent=2)


def default_stats() -> dict:
    return {
        "total_sessions": 0,
        "completed": 0,
        "stopped": 0,
        "unsafe": 0,
        "total_ingredients_saved": 0,
        "total_recipes_cooked": 0,
        "top_recipes": {},
        "stop_reasons": {},
        "streak_days": 0,
        "last_session_date": None
    }


def save_session(session: dict) -> str:
    """Save a session to disk. Returns session ID."""
    ensure_dirs()
    if "id" not in session:
        session["id"] = str(uuid.uuid4())[:8]
    if "date" not in session:
        session["date"] = datetime.now().strftime("%Y-%m-%d")

    filepath = f"{SESSIONS_DIR}/{session['date']}_{session['id']}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)

    _update_history(session)
    return session["id"]


def _update_history(session: dict):
    ensure_dirs()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    # Replace existing or append
    replaced = False
    for i, s in enumerate(history["sessions"]):
        if s.get("id") == session.get("id"):
            history["sessions"][i] = session
            replaced = True
            break
    if not replaced:
        history["sessions"].insert(0, session)

    stats = history["stats"]
    stats["total_sessions"] = len(history["sessions"])

    if session.get("status") == "completed":
        stats["completed"] += 1
        # Update streak
        today = datetime.now().strftime("%Y-%m-%d")
        if stats["last_session_date"]:
            diff = (datetime.now() - datetime.strptime(stats["last_session_date"], "%Y-%m-%d")).days
            if diff <= 2:
                stats["streak_days"] += 1
            else:
                stats["streak_days"] = 1
        else:
            stats["streak_days"] = 1
        stats["last_session_date"] = today
    elif session.get("status") == "stopped":
        stats["stopped"] += 1
        reason = session.get("stop_reason", "unknown")
        stats["stop_reasons"][reason] = stats["stop_reasons"].get(reason, 0) + 1
    elif session.get("status") == "unsafe":
        stats["unsafe"] += 1

    if session.get("ingredients_input"):
        stats["total_ingredients_saved"] += len(session["ingredients_input"])

    if session.get("recipe_id"):
        rid = session["recipe_id"]
        stats["top_recipes"][rid] = stats["top_recipes"].get(rid, 0) + 1
        stats["total_recipes_cooked"] += 1

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def load_history() -> dict:
    ensure_dirs()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_stats_summary() -> dict:
    """Get a clean summary dict for use in conversation."""
    h = load_history()
    s = h["stats"]
    return {
        "total": s["total_sessions"],
        "completed": s["completed"],
        "stopped": s["stopped"],
        "unsafe": s["unsafe"],
        "ingredients": s["total_ingredients_saved"],
        "recipes": s["total_recipes_cooked"],
        "streak": s["streak_days"],
        "top_recipes": dict(sorted(s["top_recipes"].items(), key=lambda x: x[1], reverse=True)[:3])
    }


def format_stats() -> str:
    """Human-readable stats for display."""
    h = load_history()
    s = h["stats"]
    t = s["total_sessions"]
    c = s["completed"]
    rate = round((c / t * 100), 1) if t > 0 else 0
    streak = s.get("streak_days", 0)

    lines = [
        "📊 *Statistik Dont Waste Food*",
        "",
        f"• Total sesi masak: *{t}*",
        f"• Selesai: ✅ *{c}* ({rate}% completion rate)",
        f"• Dihentikan: ⏹️ *{s['stopped']}*",
        f"• Tidak aman: 🚫 *{s['unsafe']}*",
        f"• Total bahan diolah: 🛒 *{s['total_ingredients_saved']}*",
        f"• Total resep dimasak: 🍳 *{s['total_recipes_cooked']}*",
    ]

    if streak > 0:
        lines.append(f"• Streak: 🔥 *{streak} hari*")

    top = dict(sorted(s["top_recipes"].items(), key=lambda x: x[1], reverse=True)[:3])
    if top:
        lines.append("")
        lines.append("🏆 *Resep paling sering dimasak:*")
        for rid, count in top.items():
            name = rid.replace("_", " ").title()
            lines.append(f"   • {name} — {count}x")

    reasons = dict(sorted(s["stop_reasons"].items(), key=lambda x: x[1], reverse=True)[:3])
    if reasons:
        lines.append("")
        lines.append("⚠️ *Alasan berhenti:*")
        for reason, count in reasons.items():
            lines.append(f"   • {reason}: {count}x")

    return "\n".join(lines)


def format_history(limit: int = 10) -> str:
    """Human-readable session history."""
    h = load_history()
    sessions = h["sessions"][:limit]

    if not sessions:
        return ("Belum ada riwayat masak sama sekali! 🍳\n\n"
                "Yuk mulai dari sekarang — kasih tahu aku bahan apa yang ada di kulkasmu!")

    lines = ["📋 *Riwayat Masak Terakhir*", ""]
    for i, s in enumerate(sessions, 1):
        emoji = {"completed": "✅", "stopped": "⏹️", "unsafe": "🚫"}.get(s.get("status"), "❓")
        ingredients = s.get("ingredients_input", [])
        short_ing = ", ".join(ingredients[:3])
        if len(ingredients) > 3:
            short_ing += f" +{len(ingredients) - 3}"
        recipe = s.get("recipe_name", "—")
        rating = s.get("rating")
        rating_str = f"{'⭐' * rating}" if rating else ""
        lines.append(f"{i}. {emoji} *{s['date']}* — {recipe}")
        lines.append(f"   Bahan: {short_ing}")
        if rating_str:
            lines.append(f"   Rating: {rating_str}")
        if s.get("stop_reason"):
            lines.append(f"   ⏹️ Alasan: {s['stop_reason']}")
        lines.append("")

    return "\n".join(lines)


def delete_all() -> str:
    import shutil
    if os.path.exists(WORKSPACE):
        shutil.rmtree(WORKSPACE)
    ensure_dirs()
    return "Semua data riwayat dihapus. Mulai dari nol! 🚀"


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "stats":
        print(format_stats())
    elif cmd == "history":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        print(format_history(limit))
    elif cmd == "clear":
        print(delete_all())
    else:
        print("Usage: session_manager.py [stats|history|clear]")
