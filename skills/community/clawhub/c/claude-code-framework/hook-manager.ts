/**
 * Hook Manager - 钩子管理器
 * 
 * 提供生命周期干预能力，参考 Claude Code 的 Hook 系统
 */

export type HookName = 
  | 'pre_task'
  | 'post_task'
  | 'pre_tool_call'
  | 'post_tool_call'
  | 'on_tool_result'
  | 'pre_compact'
  | 'post_compact'
  | 'pre_agent_spawn'
  | 'post_agent_spawn'
  | 'on_agent_message'
  | 'pre_send_message'
  | 'post_send_message'
  | 'on_error'
  | 'on_session_end';

export interface HookResult {
  proceed: boolean;
  [key: string]: any;
}

export type HookHandler = (input: any) => Promise<HookResult> | HookResult;

export interface HookConfig {
  enabled: boolean;
  priority: number;
  timeout?: number;
  continueOnError: boolean;
}

const DEFAULT_HOOK_CONFIG: HookConfig = {
  enabled: true,
  priority: 100,
  timeout: 5000,
  continueOnError: false
};

export class HookManager {
  private hooks: Map<HookName, Map<string, {
    handler: HookHandler;
    config: HookConfig;
    name: string;
  }>>;
  
  private executionLog: {
    hook: HookName;
    handler: string;
    input: any;
    output: HookResult;
    duration: number;
    error?: string;
  }[];
  
  constructor() {
    this.hooks = new Map();
    this.executionLog = [];
    
    // 初始化所有 Hook 类型
    const hookTypes: HookName[] = [
      'pre_task', 'post_task',
      'pre_tool_call', 'post_tool_call', 'on_tool_result',
      'pre_compact', 'post_compact',
      'pre_agent_spawn', 'post_agent_spawn', 'on_agent_message',
      'pre_send_message', 'post_send_message',
      'on_error', 'on_session_end'
    ];
    
    for (const type of hookTypes) {
      this.hooks.set(type, new Map());
    }
  }
  
  /**
   * 注册 Hook
   */
  register(
    name: HookName,
    handler: HookHandler,
    config: Partial<HookConfig> = {}
  ): string {
    const id = `hook_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const hookConfig = { ...DEFAULT_HOOK_CONFIG, ...config };
    
    this.hooks.get(name)!.set(id, {
      handler,
      config: hookConfig,
      name: id
    });
    
    return id;
  }
  
  /**
   * 注销 Hook
   */
  unregister(name: HookName, id: string): boolean {
    return this.hooks.get(name)!.delete(id);
  }
  
  /**
   * 执行 Hook
   */
  async execute(name: HookName, input: any): Promise<HookResult> {
    const hookMap = this.hooks.get(name);
    if (!hookMap || hookMap.size === 0) {
      return { proceed: true };
    }
    
    // 按优先级排序
    const sorted = Array.from(hookMap.values())
      .filter(h => h.config.enabled)
      .sort((a, b) => a.config.priority - b.config.priority);
    
    let result: HookResult = { proceed: true };
    let lastError: Error | undefined;
    
    for (const hook of sorted) {
      const startTime = Date.now();
      
      try {
        const timeout = hook.config.timeout ?? 5000;
        const promise = hook.handler({ ...input, ...result });
        
        // 处理超时
        const wrappedPromise = Promise.race([
          promise,
          new Promise<never>((_, reject) => 
            setTimeout(() => reject(new Error(`Hook timeout: ${hook.name}`)), timeout)
          )
        ]);
        
        result = await wrappedPromise;
        
        // 记录执行
        this.logExecution({
          hook: name,
          handler: hook.name,
          input,
          output: result,
          duration: Date.now() - startTime
        });
        
        // 如果 proceed 为 false，停止执行
        if (result.proceed === false) {
          break;
        }
        
      } catch (error) {
        lastError = error as Error;
        
        this.logExecution({
          hook: name,
          handler: hook.name,
          input,
          output: { proceed: false },
          duration: Date.now() - startTime,
          error: lastError.message
        });
        
        if (!hook.config.continueOnError) {
          throw error;
        }
      }
    }
    
    return result;
  }
  
  /**
   * 执行多个 Hook（并行）
   */
  async executeParallel(
    hooks: HookName[],
    input: any
  ): Promise<Map<HookName, HookResult>> {
    const results = new Map<HookName, HookResult>();
    
    await Promise.all(
      hooks.map(async (name) => {
        const result = await this.execute(name, input);
        results.set(name, result);
      })
    );
    
    return results;
  }
  
  /**
   * 列出所有注册的 Hook
   */
  listHooks(): { name: HookName; handlers: string[] }[] {
    return Array.from(this.hooks.entries()).map(([name, handlers]) => ({
      name,
      handlers: Array.from(handlers.keys())
    }));
  }
  
  /**
   * 获取执行日志
   */
  getLog(limit?: number): typeof this.executionLog {
    return limit ? this.executionLog.slice(-limit) : [...this.executionLog];
  }
  
  /**
   * 清空日志
   */
  clearLog(): void {
    this.executionLog = [];
  }
  
  /**
   * 启用/禁用 Hook
   */
  setEnabled(name: HookName, id: string, enabled: boolean): void {
    const hook = this.hooks.get(name)?.get(id);
    if (hook) {
      hook.config.enabled = enabled;
    }
  }
  
  private logExecution(entry: typeof this.executionLog[0]): void {
    this.executionLog.push(entry);
    
    // 保持日志大小
    if (this.executionLog.length > 1000) {
      this.executionLog = this.executionLog.slice(-500);
    }
  }
  
  /**
   * 创建 Hook 装饰器（用于函数式注册）
   */
  static hook(name: HookName, config?: Partial<HookConfig>) {
    return (target: any, propertyKey: string, descriptor: PropertyDescriptor) => {
      const originalMethod = descriptor.value;
      
      descriptor.value = async function(...args: any[]) {
        const manager = (this as any).hookManager as HookManager;
        if (manager) {
          return manager.execute(name, { method: propertyKey, args });
        }
        return originalMethod.apply(this, args);
      };
      
      return descriptor;
    };
  }
}

// ============== 预设 Hook 工厂 ==============

export const PresetHooks = {
  /**
   * 权限检查 Hook
   */
  permissionCheck(toolRiskChecker: (tool: string, args: any) => { risk: string; reason: string }): HookHandler {
    return async (input: any) => {
      if (input.tool) {
        const assessment = toolRiskChecker(input.tool, input.args);
        if (assessment.risk === 'BLOCK') {
          return { proceed: false, reason: assessment.reason, action: 'block' };
        }
        if (assessment.risk === 'APPROVE') {
          return { proceed: true, reason: assessment.reason, action: 'approve' };
        }
      }
      return { proceed: true };
    };
  },
  
  /**
   * 日志记录 Hook
   */
  logger(label: string): HookHandler {
    return async (input: any) => {
      console.log(`[${label}]`, input);
      return { proceed: true };
    };
  },
  
  /**
   * 错误恢复 Hook
   */
  errorRecovery(): HookHandler {
    return async (input: any) => {
      if (input.error) {
        console.error(`❌ Error in ${input.context}:`, input.error);
        return {
          proceed: false,
          suggestion: 'Check logs for details'
        };
      }
      return { proceed: true };
    };
  }
};
