/**
 * Deploy Layer Detector / 部署层安全检测器
 * Detects: Environment Variable Leaks, Debug Information Disclosure
 * 检测: 环境变量泄露、调试信息泄露
 */

const fs = require('fs');
const path = require('path');

class DeployDetector {
  constructor(skillPath) {
    this.skillPath = skillPath;
    this.rules = {};
    this._loadRules();
  }

  _loadRules() {
    const rulesDir = path.join(this.skillPath, 'rules', 'deploy');
    if (!fs.existsSync(rulesDir)) return;

    const ruleFiles = ['env_leak.json', 'debug_info.json'];
    
    ruleFiles.forEach(file => {
      const filePath = path.join(rulesDir, file);
      if (fs.existsSync(filePath)) {
        const ruleData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        const category = ruleData.category || file.replace('.json', '');
        this.rules[category] = ruleData;
      }
    });
  }

  detect(input) {
    if (!input || typeof input !== 'string') {
      return { safe: true, threats: [], confidence: 0 };
    }

    const threats = [];
    let maxConfidence = 0;

    for (const [category, ruleData] of Object.entries(this.rules)) {
      if (!ruleData.patterns) continue;

      for (const pattern of ruleData.patterns) {
        try {
          const regex = new RegExp(pattern.pattern, 'gi');
          if (regex.test(input)) {
            threats.push({
              type: category,
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
    }

    return {
      safe: threats.length === 0,
      threats,
      confidence: maxConfidence
    };
  }
}

module.exports = DeployDetector;
