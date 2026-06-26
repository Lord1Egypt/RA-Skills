#!/bin/bash
# API Monitor - Quick Start

set -e

ACTION="${1:-start}"
CONFIG="${2:-config.json}"

case $ACTION in
  start)
    echo "🚀 Starting API Monitor..."
    mkdir -p data logs
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js not found"
        exit 1
    fi
    
    # Create simple server
    cat > server.js << 'EOF'
const http = require('http');
const fs = require('fs');

const endpoints = JSON.parse(fs.readFileSync('endpoints.json', 'utf8') || '[]');
const results = [];

async function checkEndpoint(url) {
    const start = Date.now();
    try {
        const res = await fetch(url);
        const time = Date.now() - start;
        return { url, status: res.status, time, ok: res.ok };
    } catch (e) {
        return { url, status: 0, time: Date.now() - start, ok: false, error: e.message };
    }
}

async function monitor() {
    const checks = await Promise.all(endpoints.map(checkEndpoint));
    results.push(...checks);
    console.log(JSON.stringify(checks, null, 2));
}

setInterval(monitor, 60000);
monitor();

const html = `
<!DOCTYPE html>
<html>
<head><title>API Monitor</title></head>
<body>
<h1>API Monitor Dashboard</h1>
<pre id="results">Loading...</pre>
<script>
setInterval(() => fetch('/data').then(r=>r.json()).then(d=>{
    document.getElementById('results').textContent = JSON.stringify(d, null, 2);
}), 5000);
</script>
</body>
</html>
`;

require('http').createServer((req, res) => {
    if (req.url === '/data') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify(results.slice(-50)));
    } else {
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.end(html);
    }
}).listen(3000);

console.log('📊 Dashboard: http://localhost:3000');
EOF

    # Create endpoints file
    echo '[]' > endpoints.json
    
    echo "✅ Started!"
    echo "📊 Dashboard: http://localhost:3000"
    ;;
    
  add)
    URL="$2"
    if [ -z "$URL" ]; then
        echo "Usage: $0 add <url>"
        exit 1
    fi
    echo "Adding $URL..."
    cat endpoints.json | jq ". += [\"$URL\"]" > tmp.json && mv tmp.json endpoints.json
    echo "✅ Added $URL"
    ;;
    
  status)
    echo "📊 Recent checks:"
    cat data/*.json 2>/dev/null | tail -20 || echo "No data yet"
    ;;
    
  *)
    echo "Usage: $0 {start|add|status}"
    exit 1
    ;;
esac
