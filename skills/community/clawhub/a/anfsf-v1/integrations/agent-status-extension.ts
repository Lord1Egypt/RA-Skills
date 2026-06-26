/**
 * ASF V4.0 OpenClaw Integration - Agent Status Extension
 * 
 * Phase 2: Extends OpenClaw Agent Status with Role KPI data.
 * Version: v0.9.0
 */

import type { RoleKPISnapshot } from '../../../src/core/role/kpi-types';

/**
 * ASF V4.0 Agent Status Extension.
 * 
 * This extends OpenClaw's agent status to include ASF governance metrics.
 */
export interface AsfAgentStatusExtension {
  /** ASF V4.0 version */
  asfVersion: string;
  
  /** Role KPI data */
  roleKPI?: {
    /** Current role ID */
    roleId: string;
    
    /** KPI snapshot */
    snapshot: RoleKPISnapshot;
    
    /** Trend compared to previous period */
    trend: 'improving' | 'stable' | 'degrading';
    
    /** Triggered actions */
    triggeredActions: Array<{
      action: string;
      priority: 'low' | 'medium' | 'high';
      message: string;
    }>;
  };
  
  /** Interface budget status */
  interfaceBudget?: {
    /** Role ID */
    roleId: string;
    
    /** Total budget */
    totalBudget: number;
    
    /** Used budget */
    usedBudget: number;
    
    /** Utilization rate (0-1) */
    utilizationRate: number;
    
    /** Status */
    status: 'healthy' | 'warning' | 'critical';
    
    /** Cross-role edge count */
    crossRoleEdges: number;
  };
  
  /** Governance status */
  governance?: {
    /** Pending proposals count */
    pendingProposals: number;
    
    /** Veto violations count */
    vetoViolations: number;
    
    /** Ownership proof validity */
    ownershipProofValid: boolean;
    
    /** Last governance check timestamp */
    lastCheck: number;
  };
  
  /** Timestamp of last update */
  timestamp: number;
}

/**
 * Extend Agent Status with Role KPI data.
 * 
 * @param agentId - Agent ID to extend
 * @param kpiData - Role KPI data
 * @returns Promise resolving when extension is applied
 */
export async function extendAgentStatusWithKPI(
  agentId: string,
  kpiData: RoleKPISnapshot
): Promise<void> {
  const extension: AsfAgentStatusExtension = {
    asfVersion: '0.9.0',
    roleKPI: {
      roleId: kpiData.roleId,
      snapshot: kpiData,
      trend: kpiData.trend,
      triggeredActions: [],
    },
    timestamp: Date.now(),
  };
  
  // Determine triggered actions based on KPI
  if (kpiData.queuePressure > 1.2) {
    extension.roleKPI.triggeredActions.push({
      action: 'suggest_split',
      priority: 'high',
      message: `Queue pressure critical (${kpiData.queuePressure.toFixed(2)})`,
    });
  }
  
  if (kpiData.driftIndex > 0.35) {
    extension.roleKPI.triggeredActions.push({
      action: 'suggest_reassign',
      priority: 'high',
      message: `Drift index high (${kpiData.driftIndex.toFixed(2)})`,
    });
  }
  
  if (kpiData.conflictRate > 0.15) {
    extension.roleKPI.triggeredActions.push({
      action: 'alert',
      priority: 'medium',
      message: `Conflict rate elevated (${(kpiData.conflictRate * 100).toFixed(1)}%)`,
    });
  }
  
  try {
    // Placeholder for actual OpenClaw Agent Status API
    // await openclaw.agent.extendStatus(agentId, { asfV4: extension });
    
    console.log('[asf-v4/status] Extending agent status:', {
      agentId,
      roleKPI: extension.roleKPI?.snapshot.healthScore,
      trend: extension.roleKPI?.trend,
      triggeredActions: extension.roleKPI?.triggeredActions.length,
    });
    
    // Store in local registry for now
    await updateAgentStatusRegistry(agentId, extension);
    
  } catch (error) {
    console.error('[asf-v4/status] Failed to extend agent status:', error);
    throw error;
  }
}

/**
 * Extend Agent Status with Interface Budget data.
 */
