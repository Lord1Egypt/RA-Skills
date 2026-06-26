/**
 * Telegram文件传输适配器
 * 
 * 负责处理Telegram平台的文件传输逻辑，包括：
 * 1. 文件上传到Telegram
 * 2. 消息发送和回复
 * 3. 进度跟踪和状态更新
 * 4. 错误处理和重试机制
 * 
 * @module adapters/telegram-adapter
 */

import { ContextEngine } from '../core/context-engine.js';
import { FileManager } from '../core/file-manager.js';
import { formatBytes } from '../utils/format.js';

/**
 * Telegram文件传输适配器
 */
export class TelegramAdapter {
  /**
   * 创建Telegram适配器实例
   * @param {Object} config - 适配器配置
   */
  constructor(config = {}) {
    this.config = {
      maxFileSize: config.maxFileSize || 50 * 1024 * 1024, // 50MB Telegram限制
      supportedFormats: config.supportedFormats || [
        // 文档
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'text/markdown',
        'application/json',
        
        // 图片
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
        
        // 视频
        'video/mp4',
        'video/quicktime',
        
        // 压缩包
        'application/zip',
        'application/x-rar-compressed',
        'application/x-tar',
        'application/gzip'
      ],
      chunkSize: config.chunkSize || 10 * 1024 * 1024, // 10MB分块
      retryAttempts: config.retryAttempts || 3,
      retryDelay: config.retryDelay || 1000, // 1秒
      ...config
    };

    // 初始化核心模块
    this.contextEngine = new ContextEngine();
    this.fileManager = new FileManager({
      maxFileSize: this.config.maxFileSize,
      chunkSize: this.config.chunkSize
    });

    // 传输状态跟踪
    this.activeTransfers = new Map();
  }

  /**
   * 发送文件到Telegram
   * @param {Object} params - 发送参数
   * @param {string} params.filePath - 文件路径
   * @param {string} params.chatId - 聊天ID
   * @param {string} params.caption - 文件描述
   * @param {Object} params.options - 发送选项
   * @returns {Promise<Object>} 发送结果
   */
  async sendFile(params) {
    const {
      filePath,
      chatId,
      caption = '',
      options = {}
    } = params;

    const transferId = `telegram_${Date.now()}_${Math.random().toString(36).substring(2)}`;
    
    try {
      console.log(`📤 开始Telegram文件传输: ${transferId}`);
      console.log(`   文件: ${filePath}`);
      console.log(`   目标: ${chatId}`);

      // 1. 验证文件
      const validation = await this.fileManager.validateFile(filePath);
      if (!validation.valid) {
        throw new Error(`文件验证失败: ${validation.error}`);
      }

      // 2. 分析上下文
      const context = {
        filePath,
        fileName: validation.name,
        fileSize: validation.size,
        fileType: validation.mimeType,
        caption,
        chatInfo: {
          chatId,
          isGroupChat: chatId.startsWith('-100'),
          chatType: chatId.startsWith('-100') ? 'group' : 'private'
        },
        channelInfo: {
          type: 'telegram',
          id: chatId
        },
        history: []
      };

      const analysis = await this.contextEngine.analyzeContext(context);
      console.log(`📊 上下文分析: ${analysis.scenario}, 紧急程度: ${analysis.urgency}`);

      // 3. 准备传输
      const transfer = {
        id: transferId,
        filePath,
        chatId,
        caption,
        status: 'preparing',
        progress: 0,
        startTime: Date.now(),
        analysis
      };

      this.activeTransfers.set(transferId, transfer);

      // 4. 模拟文件传输（实际实现中会调用Telegram API）
      console.log('🔄 模拟Telegram文件传输中...');
      
      // 模拟进度更新
      for (let i = 0; i <= 100; i += 10) {
        await new Promise(resolve => setTimeout(resolve, 100));
        transfer.progress = i;
        transfer.status = i < 100 ? 'uploading' : 'completed';
        console.log(`  进度: ${i}%`);
      }

      // 5. 完成传输
      transfer.status = 'completed';
      transfer.endTime = Date.now();
      transfer.duration = transfer.endTime - transfer.startTime;

      const result = {
        success: true,
        transferId,
        messageId: `msg_${Date.now()}`,
        fileSize: validation.size,
        duration: transfer.duration,
        analysis
      };

      console.log(`✅ Telegram文件传输完成: ${transferId}`);
      console.log(`   耗时: ${transfer.duration}ms`);
      console.log(`   文件大小: ${this.formatBytes(validation.size)}`);

      return result;

    } catch (error) {
      console.error(`❌ Telegram文件传输失败: ${transferId}`, error);
      
      if (this.activeTransfers.has(transferId)) {
        const transfer = this.activeTransfers.get(transferId);
        transfer.status = 'failed';
        transfer.error = error.message;
        transfer.endTime = Date.now();
      }

      throw error;
    } finally {
      // 清理传输记录（保留一段时间用于调试）
      setTimeout(() => {
        this.activeTransfers.delete(transferId);
      }, 5 * 60 * 1000); // 5分钟后清理
    }
  }

  /**
   * 获取传输状态
   * @param {string} transferId - 传输ID
   * @returns {Object} 传输状态
   */
  getTransferStatus(transferId) {
    const transfer = this.activeTransfers.get(transferId);
    if (!transfer) {
      return {
        found: false,
        message: '传输记录不存在或已过期'
      };
    }

    return {
      found: true,
      transferId: transfer.id,
      status: transfer.status,
      progress: transfer.progress,
      fileName: transfer.filePath.split('/').pop(),
      startTime: transfer.startTime,
      endTime: transfer.endTime,
      duration: transfer.endTime ? transfer.endTime - transfer.startTime : null,
      analysis: transfer.analysis,
      error: transfer.error
    };
  }

  /**
   * 获取所有活动传输
   * @returns {Array} 活动传输列表
   */
  getActiveTransfers() {
    return Array.from(this.activeTransfers.values()).map(transfer => ({
      transferId: transfer.id,
      fileName: transfer.filePath.split('/').pop(),
      status: transfer.status,
      progress: transfer.progress,
      startTime: transfer.startTime,
      chatId: transfer.chatId
    }));
  }

  /**
   * 格式化字节大小
   * @private
   */
  formatBytes(bytes, decimals = 2) {
    return formatBytes(bytes, decimals);
  }

  /**
   * 获取适配器信息
   * @returns {Object} 适配器信息
   */
  getInfo() {
    return {
      name: 'Telegram File Transfer Adapter',
      version: '0.2.0-beta',
      platform: 'telegram',
      maxFileSize: this.config.maxFileSize,
      supportedFormats: this.config.supportedFormats.length,
      activeTransfers: this.activeTransfers.size,
      coreModules: {
        contextEngine: 'loaded',
        fileManager: 'loaded'
      }
    };
  }
}

export default TelegramAdapter;