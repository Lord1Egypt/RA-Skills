/**
 * LLM Layer Detector / LLM层检测器
 * Detects: Prompt Injection, Jailbreak, Prompt Leaking, Encoding Obfuscation
 * 检测: 提示注入、越狱、提示泄露、编码混淆
 */

const fs = require('fs');
const path = require('path');

class LLMDetector {
  constructor(skillPath) {
    this.skillPath = skillPath;
    this.rules = {};
    this.config = {};
    this.whitelist = {};
    this._init();
  }

  _init() {
    // 加载配置
    const configPath = path.join(this.skillPath, 'config.json');
    if (fs.existsSync(configPath)) {
      this.config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    }

    // 加载白名单
    const whitelistPath = path.join(this.skillPath, 'whitelist.json');
    if (fs.existsSync(whitelistPath)) {
      this.whitelist = JSON.parse(fs.readFileSync(whitelistPath, 'utf-8'));
    }

    // 加载规则文件
    const rulesDir = path.join(this.skillPath, 'rules');
    if (fs.existsSync(rulesDir)) {
      const ruleFiles = ['injection.json', 'jailbreak.json', 'prompt_leak.json', 'encoding.json'];
      ruleFiles.forEach(file => {
        const filePath = path.join(rulesDir, file);
        if (fs.existsSync(filePath)) {
          const ruleData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
          this.rules[ruleData.category] = ruleData;
        }
      });
    }
  }

  /**
   * 检查是否匹配白名单
   * @param {string} input - 用户输入
   * @returns {boolean}
   */
  _checkWhitelist(input) {
    if (!this.whitelist.patterns) return false;

    for (const pattern of this.whitelist.patterns) {
      const regex = new RegExp(pattern, 'i');
      if (regex.test(input)) {
        return true;
      }
    }

    if (this.whitelist.keywords) {
      for (const keyword of this.whitelist.keywords) {
        if (input.toLowerCase().includes(keyword.toLowerCase())) {
          return true;
        }
      }
    }

    return false;
  }

  /**
   * 检测单个规则类别
   * @param {string} input - 用户输入
   * @param {object} ruleSet - 规则集
   * @returns {Array} 匹配的威胁
   */
  _detectCategory(input, ruleSet) {
    const threats = [];
    if (!ruleSet || !ruleSet.patterns) return threats;

    for (const rule of ruleSet.patterns) {
      try {
        const regex = new RegExp(rule.pattern, 'i');
        if (regex.test(input)) {
          threats.push({
            id: rule.id,
            category: ruleSet.category,
            name: ruleSet.name,
            severity: rule.severity,
            weight: rule.weight,
            matched: input.match(regex)[0]
          });
        }
      } catch (e) {
        console.error(`Regex error for rule ${rule.id}:`, e.message);
      }
    }

    return threats;
  }

  /**
   * 执行检测
   * @param {string} input - 用户输入
   * @returns {object} 检测结果
   */
  detect(input) {
    // 白名单检查
    if (this._checkWhitelist(input)) {
      return {
        safe: true,
        threats: [],
        confidence: 1.0,
        whitelist: true
      };
    }

    const allThreats = [];
    const categories = ['injection', 'jailbreak', 'prompt_leak', 'encoding'];

    for (const category of categories) {
      if (this.rules[category]) {
        const threats = this._detectCategory(input, this.rules[category]);
        allThreats.push(...threats);
      }
    }

    // 计算置信度
    const confidence = this._calculateConfidence(allThreats);
    const safe = allThreats.length === 0 || confidence < (this.config.detection?.confidenceThreshold || 0.6);

    return {
      safe,
      threats: allThreats,
      confidence,
      scannedAt: new Date().toISOString()
    };
  }

  /**
   * 计算威胁置信度
   * @param {Array} threats - 威胁列表
   * @returns {number} 置信度 0-1
   */
  _calculateConfidence(threats) {
    if (threats.length === 0) return 0;

    // 按权重和严重性计算
    const severityWeights = {
      critical: 1.0,
      high: 0.8,
      medium: 0.5,
      low: 0.2
    };

    let totalWeight = 0;
    let maxSeverity = 0;

    for (const threat of threats) {
      const severityValue = severityWeights[threat.severity] || 0.5;
      totalWeight += (threat.weight || 0.5) * severityValue;
      maxSeverity = Math.max(maxSeverity, severityValue);
    }

    // 组合计算
    const avgWeight = totalWeight / threats.length;
    const combined = (avgWeight + maxSeverity) / 2;

    return Math.min(combined, 1.0);
  }

  /**
   * 重新加载规则
   */
  reload() {
    this._init();
  }
}

module.exports = LLMDetector;
