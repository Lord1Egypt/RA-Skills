#!/usr/bin/env node
/**
 * GitHub API自动发布脚本
 * 使用GitHub API自动创建仓库和发布
 */

const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');
const chalk = require('chalk');
const yaml = require('js-yaml');
const https = require('https');

class GitHubAPIRelease {
  constructor() {
    this.projectDir = process.cwd();
    this.configPath = path.join(this.projectDir, '..', 'config.yaml');
    this.githubToken = null;
    this.githubUsername = null;
  }

  async loadConfig() {
    console.log(chalk.blue('📋 加载配置文件...'));
    
    try {
      const configContent = await fs.readFile(this.configPath, 'utf8');
      const config = yaml.load(configContent);
      this.githubToken = config.github?.token;
      
      if (!this.githubToken) {
        throw new Error('未找到GitHub token');
      }
      
      // 从token解析用户名（token格式：ghp_xxxxxxxxxxxxxxxx）
      // 需要调用API获取用户名
      await this.getGitHubUsername();
      
      console.log(chalk.green('✅ 配置文件加载成功'));
      console.log(chalk.gray(`   用户: ${this.githubUsername}`));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 配置文件加载失败:'), error.message);
      return false;
    }
  }

  async getGitHubUsername() {
    return new Promise((resolve, reject) => {
      const options = {
        hostname: 'api.github.com',
        port: 443,
        path: '/user',
        method: 'GET',
        headers: {
          'Authorization': `token ${this.githubToken}`,
          'User-Agent': 'E2E-Test-Recorder-Release',
          'Accept': 'application/vnd.github.v3+json'
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const userInfo = JSON.parse(data);
              this.githubUsername = userInfo.login;
              resolve(this.githubUsername);
            } catch (error) {
              reject(new Error('解析用户信息失败'));
            }
          } else {
            reject(new Error(`API请求失败: ${res.statusCode}`));
          }
        });
      });
      
      req.on('error', (error) => {
        reject(error);
      });
      
      req.end();
    });
  }

  async createGitHubRepo() {
    console.log(chalk.blue('\n🔄 创建GitHub仓库...'));
    
    const repoData = {
      name: 'e2e-test-recorder',
      description: 'Automated end-to-end test recorder with screen recording capabilities',
      private: false,
      auto_init: false,
      license_template: 'mit',
      gitignore_template: 'Node'
    };
    
    return new Promise((resolve, reject) => {
      const postData = JSON.stringify(repoData);
      
      const options = {
        hostname: 'api.github.com',
        port: 443,
        path: '/user/repos',
        method: 'POST',
        headers: {
          'Authorization': `token ${this.githubToken}`,
          'User-Agent': 'E2E-Test-Recorder-Release',
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(postData)
        }
      };
      
      const req = https.request(options, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          if (res.statusCode === 201) {
            try {
              const repoInfo = JSON.parse(data);
              console.log(chalk.green(`✅ 仓库创建成功: ${repoInfo.html_url}`));
              console.log(chalk.gray(`   SSH URL: ${repoInfo.ssh_url}`));
              console.log(chalk.gray(`   HTTPS URL: ${repoInfo.clone_url}`));
              resolve(repoInfo);
            } catch (error) {
              reject(new Error('解析仓库信息失败'));
            }
          } else if (res.statusCode === 422) {
            console.log(chalk.yellow('⚠️  仓库可能已存在，尝试使用现有仓库'));
            resolve(null);
          } else {
            console.error(chalk.red('❌ 仓库创建失败:'), data);
            reject(new Error(`创建仓库失败: ${res.statusCode}`));
          }
        });
      });
      
      req.on('error', (error) => {
        reject(error);
      });
      
      req.write(postData);
      req.end();
    });
  }

  async setupGitRemote(repoInfo) {
    console.log(chalk.blue('\n🔗 配置Git远程仓库...'));
    
    try {
      // 检查是否已配置远程仓库
      const remotes = execSync('git remote -v', { encoding: 'utf8' });
      if (remotes.includes('origin')) {
        console.log(chalk.yellow('⚠️  远程仓库已配置，跳过配置'));
        return true;
      }
      
      if (!repoInfo) {
        console.log(chalk.yellow('📝 需要手动配置远程仓库:'));
        console.log('1. 创建GitHub仓库: https://github.com/new');
        console.log('2. 仓库名: e2e-test-recorder');
        console.log('3. 复制仓库URL');
        console.log('4. 执行以下命令:');
        console.log(chalk.cyan('   git remote add origin <你的仓库URL>'));
        console.log(chalk.cyan('   git branch -M main'));
        return false;
      }
      
      // 配置远程仓库
      const sshUrl = repoInfo.ssh_url;
      console.log(chalk.yellow(`配置远程仓库: ${sshUrl}`));
      
      execSync(`git remote add origin ${sshUrl}`, { stdio: 'inherit' });
      execSync('git branch -M main', { stdio: 'inherit' });
      
      console.log(chalk.green('✅ 远程仓库配置成功'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 配置远程仓库失败:'), error.message);
      return false;
    }
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

  async createReleaseNotes() {
    console.log(chalk.blue('\n📝 生成发布说明...'));
    
    const releaseNotes = `## 🎉 E2E Test Recorder v1.0.0

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
git clone https://github.com/${this.githubUsername}/e2e-test-recorder.git
cd e2e-test-recorder
npm install --legacy-peer-deps

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
    
    const notesPath = path.join(this.projectDir, 'RELEASE_NOTES.md');
    await fs.writeFile(notesPath, releaseNotes, 'utf8');
    
    console.log(chalk.green('✅ 发布说明已生成: RELEASE_NOTES.md'));
    
    // 显示手动创建Release的步骤
    console.log(chalk.yellow('\n📋 手动创建GitHub Release:'));
    console.log(`1. 访问 https://github.com/${this.githubUsername}/e2e-test-recorder`);
    console.log('2. 点击 "Releases" → "Draft a new release"');
    console.log('3. 选择标签: v1.0.0');
    console.log('4. 标题: E2E Test Recorder v1.0.0');
    console.log('5. 复制 RELEASE_NOTES.md 内容到发布说明');
    console.log('6. 点击 "Publish release"');
    
    return true;
  }

  async generateFinalGuide() {
    console.log(chalk.blue('\n📋 生成最终发布指南...'));
    
    const finalGuide = `# 🚀 发布完成指南

## GitHub发布状态
- ✅ 仓库创建: https://github.com/${this.githubUsername}/e2e-test-recorder
- ✅ 代码推送: 完成
- ✅ 标签创建: v1.0.0
- ⏳ Release创建: 需要手动操作

## 剩余操作

### 1. 创建GitHub Release
\`\`\`bash
# 访问仓库并创建Release
# 使用 RELEASE_NOTES.md 作为发布说明
\`\`\`

### 2. 发布到ClawHub
1. 访问 https://clawhub.com
2. 登录账号（支持GitHub登录）
3. 点击 "发布新技能"
4. 填写技能信息（参考 CLAWHUB_PUBLISH.md）
5. 仓库URL: https://github.com/${this.githubUsername}/e2e-test-recorder
6. 提交审核

### 3. 验证发布
\`\`\`bash
# 测试安装
git clone https://github.com/${this.githubUsername}/e2e-test-recorder.git
cd e2e-test-recorder
npm install --legacy-peer-deps
node scripts/cli.js --version
\`\`\`

## 技术支持
- GitHub Issues: 报告问题
- 项目文档: 查看详细使用说明
- 社区支持: 分享使用经验

---
**发布完成时间**: ${new Date().toLocaleString()}
**技能版本**: v1.0.0
**开发者**: ${this.githubUsername}`;
    
    const guidePath = path.join(this.projectDir, 'RELEASE_COMPLETE.md');
    await fs.writeFile(guidePath, finalGuide, 'utf8');
    
    console.log(chalk.green('✅ 最终发布指南已生成: RELEASE_COMPLETE.md'));
    return true;
  }

  async run() {
    console.log(chalk.cyan('🚀 GitHub API自动发布工具'));
    console.log(chalk.gray('='.repeat(60)));

    try {
      // 加载配置
      if (!await this.loadConfig()) {
        return;
      }

      // 创建GitHub仓库
      const repoInfo = await this.createGitHubRepo();

      // 配置Git远程仓库
      if (!await this.setupGitRemote(repoInfo)) {
        console.log(chalk.yellow('⚠️  需要手动配置远程仓库'));
        console.log(chalk.yellow('   参考 EXECUTE_RELEASE.md 步骤1-2'));
        return;
      }

      // 推送代码
      if (!await this.pushToGitHub()) {
        console.log(chalk.yellow('⚠️  推送失败，请手动操作'));
        return;
      }

      // 生成发布说明
      await this.createReleaseNotes();

      // 生成最终指南
      await this.generateFinalGuide();

      console.log(chalk.green('\n✅ 自动发布流程完成！'));
      console.log(chalk.yellow('\n📋 剩余操作：'));
      console.log('1. 手动创建GitHub Release（使用RELEASE_NOTES.md）');
      console.log('2. 按照CLAWHUB_PUBLISH.md发布到ClawHub');
      console.log('3. 验证发布结果（参考RELEASE_COMPLETE.md）');

    } catch (error) {
      console.error(chalk.red('\n❌ 发布失败:'), error.message);
      console.log(chalk.yellow('\n💡 备用方案：'));
      console.log('1. 手动创建GitHub仓库');
      console.log('2. 按照 EXECUTE_RELEASE.md 操作');
      console.log('3. 使用 CLAWHUB_PUBLISH.md 发布到ClawHub');
    }
  }
}

// 运行发布
const release = new GitHubAPIRelease();
release.run().catch(console.error);