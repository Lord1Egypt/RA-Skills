/**
 * 跨平台内容自动发布 - 主入口
 */

const XiaohongshuTextImageWorkflow = require('./src/workflows/xiaohongshu-text-image');
const VideoCrossPostWorkflow = require('./src/workflows/video-cross-post');
const XiaohongshuVideoWorkflow = require('./src/workflows/xiaohongshu-video');
const XiaohongshuPublisher = require('./src/platforms/xiaohongshu-publisher');
const TiktokPublisher = require('./src/platforms/tiktok-publisher');
const YoutubePublisher = require('./src/platforms/youtube-publisher');

module.exports = {
  // 工作流
  XiaohongshuTextImageWorkflow,
  VideoCrossPostWorkflow,
  XiaohongshuVideoWorkflow,
  // 平台发布器
  XiaohongshuPublisher,
  TiktokPublisher,
  YoutubePublisher,
  // 版本
  version: '1.0.0',
  /**
   * 快速运行小红书图文发布
   */
  async publishXiaohongshuTextImage(options) {
    const workflow = new XiaohongshuTextImageWorkflow();
    return await workflow.run(options);
  },
  /**
   * 快速运行视频跨平台搬运
   */
  async runVideoCrossPost(options) {
    const workflow = new VideoCrossPostWorkflow();
    return await workflow.run(options);
  },
  /**
   * 添加账号（首次登录）
   */
  async addAccount(platform, accountName, cookiePath) {
    let publisher;
    switch(platform) {
      case 'xiaohongshu':
        publisher = new XiaohongshuPublisher({ headless: false });
        break;
      case 'tiktok':
        publisher = new TiktokPublisher({ headless: false });
        break;
      case 'youtube':
        publisher = new YoutubePublisher({ headless: false });
        break;
      default:
        throw new Error(`不支持的平台: ${platform}`);
    }
    await publisher.init({ name: accountName });
    await publisher.loginAndSave(cookiePath);
    await publisher.close();
    return { success: true, platform, accountName, cookiePath };
  },
  /**
   * 快速运行小红书口播视频发布
   */
  async publishXiaohongshuVideo(options) {
    const workflow = new XiaohongshuVideoWorkflow();
    return await workflow.run(options);
  }
};
