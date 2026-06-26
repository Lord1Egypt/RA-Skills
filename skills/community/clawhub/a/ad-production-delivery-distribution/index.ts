import { OpenClawSkillApi } from "openclaw/skill-sdk";

interface DeliveryPackage {
  id: string;
  name: string;
  materials: string[]; // material IDs
  format: "zip" | "folder" | "direct_upload";
  platforms: string[];
  status: "preparing" | "ready" | "uploading" | "completed" | "failed";
  downloadUrl?: string;
  uploadStatus?: Record<string, "pending" | "success" | "failed">;
  createdAt: Date;
  completedAt?: Date;
}

class DeliveryDistribution {
  private packages: Map<string, DeliveryPackage> = new Map();
  private api: OpenClawSkillApi;

  // Platform-specific requirements
  private platformRequirements: Record<string, {
    formats: string[];
    maxSizeMB: number;
    dimensions?: { width: number; height: number }[];
    duration?: { min: number; max: number };
  }> = {
    "抖音": {
      formats: ["mp4", "mov"],
      maxSizeMB: 100,
      dimensions: [
        { width: 1080, height: 1920 }, // 9:16
        { width: 720, height: 1280 }
      ],
      duration: { min: 1, max: 60 }
    },
    "穿山甲": {
      formats: ["mp4", "jpg", "png"],
      maxSizeMB: 50,
      dimensions: [
        { width: 1080, height: 1920 },
        { width: 1920, height: 1080 }
      ]
    },
    "Google Ads": {
      formats: ["mp4", "jpg", "png", "gif"],
      maxSizeMB: 150,
      dimensions: [
        { width: 1080, height: 1080 }, // Square
        { width: 1920, height: 1080 }, // 16:9
        { width: 1080, height: 1920 }  // 9:16
      ]
    },
    "Facebook": {
      formats: ["mp4", "jpg", "png"],
      maxSizeMB: 100,
      dimensions: [
        { width: 1080, height: 1080 },
        { width: 1200, height: 628 },
        { width: 1080, height: 1350 }
      ]
    }
  };

  constructor(api: OpenClawSkillApi) {
    this.api = api;
  }

