/**
 * CDP Browser Automation Module
 * Supports Edge (port 9222) and Chrome (port 9223)
 * Uses the user's already-running browser with remote debugging enabled
 */

const WebSocket = require('/home/yeying233/.npm-global/lib/node_modules/openclaw/node_modules/ws');
const http = require('http');

const DEFAULT_PORTS = { edge: 9222, chrome: 9223 };

// ─── Connection Manager ────────────────────────────────────────────────────────

class ConnectionManager {
    constructor() {
        this.connections = {}; // port -> { ws, browserWs, ready }
    }

    async getConnection(port) {
        if (this.connections[port] && this.connections[port].ws && this.connections[port].ws.readyState === 1) {
            return this.connections[port];
        }

        // Fetch browser WebSocket URL from CDP HTTP endpoint
        const browserUrl = await new Promise((resolve, reject) => {
            http.get(`http://127.0.0.1:${port}/json/version`, r => {
                let d = '';
                r.on('data', c => d += c);
                r.on('end', () => {
                    try { resolve(JSON.parse(d).webSocketDebuggerUrl); }
                    catch { reject(new Error('Failed to parse browser info')); }
                });
            }).on('error', reject);
        });

        // Connect to browser-level CDP
        const ws = await this._connect(browserUrl);

        this.connections[port] = {
            ws,
            ready: true,
            pendingCommands: {},
            idCounter: 0
        };

        return this.connections[port];
    }

    _connect(url) {
        return new Promise((resolve, reject) => {
            const ws = new WebSocket(url, { handshakeTimeout: 10000 });
            ws.on('open', () => resolve(ws));
            ws.on('error', e => reject(e));
            setTimeout(() => reject(new Error('WebSocket timeout')), 10000);
        });
    }

    async send(port, id, method, params = {}) {
        const conn = await this.getConnection(port);
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                conn.pendingCommands[id] = null;
                reject(new Error(`CDP command ${id} (${method}) timed out`));
            }, 20000);

            conn.pendingCommands[id] = (msg) => {
                clearTimeout(timeout);
                resolve(msg);
            };

            conn.ws.send(JSON.stringify({ id, method, params }));
        });
    }
}

// ─── Browser Class ───────────────────────────────────────────────────────────

class Browser {
    constructor(port, name = 'browser') {
        this.port = port;
        this.name = name;
        this.cm = connManager;
        this._tabId = null;
        this._tabWsUrl = null;
    }

    async tabs() {
        // Use HTTP endpoint directly to avoid WebSocket routing complexity in cm.send
        // This is the same approach that works in test scripts
        const doHttp = () => new Promise((resolve, reject) => {
            http.get(`http://127.0.0.1:${this.port}/json/list`, r => {
                let d = '';
                r.on('data', c => d += c);
                r.on('end', () => { try { resolve(JSON.parse(d)); } catch(e) { reject(e); } });
            }).on('error', reject);
        });
        const tabs = await doHttp();
        return tabs.map(t => ({
            id: t.id,
            url: t.url,
            title: t.title,
            type: t.type
        }));
    }

    async newTab(url) {
        // Create a new tab via browser-level WebSocket using HTTP/WS directly (bypasses cm.send routing)
        const browserInfo = await new Promise((res, rej) => {
            http.get(`http://127.0.0.1:${this.port}/json/version`, r => {
                let d = ''; r.on('data', c => d += c); r.on('end', () => { try { res(JSON.parse(d)); } catch(e) { rej(e); } });
            }).on('error', rej);
        });
        const ws = await new Promise((res, rej) => {
            const w = new WebSocket(browserInfo.webSocketDebuggerUrl);
            w.on('open', () => res(w)); w.on('error', rej);
            setTimeout(() => rej(new Error('WS open timeout')), 10000);
        });
        const tabId = await new Promise((resolve, reject) => {
            const id = Math.floor(Math.random() * 999999) + 1;
            const timeout = setTimeout(() => { ws.removeAllListeners('message'); reject(new Error('createTarget timeout')); }, 15000);
            const handler = (data) => {
                const msg = JSON.parse(data.toString());
                if (msg.id === id && msg.result?.targetId) { clearTimeout(timeout); ws.removeListener('message', handler); resolve(msg.result.targetId); }
            };
            ws.on('message', handler);
            ws.send(JSON.stringify({ id, method: 'Target.createTarget', params: { url: url || 'about:blank' } }));
        });
        ws.close();
        this._tabId = tabId;
        this._tabWsUrl = `ws://127.0.0.1:${this.port}/devtools/page/${tabId}`;
        return tabId;
    }

