#!/usr/bin/env node
/**
 * 执行验证器 v7.13（通用版）
 * 
 * 核心功能:
 * 1. 验证各类任务完成状态
 * 2. 支持多任务类型配置
 * 3. 文件存在性检查
 * 4. 内容完整性验证
 */

const fs = require('fs');
const path = require('path');

class ExecutionVerifier {
  constructor(config = {}) {
    this.workspace = config.workspace || '/home/ubutu/.openclaw/workspace';
    this.taskConfigs = this.loadTaskConfigs();
  }

  /**
   * 加载任务类型配置
   */
  loadTaskConfigs() {
    return {
      // 小说创作
      'novel-outline': {
        name: '小说章节细纲',
        dir: '04_章节细纲',
        expectedFiles: ['第*.md'],
        minFiles: 1,
        minContent: 500,  // 每章最少字数
        filePattern: /第(\d+) 章/
      },
      'novel-chapter': {
        name: '小说正文章节',
        dir: '05_正文创作',
        expectedFiles: ['第*.md'],
        minFiles: 1,
        minContent: 6500,  // 每章最少字数
        filePattern: /第(\d+) 章/
      },
      
      // 代码开发
      'code-module': {
        name: '代码模块',
        dir: 'src/modules',
        expectedFiles: ['*.js', '*.py'],
        minFiles: 1,
        minContent: 100,
        filePattern: /\.(js|py)$/
      },
      'code-test': {
        name: '代码测试',
        dir: 'tests',
        expectedFiles: ['*.test.js', '*.test.py'],
        minFiles: 1,
        minContent: 50,
        filePattern: /\.test\.(js|py)$/
      },
      
      // 数据清洗
      'data-cleaning': {
        name: '数据清洗',
        dir: 'output/cleaned',
        expectedFiles: ['*.csv', '*.json'],
        minFiles: 1,
        minContent: 1000,
        filePattern: /\.(csv|json)$/
      },
      'data-analysis': {
        name: '数据分析',
        dir: 'output/analysis',
        expectedFiles: ['*.md', '*.json'],
        minFiles: 1,
        minContent: 2000,
        filePattern: /\.(md|json)$/
      },
      
      // 市场调研
      'research-report': {
        name: '调研报告',
        dir: 'reports',
        expectedFiles: ['*.md', '*.pdf'],
        minFiles: 1,
        minContent: 3000,
        filePattern: /\.(md|pdf)$/
      },
      'market-data': {
        name: '市场数据',
        dir: 'data/market',
        expectedFiles: ['*.json', '*.csv'],
        minFiles: 1,
        minContent: 5000,
        filePattern: /\.(json|csv)$/
      },
      
      // 文档编写
      'documentation': {
        name: '文档编写',
        dir: 'docs',
        expectedFiles: ['*.md'],
        minFiles: 1,
        minContent: 1000,
        filePattern: /\.md$/
      }
    };
  }

  /**
   * 验证任务完成状态
   */
  async verifyTaskCompletion(projectDir, taskType) {
    const config = this.taskConfigs[taskType];
    
    if (!config) {
      return {
        valid: false,
        error: `未知任务类型：${taskType}`,
        supported: Object.keys(this.taskConfigs)
      };
    }
    
    const result = {
      taskType,
      taskName: config.name,
      projectDir,
      timestamp: new Date().toISOString(),
      checks: {}
    };
    
    // 1. 检查目录存在
    result.checks.directory = await this.checkDirectory(
      path.join(projectDir, config.dir)
    );
    
    if (!result.checks.directory.exists) {
      result.valid = false;
      result.error = '目录不存在';
      return result;
    }
    
    // 2. 检查文件存在
    result.checks.files = await this.checkFiles(
      path.join(projectDir, config.dir),
      config.expectedFiles
    );
    
    if (result.checks.files.count < config.minFiles) {
      result.valid = false;
      result.error = `文件数量不足：${result.checks.files.count}/${config.minFiles}`;
      return result;
    }
    
    // 3. 检查内容完整性
    result.checks.content = await this.checkContent(
      result.checks.files.files,
      config.minContent
    );
    
    // 4. 检查完成度
    result.checks.completion = await this.checkCompletion(
      result.checks.files.files,
      config
    );
    
    // 总体评估
    result.valid = 
      result.checks.directory.exists &&
      result.checks.files.count >= config.minFiles &&
      result.checks.content.valid &&
      result.checks.completion.valid;
    
    result.summary = this.generateSummary(result);
    
    return result;
  }