  async createPackage(packageData: {
    name: string;
    materialIds: string[];
    platforms: string[];
    format?: DeliveryPackage["format"];
  }): Promise<string> {
    const id = `PKG-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const format = packageData.format || "zip";

    const pkg: DeliveryPackage = {
      id,
      name: packageData.name,
      materials: packageData.materialIds,
      format,
      platforms: packageData.platforms,
      status: "preparing",
      createdAt: new Date()
    };

    this.packages.set(id, pkg);
    this.api.log(`info`, `Delivery package created: ${id}`);

    // Start preparation
    await this.preparePackage(id);

    return id;
  }

  async getPackage(id: string): Promise<DeliveryPackage | null> {
    return this.packages.get(id) || null;
  }

  async listPackages(status?: DeliveryPackage["status"]): Promise<DeliveryPackage[]> {
    const all = Array.from(this.packages.values());
    if (status) {
      return all.filter(p => p.status === status);
    }
    return all;
  }

  async addMaterials(packageId: string, materialIds: string[]): Promise<boolean> {
    const pkg = this.packages.get(packageId);
    if (!pkg) {
      throw new Error(`Package not found: ${packageId}`);
    }

    if (pkg.status !== "preparing") {
      throw new Error(`Cannot add materials to package in status: ${pkg.status}`);
    }

    pkg.materials.push(...materialIds);
    pkg.updatedAt = new Date();
    this.packages.set(packageId, pkg);

    this.api.log(`info`, `Added ${materialIds.length} materials to package ${packageId}`);
    return true;
  }

  async removeMaterial(packageId: string, materialId: string): Promise<boolean> {
    const pkg = this.packages.get(packageId);
    if (!pkg) {
      throw new Error(`Package not found: ${packageId}`);
    }

    const index = pkg.materials.indexOf(materialId);
    if (index > -1) {
      pkg.materials.splice(index, 1);
      pkg.updatedAt = new Date();
      this.packages.set(packageId, pkg);
      this.api.log(`info`, `Removed material ${materialId} from package ${packageId}`);
    }

    return true;
  }

  async preparePackage(packageId: string): Promise<boolean> {
    const pkg = this.packages.get(packageId);
    if (!pkg) {
      throw new Error(`Package not found: ${packageId}`);
    }

    pkg.status = "preparing";
    this.packages.set(packageId, pkg);

    try {
      // Validate materials for each platform
      const validationResults = await this.validateMaterials(pkg);

      // Check if any materials don't meet requirements
      for (const [platform, issues] of Object.entries(validationResults)) {
        if (issues.length > 0) {
          this.api.log(`warn`, `Validation issues for ${platform}: ${issues.join(", ")}`);
        }
      }

      // Prepare package based on format
      switch (pkg.format) {
        case "zip":
          pkg.downloadUrl = await this.createZip(pkg);
          break;
        case "folder":
          // Create a shared folder
          pkg.downloadUrl = await this.createFolder(pkg);
          break;
        case "direct_upload":
          // Will upload directly to platforms
          break;
      }

      pkg.status = "ready";
      pkg.updatedAt = new Date();
      this.packages.set(packageId, pkg);

      this.api.log(`info`, `Package prepared: ${packageId}`);
      return true;
    } catch (error) {
      pkg.status = "failed";
      pkg.updatedAt = new Date();
      this.packages.set(packageId, pkg);
      this.api.log(`error`, `Package preparation failed: ${error}`);
      throw error;
    }
  }

  async distribute(packageId: string): Promise<Record<string, "success" | "failed">> {
    const pkg = this.packages.get(packageId);
    if (!pkg) {
      throw new Error(`Package not found: ${packageId}`);
    }

    if (pkg.status !== "ready") {
      throw new Error(`Package not ready for distribution: ${pkg.status}`);
    }

    pkg.status = "uploading";
    pkg.uploadStatus = {};
    this.packages.set(packageId, pkg);

    const results: Record<string, "success" | "failed"> = {};

    for (const platform of pkg.platforms) {
      try {
        await this.uploadToPlatform(packageId, platform);
        results[platform] = "success";
        if (pkg.uploadStatus) {
          pkg.uploadStatus[platform] = "success";
        }
      } catch (error) {
        results[platform] = "failed";
        if (pkg.uploadStatus) {
          pkg.uploadStatus[platform] = "failed";
        }
        this.api.log(`error`, `Upload to ${platform} failed: ${error}`);
      }
    }

    pkg.status = "completed";
    pkg.completedAt = new Date();
    pkg.updatedAt = new Date();
    this.packages.set(packageId, pkg);

    this.api.log(`info`, `Distribution completed for ${packageId}: ${JSON.stringify(results)}`);
    this.api.emit("delivery.completed", { packageId, results });

    return results;
  }

  async getPlatformRequirements(platform: string): Promise<any> {
    return this.platformRequirements[platform] || null;
  }

  async listPlatforms(): Promise<string[]> {
    return Object.keys(this.platformRequirements);
  }

  private async validateMaterials(pkg: DeliveryPackage): Promise<Record<string, string[]>> {
    const issues: Record<string, string[]> = {};

    for (const platform of pkg.platforms) {
      const req = this.platformRequirements[platform];
      if (!req) {
        issues[platform] = [`Unknown platform: ${platform}`];
        continue;
      }

      // Would validate each material against platform requirements
      // For now, return empty (no issues)
      issues[platform] = [];
    }

    return issues;
  }

  private async createZip(pkg: DeliveryPackage): Promise<string> {
    // Would create a zip file with all materials
    // For now, return a mock URL
    return `/tmp/delivery/${pkg.id}.zip`;
  }

  private async createFolder(pkg: DeliveryPackage): Promise<string> {
    // Would create a shared folder
    return `/tmp/delivery/${pkg.id}/`;
  }

  private async uploadToPlatform(packageId: string, platform: string): Promise<void> {
    const pkg = this.packages.get(packageId);
    if (!pkg) throw new Error(`Package not found: ${packageId}`);

    // This would integrate with platform APIs
    // For now, simulate upload
    this.api.log(`info`, `Uploading ${packageId} to ${platform}`);
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Random failure for demo (10% chance)
    if (Math.random() < 0.1) {
      throw new Error(`Upload failed: simulated error`);
    }
  }

  async convertFormat(materialId: string, targetFormat: string): Promise<{convertedId: string; path: string}> {
    // Would convert material to different format
    // For now, return mock
    return {
      convertedId: `${materialId}-conv-${Date.now()}`,
      path: `/tmp/conversions/${materialId}.${targetFormat}`
    };
  }

  async generateManifest(packageId: string): Promise<any> {
    const pkg = this.packages.get(packageId);
    if (!pkg) {
      throw new Error(`Package not found: ${packageId}`);
    }

    return {
      packageId: pkg.id,
      name: pkg.name,
      created: pkg.createdAt,
      format: pkg.format,
      platforms: pkg.platforms,
      materials: pkg.materials,
      status: pkg.status,
      downloadUrl: pkg.downloadUrl,
      uploadStatus: pkg.uploadStatus
    };
  }
}

export async function register(api: OpenClawSkillApi) {
  const delivery = new DeliveryDistribution(api);

  api.registerCommand("delivery", {
    description: "资源交付分发命令",
    subcommands: {
      create: {
        description: "创建交付包",
        arguments: {
          name: { type: "string", required: true, help: "包名称" },
          materialIds: { type: "string[]", required: true, help: "素材ID列表" },
          platforms: { type: "string[]", required: true, help: "目标平台列表" },
          format: { 
            type: "enum", 
            options: ["zip", "folder", "direct_upload"],
            help: "打包格式"
          }
        },
        execute: async (args) => {
          const packageId = await delivery.createPackage({
            name: args.name,
            materialIds: args.materialIds,
            platforms: args.platforms,
            format: args.format
          });
          return { success: true, packageId, message: `交付包已创建: ${packageId}` };
        }
      },
      get: {
        description: "查看交付包",
        arguments: {
          id: { type: "string", required: true, help: "包ID" }
        },
        execute: async (args) => {
          const pkg = await delivery.getPackage(args.id);
          if (!pkg) {
            return { success: false, error: `交付包未找到: ${args.id}` };
          }
          return { success: true, package: pkg };
        }
      },
      list: {
        description: "列出交付包",
        arguments: {
          status: { 
            type: "enum",
            options: ["preparing", "ready", "uploading", "completed", "failed"]
          }
        },
        execute: async (args) => {
          const packages = await delivery.listPackages(args.status);
          return { success: true, count: packages.length, packages };
        }
      },
      add: {
        description: "向包添加素材",
        arguments: {
          id: { type: "string", required: true, help: "包ID" },
          materialIds: { type: "string[]", required: true, help: "素材ID列表" }
        },
        execute: async (args) => {
          await delivery.addMaterials(args.id, args.materialIds);
          return { success: true, message: `已添加素材到包 ${args.id}` };
        }
      },
      prepare: {
        description: "准备交付包",
        arguments: {
          id: { type: "string", required: true, help: "包ID" }
        },
        execute: async (args) => {
          await delivery.preparePackage(args.id);
          const pkg = await delivery.getPackage(args.id);
          return { 
            success: true, 
            message: `包已准备就绪: ${args.id}`,
            downloadUrl: pkg?.downloadUrl
          };
        }
      },
      distribute: {
        description: "分发到目标平台",
        arguments: {
          id: { type: "string", required: true, help: "包ID" }
        },
        execute: async (args) => {
          const results = await delivery.distribute(args.id);
          return { success: true, results, message: `分发完成: ${JSON.stringify(results)}` };
        }
      },
      platforms: {
        description: "列出支持的平台",
        execute: async () => {
          const platforms = await delivery.listPlatforms();
          return { success: true, platforms };
        }
      },
      requirements: {
        description: "获取平台要求",
        arguments: {
          platform: { type: "string", required: true, help: "平台名称" }
        },
        execute: async (args) => {
          const req = await delivery.getPlatformRequirements(args.platform);
          if (!req) {
            return { success: false, error: `未知平台: ${args.platform}` };
          }
          return { success: true, platform: args.platform, requirements: req };
        }
      },
      convert: {
        description: "转换素材格式",
        arguments: {
          materialId: { type: "string", required: true, help: "素材ID" },
          format: { type: "string", required: true, help: "目标格式 (如: mp4, png)" }
        },
        execute: async (args) => {
          const result = await delivery.convertFormat(args.materialId, args.format);
          return { success: true, ...result, message: `格式转换完成` };
        }
      },
      manifest: {
        description: "生成清单",
        arguments: {
          id: { type: "string", required: true, help: "包ID" }
        },
        execute: async (args) => {
          const manifest = await delivery.generateManifest(args.id);
          return { success: true, manifest };
        }
      }
    }
  });

  // Listen for review completions to auto-package approved materials
  api.on("review.completed", async (data) => {
    const { review } = data as { review: any };
    if (review.passed) {
      api.log("info", `Material ${review.materialId} approved, could auto-package`);
      // Could auto-create delivery package for approved materials
    }
  });

  api.log("info", "Delivery & Distribution skill loaded");
}