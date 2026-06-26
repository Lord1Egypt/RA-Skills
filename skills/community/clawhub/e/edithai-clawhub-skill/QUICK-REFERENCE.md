# EdithAI Quick Reference

## Basic Commands

| Command | Description |
|---------|-------------|
| `edithai -query "analysis request"` | Analyze logs using natural language |
| `edithai -i` | Start interactive mode |
| `edithai --version` | Show version information |
| `edithai --help` | Show help message |

## Common Queries

### Log Analysis
```
"analyze error logs in current directory"
"find all database connection failures"
"show memory usage trends"
"identify performance bottlenecks"
"detect unusual activities"
```

### File Operations
```
"read /var/log/application.log"
"search for 'ERROR' in all .log files"
"analyze log file size patterns"
"find largest log files"
```

### System Analysis
```
"show running processes"
"check network connections"
"analyze disk space usage"
"find high CPU usage processes"
```

## Interactive Mode Commands

| Command | Action |
|---------|--------|
| `exit` or `quit` | Exit interactive mode |
| `help` | Show available commands |
| `clear` | Clear screen |
| `history` | Show conversation history |

## Configuration

### Environment Variables
```bash
DEEPSEEK_API_KEY=your-api-key-here
```

### Config File: `~/.edithai/config.json`
```json
{
  "api": {
    "timeout": 30,
    "max_tokens": 4000
  },
  "security": {
    "whitelist_commands": ["ls", "cat", "grep"],
    "blacklist_commands": ["rm", "dd"],
    "tool_payload_max_chars": 2000
  }
}
```

## Security Features

### Safe Commands (Default Allowed)
- `ls`, `cat`, `grep`, `tail`, `head`
- `find`, `wc`, `sort`, `uniq`
- File viewing and searching tools

### Dangerous Commands (Default Blocked)
- `rm`, `dd`, `mkfs`
- Shell operators: `&&`, `||`, `;`, `|`, `>`
- Command substitution: `$(...)`, ``` ` ``

## Tips

1. **Be Specific**: Use detailed descriptions for better results
2. **Iterate**: Ask follow-up questions for deeper analysis
3. **Context**: Include file paths and time ranges when relevant
4. **Security**: Customize command lists for your environment
5. **Cost**: Monitor API usage with DeepSeek tracking

## File Locations

| Location | Purpose |
|----------|---------|
| `~/.edithai/config.json` | User configuration |
| `~/.edithai/history.json` | Conversation history |
| Current directory | Default log analysis location |