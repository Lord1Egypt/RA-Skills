import { OpenClawSkillApi } from "openclaw/skill-sdk";

interface MaterialPerformance {
  materialId: string;
  impressions: number;
  clicks: number;
  conversions: number;
  cost: number;
  revenue: number;
  ctr: number; // click-through rate
  cvr: number; // conversion rate
  roas: number; // return on ad spend
  avgCpc: number; // average cost per click
  startDate: Date;
  endDate: Date;
}

interface Campaign {
  id: string;
  name: string;
  platform: string;
  materials: string[];
  startDate: Date;
  endDate?: Date;
  budget: number;
  spent: number;
  status: "active" | "paused" | "completed";
}

interface Report {
  id: string;
  period: "daily" | "weekly" | "monthly" | "custom";
  startDate: Date;
  endDate: Date;
  summary: {
    totalImpressions: number;
    totalClicks: number;
    totalConversions: number;
    totalCost: number;
    totalRevenue: number;
    avgCtr: number;
    avgCvr: number;
    avgRoas: number;
  };
  topPerformers: MaterialPerformance[];
  underperformers: MaterialPerformance[];
  insights: string[];
  createdAt: Date;
}

class AnalyticsFeedback {
  private campaigns: Map<string, Campaign> = new Map();
  private performance: Map<string, MaterialPerformance> = new Map();
  private reports: Map<string, Report> = new Map();
  private api: OpenClawSkillApi;

  // Thresholds for alerts
  private readonly POOR_CTR_THRESHOLD = 0.01; // 1%
  private readonly POOR_CVR_THRESHOLD = 0.005; // 0.5%
  private readonly LOW_ROAS_THRESHOLD = 2.0; // < 2x return

  constructor(api: OpenClawSkillApi) {
    this.api = api;
  }

  // Data Ingestion
  async ingestPerformance(data: {
    materialId: string;
    campaignId?: string;
    impressions: number;
    clicks: number;
    conversions: number;
    cost: number;
    revenue: number;
    date: Date;
  }): Promise<boolean> {
    const existing = this.performance.get(data.materialId) || {
      materialId: data.materialId,
      impressions: 0,
      clicks: 0,
      conversions: 0,
      cost: 0,
      revenue: 0,
      startDate: data.date,
      endDate: data.date,
    };

    // Aggregate (in real system, would store time-series)
    const updated: MaterialPerformance = {
      ...existing,
      impressions: existing.impressions + data.impressions,
      clicks: existing.clicks + data.clicks,
      conversions: existing.conversions + data.conversions,
      cost: existing.cost + data.cost,
      revenue: existing.revenue + data.revenue,
      endDate: data.date,
    };

    // Calculate metrics
    updated.ctr = updated.clicks / updated.impressions || 0;
    updated.cvr = updated.conversions / updated.clicks || 0;
    updated.roas = updated.revenue / updated.cost || 0;
    updated.avgCpc = updated.cost / updated.clicks || 0;

    this.performance.set(data.materialId, updated);

    // Check for alerts
    await this.checkPerformanceAlerts(updated);

    this.api.log("debug", `Ingested performance for ${data.materialId}`);
    return true;
  }

