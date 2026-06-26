require('dotenv').config();
const express = require('express');
const SkillPayment = require('./payment');
const RootDataScraper = require('./scrapers/rootdata');
const TwitterScraper = require('./scrapers/twitter');
const TelegramNotifier = require('./notifiers/telegram');
const DiscordNotifier = require('./notifiers/discord');
const EmailNotifier = require('./notifiers/email');
const Scheduler = require('./scheduler');

/**
 * 主应用类
 */
class CryptoFundingMonitor {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 3000;

    // 初始化支付系统
    this.payment = new SkillPayment(process.env.SKILLPAY_API_KEY);

    // 初始化数据抓取器
    this.rootDataScraper = new RootDataScraper(process.env.ROOTDATA_API_KEY);
    this.twitterScraper = new TwitterScraper(process.env.TWITTER_BEARER_TOKEN);

    // 初始化通知推送器
    this.telegramNotifier = new TelegramNotifier(process.env.TELEGRAM_BOT_TOKEN);
    this.discordNotifier = new DiscordNotifier(process.env.DISCORD_WEBHOOK_URL);
    this.emailNotifier = new EmailNotifier({
      host: process.env.EMAIL_HOST,
      port: process.env.EMAIL_PORT,
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS
    });

    // 初始化调度器
    this.scheduler = new Scheduler();

    // 用户订阅数据（实际应用中应使用数据库）
    this.subscriptions = new Map();

