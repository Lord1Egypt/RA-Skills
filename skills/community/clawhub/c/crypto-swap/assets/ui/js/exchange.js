/**
 * LightningEX - Exchange Functionality
 */

document.addEventListener('DOMContentLoaded', () => {
  initExchange();
});

function initExchange() {
  initCurrencySelectors();
  initAmountInputs();
  initSwapButton();
  initExchangeButton();
  startRateTimer();
  // Initialize exchange rate display as empty
  clearExchangeRateUI();
}

// Currency Selectors
function initCurrencySelectors() {
  const sendSelect = document.getElementById('sendCurrencySelect');
  const receiveSelect = document.getElementById('receiveCurrencySelect');
  
  if (sendSelect) {
    sendSelect.addEventListener('click', () => openCurrencyModal('send'));
  }
  
  if (receiveSelect) {
    receiveSelect.addEventListener('click', () => openCurrencyModal('receive'));
  }
}

function openCurrencyModal(type) {
  const modal = document.getElementById('currencyModal');
  const search = document.getElementById('currencySearch');
  const list = document.getElementById('currencyList');
  const close = document.getElementById('currencyModalClose');
  
  if (!modal || !list) return;
  
  // Render currency list
  renderCurrencyList(type);
  
  modal.classList.add('active');
  
  // Search functionality
  if (search) {
    search.value = '';
    search.focus();
    search.oninput = () => filterCurrencies(search.value, type);
  }
  
  // Close handlers
  close.onclick = () => modal.classList.remove('active');
  modal.onclick = (e) => {
    if (e.target === modal) modal.classList.remove('active');
  };
}

function renderCurrencyList(type) {
  const list = document.getElementById('currencyList');
  if (!list || !window.state.currencies.length) return;
  
  const isSend = type === 'send';
  
  list.innerHTML = window.state.currencies.map(currency => {
    const networks = currency.networkList || [];
    const availableNetworks = isSend 
      ? networks.filter(n => n.sendStatus)
      : networks.filter(n => n.receiveStatus);
    
    if (availableNetworks.length === 0) return '';
    
    return availableNetworks.map(network => {
      const isSelected = isSend 
        ? window.state.selectedSendCurrency?.currency === currency.currency && 
          window.state.selectedSendCurrency?.network === network.network
        : window.state.selectedReceiveCurrency?.currency === currency.currency &&
          window.state.selectedReceiveCurrency?.network === network.network;
      
      return `
        <div class="currency-list-item ${isSelected ? 'active' : ''}" 
             data-currency="${currency.currency}" 
             data-network="${network.network}">
          <div class="currency-list-icon">${currency.currency.charAt(0)}</div>
          <div class="currency-list-info">
            <div class="currency-list-code">${currency.currency}</div>
            <div class="currency-list-name">${currency.name}</div>
          </div>
          <span class="currency-list-network">${network.name}</span>
        </div>
      `;
    }).join('');
  }).join('');
  
  // Add click handlers
  list.querySelectorAll('.currency-list-item').forEach(item => {
    item.addEventListener('click', () => {
      const currencyCode = item.dataset.currency;
      const networkCode = item.dataset.network;
      selectCurrency(type, currencyCode, networkCode);
      document.getElementById('currencyModal').classList.remove('active');
    });
  });
}

function filterCurrencies(query, type) {
  const items = document.querySelectorAll('.currency-list-item');
  const lowerQuery = query.toLowerCase();
  
  items.forEach(item => {
    const code = item.dataset.currency.toLowerCase();
    const name = item.querySelector('.currency-list-name').textContent.toLowerCase();
    
    if (code.includes(lowerQuery) || name.includes(lowerQuery)) {
      item.style.display = 'flex';
    } else {
      item.style.display = 'none';
    }
  });
}

function selectCurrency(type, currencyCode, networkCode) {
  const currency = window.state.currencies.find(c => c.currency === currencyCode);
  if (!currency) return;
  
  const network = currency.networkList.find(n => n.network === networkCode);
  if (!network) return;
  
  const selection = {
    ...currency,
    network: networkCode,
    networkName: network.name
  };
  
  if (type === 'send') {
    window.state.selectedSendCurrency = selection;
  } else {
    window.state.selectedReceiveCurrency = selection;
  }
  
  updateCurrencyUI();
  
  // Always fetch Pair Info first when currency/network changes (for min/max amount)
  fetchPairInfo().then(() => {
    // Then fetch Exchange Rate if there's a valid amount
    const sendAmount = document.getElementById('sendAmount')?.value;
    if (sendAmount && parseFloat(sendAmount) > 0) {
      fetchExchangeRate();
    }
  });
}

