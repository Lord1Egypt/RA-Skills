import { OpenClawSkillApi } from "openclaw/skill-sdk";

interface Material {
  id: string;
  name: string;
  type: "image" | "video" | "audio" | "other";
  format: string;
  size: { width?: number; height?: number; duration?: number };
  source: string;
  tags: string[];
  prompt?: string;
  generationParams?: Record<string, any>;
  version: number;
  status: "uploaded" | "processing" | "available" | "archived";
  createdAt: Date;
  updatedAt: Date;
  metadata?: Record<string, any>;
  fileToken?: string;
}

class MaterialLibrary {
  private materials: Map<string, Material> = new Map();
  private api: OpenClawSkillApi;

  constructor(api: OpenClawSkillApi) {
    this.api = api;
  }

  async upload(file: Buffer, metadata: {
    name: string;
    type: Material["type"];
    format: string;
    tags?: string[];
    prompt?: string;
  }): Promise<string> {
    const id = `MAT-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    // Store file (would integrate with drive or storage)
    const fileToken = await this.storeFile(file, id, metadata.format);

    const material: Material = {
      id,
      name: metadata.name,
      type: metadata.type,
      format: metadata.format,
      size: {}, // Extract from file
      source: "upload",
      tags: metadata.tags || [],
      prompt: metadata.prompt,
      version: 1,
      status: "uploaded",
      createdAt: new Date(),
      updatedAt: new Date(),
      fileToken,
    };

    this.materials.set(id, material);

    // Auto-tagging if configured
    if (this.api.config?.autoTagging) {
      await this.autoTag(id);
    }

    this.api.log(`info`, `Material uploaded: ${id} (${metadata.name})`);
    return id;
  }

  async get(id: string): Promise<Material | null> {
    return this.materials.get(id) || null;
  }

  async search(query: {
    tags?: string[];
    type?: Material["type"];
    format?: string;
    hasPrompt?: boolean;
    minVersion?: number;
  }): Promise<Material[]> {
    const all = Array.from(this.materials.values());
    
    return all.filter(m => {
      if (query.tags && !query.tags.some(t => m.tags.includes(t))) return false;
      if (query.type && m.type !== query.type) return false;
      if (query.format && m.format !== query.format) return false;
      if (query.hasPrompt && !m.prompt) return false;
      if (query.minVersion && m.version < query.minVersion) return false;
      return true;
    });
  }

  async findSimilar(materialId: string, limit: number = 10): Promise<Material[]> {
    const source = this.materials.get(materialId);
    if (!source) {
      throw new Error(`Material not found: ${materialId}`);
    }

    // Find materials with overlapping tags and similar type/format
    const all = Array.from(this.materials.values());
    const scores = all
      .filter(m => m.id !== materialId)
      .map(m => ({
        material: m,
        score: this.calculateSimilarity(source, m)
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
      .map(s => s.material);

    return scores;
  }

  async createVersion(materialId: string, changes: {
    newFile?: Buffer;
    newTags?: string[];
    newMetadata?: Record<string, any>;
  }): Promise<string> {
    const original = this.materials.get(materialId);
    if (!original) {
      throw new Error(`Material not found: ${materialId}`);
    }

    const newId = `${materialId}.v${original.version + 1}`;
    
    const newMaterial: Material = {
      ...original,
      id: newId,
      version: original.version + 1,
      updatedAt: new Date(),
      tags: changes.newTags || original.tags,
      metadata: { ...original.metadata, ...changes.newMetadata },
    };

    if (changes.newFile) {
      newMaterial.fileToken = await this.storeFile(changes.newFile, newId, original.format);
    }

    this.materials.set(newId, newMaterial);

    this.api.log(`info`, `Created new version: ${materialId} -> ${newId}`);
    return newId;
  }

  async archive(materialId: string): Promise<boolean> {
    const material = this.materials.get(materialId);
    if (!material) {
      throw new Error(`Material not found: ${materialId}`);
    }

    material.status = "archived";
    material.updatedAt = new Date();
    this.materials.set(materialId, material);

    this.api.log(`info`, `Material archived: ${materialId}`);
    return true;
  }

  async addTags(materialId: string, tags: string[]): Promise<boolean> {
    const material = this.materials.get(materialId);
    if (!material) {
      throw new Error(`Material not found: ${materialId}`);
    }

    for (const tag of tags) {
      if (!material.tags.includes(tag)) {
        material.tags.push(tag);
      }
    }

    material.updatedAt = new Date();
    this.materials.set(materialId, material);

    this.api.log(`info`, `Added tags to ${materialId}: ${tags.join(", ")}`);
    return true;
  }

  async getStats(): Promise<{
    total: number;
    byType: Record<string, number>;
    byStatus: Record<string, number>;
    totalSize: number;
  }> {
    const all = Array.from(this.materials.values());
    
    const byType: Record<string, number> = {};
    const byStatus: Record<string, number> = {};

    for (const m of all) {
      byType[m.type] = (byType[m.type] || 0) + 1;
      byStatus[m.status] = (byStatus[m.status] || 0) + 1;
    }

    return {
      total: all.length,
      byType,
      byStatus,
      totalSize: 0, // Calculate from storage
    };
  }

  private async storeFile(file: Buffer, id: string, format: string): Promise<string> {
    // This would integrate with feishu_drive_file or other storage
    // For now, return a mock token
    return `token-${id}-${Date.now()}`;
  }

  private async autoTag(materialId: string): Promise<void> {
    const material = this.materials.get(materialId);
    if (!material) return;

    // AI-based auto-tagging would go here
    // For now, add some basic tags
    if (material.type === "video") {
      material.tags.push("video", "motion");
    } else if (material.type === "image") {
      material.tags.push("static", "image");
    }

    this.api.log(`debug`, `Auto-tagged ${materialId}: ${material.tags.join(", ")}`);
  }

  private calculateSimilarity(a: Material, b: Material): number {
    let score = 0;

    // Same type increases score
    if (a.type === b.type) score += 10;

    // Overlapping tags
    const commonTags = a.tags.filter(t => b.tags.includes(t));
    score += commonTags.length * 5;

    // Same format
    if (a.format === b.format) score += 5;

    // Similar prompt keywords (very basic)
    if (a.prompt && b.prompt) {
      const aWords = new Set(a.prompt.toLowerCase().split(/\s+/));
      const bWords = new Set(b.prompt.toLowerCase().split(/\s+/));
      const commonWords = [...aWords].filter(w => bWords.has(w));
      score += commonWords.length * 2;
    }

    return score;
  }
}

export async function register(api: OpenClawSkillApi) {
  const library = new MaterialLibrary(api);

  api.registerCommand("material", {
    description: "素材库管理命令",
    subcommands: {
      upload: {
        description: "上传素材",
        arguments: {
          name: { type: "string", required: true, help: "素材名称" },
          type: { 
            type: "enum", 
            required: true, 
            options: ["image", "video", "audio", "other"],
            help: "素材类型"
          },
          format: { type: "string", required: true, help: "格式 (如: png, mp4, wav)" },
          tags: { type: "string[]", help: "标签列表" },
          prompt: { type: "string", help: "生成提示词 (可选)" }
        },
        execute: async (args) => {
          // Note: file upload would need different handling in OpenClaw
          // This is a simplified version
          return { 
            success: false, 
            error: "文件上传需要额外的OpenClaw集成，请使用飞书文件上传或本地路径" 
          };
        }
      },
      get: {
        description: "获取素材详情",
        arguments: {
          id: { type: "string", required: true, help: "素材ID" }
        },
        execute: async (args) => {
          const material = await library.get(args.id);
          if (!material) {
            return { success: false, error: `素材未找到: ${args.id}` };
          }
          return { success: true, material };
        }
      },
      search: {
        description: "搜索素材",
        arguments: {
          tags: { type: "string[]", help: "标签筛选" },
          type: { type: "string", help: "类型筛选" },
          format: { type: "string", help: "格式筛选" }
        },
        execute: async (args) => {
          const results = await library.search({
            tags: args.tags,
            type: args.type,
            format: args.format
          });
          return { success: true, count: results.length, materials: results };
        }
      },
      similar: {
        description: "查找相似素材",
        arguments: {
          id: { type: "string", required: true, help: "素材ID" },
          limit: { type: "number", help: "返回数量 (默认10)" }
        },
        execute: async (args) => {
          const results = await library.findSimilar(args.id, args.limit);
          return { success: true, count: results.length, materials: results };
        }
      },
      stats: {
        description: "获取库统计信息",
        execute: async () => {
          const stats = await library.getStats();
          return { success: true, stats };
        }
      },
      version: {
        description: "创建新版本",
        arguments: {
          id: { type: "string", required: true, help: "素材ID" }
        },
        execute: async (args) => {
          const newId = await library.createVersion(args.id, {});
          return { success: true, newId, message: `新版本: ${newId}` };
        }
      },
      archive: {
        description: "归档素材",
        arguments: {
          id: { type: "string", required: true, help: "素材ID" }
        },
        execute: async (args) => {
          await library.archive(args.id);
          return { success: true, message: `素材已归档: ${args.id}` };
        }
      }
    }
  });

  api.log("info", "Material Library skill loaded");
}