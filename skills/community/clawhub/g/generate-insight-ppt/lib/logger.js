/**
 * lib/logger.js - 日志工具
 */
const fs = require('fs');
const path = require('path');
const config = require('./config');

/**
 * 简易日志类
 */
class Logger {
  constructor(sessionId) {
    this.sessionId = sessionId;
    this.logFile = path.join(config.getSessionDir(sessionId), 'run.log');
    this.steps = [];
  }

  /**
   * 记录日志到文件
   * @param {string} level 
   * @param {string} message 
   */
  log(level, message) {
    const timestamp = new Date().toISOString();
    const line = `[${timestamp}] [${level}] ${message}`;
    console.log(line);
    
    // 追加到日志文件
    if (this.logFile) {
      fs.appendFileSync(this.logFile, line + '\n');
    }
  }

  info(message) { this.log('INFO', message); }
  warn(message) { this.log('WARN', message); }
  error(message) { this.log('ERROR', message); }

  /**
   * 记录步骤开始
   * @param {number} stepNum 
   * @param {string} stepName 
   * @param {string} description 
   */
  stepStart(stepNum, stepName, description) {
    this.info(`\n${'='.repeat(60)}`);
    this.info(`STEP ${stepNum}/5: ${stepName}`);
    this.info(`说明: ${description}`);
    this.info('='.repeat(60));
    
    this.steps.push({
      step: stepNum,
      name: stepName,
      description,
      status: 'running',
      startTime: Date.now()
    });
  }

  /**
   * 记录步骤完成
   * @param {number} stepNum 
   * @param {object} summary 
   */
  stepComplete(stepNum, summary = {}) {
    const step = this.steps.find(s => s.step === stepNum);
    if (step) {
      step.status = 'complete';
      step.endTime = Date.now();
      step.duration = step.endTime - step.startTime;
      step.summary = summary;
    }
    
    this.info(`\n✅ STEP ${stepNum} 完成`);
    if (Object.keys(summary).length > 0) {
      this.info(`   摘要: ${JSON.stringify(summary, null, 2).replace(/\n/g, '\n   ')}`);
    }
  }

  /**
   * 记录步骤失败
   * @param {number} stepNum 
   * @param {string} error 
   */
  stepFailed(stepNum, error) {
    const step = this.steps.find(s => s.step === stepNum);
    if (step) {
      step.status = 'failed';
      step.error = error;
      step.endTime = Date.now();
    }
    this.error(`❌ STEP ${stepNum} 失败: ${error}`);
  }

  /**
   * 获取完整报告
   */
  getReport() {
    const report = {
      sessionId: this.sessionId,
      totalSteps: this.steps.length,
      completedSteps: this.steps.filter(s => s.status === 'complete').length,
      steps: this.steps.map(s => ({
        step: s.step,
        name: s.name,
        description: s.description,
        status: s.status,
        duration: s.duration ? `${(s.duration / 1000).toFixed(1)}s` : null,
        summary: s.summary,
        error: s.error
      }))
    };

    // 计算总耗时
    const completedSteps = this.steps.filter(s => s.status === 'complete');
    if (completedSteps.length > 0) {
      report.totalDuration = completedSteps.reduce((acc, s) => acc + (s.duration || 0), 0);
    }

    return report;
  }

  /**
   * 打印报告到控制台
   */
  printReport() {
    const report = this.getReport();
    console.log('\n' + '='.repeat(60));
    console.log('📊 执行报告');
    console.log('='.repeat(60));
    
    for (const step of report.steps) {
      const icon = step.status === 'complete' ? '✅' : step.status === 'failed' ? '❌' : '⏳';
      const duration = step.duration ? ` (${step.duration})` : '';
      console.log(`${icon} Step ${step.step}: ${step.name}${duration}`);
      console.log(`   状态: ${step.status}`);
      if (step.summary) console.log(`   摘要:`, step.summary);
      if (step.error) console.log(`   错误: ${step.error}`);
    }

    if (report.totalDuration) {
      console.log(`\n⏱️  总耗时: ${(report.totalDuration / 1000).toFixed(1)}s`);
    }
    console.log('='.repeat(60));
  }
}

module.exports = Logger;
