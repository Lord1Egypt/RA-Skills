/**
 * CLI 模块
 * 命令行接口入口
 * v1.0.2 - 增加选择性备份文件选择交互
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');

const { 
  loadConfig, 
  saveConfig, 
  resetConfig, 
  getConfigPaths, 
  configExists,
  ensureConfigDir,
  updateConfig,
  loadOpenClawConfig,
  getChannelTargets,
  BACKUPS_DIR 
} = require('./config');
const { info, warn, error, readLogs } = require('./logger');
const { BackupManager, initBackupManager, OPENCLAW_ROOT } = require('./backup');
const { Cleaner } = require('./cleaner');
const { describeCron } = require('./scheduler');

/**
 * CLI 命令处理器
 */
class CLI {
  constructor() {
    this.backupManager = null;
  }

  /**
   * 初始化
   */
  async init() {
    this.backupManager = await initBackupManager();
  }

  /**
   * 执行命令
   */
  async execute(command, args = {}) {
    // 确保初始化
    if (!this.backupManager) {
      await this.init();
    }

    switch (command) {
      case 'now':
      case 'backup_now':
        return this.cmdBackupNow(args);
      
      case 'status':
      case 'backup_status':
        return this.cmdBackupStatus();
      
      case 'config':
      case 'backup_config':
        return this.cmdBackupConfig(args);
      
      case 'list':
      case 'backup_list':
        return this.cmdBackupList(args);
      
      case 'clean':
      case 'backup_clean':
        return this.cmdBackupClean(args);
      
      case 'help':
        return this.cmdHelp();
      
      default:
        return this.outputError(`未知命令: ${command}`);
    }
  }

  /**
   * /backup_now - 立即执行备份
   */
  async cmdBackupNow(args) {
    const output = [];
    output.push('🔄 开始执行备份...');
    output.push('');
    
    try {
      const options = {
        full: args.full !== false,
        targets: args.targets
      };
      
      const result = await this.backupManager.execute(options);
      
      if (result.success) {
        output.push('✅ 备份完成！');
        output.push('');
        output.push(`📁 文件：${path.basename(result.outputPath)}`);
        output.push(`📊 文件数量：${result.filesTotal} 个`);
        output.push(`📏 大小：${this.formatSize(result.sizeBytes)}`);
        output.push(`⏱️ 耗时：${this.formatDuration(result.duration)}`);
        
        if (result.cleanResult && result.cleanResult.deleted > 0) {
          output.push(`🗑️ 清理旧备份：${result.cleanResult.deleted} 个`);
        }
      } else {
        output.push('❌ 备份失败！');
        output.push('');
        output.push(`错误：${result.errors.join('; ')}`);
      }
      
      return this.outputSuccess(output.join('\n'), result);
    } catch (err) {
      return this.outputError(`备份失败: ${err.message}`);
    }
  }

  /**
   * /backup_status - 查看备份状态
   */
  async cmdBackupStatus() {
    const output = [];
    
    try {
      const status = await this.backupManager.getStatus();
      const config = await loadConfig();
      
      output.push('📊 备份状态');
      output.push('━'.repeat(40));
      output.push('');
      
      // 调度状态
      output.push('🔄 调度状态');
      output.push(`  - 定时备份：${status.schedule.enabled ? '已启用' : '已禁用'}`);
      
      if (status.schedule.enabled) {
        output.push(`  - 执行时间：${describeCron(status.schedule.cron)}`);
        output.push(`  - 下次执行：${status.schedule.nextRun || '计算中...'}`);
      }
      
      if (status.schedule.lastRun) {
        output.push(`  - 上次执行：${new Date(status.schedule.lastRun).toLocaleString('zh-CN')}`);
      }
      
      output.push('');
      
      // 备份统计
      output.push('📦 备份统计');
      output.push(`  - 总备份数：${status.backups.count} 个`);
      output.push(`  - 总大小：${status.backups.totalSize}`);
      
      if (status.backups.newestBackup) {
        output.push(`  - 最近备份：${status.backups.newestBackup}`);
      }
      
      output.push('');
      
      // 存储位置
      output.push('📁 存储位置');
      output.push(`  ${this.backupManager.config.output.path}`);
      output.push('');
      
      // 当前配置
      output.push('⚙️ 当前配置');
      output.push(`  - 备份模式：${status.config.mode === 'full' ? '全量备份' : '选择性备份'}`);
      output.push(`  - 保留策略：${status.config.retention.mode === 'days' ? `${status.config.retention.days} 天` : `${status.config.retention.count} 份`}`);
      
      // 通知配置
      const notification = config.notification;
      const channels = notification.channels || [];
      const targets = notification.targets || {};
      
      let notificationInfo = channels.map(ch => {
        const t = targets[ch] || [];
        if (t.length > 0) {
          return `${ch}(${t.length}个目标)`;
        }
        return ch;
      }).join(', ') || '未配置';
      
      output.push(`  - 通知渠道：${notificationInfo}`);
      
      return this.outputSuccess(output.join('\n'), status);
    } catch (err) {
      return this.outputError(`获取状态失败: ${err.message}`);
    }
  }

