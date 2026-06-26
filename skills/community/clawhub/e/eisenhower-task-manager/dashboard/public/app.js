/**
 * Eisenhower Task Dashboard - Frontend Application
 * Handles UI rendering and WebSocket communication
 * Supports internationalization (i18n)
 */

// Global state
let currentData = null;
let ws = null;
let currentTab = 'matrix';
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

// Drag and drop state
let draggedTask = null;
let draggedSourceQuadrant = null;
let dropIndicator = null;

// Customer project drag and drop state
let draggedCustomerProject = null;
let draggedSourceCustomer = null;

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initFilters();
  initLanguageSwitcher();
  initTerminal();
  connectWebSocket();
  // Initial data load via fetch as fallback
  fetchInitialData();
});

// Terminal State
let terminal = null;
let terminalFitAddon = null;
let terminalWs = null;
let terminalVisible = false;

// Initialize Terminal
function initTerminal() {
  const terminalContainer = document.getElementById('terminalContainer');
  const terminalElement = document.getElementById('terminal');
  const toggleBtn = document.getElementById('terminalToggleBtn');
  const closeBtn = document.getElementById('terminalCloseBtn');
  
  if (!terminalElement || !toggleBtn || !closeBtn) return;
  
  // Toggle button handler
  toggleBtn.addEventListener('click', () => {
    toggleTerminal();
  });
  
  // Close button handler
  closeBtn.addEventListener('click', () => {
    toggleTerminal(false);
  });
  
  // Keyboard shortcut to toggle terminal (Ctrl+` or Cmd+j like VS Code)
  document.addEventListener('keydown', (e) => {
    // Ctrl+` or Cmd+j
    if ((e.ctrlKey && e.key === '`') || (e.metaKey && e.key === 'j')) {
      e.preventDefault();
      toggleTerminal();
    }
  });
  
  // Restore state from localStorage
  const savedState = localStorage.getItem('eisenhower_terminal_visible');
  if (savedState === 'true') {
    toggleTerminal(true);
  }
  
  // Terminal Resize Logic
  initTerminalResizer();
}

function initTerminalResizer() {
  const container = document.getElementById('terminalContainer');
  const resizer = document.getElementById('terminalResizer');
  
  if (!container || !resizer) return;
  
  let isResizing = false;
  let startY;
  let startHeight;
  
  // Also restore saved height if available
  const savedHeight = localStorage.getItem('eisenhower_terminal_height');
  if (savedHeight) {
    container.style.height = `${savedHeight}px`;
  }
  
  // Double click header to maximize/restore
  const header = document.querySelector('.terminal-header');
  let isMaximized = false;
  let preMaxHeight = '';
  
  if (header) {
    header.addEventListener('dblclick', () => {
      if (!isMaximized) {
        preMaxHeight = container.style.height || '30%';
        container.style.height = 'calc(100vh - 60px)';
        isMaximized = true;
      } else {
        container.style.height = preMaxHeight;
        isMaximized = false;
      }
      
      // Save and refit
      setTimeout(() => {
        localStorage.setItem('eisenhower_terminal_height', container.getBoundingClientRect().height);
        if (terminalFitAddon && terminalWs && terminalWs.readyState === WebSocket.OPEN) {
          terminalFitAddon.fit();
          terminalWs.send(JSON.stringify({
            type: 'resize',
            cols: terminal.cols,
            rows: terminal.rows
          }));
        }
      }, 10);
    });
  }
  
  resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    startY = e.clientY;
    startHeight = container.getBoundingClientRect().height;
    
    // Add visual feedback
    resizer.classList.add('active');
    document.body.style.cursor = 'ns-resize';
    
    // Prevent text selection while dragging
    e.preventDefault();
  });
  
  window.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    
    // Calculate new height (drag up = increase height)
    const dy = startY - e.clientY;
    const newHeight = startHeight + dy;
    
    // Let CSS min/max height handle the boundaries, just set the value
    container.style.height = `${newHeight}px`;
    
    // Continually fit the terminal as it resizes
    if (terminalFitAddon) {
      terminalFitAddon.fit();
    }
  });
  
  window.addEventListener('mouseup', () => {
    if (isResizing) {
      isResizing = false;
      resizer.classList.remove('active');
      document.body.style.cursor = '';
      
      // Save final height
      localStorage.setItem('eisenhower_terminal_height', container.getBoundingClientRect().height);
      
      // Do one final precise fit and notify server
      if (terminalFitAddon && terminalWs && terminalWs.readyState === WebSocket.OPEN) {
        terminalFitAddon.fit();
        terminalWs.send(JSON.stringify({
          type: 'resize',
          cols: terminal.cols,
          rows: terminal.rows
        }));
      }
    }
  });
}

function toggleTerminal(show) {
  const terminalContainer = document.getElementById('terminalContainer');
  const toggleBtn = document.getElementById('terminalToggleBtn');
  
  terminalVisible = show !== undefined ? show : !terminalVisible;
  
  // Save state
  localStorage.setItem('eisenhower_terminal_visible', terminalVisible);
  
  if (terminalVisible) {
    terminalContainer.classList.add('show');
    toggleBtn.classList.add('active');
    
    // Lazy initialize terminal
    if (!terminal) {
      setupTerminal();
    } else {
      // Re-fit when shown
      setTimeout(() => {
        terminalFitAddon.fit();
        if (terminalWs && terminalWs.readyState === WebSocket.OPEN) {
          terminalWs.send(JSON.stringify({
            type: 'resize',
            cols: terminal.cols,
            rows: terminal.rows
          }));
          terminal.focus();
        }
      }, 50);
    }
  } else {
    terminalContainer.classList.remove('show');
    toggleBtn.classList.remove('active');
  }
}

function setupTerminal() {
  const terminalElement = document.getElementById('terminal');
  
  terminal = new window.Terminal({
    cursorBlink: true,
    fontFamily: 'Menlo, Monaco, "Courier New", monospace',
    fontSize: 14,
    theme: {
      background: '#000000',
      foreground: '#e6edf3'
    }
  });
  
  terminalFitAddon = new window.FitAddon.FitAddon();
  terminal.loadAddon(terminalFitAddon);
  
  terminal.open(terminalElement);
  
  // Need a small timeout to let the container render before fitting
  setTimeout(() => {
    terminalFitAddon.fit();
    connectTerminalWebSocket();
  }, 10);
  
  // Handle window resize
  window.addEventListener('resize', () => {
    if (terminalVisible && terminalFitAddon) {
      terminalFitAddon.fit();
      if (terminalWs && terminalWs.readyState === WebSocket.OPEN) {
        terminalWs.send(JSON.stringify({
          type: 'resize',
          cols: terminal.cols,
          rows: terminal.rows
        }));
      }
    }
  });
}

function connectTerminalWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/terminal`;
  
  terminalWs = new WebSocket(wsUrl);
  
  terminalWs.onopen = () => {
    console.log('[Terminal] Connected');
    
    // Send initial size
    terminalWs.send(JSON.stringify({
      type: 'resize',
      cols: terminal.cols,
      rows: terminal.rows
    }));
    
    // Hook up terminal input to websocket
    terminal.onData(data => {
      if (terminalWs.readyState === WebSocket.OPEN) {
        terminalWs.send(data);
      }
    });
  };
  
  terminalWs.onmessage = (event) => {
    // Write websocket data to terminal
    if (event.data instanceof Blob) {
      const reader = new FileReader();
      reader.onload = () => {
        terminal.write(reader.result);
      };
      reader.readAsText(event.data);
    } else {
      terminal.write(event.data);
    }
  };
  
  terminalWs.onclose = () => {
    console.log('[Terminal] Disconnected');
    terminal.write('\r\n\x1b[31m[Terminal Connection Closed]\x1b[0m\r\n');
    
    // Try to reconnect if terminal is still visible
    if (terminalVisible) {
      setTimeout(connectTerminalWebSocket, 3000);
    }
  };
  
  terminalWs.onerror = (error) => {
    console.error('[Terminal] Error:', error);
  };
}

// Initialize language switcher
function initLanguageSwitcher() {
  const langBtn = document.getElementById('langBtn');
  const langDropdown = document.getElementById('langDropdown');

  if (!langBtn || !langDropdown) return;

  // Set initial button state based on current language
  updateLangButton(i18n.getLanguage());

  // Toggle dropdown
  langBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    langDropdown.classList.toggle('show');
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', () => {
    langDropdown.classList.remove('show');
  });

  // Language selection
  langDropdown.querySelectorAll('.lang-option').forEach(option => {
    option.addEventListener('click', () => {
      const lang = option.dataset.lang;
      if (i18n.setLanguage(lang)) {
        updateLangButton(lang);
        // Re-render dynamic content
        renderAll();
      }
    });
  });
}

// Update language button display
function updateLangButton(lang) {
  const langBtn = document.getElementById('langBtn');
  const langText = langBtn.querySelector('.lang-text');
  langText.textContent = lang === 'zh-CN' ? '中文' : 'EN';
  langBtn.dataset.current = lang;
}

// Tab switching
function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.dataset.tab;
      currentTab = tabId;

      // Update active states
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    });
  });
}

// Filter buttons
function initFilters() {
  // Customer filters
  const customerFilters = document.querySelectorAll('#customers .filter-btn');
  customerFilters.forEach(btn => {
    btn.addEventListener('click', () => {
      customerFilters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderCustomers(currentData?.customerProjects, btn.dataset.filter);
    });
  });

  // Delegation filters
  const delegationFilters = document.querySelectorAll('#delegation .filter-btn');
  delegationFilters.forEach(btn => {
    btn.addEventListener('click', () => {
      delegationFilters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderDelegation(currentData?.delegation, btn.dataset.filter);
    });
  });
}

// WebSocket connection
function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  
  // The backend uses a manual upgrade handler for '/ws' attached to the HTTP server
  const wsUrl = `${protocol}//${window.location.host}/ws`;

  updateConnectionStatus('connecting');

  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('[WebSocket] Connected');
    updateConnectionStatus('connected');
    reconnectAttempts = 0;
  };

  ws.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data);
      if (message.type === 'init' || message.type === 'update') {
        currentData = message.data;
        renderAll();
      }
    } catch (e) {
      console.error('[WebSocket] Parse error:', e);
    }
  };

  ws.onclose = () => {
    console.log('[WebSocket] Disconnected');
    updateConnectionStatus('disconnected');

    // Attempt reconnection
    if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
      reconnectAttempts++;
      setTimeout(connectWebSocket, 3000 * reconnectAttempts);
    }
  };

  ws.onerror = (error) => {
    console.error('[WebSocket] Error:', error);
    updateConnectionStatus('disconnected');
  };
}

