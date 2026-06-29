/**
 * AutoClaw Chrome Extension - Background Service Worker
 * @version 6.1.0
 * 修复记录:
 * 1. [崩溃] 移除重复Ping定时器（原有5s+10s双ping会造成双倍心跳压力）
 * 2. [崩溃] onRelayClosed 中批量 detach 改为串行，防止并发崩溃
 * 3. [崩溃] attachTab 时增加 Network.enable + Input.enable，保证 CDP 协议完整启用
 * 4. [交互] handleForwardCdpCommand 修复 debuggee session 混淆问题
 * 5. [交互] Target.getTargets 改用 chrome.tabs.query 实现，更准确
 * 6. [稳定] 重连使用指数退避，避免频繁重连冲击服务器
 * 7. [稳定] tab 创建延迟从 500ms 提升到 800ms，给页面更多初始化时间
 * 8. [交互] 添加 Input.enable，启用 Input 域支持触摸和键盘事件
 * 
 * 优化记录 (v5.2.0):
 * 1. [性能] CDP域按需开启：不再一次性开启所有域，根据实际使用动态开启Network/Input等
 * 2. [性能] 降低轮询频率：连接监控从5秒改为30秒，popup状态检查从3秒改为10秒
 * 3. [性能] DOM缓存机制：添加15秒DOM缓存，减少重复获取
 * 4. [功能] 简化DOM获取：新增getSimplifiedDOM方法，返回索引化可交互元素
 * 
 * 重大更新 (v6.0.0):
 * 1. [简化] 移除双端口模式，简化为单一端口配置
 * 2. [功能] 用户可自定义Token，不再强制使用内置Token
 * 3. [UI] 设置页面简化，端口和Token可直接编辑
 * 
 * 新功能 (v6.1.0):
 * 1. [功能] 操作录制/回放：记录用户在页面上的操作并回放
 * 2. [功能] 预设工作流模板：内置常用自动化流程
 * 3. [调试] 调试日志面板：实时显示操作日志
 * 4. [UI] 新的Tab界面：Main/Record/Workflows/Debug
 */
'use strict';

const DEFAULT_PORT = 30000;
const BUILT_IN_TOKEN = 'autoclaw_builtin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs';
const DEFAULT_AUTH_HOURS = 24;
const DEFAULT_MAX_TABS = 50;

const BADGE = {
  off:        { text: 'OFF', color: '#9CA3AF' },
  connecting: { text: '···', color: '#F59E0B' },
  on:         { text: 'ON',  color: '#10B981' },
  error:      { text: '!',   color: '#EF4444' },
};

let relayWs = null;
let relayConnecting = false;
let debugListenersInstalled = false;
let nextSession = 1;
let reconnectDelay = 3000;
const MAX_RECONNECT_DELAY = 30000;

const tabs = new Map();
const tabBySession = new Map();
const childSessionToTab = new Map();
const pending = new Map();

// [优化#1] CDP域按需管理 - 减少资源占用
const cdpDomainsEnabled = new Map(); // tabId -> Set(enabledDomains)

// 基础必须开启的域
const BASE_DOMAINS = ['Page', 'Runtime'];

async function enableCDPDomainIfNeeded(tabId, domain) {
  const domains = cdpDomainsEnabled.get(tabId);
  if (domains && domains.has(domain)) return true;
  
  const debuggee = { tabId };
  try {
    await chrome.debugger.sendCommand(debuggee, `${domain}.enable`);
    if (!domains) {
      cdpDomainsEnabled.set(tabId, new Set([...BASE_DOMAINS]));
    }
    cdpDomainsEnabled.get(tabId).add(domain);
    console.log(`[AutoClaw] CDP域 ${domain} 已开启 for tab ${tabId}`);
    return true;
  } catch (err) {
    console.warn(`[AutoClaw] 开启CDP域 ${domain} 失败:`, err.message);
    return false;
  }
}

// 根据CDP方法名自动判断需要开启的域
function getRequiredDomain(method) {
  if (method.includes('Network.') || method === 'Fetch.enable' || method === 'Fetch.disable') {
    return 'Network';
  }
  if (method.includes('Input.') || method.includes('Emulation.')) {
    return 'Input';
  }
  if (method.includes('Log.') || method.includes('Console.')) {
    return 'Log';
  }
  if (method.includes('Debugger.') || method.includes('Breakpoint')) {
    return 'Debugger';
  }
  if (method.includes('Performance.')) {
    return 'Performance';
  }
  if (method.includes('Animation.')) {
    return 'Animation';
  }
  return null;
}

