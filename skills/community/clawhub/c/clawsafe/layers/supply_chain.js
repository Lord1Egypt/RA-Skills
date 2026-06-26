/**
 * Supply Chain Detector / 供应链安全检测器
 * Detects: Malicious Dependencies, Dangerous Imports, Code Execution
 * 检测: 恶意依赖、危险导入、代码执行
 */

const fs = require('fs');
const path = require('path');

class SupplyChainDetector {
  constructor(skillPath) {
    this.skillPath = skillPath;
    this.rules = {};
    this._loadRules();
  }

  _loadRules() {
    const rulesFile = path.join(this.skillPath, 'rules', 'supply_chain', 'deps.json');
    if (fs.existsSync(rulesFile)) {
      const ruleData = JSON.parse(fs.readFileSync(rulesFile, 'utf-8'));
      this.rules = ruleData;
    }
  }

  detect(input) {
    if (!input || typeof input !== 'string') {
      return { safe: true, threats: [], confidence: 0 };
    }

    const threats = [];
    let maxConfidence = 0;

    if (!this.rules.patterns) {
      return { safe: true, threats: [], confidence: 0 };
    }

    for (const pattern of this.rules.patterns) {
      try {
        const regex = new RegExp(pattern.pattern, 'gi');
        if (regex.test(input)) {
          threats.push({
            type: pattern.category || 'supply_chain',
            pattern: pattern.id,
            severity: pattern.severity,
            confidence: pattern.weight,
            description: pattern.description
          });
          maxConfidence = Math.max(maxConfidence, pattern.weight);
        }
      } catch (e) {
        // Skip invalid regex
      }
    }

    return {
      safe: threats.length === 0,
      threats,
      confidence: maxConfidence
    };
  }
}

module.exports = SupplyChainDetector;
