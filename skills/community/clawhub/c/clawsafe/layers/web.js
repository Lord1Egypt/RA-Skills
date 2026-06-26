/**
 * Web Layer Detector / Web层安全检测器
 * Detects: SQL Injection, XSS, CSRF, SSRF
 * 检测: SQL注入、跨站脚本、跨站请求伪造、服务器端请求伪造
 */

const fs = require('fs');
const path = require('path');

class WebDetector {
  constructor(skillPath) {
    this.skillPath = skillPath;
    this.rules = {};
    this._loadRules();
  }

  _loadRules() {
    const rulesDir = path.join(this.skillPath, 'rules', 'web');
    if (!fs.existsSync(rulesDir)) return;

    const ruleFiles = ['sql_injection.json', 'xss.json', 'csrf.json', 'ssrf.json'];
    
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
   * Web 层检测入口
   * @param {string} input - 用户输入/请求内容
   * @returns {object} { safe, threats, confidence }
   */
  detect(input) {
    if (!input || typeof input !== 'string') {
      return { safe: true, threats: [], confidence: 0 };
    }

    const threats = [];
    let maxConfidence = 0;

    // 检测各类型攻击
    const results = [
      this._detectSQLInjection(input),
      this._detectXSS(input),
      this._detectCSRF(input),
      this._detectSSRF(input)
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

  _detectSQLInjection(input) {
    return this._matchRules(input, this.rules.sql_injection, 'sql_injection');
  }

  _detectXSS(input) {
    return this._matchRules(input, this.rules.xss, 'xss');
  }

  _detectCSRF(input) {
    return this._matchRules(input, this.rules.csrf, 'csrf');
  }

  _detectSSRF(input) {
    return this._matchRules(input, this.rules.ssrf, 'ssrf');
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

module.exports = WebDetector;
