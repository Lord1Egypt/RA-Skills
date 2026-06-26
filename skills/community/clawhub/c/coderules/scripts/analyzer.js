#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * 项目分析器 - 自动识别技术栈
 * 用于 CodeRules Skill 自动检测项目语言和框架
 */
class ProjectAnalyzer {
  constructor(projectPath = process.cwd()) {
    this.projectPath = projectPath;
    this.context = {
      languages: new Set(),
      frameworks: new Set(),
      packageManager: null,
      testFramework: null,
      lintConfig: null,
      detectedFiles: []
    };
  }

  /**
   * 主分析入口
   */
  async analyze() {
    await this.detectPackageJson();
    await this.detectConfigFiles();
    await this.detectSourceFiles();
    return this.formatResult();
  }

  /**
   * 分析 package.json
   */
  async detectPackageJson() {
    const packagePath = path.join(this.projectPath, 'package.json');
    if (!fs.existsSync(packagePath)) return;

    const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };

    // 检测语言
    if (deps.typescript) {
      this.context.languages.add('typescript');
    } else if (deps['@babel/core'] || deps.eslint) {
      this.context.languages.add('javascript');
    }

    // 检测框架
    if (deps.react) this.context.frameworks.add('react');
    if (deps.vue) this.context.frameworks.add('vue');
    if (deps.next) this.context.frameworks.add('nextjs');
    if (deps.nuxt) this.context.frameworks.add('nuxt');
    if (deps.express) this.context.frameworks.add('express');
    if (deps['@angular/core']) this.context.frameworks.add('angular');
    if (deps.svelte) this.context.frameworks.add('svelte');

    // 检测测试框架
    if (deps.jest) this.context.testFramework = 'jest';
    if (deps.vitest) this.context.testFramework = 'vitest';
    if (deps['@testing-library/react']) this.context.testFramework = 'testing-library';
    if (deps.pytest) this.context.testFramework = 'pytest';

