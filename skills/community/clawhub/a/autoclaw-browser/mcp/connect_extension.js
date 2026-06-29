const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 30000 });

wss.on('connection', function connection(ws) {
  console.log('Extension connected');
  
  ws.on('message', function incoming(message) {
    console.log('Received:', message);
  });
  
  ws.on('close', function close() {
    console.log('Extension disconnected');
  });
});

console.log('AutoClaw MCP Server running on port 30000');
