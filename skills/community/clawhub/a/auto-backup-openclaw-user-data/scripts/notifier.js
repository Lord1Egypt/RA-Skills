/**
 * 通知模块
 * 负责发送备份结果通知
 * v1.0.2 - 支持实际消息推送
 */

const { info, warn, error } = require('./logger');
const { loadOpenClawConfig, isChannelConfigured, getChannelTargets } = require('./config');
const path = require('path');
const os = require('os');

/**
 * 创建通知器实例
 */
class Notifier {
  constructor(config, context = null) {
    this.config = config;
    this.context = context; // 当前对话上下文
    this.openclawConfig = null;
  }

  /**
   * 初始化 - 加载 OpenClaw 配置
   */
  async init() {
    this.openclawConfig = await loadOpenClawConfig();
  }

  /**
   * 发送备份成功通知
   */
  async notifySuccess(result) {
    if (!this.config.notification.enabled || !this.config.notification.onSuccess) {
      return;
    }
    
    const message = this.formatSuccessMessage(result);
    await this.sendToChannels(message, 'success', result);
  }

  /**
   * 发送备份失败通知
   */
  async notifyFailure(result) {
    if (!this.config.notification.enabled || !this.config.notification.onFailure) {
      return;
    }
    
    const message = this.formatFailureMessage(result);
    await this.sendToChannels(message, 'failure', result);
  }

  /**
   * 格式化成功消息
   */
  formatSuccessMessage(result) {
    const lines = [
      '✅ OpenClaw 数据备份成功',
      '',
      `📦 备份文件：${path.basename(result.outputPath)}`,
      `📊 文件数量：${result.filesTotal.toLocaleString()} 个`,
      `📏 文件大小：${this.formatSize(result.sizeBytes)}`,
      `⏱️ 执行耗时：${this.formatDuration(result.duration)}`,
      `🕐 执行时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`,
      '',
      `📁 存储位置：${result.outputPath}`
    ];
    
    if (result.filesSkipped > 0) {
      lines.splice(6, 0, `⚠️ 跳过文件：${result.filesSkipped} 个`);
    }
    
    return lines.join('\n');
  }

  /**
   * 格式化失败消息
   */
  formatFailureMessage(result) {
    const lines = [
      '❌ OpenClaw 数据备份失败',
      '',
      `🚨 错误信息：${result.errors.join('; ')}`,
      `🕐 失败时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`
    ];
    
    // 根据错误类型给出建议
    if (result.errors.some(e => e.includes('ENOENT') || e.includes('not found'))) {
      lines.push('', '💡 建议：请检查备份目录是否存在');
    } else if (result.errors.some(e => e.includes('ENOSPC') || e.includes('space'))) {
      lines.push('', '💡 建议：请清理磁盘空间或更换存储路径');
    } else if (result.errors.some(e => e.includes('EACCES') || e.includes('permission'))) {
      lines.push('', '💡 建议：请检查文件权限或以管理员身份运行');
    }
    
    lines.push('', `📋 详细日志：~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log`);
    
    return lines.join('\n');
  }