// Update connection status indicator
function updateConnectionStatus(status) {
  const statusEl = document.getElementById('connectionStatus');
  const dot = statusEl.querySelector('.status-dot');
  const text = statusEl.querySelector('.status-text');

  dot.className = 'status-dot';

  switch (status) {
    case 'connected':
      dot.classList.add('connected');
      text.textContent = i18n.t('status_live');
      break;
    case 'disconnected':
      dot.classList.add('disconnected');
      text.textContent = i18n.t('status_offline');
      break;
    default:
      text.textContent = i18n.t('status_connecting');
  }
}

// Fetch initial data via HTTP
async function fetchInitialData() {
  try {
    const response = await fetch('/api/tasks');
    if (!response.ok) throw new Error('HTTP ' + response.status);

    const data = await response.json();
    currentData = data;
    renderAll();
  } catch (e) {
    console.error('[Fetch] Error:', e);
  }
}

// Render all components
function renderAll() {
  if (!currentData) return;

  renderStats();
  renderMatrix();
  renderCustomers(currentData.customerProjects);
  renderDelegation(currentData.delegation);
  renderMaybe(currentData.maybe);
  updateTimestamp();
}

// Update stats bar
function renderStats() {
  const tasks = currentData.tasks;
  const customers = currentData.customerProjects;
  const delegation = currentData.delegation;
  const maybe = currentData.maybe;

  document.getElementById('q1Count').textContent = tasks?.stats?.q1 || 0;
  document.getElementById('q2Count').textContent = tasks?.stats?.q2 || 0;
  document.getElementById('q3Count').textContent = tasks?.stats?.q3 || 0;
  document.getElementById('q4Count').textContent = tasks?.stats?.q4 || 0;
  document.getElementById('customerCount').textContent = customers?.stats?.total || 0;
  document.getElementById('delegationCount').textContent = delegation?.stats?.total || 0;
  document.getElementById('maybeCount').textContent = maybe?.stats?.total || 0;
}

// Render quadrant matrix
function renderMatrix() {
  const tasks = currentData.tasks;
  if (!tasks) return;

  renderTaskList('q1List', tasks.q1, 'Q1');
  renderTaskList('q2List', tasks.q2, 'Q2');
  renderTaskList('q3List', tasks.q3, 'Q3');
  renderTaskList('q4List', tasks.q4, 'Q4');
}

// Store tooltip elements keyed by task ID for proper cleanup
const activeTooltips = new Map();

// Render a task list
function renderTaskList(elementId, tasks, quadrant) {
  const container = document.getElementById(elementId);
  if (!container) return;

  // Clean up existing tooltips for this container
  container.querySelectorAll('.task-card').forEach(card => {
    const taskId = card.dataset.taskId;
    if (activeTooltips.has(taskId)) {
      const tooltip = activeTooltips.get(taskId);
      if (tooltip && tooltip.parentNode) {
        tooltip.parentNode.removeChild(tooltip);
      }
      activeTooltips.delete(taskId);
    }
  });

  if (!tasks || tasks.length === 0) {
    container.innerHTML = `<div class="empty-state">${i18n.t('empty_tasks')}</div>`;
    // Add drop zone handling even for empty lists
    initDragAndDrop(container, quadrant);
    return;
  }

  container.innerHTML = tasks.map(task => `
    <div class="task-card ${task.blocked ? 'blocked' : ''} ${task.priority ? 'priority-' + task.priority.toLowerCase() : ''}" 
         data-task-id="${task.id}" 
         data-quadrant="${quadrant}">
      <div class="drag-handle" draggable="true" title="Drag to move"></div>
      <button class="copy-btn" data-task-id="${task.id}" data-source="${quadrant}" data-type="quadrant" title="Copy to...">⎘</button>
      <button class="move-btn" data-task-id="${task.id}" data-source="${quadrant}" data-type="quadrant-to-maybe" title="Move to Maybe...">→</button>
      <button class="complete-btn" data-task-id="${task.id}" data-quadrant="${quadrant}" title="Complete">✓</button>
      <button class="delete-btn" data-task-id="${task.id}" data-quadrant="${quadrant}" title="Delete">×</button>
      <div class="task-title-row">
        <span class="task-id">#${task.id}</span>
        ${task.priority ? `<span class="task-priority ${task.priority.toLowerCase()}">${task.priority}</span>` : ''}
        <span class="task-title-text">${escapeHtml(task.title)}</span>
      </div>
      ${task.description ? `<div class="task-desc">${escapeHtml(task.description)}</div>` : ''}
      ${task.tags.length > 0 ? `
        <div class="task-tags">
          ${task.tags.map(tag => `<span class="task-tag">${escapeHtml(tag)}</span>`).join('')}
        </div>
      ` : ''}
      ${task.blocked ? `<div class="task-meta"><span class="blocked-badge">${i18n.t('blocked_badge')}</span></div>` : ''}
    </div>
  `).join('');

  // Initialize drag and drop for this container
  initDragAndDrop(container, quadrant);

  // Add complete button event listeners
  container.querySelectorAll('.complete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      const taskQuadrant = btn.dataset.quadrant;
      showConfirm(`Complete task #${taskId}?`, () => {
        completeTask(taskId, taskQuadrant);
      });
    });
  });

  // Add delete button event listeners
  container.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      const taskQuadrant = btn.dataset.quadrant;
      showConfirm(`Delete task #${taskId}?`, () => {
        deleteTask(taskId, taskQuadrant);
      });
    });
  });

  // Add copy button event listeners
  container.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      const source = btn.dataset.source;
      const type = btn.dataset.type;
      showCopyMenu(taskId, source, type);
    });
  });

  // Add move button event listeners for moving to Maybe or Delegation
  container.querySelectorAll('.move-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      const source = btn.dataset.source;
      showMoveToMenu(taskId, source);
    });
  });

  // Add hover event listeners for tooltips
  container.querySelectorAll('.task-card').forEach((card, index) => {
    const task = tasks[index];
    if (!task) return;

    // Create tooltip element and append to body to avoid CSS containment issues
    const tooltip = document.createElement('div');
    tooltip.className = 'task-tooltip';
    tooltip.innerHTML = `
      <div class="tooltip-header">
        <span class="tooltip-id">#${task.id}</span>
        ${task.priority ? `<span class="tooltip-priority ${task.priority.toLowerCase()}">${task.priority}</span>` : ''}
        ${task.blocked ? `<span class="tooltip-blocked">🚫 ${i18n.t('blocked_badge')}</span>` : ''}
      </div>
      <div class="tooltip-title">${escapeHtml(task.title)}</div>
      ${task.description ? `<div class="tooltip-section"><div class="tooltip-label">${i18n.t('description')}</div><div class="tooltip-desc">${escapeHtml(task.description)}</div></div>` : ''}
      ${task.subtasks && task.subtasks.length > 0 ? `
        <div class="tooltip-section">
          <div class="tooltip-label">${i18n.t('subtasks')} (${task.subtasks.length})</div>
          <div class="tooltip-subtasks">
            ${task.subtasks.map(sub => `<div class="tooltip-subtask">• ${escapeHtml(sub.title)}${sub.content ? `<br><small>${escapeHtml(sub.content)}</small>` : ''}</div>`).join('')}
          </div>
        </div>
      ` : ''}
      ${task.tags.length > 0 ? `
        <div class="tooltip-section">
          <div class="tooltip-label">${i18n.t('tags')}</div>
          <div class="tooltip-tags">
            ${task.tags.map(tag => `<span class="tooltip-tag">${escapeHtml(tag)}</span>`).join('')}
          </div>
        </div>
      ` : ''}
      <div class="tooltip-meta">
        ${task.created ? `<div><span class="tooltip-label">${i18n.t('created_prefix')}</span> ${task.created}</div>` : ''}
        ${task.updated ? `<div><span class="tooltip-label">${i18n.t('updated_prefix')}</span> ${task.updated}</div>` : ''}
      </div>
    `;
    document.body.appendChild(tooltip);
    activeTooltips.set(String(task.id), tooltip);

    card.addEventListener('mouseenter', (e) => {
      // First show tooltip to get its dimensions
      tooltip.classList.add('show');
      
      // Then calculate position based on actual dimensions
      const tooltipRect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      let left = e.clientX + 15;
      let top = e.clientY + 15;

      // Adjust if tooltip goes off right edge
      if (left + tooltipRect.width > viewportWidth) {
        left = e.clientX - tooltipRect.width - 15;
      }

      // Adjust if tooltip goes off bottom edge
      if (top + tooltipRect.height > viewportHeight) {
        top = e.clientY - tooltipRect.height - 15;
      }

      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });

    card.addEventListener('mouseleave', () => {
      tooltip.classList.remove('show');
    });

    card.addEventListener('mousemove', (e) => {
      const tooltipRect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      // Calculate position relative to viewport
      let left = e.clientX + 15;
      let top = e.clientY + 15;

      // Adjust if tooltip goes off right edge
      if (left + tooltipRect.width > viewportWidth) {
        left = e.clientX - tooltipRect.width - 15;
      }

      // Adjust if tooltip goes off bottom edge
      if (top + tooltipRect.height > viewportHeight) {
        top = e.clientY - tooltipRect.height - 15;
      }

      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });
  });

  // Initialize drag and drop for customer project lists
  container.querySelectorAll('.projects-list').forEach(projectList => {
    initCustomerDragAndDrop(projectList);
  });
}

