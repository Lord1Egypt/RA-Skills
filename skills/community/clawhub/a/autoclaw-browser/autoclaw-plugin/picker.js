// AutoClaw Content Script - Element Picker
// This script runs on web pages to enable element selection

let pickerActive = false;
let hoveredElement = null;
let highlightOverlay = null;

// Create highlight overlay
function createHighlightOverlay() {
  if (highlightOverlay) return;
  
  try {
    highlightOverlay = document.createElement('div');
    highlightOverlay.id = 'autoclaw-picker-overlay';
    highlightOverlay.style.cssText = `
      position: fixed;
      pointer-events: none;
      z-index: 2147483647;
      border: 2px solid #8B5CF6;
      background: rgba(139, 92, 246, 0.1);
      transition: all 0.1s ease;
      border-radius: 4px;
      display: none;
    `;
    document.body.appendChild(highlightOverlay);
  } catch (e) {
    console.warn('[AutoClaw] Cannot create highlight overlay:', e);
  }
}

// Remove highlight overlay
function removeHighlightOverlay() {
  if (highlightOverlay) {
    try {
      highlightOverlay.remove();
    } catch (e) {}
    highlightOverlay = null;
  }
}

// Generate CSS selector for element
function generateSelector(element) {
  if (element.id) {
    return '#' + element.id;
  }
  
  if (element.className && typeof element.className === 'string') {
    const classes = element.className.trim().split(/\s+/).filter(c => c);
    if (classes.length > 0) {
      return element.tagName.toLowerCase() + '.' + classes[0];
    }
  }
  
  // Use nth-child
  let selector = element.tagName.toLowerCase();
  let parent = element.parentElement;
  
  if (parent) {
    const children = Array.from(parent.children).filter(child => 
      child.tagName === element.tagName
    );
    if (children.length > 1) {
      const index = children.indexOf(element) + 1;
      selector += ':nth-child(' + index + ')';
    }
  }
  
  return selector;
}

// Highlight element on hover
function highlightElement(element) {
  if (!highlightOverlay || !element) return;
  
  try {
    const rect = element.getBoundingClientRect();
    highlightOverlay.style.display = 'block';
    highlightOverlay.style.left = (rect.left + window.scrollX - 2) + 'px';
    highlightOverlay.style.top = (rect.top + window.scrollY - 2) + 'px';
    highlightOverlay.style.width = (rect.width + 4) + 'px';
    highlightOverlay.style.height = (rect.height + 4) + 'px';
  } catch (e) {}
}

// Handle mouse move
function handleMouseMove(event) {
  if (!pickerActive) return;
  
  // Remove from previous element
  if (hoveredElement) {
    hoveredElement.removeEventListener('mouseover', highlightOn);
    hoveredElement.removeEventListener('mouseout', removeHighlight);
    hoveredElement.removeEventListener('click', handleClick);
  }
  
  // Get target element
  hoveredElement = event.target;
  
  // Skip body and html
  if (hoveredElement === document.body || hoveredElement === document.documentElement) {
    return;
  }
  
  // Add listeners
  hoveredElement.addEventListener('mouseover', highlightOn);
  hoveredElement.addEventListener('mouseout', removeHighlight);
  hoveredElement.addEventListener('click', handleClick, { once: true });
  
  highlightOn();
}

function highlightOn() {
  if (!hoveredElement) return;
  highlightElement(hoveredElement);
}

function removeHighlight() {
  if (highlightOverlay) {
    highlightOverlay.style.display = 'none';
  }
}

// Handle click - select element
function handleClick(event) {
  if (!pickerActive) return;
  
  event.preventDefault();
  event.stopPropagation();
  
  const selector = generateSelector(hoveredElement);
  
  // Send selector to popup/background
  chrome.runtime.sendMessage({
    type: 'elementSelected',
    selector: selector,
    tag: hoveredElement.tagName.toLowerCase(),
    text: hoveredElement.textContent?.trim().substring(0, 50)
  });
  
  // Deactivate picker
  deactivatePicker();
}

// Activate picker
function activatePicker() {
  pickerActive = true;
  createHighlightOverlay();
  document.addEventListener('mousemove', handleMouseMove);
  document.body.style.cursor = 'crosshair';
  
  console.log('[AutoClaw] Element picker activated');
}

// Deactivate picker
function deactivatePicker() {
  pickerActive = false;
  removeHighlightOverlay();
  document.removeEventListener('mousemove', handleMouseMove);
  document.body.style.cursor = '';
  
  if (hoveredElement) {
    hoveredElement.removeEventListener('mouseover', highlightOn);
    hoveredElement.removeEventListener('mouseout', removeHighlight);
    hoveredElement.removeEventListener('click', handleClick);
    hoveredElement = null;
  }
  
  console.log('[AutoClaw] Element picker deactivated');
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'activatePicker') {
    activatePicker();
  } else if (message.action === 'deactivatePicker') {
    deactivatePicker();
  }
});

console.log('[AutoClaw] Content script loaded');
