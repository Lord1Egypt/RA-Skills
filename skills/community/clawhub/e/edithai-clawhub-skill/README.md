# EdithAI ClawHub Skill

This skill packages EdithAI, an intelligent log analysis CLI tool, for use with ClawHub.

## What is EdithAI?

EdithAI is a powerful CLI tool that combines natural language processing with 30+ built-in tools for comprehensive log analysis. It uses the DeepSeek API to transform complex log data into actionable insights through simple, conversational commands.

## Quick Start

1. **Install the Skill**: Add this skill to your ClawHub workspace
2. **Set Environment Variable**: Configure your `DEEPSEEK_API_KEY`
3. **Install EdithAI CLI**:
   ```bash
   npm install -g @xin9min9/edithai-cli
   ```
4. **Start Analyzing**: Use natural language to analyze your logs

## Usage Examples

```bash
# Basic log analysis
edithai -query "analyze error logs in current directory"

# Interactive mode
edithai -i

# Specific pattern detection
edithai -query "find all database connection failures in the last hour"
```

## Key Features

- 🔍 **Intelligent Analysis**: Understand complex log patterns through AI
- 🛠️ **30+ Built-in Tools**: File operations, system diagnostics, data processing
- 🎯 **Targeted Queries**: Natural language log analysis
- 💰 **Cost Tracking**: Monitor API usage with DeepSeek pricing
- 🔒 **Security First**: Command whitelisting and input validation
- 📊 **Multi-format Support**: Handle various log formats and timestamps

## Requirements

- DeepSeek API key
- Go 1.24+ runtime
- Text-based log files (JSON, CSV, plain text)

## Security Note

EdithAI includes robust security features:
- Command whitelisting/blacklisting for terminal operations
- File extension restrictions
- Path traversal protection
- Command injection detection

## Documentation

For detailed documentation, see [SKILL.md](SKILL.md).

## Support

For issues and questions, please refer to the main EdithAI repository.