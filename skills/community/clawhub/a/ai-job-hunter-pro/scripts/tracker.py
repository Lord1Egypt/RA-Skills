#!/usr/bin/env python3
"""
AI Job Hunter Pro — Application Tracker
Status tracking, daily reports, and funnel analytics.
"""

import argparse
import json
import os
import sqlite3
from datetime import datetime, timedelta
from collections import Counter

DB_PATH = os.path.expanduser("~/.ai-job-hunter-pro/applications.db")

# ---------------------------------------------------------------------------
# Status Constants
# ---------------------------------------------------------------------------
STATUSES = ["discovered", "applied", "screening", "interview", "offer", "rejected"]
STATUS_EMOJI = {
    "discovered": "🔍",
    "applied": "📨",
    "screening": "📋",
    "interview": "💬",
    "offer": "🎉",
    "rejected": "❌"
}

# ---------------------------------------------------------------------------
# Tracker
# ---------------------------------------------------------------------------
class ApplicationTracker:
    def __init__(self, db_path=DB_PATH):
        if not os.path.exists(db_path):
            print(f"[ERROR] Database not found at {db_path}")
            print("Run the apply pipeline first to create the database.")
            self.conn = None
            return
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def update_status(self, job_id: str, new_status: str, notes: str = None) -> dict:
        """Update an application's status."""
        if new_status not in STATUSES:
            return {"error": f"Invalid status. Must be one of: {', '.join(STATUSES)}"}

        cur = self.conn.execute(
            "SELECT status FROM applications WHERE job_id = ?", (job_id,)
        )
        row = cur.fetchone()
        if not row:
            return {"error": f"Application not found: {job_id}"}

        old_status = row["status"]
        now = datetime.now().isoformat()

        self.conn.execute(
            "UPDATE applications SET status = ?, updated_at = ?, notes = COALESCE(?, notes) WHERE job_id = ?",
            (new_status, now, notes, job_id)
        )
        self.conn.execute(
            "INSERT INTO status_history (application_id, old_status, new_status, changed_at) VALUES (?, ?, ?, ?)",
            (f"app_{job_id}", old_status, new_status, now)
        )
        self.conn.commit()

        return {
            "job_id": job_id,
            "old_status": f"{STATUS_EMOJI.get(old_status, '')} {old_status}",
            "new_status": f"{STATUS_EMOJI.get(new_status, '')} {new_status}",
            "updated_at": now
        }

    def get_daily_report(self) -> dict:
        """Generate daily summary report."""
        today = datetime.now().date().isoformat()
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()

        # Status distribution
        status_counts = {}
        for row in self.conn.execute("SELECT status, COUNT(*) as cnt FROM applications GROUP BY status"):
            status_counts[row["status"]] = row["cnt"]

        # Today's activity
        today_applied = self.conn.execute(
            "SELECT COUNT(*) as cnt FROM applications WHERE applied_at LIKE ?",
            (f"{today}%",)
        ).fetchone()["cnt"]

        # This week's activity
        week_applied = self.conn.execute(
            "SELECT COUNT(*) as cnt FROM applications WHERE applied_at > ?",
            (week_ago,)
        ).fetchone()["cnt"]

        # Recent status changes
        recent_changes = []
        for row in self.conn.execute("""
            SELECT sh.*, a.job_title, a.company
            FROM status_history sh
            JOIN applications a ON sh.application_id = 'app_' || a.job_id
            ORDER BY sh.changed_at DESC LIMIT 10
        """):
            recent_changes.append({
                "job": f"{row['job_title']} @ {row['company']}",
                "change": f"{row['old_status']} → {row['new_status']}",
                "when": row["changed_at"]
            })

        # Top matches not yet applied
        pending = []
        for row in self.conn.execute("""
            SELECT job_title, company, match_score, platform
            FROM applications
            WHERE status = 'discovered'
            ORDER BY match_score DESC LIMIT 5
        """):
            pending.append(dict(row))

        total = sum(status_counts.values())

        return {
            "report_date": today,
            "summary": {
                "total_tracked": total,
                "applied_today": today_applied,
                "applied_this_week": week_applied,
            },
            "status_distribution": {
                f"{STATUS_EMOJI.get(s, '')} {s}": status_counts.get(s, 0)
                for s in STATUSES
            },
            "funnel_analysis": self._calculate_funnel(status_counts),
            "recent_activity": recent_changes[:5],
            "pending_high_matches": pending,
        }

    def _calculate_funnel(self, status_counts: dict) -> dict:
        """Calculate conversion rates between stages."""
        funnel = {}
        prev_count = None
        for status in STATUSES:
            count = status_counts.get(status, 0)
            if prev_count is not None and prev_count > 0:
                rate = round(count / prev_count * 100, 1)
                funnel[f"{STATUSES[STATUSES.index(status)-1]} → {status}"] = f"{rate}%"
            prev_count = (prev_count or 0) + count if status != "rejected" else prev_count

        # Overall success rate
        total_applied = sum(status_counts.get(s, 0) for s in ["applied", "screening", "interview", "offer"])
        offers = status_counts.get("offer", 0)
        if total_applied > 0:
            funnel["overall_success_rate"] = f"{round(offers / total_applied * 100, 1)}%"

        return funnel

    def get_all_applications(self, status_filter: str = None) -> list:
        """List all applications, optionally filtered by status."""
        query = "SELECT * FROM applications"
        params = []
        if status_filter:
            query += " WHERE status = ?"
            params.append(status_filter)
        query += " ORDER BY match_score DESC"

        return [dict(row) for row in self.conn.execute(query, params)]

    def get_analytics(self) -> dict:
        """Advanced analytics: platform performance, response rates, timing."""
        # Platform breakdown
        platform_stats = {}
        for row in self.conn.execute("""
            SELECT platform, status, COUNT(*) as cnt
            FROM applications
            GROUP BY platform, status
        """):
            platform = row["platform"] or "unknown"
            if platform not in platform_stats:
                platform_stats[platform] = {}
            platform_stats[platform][row["status"]] = row["cnt"]

        # Average match score by status
        score_by_status = {}
        for row in self.conn.execute("""
            SELECT status, AVG(match_score) as avg_score, COUNT(*) as cnt
            FROM applications
            WHERE match_score > 0
            GROUP BY status
        """):
            score_by_status[row["status"]] = {
                "avg_match_score": round(row["avg_score"], 3),
                "count": row["cnt"]
            }

        # Time-to-response (applied → screening/interview)
        response_times = []
        for row in self.conn.execute("""
            SELECT a.applied_at, MIN(sh.changed_at) as first_response
            FROM applications a
            JOIN status_history sh ON sh.application_id = 'app_' || a.job_id
            WHERE a.applied_at IS NOT NULL
              AND sh.new_status IN ('screening', 'interview')
            GROUP BY a.job_id
        """):
            if row["applied_at"] and row["first_response"]:
                try:
                    applied = datetime.fromisoformat(row["applied_at"])
                    responded = datetime.fromisoformat(row["first_response"])
                    days = (responded - applied).days
                    response_times.append(days)
                except ValueError:
                    pass

        avg_response_days = round(sum(response_times) / len(response_times), 1) if response_times else None

        return {
            "platform_breakdown": platform_stats,
            "score_by_status": score_by_status,
            "avg_response_time_days": avg_response_days,
            "total_response_data_points": len(response_times)
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter Pro — Application Tracker")
    parser.add_argument("--report", choices=["daily", "analytics", "list"],
                        help="Report type to generate")
    parser.add_argument("--update", type=str, help="Job ID to update status")
    parser.add_argument("--status", type=str, help="New status for --update")
    parser.add_argument("--notes", type=str, help="Notes for status update")
    parser.add_argument("--filter", type=str, help="Filter applications by status")

    args = parser.parse_args()
    tracker = ApplicationTracker()

    if tracker.conn is None:
        return

    if args.update:
        if not args.status:
            print("[ERROR] --status required with --update")
            return
        result = tracker.update_status(args.update, args.status, args.notes)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.report == "daily":
        report = tracker.get_daily_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    if args.report == "analytics":
        analytics = tracker.get_analytics()
        print(json.dumps(analytics, indent=2, ensure_ascii=False))
        return

    if args.report == "list":
        apps = tracker.get_all_applications(status_filter=args.filter)
        print(json.dumps(apps, indent=2, ensure_ascii=False))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
