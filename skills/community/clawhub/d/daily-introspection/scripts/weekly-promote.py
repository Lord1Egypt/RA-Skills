#!/usr/bin/env python3
"""
weekly-promote: Promote weekly lessons to permanent system rules
Reads all daily introspections from the week, identifies repeated patterns,
promotes mature lessons to AGENTS.md / MEMORY.md / TOOLS.md
"""

import os
import sys
import argparse
from datetime import datetime, timedelta

def get_workspace():
    """Get workspace root"""
    return os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))

def get_references_dir():
    """Get references directory (daily records stored in private dir)"""
    return get_private_data_dir()

def get_private_data_dir():
    """Get private data directory"""
    private_dir = os.path.join(get_workspace(), ".daily-introspection")
    if not os.path.exists(private_dir):
        os.makedirs(private_dir)
    return private_dir

def get_weekly_introspections(year, week):
    """Get all daily introspections for the specified week"""
    refs_dir = get_references_dir()
    intro_files = []
    
    # Simple date-based collection - iterate all introspection files
    for f in os.listdir(refs_dir):
        if f.startswith("introspection-") and f.endswith(".md"):
            # Extract date from filename
            date_str = f.replace("introspection-", "").replace(".md", "")
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                # Check if this date is in the target week
                if dt.isocalendar()[0] == year and dt.isocalendar()[1] == week:
                    full_path = os.path.join(refs_dir, f)
                    with open(full_path, "r", encoding="utf-8") as file:
                        content = file.read()
                    intro_files.append((date_str, content))
            except:
                continue
    
    # Sort by date
    intro_files.sort(key=lambda x: x[0])
    return intro_files

def get_last_week_pending_promotions(year, week):
    """Read last week's evolution report to get list of rules pending promotion this week
    
    Last week's evolution already marked which rules are "Promotion scheduled after this week"
    We read these to double check and make sure none are missed.
    """
    private_dir = get_private_data_dir()
    # Last week is (year, week-1), handle year rollover
    if week == 1:
        last_year = year - 1
        last_week = 52
    else:
        last_year = year
        last_week = week - 1
    evolution_file = os.path.join(private_dir, f"evolution-{last_year % 100}{last_week}.md")
    
    pending = []
    if not os.path.exists(evolution_file):
        return pending
    
    with open(evolution_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Parse the "Rules Remaining in Verification" table
    # All lines with "Promotion scheduled for after ..." are pending
    lines = content.split('\n')
    for line in lines:
        if 'Promotion scheduled for after' in line or 'promotion scheduled' in line:
            pending.append(line.strip())
    
    return pending

def get_current_week():
    """Get current (year, week)"""
    dt = datetime.now()
    return dt.isocalendar()[0], dt.isocalendar()[1]

def main():
    parser = argparse.ArgumentParser(description='Weekly promotion of lessons')
    parser.add_argument('--year', type=int, help='Year')
    parser.add_argument('--week', type=int, help='Week number')
    args = parser.parse_args()

    # Use current week if not specified
    if args.year and args.week:
        year, week = args.year, args.week
    else:
        year, week = get_current_week()

    print(f"[INFO] Starting weekly promotion for {year} Week {week}")

    # Ensure directories exist
    get_private_data_dir()
    refs_dir = get_references_dir()
    if not os.path.exists(refs_dir):
        os.makedirs(refs_dir)

    # Get all daily introspections
    introspections = get_weekly_introspections(year, week)
    
    # Get pending promotions marked last week that should be promoted this week
    pending_promotions = get_last_week_pending_promotions(year, week)
    
    if not introspections and not pending_promotions:
        print("[WARN] No introspections found for this week, exiting")
        sys.exit(0)

    if pending_promotions:
        print(f"[INFO] Found {len(pending_promotions)} pending promotions marked from last week")
    
    print(f"[INFO] Found {len(introspections)} daily introspections this week")
    
    # The actual LLM analysis and rule promotion happens via OpenClaw tool calling
    # This script just sets up the infrastructure and collects the inputs
    # LLM will:
    # 1. Analyze all daily entries from this week
    # 2. Check pending promotions from last week
    # 3. Identify which rules are eligible (>= 1 week no recurrence)
    # 4. Promote mature rules to permanent system files (AGENTS.md / MEMORY.md / TOOLS.md)
    # 5. Write the weekly evolution report
    # 6. Pending rules are already marked from last week, double check

if __name__ == "__main__":
    main()
