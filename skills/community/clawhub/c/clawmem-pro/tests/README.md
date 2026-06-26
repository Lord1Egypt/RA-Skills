# OpenClaw Memory System — Tests

This directory contains automated tests to verify the memory system works correctly.

## Running Tests

### PowerShell (Windows)
```powershell
cd tests
./test-memory-system.ps1
```

### Bash (Linux/macOS)
```bash
cd tests
./test-memory-system.sh
```

## Test Cases

| # | Test | What It Verifies |
|---|---|---|
| 1 | Installation | Directory structure and template files are created |
| 2 | Daily Notes | Today's file is created and formatted correctly |
| 3 | Cron Inbox | Inbox processing works — entries move to daily notes |
| 4 | Memory Extraction | Significant entries are extracted to MEMORY.md |
| 5 | Heartbeat State | State file is updated after heartbeat runs |

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | All tests passed |
| 1 | One or more tests failed |
