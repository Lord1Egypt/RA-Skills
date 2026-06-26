#!/usr/bin/env node
// Activity Control UI - Local Server
// Starts a simple HTTP and WebSocket server for the activity dashboard

const http = require('http');
const fs = require('fs');
const path = require('path');
const { WebSocketServer } = require('ws');

const DEFAULT_PORT = process.env.PORT || 8080;
const port = process.argv[2] ? parseInt(process.argv[2], 10) || DEFAULT_PORT : DEFAULT_PORT;

// MIME types for serving static files
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml'
};

const skillDir = path.dirname(path.dirname(__filename));
let connectedClients = new Set();
let currentStatus = {
    model: 'unknown',
    session: 'unknown',
    tokensUsed: 0,
    tokensTotal: 262144,
    compactions: 0,
    tasks: []
};
let activityHistory = [];
const MAX_HISTORY = 100;

// Try to load status from OpenClaw (when run from OpenClaw context)
function getOpenClawStatus() {
    try {
        // In the real OpenClaw environment, we'd get this from the API
        // For now, we keep it updated via broadcast
        return currentStatus;
    } catch (e) {
        return currentStatus;
    }
}

function handleRequest(req, res) {
    let filePath = req.url;
    
    if (filePath === '/') {
        filePath = '/assets/control-ui.html';
    }
    
    if (filePath === '/api/status') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(getOpenClawStatus()));
        return;
    }
    
    const fullPath = path.join(skillDir, filePath);
    const ext = path.extname(fullPath);
    
    fs.readFile(fullPath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end('Not Found');
            return;
        }
        
        const contentType = mimeTypes[ext] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(data);
    });
}

const server = http.createServer(handleRequest);
const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
    connectedClients.add(ws);
    
    // Send current state on connect
    ws.send(JSON.stringify({
        type: 'status',
        ...currentStatus
    }));
    
    if (activityHistory.length > 0) {
        activityHistory.forEach(activity => {
            ws.send(JSON.stringify({
                type: 'activity',
                ...activity
            }));
        });
    }
    
    ws.send(JSON.stringify({
        type: 'tasks',
        tasks: currentStatus.tasks
    }));
    
    ws.on('message', (data) => {
        try {
            const msg = JSON.parse(data);
            if (msg.action === 'compact') {
                // Tell all clients we're compacting - the actual compact is handled by OpenClaw
                broadcastActivity('Initiating context compaction...', 'info');
                // In real integration, this would call the OpenClaw API
            }
        } catch (e) {
            console.error('WS message error:', e);
        }
    });
    
    ws.on('close', () => {
        connectedClients.delete(ws);
    });
});

function broadcastStatus(status) {
    currentStatus = { ...currentStatus, ...status };
    const msg = JSON.stringify({ type: 'status', ...currentStatus });
    connectedClients.forEach(client => {
        if (client.readyState === 1) {
            client.send(msg);
        }
    });
}

function broadcastActivity(text, type = 'info') {
    const activity = {
        timestamp: Math.floor(Date.now() / 1000),
        text,
        type
    };
    activityHistory.unshift(activity);
    if (activityHistory.length > MAX_HISTORY) {
        activityHistory.pop();
    }
    
    const msg = JSON.stringify({ type: 'activity', ...activity });
    connectedClients.forEach(client => {
        if (client.readyState === 1) {
            client.send(msg);
        }
    });
}

function broadcastTasks(tasks) {
    currentStatus.tasks = tasks;
    const msg = JSON.stringify({ type: 'tasks', tasks });
    connectedClients.forEach(client => {
        if (client.readyState === 1) {
            client.send(msg);
        }
    });
}

// Export broadcast functions for use by OpenClaw
module.exports = {
    broadcastStatus,
    broadcastActivity,
    broadcastTasks
};

server.listen(port, () => {
    console.log(`Activity Control UI running at http://localhost:${port}`);
    console.log('WebSocket endpoint: ws://localhost:${port}/ws/activity');
});

// Handle exit
process.on('SIGINT', () => {
    server.close();
    process.exit(0);
});