  /**
   * 检查目录存在
   */
  async checkDirectory(dirPath) {
    const exists = fs.existsSync(dirPath);
    const isDirectory = exists && fs.statSync(dirPath).isDirectory();
    
    return {
      path: dirPath,
      exists,
      isDirectory,
      valid: exists && isDirectory
    };
  }

  /**
   * 检查文件存在
   */
  async checkFiles(dirPath, patterns) {
    if (!fs.existsSync(dirPath)) {
      return {
        count: 0,
        files: [],
        valid: false
      };
    }
    
    const allFiles = fs.readdirSync(dirPath);
    const matchedFiles = [];
    
    for (const pattern of patterns) {
      const regex = new RegExp('^' + pattern.replace('*', '.*') + '$');
      for (const file of allFiles) {
        if (regex.test(file) && !matchedFiles.includes(file)) {
          matchedFiles.push(file);
        }
      }
    }
    
    const fullPaths = matchedFiles.map(f => path.join(dirPath, f));
    
    return {
      count: matchedFiles.length,
      files: fullPaths,
      valid: matchedFiles.length > 0
    };
  }

  /**
   * 检查内容完整性
   */
  async checkContent(filePaths, minContent) {
    const results = [];
    let totalValid = true;
    
    for (const filePath of filePaths) {
      if (!fs.existsSync(filePath)) {
        results.push({
          file: filePath,
          valid: false,
          error: '文件不存在'
        });
        totalValid = false;
        continue;
      }
      
      const content = fs.readFileSync(filePath, 'utf8');
      const charCount = content.length;
      const valid = charCount >= minContent;
      
      results.push({
        file: filePath,
        charCount,
        minRequired: minContent,
        valid
      });
      
      if (!valid) {
        totalValid = false;
      }
    }
    
    return {
      files: results,
      valid: totalValid,
      averageContent: results.reduce((sum, r) => sum + (r.charCount || 0), 0) / results.length
    };
  }

  /**
   * 检查完成度
   */
  async checkCompletion(filePaths, config) {
    // 提取章节号/模块号
    const numbers = [];
    
    for (const filePath of filePaths) {
      const fileName = path.basename(filePath);
      const match = fileName.match(config.filePattern);
      if (match && match[1]) {
        numbers.push(parseInt(match[1]));
      }
    }
    
    // 检查连续性
    numbers.sort((a, b) => a - b);
    const expected = numbers.length > 0 ? 
      Array.from({length: numbers[numbers.length - 1]}, (_, i) => i + 1) : [];
    const missing = expected.filter(n => !numbers.includes(n));
    
    return {
      completed: numbers,
      missing,
      continuous: missing.length === 0,
      total: numbers.length,
      valid: missing.length === 0
    };
  }

  /**
   * 生成总结
   */
  generateSummary(result) {
    if (result.valid) {
      return `✅ ${result.taskName} 验证通过`;
    } else {
      return `❌ ${result.taskName} 验证失败：${result.error}`;
    }
  }

  /**
   * 批量验证多个项目
   */
  async verifyMultipleProjects(projects) {
    const results = [];
    
    for (const project of projects) {
      const result = await this.verifyTaskCompletion(
        project.dir,
        project.taskType
      );
      results.push(result);
    }
    
    return {
      total: results.length,
      valid: results.filter(r => r.valid).length,
      invalid: results.filter(r => !r.valid).length,
      results
    };
  }

  /**
   * 添加新任务类型配置
   */
  registerTaskType(taskType, config) {
    this.taskConfigs[taskType] = config;
  }
}

module.exports = ExecutionVerifier;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [projectDir, taskType] = args;
  
  if (!projectDir || !taskType) {
    console.log('用法：node execution-verifier.js <项目目录> <任务类型>');
    console.log('支持的任务类型:');
    
    const verifier = new ExecutionVerifier();
    for (const [type, config] of Object.entries(verifier.taskConfigs)) {
      console.log(`  ${type}: ${config.name}`);
    }
    process.exit(1);
  }
  
  const verifier = new ExecutionVerifier();
  verifier.verifyTaskCompletion(projectDir, taskType)
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.valid ? 0 : 1);
    })
    .catch(error => {
      console.error('验证失败:', error);
      process.exit(1);
    });
}
