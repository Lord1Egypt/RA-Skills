import { OpenClawSkillApi } from "openclaw/skill-sdk";

interface Workflow {
  id: string;
  name: string;
  definition: WorkflowStep[];
  status: "draft" | "running" | "paused" | "completed" | "failed";
  context: Record<string, any>;
  currentStep?: number;
  startTime?: Date;
  endTime?: Date;
  error?: string;
  createdAt: Date;
}

interface WorkflowStep {
  id: string;
  name: string;
  skill: string;
  command: string;
  args: Record<string, any>;
  dependsOn?: string[]; // step IDs
  condition?: string; // expression evaluated against context
  retry?: {
    maxAttempts: number;
    delayMs: number;
  };
  timeoutMs?: number;
}

interface Execution {
  workflowId: string;
  stepId: string;
  status: "pending" | "running" | "success" | "failed" | "skipped";
  attempts: number;
  lastError?: string;
  startedAt?: Date;
  completedAt?: Date;
}

class WorkflowOrchestrator {
  private workflows: Map<string, Workflow> = new Map();
  private executions: Map<string, Execution[]> = new Map();
  private api: OpenClawSkillApi;

  constructor(api: OpenClawSkillApi) {
    this.api = api;
  }

  async createWorkflow(workflow: {
    name: string;
    steps: WorkflowStep[];
    context?: Record<string, any>;
  }): Promise<string> {
    const id = `WF-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    const wf: Workflow = {
      id,
      name: workflow.name,
      definition: workflow.steps,
      status: "draft",
      context: workflow.context || {},
      createdAt: new Date(),
    };

    this.workflows.set(id, wf);
    this.executions.set(id, []);

    this.api.log(`info`, `Workflow created: ${id} - ${workflow.name}`);
    return id;
  }

  async getWorkflow(id: string): Promise<Workflow | null> {
    return this.workflows.get(id) || null;
  }

  async listWorkflows(status?: Workflow["status"]): Promise<Workflow[]> {
    const all = Array.from(this.workflows.values());
    if (status) {
      return all.filter(w => w.status === status);
    }
    return all;
  }

  async startWorkflow(id: string, overrides?: Record<string, any>): Promise<boolean> {
    const wf = this.workflows.get(id);
    if (!wf) {
      throw new Error(`Workflow not found: ${id}`);
    }

    if (wf.status !== "draft" && wf.status !== "paused") {
      throw new Error(`Cannot start workflow in status: ${wf.status}`);
    }

    wf.status = "running";
    wf.startTime = new Date();
    wf.currentStep = 0;
    wf.context = { ...wf.context, ...overrides };
    this.workflows.set(id, wf);

    this.api.log(`info`, `Workflow started: ${id}`);

    // Begin execution in background
    this.executeWorkflow(id);

    return true;
  }

  async pauseWorkflow(id: string): Promise<boolean> {
    const wf = this.workflows.get(id);
    if (!wf) {
      throw new Error(`Workflow not found: ${id}`);
    }

    if (wf.status !== "running") {
      throw new Error(`Cannot pause workflow in status: ${wf.status}`);
    }

    wf.status = "paused";
    this.workflows.set(id, wf);

    this.api.log(`info`, `Workflow paused: ${id}`);
    return true;
  }

  async resumeWorkflow(id: string): Promise<boolean> {
    const wf = this.workflows.get(id);
    if (!wf) {
      throw new Error(`Workflow not found: ${id}`);
    }

    if (wf.status !== "paused") {
      throw new Error(`Cannot resume workflow in status: ${wf.status}`);
    }

    wf.status = "running";
    this.workflows.set(id, wf);

    this.api.log(`info`, `Workflow resumed: ${id}`);
    this.executeWorkflow(id);
    return true;
  }

  async cancelWorkflow(id: string): Promise<boolean> {
    const wf = this.workflows.get(id);
    if (!wf) {
      throw new Error(`Workflow not found: ${id}`);
    }

    wf.status = "failed";
    wf.error = "Cancelled by user";
    wf.endTime = new Date();
    this.workflows.set(id, wf);

    this.api.log(`info`, `Workflow cancelled: ${id}`);
    return true;
  }

  async getStatus(id: string): Promise<any> {
    const wf = this.workflows.get(id);
    if (!wf) {
      throw new Error(`Workflow not found: ${id}`);
    }

    const execs = this.executions.get(id) || [];
    const currentExec = wf.currentStep !== undefined 
      ? execs.find(e => e.stepId === wf.definition[wf.currentStep]?.id)
      : null;

    return {
      workflow: wf,
      currentStep: wf.currentStep !== undefined ? wf.definition[wf.currentStep] : null,
      execution: currentExec,
      completedSteps: execs.filter(e => e.status === "success").length,
      totalSteps: wf.definition.length,
      failedSteps: execs.filter(e => e.status === "failed").length
    };
  }

  async getExecutions(id: string): Promise<Execution[]> {
    return this.executions.get(id) || [];
  }

  // Built-in templates
  async createStandardAdWorkflow(params: {
    demandId: string;
    prompt: string;
    count: number;
    platforms: string[];
    targetModels?: string[];
  }): Promise<string> {
    const steps: WorkflowStep[] = [
      {
        id: "fetch-demand",
        name: "获取需求详情",
        skill: "demand-management",
        command: "demand.get",
        args: { id: params.demandId }
      },
      {
        id: "generate-assets",
        name: "AI生成素材",
        skill: "ai-generation",
        command: "ai.generate",
        args: {
          prompt: params.prompt,
          model: params.targetModels?.[0] || "flux",
          count: params.count
        },
        dependsOn: ["fetch-demand"],
        retry: { maxAttempts: 3, delayMs: 5000 }
      },
      {
        id: "auto-check",
        name: "自动质检",
        skill: "review-quality",
        command: "review.check",
        args: { materialId: "{{results.generate-assets.materialIds}}" },
        dependsOn: ["generate-assets"]
      },
      {
        id: "manual-review",
        name: "人工审核",
        skill: "review-quality",
        command: "review.submit",
        args: {
          taskId: "{{executionId}}",
          materialId: "{{results.auto-check.materialId}}",
          score: 0,
          passed: false
        },
        dependsOn: ["auto-check"],
        // Skip if auto-check score is high
        condition: "results.auto-check.score < 8"
      },
      {
        id: "prepare-delivery",
        name: "准备交付",
        skill: "delivery-distribution",
        command: "delivery.create",
        args: {
          name: "交付包-{{demand.title}}",
          materialIds: "{{results.manual-review.approvedMaterials || results.auto-check.materialIds}}",
          platforms: params.platforms,
          format: "zip"
        },
        dependsOn: ["manual-review", "auto-check"]
      },
      {
        id: "distribute",
        name: "分发到平台",
        skill: "delivery-distribution",
        command: "delivery.distribute",
        args: { id: "{{results.prepare-delivery.packageId}}" },
        dependsOn: ["prepare-delivery"]
      },
      {
        id: "record-analytics",
        name: "记录分析数据",
        skill: "analytics-feedback",
        command: "analytics.ingest",
        args: {
          materialId: "{{results.distribute.materialIds}}",
          impressions: 0, // Will be updated later via API
          clicks: 0,
          conversions: 0,
          cost: 0,
          revenue: 0
        },
        dependsOn: ["distribute"]
      }
    ];

    return this.createWorkflow({
      name: `广告生产流程 - ${params.demandId}`,
      steps: steps,
      context: { demandId: params.demandId, platforms: params.platforms }
    });
  }

  // Execution engine
  private async executeWorkflow(workflowId: string): Promise<void> {
    const wf = this.workflows.get(workflowId);
    if (!wf) return;

    const executions = this.executions.get(workflowId) || [];

    for (let i = 0; i < wf.definition.length; i++) {
      if (wf.status !== "running") {
        this.api.log(`info`, `Workflow ${workflowId} stopped (status: ${wf.status})`);
        return;
      }

      const step = wf.definition[i];
      wf.currentStep = i;
      this.workflows.set(workflowId, wf);

      // Check dependencies
      if (step.dependsOn) {
        const allDepsSucceeded = step.dependsOn.every(depId => {
          const depExec = executions.find(e => e.stepId === depId);
          return depExec && depExec.status === "success";
        });

        if (!allDepsSucceeded) {
          this.api.log(`warn`, `Skipping step ${step.id}: dependencies not met`);
          const skipped: Execution = {
            workflowId,
            stepId: step.id,
            status: "skipped",
            attempts: 0,
            startedAt: new Date(),
            completedAt: new Date()
          };
          executions.push(skipped);
          this.executions.set(workflowId, executions);
          continue;
        }
      }

      // Check condition
      if (step.condition) {
        const context = this.buildContext(workflowId, wf, executions);
        const conditionMet = this.evaluateCondition(step.condition, context);
        if (!conditionMet) {
          this.api.log(`info`, `Skipping step ${step.id}: condition not met`);
          const skipped: Execution = {
            workflowId,
            stepId: step.id,
            status: "skipped",
            attempts: 0,
            startedAt: new Date(),
            completedAt: new Date()
          };
          executions.push(skipped);
          this.executions.set(workflowId, executions);
          continue;
        }
      }

      // Execute step with retry
      const execResult = await this.executeStepWithRetry(workflowId, step, wf.context);
      executions.push(execResult);
      this.executions.set(workflowId, executions);

      // Update context with results
      if (execResult.status === "success" && execResult.result) {
        wf.context = {
          ...wf.context,
          [`results.${step.id}`]: execResult.result
        };
        this.workflows.set(workflowId, wf);
      }

      // Check if step failed after retries
      if (execResult.status === "failed") {
        wf.status = "failed";
        wf.error = `Step ${step.id} failed: ${execResult.lastError}`;
        wf.endTime = new Date();
        this.workflows.set(workflowId, wf);
        this.api.log(`error`, `Workflow ${workflowId} failed at step ${step.id}: ${wf.error}`);
        return;
      }
    }

    // All steps completed
    wf.status = "completed";
    wf.endTime = new Date();
    this.workflows.set(workflowId, wf);
    this.api.log(`info`, `Workflow ${workflowId} completed successfully`);

    // Emit completion event
    this.api.emit("workflow.completed", { workflowId, context: wf.context });
  }

  private async executeStepWithRetry(
    workflowId: string, 
    step: WorkflowStep, 
    context: Record<string, any>
  ): Promise<Execution> {
    const exec: Execution = {
      workflowId,
      stepId: step.id,
      status: "pending",
      attempts: 0
    };

    const maxAttempts = step.retry?.maxAttempts || 1;
    const delayMs = step.retry?.delayMs || 1000;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      exec.attempts = attempt;
      exec.status = "running";
      exec.startedAt = new Date();
      this.updateExecution(workflowId, exec);

      try {
        // Resolve args with context variables
        const resolvedArgs = this.resolveArgs(step.args, context);
        
        // Add workflow metadata
        resolvedArgs._workflow = { workflowId, stepId: step.id, attempt };

        this.api.log(`debug`, `Executing ${step.skill}:${step.command} with args: ${JSON.stringify(resolvedArgs)}`);

        // Execute command via API
        const result = await this.api.executeCommand(step.skill, step.command, resolvedArgs);

        exec.status = "success";
        exec.completedAt = new Date();
        exec.result = result;
        this.updateExecution(workflowId, exec);

        this.api.log(`info`, `Step ${step.id} completed successfully`);
        return exec;

      } catch (error: any) {
        exec.lastError = error.message;
        exec.completedAt = new Date();

        if (attempt < maxAttempts) {
          this.api.log(`warn`, `Step ${step.id} failed, retrying in ${delayMs}ms: ${error.message}`);
          await this.sleep(delayMs);
          continue;
        } else {
          exec.status = "failed";
          this.updateExecution(workflowId, exec);
          this.api.log(`error`, `Step ${step.id} failed after ${maxAttempts} attempts: ${error.message}`);
          return exec;
        }
      }
    }

    exec.status = "failed";
    return exec;
  }

  private resolveArgs(args: Record<string, any>, context: Record<string, any>): Record<string, any> {
    const resolved: Record<string, any> = {};

    for (const [key, value] of Object.entries(args)) {
      if (typeof value === "string" && value.startsWith("{{") && value.endsWith("}}")) {
        // Template variable
        const path = value.slice(2, -2).trim();
        resolved[key] = this.getContextValue(path, context);
      } else {
        resolved[key] = value;
      }
    }

    return resolved;
  }

  private getContextValue(path: string, context: Record<string, any>): any {
    const parts = path.split(".");
    let current: any = context;

    for (const part of parts) {
      if (current && typeof current === "object") {
        current = current[part];
      } else {
        return undefined;
      }
    }

    return current;
  }

  private buildContext(workflowId: string, wf: Workflow, executions: Execution[]): Record<string, any> {
    const context: Record<string, any> = {
      workflowId,
      workflowName: wf.name,
      stepResults: {},
      executionId: workflowId // For simplicity
    };

    for (const exec of executions) {
      if (exec.status === "success" && exec.result) {
        context.stepResults[exec.stepId] = exec.result;
      }
    }

    return { ...context, ...wf.context };
  }

  private evaluateCondition(condition: string, context: Record<string, any>): boolean {
    try {
      // Very simple condition evaluation - in production use a proper expression parser
      // For now, just check if a context variable exists and is truthy
      if (condition.startsWith("results.")) {
        const path = condition.slice(7);
        const value = this.getContextValue(path, context);
        return value ? true : false;
      }

      // Default: condition must be a boolean expression
      // This is a placeholder - real implementation would use a safe eval
      return true;
    } catch (error) {
      this.api.log(`error`, `Condition evaluation failed: ${condition} - ${error}`);
      return false;
    }
  }

  private updateExecution(workflowId: string, exec: Execution): void {
    const executions = this.executions.get(workflowId) || [];
    const index = executions.findIndex(e => e.stepId === exec.stepId);
    if (index >= 0) {
      executions[index] = exec;
    } else {
      executions.push(exec);
    }
    this.executions.set(workflowId, executions);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Monitoring
  async getWorkflowStats(): Promise<{
    total: number;
    byStatus: Record<string, number>;
    averageDurationMs?: number;
  }> {
    const all = Array.from(this.workflows.values());
    const byStatus: Record<string, number> = {};

    for (const wf of all) {
      byStatus[wf.status] = (byStatus[wf.status] || 0) + 1;
    }

    // Calculate average duration for completed workflows
    const completed = all.filter(w => w.status === "completed" && w.startTime && w.endTime);
    const avgDuration = completed.length > 0
      ? completed.reduce((sum, w) => sum + (w.endTime!.getTime() - w.startTime!.getTime()), 0) / completed.length
      : undefined;

    return {
      total: all.length,
      byStatus,
      averageDurationMs: avgDuration
    };
  }
}

export async function register(api: OpenClawSkillApi) {
  const orchestrator = new WorkflowOrchestrator(api);

  api.registerCommand("workflow", {
    description: "工作流编排中心命令",
    subcommands: {
      create: {
        description: "创建工作流 (JSON定义)",
        arguments: {
          definition: { type: "object", required: true, help: "工作流定义 (steps数组)" },
          name: { type: "string", required: true, help: "工作流名称" },
          context: { type: "object", help: "初始上下文" }
        },
        execute: async (args) => {
          const id = await orchestrator.createWorkflow({
            name: args.name,
            steps: args.definition,
            context: args.context
          });
          return { success: true, workflowId: id, message: `工作流已创建: ${id}` };
        }
      },
      start: {
        description: "启动工作流",
        arguments: {
          id: { type: "string", required: true, help: "工作流ID" },
          overrides: { type: "object", help: "覆盖上下文变量" }
        },
        execute: async (args) => {
          await orchestrator.startWorkflow(args.id, args.overrides);
          return { success: true, message: `工作流已启动: ${args.id}` };
        }
      },
      pause: {
        description: "暂停工作流",
        arguments: {
          id: { type: "string", required: true, help: "工作流ID" }
        },
        execute: async (args) => {
          await orchestrator.pauseWorkflow(args.id);
          return { success: true, message: `工作流已暂停: ${args.id}` };
        }
      },
      resume: {
        description: "恢复工作流",
        arguments: {
          id: { type: "string", required: true, help: "工作流ID" }
        },
        execute: async (args) => {
          await orchestrator.resumeWorkflow(args.id);
          return { success: true, message: `工作流已恢复: ${args.id}` };
        }
      },
      cancel: {
        description: "取消工作流",
        arguments: {
          id: { type: "string", required: true, help: "工作流ID" }
        },
        execute: async (args) => {
          await orchestrator.cancelWorkflow(args.id);
          return { success: true, message: `工作流已取消: ${args.id}` };
        }
      },
      status: {
        description: "查看工作流状态",
        arguments: {
          id: { type: "string", required: true, help: "工作流ID" }
        },
        execute: async (args) => {
          const status = await orchestrator.getStatus(args.id);
          return { success: true, ...status };
        }
      },
      list: {
        description: "列出工作流",
        arguments: {
          status: { 
            type: "enum",
            options: ["draft", "running", "paused", "completed", "failed"]
          }
        },
        execute: async (args) => {
          const workflows = await orchestrator.listWorkflows(args.status);
          return { success: true, count: workflows.length, workflows };
        }
      },
      template: {
        description: "使用标准模板创建工作流",
        arguments: {
          type: { 
            type: "enum", 
            required: true,
            options: ["ad-production"],
            help: "模板类型"
          },
          demandId: { type: "string", required: true, help: "需求ID" },
          prompt: { type: "string", required: true, help: "生成提示词" },
          count: { type: "number", help: "生成数量 (默认10)", default: 10 },
          platforms: { type: "string[]", required: true, help: "目标平台列表" }
        },
        execute: async (args) => {
          let workflowId: string;
          
          switch (args.type) {
            case "ad-production":
              workflowId = await orchestrator.createStandardAdWorkflow({
                demandId: args.demandId,
                prompt: args.prompt,
                count: args.count,
                platforms: args.platforms
              });
              break;
            default:
              return { success: false, error: `Unknown template type: ${args.type}` };
          }

          return { success: true, workflowId, message: `工作流已创建 (${args.type}): ${workflowId}` };
        }
      },
      stats: {
        description: "工作流统计",
        execute: async () => {
          const stats = await orchestrator.getWorkflowStats();
          return { success: true, stats };
        }
      },
      executions: {
        description: "查看执行历史",
        arguments: {
          id: { type: "string", required: true, help: "工作流ID" }
        },
        execute: async (args) => {
          const execs = await orchestrator.getExecutions(args.id);
          return { success: true, count: execs.length, executions: execs };
        }
      }
    }
  });

  // Listen for events from other skills to auto-trigger workflows
  api.on("demand.approved", async (data) => {
    const { demandId, demand } = data as { demandId: string; demand: any };
    api.log("info", `Demand approved: ${demandId}, creating auto-workflow`);

    // Create a standard ad production workflow
    try {
      const wfId = await orchestrator.createStandardAdWorkflow({
        demandId,
        prompt: demand.description || "Standard creative",
        count: 10,
        platforms: ["抖音", "穿山甲"] // Default platforms
      });

      api.log("info", `Auto-created workflow: ${wfId}`);
      
      // Optionally start immediately
      await orchestrator.startWorkflow(wfId);
      api.log("info", `Workflow ${wfId} started automatically`);
    } catch (error) {
      api.log("error", `Failed to create auto-workflow: ${error}`);
    }
  });

  // Listen for delivery completion to close the loop
  api.on("delivery.completed", async (data) => {
    const { packageId, results } = data as { packageId: string; results: any };
    api.log("info", `Delivery completed: ${packageId}, analytics tracking initiated`);
    
    // Would trigger analytics setup here
  });

  api.log("info", "Workflow Orchestrator skill loaded");
}