  /**
   * /backup_config - 配置向导
   */
  async cmdBackupConfig(args) {
    const output = [];
    
    try {
      // 检查配置文件是否存在
      const exists = await configExists();
      
      if (args.mode === 'show') {
        // 显示当前配置
        const config = await loadConfig();
        output.push('📋 当前配置');
        output.push('━'.repeat(40));
        output.push('');
        output.push('```json');
        output.push(JSON.stringify(config, null, 2));
        output.push('```');
        output.push('');
        output.push(`📁 配置文件：${getConfigPaths().configFile}`);
        
        return this.outputSuccess(output.join('\n'), { config });
      }
      
      if (args.mode === 'reset') {
        // 重置配置
        await resetConfig();
        output.push('✅ 配置已重置为默认值');
        output.push(`📁 配置文件：${getConfigPaths().configFile}`);
        
        return this.outputSuccess(output.join('\n'));
      }
      
      if (args.mode === 'manual') {
        // 手动配置指引
        output.push('📝 手动修改配置文件');
        output.push('━'.repeat(40));
        output.push('');
        output.push('配置文件路径：');
        output.push(`  ${getConfigPaths().configFile}`);
        output.push('');
        output.push('操作步骤：');
        output.push('  1. 使用文本编辑器打开配置文件');
        output.push('  2. 修改需要的配置项');
        output.push('  3. 保存文件');
        output.push('  4. 运行 /backup_config 验证配置');
        output.push('');
        output.push('💡 提示：修改后运行验证确保格式正确');
        
        return this.outputSuccess(output.join('\n'));
      }
      
      if (args.mode === 'interactive' || !args.mode) {
        // 交互式配置 - 返回配置菜单
        output.push('📋 备份配置向导');
        output.push('━'.repeat(40));
        output.push('');
        output.push('请选择配置方式：');
        output.push('');
        output.push('[1] 交互式配置（推荐）');
        output.push('[2] 手动修改配置文件');
        output.push('[3] 重置为默认配置');
        output.push('[4] 查看当前配置');
        output.push('');
        output.push('请输入选项编号或具体配置项，例如：');
        output.push('  - backup_config 1  （选择交互式配置）');
        output.push('  - backup_config mode=partial  （设置备份模式）');
        output.push('  - backup_config time=03:00  （设置执行时间）');
        output.push('  - backup_config days=30  （设置保留天数）');
        
        return this.outputSuccess(output.join('\n'));
      }
      
      // 快捷配置
      if (args.mode === 'set' && args.key && args.value !== undefined) {
        const config = await loadConfig();
        
        // 根据键更新配置
        switch (args.key) {
          case 'mode':
            config.backup.mode = args.value;
            break;
          case 'time':
            const [hour, minute] = args.value.split(':').map(Number);
            config.schedule.cron = `${minute || 0} ${hour || 3} * * *`;
            break;
          case 'days':
            config.retention.mode = 'days';
            config.retention.days = parseInt(args.value);
            break;
          case 'count':
            config.retention.mode = 'count';
            config.retention.count = parseInt(args.value);
            break;
          default:
            return this.outputError(`未知的配置项: ${args.key}`);
        }
        
        await saveConfig(config);
        output.push(`✅ 已更新配置：${args.key} = ${args.value}`);
        
        return this.outputSuccess(output.join('\n'), { config });
      }
      
      // 选项式配置
      if (args.option) {
        switch (args.option) {
          case '1':
            // 交互式配置的详细步骤
            return this.interactiveConfig();
          
          case '2':
            return this.cmdBackupConfig({ mode: 'manual' });
          
          case '3':
            return this.cmdBackupConfig({ mode: 'reset' });
          
          case '4':
            return this.cmdBackupConfig({ mode: 'show' });
          
          default:
            return this.outputError(`无效的选项: ${args.option}`);
        }
      }
      
    } catch (err) {
      return this.outputError(`配置失败: ${err.message}`);
    }
  }

  /**
   * 交互式配置
   */
  async interactiveConfig() {
    const output = [];

    output.push('📋 交互式配置向导');
    output.push('━'.repeat(40));
    output.push('');
    output.push('Step 1/8: 备份范围');
    output.push('  [1] 全量备份 .openclaw');
    output.push('  [2] 选择性备份');
    output.push('');
    output.push('请回复选项编号继续配置：');

    // 注意：这是一个交互式的开始，需要用户响应后继续
    // 实际实现中，这里会保存状态并等待用户下一步输入

    return this.outputSuccess(output.join('\n'), {
      step: 1,
      total: 8,
      type: 'interactive'
    });
  }