// Track which containers have been initialized for drag and drop
const dndInitializedContainers = new Set();

// Track which customer project containers have been initialized for drag and drop
const customerDndInitializedContainers = new Set();

// Initialize drag and drop for a task list
function initDragAndDrop(container, quadrant) {
  // Only initialize container-level events once
  if (!dndInitializedContainers.has(container.id)) {
    dndInitializedContainers.add(container.id);
    container.addEventListener('dragover', handleDragOver);
    container.addEventListener('dragenter', handleDragEnter);
    container.addEventListener('dragleave', handleDragLeave);
    container.addEventListener('drop', (e) => handleDrop(e, quadrant));
  }

  // Make drag handles draggable (these need to be re-attached after each render)
  container.querySelectorAll('.drag-handle').forEach(handle => {
    // Remove existing listeners to prevent duplicates
    handle.removeEventListener('dragstart', handleDragStart);
    handle.removeEventListener('dragend', handleDragEnd);
    // Add listeners
    handle.addEventListener('dragstart', handleDragStart);
    handle.addEventListener('dragend', handleDragEnd);
  });
}

// Drag start handler
function handleDragStart(e) {
  // Find the parent task card from the drag handle
  const card = e.target.closest('.task-card');
  if (!card) return;
  
  draggedTask = {
    id: parseInt(card.dataset.taskId),
    quadrant: card.dataset.quadrant,
    element: card
  };
  draggedSourceQuadrant = card.dataset.quadrant;
  
  card.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', JSON.stringify({
    id: draggedTask.id,
    quadrant: draggedTask.quadrant
  }));
  
  console.log('[Drag] Started:', draggedTask);
}

// Drag end handler
function handleDragEnd(e) {
  // Remove dragging class from the parent card
  const card = e.target.closest('.task-card');
  if (card) {
    card.classList.remove('dragging');
  }
  
  // Clean up drop indicators and drop zone highlighting
  document.querySelectorAll('.drop-indicator').forEach(el => el.remove());
  document.querySelectorAll('.task-list').forEach(el => {
    el.classList.remove('drag-over', 'q1-list', 'q2-list', 'q3-list', 'q4-list');
  });
  
  // Clear drag state (drop handler may have already processed the move)
  draggedTask = null;
  draggedSourceQuadrant = null;
  console.log('[Drag] Ended');
}

// Drag enter handler
function handleDragEnter(e) {
  e.preventDefault();
  const container = e.currentTarget;
  const quadrant = container.id.replace('List', '').toUpperCase();
  container.classList.add('drag-over', `${quadrant.toLowerCase()}-list`);
}

// Drag leave handler
function handleDragLeave(e) {
  const container = e.currentTarget;
  // Only remove if we're actually leaving the container (not entering a child)
  if (!container.contains(e.relatedTarget)) {
    container.classList.remove('drag-over', 'q1-list', 'q2-list', 'q3-list', 'q4-list');
  }
}

// Drag over handler - for reordering within list
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  
  if (!draggedTask) return;
  
  const container = e.currentTarget;
  const afterElement = getDragAfterElement(container, e.clientY);
  
  // Update drop indicator
  document.querySelectorAll('.drop-indicator').forEach(el => el.remove());
  
  const indicator = document.createElement('div');
  indicator.className = 'drop-indicator';
  
  if (afterElement == null) {
    container.appendChild(indicator);
  } else {
    container.insertBefore(indicator, afterElement);
  }
}

// Get the element after which to insert the dragged element
function getDragAfterElement(container, y, selector = '.task-card', x = null) {
  const draggableElements = [...container.querySelectorAll(`${selector}:not(.dragging)`)];

  // For grid layout, we need to consider 2D position
  // Find the element that is closest to the cursor in grid order
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();

    // Calculate distance to the center of the element
    const centerX = box.left + box.width / 2;
    const centerY = box.top + box.height / 2;

    // For grid layout, check if cursor is before this element in reading order
    // (top to bottom, left to right)
    let isBefore;
    if (x !== null) {
      // Grid layout: check row first, then column
      const sameRow = Math.abs(y - centerY) < box.height / 2;
      if (sameRow) {
        isBefore = x < centerX;
      } else {
        isBefore = y < box.top;
      }
    } else {
      // List layout: only check Y position
      isBefore = y < box.top + box.height / 2;
    }

    // Calculate a score based on proximity
    const dx = x !== null ? x - centerX : 0;
    const dy = y - centerY;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (isBefore && distance < closest.distance) {
      return { distance: distance, element: child };
    } else {
      return closest;
    }
  }, { distance: Number.POSITIVE_INFINITY }).element;
}

// Track if a drop is currently being processed
let isProcessingDrop = false;

// Drop handler
async function handleDrop(e, targetQuadrant) {
  e.preventDefault();
  
  // Prevent duplicate drop processing
  if (isProcessingDrop) {
    console.log('[Drop] Already processing a drop, ignoring duplicate');
    return;
  }
  isProcessingDrop = true;
  
  const container = e.currentTarget;
  container.classList.remove('drag-over', 'q1-list', 'q2-list', 'q3-list', 'q4-list');
  
  // Clean up drop indicators
  document.querySelectorAll('.drop-indicator').forEach(el => el.remove());
  
  if (!draggedTask) {
    isProcessingDrop = false;
    return;
  }
  
  const sourceQuadrant = draggedTask.quadrant;
  const taskId = draggedTask.id;
  const draggedElement = draggedTask.element;
  
  // Find the insert position
  const afterElement = getDragAfterElement(container, e.clientY);
  let insertIndex = -1; // -1 means append at end
  
  if (afterElement) {
    const allCards = [...container.querySelectorAll('.task-card')];
    // Filter out the dragging card
    const visibleCards = allCards.filter(c => !c.classList.contains('dragging'));
    insertIndex = visibleCards.indexOf(afterElement);
  }
  
  console.log('[Drop] Task:', taskId, 'from', sourceQuadrant, 'to', targetQuadrant, 'at index', insertIndex);
  
  // OPTIMISTIC UPDATE: Immediately move the DOM element
  // Remove dragging class first
  draggedElement.classList.remove('dragging');
  
  // Move element to new position in DOM
  if (afterElement) {
    container.insertBefore(draggedElement, afterElement);
  } else {
    container.appendChild(draggedElement);
  }
  
  // Update the data-quadrant attribute
  draggedElement.dataset.quadrant = targetQuadrant;
  
  // Note: We do NOT renumber tasks here because the API needs the original taskId
  // The server will handle renumbering and we'll refresh after API call
  
  // Call API to persist changes
  try {
    const response = await fetch('/api/tasks/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        taskId: taskId,
        sourceQuadrant: sourceQuadrant,
        targetQuadrant: targetQuadrant,
        insertIndex: insertIndex
      })
    });
    
    if (!response.ok) {
      throw new Error('Failed to move task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Drop] Success:', result);
    
    // Refresh data from server to ensure consistency
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Drop] Error:', error);
    alert('Failed to move task: ' + error.message);
    // On error, refresh to get correct state from server
    await fetchInitialData();
  } finally {
    // Reset processing flag
    isProcessingDrop = false;
  }
}

// Initialize drag and drop for customer project lists
function initCustomerDragAndDrop(projectList) {
  const customerName = projectList.dataset.customer;

  // Always bind container-level events (elements are recreated on each render)
  projectList.addEventListener('dragover', handleCustomerDragOver);
  projectList.addEventListener('dragenter', handleCustomerDragEnter);
  projectList.addEventListener('dragleave', handleCustomerDragLeave);
  projectList.addEventListener('drop', (e) => handleCustomerDrop(e, customerName));

  // Make drag handles draggable
  projectList.querySelectorAll('.customer-drag-handle').forEach(handle => {
    handle.draggable = true;
    handle.removeEventListener('dragstart', handleCustomerDragStart);
    handle.removeEventListener('dragend', handleCustomerDragEnd);
    handle.addEventListener('dragstart', handleCustomerDragStart);
    handle.addEventListener('dragend', handleCustomerDragEnd);
  });
}

