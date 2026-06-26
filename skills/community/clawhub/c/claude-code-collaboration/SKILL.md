# Claude Code Collaboration

Enable OpenClaw to delegate tasks to Claude Code CLI for collaborative discussions and complex task execution. When OpenClaw needs deeper analysis, coding assistance, or multi-turn discussions with a powerful code-generation model, it writes tasks to a queue and Claude Code Interface Agent executes them.

## Architecture

```
OpenClaw (main agent)
  ↓ writes task .json
Claude Code Interface Agent (polling loop)
  ↓ calls claude CLI with env vars
Claude Code CLI →阿里云 API (qwen3.5-plus)
  ↓ returns result .json
OpenClaw reads result and continues
```

## Setup Requirements

### 1. Install Claude Code CLI

```bash
# macOS
brew install anthropic/claude-code/claude-code

# Or via npm
npm install -g @anthropic/claude-code
```

### 2. Configure Environment Variables

The agent requires these environment variables:

```bash
export ANTHROPIC_AUTH_TOKEN="your-api-token"
export ANTHROPIC_BASE_URL="https://coding.dashscope.aliyuncs.com/apps/anthropic"
export ANTHROPIC_MODEL="qwen3.5-plus"  # or your preferred model
```

### 3. Start the Interface Agent

```bash
mkdir -p ~/.openclaw/agents/main/workspace/.oc-cc-in
mkdir -p ~/.openclaw/agents/main/workspace/.oc-cc-out

python3 agent.py &
```

## Usage

### Sending a Task

Create a JSON file in `.oc-cc-in/` with:

```json
{
  "task_id": "unique-task-id",
  "prompt": "Your question or task for Claude Code",
  "priority": "normal"
}
```

The interface agent polls the directory, executes via Claude Code CLI, and writes results to `.oc-cc-out/{task_id}.json`.

### Reading Results

Results are JSON files with:
- `task_id`: Task identifier
- `status`: "completed" or "failed"
- `prompt`: Original prompt
- `stdout`: Claude Code's response
- `stderr`: Error output if any
- `returncode`: Exit code
- `completed_at`: ISO timestamp

### Example: Collaborative Discussion

OpenClaw sends:
```json
{
  "task_id": "discuss-01",
  "prompt": "Analyze the pros and cons of microservices vs monolith for a small startup. Provide concrete recommendations.",
  "priority": "high"
}
```

Claude Code returns detailed analysis in `stdout`, OpenClaw reads it and continues the conversation with the user.

## Directory Structure

```
.oc-cc-agent/
├── agent.py          # Interface agent (polling loop)
.oc-cc-in/            # Input queue (tasks to process)
.oc-cc-out/           # Output queue (results)
.oc-cc-chat.log      # Conversation log
.oc-cc-status.json   # Agent status
```

## Monitoring

- **Status**: Check `.oc-cc-status.json` for agent state
- **Logs**: Conversation log at `.oc-cc-chat.log`
- **View Results**: Read JSON files in `.oc-cc-out/`

## Configuration

Key settings in `agent.py`:

```python
WORK_DIR = "/path/to/workspace"  # Claude Code's working directory
IN_DIR = f"{WORK_DIR}/.oc-cc-in"
OUT_DIR = f"{WORK_DIR}/.oc-cc-out"
LOG_FILE = f"{WORK_DIR}/.oc-cc-chat.log"
PORT = 18790  # Optional HTTP server port
TIMEOUT = 120  # seconds
```
