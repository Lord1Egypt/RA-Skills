/**
 * LightningEX - Order Detail Page
 */

const API_BASE = 'https://api.lightningex.io';
let orderId = null;
let pollInterval = null;

function getOrderIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

document.addEventListener('DOMContentLoaded', () => {
  orderId = getOrderIdFromUrl();
  if (!orderId) {
    showError();
    return;
  }
  document.getElementById('displayOrderId').textContent = orderId;
  loadOrderStatus();
  pollInterval = setInterval(loadOrderStatus, 15000);
});

function showError() {
  document.getElementById('loadingState').classList.add('hidden');
  document.getElementById('errorState').classList.remove('hidden');
}

async function loadOrderStatus() {
  try {
    const response = await fetch(`${API_BASE}/exchange/order/get?id=${orderId}`);
    const result = await response.json();
    
    if (result.code !== 200) {
      showError();
      return;
    }

    const data = result.data;
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('orderContent').classList.remove('hidden');

    updateProgressSteps(data.status);
    updateStatusContent(data);
    updateTransactionDetails(data);

    if (['Complete', 'Failed', 'Refund', 'Request Overdue'].includes(data.status)) {
      clearInterval(pollInterval);
    }
  } catch (error) {
    console.error('Failed to load order:', error);
  }
}

function updateProgressSteps(currentStatus) {
  const steps = document.querySelectorAll('.step');
  const statusOrder = ['Awaiting Deposit', 'Confirming Deposit', 'Exchanging', 'Sending', 'Complete'];
  const currentIndex = statusOrder.indexOf(currentStatus);

  steps.forEach((step, index) => {
    step.classList.remove('active', 'completed');
    if (index < currentIndex) {
      step.classList.add('completed');
      step.querySelector('.step-circle').textContent = '✓';
    } else if (index === currentIndex) {
      step.classList.add('active');
      step.querySelector('.step-circle').textContent = index + 1;
    } else {
      step.querySelector('.step-circle').textContent = index + 1;
    }
  });

  if (['Failed', 'Refund', 'Action Request', 'Request Overdue'].includes(currentStatus)) {
    steps.forEach(step => step.classList.remove('active'));
  }
}

const STATUS_MESSAGES = {
  'Awaiting Deposit': {
    lines: [
      { text: 'Your order will automatically proceed to the next step once your deposit receives its first confirmation on the blockchain.' },
      { text: 'If you do not deposit the amount shown above, or your deposit does not arrive within 1 hour, for security purposes your order will not be processed automatically.' }
    ]
  },
  'Confirming Deposit': {
    lines: [
      { text: 'You successfully sent {sendAmount} {send}! Please wait while your deposit is being confirmed.', highlight: 'You successfully sent {sendAmount} {send}!' },
      { text: 'Your order will automatically proceed to the next step after the deposit transaction gets 1 confirmation.' },
      { text: 'Nothing more is expected from you in this step.' }
    ]
  },
  'Exchanging': {
    lines: [
      { text: 'Your deposit has been confirmed! We are now exchanging your {sendAmount} {send} to {receiveAmount} {receive}.', highlight: 'We are now exchanging your {sendAmount} {send} to {receiveAmount} {receive}' },
      { text: 'This may take a few minutes, please be patient.' }
    ]
  },
  'Sending': {
    lines: [
      { text: 'Your order is almost complete! We are forwarding {receiveAmount} {receive} to the following address: {receiveAddress}', highlight: 'We are forwarding {receiveAmount} {receive}' }
    ]
  },
  'Complete': {
    lines: [
      { text: 'Your order is successfully completed! We forwarded {receiveAmount} {receive} to the following address: {receiveAddress}', highlight: 'We forwarded {receiveAmount} {receive}' }
    ]
  },
  'Action Request': {
    lines: [
      { text: 'This transaction has been detected with risks and needs to be verified before proceeding.' },
      { text: 'Please contact lightningex.io for support.' }
    ]
  },
  'Failed': {
    lines: [
      { text: 'The order failed because of one of the following reasons:', highlight: 'The order failed' },
      { text: '• You didn\'t send {sendAmount} {send} on the {sendNetwork} network.' },
      { text: '• Your deposit was not confirmed within 2 hours.' },
      { text: '• For any other reason.' }
    ]
  },
  'Request Overdue': {
    lines: [
      { text: 'The transaction request has expired.', highlight: 'expired' },
      { text: 'If you have other questions, please seek support from lightningex.io.' }
    ]
  }
};

