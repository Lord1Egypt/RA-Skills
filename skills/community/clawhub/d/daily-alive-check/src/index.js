require('dotenv').config();
const express = require('express');
const SkillPayment = require('./payment');
const UserManager = require('./utils/userManager');
const AlertMonitor = require('./utils/alertMonitor');
const TelegramNotifier = require('./notifiers/telegram');
const DiscordNotifier = require('./notifiers/discord');
const EmailNotifier = require('./notifiers/email');
const Scheduler = require('./scheduler');

/**
 * 还活着么监测服务
 */
class AliveCheckMonitor {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 3000;

    // 初始化模块
    this.payment = new SkillPayment(process.env.SKILLPAY_API_KEY);
    this.userManager = new UserManager();

    // 初始化通知器
    const notifiers = {
      telegram: new TelegramNotifier(process.env.TELEGRAM_BOT_TOKEN),
      discord: new DiscordNotifier(process.env.DISCORD_WEBHOOK_URL),
      email: new EmailNotifier({
        host: process.env.EMAIL_HOST,
        port: process.env.EMAIL_PORT,
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
      })
    };

    this.alertMonitor = new AlertMonitor(this.userManager, notifiers);
    this.scheduler = new Scheduler();

    this.setupMiddleware();
    this.setupRoutes();
    this.setupScheduledTasks();
  }

  setupMiddleware() {
    this.app.use(express.json());
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      next();
    });
    this.app.use((req, res, next) => {
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
      next();
    });
  }

  setupRoutes() {
    // 健康检查
    this.app.get('/health', (req, res) => {
      res.json({ status: 'ok', timestamp: new Date().toISOString() });
    });

    // 注册用户
    this.app.post('/register', async (req, res) => {
      try {
        const { userId, name, phone, emergencyContacts } = req.body;

        if (!userId || !name) {
          return res.status(400).json({ error: '缺少必需字段' });
        }

        const user = this.userManager.registerUser(userId, {
          name,
          phone,
          emergencyContacts
        });

        res.json({
          success: true,
          message: '注册成功',
          user
        });
      } catch (error) {
        console.error('注册失败:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // 用户签到
    this.app.post('/checkin', async (req, res) => {
      try {
        const { userId, message, mood, location } = req.body;

        if (!userId) {
          return res.status(400).json({ error: '缺少userId' });
        }

        const result = this.userManager.checkin(userId, {
          message,
          mood,
          location
        });

        res.json({
          success: true,
          message: '签到成功！',
          data: result
        });
      } catch (error) {
        console.error('签到失败:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // 查询状态
    this.app.get('/status/:userId', (req, res) => {
      try {
        const { userId } = req.params;
        const status = this.userManager.getUserStatus(userId);

        if (!status) {
          return res.status(404).json({ error: '用户不存在' });
        }

        res.json({
          success: true,
          data: status
        });
      } catch (error) {
        console.error('查询状态失败:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // 查看签到历史
    this.app.get('/history/:userId', (req, res) => {
      try {
        const { userId } = req.params;
        const { days = 7 } = req.query;

        const history = this.userManager.getCheckinHistory(userId, parseInt(days));

        res.json({
          success: true,
          userId,
          days: parseInt(days),
          count: history.length,
          data: history
        });
      } catch (error) {
        console.error('查询历史失败:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // 更新紧急联系人
    this.app.post('/emergency-contacts', async (req, res) => {
      try {
        const { userId, contacts } = req.body;

        if (!userId || !contacts) {
          return res.status(400).json({ error: '缺少必需字段' });
        }

        const user = this.userManager.updateEmergencyContacts(userId, contacts);

        res.json({
          success: true,
          message: '更新成功',
          user
        });
      } catch (error) {
        console.error('更新联系人失败:', error);
        res.status(500).json({ error: error.message });
      }
    });
  }

  setupScheduledTasks() {
    const checkInterval = process.env.CHECK_INTERVAL_HOURS || 6;
    const schedule = `0 */${checkInterval} * * *`;

    this.scheduler.addTask(
      schedule,
      async () => {
        await this.alertMonitor.checkAllUsers();
      },
      '用户状态检查'
    );

    this.scheduler.startAll();
  }

  start() {
    this.app.listen(this.port, () => {
      console.log(`\n💝 还活着么监测服务已启动`);
      console.log(`📡 服务器运行在端口 ${this.port}`);
      console.log(`💰 SkillPay集成: ${this.payment.apiKey ? '已启用' : '未启用'}`);
      console.log(`📅 定时任务: ${this.scheduler.getTasks().length} 个`);
      console.log(`\n端点:`);
      console.log(`  POST /register - 注册用户`);
      console.log(`  POST /checkin - 每日签到`);
      console.log(`  GET  /status/:userId - 查询状态`);
      console.log(`  GET  /history/:userId - 签到历史`);
      console.log(`  POST /emergency-contacts - 更新紧急联系人`);
      console.log(`\n`);
    });

    process.on('SIGINT', () => {
      console.log('\n正在关闭服务...');
      this.scheduler.stopAll();
      process.exit(0);
    });
  }
}

if (require.main === module) {
  const monitor = new AliveCheckMonitor();
  monitor.start();
}

module.exports = AliveCheckMonitor;
