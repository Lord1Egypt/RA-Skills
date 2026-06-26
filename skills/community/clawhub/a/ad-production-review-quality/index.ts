import { OpenClawSkillApi } from "openclaw/skill-sdk";

interface Review {
  id: string;
  taskId: string;
  materialId: string;
  reviewer: string;
  score: number;
  passed: boolean;
  comments?: string;
  issues?: string[];
  createdAt: Date;
  updatedAt: Date;
}

interface QualityCheck {
  materialId: string;
  automatedScore: number;
  checks: {
    resolution: boolean;
    artifacts: boolean;
    watermark: boolean;
    nsfw: boolean;
    blur: boolean;
  };
  suggestions: string[];
}

class ReviewQuality {
  private reviews: Map<string, Review> = new Map();
  private api: OpenClawSkillApi;

  constructor(api: OpenClawSkillApi) {
    this.api = api;
  }

  async autoCheck(materialId: string): Promise<QualityCheck> {
    // Would integrate with material-library to get material
    // For now, return mock check
    const check: QualityCheck = {
      materialId,
      automatedScore: Math.random() * 10,
      checks: {
        resolution: true,
        artifacts: false,
        watermark: false,
        nsfw: false,
        blur: false
      },
      suggestions: []
    };

    // Add suggestions based on issues
    if (!check.checks.resolution) {
      check.suggestions.push("分辨率不符合要求");
    }
    if (check.checks.artifacts) {
      check.suggestions.push("检测到 artifacts，建议重新生成");
    }
    if (check.checks.blur) {
      check.suggestions.push("图片模糊，建议提高清晰度");
    }

    return check;
  }

