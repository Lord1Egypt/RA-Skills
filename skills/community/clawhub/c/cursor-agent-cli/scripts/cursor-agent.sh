#!/bin/bash
# Cursor Agent CLI helper script
# Usage: ./cursor-agent.sh [command] [args...]

set -e

AGENT_BIN="agent"

# Check if agent is installed
if ! command -v $AGENT_BIN &> /dev/null; then
    echo "❌ Cursor Agent CLI not found!"
    echo "Install: curl https://cursor.com/install -fsS | bash"
    exit 1
fi

# Commands
case "${1:-interactive}" in
    interactive|i)
        # Interactive session with optional prompt
        shift
        if [ -n "$1" ]; then
            $AGENT_BIN "$@"
        else
            $AGENT_BIN
        fi
        ;;
    
    plan|p)
        # Planning mode (read-only)
        shift
        $AGENT_BIN --plan "$@"
        ;;
    
    ask|a)
        # Ask mode (Q&A only)
        shift
        $AGENT_BIN --mode=ask "$@"
        ;;
    
    print|pr)
        # Non-interactive print mode
        shift
        $AGENT_BIN -p "$@"
        ;;
    
    cloud|c)
        # Cloud Agent mode
        shift
        $AGENT_BIN -c "$@"
        ;;
    
    resume|r)
        # Resume latest session
        $AGENT_BIN resume
        ;;
    
    continue|cont)
        # Continue previous session
        $AGENT_BIN --continue
        ;;
    
    list|ls)
        # List all sessions
        $AGENT_BIN ls
        ;;
    
    models|m)
        # List available models
        $AGENT_BIN --list-models
        ;;
    
    login)
        # Authenticate
        $AGENT_BIN login
        ;;
    
    status|whoami)
        # Check auth status
        $AGENT_BIN status
        ;;
    
    version|v)
        # Show version
        $AGENT_BIN --version
        ;;
    
    update|u)
        # Update to latest
        $AGENT_BIN update
        ;;
    
    about)
        # System and account info
        $AGENT_BIN about
        ;;
    
    help|h)
        cat << 'EOF'
Cursor Agent CLI Helper

Usage: ./cursor-agent.sh [command] [args...]

Commands:
  interactive, i [prompt]  Start interactive session (default)
  plan, p <prompt>         Planning mode (read-only)
  ask, a <prompt>          Ask mode (Q&A only)
  print, pr <prompt>       Non-interactive mode
  cloud, c <prompt>        Cloud Agent mode
  resume, r                Resume latest session
  continue, cont           Continue previous session
  list, ls                 List all sessions
  models, m                List available models
  login                    Authenticate
  status, whoami           Check auth status
  version, v               Show version
  update, u                Update to latest
  about                    System info
  help, h                  Show this help

Examples:
  ./cursor-agent.sh interactive "refactor auth module"
  ./cursor-agent.sh plan "analyze code structure"
  ./cursor-agent.sh print "fix bugs" --output-format json
  ./cursor-agent.sh cloud "implement feature X"
  ./cursor-agent.sh resume

Options (pass after command):
  --model <model>          Specify model (gpt-5, sonnet-4, etc.)
  --force, --yolo          Auto-approve all commands
  --output-format <fmt>    Output format (text, json, stream-json)
  --workspace <path>       Specify workspace directory
  --sandbox <mode>         Sandbox mode (enabled, disabled)

Documentation: https://cursor.com/docs/cli/overview
EOF
        ;;
    
    *)
        echo "Unknown command: $1"
        echo "Run './cursor-agent.sh help' for usage"
        exit 1
        ;;
esac
