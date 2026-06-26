/**
 * 错误处理
 */

export class ClawCompanyError extends Error {
  constructor(message: string, public code: string, public details?: any) {
    super(message)
    this.name = 'ClawCompanyError'
  }
}

export class AgentError extends ClawCompanyError {
  constructor(agent: string, message: string, details?: any) {
    super(`${agent} Agent 失败: ${message}`, 'AGENT_ERROR', { agent, ...details })
    this.name = 'AgentError'
  }
}

export class ConfigError extends ClawCompanyError {
  constructor(message: string, details?: any) {
    super(message, 'CONFIG_ERROR', details)
    this.name = 'ConfigError'
  }
}

export class TaskError extends ClawCompanyError {
  constructor(taskId: string, message: string, details?: any) {
    super(`任务 ${taskId} 失败: ${message}`, 'TASK_ERROR', { taskId, ...details })
    this.name = 'TaskError'
  }
}

/**
 * 错误处理包装器
 */
export async function withErrorHandling<T>(
  operation: string,
  fn: () => Promise<T>
): Promise<T> {
  try {
    return await fn()
  } catch (error) {
    if (error instanceof ClawCompanyError) {
      throw error
    }
    
    throw new ClawCompanyError(
      `${operation} 失败`,
      'OPERATION_ERROR',
      { operation, error: error instanceof Error ? error.message : String(error) }
    )
  }
}
