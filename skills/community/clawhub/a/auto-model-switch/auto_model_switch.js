#!/usr/bin/env node
/**
 * 自动切换模型 - OpenClaw集成版
 * 
 * 功能：
 * - 自动检测token消耗
 * - 自动检测API限流
 * - 智能切换备用模型
 * - 与OpenClaw网关集成
 * - 支持心跳触发
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const http = require('http');
const https = require('https');

class AutoModelSwitch {
  constructor(configPath = null) {
    // 配置路径
    this.configPath = configPath || path.join(__dirname, 'config.yaml');
    this.statePath = path.join(__dirname, 'state', 'model-switch.json');
    this.historyPath = path.join(__dirname, 'state', 'switch-history.json');
    
    // 加载配置和状态
    this.config = this.loadConfig();
    this.state = this.loadState();
    this.history = this.loadHistory();
    
    // OpenClaw网关配置
    this.gatewayUrl = process.env.OPENCLAW_GATEWAY_URL || 'http://localhost:3000';
    this.gatewayToken = process.env.OPENCLAW_GATEWAY_TOKEN || '';
  }

  // ========== 配置和状态管理 ==========

  loadConfig() {
    try {
      if (fs.existsSync(this.configPath)) {
        const content = fs.readFileSync(this.configPath, 'utf8');
        return yaml.load(content);
      }
    } catch (e) {
      console.error('配置加载失败:', e.message);
    }
    
    // 默认配置
    return {
      models: [
        { id: 'primary', model: 'custom-maas-coding-api-cn-huabei-1-xf-yun-com/astron-code-latest', name: 'Astron Code', daily_limit: 10000000, priority: 1 },
        { id: 'backup-1', model: 'zai/glm-5', name: 'GLM-4.5', daily_limit: null, priority: 2 }
      ],
      notification: { enabled: true },
      auto_switch: { on_limit_exceeded: true, on_rate_limit: true, warning_threshold: 0.8, critical_threshold: 0.95 }
    };
  }

  loadState() {
    try {
      if (fs.existsSync(this.statePath)) {
        let content = fs.readFileSync(this.statePath, 'utf8');
        // 移除BOM
        if (content.charCodeAt(0) === 0xFEFF) {
          content = content.slice(1);
        }
        return JSON.parse(content);
      }
    } catch (e) {
      console.error('状态加载失败:', e.message);
    }
    
    return {
      current_model: null,
      token_usage: {},
      rate_limits: {},
      last_check: null
    };
  }

  saveState() {
    const dir = path.dirname(this.statePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    this.state.last_check = new Date().toISOString();
    fs.writeFileSync(this.statePath, JSON.stringify(this.state, null, 2));
  }

  loadHistory() {
    try {
      if (fs.existsSync(this.historyPath)) {
        let content = fs.readFileSync(this.historyPath, 'utf8');
        // 移除BOM
        if (content.charCodeAt(0) === 0xFEFF) {
          content = content.slice(1);
        }
        return JSON.parse(content);
      }
    } catch (e) {}
    
    return { switches: [] };
  }

  saveHistory(entry) {
    const dir = path.dirname(this.historyPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    this.history.switches.push({
      timestamp: new Date().toISOString(),
      ...entry
    });
    
    // 只保留最近100条
    if (this.history.switches.length > 100) {
      this.history.switches = this.history.switches.slice(-100);
    }
    
    fs.writeFileSync(this.historyPath, JSON.stringify(this.history, null, 2));
  }

  // ========== 模型管理 ==========

  getCurrentModel() {
    return this.state.current_model || this.config.models[0]?.model;
  }

  getModelConfig(modelId) {
    return this.config.models.find(m => m.model === modelId || m.id === modelId);
  }

  getTokenUsage(model) {
    const today = new Date().toISOString().split('T')[0];
    const usage = this.state.token_usage[today];
    if (!usage) return 0;
    return usage[model] || 0;
  }

  getUsagePercentage(model) {
    const config = this.getModelConfig(model);
    if (!config || !config.daily_limit) return 0;
    return this.getTokenUsage(model) / config.daily_limit;
  }

  // ========== OpenClaw集成 ==========

  async getGatewayStatus() {
    return new Promise((resolve, reject) => {
      const url = new URL('/api/status', this.gatewayUrl);
      const client = url.protocol === 'https:' ? https : http;
      
      const req = client.get(url, {
        headers: {
          'Authorization': `Bearer ${this.gatewayToken}`,
          'Content-Type': 'application/json'
        }
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(e);
          }
        });
      });
      
      req.on('error', reject);
      req.setTimeout(5000, () => {
        req.destroy();
        reject(new Error('Timeout'));
      });
    });
  }

  async switchModelViaGateway(targetModel) {
    return new Promise((resolve, reject) => {
      const url = new URL('/api/config/model', this.gatewayUrl);
      const client = url.protocol === 'https:' ? https : http;
      
      const data = JSON.stringify({ model: targetModel });
      
      const options = {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.gatewayToken}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(data)
        }
      };
      
      const req = client.request(url, options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ success: true });
          } else {
            reject(new Error(`HTTP ${res.statusCode}: ${body}`));
          }
        });
      });
      
      req.on('error', reject);
      req.write(data);
      req.end();
    });
  }

  // ========== 切换逻辑 ==========

  shouldSwitch() {
    const current = this.getCurrentModel();
    const percentage = this.getUsagePercentage(current);
    const threshold = this.config.auto_switch?.critical_threshold || 0.95;
    
    return percentage >= threshold;
  }

  shouldWarn() {
    const current = this.getCurrentModel();
    const percentage = this.getUsagePercentage(current);
    const threshold = this.config.auto_switch?.warning_threshold || 0.8;
    
    return percentage >= threshold && percentage < (this.config.auto_switch?.critical_threshold || 0.95);
  }

  getNextModel() {
    const current = this.getCurrentModel();
    const models = [...this.config.models].sort((a, b) => a.priority - b.priority);
    
    for (const model of models) {
      if (model.model === current) continue;
      
      // 检查是否被限流
      if (this.isRateLimited(model.model)) continue;
      
      return model;
    }
    
    return null;
  }

  isRateLimited(model) {
    if (!this.state.rate_limits) return false;
    const limit = this.state.rate_limits[model];
    if (!limit) return false;
    
    // 限流60秒后自动解除
    const retryDelay = this.config.auto_switch?.retry_delay || 60;
    const elapsed = (Date.now() - new Date(limit.timestamp).getTime()) / 1000;
    
    return elapsed < retryDelay;
  }

  recordRateLimit(model) {
    this.state.rate_limits[model] = {
      timestamp: new Date().toISOString()
    };
    this.saveState();
  }

  async switch(reason = 'token_limit') {
    if (!this.shouldSwitch()) {
      return { switched: false, reason: 'no_need' };
    }
    
    const next = this.getNextModel();
    if (!next) {
      this.notify('❌ 所有模型不可用');
      return { switched: false, reason: 'no_available_model' };
    }
    
    const old = this.getCurrentModel();
    
    try {
      // 尝试通过网关切换
      if (this.gatewayToken) {
        await this.switchModelViaGateway(next.model);
      }
      
      // 更新状态
      this.state.current_model = next.model;
      this.saveState();
      
      // 记录历史
      this.saveHistory({
        from: old,
        to: next.model,
        reason: reason,
        token_usage: this.getTokenUsage(old)
      });
      
      this.notify(`✅ 模型切换: ${old} → ${next.name}`);
      
      return { switched: true, from: old, to: next.model };
    } catch (e) {
      console.error('切换失败:', e.message);
      return { switched: false, reason: 'switch_failed', error: e.message };
    }
  }

  // ========== Token更新 ==========

  updateUsage(model, tokens) {
    const today = new Date().toISOString().split('T')[0];
    if (!this.state.token_usage[today]) {
      this.state.token_usage[today] = {};
    }
    this.state.token_usage[today][model] = 
      (this.state.token_usage[today][model] || 0) + tokens;
    this.saveState();
  }

  // 从OpenClaw状态更新token使用量
  async syncFromGateway() {
    try {
      const status = await this.getGatewayStatus();
      if (status.usage) {
        const model = status.model || this.getCurrentModel();
        this.updateUsage(model, status.usage.total_tokens || 0);
        return true;
      }
    } catch (e) {
      console.error('同步失败:', e.message);
    }
    return false;
  }

  // ========== 通知 ==========

  notify(message) {
    if (this.config.notification?.enabled) {
      console.log(`[AutoModelSwitch] ${message}`);
      
      // 可以扩展：发送到飞书、邮件等
      // this.sendToFeishu(message);
    }
  }

  // ========== 状态报告 ==========

  getStatusReport() {
    const current = this.getCurrentModel();
    const currentConfig = this.getModelConfig(current);
    const usage = currentConfig ? this.getTokenUsage(current) : 0;
    const percentage = currentConfig?.daily_limit ? usage / currentConfig.daily_limit : 0;
    
    let report = `📊 模型状态\n`;
    report += `当前：${currentConfig?.name || current}\n`;
    
    if (currentConfig?.daily_limit) {
      const used = (usage / 1000000).toFixed(1);
      const total = (currentConfig.daily_limit / 1000000).toFixed(0);
      const pct = (percentage * 100).toFixed(0);
      report += `Token：${used}M / ${total}M (${pct}%)\n`;
    } else {
      report += `Token：无限制\n`;
    }
    
    // 备用模型状态
    const backups = this.config.models.filter(m => m.model !== current);
    if (backups.length > 0) {
      report += `\n备用模型：\n`;
      for (const backup of backups) {
        const limited = this.isRateLimited(backup.model) ? ' (限流中)' : ' (可用)';
        report += `- ${backup.name}${limited}\n`;
      }
    }
    
    return report;
  }

  // ========== 心跳检查 ==========

  async heartbeat() {
    // 同步token使用量
    await this.syncFromGateway();
    
    // 检查是否需要警告
    if (this.shouldWarn()) {
      const current = this.getCurrentModel();
      const pct = (this.getUsagePercentage(current) * 100).toFixed(0);
      this.notify(`⚠️ Token使用已达 ${pct}%，建议切换模型`);
      return { action: 'warn', percentage: pct };
    }
    
    // 检查是否需要切换
    if (this.shouldSwitch()) {
      const result = await this.switch();
      return { action: 'switch', ...result };
    }
    
    return { action: 'ok' };
  }
}

// ========== CLI入口 ==========

if (require.main === module) {
  const args = process.argv.slice(2);
  const ams = new AutoModelSwitch();
  
  (async () => {
    try {
      switch (args[0]) {
        case 'status':
          console.log(ams.getStatusReport());
          break;
          
        case 'switch':
          const result = await ams.switch(args[1] || 'manual');
          console.log(JSON.stringify(result, null, 2));
          break;
          
        case 'heartbeat':
          const hbResult = await ams.heartbeat();
          console.log(JSON.stringify(hbResult, null, 2));
          break;
          
        case 'sync':
          const synced = await ams.syncFromGateway();
          console.log(synced ? '同步成功' : '同步失败');
          break;
          
        case 'update':
          // 手动更新token: node auto_model_switch.js update <model> <tokens>
          if (args[1] && args[2]) {
            ams.updateUsage(args[1], parseInt(args[2]));
            console.log('已更新');
          } else {
            console.log('用法: node auto_model_switch.js update <model> <tokens>');
          }
          break;
          
        default:
          console.log(`
用法: node auto_model_switch.js <command>

命令:
  status     显示当前模型状态
  switch     手动切换模型
  heartbeat  心跳检查（自动检测和切换）
  sync       从网关同步token使用量
  update     手动更新token使用量

示例:
  node auto_model_switch.js status
  node auto_model_switch.js switch
  node auto_model_switch.js heartbeat
`);
      }
    } catch (e) {
      console.error('错误:', e.message);
      process.exit(1);
    }
  })();
}

module.exports = AutoModelSwitch;
