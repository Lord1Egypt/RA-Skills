// AccessMind Inspector - Popup Script
// WCAG 2.2 Accessibility Inspector with Visual AI Analysis

let currentTab = null;
let scanResults = null;
let visualAIResults = null;

// Initialize popup
document.addEventListener('DOMContentLoaded', async () => {
  updateTimestamp();
  
  // Get current tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  currentTab = tab;
  
  if (tab) {
    document.getElementById('currentUrl').textContent = tab.url;
  }
  
  // Load saved results
  loadSavedResults();
  
  // Button event listeners
  document.getElementById('btnQuickScan').addEventListener('click', runQuickScan);
  document.getElementById('btnFullAudit').addEventListener('click', runFullAudit);
  document.getElementById('btnVisualAI').addEventListener('click', runVisualAI);
  document.getElementById('btnKeyboardNav').addEventListener('click', runKeyboardTest);
  document.getElementById('btnExportJSON').addEventListener('click', exportJSON);
  document.getElementById('btnExportHTML').addEventListener('click', exportHTML);
  document.getElementById('btnSettings').addEventListener('click', openSettings);
});

function updateTimestamp() {
  const now = new Date();
  document.getElementById('timestamp').textContent = 
    `${now.toLocaleDateString('tr-TR')} ${now.toLocaleTimeString('tr-TR')}`;
}

function setStatus(status, type = 'ready') {
  const indicator = document.getElementById('statusIndicator');
  const text = document.getElementById('statusText');
  
  indicator.className = 'status-indicator';
  if (type === 'scanning') indicator.classList.add('scanning');
  if (type === 'error') indicator.classList.add('error');
  
  text.textContent = status;
}

function loadSavedResults() {
  chrome.storage.local.get(['lastScan', 'visualAI'], (result) => {
    if (result.lastScan) {
      scanResults = result.lastScan;
      updateQuickResults(scanResults);
    }
    if (result.visualAI) {
      visualAIResults = result.visualAI;
      updateAIResults(visualAIResults);
    }
  });
}

// Quick Scan - Basic WCAG checks
async function runQuickScan() {
  setStatus('Hızlı tarama yapılıyor...', 'scanning');
  
  try {
    // Inject content script and run scan
    const results = await chrome.scripting.executeScript({
      target: { tabId: currentTab.id },
      function: performQuickScan
    });
    
    scanResults = results[0].result;
    updateQuickResults(scanResults);
    
    // Save results
    chrome.storage.local.set({ lastScan: scanResults });
    
    setStatus('Tarama tamamlandı', 'ready');
  } catch (error) {
    console.error('Quick scan error:', error);
    setStatus('Hata: ' + error.message, 'error');
  }
}

