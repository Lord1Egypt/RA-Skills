#!/usr/bin/env node
/**
 * 自动分片器 v7.18
 * 
 * 核心功能:
 * 1. 自动分片大消息
 * 2. 并行/串行处理分片
 * 3. 合并分片结果
 */

const TokenCounter = require('./token-counter');

class AutoChunker {
  constructor(config = {}) {
    this.maxTokenPerChunk = config.maxTokenPerChunk || 80000;
    this.counter = new TokenCounter();
    this.results = [];
  }

  /**
   * 自动分片
   */
  chunkMessages(messages) {
    const chunks = [];
    let currentChunk = [];
    let currentToken = 0;
    
    for (const msg of messages) {
      const msgToken = this.counter.calculateMessageToken([msg]);
      
      if (currentToken + msgToken > this.maxTokenPerChunk) {
        // 当前 chunk 已满，创建新 chunk
        if (currentChunk.length > 0) {
          chunks.push(currentChunk);
        }
        currentChunk = [msg];
        currentToken = msgToken;
      } else {
        currentChunk.push(msg);
        currentToken += msgToken;
      }
    }
    
    // 添加最后一个 chunk
    if (currentChunk.length > 0) {
      chunks.push(currentChunk);
    }
    
    console.log(`📊 分片完成：${chunks.length} 个分片`);
    chunks.forEach((chunk, i) => {
      const token = this.counter.calculateMessageToken(chunk);
      console.log(`  分片 ${i + 1}: ${token} tokens`);
    });
    
    return chunks;
  }

  /**
   * 处理分片（支持并行/串行）
   */
  async processChunks(chunks, processor, options = {}) {
    const parallel = options.parallel || false;
    const results = [];
    
    console.log(`🚀 开始处理 ${chunks.length} 个分片...`);
    
    if (parallel) {
      // 并行处理
      const promises = chunks.map((chunk, i) => {
        console.log(`📦 并行处理分片 ${i + 1}/${chunks.length}`);
        return processor(chunk, i);
      });
      
      const resultsArray = await Promise.all(promises);
      results.push(...resultsArray);
    } else {
      // 串行处理
      for (let i = 0; i < chunks.length; i++) {
        console.log(`📦 串行处理分片 ${i + 1}/${chunks.length}`);
        const result = await processor(chunks[i], i);
        results.push(result);
      }
    }
    
    console.log(`✅ 分片处理完成`);
    return this.mergeResults(results);
  }

  /**
   * 合并分片结果
   */
  mergeResults(results) {
    if (results.length === 0) {
      return '';
    }
    
    if (results.length === 1) {
      return results[0];
    }
    
    // 合并多个结果
    return results.join('\n\n---\n\n');
  }

  /**
   * 智能分片处理（自动检测是否需要分片）
   */
  async smartProcess(messages, processor, options = {}) {
    const status = this.counter.isExceedLimit(messages, this.maxTokenPerChunk);
    
    if (!status.exceed) {
      // 不需要分片，直接处理
      console.log(`✅ Token 使用 ${status.usage}%，无需分片`);
      return await processor(messages, 0);
    }
    
    // 需要分片
    console.log(`⚠️ Token 使用 ${status.usage}%，启用自动分片`);
    const chunks = this.chunkMessages(messages);
    return await this.processChunks(chunks, processor, options);
  }
}

module.exports = AutoChunker;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [command] = args;
  
  if (!command) {
    console.log('用法：node auto-chunker.js <命令>');
    console.log('命令：test, demo');
    process.exit(1);
  }
  
  const chunker = new AutoChunker({ maxTokenPerChunk: 80000 });
  
  if (command === 'test') {
    // 测试分片
    const messages = [];
    for (let i = 0; i < 100; i++) {
      messages.push({
        role: 'user',
        content: `这是第 ${i + 1} 条消息，内容长度约 1000 字符。`.repeat(25)
      });
    }
    
    const chunks = chunker.chunkMessages(messages);
    console.log(`\n总消息数：${messages.length}`);
    console.log(`分片数：${chunks.length}`);
  }
  
  if (command === 'demo') {
    // 演示智能处理
    const messages = [{
      role: 'user',
      content: '这是一条测试消息'.repeat(10000)
    }];
    
    chunker.smartProcess(messages, async (chunk, index) => {
      console.log(`处理分片 ${index}: ${chunk.length} 条消息`);
      return `分片 ${index} 处理完成`;
    }).then(result => {
      console.log(`\n最终结果：${result}`);
    });
  }
}
