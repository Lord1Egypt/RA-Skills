import { spawn } from 'child_process';
import path from 'path';

const uvxCmd = path.join(process.env.USERPROFILE, '.local', 'bin', 'uvx.exe');
const child = spawn(uvxCmd, ['blender-mcp'], { stdio: ['pipe', 'pipe', 'pipe'], shell: true });

child.stdout.on('data', (data) => {
  const lines = data.toString().split('\n');
  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const resp = JSON.parse(line);
      console.log(JSON.stringify(resp, null, 2));
      if (resp.id === 2) process.exit(0);
    } catch(e) {}
  }
});

// 1. Init
child.stdin.write(JSON.stringify({
  jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'test', version: '1.0' } }
}) + '\n');

// 2. List Tools
setTimeout(() => {
  child.stdin.write(JSON.stringify({
    jsonrpc: '2.0', id: 2, method: 'tools/list', params: {}
  }) + '\n');
}, 1000);

setTimeout(() => process.exit(1), 5000);
