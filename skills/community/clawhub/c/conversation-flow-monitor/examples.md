# Conversation Flow Monitor - Usage Examples

This document provides practical examples of how to use the Conversation Flow Monitor skill to prevent stuck conversations and handle errors gracefully.

## Table of Contents
- [Basic Usage](#basic-usage)
- [Browser Operations](#browser-operations)
- [File Operations](#file-operations)
- [Shell Commands](#shell-commands)
- [Integration with Other Skills](#integration-with-other-skills)
- [Heartbeat Integration](#heartbeat-integration)
- [Custom Error Handling](#custom-error-handling)

---

## Basic Usage

The simplest way to use the conversation monitor is with the context manager:

```python
from conversation_monitor import ConversationMonitor

monitor = ConversationMonitor()

# Basic operation monitoring
with monitor.track_operation("data_processing", timeout=30):
    # Your operation here
    result = process_data()
```

### Health Checking
You can also check conversation health periodically:

```python
health = monitor.get_conversation_health()
if not health['is_healthy']:
    print("Conversation may be stuck - consider intervention")
```

---

## Browser Operations

Monitor browser operations that might hang due to slow page loads or network issues:

```python
from conversation_monitor import ConversationMonitor
from your_browser_module import browser_use

monitor = ConversationMonitor()

# Monitor browser navigation with extended timeout
with monitor.track_operation("browser_navigation", timeout=60):
    result = browser_use(action="open", url="https://example.com")
    browser_use(action="click", ref="submit_button")
```

**Common Scenarios:**
- Page loading timeouts
- Element not found errors  
- Network connectivity issues
- Slow JavaScript execution

---

## File Operations

Protect file operations that might hang due to large files or permission issues:

```python
from conversation_monitor import ConversationMonitor
import os

monitor = ConversationMonitor()

# Monitor file reading/writing
with monitor.track_operation("file_processing", timeout=20):
    with open("large_file.txt", "r") as f:
        content = f.read()
    
    with open("output.txt", "w") as f:
        f.write(processed_content)
```

**Common Scenarios:**
- Large file processing
- Network drive access delays
- Permission denied errors
- Disk space issues

---

## Shell Commands

Monitor external command execution that might hang or fail:

```python
from conversation_monitor import ConversationMonitor
import subprocess

monitor = ConversationMonitor()

# Monitor shell command execution
with monitor.track_operation("system_command", timeout=45):
    result = subprocess.run(
        ["git", "status"], 
        capture_output=True, 
        text=True, 
        timeout=30
    )
```

**Common Scenarios:**
- Long-running system commands
- Interactive prompts hanging
- Resource-intensive operations
- External tool failures

---

## Integration with Other Skills

### With Self-Improving Agent
Combine conversation monitoring with automatic learning:

```python
from conversation_monitor import ConversationMonitor
from self_improving_agent import log_learning

monitor = ConversationMonitor()

try:
    with monitor.track_operation("skill_execution", timeout=45):
        result = execute_complex_skill()
except Exception as e:
    # Log the error for self-improvement
    log_learning({
        'error': str(e),
        'context': 'skill_execution',
        'recovery_action': 'manual_intervention_required'
    })
    raise
```

### With Temporal Personality Evolution Tracker
Monitor personality tracking operations:

```python
from conversation_monitor import ConversationMonitor
from temporal_personality_evolution_tracker import update_traits

monitor = ConversationMonitor()

with monitor.track_operation("personality_update", timeout=15):
    traits = analyze_conversation_patterns()
    update_traits(user_id, traits)
```

---

## Heartbeat Integration

The skill includes built-in heartbeat support for periodic monitoring:

```python
# In your heartbeat configuration
{
    "hooks": {
        "conversation-flow-monitor": {
            "enabled": true,
            "frequency_minutes": 30
        }
    }
}
```

The heartbeat will automatically:
- Check for stuck conversations (older than 30 minutes)
- Clean up old log files (retention: 7 days)
- Validate skill file integrity
- Report health status

---

## Custom Error Handling

For advanced use cases, you can customize error handling behavior:

```python
from conversation_monitor import ConversationMonitor
from error_handler import ConversationErrorHandler

# Custom error handler with different retry strategy
custom_handler = ConversationErrorHandler(
    max_retries=5,  # Increase from default 3
    default_timeout=60  # Increase from default 30
)

# Use custom handler
try:
    with monitor.track_operation("critical_operation", timeout=120):
        result = perform_critical_task()
except Exception as e:
    error_info = custom_handler.handle_error(e, "critical_operation")
    
    if error_info['recovery_action'] == 'max_attempts_reached':
        # Escalate to user
        notify_user("Critical operation failed after all retries")
    else:
        # Continue with recovery
        continue_with_fallback()
```

---

## Configuration Options

The skill can be configured via `config.json`:

```json
{
  "timeout_threshold_seconds": 30,
  "max_recovery_attempts": 3,
  "stuck_conversation_threshold_minutes": 30,
  "log_retention_days": 7,
  "enable_heartbeat_monitoring": true,
  "monitoring_enabled": true,
  "default_tool_timeout": 45,
  "browser_operation_timeout": 60,
  "file_operation_timeout": 20,
  "network_operation_timeout": 45
}
```

---

## Best Practices

### 1. Choose Appropriate Timeouts
- **Browser operations**: 45-60 seconds
- **File operations**: 15-30 seconds  
- **Simple computations**: 10-20 seconds
- **Network requests**: 30-45 seconds

### 2. Use Descriptive Operation Names
```python
# Good
with monitor.track_operation("fetch_user_profile_data", timeout=30):

# Avoid
with monitor.track_operation("operation1", timeout=30):
```

### 3. Handle Errors Gracefully
Always wrap monitored operations in try-catch blocks when you need custom error handling:

```python
try:
    with monitor.track_operation("important_task", timeout=60):
        result = do_important_work()
except TimeoutError:
    # Handle timeout specifically
    result = use_cached_data()
except Exception as e:
    # Handle other errors
    log_error_and_notify(e)
```

### 4. Monitor Critical Paths Only
Don't over-monitor simple operations. Focus on:
- External API calls
- File I/O operations  
- Browser interactions
- Complex computations
- Any operation that has previously caused hangs

---

## Troubleshooting

### Common Issues and Solutions

**Issue**: Monitor doesn't detect timeouts
- **Solution**: Ensure your code actually waits long enough or use asyncio.wait_for() for actual timeout enforcement

**Issue**: Too many recovery attempts
- **Solution**: Adjust `max_recovery_attempts` in config.json or implement custom logic

**Issue**: Log files growing too large
- **Solution**: Adjust `log_retention_days` in config.json or manually clean logs

**Issue**: False positives on healthy operations  
- **Solution**: Increase timeout values for specific operation types in config.json

### Log Analysis

Check the conversation monitor logs at:
```
~/.copaw/.logs/conversation_monitor.log
```

Look for patterns like:
- Repeated timeouts on the same operation type
- Recovery attempts reaching maximum limits
- Operations consistently taking longer than expected

---

## Real-World Example: YAML Front Matter Protection

This is the primary use case the skill was designed for:

```python
from conversation_monitor import ConversationMonitor

def load_skill_with_protection(skill_name):
    """Load a skill with conversation flow protection"""
    monitor = ConversationMonitor()
    
    try:
        with monitor.track_operation(f"load_skill_{skill_name}", timeout=10):
            # This might fail if YAML front matter is missing
            skill = load_skill_from_directory(skill_name)
            return skill
    except ValueError as e:
        if "YAML front matter" in str(e):
            # Handle the specific YAML issue
            log_yalm_error(skill_name)
            return create_safe_fallback_skill()
        else:
            # Re-raise other errors
            raise
```

This pattern prevents the conversation from hanging when skills have missing YAML front matter, which was causing empty tool names and conversation freezes.

---

> **Note**: These examples are for educational purposes only. Adapt them to your specific use cases and requirements. The conversation-flow-monitor skill itself contains no executable example code - only the core monitoring functionality.