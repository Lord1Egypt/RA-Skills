// AutoClaw popup.js v6.1.0
// Features: Debug Panel + Operation Recording + Workflow Templates + Element Picker

// Workflow Templates
const WORKFLOW_TEMPLATES = [
  {
    id: 'douyin_like',
    name: '抖音点赞',
    nameEn: 'Douyin Like',
    description: '自动点赞视频',
    descriptionEn: 'Auto-like videos',
    steps: [
      { action: 'navigate', url: 'https://www.douyin.com' },
      { action: 'wait', ms: 2000 },
      { action: 'scroll', deltaY: 500 },
      { action: 'click_element', selector: '.like-btn' }
    ]
  },
  {
    id: 'batch_screenshot',
    name: '批量截图',
    nameEn: 'Batch Screenshot',
    description: '批量截取多页面',
    descriptionEn: 'Screenshot multiple pages',
    steps: [
      { action: 'navigate', url: '' },
      { action: 'wait', ms: 1500 },
      { action: 'screenshot', fullPage: false },
      { action: 'close_tab' }
    ]
  },
  {
    id: 'auto_signin',
    name: '自动签到',
    nameEn: 'Auto Sign-in',
    description: '网站自动签到',
    descriptionEn: 'Auto sign-in for websites',
    steps: [
      { action: 'navigate', url: '' },
      { action: 'wait_for_element', selector: '.signin-btn', timeout: 5000 },
      { action: 'click_element', selector: '.signin-btn' }
    ]
  },
  {
    id: 'form_fill',
    name: '表单填写',
    nameEn: 'Form Fill',
    description: '自动填写表单',
    descriptionEn: 'Auto-fill forms',
    steps: [
      { action: 'navigate', url: '' },
      { action: 'fill_input', selector: 'input[name="username"]', text: '{{username}}' },
      { action: 'fill_input', selector: 'input[name="password"]', text: '{{password}}' },
      { action: 'click_element', selector: 'button[type="submit"]' }
    ]
  }
];