// Customer project drag start handler
function handleCustomerDragStart(e) {
  const projectItem = e.target.closest('.project-item');
  if (!projectItem) return;

  draggedCustomerProject = {
    id: parseInt(projectItem.dataset.projectId),
    customer: projectItem.dataset.customer,
    element: projectItem
  };
  draggedSourceCustomer = projectItem.dataset.customer;

  projectItem.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', JSON.stringify({
    id: draggedCustomerProject.id,
    customer: draggedCustomerProject.customer
  }));

  console.log('[Customer Drag] Started:', draggedCustomerProject);
}

// Customer project drag end handler
function handleCustomerDragEnd(e) {
  const projectItem = e.target.closest('.project-item');
  if (projectItem) {
    projectItem.classList.remove('dragging');
  }

  // Clean up
  document.querySelectorAll('.drop-indicator').forEach(el => el.remove());
  document.querySelectorAll('.projects-list').forEach(el => {
    el.classList.remove('drag-over');
  });

  draggedCustomerProject = null;
  draggedSourceCustomer = null;
  console.log('[Customer Drag] Ended');
}

// Customer project drag leave handler
function handleCustomerDragLeave(e) {
  const projectList = e.currentTarget;
  if (!projectList.contains(e.relatedTarget)) {
    projectList.classList.remove('drag-over');
  }
}

// Customer project drag enter handler
function handleCustomerDragEnter(e) {
  e.preventDefault();
  const projectList = e.currentTarget;
  projectList.classList.add('drag-over');
}

// Customer project drag over handler
function handleCustomerDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';

  if (!draggedCustomerProject) return;

  const projectList = e.currentTarget;
  const afterElement = getDragAfterElementForProjects(projectList, e.clientY);

  // Update drop indicator
  document.querySelectorAll('.drop-indicator').forEach(el => el.remove());

  const indicator = document.createElement('div');
  indicator.className = 'drop-indicator customer-drop-indicator';

  if (afterElement == null) {
    projectList.appendChild(indicator);
  } else {
    projectList.insertBefore(indicator, afterElement);
  }
}





// Get the element after which to insert the dragged project
function getDragAfterElementForProjects(container, y) {
  const draggableElements = [...container.querySelectorAll('.project-item:not(.dragging)')];

  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;

    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

// Track if a customer project drop is being processed
let isProcessingCustomerDrop = false;

// Customer project drop handler
async function handleCustomerDrop(e, targetCustomer) {
  e.preventDefault();

  if (isProcessingCustomerDrop) {
    console.log('[Customer Drop] Already processing, ignoring duplicate');
    return;
  }
  isProcessingCustomerDrop = true;

  const projectList = e.currentTarget;
  projectList.classList.remove('drag-over');

  // Clean up drop indicators
  document.querySelectorAll('.drop-indicator').forEach(el => el.remove());

  if (!draggedCustomerProject) {
    isProcessingCustomerDrop = false;
    return;
  }

  const sourceCustomer = draggedCustomerProject.customer;
  const projectId = draggedCustomerProject.id;
  const draggedElement = draggedCustomerProject.element;

  // Find insert position
  const afterElement = getDragAfterElementForProjects(projectList, e.clientY);
  let insertIndex = -1;

  if (afterElement) {
    const allItems = [...projectList.querySelectorAll('.project-item')];
    const visibleItems = allItems.filter(i => !i.classList.contains('dragging'));
    insertIndex = visibleItems.indexOf(afterElement);
  }

  console.log('[Customer Drop] Project:', projectId, 'from', sourceCustomer, 'to', targetCustomer, 'at index', insertIndex);

  // Optimistic update
  draggedElement.classList.remove('dragging');

  if (afterElement) {
    projectList.insertBefore(draggedElement, afterElement);
  } else {
    projectList.appendChild(draggedElement);
  }

  // Update data attribute
  draggedElement.dataset.customer = targetCustomer;

  // Call API
  try {
    const response = await fetch('/api/customer-projects/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectId: projectId,
        sourceCustomer: sourceCustomer,
        targetCustomer: targetCustomer,
        insertIndex: insertIndex
      })
    });

    if (!response.ok) {
      throw new Error('Failed to move project: ' + response.statusText);
    }

    const result = await response.json();
    console.log('[Customer Drop] Success:', result);

    await fetchInitialData();

  } catch (error) {
    console.error('[Customer Drop] Error:', error);
    alert('Failed to move project: ' + error.message);
    await fetchInitialData();
  } finally {
    isProcessingCustomerDrop = false;
  }
}

// Render customer projects
function renderCustomers(data, filter = 'all') {
  const container = document.getElementById('customerList');
  if (!container || !data) return;

  const customers = data.customers || [];

  if (customers.length === 0) {
    container.innerHTML = `<div class="empty-state">${i18n.t('empty_customer')}</div>`;
    return;
  }

  // Clear any existing customer tooltips
  document.querySelectorAll('.customer-tooltip').forEach(t => t.remove());

  container.innerHTML = customers.map(customer => {
    // Filter projects
    let projects = customer.projects || [];
    if (filter === 'active') {
      projects = projects.filter(p => !p.blocked && p.status.toLowerCase().includes('active'));
    } else if (filter === 'blocked') {
      projects = projects.filter(p => p.blocked);
    }

    if (projects.length === 0) return '';

    return `
      <div class="customer-card" data-customer="${escapeHtml(customer.name)}">
        <div class="customer-header">
          <div class="customer-name">${escapeHtml(customer.name)}</div>
          <div class="customer-priority">${escapeHtml(customer.priority)}</div>
        </div>
        <div class="projects-list" data-customer="${escapeHtml(customer.name)}">
          ${projects.map(project => `
            <div class="project-item ${project.blocked ? 'blocked' : ''}" data-project-id="${project.id}" data-customer="${escapeHtml(customer.name)}">
              <div class="drag-handle customer-drag-handle" draggable="true" title="${i18n.t('drag_to_reorder') || 'Drag to reorder'}"></div>
              <button class="copy-btn customer-copy-btn" data-task-id="${project.id}" data-source="${escapeHtml(customer.name)}" data-type="customer" title="Copy to...">⎘</button>
              <button class="complete-btn customer-complete-btn" data-project-id="${project.id}" data-customer="${escapeHtml(customer.name)}" title="Complete">✓</button>
              <button class="delete-btn customer-delete-btn" data-project-id="${project.id}" data-customer="${escapeHtml(customer.name)}" title="Delete">×</button>
              <div class="project-content">
                <div class="project-header">
                  <div class="project-name"><span class="task-id">#${project.id}</span> ${escapeHtml(project.name)}</div>
                  <div class="project-status ${project.blocked ? 'blocked' : project.status.toLowerCase().replace(/\s+/g, '')}">
                    ${project.blocked ? '🟡 ' + i18n.t('status_blocked') : escapeHtml(project.status)}
                  </div>
                </div>
                <div class="project-meta">
                  <span>${i18n.t('type_prefix')} ${escapeHtml(project.type)}</span>
                  <span>${i18n.t('priority_prefix')} ${escapeHtml(project.priority)}</span>
                  ${project.lastReview ? `<span>${i18n.t('reviewed_prefix')} ${escapeHtml(project.lastReview)}</span>` : ''}
                </div>
                ${project.notes ? `<div class="project-notes">${escapeHtml(project.notes)}</div>` : ''}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }).filter(Boolean).join('') || `<div class="empty-state">${i18n.t('empty_filtered')}</div>`;

  // Add hover tooltips for project items
  container.querySelectorAll('.project-item').forEach(item => {
    const customerCard = item.closest('.customer-card');
    const customerName = customerCard?.dataset.customer || '';
    const projectId = item.dataset.projectId;
    
    // Find project data
    let project = null;
    for (const customer of customers) {
      project = customer.projects?.find(p => p.id.toString() === projectId);
      if (project) break;
    }
    if (!project) return;

    const tooltip = document.createElement('div');
    tooltip.className = 'task-tooltip customer-tooltip';
    tooltip.innerHTML = `
      <div class="tooltip-header">
        <span class="tooltip-id">#${project.id}</span>
        <span class="tooltip-priority">${escapeHtml(customerName)}</span>
      </div>
      <div class="tooltip-title">${escapeHtml(project.name)}</div>
      <div class="tooltip-section">
        <div class="tooltip-label">${i18n.t('status_active')}</div>
        <div class="tooltip-desc">${project.blocked ? '🟡 ' + i18n.t('status_blocked') : escapeHtml(project.status)}</div>
      </div>
      <div class="tooltip-section">
        <div class="tooltip-label">${i18n.t('type_prefix')}</div>
        <div class="tooltip-desc">${escapeHtml(project.type)}</div>
      </div>
      <div class="tooltip-section">
        <div class="tooltip-label">${i18n.t('priority_prefix')}</div>
        <div class="tooltip-desc">${escapeHtml(project.priority)}</div>
      </div>
      ${project.notes ? `<div class="tooltip-section"><div class="tooltip-label">${i18n.t('description')}</div><div class="tooltip-desc">${escapeHtml(project.notes)}</div></div>` : ''}
      <div class="tooltip-meta">
        ${project.created ? `<div><span class="tooltip-label">${i18n.t('created_prefix')}</span> ${project.created}</div>` : ''}
        ${project.lastReview ? `<div><span class="tooltip-label">${i18n.t('reviewed_prefix')}</span> ${project.lastReview}</div>` : ''}
      </div>
    `;
    document.body.appendChild(tooltip);

    item.addEventListener('mouseenter', (e) => {
      tooltip.classList.add('show');
      const tooltipRect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      let left = e.clientX + 15;
      let top = e.clientY + 15;
      if (left + tooltipRect.width > viewportWidth) left = e.clientX - tooltipRect.width - 15;
      if (top + tooltipRect.height > viewportHeight) top = e.clientY - tooltipRect.height - 15;
      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });

    item.addEventListener('mouseleave', () => tooltip.classList.remove('show'));

    item.addEventListener('mousemove', (e) => {
      const tooltipRect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      let left = e.clientX + 15;
      let top = e.clientY + 15;
      if (left + tooltipRect.width > viewportWidth) left = e.clientX - tooltipRect.width - 15;
      if (top + tooltipRect.height > viewportHeight) top = e.clientY - tooltipRect.height - 15;
      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });
  });

  // Initialize drag and drop for customer project lists
  container.querySelectorAll('.projects-list').forEach(projectList => {
    initCustomerDragAndDrop(projectList);
  });

  // Add copy button event listeners for customer projects
  container.querySelectorAll('.customer-copy-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      const source = btn.dataset.source;
      const type = btn.dataset.type;
      showCopyMenu(taskId, source, type);
    });
  });

  // Add complete button event listeners for customer projects
  container.querySelectorAll('.customer-complete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const projectId = parseInt(btn.dataset.projectId);
      const customerName = btn.dataset.customer;
      showConfirm(`Complete project #${projectId} from ${customerName}?`, () => {
        completeCustomerProject(projectId, customerName);
      });
    });
  });

  // Add delete button event listeners for customer projects
  container.querySelectorAll('.customer-delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const projectId = parseInt(btn.dataset.projectId);
      const customerName = btn.dataset.customer;
      showConfirm(`Delete project #${projectId} from ${customerName}?`, () => {
        deleteCustomerProject(projectId, customerName);
      });
    });
  });
}