// [优化#2] DOM缓存机制 - 减少重复获取
const domCache = new Map(); // tabId -> { timestamp, simplifiedDOM }
const DOM_CACHE_TTL = 15000; // 15秒缓存有效期

function getCachedDOM(tabId) {
  const cached = domCache.get(tabId);
  if (cached && Date.now() - cached.timestamp < DOM_CACHE_TTL) {
    return cached.simplifiedDOM;
  }
  return null;
}

function setCachedDOM(tabId, simplifiedDOM) {
  domCache.set(tabId, { timestamp: Date.now(), simplifiedDOM });
}

function clearCachedDOM(tabId) {
  domCache.delete(tabId);
}

// [优化#3] 简化DOM获取函数 - 借鉴Page Agent核心技术
// 返回索引化的可交互元素列表，大幅减少数据传输量
async function getSimplifiedDOM(tabId) {
  // 优先使用缓存
  const cached = getCachedDOM(tabId);
  if (cached) {
    return cached;
  }

  // 如果tab未连接，返回空
  if (!tabs.has(tabId)) {
    return '[]';
  }

  try {
    // 确保Runtime域已开启
    await enableCDPDomainIfNeeded(tabId, 'Runtime');

    const result = await chrome.debugger.sendCommand(
      { tabId },
      'Runtime.evaluate',
      {
        expression: `
          (function() {
            // 选取可交互元素
            const selectors = [
              'button', 'a', 'input', 'select', 'textarea',
              '[role="button"]', '[role="link"]', '[onclick]',
              '[tabindex]', '[contenteditable="true"]'
            ];
            const elements = document.querySelectorAll(selectors.join(','));
            
            // 过滤并索引化
            const interactive = [];
            elements.forEach((el, idx) => {
              if (el.offsetParent === null) return; // 隐藏元素跳过
              
              const tag = el.tagName.toLowerCase();
              let text = el.textContent?.trim() || '';
              let placeholder = el.placeholder || '';
              let value = el.value || '';
              let id = el.id || '';
              let name = el.name || '';
              let type = el.type || '';
              let href = el.href || '';
              let classes = el.className || '';
              
              // 文本太长则截断
              if (text.length > 60) text = text.substring(0, 60) + '...';
              
              // 排除空白元素
              if (!text && !placeholder && !value && tag !== 'a') return;
              
              interactive.push({
                index: idx,
                tag: tag,
                text: text,
                placeholder: placeholder,
                value: value,
                id: id,
                name: name,
                type: type,
                href: href,
                classes: classes
              });
            });
            
            return JSON.stringify(interactive.slice(0, 50)); // 最多50个元素
          })()
        `,
        returnByValue: true
      }
    );

    let simplifiedDOM = '[]';
    if (result?.result?.value) {
      simplifiedDOM = result.result.value;
      setCachedDOM(tabId, simplifiedDOM);
    }
    return simplifiedDOM;
  } catch (err) {
    console.warn('[AutoClaw] getSimplifiedDOM 失败:', err.message);
    return '[]';
  }
}

async function getConfig() {
  const s = await chrome.storage.local.get([
    'relayPort', 'gatewayToken', 'authTimestamp', 'authHours',
    'autoAttachAll', 'openMode', 'maxTabs'
  ]);
  const port = parseInt(String(s.relayPort || ''), 10) || DEFAULT_PORT;
  // 用户自定义token或默认内置token
  const token = s.gatewayToken ? String(s.gatewayToken).trim() : BUILT_IN_TOKEN;
  
  return {
    port:         port,
    token:        token,
    timestamp:    Number(s.authTimestamp) || 0,
    authHours:    Number(s.authHours) || DEFAULT_AUTH_HOURS,
    autoAttachAll: s.autoAttachAll === true,
    openMode:     s.openMode || 'newTab',
    maxTabs:      Number(s.maxTabs) || DEFAULT_MAX_TABS,
  };
}

async function isAuthValid() {
  // 取消时间授权，改为永久化授权
  // 只要插件安装并连接成功，就保持授权状态
  return true;
}

async function setAllBadges(kind) {
  const cfg = BADGE[kind] || BADGE.off;
  const tabCount = tabs.size;
  const displayText = kind === 'on' && tabCount > 0 ? String(tabCount) : cfg.text;
  const titles = {
    off:        `AutoClaw: Not Connected (${tabCount} tabs)`,
    connecting: 'AutoClaw: Connecting...',
    on:         `AutoClaw: Connected (${tabCount} tabs)`,
    error:      'AutoClaw: Connection Error',
  };
  try {
    await chrome.action.setBadgeText({ text: displayText });
    await chrome.action.setBadgeBackgroundColor({ color: cfg.color });
    await chrome.action.setTitle({ title: titles[kind] || 'AutoClaw' });
  } catch {}
}