    this.setupMiddleware();
    this.setupRoutes();
    this.setupScheduledTasks();
  }

  /**
   * 设置中间件
   */
  setupMiddleware() {
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // CORS
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
      next();
    });

    // 日志
    this.app.use((req, res, next) => {
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
      next();
    });
  }

  /**
   * 设置路由
   */
  setupRoutes() {
    // 健康检查
    this.app.get('/health', (req, res) => {
      res.json({ status: 'ok', timestamp: new Date().toISOString() });
    });

    // 触发监测并推送
    this.app.post('/monitor', async (req, res) => {
      try {
        const { userId, transactionId, channels } = req.body;

        // 验证支付
        const paymentVerified = await this.payment.verifyPayment(userId, transactionId);
        if (!paymentVerified) {
          return res.status(402).json({ error: 'Payment required or verification failed' });
        }

        // 收集数据
        const data = await this.collectData();

        // 推送通知
        const results = await this.sendNotifications(data, channels);

        // 记录使用
        await this.payment.logUsage(userId, 'monitor');

        res.json({
          success: true,
          data: {
            fundingCount: data.funding.length,
            tegCount: data.teg.length,
            notifications: results
          }
        });
      } catch (error) {
        console.error('Monitor endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // 订阅服务
    this.app.post('/subscribe', async (req, res) => {
      try {
        const { userId, channels, schedule } = req.body;

        if (!userId || !channels) {
          return res.status(400).json({ error: 'Missing required fields' });
        }

        // 创建支付请求
        const paymentRequest = await this.payment.createPaymentRequest(userId);

        // 保存订阅信息（待支付确认）
        this.subscriptions.set(userId, {
          channels,
          schedule: schedule || ['0 9 * * *', '0 18 * * *'],
          status: 'pending',
          paymentId: paymentRequest.paymentId
        });

        res.json({
          success: true,
          message: 'Subscription created, please complete payment',
          payment: paymentRequest
        });
      } catch (error) {
        console.error('Subscribe endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // 取消订阅
    this.app.post('/unsubscribe', async (req, res) => {
      try {
        const { userId } = req.body;

        if (!userId) {
          return res.status(400).json({ error: 'Missing userId' });
        }

        this.subscriptions.delete(userId);

        res.json({
          success: true,
          message: 'Subscription cancelled'
        });
      } catch (error) {
        console.error('Unsubscribe endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // 获取订阅状态
    this.app.get('/subscription/:userId', (req, res) => {
      const { userId } = req.params;
      const subscription = this.subscriptions.get(userId);

      if (!subscription) {
        return res.status(404).json({ error: 'Subscription not found' });
      }

      res.json({
        success: true,
        subscription
      });
    });

    // 支付回调
    this.app.post('/payment/callback', async (req, res) => {
      try {
        const { userId, paymentId, status } = req.body;

        if (status === 'completed') {
          const subscription = this.subscriptions.get(userId);
          if (subscription && subscription.paymentId === paymentId) {
            subscription.status = 'active';
            this.subscriptions.set(userId, subscription);
          }
        }

        res.json({ success: true });
      } catch (error) {
        console.error('Payment callback error:', error);
        res.status(500).json({ error: error.message });
      }
    });
  }

  /**
   * 收集数据
   */
  async collectData() {
    console.log('Collecting data from sources...');

    const [
      rootDataFunding,
      rootDataTEG,
      twitterFunding,
      twitterTEG
    ] = await Promise.all([
      this.rootDataScraper.getLatestFunding(),
      this.rootDataScraper.getTEGProjects(),
      this.twitterScraper.searchFundingTweets(),
      this.twitterScraper.searchTEGTweets()
    ]);

    return {
      funding: [...rootDataFunding],
      teg: [...rootDataTEG],
      tweets: {
        funding: twitterFunding,
        teg: twitterTEG
      }
    };
  }

  /**
   * 发送通知
   */
  async sendNotifications(data, channels = {}) {
    const results = {};

    // Telegram
    if (channels.telegram && channels.telegram.chatId) {
      results.telegram = await this.telegramNotifier.sendFundingReport(
        channels.telegram.chatId,
        data.funding,
        data.teg
      );
    }

    // Discord
    if (channels.discord) {
      results.discord = await this.discordNotifier.sendEmbedReport(
        data.funding,
        data.teg
      );
    }

    // Email
    if (channels.email && channels.email.to) {
      results.email = await this.emailNotifier.sendReport(
        channels.email.to,
        data.funding,
        data.teg
      );
    }

    return results;
  }

  /**
   * 设置定时任务
   */
  setupScheduledTasks() {
    // 早上9点推送
    this.scheduler.addTask(
      process.env.SCHEDULE_MORNING || '0 9 * * *',
      async () => {
        await this.runScheduledReport();
      },
      'Morning Report'
    );

    // 晚上6点推送
    this.scheduler.addTask(
      process.env.SCHEDULE_EVENING || '0 18 * * *',
      async () => {
        await this.runScheduledReport();
      },
      'Evening Report'
    );

    this.scheduler.startAll();
  }

  /**
   * 执行定时报告
   */
  async runScheduledReport() {
    console.log('Running scheduled report...');

    try {
      const data = await this.collectData();

      // 遍历所有活跃订阅
      for (const [userId, subscription] of this.subscriptions.entries()) {
        if (subscription.status === 'active') {
          await this.sendNotifications(data, subscription.channels);
          await this.payment.logUsage(userId, 'scheduled_report');
        }
      }

      console.log('Scheduled report completed');
    } catch (error) {
      console.error('Scheduled report failed:', error);
    }
  }

  /**
   * 启动服务器
   */
  start() {
    this.app.listen(this.port, () => {
      console.log(`\n🚀 Crypto Funding Monitor started`);
      console.log(`📡 Server running on port ${this.port}`);
      console.log(`💰 SkillPay integration: ${this.payment.apiKey ? 'Enabled' : 'Disabled'}`);
      console.log(`📅 Scheduled tasks: ${this.scheduler.getTasks().length}`);
      console.log(`\nEndpoints:`);
      console.log(`  POST /monitor - Trigger monitoring`);
      console.log(`  POST /subscribe - Subscribe to reports`);
      console.log(`  POST /unsubscribe - Unsubscribe`);
      console.log(`  GET  /health - Health check`);
      console.log(`\n`);
    });

    // 启动Telegram bot
    if (process.env.TELEGRAM_BOT_TOKEN) {
      this.telegramNotifier.launch();
    }

    // 优雅关闭
    process.on('SIGINT', () => {
      console.log('\nShutting down gracefully...');
      this.scheduler.stopAll();
      process.exit(0);
    });
  }
}

// 启动应用
if (require.main === module) {
  const monitor = new CryptoFundingMonitor();
  monitor.start();
}

module.exports = CryptoFundingMonitor;
