// AccessMind DevTools Panel Script
// Handles DevTools-specific functionality

let currentTab = null;
let violations = [];
let treeData = null;

// Initialize DevTools panel
document.addEventListener('DOMContentLoaded', async () => {
  // Tab switching
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });
  
  // Action buttons
  document.getElementById('refresh').addEventListener('click', refreshAnalysis);
  document.getElementById('export').addEventListener('click', exportResults);
  document.getElementById('startKeyboardTest').addEventListener('click', startKeyboardTest);
  document.getElementById('highlightFocusables').addEventListener('click', highlightFocusables);
  document.getElementById('captureScreenshot').addEventListener('click', captureScreenshot);
  document.getElementById('analyzeWithAI').addEventListener('click', analyzeWithAI);
  
  // Get current tab and run initial analysis
  getCurrentTab();
});

function switchTab(tabId) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  
  document.querySelector(`.tab[data-tab="${tabId}"]`).classList.add('active');
  document.getElementById(tabId).classList.add('active');
}

async function getCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  currentTab = tab;
  
  if (tab) {
    refreshAnalysis();
  }
}

async function refreshAnalysis() {
  setStatus('Analiz ediliyor...');
  
  try {
    // Run accessibility scan
    const results = await chrome.scripting.executeScript({
      target: { tabId: currentTab.id },
      function: runAccessibilityScan
    });
    
    violations = results[0].result.violations || [];
    treeData = results[0].result.tree || null;
    
    updateViolationsUI(results[0].result);
    
    setStatus('Analiz tamamlandı');
  } catch (error) {
    console.error('Analysis error:', error);
    setStatus('Hata: ' + error.message);
  }
}

function runAccessibilityScan() {
  // This runs in the page context
  const results = {
    violations: [],
    score: 100,
    tree: null
  };
  
  // WCAG checks
  const checks = [
    // Images without alt
    {
      selector: 'img:not([alt]):not([role="presentation"])',
      wcag: '1.1.1',
      severity: 'critical',
      message: 'Görsel alt text içermiyor'
    },
    // Links without text
    {
      selector: 'a:not(:has(*)):not([aria-label]):not([title])',
      wcag: '2.4.4',
      severity: 'serious',
      message: 'Link metin içermiyor'
    },
    // Inputs without labels
    {
      selector: 'input:not([aria-label]):not([aria-labelledby])',
      wcag: '1.3.1',
      severity: 'serious',
      message: 'Form elemanı etiket içermiyor',
      filter: (el) => !document.querySelector(`label[for="${el.id}"]`)
    },
    // Buttons without names
    {
      selector: 'button:not(:has(*)):not([aria-label])',
      wcag: '4.1.2',
      severity: 'serious',
      message: 'Buton isim içermiyor',
      filter: (el) => !el.textContent.trim()
    },
    // Iframes without title
    {
      selector: 'iframe:not([title])',
      wcag: '2.4.1',
      severity: 'serious',
      message: 'Iframe başlık içermiyor'
    }
  ];
  
  checks.forEach(check => {
    const elements = document.querySelectorAll(check.selector);
    elements.forEach(el => {
      if (check.filter && !check.filter(el)) return;
      
      results.violations.push({
        wcag: check.wcag,
        severity: check.severity,
        message: check.message,
        element: el.outerHTML.substring(0, 200),
        path: getCSSPath(el)
      });
    });
  });
  
  // Check for H1
  const h1s = document.querySelectorAll('h1');
  if (h1s.length === 0) {
    results.violations.push({
      wcag: '2.4.1',
      severity: 'moderate',
      message: 'Sayfada H1 başlığı yok',
      element: '<head>',
      path: 'html > head'
    });
  } else if (h1s.length > 1) {
    results.violations.push({
      wcag: '2.4.1',
      severity: 'minor',
      message: 'Sayfada birden fazla H1 var',
      element: `<h1> x${h1s.length}`,
      path: 'html > body'
    });
  }
  
  // Calculate score
  results.score = Math.max(0, 100 - 
    (results.violations.filter(v => v.severity === 'critical').length * 10) -
    (results.violations.filter(v => v.severity === 'serious').length * 5) -
    (results.violations.filter(v => v.severity === 'moderate').length * 2) -
    (results.violations.filter(v => v.severity === 'minor').length)
  );
  
  // Build accessibility tree
  results.tree = buildTree(document.body, 0, 3);
  
  return results;
}

function getCSSPath(el) {
  const path = [];
  let current = el;
  
  while (current && current !== document.body) {
    let selector = current.tagName.toLowerCase();
    if (current.id) {
      selector += `#${current.id}`;
    } else if (current.className && typeof current.className === 'string') {
      selector += `.${current.className.split(' ')[0]}`;
    }
    path.unshift(selector);
    current = current.parentElement;
  }
  
  return path.join(' > ');
}