  /**
   * 处理交互式配置步骤
   * @param {number} step 当前步骤
   * @param {string} input 用户输入
   * @param {object} state 配置状态
   */
  async handleInteractiveStep(step, input, state = {}) {
    const output = [];
    
    switch (step) {
      case 1: // 备份范围
        if (input === '1') {
          // 全量备份 - 直接进入下一步
          state.mode = 'full';
          return this.askBackupTime(state);
        } else if (input === '2') {
          // 选择性备份 - 进入文件选择流程
          state.mode = 'partial';
          return this.askBackupFiles(state);
        } else {
          return this.outputError('请输入 1 或 2');
        }
        
      // ===== 选择性备份文件选择流程 =====
      case 1.1: // 文件选择输入
        return this.handleFileSelection(input, state);
        
      case 1.2: // 确认选择
        return this.handleFileConfirm(input, state);
        
      case 2: // 备份时间
        if (input.toLowerCase() === 'y') {
          output.push('Step 2/8: 备份时间');
          output.push('━'.repeat(40));
          output.push('');
          output.push('请输入执行时间（格式：HH:MM，如 03:00）：');
          output.push('');
          output.push('请直接回复时间：');

          return this.outputSuccess(output.join('\n'), { step: 2.1, total: 8, state, type: 'interactive' });
        }

        // 继续下一步
        state.time = '03:00';
        return this.askStoragePath(state);

      case 2.1: // 输入具体时间
        const timeMatch = input.match(/^(\d{1,2}):(\d{2})$/);
        if (!timeMatch) {
          return this.outputError('时间格式无效，请使用 HH:MM 格式（如 03:00）');
        }
        state.time = input;
        return this.askStoragePath(state);

      case 3: // 存储路径选择
        if (input.toLowerCase() === 'y') {
          output.push('Step 3/8: 存储路径');
          output.push('━'.repeat(40));
          output.push('');
          output.push('请输入新的备份存储路径：');
          output.push('');
          output.push('示例格式：');
          output.push('  D:\\Backups\\openclaw');
          output.push('  /home/user/backups');
          output.push('');
          output.push('请直接回复路径，或回复 c 取消：');

          return this.outputSuccess(output.join('\n'), { step: 3.1, total: 8, state, type: 'interactive' });
        }

        // 使用默认路径
        state.outputPath = null;
        return this.askRetention(state);
        
      case 3.1: // 输入具体路径
        if (input.toLowerCase() === 'c') {
          return this.askStoragePath(state);
        }
        state.outputPath = input;
        return this.askRetention(state);
        
      case 4: // 保留策略选择
        if (input === '1') {
          state.retentionMode = 'days';
          output.push('Step 4/8: 保留策略');
          output.push('━'.repeat(40));
          output.push('');
          output.push('请输入保留天数（默认 30 天）：');
          output.push('');
          output.push('请直接回复数字，或回复 d 使用默认值：');

          return this.outputSuccess(output.join('\n'), { step: 4.1, total: 8, state, type: 'interactive' });
        } else if (input === '2') {
          state.retentionMode = 'count';
          output.push('Step 4/8: 保留策略');
          output.push('━'.repeat(40));
          output.push('');
          output.push('请输入保留份数（默认 10 份）：');
          output.push('');
          output.push('建议范围: 5 - 30 份');
          output.push('');
          output.push('请直接回复数字，或回复 d 使用默认值：');

          return this.outputSuccess(output.join('\n'), { step: 4.2, total: 8, state, type: 'interactive' });
        }
        return this.outputError('请输入 1 或 2');
        
      case 4.1: // 按天数
        if (input.toLowerCase() === 'd') {
          state.retentionValue = 30;
        } else {
          const days = parseInt(input);
          if (isNaN(days) || days < 1) {
            return this.outputError('请输入有效的天数（大于 0 的数字）');
          }
          state.retentionValue = days;
        }
        return this.askNotificationChannel(state);
        
      case 4.2: // 按份数
        if (input.toLowerCase() === 'd') {
          state.retentionValue = 10;
        } else {
          const count = parseInt(input);
          if (isNaN(count) || count < 1) {
            return this.outputError('请输入有效的份数（大于 0 的数字）');
          }
          state.retentionValue = count;
        }
        return this.askNotificationChannel(state);
        
      case 5: // 选择通知渠道
        const selectedChannels = input.split(/\s+/).filter(s => s);
        const channelMap = { '1': 'feishu', '2': 'telegram', '3': 'discord', '4': 'slack' };
        
        state.selectedChannels = selectedChannels.map(c => channelMap[c]).filter(c => c);
        
        if (state.selectedChannels.length === 0) {
          return this.outputError('请至少选择一个渠道');
        }
        
        // 开始配置每个渠道的推送目标
        state.channelIndex = 0;
        return this.askChannelTargets(state);
        
      case 6: // 选择推送目标
        const selectedTargets = input.split(/\s+/).filter(s => s);
        const currentChannel = state.selectedChannels[state.channelIndex];

        if (selectedTargets.length > 0 && state.availableTargets) {
          state.targets = state.targets || {};
          state.targets[currentChannel] = selectedTargets.map(idx =>
            state.availableTargets[parseInt(idx) - 1]
          ).filter(t => t);
        }

        state.channelIndex++;

        if (state.channelIndex < state.selectedChannels.length) {
          return this.askChannelTargets(state);
        }

        // 所有渠道配置完成，进入敏感文件配置
        return this.askSensitiveFilesConfig(state);

      case 7:  // 敏感文件排除配置
        return this.handleSensitiveExcludeInput(input, state);

      case 7.1:  // 手动配置确认
        return this.handleManualConfigConfirm(input, state);

      case 8:  // ZIP加密配置
        return this.handleEncryptionInput(input, state);

      case 8.1:  // 密码输入
        return this.handlePasswordInput(input, state);

      case 8.2:  // 随机密码确认
        return this.handleRandomPasswordConfirm(input, state);

      case 8.3:  // 密码确认
        return this.handlePasswordConfirm(input, state);

      default:
        return this.outputError('未知步骤');
    }
  }

  /**
   * 询问备份时间
   */
  async askBackupTime(state) {
    const output = [];

    output.push('Step 2/8: 备份时间');
    output.push('━'.repeat(40));
    output.push('');
    output.push('当前设置: 每天凌晨 3:00');
    output.push('');
    output.push('是否修改执行时间？');
    output.push('  [y] 是，修改时间');
    output.push('  [n] 否，保持默认');
    output.push('');
    output.push('请回复 y 或 n：');

    return this.outputSuccess(output.join('\n'), { step: 2, total: 8, state, type: 'interactive' });
  }

