"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getBrowserSamplerSource = getBrowserSamplerSource;
const pageAnalyzer_1 = require("./analyzer/pageAnalyzer");
function getBrowserSamplerSource() {
    return pageAnalyzer_1.collectRawPageAnalysis.toString();
}