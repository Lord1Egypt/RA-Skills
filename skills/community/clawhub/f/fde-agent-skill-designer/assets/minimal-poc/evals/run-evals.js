#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const logic = require('../logic.js');

const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'cases.json'), 'utf8')).cases;
const results = cases.map((item) => {
  const output = logic.run(item.input);
  const passed = output.status === item.expected_status && output.external_action === false && output.human_review_required === true;
  return { id: item.id, expected: item.expected_status, actual: output.status, passed };
});

for (const item of results) console.log(`${item.passed ? 'PASS' : 'FAIL'}｜${item.id}｜${item.actual}`);
const failed = results.filter((item) => !item.passed);
console.log(`Evaluation results:${results.length - failed.length}/${results.length}passed.`);
if (failed.length > 0) process.exit(1);
