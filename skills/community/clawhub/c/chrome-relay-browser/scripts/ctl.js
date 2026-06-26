#!/usr/bin/env node

const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// 从 secrets 读取配置
const SECRETS_PATH = path.join(process.env.HOME || os.homedir(), '.openclaw/secrets/browser-relay.env');
let TOKEN = '';
let PORT = 18792;

if (fs.existsSync(SECRETS_PATH)) {
  const content = fs.readFileSync(SECRETS_PATH, 'utf8');
  const tokenMatch = content.match(/RELAY_TOKEN=(.+)/);
  const portMatch = content.match(/RELAY_PORT=(\d+)/);
  if (tokenMatch) TOKEN = tokenMatch[1].trim();
  if (portMatch) PORT = parseInt(portMatch[1], 10);
}

if (!TOKEN) {
  console.error('Error: RELAY_TOKEN not found in', SECRETS_PATH);
  process.exit(1);
}

function getCDP() {
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: '127.0.0.1',
      port: PORT,
      path: '/json',
      headers: { 'x-openclaw-relay-token': TOKEN }
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const tabs = JSON.parse(data);
          if (tabs.length === 0) {
            reject(new Error('No tabs available. Please attach a Chrome tab first.'));
          } else {
            resolve(tabs[0]);
          }
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

function connectCDP() {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(`ws://127.0.0.1:${PORT}/cdp`, {
      headers: { 'x-openclaw-relay-token': TOKEN }
    });
    ws.on('open', () => resolve(ws));
    ws.on('error', reject);
  });
}

async function sendCommand(ws, method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = Math.floor(Math.random() * 10000);
    const handler = (data) => {
      const msg = JSON.parse(data);
      if (msg.id === id) {
        ws.off('message', handler);
        if (msg.result) {
          resolve(msg.result);
        } else if (msg.error) {
          reject(new Error(msg.error.message));
        }
      }
    };
    ws.on('message', handler);
    ws.send(JSON.stringify({ id, method, params }));
    setTimeout(() => {
      ws.off('message', handler);
      reject(new Error('Timeout'));
    }, 10000);
  });
}

async function main() {
  const cmd = process.argv[2];
  const args = process.argv.slice(3);

  if (!cmd) {
    console.log('Usage: node ctl.js <command> [args]');
    console.log('Commands:');
    console.log('  navigate <url>    - Navigate to URL');
    console.log('  screenshot [path] - Take screenshot');
    console.log('  title             - Get page title');
    console.log('  url               - Get current URL');
    console.log('  evaluate <js>     - Execute JS');
    console.log('  click <selector>  - Click element');
    console.log('  fill <selector> <text> - Fill input');
    process.exit(1);
  }

  try {
    const tab = await getCDP();
    const ws = await connectCDP();

    switch (cmd) {
      case 'navigate': {
        const url = args[0];
        if (!url) throw new Error('URL required');
        await sendCommand(ws, 'Page.navigate', { url });
        await new Promise(r => setTimeout(r, 2000));
        console.log('Navigated to:', url);
        break;
      }
      
      case 'screenshot': {
        const result = await sendCommand(ws, 'Page.captureScreenshot', { format: 'png' });
        const filePath = args[0] || '/tmp/screenshot.png';
        fs.writeFileSync(filePath, Buffer.from(result.data, 'base64'));
        console.log('Screenshot saved to:', filePath);
        break;
      }
      
      case 'title': {
        const result = await sendCommand(ws, 'Runtime.evaluate', { expression: 'document.title' });
        console.log(result.result.value);
        break;
      }
      
      case 'url': {
        console.log(tab.url);
        break;
      }
      
      case 'evaluate': {
        const js = args.join(' ');
        const result = await sendCommand(ws, 'Runtime.evaluate', { expression: js });
        console.log(result.result.value);
        break;
      }
      
      case 'click': {
        const selector = args[0];
        if (!selector) throw new Error('Selector required');
        await sendCommand(ws, 'Runtime.evaluate', { 
          expression: `document.querySelector('${selector}')?.click()` 
        });
        console.log('Clicked:', selector);
        break;
      }
      
      case 'fill': {
        const selector = args[0];
        const text = args.slice(1).join(' ');
        if (!selector) throw new Error('Selector required');
        await sendCommand(ws, 'Runtime.evaluate', { 
          expression: `document.querySelector('${selector}').value = '${text.replace(/'/g, "\\'")}'` 
        });
        console.log('Filled:', selector, 'with:', text);
        break;
      }
      
      default:
        console.log('Unknown command:', cmd);
        process.exit(1);
    }

    ws.close();
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();