// Render delegation tasks
function renderDelegation(data, filter = 'all') {
  const container = document.getElementById('delegationList');
  if (!container || !data) return;

  let tasks = data.tasks || [];

  if (filter === 'inProgress') {
    tasks = tasks.filter(t => t.status === i18n.t('status_in_progress') || t.status === '进行中');
  } else if (filter === 'overdue') {
    tasks = tasks.filter(t => t.overdue);
  }

  if (tasks.length === 0) {
    container.innerHTML = `<div class="empty-state">${i18n.t('empty_delegation')}</div>`;
    return;
  }

  // Clear existing delegation tooltips
  document.querySelectorAll('.delegation-tooltip').forEach(t => t.remove());

  container.innerHTML = tasks.map(task => `
    <div class="delegation-card ${task.overdue ? 'overdue' : ''}" data-task-id="${task.id}">
      <div class="drag-handle delegation-drag-handle" draggable="true" title="Drag to reorder"></div>
      <button class="complete-btn delegation-complete-btn" data-task-id="${task.id}" title="Complete">✓</button>
      <button class="delete-btn delegation-delete-btn" data-task-id="${task.id}" title="Delete">×</button>
      <div class="delegation-header">
        <div class="delegation-title"><span class="task-id">#${task.id}</span><span class="delegation-title-text">${escapeHtml(task.title)}</span></div>
        <div class="delegation-status ${task.status === i18n.t('status_in_progress') || task.status === '进行中' ? 'inprogress' : 'todo'}">
          ${task.status}
        </div>
      </div>
      ${task.description ? `<div class="delegation-desc">${escapeHtml(task.description)}</div>` : ''}
      <div class="delegation-meta">
        <span class="delegation-assignee">${escapeHtml(task.assignee)}</span>
        ${task.deadline ? `<span class="delegation-deadline ${task.overdue ? 'overdue' : ''}">
          ${task.overdue ? i18n.t('deadline_overdue') : i18n.t('deadline_prefix')} ${escapeHtml(task.deadline)}
        </span>` : ''}
      </div>
    </div>
  `).join('');

  // Add hover tooltips for delegation cards
  container.querySelectorAll('.delegation-card').forEach((card, index) => {
    const task = tasks[index];
    if (!task) return;

    const tooltip = document.createElement('div');
    tooltip.className = 'task-tooltip delegation-tooltip';
    tooltip.innerHTML = `
      <div class="tooltip-header">
        <span class="tooltip-id">#${task.id}</span>
        ${task.overdue ? `<span class="tooltip-blocked">⚠️ ${i18n.t('deadline_overdue')}</span>` : ''}
      </div>
      <div class="tooltip-title">${escapeHtml(task.title)}</div>
      ${task.description ? `<div class="tooltip-section"><div class="tooltip-label">${i18n.t('description')}</div><div class="tooltip-desc">${escapeHtml(task.description)}</div></div>` : ''}
      <div class="tooltip-section">
        <div class="tooltip-label">${i18n.t('status_in_progress')}</div>
        <div class="tooltip-desc">${escapeHtml(task.status)}</div>
      </div>
      <div class="tooltip-section">
        <div class="tooltip-label">${i18n.t('assignee_prefix')}</div>
        <div class="tooltip-desc">${escapeHtml(task.assignee)}</div>
      </div>
      ${task.deadline ? `<div class="tooltip-section"><div class="tooltip-label">${i18n.t('deadline_prefix')}</div><div class="tooltip-desc ${task.overdue ? 'overdue' : ''}">${escapeHtml(task.deadline)}</div></div>` : ''}
      ${task.created ? `<div class="tooltip-meta"><span class="tooltip-label">${i18n.t('created_prefix')}</span> ${task.created}</div>` : ''}
    `;
    document.body.appendChild(tooltip);

    card.addEventListener('mouseenter', (e) => {
      tooltip.classList.add('show');
      const tooltipRect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      let left = e.clientX + 15;
      let top = e.clientY + 15;
      if (left + tooltipRect.width > viewportWidth) left = e.clientX - tooltipRect.width - 15;
      if (top + tooltipRect.height > viewportHeight) top = e.clientY - tooltipRect.height - 15;
      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });

    card.addEventListener('mouseleave', () => tooltip.classList.remove('show'));

    card.addEventListener('mousemove', (e) => {
      const tooltipRect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      let left = e.clientX + 15;
      let top = e.clientY + 15;
      if (left + tooltipRect.width > viewportWidth) left = e.clientX - tooltipRect.width - 15;
      if (top + tooltipRect.height > viewportHeight) top = e.clientY - tooltipRect.height - 15;
      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });
  });

  // Initialize drag and drop for delegation list
  initDelegationDragAndDrop(container);

  // Add complete button event listeners for delegation tasks
  container.querySelectorAll('.delegation-complete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      showConfirm(`Complete delegation task #${taskId}?`, () => {
        completeDelegationTask(taskId);
      });
    });
  });

  // Add delete button event listeners for delegation tasks
  container.querySelectorAll('.delegation-delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      showConfirm(`Delete delegation task #${taskId}?`, () => {
        deleteDelegationTask(taskId);
      });
    });
  });
}

