/**
 * ASF V4.0 OpenClaw Integration Modules
 * 
 * Phase 2: Agent OS Integration utilities.
 * Version: v0.9.0
 */

// Memory Extension
export * from './memory-extension';
export { MemoryExtension } from './memory-extension';

// Agent Status Extension
export * from './agent-status-extension';
export { AgentStatusExtension } from './agent-status-extension';

// Security Audit Extension
export * from './security-audit-extension';
export { SecurityAuditExtension } from './security-audit-extension';

// Combined integration helper
import { MemoryExtension } from './memory-extension';
import { AgentStatusExtension } from './agent-status-extension';
import { SecurityAuditExtension } from './security-audit-extension';

/**
 * ASF V4.0 Integration Manager.
 * 
 * Provides unified access to all integration modules.
 */
export const IntegrationManager = {
  memory: MemoryExtension,
  agentStatus: AgentStatusExtension,
  security: SecurityAuditExtension,
};

/**
 * Initialize all integrations.
 */
export async function initializeIntegrations(): Promise<void> {
  console.log('[asf-v4/integration] Initializing integrations...');
  
  // Memory extension
  console.log(`[asf-v4/integration] Memory cache size: ${MemoryExtension.getCacheSize()}`);
  
  // Agent status extension
  console.log(`[asf-v4/integration] Agent status registry size: ${AgentStatusExtension.getRegistrySize()}`);
  
  // Security extension
  console.log('[asf-v4/integration] Security checks ready: 4');
  
  console.log('[asf-v4/integration] Integrations initialized');
}

/**
 * Cleanup all integrations.
 */
export async function cleanupIntegrations(): Promise<void> {
  console.log('[asf-v4/integration] Cleaning up integrations...');
  
  MemoryExtension.clearCache();
  AgentStatusExtension.clearRegistry();
  
  console.log('[asf-v4/integration] Integrations cleaned up');
}

export default IntegrationManager;
