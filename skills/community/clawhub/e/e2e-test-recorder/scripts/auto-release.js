#!/usr/bin/env node
/**
 * 自动发布脚本
 * 使用配置中的GitHub token自动发布
 */

const fs = require('fs-extra');
const path = require('path');
const { execSync, spawn } = require('child_process');
const chalk = require('chalk');
const yaml = require('js-yaml');

class AutoRelease {
  constructor() {
    this.projectDir = process.cwd();
    this.configPath = path.join(this.projectDir, '..', 'config.yaml');
    this.config = null;
    this.githubToken = null;
  }

  async loadConfig() {
    console.log(chalk.blue('📋 加载配置文件...'));
    
    try {
      const configContent = await fs.readFile(this.configPath, 'utf8');
      this.config = yaml.load(configContent);
      this.githubToken = this.config.github?.token;
      
      if (!this.githubToken) {
        throw new Error('未找到GitHub token');
      }
      
      console.log(chalk.green('✅ 配置文件加载成功'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 配置文件加载失败:'), error.message);
      return false;
    }
  }

  async checkGitStatus() {
    console.log(chalk.blue('\n📊 检查Git状态...'));
    
    try {
      const status = execSync('git status --porcelain', { encoding: 'utf8' });
      if (status.trim()) {
        console.log(chalk.yellow('⚠️  有未提交的更改:'));
        console.log(status);
        return false;
      } else {
        console.log(chalk.green('✅ Git状态正常'));
        return true;
      }
    } catch (error) {
      console.error(chalk.red('❌ Git检查失败:'), error.message);
      return false;
    }
  }

  async setupGitRemote() {
    console.log(chalk.blue('\n🔗 配置Git远程仓库...'));
    
    // 检查是否已配置远程仓库
    try {
      const remotes = execSync('git remote -v', { encoding: 'utf8' });
      if (remotes.includes('origin')) {
        console.log(chalk.green('✅ 远程仓库已配置'));
        return true;
      }
    } catch (error) {
      // 忽略错误
    }
    
    // 需要用户提供GitHub用户名
    console.log(chalk.yellow('📝 需要手动配置远程仓库:'));
    console.log('1. 创建GitHub仓库: https://github.com/new');
    console.log('2. 仓库名: e2e-test-recorder');
    console.log('3. 复制仓库URL');
    console.log('4. 执行以下命令:');
    console.log(chalk.cyan('   git remote add origin <你的仓库URL>'));
    console.log(chalk.cyan('   git branch -M main'));
    
    return false;
  }

  async pushToGitHub() {
    console.log(chalk.blue('\n📤 推送代码到GitHub...'));
    
    try {
      // 设置GitHub token环境变量
      process.env.GITHUB_TOKEN = this.githubToken;
      
      // 推送代码
      console.log(chalk.yellow('正在推送代码...'));
      execSync('git push -u origin main', { stdio: 'inherit' });
      
      // 创建标签
      console.log(chalk.yellow('创建标签 v1.0.0...'));
      execSync('git tag -a v1.0.0 -m "Initial release: E2E Test Recorder v1.0.0"', { stdio: 'inherit' });
      
      // 推送标签
      console.log(chalk.yellow('推送标签...'));
      execSync('git push origin v1.0.0', { stdio: 'inherit' });
      
      console.log(chalk.green('✅ 代码推送成功'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 推送失败:'), error.message);
      return false;
    }
  }

  async createGitHubRelease() {
    console.log(chalk.blue('\n🎉 创建GitHub Release...'));
    
    // 创建release说明文件
    const releaseNotes = this.generateReleaseNotes();
    const notesPath = path.join(this.projectDir, 'RELEASE_NOTES.md');
    
    await fs.writeFile(notesPath, releaseNotes, 'utf8');
    
    console.log(chalk.yellow('📝 Release说明已生成: RELEASE_NOTES.md'));
    console.log(chalk.yellow('\n📋 手动创建Release步骤:'));
    console.log('1. 访问你的GitHub仓库: https://github.com/YOUR_USERNAME/e2e-test-recorder');
    console.log('2. 点击 "Releases" → "Draft a new release"');
    console.log('3. 选择标签: v1.0.0');
    console.log('4. 标题: E2E Test Recorder v1.0.0');
    console.log('5. 复制 RELEASE_NOTES.md 内容到发布说明');
    console.log('6. 点击 "Publish release"');
    
    return true;
  }

  generateReleaseNotes() {
    return `## 🎉 E2E Test Recorder v1.0.0

### 功能特性
- 🎥 **浏览器操作录制**: 基于Puppeteer的浏览器录制
- 🎯 **端到端测试录制**: 完整的测试流程录制
- 🔄 **格式转换**: 支持MP4、GIF、WebM格式
- ⚡ **自动化测试集成**: 可与测试框架集成
- 📊 **性能监控**: 录制过程中的性能数据
- 🎨 **视频编辑**: 基础视频编辑功能

### 技术特性
- **跨平台**: 支持Windows、macOS、Linux
- **高性能**: 基于硬件加速和优化算法
- **易扩展**: 模块化架构，易于添加新功能
- **标准化**: 符合WorkBuddy和OpenClaw技能协议

### 安装方式
\`\`\`bash
# 从GitHub安装
git clone https://github.com/YOUR_USERNAME/e2e-test-recorder.git
cd e2e-test-recorder
npm install

# 或者全局安装CLI
npm install -g .
\`\`\`

### 快速开始
\`\`\`bash
# 查看帮助
e2e-test --help

# 录制网页操作
e2e-test record https://example.com --output demo.mp4

# 录制端到端测试
e2e-test test configs/test.json --record
\`\`\`

### 文档
- [README.md](README.md) - 项目说明
- [INSTALLATION.md](INSTALLATION.md) - 安装指南
- [SKILL.md](SKILL.md) - 技能文档
- [examples/](examples/) - 使用示例

### 开源协议
MIT License - 详见 [LICENSE](LICENSE)`;
  }

  async generateClawHubGuide() {
    console.log(chalk.blue('\n🦀 生成ClawHub发布指南...'));
    
    const clawhubGuide = `
# ClawHub发布检查清单

## 发布前准备
- [ ] GitHub仓库已创建并推送
- [ ] GitHub Release已创建
- [ ] 技能文档完整
- [ ] 使用示例可用

## ClawHub发布步骤
1. 访问 https://clawhub.com
2. 登录账号（支持GitHub登录）
3. 点击 "发布新技能"

## 技能信息
- **技能名称**: e2e-test-recorder
- **显示名称**: E2E Test Recorder
- **技能描述**: 自动化端到端测试录制工具，支持浏览器操作录制和测试过程录制
- **技能分类**: 开发工具 → 测试工具
- **技能标签**: e2e-testing, screen-recording, automation, testing, puppeteer, nodejs
- **开源协议**: MIT License

## 上传方式
- **方式**: GitHub仓库
- **仓库URL**: https://github.com/YOUR_USERNAME/e2e-test-recorder
- **分支**: main
- **技能版本**: 1.0.0

## 详细说明
参考 CLAWHUB_PUBLISH.md 文件

## 提交审核
1. 预览检查所有信息
2. 提交审核
3. 等待审核结果（1-3个工作日）
`;
    
    const guidePath = path.join(this.projectDir, 'CLAWHUB_CHECKLIST.md');
    await fs.writeFile(guidePath, clawhubGuide, 'utf8');
    
    console.log(chalk.green('✅ ClawHub发布指南已生成: CLAWHUB_CHECKLIST.md'));
    return true;
  }

  async run() {
    console.log(chalk.cyan('🚀 E2E Test Recorder 自动发布工具'));
    console.log(chalk.gray('='.repeat(60)));

    // 加载配置
    if (!await this.loadConfig()) {
      return;
    }

    // 检查Git状态
    if (!await this.checkGitStatus()) {
      console.log(chalk.yellow('⚠️  请先提交所有更改'));
      return;
    }

    // 配置远程仓库
    if (!await this.setupGitRemote()) {
      console.log(chalk.yellow('⚠️  需要手动配置远程仓库'));
      console.log(chalk.yellow('   参考 EXECUTE_RELEASE.md 步骤1-2'));
      return;
    }

    // 推送代码
    if (!await this.pushToGitHub()) {
      console.log(chalk.yellow('⚠️  推送失败，请手动操作'));
      return;
    }

    // 创建Release
    await this.createGitHubRelease();

    // 生成ClawHub指南
    await this.generateClawHubGuide();

    console.log(chalk.green('\n✅ 自动发布流程完成！'));
    console.log(chalk.yellow('\n📋 剩余手动操作：'));
    console.log('1. 手动创建GitHub Release（使用RELEASE_NOTES.md）');
    console.log('2. 按照CLAWHUB_CHECKLIST.md发布到ClawHub');
    console.log('3. 验证发布结果');
  }
}

// 运行发布
const release = new AutoRelease();
release.run().catch(console.error);