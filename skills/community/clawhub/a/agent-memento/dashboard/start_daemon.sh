#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Run securely on localhost, require manual flag for public exposure
nohup node server.js "$@" > dashboard.log 2>&1 &
echo $! > dashboard.pid
echo "Dashboard daemon started with PID $(cat dashboard.pid). Logs in dashboard.log"
