#!/usr/bin/env node
/**
 * Crypto Exchange CLI - LightningEX API Client (Node.js)
 * Usage: crypto-swap [command] [options]
 */
const https = require('https');
const readline = require('readline');
const path = require('path');
const fs = require('fs');
const http = require('http');
const API_BASE = 'api.lightningex.io';
const useColor = !process.env.NO_COLOR && process.stdout.isTTY;
const COLORS = {
  reset: useColor ? '\x1b[0m' : '',
  bright: useColor ? '\x1b[1m' : '',
  green: useColor ? '\x1b[32m' : '',
  brightGreen: useColor ? '\x1b[1;32m' : ''
};
const STATUS_MESSAGES = {
  'Awaiting Deposit': {
    title: '⏳ Awaiting Deposit',
    lines: [
      'Your order will automatically proceed to the next step once your deposit receives its first confirmation on the blockchain.',
      'If you do not deposit the amount shown above, or your deposit does not arrive within 1 hour, for security purposes your order will not be processed automatically.'
    ]
  },
  'Confirming Deposit': {
    title: '✅ Confirming Deposit',
    lines: [
      'You successfully sent {sendAmount} {send}! Please wait while your deposit is being confirmed.',
      'Your order will automatically proceed to the next step after the deposit transaction gets 1 confirmation.',
      'Nothing more is expected from you in this step.'
    ]
  },
  'Exchanging': {
    title: '🔄 Exchanging',
    lines: [
      'Your deposit has been confirmed! We are now exchanging your {sendAmount} {send} to {receiveAmount} {receive}.',
      'This may take a few minutes, please be patient.'
    ]
  },
  'Sending': {
    title: '📤 Sending',
    lines: [
      'Your order is almost complete! We are forwarding {receiveAmount} {receive} to the following address: {receiveAddress}'
    ]
  },
  'Complete': {
    title: '🎉 Complete',
    lines: [
      'Your order is successfully completed! We forwarded {receiveAmount} {receive} to the following address: {receiveAddress}'
    ]
  },
  'Action Request': {
    title: '⚠️ Action Request',
    lines: [
      'This transaction has been detected with risks and needs to be verified before proceeding.',
      'Please contact lightningex.io for support.'
    ]
  },
  'Failed': {
    title: '❌ Failed',
    lines: [
      'The order failed because of one of the following reasons:',
      '• You didn\'t send {sendAmount} {send} on the {sendNetwork} network.',
      '• Your deposit was not confirmed within 2 hours.',
      '• For any other reason.'
    ]
  },
  'Request Overdue': {
    title: '⏰ Request Overdue',
    lines: [
      'The transaction request has expired.',
      'If you have other questions, please seek support from lightningex.io.'
    ]
  }
};
function apiRequest(endpoint, method = 'GET', data = null, silent = false) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: API_BASE,
      path: endpoint,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 30000
    };
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.code !== 200 && !silent) {
            console.error(`❌ API Error: ${result.msg || 'Unknown error'}`);
          }
          resolve(result);
        } catch (e) {
          if (!silent) console.error(`❌ Parse Error: ${e.message}`);
          resolve({ code: 500, msg: e.message });
        }
      });
    });
    req.on('error', (e) => {
      if (!silent) console.error(`❌ Error: ${e.message}`);
      resolve({ code: 500, msg: e.message });
    });
    req.on('timeout', () => {
      req.destroy();
      if (!silent) console.error('❌ Request timeout');
      resolve({ code: 500, msg: 'Timeout' });
    });
    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}
