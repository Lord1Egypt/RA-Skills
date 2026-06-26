// AccessMind Inspector - Content Script v1.1
// Injected into pages to perform accessibility analysis
// Production Ready - Error handling + Async/Await + User feedback

(function() {
  'use strict';
  
  // State
  let isScanning = false;
  let highlights = [];
  
  // Listen for messages from popup/background
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    handleMessage(request)
      .then(sendResponse)
      .catch(error => {
        console.error('[AccessMind]', error);
        sendResponse({ error: error.message, success: false });
      });
    return true; // Keep channel open for async response
  });
  
  // Message handler with async support
  async function handleMessage(request) {
    switch (request.action) {
      case 'highlight':
        return await highlightElement(request.selector, request.severity);
      
      case 'clearHighlights':
        return clearHighlights();
      
      case 'getAccessibilityTree':
        return buildAccessibilityTree();
      
      case 'simulateKeyboard':
        return await simulateKeyboardNavigation(request.steps || 50);
      
      case 'getPageSnapshot':
        return getPageSnapshot();
      
      case 'quickScan':
        return await quickAccessibilityScan();
      
      case 'showNotification':
        return showNotification(request.message, request.type);
      
      default:
        return { error: 'Unknown action', success: false };
    }
  }
  
  // Highlight element on page
  async function highlightElement(selector, severity = 'serious') {
    try {
      const elements = document.querySelectorAll(selector);
      
      if (elements.length === 0) {
        return { success: false, message: 'Element bulunamadı' };
      }
      
      const colors = {
        critical: '#ef4444',
        serious: '#f59e0b',
        moderate: '#3b82f6',
        minor: '#8b5cf6'
      };
      
      const color = colors[severity] || colors.serious;
      
      elements.forEach(el => {
        // Remove existing highlight if any
        const existingOverlay = el._accessmindHighlight;
        if (existingOverlay) {
          existingOverlay.remove();
        }
        
        // Create highlight overlay
        const rect = el.getBoundingClientRect();
        const overlay = document.createElement('div');
        overlay.className = 'accessmind-highlight';
        overlay.style.cssText = `
          position: absolute;
          top: ${rect.top + window.scrollY}px;
          left: ${rect.left + window.scrollX}px;
          width: ${rect.width}px;
          height: ${rect.height}px;
          border: 3px solid ${color};
          background: ${color}20;
          pointer-events: none;
          z-index: 2147483647;
          box-sizing: border-box;
          border-radius: 4px;
          transition: opacity 0.2s ease;
        `;
        
        // Add label
        const label = document.createElement('div');
        label.style.cssText = `
          position: absolute;
          top: -24px;
          left: 0;
          background: ${color};
          color: white;
          padding: 4px 8px;
          font-size: 11px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          border-radius: 4px;
          white-space: nowrap;
          font-weight: 600;
          box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        `;
        label.textContent = severity.toUpperCase();
        overlay.appendChild(label);
        
        document.body.appendChild(overlay);
        highlights.push(overlay);
        el._accessmindHighlight = overlay;
      });
      
      return { 
        success: true, 
        highlightedCount: elements.length,
        message: `${elements.length} element vurgulandı`
      };
    } catch (error) {
      console.error('[AccessMind] Highlight error:', error);
      return { success: false, message: error.message };
    }
  }
  
  // Clear all highlights
  function clearHighlights() {
    try {
      highlights.forEach(overlay => overlay.remove());
      highlights = [];
      
      // Remove from elements
      document.querySelectorAll('._accessmindHighlight').forEach(el => {
        delete el._accessmindHighlight;
      });
      
      return { success: true, message: 'Vurgulamalar temizlendi' };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }
  
  // Build accessibility tree
  function buildAccessibilityTree(root = document.body, maxDepth = 20) {
    try {
      function processNode(node, depth = 0) {
        if (!node || node.nodeType !== Node.ELEMENT_NODE || depth > maxDepth) {
          return null;
        }
        
        // Skip hidden elements
        const style = window.getComputedStyle(node);
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
          return null;
        }
        
        // Skip script, style, noscript
        const skipTags = ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'];
        if (skipTags.includes(node.tagName)) {
          return null;
        }
        
        const result = {
          role: node.getAttribute('role') || getImplicitRole(node),
          tagName: node.tagName.toLowerCase(),
          name: getAccessibleName(node),
          children: [],
          attributes: {},
          issues: [],
          depth: depth
        };
        
        // Get relevant attributes
        const ariaAttrs = [
          'aria-label', 'aria-labelledby', 'aria-describedby', 'aria-hidden',
          'aria-live', 'aria-expanded', 'aria-selected', 'aria-checked',
          'aria-pressed', 'aria-haspopup', 'aria-controls', 'aria-owns',
          'tabindex', 'href', 'src', 'alt', 'title', 'type', 'name', 'value'
        ];
        
        ariaAttrs.forEach(attr => {
          if (node.hasAttribute(attr)) {
            result.attributes[attr] = node.getAttribute(attr);
          }
        });
        
        // Check for issues
        checkAccessibilityIssues(node, result);
        
        // Process children
        for (const child of node.children) {
          const childNode = processNode(child, depth + 1);
          if (childNode) {
            result.children.push(childNode);
          }
        }
        
        return result;
      }
      
      return processNode(root);
    } catch (error) {
      console.error('[AccessMind] Build tree error:', error);
      return { error: error.message, children: [] };
    }
  }
  
  // Get implicit ARIA role
  function getImplicitRole(el) {
    if (!el || !el.tagName) return null;
    
    const tag = el.tagName.toLowerCase();
    const type = el.getAttribute('type');
    
    const roles = {
      'a': el.hasAttribute('href') ? 'link' : null,
      'button': 'button',
      'input': {
        'button': 'button',
        'checkbox': 'checkbox',
        'radio': 'radio',
        'range': 'slider',
        'search': 'searchbox',
        'submit': 'button',
        'text': 'textbox',
        'email': 'textbox',
        'tel': 'textbox',
        'url': 'textbox',
        'password': 'textbox',
        'number': 'spinbutton'
      }[type] || 'textbox',
      'select': el.hasAttribute('multiple') || el.size > 1 ? 'listbox' : 'combobox',
      'textarea': 'textbox',
      'img': el.hasAttribute('alt') ? 'img' : 'img',
      'nav': 'navigation',
      'main': 'main',
      'header': 'banner',
      'footer': 'contentinfo',
      'aside': 'complementary',
      'article': 'article',
      'section': 'region',
      'form': 'form',
      'table': 'table',
      'ul': 'list',
      'ol': 'list',
      'li': 'listitem',
      'h1': 'heading',
      'h2': 'heading',
      'h3': 'heading',
      'h4': 'heading',
      'h5': 'heading',
      'h6': 'heading',
      'dialog': 'dialog',
      'menu': 'menu',
      'menuitem': 'menuitem',
      'summary': 'button'
    };
    
    return roles[tag] || null;
  }
  
  // Get accessible name
  function getAccessibleName(el) {
    if (!el) return null;
    
    try {
      // Priority: aria-label, aria-labelledby, title, alt, label, text content
      
      // 1. aria-label
      if (el.getAttribute('aria-label')) {
        return el.getAttribute('aria-label').trim().substring(0, 100);
      }
      
      // 2. aria-labelledby
      if (el.getAttribute('aria-labelledby')) {
        const labelEl = document.getElementById(el.getAttribute('aria-labelledby'));
        if (labelEl) {
          return labelEl.textContent.trim().substring(0, 100);
        }
      }
      
      // 3. alt (for images)
      if (el.tagName === 'IMG' && el.alt) {
        return el.alt.trim().substring(0, 100);
      }
      
      // 4. title attribute
      if (el.getAttribute('title')) {
        return el.getAttribute('title').trim().substring(0, 100);
      }
      
      // 5. label element (for form controls)
      if (el.id) {
        const label = document.querySelector(`label[for="${el.id}"]`);
        if (label) {
          return label.textContent.trim().substring(0, 100);
        }
      }
      
      // 6. placeholder (for inputs)
      if ((el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') && el.placeholder) {
        return el.placeholder.trim().substring(0, 100);
      }
      
      // 7. text content (for buttons, links)
      const text = el.textContent?.trim();
      if (text && text.length > 0 && text.length < 100) {
        return text;
      }
      
      // 8. value (for input buttons)
      if (el.tagName === 'INPUT' && ['submit', 'button', 'reset'].includes(el.type)) {
        return el.value?.trim().substring(0, 100) || null;
      }
      
      return null;
    } catch (error) {
      return null;
    }
  }
  
  // Check for accessibility issues
  function checkAccessibilityIssues(el, result) {
    if (!el) return;
    
    try {
      // 1.1.1 - Images without alt
      if (el.tagName === 'IMG') {
        if (!el.alt && !el.getAttribute('aria-label') && el.getAttribute('role') !== 'presentation') {
          result.issues.push({
            wcag: '1.1.1',
            severity: 'critical',
            message: 'Görsel alt text içermiyor',
            element: el.tagName.toLowerCase()
          });
        }
      }
      
      // 2.4.4 - Links without accessible names
      if (el.tagName === 'A' && el.hasAttribute('href')) {
        if (!result.name && !el.querySelector('img[alt]')) {
          result.issues.push({
            wcag: '2.4.4',
            severity: 'serious',
            message: 'Link erişilebilir isim içermiyor',
            element: el.tagName.toLowerCase()
          });
        }
      }
      
      // 1.3.1 - Form inputs without labels
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName)) {
        const inputType = el.type?.toLowerCase();
        const hiddenTypes = ['hidden', 'submit', 'button', 'reset', 'image'];
        
        if (!hiddenTypes.includes(inputType) && !result.name && !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby')) {
          result.issues.push({
            wcag: '1.3.1',
            severity: 'serious',
            message: 'Form elemanı etiket içermiyor',
            element: el.tagName.toLowerCase()
          });
        }
      }
      
      // 4.1.2 - Buttons without names
      if (el.tagName === 'BUTTON') {
        if (!result.name && !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby')) {
          result.issues.push({
            wcag: '4.1.2',
            severity: 'serious',
            message: 'Buton erişilebilir isim içermiyor',
            element: el.tagName.toLowerCase()
          });
        }
      }
      
      // 2.4.7 - Focus visibility
      const tabindex = el.getAttribute('tabindex');
      if (tabindex && tabindex !== '-1') {
        const style = window.getComputedStyle(el);
        if (style.outline === 'none' && !style.boxShadow.includes('outline')) {
          // Check for :focus-visible in stylesheets
          // This is a simplified check
          result.issues.push({
            wcag: '2.4.7',
            severity: 'moderate',
            message: 'Element focus göstergesi içermeyebilir',
            element: el.tagName.toLowerCase()
          });
        }
      }
      
      // 3.1.2 - Language of parts
      if (el.getAttribute('lang') && el.getAttribute('lang') !== document.documentElement.lang) {
        // This could be an issue if not properly handled
      }
      
      // 4.1.3 - Status messages
      const liveAria = ['polite', 'assertive', 'off'];
      const live = el.getAttribute('aria-live');
      const role = el.getAttribute('role');
      
      if (live === 'assertive' && role !== 'alert') {
        result.issues.push({
          wcag: '4.1.3',
          severity: 'moderate',
          message: 'aria-live="assertive" role="alert" ile kullanılmalı',
          element: el.tagName.toLowerCase()
        });
      }
    } catch (error) {
      console.error('[AccessMind] Issue check error:', error);
    }
  }
  
  // Simulate keyboard navigation with detailed tracking
  async function simulateKeyboardNavigation(steps = 50) {
    return new Promise((resolve) => {
      try {
        const focusables = Array.from(document.querySelectorAll(
          'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        )).filter(el => {
          const style = window.getComputedStyle(el);
          return style.display !== 'none' && 
                 style.visibility !== 'hidden' && 
                 el.offsetParent !== null;
        });
        
        const results = {
          totalFocusables: focusables.length,
          steps: [],
          traps: [],
          focusVisibleCount: 0,
          focusMissingCount: 0,
          visitedElements: [],
          startTime: Date.now()
        };
        
        let currentIndex = -1;
        let stepCount = 0;
        
        function step() {
          if (stepCount >= steps || currentIndex >= focusables.length - 1) {
            results.endTime = Date.now();
            results.duration = results.endTime - results.startTime;
            resolve(results);
            return;
          }
          
          currentIndex++;
          const el = focusables[currentIndex];
          
          if (el) {
            try {
              el.focus();
              
              const hasVisibleFocus = checkFocusVisibility(el);
              
              results.steps.push({
                step: stepCount + 1,
                element: {
                  tagName: el.tagName,
                  type: el.type || null,
                  text: (el.textContent?.substring(0, 50) || el.alt || el.placeholder || el.value || '').trim(),
                  tabindex: el.tabIndex,
                  ariaLabel: el.getAttribute('aria-label') || null
                },
                hasFocus: document.activeElement === el,
                hasVisibleFocus: hasVisibleFocus,
                cssPath: getCSSPath(el)
              });
              
              if (hasVisibleFocus) {
                results.focusVisibleCount++;
              } else {
                results.focusMissingCount++;
              }
              
              results.visitedElements.push(el);
              
              // Check for trap
              if (results.visitedElements.length >= 3) {
                const lastThree = results.visitedElements.slice(-3);
                if (lastThree[0] === lastThree[1] && lastThree[1] === lastThree[2]) {
                  results.traps.push({
                    step: stepCount + 1,
                    element: el.tagName.toLowerCase(),
                    message: 'Focus tuzağı tespit edildi'
                  });
                }
              }
            } catch (e) {
              results.steps.push({
                step: stepCount + 1,
                error: e.message
              });
            }
          }
          
          stepCount++;
          // Use requestAnimationFrame for smoother execution
          requestAnimationFrame(() => setTimeout(step, 10));
        }
        
        step();
      } catch (error) {
        resolve({ error: error.message, success: false });
      }
    });
  }
  
  // Check if element has visible focus indicator
  function checkFocusVisibility(el) {
    try {
      const style = window.getComputedStyle(el);
      
      // Check for outline
      if (style.outline !== 'none' && style.outlineWidth !== '0px') {
        return true;
      }
      
      // Check for box-shadow (often used for focus)
      if (style.boxShadow !== 'none') {
        return true;
      }
      
      // Check for border change (often used for focus)
      if (style.border !== 'none') {
        return true;
      }
      
      // Check for background change
      if (style.backgroundColor !== 'transparent' && style.backgroundColor !== 'rgba(0, 0, 0, 0)') {
        return true;
      }
      
      return false;
    } catch (e) {
      return false;
    }
  }
  
  // Get CSS path for element
  function getCSSPath(el) {
    if (!el || el === document.body) return 'body';
    
    const path = [];
    let current = el;
    
    while (current && current !== document.body) {
      let selector = current.tagName.toLowerCase();
      
      if (current.id) {
        selector = `#${current.id}`;
        path.unshift(selector);
        break;
      }
      
      if (current.className && typeof current.className === 'string') {
        const classes = current.className.trim().split(/\s+/).slice(0, 2);
        selector += classes.map(c => `.${c}`).join('');
      }
      
      const siblings = Array.from(current.parentElement?.children || []);
      if (siblings.length > 1) {
        const index = siblings.indexOf(current) + 1;
        selector += `:nth-child(${index})`;
      }
      
      path.unshift(selector);
      current = current.parentElement;
    }
    
    return path.join(' > ').substring(0, 200);
  }
  
  // Get page snapshot for analysis
  function getPageSnapshot() {
    try {
      return {
        title: document.title,
        url: window.location.href,
        viewport: {
          width: window.innerWidth,
          height: window.innerHeight,
          devicePixelRatio: window.devicePixelRatio
        },
        documentSize: {
          width: document.documentElement.scrollWidth,
          height: document.documentElement.scrollHeight
        },
        headings: Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => ({
          level: parseInt(h.tagName.charAt(1)),
          text: h.textContent.trim().substring(0, 100),
          visible: h.offsetParent !== null
        })),
        landmarks: {
          main: !!document.querySelector('main, [role="main"]'),
          nav: !!document.querySelector('nav, [role="navigation"]'),
          aside: !!document.querySelector('aside, [role="complementary"]'),
          header: !!document.querySelector('header, [role="banner"]'),
          footer: !!document.querySelector('footer, [role="contentinfo"]'),
          search: !!document.querySelector('[role="search"], input[type="search"]')
        },
        skipLinks: (() => {
          const skipLinks = Array.from(document.querySelectorAll('a[href^="#"]'));
          return skipLinks.filter(a => 
            a.textContent.toLowerCase().match(/atla|skip|geç/) ||
            a.getAttribute('aria-label')?.toLowerCase().match(/atla|skip|geç/)
          ).length;
        })(),
        focusables: document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]').length,
        images: {
          total: document.querySelectorAll('img').length,
          withAlt: document.querySelectorAll('img[alt]').length,
          withoutAlt: document.querySelectorAll('img:not([alt])').length,
          decorative: document.querySelectorAll('img[alt=""], img[role="presentation"]').length
        },
        links: {
          total: document.querySelectorAll('a[href]').length,
          withText: Array.from(document.querySelectorAll('a[href]')).filter(a => a.textContent.trim()).length,
          empty: Array.from(document.querySelectorAll('a[href]')).filter(a => !a.textContent.trim() && !a.querySelector('img[alt]')).length
        },
        forms: {
          total: document.querySelectorAll('form').length,
          inputs: document.querySelectorAll('input:not([type="hidden"]), select, textarea').length,
          inputsWithLabels: Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea')).filter(i => 
            i.labels?.length || i.getAttribute('aria-label') || i.getAttribute('aria-labelledby')
          ).length
        },
        ariaLiveRegions: document.querySelectorAll('[aria-live], [role="alert"], [role="status"]').length,
        lang: document.documentElement.lang || null,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { error: error.message, success: false };
    }
  }
  
  // Quick accessibility scan
  async function quickAccessibilityScan() {
    try {
      const tree = buildAccessibilityTree();
      const snapshot = getPageSnapshot();
      
      // Collect all issues from tree
      const issues = [];
      
      function collectIssues(node) {
        if (!node) return;
        if (node.issues && node.issues.length > 0) {
          issues.push(...node.issues);
        }
        if (node.children) {
          node.children.forEach(collectIssues);
        }
      }
      
      collectIssues(tree);
      
      // Group by severity
      const critical = issues.filter(i => i.severity === 'critical');
      const serious = issues.filter(i => i.severity === 'serious');
      const moderate = issues.filter(i => i.severity === 'moderate');
      const minor = issues.filter(i => i.severity === 'minor');
      
      return {
        success: true,
        issues: {
          total: issues.length,
          critical: critical.length,
          serious: serious.length,
          moderate: moderate.length,
          minor: minor.length,
          details: issues.slice(0, 20) // First 20 issues
        },
        snapshot: snapshot,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { error: error.message, success: false };
    }
  }
  
  // Show notification on page
  function showNotification(message, type = 'info') {
    try {
      // Remove existing notification
      const existing = document.getElementById('accessmind-notification');
      if (existing) existing.remove();
      
      const colors = {
        info: '#3b82f6',
        success: '#22c55e',
        warning: '#f59e0b',
        error: '#ef4444'
      };
      
      const notification = document.createElement('div');
      notification.id = 'accessmind-notification';
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type] || colors.info};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        font-weight: 500;
        z-index: 2147483647;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        max-width: 400px;
        animation: accessmind-slidein 0.3s ease;
      `;
      notification.textContent = message;
      
      // Add animation
      const style = document.createElement('style');
      style.textContent = `
        @keyframes accessmind-slidein {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `;
      document.head.appendChild(style);
      
      document.body.appendChild(notification);
      
      // Auto remove after 3 seconds
      setTimeout(() => {
        notification.style.animation = 'accessmind-slidein 0.3s ease reverse';
        setTimeout(() => notification.remove(), 300);
      }, 3000);
      
      return { success: true };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }
  
  // Keyboard shortcut
  document.addEventListener('keydown', (e) => {
    // Ctrl+Shift+A for quick analysis
    if (e.ctrlKey && e.shiftKey && e.key === 'A') {
      e.preventDefault();
      chrome.runtime.sendMessage({ action: 'quickAnalyze' });
      showNotification('Erişilebilirlik taraması başlatıldı...', 'info');
    }
    
    // Ctrl+Shift+H for highlight toggle
    if (e.ctrlKey && e.shiftKey && e.key === 'H') {
      e.preventDefault();
      if (highlights.length > 0) {
        clearHighlights();
        showNotification('Vurgulamalar temizlendi', 'success');
      }
    }
  });
  
  // Console message for developers
  console.log('%c🔍 AccessMind Inspector v1.1 loaded', 'color: #4a9eff; font-size: 14px; font-weight: bold;');
  console.log('%cKlavye kısayolları:', 'color: #888; font-weight: bold;');
  console.log('%c  Ctrl+Shift+A: Hızlı Tarama', 'color: #888;');
  console.log('%c  Ctrl+Shift+H: Vurgulamaları Temizle', 'color: #888;');
  
})();