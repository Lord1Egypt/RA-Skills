/**
 * Core Utilities - ANFSF v2.0
 * 
 * 核心工具函数集合，提供通用的计算和验证功能
 * 
 * @module asf-v4/utils/core-utils
 */

// ============================================================================
// 成本计算工具
// ============================================================================

/**
 * 计算角色成本
 * @param role 角色对象
 * @returns 成本数值
 */
export function computeRoleCost(role: any): number {
  const baseCost = role.complexity || 1;
  const teamSize = role.teamSize || 1;
  const duration = role.duration || 1;
  
  return baseCost * teamSize * duration;
}

/**
 * 计算经济学评分
 * @param roles 角色数组
 * @param totalBudget 总预算
 * @returns 经济学评分 (0-1)
 */
export function computeEconomicsScore(roles: any[], totalBudget: number): number {
  const totalCost = roles.reduce((sum, role) => sum + computeRoleCost(role), 0);
  return Math.max(0, 1 - totalCost / totalBudget);
}

/**
 * 计算接口成本
 * @param interfaces 接口数组
 * @returns 接口总成本
 */
export function computeInterfaceCost(interfaces: any[]): number {
  return interfaces.reduce((sum, iface) => sum + (iface.complexity || 1), 0);
}

// ============================================================================
// 返工风险工具
// ============================================================================

/**
 * 预测单个任务的返工风险
 * @param task 任务对象
 * @returns 返工风险 (0-1)
 */
export function predictReworkRisk(task: any): number {
  let risk = 0;
  
  // 需求不明确增加风险
  if (!task.requirements || task.requirements.length < 3) {
    risk += 0.3;
  }
  
  // 复杂度高增加风险
  if (task.complexity > 7) {
    risk += 0.2;
  }
  
  // 团队规模小增加风险
  if (task.teamSize < 2) {
    risk += 0.2;
  }
  
  // 历史返工率高增加风险
  if (task.history?.reworkRate > 0.2) {
    risk += 0.3;
  }
  
  return Math.min(1, risk);
}

/**
 * 计算任务组的总返工风险
 * @param tasks 任务数组
 * @returns 平均返工风险
 */
export function computeTotalReworkRisk(tasks: any[]): number {
  if (tasks.length === 0) return 0;
  
  const risks = tasks.map(predictReworkRisk);
  return risks.reduce((sum, r) => sum + r, 0) / risks.length;
}

// ============================================================================
// 合同分析工具
// ============================================================================

/**
 * 确定最优角色数量
 * @param complexity 复杂度
 * @returns 角色数量
 */
export function determineOptimalRoleCount(complexity: number): number {
  if (complexity < 3) return 1;
  if (complexity < 7) return 2;
  if (complexity < 12) return 3;
  return 4;
}

/**
 * 计算合同耦合边界
 * @param roles 角色数组
 * @returns 耦合度 (0-1)
 */
export function computeContractCouplingBound(roles: any[]): number {
  const dependencies = roles.reduce((sum, role) => 
    sum + (role.dependencies?.length || 0), 0);
  return Math.min(1, dependencies / (roles.length || 1));
}

// ============================================================================
// 所有权证明工具
// ============================================================================

/**
 * 生成所有权证明
 * @param resource 资源对象
 * @returns 证明字符串
 */
export function generateOwnershipProof(resource: any): string {
  const timestamp = Date.now();
  const hash = JSON.stringify(resource) + timestamp;
  return `proof-${hash.substring(0, 16)}`;
}

/**
 * 验证证明列表
 * @param proofs 证明数组
 * @returns 验证结果
 */
export function validateProofs(proofs: any[]): boolean {
  return proofs.every(proof => 
    proof && typeof proof === 'string' && proof.startsWith('proof-')
  );
}

/**
 * 规范化资源
 * @param resource 资源对象
 * @returns 规范化后的资源
 */
export function canonicalizeResource(resource: any): any {
  const sorted = { ...resource };
  if (sorted.keywords) {
    sorted.keywords = [...sorted.keywords].sort();
  }
  return sorted;
}

// ============================================================================
// 冲突解决工具
// ============================================================================

/**
 * 解决所有权冲突
 * @param conflict 冲突对象
 * @returns 解决方案
 */
export function resolveOwnershipConflict(conflict: any): { resolved: boolean; solution: any } {
  // 简单冲突解决逻辑
  if (conflict.type === 'duplicate') {
    return {
      resolved: true,
      solution: { action: 'merge', target: conflict.primary }
    };
  }
  
  if (conflict.type === 'dependency') {
    return {
      resolved: true,
      solution: { action: 'reorder', order: conflict.dependencies }
    };
  }
  
  return { resolved: false, solution: null };
}