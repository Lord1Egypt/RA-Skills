// AutoClaw options.js - Settings Page
const DEFAULT_PORT = 30000;
const BUILT_IN_TOKEN = 'autoclaw_builtin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs';
const OFFICIAL_URL = 'https://www.wboke.com';

// Translations
const translations = {
  zh: {
    title: '疯狂小龙虾',
    portModeTitle: '📡 连接模式',
    portTipTitle: '💡 模式说明',
    portTip18792: '18792 - 简单模式，直连OpenClaw Gateway。仅支持基础网页操作，无书签管理和高级功能。',
    portTip30000: '30000 - ⭐推荐⭐ 增强模式，完整MCP支持，深度浏览器控制、书签管理、截图、JavaScript执行等。',
    connTitle: '🔌 连接状态',
    statusText: '未连接',
    portInputLabel: 'MCP/Gateway 端口',
    tokenLabel: '认证 Token',
    authTitle: '⏰ 授权设置',
    authHoursLabel: '授权有效期（小时）',
    authHoursHint: '授权有效期。过期后需要重新保存设置以续期。',
    autoTitle: '⚡ 自动化设置',
    autoAttachLabel: '自动接管所有标签页',
    autoAttachWarning: '⚠️ 风险提示：开启后，AI智能体将对安装此插件的所有浏览器标签页具有完全控制权限。包括读取页面内容、填写表单、点击元素，执行JavaScript等。仅在您信任AI并了解风险时启用。',
    openModeLabel: '打开链接方式',
    openModeNewLabel: '新标签页',
    openModeCurrentLabel: '当前页',
    maxTabsLabel: '最大接管标签数',
    saveBtn: '保存设置',
    testBtn: '测试连接',
    attachAllBtn: '立即接管所有标签页',
    infoTitle: 'ℹ️ 连接信息',
    download: '下载更新',
    days: '天',
    hours: '时',
    mins: '分',
    secs: '秒',
    classifyTitle: '🗂️ 书签分类模式',
    classifyModeLabel: '分类模式',
    classifyLocalLabel: '本地分析（隐私优先）',
    classifyCloudLabel: '云端数据库（快速·协作）',
    dbUrlLabel: '数据库 API 地址',
    apiKeyLabel: 'API 密钥',
    testDbBtnText: '测试连接',
    dbStatusOk: '✓ 连接成功',
    dbStatusFail: '✗ 连接失败',
    dbStatusTesting: '测试中...'
  },
  en: {
    title: 'AUTOCLAW',
    portModeTitle: '📡 Connection Mode',
    portTipTitle: '💡 Mode Description',
    portTip18792: '18792 - Simple mode - Direct connection to OpenClaw Gateway. Basic page operations only, no bookmark management or advanced features.',
    portTip30000: '30000 - ⭐ Recommended ⭐ Enhanced mode - Full MCP support with deep browser control, bookmark management, screenshots, JavaScript execution, and more.',
    connTitle: '🔌 Connection Status',
    statusText: 'Not connected',
    portInputLabel: 'MCP/Gateway Port',
    tokenLabel: 'Auth Token',
    authTitle: '⏰ Authorization',
    authHoursLabel: 'Authorization Validity Period',
    authHoursHint: 'How long the authorization remains valid. After expiration, you need to save settings again to re-authorize.',
    autoTitle: '⚡ Automation Settings',
    autoAttachLabel: 'Auto Attach All Tabs',
    autoAttachWarning: '⚠️ Risk Warning: When enabled, the AI agent will have full control over ALL tabs in your browser where this extension is installed. This includes reading page content, filling forms, clicking elements, executing JavaScript, and more. Only enable if you trust the AI and understand the risks.',
    openModeLabel: 'Open Link Mode',
    openModeNewLabel: 'New Tab',
    openModeCurrentLabel: 'Current Tab',
    maxTabsLabel: 'Max Tabs',
    saveBtn: 'Save Settings',
    testBtn: 'Test Connection',
    attachAllBtn: 'Attach All Tabs',
    infoTitle: 'ℹ️ Connection Info',
    download: 'Download',
    days: 'Days',
    hours: 'Hours',
    mins: 'Mins',
    secs: 'Secs',
    classifyTitle: '🗂️ Bookmark Classification',
    classifyModeLabel: 'Classification Mode',
    classifyLocalLabel: 'Local Analysis (Privacy)',
    classifyCloudLabel: 'Cloud Database (Fast)',
    dbUrlLabel: 'Database API URL',
    apiKeyLabel: 'API Key',
    testDbBtnText: 'Test Connection',
    dbStatusOk: '✓ Connected',
    dbStatusFail: '✗ Failed',
    dbStatusTesting: 'Testing...'
  }
};