  async registerCampaign(campaign: {
    name: string;
    platform: string;
    materials: string[];
    budget: number;
    startDate: Date;
  }): Promise<string> {
    const id = `CAMP-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    const newCampaign: Campaign = {
      id,
      name: campaign.name,
      platform: campaign.platform,
      materials: campaign.materials,
      startDate: campaign.startDate,
      budget: campaign.budget,
      spent: 0,
      status: "active",
    };

    this.campaigns.set(id, newCampaign);
    this.api.log("info", `Campaign registered: ${id} - ${campaign.name}`);
    return id;
  }

  async getPerformance(materialId: string): Promise<MaterialPerformance | null> {
    return this.performance.get(materialId) || null;
  }

  async getCampaignPerformance(campaignId: string): Promise<MaterialPerformance[]> {
    const campaign = this.campaigns.get(campaignId);
    if (!campaign) {
      throw new Error(`Campaign not found: ${campaignId}`);
    }

    return campaign.materials
      .map(mid => this.performance.get(mid))
      .filter(p => p !== undefined) as MaterialPerformance[];
  }

  // Reporting
  async generateReport(params: {
    period: "daily" | "weekly" | "monthly" | "custom";
    startDate: Date;
    endDate: Date;
    campaignIds?: string[];
    includeTopN?: number;
  }): Promise<Report> {
    const id = `RPT-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    // Gather all relevant performance data
    let allPerformance = Array.from(this.performance.values());

    // Filter by campaign if specified
    if (params.campaignIds) {
      const materialSet = new Set<string>();
      for (const campId of params.campaignIds) {
        const camp = this.campaigns.get(campId);
        if (camp) {
          camp.materials.forEach(mid => materialSet.add(mid));
        }
      }
      allPerformance = allPerformance.filter(p => materialSet.has(p.materialId));
    }

    // Filter by date range
    allPerformance = allPerformance.filter(p => 
      p.startDate <= params.endDate && (!p.endDate || p.endDate >= params.startDate)
    );

    // Calculate summary
    const summary = {
      totalImpressions: allPerformance.reduce((sum, p) => sum + p.impressions, 0),
      totalClicks: allPerformance.reduce((sum, p) => sum + p.clicks, 0),
      totalConversions: allPerformance.reduce((sum, p) => sum + p.conversions, 0),
      totalCost: allPerformance.reduce((sum, p) => sum + p.cost, 0),
      totalRevenue: allPerformance.reduce((sum, p) => sum + p.revenue, 0),
      avgCtr: allPerformance.reduce((sum, p) => sum + p.ctr, 0) / allPerformance.length,
      avgCvr: allPerformance.reduce((sum, p) => sum + p.cvr, 0) / allPerformance.length,
      avgRoas: allPerformance.reduce((sum, p) => sum + p.roas, 0) / allPerformance.length,
    };

    summary.avgCtr = isNaN(summary.avgCtr) ? 0 : summary.avgCtr;
    summary.avgCvr = isNaN(summary.avgCvr) ? 0 : summary.avgCvr;
    summary.avgRoas = isNaN(summary.avgRoas) ? 0 : summary.avgRoas;

    // Sort by performance
    const topPerformers = [...allPerformance]
      .sort((a, b) => b.roas - a.roas)
      .slice(0, params.includeTopN || 10);

    const underperformers = allPerformance
      .filter(p => p.roas < this.LOW_ROAS_THRESHOLD || p.ctr < this.POOR_CTR_THRESHOLD)
      .sort((a, b) => a.roas - b.roas)
      .slice(0, 10);

    // Generate insights
    const insights = this.generateInsights(allPerformance, summary);

    const report: Report = {
      id,
      period: params.period,
      startDate: params.startDate,
      endDate: params.endDate,
      summary,
      topPerformers,
      underperformers,
      insights,
      createdAt: new Date(),
    };

    this.reports.set(id, report);
    this.api.log("info", `Report generated: ${id}`);
    return report;
  }

  async getReport(id: string): Promise<Report | null> {
    return this.reports.get(id) || null;
  }

  async listReports(): Promise<Report[]> {
    return Array.from(this.reports.values()).sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }

  // Feedback Loop
  async generateFeedback(materialId: string): Promise<{
    suggestions: string[];
    promptImprovements: string[];
    modelRecommendations: string[];
  }> {
    const perf = this.performance.get(materialId);
    if (!perf) {
      throw new Error(`No performance data for material: ${materialId}`);
    }

    const suggestions: string[] = [];
    const promptImprovements: string[] = [];
    const modelRecommendations: string[] = [];

    // Analyze CTR
    if (perf.ctr < this.POOR_CTR_THRESHOLD) {
      suggestions.push("点击率偏低，建议优化创意吸引力");
      promptImprovements.push("增加动态元素", "使用更醒目的配色", "添加行动号召");
    }

    // Analyze CVR
    if (perf.cvr < this.POOR_CVR_THRESHOLD) {
      suggestions.push("转化率偏低，建议优化落地页或素材相关性");
      promptImprovements.push("突出产品核心卖点", "添加信任要素", "明确价值主张");
    }

    // Analyze ROAS
    if (perf.roas < this.LOW_ROAS_THRESHOLD) {
      suggestions.push("ROI较低，建议调整投放策略或重新设计素材");
    } else if (perf.roas > 5) {
      suggestions.push("表现优异，考虑扩大投放或复用成功元素");
    }

    // Model recommendations based on performance
    if (perf.roas > 4) {
      modelRecommendations.push("当前模型表现优秀，建议保持");
    } else {
      modelRecommendations.push("尝试其他模型 (如Flux, SDXL)");
      modelRecommendations.push("增加生成多样性");
    }

    // Additional data-driven suggestions
    if (perf.avgCpc > 2) {
      suggestions.push("CPC偏高，建议优化受众定位");
    }

    this.api.log("info", `Generated feedback for ${materialId}`);
    return {
      suggestions,
      promptImprovements,
      modelRecommendations
    };
  }

