const CookieStore = require('./storage/cookie-store');
const Auth115 = require('./auth');
const SessionManager = require('./session');
const FileBrowser = require('./files/browser');
const FileOperations = require('./files/operations');
const FileTransfer = require('./files/transfer');
const ShareTransfer = require('./share/transfer');
const LixianDownload = require('./lixian/download');
const SmartOrganizer = require('./organizer/smart-organizer');
const { formatSize: formatSizeUtil } = require('./utils/helpers');

/**
 * 115 Cloud Master Skill 主入口
 */
class Skill115Master {
  constructor(agent) {
    this.agent = agent;
    this.cookieStore = new CookieStore();
    this.auth = new Auth115(this.cookieStore);
    this.session = new SessionManager(this.cookieStore);
    
    // 客户端实例（登录后初始化）
    this.client = null;
  }

  /**
   * 初始化客户端
   */
  async initClient() {
    const cookie = await this.cookieStore.load();
    if (!cookie) {
      return false;
    }

    this.client = {
      browser: new FileBrowser(cookie),
      operations: new FileOperations(cookie),
      transfer: new FileTransfer(cookie),
      share: new ShareTransfer(cookie),
      lixian: new LixianDownload(cookie),
      organizer: new SmartOrganizer(cookie)
    };

    return true;
  }

  /**
   * 处理消息
   * @param {string} message - 用户消息
   * @param {Object} context - 上下文
   * @returns {Promise<string>} 回复
   */
  async handle(message, _context = {}) {
    // 输入校验
    if (typeof message !== 'string' || !message.trim()) {
      return '❌ 参数错误，请提供有效的消息';
    }

    const msg = message.trim().toLowerCase();

    // 登录
    if (msg.includes('登录') || msg.includes('登陆')) {
      return this.handleLogin();
    }

    // 检查登录状态
    const isLoggedIn = await this.initClient();
    if (!isLoggedIn) {
      return '🔐 请先登录 115 网盘\n说"登录 115"开始';
    }

    // 容量查询
    if (msg.includes('容量') || msg.includes('空间') || msg.includes('还剩')) {
      return this.handleCapacity();
    }

    // 文件列表
    if (msg.includes('查看') || msg.includes('列表') || (msg.includes('文件') && !msg.includes('转存'))) {
      return this.handleListFiles(message);
    }

    // 转存
    if (msg.includes('转存') || msg.includes('115.com/s/')) {
      return this.handleTransfer(message);
    }

    // 离线下载
    if (msg.includes('磁力') || msg.includes('magnet:') || msg.includes('种子')) {
      return this.handleLixian(message);
    }

    // 下载任务
    if (msg.includes('下载任务') || msg.includes('任务列表')) {
      return this.handleTaskList();
    }

    // 整理
    if (msg.includes('整理') || msg.includes('分类')) {
      return this.handleOrganize(message);
    }

    // 搜索
    if (msg.includes('搜索') || msg.includes('找')) {
      return this.handleSearch(message);
    }

    // 清理建议
    if (msg.includes('清理') || msg.includes('建议')) {
      return this.handleCleanup();
    }

    // 帮助
    if (msg.includes('帮助') || msg.includes('功能')) {
      return this.showHelp();
    }

    // 默认回复
    return this.showHelp();
  }

  /**
   * 登录处理
   */
  async handleLogin() {
    const sessionInfo = await this.session.getSessionInfo();
    if (sessionInfo.loggedIn) {
      return `✅ 已登录\n👤 UID: ${sessionInfo.uid}\n💎 VIP: ${sessionInfo.vip ? sessionInfo.vipType || '是' : '否'}`;
    }

    // 生成二维码
    const qrData = await this.auth.generateQRCode();
    if (!qrData.success) {
      return `❌ 生成二维码失败：${qrData.error}`;
    }

    // 发送二维码
    await this.agent.sendImage(qrData.image, '📱 请使用 115 手机 APP 扫码登录\n⏱️ 二维码 5 分钟有效');

    // 开始轮询
    await this.agent.sendMessage('⏳ 等待扫码中...');

    // 异步登录
    this.auth.login({
      onStatus: async (status) => {
        if (status.status === 'scanned') {
          await this.agent.sendMessage('✅ 已扫码，请在手机上确认');
        }
      },
      onComplete: async (_result) => {
        await this.initClient();
        await this.agent.sendMessage(`🎉 登录成功！\n说"帮助"查看功能`);
      },
      onError: async (error) => {
        await this.agent.sendMessage(`❌ 登录失败：${error.message}`);
      }
    });

    return '';
  }

  /**
   * 容量查询
   */
  async handleCapacity() {
    const userInfo = await this.client.browser.http.get('/user/info');
    const data = userInfo.data || {};
    const usageRate = (data.used_capacity / data.capacity * 100).toFixed(1);

    return `📊 115 网盘容量
━━━━━━━━━━━━━━
👤 ${data.user_name || '用户'}
💎 ${data.vip ? (data.vip_type || 'VIP') : '普通用户'}

💾 存储空间
  已用：${this.formatSize(data.used_capacity)}
  总计：${this.formatSize(data.capacity)}
  剩余：${this.formatSize(data.capacity - data.used_capacity)}
  使用率：${usageRate}%`;
  }