function setTabBadge(tabId, kind) {
  const cfg = BADGE[kind] || BADGE.off;
  chrome.action.setBadgeText({ tabId, text: cfg.text }).catch(() => {});
  chrome.action.setBadgeBackgroundColor({ tabId, color: cfg.color }).catch(() => {});
}

async function connectGateway() {
  if (relayWs && relayWs.readyState === WebSocket.OPEN) return;
  if (relayConnecting) { await new Promise(r => setTimeout(r, 500)); return; }

  const { port, token } = await getConfig();
  if (!token) throw new Error('Token not configured');

  relayConnecting = true;
  await setAllBadges('connecting');

  try {
    const wsUrl = token ? `ws://127.0.0.1:${port}/extension?token=${encodeURIComponent(token)}` : `ws://127.0.0.1:${port}/extension`;
    console.log('[AutoClaw] Connecting to MCP Server:', wsUrl.replace(token, '***'));

    await new Promise((resolve, reject) => {
      const ws = new WebSocket(wsUrl);
      const timeout = setTimeout(() => { ws.close(); reject(new Error('Connection timeout')); }, 3000);  // 减少到3秒

      ws.onopen = () => {
        clearTimeout(timeout);
        relayWs = ws;
        reconnectDelay = 3000; // 重置退避
        if (!debugListenersInstalled) {
          debugListenersInstalled = true;
          chrome.debugger.onEvent.addListener(onDebuggerEvent);
          chrome.debugger.onDetach.addListener(onDebuggerDetach);
        }
        ws.onmessage = (e) => onRelayMessage(String(e.data));
        ws.onclose   = (event) => {
          clearTimeout(timeout);
          onRelayClosed('closed');
          reject(new Error(`Connection closed code=${event.code}`));
        };
        ws.onerror   = (error) => {
          clearTimeout(timeout);
          onRelayClosed('error');
          reject(new Error('Connection failed'));
        };
        updateConnectionStatus();
        resolve();
      };
    });

    await setAllBadges('on');
    console.log('[AutoClaw] MCP Server Connected');
  } catch (err) {
    relayWs = null;
    await setAllBadges('error');
    throw err;
  } finally {
    relayConnecting = false;
  }
}

// [修复#2] 串行 detach，避免并发崩溃
async function onRelayClosed(reason) {
  console.log('[AutoClaw] MCP Server Disconnected:', reason);
  relayWs = null;
  for (const [id, p] of pending.entries()) { pending.delete(id); p.reject(new Error(`Connection lost: ${reason}`)); }
  for (const tabId of [...tabs.keys()]) {
    try { await chrome.debugger.detach({ tabId }); } catch {}
    setTabBadge(tabId, 'off');
  }
  tabs.clear(); tabBySession.clear(); childSessionToTab.clear();
  await setAllBadges('off');
  updateConnectionStatus();
  // [增强] 智能重连机制：立即重试 + 指数退避
  const attemptReconnect = async () => {
    if (!(await isAuthValid())) return;
    
    console.log(`[AutoClaw] 尝试重新连接 (延迟: ${reconnectDelay}ms)`);
    
    try {
      await connectGateway();
      reconnectDelay = 3000; // 成功连接后重置延迟
      console.log('[AutoClaw] ✅ 重新连接成功');
    } catch (error) {
      console.log(`[AutoClaw] ❌ 重新连接失败: ${error.message}`);
      // 指数退避，但最大不超过30秒
      reconnectDelay = Math.min(reconnectDelay * 2, MAX_RECONNECT_DELAY);
      setTimeout(attemptReconnect, reconnectDelay);
    }
  };
  
  // 立即开始第一次重试
  setTimeout(attemptReconnect, 1000);
}

// 简化消息发送 - 单端口模式
function sendToRelay(payload) {
  if (!relayWs || relayWs.readyState !== WebSocket.OPEN) {
    throw new Error('No active MCP server connection');
  }
  relayWs.send(JSON.stringify(payload));
}



