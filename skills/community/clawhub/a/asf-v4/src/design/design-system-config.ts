/**
 * Design System 配置加载器
 * 
 * 层级：Layer 8.5.6 - UI Contract Pack
 * 功能：读取 design-mapping.yaml，关键词匹配设计系统
 * 版本：V1.0.0
 * 状态：✅ 完成
 */

import * as fs from 'fs';
import * as path from 'path';
import { load as parseYaml } from 'js-yaml';

// ============== 类型定义 ==============

export interface DesignMappingConfig {
  version: string;
  default: string;
  keywords: Record<string, string>;
  excludes: Array<{ pattern: string; design: string }>;
  aliases: Record<string, string[]>;
  designSystems: Record<string, DesignSystemMeta>;
}

export interface DesignSystemMeta {
  name: string;
  description: string;
  tags: string[];
  primaryColor: string;
  darkMode: boolean;
}

export interface MatchResult {
  designSystem: string;
  matchedBy: 'user_specified' | 'keyword' | 'alias' | 'default';
  confidence: number;
  metadata?: DesignSystemMeta;
}

// ============== 核心类 ==============

export class DesignSystemConfigLoader {
  private static instance: DesignSystemConfigLoader;
  private config: DesignMappingConfig | null = null;
  private configPath: string;
  private lastModified: number = 0;
  private fileWatcher: fs.FSWatcher | null = null;

  private constructor(configPath?: string) {
    this.configPath = configPath || path.join(
      __dirname,
      '../../config/design-mapping.yaml'
    );
    this.loadConfig();
    this.watchConfigFile();
  }

  static getInstance(configPath?: string): DesignSystemConfigLoader {
    if (!DesignSystemConfigLoader.instance) {
      DesignSystemConfigLoader.instance = new DesignSystemConfigLoader(configPath);
    }
    return DesignSystemConfigLoader.instance;
  }

  /**
   * 加载配置文件
   */
  private loadConfig(): void {
    try {
      const yamlContent = fs.readFileSync(this.configPath, 'utf-8');
      this.config = this.parseYaml(yamlContent);
      this.lastModified = fs.statSync(this.configPath).mtimeMs;
      console.log(`[DesignSystemConfig] ✅ Config loaded: ${this.configPath}`);
    } catch (error) {
      console.error(`[DesignSystemConfig] ❌ Failed to load config:`, error);
      // 使用默认配置
      this.config = this.getDefaultConfig();
    }
  }

  /**
   * 解析 YAML (使用 js-yaml)
   */
  private parseYaml(yaml: string): DesignMappingConfig {
    try {
      const config = parseYaml(yaml) as DesignMappingConfig;
      return config;
    } catch (error) {
      console.error('[DesignSystemConfig] ❌ YAML parse error:', error);
      return this.getDefaultConfig();
    }
  }

  /**
   * 获取默认配置
   */
  private getDefaultConfig(): DesignMappingConfig {
    return {
      version: '1.0.0',
      default: 'linear',
      keywords: {
        'saas|生产力': 'linear',
        '支付|payment': 'stripe',
        '营销|landing': 'vercel',
        'apple|苹果': 'apple',
        'ai|人工智能': 'claude',
      },
      excludes: [],
      aliases: {},
      designSystems: {},
    };
  }

  /**
   * 监听配置文件变化
   */
  private watchConfigFile(): void {
    try {
      this.fileWatcher = fs.watch(this.configPath, (event) => {
        if (event === 'change') {
          this.reload();
        }
      });
      console.log(`[DesignSystemConfig] 👁️ Watching config file`);
    } catch (error) {
      console.error(`[DesignSystemConfig] ⚠️ Cannot watch file:`, error);
    }
  }

  /**
   * 重新加载配置
   */
  private reload(): void {
    const stats = fs.statSync(this.configPath);
    if (stats.mtimeMs > this.lastModified) {
      this.loadConfig();
      console.log(`[DesignSystemConfig] 🔄 Config reloaded`);
    }
  }

  /**
   * 匹配设计系统
   */
  match(text: string): MatchResult {
    // 1. 检查用户是否直接指定了设计系统
    const userSpecified = this.extractUserSpecified(text);
    if (userSpecified) {
      const resolved = this.resolveAlias(userSpecified);
      return {
        designSystem: resolved || userSpecified,
        matchedBy: 'user_specified',
        confidence: 1.0,
        metadata: this.config?.designSystems[resolved || userSpecified],
      };
    }

    // 2. 关键词匹配
    for (const [pattern, design] of Object.entries(this.config?.keywords || {})) {
      const regex = new RegExp(pattern, 'i');
      if (regex.test(text)) {
        // 检查排除规则
        if (this.isExcluded(text, design)) {
          continue;
        }
        return {
          designSystem: design,
          matchedBy: 'keyword',
          confidence: 0.8,
          metadata: this.config?.designSystems[design],
        };
      }
    }

    // 3. 使用默认值
    return {
      designSystem: this.config?.default || 'linear',
      matchedBy: 'default',
      confidence: 0.5,
      metadata: this.config?.designSystems[this.config?.default || 'linear'],
    };
  }

  /**
   * 提取用户指定的设计系统
   */
  private extractUserSpecified(text: string): string | null {
    const patterns = [
      /使用\s*([a-zA-Z\u4e00-\u9fa5]+)\s*风格/,
      /按\s*([a-zA-Z\u4e00-\u9fa5]+)\s*设计/,
      /参考\s*([a-zA-Z\u4e00-\u9fa5]+)/,
      /design[:\s]*([a-zA-Z]+)/i,
      /style[:\s]*([a-zA-Z]+)/i,
    ];

    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        return match[1].toLowerCase();
      }
    }
    return null;
  }

  /**
   * 解析别名
   */
  resolveAlias(input: string): string | null {
    const normalized = input.toLowerCase();
    for (const [design, aliases] of Object.entries(this.config?.aliases || {})) {
      if (aliases.includes(normalized)) {
        return design;
      }
    }
    return null;
  }

  /**
   * 检查排除规则
   */
  private isExcluded(text: string, design: string): boolean {
    for (const exclude of this.config?.excludes || []) {
      if (exclude.design === design) {
        const regex = new RegExp(exclude.pattern, 'i');
        if (regex.test(text)) {
          return true;
        }
      }
    }
    return false;
  }

  /**
   * 获取默认设计系统
   */
  getDefault(): string {
    return this.config?.default || 'linear';
  }

  /**
   * 获取所有设计系统元数据
   */
  getAllDesignSystems(): Record<string, DesignSystemMeta> {
    return this.config?.designSystems || {};
  }

  /**
   * 获取配置版本
   */
  getVersion(): string {
    return this.config?.version || '1.0.0';
  }

  /**
   * 清理资源
   */
  dispose(): void {
    if (this.fileWatcher) {
      this.fileWatcher.close();
      this.fileWatcher = null;
    }
  }
}

// ============== 导出 ==============

export default DesignSystemConfigLoader;
