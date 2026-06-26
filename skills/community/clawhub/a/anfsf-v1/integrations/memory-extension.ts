/**
 * ASF V4.0 OpenClaw Integration - Memory Schema Extension
 * 
 * Phase 2: Extends OpenClaw Memory to support ASF ChangeEvents.
 * Version: v0.9.0
 */

import type { ChangeEvent } from '../../../src/core/graph/types';

/**
 * ASF ChangeEvent Memory Schema.
 * 
 * This schema extends OpenClaw's memory system to store ASF governance events.
 */
export interface AsfMemoryEntry {
  /** Entry type identifier */
  type: 'asf_change_event';
  
  /** Timestamp when event occurred */
  timestamp: number;
  
  /** Event data */
  data: {
    /** Event unique ID */
    id: string;
    
    /** Action performed */
    action: 'create' | 'update' | 'delete' | 'approve' | 'reject';
    
    /** Target of the change */
    target: {
      kind: 'graph' | 'code' | 'contract';
      idOrPath: string;
    };
    
    /** Role that performed the action */
    actorRoleId: string;
    
    /** Risk score (0-100) */
    riskScore?: number;
    
    /** Blast radius (number of affected nodes) */
    blastRadius?: number;
    
    /** Heat score */
    heatScore?: number;
  };
  
  /** Tags for searching */
  tags: string[];
  
  /** Optional metadata */
  metadata?: {
    ownershipRuleId?: string;
    contractType?: string;
    projectId?: string;
  };
}

/**
 * Write ChangeEvent to OpenClaw Memory.
 * 
 * @param changeEvent - The change event to store
 * @param options - Optional metadata
 * @returns Promise resolving when write is complete
 */
export async function writeChangeToMemory(
  changeEvent: ChangeEvent,
  options: { projectId?: string; contractType?: string } = {}
): Promise<void> {
  const memoryEntry: AsfMemoryEntry = {
    type: 'asf_change_event',
    timestamp: changeEvent.ts,
    data: {
      id: changeEvent.id,
      action: changeEvent.action,
      target: changeEvent.target,
      actorRoleId: changeEvent.actorRoleId,
      riskScore: changeEvent.riskScore,
      blastRadius: changeEvent.blastRadius,
      heatScore: changeEvent.heatScore,
    },
    tags: [
      'asf-v4',
      'governance',
      'change',
      changeEvent.action,
      changeEvent.target.kind,
    ],
    metadata: {
      ownershipRuleId: changeEvent.ownershipRuleId,
      contractType: options.contractType,
      projectId: options.projectId,
    },
  };

  // OpenClaw Memory API integration
  // This would use the actual OpenClaw memory API when available
  try {
    // Placeholder for actual OpenClaw Memory API
    // await openclaw.memory.write(memoryEntry);
    
    console.log('[asf-v4/memory] Writing change event:', {
      id: memoryEntry.data.id,
      action: memoryEntry.data.action,
      target: memoryEntry.data.target.idOrPath,
      timestamp: new Date(memoryEntry.timestamp).toISOString(),
    });
    
    // Store in local cache for now
    await cacheMemoryEntry(memoryEntry);
    
  } catch (error) {
    console.error('[asf-v4/memory] Failed to write change event:', error);
    throw error;
  }
}

/**
 * Read change history from OpenClaw Memory.
 * 
 * @param options - Query options
 * @returns Array of change events
 */
export async function readChangeHistory(
  options: {
    since?: number;
    until?: number;
    limit?: number;
    tags?: string[];
    action?: string;
    projectId?: string;
  } = {}
): Promise<AsfMemoryEntry[]> {
  try {
    // Placeholder for actual OpenClaw Memory API
    // const entries = await openclaw.memory.query({
    //   type: 'asf_change_event',
    //   ...options
    // });
    
    console.log('[asf-v4/memory] Reading change history:', options);
    
    // Retrieve from local cache for now
    const entries = await getCachedMemoryEntries(options);
    
    return entries;
    
  } catch (error) {
    console.error('[asf-v4/memory] Failed to read change history:', error);
    return [];
  }
}

/**
 * Get change statistics.
 */