function performQuickScan() {
  // Run in page context
  const results = {
    url: window.location.href,
    timestamp: new Date().toISOString(),
    violations: [],
    passes: [],
    score: 100,
    critical: 0,
    serious: 0,
    moderate: 0,
    minor: 0
  };
  
  // Check for common WCAG violations
  
  // 1. Images without alt text (1.1.1)
  const images = document.querySelectorAll('img');
  images.forEach(img => {
    if (!img.alt && !img.getAttribute('aria-label') && !img.getAttribute('role')) {
      results.violations.push({
        wcag: '1.1.1',
        severity: 'critical',
        element: img.outerHTML.substring(0, 100),
        message: 'Görsel alt text içermiyor'
      });
      results.critical++;
    }
  });
  
  // 2. Links without accessible names (2.4.4)
  const links = document.querySelectorAll('a');
  links.forEach(link => {
    const text = link.textContent.trim();
    const ariaLabel = link.getAttribute('aria-label');
    const title = link.getAttribute('title');
    if (!text && !ariaLabel && !title && !link.querySelector('img[alt]')) {
      results.violations.push({
        wcag: '2.4.4',
        severity: 'serious',
        element: link.outerHTML.substring(0, 100),
        message: 'Link erişilebilir isim içermiyor'
      });
      results.serious++;
    }
  });
  
  // 3. Form inputs without labels (1.3.1)
  const inputs = document.querySelectorAll('input, select, textarea');
  inputs.forEach(input => {
    const id = input.id;
    const hasLabel = id && document.querySelector(`label[for="${id}"]`);
    const ariaLabel = input.getAttribute('aria-label');
    const ariaLabelledby = input.getAttribute('aria-labelledby');
    if (!hasLabel && !ariaLabel && !ariaLabelledby) {
      results.violations.push({
        wcag: '1.3.1',
        severity: 'serious',
        element: input.outerHTML.substring(0, 100),
        message: 'Form elemanı etiket içermiyor'
      });
      results.serious++;
    }
  });
  
  // 4. Missing H1 (2.4.1)
  const h1s = document.querySelectorAll('h1');
  if (h1s.length === 0) {
    results.violations.push({
      wcag: '2.4.1',
      severity: 'moderate',
      element: '<head>',
      message: 'Sayfada H1 başlığı yok'
    });
    results.moderate++;
  } else if (h1s.length > 1) {
    results.violations.push({
      wcag: '2.4.1',
      severity: 'minor',
      element: '<h1>',
      message: 'Sayfada birden fazla H1 var'
    });
    results.minor++;
  }
  
  // 5. Buttons without accessible names (4.1.2)
  const buttons = document.querySelectorAll('button');
  buttons.forEach(btn => {
    const text = btn.textContent.trim();
    const ariaLabel = btn.getAttribute('aria-label');
    const ariaLabelledby = btn.getAttribute('aria-labelledby');
    const title = btn.getAttribute('title');
    if (!text && !ariaLabel && !ariaLabelledby && !title) {
      results.violations.push({
        wcag: '4.1.2',
        severity: 'serious',
        element: btn.outerHTML.substring(0, 100),
        message: 'Buton erişilebilir isim içermiyor'
      });
      results.serious++;
    }
  });
  
  // 6. Skip links (2.4.1)
  const skipLinks = document.querySelectorAll('a[href^="#"]');
  const hasSkipLink = Array.from(skipLinks).some(link => 
    link.textContent.toLowerCase().includes('atla') ||
    link.textContent.toLowerCase().includes('skip')
  );
  if (!hasSkipLink) {
    results.violations.push({
      wcag: '2.4.1',
      severity: 'moderate',
      element: '<body>',
      message: 'Skip link yok'
    });
    results.moderate++;
  }
  
  // 7. ARIA landmarks (1.3.1)
  const landmarks = document.querySelectorAll('main, nav, aside, header, footer, [role="main"], [role="navigation"], [role="complementary"]');
  if (landmarks.length === 0) {
    results.violations.push({
      wcag: '1.3.1',
      severity: 'moderate',
      element: '<body>',
      message: 'ARIA landmark yok'
    });
    results.moderate++;
  }
  
  // 8. Iframes without title (2.4.1)
  const iframes = document.querySelectorAll('iframe');
  iframes.forEach(iframe => {
    if (!iframe.title) {
      results.violations.push({
        wcag: '2.4.1',
        severity: 'serious',
        element: iframe.outerHTML.substring(0, 100),
        message: 'Iframe başlık içermiyor'
      });
      results.serious++;
    }
  });
  
  // Calculate score
  results.score = Math.max(0, 100 - (results.critical * 10) - (results.serious * 5) - (results.moderate * 2) - results.minor);
  
  // Count passes
  results.passes = [
    images.length - results.violations.filter(v => v.wcag === '1.1.1').length,
    links.length - results.violations.filter(v => v.wcag === '2.4.4').length,
    inputs.length - results.violations.filter(v => v.wcag === '1.3.1' && v.element.includes('input')).length
  ];
  
  return results;
}

function updateQuickResults(results) {
  document.getElementById('overallScore').textContent = results.score;
  document.getElementById('criticalCount').textContent = results.critical;
  document.getElementById('seriousCount').textContent = results.serious;
  document.getElementById('moderateCount').textContent = results.moderate;
  
  // Color based on score
  const scoreEl = document.getElementById('overallScore');
  if (results.score >= 80) {
    scoreEl.style.color = '#4ade80';
  } else if (results.score >= 60) {
    scoreEl.style.color = '#fbbf24';
  } else {
    scoreEl.style.color = '#f87171';
  }
}

