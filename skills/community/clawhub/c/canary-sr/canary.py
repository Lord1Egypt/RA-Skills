#!/usr/bin/env python3
"""
Canary — Agent Safety Tripwire System
Main safety monitoring engine for AI agents.

Author: Shadow Rose
License: MIT
"""

import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class CanaryMonitor:
    """Main safety monitoring engine."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Canary monitor.
        
        Args:
            config_path: Path to configuration file (default: config.py)
        """
        self.config = self._load_config(config_path)
        self.log_file = Path(self.config.get('log_file', 'canary.log'))
        self.action_log = []
        self.alert_history = []
        self.rate_limits = {}
        self.violation_count = 0
        self.start_time = time.time()
        
        # Load protected paths and patterns
        self.protected_paths = set(self.config.get('protected_paths', []))
        self.forbidden_patterns = self.config.get('forbidden_patterns', [])
        self.severity_levels = self.config.get('severity_levels', {})
        
        # Auto-halt threshold
        self.halt_threshold = self.config.get('halt_threshold', 5)
        self.halted = False
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from a JSON file or use defaults."""
        if config_path and Path(config_path).exists():
            if not config_path.endswith(".json"):
                raise ValueError(f"Config must be a .json file: {config_path}")
            if os.path.getsize(config_path) > 1_000_000:
                raise ValueError(f"Config file too large (>1MB): {config_path}")
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default config
        return {
            'log_file': 'canary.log',
            'protected_paths': [
                '/etc/',
                '/sys/',
                '/proc/',
                '~/.ssh/',
                '~/.aws/',
            ],
            'forbidden_patterns': [
                r'rm\s+-rf\s+/',
                r'chmod\s+777',
                r'curl.*\|\s*sh',
                r'eval\s*\(',
                r'exec\s*\(',
            ],
            'severity_levels': {
                'critical': 100,
                'high': 75,
                'medium': 50,
                'low': 25,
                'info': 10,
            },
            'halt_threshold': 5,
            'rate_limits': {
                'file_operations': {'limit': 100, 'window': 60},
                'network_requests': {'limit': 50, 'window': 60},
                'command_executions': {'limit': 20, 'window': 60},
            },
        }
    
    def check_path(self, path: str, operation: str = 'access') -> Tuple[bool, Optional[str]]:
        """
        Check if path operation is safe.
        
        Args:
            path: Path to check
            operation: Type of operation (read, write, delete, access)
            
        Returns:
            (is_safe, reason) tuple
        """
        if self.halted:
            return False, "Canary: System halted due to safety violations"
        
        # Expand home directory
        expanded_path = os.path.expanduser(path)
        abs_path = os.path.abspath(expanded_path)
        
        # Check against protected paths
        for protected in self.protected_paths:
            protected_expanded = os.path.expanduser(protected)
            protected_abs = os.path.abspath(protected_expanded)
            
            if abs_path.startswith(protected_abs):
                reason = f"Canary: Protected path access blocked: {path}"
                self._log_violation('critical', f"Attempted {operation} on protected path: {path}")
                return False, reason
        
        # Check for dangerous patterns in path
        for pattern in self.forbidden_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                reason = f"Canary: Forbidden pattern in path: {pattern}"
                self._log_violation('high', f"Forbidden pattern in path: {path}")
                return False, reason
        
        # Log safe operation
        self._log_action(operation, path, 'info')
        
        return True, None
    
    def check_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        Check if command is safe to execute.
        
        Args:
            command: Command string to check
            
        Returns:
            (is_safe, reason) tuple
        """
        if self.halted:
            return False, "Canary: System halted due to safety violations"
        
        # Check against forbidden patterns
        for pattern in self.forbidden_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                reason = f"Canary: Forbidden command pattern: {pattern}"
                self._log_violation('critical', f"Forbidden command blocked: {command}")
                return False, reason
        
        # Check rate limits
        if not self._check_rate_limit('command_executions'):
            reason = "Canary: Command execution rate limit exceeded"
            self._log_violation('high', f"Rate limit exceeded for command: {command}")
            return False, reason
        
        # Log safe command
        self._log_action('command', command, 'info')
        
        return True, None
    
    def check_pattern(self, text: str, context: str = 'general') -> List[Dict]:
        """
        Check text for forbidden patterns.
        
        Args:
            text: Text to check
            context: Context description
            
        Returns:
            List of violation dictionaries
        """
        violations = []
        
        for pattern in self.forbidden_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                violation = {
                    'pattern': pattern,
                    'match': match.group(),
                    'position': match.span(),
                    'context': context,
                    'severity': 'high',
                    'timestamp': datetime.now().isoformat(),
                }
                violations.append(violation)
                self._log_violation('high', f"Pattern match in {context}: {pattern}")
        
        return violations
    
    def _check_rate_limit(self, action_type: str) -> bool:
        """
        Check if action is within rate limits.
        
        Args:
            action_type: Type of action to check
            
        Returns:
            True if within limits, False otherwise
        """
        limits = self.config.get('rate_limits', {}).get(action_type)
        if not limits:
            return True  # No limit configured
        
        now = time.time()
        window = limits['window']
        limit = limits['limit']
        
        # Initialize tracking if needed
        if action_type not in self.rate_limits:
            self.rate_limits[action_type] = []
        
        # Remove old entries outside window
        self.rate_limits[action_type] = [
            t for t in self.rate_limits[action_type]
            if now - t < window
        ]
        
        # Check limit
        if len(self.rate_limits[action_type]) >= limit:
            return False
        
        # Record this action
        self.rate_limits[action_type].append(now)
        return True
    
    def _log_action(self, action_type: str, target: str, severity: str):
        """Log action to action log."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': action_type,
            'target': target,
            'severity': severity,
        }
        self.action_log.append(entry)
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def _log_violation(self, severity: str, message: str):
        """
        Log safety violation.
        
        Args:
            severity: Severity level (critical, high, medium, low, info)
            message: Violation message
        """
        self.violation_count += 1
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'message': message,
            'violation_number': self.violation_count,
        }
        
        self.alert_history.append(entry)
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(f"VIOLATION: {json.dumps(entry)}\n")
        
        # Check for auto-halt
        if severity in ['critical', 'high']:
            if self.violation_count >= self.halt_threshold:
                self._halt_system()
    
    def _halt_system(self):
        """Halt system due to excessive violations."""
        self.halted = True
        halt_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'SYSTEM_HALT',
            'reason': f'Violation threshold exceeded ({self.violation_count} violations)',
            'uptime_seconds': time.time() - self.start_time,
        }
        
        with open(self.log_file, 'a') as f:
            f.write(f"HALT: {json.dumps(halt_entry)}\n")
        
        print("\n" + "="*70)
        print("⚠️  CANARY SYSTEM HALT")
        print("="*70)
        print(f"Violation count: {self.violation_count}")
        print(f"Threshold: {self.halt_threshold}")
        print(f"Uptime: {halt_entry['uptime_seconds']:.2f}s")
        print("="*70)
        print("\nSystem halted. Manual review required.")
        print(f"See log: {self.log_file}")
        print()
    
    def get_status(self) -> Dict:
        """
        Get current monitoring status.
        
        Returns:
            Status dictionary
        """
        uptime = time.time() - self.start_time
        
        return {
            'halted': self.halted,
            'violation_count': self.violation_count,
            'halt_threshold': self.halt_threshold,
            'uptime_seconds': uptime,
            'total_actions': len(self.action_log),
            'total_violations': len(self.alert_history),
            'protected_paths_count': len(self.protected_paths),
            'forbidden_patterns_count': len(self.forbidden_patterns),
        }
    
    def reset(self, clear_logs: bool = False):
        """
        Reset monitoring state.
        
        Args:
            clear_logs: If True, clear action and violation logs
        """
        self.halted = False
        self.violation_count = 0
        self.start_time = time.time()
        self.rate_limits = {}
        
        if clear_logs:
            self.action_log = []
            self.alert_history = []
            
            # Clear log file
            with open(self.log_file, 'w') as f:
                f.write(f"# Canary log reset at {datetime.now().isoformat()}\n")


def main():
    """CLI for Canary monitoring."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Canary Agent Safety Monitor')
    parser.add_argument('action', choices=['status', 'check-path', 'check-command', 'reset'],
                       help='Action to perform')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--path', help='Path to check (for check-path)')
    parser.add_argument('--operation', default='access', help='Operation type')
    parser.add_argument('--command', help='Command to check (for check-command)')
    parser.add_argument('--clear-logs', action='store_true', help='Clear logs on reset')
    
    args = parser.parse_args()
    
    canary = CanaryMonitor(args.config)
    
    if args.action == 'status':
        status = canary.get_status()
        print("\nCanary Status:")
        print("-" * 50)
        for key, value in status.items():
            print(f"{key:30} {value}")
        print()
    
    elif args.action == 'check-path':
        if not args.path:
            print("Error: --path required")
            return
        
        is_safe, reason = canary.check_path(args.path, args.operation)
        if is_safe:
            print(f"✅ Path safe: {args.path}")
        else:
            print(f"❌ Path blocked: {reason}")
    
    elif args.action == 'check-command':
        if not args.command:
            print("Error: --command required")
            return
        
        is_safe, reason = canary.check_command(args.command)
        if is_safe:
            print(f"✅ Command safe: {args.command}")
        else:
            print(f"❌ Command blocked: {reason}")
    
    elif args.action == 'reset':
        canary.reset(clear_logs=args.clear_logs)
        print("✅ Canary reset complete")


if __name__ == '__main__':
    main()
