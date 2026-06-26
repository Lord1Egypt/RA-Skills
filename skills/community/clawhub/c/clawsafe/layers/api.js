/**
 * API Layer Detector / API层安全检测器
 * Detects: API Key Exposure, Rate Limiting, Authentication Issues
 * 检测: API密钥泄露、频率限制、认证问题
 */

const fs = require('fs');
const path = require('path');

class APIDetector {
  constructor(skillPath) {
    this.skillPath = skillPath;
    this.rules = {};
    this._loadRules();
  }

  _loadRules() {
    const rulesDir = path.join(this.skillPath, 'rules', 'api');
    if (!fs.existsSync(rulesDir)) return;

    const ruleFiles = ['key_exposure.json', 'rate_limit.json', 'auth.json'];
    
    ruleFiles.forEach(file => {
      const filePath = path.join(rulesDir, file);
      if (fs.existsSync(filePath)) {
        const ruleData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        const category = ruleData.category || file.replace('.json', '');
        this.rules[category] = ruleData;
      }
    });
  }

  /**
   * API 层检测入口
   * @param {string} input - 代码/配置内容
   * @returns {object} { safe, threats, confidence }
   */
  detect(input) {
    if (!input || typeof input !== 'string') {
      return { safe: true, threats: [], confidence: 0 };
    }

    const threats = [];
    let maxConfidence = 0;

    // 检测各类型问题
    const results = [
      this._detectKeyExposure(input),
      this._detectRateLimit(input),
      this._detectAuthIssues(input)
    ];

    results.forEach(result => {
      if (result.threats.length > 0) {
        threats.push(...result.threats);
        maxConfidence = Math.max(maxConfidence, result.confidence);
      }
    });

    return {
      safe: threats.length === 0,
      threats,
      confidence: maxConfidence
    };
  }

  _detectKeyExposure(input) {
    return this._matchRules(input, this.rules.key_exposure, 'key_exposure');
  }

  _detectRateLimit(input) {
    return this._matchRules(input, this.rules.rate_limit, 'rate_limit');
  }

  _detectAuthIssues(input) {
    return this._matchRules(input, this.rules.auth, 'auth');
  }

  _matchRules(input, ruleSet, type) {
    if (!ruleSet || !ruleSet.patterns) {
      return { threats: [], confidence: 0 };
    }

    const threats = [];
    
    for (const pattern of ruleSet.patterns) {
      try {
        const regex = new RegExp(pattern.pattern, 'gi');
        if (regex.test(input)) {
          threats.push({
            type,
            id: pattern.id,
            name: ruleSet.name,
            severity: pattern.severity,
            description: pattern.description,
            confidence: pattern.weight,
            pattern: pattern.pattern
          });
        }
      } catch (e) {
        // 正则错误，跳过
      }
    }

    const confidence = threats.length > 0 
      ? Math.max(...threats.map(t => t.confidence))
      : 0;

    return { threats, confidence };
  }

  reload() {
    this.rules = {};
    this._loadRules();
  }
}

module.exports = APIDetector;
