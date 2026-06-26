/**
 * TikTok 自动回复技能 - 主程序
 * 
 * ⚠️ 使用前请确保：
 * 1. 已配置 config.json
 * 2. 了解 TikTok API 使用限制
 * 3. 知晓自动化回复的风险
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG_PATH = path.join(__dirname, 'config.json');

// 加载配置
function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在！请复制 config.example.json 为 config.json 并配置');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
}

// TikTok API 客户端（简化版）
class TikTokClient {
  constructor(config) {
    this.accessToken = config.tiktok.accessToken;
    this.baseUrl = 'https://open.tiktokapis.com/v2';
  }

  // 获取热门视频
  async searchVideos(keywords) {
    console.log(`🔍 搜索关键词：${keywords.join(', ')}`);
    
    // 注意：实际使用需要调用 TikTok Research API 或 Content Posting API
    // 这里只是示例框架
    console.log('⚠️  需要 TikTok 企业 API 权限才能调用搜索接口');
    console.log('📖 参考：https://developers.tiktok.com/doc/research-api-specs-search-videos');
    
    // 模拟返回（实际使用需要替换为真实 API 调用）
    return {
      videos: []
    };
  }

  // 获取视频评论
  async getVideoComments(videoId) {
    console.log(`📝 获取视频评论：${videoId}`);
    
    // 需要 TikTok API 权限
    console.log('⚠️  需要 TikTok API 评论读取权限');
    
    return {
      comments: []
    };
  }

  // 回复评论
  async replyComment(videoId, commentId, text) {
    console.log(`💬 回复评论：${videoId}/${commentId}`);
    console.log(`   内容：${text}`);
    
    // 需要 TikTok API 评论写入权限
    console.log('⚠️  需要 TikTok API 评论写入权限（企业权限）');
    
    // 模拟回复
    return {
      success: true,
      replyId: 'mock_reply_' + Date.now()
    };
  }
}

// 自动回复逻辑
class AutoReplier {
  constructor(config) {
    this.config = config;
    this.client = new TikTokClient(config);
    this.replyCount = 0;
    this.lastReset = Date.now();
  }

  // 选择回复模板
  pickReplyTemplate() {
    const templates = this.config.replyTemplates;
    return templates[Math.floor(Math.random() * templates.length)];
  }

  // 检查是否超过限制
  canReply() {
    const now = Date.now();
    const hourMs = 60 * 60 * 1000;
    
    // 每小时重置计数
    if (now - this.lastReset > hourMs) {
      this.replyCount = 0;
      this.lastReset = now;
    }
    
    return this.replyCount < this.config.maxRepliesPerHour;
  }

  // 执行一次检查
  async check() {
    console.log('\n🔔 开始检查热门视频...');
    
    const { videos } = await this.client.searchVideos(this.config.keywords);
    
    if (videos.length === 0) {
      console.log('✅ 没有找到相关视频');
      return;
    }
    
    console.log(`📺 找到 ${videos.length} 个视频`);
    
    for (const video of videos.slice(0, 5)) {
      if (!this.canReply()) {
        console.log('⏸️  已达到每小时回复上限');
        break;
      }
      
      const { comments } = await this.client.getVideoComments(video.id);
      
      // 回复最新评论（示例逻辑）
      if (comments.length > 0) {
        const replyText = this.pickReplyTemplate();
        await this.client.replyComment(video.id, comments[0].id, replyText);
        this.replyCount++;
      }
    }
    
    console.log(`✅ 本次检查完成，回复数：${this.replyCount}/${this.config.maxRepliesPerHour}`);
  }

  // 持续监控
  async watch() {
    const interval = this.config.checkIntervalMinutes * 60 * 1000;
    console.log(`👀 开始监控，检查间隔：${this.config.checkIntervalMinutes} 分钟`);
    
    // 立即执行一次
    await this.check();
    
    // 定时执行
    setInterval(async () => {
      await this.check();
    }, interval);
  }
}

// 主程序
async function main() {
  console.log('🦞 TikTok 自动回复技能启动\n');
  console.log('⚠️  风险提示：自动化操作可能导致账号受限，请谨慎使用！\n');
  
  const config = loadConfig();
  
  if (config.dryRun) {
    console.log('🧪 当前为演示模式（dryRun=true），不会实际发送回复\n');
  }
  
  const replier = new AutoReplier(config);
  
  // 检查模式：运行一次
  // 监控模式：持续运行
  const mode = process.argv[2] || 'check';
  
  if (mode === 'watch') {
    await replier.watch();
  } else {
    await replier.check();
    console.log('\n✅ 执行完成');
  }
}

// 运行
main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