  async submitReview(review: {
    taskId: string;
    materialId: string;
    score: number;
    passed: boolean;
    comments?: string;
    issues?: string[];
  }): Promise<string> {
    const id = `REV-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    const newReview: Review = {
      id,
      taskId: review.taskId,
      materialId: review.materialId,
      reviewer: this.api.user?.id || "anonymous",
      score: review.score,
      passed: review.passed,
      comments: review.comments,
      issues: review.issues || [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.reviews.set(id, newReview);
    this.api.log(`info`, `Review submitted: ${id} for material ${review.materialId}`);

    // Emit event
    this.api.emit("review.completed", { reviewId: id, review: newReview });

    // If review fails, trigger regeneration request
    if (!review.passed) {
      this.api.emit("review.rejected", { materialId: review.materialId, review: newReview });
    }

    return id;
  }

  async getReview(id: string): Promise<Review | null> {
    return this.reviews.get(id) || null;
  }

  async getReviewsForTask(taskId: string): Promise<Review[]> {
    return Array.from(this.reviews.values()).filter(r => r.taskId === taskId);
  }

  async getReviewsForMaterial(materialId: string): Promise<Review[]> {
    return Array.from(this.reviews.values()).filter(r => r.materialId === materialId);
  }

  async batchReview(reviews: Array<{
    taskId: string;
    materialId: string;
    score: number;
    passed: boolean;
    comments?: string;
    issues?: string[];
  }>): Promise<{submitted: number; ids: string[]}> {
    const ids: string[] = [];

    for (const review of reviews) {
      const id = await this.submitReview(review);
      ids.push(id);
    }

    this.api.log(`info`, `Batch review completed: ${ids.length} reviews submitted`);
    return { submitted: ids.length, ids };
  }

  async approveBatch(taskId: string, materialIds: string[]): Promise<{approved: number; reviewIds: string[]}> {
    const reviews = materialIds.map(mid => ({
      taskId,
      materialId: mid,
      score: 10,
      passed: true,
      comments: "批量批准"
    }));

    const result = await this.batchReview(reviews);
    return { approved: result.submitted, reviewIds: result.ids };
  }

  async rejectBatch(taskId: string, materialIds: string[], reason: string): Promise<{rejected: number; reviewIds: string[]}> {
    const reviews = materialIds.map(mid => ({
      taskId,
      materialId: mid,
      score: 0,
      passed: false,
      comments: reason,
      issues: [reason]
    }));

    const result = await this.batchReview(reviews);
    return { rejected: result.submitted, reviewIds: result.ids };
  }

  async getStats(taskId?: string): Promise<{
    total: number;
    passed: number;
    failed: number;
    averageScore: number;
  }> {
    let reviews = Array.from(this.reviews.values());
    if (taskId) {
      reviews = reviews.filter(r => r.taskId === taskId);
    }

    const total = reviews.length;
    const passed = reviews.filter(r => r.passed).length;
    const failed = total - passed;
    const averageScore = total > 0 
      ? reviews.reduce((sum, r) => sum + r.score, 0) / total 
      : 0;

    return { total, passed, failed, averageScore };
  }

  async resolveIssue(reviewId: string): Promise<boolean> {
    const review = this.reviews.get(reviewId);
    if (!review) {
      throw new Error(`Review not found: ${reviewId}`);
    }

    // Mark issues as resolved
    review.issues = [];
    review.updatedAt = new Date();
    this.reviews.set(reviewId, review);

    this.api.log(`info`, `Issues resolved for review: ${reviewId}`);
    return true;
  }
}

export async function register(api: OpenClawSkillApi) {
  const reviewer = new ReviewQuality(api);

  api.registerCommand("review", {
    description: "审核质检命令",
    subcommands: {
      check: {
        description: "自动质量检查",
        arguments: {
          materialId: { type: "string", required: true, help: "素材ID" }
        },
        execute: async (args) => {
          const result = await reviewer.autoCheck(args.materialId);
          return { 
            success: true, 
            materialId: args.materialId,
            score: result.automatedScore,
            checks: result.checks,
            suggestions: result.suggestions
          };
        }
      },
      submit: {
        description: "提交审核",
        arguments: {
          taskId: { type: "string", required: true, help: "任务ID" },
          materialId: { type: "string", required: true, help: "素材ID" },
          score: { type: "number", required: true, help: "评分 (0-10)" },
          passed: { type: "boolean", required: true, help: "是否通过" },
          comments: { type: "string", help: "审核意见" },
          issues: { type: "string[]", help: "问题列表" }
        },
        execute: async (args) => {
          const reviewId = await reviewer.submitReview({
            taskId: args.taskId,
            materialId: args.materialId,
            score: args.score,
            passed: args.passed,
            comments: args.comments,
            issues: args.issues
          });
          return { success: true, reviewId, message: `审核已提交: ${reviewId}` };
        }
      },
      get: {
        description: "查看审核记录",
        arguments: {
          id: { type: "string", required: true, help: "审核ID" }
        },
        execute: async (args) => {
          const review = await reviewer.getReview(args.id);
          if (!review) {
            return { success: false, error: `审核记录未找到: ${args.id}` };
          }
          return { success: true, review };
        }
      },
      list: {
        description: "列出审核记录",
        arguments: {
          taskId: { type: "string", help: "按任务筛选" },
          materialId: { type: "string", help: "按素材筛选" }
        },
        execute: async (args) => {
          let reviews: Review[];
          if (args.taskId) {
            reviews = await reviewer.getReviewsForTask(args.taskId);
          } else if (args.materialId) {
            reviews = await reviewer.getReviewsForMaterial(args.materialId);
          } else {
            reviews = Array.from(reviewer['reviews'].values());
          }
          return { success: true, count: reviews.length, reviews };
        }
      },
      batch: {
        description: "批量审核",
        arguments: {
          taskId: { type: "string", required: true, help: "任务ID" },
          passed: { type: "boolean", required: true, help: "是否通过" },
          materialIds: { type: "string[]", required: true, help: "素材ID列表" },
          comments: { type: "string", help: "批量评论" }
        },
        execute: async (args) => {
          if (args.passed) {
            const result = await reviewer.approveBatch(args.taskId, args.materialIds);
            return { success: true, ...result, message: `已批准 ${result.approved} 个素材` };
          } else {
            const result = await reviewer.rejectBatch(args.taskId, args.materialIds, args.comments || "未通过审核");
            return { success: true, ...result, message: `已拒绝 ${result.rejected} 个素材` };
          }
        }
      },
      resolve: {
        description: "标记问题已解决",
        arguments: {
          reviewId: { type: "string", required: true, help: "审核ID" }
        },
        execute: async (args) => {
          await reviewer.resolveIssue(args.reviewId);
          return { success: true, message: `问题已解决: ${args.reviewId}` };
        }
      },
      stats: {
        description: "审核统计",
        arguments: {
          taskId: { type: "string", help: "任务ID (可选)" }
        },
        execute: async (args) => {
          const stats = await reviewer.getStats(args.taskId);
          return { success: true, stats };
        }
      }
    }
  });

  // Listen for generation completion to trigger auto-check
  api.on("generation.completed", async (data) => {
    const { result } = data as { result: any };
    api.log("info", `Auto-checking generated material: ${result.materialId}`);
    
    try {
      const check = await reviewer.autoCheck(result.materialId);
      if (check.automatedScore < 5) {
        api.log("warn", `Low quality score for ${result.materialId}: ${check.automatedScore}`);
      }
    } catch (error) {
      api.log("error", `Auto-check failed: ${error}`);
    }
  });

  api.log("info", "Review & Quality skill loaded");
}