// Render maybe list
function renderMaybe(data) {
  const container = document.getElementById('maybeList');
  if (!container || !data) return;

  const tasks = data.tasks || [];

  if (tasks.length === 0) {
    container.innerHTML = `<div class="empty-state">${i18n.t('empty_maybe')}</div>`;
    return;
  }

  // Clear existing maybe tooltips
  document.querySelectorAll('.maybe-tooltip').forEach(t => t.remove());

  container.innerHTML = tasks.map(task => `
    <div class="maybe-card" data-task-id="${task.id}">
      <div class="drag-handle maybe-drag-handle" draggable="true" title="Drag to reorder"></div>
      <button class="complete-btn maybe-complete-btn" data-task-id="${task.id}" title="Complete">✓</button>
      <button class="move-btn maybe-move-btn" data-task-id="${task.id}" data-type="maybe" title="Move to Quadrant...">→</button>
      <button class="delete-btn maybe-delete-btn" data-task-id="${task.id}" title="Delete">×</button>
      <div class="maybe-header">
        <div class="maybe-title"><span class="task-id">#${task.id}</span><span class="maybe-title-text">${escapeHtml(task.title)}</span></div>
        ${task.category ? `<div class="maybe-category">${escapeHtml(task.category)}</div>` : ''}
      </div>
      ${task.description ? `<div class="maybe-desc">${escapeHtml(task.description)}</div>` : ''}
    </div>
  `).join('');

  // Add hover tooltips for maybe cards
  container.querySelectorAll('.maybe-card').forEach((card, index) => {
    const task = tasks[index];
    if (!task) return;

    const tooltip = document.createElement('div');
    tooltip.className = 'task-tooltip maybe-tooltip';
    tooltip.innerHTML = `
      <div class="tooltip-header">
        <span class="tooltip-id">#${task.id}</span>
        ${task.category ? `<span class="tooltip-priority">${escapeHtml(task.category)}</span>` : ''}
      </div>
      <div class="tooltip-title">${escapeHtml(task.title)}</div>
      ${task.description ? `<div class="tooltip-section"><div class="tooltip-label">${i18n.t('description')}</div><div class="tooltip-desc">${escapeHtml(task.description)}</div></div>` : ''}
      ${task.created ? `<div class="tooltip-meta"><span class="tooltip-label">${i18n.t('created_prefix')}</span> ${task.created}</div>` : ''}
    `;
    document.body.appendChild(tooltip);

    card.addEventListener('mouseenter', (e) => {
      tooltip.classList.add('show');
      const tooltipRect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      let left = e.clientX + 15;
      let top = e.clientY + 15;
      if (left + tooltipRect.width > viewportWidth) left = e.clientX - tooltipRect.width - 15;
      if (top + tooltipRect.height > viewportHeight) top = e.clientY - tooltipRect.height - 15;
      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });

    card.addEventListener('mouseleave', () => tooltip.classList.remove('show'));

    card.addEventListener('mousemove', (e) => {
      const tooltipRect = tooltip.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      let left = e.clientX + 15;
      let top = e.clientY + 15;
      if (left + tooltipRect.width > viewportWidth) left = e.clientX - tooltipRect.width - 15;
      if (top + tooltipRect.height > viewportHeight) top = e.clientY - tooltipRect.height - 15;
      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });
  });

  // Initialize drag and drop for maybe list
  initMaybeDragAndDrop(container);

  // Add complete button event listeners for maybe tasks
  container.querySelectorAll('.maybe-complete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      showConfirm(`Complete maybe task #${taskId}?`, () => {
        completeMaybeTask(taskId);
      });
    });
  });

  // Add move button event listeners for maybe tasks
  container.querySelectorAll('.maybe-move-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      const type = btn.dataset.type;
      showMoveMenu(taskId, type);
    });
  });

  // Add delete button event listeners for maybe tasks
  container.querySelectorAll('.maybe-delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const taskId = parseInt(btn.dataset.taskId);
      showConfirm(`Delete maybe task #${taskId}?`, () => {
        deleteMaybeTask(taskId);
      });
    });
  });
}

// Update timestamp
function updateTimestamp() {
  const el = document.getElementById('lastUpdate');
  if (el && currentData?.timestamp) {
    const date = new Date(currentData.timestamp);
    // Use locale based on current language
    const locale = i18n.getLanguage() === 'zh-CN' ? 'zh-CN' : 'en-US';
    el.textContent = date.toLocaleString(locale);
  }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Refresh button handler (manual refresh)
function refreshData() {
  fetchInitialData();
}

// Export for debugging
window.taskDashboard = {
  refresh: refreshData,
  getData: () => currentData,
  getWebSocket: () => ws
};

// Delete task from tasks.md
async function completeTask(taskId, quadrant) {
  try {
    console.log('[Complete] Task:', taskId, 'from', quadrant);
    
    const response = await fetch('/api/tasks/complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId, quadrant })
    });
    
    if (!response.ok) {
      throw new Error('Failed to complete task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Complete] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Complete] Error:', error);
    alert('Failed to complete task: ' + error.message);
  }
}

async function deleteTask(taskId, quadrant) {
  try {
    console.log('[Delete] Task:', taskId, 'from', quadrant);
    
    const response = await fetch('/api/tasks/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId, quadrant })
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Delete] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Delete] Error:', error);
    alert('Failed to delete task: ' + error.message);
  }
}

// Complete customer project
async function completeCustomerProject(projectId, customerName) {
  try {
    console.log('[Complete] Customer project:', projectId, 'from', customerName);
    
    const response = await fetch('/api/customer-projects/complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectId, customerName })
    });
    
    if (!response.ok) {
      throw new Error('Failed to complete project: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Complete] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Complete] Error:', error);
    alert('Failed to complete project: ' + error.message);
  }
}

// Delete customer project
async function deleteCustomerProject(projectId, customerName) {
  try {
    console.log('[Delete] Customer project:', projectId, 'from', customerName);
    
    const response = await fetch('/api/customer-projects/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectId, customerName })
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete project: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Delete] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Delete] Error:', error);
    alert('Failed to delete project: ' + error.message);
  }
}

// Complete delegation task
async function completeDelegationTask(taskId) {
  try {
    console.log('[Complete] Delegation task:', taskId);
    
    const response = await fetch('/api/delegation/complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId })
    });
    
    if (!response.ok) {
      throw new Error('Failed to complete task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Complete] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Complete] Error:', error);
    alert('Failed to complete task: ' + error.message);
  }
}

// Delete delegation task
async function deleteDelegationTask(taskId) {
  try {
    console.log('[Delete] Delegation task:', taskId);
    
    const response = await fetch('/api/delegation/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId })
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Delete] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Delete] Error:', error);
    alert('Failed to delete task: ' + error.message);
  }
}

// Complete maybe task
async function completeMaybeTask(taskId) {
  try {
    console.log('[Complete] Maybe task:', taskId);
    
    const response = await fetch('/api/maybe/complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId })
    });
    
    if (!response.ok) {
      throw new Error('Failed to complete task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Complete] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Complete] Error:', error);
    alert('Failed to complete task: ' + error.message);
  }
}

// Delete maybe task
async function deleteMaybeTask(taskId) {
  try {
    console.log('[Delete] Maybe task:', taskId);
    
    const response = await fetch('/api/maybe/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId })
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Delete] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Delete] Error:', error);
    alert('Failed to delete task: ' + error.message);
  }
}

// Copy Menu Functions
let currentCopyTaskId = null;
let currentCopySource = null;
let currentCopyType = null;

function showCopyMenu(taskId, source, type) {
  currentCopyTaskId = taskId;
  currentCopySource = source;
  currentCopyType = type;
  
  // Remove existing menu
  const existingMenu = document.getElementById('copyMenuOverlay');
  if (existingMenu) {
    existingMenu.remove();
  }
  
  const overlay = document.createElement('div');
  overlay.id = 'copyMenuOverlay';
  overlay.className = 'copy-menu-overlay';
  
  const isCustomerProject = type === 'customer';
  const isQuadrantTask = type === 'quadrant';
  const title = isCustomerProject ? i18n.t('copy_project_to') || 'Copy Project to...' : i18n.t('copy_task_to') || 'Copy Task to...';
  
  // Build customer options if copying from quadrant
  let customerOptions = '';
  if (isQuadrantTask && currentData?.customerProjects?.customers) {
    customerOptions = currentData.customerProjects.customers.map(c => 
      `<button class="copy-menu-btn customer" data-target="customer" data-customer="${escapeHtml(c.name)}">🏢 ${escapeHtml(c.name)}</button>`
    ).join('');
  }
  
  // Build delegation option for quadrant tasks
  let delegationOption = '';
  if (isQuadrantTask) {
    delegationOption = `
      <div class="copy-menu-section">
        <div class="copy-menu-label">${i18n.t('delegation') || 'Delegation'}</div>
        <div class="copy-menu-options">
          <button class="copy-menu-btn delegation" data-target="delegation">👑 ${i18n.t('delegation_list') || 'Delegation List'}</button>
        </div>
      </div>
    `;
  }
  
  overlay.innerHTML = `
    <div class="copy-menu">
      <div class="copy-menu-header">${title}</div>
      <div class="copy-menu-section">
        <div class="copy-menu-label">${i18n.t('quadrants') || 'Four Quadrants'}</div>
        <div class="copy-menu-options">
          <button class="copy-menu-btn q1" data-target="Q1">🔥 Q1</button>
          <button class="copy-menu-btn q2" data-target="Q2">💼 Q2</button>
          <button class="copy-menu-btn q3" data-target="Q3">⚡ Q3</button>
          <button class="copy-menu-btn q4" data-target="Q4">🧘 Q4</button>
        </div>
      </div>
      ${isQuadrantTask && customerOptions ? `
      <div class="copy-menu-section">
        <div class="copy-menu-label">${i18n.t('customer_projects') || 'Customer Projects'}</div>
        <div class="copy-menu-options">
          ${customerOptions}
        </div>
      </div>
      ` : ''}
      ${delegationOption}
      ${isCustomerProject ? `
      <div class="copy-menu-section">
        <div class="copy-menu-label">${i18n.t('delegation') || 'Delegation'}</div>
        <div class="copy-menu-options">
          <button class="copy-menu-btn delegation" data-target="delegation">👑 ${i18n.t('delegation_list') || 'Delegation List'}</button>
        </div>
      </div>
      ` : ''}
      <button class="copy-menu-cancel">${i18n.t('cancel') || 'Cancel'}</button>
    </div>
  `;
  
  document.body.appendChild(overlay);
  
  // Show menu with animation
  requestAnimationFrame(() => {
    overlay.classList.add('show');
  });
  
  // Add event listeners
  overlay.querySelectorAll('.copy-menu-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.target;
      const customerName = btn.dataset.customer;
      executeCopy(target, customerName);
      hideCopyMenu();
    });
  });
  
  overlay.querySelector('.copy-menu-cancel').addEventListener('click', hideCopyMenu);
  
  // Close on overlay click
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      hideCopyMenu();
    }
  });
  
  // Close on Escape key
  document.addEventListener('keydown', handleCopyMenuKeydown);
}

