/**
 * Requirement Refiner Skill - ANFSF V1.5.0 需求分析阶段优化
 * 
 * 优化版本：v2.3-hybrid-adaptive-parser (2026-04-14)
 * 作用：Hybrid Adaptive Parser - 智能检测复杂需求，自动选择解析策略
 * 
 * @module asf-v4/skills/requirement-refiner-skill
 */

import { Skill, SkillContext } from '../core/skill';
import { RefinedGraph, RefinedModule } from '../core/types';
import { createModuleLogger } from '../utils/logger';

const logger = createModuleLogger('RequirementRefiner');

// ============================================================================
// 复杂度检测配置 - 加权评分系统
// ============================================================================

interface ComplexityRule {
  pattern: RegExp;
  weight: number;
  description: string;
}

const COMPLEXITY_RULES: ComplexityRule[] = [
  { pattern: /(多级|多层|多步).{0,5}审批|审批流|工作流|状态机/i, weight: 3, description: '多级审批流程' },
  { pattern: /(投资管理部|工程部|审计部|财务部|计划部|现场项目经理|监理)/g, weight: 1, description: '跨部门协作' },
  { pattern: /(复杂报表|多维度筛选|可视化图表|仪表盘|数据看板)/i, weight: 2, description: '复杂数据展示' },
  { pattern: /外部数据接入|API|数据转送|接口契约|第三方集成/i, weight: 2, description: '外部系统集成' },
  { pattern: /RBAC|角色权限|权限管理|用户角色定义|访问控制/i, weight: 2, description: '复杂权限体系' },
  { pattern: /(全流程|端到端|全生命周期)/i, weight: 2, description: '全流程覆盖' },
  { pattern: /(≥|大于等于|至少).{0,3}(3|三|4|四|5|五|6|六|7|七|8|八|9|九|10|十)个.{0,5}(部门|角色|模块|阶段)/i, weight: 2, description: '多实体协作' }
];

// 否定词模式 - 用于降低误判
const NEGATION_PATTERNS = [
  /不需要|无需|不要|no|without|not required|不涉及|排除|除外/i
];

// 复杂度阈值 - 超过此分数触发高级解析
const COMPLEXITY_THRESHOLD = 3;

// 模块化拆分配置
const MODULAR_SCOPE_CONFIG = [
  { name: '项目台账与拆解', scope: '阶段 1', priority: 1 },
  { name: '设计采购与报批', scope: '阶段 2', priority: 2 },
  { name: '合同管理', scope: '阶段 3', priority: 3 },
  { name: '工程实施与监理', scope: '阶段 4', priority: 4 },
  { name: '结算审计资金决算与报表', scope: '阶段 5-9', priority: 5 }
];

// ============================================================================
// Requirement Refiner Skill - Hybrid Adaptive Parser
// ============================================================================

export class RequirementRefinerSkill extends Skill {
  private mempalace: any;
  private logger: any;

  constructor(context: SkillContext) {
    super('requirement-refiner', context);
    this.mempalace = context.mempalace;
    this.logger = context.logger || console;
  }

  /**
   * 精炼需求 - 主入口 (Hybrid Adaptive Parser)
   */
  async refine(rawRequirement: string): Promise<RefinedGraph> {
    // 边界情况处理
    if (!rawRequirement || rawRequirement.trim().length === 0) {
      this.logger.warn('⚠️ 空输入，使用标准精炼');
      return this.standardRefine(rawRequirement);
    }

    // 检测复杂度并获取评分
    const complexityResult = this.analyzeComplexity(rawRequirement);
    
    this.logger.log(`📊 复杂度分析结果: score=${complexityResult.score}, isComplex=${complexityResult.isComplex}`);
    
    // 根据复杂度选择解析策略
    if (complexityResult.isComplex) {
      this.logger.log('🔍 检测到复杂需求，启用 Hybrid Adaptive Parser');
      return await this.hybridAdaptiveParse(rawRequirement, complexityResult);
    } else {
      this.logger.log('📋 简单需求，使用标准精炼流程');
      return this.standardRefine(rawRequirement);
    }
  }