    // 检测包管理器
    if (fs.existsSync(path.join(this.projectPath, 'pnpm-lock.yaml'))) {
      this.context.packageManager = 'pnpm';
    } else if (fs.existsSync(path.join(this.projectPath, 'yarn.lock'))) {
      this.context.packageManager = 'yarn';
    } else if (fs.existsSync(path.join(this.projectPath, 'bun.lockb'))) {
      this.context.packageManager = 'bun';
    } else if (fs.existsSync(path.join(this.projectPath, 'package-lock.json'))) {
      this.context.packageManager = 'npm';
    }
  }

  /**
   * 分析配置文件
   */
  async detectConfigFiles() {
    const configs = {
      'tsconfig.json': () => this.context.languages.add('typescript'),
      'jsconfig.json': () => this.context.languages.add('javascript'),
      'go.mod': () => this.context.languages.add('go'),
      'requirements.txt': () => this.context.languages.add('python'),
      'pyproject.toml': () => this.context.languages.add('python'),
      'Cargo.toml': () => this.context.languages.add('rust'),
      'pom.xml': () => this.context.languages.add('java'),
      'build.gradle': () => this.context.languages.add('java'),
      'next.config.js': () => this.context.frameworks.add('nextjs'),
      'next.config.mjs': () => this.context.frameworks.add('nextjs'),
      'vue.config.js': () => this.context.frameworks.add('vue'),
      'nuxt.config.ts': () => this.context.frameworks.add('nuxt'),
      'angular.json': () => this.context.frameworks.add('angular'),
      '.eslintrc.js': () => this.context.lintConfig = 'eslint',
      '.eslintrc.json': () => this.context.lintConfig = 'eslint',
      'eslint.config.js': () => this.context.lintConfig = 'eslint',
      '.prettierrc': () => this.context.lintConfig = 'prettier',
      '.prettierrc.json': () => this.context.lintConfig = 'prettier'
    };

    for (const [file, handler] of Object.entries(configs)) {
      if (fs.existsSync(path.join(this.projectPath, file))) {
        this.context.detectedFiles.push(file);
        handler();
      }
    }
  }

  /**
   * 分析源代码文件（抽样）
   */
  async detectSourceFiles() {
    const srcPaths = ['src', 'lib', 'app', 'pages', 'components', 'server'];
    
    for (const srcPath of srcPaths) {
      const fullPath = path.join(this.projectPath, srcPath);
      if (!fs.existsSync(fullPath)) continue;

      try {
        const files = this.walkSync(fullPath);
        
        // 统计扩展名
        const extensions = files
          .map(f => path.extname(f))
          .filter(ext => ext);
        
        const extCount = {};
        extensions.forEach(ext => { extCount[ext] = (extCount[ext] || 0) + 1; });
        
        // 根据扩展名推断语言
        if (extCount['.tsx'] || extCount['.ts']) {
          this.context.languages.add('typescript');
        } else if (extCount['.jsx'] || extCount['.js']) {
          this.context.languages.add('javascript');
        }
        if (extCount['.py']) this.context.languages.add('python');
        if (extCount['.go']) this.context.languages.add('go');
        if (extCount['.rs']) this.context.languages.add('rust');
        if (extCount['.vue']) this.context.frameworks.add('vue');
        if (extCount['.svelte']) this.context.frameworks.add('svelte');
        
        break; // 只检查第一个存在的源码目录
      } catch (err) {
        // 忽略权限错误等
        continue;
      }
    }
  }

  /**
   * 递归遍历目录
   */
  walkSync(dir, filelist = [], depth = 0) {
    // 限制递归深度，避免遍历太深
    if (depth > 5) return filelist;
    
    try {
      const files = fs.readdirSync(dir);
      files.forEach(file => {
        const filepath = path.join(dir, file);
        try {
          if (fs.statSync(filepath).isDirectory()) {
            if (!['node_modules', '.git', 'dist', 'build', '__pycache__', 'venv', '.venv', 'vendor'].includes(file)) {
              this.walkSync(filepath, filelist, depth + 1);
            }
          } else {
            filelist.push(filepath);
          }
        } catch (err) {
          // 忽略单个文件错误
        }
      });
    } catch (err) {
      // 忽略目录读取错误
    }
    return filelist;
  }

  /**
   * 格式化结果
   */
  formatResult() {
    return {
      languages: Array.from(this.context.languages),
      frameworks: Array.from(this.context.frameworks),
      packageManager: this.context.packageManager,
      testFramework: this.context.testFramework,
      lintConfig: this.context.lintConfig,
      detectedFiles: this.context.detectedFiles,
      recommendation: this.generateRecommendation()
    };
  }

  /**
   * 生成规范推荐
   */
  generateRecommendation() {
    const langs = Array.from(this.context.languages);
    const frameworks = Array.from(this.context.frameworks);
    
    const recommendation = [];
    
    // 语言规范
    if (langs.includes('typescript')) {
      recommendation.push('加载 TypeScript 规范');
    } else if (langs.includes('javascript')) {
      recommendation.push('加载 JavaScript 规范');
    }
    if (langs.includes('python')) {
      recommendation.push('加载 Python 规范');
    }
    if (langs.includes('go')) {
      recommendation.push('加载 Go 规范');
    }
    if (langs.includes('rust')) {
      recommendation.push('加载 Rust 规范');
    }
    
    // 框架规范
    if (frameworks.includes('react')) {
      recommendation.push('加载 React 规范');
    }
    if (frameworks.includes('vue')) {
      recommendation.push('加载 Vue 规范');
    }
    if (frameworks.includes('nextjs')) {
      recommendation.push('加载 Next.js 规范');
    }
    if (frameworks.includes('nuxt')) {
      recommendation.push('加载 Nuxt 规范');
    }
    if (frameworks.includes('angular')) {
      recommendation.push('加载 Angular 规范');
    }
    if (frameworks.includes('svelte')) {
      recommendation.push('加载 Svelte 规范');
    }
    
    if (recommendation.length === 0) {
      recommendation.push('加载通用规范');
    }
    
    return recommendation;
  }
}

// CLI 入口
if (require.main === module) {
  const projectPath = process.argv[2] || process.cwd();
  console.log(`\n🔍 分析项目: ${projectPath}\n`);
  
  const analyzer = new ProjectAnalyzer(projectPath);
  analyzer.analyze().then(result => {
    console.log('📊 分析结果:');
    console.log(JSON.stringify(result, null, 2));
  }).catch(err => {
    console.error('❌ 分析失败:', err.message);
    process.exit(1);
  });
}

module.exports = ProjectAnalyzer;