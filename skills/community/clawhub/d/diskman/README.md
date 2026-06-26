# Diskman

<p align="center">
  <img src="Diskman.png" alt="Diskman Logo" width="200">
</p>

<p align="center">
  <strong>AI-ready disk space analysis and management</strong>
</p>

## Features

- 🔍 **Smart Scan** - Analyze directory sizes with link type detection
- 🧠 **Intelligent Analysis** - Rule-based + AI-powered recommendations
- 🔄 **Safe Migration** - Move directories using symbolic links
- 🧹 **Smart Clean** - Safe cleanup with risk evaluation
- 🤖 **AI-Ready** - Built-in AI analysis (OpenAI/DeepSeek/Qwen compatible)
- 🔌 **MCP Integration** - AI agent automation via MCP protocol
- 🔒 **Accurate Statistics** - Correctly handles symlinks/junctions to avoid double-counting

<p align="center">
  <img src="Diskman%20detail.png" alt="Diskman Features" width="600">
</p>

## Install

```bash
# Core functionality
pip install diskman

# With MCP support (for AI agents)
pip install "diskman[mcp]"

# With AI support (for AI-powered analysis)
pip install "diskman[ai]"

# With everything
pip install "diskman[all]"
```

## Quick Start

### CLI Usage

```bash
# Scan directory
diskman scan ~/project

# Scan user profile for large directories
diskman profile

# Analyze a directory (get recommendations)
diskman analyze ~/.cache

# Migrate directory with symbolic link
diskman migrate ~/.conda /data/.conda

# Clean directory (dry run by default)
diskman clean ~/temp

# Check link status
diskman link ~/.cache
```

### Python API

```python
from diskman import DirectoryScanner, DirectoryAnalyzer, DirectoryMigrator

# Scan
scanner = DirectoryScanner()
result = scanner.scan_user_profile()

for info in result.directories[:10]:
    print(f"{info.size_mb:.0f} MB - {info.path}")

# Analyze
analyzer = DirectoryAnalyzer()
analysis = analyzer.analyze(result.directories[0])

print(f"Action: {analysis.recommended_action.value}")
print(f"Risk: {analysis.risk_level.value}")
print(f"Reason: {analysis.reason}")

# Migrate
migrator = DirectoryMigrator()
result = migrator.migrate("~/.conda", "/data/.conda")
```

### AI-Powered Analysis

```python
import asyncio
from diskman import DirectoryScanner, AIService, AIConfig

async def analyze_with_ai():
    # Configure AI (supports OpenAI-compatible APIs)
    ai = AIService(AIConfig(
        api_key="your-api-key",
        base_url="https://api.deepseek.com",  # or OpenAI, Qwen, etc.
        model="deepseek-chat",
    ))
    
    # Scan
    scanner = DirectoryScanner()
    result = scanner.scan_user_profile()
    
    # AI Analysis
    ai_result = await ai.analyze(
        directories=result.directories[:30],
        user_context="I'm a Python developer",
        target_drive="D:\\",
    )
    
    print(ai_result["summary"])
    for rec in ai_result["recommendations"]:
        print(f"{rec['path']}: {rec['action']} - {rec['reason']}")

asyncio.run(analyze_with_ai())
```