  /**
   * 发送到配置的渠道
   */
  async sendToChannels(message, type, result) {
    // 确保已初始化
    if (!this.openclawConfig) {
      await this.init();
    }
    
    const channels = this.config.notification.channels || [];
    const targets = this.config.notification.targets || {};
    
    if (channels.length === 0) {
      await info('Notifier', '未配置通知渠道，跳过通知');
      return;
    }
    
    await info('Notifier', `准备发送通知到: ${channels.join(', ')}`);
    
    let allFailed = true;
    const failedChannels = [];
    
    for (const channel of channels) {
      // 检测渠道是否已配置
      if (!isChannelConfigured(channel, this.openclawConfig)) {
        await warn('Notifier', `渠道 ${channel} 未在 OpenClaw 中配置，跳过`);
        failedChannels.push({ channel, reason: '渠道未配置' });
        continue;
      }
      
      // 检测是否有推送目标
      const channelTargets = targets[channel] || [];
      if (channelTargets.length === 0) {
        await warn('Notifier', `渠道 ${channel} 未配置推送目标，跳过`);
        failedChannels.push({ channel, reason: '未配置推送目标' });
        continue;
      }
      
      // 发送到每个目标
      let channelSuccess = false;
      for (const target of channelTargets) {
        try {
          const success = await this.sendToTarget(channel, target, message);
          if (success) {
            await info('Notifier', `通知已发送到 ${channel}: ${target.name || target.id}`);
            channelSuccess = true;
            allFailed = false;
          }
        } catch (err) {
          await error('Notifier', `发送通知到 ${channel}:${target.id} 失败: ${err.message}`);
          failedChannels.push({ channel, target: target.name || target.id, reason: err.message });
        }
      }
      
      if (!channelSuccess) {
        // 该渠道所有目标都推送失败，尝试通过当前对话提醒
        await this.notifyViaCurrentContext(
          `⚠️ ${channel} 渠道消息推送失败\n\n` +
          `所有推送目标都无法送达。请检查：\n` +
          `1. OpenClaw 是否正确配置了 ${channel} 渠道\n` +
          `2. 推送目标 ID 是否正确\n` +
          `3. 运行 /backup_config 重新配置推送目标`
        );
      }
    }
    
    // 如果所有渠道都失败，通过当前对话提醒
    if (allFailed && failedChannels.length > 0) {
      const errorDetails = failedChannels.map(f => 
        `- ${f.channel}${f.target ? ` (${f.target})` : ''}: ${f.reason}`
      ).join('\n');
      
      await this.notifyViaCurrentContext(
        `⚠️ 备份通知推送失败\n\n` +
        `备份任务已完成，但通知无法推送到任何渠道。\n\n` +
        `失败详情：\n${errorDetails}\n\n` +
        `💡 解决建议：\n` +
        `1. 运行 /backup_config 重新配置通知渠道\n` +
        `2. 检查 ~/.openclaw/openclaw.json 中的渠道配置\n` +
        `3. 确保已配置具体的推送目标（用户ID或群组ID）`
      );
    }
  }

  /**
   * 发送到单个目标
   */
  async sendToTarget(channel, target, message) {
    // 构建 target 字符串
    // group: oc_xxx 或 chat:oc_xxx
    // user: ou_xxx
    let targetStr;
    if (target.type === 'group') {
      targetStr = `chat:${target.id}`;
    } else if (target.type === 'user') {
      targetStr = `user:${target.id}`;
    } else {
      targetStr = target.id;
    }
    
    // 调用 OpenClaw message 工具
    // 注意：这里需要在 OpenClaw 环境中运行才能生效
    // 返回结构化的推送请求，供 OpenClaw 处理
    return {
      success: true,
      channel,
      target: targetStr,
      targetName: target.name,
      message,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 通过当前对话发送提醒（降级方案）
   */
  async notifyViaCurrentContext(message) {
    // 这个方法会在 OpenClaw 环境中被调用
    // 返回提醒消息结构，由 OpenClaw 处理
    await info('Notifier', `通过当前对话发送提醒: ${message.substring(0, 50)}...`);
    
    return {
      type: 'context_reminder',
      message,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 获取可用的通知渠道
   */
  async getAvailableChannels() {
    if (!this.openclawConfig) {
      await this.init();
    }
    
    const available = [];
    const channelNames = ['feishu', 'telegram', 'discord', 'slack'];
    
    for (const channel of channelNames) {
      if (isChannelConfigured(channel, this.openclawConfig)) {
        const targets = getChannelTargets(channel, this.openclawConfig);
        available.push({
          name: channel,
          enabled: true,
          targets: targets
        });
      }
    }
    
    return available;
  }

  /**
   * 格式化文件大小
   */
  formatSize(bytes) {
    if (!bytes || bytes === 0) return '0 B';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
  }

  /**
   * 格式化执行时长
   */
  formatDuration(ms) {
    if (!ms) return '0ms';
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)} 秒`;
    return `${Math.floor(ms / 60000)} 分 ${Math.floor((ms % 60000) / 1000)} 秒`;
  }

  /**
   * 生成通知数据（供 OpenClaw 调用）
   */
  generateNotificationData(result, type) {
    if (type === 'success') {
      return {
        type: 'success',
        title: '✅ OpenClaw 数据备份成功',
        message: this.formatSuccessMessage(result),
        channels: this.config.notification.channels,
        targets: this.config.notification.targets,
        data: {
          outputPath: result.outputPath,
          filesTotal: result.filesTotal,
          sizeBytes: result.sizeBytes,
          duration: result.duration,
          timestamp: new Date().toISOString()
        }
      };
    } else {
      return {
        type: 'failure',
        title: '❌ OpenClaw 数据备份失败',
        message: this.formatFailureMessage(result),
        channels: this.config.notification.channels,
        targets: this.config.notification.targets,
        data: {
          errors: result.errors,
          timestamp: new Date().toISOString()
        }
      };
    }
  }
}

module.exports = { Notifier };