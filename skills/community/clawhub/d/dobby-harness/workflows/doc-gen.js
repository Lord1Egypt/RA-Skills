/**
 * Documentation Generation Workflow - 文档生成工作流
 * 
 * 功能：
 * - 自动生成 API 文档
 * - 生成 README
 * - 生成使用示例
 * - 生成变更日志
 * - 更新文档索引
 * 
 * @example
 * const result = await docGenWorkflow({
 *   files: ['src/*.js'],
 *   output: 'docs/api',
 *   format: 'markdown',
 *   includeExamples: true,
 * });
 */

import { HarnessOrchestrator } from '../harness/orchestrator.js';
import { createValidator, validators } from '../harness/utils/validator.js';

// ============================================================================
// 配置
// ============================================================================

const DEFAULT_CONFIG = {
  maxParallel: 5,
  timeoutSeconds: 300,
  format: 'markdown',  // markdown | html | pdf
  output: 'docs',
  includeExamples: true,
  includeTypes: true,
  autoCommit: false,
  language: 'zh-CN',
};

// ============================================================================
// 文档模板
// ============================================================================

const DOC_TEMPLATES = {
  api: `
# {componentName} API

## 概述

{description}

## 安装

\`\`\`bash
{installation}
\`\`\`

## 使用方法

\`\`\`javascript
{usage}
\`\`\`

## API 参考

{apiReference}

## 示例

{examples}

## 常见问题

{faq}
`,

  readme: `
# {projectName}

![Version](https://img.shields.io/badge/version-{version}-blue)
![License](https://img.shields.io/badge/license-{license}-green)

## 📖 简介

{description}

## ✨ 特性

{features}

## 🚀 快速开始

{quickstart}

## 📚 文档

- [API 文档]({apiDocs})
- [使用指南]({guide})
- [示例代码]({examples})

## 📦 安装

{installation}

## 💡 使用示例

{examples}

## 🤝 贡献

{contributing}

## 📄 许可证

{license}
`,

  changelog: `
# 变更日志

## {version} ({date})

### 新增

{features}

### 改进

{improvements}

### 修复

{fixes}

### 破坏性变更

{breaking}
`,
};

// ============================================================================
// 文档生成工作流类
// ============================================================================

export class DocGenWorkflow {
  constructor(config = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.orchestrator = new HarnessOrchestrator({
      maxParallel: this.config.maxParallel,
      timeoutSeconds: this.config.timeoutSeconds,
      retryAttempts: 2,
    });
  }

  /**
   * 执行文档生成
   * 
   * @param {Object} options
   * @param {Array} options.files - 源文件列表
   * @param {string} options.output - 输出目录
   * @param {string} options.format - 输出格式
   * @returns {Promise<Object>} 生成结果
   */
  async execute(options) {
    const { files = [], output = this.config.output } = options;

    console.log(`[DocGen] Starting documentation generation`);
    console.log(`[DocGen] Files: ${files.length}, Output: ${output}`);

    // 分析代码
    const analysis = await this.analyzeCode(files);

    // 构建子任务
    const subTasks = this.buildSubTasks(analysis, options);

    // 执行生成
    const result = await this.orchestrator.execute({
      task: `生成项目文档`,
      pattern: 'pipeline',
      subTasks,
    });

    // 整合文档
    const docs = this.consolidateDocs(result, analysis);

    return {
      success: result.success,
      docs,
      rawResult: result,
    };
  }

  /**
   * 分析代码
   */
  async analyzeCode(files) {
    // TODO: 实际实现应该解析代码注释和结构
    const analysis = {
      projectName: this.extractProjectName(),
      version: '1.0.0',
      description: '项目描述',
      components: [],
      apis: [],
      examples: [],
    };

    for (const file of files) {
      analysis.components.push({
        file,
        name: this.extractComponentName(file),
        description: '组件描述',
        functions: [
          {
            name: 'mainFunction',
            params: [{ name: 'arg1', type: 'string' }],
            returns: 'Promise<void>',
            description: '函数描述',
          },
        ],
      });
    }

    return analysis;
  }