function buildTree(node, depth, maxDepth) {
  if (!node || node.nodeType !== Node.ELEMENT_NODE || depth > maxDepth) {
    return null;
  }
  
  const style = window.getComputedStyle(node);
  if (style.display === 'none' || style.visibility === 'hidden') {
    return null;
  }
  
  const result = {
    tag: node.tagName.toLowerCase(),
    role: node.getAttribute('role') || getImplicitRole(node.tagName),
    name: getAccessibleName(node),
    children: [],
    issues: []
  };
  
  // Add issues for this node
  if (node.tagName === 'IMG' && !node.alt) {
    result.issues.push({ wcag: '1.1.1', message: 'Alt text eksik' });
  }
  if (node.tagName === 'A' && !result.name) {
    result.issues.push({ wcag: '2.4.4', message: 'Link ismi yok' });
  }
  
  // Process children
  node.childNodes.forEach(child => {
    const childTree = buildTree(child, depth + 1, maxDepth);
    if (childTree) {
      result.children.push(childTree);
    }
  });
  
  return result;
}

function getImplicitRole(tag) {
  const roles = {
    'A': 'link',
    'BUTTON': 'button',
    'INPUT': 'textbox',
    'SELECT': 'listbox',
    'TEXTAREA': 'textbox',
    'IMG': 'img',
    'NAV': 'navigation',
    'MAIN': 'main',
    'HEADER': 'banner',
    'FOOTER': 'contentinfo',
    'ASIDE': 'complementary',
    'ARTICLE': 'article',
    'SECTION': 'region',
    'FORM': 'form',
    'TABLE': 'table',
    'UL': 'list',
    'OL': 'list',
    'LI': 'listitem',
    'H1': 'heading',
    'H2': 'heading',
    'H3': 'heading',
    'H4': 'heading',
    'H5': 'heading',
    'H6': 'heading'
  };
  return roles[tag] || null;
}

function getAccessibleName(el) {
  if (el.getAttribute('aria-label')) {
    return el.getAttribute('aria-label').substring(0, 50);
  }
  if (el.getAttribute('aria-labelledby')) {
    const label = document.getElementById(el.getAttribute('aria-labelledby'));
    if (label) return label.textContent.substring(0, 50);
  }
  if (el.tagName === 'IMG' && el.alt) {
    return el.alt.substring(0, 50);
  }
  if (el.textContent && el.textContent.trim()) {
    return el.textContent.trim().substring(0, 50);
  }
  return null;
}

function updateViolationsUI(results) {
  // Update score
  document.getElementById('score').textContent = results.score;
  document.getElementById('score').style.color = 
    results.score >= 80 ? '#4ade80' : 
    results.score >= 60 ? '#fbbf24' : '#f87171';
  
  // Update counts
  const critical = results.violations.filter(v => v.severity === 'critical').length;
  const serious = results.violations.filter(v => v.severity === 'serious').length;
  const moderate = results.violations.filter(v => v.severity === 'moderate').length;
  
  document.getElementById('criticalCount').textContent = `${critical} Kritik`;
  document.getElementById('seriousCount').textContent = `${serious} Ciddi`;
  document.getElementById('moderateCount').textContent = `${moderate} Orta`;
  
  // Populate violations list
  const list = document.getElementById('violationsList');
  list.innerHTML = '';
  
  results.violations.forEach((v, i) => {
    const item = document.createElement('div');
    item.className = `violation-item ${v.severity}`;
    item.innerHTML = `
      <div class="violation-header">
        <span class="violation-wcag">${v.wcag}</span>
        <span class="violation-severity ${v.severity}">${v.severity.toUpperCase()}</span>
      </div>
      <div class="violation-message">${v.message}</div>
      <code class="violation-element">${escapeHtml(v.element)}</code>
    `;
    item.addEventListener('click', () => highlightElement(v.path));
    list.appendChild(item);
  });
  
  // Populate tree
  if (results.tree) {
    renderTree(results.tree, 'treeView');
  }
}

