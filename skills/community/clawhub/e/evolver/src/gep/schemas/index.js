'use strict';

const gene = require('./gene');
const capsule = require('./capsule');
const task = require('./task');
const protocol = require('./protocol');

module.exports = { ...gene, ...capsule, ...task, ...protocol };