  async getMaterialInsights(materialId: string): Promise<any> {
    const perf = this.performance.get(materialId);
    if (!perf) {
      return { error: "No performance data" };
    }

    const feedback = await this.generateFeedback(materialId);

    return {
      materialId,
      performance: perf,
      feedback,
      benchmarks: {
        avgCtr: 0.02, // Industry average 2%
        avgCvr: 0.01, // Industry average 1%
        avgRoas: 3.0, // Industry average 3x
      },
      rating: this.calculateRating(perf)
    };
  }

  async exportCSV(reportId: string): Promise<string> {
    const report = this.reports.get(reportId);
    if (!report) {
      throw new Error(`Report not found: ${reportId}`);
    }

    // Generate CSV
    const headers = ["Material ID", "Impressions", "Clicks", "CTR", "Conversions", "CVR", "Cost", "Revenue", "ROAS"];
    const rows = report.topPerformers.map(p => [
      p.materialId,
      p.impressions.toString(),
      p.clicks.toString(),
      (p.ctr * 100).toFixed(2) + "%",
      p.conversions.toString(),
      (p.cvr * 100).toFixed(2) + "%",
      p.cost.toFixed(2),
      p.revenue.toFixed(2),
      p.roas.toFixed(2)
    ]);

    const csv = [headers, ...rows].map(row => row.join(",")).join("\n");
    return csv;
  }

  // Alerts & Notifications
  private async checkPerformanceAlerts(perf: MaterialPerformance): Promise<void> {
    const alerts: string[] = [];

    if (perf.ctr < this.POOR_CTR_THRESHOLD) {
      alerts.push(`低点击率: ${(perf.ctr * 100).toFixed(2)}% < 1%`);
    }

    if (perf.cvr < this.POOR_CVR_THRESHOLD) {
      alerts.push(`低转化率: ${(perf.cvr * 100).toFixed(2)}% < 0.5%`);
    }

    if (perf.roas < this.LOW_ROAS_THRESHOLD) {
      alerts.push(`低ROI: ${perf.roas.toFixed(2)}x < 2x`);
    }

    if (alerts.length > 0) {
      this.api.emit("analytics.alert", {
        materialId: perf.materialId,
        alerts,
        performance: perf
      });

      // Send notification if configured
      if (this.api.config?.notifyOnAlerts) {
        await this.sendAlertNotification(perf.materialId, alerts);
      }
    }
  }

  private async sendAlertNotification(materialId: string, alerts: string[]): Promise<void> {
    // Would send via feishu_im_user_message or similar
    this.api.log("warn", `Alerts for ${materialId}: ${alerts.join(", ")}`);
  }

  private generateInsights(performance: MaterialPerformance[], summary: any): string[] {
    const insights: string[] = [];

    if (summary.totalImpressions > 0) {
      insights.push(`总计 ${summary.totalImpressions.toLocaleString()} 次展示`);
    }

    if (summary.avgCtr > 0.02) {
      insights.push(`平均点击率 ${(summary.avgCtr * 100).toFixed(2)}% 高于行业基准`);
    } else {
      insights.push(`平均点击率 ${(summary.avgCtr * 100).toFixed(2)}% 低于行业基准，需优化`);
    }

    if (summary.avgRoas > 3) {
      insights.push(`平均ROI ${summary.avgRoas.toFixed(2)}x 表现优秀`);
    } else {
      insights.push(`平均ROI ${summary.avgRoas.toFixed(2)}x 有提升空间`);
    }

    // Top performer highlight
    if (performance.length > 0) {
      const top = performance.reduce((max, p) => p.roas > max.roas ? p : performance[0]);
      insights.push(`最佳表现: ${top.materialId} (ROI: ${top.roas.toFixed(2)}x)`);
    }

    return insights;
  }

  private calculateRating(perf: MaterialPerformance): "excellent" | "good" | "average" | "poor" {
    if (perf.roas >= 5 && perf.ctr >= 0.03) return "excellent";
    if (perf.roas >= 3 && perf.ctr >= 0.02) return "good";
    if (perf.roas >= 1.5 && perf.ctr >= 0.01) return "average";
    return "poor";
  }
}

