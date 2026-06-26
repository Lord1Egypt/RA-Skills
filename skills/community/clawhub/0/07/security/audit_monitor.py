#!/usr/bin/env python3
"""
Agent Reach 审计监控工具
实时监控 Agent Reach 的活动并记录安全事件
"""

import os
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any
import threading
import time

class SecurityEvent:
    """安全事件"""

    SEVERITY_LEVELS = {
        'INFO': 0,
        'WARNING': 1,
        'ERROR': 2,
        'CRITICAL': 3
    }

    def __init__(self, event_type: str, message: str, severity: str = 'INFO',
                 details: Dict[str, Any] = None):
        self.event_type = event_type
        self.message = message
        self.severity = severity
        self.details = details or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type,
            'severity': self.severity,
            'message': self.message,
            'details': self.details
        }


class AuditLogger:
    """审计日志记录器"""

    def __init__(self, log_dir: str = None):
        self.log_dir = Path(log_dir or os.path.expanduser("~/agent-reach-secure/logs"))
        self.log_dir.mkdir(parents=True, exist_ok=True, mode=0o700)

        self.audit_log = self.log_dir / "audit.log"
        self.security_log = self.log_dir / "security_events.jsonl"
        self.access_log = self.log_dir / "access.log"

    def log_event(self, event: SecurityEvent):
        """记录安全事件"""
        # 写入安全事件日志（JSONL 格式）
        with open(self.security_log, 'a') as f:
            f.write(json.dumps(event.to_dict()) + '\n')

        # 写入人类可读的审计日志
        with open(self.audit_log, 'a') as f:
            f.write(f"[{event.timestamp}] [{event.severity}] {event.message}\n")

        # 如果是严重事件，打印到控制台
        if event.severity in ['ERROR', 'CRITICAL']:
            print(f"🚨 [{event.severity}] {event.message}")

    def log_access(self, platform: str, action: str, resource: str, success: bool):
        """记录平台访问"""
        event = SecurityEvent(
            event_type='access',
            message=f"{platform} {action} {resource}",
            severity='WARNING' if not success else 'INFO',
            details={
                'platform': platform,
                'action': action,
                'resource': resource,
                'success': success
            }
        )
        self.log_event(event)

        with open(self.access_log, 'a') as f:
            status = "SUCCESS" if success else "FAILED"
            f.write(f"[{datetime.now()}] {platform} {action} {resource} - {status}\n")

    def get_recent_events(self, hours: int = 24, severity: str = None) -> List[Dict]:
        """获取最近的安全事件"""
        cutoff = datetime.now() - timedelta(hours=hours)
        events = []

        if not self.security_log.exists():
            return events

        with open(self.security_log, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    timestamp = datetime.fromisoformat(event['timestamp'])

                    if timestamp >= cutoff:
                        if severity is None or event['severity'] == severity:
                            events.append(event)
                except (json.JSONDecodeError, KeyError):
                    continue

        return events

    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """获取统计信息"""
        events = self.get_recent_events(hours=days * 24)

        stats = {
            'total_events': len(events),
            'by_severity': {},
            'by_platform': {},
            'failed_requests': 0
        }

        for event in events:
            # 按严重程度统计
            severity = event['severity']
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1

            # 按平台统计
            if event['event_type'] == 'access':
                platform = event['details'].get('platform', 'unknown')
                stats['by_platform'][platform] = stats['by_platform'].get(platform, 0) + 1

                # 失败请求
                if not event['details'].get('success', True):
                    stats['failed_requests'] += 1

        return stats


class SecurityMonitor:
    """安全监控器"""

    # 可疑模式
    SUSPICIOUS_PATTERNS = {
        'rapid_requests': {
            'threshold': 100,  # 每分钟请求数
            'window': 60,  # 秒
            'message': '检测到异常高频请求'
        },
        'failed_auth': {
            'threshold': 5,
            'window': 300,
            'message': '检测到多次认证失败'
        },
        'large_download': {
            'threshold': 100,  # MB
            'message': '检测到异常大量数据下载'
        }
    }

    def __init__(self, audit_logger: AuditLogger = None):
        self.audit = audit_logger or AuditLogger()
        self.request_times = []
        self.failed_auths = []

    def check_request_rate(self) -> bool:
        """检查请求频率"""
        now = time.time()

        # 清理旧记录
        self.request_times = [t for t in self.request_times
                              if now - t < self.SUSPICIOUS_PATTERNS['rapid_requests']['window']]

        # 添加当前请求
        self.request_times.append(now)

        # 检查阈值
        if len(self.request_times) > self.SUSPICIOUS_PATTERNS['rapid_requests']['threshold']:
            event = SecurityEvent(
                event_type='rate_limit',
                message=self.SUSPICIOUS_PATTERNS['rapid_requests']['message'],
                severity='WARNING',
                details={
                    'requests_per_minute': len(self.request_times),
                    'threshold': self.SUSPICIOUS_PATTERNS['rapid_requests']['threshold']
                }
            )
            self.audit.log_event(event)
            return False

        return True

    def check_auth_failure(self, platform: str) -> bool:
        """检查认证失败"""
        now = time.time()

        # 清理旧记录
        self.failed_auths = [t for t in self.failed_auths
                             if now - t < self.SUSPICIOUS_PATTERNS['failed_auth']['window']]

        # 添加当前失败
        self.failed_auths.append(now)

        # 检查阈值
        if len(self.failed_auths) > self.SUSPICIOUS_PATTERNS['failed_auth']['threshold']:
            event = SecurityEvent(
                event_type='auth_failure',
                message=f"{platform} {self.SUSPICIOUS_PATTERNS['failed_auth']['message']}",
                severity='CRITICAL',
                details={
                    'platform': platform,
                    'failures': len(self.failed_auths),
                    'threshold': self.SUSPICIOUS_PATTERNS['failed_auth']['threshold']
                }
            )
            self.audit.log_event(event)
            return False

        return True

    def scan_logs_for_threats(self) -> List[SecurityEvent]:
        """扫描日志查找威胁"""
        threats = []

        # 威胁模式
        threat_patterns = {
            'injection': [
                r'<script>',  # XSS
                r'\.\./',  # 路径遍历
                r';drop\s+table',  # SQL 注入
            ],
            'brute_force': [
                r'authentication failed',
                r'unauthorized',
                r'invalid credentials'
            ],
            'data_exfil': [
                r'downloaded\s+\d+\s*MB',
                r'export.*all'
            ]
        }

        if not self.audit.audit_log.exists():
            return threats

        with open(self.audit.audit_log, 'r') as f:
            for line_no, line in enumerate(f, 1):
                for threat_type, patterns in threat_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            event = SecurityEvent(
                                event_type='threat_detected',
                                message=f"检测到 {threat_type} 模式",
                                severity='WARNING' if threat_type == 'brute_force' else 'CRITICAL',
                                details={
                                    'threat_type': threat_type,
                                    'pattern': pattern,
                                    'line': line.strip(),
                                    'line_no': line_no
                                }
                            )
                            threats.append(event)
                            self.audit.log_event(event)

        return threats


class LogAnalyzer:
    """日志分析工具"""

    def __init__(self, log_dir: str = None):
        self.audit = AuditLogger(log_dir)

    def generate_report(self, days: int = 7) -> str:
        """生成安全报告"""
        stats = self.audit.get_statistics(days)
        events = self.audit.get_recent_events(hours=days * 24)

        report = []
        report.append("=" * 60)
        report.append("Agent Reach 安全审计报告")
        report.append(f"时间范围: 最近 {days} 天")
        report.append("=" * 60)
        report.append("")

        # 总体统计
        report.append("📊 总体统计")
        report.append(f"  总事件数: {stats['total_events']}")
        report.append(f"  失败请求: {stats['failed_requests']}")
        report.append("")

        # 按严重程度
        report.append("🚨 事件按严重程度分布")
        for severity in ['CRITICAL', 'ERROR', 'WARNING', 'INFO']:
            count = stats['by_severity'].get(severity, 0)
            if count > 0:
                bar = '█' * min(count, 50)
                report.append(f"  {severity:8s}: {count:4d} {bar}")
        report.append("")

        # 按平台
        report.append("🌐 平台访问统计")
        for platform, count in sorted(stats['by_platform'].items(),
                                     key=lambda x: x[1], reverse=True):
            report.append(f"  {platform:15s}: {count:4d} 次")
        report.append("")

        # 关键事件
        critical_events = [e for e in events if e['severity'] in ['CRITICAL', 'ERROR']]
        if critical_events:
            report.append("⚠️  关键事件（最近10条）")
            for event in critical_events[-10:]:
                report.append(f"  [{event['timestamp']}] {event['message']}")
            report.append("")

        # 建议
        report.append("💡 安全建议")
        if stats['failed_requests'] > 10:
            report.append("  - 失败请求较多，请检查 Cookie 是否过期")
        if stats['by_severity'].get('CRITICAL', 0) > 0:
            report.append("  - 存在严重安全事件，请立即查看日志")
        report.append("  - 定期轮换 Cookie（建议每月一次）")
        report.append("  - 使用 agent-check 进行日常检查")
        report.append("")

        report.append("=" * 60)

        return "\n".join(report)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Agent Reach 安全审计监控")
    parser.add_argument('action', choices=['report', 'monitor', 'scan'],
                       help='操作类型')
    parser.add_argument('--days', type=int, default=7,
                       help='统计天数（默认7天）')
    parser.add_argument('--output', help='输出报告到文件')

    args = parser.parse_args()

    analyzer = LogAnalyzer()

    if args.action == 'report':
        report = analyzer.generate_report(args.days)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"✅ 报告已保存到: {args.output}")
        else:
            print(report)

    elif args.action == 'monitor':
        monitor = SecurityMonitor()
        print("🔍 开始实时监控（按 Ctrl+C 停止）...")
        print()

        try:
            while True:
                # 模拟请求检查
                monitor.check_request_rate()

                # 扫描日志
                threats = monitor.scan_logs_for_threats()
                if threats:
                    print(f"⚠️  检测到 {len(threats)} 个潜在威胁")

                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n✅ 监控已停止")

    elif args.action == 'scan':
        monitor = SecurityMonitor()
        threats = monitor.scan_logs_for_threats()

        if threats:
            print(f"⚠️  发现 {len(threats)} 个威胁：")
            for threat in threats:
                print(f"  - {threat.to_dict()}")
        else:
            print("✅ 未检测到威胁")


if __name__ == "__main__":
    main()
