'use strict';

const fs = require('fs');
const path = require('path');

const { getIndexHtml } = require('./indexHtml');
const { getClientJs } = require('./clientJs');
const { getStylesCss } = require('./stylesCss');

let _vendorEchartsCache = null;
function getVendorEcharts() {
  if (!_vendorEchartsCache) {
    _vendorEchartsCache = fs.readFileSync(path.join(__dirname, 'vendor', 'echarts.min.js'));
  }
  return _vendorEchartsCache;
}

module.exports = {
  getIndexHtml,
  getClientJs,
  getStylesCss,
  getVendorEcharts,
};