let currentLang = localStorage.getItem('autoclaw_lang') || 'en';

function checkIntegrity() {
  const downloadBtn = document.getElementById('downloadBtn');
  if (!downloadBtn) return false;
  const href = downloadBtn.getAttribute('href');
  if (!href || href !== OFFICIAL_URL) return false;
  const manifestLink = document.querySelector('link[rel="manifest"]');
  if (!manifestLink) return false;
  return true;
}

function verifyAndRun(callback) {
  if (!checkIntegrity()) {
    alert('Integrity check failed. Please download the original version from: ' + OFFICIAL_URL);
    return false;
  }
  return callback ? callback() : true;
}

function toggleLang() {
  currentLang = currentLang === 'zh' ? 'en' : 'zh';
  localStorage.setItem('autoclaw_lang', currentLang);
  applyLang();
}

function applyLang() {
  const t = translations[currentLang];
  const logo = '<span style="font-size:28px;">🦞</span> ';
  document.getElementById('title').innerHTML = logo + t.title;
  document.getElementById('portModeTitle').textContent = t.portModeTitle;
  document.getElementById('portTipTitle').textContent = t.portTipTitle;
  document.getElementById('connTitle').textContent = t.connTitle;
  // 不覆盖连接状态文本，保留当前状态
  document.getElementById('portInputLabel').textContent = t.portInputLabel;
  document.getElementById('tokenLabel').textContent = t.tokenLabel;
  document.getElementById('authTitle').textContent = t.authTitle;
  document.getElementById('autoTitle').textContent = t.autoTitle;
  document.getElementById('autoAttachLabel').textContent = t.autoAttachLabel;
  document.getElementById('openModeLabel').textContent = t.openModeLabel;
  document.getElementById('openModeNewLabel').textContent = t.openModeNewLabel;
  document.getElementById('openModeCurrentLabel').textContent = t.openModeCurrentLabel;
  document.getElementById('maxTabsLabel').textContent = t.maxTabsLabel;
  document.getElementById('saveBtn').querySelector('.lang-text').textContent = t.saveBtn;
  if (document.getElementById('testBtn')) {
    document.getElementById('testBtn').querySelector('.lang-text').textContent = t.testBtn;
  }
  document.getElementById('attachAllBtn').querySelector('.lang-text').textContent = t.attachAllBtn;
  document.getElementById('infoTitle').textContent = t.infoTitle;
  document.getElementById('downloadBtn').querySelector('.lang-text').textContent = t.download;

  // Bookmark classification translations
  if (document.getElementById('classifyTitle')) document.getElementById('classifyTitle').textContent = t.classifyTitle;
  if (document.getElementById('classifyModeLabel')) document.getElementById('classifyModeLabel').textContent = t.classifyModeLabel;
  if (document.getElementById('classifyLocalLabel')) document.getElementById('classifyLocalLabel').textContent = t.classifyLocalLabel;
  if (document.getElementById('classifyCloudLabel')) document.getElementById('classifyCloudLabel').textContent = t.classifyCloudLabel;
  if (document.getElementById('dbUrlLabel')) document.getElementById('dbUrlLabel').textContent = t.dbUrlLabel;
  if (document.getElementById('apiKeyLabel')) document.getElementById('apiKeyLabel').textContent = t.apiKeyLabel;
  if (document.getElementById('testDbBtnText')) document.getElementById('testDbBtnText').textContent = t.testDbBtnText;



  document.querySelectorAll('.lang-en').forEach(el => el.style.display = currentLang === 'en' ? '' : 'none');
  document.querySelectorAll('.lang-zh').forEach(el => el.style.display = currentLang === 'zh' ? '' : 'none');
}