// ==================== Bookmark Operations ====================
async function handleBookmarkOp(msg) {
  const { id, action, payload } = msg;
  try {
    let result;
    switch (action) {
      case 'getBookmarks': {
        const tree = await chrome.bookmarks.getTree();
        const flatten = (nodes) => {
          const list = [];
          for (const node of nodes) {
            if (node.url) list.push({ id: node.id, title: node.title, url: node.url, parentId: node.parentId, dateAdded: node.dateAdded });
            if (node.children) list.push(...flatten(node.children));
          }
          return list;
        };
        result = flatten(tree);
        break;
      }
      case 'getBookmarkTree': result = await chrome.bookmarks.getTree(); break;
      case 'searchBookmarks': result = await chrome.bookmarks.search(String(payload?.query || '')); break;
      case 'createBookmark': {
        const d = { title: String(payload.title || ''), url: String(payload.url || '') };
        if (payload.parentId) d.parentId = String(payload.parentId);
        result = await chrome.bookmarks.create(d);
        break;
      }
      case 'updateBookmark': {
        const upd = {};
        if (payload.title !== undefined) upd.title = payload.title;
        if (payload.url   !== undefined) upd.url   = payload.url;
        result = await chrome.bookmarks.update(String(payload.id), upd);
        break;
      }
      case 'deleteBookmark': {
        await chrome.bookmarks.remove(String(payload.id));
        result = { success: true, id: payload.id };
        break;
      }
      case 'removeFolder': {
        await chrome.bookmarks.removeTree(String(payload.id));
        result = { success: true, id: payload.id };
        break;
      }
      case 'createFolder': {
        const fd = { title: String(payload.title || 'New Folder') };
        if (payload.parentId) fd.parentId = String(payload.parentId);
        result = await chrome.bookmarks.create(fd);
        break;
      }
      case 'moveBookmark': {
        result = await chrome.bookmarks.move(String(payload.id), { parentId: String(payload.parentId), index: payload.index });
        break;
      }
      case 'openInNewTab': {
        const url = String(payload?.url || '');
        if (!url) throw new Error('URL cannot be empty');
        const newTab = await chrome.tabs.create({ url, active: false });
        const config = await getConfig();
        if (config.autoAttachAll && newTab.id && tabs.size < config.maxTabs) {
          setTimeout(async () => {
            try { await connectGateway(); await attachTab(newTab.id); } catch {}
          }, 800); // [修复#7]
        }
        result = { success: true, tabId: newTab.id, url };
        break;
      }
      default:
        throw new Error(`Unknown bookmark operation: ${action}`);
    }
    sendToRelay({ id, result });
  } catch (err) {
    console.error('[AutoClaw] Bookmark operation failed:', err.message);
    sendToRelay({ id, error: err.message });
  }
}

async function onRelayMessage(text) {
  let msg;
  try { msg = JSON.parse(text); } catch { return; }
  // [修复#1] 只响应 ping，不自己发起心跳（服务端已有心跳定时器）
  if (msg.method === 'ping') { try { sendToRelay({ method: 'pong' }); } catch {} return; }
  if (msg.method === 'bookmarkOp') { await handleBookmarkOp(msg); return; }
  if (msg.method === 'configOp') { await handleConfigOp(msg); return; }
  if (typeof msg.id === 'number' && (msg.result !== undefined || msg.error !== undefined)) {
    const p = pending.get(msg.id);
    if (!p) return;
    pending.delete(msg.id);
    if (msg.error) p.reject(new Error(String(msg.error))); else p.resolve(msg.result);
    return;
  }
  if (typeof msg.id === 'number' && msg.method === 'forwardCDPCommand') {
    try {
      const result = await handleForwardCdpCommand(msg);
      sendToRelay({ id: msg.id, result });
    } catch (err) {
      const method = msg?.params?.method || '';
      if (err.message.includes('not attached') || err.message.includes('No attached tab')) {
        console.log('[AutoClaw] CDP session invalid, trying to reattach...');
        const tabId = getAnyConnectedTab();
        if (tabId) {
          try { await chrome.debugger.detach({ tabId }); } catch {}
          tabs.delete(tabId);
          tabBySession.delete(tabId);
          childSessionToTab.forEach((csid, ptid) => { if (ptid === tabId) childSessionToTab.delete(csid); });
        }
      }
      sendToRelay({ id: msg.id, error: err.message });
    }
  }

  // [优化#3] 新增：获取简化DOM的命令
  if (msg.method === 'getSimplifiedDOM') {
    try {
      const tabId = getAnyConnectedTab();
      if (!tabId) throw new Error('No connected tab');
      const dom = await getSimplifiedDOM(tabId);
      sendToRelay({ id: msg.id, result: dom });
    } catch (err) {
      sendToRelay({ id: msg.id, error: err.message });
    }
  }
}

