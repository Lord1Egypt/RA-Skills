# Hevy CLI API Commands Reference

## Core Commands

### Workouts
- `hevycli workout list [--since YYYY-MM-DD] [--all] [--output json|table|plain]`
- `hevycli workout get <workout-id> [--output json]`
- `hevycli workout count [--output json]`
- `hevycli workout create --file workout.json`
- `hevycli workout update <id> --file workout.json`
- `hevycli workout delete <id>`
- `hevycli workout start` (interactive session)

### Routines
- `hevycli routine list [--output json]`
- `hevycli routine get <routine-id> [--output json]`
- `hevycli routine create --file routine.json`
- `hevycli routine update <id> --file routine.json`
- `hevycli routine builder` (interactive)

### Exercises
- `hevycli exercise list [--output json]`
- `hevycli exercise get <exercise-id> [--output json]`
- `hevycli exercise search "<query>" [--output json]`
- `hevycli exercise create --title "Exercise Name" --type weight_reps --muscle chest`
- `hevycli exercise interactive` (browse exercises)

### Statistics & Analytics
- `hevycli stats summary [--period week|month|year] [--output json]`
- `hevycli stats progress "<exercise-name>" [--metric weight|1rm] [--output json]`
- `hevycli stats records [--exercise "<name>"] [--output json]`

### Configuration
- `hevycli config init` (interactive setup)
- `hevycli config show`
- `hevycli config set api-key <key>`

## Output Formats

### JSON (Recommended for Agent Use)
```bash
hevycli workout list --output json
```
Returns structured data suitable for parsing and analysis.

### Table (Human-Readable)
```bash
hevycli workout list --output table
```
Default format. Good for console display.

### Plain (Pipe-Delimited)
```bash
hevycli workout list --output plain
```
Simple format for basic parsing.

## Common Patterns

### Recent Activity Analysis
```bash
# Last 7 days
hevycli workout list --since $(date -d '7 days ago' '+%Y-%m-%d') --output json

# Last 30 days
hevycli workout list --since $(date -d '30 days ago' '+%Y-%m-%d') --output json
```

### Progress Tracking
```bash
# Track weight progression
hevycli stats progress "Bench Press" --output json

# Track estimated 1RM
hevycli stats progress "Squat" --metric 1rm --output json
```

### Workout Summary
```bash
# Monthly overview
hevycli stats summary --period month --output json

# Weekly overview
hevycli stats summary --period week --output json
```

## Exit Codes
- 0: Success
- 1: General error
- 2: Invalid arguments
- 3: API authentication error
- 4: API rate limit exceeded
- 5: Network error
- 6: Resource not found
- 7: Validation error

## Environment Variables
- `HEVYCLI_API_KEY`: API key override
- `HEVYCLI_OUTPUT_FORMAT`: Default output format (json|table|plain)
- `HEVYCLI_UNITS`: Units preference (metric|imperial)
- `HEVYCLI_NO_COLOR`: Disable color output (true|false)