// Initialize on load
document.addEventListener('DOMContentLoaded', async () => {
  // Setup language toggle
  const langSwitchBtn = document.getElementById('langSwitchBtn');
  if (langSwitchBtn) {
    langSwitchBtn.addEventListener('click', toggleLang);
  }

  // Get elements
  const relayPort = document.getElementById('relayPort');
  const autoAttachAll = document.getElementById('autoAttachAll');
  const openModeNew = document.getElementById('openModeNew');
  const openModeCurrent = document.getElementById('openModeCurrent');
  const maxTabs = document.getElementById('maxTabs');
  const saveBtn = document.getElementById('saveBtn');
  const testBtn = document.getElementById('testBtn');
  const attachAllBtn = document.getElementById('attachAllBtn');
  const successMsg = document.getElementById('successMsg');
  const tokenDisplay = document.getElementById('tokenDisplay');
  const connectionStatus = document.getElementById('connectionStatus');
  const statusText = document.getElementById('statusText');
  const wsDisplay = document.getElementById('wsDisplay');
  const classifyLocal = document.getElementById('classifyLocal');
  const classifyCloud = document.getElementById('classifyCloud');
  const dbConfigGroup = document.getElementById('dbConfigGroup');
  const classifyDbUrl = document.getElementById('classifyDbUrl');
  const classifyApiKey = document.getElementById('classifyApiKey');
  const testDbBtn = document.getElementById('testDbBtn');
  const dbStatus = document.getElementById('dbStatus');

  // Apply language on load
  applyLang();

  async function loadSettings() {
    const s = await chrome.storage.local.get([
      'relayPort', 'gatewayToken',
      'autoAttachAll', 'openMode', 'maxTabs',
      'classifyMode', 'classifyDbUrl', 'classifyApiKey'
    ]);

    // 端口设置
    relayPort.value = s.relayPort || DEFAULT_PORT;
    
    // 加载保存的token到输入框
    const savedToken = s.gatewayToken || BUILT_IN_TOKEN;
    document.getElementById('customToken').value = savedToken === BUILT_IN_TOKEN ? '' : savedToken;
    
    // 显示token（隐藏中间部分）
    if (savedToken.length > 20) {
      tokenDisplay.textContent = savedToken.substring(0, 12) + '***' + savedToken.substring(savedToken.length - 8);
    } else {
      tokenDisplay.textContent = savedToken;
    }

    // 默认勾选Auto Attach All Tabs
    autoAttachAll.checked = s.autoAttachAll !== false;
    maxTabs.value = s.maxTabs || 50;

    // Bookmark Classification Settings
    const classifyMode = s.classifyMode || 'local';
    if (classifyMode === 'cloud') {
      classifyCloud.checked = true;
      document.getElementById('dbConfigGroup').style.display = 'block';
    } else {
      classifyLocal.checked = true;
      document.getElementById('dbConfigGroup').style.display = 'none';
    }
    document.getElementById('classifyDbUrl').value = s.classifyDbUrl || 'https://www.mark.wboke.com';
    document.getElementById('classifyApiKey').value = s.classifyApiKey || '';

    // 默认选择new tab
    if (s.openMode === 'currentTab') {
      openModeCurrent.checked = true;
    } else {
      openModeNew.checked = true;
    }

    // Update WebSocket display
    const port = s.relayPort || DEFAULT_PORT;
    wsDisplay.textContent = `ws://127.0.0.1:${port}/extension`;

    await checkConnection();
  }

  async function checkConnection() {
    try {
      const port = parseInt(relayPort.value) || DEFAULT_PORT;
      const response = await chrome.runtime.sendMessage({ 
        action: 'getStatus',
        port: port 
      });
      if (response && response.connected) {
        connectionStatus.className = 'status-indicator connected';
        statusText.textContent = 'Connected';
      } else {
        connectionStatus.className = 'status-indicator disconnected';
        statusText.textContent = 'Not connected';
      }
    } catch (e) {
      connectionStatus.className = 'status-indicator disconnected';
      statusText.textContent = 'Check failed';
    }
  }

  async function saveSettings() {
    if (!verifyAndRun()) return;

    // 简化为单一端口配置，用户可自定义
    const port = parseInt(relayPort.value) || DEFAULT_PORT;
    const customToken = document.getElementById('customToken').value.trim();
    const token = customToken || BUILT_IN_TOKEN; // 用户自定义或默认
    const tabs = parseInt(maxTabs.value) || 50;
    const openMode = openModeNew.checked ? 'newTab' : 'currentTab';
    const classifyMode = classifyCloud.checked ? 'cloud' : 'local';

    await chrome.storage.local.set({
      relayPort: port,
      gatewayToken: token, // 保存用户自定义的token
      autoAttachAll: autoAttachAll.checked,
      openMode: openMode,
      maxTabs: tabs,
      classifyMode: classifyMode,
      classifyDbUrl: classifyDbUrl.value.trim(),
      classifyApiKey: classifyApiKey.value.trim()
    });

    successMsg.classList.add('show');
    setTimeout(() => successMsg.classList.remove('show'), 2000);

    await checkConnection();
  }

  // Event listeners
  saveBtn.addEventListener('click', async () => {
    await saveSettings();
  });

  testBtn.addEventListener('click', async () => {
    if (!verifyAndRun()) return;
    const port = parseInt(relayPort.value) || DEFAULT_PORT;
    const customToken = document.getElementById('customToken').value.trim();
    const token = customToken || BUILT_IN_TOKEN;
    testBtn.disabled = true;
    testBtn.querySelector('.lang-text').textContent = 'Testing...';
    
    try {
      await new Promise((resolve, reject) => {
        const ws = new WebSocket(`ws://127.0.0.1:${port}/extension?token=${encodeURIComponent(token)}`);
        const t = setTimeout(() => { ws.close(); reject(new Error('Connection timeout')); }, 4000);
        ws.onopen = () => { clearTimeout(t); ws.close(); resolve(); };
        ws.onerror = () => { clearTimeout(t); reject(new Error('Connection failed')); };
        ws.onclose = (e) => { if (e.code !== 1000) { clearTimeout(t); reject(new Error(`code=${e.code}`)); } };
      });
      alert(`✓ Connection successful - MCP running on port ${port}`);
    } catch (e) {
      alert(`✗ ${e.message}`);
    } finally {
      testBtn.disabled = false;
      testBtn.querySelector('.lang-text').textContent = translations[currentLang].testBtn;
    }
  });

  attachAllBtn.addEventListener('click', async () => {
    if (!verifyAndRun()) return;
    attachAllBtn.disabled = true;
    attachAllBtn.querySelector('.lang-text').textContent = 'Connecting...';
    try {
      const port = parseInt(relayPort.value) || DEFAULT_PORT;
      const response = await chrome.runtime.sendMessage({ 
        action: 'authorizeAndAttachAll',
        port: port
      });
      if (response && response.success) {
        alert(`Success! Attached ${response.count} tabs`);
        await checkConnection();
      } else {
        alert('Failed: ' + (response?.error || 'Unknown error'));
      }
    } catch (e) {
      alert('Error: ' + e.message);
    }
    attachAllBtn.disabled = false;
    attachAllBtn.querySelector('.lang-text').textContent = translations[currentLang].attachAllBtn;
  });

  // Classification mode toggle
  classifyCloud.addEventListener('change', () => {
    dbConfigGroup.style.display = 'block';
  });
  classifyLocal.addEventListener('change', () => {
    dbConfigGroup.style.display = 'none';
  });

  // Test database connection
  testDbBtn.addEventListener('click', async () => {
    const dbUrl = classifyDbUrl.value.trim();
    const apiKey = classifyApiKey.value.trim();
    if (!dbUrl) {
      dbStatus.textContent = '⚠️ Please enter URL';
      return;
    }
    if (!apiKey) {
      dbStatus.textContent = '⚠️ Please enter API Key';
      return;
    }

    const t = translations[currentLang];
    dbStatus.textContent = t.dbStatusTesting;
    dbStatus.style.color = '#6B7280';
    testDbBtn.disabled = true;

    try {
      const res = await fetch(`${dbUrl}/health`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${apiKey}` },
        signal: AbortSignal.timeout(5000)
      });
      if (res.ok) {
        dbStatus.textContent = t.dbStatusOk;
        dbStatus.style.color = '#059669';
      } else {
        dbStatus.textContent = `${t.dbStatusFail} (${res.status})`;
        dbStatus.style.color = '#DC2626';
      }
    } catch (e) {
      dbStatus.textContent = t.dbStatusFail;
      dbStatus.style.color = '#DC2626';
    } finally {
      testDbBtn.disabled = false;
    }
  });

  // 端口输入框变化时更新显示
  relayPort.addEventListener('change', () => { 
    const port = relayPort.value || DEFAULT_PORT;
    wsDisplay.textContent = `ws://127.0.0.1:${port}/extension`;
    checkConnection(); 
  });

  await loadSettings();
});