// [优化#1] attachTab 改为按需开启CDP域 - 减少资源占用
async function attachTab(tabId, opts = {}) {
  const config = await getConfig();
  if (tabs.size >= config.maxTabs) throw new Error(`Tab limit reached (${config.maxTabs})`);
  const debuggee = { tabId };
  
  // 先清理该tab的CDP域状态
  cdpDomainsEnabled.delete(tabId);
  clearCachedDOM(tabId);
  
  try { await chrome.debugger.detach(debuggee); } catch {}
  await chrome.debugger.attach(debuggee, '1.3');
  
  // [优化] 只开启基础必需的域，其他按需开启
  await chrome.debugger.sendCommand(debuggee, 'Page.enable').catch(() => {});
  await chrome.debugger.sendCommand(debuggee, 'Runtime.enable').catch(() => {});
  cdpDomainsEnabled.set(tabId, new Set(BASE_DOMAINS));
  
  // Network和Input按需开启，不在这里一次性开启
  // 等待实际使用时再动态开启
  
  const info = await chrome.debugger.sendCommand(debuggee, 'Target.getTargetInfo').catch(() => ({}));
  const targetId = String(info?.targetInfo?.targetId || `local-${tabId}`);
  const sessionId = `cb-tab-${nextSession++}`;
  tabs.set(tabId, { state: 'connected', sessionId, targetId });
  tabBySession.set(sessionId, tabId);
  if (!opts.skipEvent) {
    try { sendToRelay({ method: 'forwardCDPEvent', params: { method: 'Target.attachedToTarget', params: { sessionId, targetInfo: { ...(info.targetInfo || {}), targetId, attached: true }, waitingForDebugger: false } } }); } catch {}
  }
  setTabBadge(tabId, 'on');
  return { sessionId, targetId };
}

async function detachTab(tabId, reason) {
  const tab = tabs.get(tabId);
  if (tab?.sessionId && tab?.targetId) {
    try { sendToRelay({ method: 'forwardCDPEvent', params: { method: 'Target.detachedFromTarget', params: { sessionId: tab.sessionId, targetId: tab.targetId, reason } } }); } catch {}
  }
  if (tab?.sessionId) tabBySession.delete(tab.sessionId);
  tabs.delete(tabId);
  for (const [csid, ptid] of childSessionToTab.entries()) { if (ptid === tabId) childSessionToTab.delete(csid); }
  try { await chrome.debugger.detach({ tabId }); } catch {}
  // [优化] 清理该tab的CDP域状态和缓存
  cdpDomainsEnabled.delete(tabId);
  clearCachedDOM(tabId);
  setTabBadge(tabId, 'off');
}

function getTabBySessionId(sessionId) { return tabBySession.get(sessionId) || null; }
function getTabByTargetId(targetId) { for (const [tabId, tab] of tabs.entries()) { if (tab.targetId === targetId) return tabId; } return null; }
function getAnyConnectedTab() { for (const [tabId, tab] of tabs.entries()) { if (tab.state === 'connected') return tabId; } return null; }

// [修复#4 #5] 修复 CDP 转发：debuggee session 混淆问题 + Target.getTargets 实现
async function handleForwardCdpCommand(msg) {
  const method    = String(msg?.params?.method || '').trim();
  const params    = msg?.params?.params;
  const sessionId = typeof msg?.params?.sessionId === 'string' ? msg.params.sessionId : undefined;
  const tabId = (sessionId ? getTabBySessionId(sessionId) : null) || (params?.targetId ? getTabByTargetId(params.targetId) : null) || getAnyConnectedTab();
  if (!tabId) throw new Error(`No attached tab: ${method}`);
  const debuggee = { tabId };

  if (method === 'Target.createTarget') {
    const config = await getConfig();
    if (tabs.size >= config.maxTabs) throw new Error(`Tab limit reached`);
    const url = typeof params?.url === 'string' ? params.url : 'about:blank';
    if (config.openMode === 'newTab') {
      const newTab = await chrome.tabs.create({ url, active: false });
      if (!newTab.id) throw new Error('Failed to create tab');
      await new Promise(r => setTimeout(r, 300));
      const attached = await attachTab(newTab.id);
      return { targetId: attached.targetId };
    } else {
      await chrome.tabs.update(tabId, { url });
      return { targetId: tabs.get(tabId)?.targetId };
    }
  }

  if (method === 'Target.closeTarget') {
    const toClose = params?.targetId ? getTabByTargetId(params.targetId) : tabId;
    if (!toClose) return { success: false };
    try { await chrome.tabs.remove(toClose); } catch { return { success: false }; }
    return { success: true };
  }

  if (method === 'Target.activateTarget') {
    const toActivate = params?.targetId ? getTabByTargetId(params.targetId) : tabId;
    if (!toActivate) return {};
    const t = await chrome.tabs.get(toActivate).catch(() => null);
    if (!t) return {};
    if (t.windowId) await chrome.windows.update(t.windowId, { focused: true }).catch(() => {});
    await chrome.tabs.update(toActivate, { active: true }).catch(() => {});
    return {};
  }

  // [修复#5] Target.getTargets 使用 chrome.tabs.query 实现，更准确
  if (method === 'Target.getTargets') {
    const allTabs = await chrome.tabs.query({});
    return {
      targetInfo: allTabs.map(t => ({
        targetId: tabs.get(t.id)?.targetId || String(t.id),
        type: 'page',
        url: t.url || '',
        title: t.title || '',
        attached: tabs.has(t.id),
        browserContextId: ''
      }))
    };
  }

  // [修复#4] 只有子session才混入sessionId，避免主tab session混淆
  const tabState = tabs.get(tabId);
  const useDebugger = (sessionId && tabState?.sessionId && sessionId !== tabState.sessionId)
    ? { ...debuggee, sessionId }
    : debuggee;

  // [优化#1] 按需开启CDP域 - 根据方法名自动判断需要的域
  const requiredDomain = getRequiredDomain(method);
  if (requiredDomain) {
    await enableCDPDomainIfNeeded(tabId, requiredDomain);
  }

  // 对于需要输入的操作，确保Input域已开启
  if (method.includes('Input.') || method === 'Runtime.evaluate') {
    await enableCDPDomainIfNeeded(tabId, 'Input');
  }

  // [优化#3] 页面加载/导航时清除缓存
  if (method === 'Page.navigate' || method === 'Page.reload') {
    clearCachedDOM(tabId);
  }

  return await chrome.debugger.sendCommand(useDebugger, method, params);
}