  /**
   * 复杂度分析 - 加权评分 + 否定词处理
   */
  private analyzeComplexity(text: string): { isComplex: boolean; score: number; matchedRules: string[] } {
    let score = 0;
    const matchedRules: string[] = [];
    
    // 检测否定词
    const hasNegation = NEGATION_PATTERNS.some(neg => neg.test(text));
    
    // 应用复杂度规则
    for (const rule of COMPLEXITY_RULES) {
      const matches = text.match(rule.pattern);
      if (matches) {
        const ruleScore = rule.weight * (hasNegation ? -0.5 : 1);
        score += ruleScore;
        
        if (ruleScore > 0) {
          matchedRules.push(`${rule.description} (+${rule.weight})`);
        } else {
          matchedRules.push(`${rule.description} (${ruleScore}) - 否定词影响`);
        }
        
        this.logger.debug(`🎯 规则匹配: ${rule.description}, 权重: ${rule.weight}, 否定词影响: ${hasNegation}`);
      }
    }
    
    // 估算依赖深度作为额外评分
    const dependencyDepth = this.estimateDependencyDepth(text);
    if (dependencyDepth > 5) {
      const depthScore = Math.min(2, Math.floor(dependencyDepth / 5));
      score += depthScore;
      matchedRules.push(`依赖深度 (${dependencyDepth}) (+${depthScore})`);
    }
    
    return { 
      isComplex: score >= COMPLEXITY_THRESHOLD, 
      score: Math.max(0, score), // 确保分数非负
      matchedRules 
    };
  }

  /**
   * Hybrid Adaptive Parser - 高级解析策略
   */
  private async hybridAdaptiveParse(rawRequirement: string, complexity: { score: number; matchedRules: string[] }): Promise<RefinedGraph> {
    try {
      // 记录解析开始
      this.logger.log(`🚀 开始 Hybrid Adaptive 解析 (复杂度评分: ${complexity.score})`);
      this.logger.log(`📝 匹配规则: ${complexity.matchedRules.join(', ')}`);
      
      // 检测是否需要模块化拆分
      const shouldModularize = this.shouldModularize(rawRequirement, complexity);
      
      if (shouldModularize) {
        this.logger.log('📦 启用模块化拆分策略');
        return await this.splitIntoModularGraph(rawRequirement);
      } else {
        this.logger.log('🔄 使用增强型单模块解析');
        return await this.enhancedSingleModuleParse(rawRequirement);
      }
    } catch (error: any) {
      // 错误处理 - 回退到标准精炼
      this.logger.error(`❌ Hybrid Adaptive Parser 失败: ${error?.message || 'Unknown error'}`, error);
      this.logger.warn('🔄 回退到标准精炼流程');
      return this.standardRefine(rawRequirement);
    }
  }

  /**
   * 判断是否需要模块化拆分
   */
  private shouldModularize(req: string, complexity: { score: number; matchedRules: string[] }): boolean {
    // 基于部门关键词数量判断
    const departmentMatches = COMPLEXITY_RULES[1].pattern.exec(req);
    const departmentCount = departmentMatches ? departmentMatches.length : 0;
    
    // 基于复杂度评分和部门数量综合判断
    const hasMultipleDepartments = departmentCount >= 3;
    const highComplexity = complexity.score >= 5;
    
    this.logger.log(`🏢 部门检测: ${departmentCount} 个部门, 高复杂度: ${highComplexity}`);
    
    return hasMultipleDepartments || highComplexity;
  }

  /**
   * 估算依赖深度 - 复用 ContextCompressor 已有方法
   */
  private estimateDependencyDepth(req: string): number {
    try {
      const paragraphs = req.split('\n\n').length;
      const connectors = (req.match(/然后 | 之后 | 接着 | 再 | 最后 | 同时 | 并且/g) || []).length;
      const dataFlows = (req.match(/→|->|流转到 | 提交给 | 发送给/g) || []).length;
      const conditionalFlows = (req.match(/如果 | 当 | 只要 | 除非/g) || []).length;
      
      return paragraphs * 2 + connectors + dataFlows * 2 + conditionalFlows;
    } catch (error: any) {
      this.logger.warn(`⚠️ 依赖深度估算失败: ${error?.message || 'Unknown error'}`);
      return 0;
    }
  }

