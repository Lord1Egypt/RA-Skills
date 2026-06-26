import { SemanticDomain } from '../core/types';

// --- Interfaces ---

export interface TaskDefinition {
  id: string;
  name: string;
  description: string;
  version: string;
  ownerId: string;
  
  schedule: {
    type: 'CRON' | 'INTERVAL' | 'EVENT' | 'MANUAL';
    cron?: string;
    intervalMs?: number;
    eventPatterns?: string[];
    timezone?: string;
    enabled: boolean;
    maxConcurrent: number;
    retry: {
      maxAttempts: number;
      backoffMs: number;
      backoffMultiplier: number;
    };
  };
  
  inputs: {
    schema: {
      type: 'object';
      properties: Record<string, any>;
      required: string[];
    };
    example?: Record<string, any>;
    smfSignature?: number[];
  };
  
  output: {
    schema: { type: 'object'; properties: Record<string, any>; };
    format: 'JSON' | 'TEXT' | 'MARKDOWN' | 'HTML' | 'BINARY';
    storage: {
      toConversation?: boolean;
      toGMF?: boolean;
      toContentStore?: boolean;
      webhookUrl?: string;
    };
  };
  
  preferredModel: {
    provider: 'openai' | 'anthropic' | 'local-llama' | 'vertex-ai' | 'any';
    modelName?: string;
  };
  
  requiredServices: Array<{
    serviceId: string;
    required: boolean;
  }>;
  
  requiredSkills: string[];
  semanticDomain: SemanticDomain;
  requiredTier: 'Neophyte' | 'Adept' | 'Magus' | 'Archon';
  
  prompt: {
    system: string;
    userTemplate: string;
  };
  
  validation: {
    preExecution: Array<{ type: string; config?: any; errorMessage: string; }>;
    postExecution: Array<{ type: string; config?: any; errorMessage: string; action: 'FAIL' | 'WARN' | 'RETRY'; }>;
    minCoherence: number;
    timeoutMs: number;
  };
  
  tags: string[];
  category: string;
}

export interface TaskExecution {
  executionId: string;
  taskId: string;
  conversationId?: string;
  triggeredBy: string;
  input: Record<string, any>;
  status: 'PENDING' | 'VALIDATING' | 'RUNNING' | 'AWAITING_SERVICE' | 'COMPLETED' | 'FAILED' | 'CANCELLED' | 'TIMEOUT';
  executorNodeId: string;
  sriaSessionId?: string;
  timeline: {
    scheduledAt: number;
    startedAt?: number;
    completedAt?: number;
  };
  attempts: {
    current: number;
    max: number;
    history: Array<{
      attemptNumber: number;
      startedAt: number;
      endedAt: number;
      status: string;
      error?: string;
    }>;
  };
  output?: {
    data: any;
    format: string;
    smfSignature: number[];
    coherence: number;
  };
  error?: {
    code: string;
    message: string;
    recoverable: boolean;
  };
}

// --- Task Manager ---

export class TaskManager {
  private tasks: Map<string, TaskDefinition> = new Map();
  private executions: Map<string, TaskExecution> = new Map();
  private scheduleInterval: NodeJS.Timeout | null = null;

  constructor(
      private gun: any, 
      private localNodeId: string
  ) {
      // Start scheduling loop
      this.scheduleInterval = setInterval(() => this.pollSchedules(), 60000); // Check every minute
  }

  public registerTask(task: TaskDefinition): void {
      this.tasks.set(task.id, task);
      // Persist to Gun
      this.gun.get('tasks').get(task.id).put({ definition: task });
  }

  public async executeTask(
      taskId: string, 
      input: Record<string, any>, 
      context: { triggeredBy: string; conversationId?: string }
  ): Promise<TaskExecution> {
      const task = this.tasks.get(taskId);
      if (!task) throw new Error(`Task ${taskId} not found`);

      const executionId = `exec-${taskId}-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`;
      const execution: TaskExecution = {
          executionId,
          taskId,
          conversationId: context.conversationId,
          triggeredBy: context.triggeredBy,
          input,
          status: 'PENDING',
          executorNodeId: this.localNodeId,
          timeline: { scheduledAt: Date.now() },
          attempts: { current: 0, max: task.schedule.retry.maxAttempts, history: [] }
      };
      
      this.executions.set(executionId, execution);
      this.runExecution(execution, task); // Fire and forget (async)
      
      return execution;
  }