function formatStatusMessage(status, data) {
  const msgInfo = STATUS_MESSAGES[status];
  if (!msgInfo) return '';

  return msgInfo.lines.map(lineObj => {
    const line = typeof lineObj === 'string' ? lineObj : lineObj.text;
    const highlight = typeof lineObj === 'object' ? lineObj.highlight : null;

    let formatted = line;
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formatted = formatted.replace(new RegExp(`{${key}}`, 'g'), data[key]);
      }
    });

    if (highlight) {
      let highlightText = highlight;
      Object.keys(data).forEach(key => {
        if (data[key] !== null && data[key] !== undefined) {
          highlightText = highlightText.replace(new RegExp(`{${key}}`, 'g'), data[key]);
        }
      });
      formatted = formatted.replace(highlightText, `<span class="status-highlight">${highlightText}</span>`);
    }

    return formatted;
  }).join('<br>');
}

function updateStatusContent(data) {
  const container = document.getElementById('statusContent');
  const statusClass = getStatusClass(data.status);
  const statusMessage = formatStatusMessage(data.status, data);

  let html = `
    <div class="status-header">
      <div class="status-badge ${statusClass}">${data.status}</div>
    </div>
  `;

  if (statusMessage) {
    html += `
      <div class="status-message-box">
        <p>${statusMessage}</p>
      </div>
    `;
  }

  if (data.status === 'Awaiting Deposit') {
    html += `
      <div class="deposit-section">
        <div class="qr-container">
          <div id="qrcode"></div>
        </div>
        <div class="deposit-info">
          <div class="info-row">
            <span class="info-label">Send ${data.send} on ${data.sendNetwork} network to this address</span>
            <div class="info-value">
              <span class="address-value">${data.sendAddress}</span>
              <button class="copy-btn" onclick="copyToClipboard('${data.sendAddress}')">Copy</button>
            </div>
          </div>
          ${data.sendTag ? `
          <div class="info-row">
            <span class="info-label">Tag/MEMO (Required)</span>
            <div class="info-value">
              <span class="address-value">${data.sendTag}</span>
              <button class="copy-btn" onclick="copyToClipboard('${data.sendTag}')">Copy</button>
            </div>
          </div>
          ` : ''}
          <div class="info-row">
            <span class="info-label">Amount to Send</span>
            <div class="info-value">
              <span>${data.sendAmount} ${data.send}</span>
              <button class="copy-btn" onclick="copyToClipboard('${data.sendAmount}')">Copy</button>
            </div>
          </div>
          <div class="warning-box">
            ⚠️ Please send exactly the specified amount. Sending a different amount may result in delays or additional fees.
          </div>
        </div>
      </div>
    `;

    setTimeout(() => {
      const qrContainer = document.getElementById('qrcode');
      if (qrContainer) {
        qrContainer.innerHTML = '';
        new QRCode(qrContainer, {
          text: data.sendAddress,
          width: 140,
          height: 140,
          colorDark: '#000000',
          colorLight: '#ffffff'
        });
      }
    }, 0);
  }

  if (['Confirming Deposit', 'Exchanging', 'Sending'].includes(data.status)) {
    html += `
      <div class="processing-container">
        <div class="loading-spinner"></div>
        <p style="color: var(--neon-cyan);">Estimated time: ${data.processingTime || '3-5'} minutes</p>
      </div>
    `;
  }

  if (data.status === 'Complete') {
    html += `
      <div class="complete-container">
        <div class="complete-icon">🎉</div>
        <h2 style="color: var(--neon-green); margin-bottom: 20px;">Exchange Complete!</h2>
        <a href="./index.html" class="btn btn-primary">Start New Exchange →</a>
      </div>
    `;
  }

  if (['Failed', 'Refund', 'Action Request', 'Request Overdue'].includes(data.status)) {
    const icon = data.status === 'Action Request' ? '⚠️' : (data.status === 'Request Overdue' ? '⏰' : '❌');
    html += `
      <div class="failed-container">
        <div class="failed-icon">${icon}</div>
        ${data.statusNote ? `<p style="color: var(--text-secondary); margin-top: 10px;">${data.statusNote}</p>` : ''}
        <a href="https://www.lightningex.io" target="_blank" class="btn btn-secondary" style="margin-top: 20px;">Contact Support</a>
      </div>
    `;
  }

  container.innerHTML = html;
}

