#!/usr/bin/env node

/**
 * 部署脚本 - 用于发布到GitHub和ClawHub
 */

const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');
const chalk = require('chalk');
const inquirer = require('inquirer');

class DeployManager {
  constructor() {
    this.projectRoot = process.cwd();
    this.packageJson = require(path.join(this.projectRoot, 'package.json'));
  }

  async checkGitStatus() {
    console.log(chalk.blue('🔍 检查Git状态...'));
    
    try {
      const status = execSync('git status --porcelain', { encoding: 'utf8' });
      if (status.trim()) {
        console.log(chalk.yellow('⚠️  有未提交的更改:'));
        console.log(status);
        
        const { shouldCommit } = await inquirer.prompt([
          {
            type: 'confirm',
            name: 'shouldCommit',
            message: '是否提交这些更改？',
            default: true
          }
        ]);
        
        if (shouldCommit) {
          const { commitMessage } = await inquirer.prompt([
            {
              type: 'input',
              name: 'commitMessage',
              message: '提交信息:',
              default: 'Update before deployment'
            }
          ]);
          
          execSync(`git add . && git commit -m "${commitMessage}"`, { stdio: 'inherit' });
        }
      } else {
        console.log(chalk.green('✅ Git仓库干净'));
      }
    } catch (error) {
      console.error(chalk.red('❌ Git检查失败:'), error.message);
    }
  }

  async checkRemote() {
    console.log(chalk.blue('🔍 检查远程仓库...'));
    
    try {
      const remotes = execSync('git remote -v', { encoding: 'utf8' });
      if (remotes.includes('origin')) {
        console.log(chalk.green('✅ 已配置远程仓库:'));
        console.log(remotes);
        return true;
      } else {
        console.log(chalk.yellow('⚠️  未配置远程仓库'));
        return false;
      }
    } catch (error) {
      console.error(chalk.red('❌ 检查远程仓库失败:'), error.message);
      return false;
    }
  }

