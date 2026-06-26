import { OpenClawSkillApi } from "openclaw/skill-sdk";

interface GenerationTask {
  id: string;
  demandId?: string;
  prompt: string;
  model: string;
  params: Record<string, any>;
  count: number;
  status: "queued" | "generating" | "completed" | "failed" | "cancelled";
  results?: GenerationResult[];
  error?: string;
  createdAt: Date;
  updatedAt: Date;
}

interface GenerationResult {
  materialId: string;
  prompt: string;
  model: string;
  params: Record<string, any>;
  score?: number;
  status: "generated" | "selected" | "rejected";
}

class AIGeneration {
  private tasks: Map<string, GenerationTask> = new Map();
  private api: OpenClawSkillApi;

  constructor(api: OpenClawSkillApi) {
    this.api = api;
  }

  async create(task: {
    demandId?: string;
    prompt: string;
    model?: string;
    params?: Record<string, any>;
    count: number;
  }): Promise<string> {
    const id = `GEN-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const model = task.model || this.api.config?.defaultModel || "flux";

    const genTask: GenerationTask = {
      id,
      demandId: task.demandId,
      prompt: task.prompt,
      model,
      params: task.params || {},
      count: task.count,
      status: "queued",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.tasks.set(id, genTask);
    this.api.log(`info`, `Generation task created: ${id}`);

    // Queue for processing
    await this.queueTask(id);

    return id;
  }

  async get(id: string): Promise<GenerationTask | null> {
    return this.tasks.get(id) || null;
  }

  async list(status?: GenerationTask["status"]): Promise<GenerationTask[]> {
    const all = Array.from(this.tasks.values());
    if (status) {
      return all.filter(t => t.status === status);
    }
    return all;
  }

  async cancel(id: string): Promise<boolean> {
    const task = this.tasks.get(id);
    if (!task) {
      throw new Error(`Task not found: ${id}`);
    }

    if (task.status === "generating") {
      task.status = "cancelled";
      task.updatedAt = new Date();
      this.tasks.set(id, task);
      this.api.log(`info`, `Generation task cancelled: ${id}`);
    } else {
      throw new Error(`Cannot cancel task in status: ${task.status}`);
    }

    return true;
  }

  async selectResult(taskId: string, resultIndex: number): Promise<boolean> {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    if (!task.results || task.results.length <= resultIndex) {
      throw new Error(`Result index out of range: ${resultIndex}`);
    }

    // Mark selected result
    for (let i = 0; i < task.results.length; i++) {
      task.results[i].status = i === resultIndex ? "selected" : "rejected";
    }

    task.status = "completed";
    task.updatedAt = new Date();
    this.tasks.set(taskId, task);

    // Emit event for review process
    this.api.emit("generation.completed", { taskId, result: task.results[resultIndex] });

    this.api.log(`info`, `Result selected for task ${taskId}: index ${resultIndex}`);
    return true;
  }

  async getBestResults(taskId: string, limit: number = 5): Promise<GenerationResult[]> {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    if (!task.results) {
      return [];
    }

    // Sort by score (if available)
    const scored = task.results
      .filter(r => r.status !== "rejected")
      .map(r => ({
        ...r,
        score: r.score || this.estimateQuality(r)
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);

    return scored;
  }

  async optimizePrompt(prompt: string, feedback?: string): Promise<{optimizedPrompt: string; suggestions: string[]}> {
    // This would integrate with an LLM to optimize prompts
    // For now, return mock optimization
    const suggestions = [
      "添加更多细节描述",
      "指定艺术风格",
      "明确光照条件",
      "定义构图",
      "指定质量关键词"
    ];

    // Simple optimization: add quality keywords
    const optimizedPrompt = `${prompt}, high quality, detailed, 8k, professional`;

    return {
      optimizedPrompt,
      suggestions: feedback ? [feedback, ...suggestions] : suggestions
    };
  }

  async deduplicate(taskId: string, threshold: number = 0.9): Promise<{unique: number; duplicates: number}> {
    const task = this.tasks.get(taskId);
    if (!task || !task.results) {
      throw new Error(`Task not found or no results: ${taskId}`);
    }

    // Simple deduplication based on prompt similarity
    const unique: GenerationResult[] = [];
    const duplicates: GenerationResult[] = [];

    for (const result of task.results) {
      let isDuplicate = false;
      for (const existing of unique) {
        if (this.calculateSimilarity(result.prompt, existing.prompt) > threshold) {
          isDuplicate = true;
          duplicates.push(result);
          break;
        }
      }
      if (!isDuplicate) {
        unique.push(result);
      }
    }

    // Update results status
    for (const result of task.results) {
      result.status = duplicates.includes(result) ? "rejected" : "generated";
    }

    this.api.log(`info`, `Deduplication complete for ${taskId}: ${unique.length} unique, ${duplicates.length} duplicates`);
    return { unique: unique.length, duplicates: duplicates.length };
  }

  private async queueTask(id: string): Promise<void> {
    const task = this.tasks.get(id);
    if (!task) return;

    task.status = "generating";
    this.tasks.set(id, task);

    // Simulate generation (would integrate with actual AI models)
    this.api.log(`info`, `Starting generation for task ${id}`);

    // Process with configured concurrency
    const maxConcurrent = this.api.config?.maxConcurrent || 3;
    // In real implementation, would manage a queue

    // For demo, simulate completion after delay
    setTimeout(async () => {
      await this.simulateCompletion(id);
    }, 2000);
  }

  private async simulateCompletion(id: string): Promise<void> {
    const task = this.tasks.get(id);
    if (!task) return;

    // Generate mock results
    task.results = [];
    for (let i = 0; i < task.count; i++) {
      task.results.push({
        materialId: `MAT-${id}-${i}`,
        prompt: task.prompt,
        model: task.model,
        params: task.params,
        score: Math.random() * 10, // Random score 0-10
        status: "generated"
      });
    }

    task.status = "completed";
    task.updatedAt = new Date();
    this.tasks.set(id, task);

    this.api.log(`info`, `Generation completed for task ${id}: ${task.count} results`);
    this.api.emit("generation.batch_completed", { taskId: id, count: task.count });
  }

  private estimateQuality(result: GenerationResult): number {
    // Very basic quality estimation
    const base = result.score || Math.random() * 10;
    
    // Boost for certain models
    if (result.model === "flux") base += 1;
    if (result.model === "sdxl") base += 0.5;

    return Math.min(10, base);
  }

  private calculateSimilarity(a: string, b: string): number {
    const wordsA = new Set(a.toLowerCase().split(/\s+/));
    const wordsB = new Set(b.toLowerCase().split(/\s+/));
    
    const intersection = [...wordsA].filter(w => wordsB.has(w));
    const union = new Set([...wordsA, ...wordsB]);

    return intersection.length / union.size;
  }
}

export async function register(api: OpenClawSkillApi) {
  const generator = new AIGeneration(api);

  api.registerCommand("ai", {
    description: "AI资源生成命令",
    subcommands: {
      generate: {
        description: "创建生成任务",
        arguments: {
          prompt: { type: "string", required: true, help: "生成提示词" },
          model: { 
            type: "enum",
            options: ["flux", "sdxl", "sd3", "dalle3", "midjourney"],
            help: "AI模型"
          },
          count: { type: "number", help: "生成数量 (默认4)", default: 4 },
          params: { type: "object", help: "额外参数 (JSON)" }
        },
        execute: async (args) => {
          const id = await generator.create({
            prompt: args.prompt,
            model: args.model,
            count: args.count || 4,
            params: args.params
          });
          return { success: true, taskId: id, message: `生成任务已创建: ${id}` };
        }
      },
      status: {
        description: "查看任务状态",
        arguments: {
          id: { type: "string", required: true, help: "任务ID" }
        },
        execute: async (args) => {
          const task = await generator.get(args.id);
          if (!task) {
            return { success: false, error: `任务未找到: ${args.id}` };
          }
          return { success: true, task };
        }
      },
      list: {
        description: "列出任务",
        arguments: {
          status: { 
            type: "enum",
            options: ["queued", "generating", "completed", "failed", "cancelled"]
          }
        },
        execute: async (args) => {
          const tasks = await generator.list(args.status);
          return { success: true, count: tasks.length, tasks };
        }
      },
      cancel: {
        description: "取消任务",
        arguments: {
          id: { type: "string", required: true, help: "任务ID" }
        },
        execute: async (args) => {
          await generator.cancel(args.id);
          return { success: true, message: `任务已取消: ${args.id}` };
        }
      },
      select: {
        description: "选择生成结果",
        arguments: {
          taskId: { type: "string", required: true, help: "任务ID" },
          index: { type: "number", required: true, help: "结果索引" }
        },
        execute: async (args) => {
          await generator.selectResult(args.taskId, args.index);
          return { success: true, message: `已选择结果 ${args.index}` };
        }
      },
      best: {
        description: "获取最佳结果",
        arguments: {
          taskId: { type: "string", required: true, help: "任务ID" },
          limit: { type: "number", help: "数量 (默认5)" }
        },
        execute: async (args) => {
          const results = await generator.getBestResults(args.taskId, args.limit);
          return { success: true, count: results.length, results };
        }
      },
      optimize: {
        description: "优化提示词",
        arguments: {
          prompt: { type: "string", required: true, help: "原始提示词" },
          feedback: { type: "string", help: "反馈意见" }
        },
        execute: async (args) => {
          const result = await generator.optimizePrompt(args.prompt, args.feedback);
          return { success: true, ...result };
        }
      },
      dedup: {
        description: "去重",
        arguments: {
          taskId: { type: "string", required: true, help: "任务ID" },
          threshold: { type: "number", help: "相似度阈值 (默认0.9)" }
        },
        execute: async (args) => {
          const result = await generator.deduplicate(args.taskId, args.threshold);
          return { success: true, ...result, message: `去重完成: ${result.unique} 个唯一, ${result.duplicates} 个重复` };
        }
      }
    }
  });

  // Listen for demand approval to auto-generate
  api.on("demand.approved", async (data) => {
    const { demandId, demand } = data as { demandId: string; demand: any };
    api.log("info", `Auto-starting generation for approved demand: ${demandId}`);

    // Would create generation task from demand
    // await generator.create({
    //   demandId,
    //   prompt: demand.description,
    //   count: 10
    // });
  });

  api.log("info", "AI Generation skill loaded");
}