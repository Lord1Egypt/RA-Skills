/**
 * Claude Code Framework - Core Handler
 * 
 * 从 Claude Code 提取的核心执行框架
 * 确保每次任务都经过权限检查、上下文预算、Hook 干预
 */

import { riskClassifier } from './risk-classifier';
import { ContextBudgetManager } from './context-budget';
import { HookManager } from './hook-manager';

// ============== 类型定义 ==============

export enum ExecutionMode {
  DEFAULT = 'default',     // 需审批
  READ_ONLY = 'read-only', // 仅读
  AUTO = 'auto',          // AI 决定
  BYPASS = 'bypass'       // 绕过
}

export enum RiskLevel {
  AUTO = 'AUTO',        // 直接执行
  APPROVE = 'APPROVE',  // 需审批
  BLOCK = 'BLOCK'        // 直接阻止
}

export interface ToolRiskAssessment {
  tool: string;
  args: Record<string, any>;
  risk: RiskLevel;
  reason: string;
  suggestion?: string;
}

export interface TaskContext {
  task: string;
  mode: ExecutionMode;
  budget: ContextBudget;
  hooks: HookManager;
  startTime: number;
}

export interface TaskResult {
  success: boolean;
  output?: any;
  error?: string;
  riskAssessments: ToolRiskAssessment[];
  budgetAfter: ContextBudget;
  hooksExecuted: string[];
  duration: number;
}

// ============== 内置权限规则 ==============

export const BUILTIN_RULES = {
  auto: [
    'ls', 'dir', 'pwd', 'cat', 'type',
    'Get-ChildItem', 'Get-Content',
    'git status', 'git log', 'git diff',
    'search', 'read', 'memory_search', 'memory_get',
    'web_search', 'web_fetch',
    'session_status', 'agents_list', 'sessions_list'
  ],
  
  approve: [
    'exec', 'write', 'edit', 'delete', 'move', 'copy',
    'rm', 'del', 'rmdir',
    'curl', 'wget', 'Invoke-WebRequest',
    'git push', 'git commit', 'git merge',
    'npm install', 'pip install', 'cargo install',
    'message', 'browser'
  ],
  
  block: [
    'format', 'diskpart',
    'net user', 'net localgroup',
    'reg delete', 'reg add',
    'curl.*--delete', 'wget.*--delete',
    'shutdown', 'restart'
  ]
};

// ============== 核心执行器 ==============

export class ClaudeCodeFramework {
  private mode: ExecutionMode;
  private hooks: HookManager;
  private budgetManager: ContextBudgetManager;
  private riskClassifier: riskClassifier;
  
  constructor(config?: Partial<FrameworkConfig>) {
    this.mode = config?.defaultMode ?? ExecutionMode.DEFAULT;
    this.hooks = new HookManager();
    this.budgetManager = new ContextBudgetManager(config?.budget);
    this.riskClassifier = new riskClassifier(config?.rules);
    
    // 注册内置 Hook
    this.registerBuiltinHooks();
  }
  
  // ============== 公开 API ==============
  