  /**
   * 文件列表
   */
  async handleListFiles(message) {
    const cidMatch = message.match(/cid[=:]\s*(\d+)/i);
    const cid = cidMatch ? cidMatch[1] : '0';

    const result = await this.client.browser.listFiles(cid, { page: 1, size: 20 });
    
    const files = result.files.slice(0, 10).map(f => 
      `${f.is_dir ? '📁' : '📄'} ${f.file_name} (${this.formatSize(f.file_size)})`
    ).join('\n');

    return `📁 文件列表
━━━━━━━━━━━━━━
${files || '空目录'}
━━━━━━━━━━━━━━
共 ${result.totalCount} 个文件`;
  }

  /**
   * 转存处理
   */
  async handleTransfer(message) {
    const shareMatch = message.match(/115\.com\/s\/([a-zA-Z0-9]+)/i);
    if (!shareMatch) {
      return '请提供 115 分享链接\n格式：https://115.com/s/xxx';
    }

    const shareCode = shareMatch[1];
    const pwdMatch = message.match(/密码 [=:]\s*([a-zA-Z0-9]{4})/i);
    const password = pwdMatch ? pwdMatch[1] : '';

    const shareInfo = await this.client.share.getShareInfo(shareCode, password);
    
    const preview = shareInfo.files.slice(0, 5).map(f => 
      `  📄 ${f.file_name} (${this.formatSize(f.file_size)})`
    ).join('\n');

    return `📦 分享详情
━━━━━━━━━━━━━━
📝 ${shareInfo.title}
📁 ${shareInfo.totalCount} 个文件
💾 ${this.formatSize(shareInfo.totalSize)}

${preview}
━━━━━━━━━━━━━━
回复"确认转存"开始转存`;
  }

  /**
   * 离线下载
   */
  async handleLixian(message) {
    const magnetMatch = message.match(/magnet:\?xt=urn:btih:[a-zA-Z0-9]+/i);
    if (magnetMatch) {
      const result = await this.client.lixian.addMagnet(magnetMatch[0]);
      return `✅ 磁力任务已添加\n📥 ${result.fileName || '解析中...'}\n💾 ${this.formatSize(result.fileSize || 0)}`;
    }

    return '请提供磁力链接\n格式：magnet:?xt=urn:btih:...';
  }

  /**
   * 任务列表
   */
  async handleTaskList() {
    const stats = await this.client.lixian.getTaskStats();
    const taskList = await this.client.lixian.getTaskList({ size: 10 });

    const tasks = taskList.tasks.slice(0, 5).map(t => 
      `  ${this.getStatusIcon(t.status)} ${t.file_name} - ${t.percent || 0}%`
    ).join('\n');

    return `📥 离线下载任务
━━━━━━━━━━━━━━
📊 统计：共${stats.total} | ⏳${stats.pending} | ⬇️${stats.downloading} | ✅${stats.completed}

${tasks || '  暂无任务'}`;
  }

  /**
   * 整理处理
   */
  async handleOrganize(message) {
    if (message.includes('自动') || message.includes('智能')) {
      const result = await this.client.organizer.autoOrganizeByType('0', '/已整理');
      return `✅ 智能整理完成\n📁 移动：${result.moved}个\n❌ 失败：${result.failed}个`;
    }

    return '请选择：\n1. 自动按类型整理\n2. 按时间整理\n3. 查找重复文件';
  }

  /**
   * 搜索
   */
  async handleSearch(message) {
    const keywordMatch = message.match(/搜索\s+(.+)/i) || message.match(/找\s+(.+)/i);
    if (!keywordMatch) {
      return '请提供搜索关键词\n格式：搜索 文件名';
    }

    const result = await this.client.browser.searchFiles(keywordMatch[1], { page: 1, size: 10 });
    const files = result.files.slice(0, 5).map(f => 
      `📄 ${f.file_name} (${this.formatSize(f.file_size)})`
    ).join('\n');

    return `🔍 搜索结果
━━━━━━━━━━━━━━
${files || '未找到相关文件'}
━━━━━━━━━━━━━━
共 ${result.totalCount} 个结果`;
  }

  /**
   * 清理建议
   */
  async handleCleanup() {
    const suggestions = await this.client.organizer.getCleanupSuggestions('0');
    
    const list = suggestions.suggestions.map(s => 
      `${s.type === 'critical' ? '🔴' : s.type === 'warning' ? '🟡' : '🔵'} ${s.title}: ${s.message}`
    ).join('\n');

    return `💡 清理建议
━━━━━━━━━━━━━━
${list || '无需清理'}
━━━━━━━━━━━━━━`;
  }

  /**
   * 帮助信息
   */
  showHelp() {
    return `🎯 115 Cloud Master 功能
━━━━━━━━━━━━━━━━━━
🔐 登录 115 - 扫码登录
📊 容量/空间 - 查看存储
📁 查看文件 - 浏览文件
🔍 搜索 xxx - 搜索文件
🔄 转存 [链接] - 转存文件
⬇️ 磁力 [链接] - 离线下载
📥 下载任务 - 查看任务
🤖 整理文件 - 智能整理
💡 清理建议 - 获取建议
━━━━━━━━━━━━━━━━━━`;
  }

  /**
   * 格式化大小（使用工具函数）
   */
  formatSize(bytes) {
    return formatSizeUtil(bytes);
  }

  /**
   * 状态图标
   */
  getStatusIcon(status) {
    const icons = { 0: '⏳', 1: '⬇️', 2: '✅', '-1': '❌' };
    return icons[status] || '📄';
  }
}

module.exports = Skill115Master;