function hideCopyMenu() {
  const overlay = document.getElementById('copyMenuOverlay');
  if (overlay) {
    overlay.classList.remove('show');
    setTimeout(() => overlay.remove(), 200);
  }
  document.removeEventListener('keydown', handleCopyMenuKeydown);
  currentCopyTaskId = null;
  currentCopySource = null;
  currentCopyType = null;
}

function handleCopyMenuKeydown(e) {
  if (e.key === 'Escape') {
    hideCopyMenu();
  }
}

async function executeCopy(target, customerName = null) {
  if (!currentCopyTaskId || !currentCopySource) return;
  
  console.log('[Copy]', currentCopyType, currentCopyTaskId, 'from', currentCopySource, 'to', target, customerName ? `customer: ${customerName}` : '');
  
  try {
    // Handle copy to delegation list
    if (target === 'delegation' && currentCopyType === 'quadrant') {
      const response = await fetch('/api/tasks/copy-to-delegation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          taskId: currentCopyTaskId, 
          sourceQuadrant: currentCopySource
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to copy to delegation: ' + response.statusText);
      }
      
      const result = await response.json();
      console.log('[Copy to Delegation] Success:', result);
      await fetchInitialData();
      return;
    }
    
    // Handle copy to customer project
    if (target === 'customer' && customerName) {
      const response = await fetch('/api/tasks/copy-to-customer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          taskId: currentCopyTaskId, 
          sourceQuadrant: currentCopySource, 
          targetCustomer: customerName 
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to copy: ' + response.statusText);
      }
      
      const result = await response.json();
      console.log('[Copy] Success:', result);
      await fetchInitialData();
      return;
    }
    
    const endpoint = currentCopyType === 'customer' 
      ? '/api/customer-projects/copy' 
      : '/api/tasks/copy';
    
    const body = currentCopyType === 'customer'
      ? { projectId: currentCopyTaskId, sourceCustomer: currentCopySource, target }
      : { taskId: currentCopyTaskId, sourceQuadrant: currentCopySource, target };
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    
    if (!response.ok) {
      throw new Error('Failed to copy: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Copy] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Copy] Error:', error);
    alert('Failed to copy: ' + error.message);
  }
}

// Move Menu Functions (for Maybe List)
let currentMoveTaskId = null;
let currentMoveType = null;

function showMoveMenu(taskId, type) {
  currentMoveTaskId = taskId;
  currentMoveType = type;
  
  // Remove existing menu
  const existingMenu = document.getElementById('moveMenuOverlay');
  if (existingMenu) {
    existingMenu.remove();
  }
  
  const overlay = document.createElement('div');
  overlay.id = 'moveMenuOverlay';
  overlay.className = 'copy-menu-overlay';
  
  const title = i18n.t('move_task_to') || 'Move Task to Quadrant...';
  
  overlay.innerHTML = `
    <div class="copy-menu">
      <div class="copy-menu-header">${title}</div>
      <div class="copy-menu-section">
        <div class="copy-menu-label">${i18n.t('quadrants') || 'Four Quadrants'}</div>
        <div class="copy-menu-options">
          <button class="copy-menu-btn q1" data-target="Q1">🔥 Q1</button>
          <button class="copy-menu-btn q2" data-target="Q2">💼 Q2</button>
          <button class="copy-menu-btn q3" data-target="Q3">⚡ Q3</button>
          <button class="copy-menu-btn q4" data-target="Q4">🧘 Q4</button>
        </div>
      </div>
      <button class="copy-menu-cancel">${i18n.t('cancel') || 'Cancel'}</button>
    </div>
  `;
  
  document.body.appendChild(overlay);
  
  // Show menu with animation
  requestAnimationFrame(() => {
    overlay.classList.add('show');
  });
  
  // Add event listeners
  overlay.querySelectorAll('.copy-menu-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.target;
      executeMove(target);
      hideMoveMenu();
    });
  });
  
  overlay.querySelector('.copy-menu-cancel').addEventListener('click', hideMoveMenu);
  
  // Close on overlay click
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      hideMoveMenu();
    }
  });
  
  // Close on Escape key
  document.addEventListener('keydown', handleMoveMenuKeydown);
}

function hideMoveMenu() {
  const overlay = document.getElementById('moveMenuOverlay');
  if (overlay) {
    overlay.classList.remove('show');
    setTimeout(() => overlay.remove(), 200);
  }
  document.removeEventListener('keydown', handleMoveMenuKeydown);
  currentMoveTaskId = null;
  currentMoveType = null;
}

function handleMoveMenuKeydown(e) {
  if (e.key === 'Escape') {
    hideMoveMenu();
  }
}

async function executeMove(target) {
  if (!currentMoveTaskId) return;
  
  console.log('[Move]', currentMoveType, currentMoveTaskId, 'to', target);
  
  try {
    const response = await fetch('/api/maybe/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        taskId: currentMoveTaskId, 
        targetQuadrant: target 
      })
    });
    
    if (!response.ok) {
      throw new Error('Failed to move: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Move] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Move] Error:', error);
    alert('Failed to move: ' + error.message);
  }
}

// Move task from quadrant to Maybe List
let currentMoveToTaskId = null;
let currentMoveToSource = null;

function showMoveToMenu(taskId, source) {
  currentMoveToTaskId = taskId;
  currentMoveToSource = source;
  
  // Remove existing menu
  const existingMenu = document.getElementById('moveToMenuOverlay');
  if (existingMenu) {
    existingMenu.remove();
  }
  
  const overlay = document.createElement('div');
  overlay.id = 'moveToMenuOverlay';
  overlay.className = 'copy-menu-overlay';
  
  const title = i18n.t('move_task_to') || 'Move Task to...';
  
  overlay.innerHTML = `
    <div class="copy-menu">
      <div class="copy-menu-header">${title}</div>
      <div class="copy-menu-section">
        <div class="copy-menu-label">${i18n.t('target_list') || 'Target List'}</div>
        <div class="copy-menu-options">
          <button class="copy-menu-btn maybe" data-target="maybe">🌱 ${i18n.t('maybe_list') || 'Maybe List'}</button>
          <button class="copy-menu-btn delegation" data-target="delegation">👑 ${i18n.t('delegation_list') || 'Delegation List'}</button>
        </div>
      </div>
      <button class="copy-menu-cancel">${i18n.t('cancel') || 'Cancel'}</button>
    </div>
  `;
  
  document.body.appendChild(overlay);
  
  // Show menu with animation
  requestAnimationFrame(() => {
    overlay.classList.add('show');
  });
  
  // Add event listeners
  overlay.querySelectorAll('.copy-menu-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.target;
      executeMoveTo(target);
      hideMoveToMenu();
    });
  });
  
  overlay.querySelector('.copy-menu-cancel').addEventListener('click', hideMoveToMenu);
  
  // Close on overlay click
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      hideMoveToMenu();
    }
  });
  
  // Close on Escape key
  document.addEventListener('keydown', handleMoveToMenuKeydown);
}

function hideMoveToMenu() {
  const overlay = document.getElementById('moveToMenuOverlay');
  if (overlay) {
    overlay.classList.remove('show');
    setTimeout(() => overlay.remove(), 200);
  }
  document.removeEventListener('keydown', handleMoveToMenuKeydown);
  currentMoveToTaskId = null;
  currentMoveToSource = null;
}

function handleMoveToMenuKeydown(e) {
  if (e.key === 'Escape') {
    hideMoveToMenu();
  }
}

async function executeMoveTo(target) {
  if (!currentMoveToTaskId || !currentMoveToSource) return;
  
  if (target === 'maybe') {
    await moveTaskToMaybe(currentMoveToTaskId, currentMoveToSource);
  } else if (target === 'delegation') {
    await moveTaskToDelegation(currentMoveToTaskId, currentMoveToSource);
  }
}

async function moveTaskToMaybe(taskId, sourceQuadrant) {
  try {
    console.log('[Move to Maybe] Task:', taskId, 'from', sourceQuadrant);
    
    const response = await fetch('/api/tasks/move-to-maybe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId, sourceQuadrant })
    });
    
    if (!response.ok) {
      throw new Error('Failed to move task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Move to Maybe] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Move to Maybe] Error:', error);
    alert('Failed to move: ' + error.message);
  }
}

async function moveTaskToDelegation(taskId, sourceQuadrant) {
  try {
    console.log('[Move to Delegation] Task:', taskId, 'from', sourceQuadrant);
    
    const response = await fetch('/api/tasks/move-to-delegation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId, sourceQuadrant })
    });
    
    if (!response.ok) {
      throw new Error('Failed to move task: ' + response.statusText);
    }
    
    const result = await response.json();
    console.log('[Move to Delegation] Success:', result);
    
    await fetchInitialData();
    
  } catch (error) {
    console.error('[Move to Delegation] Error:', error);
    alert('Failed to move: ' + error.message);
  }
}

// Delegation List Drag and Drop
let draggedDelegationTask = null;