// Amount Inputs
function initAmountInputs() {
  const sendInput = document.getElementById('sendAmount');

  if (sendInput) {
    // Prevent invalid input
    sendInput.addEventListener('keydown', (e) => {
      // Prevent minus sign
      if (e.key === '-') {
        e.preventDefault();
      }
    });

    sendInput.addEventListener('input', () => {
      let value = sendInput.value;

      // Prevent decimal point at start
      if (value.startsWith('.')) {
        value = '0' + value;
      }

      // Remove leading zeros (except for "0." case)
      if (value.length > 1 && value.startsWith('0') && !value.startsWith('0.')) {
        value = value.replace(/^0+/, '');
      }

      // Ensure value is positive
      if (parseFloat(value) < 0) {
        value = Math.abs(parseFloat(value)).toString();
      }

      // Update input if changed
      if (value !== sendInput.value) {
        sendInput.value = value;
      }

      // Validate min/max and update border color
      validateAmountRange();

      // Fetch rate with debounce only if valid amount (1.5s delay)
      debounce(() => {
        const numValue = parseFloat(sendInput.value);
        if (numValue > 0) {
          fetchExchangeRate();
        } else {
          // Clear exchange rate display when amount is empty or 0
          clearExchangeRateUI();
        }
      }, 1500)();
    });
  }
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Validate amount against min/max and update border color
function validateAmountRange() {
  const sendInput = document.getElementById('sendAmount');
  if (!sendInput) return;
  
  const value = parseFloat(sendInput.value);
  const minAmount = parseFloat(window.state.pairInfo?.minimumAmount || '0');
  const maxAmount = parseFloat(window.state.pairInfo?.maximumAmount || '999999999');
  
  if (sendInput.value && (value < minAmount || value > maxAmount)) {
    sendInput.style.borderColor = '#ff4444';
    sendInput.style.boxShadow = '0 0 10px rgba(255, 68, 68, 0.3)';
  } else {
    sendInput.style.borderColor = '';
    sendInput.style.boxShadow = '';
  }
}

// Swap Button
function initSwapButton() {
  const swapBtn = document.getElementById('swapButton');
  
  if (swapBtn) {
    swapBtn.addEventListener('click', () => {
      // Swap currencies
      const temp = window.state.selectedSendCurrency;
      window.state.selectedSendCurrency = window.state.selectedReceiveCurrency;
      window.state.selectedReceiveCurrency = temp;
      
      // Swap amounts
      const sendInput = document.getElementById('sendAmount');
      const receiveInput = document.getElementById('receiveAmount');
      
      if (sendInput && receiveInput) {
        const tempAmount = sendInput.value;
        sendInput.value = receiveInput.value;
        receiveInput.value = tempAmount;
      }
      
      updateCurrencyUI();
      
      // Always fetch Pair Info first after swap (for min/max amount)
      fetchPairInfo().then(() => {
        // Then fetch Exchange Rate if there's a valid amount
        const sendAmount = document.getElementById('sendAmount')?.value;
        if (sendAmount && parseFloat(sendAmount) > 0) {
          fetchExchangeRate();
        }
      });
    });
  }
}

// Exchange Button
function initExchangeButton() {
  const exchangeBtn = document.getElementById('exchangeButton');
  
  if (exchangeBtn) {
    exchangeBtn.addEventListener('click', startExchange);
  }
}

async function startExchange() {
  const sendAmountInput = document.getElementById('sendAmount');
  const sendAmount = sendAmountInput.value;

  // Browser validation for amount
  if (!sendAmount || parseFloat(sendAmount) <= 0) {
    sendAmountInput.focus();
    window.showToast('error', 'Please enter a valid amount');
    return;
  }

  // Validate amount is within min/max range
  const numAmount = parseFloat(sendAmount);
  const minAmount = parseFloat(window.state.pairInfo?.minimumAmount || '0');
  const maxAmount = parseFloat(window.state.pairInfo?.maximumAmount || '999999999');
  
  if (numAmount < minAmount || numAmount > maxAmount) {
    sendAmountInput.focus();
    window.showToast('error', `Amount must be between ${minAmount} and ${maxAmount} ${window.state.selectedSendCurrency?.currency || ''}`);
    return;
  }

  if (!window.state.selectedSendCurrency || !window.state.selectedReceiveCurrency) {
    window.showToast('error', 'Please select currencies');
    return;
  }

  // Open order modal with address input step
  openOrderModal('address');
}

// API Calls
async function fetchPairInfo() {
  if (!window.state.selectedSendCurrency || !window.state.selectedReceiveCurrency) return;
  
  try {
    const result = await window.apiGet('/exchange/pair/info', {
      send: window.state.selectedSendCurrency.currency,
      receive: window.state.selectedReceiveCurrency.currency,
      sendNetwork: window.state.selectedSendCurrency.network,
      receiveNetwork: window.state.selectedReceiveCurrency.network
    });
    
    if (result.code === 200 && result.data) {
      updatePairInfo(result.data);
    }
  } catch (error) {
    console.error('Failed to fetch pair info:', error);
  }
}

function updatePairInfo(data) {
  // Save pair info to state for validation
  window.state.pairInfo = data;
  
  const sendMin = document.getElementById('sendMin');
  const sendMax = document.getElementById('sendMax');
  const sendMinCurrency = document.getElementById('sendMinCurrency');
  const sendMaxCurrency = document.getElementById('sendMaxCurrency');
  const networkFee = document.getElementById('networkFee');
  const processingTime = document.getElementById('processingTime');
  
  if (sendMin) sendMin.textContent = data.minimumAmount || '0.001';
  if (sendMax) sendMax.textContent = data.maximumAmount || '420';
  if (sendMinCurrency && window.state.selectedSendCurrency) sendMinCurrency.textContent = window.state.selectedSendCurrency.currency;
  if (sendMaxCurrency && window.state.selectedSendCurrency) sendMaxCurrency.textContent = window.state.selectedSendCurrency.currency;
  if (networkFee) networkFee.textContent = `${data.networkFee || '0'} ${window.state.selectedReceiveCurrency?.currency || ''}`;
  if (processingTime) processingTime.textContent = `${data.processingTime || '2-5'} minutes`;
  
  // Re-validate current input
  validateAmountRange();
}

async function fetchExchangeRate() {
  const sendAmount = document.getElementById('sendAmount').value;
  
  if (!sendAmount || parseFloat(sendAmount) <= 0) return;
  if (!window.state.selectedSendCurrency || !window.state.selectedReceiveCurrency) return;
  
  try {
    const result = await window.apiGet('/exchange/rate', {
      send: window.state.selectedSendCurrency.currency,
      receive: window.state.selectedReceiveCurrency.currency,
      sendNetwork: window.state.selectedSendCurrency.network,
      receiveNetwork: window.state.selectedReceiveCurrency.network,
      amount: sendAmount
    });
    
    if (result.code === 200 && result.data) {
      window.state.exchangeRate = result.data;
      updateExchangeRateUI(result.data);
    }
  } catch (error) {
    console.error('Failed to fetch exchange rate:', error);
  }
}

function updateExchangeRateUI(data) {
  const receiveInput = document.getElementById('receiveAmount');
  const exchangeRate = document.getElementById('exchangeRate');
  const networkFee = document.getElementById('networkFee');
  const processingTime = document.getElementById('processingTime');
  
  // Save rate data to state for use in order modal
  window.state.currentRate = data;
  
  if (receiveInput) receiveInput.value = data.receiveAmount || '0.00';
  if (exchangeRate) {
    const rate = data.rate || '0';
    exchangeRate.textContent = `1 ${window.state.selectedSendCurrency?.currency} ≈ ${rate} ${window.state.selectedReceiveCurrency?.currency}`;
  }
  if (networkFee) networkFee.textContent = `${data.networkFee || '0.0005'} ${window.state.selectedReceiveCurrency?.currency || ''}`;
  if (processingTime) processingTime.textContent = `${data.processingTime || '2-5'} minutes`;
}

// Clear exchange rate display when no valid amount
function clearExchangeRateUI() {
  const receiveInput = document.getElementById('receiveAmount');
  const exchangeRate = document.getElementById('exchangeRate');
  
  if (receiveInput) receiveInput.value = '';
  if (exchangeRate) exchangeRate.textContent = '--';
}

// Rate Timer
function startRateTimer() {
  const timerEl = document.getElementById('rateTimer');
  if (!timerEl) return;
  
  let timeLeft = 20;
  
  if (window.state.rateTimer) {
    clearInterval(window.state.rateTimer);
  }
  
  window.state.rateTimer = setInterval(() => {
    timeLeft--;
    if (timeLeft <= 0) {
      timeLeft = 20;
      // Only fetch rate if there's a valid amount
      const sendAmount = document.getElementById('sendAmount')?.value;
      if (sendAmount && parseFloat(sendAmount) > 0) {
        fetchExchangeRate();
      }
    }
    timerEl.textContent = timeLeft;
  }, 1000);
}

// Order Modal
function openOrderModal(step, orderData = null) {
  const modal = document.getElementById('orderModal');
  const content = document.getElementById('orderContent');
  const close = document.getElementById('orderModalClose');
  
  if (!modal || !content) return;
  
  if (step === 'address') {
    content.innerHTML = renderAddressStep();
    initAddressStep();
  } else if (step === 'deposit' && orderData) {
    content.innerHTML = renderDepositStep(orderData);
    initDepositStep(orderData);
    startOrderStatusCheck(orderData.id);
  } else if (step === 'status' && orderData) {
    content.innerHTML = renderStatusStep(orderData);
  }
  
  modal.classList.add('active');
  
  close.onclick = () => {
    modal.classList.remove('active');
    stopOrderStatusCheck();
  };
}

function renderAddressStep() {
  const sendAmount = document.getElementById('sendAmount').value;
  const receiveAmount = document.getElementById('receiveAmount').value;
  const rate = window.state.currentRate?.rate || '0';
  const processingTime = window.state.currentRate?.processingTime || '3-5';
  
  return `
    <div class="order-step">
      <div class="order-step-icon">📋</div>
      <h3 class="order-step-title">Enter Your Address</h3>
      <p class="order-step-desc">Please provide the wallet address where you want to receive ${window.state.selectedReceiveCurrency?.currency}</p>
      
      <div class="order-details">
        <div class="order-detail-row">
          <span class="order-detail-label">You Send</span>
          <span class="order-detail-value">${sendAmount} ${window.state.selectedSendCurrency?.currency} <span style="color: var(--text-muted); font-size: 0.875rem;">(${window.state.selectedSendCurrency?.networkName})</span></span>
        </div>
        <div class="order-detail-row">
          <span class="order-detail-label">You Receive</span>
          <span class="order-detail-value highlight">${receiveAmount} ${window.state.selectedReceiveCurrency?.currency} <span style="color: var(--text-muted); font-size: 0.875rem;">(${window.state.selectedReceiveCurrency?.networkName})</span></span>
        </div>
        <div class="order-detail-row">
          <span class="order-detail-label">Exchange Rate</span>
          <span class="order-detail-value">1 ${window.state.selectedSendCurrency?.currency} ≈ ${rate} ${window.state.selectedReceiveCurrency?.currency}</span>
        </div>
        <div class="order-detail-row">
          <span class="order-detail-label">Network Fee</span>
          <span class="order-detail-value">${window.state.currentRate?.networkFee || '0'} ${window.state.selectedReceiveCurrency?.currency}</span>
        </div>
        <div class="order-detail-row">
          <span class="order-detail-label">Processing Time</span>
          <span class="order-detail-value">${processingTime} minutes</span>
        </div>
      </div>
      
      <div style="text-align: left; margin: var(--space-lg) 0;">
        <label style="display: block; margin-bottom: var(--space-sm); color: var(--text-secondary); font-size: 0.875rem;">
          ${window.state.selectedReceiveCurrency?.currency} Address (${window.state.selectedReceiveCurrency?.networkName})
        </label>
        <input type="text" class="input" id="receiveAddress" placeholder="Enter your ${window.state.selectedReceiveCurrency?.currency} address" required>
        <p style="margin-top: var(--space-sm); font-size: 0.75rem; color: var(--text-muted);">
          Make sure the address supports ${window.state.selectedReceiveCurrency?.networkName} network
        </p>
      </div>
      
      <button class="btn btn-primary btn-glow" id="confirmAddressBtn" style="width: 100%;">
        Confirm & Create Order
      </button>
    </div>
  `;
}

function initAddressStep() {
  const confirmBtn = document.getElementById('confirmAddressBtn');
  
  if (confirmBtn) {
    confirmBtn.addEventListener('click', async () => {
      const addressInput = document.getElementById('receiveAddress');
      const address = addressInput.value.trim();
      
      if (!address) {
        addressInput.focus();
        window.showToast('error', 'Please enter a valid address');
        return;
      }
      
      // Validate address
      try {
        const validation = await window.apiGet('/exchange/address/validate', {
          currency: window.state.selectedReceiveCurrency.currency,
          address: address,
          network: window.state.selectedReceiveCurrency.network
        });
        
        if (validation.code !== 200 || !validation.data) {
          window.showToast('error', 'Invalid address. Please check and try again.');
          return;
        }
        
        // Create order
        await createOrder(address);
      } catch (error) {
        console.error('Validation error:', error);
        window.showToast('error', 'Failed to validate address. Please try again.');
      }
    });
  }
}

async function createOrder(address) {
  const sendAmount = document.getElementById('sendAmount').value;

  try {
    const result = await window.apiPost('/exchange/order/place', {
      send: window.state.selectedSendCurrency.currency,
      receive: window.state.selectedReceiveCurrency.currency,
      sendNetwork: window.state.selectedSendCurrency.network,
      receiveNetwork: window.state.selectedReceiveCurrency.network,
      amount: parseFloat(sendAmount),
      receiveAddress: address
    });
    
    if (result.code === 200 && result.data) {
      window.showToast('success', 'Order created successfully!');
      
      // Redirect to order detail page
      window.location.href = `order.html?id=${result.data}`;
    } else {
      window.showToast('error', result.msg || 'Failed to create order');
    }
  } catch (error) {
    console.error('Create order error:', error);
    window.showToast('error', 'Failed to create order. Please try again.');
  }
}

function renderDepositStep(order) {
  const statusClass = getStatusClass(order.status);
  const statusTip = getStatusTip(order);
  
  return `
    <div class="order-step">
      <div class="order-step-icon">💎</div>
      <h3 class="order-step-title">Awaiting Your Deposit</h3>
      
      <div class="order-status-badge ${statusClass}">
        ${order.status}
      </div>
      
      <p class="order-step-desc" style="margin-top: var(--space-md);">${statusTip}</p>
      
      <div class="order-details">
        <div class="order-detail-row">
          <span class="order-detail-label">Order ID</span>
          <span class="order-detail-value">${order.id}</span>
        </div>
        <div class="order-detail-row">
          <span class="order-detail-label">Send Amount</span>
          <span class="order-detail-value">${order.sendAmount} ${order.send}</span>
        </div>
        <div class="order-detail-row">
          <span class="order-detail-label">Receive Amount</span>
          <span class="order-detail-value highlight">${order.receiveAmount} ${order.receive}</span>
        </div>
      </div>
      
      <div style="margin: var(--space-lg) 0;">
        <label style="display: block; margin-bottom: var(--space-sm); color: var(--text-secondary); font-size: 0.875rem;">
          Send ${order.send} to this address (${order.sendNetwork})
        </label>
        <div class="order-address-box">
          <span class="order-address">${order.sendAddress}</span>
          <button class="order-copy-btn" onclick="window.copyToClipboard('${order.sendAddress}')">Copy</button>
        </div>
        ${order.sendTag ? `
          <label style="display: block; margin-top: var(--space-md); margin-bottom: var(--space-sm); color: var(--text-secondary); font-size: 0.875rem;">
            Tag/MEMO (Required)
          </label>
          <div class="order-address-box">
            <span class="order-address">${order.sendTag}</span>
            <button class="order-copy-btn" onclick="window.copyToClipboard('${order.sendTag}')">Copy</button>
          </div>
        ` : ''}
      </div>
      
      <div class="order-progress">
        <div class="order-progress-bar" style="width: ${getProgressWidth(order.status)}%"></div>
        <div class="order-progress-step ${order.status === 'Awaiting Deposit' ? 'active' : 'completed'}">
          <div class="order-progress-dot">1</div>
          <span class="order-progress-label">Deposit</span>
        </div>
        <div class="order-progress-step ${order.status === 'Confirming Deposit' ? 'active' : (['Exchanging', 'Sending', 'Complete'].includes(order.status) ? 'completed' : '')}">
          <div class="order-progress-dot">2</div>
          <span class="order-progress-label">Confirm</span>
        </div>
        <div class="order-progress-step ${order.status === 'Exchanging' ? 'active' : (['Sending', 'Complete'].includes(order.status) ? 'completed' : '')}">
          <div class="order-progress-dot">3</div>
          <span class="order-progress-label">Exchange</span>
        </div>
        <div class="order-progress-step ${order.status === 'Sending' ? 'active' : (order.status === 'Complete' ? 'completed' : '')}">
          <div class="order-progress-dot">4</div>
          <span class="order-progress-label">Send</span>
        </div>
      </div>
    </div>
  `;
}

function initDepositStep(order) {
  // Any additional initialization for deposit step
}

function getStatusClass(status) {
  const statusMap = {
    'Awaiting Deposit': 'awaiting',
    'Confirming Deposit': 'confirming',
    'Exchanging': 'exchanging',
    'Sending': 'sending',
    'Complete': 'complete',
    'Failed': 'failed',
    'Action Request': 'failed',
    'Request Overdue': 'failed'
  };
  return statusMap[status] || 'awaiting';
}

function getStatusTip(order) {
  const tips = {
    'Awaiting Deposit': `Your order will automatically proceed to the next step once your deposit receives its first confirmation on the blockchain. If you do not deposit ${order.sendAmount} ${order.send}, or your deposit does not arrive within 1 hour, for security purposes your order will not be processed automatically.`,
    'Confirming Deposit': `You successfully sent ${order.sendAmount} ${order.send}! Please wait while your deposit is being confirmed. Your order will automatically proceed to the next step after the deposit transaction gets 1 confirmation. Nothing more is expected from you in this step.`,
    'Exchanging': `Your deposit has been confirmed! We are now exchanging your ${order.sendAmount} ${order.send} to ${order.receiveAmount} ${order.receive}. This may take a few minutes, please be patient.`,
    'Sending': `Your order is almost complete! We are forwarding ${order.receiveAmount} ${order.receive} to the following address: ${order.receiveAddress}`,
    'Complete': `Your order is successfully completed! We forwarded ${order.receiveAmount} ${order.receive} to the following address: ${order.receiveAddress}`,
    'Failed': 'The order failed because of one of the following reasons: You didn\'t send the correct amount, your deposit was not confirmed within 2 hours, or another reason.',
    'Action Request': 'This transaction has been detected with risks and needs to be verified before proceeding. Please contact lightningex.io for support.',
    'Request Overdue': 'The transaction request has expired. If you have other questions, please seek support from lightningex.io.'
  };
  return tips[order.status] || '';
}

function getProgressWidth(status) {
  const progressMap = {
    'Awaiting Deposit': 0,
    'Confirming Deposit': 25,
    'Exchanging': 50,
    'Sending': 75,
    'Complete': 100,
    'Failed': 0,
    'Action Request': 0,
    'Request Overdue': 0
  };
  return progressMap[status] || 0;
}

// Order Status Polling
function startOrderStatusCheck(orderId) {
  if (window.state.orderCheckInterval) {
    clearInterval(window.state.orderCheckInterval);
  }
  
  window.state.orderCheckInterval = setInterval(async () => {
    try {
      const result = await window.apiGet('/exchange/order/get', { id: orderId });
      
      if (result.code === 200 && result.data) {
        const order = result.data;
        
        // Update UI if status changed
        if (order.status !== document.querySelector('.order-status-badge')?.textContent.trim()) {
          openOrderModal('deposit', order);
          
          if (order.status === 'Complete') {
            window.showToast('success', 'Your exchange is complete!');
            stopOrderStatusCheck();
          } else if (['Failed', 'Action Request', 'Request Overdue'].includes(order.status)) {
            window.showToast('error', 'Order issue detected. Please contact support.');
            stopOrderStatusCheck();
          }
        }
      }
    } catch (error) {
      console.error('Status check error:', error);
    }
  }, 15000); // Check every 15 seconds
}

function stopOrderStatusCheck() {
  if (window.state.orderCheckInterval) {
    clearInterval(window.state.orderCheckInterval);
    window.state.orderCheckInterval = null;
  }
}
