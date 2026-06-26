#!/usr/bin/env node
/**
 * Token 计数器 v7.18
 * 
 * 核心功能:
 * 1. 估算文本 token 数
 * 2. 计算消息总 token（含图片）
 * 3. 检查是否超限并预警
 */

class TokenCounter {
  constructor(config = {}) {
    // 1 token ≈ 4 字符（中文）或 0.75 单词（英文）
    this.chineseFactor = config.chineseFactor || 4;
    this.englishFactor = config.englishFactor || 0.75;
    this.imageToken = config.imageToken || 1000;  // 每张图片约 1000 token
  }

  /**
   * 估算文本 token 数
   */
  estimateToken(text) {
    if (!text) return 0;
    
    // 检测中英文比例
    const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const englishWords = text.split(/\s+/).filter(w => w.length > 0).length;
    
    // 混合估算
    const chineseToken = chineseChars / this.chineseFactor;
    const englishToken = englishWords * this.englishFactor;
    const otherToken = (text.length - chineseChars) / this.chineseFactor;
    
    return Math.ceil(chineseToken + englishToken + otherToken);
  }

  /**
   * 计算消息总 token（含图片）
   */
  calculateMessageToken(messages) {
    let total = 0;
    
    if (!Array.isArray(messages)) {
      messages = [messages];
    }
    
    for (const msg of messages) {
      // 文本 token
      if (msg.content) {
        total += this.estimateToken(msg.content);
      }
      
      // 图片 token
      if (msg.images && Array.isArray(msg.images)) {
        total += msg.images.length * this.imageToken;
      }
      
      // 角色 token（system/user/assistant）
      total += 10;
    }
    
    return total;
  }

  /**
   * 检查是否超限
   */
  isExceedLimit(messages, limit = 100000) {
    const token = this.calculateMessageToken(messages);
    const usage = (token / limit) * 100;
    
    return {
      exceed: token > limit,
      current: token,
      limit: limit,
      usage: Math.round(usage * 100) / 100,
      warning: usage > 80  // 超过 80% 预警
    };
  }

  /**
   * 获取优化建议
   */
  getOptimizationSuggestion(messages, limit = 100000) {
    const status = this.isExceedLimit(messages, limit);
    const suggestions = [];
    
    if (status.exceed) {
      suggestions.push({
        type: 'chunk',
        priority: 'high',
        message: `Token 超限 ${Math.round(status.usage - 100)}%，建议启用自动分片`
      });
    }
    
    if (status.warning) {
      suggestions.push({
        type: 'summarize',
        priority: 'medium',
        message: `Token 使用 ${status.usage}%，建议摘要历史对话`
      });
    }
    
    if (status.usage < 50) {
      suggestions.push({
        type: 'model',
        priority: 'low',
        message: `Token 使用 ${status.usage}%，可切换更小模型节省成本`
      });
    }
    
    return {
      status,
      suggestions
    };
  }
}

module.exports = TokenCounter;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [text, limit] = args;
  
  if (!text) {
    console.log('用法：node token-counter.js <文本> [限制]');
    process.exit(1);
  }
  
  const counter = new TokenCounter();
  const token = counter.estimateToken(text);
  const limitNum = parseInt(limit) || 100000;
  const status = counter.isExceedLimit([{ content: text }], limitNum);
  
  console.log(`文本长度：${text.length} 字符`);
  console.log(`估算 Token: ${token}`);
  console.log(`限制：${limitNum}`);
  console.log(`使用率：${status.usage}%`);
  console.log(`状态：${status.exceed ? '❌ 超限' : status.warning ? '⚠️ 预警' : '✅ 正常'}`);
}