document.addEventListener('DOMContentLoaded', async () => {
  // Elements
  const statusDot = document.getElementById('statusDot');
  const statusText = document.getElementById('statusText');
  const tabsCount = document.getElementById('tabsCount');
  const attachAllBtn = document.getElementById('attachAllBtn');
  const disconnectBtn = document.getElementById('disconnectBtn');
  const openOptions = document.getElementById('openOptions');
  const content = document.getElementById('content');
  const loading = document.getElementById('loading');
  const openNewTab = document.getElementById('openNewTab');
  const modalOverlay = document.getElementById('modalOverlay');
  const modalIcon = document.getElementById('modalIcon');
  const modalTitle = document.getElementById('modalTitle');
  const modalMessage = document.getElementById('modalMessage');
  const modalBtn = document.getElementById('modalBtn');

  // New elements for v6.0.0
  const debugPanel = document.getElementById('debugPanel');
  const debugLogs = document.getElementById('debugLogs');
  const clearLogsBtn = document.getElementById('clearLogs');
  const recordBtn = document.getElementById('recordBtn');
  const stopRecordBtn = document.getElementById('stopRecordBtn');
  const recordStatus = document.getElementById('recordStatus');
  const recordedSteps = document.getElementById('recordedSteps');
  const playRecordBtn = document.getElementById('playRecordBtn');
  const templateList = document.getElementById('templateList');
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  // Recording state
  let isRecording = false;
  let recordedActions = [];
  let currentTab = 'main';

  // Tab switching
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.dataset.tab;
      currentTab = tabId;
      tabButtons.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    });
  });

  // Logging function
  function addLog(type, message, data = null) {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry log-${type}`;
    logEntry.innerHTML = `
      <span class="log-time">${timestamp}</span>
      <span class="log-type">[${type.toUpperCase()}]</span>
      <span class="log-message">${message}</span>
      ${data ? `<span class="log-data">${JSON.stringify(data).substring(0, 50)}</span>` : ''}
    `;
    if (debugLogs) {
      debugLogs.insertBefore(logEntry, debugLogs.firstChild);
      
      // Keep only last 100 logs
      while (debugLogs.children.length > 100) {
        debugLogs.removeChild(debugLogs.lastChild);
      }
    }
  }

  // Clear logs
  clearLogsBtn?.addEventListener('click', () => {
    if (debugLogs) debugLogs.innerHTML = '';
    addLog('info', 'Logs cleared');
  });

  // Modal functions
  function showModal(icon, title, message, type = 'success') {
    modalIcon.textContent = icon;
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    modalBtn.className = 'modal-btn ' + type;
    modalOverlay.classList.add('show');
  }

  modalBtn.addEventListener('click', () => {
    modalOverlay.classList.remove('show');
  });

  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
      modalOverlay.classList.remove('show');
    }
  });

  function showLoading(show) {
    content.style.display = show ? 'none' : 'block';
    loading.classList.toggle('active', show);
  }

  function updateStatus(connected, count) {
    tabsCount.textContent = count;
    if (connected) {
      statusDot.className = 'status-dot connected';
      statusText.textContent = 'Connected';
    } else {
      statusDot.className = 'status-dot disconnected';
      statusText.textContent = 'Not connected';
    }
  }

  // ===== ELEMENT PICKER =====
  
  let isPickerActive = false;
  const pickerBtn = document.getElementById('pickerBtn');
  
  pickerBtn?.addEventListener('click', async () => {
    if (!pickerBtn) return;
    
    if (isPickerActive) {
      // Deactivate picker
      isPickerActive = false;
      pickerBtn.textContent = '🎯 Element Picker';
      pickerBtn.classList.remove('active');
      
      // Send message to deactivate
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tabs[0]?.id) {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'deactivatePicker' });
      }
      
      addLog('picker', 'Element picker deactivated');
      return;
    }
    
    // Activate picker
    isPickerActive = true;
    if (pickerBtn) {
      pickerBtn.textContent = '⏹ Stop Picker';
      pickerBtn.classList.add('active');
    }
    
    addLog('picker', 'Element picker activated - click on any element');
    
    // Send message to activate
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tabs[0]?.id) {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'activatePicker' });
    }
  });
  
  // Listen for selected element from content script
  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === 'elementSelected') {
      const selector = msg.selector;
      isPickerActive = false;
      if (pickerBtn) {
        pickerBtn.textContent = '🎯 Element Picker';
        pickerBtn.classList.remove('active');
      }
      
      // Copy to clipboard
      navigator.clipboard.writeText(selector).then(() => {
        addLog('picker', `Selector copied: ${selector}`);
        showModal('✅', 'Selector Copied!', `CSS: ${selector}`, 'success');
      }).catch(() => {
        addLog('picker', `Selector: ${selector}`);
        showModal('📋', 'Selector', `CSS: ${selector}`, 'info');
      });
    }
  });

  async function checkStatus() {
    try {
      const response = await chrome.runtime.sendMessage({ action: 'getStatus' });
      updateStatus(response?.connected ?? false, response?.tabsCount ?? 0);
    } catch (e) {
      updateStatus(false, 0);
    }
  }

  // ===== OPERATION RECORDING =====

  // Start recording
  recordBtn?.addEventListener('click', async () => {
    if (isRecording) return;
    
    isRecording = true;
    recordedActions = [];
    if (recordedSteps) recordedSteps.innerHTML = '<div class="step-item">Recording started...</div>';
    if (recordBtn) recordBtn.style.display = 'none';
    if (stopRecordBtn) stopRecordBtn.style.display = 'inline-flex';
    if (recordStatus) {
      recordStatus.textContent = '● Recording';
      recordStatus.className = 'record-status recording';
    }
    
    addLog('record', 'Started recording operations');
    
    // Listen for operations from background
    chrome.runtime.onMessage.addListener((msg) => {
      if (msg.type === 'operation_record') {
        recordedActions.push(msg.data);
        updateRecordedSteps();
        addLog('record', `Recorded: ${msg.data.action}`, msg.data);
      }
    });
    
    showModal('🎬', 'Recording', 'Start performing operations on the page. Click "Stop" when done.', 'info');
  });

  // Stop recording
  stopRecordBtn?.addEventListener('click', () => {
    isRecording = false;
    if (recordBtn) recordBtn.style.display = 'inline-flex';
    if (stopRecordBtn) stopRecordBtn.style.display = 'none';
    if (recordStatus) {
      recordStatus.textContent = '○ Not recording';
      recordStatus.className = 'record-status';
    }
    
    addLog('record', `Stopped recording. Total: ${recordedActions.length} operations`);
    showModal('✅', 'Recorded!', `Recorded ${recordedActions.length} operations. Click "Play" to replay.`, 'success');
  });

  // Update recorded steps display
  function updateRecordedSteps() {
    if (recordedSteps) {
      recordedSteps.innerHTML = recordedActions.map((action, index) => 
        `<div class="step-item">${index + 1}. ${action.action} ${action.selector ? `- ${action.selector}` : ''}</div>`
      ).join('');
    }
  }

  // Play recorded operations
  playRecordBtn?.addEventListener('click', async () => {
    if (recordedActions.length === 0) {
      showModal('⚠️', 'No Operations', 'Please record some operations first.', 'error');
      return;
    }
    
    addLog('play', 'Starting playback...');
    showModal('▶️', 'Playing', `Executing ${recordedActions.length} operations...`, 'info');
    
    for (const action of recordedActions) {
      try {
        await chrome.runtime.sendMessage({
          action: 'executeRecordedAction',
          data: action
        });
        addLog('play', `Executed: ${action.action}`);
        await new Promise(r => setTimeout(r, 500)); // Delay between actions
      } catch (e) {
        addLog('error', `Failed: ${action.action}`, e.message);
      }
    }
    
    addLog('play', 'Playback completed');
    showModal('✅', 'Done!', 'All operations executed.', 'success');
  });

  // ===== WORKFLOW TEMPLATES =====

  // Render template list
  function renderTemplates() {
    if (!templateList) return;
    
    templateList.innerHTML = WORKFLOW_TEMPLATES.map(template => `
      <div class="template-item" data-id="${template.id}">
        <div class="template-name">${template.name} <span>(${template.nameEn})</span></div>
        <div class="template-desc">${template.description}</div>
        <div class="template-actions">
          <button class="template-btn run" data-id="${template.id}">▶️ Run</button>
        </div>
      </div>
    `).join('');
    
    // Add click handlers
    templateList.querySelectorAll('.template-btn.run').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const templateId = e.target.dataset.id;
        const template = WORKFLOW_TEMPLATES.find(t => t.id === templateId);
        if (!template) return;
        
        addLog('workflow', `Starting workflow: ${template.name}`);
        
        // Show input dialog for URL if needed
        let url = template.steps[0]?.url || '';
        if (url === '' && template.steps.some(s => s.url !== undefined)) {
          url = prompt('请输入目标URL / Enter target URL:') || '';
        }
        
        showModal('⚡', 'Running', `Executing workflow: ${template.name}`, 'info');
        
        for (const step of template.steps) {
          try {
            // Replace {{username}} etc with actual values if needed
            let stepData = { ...step };
            if (stepData.url === '') stepData.url = url;
            
            await chrome.runtime.sendMessage({
              action: 'executeWorkflowStep',
              data: stepData
            });
            
            addLog('workflow', `Step: ${step.action}`);
            
            if (step.ms) {
              await new Promise(r => setTimeout(r, step.ms));
            }
          } catch (e) {
            addLog('error', `Step failed: ${step.action}`, e.message);
          }
        }
        
        showModal('✅', 'Done!', `Workflow "${template.name}" completed!`, 'success');
        addLog('workflow', `Workflow completed: ${template.name}`);
      });
    });
  }

  renderTemplates();

  // ===== MAIN BUTTONS =====

  attachAllBtn.addEventListener('click', async () => {
    showLoading(true);
    addLog('info', 'Attempting to attach all tabs');
    try {
      const response = await chrome.runtime.sendMessage({ action: 'authorizeAndAttachAll' });
      if (response.success) {
        updateStatus(true, response.count);
        addLog('success', `Attached ${response.count} tabs`);
        showModal('🎉', 'Success!', `Attached ${response.count} tabs`, 'success');
      } else {
        addLog('error', 'Attach failed', response.error);
        showModal('❌', 'Failed', response.error || 'Unknown error', 'error');
      }
    } catch (e) {
      addLog('error', 'Attach error', e.message);
      showModal('❌', 'Error', e.message, 'error');
    }
    showLoading(false);
  });

  disconnectBtn.addEventListener('click', async () => {
    try {
      await chrome.runtime.sendMessage({ action: 'disconnect' });
      updateStatus(false, 0);
      addLog('info', 'Disconnected');
      showModal('👋', 'Disconnected', 'Connection closed', 'success');
    } catch (e) {
      showModal('❌', 'Error', e.message, 'error');
    }
  });

  openOptions.addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });

  openNewTab.addEventListener('click', (e) => {
    e.preventDefault();
    chrome.tabs.create({ url: 'https://www.wboke.com', active: false });
  });

  // Initial status check
  await checkStatus();
  addLog('info', 'AutoClaw popup loaded');

  // [优化] 降低轮询频率
  setInterval(checkStatus, 10000);

  window.addEventListener('unload', () => {
    clearInterval(checkStatus);
  });
});
