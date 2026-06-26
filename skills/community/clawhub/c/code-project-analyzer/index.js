const fs = require('fs')
const path = require('path')

// 支持的项目标识文件与对应技术栈映射
const TECH_MAPPING = {
  'package.json': 'Node.js/前端',
  'pyproject.toml': 'Python',
  'go.mod': 'Go',
  'pom.xml': 'Java',
  'requirements.txt': 'Python',
  'Cargo.toml': 'Rust',
  'vue.config.js': 'Vue 前端',
  'vite.config.js': 'Vite 前端项目',
  'next.config.js': 'Next.js 项目',
  'nuxt.config.js': 'Nuxt.js 项目'
}

// 常见目录职责映射
const DIR_ROLE = {
  'src': '核心源代码目录',
  'lib': '核心库/工具函数目录',
  'dist': '编译输出目录',
  'build': '构建脚本目录',
  'scripts': '工具脚本目录',
  'tests': '测试用例目录',
  'docs': '文档目录',
  'config': '配置文件目录',
  'public': '静态资源目录',
  'assets': '静态资源目录',
  'components': '前端组件目录',
  'utils': '工具函数目录',
  'api': '接口逻辑目录',
  'routes': '路由逻辑目录',
  'models': '数据模型目录',
  'controllers': '控制器目录'
}

class ProjectAnalyzer {
  constructor(projectPath) {
    this.projectPath = path.resolve(projectPath)
    this.result = {
      projectName: path.basename(this.projectPath),
      techStack: [],
      dirStructure: [],
      coreFeatures: [],
      scenarios: [],
      principles: []
    }
  }

  // 扫描根目录识别技术栈
  async scanTechStack() {
    const files = await fs.promises.readdir(this.projectPath)
    for (const file of files) {
      if (TECH_MAPPING[file]) {
        this.result.techStack.push(TECH_MAPPING[file])
        // 读取package.json获取更多信息
        if (file === 'package.json') {
          try {
            const pkg = JSON.parse(await fs.promises.readFile(path.join(this.projectPath, file), 'utf-8'))
            this.result.coreFeatures.push(pkg.description || '未描述核心功能')
            if (pkg.scripts) {
              const scriptKeys = Object.keys(pkg.scripts)
              if (scriptKeys.includes('build')) this.result.principles.push('支持编译打包部署')
              if (scriptKeys.includes('test')) this.result.principles.push('内置自动化测试流程')
              if (scriptKeys.includes('dev')) this.result.principles.push('支持本地开发热更新')
            }
          } catch (e) {}
        }
      }
    }
    // 尝试读取README提取信息
    try {
      const readmePath = path.join(this.projectPath, 'README.md')
      if (fs.existsSync(readmePath)) {
        const readme = await fs.promises.readFile(readmePath, 'utf-8')
        // 提取前300字作为功能参考
        this.result.coreFeatures.push(readme.slice(0, 300).replace(/#/g, '').trim())
      }
    } catch (e) {}
  }

  // 扫描目录结构
  async scanDirStructure(basePath = this.projectPath, depth = 0) {
    if (depth > 2) return // 只扫描前2层目录避免过深
    const entries = await fs.promises.readdir(basePath, { withFileTypes: true })
    for (const entry of entries) {
      if (entry.name.startsWith('.') || entry.name === 'node_modules' || entry.name === 'venv') continue
      const fullPath = path.join(basePath, entry.name)
      const relativePath = path.relative(this.projectPath, fullPath)
      if (entry.isDirectory()) {
        const role = DIR_ROLE[entry.name] || '功能模块目录'
        this.result.dirStructure.push({
          path: relativePath,
          role
        })
        await this.scanDirStructure(fullPath, depth + 1)
      }
    }
  }

  // 生成最终文档
  generateDoc() {
    return `# ${this.result.projectName} 项目介绍
## 一、基础功能
${this.result.coreFeatures.length > 0 ? this.result.coreFeatures.map(f => `- ${f}`).join('\n') : '- 未提取到明确功能描述，可结合代码逻辑进一步分析'}
- 技术栈：${this.result.techStack.join('、') || '未识别到明确技术栈'}
- 目录结构说明：
${this.result.dirStructure.map(d => `  * \`${d.path}\`: ${d.role}`).join('\n')}
## 二、应用场景
- 适合需要${this.result.techStack[0] || '对应技术栈'}技术栈的同类需求开发
- 可作为同类项目的架构参考模板
- 可直接二次开发适配自定义业务需求
## 三、实现原理
- 采用模块化目录结构设计，职责分离清晰
${this.result.principles.map(p => `- ${p}`).join('\n')}
- 符合主流${this.result.techStack[0] || '技术栈'}项目开发规范
`
  }

  async run(outputPath = null) {
    await this.scanTechStack()
    await this.scanDirStructure()
    const doc = this.generateDoc()
    if (outputPath) {
      await fs.promises.writeFile(outputPath, doc, 'utf-8')
      console.log(`✅ 项目介绍文档已生成到：${outputPath}`)
    }
    return doc
  }
}

// 命令行调用入口
if (require.main === module) {
  const args = process.argv.slice(2)
  if (args.length < 1) {
    console.log('使用方法: node index.js <项目目录路径> [输出文档路径]')
    process.exit(1)
  }
  const analyzer = new ProjectAnalyzer(args[0])
  analyzer.run(args[1] || path.join(args[0], '项目介绍.md')).then(console.log)
}

module.exports = ProjectAnalyzer
