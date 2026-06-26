# Fullrun - Task Executor

## Usage

Run the following command to execute tasks:

```bash
# Check status and run tasks if idle
./scripts/main.sh run

# Or start the background monitor (checks every minute)
./scripts/main.sh start
```

## Files

- `checklist.md` - Task list (edit to add tasks)
- `.claude-status.txt` - Execution state (1=running, 0=idle)
- `scripts/main.sh` - Main entry point

## Commands

| Command | Description |
|---------|-------------|
| `./scripts/main.sh start` | Start background monitor |
| `./scripts/main.sh stop` | Stop background monitor |
| `./scripts/main.sh run` | Run tasks once |
| `./scripts/main.sh status` | Show current status |