### MCP Integration (for AI Agents)

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "diskman": {
      "command": "diskman-mcp",
      "env": {
        "AI_API_KEY": "your-api-key",
        "AI_BASE_URL": "https://api.deepseek.com",
        "AI_MODEL": "deepseek-chat"
      }
    }
  }
}
```

**Available MCP Tools:**

| Tool | Description |
|------|-------------|
| `scan_directory` | Scan a single directory |
| `scan_user_profile` | Scan user profile for large directories |
| `check_link_status` | Check if path is symlink/junction/normal |
| `analyze_directory` | Analyze with rule-based recommendations |
| `analyze_directories` | Batch analysis with smart mode switching (AI ↔ Rules) |
| `migrate_directory` | Migrate directory with symbolic link |
| `clean_directory` | Clean directory contents |
| `get_ai_provider_info` | Check AI provider status |

## Architecture

```
diskman/
├── operations/       # File system operations
│   ├── scanner.py   # Directory scanning with link detection
│   ├── migrator.py  # Migration with symbolic links
│   └── cleaner.py   # Safe cleanup
│
├── analysis/         # Directory analysis
│   ├── analyzer.py  # Rule-based recommendations
│   └── rules/       # Built-in analysis rules
│
├── ai/              # AI-powered analysis
│   ├── service.py   # AI service wrapper
│   └── providers/   # OpenAI-compatible providers
│
├── mcp/             # MCP server for AI agents
└── cli.py           # Command-line interface
```

## Smart Analysis Mode

`analyze_directories` automatically chooses the best analysis method:

| Condition | Analysis Mode |
|-----------|---------------|
| AI configured + available | AI-powered analysis |
| No AI config / AI unavailable | Rule-based analysis |
| AI analysis fails | Falls back to rules |

This ensures the tool always works, with or without AI configuration.

## Two Analysis Modes

### Rule-Based Analysis (Default)

- 40+ built-in rules for common directories
- Pattern-based heuristics for unknown directories
- Risk assessment: safe/low/medium/high/critical
- Action recommendations: can_delete, can_move, keep, review

### AI-Powered Analysis

- Context-aware recommendations
- Natural language explanations
- Supports any OpenAI-compatible API:
  - OpenAI (gpt-4o-mini, gpt-4o)
  - DeepSeek (deepseek-chat)
  - Qwen (qwen-turbo, qwen-plus)
  - Local models (Ollama, vLLM)

## Configuration

### Parameter Passing (Recommended)

```python
from diskman import AIService, AIConfig
from diskman.mcp import create_mcp_server

# Python API
ai = AIService(AIConfig(
    api_key="your-api-key",
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
))

# MCP Server
mcp = create_mcp_server(AIConfig(
    api_key="your-api-key",
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
))
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `AI_API_KEY` or `OPENAI_API_KEY` | AI provider API key |
| `AI_BASE_URL` or `OPENAI_BASE_URL` | API base URL |
| `AI_MODEL` or `OPENAI_MODEL` | Model name (default: gpt-4o-mini) |

## Examples

### Find large directories

```python
from diskman import DirectoryScanner

scanner = DirectoryScanner()
result = scanner.scan_user_profile()

print(f"Total: {result.total_size_gb:.1f} GB")
for info in result.directories[:20]:
    print(f"{info.size_mb:>8.0f} MB  {info.path}")
```

### Get cleanup recommendations

```python
from diskman import DirectoryScanner, DirectoryAnalyzer

scanner = DirectoryScanner()
analyzer = DirectoryAnalyzer()

result = scanner.scan_user_profile()

for info in result.directories[:10]:
    analysis = analyzer.analyze(info)
    if analysis.recommended_action.value == "can_delete":
        print(f"✓ {info.path}")
        print(f"  {info.size_mb:.0f} MB - {analysis.reason}")
```

### Migrate a directory

```python
from diskman import DirectoryMigrator

migrator = DirectoryMigrator()

# Move conda environment to D drive
result = migrator.migrate(
    source=r"C:\Users\you\.conda",
    target=r"D:\migrated\.conda"
)

if result.success:
    print(f"Done! Created {result.link_type}")
```

## Accurate Space Statistics

Diskman correctly handles symbolic links and junctions:

- **Symlinks/Junctions**: Report 0 size by default (data is on target drive)
- **Normal directories**: Report actual size
- **`count_link_target=True`**: Include symlink target size if needed

```python
# Default: symlinks show 0 size (accurate C: drive usage)
info = scanner.scan_directory("C:\\Users\\you\\LinkedFolder")

# Include target size for total data analysis
info = scanner.scan_directory("C:\\Users\\you\\LinkedFolder", count_link_target=True)
```

## License

MIT
