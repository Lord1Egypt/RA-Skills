// AccessMind Inspector - Background Script (Service Worker)
// Handles Visual AI analysis via Qwen3-VL and OpenClaw Gateway
// v1.1 - Behavioral Audit Integration

const OPENCLAW_GATEWAY = 'http://127.0.0.1:8765'; // OpenClaw Gateway endpoint
const QWEN_MODEL = 'qwen3-vl:latest';
const BEHAVIORAL_BRIDGE = '/Users/sarper/.openclaw/workspace/skills/accessmind/scripts/accessmind-behavioral-bridge.py';

// Behavioral events storage
let behavioralEvents = [];
let currentPage = '';

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'visualAI') {
    handleVisualAIRequest(request.screenshot, request.url)
      .then(sendResponse)
      .catch(error => sendResponse({ error: error.message }));
    return true; // Keep the message channel open for async response
  }
  
  if (request.action === 'getPageContent') {
    // Get page content for analysis
    chrome.scripting.executeScript({
      target: { tabId: request.tabId },
      function: getPageContent
    }).then(results => {
      sendResponse(results[0].result);
    }).catch(error => {
      sendResponse({ error: error.message });
    });
    return true;
  }
});

async function handleVisualAIRequest(screenshot, url) {
  try {
    // First, try to send to OpenClaw Gateway
    const gatewayResponse = await sendToGateway(screenshot, url);
    
    if (gatewayResponse) {
      return {
        source: 'gateway',
        findings: gatewayResponse.findings,
        screenshot: screenshot,
        timestamp: new Date().toISOString()
      };
    }
  } catch (gatewayError) {
    console.log('Gateway not available, using local analysis:', gatewayError.message);
  }
  
  // Fallback to local analysis
  return performLocalVisualAnalysis(screenshot, url);
}

async function sendToGateway(screenshot, url) {
  try {
    const response = await fetch(`${OPENCLAW_GATEWAY}/api/visual-analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        image: screenshot,
        url: url,
        model: QWEN_MODEL,
        analysis_type: 'accessibility'
      })
    });
    
    if (!response.ok) {
      throw new Error(`Gateway error: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    // Gateway not available
    throw error;
  }
}

async function performLocalVisualAnalysis(screenshot, url) {
  // Use Ollama directly for visual analysis
  // This requires Ollama to be running locally with qwen3-vl model
  
  const prompt = `Analyze this webpage screenshot for accessibility issues. Check for:
1. Color contrast issues
2. Missing alt text on images
3. Readable font sizes
4. Visible focus indicators
5. Proper heading hierarchy
6. Clear link text
7. Form label visibility
8. Skip links presence

Format your response as a JSON object with:
{
  "findings": [
    {"wcag": "WCAG criterion", "severity": "critical|serious|moderate|minor", "message": "Description"}
  ],
  "overall_assessment": "Brief summary"
}`;

  try {
    // Try local Ollama API
    const ollamaResponse = await fetch('http://127.0.0.1:11434/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: QWEN_MODEL,
        prompt: prompt,
        images: [screenshot.replace('data:image/png;base64,', '')],
        stream: false
      })
    });
    
    if (!ollamaResponse.ok) {
      throw new Error(`Ollama error: ${ollamaResponse.status}`);
    }
    
    const data = await ollamaResponse.json();
    
    // Parse the response
    const analysisText = data.response;
    const jsonMatch = analysisText.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      return {
        source: 'ollama',
        findings: parsed.findings || [],
        overall_assessment: parsed.overall_assessment || analysisText,
        screenshot: screenshot,
        timestamp: new Date().toISOString()
      };
    }
    
    // Fallback if JSON parsing fails
    return {
      source: 'ollama',
      findings: [{
        wcag: '1.4.3',
        severity: 'moderate',
        message: 'Görsel analiz tamamlandı - manuel doğrulama gerekli'
      }],
      raw_response: analysisText,
      screenshot: screenshot,
      timestamp: new Date().toISOString()
    };
    
  } catch (ollamaError) {
    console.error('Ollama error:', ollamaError);
    
    // Ultimate fallback - heuristic analysis
    return {
      source: 'heuristic',
      findings: [
        {
          wcag: '1.4.3',
          severity: 'moderate',
          message: 'Contrast (Minimum): Görsel analiz için Qwen3-VL veya OpenClaw Gateway gerekli'
        },
        {
          wcag: '1.4.4',
          severity: 'minor',
          message: 'Resize Text: Font boyutları manuel kontrol edilmeli'
        },
        {
          wcag: '2.4.7',
          severity: 'serious',
          message: 'Focus Visible: Focus göstergeleri görsel olarak kontrol edilmeli'
        }
      ],
      note: 'Ollama sunucusu çalışmıyor. Qwen3-VL modeli için "ollama run qwen3-vl" komutunu çalıştırın.',
      screenshot: screenshot,
      timestamp: new Date().toISOString()
    };
  }
}

