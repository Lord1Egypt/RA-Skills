# Quick Start Guide

## 🚀 Installation

### Method 1: Install from ClawHub (Recommended)
```bash
clawhub install max-gaan/error-log-analyzer
```

### Method 2: Install from Source
```bash
git clone https://github.com/maxgaan/error-log-analyzer.git
cd error-log-analyzer
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Set API Key
```bash
# For Claude (recommended)
export ANTHROPIC_API_KEY="your-key-here"

# Or for OpenAI
export OPENAI_API_KEY="your-key-here"
```

### 2. (Optional) Create Config File
Create `.error-analyzer.yml` in your project root:
```yaml
analysis:
  enableAI: true
  cacheResults: true

filtering:
  ignorePatterns:
    - "GET /health"
    - "favicon.ico"
```

## 📖 Usage

### Command Line
```bash
# Analyze a log file
python -m src analyze /var/log/myapp/error.log

# Analyze from stdin
cat error.log | python -m src analyze -

# Output as JSON
python -m src analyze error.log --format json

# Save to file
python -m src analyze error.log --output report.html --format markdown
```

### Python API
```python
from src import LogAnalyzer

analyzer = LogAnalyzer()
results = analyzer.analyze_file("/var/log/myapp/error.log")

print(results['summary'])
for error in results['analyses']:
    print(f"{error['severity']}: {error['error_type']}")
```

### Web Interface
```bash
# Start web server
cd web
python app.py

# Open http://localhost:5000 in browser
```

### OpenClaw Integration
```
# In OpenClaw chat
Analyze these error logs:
[2026-03-06 10:23:45] ERROR: Connection refused
```

## 🎯 Examples

### Example 1: Analyze Node.js Logs
```bash
python -m src analyze /var/log/nodejs/app.log
```

### Example 2: Analyze Python Logs
```bash
python -m src analyze /var/log/django/error.log
```

### Example 3: Real-time Monitoring
```python
from src import LogAnalyzer

analyzer = LogAnalyzer()

# Watch log file for changes
import time
while True:
    results = analyzer.analyze_file("/var/log/myapp/error.log")
    if results['trends']['spike_detected']:
        send_alert(results['summary'])
    time.sleep(60)  # Check every minute
```

## 🔧 Troubleshooting

### "No module named 'src'"
Make sure you're in the project root directory or install the package:
```bash
pip install -e .
```

### "API key not found"
Set your API key as environment variable:
```bash
export ANTHROPIC_API_KEY="your-key"
```

### "Levenshtein not found"
Install the package:
```bash
pip install python-Levenshtein
```

## 📚 Next Steps

- Read the [full documentation](docs/)
- Check out [examples](examples/)
- Join [OpenClaw Discord](https://discord.gg/clawd)
- Star us on [GitHub](https://github.com/maxgaan/error-log-analyzer)

## 💬 Need Help?

- 💬 Discord: [OpenClaw Community](https://discord.gg/clawd)
- 🐛 Issues: [GitHub Issues](https://github.com/maxgaan/error-log-analyzer/issues)
- 📧 Email: support@maxgaan.com
