#!/usr/bin/env python3
"""
Canary — Configuration Example
Copy to config.py and customize for your agent.

Author: Shadow Rose
License: MIT
"""

# ==============================================================================
# LOGGING
# ==============================================================================

# Main log file for all Canary events
log_file = 'canary.log'

# Log file rotation (future enhancement)
# log_rotation_mb = 10
# log_retention_days = 30

# ==============================================================================
# PROTECTED PATHS
# ==============================================================================

# Paths that should never be modified or deleted
# Agent access to these paths will be blocked
protected_paths = [
    # System directories
    '/etc/',
    '/sys/',
    '/proc/',
    '/boot/',
    '/dev/',
    
    # User sensitive directories
    '~/.ssh/',
    '~/.aws/',
    '~/.gnupg/',
    '~/.config/',
    
    # Add your own protected paths
    # '~/important-data/',
    # '/mnt/backup/',
]

# ==============================================================================
# FORBIDDEN PATTERNS
# ==============================================================================

# Regular expressions for dangerous commands/patterns
# If matched, the action is blocked
forbidden_patterns = [
    # Destructive file operations
    r'rm\s+-rf\s+/',            # Recursive force delete from root
    r'rm\s+-rf\s+\*',           # Recursive force delete all
    r'rm\s+-rf\s+~',            # Delete home directory
    
    # Dangerous permissions
    r'chmod\s+777',             # World-writable permissions
    r'chmod\s+-R\s+777',        # Recursive world-writable
    
    # Suspicious downloads
    r'curl.*\|\s*sh',           # Curl piped to shell
    r'wget.*\|\s*sh',           # Wget piped to shell
    r'curl.*\|\s*bash',         # Curl piped to bash
    
    # Code execution risks
    r'eval\s*\(',               # Python eval
    r'exec\s*\(',               # Python exec
    
    # Network exfiltration patterns
    r'nc\s+.*-e',               # Netcat with execute
    r'bash\s+-i\s+>&',          # Reverse shell pattern
    
    # Add your own forbidden patterns
    # r'your-pattern-here',
]

# ==============================================================================
# SEVERITY LEVELS
# ==============================================================================

# Severity level scoring (higher = more critical)
severity_levels = {
    'critical': 100,    # Immediate threat, triggers auto-halt
    'high': 75,         # Serious violation, triggers auto-halt
    'medium': 50,       # Suspicious but not immediately dangerous
    'low': 25,          # Minor concern
    'info': 10,         # Informational only
}

# ==============================================================================
# AUTO-HALT CONFIGURATION
# ==============================================================================

# Number of critical/high severity violations before auto-halt
halt_threshold = 5

# Auto-restart allowed after halt (require manual intervention)
allow_auto_restart = False

# ==============================================================================
# RATE LIMITING
# ==============================================================================

# Rate limits for different action types
# Format: {'limit': max_count, 'window': seconds}
rate_limits = {
    'file_operations': {
        'limit': 100,       # Max 100 file operations
        'window': 60,       # Per 60 seconds
    },
    'network_requests': {
        'limit': 50,        # Max 50 network requests
        'window': 60,       # Per 60 seconds
    },
    'command_executions': {
        'limit': 20,        # Max 20 command executions
        'window': 60,       # Per 60 seconds
    },
}

# ==============================================================================
# TRIPWIRE CONFIGURATION
# ==============================================================================

# Directory to store tripwire files and registry
tripwire_dir = '.canary_tripwires'

# Check tripwire files this often (seconds)
tripwire_check_interval = 60

# ==============================================================================
# ALERTING
# ==============================================================================

# Alert destinations (future enhancement)
# alert_email = 'you@example.com'
# alert_webhook = 'https://hooks.slack.com/...'

# Minimum severity to trigger alert
alert_min_severity = 'high'

# ==============================================================================
# EXAMPLE CUSTOM CONFIGURATION
# ==============================================================================

# Example: Protect specific project directories
# protected_paths.extend([
#     '~/projects/production/',
#     '~/important-data/',
#     '/var/backups/',
# ])

# Example: Add domain-specific forbidden patterns
# forbidden_patterns.extend([
#     r'DROP\s+TABLE',              # SQL injection pattern
#     r'DELETE\s+FROM.*WHERE',      # Dangerous SQL
#     r'<script>',                  # XSS pattern
# ])

# Example: Custom rate limits for specific use case
# rate_limits['api_calls'] = {
#     'limit': 1000,
#     'window': 3600,  # 1000 API calls per hour
# }

# ==============================================================================
# USAGE
# ==============================================================================

# To use this config:
# 1. Copy to config.py: cp config_example.py config.py
# 2. Edit config.py with your settings
# 3. Pass to Canary:
#
#    from canary import CanaryMonitor
#    canary = CanaryMonitor('config.py')
#
# Or via CLI:
#    python3 canary.py --config config.py status
