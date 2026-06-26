#!/bin/bash
# Resume a stopped AI agent process

if [ -z "$1" ]; then
    echo "Usage: $0 <PID>"
    echo "Resume a stopped AI agent process"
    exit 1
fi

PID=$1

# Check if process exists
if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "Error: Process $PID does not exist"
    exit 1
fi

# Check if process is stopped
STATE=$(ps -o stat= -p "$PID" | head -c 1)

if [ "$STATE" != "T" ]; then
    echo "Warning: Process $PID is not stopped (state: $STATE)"
    echo "Current state: $(ps -o stat,cmd -p $PID)"
    read -p "Resume anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Resume the process
echo "Resuming process $PID..."
kill -CONT "$PID"

if [ $? -eq 0 ]; then
    echo "✅ Process $PID resumed successfully"
    sleep 1
    echo "Current state: $(ps -o stat,cmd -p $PID)"
else
    echo "❌ Failed to resume process $PID"
    exit 1
fi