  /**
   * 拆分为模块化图谱
   */
  private async splitIntoModularGraph(req: string): Promise<RefinedGraph> {
    const graph = new RefinedGraph();
    
    for (const mod of MODULAR_SCOPE_CONFIG) {
      this.logger.log(`📦 创建模块：${mod.name} (${mod.scope})`);
      
      try {
        // 每个模块独立 refine
        const subGraph = await this.refineModule(req, mod);
        graph.addModule(mod.name, subGraph);
        
        // 关键：为每个模块注入独立 MemPalace Wing（解决长生命周期状态同步问题）
        await this.mempalace.createWing(`module-${mod.name}`, subGraph);
        this.logger.log(`✅ 已为模块 "${mod.name}" 创建独立 Wing`);
      } catch (error: any) {
        this.logger.error(`❌ 模块 "${mod.name}" 创建失败: ${error?.message || 'Unknown error'}`);
        // 继续处理其他模块，不中断整个流程
        const emptySubGraph = new RefinedGraph();
        emptySubGraph.metadata = { error: error?.message || 'Unknown error' };
        graph.addModule(mod.name, emptySubGraph);
      }
    }
    
    // 显式注入跨模块事务协议（复用已有 Harness 能力）
    graph.setCrossModuleProtocol('transaction-sync');
    
    this.logger.log(`✅ 模块化图谱创建完成：${graph.modules?.length || 0}个模块`);
    
    return graph;
  }

  /**
   * 增强型单模块解析
   */
  private async enhancedSingleModuleParse(req: string): Promise<RefinedGraph> {
    const graph = new RefinedGraph();
    
    try {
      // 尝试解析多种格式
      const parsedContent = await this.parseMultiFormatContent(req);
      
      // 应用模板匹配
      const templateMatch = this.matchHistoricalTemplates(parsedContent);
      if (templateMatch) {
        this.logger.log(`📋 匹配历史模板: ${templateMatch.templateId}`);
        // 应用模板逻辑
        graph.metadata = { templateId: templateMatch.templateId, confidence: templateMatch.confidence };
      }
      
      // 执行标准精炼
      const standardResult = this.standardRefine(parsedContent);
      // 合并结果
      Object.assign(graph, standardResult);
      
    } catch (error: any) {
      this.logger.warn(`⚠️ 增强解析失败，回退到标准精炼: ${error?.message || 'Unknown error'}`);
      return this.standardRefine(req);
    }
    
    return graph;
  }

  /**
   * 多格式内容解析
   */
  private async parseMultiFormatContent(req: string): Promise<string> {
    let processedContent = req;
    
    try {
      // 检测并处理 Mermaid 图表
      if (req.includes('```mermaid')) {
        this.logger.log('📊 检测到 Mermaid 图表，提取文本描述');
        // 这里可以调用专门的 Mermaid 解析器
        // 暂时保留原内容，后续可扩展
      }
      
      // 检测并处理 PlantUML
      if (req.includes('@startuml')) {
        this.logger.log('📊 检测到 PlantUML 图表，提取文本描述');
        // 暂时保留原内容，后续可扩展
      }
      
      // 检测图片引用
      const imagePattern = /!\[.*?\]\((.*?)\)/g;
      const images = [...req.matchAll(imagePattern)];
      if (images.length > 0) {
        this.logger.log(`🖼️ 检测到 ${images.length} 张图片，可能需要 OCR 处理`);
        // 暂时保留原内容，后续可扩展
      }
      
    } catch (error: any) {
      this.logger.warn(`⚠️ 多格式解析警告: ${error?.message || 'Unknown error'}`);
    }
    
    return processedContent;
  }

  /**
   * 历史模板匹配
   */
  private matchHistoricalTemplates(content: string): { templateId: string; confidence: number } | null {
    // 简单的模板匹配逻辑
    const templates = [
      { id: 'fixed-asset-investment', keywords: ['固定资产投资', '投资计划', '资金计划'], threshold: 2 },
      { id: 'project-management', keywords: ['项目管理', '任务分配', '进度跟踪'], threshold: 2 },
      { id: 'hr-system', keywords: ['人力资源', '员工管理', '考勤系统'], threshold: 2 }
    ];
    
    for (const template of templates) {
      const matches = template.keywords.filter(keyword => content.includes(keyword)).length;
      if (matches >= template.threshold) {
        const confidence = Math.min(1.0, matches / template.keywords.length);
        return { templateId: template.id, confidence };
      }
    }
    
    return null;
  }