function getPageContent() {
  // Get page content for analysis
  return {
    title: document.title,
    url: window.location.href,
    html: document.documentElement.outerHTML,
    headings: Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => ({
      tag: h.tagName,
      text: h.textContent.substring(0, 100)
    })),
    images: Array.from(document.querySelectorAll('img')).map(img => ({
      src: img.src,
      alt: img.alt,
      hasAlt: !!img.alt
    })),
    links: Array.from(document.querySelectorAll('a')).map(a => ({
      href: a.href,
      text: a.textContent.substring(0, 50),
      hasText: !!a.textContent.trim()
    })),
    forms: Array.from(document.querySelectorAll('form')).map(form => ({
      action: form.action,
      inputs: Array.from(form.querySelectorAll('input, select, textarea')).map(input => ({
        type: input.type,
        name: input.name,
        hasLabel: !!input.labels?.length || !!input.getAttribute('aria-label')
      }))
    }))
  };
}

// Behavioral event tracking
function trackBehavioralEvent(eventType, elementData, success = true) {
  const event = {
    type: eventType,
    element_ref: elementData.ref || '',
    element_tag: elementData.tag || '',
    element_role: elementData.role || '',
    timestamp: new Date().toISOString(),
    success: success,
    context: {
      has_label: elementData.hasLabel || false,
      focus_visible: elementData.focusVisible || false,
      aria_label: elementData.ariaLabel || '',
      accessible_name: elementData.accessibleName || ''
    }
  };
  
  behavioralEvents.push(event);
  
  // Store for later analysis
  chrome.storage.local.get(['behavioralEvents'], (result) => {
    const existing = result.behavioralEvents || [];
    existing.push(event);
    // Keep last 1000 events
    if (existing.length > 1000) {
      existing.splice(0, existing.length - 1000);
    }
    chrome.storage.local.set({ behavioralEvents: existing });
  });
  
  return event;
}

// Analyze behavioral patterns
function analyzeBehavioralPatterns() {
  return new Promise((resolve) => {
    chrome.storage.local.get(['behavioralEvents'], (result) => {
      const events = result.behavioralEvents || [];
      
      // Common errors
      const errorCounts = {};
      events.filter(e => !e.success).forEach(e => {
        const key = `${e.element_tag}:${e.element_role}`;
        errorCounts[key] = (errorCounts[key] || 0) + 1;
      });
      
      // Navigation flow
      const navEvents = events.filter(e => e.type === 'keyboard_navigation');
      const navigationFlow = navEvents.slice(-20).map(e => ({
        ref: e.element_ref,
        tag: e.element_tag,
        focus_visible: e.context.focus_visible
      }));
      
      // Focus trap detection
      const focusHistory = navEvents.slice(-50).map(e => e.element_ref);
      const hasTrap = detectFocusTrap(focusHistory);
      
      resolve({
        totalEvents: events.length,
        commonErrors: Object.entries(errorCounts)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5)
          .reduce((obj, [k, v]) => ({ ...obj, [k]: v }), {}),
        navigationFlow: navigationFlow,
        focusTrapDetected: hasTrap,
        successRate: events.length > 0 
          ? events.filter(e => e.success).length / events.length 
          : 1
      });
    });
  });
}