  private async runExecution(execution: TaskExecution, task: TaskDefinition) {
      execution.status = 'RUNNING';
      execution.timeline.startedAt = Date.now();
      execution.attempts.current++;

      try {
          // 1. Validation
          this.validateInput(execution.input, task.inputs.schema); // Mock validator
          
          // 2. Build Prompt
          const prompt = this.buildPrompt(task, execution.input);
          
          // 3. Mock Execution (Integration with SRIA would happen here)
          // const result = await this.sriaEngine.process(prompt, ...);
          const result = { 
              output: `Simulated output for ${task.name}`, 
              coherence: 0.95,
              smf: new Array(16).fill(0) 
          }; // Mock result

          // 4. Output processing
          execution.output = {
              data: result.output,
              format: task.output.format,
              smfSignature: result.smf,
              coherence: result.coherence
          };
          execution.status = 'COMPLETED';
          execution.timeline.completedAt = Date.now();

      } catch (error: any) {
          execution.status = 'FAILED';
          execution.error = {
              code: 'EXEC_ERR',
              message: error.message,
              recoverable: true
          };

          // Retry logic
          if (execution.attempts.current < execution.attempts.max) {
             const delay = task.schedule.retry.backoffMs * Math.pow(task.schedule.retry.backoffMultiplier, execution.attempts.current - 1);
             setTimeout(() => this.runExecution(execution, task), delay);
          }
      }

      // Update Gun
      // this.gun.get('tasks').get(taskId).get('executions').get(execution.executionId).put(execution);
  }

  private validateInput(input: any, schema: any) {
      // Basic validation stub
      if (schema.required) {
          for (const req of schema.required) {
              if (input[req] === undefined) throw new Error(`Missing required input: ${req}`);
          }
      }
  }

  private buildPrompt(task: TaskDefinition, input: Record<string, any>): string {
      let prompt = task.prompt.userTemplate;
      for (const [key, value] of Object.entries(input)) {
        prompt = prompt.replace(new RegExp(`{{${key}}}`, 'g'), String(value));
      }
      return prompt;
  }

  // --- Scheduler ---

  private pollSchedules() {
      const now = new Date();
      for (const task of this.tasks.values()) {
          if (!task.schedule.enabled) continue;
          
          if (task.schedule.type === 'CRON' && task.schedule.cron) {
              if (this.isCronDue(task.schedule.cron, now)) {
                  this.triggerScheduledTask(task);
              }
          } else if (task.schedule.type === 'INTERVAL' && task.schedule.intervalMs) {
              // Interval check (simplified, really needs last run time from DB)
              // Assuming memory-only for this demo:
              // Use setInterval for intervals usually, but here we poll.
          }
      }
  }

  private triggerScheduledTask(task: TaskDefinition) {
      // Check concurrency limits, etc.
      console.log(`Triggering scheduled task: ${task.name}`);
      this.executeTask(task.id, {}, { triggeredBy: 'system-scheduler' });
  }

  /**
   * Simple Cron Parser (Minute Hour Day Month DayOfWeek)
   * Supports: asterisk (all), value (exact), asterisk/step (step), list (1,2)
   */
  private isCronDue(cron: string, date: Date): boolean {
      const parts = cron.split(' ');
      if (parts.length !== 5) return false;

      const [min, hour, dom, mon, dow] = parts;
      
      const match = (val: number, pattern: string) => {
          if (pattern === '*') return true;
          if (pattern.includes('/')) {
              const [base, step] = pattern.split('/');
              // Handle */step
              if (base === '*') return val % parseInt(step) === 0;
              // Handle range/step? Simplified to just *
              return false;
          }
          if (pattern.includes(',')) {
              return pattern.split(',').map(Number).includes(val);
          }
          return parseInt(pattern) === val;
      };

      return match(date.getMinutes(), min) &&
             match(date.getHours(), hour) &&
             match(date.getDate(), dom) &&
             match(date.getMonth() + 1, mon) && // Month is 0-indexed in JS
             match(date.getDay(), dow);
  }
  
  public stop() {
      if (this.scheduleInterval) clearInterval(this.scheduleInterval);
  }
}
