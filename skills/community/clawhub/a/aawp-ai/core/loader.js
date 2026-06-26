'use strict';
const path = require('path');
const crypto = require('crypto');
const a = require('./aawp-core.node');
const S = process.env.AAWP_SKILL  || path.resolve(__dirname, '..');
const C = process.env.AAWP_CONFIG || path.join(S, '.agent-config');

const _initialToken = crypto.randomBytes(32).toString('hex');
process.env.AAWP_AI_TOKEN = _initialToken;

module.exports = {
  init:       () => a._l0(C, S, '/tmp/aawp.log'),
  lh:         () => a._c0(S),
  signer:     (lh) => a._g0(C, lh || a._c0(S)),
  relay:      () => a._r0(C),
  sign:       (payload) => a._s0(payload),
  getToken:   () => a._a0(),
};
