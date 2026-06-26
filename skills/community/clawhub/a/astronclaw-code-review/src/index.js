/**
 * AI Code Review Assistant - 主入口文件
 * 
 * 提供智能代码审查功能：
 * 1. 代码质量分析
 * 2. 安全检查
 * 3. 性能分析
 * 4. AI智能建议
 * 5. 审查报告生成
 */

import { SimpleToolRegistry } from './tool-system/simple-registry.js';
import { CodeReviewTool } from './tools/code-review.js';
import { CodeQualityScanner } from './tools/code-quality-scanner.js';
import { SecurityAuditTool } from './tools/security-audit.js';
import { PerformanceAnalyzer } from './tools/performance-analyzer.js';
import { ReportGenerator } from './tools/report-generator.js';

/**
 * Code Review Assistant 核心类
 */
export class CodeReviewAssistant {
  constructor(config = {}) {
    this.config = {
      reviewLevel: config.reviewLevel || 'standard',
      aiEnabled: config.aiEnabled !== false,
      includeSecurity: config.includeSecurity !== false,
      includePerformance: config.includePerformance !== false,
      ...config
    };
    
    this.registry = new SimpleToolRegistry();
    this.initialized = false;
    this.stats = {
      startupTime: null,
      toolsRegistered: 0,
      totalReviews: 0
    };
  }
  
  /**
   * 初始化工具系统
   */
  async init() {
    if (this.initialized) {
      return;
    }
    
    console.log('🚀 初始化 AI Code Review Assistant...');
    const startTime = Date.now();
    
    try {
      // 注册核心工具
      this.registerCoreTools();
      
      this.stats.startupTime = Date.now() - startTime;
      this.stats.toolsRegistered = this.registry.stats.totalTools;
      this.initialized = true;
      
      console.log(`✅ AI Code Review Assistant 初始化完成`);
      console.log(`📊 注册工具: ${this.stats.toolsRegistered} 个`);
      console.log(`⏱️  启动时间: ${this.stats.startupTime}ms`);
      console.log(`🔧 配置: ${JSON.stringify(this.config, null, 2)}`);
      
    } catch (error) {
      console.error('❌ AI Code Review Assistant 初始化失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 注册核心工具
   */
  registerCoreTools() {
    // 主审查工具
    this.registry.registerTool({
      name: 'CodeReview',
      description: '综合代码审查 - 质量、安全、性能多维度分析',
      category: 'review',
      execute: CodeReviewTool.execute,
      metadata: {
        version: '1.0.0',
        capabilities: ['quality', 'security', 'performance', 'ai-suggestions']
      }
    });
    
    // 专项工具
    this.registry.registerTool({
      name: 'CodeQualityScan',
      description: '代码质量专项扫描 - 规范、复杂度、重复代码检测',
      category: 'quality',
      execute: CodeQualityScanner.execute
    });
    
    this.registry.registerTool({
      name: 'SecurityAudit',
      description: '安全审计 - 漏洞检测、敏感信息扫描、依赖安全检查',
      category: 'security',
      execute: SecurityAuditTool.execute
    });
    
    this.registry.registerTool({
      name: 'PerformanceAnalysis',
      description: '性能分析 - 瓶颈识别、优化建议、内存使用分析',
      category: 'performance',
      execute: PerformanceAnalyzer.execute
    });
    
    this.registry.registerTool({
      name: 'GenerateReviewReport',
      description: '生成审查报告 - Markdown/HTML格式，包含详细建议',
      category: 'reporting',
      execute: ReportGenerator.execute
    });
  }
  
  /**
   * 执行代码审查
   */
  async reviewCode(params) {
    if (!this.initialized) {
      await this.init();
    }
    
    this.stats.totalReviews++;
    
    console.log(`🔍 开始代码审查: ${params.filePath || '代码片段'}`);
    
    const result = await this.registry.executeTool('CodeReview', params, {
      environment: process.env.NODE_ENV || 'development',
      config: this.config,
      timestamp: new Date().toISOString()
    });
    
    return result;
  }
  
  /**
   * 执行专项扫描
   */
  async scanCodeQuality(params) {
    return this.executeTool('CodeQualityScan', params);
  }
  
  async auditSecurity(params) {
    return this.executeTool('SecurityAudit', params);
  }
  
  async analyzePerformance(params) {
    return this.executeTool('PerformanceAnalysis', params);
  }
  
  async generateReport(params) {
    return this.executeTool('GenerateReviewReport', params);
  }
  
  /**
   * 通用工具执行方法
   */
  async executeTool(toolName, params) {
    if (!this.initialized) {
      await this.init();
    }
    
    return this.registry.executeTool(toolName, params, {
      environment: process.env.NODE_ENV || 'development',
      config: this.config,
      timestamp: new Date().toISOString()
    });
  }
  
  /**
   * 获取系统状态
   */
  getStatus() {
    return {
      initialized: this.initialized,
      config: this.config,
      stats: {
        ...this.stats,
        toolSystem: this.registry.getStats()
      },
      availableTools: this.registry.listTools().map(t => ({
        name: t.name,
        category: t.category,
        description: t.description
      }))
    };
  }
  
  /**
   * 列出可用工具
   */
  listTools(filter) {
    return this.registry.listTools(filter);
  }
}

/**
 * 默认导出实例（单例模式）
 */
let defaultInstance = null;

export function getCodeReviewAssistant(config) {
  if (!defaultInstance) {
    defaultInstance = new CodeReviewAssistant(config);
  }
  return defaultInstance;
}

/**
 * 工具注册函数（供AstronClaw使用）
 */
export async function setupTools(context) {
  console.log('🔧 设置 AI Code Review Assistant 工具...');
  
  const assistant = getCodeReviewAssistant();
  await assistant.init();
  
  const tools = {};
  
  // 为AstronClaw创建工具映射
  assistant.listTools().forEach(tool => {
    tools[tool.name] = {
      description: tool.description,
      parameters: {
        // 通用参数
        filePath: { type: 'string', required: false },
        code: { type: 'string', required: false },
        options: { type: 'object', required: false }
      },
      execute: async (args, ctx) => {
        const result = await assistant.executeTool(tool.name, args, ctx);
        return result.success ? result.result : { error: result.error };
      }
    };
  });
  
  console.log(`✅ 工具设置完成: ${Object.keys(tools).length} 个工具`);
  return tools;
}