// Detect focus traps
function detectFocusTrap(focusHistory) {
  if (focusHistory.length < 3) return false;
  
  // Check for repeating pattern
  const last5 = focusHistory.slice(-5);
  const unique = new Set(last5);
  
  // If same 3 elements repeat, it's likely a trap
  if (unique.size <= 2 && last5.length >= 5) {
    return true;
  }
  
  // Check if focus never reaches new elements after 20 steps
  const last20 = focusHistory.slice(-20);
  const allUnique = new Set(last20);
  if (allUnique.size <= 5 && focusHistory.length >= 20) {
    return true;
  }
  
  return false;
}

// Export behavioral data for analysis
function exportBehavioralData() {
  return new Promise((resolve) => {
    chrome.storage.local.get(['behavioralEvents', 'currentPage'], (result) => {
      resolve({
        url: result.currentPage || '',
        events: result.behavioralEvents || [],
        exportedAt: new Date().toISOString()
      });
    });
  });
}

// Install handler
chrome.runtime.onInstalled.addListener(() => {
  console.log('AccessMind Inspector v1.1 installed');
  
  // Set default settings
  chrome.storage.local.set({
    settings: {
      autoScan: false,
      showOverlay: true,
      highlightViolations: true,
      apiEndpoint: OPENCLAW_GATEWAY,
      model: QWEN_MODEL,
      trackBehavior: true,  // New: Enable behavioral tracking
      sendToSkill: true      // New: Send events to skill
    },
    behavioralEvents: [],
    currentPage: ''
  });
});

// Context menu for right-click analysis
chrome.contextMenus.create({
  id: 'analyze-element',
  title: 'Erişilebilirlik Analizi Yap',
  contexts: ['all']
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'analyze-element') {
    // Inject script to analyze clicked element
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: analyzeClickedElement
    });
  }
});

function analyzeClickedElement() {
  // Get the element under cursor
  const element = document.activeElement;
  
  if (!element) {
    console.log('No element selected');
    return;
  }
  
  // Perform accessibility analysis on this element
  const analysis = {
    tagName: element.tagName,
    hasAlt: element.tagName === 'IMG' ? !!element.alt : null,
    hasAriaLabel: !!element.getAttribute('aria-label'),
    tabIndex: element.tabIndex,
    isVisible: element.offsetParent !== null,
    focusable: element.tabIndex >= 0
  };
  
  console.log('Element analysis:', analysis);
  
  // Show notification
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #1a1a2e;
    color: #fff;
    padding: 16px;
    border-radius: 8px;
    z-index: 10000;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  `;
  notification.innerHTML = `
    <h3 style="margin: 0 0 8px 0;">🔍 Element Analizi</h3>
    <p style="margin: 4px 0;"><strong>Tag:</strong> ${analysis.tagName}</p>
    <p style="margin: 4px 0;"><strong>Alt Text:</strong> ${analysis.hasAlt === null ? 'N/A' : (analysis.hasAlt ? '✅ Var' : '❌ Yok')}</p>
    <p style="margin: 4px 0;"><strong>ARIA Label:</strong> ${analysis.hasAriaLabel ? '✅ Var' : '❌ Yok'}</p>
    <p style="margin: 4px 0;"><strong>Tab Index:</strong> ${analysis.tabIndex}</p>
    <p style="margin: 4px 0;"><strong>Odaklanılabilir:</strong> ${analysis.focusable ? '✅ Evet' : '❌ Hayır'}</p>
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.remove();
  }, 5000);
}