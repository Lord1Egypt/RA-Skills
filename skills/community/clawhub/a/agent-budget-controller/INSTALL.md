# Installation Guide

## Quick Install (Recommended)

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Agent Budget Controller
export PATH="$HOME/ubik-collective/systems/ubik-pm/skills/agent-budget-controller/scripts:$PATH"
alias budget='python3 $HOME/ubik-collective/systems/ubik-pm/skills/agent-budget-controller/scripts/budget.py'
```

Then reload:
```bash
source ~/.zshrc  # or ~/.bashrc
```

Now you can use `budget` from anywhere:
```bash
budget status
budget check
```

## Alternative: Direct Execution

Run directly without install:
```bash
cd ~/ubik-collective/systems/ubik-pm/skills/agent-budget-controller
python3 scripts/budget.py status
```

## Alternative: UV Install

Install as Python package (requires uv):
```bash
cd ~/ubik-collective/systems/ubik-pm/skills/agent-budget-controller
uv pip install -e .
```

This creates a `budget` command in your Python environment.

## Verification

Test the installation:
```bash
budget --help
budget init
budget status
```

## OpenClaw Integration

Add to OpenClaw's PATH by editing `~/.openclaw/config.yaml`:
```yaml
env:
  PATH: "${PATH}:${HOME}/ubik-collective/systems/ubik-pm/skills/agent-budget-controller/scripts"
```

Or create a wrapper script in OpenClaw's bin directory:
```bash
mkdir -p ~/.openclaw/bin
cat > ~/.openclaw/bin/budget <<'EOF'
#!/bin/bash
exec python3 "$HOME/ubik-collective/systems/ubik-pm/skills/agent-budget-controller/scripts/budget.py" "$@"
EOF
chmod +x ~/.openclaw/bin/budget
```
