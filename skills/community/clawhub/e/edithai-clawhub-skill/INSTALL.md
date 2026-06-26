# Installation Guide for EdithAI ClawHub Skill

This guide explains how to install and configure the EdithAI skill for ClawHub.

## Prerequisites

### System Requirements
- Node.js >= 14.0.0 (required for npm)
- DeepSeek API key
- Command line interface

### Environment Setup
1. Ensure Node.js is installed and npm is available in your PATH
2. Obtain your DeepSeek API key from the DeepSeek platform
3. Install EdithAI CLI: `npm install -g @xin9min9/edithai-cli`

## Installation Steps

### 1. Install from ClawHub
Add the EdithAI skill to your ClawHub workspace through the ClawHub interface.

### 2. Configure Environment Variable
Set your DeepSeek API key as an environment variable:

**Linux/macOS:**
```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

**Windows:**
```cmd
set DEEPSEEK_API_KEY="your-api-key-here"
```

**Windows PowerShell:**
```powershell
$env:DEEPSEEK_API_KEY="your-api-key-here"
```

### 3. Verify Installation
Check if the skill is properly installed:
```bash
edithai --version
```

## Configuration

### Optional Configuration File
Create a configuration file at `~/.edithai/config.json` for custom settings:

```json
{
  "api": {
    "timeout": 30,
    "max_tokens": 4000
  },
  "security": {
    "whitelist_commands": ["ls", "cat", "grep", "tail"],
    "blacklist_commands": ["rm", "dd", "mkfs"],
    "tool_payload_max_chars": 2000
  }
}
```

### Security Configuration
Configure allowed/disallowed commands for terminal operations:
- `whitelist_commands`: List of commands that can be executed
- `blacklist_commands`: List of commands that are blocked

## Usage Examples

### Basic Log Analysis
```bash
# Analyze error logs in current directory
edithai -query "analyze error logs in current directory"

# Search for specific patterns
edithai -query "find all database connection errors"
```

### Interactive Mode
```bash
# Start interactive session
edithai -i

# Multi-turn conversation about logs
> show me memory usage trends
> find memory leaks in the last 24 hours
```

### File Analysis
```bash
# Analyze specific log file
edithai -query "analyze /var/log/application.log for performance issues"

# Process multiple files
edithai -query "summarize all .log files in the current directory"
```

## Troubleshooting

### Common Issues

1. **"command not found: edithai"**
   - Ensure Node.js and npm are installed
   - Run: `npm install -g @xin9min9/edithai-cli`
   - Verify the skill is properly installed in ClawHub

2. **"API key not found"**
   - Verify DEEPSEEK_API_KEY environment variable is set
   - Check that the key is valid and has sufficient quota

3. **"Permission denied"**
   - Check file permissions on log files
   - Verify command whitelist/blacklist configuration

4. **"Timeout error"**
   - Increase timeout in configuration file
   - Check network connectivity
   - Reduce query complexity

### Getting Help

For additional support:
1. Check the main EdithAI documentation
2. Review the CAPABILITIES.md file for detailed features
3. Try the interactive mode for guided assistance

## Next Steps

Once installed, you can:
1. Explore the built-in tools with `edithai -help`
2. Try the interactive mode with `edithai -i`
3. Review configuration options in SKILL.md
4. Explore advanced features in CAPABILITIES.md