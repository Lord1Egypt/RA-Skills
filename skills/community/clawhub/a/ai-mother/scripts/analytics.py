#!/usr/bin/env python3
"""
AI Mother - Performance Analytics
Analyze AI agent performance patterns and generate insights
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DB_PATH = Path.home() / ".openclaw/skills/ai-mother/ai-mother.db"

def get_agent_stats(pid):
    """Get statistics for a specific agent"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get agent info
    c.execute('SELECT * FROM agents WHERE pid = ?', (pid,))
    agent = c.fetchone()
    if not agent:
        return None
    
    # Get history
    c.execute('''
        SELECT status, COUNT(*), AVG(cpu_percent), AVG(memory_mb)
        FROM history WHERE pid = ?
        GROUP BY status
    ''', (pid,))
    status_stats = c.fetchall()
    
    # Get status transitions
    c.execute('''
        SELECT status, checked_at FROM history 
        WHERE pid = ? ORDER BY checked_at ASC
    ''', (pid,))
    transitions = c.fetchall()
    
    conn.close()
    
    # Calculate metrics
    total_checks = sum(row[1] for row in status_stats)
    status_distribution = {row[0]: row[1] for row in status_stats}
    
    # Detect patterns
    patterns = []
    if status_distribution.get('waiting_api', 0) > total_checks * 0.3:
        patterns.append("⚠️  Frequent rate limiting (>30% of checks)")
    
    if status_distribution.get('idle', 0) > total_checks * 0.5:
        patterns.append("💤 Mostly idle (>50% of checks)")
    
    if status_distribution.get('error', 0) > 5:
        patterns.append("❌ Multiple errors detected")
    
    # Calculate uptime
    runtime_hours = agent[8] / 3600 if agent[8] else 0
    
    return {
        'pid': agent[0],
        'ai_type': agent[1],
        'workdir': agent[2],
        'task': agent[3],
        'current_status': agent[4],
        'runtime_hours': round(runtime_hours, 2),
        'total_checks': total_checks,
        'status_distribution': status_distribution,
        'patterns': patterns,
        'avg_cpu': round(sum(row[2] or 0 for row in status_stats) / len(status_stats), 2) if status_stats else 0,
        'avg_memory_mb': round(sum(row[3] or 0 for row in status_stats) / len(status_stats), 2) if status_stats else 0
    }

def get_all_stats():
    """Get statistics for all agents"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT pid FROM agents')
    pids = [row[0] for row in c.fetchall()]
    conn.close()
    
    return [get_agent_stats(pid) for pid in pids]

def generate_report():
    """Generate a comprehensive report"""
    stats = get_all_stats()
    
    print("=== AI Mother Performance Report ===")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Agents: {len(stats)}")
    print("")
    
    for agent in stats:
        if not agent:
            continue
            
        print(f"📊 PID {agent['pid']} ({agent['ai_type']})")
        print(f"   Project: {agent['workdir']}")
        print(f"   Task: {agent['task']}")
        print(f"   Status: {agent['current_status']}")
        print(f"   Runtime: {agent['runtime_hours']}h")
        print(f"   Checks: {agent['total_checks']}")
        print(f"   Avg CPU: {agent['avg_cpu']}%")
        print(f"   Avg Memory: {agent['avg_memory_mb']}MB")
        
        if agent['status_distribution']:
            print("   Status Distribution:")
            for status, count in agent['status_distribution'].items():
                pct = (count / agent['total_checks']) * 100
                print(f"     - {status}: {count} ({pct:.1f}%)")
        
        if agent['patterns']:
            print("   Patterns Detected:")
            for pattern in agent['patterns']:
                print(f"     {pattern}")
        
        print("")
    
    # Overall insights
    print("=== Overall Insights ===")
    total_runtime = sum(a['runtime_hours'] for a in stats if a)
    avg_runtime = total_runtime / len(stats) if stats else 0
    print(f"Total AI Runtime: {total_runtime:.2f}h")
    print(f"Average Runtime per AI: {avg_runtime:.2f}h")
    
    # Most common issues
    all_patterns = []
    for agent in stats:
        if agent:
            all_patterns.extend(agent['patterns'])
    
    if all_patterns:
        print("\nCommon Issues:")
        pattern_counts = defaultdict(int)
        for p in all_patterns:
            pattern_counts[p] += 1
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {pattern} ({count} agents)")

if __name__ == '__main__':
    import sys
    
    # Initialize DB if needed
    if not DB_PATH.exists():
        from db import init_db
        init_db()
    
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        # Single agent stats
        stats = get_agent_stats(int(sys.argv[1]))
        if stats:
            print(json.dumps(stats, indent=2))
        else:
            print(f"No data for PID {sys.argv[1]}")
    else:
        # Full report
        generate_report()
