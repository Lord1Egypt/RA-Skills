/**
 * LightningEX - Simplified Application
 */

// API Configuration
const API_BASE_URL = 'https://api.lightningex.io';

// App State
const state = {
  currencies: [],
  selectedSendCurrency: null,
  selectedReceiveCurrency: null,
  exchangeRate: null,
  rateTimer: null
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

function initApp() {
  // Only load currencies on the exchange page (index.html)
  const path = window.location.pathname;
  const isIndexPage = path.endsWith('index.html') || path === '/' || path.endsWith('/ui/');
  if (isIndexPage) {
    loadCurrencies();
  }
}

// Load Currencies
async function loadCurrencies() {
  try {
    const response = await fetch(`${API_BASE_URL}/exchange/currency/list`);
    const result = await response.json();
    
    if (result.code === 200 && result.data) {
      state.currencies = result.data;
      
      // Set default currencies (BTC on BTC network, ETH on ERC20 network)
      if (state.currencies.length > 0) {
        const btc = state.currencies.find(c => c.currency === 'BTC');
        const eth = state.currencies.find(c => c.currency === 'ETH');
        
        if (btc) {
          const btcNetwork = btc.networkList.find(n => n.network === 'BTC') || btc.networkList[0];
          state.selectedSendCurrency = { ...btc, network: btcNetwork?.network, networkName: btcNetwork?.name };
        }
        if (eth) {
          const ethNetwork = eth.networkList.find(n => n.network === 'ERC20') || 
                            eth.networkList.find(n => n.network === 'ETH') || 
                            eth.networkList[0];
          state.selectedReceiveCurrency = { ...eth, network: ethNetwork?.network, networkName: ethNetwork?.name };
        }
        
        updateCurrencyUI();
        
        // Fetch initial Pair Info after currencies loaded
        if (state.selectedSendCurrency && state.selectedReceiveCurrency) {
          fetchPairInfo();
        }
      }
    }
  } catch (error) {
    console.error('Failed to load currencies:', error);
  }
}

function updateCurrencyUI() {
  // Update send currency
  const sendIcon = document.getElementById('sendIcon');
  const sendCode = document.getElementById('sendCode');
  const sendNetwork = document.getElementById('sendNetwork');
  
  if (sendIcon && state.selectedSendCurrency) {
    sendIcon.textContent = state.selectedSendCurrency.currency.charAt(0);
  }
  if (sendCode && state.selectedSendCurrency) {
    sendCode.textContent = state.selectedSendCurrency.currency;
  }
  if (sendNetwork && state.selectedSendCurrency) {
    sendNetwork.textContent = state.selectedSendCurrency.networkName || state.selectedSendCurrency.network;
  }
  
  // Update receive currency
  const receiveIcon = document.getElementById('receiveIcon');
  const receiveCode = document.getElementById('receiveCode');
  const receiveNetwork = document.getElementById('receiveNetwork');
  
  if (receiveIcon && state.selectedReceiveCurrency) {
    receiveIcon.textContent = state.selectedReceiveCurrency.currency.charAt(0);
  }
  if (receiveCode && state.selectedReceiveCurrency) {
    receiveCode.textContent = state.selectedReceiveCurrency.currency;
  }
  if (receiveNetwork && state.selectedReceiveCurrency) {
    receiveNetwork.textContent = state.selectedReceiveCurrency.networkName || state.selectedReceiveCurrency.network;
  }
}

// Fetch Pair Info (min/max limits)
async function fetchPairInfo() {
  if (!state.selectedSendCurrency || !state.selectedReceiveCurrency) return;
  
  try {
    const response = await fetch(
      `${API_BASE_URL}/exchange/pair/info?send=${state.selectedSendCurrency.currency}&receive=${state.selectedReceiveCurrency.currency}`
    );
    const result = await response.json();
    
    if (result.code === 200 && result.data) {
      // Update min/max display
      const sendMin = document.getElementById('sendMin');
      const sendMax = document.getElementById('sendMax');
      const sendMinCurrency = document.getElementById('sendMinCurrency');
      const sendMaxCurrency = document.getElementById('sendMaxCurrency');
      
      if (sendMin) sendMin.textContent = result.data.min || '0.001';
      if (sendMax) sendMax.textContent = result.data.max || '420';
      if (sendMinCurrency) sendMinCurrency.textContent = state.selectedSendCurrency.currency;
      if (sendMaxCurrency) sendMaxCurrency.textContent = state.selectedSendCurrency.currency;
    }
  } catch (error) {
    console.error('Failed to fetch pair info:', error);
  }
}

// API Helpers
async function apiGet(endpoint, params = {}) {
  const queryString = new URLSearchParams(params).toString();
  const url = `${API_BASE_URL}${endpoint}${queryString ? '?' + queryString : ''}`;

  const response = await fetch(url);
  return response.json();
}

async function apiPost(endpoint, data = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
}

// Utility Functions
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function formatNumber(num, decimals = 8) {
  return parseFloat(num).toFixed(decimals).replace(/\.?0+$/, '');
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert('Copied to clipboard!');
  }).catch(() => {
    alert('Failed to copy');
  });
}

// Toast Notifications
function showToast(type, message) {
  const container = document.querySelector('.toast-container') || createToastContainer();
  
  const toast = document.createElement('div');
  toast.style.cssText = `
    background: var(--bg-card);
    border: 1px solid ${type === 'error' ? '#ff4444' : type === 'success' ? '#00ff88' : '#00f5ff'};
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    color: var(--text-primary);
    font-size: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    animation: slideIn 0.3s ease;
  `;
  toast.textContent = message;
  
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.remove();
  }, 3000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.className = 'toast-container';
  container.style.cssText = `
    position: fixed;
    top: 80px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 8px;
  `;
  document.body.appendChild(container);
  return container;
}

// Export for other modules
window.API_BASE_URL = API_BASE_URL;
window.state = state;
window.apiGet = apiGet;
window.apiPost = apiPost;
window.escapeHtml = escapeHtml;
window.formatNumber = formatNumber;
window.copyToClipboard = copyToClipboard;
window.updateCurrencyUI = updateCurrencyUI;
window.fetchPairInfo = fetchPairInfo;
window.showToast = showToast;