function onDebuggerEvent(source, method, params) {
  const tabId = source.tabId;
  if (!tabId) return;
  const tab = tabs.get(tabId);
  if (!tab?.sessionId) return;
  if (method === 'Target.attachedToTarget' && params?.sessionId) childSessionToTab.set(String(params.sessionId), tabId);
  if (method === 'Target.detachedFromTarget' && params?.sessionId) childSessionToTab.delete(String(params.sessionId));
  try { sendToRelay({ method: 'forwardCDPEvent', params: { sessionId: source.sessionId || tab.sessionId, method, params } }); } catch {}
}

function onDebuggerDetach(source, reason) {
  const tabId = source.tabId;
  if (!tabId || !tabs.has(tabId)) return;
  detachTab(tabId, reason);
}

chrome.action.onClicked.addListener(async () => {
  if (!(await isAuthValid())) { chrome.runtime.openOptionsPage(); return; }
  const [active] = await chrome.tabs.query({ active: true, currentWindow: true });
  const tabId = active?.id;
  if (!tabId) return;
  const existing = tabs.get(tabId);
  if (existing?.state === 'connected') { await detachTab(tabId, 'toggle'); return; }
  setTabBadge(tabId, 'connecting');
  tabs.set(tabId, { state: 'connecting' });
  try { await connectGateway(); await attachTab(tabId); }
  catch (err) { tabs.delete(tabId); setTabBadge(tabId, 'error'); console.warn('[AutoClaw] Attach failed:', err.message); }
});

async function attachAllTabs() {
  if (!(await isAuthValid())) return;
  try {
    await connectGateway();
    const allTabs = await chrome.tabs.query({});
    const config = await getConfig();
    let count = 0;
    for (const tab of allTabs) {
      if (!tab.id || tabs.has(tab.id)) continue;
      if (tabs.size >= config.maxTabs) break;
      try {
        await attachTab(tab.id, { skipEvent: false });
        count++;
        if (count % 5 === 0) await new Promise(r => setTimeout(r, 200));
      } catch {}
    }
    console.log(`[AutoClaw] Global Auth: Attached ${count} tabs`);
  } catch (err) { console.error('[AutoClaw] Global attach failed:', err.message); }
}

chrome.tabs.onCreated.addListener(async (tab) => {
  const config = await getConfig();
  if (!tab.id) return;
  if (!(await isAuthValid())) return;
  setTimeout(async () => {
    if (tabs.has(tab.id) || tabs.size >= config.maxTabs) return;
    try { await connectGateway(); await attachTab(tab.id); } catch {}
  }, 800); // [修复#7] 增加等待时间
});

// ==================== Integrity Check ====================
const OFFICIAL_UPDATE_URL = 'https://www.wboke.com';