export async function getChangeStats(
  options: { since?: number; until?: number; projectId?: string } = {}
): Promise<{
  totalCount: number;
  byAction: Record<string, number>;
  byTargetKind: Record<string, number>;
  avgRiskScore: number;
  avgBlastRadius: number;
}> {
  const entries = await readChangeHistory(options);
  
  const stats = {
    totalCount: entries.length,
    byAction: {} as Record<string, number>,
    byTargetKind: {} as Record<string, number>,
    avgRiskScore: 0,
    avgBlastRadius: 0,
  };
  
  let riskSum = 0;
  let riskCount = 0;
  let blastSum = 0;
  let blastCount = 0;
  
  for (const entry of entries) {
    // Count by action
    const action = entry.data.action;
    stats.byAction[action] = (stats.byAction[action] || 0) + 1;
    
    // Count by target kind
    const kind = entry.data.target.kind;
    stats.byTargetKind[kind] = (stats.byTargetKind[kind] || 0) + 1;
    
    // Sum risk scores
    if (entry.data.riskScore !== undefined) {
      riskSum += entry.data.riskScore;
      riskCount++;
    }
    
    // Sum blast radius
    if (entry.data.blastRadius !== undefined) {
      blastSum += entry.data.blastRadius;
      blastCount++;
    }
  }
  
  stats.avgRiskScore = riskCount > 0 ? riskSum / riskCount : 0;
  stats.avgBlastRadius = blastCount > 0 ? blastSum / blastCount : 0;
  
  return stats;
}

/**
 * Get high-risk changes.
 */
export async function getHighRiskChanges(
  threshold: number = 70,
  options: { since?: number; limit?: number } = {}
): Promise<AsfMemoryEntry[]> {
  const entries = await readChangeHistory(options);
  return entries
    .filter((e) => (e.data.riskScore || 0) >= threshold)
    .slice(0, options.limit || 100);
}

/**
 * Get changes affecting a specific resource.
 */
export async function getChangesForResource(
  resourceId: string,
  options: { since?: number; limit?: number } = {}
): Promise<AsfMemoryEntry[]> {
  const entries = await readChangeHistory(options);
  return entries
    .filter((e) => e.data.target.idOrPath === resourceId)
    .slice(0, options.limit || 100);
}

// ============================================================================
// Local Cache (for development until OpenClaw Memory API is available)
// ============================================================================

const memoryCache: AsfMemoryEntry[] = [];

async function cacheMemoryEntry(entry: AsfMemoryEntry): Promise<void> {
  memoryCache.push(entry);
  
  // Limit cache size
  if (memoryCache.length > 10000) {
    memoryCache.splice(0, memoryCache.length - 10000);
  }
}

async function getCachedMemoryEntries(
  options: {
    since?: number;
    until?: number;
    limit?: number;
    tags?: string[];
    action?: string;
    projectId?: string;
  } = {}
): Promise<AsfMemoryEntry[]> {
  let entries = [...memoryCache];
  
  // Filter by time range
  if (options.since !== undefined) {
    entries = entries.filter((e) => e.timestamp >= options.since!);
  }
  if (options.until !== undefined) {
    entries = entries.filter((e) => e.timestamp <= options.until!);
  }
  
  // Filter by tags
  if (options.tags && options.tags.length > 0) {
    entries = entries.filter((e) =>
      options.tags!.some((tag) => e.tags.includes(tag))
    );
  }
  
  // Filter by action
  if (options.action) {
    entries = entries.filter((e) => e.data.action === options.action);
  }
  
  // Filter by project
  if (options.projectId) {
    entries = entries.filter((e) => e.metadata?.projectId === options.projectId);
  }
  
  // Sort by timestamp descending
  entries.sort((a, b) => b.timestamp - a.timestamp);
  
  // Apply limit
  if (options.limit) {
    entries = entries.slice(0, options.limit);
  }
  
  return entries;
}

/**
 * Clear local cache.
 */
export function clearCache(): void {
  memoryCache.splice(0, memoryCache.length);
  console.log('[asf-v4/memory] Cache cleared');
}

/**
 * Get cache size.
 */
export function getCacheSize(): number {
  return memoryCache.length;
}

// ============================================================================
// Export
// ============================================================================

export const MemoryExtension = {
  writeChangeToMemory,
  readChangeHistory,
  getChangeStats,
  getHighRiskChanges,
  getChangesForResource,
  clearCache,
  getCacheSize,
};

export default MemoryExtension;
