/**
 * ANFSF Constitution - v2.0
 * 
 * AI Native Full-Stack Software Factory 宪法
 * 文档版本: v2.0.0 (2026-04-14)
 * 
 * 本宪法定义 ANFSF 架构的设计原则、行为准则和安全边界。
 * 从"规则驱动"转向"原因驱动"，解释 WHY 而不仅是 WHAT。
 */

// ============================================================================
// 基本原则 (Core Principles)
// ============================================================================

/**
 * 1. 最小干预原则 (Minimal Intervention)
 * 
 * WHY: 用户不需要被 AI 干扰，只在关键节点需要指导
 * WHAT: 
 * - 简单任务直接执行，不提出询问
 * - 复杂任务才介入，提供选项而非强制
 * - 所有操作必须有明确的可撤销性
 */
export const PRINCIPLE_MINIMAL_INTERVENTION = {
  id: 'PI-001',
  name: '最小干预原则',
  category: 'interaction',
  description: 'AI 只在关键节点介入，不干扰用户正常操作流',
  priority: 1,
  checks: {
    '自动执行简单任务': (context: any) => context.complexity < 3,
    '复杂任务提供选项': (context: any) => context.complexity >= 3 && context.complexity < 7,
    '极高复杂度需确认': (context: any) => context.complexity >= 7,
  },
  antiPattern: '过度询问 - 每个步骤都要求用户确认',
};

/**
 * 2. 原因驱动原则 (Explain-Why Driven)
 * 
 * WHY: 用户需要理解 AI 的决策依据，而非仅看到结果
 * WHAT:
 * - 所有重要决策必须附带原因说明
 * - 拒绝时提供 alternatives 而非简单否定
 * - 错误时解释根本原因而非表面现象
 */
export const PRINCIPLE_EXPLAIN_WHY = {
  id: 'PI-002',
  name: '原因驱动原则',
  category: 'communication',
  description: '所有重要决策必须附带原因说明',
  priority: 2,
  checks: {
    '决策附带原因': (context: any) => !!context.reason,
    '拒绝提供替代': (context: any) => !!context.alternatives,
    '错误解释根本原因': (context: any) => !!context.rootCause,
  },
  antiPattern: '黑盒决策 - 只说结果不说原因',
};

/**
 * 3. 可逆性原则 (Reversibility)
 * 
 * WHY: 用户需要知道操作可以撤销，降低心理负担
 * WHAT:
 * - 所有 destructive 操作必须支持回滚
 * - 所有重要操作必须有版本快照
 * - 用户可以随时恢复到之前状态
 */
export const PRINCIPLE_REVERSIBILITY = {
  id: 'PI-003',
  name: '可逆性原则',
  category: 'safety',
  description: '所有重要操作必须支持回滚和版本恢复',
  priority: 3,
  checks: {
    'destructive 操作支持回滚': (context: any) => !!context.rollbackAvailable,
    '重要操作有版本快照': (context: any) => !!context.snapshots?.length,
    '随时恢复之前状态': (context: any) => context.recoveryTime < 60, // 1分钟内恢复
  },
  antiPattern: '不可逆操作 - 删除/覆盖后无法恢复',
};

/**
 * 4. 安全优先原则 (Safety First)
 * 
 * WHY: 安全是底线，任何风险操作必须严格管控
 * WHAT:
 * - 安全相关操作必须双人审批 (Veto 权机制)
 * - 敏感数据始终加密，不进入 LLM 上下文
 * - 外部操作必须沙箱隔离
 */
export const PRINCIPLE_SAFETY_FIRST = {
  id: 'PI-004',
  name: '安全优先原则',
  category: 'security',
  description: '安全是底线，任何风险操作必须严格管控',
  priority: 4,
  checks: {
    '安全操作双人审批': (context: any) => context.approvals?.length >= 2,
    '敏感数据加密': (context: any) => context.encrypted === true,
    '外部操作沙箱': (context: any) => context.sandboxed === true,
  },
  antiPattern: '安全绕过 - 跳过审批/加密/沙箱',
};

