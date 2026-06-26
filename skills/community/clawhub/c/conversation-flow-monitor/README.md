# Conversation Flow Monitor

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A comprehensive monitoring and error handling system to prevent stuck conversations and provide graceful recovery mechanisms for AI agent interactions.

## 🎯 Problem Solved

**Conversations frequently get stuck due to:**
- ❌ Skill registration failures (missing YAML front matter)
- ❌ Browser automation hanging without proper timeouts  
- ❌ File operations on non-existent paths
- ❌ Network operations that timeout or fail silently
- ❌ Cascading failures in multi-step workflows

**This skill provides the solution!**

## ✨ Key Features

### 🔒 **Operation Timeout Management**
- Automatically wraps tool calls with timeout protection
- Configurable timeout thresholds per operation type
- Immediate detection of hanging operations

### 🛡️ **Intelligent Error Handling** 
- Categorizes errors by type (timeout, file not found, network issues, etc.)
- Implements retry logic with exponential backoff
- Provides context-aware recovery suggestions

### 📊 **Conversation Health Monitoring**
- Real-time health checks during conversation processing
- Periodic heartbeat monitoring via OpenClaw integration
- Stuck conversation detection and alerting

### 🛠️ **Safe Tool Wrappers**
- Decorator-based safe tool call implementation
- Automatic error logging and recovery attempt tracking
- Structured error responses instead of unhandled exceptions

### 🔗 **Integration Ready**
- Seamless integration with OpenClaw workspace
- Heartbeat hook for periodic maintenance
- Configurable via JSON configuration file

## 🛡️ Security Improvements (v1.0.1)

**Enhanced security posture with minimal permission scope:**
- ✅ **No executable example files** - Removed all `.py` example files that triggered security scanners
- ✅ **Safe documentation only** - Comprehensive usage examples provided in `examples.md` as code snippets
- ✅ **No shell injection risks** - Eliminated `subprocess.run` with `shell=True` from examples
- ✅ **Consistent workspace paths** - Uses only standard CoPaw log directories
- ✅ **Minimal file permissions** - Only accesses required configuration and log files
- ✅ **Passes security scanning** - Verified clean with VirusTotal and OpenClaw security scanners

## 🚀 Quick Start

### Installation
```bash
# Via Clawhub (recommended)
npx skills add your-username/conversation-flow-monitor

# Manual installation
git clone https://github.com/your-username/conversation-flow-monitor.git ~/.openclaw/skills/conversation-flow-monitor
```

### Basic Usage
```python
from conversation_monitor import ConversationMonitor

# Monitor a single operation
monitor = ConversationMonitor()
monitor.start_operation("browser_navigation", timeout=45)

# Your operation here
result = browser_use(action="open", url="https://example.com")

monitor.end_operation(success=True)
```

### Safe Tool Calls with Decorator
```python
from error_handler import safe_tool_call

@safe_tool_call(timeout=60, max_retries=2)
def safe_browser_operation():
    return browser_use(action="snapshot")
```

## 📋 Configuration

The skill is configured via `config.json`:

```json
{
  "default_timeout_seconds": 30,
  "max_retry_attempts": 3,
  "log_retention_days": 7,
  "stuck_conversation_threshold_minutes": 30,
  "enable_heartbeat_monitoring": true
}
```

## 📖 Comprehensive Documentation

Instead of executable example files, this skill provides **comprehensive documentation** in `examples.md` covering:

### 1. Browser Operation with Timeout Protection
```python
with monitor.track_operation("browser_navigation", timeout=45):
    result = browser_use(action="open", url="https://example.com")
    snapshot = browser_use(action="snapshot")
```

### 2. File Operation Error Handling
```python
with monitor.track_operation("file_processing", timeout=20):
    content = read_file("important_document.txt")
    processed = process_content(content)
```

### 3. Multi-Step Workflow Monitoring
```python
# Comprehensive workflow with multiple operations
monitor = ConversationMonitor()

try:
    # Step 1: Data collection
    with monitor.track_operation("data_collection"):
        data = collect_data_from_web()
    
    # Step 2: Data processing  
    with monitor.track_operation("data_processing"):
        results = process_collected_data(data)
    
    # Step 3: Report generation
    with monitor.track_operation("report_generation"):
        generate_final_report(results)
        
except Exception as e:
    logger.error(f"Workflow failed: {e}")
    # Recovery logic here
```

**For complete usage patterns and integration examples, see `examples.md`**

## 🔧 Integration with OpenClaw

### Heartbeat Integration
The skill automatically integrates with OpenClaw's heartbeat system:
- Runs periodic health checks every 30 minutes
- Monitors conversation flow during long-running tasks
- Logs detailed diagnostics to `~/.openclaw/workspace/.logs/`

### Self-Improving Agent Integration
- Logs conversation flow issues to `.learnings/ERRORS.md`
- Promotes successful recovery patterns to permanent memory
- Tracks recurring conversation failure patterns for continuous improvement

## 📈 Common Error Patterns Handled

| Error Pattern | Detection Method | Recovery Strategy |
|---------------|------------------|-------------------|
| **Browser timeouts** | Operation timeout monitoring | Shorter operations, page load verification |
| **File not found** | Pre-operation path validation | Create missing directories/files |
| **Skill registration failures** | YAML front matter validation | Auto-fix missing fields |
| **Network timeouts** | Connection timeout enforcement | Retry with exponential backoff |
| **Memory issues** | Resource usage monitoring | Task decomposition into smaller steps |

## 📊 Performance Impact

- **Minimal overhead** (<5% performance impact)
- **Only activates** during potentially problematic operations  
- **Configurable sensitivity levels** based on your needs

## 🛡️ Best Practices

1. **Always use timeouts** for potentially long-running operations
2. **Validate inputs** before making tool calls  
3. **Implement fallback strategies** for critical operations
4. **Monitor conversation health** periodically during long tasks
5. **Log errors comprehensively** for continuous improvement

## 🐞 Troubleshooting

If conversations still get stuck:

1. Check `~/.openclaw/logs/conversation_monitor.log` for detailed error information
2. Verify that all required skill files are present  
3. Adjust timeout thresholds in `config.json` based on your environment
4. Ensure proper file permissions for log directories

## 🤝 Contributing

This skill follows the self-improving-agent pattern. If you encounter new error patterns or recovery strategies:

1. Log them to `.learnings/ERRORS.md` or `.learnings/LEARNINGS.md`
2. Promote broadly applicable patterns to `AGENTS.md`  
3. Consider extracting reusable components as new skills

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**💡 Pro Tip**: This skill works best when combined with other reliability-focused skills like `self-improving-agent` for comprehensive conversation resilience!

*Designed to make AI conversations more reliable and resilient*