function updateTransactionDetails(data) {
  document.getElementById('sendAmount').textContent = data.sendAmount;
  document.getElementById('sendCurrency').textContent = `${data.send} (${data.sendNetwork})`;
  document.getElementById('receiveAmount').textContent = data.receiveAmount;
  document.getElementById('receiveCurrency').textContent = `${data.receive} (${data.receiveNetwork})`;

  const detailList = document.getElementById('detailList');
  const createdAt = data.createdAt ? new Date(data.createdAt).toLocaleString() : 'N/A';
  
  detailList.innerHTML = `
    <div class="detail-item">
      <span class="detail-item-label">Order ID</span>
      <span class="detail-item-value">${data.id}</span>
    </div>
    <div class="detail-item">
      <span class="detail-item-label">Created At</span>
      <span class="detail-item-value">${createdAt}</span>
    </div>
    <div class="detail-item">
      <span class="detail-item-label">Receive Address</span>
      <span class="detail-item-value">${data.receiveAddress}</span>
    </div>
    ${data.receiveTag ? `
    <div class="detail-item">
      <span class="detail-item-label">Receive Tag/MEMO</span>
      <span class="detail-item-value">${data.receiveTag}</span>
    </div>
    ` : ''}
    ${data.networkFee ? `
    <div class="detail-item">
      <span class="detail-item-label">Network Fee</span>
      <span class="detail-item-value">${data.networkFee} ${data.receive}</span>
    </div>
    ` : ''}
  `;

  const txLinksContainer = document.getElementById('txLinks');
  let linksHtml = '';
  
  if (data.hashIn && data.hashIn.length > 0 && data.hashInExplorer) {
    linksHtml += `
      <div class="tx-link">
        <span>Incoming Transaction</span>
        <a href="${data.hashInExplorer.replace('{{txid}}', data.hashIn[0])}" target="_blank">View on Explorer →</a>
      </div>
    `;
  }
  
  if (data.hashOut && data.hashOut.length > 0 && data.hashOutExplorer) {
    linksHtml += `
      <div class="tx-link">
        <span>Outgoing Transaction</span>
        <a href="${data.hashOutExplorer.replace('{{txid}}', data.hashOut[0])}" target="_blank">View on Explorer →</a>
      </div>
    `;
  }
  
  txLinksContainer.innerHTML = linksHtml;
}

function getStatusClass(status) {
  const statusClasses = {
    'Awaiting Deposit': 'awaiting',
    'Confirming Deposit': 'confirming',
    'Exchanging': 'exchanging',
    'Sending': 'sending',
    'Complete': 'complete',
    'Failed': 'failed',
    'Refund': 'refund',
    'Action Request': 'action-request',
    'Request Overdue': 'request-overdue'
  };
  return statusClasses[status] || 'awaiting';
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert('Copied to clipboard!');
  });
}

function copyOrderUrl() {
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    const btn = document.getElementById('copyUrlBtn');
    const originalText = btn.textContent;
    btn.textContent = 'Copied!';
    setTimeout(() => {
      btn.textContent = originalText;
    }, 2000);
  });
}

function copyOrderId() {
  if (!orderId) return;
  navigator.clipboard.writeText(orderId).then(() => {
    alert('Order ID copied!');
  });
}