function initDelegationDragAndDrop(container) {
  container.addEventListener('dragover', handleDelegationDragOver);
  container.addEventListener('dragenter', handleDelegationDragEnter);
  container.addEventListener('dragleave', handleDelegationDragLeave);
  container.addEventListener('drop', handleDelegationDrop);
  
  container.querySelectorAll('.delegation-drag-handle').forEach(handle => {
    handle.draggable = true;
    handle.addEventListener('dragstart', handleDelegationDragStart);
    handle.addEventListener('dragend', handleDelegationDragEnd);
  });
}

function handleDelegationDragEnter(e) {
  e.preventDefault();
  // Only highlight if dragging a delegation task
  if (!draggedDelegationTask) return;
  const container = e.currentTarget;
  container.classList.add('drag-over');
}

function handleDelegationDragLeave(e) {
  const container = e.currentTarget;
  // Only remove if leaving the container entirely (not entering a child)
  if (!container.contains(e.relatedTarget)) {
    container.classList.remove('drag-over');
  }
}

function handleDelegationDragStart(e) {
  const card = e.target.closest('.delegation-card');
  if (!card) return;
  
  draggedDelegationTask = {
    id: parseInt(card.dataset.taskId),
    element: card
  };
  
  card.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  console.log('[Delegation Drag] Started:', draggedDelegationTask);
}

function handleDelegationDragEnd(e) {
  const card = e.target.closest('.delegation-card');
  if (card) {
    card.classList.remove('dragging');
  }
  // Clean up all highlights
  document.querySelectorAll('.delegation-card').forEach(c => {
    c.classList.remove('drag-over');
  });
  document.querySelectorAll('.delegation-list').forEach(el => {
    el.classList.remove('drag-over');
  });
  draggedDelegationTask = null;
}

function handleDelegationDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';

  if (!draggedDelegationTask) return;

  const container = e.currentTarget;
  const afterElement = getDragAfterElement(container, e.clientY, '.delegation-card', e.clientX);

  // Clear previous highlights
  container.querySelectorAll('.delegation-card').forEach(card => {
    card.classList.remove('drag-over');
  });

  // Highlight the target position
  if (afterElement) {
    afterElement.classList.add('drag-over');
  } else {
    // If no afterElement, highlight the last card or indicate append
    const cards = container.querySelectorAll('.delegation-card:not(.dragging)');
    if (cards.length > 0) {
      cards[cards.length - 1].classList.add('drag-over');
    }
  }
}

async function handleDelegationDrop(e) {
  e.preventDefault();

  if (!draggedDelegationTask) return;

  const container = e.currentTarget;
  const taskId = draggedDelegationTask.id;

  // Find insert position
  const targetElement = getDragAfterElement(container, e.clientY, '.delegation-card', e.clientX);
  let insertIndex = -1;

  if (targetElement) {
    const allCards = [...container.querySelectorAll('.delegation-card')];
    const targetTaskId = parseInt(targetElement.dataset.taskId);
    const targetIdx = allCards.findIndex(c => parseInt(c.dataset.taskId) === targetTaskId);
    
    // Insert at the target card's position
    // This will push the target card and all after it one position back
    insertIndex = targetIdx;
  }

  // Clear highlights
  container.querySelectorAll('.delegation-card').forEach(card => {
    card.classList.remove('drag-over');
  });
  container.classList.remove('drag-over');

  try {
    const response = await fetch('/api/delegation/reorder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId, insertIndex })
    });

    if (!response.ok) {
      throw new Error('Failed to reorder: ' + response.statusText);
    }

    await fetchInitialData();

  } catch (error) {
    console.error('[Delegation Drop] Error:', error);
    await fetchInitialData();
  }
}

// Maybe List Drag and Drop
let draggedMaybeTask = null;

function initMaybeDragAndDrop(container) {
  container.addEventListener('dragover', handleMaybeDragOver);
  container.addEventListener('dragenter', handleMaybeDragEnter);
  container.addEventListener('dragleave', handleMaybeDragLeave);
  container.addEventListener('drop', handleMaybeDrop);
  
  container.querySelectorAll('.maybe-drag-handle').forEach(handle => {
    handle.draggable = true;
    handle.addEventListener('dragstart', handleMaybeDragStart);
    handle.addEventListener('dragend', handleMaybeDragEnd);
  });
}

function handleMaybeDragEnter(e) {
  e.preventDefault();
  // Only highlight if dragging a maybe task
  if (!draggedMaybeTask) return;
  const container = e.currentTarget;
  container.classList.add('drag-over');
}

function handleMaybeDragLeave(e) {
  const container = e.currentTarget;
  // Only remove if leaving the container entirely (not entering a child)
  if (!container.contains(e.relatedTarget)) {
    container.classList.remove('drag-over');
  }
}

function handleMaybeDragStart(e) {
  const card = e.target.closest('.maybe-card');
  if (!card) return;
  
  draggedMaybeTask = {
    id: parseInt(card.dataset.taskId),
    element: card
  };
  
  card.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  console.log('[Maybe Drag] Started:', draggedMaybeTask);
}

function handleMaybeDragEnd(e) {
  const card = e.target.closest('.maybe-card');
  if (card) {
    card.classList.remove('dragging');
  }
  // Clean up all highlights
  document.querySelectorAll('.maybe-card').forEach(c => {
    c.classList.remove('drag-over');
  });
  document.querySelectorAll('.maybe-list').forEach(el => {
    el.classList.remove('drag-over');
  });
  draggedMaybeTask = null;
}

function handleMaybeDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';

  if (!draggedMaybeTask) return;

  const container = e.currentTarget;
  const afterElement = getDragAfterElement(container, e.clientY, '.maybe-card', e.clientX);

  // Clear previous highlights
  container.querySelectorAll('.maybe-card').forEach(card => {
    card.classList.remove('drag-over');
  });

  // Highlight the target position
  if (afterElement) {
    afterElement.classList.add('drag-over');
  } else {
    // If no afterElement, highlight the last card or indicate append
    const cards = container.querySelectorAll('.maybe-card:not(.dragging)');
    if (cards.length > 0) {
      cards[cards.length - 1].classList.add('drag-over');
    }
  }
}

async function handleMaybeDrop(e) {
  e.preventDefault();

  if (!draggedMaybeTask) return;

  const container = e.currentTarget;
  const taskId = draggedMaybeTask.id;

  // Find insert position
  // UI highlights a card to indicate "place dragged item HERE"
  const targetElement = getDragAfterElement(container, e.clientY, '.maybe-card', e.clientX);
  let insertIndex = -1; // -1 means append to end

  if (targetElement) {
    const allCards = [...container.querySelectorAll('.maybe-card')];
    const targetTaskId = parseInt(targetElement.dataset.taskId);
    const targetIdx = allCards.findIndex(c => parseInt(c.dataset.taskId) === targetTaskId);
    
    // Insert at the target card's position
    insertIndex = targetIdx;
  }

  // Clear highlights
  container.querySelectorAll('.maybe-card').forEach(card => {
    card.classList.remove('drag-over');
  });
  container.classList.remove('drag-over');

  console.log('[Maybe Drop] Task:', taskId, 'at index', insertIndex);

  try {
    const response = await fetch('/api/maybe/reorder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskId, insertIndex })
    });

    if (!response.ok) {
      throw new Error('Failed to reorder: ' + response.statusText);
    }

    await fetchInitialData();

  } catch (error) {
    console.error('[Maybe Drop] Error:', error);
    await fetchInitialData();
  }
}

// Custom Confirm Function
function showConfirm(message, onConfirm) {
  // Prevent multiple dialogs
  if (document.getElementById('customConfirmOverlay')) {
    return;
  }

  const overlay = document.createElement('div');
  overlay.id = 'customConfirmOverlay';
  overlay.className = 'custom-alert-overlay';

  overlay.innerHTML = `
    <div class="custom-alert-modal">
      <div class="custom-alert-message">${escapeHtml(message)}</div>
      <div class="custom-confirm-actions">
        <button class="custom-alert-btn custom-confirm-cancel">Cancel</button>
        <button class="custom-alert-btn custom-confirm-ok">OK</button>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);

  const btnOk = overlay.querySelector('.custom-confirm-ok');
  const btnCancel = overlay.querySelector('.custom-confirm-cancel');
  
  let isClosing = false;
  
  const closeConfirm = () => {
    if (isClosing) return;
    isClosing = true;
    
    document.removeEventListener('keydown', handleKeydown);
    overlay.classList.remove('show');
    
    setTimeout(() => {
      if (overlay.parentNode) {
        overlay.remove();
      }
    }, 200);
  };

  const handleKeydown = (e) => {
    if (isClosing) return;
    
    if (e.key === 'Escape') {
      e.preventDefault();
      e.stopPropagation();
      closeConfirm();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      e.stopPropagation();
      closeConfirm();
      if (onConfirm) onConfirm();
    }
  };

  btnOk.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    closeConfirm();
    if (onConfirm) onConfirm();
  });

  btnCancel.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    closeConfirm();
  });
  
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      closeConfirm();
    }
  });

  document.addEventListener('keydown', handleKeydown);

  // Trigger animation
  requestAnimationFrame(() => {
    overlay.classList.add('show');
    // Remove focus to prevent Enter key double trigger
    btnCancel.blur();
    btnOk.blur();
  });
}