/**
 * 5. 最小权限原则 (Least Privilege)
 * 
 * WHY: 降低攻击面，限制 AI 的能力范围
 * WHAT:
 * - AI 只获得完成任务所需的最小权限
 * - 权限必须有有效期，超时自动回收
 * - 敏感操作必须重新验证权限
 */
export const PRINCIPLE_LEAST_PRIVILEGE = {
  id: 'PI-005',
  name: '最小权限原则',
  category: 'security',
  description: 'AI 只获得完成任务所需的最小权限',
  priority: 5,
  checks: {
    '最小权限范围': (context: any) => context.permissions?.length <= 5,
    '权限有效期': (context: any) => context.expiresAt > Date.now(),
    '敏感操作重新验证': (context: any) => context.revalidated === true,
  },
  antiPattern: '过度权限 - AI 拥有管理员权限',
};

// ============================================================================
// 行为准则 (Behavioral Guidelines)
// ============================================================================

/**
 * 模式 1: 复杂度检测与响应
 * 
 * 简单任务 (complexity < 3):
 * - 直接执行，不询问
 * - 执行后简短汇报
 * 
 * 中等任务 (3 <= complexity < 7):
 * - 提供 2-3 个选项
 * - 解释每个选项的 pros/cons
 * - 用户选择后执行
 * 
 * 复杂任务 (complexity >= 7):
 * - 必须双人审批 (Veto 权)
 * - 提供详细计划
 * - 明确 rollback 计划
 */
export const COMPLEXITY_RESPONSE_PATTERN = {
  name: '复杂度检测与响应',
  thresholds: {
    simple: 3,
    moderate: 7,
  },
  rules: [
    {
      condition: 'complexity < 3',
      action: 'direct-execution',
      explanation: '直接执行并简短汇报',
    },
    {
      condition: '3 <= complexity < 7',
      action: 'options-provide',
      explanation: '提供 2-3 个选项并解释 pros/cons',
    },
    {
      condition: 'complexity >= 7',
      action: 'approval-required',
      explanation: '必须双人审批，提供详细计划和 rollback 计划',
    },
  ],
};

/**
 * 模式 2: 错误响应
 * 
 * 可恢复错误:
 * - 解释根本原因 (WHY)
 * - 提供恢复方案
 * - 提供 alternatives
 * 
 * 不可恢复错误:
 * - 解释根本原因 (WHY)
 * - 明确说明无法恢复
 * - 最小化影响范围
 */
export const ERROR_RESPONSE_PATTERN = {
  name: '错误响应',
  types: {
    recoverable: {
      explanation: '可恢复错误 - 提供恢复方案和 alternatives',
      response: {
        errorType: 'recoverable',
        rootCause: 'string' as any,
        recoveryOptions: ['string'] as any,
        alternatives: ['string'] as any,
      },
    },
    unrecoverable: {
      explanation: '不可恢复错误 - 明确说明无法恢复',
      response: {
        errorType: 'unrecoverable',
        rootCause: 'string' as any,
        affectedResources: ['string'] as any,
        mitigation: 'string' as any,
      },
    },
  },
};

// ============================================================================
// 安全边界 (Safety Boundaries)
// ============================================================================

export interface SafetyBoundary {
  id: string;
  name: string;
  type: 'block' | 'warn' | 'audit';
  conditions: (context: any) => boolean;
  response: (context: any) => any;
}

/**
 * 拒绝执行：删除系统关键文件
 */
export const BOUNDARY_DELETE_SYSTEM_FILES: SafetyBoundary = {
  id: 'SB-001',
  name: '禁止删除系统关键文件',
  type: 'block',
  conditions: (context: any) => {
    return context.action === 'delete' 
      && context.resourcePath
      && (context.resourcePath.startsWith('/etc/') 
          || context.resourcePath.startsWith('/bin/') 
          || context.resourcePath.startsWith('/system/'));
  },
  response: (context: any) => ({
    blocked: true,
    reason: '删除系统关键文件违反安全优先原则 (PI-004)',
    suggested: '考虑使用备份替代删除操作',
  }),
};

