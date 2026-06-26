/**
 * Dynamic Router - ANFSF V1.5.0 中大型项目优化补丁
 * 
 * 补丁版本：v2.1-minimal-patch (2026-04-12)
 * 作用：当 Graph 为模块化且跨模块依赖>8 时，自动切换到 multi-module-orchestration 策略
 * 
 * @module asf-v4/providers/dynamic-router
 */

import { RefinedGraph } from '../core/types';
import { Strategy } from '../core/strategy-config';

// ============================================================================
// 策略类型定义
// ============================================================================

export type RouterStrategy = 
  | 'standard'                    // 标准单模块策略
  | 'multi-module-orchestration'; // 多模块编排策略（复用事务协议 + 增量交付）

// ============================================================================
// Dynamic Router
// ============================================================================

export class DynamicRouter {
  /**
   * 选择执行策略
   */
  selectStrategy(graph: RefinedGraph): Strategy {
    const metadata = this.getGraphMetadata(graph);
    
    console.log(`🔍 Graph 检测：模块化=${metadata.isModular}, 跨模块依赖=${metadata.crossModuleDependencies}`);
    
    // 当 Graph 为模块化且跨模块依赖>8 时，启用多模块编排策略
    if (metadata.isModular && metadata.crossModuleDependencies > 8) {
      console.log('🚀 检测到跨模块依赖，启用 multi-module-orchestration 策略（复用事务协议 + 增量交付）');
      return this.createMultiModuleOrchestrationStrategy(graph);
    }
    
    console.log('📋 选择策略：standard（标准单模块）');
    return this.createStandardStrategy();
  }

  /**
   * 获取 Graph 元数据 - 新增辅助方法
   */
  private getGraphMetadata(graph: RefinedGraph): {
    isModular: boolean;
    crossModuleDependencies: number;
  } {
    return {
      isModular: (graph.modules && graph.modules.length > 1) ? true : false,
      crossModuleDependencies: this.countCrossModuleDeps(graph)
    };
  }

  /**
   * 计算跨模块依赖数 - 复用 GraphRAG 已有方法
   */
  private countCrossModuleDeps(graph: RefinedGraph): number {
    // 复用 GraphRAG 已有方法，统计跨模块依赖深度
    return (graph as any).crossModuleEdges?.length || 
           graph.dependencies?.length || 
           0;
  }

  /**
   * 创建多模块编排策略 - 复用 Layer 8.5 Orchestration Harness 已有能力
   */
  private createMultiModuleOrchestrationStrategy(graph: RefinedGraph): Strategy {
    return {
      name: 'multi-module-orchestration',
      type: 'orchestration',
      config: {
        // 复用已有事务协议
        transactionProtocol: true,
        
        // 增量交付
        incrementalDelivery: true,
        
        // 模块执行顺序（拓扑排序）
        executionOrder: this.computeExecutionOrder(graph),
        
        // 模块间同步点
        syncPoints: this.computeSyncPoints(graph),
        
        // 回滚策略
        rollbackStrategy: 'module-level',
        
        // 超时配置
        timeout: {
          perModule: 300,  // 每模块 5 分钟
          total: 1800      // 总计 30 分钟
        }
      }
    };
  }

  /**
   * 创建标准策略
   */
  private createStandardStrategy(): Strategy {
    return {
      name: 'standard',
      type: 'standard',
      config: {
        transactionProtocol: false,
        incrementalDelivery: false
      }
    };
  }

  /**
   * 计算模块执行顺序 - 拓扑排序
   */
  private computeExecutionOrder(graph: RefinedGraph): string[] {
    if (!graph.modules) return [];
    
    const order: string[] = [];
    const visited = new Set<string>();
    const visiting = new Set<string>();
    
    const visit = (moduleName: string) => {
      if (visited.has(moduleName)) return;
      if (visiting.has(moduleName)) {
        console.warn(`⚠️ 检测到循环依赖：${moduleName}`);
        return;
      }
      
      visiting.add(moduleName);
      
      const module = graph.modules?.find(m => m.name === moduleName);
      if (module?.dependencies) {
        for (const dep of module.dependencies) {
          visit((dep as any).target || dep);
        }
      }
      
      visiting.delete(moduleName);
      visited.add(moduleName);
      order.push(moduleName);
    };
    
    for (const module of graph.modules) {
      visit(module.name);
    }
    
    console.log(`📋 模块执行顺序：${order.join(' → ')}`);
    return order;
  }

  /**
   * 计算模块间同步点
   */
  private computeSyncPoints(graph: RefinedGraph): string[] {
    if (!graph.modules) return [];
    
    // 在每个模块完成后设置同步点
    return graph.modules.map(m => `after-${m.name}`);
  }
}

// ============================================================================
// 导出
// ============================================================================

export function createDynamicRouter(): DynamicRouter {
  return new DynamicRouter();
}
