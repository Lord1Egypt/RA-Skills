/**
 * ANFSF V1.5.0 - 内存模块 TypeScript 类型定义
 * 补充缺失的类型导出
 */

import { TemporalKnowledgeGraph } from './temporal_kg';
import { SimpleVectorDB } from './local_embedder';
import { MemoryStructureManager } from './structured';
import { LocalEmbedder } from './local_embedder';

// ============================================================================
// 类型扩展
// ============================================================================

export type WingType = 'project' | 'person' | 'topic';
export type HallType = 'facts' | 'events' | 'discoveries' | 'preferences' | 'advice';
export type SearchMode = 'default' | 'navigate' | 'temporal';

// ============================================================================
// 接口定义
// ============================================================================

export interface MemorySearchResult {
  id: string;
  content: string;
  score: number;
  wing: string;
  room: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface SearchOptions {
  topK?: number;
  minScore?: number;
  includeTemporal?: boolean;
  wing_filter?: string;
  room_filter?: string;
  mode?: SearchMode;
}

export interface TemporalTriple {
  subject: string;
  predicate: string;
  object: string;
  valid_from: string;
  valid_to?: string;
  created_at?: string;
}

export interface KGStats {
  totalTriples: number;
  activeTriples: number;
  subjects: number;
  predicates: number;
}

// ============================================================================
// 导出
// ============================================================================

export {
  TemporalKnowledgeGraph,
  SimpleVectorDB,
  MemoryStructureManager,
  LocalEmbedder
};