    async goto(url) {
        if (!this._tabId) await this.newTab(url);
        await this._tabCmd('Page.navigate', { url });
        await this._waitForLoad();
        return this;
    }

    async eval(script, returnByValue = true) {
        const data = await this._tabCmd('Runtime.evaluate', {
            expression: script,
            returnByValue
        });
        return data.result;
    }

    async click(selector) {
        await this.eval(`
            (function() {
                var el = document.querySelector('${selector.replace(/'/g, "\\'")}');
                if (!el) throw new Error('Element not found: ${selector}');
                var rect = el.getBoundingClientRect();
                var x = rect.left + rect.width / 2;
                var y = rect.top + rect.height / 2;
                document.elementFromPoint(x, y).click();
                return 'clicked at (' + x + ',' + y + ')';
            })()
        `);
    }

    async screenshot() {
        // Enable screenshot first
        await this._tabCmd('Page.enable');
        const data = await this._tabCmd('Page.captureScreenshot', { format: 'png' });
        return data.result?.data;
    }

    async wait(ms) {
        await new Promise(r => setTimeout(r, ms));
    }

    async _waitForLoad(timeoutMs = 8000) {
        // Wait for Page.loadEventFired
        const p = new Promise((resolve, reject) => {
            const timeout = setTimeout(() => resolve(), timeoutMs); // fallback
            this._tabWs.on('message', (data) => {
                const msg = JSON.parse(data.toString());
                if (msg.method === 'Page.loadEventFired') {
                    clearTimeout(timeout);
                    resolve();
                }
            });
        });
        await p;
        await this.wait(2000); // extra settle time for JS rendering
    }

    async _ensureTab() {
        if (!this._tabId) {
            // Try to use an existing bilibili tab
            const tabs = await this.tabs();
            const existing = tabs.find(t => t.url.includes('bilibili.com'));
            if (existing) {
                this._tabId = existing.id;
                this._tabWsUrl = `ws://127.0.0.1:${this.port}/devtools/page/${existing.id}`;
                return;
            }
            // Create new blank tab
            await this.newTab('about:blank');
        }
    }

    async _browserCmd(method, params = {}) {
        await this._ensureTab();
        const conn = await this.cm.getConnection(this.port);
        const id = ++conn.idCounter;
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => { conn.pendingCommands[id] = null; reject(new Error(`${method} timed out`)); }, 20000);
            conn.pendingCommands[id] = (msg) => { clearTimeout(timeout); resolve(msg); };
            conn.ws.send(JSON.stringify({ id, method, params }));
        });
    }

    async _tabCmd(method, params = {}) {
        await this._ensureTab();
        if (!this._tabWs || this._tabWs.readyState !== 1) {
            this._tabWs = await this.cm._connect(this._tabWsUrl);
        }
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => { reject(new Error(`${method} timed out`)); }, 20000);
            const handler = (data) => {
                const msg = JSON.parse(data.toString());
                if (msg.id === 999) {
                    clearTimeout(timeout);
                    this._tabWs.removeListener('message', handler);
                    resolve(msg);
                }
            };
            this._tabWs.on('message', handler);
            this._tabWs.send(JSON.stringify({ id: 999, method, params }));
        });
    }
}

// ─── Singleton ────────────────────────────────────────────────────────────────

const connManager = new ConnectionManager();
const edge = new Browser(9222, 'Edge');
const chrome = new Browser(9223, 'Chrome');

module.exports = { Browser, edge, chrome };
