#!/usr/bin/env node
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';

/**
 * Blender MCP Bridge for OpenClaw
 * Bridges OpenClaw to the 'blender-mcp' server using stdio.
 */

class BlenderMcpClient {
  constructor() {
    this.process = null;
    this.nextId = 1;
    this.pending = new Map();
    this.initialized = false;
  }

  async start() {
    if (this.initialized) return;

    // UV path check or command
    let uvxCmd = 'uvx';
    const localBin = path.join(process.env.USERPROFILE, '.local', 'bin', 'uvx.exe');
    if (fs.existsSync(localBin)) {
      uvxCmd = localBin;
    }

    this.process = spawn(uvxCmd, ['blender-mcp'], {
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: process.platform === 'win32'
    });

    this.process.stdout.on('data', (data) => {
      const lines = data.toString().split('\n');
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const resp = JSON.parse(line);
          const pending = this.pending.get(resp.id);
          if (pending) {
            this.pending.delete(resp.id);
            if (resp.error) pending.reject(new Error(resp.error.message));
            else pending.resolve(resp.result);
          }
        } catch (e) {
          // Log non-JSON output (maybe logs from the server)
          // console.error('[BlenderMCP Log]', line);
        }
      }
    });

    this.process.stderr.on('data', (data) => {
      // console.error('[BlenderMCP Error]', data.toString());
    });

    // Initialize Handshake
    const initReq = {
      jsonrpc: '2.0',
      id: this.nextId++,
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        capabilities: {},
        clientInfo: { name: 'openclaw-blender-bridge', version: '1.0.0' }
      }
    };

    await this.sendRequest(initReq);
    this.initialized = true;
  }

  sendRequest(req) {
    return new Promise((resolve, reject) => {
      this.pending.set(req.id, { resolve, reject });
      this.process.stdin.write(JSON.stringify(req) + '\n');
      setTimeout(() => {
        if (this.pending.has(req.id)) {
          this.pending.delete(req.id);
          reject(new Error('Timeout calling Blender MCP'));
        }
      }, 30000);
    });
  }

  async callTool(name, args = {}) {
    await this.start();
    const req = {
      jsonrpc: '2.0',
      id: this.nextId++,
      method: 'tools/call',
      params: { name, arguments: args }
    };
    return this.sendRequest(req);
  }
}

const client = new BlenderMcpClient();

export async function execute(inputs) {
  const { tool, arguments: args } = inputs;
  
  // Optimization: Auto-discovery if tool is missing
  if (!tool) {
     return { error: true, message: "Missing tool name. Available: execute_code, search_sketchfab_models, download_sketchfab_model, get_scene_info" };
  }

  try {
    const result = await client.callTool(tool, args || {});
    return result;
  } catch (e) {
    return { error: true, message: e.message };
  }
}