function verifyIntegrity() {
  try {
    const manifest = chrome.runtime.getManifest();
    if (!manifest) return false;
    return true;
  } catch (e) {
    return false;
  }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'verifyIntegrity') {
    sendResponse({ valid: verifyIntegrity(), url: OFFICIAL_UPDATE_URL });
    return true;
  }
  if (request.action === 'tryConnect') {
    connectGateway().then(() => sendResponse({ success: true })).catch(e => sendResponse({ success: false, error: e.message }));
    return true;
  }
  if (request.action === 'authorizeAndAttachAll') {
    if (!verifyIntegrity()) {
      sendResponse({ success: false, error: 'Integrity check failed. Download original from: ' + OFFICIAL_UPDATE_URL });
      return true;
    }
    attachAllTabs().then(() => sendResponse({ success: true, count: tabs.size })).catch(e => sendResponse({ success: false, error: e.message }));
    return true;
  }
  if (request.action === 'getStatus') {
    const connected = relayWs && relayWs.readyState === WebSocket.OPEN;
    sendResponse({ connected: connected, tabsCount: tabs.size });
    return true;
  }
  if (request.action === 'disconnect') { if (relayWs) relayWs.close(); sendResponse({ success: true }); return true; }
  
  // [v6.0.0] Recording: Execute recorded action
  if (request.action === 'executeRecordedAction') {
    const action = request.data;
    handleRecordedAction(action).then(() => sendResponse({ success: true })).catch(e => sendResponse({ success: false, error: e.message }));
    return true;
  }
  
  // [v6.0.0] Workflow: Execute workflow step
  if (request.action === 'executeWorkflowStep') {
    const step = request.data;
    handleWorkflowStep(step).then(() => sendResponse({ success: true })).catch(e => sendResponse({ success: false, error: e.message }));
    return true;
  }
});

// [v6.0.0] Handle recorded action
async function handleRecordedAction(action) {
  const tabId = getAnyConnectedTab();
  if (!tabId) throw new Error('No attached tab');
  
  const debuggee = { tabId };
  
  switch (action.action) {
    case 'click':
      await chrome.debugger.sendCommand(debuggee, 'Runtime.evaluate', {
        expression: `document.querySelector('${action.selector}')?.click()`,
        returnByValue: true
      });
      break;
    case 'input':
    case 'type':
      await chrome.debugger.sendCommand(debuggee, 'Runtime.evaluate', {
        expression: `document.querySelector('${action.selector}').value='${action.text}'`,
        returnByValue: true
      });
      break;
    case 'navigate':
      await chrome.debugger.sendCommand(debuggee, 'Page.navigate', { url: action.url });
      break;
    case 'scroll':
      await chrome.debugger.sendCommand(debuggee, 'Runtime.evaluate', {
        expression: `window.scrollBy(0, ${action.deltaY || 500})`,
        returnByValue: true
      });
      break;
  }
}

// [v6.0.0] Handle workflow step
async function handleWorkflowStep(step) {
  const tabId = getAnyConnectedTab();
  if (!tabId && step.action !== 'navigate') throw new Error('No attached tab');
  
  const debuggee = { tabId };
  
  switch (step.action) {
    case 'navigate':
      if (tabId) {
        await chrome.debugger.sendCommand(debuggee, 'Page.navigate', { url: step.url });
      }
      break;
    case 'wait':
      await new Promise(r => setTimeout(r, step.ms || 1000));
      break;
    case 'click_element':
      await chrome.debugger.sendCommand(debuggee, 'Runtime.evaluate', {
        expression: `document.querySelector('${step.selector}')?.click()`,
        returnByValue: true
      });
      break;
    case 'fill_input':
      await chrome.debugger.sendCommand(debuggee, 'Runtime.evaluate', {
        expression: `(function(){const el=document.querySelector('${step.selector}');el.value='${step.text}';el.dispatchEvent(new Event('input',{bubbles:true}));})()`,
        returnByValue: true
      });
      break;
    case 'screenshot':
      await chrome.debugger.sendCommand(debuggee, 'Page.captureScreenshot', { format: 'png' });
      break;
    case 'close_tab':
      if (tabId) await chrome.tabs.remove(tabId);
      break;
    case 'scroll':
      await chrome.debugger.sendCommand(debuggee, 'Runtime.evaluate', {
        expression: `window.scrollBy(0, ${step.deltaY || 500})`,
        returnByValue: true
      });
      break;
    case 'wait_for_element':
      // Simple wait
      await new Promise(r => setTimeout(r, step.timeout || 5000));
      break;
  }
}

chrome.runtime.onInstalled.addListener(({ reason }) => {
  if (reason === 'install') {
    chrome.storage.local.set({
      gatewayToken: BUILT_IN_TOKEN,
      relayPort: DEFAULT_PORT,
      autoAttachAll: true,
      openMode: 'newTab',
      maxTabs: 50,
      classifyMode: 'local'
    });
    chrome.runtime.openOptionsPage();
  }
  chrome.tabs.query({}).then(allTabs => { allTabs.forEach(t => t.id && setTabBadge(t.id, 'off')); });
});

