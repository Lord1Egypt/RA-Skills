/**
 * Core Types - ANFSF 核心类型定义
 * 
 * @module asf-v4/core/types
 */

// ============================================================================
// Refined Graph Types
// ============================================================================

export interface RefinedModule {
  name: string;
  description: string;
  dependencies?: Array<{ target: string; type: string }>;
  components?: RefinedComponent[];
}

export interface RefinedComponent {
  name: string;
  type: string;
  properties?: Record<string, any>;
}

export class RefinedGraph {
  id: string;
  name: string;
  description: string;
  modules?: RefinedModule[];
  dependencies?: Array<{ source: string; target: string; type: string }>;
  crossModuleEdges?: Array<{ from: string; to: string }>;
  metadata?: {
    complexity?: number;
    isModular?: boolean;
    creationTime?: number;
    error?: string;
    templateId?: string;
    confidence?: number;
    moduleName?: string;
    scope?: string;
    priority?: number;
  };
  
  constructor(id?: string, name?: string, description?: string) {
    this.id = id || 'refined-graph-' + Date.now();
    this.name = name || 'Refined Graph';
    this.description = description || 'Auto-generated refined graph';
  }
  
  addModule(name: string, module: RefinedModule): void {
    if (!this.modules) this.modules = [];
    this.modules.push({ ...module, name });
  }
  
  setCrossModuleProtocol(protocol: string): void {
    if (!this.crossModuleEdges) this.crossModuleEdges = [];
    // 设置跨模块协议
  }
}

export interface RefinedRequirement {
  id: string;
  title: string;
  description: string;
  module?: string;
  dependencies?: string[];
  priority: number;
}

export interface RefinedStrategy {
  name: string;
  type: 'standard' | 'multi-module-orchestration';
  config: any;
}

// ============================================================================
// Context Types
// ============================================================================

export interface SkillContext {
  workspace: string;
  options?: Record<string, any>;
  courseOfAction?: string;
}

export interface TaskContext {
  id: string;
  name: string;
  deps?: string[];
  description?: string;
}

// ============================================================================
// Tool Result Types
// ============================================================================

export interface ToolResult<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  metadata?: Record<string, any>;
}

export interface TestResult {
  name: string;
  passed: boolean;
  duration: number;
  error?: string;
}

// ============================================================================
// Configuration Types
// ============================================================================

export interface SkillConfig {
  name: string;
  version: string;
  type: string;
  options?: Record<string, any>;
}

export interface HarnessConfig {
  name: string;
  type: string;
  modules: string[];
  options?: Record<string, any>;
}