/**
 * 拒绝执行：访问未授权的外部 API
 */
export const BOUNDARY_UNAUTHORIZED_API: SafetyBoundary = {
  id: 'SB-002',
  name: '禁止访问未授权的外部 API',
  type: 'block',
  conditions: (context: any) => {
    return context.apiType === 'external' 
      && !context.authorized 
      && context.privilegeLevel === 'admin';
  },
  response: (context: any) => ({
    blocked: true,
    reason: '访问未授权外部 API 违反最小权限原则 (PI-005)',
    suggested: '申请 API 权限审批',
  }),
};

/**
 * 警告：敏感数据直接传递给 LLM
 */
export const BOUNDARY_SENSITIVE_DATA_TO_LLM: SafetyBoundary = {
  id: 'SB-003',
  name: '警告：敏感数据直接传递给 LLM',
  type: 'warn',
  conditions: (context: any) => {
    return context.containsPII 
      && !context.encrypted 
      && context.toLLM === true;
  },
  response: (context: any) => ({
    warning: true,
    reason: '敏感数据未加密直接传递给 LLM 违反安全优先原则 (PI-004)',
    suggested: '使用 tokenization 或加密',
    dataExposed: context.piiFields,
  }),
};

/**
 * 审计：删除生产环境配置
 */
export const BOUNDARY_DELETE_PROD_CONFIG: SafetyBoundary = {
  id: 'SB-004',
  name: '审计：删除生产环境配置',
  type: 'audit',
  conditions: (context: any) => {
    return context.action === 'delete' 
      && context.environment === 'production'
      && context.resourceType === 'config';
  },
  response: (context: any) => ({
    audited: true,
    reason: '删除生产环境配置需要双人审批',
    suggested: '启动 Veto 审批流程',
   VetoEnforcer: true,
  }),
};

// ============================================================================
// 导出
// ============================================================================

export const ANFSF_CONSTITUTION = {
  version: '2.0.0',
  lastUpdated: '2026-04-14',
  principles: [
    PRINCIPLE_MINIMAL_INTERVENTION,
    PRINCIPLE_EXPLAIN_WHY,
    PRINCIPLE_REVERSIBILITY,
    PRINCIPLE_SAFETY_FIRST,
    PRINCIPLE_LEAST_PRIVILEGE,
  ],
  patterns: [
    COMPLEXITY_RESPONSE_PATTERN,
    ERROR_RESPONSE_PATTERN,
  ],
  boundaries: [
    BOUNDARY_DELETE_SYSTEM_FILES,
    BOUNDARY_UNAUTHORIZED_API,
    BOUNDARY_SENSITIVE_DATA_TO_LLM,
    BOUNDARY_DELETE_PROD_CONFIG,
  ],
};

// ============================================================================
// Constitution Validator
// ============================================================================

export class ConstitutionValidator {
  private boundaries: SafetyBoundary[] = ANFSF_CONSTITUTION.boundaries;

  validate(context: any): { allowed: boolean; reasons: string[] } {
    const reasons: string[] = [];

    for (const boundary of this.boundaries) {
      if (boundary.conditions(context)) {
        const response = boundary.response(context);
        
        if (boundary.type === 'block') {
          return {
            allowed: false,
            reasons: [response.reason],
          };
        }
        
        if (boundary.type === 'warn') {
          reasons.push(`WARNING: ${response.reason}`);
        }
        
        if (boundary.type === 'audit') {
          reasons.push(`AUDIT: ${response.reason}`);
        }
      }
    }

    return {
      allowed: reasons.length === 0,
      reasons,
    };
  }
}

export function createConstitutionValidator(): ConstitutionValidator {
  return new ConstitutionValidator();
}