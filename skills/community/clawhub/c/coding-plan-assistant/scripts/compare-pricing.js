#!/usr/bin/env node
/**
 * compare-pricing.js
 * 
 * 对比各编程助手平台的定价方案
 */

const path = require('path');
const { comparePricing } = require('../index.js');

function showPricingComparison() {
  const output = comparePricing();
  console.log(output);
}

// 运行对比
showPricingComparison();