function createRL() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}
function prompt(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => resolve(answer.trim()));
  });
}
function printHeader(title) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`  ${title}`);
  console.log(`${'='.repeat(60)}`);
}
function printStep(stepNum, total, title) {
  console.log(`\n📍 Step ${stepNum}/${total}: ${title}`);
  console.log('-'.repeat(40));
}
async function selectFromList(items, titleKey, subtitleKey = null, promptText = 'Select') {
  if (!items || items.length === 0) {
    console.log('❌ No options available');
    return null;
  }
  console.log();
  items.forEach((item, i) => {
    const title = item[titleKey] || 'Unknown';
    if (subtitleKey && item[subtitleKey]) {
      console.log(`  ${i + 1}. ${title} (${item[subtitleKey]})`);
    } else {
      console.log(`  ${i + 1}. ${title}`);
    }
  });
  const rl = createRL();
  while (true) {
    const choice = await prompt(rl, `\n${promptText} (1-${items.length}): `);
    if (['q', 'quit', 'exit'].includes(choice.toLowerCase())) {
      rl.close();
      process.exit(0);
    }
    const idx = parseInt(choice) - 1;
    if (idx >= 0 && idx < items.length) {
      rl.close();
      return items[idx];
    }
    console.log('❌ Invalid selection');
  }
}
function formatStatusMessage(status, orderData) {
  if (!STATUS_MESSAGES[status]) {
    return `Status: ${status}`;
  }
  const msgInfo = STATUS_MESSAGES[status];
  const lines = msgInfo.lines.map(line => {
    return line.replace(/\{(\w+)\}/g, (match, key) => orderData[key] || match);
  });
  return '\n   ' + [msgInfo.title, ...lines.map(l => '• ' + l)].join('\n   ');
}
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function cmdWizard() {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ⚡ LightningEX - Crypto Exchange Wizard                 ║
║                                                          ║
║  Follow the steps to complete your exchange              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    `);
  // Step 1: Load currencies
  printStep(1, 8, 'Loading available currencies...');
  const result = await apiRequest('/exchange/currency/list');
  if (result.code !== 200) {
    console.log('❌ Failed to load currencies');
    return;
  }
  const currencies = result.data;
  const sendCurrencies = currencies.filter(c => c.sendStatusAll);
  const receiveCurrencies = currencies.filter(c => c.receiveStatusAll);
  console.log(`✓ Loaded ${sendCurrencies.length} send currencies, ${receiveCurrencies.length} receive currencies`);
  // Step 2: Select send currency
  printStep(2, 8, 'Select currency to send');
  const sendCurrency = await selectFromList(
    sendCurrencies,
    'currency',
    'name',
    'Select currency to send'
  );
  if (!sendCurrency) return;
  console.log(`${COLORS.brightGreen}✓ You selected send currency: ${sendCurrency.currency} (${sendCurrency.name})${COLORS.reset}`);
  // Step 3: Select send network
  printStep(3, 8, `Select network for ${sendCurrency.currency} send`);
  const sendNetworks = sendCurrency.networkList?.filter(n => n.sendStatus) || [];
  const sendNetwork = await selectFromList(
    sendNetworks,
    'name',
    'network',
    `Select network for ${sendCurrency.currency} send`
  );
  if (!sendNetwork) return;
  console.log(`${COLORS.brightGreen}✓ You selected send network: ${sendNetwork.name} (${sendNetwork.network})${COLORS.reset}`);
  // Step 4: Select receive currency
  printStep(4, 8, 'Select currency to receive');
  const receiveCurrency = await selectFromList(
    receiveCurrencies,
    'currency',
    'name',
    'Select currency to receive'
  );
  if (!receiveCurrency) return;
  console.log(`${COLORS.brightGreen}✓ You selected receive currency: ${receiveCurrency.currency} (${receiveCurrency.name})${COLORS.reset}`);
  // Step 5: Select receive network
  printStep(5, 8, `Select network for ${receiveCurrency.currency} receive`);
  const receiveNetworks = receiveCurrency.networkList?.filter(n => n.receiveStatus) || [];
  if (receiveNetworks.length === 0) {
    console.log(`❌ No receive networks available for ${receiveCurrency.currency}`);
    return;
  }
  const receiveNetwork = await selectFromList(
    receiveNetworks,
    'name',
    'network',
    `Select network for ${receiveCurrency.currency} receive`
  );
  if (!receiveNetwork) return;
  console.log(`${COLORS.brightGreen}✓ You selected receive network: ${receiveNetwork.name} (${receiveNetwork.network})${COLORS.reset}`);
  // Step 6: Fetch pair info (now requires all 4 selections)
  printStep(6, 8, 'Fetching pair information...');
  console.log('\n📊 Loading exchange limits...');
  const pairResult = await apiRequest(
    `/exchange/pair/info?send=${sendCurrency.currency}` +
    `&receive=${receiveCurrency.currency}` +
    `&sendNetwork=${sendNetwork.network}` +
    `&receiveNetwork=${receiveNetwork.network}`
  );
  if (pairResult.code !== 200) {
    console.log(`❌ Failed to get pair info: ${pairResult.msg || 'Unknown error'}`);
    return;
  }
  const pairInfo = pairResult.data;
  console.log(`
    ┌─────────────────────────────────────────┐
    │  Exchange Limits                        │
    ├─────────────────────────────────────────┤
    │  Minimum: ${pairInfo.minimumAmount.padStart(20)} ${sendCurrency.currency}  │
    │  Maximum: ${pairInfo.maximumAmount.padStart(20)} ${sendCurrency.currency}  │
    │  Network Fee: ${pairInfo.networkFee.padStart(16)} ${receiveCurrency.currency}  │
    │  Processing: ${pairInfo.processingTime.padStart(17)} min  │
    └─────────────────────────────────────────┘
    `);
  // Step 7: Enter amount
  printStep(7, 8, 'Enter exchange amount');
  const rl = createRL();
  let amount;
  while (true) {
    const amountInput = await prompt(
      rl,
      `Amount to send (${pairInfo.minimumAmount} - ${pairInfo.maximumAmount} ${sendCurrency.currency}): `
    );
    const parsed = parseFloat(amountInput);
    const minAmt = parseFloat(pairInfo.minimumAmount);
    const maxAmt = parseFloat(pairInfo.maximumAmount);
    if (isNaN(parsed)) {
      console.log('❌ Please enter a valid number');
      continue;
    }
    if (parsed < minAmt) {
      console.log(`❌ Amount too small. Minimum is ${pairInfo.minimumAmount}`);
      continue;
    }
    if (parsed > maxAmt) {
      console.log(`❌ Amount too large. Maximum is ${pairInfo.maximumAmount}`);
      continue;
    }
    amount = parsed;
    console.log(`${COLORS.brightGreen}✓ You entered ${amount} ${sendCurrency.currency} to send${COLORS.reset}`);
    break;
  }
  // Get exchange rate
  console.log('\n📈 Fetching exchange rate...');
  const rateResult = await apiRequest(
    `/exchange/rate?send=${sendCurrency.currency}` +
    `&receive=${receiveCurrency.currency}` +
    `&sendNetwork=${sendNetwork.network}` +
    `&receiveNetwork=${receiveNetwork.network}` +
    `&amount=${amount}`
  );
  if (rateResult.code !== 200) {
    console.log(`❌ Failed to get rate: ${rateResult.msg || 'Unknown error'}`);
    rl.close();
    return;
  }
  const rateInfo = rateResult.data;
  console.log(`
    ┌─────────────────────────────────────────┐
    │  Exchange Rate                          │
    ├─────────────────────────────────────────┤
    │  1 ${sendCurrency.currency.padEnd(6)} = ${rateInfo.rate.padStart(16)} ${receiveCurrency.currency}  │
    │                                         │
    │  You Send:      ${rateInfo.sendAmount.padStart(20)} ${sendCurrency.currency}  │
    │  You Receive:   ${rateInfo.receiveAmount.padStart(20)} ${receiveCurrency.currency}  │
    │  Network Fee:   ${rateInfo.networkFee.padStart(20)} ${receiveCurrency.currency}  │
    └─────────────────────────────────────────┘
    `);
  // Step 8: Enter receive address
  printStep(8, 8, 'Enter receive address');
  let address;
  while (true) {
    address = await prompt(
      rl,
      `Your ${receiveCurrency.currency} (${receiveNetwork.network}) address: `
    );
    if (!address) {
      console.log('❌ Address cannot be empty');
      continue;
    }
    console.log('🔍 Validating address...');
    const valResult = await apiRequest(
      `/exchange/address/validate?currency=${receiveCurrency.currency}` +
      `&address=${address}&network=${receiveNetwork.network}`
    );
    if (valResult.code === 200 && valResult.data) {
      console.log(`${COLORS.brightGreen}✓ You entered receive address: ${address}${COLORS.reset}`);
      break;
    } else {
      console.log('❌ Invalid address. Please check and try again.');
    }
  }
  // Final confirmation
  printHeader('Order Summary');
  console.log(`
    Send:        ${amount} ${sendCurrency.currency} (${sendNetwork.name})
    Receive:     ${rateInfo.receiveAmount} ${receiveCurrency.currency} (${receiveNetwork.name})
    Rate:        1 ${sendCurrency.currency} = ${rateInfo.rate} ${receiveCurrency.currency}
    To Address:  ${address}
    `);
  const confirm = await prompt(rl, '\n✋ Confirm and place order? (yes/no): ');
  if (!['yes', 'y'].includes(confirm.toLowerCase())) {
    console.log('❌ Order cancelled');
    rl.close();
    return;
  }
  // Place order
  console.log('\n🚀 Placing order...');
  const orderData = {
    send: sendCurrency.currency,
    sendNetwork: sendNetwork.network,
    receive: receiveCurrency.currency,
    receiveNetwork: receiveNetwork.network,
    amount: String(amount),
    receiveAddress: address
  };
  const orderResult = await apiRequest('/exchange/order/place', 'POST', orderData);
  if (orderResult.code !== 200) {
    console.log(`❌ Order failed: ${orderResult.msg || 'Unknown error'}`);
    rl.close();
    return;
  }
  const orderId = orderResult.data;
  console.log('\n📋 Fetching order details...');
  const orderDetails = await apiRequest(`/exchange/order/get?id=${orderId}`);
  if (orderDetails.code !== 200) {
    console.log(`⚠️  Order created but failed to get details. Order ID: ${orderId}`);
    rl.close();
    return;
  }
  const order = orderDetails.data;
  console.log(`
╔══════════════════════════════════════════════════════════╗
║  ✅ Order Placed Successfully!                           ║
╠══════════════════════════════════════════════════════════╣
║  Order ID: ${orderId.padEnd(45)} ║
╠══════════════════════════════════════════════════════════╣
║  ⬇️  SEND YOUR FUNDS TO:                                 ║
╠══════════════════════════════════════════════════════════╣
║  Currency:   ${(order.send + ' (' + order.sendNetwork + ')').padEnd(42)} ║
║  Address:    ${order.sendAddress.padEnd(42)} ║
${order.sendTag ? `║  Tag/MEMO:  ${order.sendTag.padEnd(42)} ║` : ''}
║  Amount:    ${(order.sendAmount + ' ' + order.send).padEnd(42)} ║
╠══════════════════════════════════════════════════════════╣
║  ⚠️  IMPORTANT:                                          ║
║  • Send EXACTLY the specified amount                     ║
║  • Include the Tag/MEMO if provided                      ║
║  • Transaction will be processed after confirmation      ║
╚══════════════════════════════════════════════════════════╝
    `);
  // Auto-monitor
  console.log('\n📊 Auto-monitoring order progress...');
  console.log(`\n🔑 Order ID: ${orderId}`);
  console.log('   (Save this ID to check status later)\n');
  console.log('Press Ctrl+C to stop monitoring\n');
  const statusOrder = ['Awaiting Deposit', 'Confirming Deposit', 'Exchanging', 'Sending', 'Complete'];
  let lastStatus = null;
  rl.close();
  try {
    while (true) {
      const result = await apiRequest(`/exchange/order/get?id=${orderId}`, 'GET', null, true);
      if (result.code !== 200) {
        await sleep(15000);
        continue;
      }
      const data = result.data;
      const status = data.status;
      if (status !== lastStatus) {
        lastStatus = status;
        // Progress bar
        if (statusOrder.includes(status)) {
          const currentIdx = statusOrder.indexOf(status);
          const progress = (currentIdx / (statusOrder.length - 1)) * 100;
          const barWidth = 30;
          const filled = Math.floor(barWidth * progress / 100);
          const bar = '█'.repeat(filled) + '░'.repeat(barWidth - filled);
          console.log(`\r[${bar}] ${Math.round(progress)}% - ${status}`);
        } else {
          console.log(`\rStatus: ${status}`);
        }
        console.log(formatStatusMessage(status, data));
        // Additional info
        if (status === 'Awaiting Deposit') {
          console.log(`\n   🔑 Order ID: ${orderId}`);
          console.log(`   💰 Send: ${data.sendAmount} ${data.send} (${data.sendNetwork})`);
          console.log(`   📍 Deposit Address: ${data.sendAddress}`);
          if (data.sendTag) console.log(`   🏷️  Tag/MEMO: ${data.sendTag}`);
        } else if (status === 'Confirming Deposit' && data.hashIn?.length) {
          console.log(`\n   🔗 Transaction: ${data.hashIn[0]}`);
          if (data.hashInExplorer) {
            const explorerUrl = data.hashInExplorer.replace('{{txid}}', data.hashIn[0]);
            console.log(`   🔍 Explorer: ${explorerUrl}`);
          }
        } else if (status === 'Sending' && data.hashOut?.length) {
          console.log(`\n   🔗 Outgoing TX: ${data.hashOut[0]}`);
          if (data.hashOutExplorer) {
            const explorerUrl = data.hashOutExplorer.replace('{{txid}}', data.hashOut[0]);
            console.log(`   🔍 Explorer: ${explorerUrl}`);
          }
        }
        if (status === 'Complete') {
          console.log(`
╔══════════════════════════════════════════════════════════╗
║  🎉 Exchange Complete!                                   ║
╠══════════════════════════════════════════════════════════╣
║  Received: ${(data.receiveAmount + ' ' + data.receive).padEnd(42)} ║
║  To:       ${data.receiveAddress.slice(0, 40).padEnd(42)} ║
╚══════════════════════════════════════════════════════════╝
          `);
          if (data.hashOut?.length) {
            console.log(`Transaction: ${data.hashOut[0]}`);
            if (data.hashOutExplorer) {
              const explorerUrl = data.hashOutExplorer.replace('{{txid}}', data.hashOut[0]);
              console.log(`Explorer: ${explorerUrl}`);
            }
          }
          break;
        } else if (['Failed', 'Action Request', 'Request Overdue'].includes(status)) {
          const title = STATUS_MESSAGES[status]?.title || `❌ ${status}`;
          console.log(`
╔══════════════════════════════════════════════════════════╗
║  ${title.padEnd(56)} ║
╠══════════════════════════════════════════════════════════╣
║  ${(data.statusNote || 'Please contact support at lightningex.io').slice(0, 54).padEnd(54)} ║
╚══════════════════════════════════════════════════════════╝
          `);
          break;
        }
      }
      await sleep(15000);
    }
  } catch (e) {
    if (e.name === 'SIGINT') {
      console.log(`\n\n👋 Monitoring stopped.`);
      console.log(`Order ID: ${orderId}`);
      console.log(`Check status anytime: crypto-exchange status --id ${orderId}`);
    }
  }
}
async function cmdCurrencies() {
  const result = await apiRequest('/exchange/currency/list');
  console.log('\nSupported Currencies:');
  console.log('='.repeat(80));
  for (const currency of result.data) {
    const symbol = currency.currency;
    const name = currency.name;
    const sendOk = currency.sendStatusAll ? '✓' : '✗';
    const recvOk = currency.receiveStatusAll ? '✓' : '✗';
    console.log(`\n${symbol} - ${name} [Send:${sendOk} Receive:${recvOk}]`);
    for (const net of currency.networkList || []) {
      const netSend = net.sendStatus ? '✓' : '✗';
      const netRecv = net.receiveStatus ? '✓' : '✗';
      const isDefault = net.isDefault ? ' [DEFAULT]' : '';
      console.log(`  └── ${net.network} (${net.name}) Send:${netSend} Recv:${netRecv}${isDefault}`);
    }
  }
}
async function cmdPairList(args) {
  let params = `send=${args.send}&receive=${args.receive}`;
  if (args.send_network || args.sendNetwork) {
    params += `&sendNetwork=${args.send_network || args.sendNetwork}`;
  }
  const result = await apiRequest(`/exchange/pair/list?${params}`);
  if (result.code !== 200) {
    console.log(`❌ Failed to get pair list: ${result.msg || 'Unknown error'}`);
    return;
  }
  const pairs = result.data;
  console.log('\nSupported Currency Pairs');
  console.log('='.repeat(60));
  if (pairs.length === 0) {
    console.log('No pairs found for the specified criteria.');
    return;
  }
  pairs.forEach((pair, index) => {
    console.log(`  ${index + 1}. ${pair}`);
  });
  console.log(`\nTotal: ${pairs.length} pair(s)`);
}
async function cmdPair(args) {
  let params = `send=${args.send}&receive=${args.receive}`;
  const sendNetwork = args.sendNetwork || args.send_network;
  const receiveNetwork = args.receiveNetwork || args.receive_network;
  if (sendNetwork) params += `&sendNetwork=${sendNetwork}`;
  if (receiveNetwork) params += `&receiveNetwork=${receiveNetwork}`;
  const result = await apiRequest(`/exchange/pair/info?${params}`);
  const data = result.data;
  console.log(`\nPair Info: ${args.send} → ${args.receive}`);
  console.log('='.repeat(50));
  console.log(`Minimum Amount: ${data.minimumAmount}`);
  console.log(`Maximum Amount: ${data.maximumAmount}`);
  console.log(`Network Fee: ${data.networkFee}`);
  console.log(`Confirmations: ${data.confirmations}`);
  console.log(`Processing Time: ${data.processingTime} minutes`);
}
async function cmdRate(args) {
  let params = `send=${args.send}&receive=${args.receive}&amount=${args.amount}`;
  const sendNetwork = args.sendNetwork || args.send_network;
  const receiveNetwork = args.receiveNetwork || args.receive_network;
  if (sendNetwork) params += `&sendNetwork=${sendNetwork}`;
  if (receiveNetwork) params += `&receiveNetwork=${receiveNetwork}`;
  const result = await apiRequest(`/exchange/rate?${params}`);
  const data = result.data;
  console.log(`\nExchange Rate: ${args.send} → ${args.receive}`);
  console.log('='.repeat(50));
  console.log(`Rate: 1 ${args.send} = ${data.rate} ${args.receive}`);
  console.log(`You Send: ${data.sendAmount} ${args.send}`);
  console.log(`You Receive: ${data.receiveAmount} ${args.receive}`);
  console.log(`Network Fee: ${data.networkFee}`);
  console.log(`Processing Time: ${data.processingTime} minutes`);
}
async function cmdValidate(args) {
  let params = `currency=${args.currency}&address=${args.address}`;
  if (args.network) params += `&network=${args.network}`;
  const result = await apiRequest(`/exchange/address/validate?${params}`);
  const valid = result.data;
  const status = valid ? '✓ Valid' : '✗ Invalid';
  console.log(`\nAddress Validation: ${status}`);
}
async function cmdOrder(args) {
  const sendNetwork = args.sendNetwork || args.send_network;
  const receiveNetwork = args.receiveNetwork || args.receive_network;
  const receiveAddress = args.address || args.receive_address || args.receiveAddress;
  const orderData = {
    send: args.send,
    receive: args.receive,
    amount: String(args.amount),
    receiveAddress: receiveAddress
  };
  if (sendNetwork) orderData.sendNetwork = sendNetwork;
  if (receiveNetwork) orderData.receiveNetwork = receiveNetwork;
  if (!args.yes) {
    let params = `send=${args.send}&receive=${args.receive}&amount=${args.amount}`;
    if (sendNetwork) params += `&sendNetwork=${sendNetwork}`;
    if (receiveNetwork) params += `&receiveNetwork=${receiveNetwork}`;
    const rateResult = await apiRequest(`/exchange/rate?${params}`);
    const rateData = rateResult.data;
    console.log('\nOrder Preview:');
    console.log('='.repeat(50));
    console.log(`Send: ${args.amount} ${args.send}`);
    console.log(`Receive: ${rateData.receiveAmount} ${args.receive}`);
    console.log(`To Address: ${receiveAddress}`);
    console.log(`Network Fee: ${rateData.networkFee}`);
    const rl = createRL();
    const confirm = await prompt(rl, '\nConfirm order? (yes/no): ');
    rl.close();
    if (confirm.toLowerCase() !== 'yes') {
      console.log('Order cancelled.');
      return;
    }
  }
  const result = await apiRequest('/exchange/order/place', 'POST', orderData);
  const orderId = result.data;
  console.log('\n✓ Order placed successfully!');
  console.log(`Order ID: ${orderId}`);
  console.log(`Track status: crypto-exchange monitor --id ${orderId}`);
}
async function cmdStatus(args) {
  const result = await apiRequest(`/exchange/order/get?id=${args.id}`);
  const data = result.data;
  console.log(`\nOrder Status: ${args.id}`);
  console.log('='.repeat(60));
  console.log(formatStatusMessage(data.status, data));
  if (data.statusNote) {
    console.log(`\nNote: ${data.statusNote}`);
  }
  console.log(`\n${'─'.repeat(60)}`);
  console.log(`Send: ${data.sendAmount} ${data.send} (${data.sendNetwork})`);
  console.log(`Receive: ${data.receiveAmount} ${data.receive} (${data.receiveNetwork})`);
  console.log(`\nDeposit Address: ${data.sendAddress}`);
  if (data.sendTag) console.log(`Deposit Tag: ${data.sendTag}`);
  console.log(`Receive Address: ${data.receiveAddress}`);
  if (data.hashIn?.length) {
    console.log(`\nIncoming TX: ${data.hashIn.join(', ')}`);
    if (data.hashInExplorer) {
      for (const tx of data.hashIn) {
        const explorerUrl = data.hashInExplorer.replace('{{txid}}', tx);
        console.log(`  Explorer: ${explorerUrl}`);
      }
    }
  }
  if (data.hashOut?.length) {
    console.log(`\nOutgoing TX: ${data.hashOut.join(', ')}`);
    if (data.hashOutExplorer) {
      for (const tx of data.hashOut) {
        const explorerUrl = data.hashOutExplorer.replace('{{txid}}', tx);
        console.log(`  Explorer: ${explorerUrl}`);
      }
    }
  }
  const created = new Date(data.createdAt).toLocaleString();
  console.log(`\nCreated: ${created}`);
}
async function cmdMonitor(args) {
  console.log(`Monitoring order ${args.id}...`);
  console.log('Press Ctrl+C to stop\n');
  let lastStatus = null;
  try {
    while (true) {
      const result = await apiRequest(`/exchange/order/get?id=${args.id}`);
      const data = result.data;
      const status = data.status;
      if (status !== lastStatus) {
        lastStatus = status;
        console.log(`\n${'='.repeat(60)}`);
        console.log(formatStatusMessage(status, data));
        if (status === 'Awaiting Deposit') {
          console.log(`\n💰 Send: ${data.sendAmount} ${data.send} (${data.sendNetwork})`);
          console.log(`📍 Send to: ${data.sendAddress}`);
          if (data.sendTag) console.log(`🏷️  Tag/MEMO: ${data.sendTag}`);
        } else if (status === 'Confirming Deposit' && data.hashIn?.length) {
          console.log(`\n🔗 TX: ${data.hashIn[0]}`);
        } else if (status === 'Sending' && data.hashOut?.length) {
          console.log(`\n🔗 Outgoing: ${data.hashOut[0]}`);
        }
      }
      if (['Complete', 'Failed', 'Action Request', 'Request Overdue'].includes(status)) {
        console.log(`\n${'='.repeat(60)}`);
        console.log(`Final Status: ${status}`);
        if (data.hashOut?.length) {
          console.log(`Outgoing TX: ${data.hashOut.join(', ')}`);
          if (data.hashOutExplorer) {
            for (const tx of data.hashOut) {
              const explorerUrl = data.hashOutExplorer.replace('{{txid}}', tx);
              console.log(`Explorer: ${explorerUrl}`);
            }
          }
        }
        break;
      }
      await sleep(15000);
    }
  } catch (e) {
    console.log('\n\nMonitoring stopped.');
  }
}
async function cmdUI(args) {
  const port = args.port || 8080;
  // Find UI directory (swap.js is in skill root, so __dirname is the skill dir)
  const skillDir = __dirname;
  const uiDir = path.join(skillDir, 'assets', 'ui');
  if (!fs.existsSync(uiDir)) {
    console.error(`Error: UI assets not found at ${uiDir}`);
    process.exit(1);
  }
  const server = http.createServer((req, res) => {
    // Remove query string from URL
    const urlPath = req.url.split('?')[0];
    let filePath = path.join(uiDir, urlPath === '/' ? 'index.html' : urlPath);
    
    // Prevent path traversal: ensure filePath is within uiDir
    const resolvedPath = path.resolve(filePath);
    const resolvedUiDir = path.resolve(uiDir);
    if (!resolvedPath.startsWith(resolvedUiDir)) {
      res.writeHead(403);
      res.end('Forbidden');
      return;
    }
    
    const ext = path.extname(filePath);
    const contentType = {
      '.html': 'text/html',
      '.js': 'text/javascript',
      '.css': 'text/css',
      '.json': 'application/json'
    }[ext] || 'application/octet-stream';
    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    });
  });
  server.listen(port);
  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      // Port in use, try random port
      console.log(`Port ${port} in use, trying another port...`);
      server.listen(0);
    } else {
      console.error('Server error:', err.message);
      process.exit(1);
    }
  });
  // Handle the 'listening' event for the fallback port
  server.on('listening', () => {
    const actualPort = server.address().port;
    const url = `http://localhost:${actualPort}`;
    console.log(`🚀 Crypto Swap UI running at ${url}`);
    console.log('Press Ctrl+C to stop');
  });
}
function parseArgs() {
  const args = process.argv.slice(2);
  const result = { command: null, options: {} };
  if (args.length === 0) {
    result.command = 'wizard';
    return result;
  }
  result.command = args[0];
  let i = 1;
  while (i < args.length) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2).replace(/-/g, '_');
      if (i + 1 < args.length && !args[i + 1].startsWith('-')) {
        result.options[key] = args[i + 1];
        i += 2;
      } else {
        result.options[key] = true;
        i++;
      }
    } else if (arg.startsWith('-')) {
      const key = arg.slice(1);
      if (i + 1 < args.length && !args[i + 1].startsWith('-')) {
        result.options[key] = args[i + 1];
        i += 2;
      } else {
        result.options[key] = true;
        i++;
      }
    } else {
      i++;
    }
  }
  return result;
}
function showHelp() {
  console.log(`
LightningEX Crypto Swap CLI
Usage: crypto-swap [command] [options]
Commands:
  wizard                    Start interactive exchange wizard (default)
  currencies                List supported currencies
  pair-list                 List supported currency-network pairs
  pair                      Get pair information
  rate                      Get exchange rate
  validate                  Validate address
  status                    Get order status
  monitor                   Monitor order until complete
  ui                        Launch web UI
Options:
  --send, -s               Currency to send
  --receive, -r            Currency to receive
  --amount, -a             Amount to send
  --receive-address, -addr Receive address
  --send-network           Send network
  --receive-network        Receive network
  --currency, -c           Currency for validation
  --id, -i                 Order ID
  --port, -p               Port for UI (default: 8080)
  --yes, -y                Skip confirmation
  --sendNetwork            Send network (for pair-list)
Examples:
  crypto-swap
  crypto-swap wizard
  crypto-swap currencies
  crypto-swap pair-list --send USDT --receive USDT
  crypto-swap pair-list --send USDT --receive USDT --send-network TRX
  crypto-swap pair --send USDT --receive USDT --send-network TRX --receive-network BSC
  crypto-swap rate --send USDT --receive USDT --send-network TRX --receive-network BSC --amount 100
  crypto-swap validate --currency USDT --network BSC --address 0x...
  crypto-swap status --id I1Y0...
  crypto-swap monitor --id I1Y0...
  crypto-swap ui --port 8080
`);
}
async function main() {
  const args = parseArgs();
  if (args.options.h || args.options.help) {
    showHelp();
    return;
  }
  try {
    switch (args.command) {
      case 'wizard':
        await cmdWizard();
        break;
      case 'currencies':
        await cmdCurrencies();
        break;
      case 'pair-list':
        if (!args.options.send || !args.options.receive) {
          console.log('Usage: crypto-swap pair-list --send <currency> --receive <currency>');
          console.log('       [--send-network <network>]');
          return;
        }
        await cmdPairList(args.options);
        break;
      case 'pair':
        if (!args.options.send || !args.options.receive) {
          console.log('Usage: crypto-swap pair --send <currency> --receive <currency>');
          console.log('       [--send-network <network>] [--receive-network <network>]');
          return;
        }
        await cmdPair(args.options);
        break;
      case 'rate':
        if (!args.options.send || !args.options.receive || !args.options.amount) {
          console.log('Usage: crypto-swap rate --send <currency> --receive <currency> --amount <amount>');
          console.log('       [--send-network <network>] [--receive-network <network>]');
          return;
        }
        await cmdRate(args.options);
        break;
      case 'validate':
        if (!args.options.currency || !args.options.address) {
          console.log('Usage: crypto-swap validate --currency <currency> --address <address>');
          console.log('       [--network <network>]');
          return;
        }
        await cmdValidate(args.options);
        break;
      case 'order':
        console.log('❌ The "order" command is disabled. Please use the interactive wizard to place orders:');
        console.log('   crypto-swap wizard');
        return;
      case 'status':
        if (!args.options.id) {
          console.log('Usage: crypto-swap status --id <order-id>');
          return;
        }
        await cmdStatus(args.options);
        break;
      case 'monitor':
        if (!args.options.id) {
          console.log('Usage: crypto-swap monitor --id <order-id>');
          return;
        }
        await cmdMonitor(args.options);
        break;
      case 'ui':
        await cmdUI(args.options);
        break;
      default:
        console.log(`Unknown command: ${args.command}`);
        showHelp();
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}
main();