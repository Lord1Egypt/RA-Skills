// ATP Merchant Agent Template
// Provides a ready-to-use merchant agent that registers services,
// listens for orders, processes them, and submits delivery proofs.
//
// Usage:
//   const merchant = require('./merchantAgent');
//   merchant.start({ services: [{ title: 'Code Review', ... }] });

const { getNodeId, sendHelloToHub, startHeartbeat, stopHeartbeat, consumeAvailableWork } = require('../gep/a2aProtocol');
const { publishService } = require('./serviceHelper');
const { submitDelivery, getMerchantTier, listProofs } = require('./hubClient');

let _running = false;
let _pollInterval = null;
const DEFAULT_POLL_MS = 30000;

/**
 * Start the merchant agent loop.
 * @param {object} opts
 * @param {Array<object>} opts.services - services to register
 * @param {function} opts.onOrder - async handler(order) => proofPayload
 * @param {number} [opts.pollMs] - order poll interval (default 30s)
 */
async function start(opts) {
  if (_running) {
    console.log('[ATP-Merchant] Already running, skipping duplicate start.');
    return;
  }
  _running = true;

  const hello = await sendHelloToHub();
  if (!hello || !hello.ok) {
    console.error('[ATP-Merchant] Failed to register with Hub:', hello?.error);
    _running = false;
    return;
  }

  console.log('[ATP-Merchant] Registered as', getNodeId());

  if (Array.isArray(opts.services)) {
    for (const svc of opts.services) {
      try {
        const result = await publishService(svc);
        if (result.ok) {
          console.log('[ATP-Merchant] Published service:', svc.title);
        } else {
          console.warn('[ATP-Merchant] Failed to publish service:', svc.title, result.error);
        }
      } catch (e) {
        console.warn('[ATP-Merchant] Service publish error:', e.message);
      }
    }
  }

  startHeartbeat();

  const pollMs = opts.pollMs || DEFAULT_POLL_MS;
  _pollInterval = setInterval(async () => {
    try {
      const work = consumeAvailableWork();
      if (!work || work.length === 0) return;

      for (const order of work) {
        if (typeof opts.onOrder === 'function') {
          try {
            const proofPayload = await opts.onOrder(order);
            if (proofPayload && order.atp_order_id) {
              const delivery = await submitDelivery(order.atp_order_id, proofPayload);
              if (delivery.ok) {
                console.log('[ATP-Merchant] Delivered order:', order.atp_order_id);
              } else {
                console.warn('[ATP-Merchant] Delivery failed:', delivery.error);
              }
            }
          } catch (e) {
            console.error('[ATP-Merchant] Order handler error:', e.message);
          }
        }
      }
    } catch (e) {
      console.error('[ATP-Merchant] Poll error:', e.message);
    }
  }, pollMs);

  console.log('[ATP-Merchant] Polling for orders every', pollMs, 'ms');
}

function stop() {
  _running = false;
  if (_pollInterval) {
    clearInterval(_pollInterval);
    _pollInterval = null;
  }
  stopHeartbeat();
  console.log('[ATP-Merchant] Stopped');
}

function isRunning() {
  return _running;
}

async function getStatus() {
  const tier = await getMerchantTier();
  const proofs = await listProofs({ role: 'merchant', limit: 5 });
  return {
    node_id: getNodeId(),
    running: _running,
    tier: tier.ok ? tier.data : null,
    recent_proofs: proofs.ok ? proofs.data : null,
  };
}

module.exports = {
  start,
  stop,
  isRunning,
  getStatus,
};
