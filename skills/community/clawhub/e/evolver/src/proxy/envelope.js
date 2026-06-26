'use strict';

const crypto = require('crypto');

const PROTOCOL_NAME = 'gep-a2a';
const PROTOCOL_VERSION = '1.0.0';

/**
 * Build a GEP-A2A protocol envelope around a payload.
 *
 * Strict hub endpoints (/a2a/hello, /a2a/fetch, /a2a/validate, ...) run
 * isValidProtocolMessage server-side and reject bare bodies with
 * 400 invalid_protocol_message. Lenient endpoints such as
 * /a2a/assets/search accept raw bodies and must NOT be wrapped.
 *
 * @param {string} messageType - GEP-A2A message_type ('hello'|'fetch'|'validate'|...)
 * @param {object} [payload] - Message payload (defaults to {})
 * @param {string|null} [senderId] - node_id of the sending node
 * @returns {object} Full protocol envelope
 */
function buildEnvelope(messageType, payload, senderId) {
  if (!messageType || typeof messageType !== 'string') {
    throw new Error('buildEnvelope: messageType is required');
  }
  return {
    protocol: PROTOCOL_NAME,
    protocol_version: PROTOCOL_VERSION,
    message_type: messageType,
    message_id: 'msg_' + Date.now() + '_' + crypto.randomBytes(4).toString('hex'),
    sender_id: senderId || null,
    timestamp: new Date().toISOString(),
    payload: payload || {},
  };
}

/**
 * Wrap `body` in a GEP-A2A envelope unless it already is one.
 *
 * When the caller hands us a pre-built envelope, sender_id is still forced
 * to the proxy's own node_id: callers must not be able to impersonate
 * another node through the proxy (same rule as the ATP passthrough routes).
 *
 * @param {string} messageType - message_type used when wrapping is needed
 * @param {object} [body] - Bare payload or full envelope
 * @param {string|null} [senderId] - The proxy's own node_id
 * @returns {object} Full protocol envelope
 */
function ensureEnvelope(messageType, body, senderId) {
  const b = body || {};
  const isEnvelope = b.protocol === PROTOCOL_NAME
    && typeof b.message_type === 'string'
    && b.payload && typeof b.payload === 'object';
  if (isEnvelope) {
    return { ...b, sender_id: senderId || b.sender_id || null };
  }
  return buildEnvelope(messageType, b, senderId);
}

module.exports = { buildEnvelope, ensureEnvelope, PROTOCOL_NAME, PROTOCOL_VERSION };
