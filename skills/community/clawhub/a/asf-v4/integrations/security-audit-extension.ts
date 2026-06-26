/**
 * ASF V4.0 OpenClaw Integration - Security Audit Extension
 * 
 * Phase 2: Integrates ASF governance checks with OpenClaw Security Audit.
 * Version: v0.9.0
 */

import { VetoEnforcer, DEFAULT_VETO_RULES } from '../../../src/core/synthesizer';
import {
  generateOwnershipProof,
  validateProofs,
  type ResourceKey,
} from '../../../src/core/synthesizer';

/**
 * Security check result.
 */
export interface SecurityCheckResult {
  /** Check name */
  name: string;
  
  /** Whether check passed */
  passed: boolean;
  
  /** Severity level */
  severity: 'info' | 'warn' | 'error' | 'critical';
  
  /** Check message */
  message: string;
  
  /** Detailed findings */
  findings?: Array<{
    resource?: string;
    issue: string;
    recommendation?: string;
  }>;
  
  /** Timestamp */
  timestamp: number;
}

/**
 * ASF Security Check definition.
 */
export interface AsfSecurityCheck {
  name: string;
  severity: 'info' | 'warn' | 'error' | 'critical';
  description: string;
  check: (context: any) => Promise<SecurityCheckResult>;
}

/**
 * Add ASF ownership proof check to OpenClaw Security Audit.
 * 
 * This check verifies that all resources have valid single-writer ownership proofs.
 */
export async function addOwnershipProofCheck(): Promise<AsfSecurityCheck> {
  const check: AsfSecurityCheck = {
    name: 'asf-ownership-proof',
    severity: 'warn',
    description: 'Verify single-writer ownership proofs for all resources',
    check: async (context: any) => {
      const resources: ResourceKey[] = context.resources || [];
      const roles = context.roles || [];
      const rules = context.ownershipRules || [];
      
      if (resources.length === 0) {
        return {
          name: 'asf-ownership-proof',
          passed: true,
          severity: 'info',
          message: 'No resources to check',
          timestamp: Date.now(),
        };
      }
      
      // Generate ownership proofs
      const proofs = generateOwnershipProof(resources, roles, rules);
      const validation = validateProofs(proofs);
      
      if (validation.valid) {
        return {
          name: 'asf-ownership-proof',
          passed: true,
          severity: 'info',
          message: `All ${resources.length} resources have valid ownership proofs`,
          timestamp: Date.now(),
        };
      }
      
      // Build findings
      const findings = validation.invalidProofs.map((proof) => ({
        resource: `${proof.resource.type}:${proof.resource.path}`,
        issue: proof.error || 'Invalid ownership proof',
        recommendation: 'Review ownership rules and resolve conflicts',
      }));
      
      return {
        name: 'asf-ownership-proof',
        passed: false,
        severity: 'warn',
        message: `${validation.invalidProofs.length} resources have invalid ownership proofs`,
        findings,
        timestamp: Date.now(),
      };
    },
  };
  
  console.log('[asf-v4/security] Added ownership proof check');
  return check;
}

/**
 * Add ASF veto check to OpenClaw Security Audit.
 * 
 * This check verifies that hard veto rules are satisfied for pending changes.
 */
export async function addVetoCheck(): Promise<AsfSecurityCheck> {
  const check: AsfSecurityCheck = {
    name: 'asf-veto-rules',
    severity: 'error',
    description: 'Check hard veto rules are satisfied for pending changes',
    check: async (context: any) => {
      const changes = context.changes || [];
      const approvals = context.approvals || [];
      
      if (changes.length === 0) {
        return {
          name: 'asf-veto-rules',
          passed: true,
          severity: 'info',
          message: 'No pending changes to check',
          timestamp: Date.now(),
        };
      }
      
      // Create veto enforcer with default rules
      const enforcer = new VetoEnforcer(DEFAULT_VETO_RULES);
      
      // Check veto rules
      const result = enforcer.enforce({ changes }, approvals);
      
      if (result.passed) {
        const warnings = result.warnings?.length || 0;
        return {
          name: 'asf-veto-rules',
          passed: true,
          severity: warnings > 0 ? 'info' : 'info',
          message:
            warnings > 0
              ? `All veto rules satisfied (${warnings} soft warnings)`
              : 'All veto rules satisfied',
          timestamp: Date.now(),
        };
      }
      
      return {
        name: 'asf-veto-rules',
        passed: false,
        severity: 'error',
        message: result.reason || 'Veto rule violation',
        findings: result.requiredRole
          ? [
              {
                issue: `Requires approval from: ${result.requiredRole}`,
                recommendation: 'Obtain required approval before proceeding',
              },
            ]
          : undefined,
        timestamp: Date.now(),
      };
    },
  };
  
  console.log('[asf-v4/security] Added veto rules check');
  return check;
}

/**
 * Add ASF rework risk check.
 * 
 * This check identifies high-risk changes that may lead to rework.
 */