export async function register(api: OpenClawSkillApi) {
  const analytics = new AnalyticsFeedback(api);

  api.registerCommand("analytics", {
    description: "数据分析与反馈命令",
    subcommands: {
      ingest: {
        description: "录入投放数据",
        arguments: {
          materialId: { type: "string", required: true, help: "素材ID" },
          campaignId: { type: "string", help: "活动ID" },
          impressions: { type: "number", required: true, help: "展示数" },
          clicks: { type: "number", required: true, help: "点击数" },
          conversions: { type: "number", required: true, help: "转化数" },
          cost: { type: "number", required: true, help: "花费" },
          revenue: { type: "number", required: true, help: "收入" },
          date: { type: "string", help: "日期 (ISO 8601)" }
        },
        execute: async (args) => {
          const date = args.date ? new Date(args.date) : new Date();
          await analytics.ingestPerformance({
            materialId: args.materialId,
            campaignId: args.campaignId,
            impressions: args.impressions,
            clicks: args.clicks,
            conversions: args.conversions,
            cost: args.cost,
            revenue: args.revenue,
            date
          });
          return { success: true, message: `数据已录入: ${args.materialId}` };
        }
      },
      performance: {
        description: "查看素材表现",
        arguments: {
          materialId: { type: "string", required: true, help: "素材ID" }
        },
        execute: async (args) => {
          const perf = await analytics.getPerformance(args.materialId);
          if (!perf) {
            return { success: false, error: `无性能数据: ${args.materialId}` };
          }
          return { success: true, performance: perf };
        }
      },
      campaign: {
        description: "查看活动表现",
        arguments: {
          campaignId: { type: "string", required: true, help: "活动ID" }
        },
        execute: async (args) => {
          const materials = await analytics.getCampaignPerformance(args.campaignId);
          return { success: true, count: materials.length, materials };
        }
      },
      report: {
        description: "生成报告",
        arguments: {
          period: { 
            type: "enum", 
            required: true, 
            options: ["daily", "weekly", "monthly", "custom"],
            help: "报告周期"
          },
          startDate: { type: "string", required: true, help: "开始日期 (ISO 8601)" },
          endDate: { type: "string", required: true, help: "结束日期 (ISO 8601)" },
          campaignIds: { type: "string[]", help: "活动ID列表" },
          topN: { type: "number", help: "包含前N名" }
        },
        execute: async (args) => {
          const report = await analytics.generateReport({
            period: args.period,
            startDate: new Date(args.startDate),
            endDate: new Date(args.endDate),
            campaignIds: args.campaignIds,
            includeTopN: args.topN
          });
          return { success: true, reportId: report.id, report };
        }
      },
      "feedback": {
        description: "获取素材改进反馈",
        arguments: {
          materialId: { type: "string", required: true, help: "素材ID" }
        },
        execute: async (args) => {
          const feedback = await analytics.generateFeedback(args.materialId);
          return { success: true, ...feedback };
        }
      },
      insights: {
        description: "获取素材洞察",
        arguments: {
          materialId: { type: "string", required: true, help: "素材ID" }
        },
        execute: async (args) => {
          const insights = await analytics.getMaterialInsights(args.materialId);
          return { success: true, ...insights };
        }
      },
      export: {
        description: "导出报告CSV",
        arguments: {
          reportId: { type: "string", required: true, help: "报告ID" }
        },
        execute: async (args) => {
          const csv = await analytics.exportCSV(args.reportId);
          return { success: true, csv, message: "CSV导出成功" };
        }
      },
      alerts: {
        description: "查看告警",
        execute: async () => {
          // Would fetch recent alerts from event store
          return { success: true, alerts: [], message: "告警功能待集成事件存储" };
        }
      }
    }
  });

  // Listen for delivery completion to trigger data collection setup
  api.on("delivery.completed", async (data) => {
    const { packageId, results } = data as { packageId: string; results: any };
    api.log("info", `Delivery ${packageId} completed, setting up tracking`);
    
    // Would create tracking campaigns for delivered materials
  });

  // Listen for new materials to initialize performance tracking
  api.on("material.created", async (data) => {
    api.log("debug", `New material created: ${JSON.stringify(data)}`);
    // Initialize performance tracking record
  });

  api.log("info", "Analytics & Feedback skill loaded");
}