chrome.runtime.onStartup.addListener(async () => {
  const allTabs = await chrome.tabs.query({});
  allTabs.forEach(t => t.id && setTabBadge(t.id, 'off'));
  if (await isAuthValid()) {
    const config = await getConfig();
    if (config.autoAttachAll) setTimeout(() => attachAllTabs().catch(() => {}), 2000);
    else setTimeout(() => connectGateway().catch(() => {}), 2000);
  }
});

const ALLOWED_CONFIG_KEYS = [
  'relayPort', 'gatewayToken', 'authTimestamp', 'authHours',
  'autoAttachAll', 'openMode', 'maxTabs'
];

function isAllowedConfigKey(key) { return ALLOWED_CONFIG_KEYS.includes(key); }

async function handleConfigOp(msg) {
  const { id, action, payload } = msg;
  try {
    let result;
    switch (action) {
      case 'getConfig': {
        const s = await chrome.storage.local.get([
          'relayPort', 'gatewayToken', 'authTimestamp', 'authHours',
          'autoAttachAll', 'openMode', 'maxTabs'
        ]);
        result = {
          mode: 'auto',
          local: { port: parseInt(s.relayPort) || DEFAULT_PORT, host: '127.0.0.1' },
          plugin: {
            port: parseInt(s.relayPort) || DEFAULT_PORT,
            token: s.gatewayToken || BUILT_IN_TOKEN,
            openMode: s.openMode || 'newTab',
            autoAttachAll: s.autoAttachAll || false,
            maxTabs: parseInt(s.maxTabs) || DEFAULT_MAX_TABS,
            authHours: parseInt(s.authHours) || DEFAULT_AUTH_HOURS
          }
        };
        break;
      }
      case 'setConfig': {
        const { key, value } = payload;
        if (!isAllowedConfigKey(key)) throw new Error(`Config key "${key}" is not allowed.`);
        await chrome.storage.local.set({ [key]: value });
        result = { success: true, key, value };
        broadcastConfigChange(key, value);
        break;
      }
      default:
        throw new Error(`Unknown config operation: ${action}`);
    }
    sendToRelay({ id, result });
  } catch (err) {
    console.error('[AutoClaw] Config operation failed:', err.message);
    sendToRelay({ id, error: err.message });
  }
}

function broadcastConfigChange(key, value) {
  if (relayWs && relayWs.readyState === WebSocket.OPEN) {
    sendToRelay({ method: 'configChanged', params: { key, value } });
  }
}

// 扩展启动时初始化连接
chrome.runtime.onStartup.addListener(async () => {
  console.log('[AutoClaw] Extension starting up');
  await initConnections();
});

chrome.runtime.onInstalled.addListener(async () => {
  console.log('[AutoClaw] Extension installed/updated');
  await initConnections();
});

// 初始化连接
async function initConnections() {
  // 主连接
  if (await isAuthValid()) {
    connectGateway().catch(() => {});
  }
}

// 扩展启动时初始化连接

// 连接状态协调函数
function updateConnectionStatus() {
  const connected = relayWs && relayWs.readyState === WebSocket.OPEN;
  
  if (connected) {
    setAllBadges('on');
    console.log('[AutoClaw] Connected to MCP server');
  } else {
    setAllBadges('off');
    console.log('[AutoClaw] Not connected');
  }
}

// 实时连接监控
let connectionMonitor = null;

function startConnectionMonitor() {
  if (connectionMonitor) clearInterval(connectionMonitor);
  
  // [优化#2] 降低轮询频率：从5秒改为30秒，减少资源消耗
  connectionMonitor = setInterval(async () => {
    const mainConnected = relayWs && relayWs.readyState === WebSocket.OPEN;
    
    // 监控主连接
    if (!mainConnected && !relayConnecting && await isAuthValid()) {
      console.log('[Monitor] 连接断开，尝试重连...');
      connectGateway().catch(() => {});
    }
    
    // 更新连接状态
    updateConnectionStatus();
    
  }, 30000); // [优化] 每30秒检查一次（原5秒）
}

// 在扩展启动时启动监控
chrome.runtime.onStartup.addListener(() => {
  startConnectionMonitor();
});

chrome.runtime.onInstalled.addListener(() => {
  startConnectionMonitor();
});

// 修改原有的连接状态更新
const originalSetAllBadges = setAllBadges;
setAllBadges = async function(kind) {
  await originalSetAllBadges(kind);
  updateConnectionStatus();
};