// Full Audit - Comprehensive WCAG testing
async function runFullAudit() {
  setStatus('Tam denetim yapılıyor...', 'scanning');
  
  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId: currentTab.id },
      function: performFullAudit
    });
    
    scanResults = results[0].result;
    updateQuickResults(scanResults);
    
    chrome.storage.local.set({ lastScan: scanResults });
    
    setStatus('Denetim tamamlandı', 'ready');
  } catch (error) {
    console.error('Full audit error:', error);
    setStatus('Hata: ' + error.message, 'error');
  }
}

function performFullAudit() {
  // Comprehensive audit implementation
  const quickResults = performQuickScan();
  
  // Add more detailed checks
  
  // Keyboard navigation check
  const focusables = document.querySelectorAll('a, button, input, select, textarea, [tabindex]');
  quickResults.focusableCount = focusables.length;
  
  // Heading hierarchy check
  const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
  let prevLevel = 0;
  headings.forEach(h => {
    const level = parseInt(h.tagName.charAt(1));
    if (level > prevLevel + 1) {
      quickResults.violations.push({
        wcag: '1.3.1',
        severity: 'moderate',
        element: h.outerHTML.substring(0, 100),
        message: `H${level} başlığı H${prevLevel}'dan sonra gelmemeli`
      });
      quickResults.moderate++;
    }
    prevLevel = level;
  });
  
  // Color contrast check (simplified)
  const textElements = document.querySelectorAll('p, span, a, button, h1, h2, h3, h4, h5, h6');
  quickResults.textElements = textElements.length;
  
  // ARIA attributes check
  const ariaElements = document.querySelectorAll('[aria-label], [aria-labelledby], [aria-describedby], [role]');
  quickResults.ariaElements = ariaElements.length;
  
  // Live regions check
  const liveRegions = document.querySelectorAll('[aria-live], [role="alert"], [role="status"]');
  quickResults.liveRegions = liveRegions.length;
  
  // Recalculate score
  quickResults.score = Math.max(0, 100 - 
    (quickResults.critical * 10) - 
    (quickResults.serious * 5) - 
    (quickResults.moderate * 2) - 
    quickResults.minor
  );
  
  return quickResults;
}

// Visual AI Analysis - Qwen3-VL integration
async function runVisualAI() {
  setStatus('Görsel AI analizi yapılıyor...', 'scanning');
  document.getElementById('aiStatus').innerHTML = '<span class="loading"></span> Qwen3-VL analiz ediyor...';
  
  try {
    // First, capture screenshot
    const screenshot = await chrome.tabs.captureVisibleTab(null, { format: 'png' });
    
    // Send to background script for processing
    const response = await chrome.runtime.sendMessage({
      action: 'visualAI',
      screenshot: screenshot,
      url: currentTab.url
    });
    
    visualAIResults = response;
    updateAIResults(visualAIResults);
    
    chrome.storage.local.set({ visualAI: visualAIResults });
    
    setStatus('Görsel analiz tamamlandı', 'ready');
  } catch (error) {
    console.error('Visual AI error:', error);
    setStatus('Hata: ' + error.message, 'error');
    document.getElementById('aiStatus').textContent = 'Hata: ' + error.message;
  }
}

