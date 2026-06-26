// ATP Consumer Agent Template
// Provides a ready-to-use consumer agent that searches for services,
// places orders, and manages delivery verification.
//
// Usage:
//   const consumer = require('./consumerAgent');
//   const result = await consumer.orderService({ capabilities: ['code_review'], budget: 50 });

const { getNodeId, sendHelloToHub } = require('../gep/a2aProtocol');
const { placeOrder, verifyDelivery, settleOrder, disputeOrder, getOrderStatus, getAtpPolicy } = require('./hubClient');

let _initialized = false;

async function ensureInitialized() {
  if (_initialized) return;
  const hello = await sendHelloToHub();
  if (!hello || !hello.ok) {
    throw new Error('Failed to register with Hub: ' + (hello?.error || 'unknown'));
  }
  _initialized = true;
}

/**
 * Place an ATP order for a service.
 * @param {object} opts
 * @param {string[]} opts.capabilities - what the order needs
 * @param {number} opts.budget - credits to spend
 * @param {string} [opts.routingMode] - fastest | cheapest | auction | swarm
 * @param {string} [opts.verifyMode] - auto | ai_judge | bilateral
 * @param {string} [opts.question] - description of what you need
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function orderService(opts) {
  await ensureInitialized();

  const result = await placeOrder({
    capabilities: opts.capabilities,
    budget: Math.max(1, Math.round(Number(opts.budget) || 10)),
    routingMode: opts.routingMode || 'fastest',
    verifyMode: opts.verifyMode || 'auto',
    question: opts.question,
    signals: opts.signals,
    minReputation: opts.minReputation,
  });

  if (result.ok) {
    console.log('[ATP-Consumer] Order placed:', result.data.order_id, '-> merchant:', result.data.merchant?.node_id);
  }

  return result;
}

/**
 * Confirm delivery of an order (bilateral mode).
 * @param {string} orderId
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function confirmDelivery(orderId) {
  await ensureInitialized();
  return verifyDelivery(orderId, 'confirm');
}

/**
 * Request AI judge verification.
 * @param {string} orderId
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function requestAiJudge(orderId) {
  await ensureInitialized();
  return verifyDelivery(orderId, 'ai_judge');
}

/**
 * Force settlement of an order.
 * @param {string} orderId
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function settle(orderId) {
  await ensureInitialized();
  return settleOrder(orderId);
}

/**
 * Raise a dispute for an order.
 * @param {string} orderId
 * @param {string} reason - min 10 chars
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function dispute(orderId, reason) {
  await ensureInitialized();
  return disputeOrder(orderId, reason);
}

/**
 * Check the status of an order.
 * @param {string} orderId
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function checkOrder(orderId) {
  return getOrderStatus(orderId);
}

/**
 * Get ATP policy information (tiers, rates, etc.)
 * @returns {Promise<{ok: boolean, data?: object, error?: string}>}
 */
async function getPolicy() {
  return getAtpPolicy();
}

/**
 * Full order lifecycle: place -> wait -> verify -> settle.
 * @param {object} opts - same as orderService
 * @param {number} [opts.pollIntervalMs] - how often to check status (default 10s)
 * @param {number} [opts.timeoutMs] - max wait time (default 300s)
 * @returns {Promise<{ok: boolean, order?: object, finalStatus?: object, error?: string}>}
 */
async function orderAndWait(opts) {
  const order = await orderService(opts);
  if (!order.ok) return order;

  const orderId = order.data.order_id;
  const pollMs = opts.pollIntervalMs || 10000;
  const timeoutMs = opts.timeoutMs || 300000;
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    await new Promise(resolve => setTimeout(resolve, pollMs));

    const status = await checkOrder(orderId);
    if (!status.ok) continue;

    const proofStatus = status.data.proof_status;
    if (proofStatus === 'settled') {
      return { ok: true, order: order.data, finalStatus: status.data };
    }
    if (proofStatus === 'verified' && order.data.verify_mode === 'auto') {
      return { ok: true, order: order.data, finalStatus: status.data };
    }
    if (proofStatus === 'disputed') {
      return { ok: false, order: order.data, finalStatus: status.data, error: 'order_disputed' };
    }
  }

  return { ok: false, order: order.data, error: 'order_timeout' };
}

module.exports = {
  orderService,
  confirmDelivery,
  requestAiJudge,
  settle,
  dispute,
  checkOrder,
  getPolicy,
  orderAndWait,
};
