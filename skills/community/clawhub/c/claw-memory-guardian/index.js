#!/usr/bin/env node

/**
 * Claw Memory Guardian - 主入口文件
 * 防丢失记忆系统的核心实现
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const { format } = require('date-fns');
const simpleGit = require('simple-git');

class MemoryGuardian {
  constructor() {
    this.workspacePath = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
    this.memoryPath = path.join(this.workspacePath, 'memory');
    this.config = this.loadConfig();
    this.git = simpleGit(this.workspacePath);
  }

  loadConfig() {
    const configPath = path.join(this.workspacePath, 'config.json');
    try {
      const config = fs.readJsonSync(configPath);
      return config.memoryGuardian || {
        autoSaveInterval: 300,
        autoCommitInterval: 1800,
        backupRetention: 7,
        enableSemanticSearch: true,
        enableTimeline: true
      };
    } catch (error) {
      return {
        autoSaveInterval: 300,
        autoCommitInterval: 1800,
        backupRetention: 7,
        enableSemanticSearch: true,
        enableTimeline: true
      };
    }
  }

  async init() {
    console.log(chalk.blue('🧠 初始化记忆守护者系统...'));
    
    // 创建记忆目录结构
    const dirs = [
      this.memoryPath,
      path.join(this.memoryPath, 'backup'),
      path.join(this.memoryPath, 'knowledge_base')
    ];

    for (const dir of dirs) {
      await fs.ensureDir(dir);
      console.log(chalk.green(`✅ 创建目录: ${path.relative(this.workspacePath, dir)}`));
    }

    // 创建基础记忆文件
    const files = {
      'MEMORY.md': '# MEMORY.md - 长期记忆\n\n## 欢迎使用记忆守护者系统\n\n这是你的长期记忆文件，记录重要决策、学习经验和核心知识。\n\n## 记忆系统原则\n1. **实时保存** - 每完成重要步骤立即保存\n2. **多重备份** - 本地 + git版本控制\n3. **自动索引** - 支持语义搜索，快速定位\n4. **崩溃恢复** - 意外中断后能快速恢复工作\n\n## 使用建议\n- 定期回顾和更新此文件\n- 将重要学习经验记录在此\n- 删除过时或不再相关的信息\n',
      'memory_index.json': JSON.stringify({
        version: '1.0.0',
        created: new Date().toISOString(),
        lastUpdated: new Date().toISOString(),
        fileCount: 0,
        indexStatus: 'pending'
      }, null, 2),
      'project_timeline.json': JSON.stringify({
        version: '1.0.0',
        created: new Date().toISOString(),
        projects: [],
        timeline: []
      }, null, 2)
    };

    for (const [filename, content] of Object.entries(files)) {
      const filePath = path.join(this.memoryPath, filename);
      if (!await fs.pathExists(filePath)) {
        await fs.writeFile(filePath, content);
        console.log(chalk.green(`✅ 创建文件: ${filename}`));
      }
    }

    // 创建今日记忆文件
    await this.createDailyMemoryFile();

    // 初始化git仓库（如果不存在）
    const isRepo = await this.git.checkIsRepo();
    if (!isRepo) {
      console.log(chalk.yellow('⚠️  未检测到git仓库，正在初始化...'));
      await this.git.init();
      await fs.writeFile(path.join(this.workspacePath, '.gitignore'), 'node_modules/\n*.log\n.DS_Store\n');
      await this.git.add('.gitignore');
      await this.git.commit('初始化记忆守护者系统');
      console.log(chalk.green('✅ git仓库初始化完成'));
    }

    // 创建自动保存脚本
    await this.createAutoSaveScript();

    console.log(chalk.bold.green('\n🎉 记忆守护者系统初始化完成！'));
    console.log(chalk.cyan('📁 记忆目录: ') + this.memoryPath);
    console.log(chalk.cyan('⏰ 自动保存: ') + `每${this.config.autoSaveInterval}秒`);
    console.log(chalk.cyan('🔄 自动提交: ') + `每${this.config.autoCommitInterval}秒`);
    console.log(chalk.cyan('💾 备份保留: ') + `${this.config.backupRetention}天`);
    
    console.log(chalk.yellow('\n🚀 开始使用:'));
    console.log('1. memory-guardian status    # 检查系统状态');
    console.log('2. memory-guardian save      # 手动保存当前状态');
    console.log('3. memory-guardian search    # 搜索记忆内容');
    console.log('4. memory-guardian backup    # 创建完整备份');
  }

  async createDailyMemoryFile() {
    const today = format(new Date(), 'yyyy-MM-dd');
    const dailyFile = path.join(this.memoryPath, `${today}.md`);
    
    if (!await fs.pathExists(dailyFile)) {
      const content = `# ${today}\n\n## 🧠 自动创建的记忆文件\n创建时间: ${new Date().toLocaleString('zh-CN')}\n\n## 📋 今日工作\n\n## 📝 学习记录\n\n## 💡 重要决策\n\n## 🔄 下一步计划\n\n---\n*由记忆守护者系统自动创建*\n`;
      await fs.writeFile(dailyFile, content);
      console.log(chalk.green(`✅ 创建今日记忆文件: ${today}.md`));
    }
  }

  async createAutoSaveScript() {
    const scriptContent = `#!/bin/bash
# 记忆守护者自动保存脚本
# 自动运行于后台，定期保存记忆状态

WORKSPACE="${this.workspacePath}"
MEMORY_DIR="${this.memoryPath}"
LOG_FILE="${path.join(this.memoryPath, 'auto_save.log')}"

echo "[$(date)] 记忆守护者自动保存脚本启动" >> "$LOG_FILE"

while true; do
  # 创建今日记忆文件（如果不存在）
  TODAY=$(date +%Y-%m-%d)
  DAILY_FILE="$MEMORY_DIR/$TODAY.md"
  if [ ! -f "$DAILY_FILE" ]; then
    echo "# $TODAY" > "$DAILY_FILE"
    echo "" >> "$DAILY_FILE"
    echo "## 🧠 自动创建的记忆文件" >> "$DAILY_FILE"
    echo "创建时间: $(date)" >> "$DAILY_FILE"
    echo "" >> "$DAILY_FILE"
    echo "## 📋 今日工作" >> "$DAILY_FILE"
    echo "[$(date)] 创建今日记忆文件: $TODAY.md" >> "$LOG_FILE"
  fi

  # 更新记忆索引时间戳
  INDEX_FILE="$MEMORY_DIR/memory_index.json"
  if [ -f "$INDEX_FILE" ]; then
    jq '.lastUpdated = "$(date -Iseconds)"' "$INDEX_FILE" > "$INDEX_FILE.tmp" && mv "$INDEX_FILE.tmp" "$INDEX_FILE"
  fi

  # 等待下一次保存
  sleep ${this.config.autoSaveInterval}
done
`;

    const scriptPath = path.join(this.memoryPath, 'auto_save.sh');
    await fs.writeFile(scriptPath, scriptContent);
    await fs.chmod(scriptPath, '755');
    
    console.log(chalk.green(`✅ 创建自动保存脚本: ${path.relative(this.workspacePath, scriptPath)}`));
  }

  async status() {
    console.log(chalk.blue('📊 记忆守护者系统状态检查...\n'));

    // 检查目录结构
    const checks = [
      { name: '记忆目录', path: this.memoryPath, type: 'dir' },
      { name: '备份目录', path: path.join(this.memoryPath, 'backup'), type: 'dir' },
      { name: '知识库目录', path: path.join(this.memoryPath, 'knowledge_base'), type: 'dir' },
      { name: '长期记忆文件', path: path.join(this.memoryPath, 'MEMORY.md'), type: 'file' },
      { name: '记忆索引', path: path.join(this.memoryPath, 'memory_index.json'), type: 'file' },
      { name: '项目时间线', path: path.join(this.memoryPath, 'project_timeline.json'), type: 'file' }
    ];

    let allPassed = true;
    for (const check of checks) {
      const exists = check.type === 'dir' ? 
        await fs.pathExists(check.path) && (await fs.stat(check.path)).isDirectory() :
        await fs.pathExists(check.path);

      if (exists) {
        console.log(chalk.green(`✅ ${check.name}`));
      } else {
        console.log(chalk.red(`❌ ${check.name}`));
        allPassed = false;
      }
    }

    // 检查git状态
    try {
      const isRepo = await this.git.checkIsRepo();
      if (isRepo) {
        const status = await this.git.status();
        console.log(chalk.green(`✅ Git仓库: ${status.current || '未设置分支'}`));
        console.log(chalk.cyan(`  未提交更改: ${status.files.length} 个文件`));
      } else {
        console.log(chalk.yellow('⚠️  Git仓库: 未初始化'));
      }
    } catch (error) {
      console.log(chalk.red(`❌ Git检查失败: ${error.message}`));
    }

    // 检查今日记忆文件
    const today = format(new Date(), 'yyyy-MM-dd');
    const dailyFile = path.join(this.memoryPath, `${today}.md`);
    if (await fs.pathExists(dailyFile)) {
      const stats = await fs.stat(dailyFile);
      const age = (Date.now() - stats.mtimeMs) / 1000 / 60; // 分钟
      console.log(chalk.green(`✅ 今日记忆文件: ${today}.md (${age.toFixed(1)}分钟前更新)`));
    } else {
      console.log(chalk.red(`❌ 今日记忆文件: 未创建`));
    }

    // 检查备份
    const backupDir = path.join(this.memoryPath, 'backup');
    if (await fs.pathExists(backupDir)) {
      const backups = await fs.readdir(backupDir);
      console.log(chalk.cyan(`📦 备份数量: ${backups.length} 个`));
    }

    console.log(chalk.bold('\n' + (allPassed ? '🎉 系统状态正常' : '⚠️  系统需要修复')));
  }

  async save(message = '自动保存') {
    console.log(chalk.blue('💾 手动保存记忆状态...'));
    
    // 确保今日文件存在
    await this.createDailyMemoryFile();
    
    // 更新索引时间戳
    const indexPath = path.join(this.memoryPath, 'memory_index.json');
    if (await fs.pathExists(indexPath)) {
      const index = await fs.readJson(indexPath);
      index.lastUpdated = new Date().toISOString();
      index.fileCount = (await fs.readdir(this.memoryPath)).length;
      await fs.writeJson(indexPath, index, { spaces: 2 });
    }

    // 添加到git
    try {
      await this.git.add('./memory/*');
      await this.git.commit(`记忆保存: ${message} - ${new Date().toLocaleString('zh-CN')}`);
      console.log(chalk.green(`✅ 记忆已保存并提交: "${message}"`));
    } catch (error) {
      console.log(chalk.yellow(`⚠️  Git提交失败: ${error.message}`));
      console.log(chalk.green('✅ 记忆文件已保存（本地）'));
    }
  }

  async search(query) {
    console.log(chalk.blue(`🔍 搜索记忆: "${query}"`));
    
    // 简单的文本搜索实现
    const searchResults = [];
    const files = await fs.readdir(this.memoryPath);
    
    for (const file of files) {
      if (file.endsWith('.md')) {
        const filePath = path.join(this.memoryPath, file);
        const content = await fs.readFile(filePath, 'utf8');
        
        if (content.toLowerCase().includes(query.toLowerCase())) {
          // 找到匹配行
          const lines = content.split('\n');
          const matchingLines = lines
            .map((line, index) => ({ line, index: index + 1 }))
            .filter(({ line }) => line.toLowerCase().includes(query.toLowerCase()))
            .slice(0, 3); // 只显示前3个匹配行
            
          if (matchingLines.length > 0) {
            searchResults.push({
              file,
              path: filePath,
              matches: matchingLines.length,
              preview: matchingLines[0].line.trim().substring(0, 100) + '...'
            });
          }
        }
      }
    }
    
    if (searchResults.length > 0) {
      console.log(chalk.green(`✅ 找到 ${searchResults.length} 个相关文件:`));
      searchResults.forEach((result, index) => {
        console.log(chalk.cyan(`  ${index + 1}. ${result.file}`));
        console.log(chalk.gray(`     匹配: ${result.matches} 处 | ${result.preview}`));
      });
    } else {
      console.log(chalk.yellow('⚠️  未找到相关记忆'));
    }
  }

  async backup() {
    console.log(chalk.blue('📦 创建记忆备份...'));
    
    const timestamp = format(new Date(), 'yyyyMMdd_HHmmss');
    const backupDir = path.join(this.memoryPath, 'backup', `backup_${timestamp}`);
    
    await fs.ensureDir(backupDir);
    await fs.copy(this.memoryPath, backupDir, {
      filter: (src) => !src.includes('backup') && !src.includes('node_modules')
    });
    
    // 创建备份信息文件
    const backupInfo = {
      timestamp: new Date().toISOString(),
      source: this.memoryPath,
      destination: backupDir,
      size: await this.getDirSize(this.memoryPath),
      fileCount: (await fs.readdir(this.memoryPath)).length,
      version: '1.0.0'
    };
    
    await fs.writeJson(path.join(backupDir, 'backup_info.json'), backupInfo, { spaces: 2 });
    
    console.log(chalk.green(`✅ 备份创建完成: ${path.relative(this.memoryPath, backupDir)}`));
    console.log(chalk.cyan(`  备份时间: ${new Date().toLocaleString('zh-CN')}`));
    console.log(chalk.cyan(`  备份大小: ${(backupInfo.size / 1024 / 1024).toFixed(2)} MB`));
    console.log(chalk.cyan(`  文件数量: ${backupInfo.fileCount} 个`));
  }

  async getDirSize(dir) {
    let totalSize = 0;
    const files = await fs.readdir(dir, { withFileTypes: true });
    
    for (const file of files) {
      const filePath = path.join(dir, file.name);
      if (file.isDirectory()) {
        totalSize += await this.getDirSize(filePath);
      } else {
        const stats = await fs.stat(filePath);
        totalSize += stats.size;
      }
    }
    
    return totalSize;
  }
}

// CLI接口
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  
  const guardian = new MemoryGuardian();
  
  switch (command) {
    case 'init':
      await guardian.init();
      break;
    case 'status':
      await guardian.status();
      break;
    case 'save':
      await guardian.save(args[1] || '手动保存');
      break;
    case 'search':
      if (args[1]) {
        await guardian.search(args[1]);
      } else {
        console.log(chalk.red('❌ 请提供搜索关键词'));
        console.log(chalk.yellow('用法: memory-guardian search "关键词"'));
      }
      break;
    case 'backup':
      await guardian.backup();
      break;
    case 'help':
    default:
      console.log(chalk.bold.blue('🧠 Claw Memory Guardian - 记忆守护者'));
      console.log(chalk.cyan('基于亲身教训的防丢失记忆系统\n'));
      console.log(chalk.bold('可用命令:'));
      console.log('  init          初始化记忆系统');
      console.log('  status        检查系统状态');
      console.log('  save [消息]   手动保存记忆');
      console.log('  search <关键词> 搜索记忆内容');
      console.log('  backup        创建完整备份');
      console.log('  help          显示帮助信息');
      console.log(chalk.yellow('\n示例:'));
      console.log('  memory-guardian init');
      console.log('  memory-guardian status');
      console.log('  memory-guardian search "项目进度"');
      console.log('  memory-guardian save "完成重要决策"');
      break;
  }
}

// 错误处理
main().catch(error => {
  console.error(chalk.red('❌ 错误:'), error.message);
  process.exit(1);
});