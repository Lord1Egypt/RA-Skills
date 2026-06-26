---
name: edithai
description: Intelligent log analysis CLI tool powered by DeepSeek API with 30+ built-in tools for file operations, system diagnostics, and log pattern recognition.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DEEPSEEK_API_KEY
      bin:
        - node
    primaryEnv: DEEPSEEK_API_KEY
---

# EdithAI - Intelligent Log Analysis CLI

EdithAI is a Go-based CLI tool that combines natural language processing with powerful built-in tools for comprehensive log analysis. It leverages the DeepSeek API to provide intelligent insights into log data, making complex log analysis accessible through simple commands.

## Features

### Core Capabilities
- **Intelligent Log Analysis**: Use natural language queries to analyze logs
- **30+ Built-in Tools**: File operations, system diagnostics, data processing, and pattern recognition
- **Multi-format Support**: Handles various log formats and timestamps
- **Real-time Processing**: Streamlined analysis with efficient token usage
- **Cost Estimation**: Track API costs with DeepSeek pricing integration

### Key Tools
- **File Operations**: Read, write, and search files
- **Terminal Commands**: Safe execution of diagnostic commands
- **Log Analysis**: Pattern detection, timeline analysis, and error tracking
- **Data Processing**: CSV, JSON, and text manipulation
- **System Diagnostics**: Network, process, and performance monitoring

## Usage Examples

### Basic Log Analysis
```bash
# Analyze error logs in current directory
edithai -query "analyze error logs in current directory"

# Search for specific patterns
edithai -query "find all database connection errors"

# Generate performance report
edithai -query "create performance summary from application logs"
```

### Interactive Mode
```bash
# Start interactive session
edithai -i

# Multi-turn conversation about logs
> show me memory usage trends
> find memory leaks in the last 24 hours
> export analysis to report.html
```

## Installation Requirements

### Install EdithAI CLI
First, install the EdithAI CLI tool:
```bash
npm install -g @xin9min9/edithai-cli
```

### Environment Variables
- `DEEPSEEK_API_KEY`: Your DeepSeek API key for AI-powered analysis

### System Requirements
- Node.js >= 14.0.0 (required for npm)
- Minimum 512MB RAM
- Network connectivity to DeepSeek API

## Configuration

### Default Settings
- Tool output truncation: 2000 characters
- API timeout: 30 seconds
- History file: `~/.edithai/history.json`
- Log directory: Current working directory

### Advanced Configuration
Create a configuration file at `~/.edithai/config.json`:
```json
{
  "api": {
    "timeout": 30,
    "max_tokens": 4000
  },
  "security": {
    "whitelist_commands": ["ls", "cat", "grep"],
    "blacklist_commands": ["rm", "dd", "mkfs"],
    "tool_payload_max_chars": 2000
  }
}
```

## Security Features

- **Command Whitelisting/Blacklisting**: Restrict terminal command execution
- **File Extension Protection**: Prevent execution of dangerous file types
- **Path Traversal Protection**: Safeguard against directory traversal attacks
- **Command Injection Detection**: Block shell operators and dangerous patterns

## File Structure

```
~/.edithai/
├── config.json       # User configuration
└── history.json      # Conversation history
```

## Supported Log Formats

- Plain text logs
- JSON logs
- CSV data files
- Log files with timestamps
- Application logs (web servers, databases, etc.)
- System logs (Linux/Windows)

## Tips for Best Results

1. **Be Specific**: Use clear, detailed queries for better analysis
2. **Context Matters**: Include relevant time ranges and log locations
3. **Iterative Analysis**: Use interactive mode for multi-step analysis
4. **Cost Awareness**: Monitor token usage and costs in DeepSeek provider

## License

MIT-0 License - See LICENSE file for details.

## Support

For issues and feature requests, visit the [EdithAI GitHub Repository](https://github.com/your-org/edithai-clawhub-skill).