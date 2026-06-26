# Installation Guide

## Boris Workflow for OpenClaw

This guide covers installation and setup of the Boris Workflow skill.

## Prerequisites

Before installing, ensure you have:

- **OpenClaw** installed and configured
- **Python** 3.9 or higher
- **pip** package manager
- **bash** shell (or compatible)
- **Git** (for cloning)

## Installation Steps

### 1. Clone the Repository

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/mukston/boris-workflow.git
cd boris-workflow
```

Or download and extract the skill archive to `~/.openclaw/workspace/skills/boris-workflow/`

### 2. Install Python Dependencies

```bash
# Install required dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### 3. Verify Installation

```bash
# Test the CLI
./bin/boris-run --version

# Expected output:
# boris-run 1.0.0

# Run a test with mock mode
./bin/boris-run --tasks "test1|test2|test3" --mock --dry-run
```

### 4. (Optional) Install Web UI Dependencies

If you want to use the web interface:

```bash
cd webui
pip install -r requirements.txt
```

## Configuration

### Quick Configuration

Create a user configuration file:

```bash
mkdir -p ~/.boris
cat > ~/.boris/config.yaml << 'EOF'
# Agent defaults
agents:
  default_count: 3
  max_count: 10
  timeout_seconds: 300
  model: "kimi-coding/k2p5"

# Retry configuration
retry:
  max_attempts: 2
  backoff_strategy: "exponential"

# Output settings
output:
  base_dir: "~/.boris/artifacts"
  cleanup_policy: "keep_last_10"

# Logging
logging:
  level: "info"
  format: "text"
EOF
```

### Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Boris Workflow defaults
export BORIS_AGENTS_DEFAULT=3
export BORIS_LOG_LEVEL=info
export BORIS_MODEL=kimi-coding/k2p5
```

## Upgrading

To upgrade to a newer version:

```bash
cd ~/.openclaw/workspace/skills/boris-workflow
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

To remove Boris Workflow:

```bash
# Remove the skill directory
rm -rf ~/.openclaw/workspace/skills/boris-workflow

# Remove configuration (optional)
rm -rf ~/.boris

# Uninstall Python package (if installed)
pip uninstall boris-workflow
```

## Troubleshooting

### OpenClaw CLI Not Found

```
Error: OpenClaw CLI not found at 'openclaw'
```

**Solution:** Ensure OpenClaw is installed and `openclaw` is in your PATH:

```bash
which openclaw
# If not found, add to PATH:
export PATH="$PATH:/path/to/openclaw/bin"
```

### Permission Denied

```
bash: ./bin/boris-run: Permission denied
```

**Solution:** Make the script executable:

```bash
chmod +x ./bin/boris-run
```

### Python Module Not Found

```
ModuleNotFoundError: No module named 'yaml'
```

**Solution:** Install dependencies:

```bash
pip install -r requirements.txt
```

### Web UI Port Already in Use

```
Error: [Errno 98] Address already in use
```

**Solution:** Use a different port:

```bash
cd webui/server
uvicorn main:app --host 0.0.0.0 --port 8081
```

## Verification

After installation, verify everything works:

```bash
# Test basic functionality
./bin/boris-run --tasks "hello|world" --mock --verbose

# Test with verification
./bin/boris-run --tasks "task1|task2" --mock --verify

# Test Web UI (if installed)
cd webui && ./start.sh &
curl http://localhost:8080/api/health
```

## Getting Help

- **Documentation**: See `SKILL.md` for full usage guide
- **Issues**: https://github.com/mukston/boris-workflow/issues
- **OpenClaw Community**: https://discord.gg/openclaw
