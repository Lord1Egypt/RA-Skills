/**
 * File Transfer - Main Entry Point
 *
 * @module file-transfer
 * @version 0.2.0-beta
 * @license MIT
 */

import { ContextEngine } from './core/context-engine.js';
import { FileManager } from './core/file-manager.js';
import { TelegramAdapter } from './adapters/telegram-adapter.js';

/**
 * Main File Transfer Skill class
 */
class FileTransferSkill {
  /**
   * Create a new FileTransferSkill instance
   * @param {Object} config - Configuration options
   */
  constructor(config = {}) {
    this.config = config;

    // Initialize core components
    this.contextEngine = new ContextEngine(config.contextEngine);
    this.fileManager = new FileManager(config.file);

    // Initialize channel adapters
    this.channels = this.initializeChannels();
  }

  /**
   * Initialize channel adapters based on configuration
   * @returns {Object} Map of channel adapters
   * @private
   */
  initializeChannels() {
    const channels = {};
    const channelConfigs = this.config.channels || {};

    if (channelConfigs.telegram?.enabled) {
      try {
        channels.telegram = new TelegramAdapter(channelConfigs.telegram);
      } catch (error) {
        console.error('Failed to initialize Telegram adapter', error.message);
      }
    }

    return channels;
  }

  /**
   * Send a file with context-aware intelligence
   * @param {Object} options - File transfer options
   * @param {string} options.file - Path to the file
   * @param {string} [options.caption] - File description
   * @param {Object} [options.context] - Conversation context
   * @param {Object} [options.metadata] - Additional metadata
   * @returns {Promise<Object>} Transfer result
   */
  async sendFileWithContext(options) {
    const startTime = Date.now();

    try {
      // 1. Validate and prepare file
      const fileInfo = await this.fileManager.validateFile(options.file);
      if (!fileInfo.valid) {
        throw new Error(fileInfo.error);
      }

      // 2. Analyze context
      const contextAnalysis = await this.contextEngine.analyzeContext(options.context || {});

      // 3. Select appropriate channel
      const channel = this.selectChannel(fileInfo, contextAnalysis);

      // 4. Transfer file through selected channel
      const transferResult = await channel.sendFile({
        filePath: options.file,
        chatId: options.context?.chatId,
        caption: options.caption,
        options: options.metadata
      });

      return {
        success: true,
        messageId: transferResult.messageId,
        context: contextAnalysis,
        stats: {
          size: this.fileManager.formatBytes(fileInfo.size),
          duration: Date.now() - startTime,
          channel: 'Telegram'
        }
      };

    } catch (error) {
      console.error('File transfer failed', {
        file: options.file,
        error: error.message,
        duration: Date.now() - startTime
      });
      throw error;
    }
  }

  /**
   * Select appropriate channel based on file and context
   * @param {Object} fileInfo - File information
   * @param {Object} contextAnalysis - Context analysis
   * @returns {Object} Selected channel adapter
   * @private
   */
  selectChannel(fileInfo, contextAnalysis) {
    const availableChannels = Object.values(this.channels);

    if (availableChannels.length === 0) {
      throw new Error('No available channels can handle this file');
    }

    return availableChannels[0];
  }

  /**
   * Get transfer history
   * @param {Object} [options] - Query options
   * @returns {Promise<Object>} Transfer history
   */
  async getTransferHistory(options = {}) {
    return {
      history: [],
      stats: {
        total: 0,
        successful: 0,
        failed: 0
      }
    };
  }

  /**
   * Configure the skill
   * @param {Object} newConfig - New configuration
   */
  configure(newConfig) {
    Object.assign(this.config, newConfig);

    if (newConfig.channels) {
      this.channels = this.initializeChannels();
    }
  }

  /**
   * Get skill status
   * @returns {Object} Status information
   */
  getStatus() {
    return {
      version: '0.2.0-beta',
      channels: Object.keys(this.channels),
      uptime: process.uptime()
    };
  }
}

export { FileTransferSkill };
export { ContextEngine } from './core/context-engine.js';
export { FileManager } from './core/file-manager.js';
export { TelegramAdapter } from './adapters/telegram-adapter.js';
export default FileTransferSkill;
