import { OpenClawSkillApi } from "openclaw/skill-sdk";

interface Demand {
  id: string;
  title: string;
  type: "new_material" | "reuse" | "modification";
  channel: string;
  style: string;
  size: string;
  description: string;
  status: "draft" | "pending_review" | "approved" | "rejected" | "in_production" | "completed";
  createdAt: Date;
  updatedAt: Date;
  reviewer?: string;
  reviewComments?: string;
  promptTemplate?: string;
  assignedTasks?: string[];
}

class DemandManager {
  private demands: Map<string, Demand> = new Map();
  private api: OpenClawSkillApi;

  constructor(api: OpenClawSkillApi) {
    this.api = api;
  }

  async create(demand: Omit<Demand, "id" | "status" | "createdAt" | "updatedAt">): Promise<string> {
    const id = `REQ-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const now = new Date();

    const newDemand: Demand = {
      ...demand,
      id,
      status: "draft",
      createdAt: now,
      updatedAt: now,
    };

    this.demands.set(id, newDemand);

    // Log the creation
    this.api.log(`info`, `Demand created: ${id} - ${demand.title}`);

    // Auto-generate standard demand document if configured
    if (this.api.config?.autoDocument) {
      await this.generateDocument(id);
    }

    return id;
  }

  async get(id: string): Promise<Demand | null> {
    return this.demands.get(id) || null;
  }

  async list(status?: Demand["status"]): Promise<Demand[]> {
    const all = Array.from(this.demands.values());
    if (status) {
      return all.filter(d => d.status === status);
    }
    return all;
  }

  async review(id: string, result: "approved" | "rejected", comments?: string, reviewer?: string): Promise<boolean> {
    const demand = this.demands.get(id);
    if (!demand) {
      throw new Error(`Demand not found: ${id}`);
    }

    if (demand.status !== "pending_review") {
      throw new Error(`Cannot review demand in status: ${demand.status}`);
    }

    demand.status = result === "approved" ? "approved" : "rejected";
    demand.reviewer = reviewer || this.api.user?.id;
    demand.reviewComments = comments;
    demand.updatedAt = new Date();

    this.api.log(`info`, `Demand ${id} reviewed: ${result}`);

    // If approved, trigger production pipeline
    if (result === "approved") {
      await this.triggerProduction(id);
    }

    return true;
  }

  async submitForReview(id: string): Promise<boolean> {
    const demand = this.demands.get(id);
    if (!demand) {
      throw new Error(`Demand not found: ${id}`);
    }

    if (demand.status !== "draft") {
      throw new Error(`Cannot submit demand in status: ${demand.status}`);
    }

    demand.status = "pending_review";
    demand.updatedAt = new Date();

    this.api.log(`info`, `Demand ${id} submitted for review`);

    // Notify reviewers if configured
    if (this.api.config?.reviewers?.length) {
      await this.notifyReviewers(id);
    }

    return true;
  }

  async拆解(id: string, promptTemplate?: string): Promise<{tasks: string[]}> {
    const demand = this.demands.get(id);
    if (!demand) {
      throw new Error(`Demand not found: ${id}`);
    }

    if (demand.status !== "approved") {
      throw new Error(`Cannot拆解demand in status: ${demand.status}`);
    }

    // Store the prompt template
    if (promptTemplate) {
      demand.promptTemplate = promptTemplate;
    }

    // Generate production tasks based on demand parameters
    const tasks = await this.generateTasks(demand);

    demand.assignedTasks = tasks;
    demand.status = "in_production";
    demand.updatedAt = new Date();

    this.api.log(`info`, `Demand ${id}拆解完成, 生成 ${tasks.length} 个任务`);

    return { tasks };
  }

  async complete(id: string): Promise<boolean> {
    const demand = this.demands.get(id);
    if (!demand) {
      throw new Error(`Demand not found: ${id}`);
    }

    demand.status = "completed";
    demand.updatedAt = new Date();

    this.api.log(`info`, `Demand ${id} completed`);

    return true;
  }

  private async generateTasks(demand: Demand): Promise<string[]> {
    const tasks: string[] = [];

    // Task 1: Generate initial batch
    tasks.push(`GEN-${demand.id}-1`);

    // Task 2: Quality review
    tasks.push(`REVIEW-${demand.id}-1`);

    // Task 3: Final delivery
    tasks.push(`DELIVERY-${demand.id}-1`);

    // Here we could also create separate tasks for different formats/sizes

    return tasks;
  }

  private async generateDocument(id: string): Promise<void> {
    const demand = this.demands.get(id);
    if (!demand) return;

    const docContent = `
# 需求文档: ${demand.title}

**需求ID**: ${demand.id}
**类型**: ${demand.type}
**渠道**: ${demand.channel}
**风格**: ${demand.style}
**尺寸**: ${demand.size}

## 需求描述
${demand.description}

## 生产要求
- Prompt 模板: ${demand.promptTemplate || "待定"}
- 素材格式: 待定
- 交付时间: 待定

---

*自动生成于 ${new Date().toISOString()}*
`;

    // Create a document using feishu_create_doc or other service
    // This would need the appropriate API access
    this.api.log(`debug`, `Generated document for ${id}`);
  }

  private async notifyReviewers(id: string): Promise<void> {
    const demand = this.demands.get(id);
    if (!demand) return;

    const reviewers = this.api.config?.reviewers as string[] || [];

    for (const reviewer of reviewers) {
      try {
        // Send notification (would use feishu_im_user_message or similar)
        this.api.log(`info`, `Notified reviewer ${reviewer} for demand ${id}`);
      } catch (error) {
        this.api.log(`error`, `Failed to notify reviewer ${reviewer}: ${error}`);
      }
    }
  }

  private async triggerProduction(id: string): Promise<void> {
    const demand = this.demands.get(id);
    if (!demand) return;

    // This would trigger the AI generation workflow
    this.api.log(`info`, `Triggering production for demand ${id}`);

    // Dispatch event for other skills to listen
    this.api.emit("demand.approved", { demandId: id, demand });
  }
}

export async function register(api: OpenClawSkillApi) {
  const manager = new DemandManager(api);

  // Register commands
  api.registerCommand("demand", {
    description: "需求管理命令",
    subcommands: {
      create: {
        description: "创建新需求",
        arguments: {
          title: { type: "string", required: true, help: "需求标题" },
          type: { 
            type: "enum", 
            required: true, 
            options: ["new_material", "reuse", "modification"],
            help: "需求类型"
          },
          channel: { type: "string", required: true, help: "投放渠道" },
          style: { type: "string", required: true, help: "素材风格" },
          size: { type: "string", required: true, help: "素材尺寸" },
          description: { type: "string", help: "需求描述" }
        },
        execute: async (args) => {
          const id = await manager.create({
            title: args.title,
            type: args.type,
            channel: args.channel,
            style: args.style,
            size: args.size,
            description: args.description || ""
          });
          return { success: true, demandId: id, message: `需求创建成功: ${id}` };
        }
      },
      get: {
        description: "查看需求详情",
        arguments: {
          id: { type: "string", required: true, help: "需求ID" }
        },
        execute: async (args) => {
          const demand = await manager.get(args.id);
          if (!demand) {
            return { success: false, error: `需求未找到: ${args.id}` };
          }
          return { success: true, demand };
        }
      },
      list: {
        description: "列出需求",
        arguments: {
          status: { 
            type: "enum",
            options: ["draft", "pending_review", "approved", "rejected", "in_production", "completed"],
            help: "按状态筛选"
          }
        },
        execute: async (args) => {
          const demands = await manager.list(args.status);
          return { success: true, count: demands.length, demands };
        }
      },
      review: {
        description: "评审需求",
        arguments: {
          id: { type: "string", required: true, help: "需求ID" },
          result: { 
            type: "enum", 
            required: true, 
            options: ["approved", "rejected"],
            help: "评审结果"
          },
          comments: { type: "string", help: "评审意见" }
        },
        execute: async (args) => {
          await manager.review(args.id, args.result, args.comments);
          return { success: true, message: `需求 ${args.id} 已${args.result === "approved" ? "批准" : "拒绝"}` };
        }
      },
      submit: {
        description: "提交需求评审",
        arguments: {
          id: { type: "string", required: true, help: "需求ID" }
        },
        execute: async (args) => {
          await manager.submitForReview(args.id);
          return { success: true, message: `需求 ${args.id} 已提交评审` };
        }
      },
      "拆解": {
        description: "拆解需求为生产任务",
        arguments: {
          id: { type: "string", required: true, help: "需求ID" },
          promptTemplate: { type: "string", help: "Prompt模板" }
        },
        execute: async (args) => {
          const result = await manager.拆解(args.id, args.promptTemplate);
          return { success: true, ...result, message: `需求 ${args.id} 拆解为 ${result.tasks.length} 个任务` };
        }
      },
      complete: {
        description: "标记需求完成",
        arguments: {
          id: { type: "string", required: true, help: "需求ID" }
        },
        execute: async (args) => {
          await manager.complete(args.id);
          return { success: true, message: `需求 ${args.id} 已完成` };
        }
      }
    }
  });

  // Subscribe to events from other skills
  api.on("demand.created", async (data) => {
    api.log("info", `Received demand.created event: ${JSON.stringify(data)}`);
  });

  api.log("info", "Demand Management skill loaded");
}