export async function extendAgentStatusWithBudget(
  agentId: string,
  budgetData: {
    roleId: string;
    totalBudget: number;
    usedBudget: number;
    utilizationRate: number;
    status: 'healthy' | 'warning' | 'critical';
    crossRoleEdges: number;
  }
): Promise<void> {
  const existing = await getAgentStatusExtension(agentId);
  
  const extension: AsfAgentStatusExtension = {
    ...existing,
    asfVersion: '0.9.0',
    interfaceBudget: budgetData,
    timestamp: Date.now(),
  };
  
  try {
    console.log('[asf-v4/status] Extending agent status with budget:', {
      agentId,
      utilization: (budgetData.utilizationRate * 100).toFixed(1) + '%',
      status: budgetData.status,
    });
    
    await updateAgentStatusRegistry(agentId, extension);
    
  } catch (error) {
    console.error('[asf-v4/status] Failed to extend agent status:', error);
    throw error;
  }
}

/**
 * Extend Agent Status with Governance data.
 */
export async function extendAgentStatusWithGovernance(
  agentId: string,
  governanceData: {
    pendingProposals: number;
    vetoViolations: number;
    ownershipProofValid: boolean;
  }
): Promise<void> {
  const existing = await getAgentStatusExtension(agentId);
  
  const extension: AsfAgentStatusExtension = {
    ...existing,
    asfVersion: '0.9.0',
    governance: {
      ...governanceData,
      lastCheck: Date.now(),
    },
    timestamp: Date.now(),
  };
  
  try {
    console.log('[asf-v4/status] Extending agent status with governance:', {
      agentId,
      pendingProposals: governanceData.pendingProposals,
      vetoViolations: governanceData.vetoViolations,
      ownershipProofValid: governanceData.ownershipProofValid,
    });
    
    await updateAgentStatusRegistry(agentId, extension);
    
  } catch (error) {
    console.error('[asf-v4/status] Failed to extend agent status:', error);
    throw error;
  }
}

/**
 * Get extended Agent Status.
 * 
 * @param agentId - Agent ID
 * @returns Agent status extension or null if not found
 */
export async function getExtendedAgentStatus(
  agentId: string
): Promise<AsfAgentStatusExtension | null> {
  try {
    // Placeholder for actual OpenClaw Agent Status API
    // const status = await openclaw.agent.getStatus(agentId);
    // return status.asfV4 || null;
    
    const status = await getAgentStatusFromRegistry(agentId);
    return status;
    
  } catch (error) {
    console.error('[asf-v4/status] Failed to get extended agent status:', error);
    return null;
  }
}

/**
 * Get KPI summary for agent.
 */
export async function getAgentKPISummary(
  agentId: string
): Promise<{
  healthScore: number;
  trend: string;
  triggeredActions: number;
} | null> {
  const status = await getExtendedAgentStatus(agentId);
  
  if (!status?.roleKPI) {
    return null;
  }
  
  return {
    healthScore: status.roleKPI.snapshot.healthScore,
    trend: status.roleKPI.trend,
    triggeredActions: status.roleKPI.triggeredActions.length,
  };
}

/**
 * Get budget summary for agent.
 */
export async function getAgentBudgetSummary(
  agentId: string
): Promise<{
  utilizationRate: number;
  status: string;
  crossRoleEdges: number;
} | null> {
  const status = await getExtendedAgentStatus(agentId);
  
  if (!status?.interfaceBudget) {
    return null;
  }
  
  return {
    utilizationRate: status.interfaceBudget.utilizationRate,
    status: status.interfaceBudget.status,
    crossRoleEdges: status.interfaceBudget.crossRoleEdges,
  };
}

// ============================================================================
// Local Registry (for development until OpenClaw API is available)
// ============================================================================

const agentStatusRegistry = new Map<string, AsfAgentStatusExtension>();

async function updateAgentStatusRegistry(
  agentId: string,
  extension: AsfAgentStatusExtension
): Promise<void> {
  agentStatusRegistry.set(agentId, extension);
}

async function getAgentStatusFromRegistry(
  agentId: string
): Promise<AsfAgentStatusExtension | null> {
  return agentStatusRegistry.get(agentId) || null;
}

/**
 * Get all registered agent statuses.
 */
export function getAllAgentStatuses(): Map<string, AsfAgentStatusExtension> {
  return new Map(agentStatusRegistry);
}

/**
 * Clear registry.
 */
export function clearRegistry(): void {
  agentStatusRegistry.clear();
  console.log('[asf-v4/status] Registry cleared');
}

/**
 * Get registry size.
 */
export function getRegistrySize(): number {
  return agentStatusRegistry.size;
}

// ============================================================================
// Export
// ============================================================================

export const AgentStatusExtension = {
  extendAgentStatusWithKPI,
  extendAgentStatusWithBudget,
  extendAgentStatusWithGovernance,
  getExtendedAgentStatus,
  getAgentKPISummary,
  getAgentBudgetSummary,
  getAllAgentStatuses,
  clearRegistry,
  getRegistrySize,
};

export default AgentStatusExtension;
