#!/usr/bin/env node
'use strict';
const addon = require(process.env.AAWP_CORE || require('path').join(__dirname, '..', 'core', 'aawp-core.node'));
const S = process.env.AAWP_SKILL  || require('path').resolve(__dirname, '..');
const C = process.env.AAWP_CONFIG || require('path').join(S, '.agent-config');
addon._l0(C, S, process.env.AAWP_LOG || '/tmp/aawp-daemon.log');
addon._a0(); // start accepting connections (v2.1.0+)
const sockPath = addon._x0(); // get socket path
require('fs').writeFileSync('/tmp/.aawp-daemon.lock', JSON.stringify({sock: sockPath}));
console.log('[AAWP] listening on', sockPath);
setInterval(() => {}, 1 << 30);