function updateAIResults(results) {
  document.getElementById('aiStatus').style.display = 'none';
  document.getElementById('aiResults').style.display = 'block';
  
  const findingsList = document.getElementById('aiFindings');
  findingsList.innerHTML = '';
  
  results.findings.forEach(finding => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${finding.wcag}</strong>: ${finding.message}`;
    li.style.borderLeftColor = finding.severity === 'critical' ? '#f87171' : 
                               finding.severity === 'serious' ? '#fbbf24' : '#60a5fa';
    findingsList.appendChild(li);
  });
}

// Keyboard Navigation Test
async function runKeyboardTest() {
  setStatus('Klavye testi yapılıyor...', 'scanning');
  document.getElementById('keyboardStatus').innerHTML = '<span class="loading"></span> Tab simülasyonu...';
  
  try {
    const results = await chrome.scripting.executeScript({
      target: { tabId: currentTab.id },
      function: performKeyboardTest
    });
    
    const keyboardResults = results[0].result;
    updateKeyboardResults(keyboardResults);
    
    setStatus('Klavye testi tamamlandı', 'ready');
  } catch (error) {
    console.error('Keyboard test error:', error);
    setStatus('Hata: ' + error.message, 'error');
  }
}

function performKeyboardTest() {
  const focusables = document.querySelectorAll(
    'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const results = {
    totalFocusable: focusables.length,
    tabStops: [],
    traps: []
  };
  
  // Simulate Tab navigation
  let currentFocusIndex = -1;
  
  focusables.forEach((el, index) => {
    const rect = el.getBoundingClientRect();
    const styles = window.getComputedStyle(el);
    
    const tabStop = {
      index: index + 1,
      tagName: el.tagName,
      text: el.textContent?.substring(0, 50) || el.alt || el.placeholder || '',
      hasVisibleFocus: styles.outline !== 'none' || styles.boxShadow !== 'none',
      isVisible: rect.width > 0 && rect.height > 0,
      isOffScreen: rect.top < 0 || rect.left < 0 || rect.bottom > window.innerHeight
    };
    
    results.tabStops.push(tabStop);
  });
  
  // Check for potential traps (elements with tabindex > 0 at the end)
  const highTabIndex = Array.from(focusables).filter(el => {
    const tabindex = parseInt(el.getAttribute('tabindex') || 0);
    return tabindex > 0;
  });
  
  if (highTabIndex.length > 0 && highTabIndex.length === focusables.length) {
    results.traps.push({
      type: 'tabindex_trap',
      message: 'Tüm elementler yüksek tabindex değerine sahip'
    });
  }
  
  return results;
}

function updateKeyboardResults(results) {
  document.getElementById('keyboardStatus').style.display = 'none';
  document.getElementById('keyboardStats').style.display = 'grid';
  
  document.getElementById('tabCount').textContent = results.tabStops.length;
  document.getElementById('focusableCount').textContent = results.totalFocusable;
  document.getElementById('trapCount').textContent = results.traps.length;
  
  // Color based on traps
  const trapEl = document.getElementById('trapCount');
  trapEl.style.color = results.traps.length > 0 ? '#f87171' : '#4ade80';
}

// Export Functions
function exportJSON() {
  if (!scanResults) {
    alert('Önce bir tarama yapın');
    return;
  }
  
  const blob = new Blob([JSON.stringify(scanResults, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `accessmind-audit-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
}

function exportHTML() {
  if (!scanResults) {
    alert('Önce bir tarama yapın');
    return;
  }
  
  const html = generateHTMLReport(scanResults);
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `accessmind-report-${new Date().toISOString().split('T')[0]}.html`;
  a.click();
}

function generateHTMLReport(results) {
  return `
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>AccessMind Erişilebilirlik Raporu</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #fff; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
    .score-card { display: inline-block; background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 10px; text-align: center; }
    .score { font-size: 48px; font-weight: 700; }
    .violation { background: #fff5f5; border-left: 4px solid #f87171; padding: 15px; margin: 10px 0; border-radius: 5px; }
    .wcag { font-weight: 600; color: #666; }
    .severity-critical { border-left-color: #f87171; }
    .severity-serious { border-left-color: #fbbf24; }
    .severity-moderate { border-left-color: #60a5fa; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🔍 AccessMind Erişilebilirlik Raporu</h1>
    <p>${results.url}</p>
    <p>Tarih: ${new Date(results.timestamp).toLocaleString('tr-TR')}</p>
  </div>
  
  <div class="scores">
    <div class="score-card">
      <div class="score" style="color: ${results.score >= 80 ? '#4ade80' : results.score >= 60 ? '#fbbf24' : '#f87171'}">${results.score}</div>
      <div>Genel Skor</div>
    </div>
    <div class="score-card">
      <div class="score" style="color: #f87171">${results.critical}</div>
      <div>Kritik</div>
    </div>
    <div class="score-card">
      <div class="score" style="color: #fbbf24">${results.serious}</div>
      <div>Ciddi</div>
    </div>
    <div class="score-card">
      <div class="score" style="color: #60a5fa">${results.moderate}</div>
      <div>Orta</div>
    </div>
  </div>
  
  <h2>İhlaller</h2>
  ${results.violations.map(v => `
    <div class="violation severity-${v.severity}">
      <span class="wcag">WCAG ${v.wcag}</span> - <strong>${v.severity.toUpperCase()}</strong>
      <p>${v.message}</p>
      <code>${v.element}</code>
    </div>
  `).join('')}
</body>
</html>
  `;
}

function openSettings() {
  chrome.runtime.openOptionsPage();
}