  async setupGitHub() {
    console.log(chalk.blue('🚀 设置GitHub仓库...'));
    
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'repoUrl',
        message: 'GitHub仓库URL (例如: https://github.com/username/e2e-test-recorder.git):',
        validate: input => input.includes('github.com') || '请输入有效的GitHub URL'
      },
      {
        type: 'input',
        name: 'repoName',
        message: '仓库名称 (用于README):',
        default: 'e2e-test-recorder'
      }
    ]);
    
    try {
      // 添加远程仓库
      execSync(`git remote add origin ${answers.repoUrl}`, { stdio: 'inherit' });
      
      // 更新README中的GitHub链接
      await this.updateReadme(answers.repoUrl, answers.repoName);
      
      console.log(chalk.green('✅ GitHub仓库配置完成'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 设置GitHub失败:'), error.message);
      return false;
    }
  }

  async updateReadme(repoUrl, repoName) {
    const readmePath = path.join(this.projectRoot, 'README.md');
    let readmeContent = await fs.readFile(readmePath, 'utf8');
    
    // 提取仓库用户名和仓库名
    const match = repoUrl.match(/github\.com\/([^\/]+)\/([^\/\.]+)/);
    if (match) {
      const [, username, repo] = match;
      
      // 更新GitHub部分
      readmeContent = readmeContent.replace(
        /## 📦 安装[\s\S]*?(?=## 🚀 使用)/,
        `## 📦 安装

### 作为Skill安装
\`\`\`bash
npx skills add ${username}/${repo}@e2e-test-recorder
\`\`\`

### 从GitHub安装
\`\`\`bash
# 克隆仓库
git clone ${repoUrl}
cd ${repo}

# 安装依赖
npm install

# 全局安装CLI
npm install -g .
\`\`\`

### 从npm安装 (待发布)
\`\`\`bash
npm install ${repoName}
\`\`\`
`
      );
      
      // 更新贡献部分
      const contributionSection = `## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork本仓库
2. 创建功能分支 (\`git checkout -b feature/amazing-feature\`)
3. 提交更改 (\`git commit -m 'feat: add amazing feature'\`)
4. 推送到分支 (\`git push origin feature/amazing-feature\`)
5. 创建Pull Request

### 开发环境设置
\`\`\`bash
# 克隆仓库
git clone ${repoUrl}
cd ${repo}

# 安装依赖
npm install

# 运行测试
npm test

# 运行示例
node examples/basic-recording.js
\`\`\`

### 代码规范
- 使用ESLint进行代码检查
- 遵循Conventional Commits规范
- 添加适当的测试用例
- 更新相关文档`;
      
      readmeContent = readmeContent.replace(/## 🤝 贡献[\s\S]*?(?=## 📄 许可证|$)/, contributionSection);
      
      await fs.writeFile(readmePath, readmeContent);
      console.log(chalk.green('✅ README更新完成'));
    }
  }

  async pushToGitHub() {
    console.log(chalk.blue('📤 推送到GitHub...'));
    
    try {
      // 拉取最新更改
      execSync('git pull origin main --rebase || git pull origin master --rebase', { stdio: 'inherit' });
      
      // 推送更改
      execSync('git push -u origin main || git push -u origin master', { stdio: 'inherit' });
      
      console.log(chalk.green('✅ 成功推送到GitHub'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 推送失败:'), error.message);
      
      const { forcePush } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'forcePush',
          message: '是否强制推送？(注意: 可能会覆盖远程更改)',
          default: false
        }
      ]);
      
      if (forcePush) {
        execSync('git push -u origin main --force || git push -u origin master --force', { stdio: 'inherit' });
        console.log(chalk.green('✅ 强制推送完成'));
        return true;
      }
      return false;
    }
  }

  async setupClawHub() {
    console.log(chalk.blue('🦀 设置ClawHub...'));
    
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'skillName',
        message: 'ClawHub技能名称:',
        default: 'e2e-test-recorder'
      },
      {
        type: 'input',
        name: 'skillDescription',
        message: '技能描述:',
        default: '自动化端到端测试录制工具，支持浏览器操作录制和测试过程录制'
      }
    ]);
    
    try {
      // 创建ClawHub发布配置
      const clawhubConfig = {
        name: answers.skillName,
        version: this.packageJson.version,
        description: answers.skillDescription,
        author: this.packageJson.author || 'Your Name',
        repository: this.packageJson.repository || '',
        keywords: ['e2e-test', 'recorder', 'screen-recording', 'automation', 'testing'],
        license: this.packageJson.license || 'MIT',
        dependencies: this.packageJson.dependencies,
        main: this.packageJson.main,
        bin: this.packageJson.bin,
        files: [
          "SKILL.md",
          "README.md",
          "package.json",
          "scripts/**/*.js",
          "configs/**/*.json",
          "examples/**/*.js"
        ]
      };
      
      const configPath = path.join(this.projectRoot, 'clawhub.config.json');
      await fs.writeJson(configPath, clawhubConfig, { spaces: 2 });
      
      console.log(chalk.green('✅ ClawHub配置创建完成:'), configPath);
      console.log(chalk.cyan('📝 下一步:'));
      console.log('1. 登录 ClawHub: https://clawhub.com');
      console.log('2. 创建新技能');
      console.log('3. 上传技能文件');
      console.log('4. 填写技能信息');
      console.log('5. 发布技能');
      
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 设置ClawHub失败:'), error.message);
      return false;
    }
  }

  async run() {
    console.log(chalk.cyan('🎬 E2E测试录制技能部署工具'));
    console.log(chalk.cyan('='.repeat(50)));
    
    // 检查Git状态
    await this.checkGitStatus();
    
    // 检查远程仓库
    const hasRemote = await this.checkRemote();
    
    if (!hasRemote) {
      const { setupGitHub } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'setupGitHub',
          message: '是否设置GitHub仓库？',
          default: true
        }
      ]);
      
      if (setupGitHub) {
        await this.setupGitHub();
      }
    }
    
    // 推送到GitHub
    const { pushToGitHub } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'pushToGitHub',
        message: '是否推送到GitHub？',
        default: true
      }
    ]);
    
    if (pushToGitHub) {
      await this.pushToGitHub();
    }
    
    // 设置ClawHub
    const { setupClawHub } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'setupClawHub',
        message: '是否设置ClawHub发布配置？',
        default: true
      }
    ]);
    
    if (setupClawHub) {
      await this.setupClawHub();
    }
    
    console.log(chalk.green('🎉 部署流程完成！'));
    console.log(chalk.cyan('\n📋 下一步行动:'));
    console.log('1. 在GitHub上创建Release');
    console.log('2. 在ClawHub上发布技能');
    console.log('3. 更新npm包信息');
    console.log('4. 推广你的技能');
  }
}

// 运行部署工具
if (require.main === module) {
  const deployer = new DeployManager();
  deployer.run().catch(console.error);
}

module.exports = DeployManager;