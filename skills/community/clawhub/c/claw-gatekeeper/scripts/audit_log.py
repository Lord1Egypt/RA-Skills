#!/usr/bin/env python3
"""
Claw-Gatekeeper Audit Log Manager
Records and analyzes all security decisions with comprehensive reporting

Merged from: SafeClaw (operation_logger.py) + Claw-Guardian (audit_log.py)
Features:
- Complete audit trail
- Statistical analysis
- Report generation
- Log rotation and archival
"""

import json
import os
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class AuditEntry:
    """Audit log entry"""
    timestamp: str
    operation_type: str
    operation_detail: str
    risk_level: str
    risk_score: int
    decision: str
    user_comment: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AuditLog:
    """Comprehensive audit log manager"""
    
    def __init__(self, log_dir: Optional[str] = None):
        self.log_dir = Path(log_dir) if log_dir else Path.home() / ".claw-gatekeeper" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_log = self._get_current_log_path()
        
        # Statistics tracking
        self.stats_cache: Optional[Tuple[datetime, Dict]] = None
        self.stats_cache_ttl = 60  # seconds
    
    def _get_current_log_path(self) -> Path:
        """Get current month's log file path"""
        return self.log_dir / f"audit_{datetime.now().strftime('%Y%m')}.jsonl"
    
    def log(self, entry: AuditEntry):
        """Log an audit entry"""
        self.current_log = self._get_current_log_path()
        
        try:
            with open(self.current_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Warning: Could not write to audit log: {e}", file=os.sys.stderr)
    
    def log_simple(self, operation_type: str, operation_detail: str,
                   risk_level: str, risk_score: int, decision: str,
                   comment: str = "", metadata: Optional[Dict] = None):
        """Simplified logging with automatic timestamp"""
        entry = AuditEntry(
            timestamp=datetime.now().isoformat(),
            operation_type=operation_type,
            operation_detail=operation_detail,
            risk_level=risk_level,
            risk_score=risk_score,
            decision=decision,
            user_comment=comment,
            metadata=metadata
        )
        self.log(entry)
    
    def query(self, days: int = 7, risk_level: Optional[str] = None,
             decision: Optional[str] = None, 
             operation_type: Optional[str] = None,
             start_date: Optional[str] = None,
             end_date: Optional[str] = None) -> List[Dict]:
        """
        Query audit log entries with flexible filters
        
        Args:
            days: Number of days to look back (ignored if start_date provided)
            risk_level: Filter by risk level (CRITICAL/HIGH/MEDIUM/LOW)
            decision: Filter by decision (allow_once/allow_always/deny_once/deny_always)
            operation_type: Filter by operation type
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
        """
        # Determine date range
        if start_date:
            since = datetime.fromisoformat(start_date)
        else:
            since = datetime.now() - timedelta(days=days)
        
        until = datetime.fromisoformat(end_date) if end_date else datetime.now()
        
        entries = []
        
        # Iterate all log files
        for log_file in sorted(self.log_dir.glob("audit_*.jsonl*")):
            # Check file time range
            try:
                file_month = log_file.stem.split('_')[1]
                file_date = datetime.strptime(file_month, "%Y%m")
                if file_date < since.replace(day=1):
                    continue
            except:
                pass
            
            # Read entries from file
            file_entries = self._read_log_file(log_file)
            
            for entry in file_entries:
                try:
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    
                    # Time range filter
                    if entry_time < since or entry_time > until:
                        continue
                    
                    # Apply other filters
                    if risk_level and entry.get('risk_level') != risk_level:
                        continue
                    if decision and entry.get('decision') != decision:
                        continue
                    if operation_type and entry.get('operation_type') != operation_type:
                        continue
                    
                    entries.append(entry)
                except (KeyError, ValueError):
                    continue
        
        return sorted(entries, key=lambda x: x['timestamp'], reverse=True)
    
    def _read_log_file(self, log_file: Path) -> List[Dict]:
        """Read log file (supports compressed files)"""
        entries = []
        
        try:
            if str(log_file).endswith('.gz'):
                with gzip.open(log_file, 'rt', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                entries.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
            else:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                entries.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            print(f"Error reading {log_file}: {e}", file=os.sys.stderr)
        
        return entries
    
    def get_statistics(self, days: int = 7, use_cache: bool = True) -> Dict[str, Any]:
        """Get comprehensive statistics with caching"""
        # Check cache
        if use_cache and self.stats_cache:
            cache_time, cache_data = self.stats_cache
            if (datetime.now() - cache_time).seconds < self.stats_cache_ttl:
                return cache_data
        
        operations = self.query(days=days)
        
        if not operations:
            stats = {
                "period_days": days,
                "total_operations": 0,
                "message": "No operations found in specified period"
            }
            self.stats_cache = (datetime.now(), stats)
            return stats
        
        stats = {
            "period_days": days,
            "total_operations": len(operations),
            "by_risk_level": defaultdict(int),
            "by_decision": defaultdict(int),
            "by_operation_type": defaultdict(int),
            "by_day": defaultdict(int),
            "average_risk_score": 0.0,
            "approval_rate": 0.0,
            "denial_rate": 0.0,
            "critical_count": 0,
            "high_count": 0,
            "trend": "stable"
        }
        
        total_risk = 0
        approved_count = 0
        denied_count = 0
        daily_risk_scores = defaultdict(list)
        
        for op in operations:
            # Risk level stats
            risk = op.get('risk_level', 'UNKNOWN')
            stats['by_risk_level'][risk] += 1
            
            if risk == "CRITICAL":
                stats['critical_count'] += 1
            elif risk == "HIGH":
                stats['high_count'] += 1
            
            # Decision stats
            decision = op.get('decision', 'UNKNOWN')
            stats['by_decision'][decision] += 1
            
            if 'allow' in decision:
                approved_count += 1
            elif 'deny' in decision:
                denied_count += 1
            
            # Operation type stats
            op_type = op.get('operation_type', 'UNKNOWN')
            stats['by_operation_type'][op_type] += 1
            
            # Daily stats
            try:
                day = op['timestamp'][:10]  # YYYY-MM-DD
                stats['by_day'][day] += 1
                daily_risk_scores[day].append(op.get('risk_score', 0))
            except:
                pass
            
            # Risk score
            total_risk += op.get('risk_score', 0)
        
        # Calculate averages
        stats['average_risk_score'] = round(total_risk / len(operations), 2)
        stats['approval_rate'] = round(approved_count / len(operations) * 100, 2)
        stats['denial_rate'] = round(denied_count / len(operations) * 100, 2)
        
        # Calculate trend
        if len(stats['by_day']) >= 2:
            days_sorted = sorted(stats['by_day'].keys())
            first_half = days_sorted[:len(days_sorted)//2]
            second_half = days_sorted[len(days_sorted)//2:]
            
            first_avg = sum(stats['by_day'][d] for d in first_half) / len(first_half)
            second_avg = sum(stats['by_day'][d] for d in second_half) / len(second_half)
            
            if second_avg > first_avg * 1.2:
                stats['trend'] = "increasing"
            elif second_avg < first_avg * 0.8:
                stats['trend'] = "decreasing"
            else:
                stats['trend'] = "stable"
        
        # Convert defaultdicts to regular dicts for JSON serialization
        stats['by_risk_level'] = dict(stats['by_risk_level'])
        stats['by_decision'] = dict(stats['by_decision'])
        stats['by_operation_type'] = dict(stats['by_operation_type'])
        stats['by_day'] = dict(stats['by_day'])
        
        # Update cache
        self.stats_cache = (datetime.now(), stats)
        
        return stats
    
    def get_high_risk_operations(self, limit: int = 20) -> List[Dict]:
        """Get recent high-risk operations"""
        critical = self.query(days=30, risk_level="CRITICAL")[:limit//2]
        high = self.query(days=30, risk_level="HIGH")[:limit//2]
        return sorted(critical + high, 
                     key=lambda x: x['timestamp'], 
                     reverse=True)[:limit]
    
    def get_denied_operations(self, days: int = 7) -> List[Dict]:
        """Get recently denied operations"""
        denied = self.query(days=days, decision="deny_once")
        denied_always = self.query(days=days, decision="deny_always")
        return sorted(denied + denied_always,
                     key=lambda x: x['timestamp'],
                     reverse=True)
    
    def get_repeated_denials(self, threshold: int = 3) -> List[Dict]:
        """Find operations that have been repeatedly denied"""
        denied = self.get_denied_operations(days=30)
        
        # Group by operation detail
        operation_counts = defaultdict(list)
        for entry in denied:
            key = f"{entry.get('operation_type')}:{entry.get('operation_detail', '')}"
            operation_counts[key].append(entry)
        
        # Find repeated ones
        repeated = []
        for key, entries in operation_counts.items():
            if len(entries) >= threshold:
                repeated.append({
                    "operation": key,
                    "count": len(entries),
                    "first_seen": entries[-1]['timestamp'],
                    "last_seen": entries[0]['timestamp'],
                    "entries": entries[:5]  # Include last 5 occurrences
                })
        
        return sorted(repeated, key=lambda x: x['count'], reverse=True)
    
    def archive_old_logs(self, keep_months: int = 3):
        """Archive old logs to save space"""
        cutoff = datetime.now() - timedelta(days=30 * keep_months)
        archived = 0
        
        for log_file in self.log_dir.glob("audit_*.jsonl"):
            try:
                file_month = log_file.stem.split('_')[1]
                file_date = datetime.strptime(file_month, "%Y%m")
                
                if file_date < cutoff:
                    archive_path = log_file.with_suffix('.jsonl.gz')
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(archive_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    log_file.unlink()
                    archived += 1
                    print(f"Archived {log_file.name}")
            except Exception as e:
                print(f"Error archiving {log_file}: {e}", file=os.sys.stderr)
        
        if archived:
            print(f"Archived {archived} log file(s)")
    
    def export(self, output_path: str, days: int = 30, 
               format: str = "json"):
        """Export logs to file"""
        entries = self.query(days=days)
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2)
        elif format == "jsonl":
            with open(output_path, 'w', encoding='utf-8') as f:
                for entry in entries:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if entries:
                    writer = csv.DictWriter(f, fieldnames=entries[0].keys())
                    writer.writeheader()
                    writer.writerows(entries)
        
        print(f"Exported {len(entries)} entries to {output_path}")
    
    def generate_report(self, days: int = 7, format: str = "text") -> str:
        """Generate a comprehensive security report"""
        stats = self.get_statistics(days)
        
        if stats["total_operations"] == 0:
            return "No operations recorded in the specified period."
        
        if format == "json":
            return json.dumps(stats, indent=2)
        
        # Text format
        lines = [
            "=" * 70,
            "CLAW-GUARDIAN SECURITY AUDIT REPORT",
            "=" * 70,
            f"Report Period: Last {days} days",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 70,
            f"Total Operations Monitored: {stats['total_operations']}",
            f"Average Risk Score: {stats['average_risk_score']}/100",
            f"Overall Approval Rate: {stats['approval_rate']}%",
            f"Overall Denial Rate: {stats['denial_rate']}%",
            f"Activity Trend: {stats['trend'].title()}",
            "",
            "RISK DISTRIBUTION",
            "-" * 70,
        ]
        
        for level, count in sorted(stats['by_risk_level'].items(), 
                                   key=lambda x: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN'].index(x[0]) if x[0] in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN'] else 99):
            percentage = round(count / stats['total_operations'] * 100, 1)
            emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(level, "⚪")
            lines.append(f"  {emoji} {level:12} {count:5} ({percentage:5.1f}%)")
        
        lines.extend([
            "",
            "DECISION BREAKDOWN",
            "-" * 70,
        ])
        
        for decision, count in sorted(stats['by_decision'].items()):
            percentage = round(count / stats['total_operations'] * 100, 1)
            emoji = "✅" if "allow" in decision else "❌"
            lines.append(f"  {emoji} {decision:20} {count:5} ({percentage:5.1f}%)")
        
        lines.extend([
            "",
            "OPERATION TYPES",
            "-" * 70,
        ])
        
        for op_type, count in sorted(stats['by_operation_type'].items(), 
                                     key=lambda x: x[1], reverse=True):
            percentage = round(count / stats['total_operations'] * 100, 1)
            emoji = {"file": "📁", "shell": "💻", "network": "🌐", 
                    "skill": "📦", "system": "⚙️"}.get(op_type, "📋")
            lines.append(f"  {emoji} {op_type:15} {count:5} ({percentage:5.1f}%)")
        
        # High-risk summary
        if stats.get('critical_count', 0) > 0 or stats.get('high_count', 0) > 0:
            lines.extend([
                "",
                "⚠️  HIGH-RISK ACTIVITY",
                "-" * 70,
                f"  CRITICAL operations: {stats.get('critical_count', 0)}",
                f"  HIGH operations: {stats.get('high_count', 0)}",
            ])
        
        # Repeated denials
        repeated = self.get_repeated_denials(threshold=3)
        if repeated:
            lines.extend([
                "",
                "🔄 REPEATED DENIALS",
                "-" * 70,
                "The following operations have been denied multiple times:",
            ])
            for item in repeated[:5]:
                lines.append(f"  • {item['operation'][:50]}: {item['count']} denials")
        
        lines.extend([
            "",
            "=" * 70,
        ])
        
        return "\n".join(lines)
    
    def clear(self, confirm: bool = False):
        """Clear all logs"""
        if not confirm:
            print("Warning: This will permanently delete all audit logs.")
            print("Use clear(confirm=True) to proceed.")
            return
        
        count = 0
        for log_file in self.log_dir.glob("audit_*"):
            log_file.unlink()
            count += 1
        
        print(f"Cleared {count} log file(s)")


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Claw-Guardian Audit Log Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s recent 20
  %(prog)s stats 7
  %(prog)s highrisk 10
  %(prog)s report 7 --format text
  %(prog)s export security_report.json 30
        """
    )
    
    parser.add_argument("command", choices=[
        "recent", "stats", "highrisk", "denied", "repeated",
        "report", "export", "archive", "query", "clear"
    ])
    parser.add_argument("param", nargs="?", help="Parameter (limit, days, etc.)")
    parser.add_argument("--days", "-d", type=int, help="Number of days")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Result limit")
    parser.add_argument("--risk", "-r", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                       help="Filter by risk level")
    parser.add_argument("--decision", choices=["allow_once", "allow_always", 
                                              "deny_once", "deny_always"],
                       help="Filter by decision")
    parser.add_argument("--type", "-t", help="Filter by operation type")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text",
                       help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    audit = AuditLog()
    
    if args.command == "recent":
        limit = int(args.param) if args.param else args.limit
        ops = audit.query(days=args.days or 7)[:limit]
        print(json.dumps(ops, indent=2))
    
    elif args.command == "stats":
        days = int(args.param) if args.param else (args.days or 7)
        stats = audit.get_statistics(days=days)
        print(json.dumps(stats, indent=2))
    
    elif args.command == "highrisk":
        limit = int(args.param) if args.param else args.limit
        ops = audit.get_high_risk_operations(limit=limit)
        print(json.dumps(ops, indent=2))
    
    elif args.command == "denied":
        days = int(args.param) if args.param else (args.days or 7)
        ops = audit.get_denied_operations(days=days)
        print(json.dumps(ops, indent=2))
    
    elif args.command == "repeated":
        threshold = int(args.param) if args.param else 3
        ops = audit.get_repeated_denials(threshold=threshold)
        print(json.dumps(ops, indent=2))
    
    elif args.command == "report":
        days = int(args.param) if args.param else (args.days or 7)
        report = audit.generate_report(days=days, format=args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to: {args.output}")
        else:
            print(report)
    
    elif args.command == "export":
        output_path = args.param or args.output or "audit_export.json"
        days = args.days or 30
        audit.export(output_path, days=days, format="json")
    
    elif args.command == "archive":
        audit.archive_old_logs()
    
    elif args.command == "query":
        days = int(args.param) if args.param else (args.days or 7)
        ops = audit.query(
            days=days,
            risk_level=args.risk,
            decision=args.decision,
            operation_type=args.type
        )
        print(json.dumps(ops, indent=2))
    
    elif args.command == "clear":
        print("WARNING: This will permanently delete all audit logs!")
        response = input("Type 'yes' to confirm: ")
        if response.lower() == 'yes':
            audit.clear(confirm=True)
        else:
            print("Cancelled")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
