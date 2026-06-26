// broadcast.js - Helper for broadcasting activity from OpenClaw
// Usage: node broadcast.js "activity text" [type]

const { broadcastActivity, broadcastStatus, broadcastTasks } = require('./start-server');

const text = process.argv[2];
const type = process.argv[3] || 'info';

if (!text) {
    console.error('Usage: node broadcast.js "activity text" [type]');
    process.exit(1);
}

broadcastActivity(text, type);