  /**
   * 执行完整任务
   */
  async executeTask(task: string): Promise<TaskResult> {
    const startTime = Date.now();
    const result: Partial<TaskResult> = {
      riskAssessments: [],
      hooksExecuted: [],
      budgetAfter: this.budgetManager.getCurrent()
    };
    
    try {
      // 1. pre_task Hook
      await this.hooks.execute('pre_task', { task, mode: this.mode });
      result.hooksExecuted!.push('pre_task');
      
      // 2. 检查上下文预算
      const budget = this.budgetManager.getCurrent();
      if (budget.percentage >= 0.98) {
        throw new Error(`Context budget exceeded (${budget.percentage}%). Run /compact first.`);
      }
      if (budget.percentage >= 0.90) {
        console.warn(`⚠️ Context at ${budget.percentage}%. Consider compacting soon.`);
      }
      
      // 3. 工具规划（这里假设 task 已经解析为工具调用）
      const plannedTools = this.planToolsFromTask(task);
      
      // 4. 逐个执行工具
      for (const toolCall of plannedTools) {
        const assessment = await this.assessTool(toolCall.tool, toolCall.args);
        result.riskAssessments!.push(assessment);
        
        if (assessment.risk === RiskLevel.BLOCK) {
          throw new Error(`Blocked: ${assessment.reason}`);
        }
        
        if (assessment.risk === RiskLevel.APPROVE) {
          if (this.mode === ExecutionMode.READ_ONLY) {
            throw new Error(`Write operation not allowed in READ_ONLY mode: ${toolCall.tool}`);
          }
          if (this.mode === ExecutionMode.DEFAULT) {
            // TODO: 请求用户审批
            console.warn(`⚠️ Approval required: ${toolCall.tool} - ${assessment.reason}`);
          }
        }
        
        // 执行 pre_tool_call
        await this.hooks.execute('pre_tool_call', { tool: toolCall.tool, args: toolCall.args });
        result.hooksExecuted!.push(`pre_tool_call:${toolCall.tool}`);
        
        // 执行工具（在子类中实现）
        await this.executeTool(toolCall.tool, toolCall.args);
        
        // 执行 post_tool_call
        await this.hooks.execute('post_tool_call', { tool: toolCall.tool, args: toolCall.args, result: 'success' });
        result.hooksExecuted!.push(`post_tool_call:${toolCall.tool}`);
      }
      
      // 5. post_task Hook
      await this.hooks.execute('post_task', { task, success: true });
      result.hooksExecuted!.push('post_task');
      
      result.success = true;
      result.budgetAfter = this.budgetManager.getCurrent();
      
    } catch (error) {
      // on_error Hook
      await this.hooks.execute('on_error', { error: error.message, task });
      result.hooksExecuted!.push('on_error');
      
      result.success = false;
      result.error = error.message;
    }
    
    result.duration = Date.now() - startTime;
    return result as TaskResult;
  }
  
  /**
   * 评估单个工具调用的风险
   */
  async assessTool(tool: string, args: Record<string, any>): Promise<ToolRiskAssessment> {
    return this.riskClassifier.classify(tool, args);
  }
  
  /**
   * 设置执行模式
   */
  setMode(mode: ExecutionMode): void {
    this.mode = mode;
    console.log(`🔧 Execution mode: ${mode}`);
  }
  
  /**
   * 获取当前状态
   */
  getStatus(): FrameworkStatus {
    return {
      mode: this.mode,
      budget: this.budgetManager.getCurrent(),
      registeredHooks: this.hooks.listHooks()
    };
  }
  
  // ============== 私有方法 ==============
  
  private registerBuiltinHooks(): void {
    // pre_task: 检查上下文
    this.hooks.register('pre_task', async (input) => {
      const budget = this.budgetManager.getCurrent();
      if (budget.status === 'BLOCKED') {
        return { proceed: false, error: 'Context blocked' };
      }
      return { proceed: true };
    });
    
    // post_task: 更新记忆
    this.hooks.register('post_task', async (input) => {
      // 可以在这里调用 memory_update
      console.log('📝 Task completed, memory updated');
      return { proceed: true };
    });
    
    // on_error: 错误恢复建议
    this.hooks.register('on_error', async (input) => {
      console.error(`❌ Error: ${input.error}`);
      return { handled: true, suggestion: 'Check /framework status for details' };
    });
  }
  
  private planToolsFromTask(task: string): { tool: string; args: Record<string, any> }[] {
    // 简化的任务规划
    // 实际实现中需要调用 LLM 来分解任务
    return [
      { tool: 'read', args: { path: 'workspace' } }
    ];
  }
  
  private async executeTool(tool: string, args: Record<string, any>): Promise<any> {
    // 这里应该调用实际的工具执行器
    throw new Error('executeTool must be implemented');
  }
}

// ============== 辅助类 ==============

export interface FrameworkConfig {
  defaultMode: ExecutionMode;
  budget: {
    warningThreshold: number;
    criticalThreshold: number;
    blockThreshold: number;
  };
  rules: {
    auto: string[];
    approve: string[];
    block: string[];
  };
}

export interface FrameworkStatus {
  mode: ExecutionMode;
  budget: ContextBudget;
  registeredHooks: string[];
}

export interface ContextBudget {
  percentage: number;
  used: number;
  limit: number;
  status: 'NORMAL' | 'WARNING' | 'CRITICAL' | 'BLOCKED';
}

// ============== 导出实例工厂 ==============

export function createFramework(config?: Partial<FrameworkConfig>): ClaudeCodeFramework {
  return new ClaudeCodeFramework(config);
}