  /**
   * 精炼模块子图谱 - 复用原有实现
   */
  private async refineModule(req: string, mod: any): Promise<RefinedGraph> {
    const subGraph = new RefinedGraph();
    subGraph.metadata = {
      moduleName: mod.name,
      scope: mod.scope,
      priority: mod.priority,
      isModular: true
    };
    
    // 提取模块相关需求并精炼
    const moduleReq = this.extractModuleRequirement(req, mod.name);
    // ... 原有精炼逻辑
    
    return subGraph;
  }

  /**
   * 提取模块相关需求
   */
  private extractModuleRequirement(req: string, moduleName: string): string {
    // 基于模块名关键词提取相关段落
    const keywords = this.getModuleKeywords(moduleName);
    const paragraphs = req.split('\n\n');
    const relevant = paragraphs.filter(p => 
      keywords.some(k => p.includes(k))
    );
    return relevant.join('\n\n');
  }

  /**
   * 获取模块关键词
   */
  private getModuleKeywords(moduleName: string): string[] {
    const keywordMap: Record<string, string[]> = {
      '项目台账与拆解': ['立项', '台账', '拆解', '准备'],
      '设计采购与报批': ['设计', '采购', '报批', '招标'],
      '合同管理': ['合同', '签订', '审批', '台账'],
      '工程实施与监理': ['施工', '实施', '监理', '进度', '质量'],
      '结算审计资金决算与报表': ['竣工', '结算', '审计', '资金', '决算', '报表']
    };
    return keywordMap[moduleName] || [];
  }

  /**
   * 标准精炼流程 - 原有实现保持不变
   */
  private standardRefine(req: string): RefinedGraph {
    // 原有标准精炼逻辑
    const graph = new RefinedGraph();
    // ... 原有实现
    return graph;
  }
}

// ============================================================================
// 回滚机制 - Evolution Harness 集成
// ============================================================================

export class HybridParserRollback {
  private readonly ROLLBACK_THRESHOLD = 0.93;
  private readonly OBSERVATION_WINDOW = 3; // 观察3天
  
  async shouldRollback(): Promise<boolean> {
    try {
      const stats = await this.getParseAccuracyStats(this.OBSERVATION_WINDOW);
      
      // 连续3天准确率低于阈值 → 自动回滚
      if (stats.dailyAccuracy.every(a => a < this.ROLLBACK_THRESHOLD)) {
        await this.rollbackToV21();
        await this.notifyTeam({
          reason: `Parse accuracy below ${this.ROLLBACK_THRESHOLD} for ${this.OBSERVATION_WINDOW} days`,
          stats
        });
        return true;
      }
      return false;
    } catch (error) {
      logger.error('回滚检查失败:', error);
      return false;
    }
  }
  
  private async getParseAccuracyStats(days: number): Promise<{ dailyAccuracy: number[] }> {
    // 模拟获取准确率统计
    // 实际实现需要从监控系统获取数据
    return { dailyAccuracy: [0.95, 0.94, 0.96] }; // 示例数据
  }
  
  private async rollbackToV21(): Promise<void> {
    // 1. 备份当前版本
    await this.backupCurrentVersion();
    
    // 2. 恢复v2.1代码
    await this.gitRevertToV21();
    
    // 3. 重新部署
    await this.deploy();
    
    // 4. 记录回滚事件
    await this.recordChangeEvent({ type: 'rollback', from: 'hybrid-v2.3', to: 'v2.1' });
  }
  
  private async backupCurrentVersion(): Promise<void> {
    logger.info('💾 备份当前版本...');
    // 实际备份逻辑
  }
  
  private async gitRevertToV21(): Promise<void> {
    logger.info('↩️ 回滚到 v2.1 版本...');
    // 实际 Git 回滚逻辑
  }
  
  private async deploy(): Promise<void> {
    logger.info('🚀 重新部署...');
    // 实际部署逻辑
  }
  
  private async recordChangeEvent(event: any): Promise<void> {
    logger.info('📝 记录变更事件:', event);
    // 实际记录逻辑
  }
  
  private async notifyTeam(notification: any): Promise<void> {
    logger.info('📢 通知团队:', notification);
    // 实际通知逻辑
  }
}

// ============================================================================
// 导出
// ============================================================================

export function createRequirementRefinerSkill(context: SkillContext): RequirementRefinerSkill {
  return new RequirementRefinerSkill(context);
}

export function createHybridParserRollback(): HybridParserRollback {
  return new HybridParserRollback();
}