export async function addReworkRiskCheck(): Promise<AsfSecurityCheck> {
  const check: AsfSecurityCheck = {
    name: 'asf-rework-risk',
    severity: 'warn',
    description: 'Identify high-risk changes that may lead to rework',
    check: async (context: any) => {
      const tasks = context.tasks || [];
      const contractChanges = context.contractChanges || [];
      
      if (tasks.length === 0) {
        return {
          name: 'asf-rework-risk',
          passed: true,
          severity: 'info',
          message: 'No tasks to analyze',
          timestamp: Date.now(),
        };
      }
      
      // Analyze rework risk
      const highRiskTasks: Array<{ task: any; risk: any }> = [];
      
      for (const task of tasks) {
        // Simple risk calculation (full implementation would use predictReworkRisk)
        let riskScore = 0;
        const factors: string[] = [];
        
        // Check for breaking contract changes
        for (const change of contractChanges) {
          if (change.breaking) {
            riskScore += 0.4;
            factors.push(`Breaking change in ${change.contractId}`);
          }
        }
        
        // Check task risk label
        if (task.risk === 'high') {
          riskScore += 0.3;
          factors.push('High risk task');
        }
        
        if (riskScore >= 0.5) {
          highRiskTasks.push({
            task,
            risk: { score: riskScore, factors },
          });
        }
      }
      
      if (highRiskTasks.length === 0) {
        return {
          name: 'asf-rework-risk',
          passed: true,
          severity: 'info',
          message: 'No high-risk tasks detected',
          timestamp: Date.now(),
        };
      }
      
      return {
        name: 'asf-rework-risk',
        passed: true, // Pass but warn
        severity: 'warn',
        message: `${highRiskTasks.length} high-risk tasks detected`,
        findings: highRiskTasks.slice(0, 5).map(({ task, risk }) => ({
          resource: task.id,
          issue: `Risk score: ${(risk.score * 100).toFixed(0)}%`,
          recommendation: risk.factors.join('; '),
        })),
        timestamp: Date.now(),
      };
    },
  };
  
  console.log('[asf-v4/security] Added rework risk check');
  return check;
}

/**
 * Add ASF interface budget check.
 * 
 * This check monitors interface budget utilization.
 */
export async function addInterfaceBudgetCheck(): Promise<AsfSecurityCheck> {
  const check: AsfSecurityCheck = {
    name: 'asf-interface-budget',
    severity: 'warn',
    description: 'Monitor interface budget utilization',
    check: async (context: any) => {
      const budgetData = context.budgetData || {};
      
      if (!budgetData.utilizationRate) {
        return {
          name: 'asf-interface-budget',
          passed: true,
          severity: 'info',
          message: 'No budget data available',
          timestamp: Date.now(),
        };
      }
      
      const utilization = budgetData.utilizationRate;
      const status =
        utilization >= 0.9 ? 'critical' : utilization >= 0.7 ? 'warning' : 'healthy';
      
      if (status === 'healthy') {
        return {
          name: 'asf-interface-budget',
          passed: true,
          severity: 'info',
          message: `Budget utilization: ${(utilization * 100).toFixed(1)}%`,
          timestamp: Date.now(),
        };
      }
      
      return {
        name: 'asf-interface-budget',
        passed: status !== 'critical',
        severity: status === 'critical' ? 'error' : 'warn',
        message: `Budget utilization critical: ${(utilization * 100).toFixed(1)}%`,
        findings: [
          {
            issue: `Used: ${budgetData.usedBudget || 0} / ${budgetData.totalBudget || 100}`,
            recommendation:
              status === 'critical'
                ? 'Immediate action required: reduce dependencies or merge roles'
                : 'Review cross-role dependencies',
          },
        ],
        timestamp: Date.now(),
      };
    },
  };
  
  console.log('[asf-v4/security] Added interface budget check');
  return check;
}

/**
 * Run all ASF security checks.
 */
export async function runAllAsfChecks(
  context: any
): Promise<SecurityCheckResult[]> {
  const checks = [
    await addOwnershipProofCheck(),
    await addVetoCheck(),
    await addReworkRiskCheck(),
    await addInterfaceBudgetCheck(),
  ];
  
  const results: SecurityCheckResult[] = [];
  
  for (const check of checks) {
    try {
      const result = await check.check(context);
      results.push(result);
    } catch (error) {
      results.push({
        name: check.name,
        passed: false,
        severity: 'error',
        message: `Check failed: ${error}`,
        timestamp: Date.now(),
      });
    }
  }
  
  return results;
}

/**
 * Get security summary.
 */
export function getSecuritySummary(
  results: SecurityCheckResult[]
): {
  totalChecks: number;
  passed: number;
  failed: number;
  bySeverity: Record<string, number>;
  hasCritical: boolean;
  hasError: boolean;
} {
  const summary = {
    totalChecks: results.length,
    passed: results.filter((r) => r.passed).length,
    failed: results.filter((r) => !r.passed).length,
    bySeverity: {} as Record<string, number>,
    hasCritical: false,
    hasError: false,
  };
  
  for (const result of results) {
    summary.bySeverity[result.severity] =
      (summary.bySeverity[result.severity] || 0) + 1;
    
    if (result.severity === 'critical') summary.hasCritical = true;
    if (result.severity === 'error') summary.hasError = true;
  }
  
  return summary;
}

// ============================================================================
// Export
// ============================================================================

export const SecurityAuditExtension = {
  addOwnershipProofCheck,
  addVetoCheck,
  addReworkRiskCheck,
  addInterfaceBudgetCheck,
  runAllAsfChecks,
  getSecuritySummary,
};

export default SecurityAuditExtension;
