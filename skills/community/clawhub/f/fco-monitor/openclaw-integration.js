// FC Online官网监控 - OpenClaw集成脚本
// 版本：v1.0.0

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class FCOMonitor {
  constructor() {
    this.skillDir = __dirname;
    this.scriptPath = path.join(this.skillDir, 'fco-monitor.sh');
    this.configPath = '/tmp/fco-monitor-config.json';
    this.logDir = '/tmp/fco-monitor-logs';
    
    // 确保日志目录存在
    if (!fs.existsSync(this.logDir)) {
      fs.mkdirSync(this.logDir, { recursive: true });
    }
  }

  // 执行shell命令
  execCommand(command, options = {}) {
    try {
      const result = execSync(command, {
        cwd: this.skillDir,
        encoding: 'utf8',
        stdio: 'pipe',
        ...options
      });
      return { success: true, output: result.trim() };
    } catch (error) {
      return { 
        success: false, 
        error: error.message,
        stderr: error.stderr?.toString() || '',
        stdout: error.stdout?.toString() || ''
      };
    }
  }

  // 立即检查官网
  async checkNow() {
    console.log('🔍 开始检查FC Online官网...');
    
    const result = this.execCommand(`"${this.scriptPath}" check-now`);
    
    if (result.success) {
      const output = result.output;
      
      if (output.includes('无新活动') || output.includes('未发现明显的活动信息')) {
        console.log('ℹ️ 无新活动');
        return { hasNewActivities: false, message: output };
      } else {
        console.log('🎯 发现新活动！');
        return { hasNewActivities: true, message: output };
      }
    } else {
      console.error('❌ 检查失败:', result.error);
      return { 
        hasNewActivities: false, 
        message: `检查失败: ${result.error}`,
        error: true 
      };
    }
  }

  // 设置定时监控
  async setupMonitor(startHour = 8, endHour = 23, intervalMinutes = 60) {
    console.log(`⏰ 设置监控: ${startHour}:00-${endHour}:00, 间隔${intervalMinutes}分钟`);
    
    const result = this.execCommand(
      `"${this.scriptPath}" setup ${startHour} ${endHour} ${intervalMinutes}`
    );
    
    if (result.success) {
      console.log('✅ 监控设置成功');
      
      // 创建OpenClaw cron任务
      await this.createOpenClawCronJob(startHour, endHour);
      
      return { success: true, message: result.output };
    } else {
      console.error('❌ 监控设置失败:', result.error);
      return { success: false, error: result.error };
    }
  }

  // 创建OpenClaw cron任务
  async createOpenClawCronJob(startHour, endHour) {
    try {
      // 生成cron表达式：每天startHour到endHour的整点
      const cronExpr = `0 ${startHour}-${endHour} * * *`;
      
      const jobConfig = {
        name: "FC Online官网整点检查",
        schedule: {
          kind: "cron",
          expr: cronExpr,
          tz: "Asia/Shanghai"
        },
        payload: {
          kind: "agentTurn",
          message: "执行FC Online官网检查：访问https://fco.qq.com/main.shtml检查最新活动，如果有新活动则总结关键信息通知用户。"
        },
        sessionTarget: "isolated",
        enabled: true,
        delivery: {
          mode: "announce"
        }
      };
      
      console.log(`📅 创建cron任务: ${cronExpr}`);
      
      // 这里应该调用OpenClaw的cron API
      // 实际实现中，这会通过OpenClaw的工具调用
      
      return { success: true, cronExpr };
    } catch (error) {
      console.error('❌ 创建cron任务失败:', error);
      return { success: false, error: error.message };
    }
  }

  // 显示状态
  async showStatus() {
    console.log('📊 获取监控状态...');
    
    const result = this.execCommand(`"${this.scriptPath}" status`);
    
    if (result.success) {
      console.log('✅ 状态获取成功');
      return { success: true, status: result.output };
    } else {
      console.error('❌ 状态获取失败:', result.error);
      return { success: false, error: result.error };
    }
  }

  // 获取最近日志
  async getRecentLogs(limit = 10) {
    try {
      const logFiles = fs.readdirSync(this.logDir)
        .filter(file => file.endsWith('.log'))
        .sort()
        .reverse()
        .slice(0, 5); // 最近5个日志文件
      
      let logs = [];
      
      for (const file of logFiles) {
        const filePath = path.join(this.logDir, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n').filter(line => line.trim());
        
        // 取最后limit行
        const recentLines = lines.slice(-limit);
        logs.push(`=== ${file} ===`);
        logs.push(...recentLines);
      }
      
      return { success: true, logs: logs.join('\n') };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // 测试连接
  async testConnection() {
    console.log('🔗 测试FC Online官网连接...');
    
    const testUrl = 'https://fco.qq.com/main.shtml';
    
    try {
      const result = this.execCommand(`curl -s -I --connect-timeout 10 "${testUrl}" | head -1`);
      
      if (result.success && result.output.includes('200')) {
        console.log('✅ 连接测试成功');
        return { success: true, message: '官网可正常访问' };
      } else {
        console.log('⚠️ 连接测试异常:', result.output);
        return { success: false, message: result.output || '连接失败' };
      }
    } catch (error) {
      console.error('❌ 连接测试失败:', error);
      return { success: false, error: error.message };
    }
  }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
  module.exports = FCOMonitor;
}

// 命令行接口
if (require.main === module) {
  const monitor = new FCOMonitor();
  const command = process.argv[2];
  
  async function run() {
    switch (command) {
      case 'check':
      case 'check-now':
        const checkResult = await monitor.checkNow();
        console.log(checkResult.message);
        break;
        
      case 'setup':
        const startHour = parseInt(process.argv[3]) || 8;
        const endHour = parseInt(process.argv[4]) || 23;
        const interval = parseInt(process.argv[5]) || 60;
        const setupResult = await monitor.setupMonitor(startHour, endHour, interval);
        console.log(setupResult.message || setupResult.error);
        break;
        
      case 'status':
        const statusResult = await monitor.showStatus();
        console.log(statusResult.status || statusResult.error);
        break;
        
      case 'test':
        const testResult = await monitor.testConnection();
        console.log(testResult.message || testResult.error);
        break;
        
      case 'logs':
        const limit = parseInt(process.argv[3]) || 10;
        const logsResult = await monitor.getRecentLogs(limit);
        console.log(logsResult.logs || logsResult.error);
        break;
        
      case 'help':
      default:
        console.log(`
FC Online官网监控工具 - OpenClaw集成版
版本: 1.0.0

使用方法:
  node openclaw-integration.js <命令> [参数]

命令:
  check-now          立即检查官网活动
  setup [开始] [结束] [间隔]  设置定时监控
  status             显示监控状态
  test               测试官网连接
  logs [行数]        查看最近日志
  help               显示帮助信息

示例:
  node openclaw-integration.js check-now
  node openclaw-integration.js setup 8 23 60
  node openclaw-integration.js status
  node openclaw-integration.js logs 20
        `);
        break;
    }
  }
  
  run().catch(console.error);
}