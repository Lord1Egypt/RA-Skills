/**
 * MemPalace Wing Manager - ANFSF V1.5.0 优化版
 * 
 * 支持中大型项目的模块化 Wing 隔离管理
 * 
 * @module asf-v4/memory/mempalace-wing-manager
 */

import { RefinedGraph } from '../../core/types';

// ============================================================================
// Wing 配置
// ============================================================================

export interface WingConfig {
  name: string;
  scope: string;
  maxSize: number;           // 最大记忆条目数
  ttl: number;               // 生存时间（秒）
  isolation: boolean;        // 是否隔离
}

export interface WingState {
  config: WingConfig;
  entries: Map<string, any>;
  createdAt: number;
  lastAccessed: number;
  accessCount: number;
}

const DEFAULT_WING_CONFIG: Omit<WingConfig, 'name' | 'scope'> = {
  maxSize: 1000,
  ttl: 3600,  // 1 小时
  isolation: true
};

// ============================================================================
// Wing Manager
// ============================================================================

export class MemPalaceWingManager {
  private wings: Map<string, WingState>;
  private defaultConfig: typeof DEFAULT_WING_CONFIG;

  constructor() {
    this.wings = new Map();
    this.defaultConfig = DEFAULT_WING_CONFIG;
  }

  /**
   * 创建 Wing
   */
  async createWing(name: string, graph: RefinedGraph): Promise<void> {
    const config: WingConfig = {
      name,
      scope: graph.metadata?.scope || 'default',
      ...this.defaultConfig
    };

    const state: WingState = {
      config,
      entries: new Map(),
      createdAt: Date.now(),
      lastAccessed: Date.now(),
      accessCount: 0
    };

    this.wings.set(name, state);
    console.log(`🏛️ Wing 已创建：${name} (scope: ${config.scope})`);

    // 初始化 Wing 数据
    await this.initializeWing(state, graph);
  }

  /**
   * 初始化 Wing 数据
   */
  private async initializeWing(state: WingState, graph: RefinedGraph): Promise<void> {
    // 存储图谱元数据
    state.entries.set('metadata', graph.metadata);
    
    // 存储模块信息
    if (graph.modules) {
      state.entries.set('modules', graph.modules.map(m => ({
        name: m.name,
        scope: m.scope,
        dependencies: m.dependencies
      })));
    }
    
    // 存储依赖关系
    if (graph.dependencies) {
      state.entries.set('dependencies', graph.dependencies);
    }
    
    console.log(`✅ Wing ${state.config.name} 已初始化 ${state.entries.size} 条数据`);
  }

  /**
   * 获取 Wing
   */
  getWing(name: string): WingState | undefined {
    const wing = this.wings.get(name);
    if (wing) {
      wing.lastAccessed = Date.now();
      wing.accessCount++;
    }
    return wing;
  }

  /**
   * 存储数据到 Wing
   */
  set<T>(wingName: string, key: string, value: T): void {
    const wing = this.getWing(wingName);
    if (!wing) {
      throw new Error(`Wing 不存在：${wingName}`);
    }
    
    // 检查大小限制
    if (wing.entries.size >= wing.config.maxSize) {
      this.evictOldest(wing);
    }
    
    wing.entries.set(key, value);
    console.log(`📝 Wing ${wingName} 已存储：${key}`);
  }

  /**
   * 从 Wing 获取数据
   */
  get<T>(wingName: string, key: string): T | undefined {
    const wing = this.getWing(wingName);
    if (!wing) {
      return undefined;
    }
    return wing.entries.get(key);
  }

  /**
   * 清除过期 Wing
   */
  cleanupExpired(): number {
    const now = Date.now();
    let count = 0;
    
    for (const [name, state] of this.wings.entries()) {
      if (now - state.lastAccessed > state.config.ttl * 1000) {
        this.wings.delete(name);
        count++;
        console.log(`🗑️ Wing 已清除：${name}`);
      }
    }
    
    return count;
  }

  /**
   * 驱逐最旧数据
   */
  private evictOldest(wing: WingState): void {
    // 简单实现：删除第一个条目
    const firstKey = wing.entries.keys().next().value;
    if (firstKey) {
      wing.entries.delete(firstKey);
      console.log(`🗑️ Wing ${wing.config.name} 已驱逐：${firstKey}`);
    }
  }

  /**
   * 获取 Wing 状态报告
   */
  getStatus(): {
    totalWings: number;
    totalEntries: number;
    wings: Array<{
      name: string;
      scope: string;
      entries: number;
      accessCount: number;
      age: number;
    }>;
  } {
    const now = Date.now();
    let totalEntries = 0;
    
    const wings = Array.from(this.wings.entries()).map(([name, state]) => {
      totalEntries += state.entries.size;
      return {
        name: state.config.name,
        scope: state.config.scope,
        entries: state.entries.size,
        accessCount: state.accessCount,
        age: Math.round((now - state.createdAt) / 1000)
      };
    });
    
    return {
      totalWings: this.wings.size,
      totalEntries,
      wings
    };
  }
}

// ============================================================================
// 全局单例
// ============================================================================

let globalWingManager: MemPalaceWingManager | null = null;

export function getGlobalWingManager(): MemPalaceWingManager {
  if (!globalWingManager) {
    globalWingManager = new MemPalaceWingManager();
  }
  return globalWingManager;
}

// ============================================================================
// 导出
// ============================================================================

export function createWingManager(): MemPalaceWingManager {
  return new MemPalaceWingManager();
}