  /**
   * 询问选择性备份文件（新增）
   * 列出 ~/.openclaw/ 目录下的文件和文件夹供用户选择
   */
  async askBackupFiles(state) {
    const output = [];

    output.push('Step 1/8: 选择备份文件');
    output.push('━'.repeat(40));
    output.push('');
    output.push('正在读取 ~/.openclaw/ 目录...');
    output.push('');

    try {
      // 读取 OpenClaw 根目录下的文件和文件夹
      const openclawRoot = OPENCLAW_ROOT;
      const entries = await fs.readdir(openclawRoot, { withFileTypes: true });

      // 排除默认不需要备份的目录
      const excludeDefault = ['logs', 'cache', 'tmp', 'node_modules', 'completions', 'delivery-queue', 'exec-approvals.json'];

      // 过滤并分类
      const folders = [];
      const files = [];

      for (const entry of entries) {
        if (excludeDefault.includes(entry.name)) continue;
        if (entry.name.startsWith('.')) continue; // 隐藏文件跳过

        if (entry.isDirectory()) {
          folders.push({
            name: entry.name,
            type: 'folder',
            selected: false
          });
        } else if (entry.isFile()) {
          files.push({
            name: entry.name,
            type: 'file',
            selected: false
          });
        }
      }

      // 排序
      folders.sort((a, b) => a.name.localeCompare(b.name));
      files.sort((a, b) => a.name.localeCompare(b.name));

      // 保存到 state
      state.availableFiles = [...folders, ...files];

      if (state.availableFiles.length === 0) {
        output.push('⚠️ 未找到可备份的文件或文件夹');
        output.push('');
        output.push('请检查 ~/.openclaw/ 目录是否存在');
        output.push('');
        output.push('按任意键返回上一步...');
        return this.outputSuccess(output.join('\n'), { step: 1, total: 8, state, type: 'interactive' });
      }

      output.push('📋 文件列表（目录 + 文件）：');
      output.push('');
      output.push('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

      // 显示文件夹
      if (folders.length > 0) {
        output.push('');
        output.push('📁 文件夹：');
        folders.forEach((item, idx) => {
          output.push(`  [${idx + 1}] [ ] 📁 ${item.name}`);
        });
      }

      // 显示文件
      if (files.length > 0) {
        output.push('');
        output.push('📄 文件：');
        files.forEach((item, idx) => {
          const fileIdx = folders.length + idx + 1;
          output.push(`  [${fileIdx}] [ ] 📄 ${item.name}`);
        });
      }

      output.push('');
      output.push('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      output.push('');
      output.push('📝 选择说明：');
      output.push('');
      output.push('  选择样式：输入编号，用空格分隔，如：1 3 5 7');
      output.push('  示例：选择第 1、3、5 项 → 输入 1 3 5');
      output.push('');
      output.push('  已选择后会显示：[×] 或 [√]');
      output.push('');
      output.push('请输入要备份的文件/文件夹编号：');

      return this.outputSuccess(output.join('\n'), { step: 1.1, total: 8, state, type: 'interactive' });

    } catch (err) {
      output.push(`❌ 读取目录失败: ${err.message}`);
      output.push('');
      output.push('按任意键返回上一步...');
      return this.outputSuccess(output.join('\n'), { step: 1, total: 8, state, type: 'interactive' });
    }
  }

  /**
   * 处理文件选择输入（新增）
   */
  async handleFileSelection(input, state) {
    const output = [];

    // 解析用户输入的编号
    const selectedIndices = input.split(/\s+/)
      .map(s => parseInt(s.trim()))
      .filter(n => !isNaN(n) && n > 0 && n <= state.availableFiles.length);

    if (selectedIndices.length === 0) {
      return this.outputError('请输入有效的编号（如：1 3 5）');
    }

    // 更新选择状态
    state.selectedFiles = selectedIndices.map(idx => state.availableFiles[idx - 1]);

    // 显示确认界面
    output.push('Step 1/8: 确认选择');
    output.push('━'.repeat(40));
    output.push('');
    output.push('您已选择以下文件/文件夹：');
    output.push('');
    output.push('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

    state.selectedFiles.forEach((item, idx) => {
      const icon = item.type === 'folder' ? '📁' : '📄';
      output.push(`  [√] ${icon} ${item.name}`);
    });

    output.push('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    output.push('');
    output.push(`共选择 ${state.selectedFiles.length} 项`);
    output.push('');
    output.push('请确认选择：');
    output.push('  [1] 确认，继续配置');
    output.push('  [2] 取消，重新选择');
    output.push('');
    output.push('请回复 1 或 2：');

    return this.outputSuccess(output.join('\n'), { step: 1.2, total: 8, state, type: 'interactive' });
  }

  /**
   * 处理文件确认（新增）
   */
  async handleFileConfirm(input, state) {
    const output = [];
    
    if (input === '1') {
      // 确认选择 - 进入下一步
      // 将选择的文件名保存到 state.targets
      state.backupTargets = state.selectedFiles.map(f => f.name);
      return this.askBackupTime(state);
      
    } else if (input === '2') {
      // 重新选择 - 返回文件列表
      state.selectedFiles = [];
      return this.askBackupFiles(state);
      
    } else {
      return this.outputError('请输入 1 或 2');
    }
  }

  /**
   * 询问存储路径
   */
  async askStoragePath(state) {
    const output = [];

    output.push('Step 3/8: 存储路径');
    output.push('━'.repeat(40));
    output.push('');
    output.push('当前设置: ');
    output.push('  ~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backups');
    output.push('');
    output.push('是否修改存储路径？');
    output.push('  [y] 是，修改路径');
    output.push('  [n] 否，保持默认');
    output.push('');
    output.push('请回复 y 或 n：');

    return this.outputSuccess(output.join('\n'), { step: 3, total: 8, state, type: 'interactive' });
  }

  /**
   * 询问保留策略
   */
  async askRetention(state) {
    const output = [];

    output.push('Step 4/8: 保留策略');
    output.push('━'.repeat(40));
    output.push('');
    output.push('请选择清理模式：');
    output.push('');
    output.push('[1] 按天数保留');
    output.push('    保留最近 N 天的备份（默认 30 天）');
    output.push('');
    output.push('[2] 按份数保留');
    output.push('    保留最近 N 份备份（默认 10 份）');
    output.push('');
    output.push('请回复选项编号：');

    return this.outputSuccess(output.join('\n'), { step: 4, total: 8, state, type: 'interactive' });
  }

  /**
   * 询问通知渠道
   */
  async askNotificationChannel(state) {
    const output = [];

    // 加载 OpenClaw 配置
    const openclawConfig = await loadOpenClawConfig();

    output.push('Step 5/8: 通知渠道');
    output.push('━'.repeat(40));
    output.push('');
    output.push('正在检测 OpenClaw 已配置的渠道...');
    output.push('');

    // 显示可用渠道
    const channels = [];
    if (openclawConfig.channels.feishu?.enabled) {
      channels.push({ key: '1', name: 'feishu', label: '飞书' });
    }
    if (openclawConfig.channels.telegram?.enabled) {
      channels.push({ key: '2', name: 'telegram', label: 'Telegram' });
    }
    if (openclawConfig.channels.discord?.enabled) {
      channels.push({ key: '3', name: 'discord', label: 'Discord' });
    }
    if (openclawConfig.channels.slack?.enabled) {
      channels.push({ key: '4', name: 'slack', label: 'Slack' });
    }

    if (channels.length === 0) {
      output.push('⚠️ 未检测到已配置的渠道');
      output.push('');
      output.push('请先在 OpenClaw 中配置至少一个通信渠道。');
      output.push('配置文件位置：~/.openclaw/openclaw.json');
      output.push('');
      output.push('配置完成后，运行 /backup_config 重新配置通知。');

      // 跳过通知配置，直接保存
      state.selectedChannels = [];
      return this.saveInteractiveConfig(state);
    }

    output.push('✅ 已检测到可用渠道：');
    output.push('');
    channels.forEach(ch => {
      output.push(`  [${ch.key}] ${ch.name} - ${ch.label}`);
    });
    output.push('');
    output.push('请选择要启用的通知渠道（输入编号，可多选，如：1 2）：');

    return this.outputSuccess(output.join('\n'), { step: 5, total: 8, state, type: 'interactive' });
  }

  /**
   * 询问渠道推送目标
   */
  async askChannelTargets(state) {
    const output = [];
    const channel = state.selectedChannels[state.channelIndex];
    const channelNames = { feishu: '飞书', telegram: 'Telegram', discord: 'Discord', slack: 'Slack' };

    output.push(`Step 6/8: 配置 ${channelNames[channel]} 推送目标`);
    output.push('━'.repeat(40));
    output.push('');

    // 加载可用目标
    const openclawConfig = await loadOpenClawConfig();
    const targets = getChannelTargets(channel, openclawConfig);

    if (targets.length === 0) {
      output.push(`⚠️ 未检测到 ${channelNames[channel]} 的可用推送目标`);
      output.push('');
      output.push('可能原因：');
      output.push('  - OpenClaw 未绑定任何群组或用户');
      output.push('  - 渠道配置不完整');
      output.push('');
      output.push('将跳过此渠道的推送目标配置。');
      output.push('');
      output.push('请回复任意键继续：');

      state.availableTargets = [];
    } else {
      output.push(`${channelNames[channel]} 推送目标列表：`);
      output.push('');

      targets.forEach((t, idx) => {
        const icon = t.type === 'group' ? '📢' : '👤';
        output.push(`  [${idx + 1}] ${icon} ${t.name || t.id}（${t.type === 'group' ? '群组' : '用户'}）`);
      });

      output.push('');
      output.push('请选择推送目标（输入编号，可多选，如：1 2 3）：');

      state.availableTargets = targets;
    }

    return this.outputSuccess(output.join('\n'), { step: 6, total: 8, state, type: 'interactive' });
  }

  /**
   * Step 7/8: 敏感文件排除配置（新增）
   */
  async askSensitiveFilesConfig(state) {
    const output = [];

    output.push('Step 7/8: 敏感文件排除配置');
    output.push('━'.repeat(40));
    output.push('');
    output.push('⚠️ 安全提醒：');
    output.push('');
    output.push('您的备份可能包含以下敏感文件：');
    output.push('');
    output.push('📁 敏感目录（可能包含密钥、凭证）：');
    output.push('  - .ssh, .gnupg（SSH密钥）');
    output.push('  - credentials, secrets（凭证目录）');
    output.push('');
    output.push('📄 敏感文件（可能包含Token、密钥）：');
    output.push('  - *.key, *.pem, *.p12, *.pfx（密钥文件）');
    output.push('  - .env, .env.local（环境变量）');
    output.push('  - credentials.json, secrets.json（凭证文件）');
    output.push('  - *_token.json, *_key.json（敏感配置）');
    output.push('');
    output.push('💡 风险说明：');
    output.push('  如果备份中包含敏感文件，可能导致：');
    output.push('  - API Token泄露');
    output.push('  - 密钥文件泄露');
    output.push('  - 环境变量泄露');
    output.push('  - 用户隐私数据泄露');
    output.push('');
    output.push('是否启用敏感文件排除？');
    output.push('  [1] 启用排除 - 添加敏感文件到排除列表');
    output.push('  [2] 不启用 - 保持当前排除列表（仅排除临时文件）');
    output.push('  [3] 自定义 - 手动编辑排除列表');
    output.push('');
    output.push('请回复选项编号：');

    return this.outputSuccess(output.join('\n'), {
      step: 7,
      total: 8,
      state,
      type: 'interactive'
    });
  }

  /**
   * 处理敏感文件排除输入（新增）
   */
  async handleSensitiveExcludeInput(input, state) {
    const output = [];
    const { loadConfig } = require('./config');

    if (input === '1') {
      // 启用排除 - 添加敏感文件到排除列表
      state.enableSensitiveExclude = true;

      // 加载默认配置获取建议列表
      const config = await loadConfig();

      // 将建议的敏感文件添加到排除列表
      state.excludePatterns = [
        ...config.backup.excludePatterns,
        ...config.backup.sensitiveExcludeSuggestion
      ];
      state.exclude = [
        ...config.backup.exclude,
        ...config.backup.sensitiveExcludeDirectories
      ];

      output.push('✅ 已启用敏感文件排除');
      output.push('');
      output.push('排除列表已更新：');
      output.push(`  - 目录：${state.exclude.length} 个`);
      output.push(`  - 文件模式：${state.excludePatterns.length} 个`);
      output.push('');
      output.push('继续下一步加密配置...');

      return this.outputSuccess(output.join('\n'), {
        step: 7,
        total: 8,
        state,
        type: 'interactive'
      });

    } else if (input === '2') {
      // 不启用 - 保持默认
      state.enableSensitiveExclude = false;

      output.push('已选择不启用敏感文件排除');
      output.push('');
      output.push('当前排除列表仅包含临时文件：');
      output.push('  - logs, cache, tmp, node_modules');
      output.push('  - *.log, *.tmp, .DS_Store, Thumbs.db');
      output.push('');
      output.push('继续下一步加密配置...');

      return this.outputSuccess(output.join('\n'), {
        step: 7,
        total: 8,
        state,
        type: 'interactive'
      });

    } else if (input === '3') {
      // 自定义 - 显示手动编辑说明
      output.push('📝 手动编辑排除列表');
      output.push('━'.repeat(40));
      output.push('');
      output.push('配置文件位置：');
      output.push(`  ${getConfigPaths().configFile}`);
      output.push('');
      output.push('编辑方法：');
      output.push('  1. 打开config.json文件');
      output.push('  2. 编辑 backup.exclude 或 backup.excludePatterns');
      output.push('  3. 添加需要排除的文件模式');
      output.push('');
      output.push('示例：');
      output.push('  "exclude": ["logs", "cache", "*.key"]');
      output.push('  "excludePatterns": ["*.pem", ".env", "credentials.json"]');
      output.push('');
      output.push('请回复 c 继续配置：');

      state.enableSensitiveExclude = false;
      state.manualConfig = true;

      return this.outputSuccess(output.join('\n'), {
        step: 7.1,
        total: 8,
        state,
        type: 'interactive'
      });

    } else {
      return this.outputError('请输入 1、2 或 3');
    }
  }

  /**
   * 处理手动配置确认（新增）
   */
  async handleManualConfigConfirm(input, state) {
    if (input.toLowerCase() === 'c') {
      return this.askEncryptionConfig(state);
    } else {
      return this.outputError('请回复 c 继续配置');
    }
  }

  /**
   * Step 8/8: ZIP加密配置（新增）
   */
  async askEncryptionConfig(state) {
    const output = [];

    output.push('Step 8/8: ZIP加密配置');
    output.push('━'.repeat(40));
    output.push('');
    output.push('是否启用ZIP加密功能？');
    output.push('');
    output.push('  [1] 启用加密 - 使用密码保护备份文件');
    output.push('  [2] 不启用加密 - 备份文件不加密（默认）');
    output.push('');
    output.push('请回复选项编号：');

    return this.outputSuccess(output.join('\n'), {
      step: 8,
      total: 8,
      state,
      type: 'interactive'
    });
  }

  /**
   * 处理加密配置输入（新增）
   */
  async handleEncryptionInput(input, state) {
    const output = [];

    if (input === '1') {
      // 启用加密 - 显示加密提醒
      output.push('⚠️ 重要提醒：ZIP加密功能使用须知');
      output.push('━'.repeat(40));
      output.push('');
      output.push('加密方式：AES-256加密算法');
      output.push('密码存储：存储在config.json配置文件中');
      output.push('');
      output.push('解密兼容性说明：');
      output.push('  ✅ 支持工具：7-Zip、WinRAR、PeaZip');
      output.push('  ❌ 不支持工具：');
      output.push('     - macOS Finder原生解压');
      output.push('     - Windows资源管理器原生解压');
      output.push('     - Linux unzip命令（部分版本）');
      output.push('');
      output.push('解密方法：');
      output.push('  Windows: 右键文件 → 7-Zip → 解压 → 输入密码');
      output.push('  macOS: 打开7-Zip或WinRAR → 选择文件 → 解压 → 输入密码');
      output.push('  Linux: 7z x backup.zip -p密码');
      output.push('');
      output.push('⚠️ 重要风险提示：');
      output.push('  1. 密码丢失将无法解密备份文件');
      output.push('  2. config.json文件损坏或丢失将无法找回密码');
      output.push('  3. 建议将密码备份到安全位置（如密码管理器）');
      output.push('  4. 密码存储在本地配置文件，需妥善保护config.json');
      output.push('');
      output.push('请设置加密密码：');
      output.push('  输入密码（至少8位，建议包含字母+数字+符号）：');
      output.push('  或输入 \'d\' 使用默认随机密码（系统将生成并显示）');
      output.push('');
      output.push('请直接回复：');

      state.encryptionEnabled = true;
      return this.outputSuccess(output.join('\n'), {
        step: 8.1,
        total: 8,
        state,
        type: 'interactive'
      });

    } else if (input === '2') {
      // 不启用加密
      state.encryptionEnabled = false;
      return this.saveInteractiveConfig(state);  // 直接保存配置

    } else {
      return this.outputError('请输入 1 或 2');
    }
  }

  /**
   * 处理密码输入（新增）
   */
  async handlePasswordInput(input, state) {
    const output = [];

    if (input.toLowerCase() === 'd') {
      // 使用随机密码
      const randomPassword = this.generateRandomPassword();

      output.push('系统已生成随机密码：');
      output.push('━'.repeat(40));
      output.push('');
      output.push(`  密码：${randomPassword}`);
      output.push('');
      output.push('⚠️ 请务必记录此密码！');
      output.push('建议：复制密码并保存到安全位置（如密码管理器）。');
      output.push('');
      output.push('密码丢失风险：');
      output.push('  - 无法解密备份文件');
      output.push('  - 数据将永久无法访问');
      output.push('');
      output.push('请确认已记录密码后继续：');
      output.push('  回复 \'c\' 确认已记录：');

      state.encryptionPassword = randomPassword;
      return this.outputSuccess(output.join('\n'), {
        step: 8.2,
        total: 8,
        state,
        type: 'interactive'
      });

    } else if (input.length >= 8) {
      // 用户自定义密码
      output.push('密码已设置：' + input);
      output.push('');
      output.push('⚠️ 请务必妥善保存密码！');
      output.push('建议：将密码记录到密码管理器或其他安全位置。');
      output.push('');
      output.push('密码丢失风险：');
      output.push('  - 无法解密备份文件');
      output.push('  - 数据将永久无法访问');
      output.push('');
      output.push('请确认密码设置：');
      output.push('  [1] 确认，保存配置');
      output.push('  [2] 重新设置密码');
      output.push('  [3] 取消加密功能');
      output.push('');
      output.push('请回复选项编号：');

      state.encryptionPassword = input;
      return this.outputSuccess(output.join('\n'), {
        step: 8.3,
        total: 8,
        state,
        type: 'interactive'
      });

    } else {
      return this.outputError('密码长度至少8位，请重新输入');
    }
  }

  /**
   * 生成随机密码（新增）
   */
  generateRandomPassword() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#$@%&';
    let password = '';
    for (let i = 0; i < 16; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return password;
  }

  /**
   * 处理密码确认（新增）
   */
  async handlePasswordConfirm(input, state) {
    if (input === '1') {
      // 确认密码，保存配置
      return this.saveInteractiveConfig(state);

    } else if (input === '2') {
      // 重新设置密码
      return this.handleEncryptionInput('1', state);

    } else if (input === '3') {
      // 取消加密功能
      state.encryptionEnabled = false;
      return this.saveInteractiveConfig(state);

    } else {
      return this.outputError('请输入 1、2 或 3');
    }
  }

  /**
   * 处理随机密码确认（新增）
   */
  async handleRandomPasswordConfirm(input, state) {
    if (input.toLowerCase() === 'c') {
      // 确认已记录，保存配置
      return this.saveInteractiveConfig(state);
    } else {
      return this.outputError('请回复 c 确认已记录密码');
    }
  }

  /**
   * 保存交互式配置
   */
  async saveInteractiveConfig(state) {
    const output = [];

    try {
      const config = await loadConfig();

      // 更新配置
      if (state.mode) {
        config.backup.mode = state.mode;
      }

      // 保存选择性备份的目标文件（新增）
      if (state.mode === 'partial' && state.backupTargets) {
        config.backup.targets = state.backupTargets;
      }

      if (state.time) {
        const [hour, minute] = state.time.split(':').map(Number);
        config.schedule.cron = `${minute || 0} ${hour || 3} * * *`;
      }

      if (state.outputPath) {
        config.output.path = state.outputPath;
      }

      if (state.retentionMode && state.retentionValue) {
        config.retention.mode = state.retentionMode;
        if (state.retentionMode === 'days') {
          config.retention.days = state.retentionValue;
        } else {
          config.retention.count = state.retentionValue;
        }
      }

      if (state.selectedChannels) {
        config.notification.channels = state.selectedChannels;
      }

      if (state.targets) {
        config.notification.targets = state.targets;
      }

      // 新增：敏感文件排除配置保存
      if (state.enableSensitiveExclude !== undefined) {
        config.backup.enableSensitiveExclude = state.enableSensitiveExclude;
      }

      if (state.excludePatterns) {
        config.backup.excludePatterns = state.excludePatterns;
      }

      if (state.exclude) {
        config.backup.exclude = state.exclude;
      }

      // 新增：加密配置保存
      if (state.encryptionEnabled !== undefined) {
        // 确保output.encryption配置结构存在
        if (!config.output.encryption) {
          config.output.encryption = {
            enabled: false,
            password: null,
            algorithm: "aes-256",
            reminderShown: false
          };
        }
        config.output.encryption.enabled = state.encryptionEnabled;
      }

      if (state.encryptionPassword) {
        // 确保output.encryption配置结构存在
        if (!config.output.encryption) {
          config.output.encryption = {
            enabled: false,
            password: null,
            algorithm: "aes-256",
            reminderShown: false
          };
        }
        config.output.encryption.password = state.encryptionPassword;
      }

      await saveConfig(config);

      output.push('✅ 配置完成！');
      output.push('━'.repeat(40));
      output.push('');

      // 显示配置摘要
      if (state.mode) {
        if (state.mode === 'full') {
          output.push('备份范围: 全量备份');
        } else {
          output.push('备份范围: 选择性备份');
          if (state.backupTargets && state.backupTargets.length > 0) {
            output.push('');
            output.push('已选项目标：');
            state.backupTargets.forEach(t => {
              output.push(`  - ${t}`);
            });
          }
        }
      }

      if (state.enableSensitiveExclude) {
        output.push('敏感文件排除: 已启用');
      } else {
        output.push('敏感文件排除: 未启用（仅排除临时文件）');
      }

      if (state.encryptionEnabled) {
        output.push('ZIP加密: 已启用');
        if (state.encryptionPassword) {
          output.push(`密码: ${state.encryptionPassword.substring(0, 3)}***（已设置）`);
        }
      } else {
        output.push('ZIP加密: 未启用');
      }

      if (state.time) {
        output.push(`执行时间: 每天 ${state.time}`);
      }

      if (state.outputPath) {
        output.push(`存储路径: ${state.outputPath}`);
      }

      if (state.retentionMode && state.retentionValue) {
        output.push(`保留策略: ${state.retentionMode === 'days' ? `${state.retentionValue} 天` : `${state.retentionValue} 份`}`);
      }

      if (state.selectedChannels && state.selectedChannels.length > 0) {
        const channelNames = { feishu: '飞书', telegram: 'Telegram', discord: 'Discord', slack: 'Slack' };
        const channelInfo = state.selectedChannels.map(c => channelNames[c]).join('、');
        output.push(`通知渠道: ${channelInfo}`);
      }

      output.push('');
      output.push(`📁 配置文件: ${getConfigPaths().configFile}`);
      output.push('');
      output.push('💡 可用命令:');
      output.push('  /backup_now     - 立即执行备份');
      output.push('  /backup_status  - 查看备份状态');
      output.push('  /backup_list    - 列出备份文件');

      return this.outputSuccess(output.join('\n'), { config });

    } catch (err) {
      return this.outputError(`保存配置失败: ${err.message}`);
    }
  }

  /**
   * /backup_list - 列出备份文件
   */
  async cmdBackupList(args) {
    const output = [];
    
    try {
      const config = await loadConfig();
      const cleaner = new Cleaner(config);
      const stats = await cleaner.getStats();
      
      output.push('📦 备份文件列表');
      output.push('━'.repeat(60));
      output.push('');
      
      if (stats.count === 0) {
        output.push('暂无备份文件');
        output.push('');
        output.push(`📁 存储目录：${config.output.path}`);
        
        return this.outputSuccess(output.join('\n'), stats);
      }
      
      output.push('#    文件名                                          大小');
      output.push('─'.repeat(60));
      
      const files = args.all ? stats.files : stats.files.slice(0, 10);
      
      files.forEach((file, index) => {
        const num = String(index + 1).padStart(2, '0');
        const name = file.name.length > 40 ? file.name.substring(0, 37) + '...' : file.name;
        output.push(`${num}   ${name.padEnd(45)} ${file.size}`);
      });
      
      output.push('');
      output.push(`共 ${stats.count} 个备份文件，总计 ${stats.totalSize}`);
      
      if (stats.count > 10 && !args.all) {
        output.push('');
        output.push('💡 使用 --all 查看全部备份文件');
      }
      
      return this.outputSuccess(output.join('\n'), stats);
    } catch (err) {
      return this.outputError(`获取备份列表失败: ${err.message}`);
    }
  }

  /**
   * /backup_clean - 清理旧备份
   */
  async cmdBackupClean(args) {
    const output = [];
    
    try {
      const config = await loadConfig();
      const cleaner = new Cleaner(config);
      
      // 预览模式
      if (args.preview || args.dryRun) {
        const preview = await cleaner.getPreview();
        
        output.push('🗑️ 清理预览');
        output.push('━'.repeat(40));
        output.push('');
        output.push(`当前备份数：${preview.total} 个`);
        output.push(`将要删除：${preview.toDeleteCount} 个`);
        output.push(`将会保留：${preview.toKeepCount} 个`);
        
        if (preview.toDeleteCount > 0) {
          output.push('');
          output.push('将要删除的文件：');
          preview.toDeleteFiles.slice(0, 5).forEach(f => {
            output.push(`  - ${f.name} (${f.size})`);
          });
          if (preview.toDeleteFiles.length > 5) {
            output.push(`  ... 还有 ${preview.toDeleteFiles.length - 5} 个`);
          }
        }
        
        output.push('');
        output.push('💡 使用 --confirm 执行实际清理');
        
        return this.outputSuccess(output.join('\n'), preview);
      }
      
      // 执行清理
      const result = await cleaner.execute();
      
      if (result.skipped) {
        output.push('⚠️ 保留策略未启用');
        output.push('请在配置中启用 retention.enabled');
      } else {
        output.push('🗑️ 清理完成');
        output.push('━'.repeat(40));
        output.push('');
        output.push(`✅ 删除：${result.deleted} 个`);
        output.push(`📁 保留：${result.kept} 个`);
      }
      
      return this.outputSuccess(output.join('\n'), result);
    } catch (err) {
      return this.outputError(`清理失败: ${err.message}`);
    }
  }

  /**
   * /help - 帮助
   */
  async cmdHelp() {
    const output = [];
    
    output.push('📖 Auto Backup OpenClaw User Data - 命令帮助');
    output.push('━'.repeat(50));
    output.push('');
    output.push('可用命令：');
    output.push('');
    output.push('/backup_now         立即执行备份');
    output.push('  --full            全量备份（默认）');
    output.push('  --partial         选择性备份');
    output.push('');
    output.push('/backup_status      查看备份状态');
    output.push('');
    output.push('/backup_config      配置向导');
    output.push('  [1]               交互式配置');
    output.push('  [2]               手动配置');
    output.push('  [3]               重置配置');
    output.push('  [4]               查看配置');
    output.push('');
    output.push('/backup_list        列出备份文件');
    output.push('  --all             显示全部');
    output.push('');
    output.push('/backup_clean       清理旧备份');
    output.push('  --preview         预览模式');
    output.push('  --confirm         确认执行');
    output.push('');
    output.push('📁 配置文件：~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/config.json');
    output.push('📋 日志文件：~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log');
    
    return this.outputSuccess(output.join('\n'));
  }

  /**
   * 格式化成功输出
   */
  outputSuccess(message, data = null) {
    return {
      success: true,
      message,
      data
    };
  }

  /**
   * 格式化错误输出
   */
  outputError(message) {
    return {
      success: false,
      message,
      error: message
    };
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
}

/**
 * 创建 CLI 实例并执行命令
 */
async function runCommand(command, args = {}) {
  const cli = new CLI();
  return cli.execute(command, args);
}

module.exports = {
  CLI,
  runCommand
};