"""
Utility functions for error log analyzer.
"""
from typing import List, Dict, Any
from collections import Counter
from datetime import datetime, timedelta
import re


def cluster_errors(errors: List[Any], similarity_threshold: float = 0.8) -> Dict[str, List[Any]]:
    """Group similar errors together."""
    clusters = {}
    
    for error in errors:
        message = error.message if hasattr(error, 'message') else str(error)
        
        # Normalize message for comparison
        normalized = normalize_message(message)
        
        # Find existing cluster or create new one
        found_cluster = None
        for cluster_key in clusters:
            if calculate_similarity(normalized, cluster_key) >= similarity_threshold:
                found_cluster = cluster_key
                break
        
        if found_cluster:
            clusters[found_cluster].append(error)
        else:
            clusters[normalized] = [error]
    
    return clusters


def normalize_message(message: str) -> str:
    """Normalize error message for comparison."""
    # Remove variable parts (numbers, UUIDs, timestamps)
    normalized = re.sub(r'\d+', 'N', message)
    normalized = re.sub(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', 'UUID', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}', 'TIMESTAMP', normalized)
    normalized = re.sub(r'/[\w/.-]+', '/PATH', normalized)  # Replace file paths
    
    return normalized.lower().strip()


def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity between two strings using simple approach."""
    # Use Levenshtein distance ratio if available
    try:
        from Levenshtein import ratio
        return ratio(str1, str2)
    except ImportError:
        # Fallback to simple word overlap
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)


def detect_error_trends(errors: List[Any], time_window_hours: int = 24) -> Dict[str, Any]:
    """Detect trends in error frequency."""
    from datetime import timezone
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(hours=time_window_hours)
    
    # Filter errors within time window
    recent_errors = []
    for e in errors:
        if hasattr(e, 'timestamp') and e.timestamp:
            # Ensure both datetimes are timezone-aware for comparison
            ts = e.timestamp
            if ts.tzinfo is None:
                # Assume UTC if no timezone
                ts = ts.replace(tzinfo=timezone.utc)
            if ts >= window_start:
                recent_errors.append(e)
    
    if not recent_errors:
        return {
            'trend': 'stable',
            'error_count': 0,
            'spike_detected': False
        }
    
    # Count errors by hour
    hourly_counts = Counter()
    for error in recent_errors:
        hour = error.timestamp.replace(minute=0, second=0, microsecond=0)
        hourly_counts[hour] += 1
    
    # Detect spike (more than 2x average in last hour)
    if len(hourly_counts) >= 2:
        avg_count = sum(hourly_counts.values()) / len(hourly_counts)
        last_hour_count = hourly_counts[max(hourly_counts.keys())]
        
        spike_detected = last_hour_count > avg_count * 2
        
        if spike_detected:
            trend = 'spike'
        elif last_hour_count > avg_count:
            trend = 'increasing'
        elif last_hour_count < avg_count:
            trend = 'decreasing'
        else:
            trend = 'stable'
    else:
        trend = 'stable'
        spike_detected = False
    
    return {
        'trend': trend,
        'error_count': len(recent_errors),
        'spike_detected': spike_detected,
        'hourly_distribution': dict(hourly_counts)
    }


def filter_noise(errors: List[Any], ignore_patterns: List[str] = None) -> List[Any]:
    """Filter out known/expected errors."""
    if not ignore_patterns:
        ignore_patterns = [
            'GET /health',
            'GET /favicon.ico',
            'Connection reset by peer',
            'client closed connection'
        ]
    
    filtered = []
    for error in errors:
        message = error.message if hasattr(error, 'message') else str(error)
        
        # Check if error matches any ignore pattern
        should_ignore = False
        for pattern in ignore_patterns:
            if pattern.lower() in message.lower():
                should_ignore = True
                break
        
        if not should_ignore:
            filtered.append(error)
    
    return filtered


def assess_severity(error: Any) -> str:
    """Assess error severity based on type and context."""
    message = error.message if hasattr(error, 'message') else str(error)
    level = error.level if hasattr(error, 'level') else 'INFO'
    
    # Critical patterns
    critical_patterns = [
        'out of memory',
        'database connection failed',
        'authentication failed',
        'security violation',
        'data corruption'
    ]
    
    # High priority patterns
    high_patterns = [
        'connection refused',
        'timeout',
        'failed to',
        'unable to',
        'error'
    ]
    
    message_lower = message.lower()
    
    if level == 'ERROR' or level == 'FATAL':
        for pattern in critical_patterns:
            if pattern in message_lower:
                return 'CRITICAL'
        
        for pattern in high_patterns:
            if pattern in message_lower:
                return 'HIGH'
        
        return 'MEDIUM'
    
    elif level == 'WARN':
        return 'MEDIUM'
    
    else:
        return 'LOW'


def generate_report(analysis_results: List[Dict], format: str = 'text') -> str:
    """Generate analysis report in specified format."""
    
    if format == 'json':
        import json
        return json.dumps(analysis_results, indent=2, default=str)
    
    elif format == 'markdown':
        return _generate_markdown_report(analysis_results)
    
    else:  # text format
        return _generate_text_report(analysis_results)


def _generate_text_report(results: List[Dict]) -> str:
    """Generate plain text report."""
    report = []
    report.append("=" * 60)
    report.append("ERROR LOG ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Summary
    total_errors = len(results)
    critical = sum(1 for r in results if r.get('severity') == 'CRITICAL')
    high = sum(1 for r in results if r.get('severity') == 'HIGH')
    
    report.append(f"Total errors analyzed: {total_errors}")
    report.append(f"Critical: {critical}, High: {high}")
    report.append("")
    
    # Details
    for i, result in enumerate(results[:10], 1):  # Show top 10
        report.append(f"\n--- Error #{i} ---")
        report.append(f"Type: {result.get('error_type', 'Unknown')}")
        report.append(f"Severity: {result.get('severity', 'Unknown')}")
        report.append(f"\nWhat happened:")
        report.append(result.get('explanation', 'No explanation available'))
        report.append(f"\nHow to fix:")
        for suggestion in result.get('suggestions', []):
            report.append(f"  • {suggestion}")
    
    return '\n'.join(report)


def _generate_markdown_report(results: List[Dict]) -> str:
    """Generate markdown report."""
    report = []
    report.append("# Error Log Analysis Report\n")
    
    # Summary
    total = len(results)
    critical = sum(1 for r in results if r.get('severity') == 'CRITICAL')
    high = sum(1 for r in results if r.get('severity') == 'HIGH')
    
    report.append("## Summary\n")
    report.append(f"- **Total errors**: {total}")
    report.append(f"- **Critical**: {critical}")
    report.append(f"- **High priority**: {high}\n")
    
    # Details
    report.append("## Top Errors\n")
    for i, result in enumerate(results[:10], 1):
        severity_emoji = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }.get(result.get('severity', 'MEDIUM'), '⚪')
        
        report.append(f"### {i}. {severity_emoji} {result.get('error_type', 'Unknown Error')}\n")
        report.append(f"**Severity**: {result.get('severity', 'Unknown')}\n")
        report.append(f"**What happened**: {result.get('explanation', '')}\n")
        report.append(f"**How to fix**:")
        for suggestion in result.get('suggestions', []):
            report.append(f"- {suggestion}")
        report.append("")
    
    return '\n'.join(report)