  /**
   * 提取项目名
   */
  extractProjectName() {
    return 'my-project';
  }

  /**
   * 提取组件名
   */
  extractComponentName(filePath) {
    const match = filePath.match(/\/([^/]+)\.(js|ts|py)$/);
    return match ? match[1] : 'Unknown';
  }

  /**
   * 构建子任务
   */
  buildSubTasks(analysis, options) {
    const subTasks = [];

    // 1. 生成 API 文档
    for (const component of analysis.components) {
      subTasks.push({
        task: `生成 ${component.name} 的 API 文档`,
        agent: 'doc-writer-agent',
        context: {
          component,
          format: this.config.format,
          template: DOC_TEMPLATES.api,
          includeExamples: this.config.includeExamples,
          includeTypes: this.config.includeTypes,
        },
        priority: 1,
      });
    }

    // 2. 生成 README
    subTasks.push({
      task: '生成项目 README.md',
      agent: 'doc-writer-agent',
      context: {
        project: analysis,
        template: DOC_TEMPLATES.readme,
        language: this.config.language,
      },
      priority: 2,
    });

    // 3. 生成使用示例
    if (this.config.includeExamples) {
      subTasks.push({
        task: '生成使用示例代码',
        agent: 'example-writer-agent',
        context: {
          components: analysis.components,
          format: 'javascript',
        },
        priority: 3,
      });
    }

    // 4. 生成变更日志
    subTasks.push({
      task: '生成 CHANGELOG.md',
      agent: 'doc-writer-agent',
      context: {
        project: analysis,
        template: DOC_TEMPLATES.changelog,
      },
      priority: 4,
    });

    return subTasks;
  }

  /**
   * 整合文档
   */
  consolidateDocs(result, analysis) {
    const docs = [];

    for (const output of (result.outputs || [])) {
      docs.push({
        file: output.docFile,
        content: output.docContent,
        type: output.docType,
        size: output.docContent?.length || 0,
      });
    }

    return docs;
  }

  /**
   * 保存文档文件
   */
  async saveDocs(docs, outputDir = this.config.output) {
    const saved = [];

    for (const doc of docs) {
      const filePath = `${outputDir}/${doc.file}`;
      console.log(`[DocGen] Would save doc: ${filePath}`);
      // await fs.writeFile(filePath, doc.content);
      saved.push(filePath);
    }

    return saved;
  }

  /**
   * 生成文档索引
   */
  generateIndex(docs) {
    const index = {
      timestamp: new Date().toISOString(),
      totalDocs: docs.length,
      byType: {},
      files: [],
    };

    for (const doc of docs) {
      const type = doc.type || 'other';
      if (!index.byType[type]) {
        index.byType[type] = 0;
      }
      index.byType[type]++;
      index.files.push({
        file: doc.file,
        type,
        size: doc.size,
      });
    }

    return index;
  }

  /**
   * 生成文档报告
   */
  generateReport(docs, analysis) {
    return {
      timestamp: new Date().toISOString(),
      projectName: analysis.projectName,
      docsGenerated: docs.length,
      totalSize: docs.reduce((sum, d) => sum + d.size, 0),
      docs: docs.map(d => ({
        file: d.file,
        type: d.type,
        size: d.size,
      })),
      index: this.generateIndex(docs),
    };
  }
}

// ============================================================================
// 快捷函数
// ============================================================================

/**
 * 快速生成文档
 */
export async function generateDocs(options) {
  const workflow = new DocGenWorkflow(options.config);
  return workflow.execute(options);
}

/**
 * 生成 API 文档
 */
export async function generateApiDocs(files, options = {}) {
  const workflow = new DocGenWorkflow(options);
  return workflow.execute({
    files,
    type: 'api',
    ...options,
  });
}

/**
 * 生成 README
 */
export async function generateReadme(projectInfo, options = {}) {
  const workflow = new DocGenWorkflow(options);
  return workflow.execute({
    projectInfo,
    type: 'readme',
    ...options,
  });
}

export default DocGenWorkflow;