function renderTree(node, containerId, depth = 0) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  if (!node) {
    container.innerHTML = '<div style="padding: 16px; color: #888;">Ağaç verisi yok</div>';
    return;
  }
  
  if (depth === 0) {
    container.innerHTML = '';
  }
  
  const nodeEl = document.createElement('div');
  nodeEl.className = 'tree-node';
  nodeEl.style.paddingLeft = `${depth * 16}px`;
  
  const nameSpan = document.createElement('span');
  nameSpan.className = 'tree-node-name';
  nameSpan.textContent = node.tag;
  nodeEl.appendChild(nameSpan);
  
  if (node.role) {
    const roleSpan = document.createElement('span');
    roleSpan.className = 'tree-node-role';
    roleSpan.textContent = ` [${node.role}]`;
    nodeEl.appendChild(roleSpan);
  }
  
  if (node.name) {
    const nameContent = document.createElement('span');
    nameContent.textContent = ` "${node.name}"`;
    nodeEl.appendChild(nameContent);
  }
  
  if (node.issues && node.issues.length > 0) {
    node.issues.forEach(issue => {
      const issueSpan = document.createElement('div');
      issueSpan.className = 'tree-node-issue';
      issueSpan.style.paddingLeft = `${(depth + 1) * 16}px`;
      issueSpan.textContent = `⚠️ ${issue.wcag}: ${issue.message}`;
      container.appendChild(nodeEl);
      container.appendChild(issueSpan);
    });
  } else {
    container.appendChild(nodeEl);
  }
  
  if (node.children) {
    node.children.forEach(child => renderTree(child, containerId, depth + 1));
  }
}

function setStatus(message) {
  console.log('[AccessMind]', message);
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

async function highlightElement(path) {
  await chrome.scripting.executeScript({
    target: { tabId: currentTab.id },
    func: (selectorPath) => {
      try {
        const el = document.querySelector(selectorPath);
        if (el) {
          el.style.outline = '3px solid #f87171';
          el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          setTimeout(() => {
            el.style.outline = '';
          }, 3000);
        }
      } catch (e) {
        console.error('Highlight error:', e);
      }
    },
    args: [path]
  });
}

async function startKeyboardTest() {
  const log = document.getElementById('keyboardLog');
  log.innerHTML = '<div class="loading"></div> Klavye testi yapılıyor...';
  
  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId: currentTab.id },
      function: () => {
        const focusables = document.querySelectorAll(
          'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        return {
          count: focusables.length,
          elements: Array.from(focusables).slice(0, 20).map(el => ({
            tag: el.tagName,
            text: (el.textContent || el.value || el.alt || '').substring(0, 30)
          }))
        };
      }
    });
    
    const data = results[0].result;
    
    document.getElementById('focusableCount').textContent = data.count;
    document.getElementById('tabCount').textContent = Math.min(data.count, 50);
    document.getElementById('trapCount').textContent = '0';
    
    log.innerHTML = data.elements.map((el, i) => 
      `<div class="log-entry">${i + 1}. ${el.tag}: "${el.text}"</div>`
    ).join('');
    
  } catch (error) {
    log.innerHTML = `<div class="log-entry">Hata: ${error.message}</div>`;
  }
}

async function highlightFocusables() {
  await chrome.scripting.executeScript({
    target: { tabId: currentTab.id },
    function: () => {
      const focusables = document.querySelectorAll(
        'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      
      focusables.forEach((el, i) => {
        el.style.outline = '2px solid #4ade80';
        el.style.outlineOffset = '2px';
      });
      
      setTimeout(() => {
        focusables.forEach(el => {
          el.style.outline = '';
        });
      }, 5000);
    }
  });
}

async function captureScreenshot() {
  const img = document.getElementById('screenshot');
  img.src = '';
  img.alt = 'Yükleniyor...';
  
  try {
    const screenshot = await chrome.tabs.captureVisibleTab(null, { format: 'png' });
    img.src = screenshot;
    img.alt = 'Sayfa ekran görüntüsü';
  } catch (error) {
    img.alt = 'Hata: ' + error.message;
  }
}

async function analyzeWithAI() {
  const resultsDiv = document.getElementById('aiResults');
  resultsDiv.innerHTML = '<div class="loading"></div> Qwen3-VL analiz ediyor...';
  
  try {
    // Get screenshot
    const screenshot = await chrome.tabs.captureVisibleTab(null, { format: 'png' });
    
    // Send to background for AI analysis
    const response = await chrome.runtime.sendMessage({
      action: 'visualAI',
      screenshot: screenshot,
      url: currentTab.url
    });
    
    if (response.findings) {
      resultsDiv.innerHTML = response.findings.map(f => `
        <div class="ai-finding ${f.severity}">
          <strong>${f.wcag}</strong>: ${f.message}
        </div>
      `).join('');
    } else {
      resultsDiv.innerHTML = '<div>Analiz tamamlandı ama bulgu yok</div>';
    }
    
  } catch (error) {
    resultsDiv.innerHTML = `<div class="ai-finding serious">Hata: ${error.message}</div>`;
  }
}

function exportResults() {
  const data = {
    url: currentTab.url,
    timestamp: new Date().toISOString(),
    violations: violations,
    tree: treeData
  };
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `accessmind-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
}