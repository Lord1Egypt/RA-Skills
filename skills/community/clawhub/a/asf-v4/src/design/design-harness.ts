/**
 * Design UI/UX Harness 集成
 * 
 * 层级：Layer 8.5.6 - UI Contract Pack
 * 功能：将 DesignSystemConfigLoader 集成到 ANFSF UI/UX Harness
 * 版本：V1.0.0
 * 状态：✅ 完成
 */

import { DesignSystemConfigLoader, MatchResult, DesignSystemMeta } from './design-system-config';
import * as fs from 'fs';
import * as path from 'path';

// ============== 类型定义 ==============

export interface DesignContext {
  requirement: string;
  matchedDesign?: MatchResult;
  designContent?: string;
}

export interface DesignSystemResponse {
  designSystem: string;
  matchedBy: 'user_specified' | 'keyword' | 'alias' | 'default';
  confidence: number;
  metadata?: DesignSystemMeta;
  designContent?: string;
  error?: string;
}

// ============== 核心类 ==============

/**
 * UI/UX Design Harness
 * 
 * 负责根据用户需求匹配设计系统，并加载对应的 DESIGN.md 内容
 */
export class DesignHarness {
  private configLoader: DesignSystemConfigLoader;
  private designSystemsPath: string;

  constructor(designSystemsPath?: string) {
    this.configLoader = DesignSystemConfigLoader.getInstance();
    this.designSystemsPath = designSystemsPath || path.join(
      __dirname,
      '../../design-systems'
    );
  }

  /**
   * 根据需求匹配设计系统
   * 
   * @param requirement 用户需求描述
   * @returns 设计系统匹配结果
   */
  match(requirement: string): DesignSystemResponse {
    try {
      const result = this.configLoader.match(requirement);
      
      return {
        designSystem: result.designSystem,
        matchedBy: result.matchedBy,
        confidence: result.confidence,
        metadata: result.metadata,
      };
    } catch (error) {
      return {
        designSystem: this.configLoader.getDefault(),
        matchedBy: 'default',
        confidence: 0.5,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  /**
   * 获取设计系统内容
   * 
   * @param designSystemName 设计系统名称
   * @returns DESIGN.md 内容
   */
  getDesignContent(designSystemName: string): string | null {
    try {
      const designPath = path.join(
        this.designSystemsPath,
        designSystemName,
        'DESIGN.md'
      );

      if (fs.existsSync(designPath)) {
        return fs.readFileSync(designPath, 'utf-8');
      }

      return null;
    } catch (error) {
      console.error(`[DesignHarness] ❌ Failed to read design content:`, error);
      return null;
    }
  }

  /**
   * 根据需求匹配并获取设计系统内容
   * 
   * @param requirement 用户需求描述
   * @returns 完整的设计系统响应
   */
  matchWithContent(requirement: string): DesignSystemResponse {
    const matchResult = this.match(requirement);
    
    if (matchResult.error) {
      return matchResult;
    }

    const content = this.getDesignContent(matchResult.designSystem);
    
    return {
      ...matchResult,
      designContent: content || undefined,
    };
  }

  /**
   * 获取所有可用的设计系统
   * 
   * @returns 设计系统元数据列表
   */
  getAllDesignSystems(): Record<string, DesignSystemMeta> {
    return this.configLoader.getAllDesignSystems();
  }

  /**
   * 获取设计系统列表（仅名称）
   * 
   * @returns 设计系统名称数组
   */
  getDesignSystemList(): string[] {
    return Object.keys(this.configLoader.getAllDesignSystems());
  }

  /**
   * 获取默认设计系统
   * 
   * @returns 默认设计系统名称
   */
  getDefault(): string {
    return this.configLoader.getDefault();
  }

  /**
   * 获取配置版本
   * 
   * @returns 配置版本号
   */
  getVersion(): string {
    return this.configLoader.getVersion();
  }

  /**
   * 验证设计系统是否存在
   * 
   * @param designSystemName 设计系统名称
   * @returns 是否存在
   */
  exists(designSystemName: string): boolean {
    const designPath = path.join(
      this.designSystemsPath,
      designSystemName,
      'DESIGN.md'
    );
    return fs.existsSync(designPath);
  }

  /**
   * 搜索设计系统
   * 
   * @param query 搜索关键词
   * @returns 匹配的设计系统列表
   */
  search(query: string): DesignSystemResponse[] {
    const results: DesignSystemResponse[] = [];
    const systems = this.getAllDesignSystems();

    for (const [name, metadata] of Object.entries(systems)) {
      // 按名称匹配
      if (name.toLowerCase().includes(query.toLowerCase())) {
        results.push({
          designSystem: name,
          matchedBy: 'keyword',
          confidence: 1.0,
          metadata,
        });
        continue;
      }

      // 按标签匹配
      if (metadata.tags?.some(tag => 
        tag.toLowerCase().includes(query.toLowerCase())
      )) {
        results.push({
          designSystem: name,
          matchedBy: 'keyword',
          confidence: 0.8,
          metadata,
        });
      }
    }

    return results;
  }
}

// ============== 导出 ==============

// 单例实例
let designHarnessInstance: DesignHarness | null = null;

export function getDesignHarness(designSystemsPath?: string): DesignHarness {
  if (!designHarnessInstance) {
    designHarnessInstance = new DesignHarness(designSystemsPath);
  }
  return designHarnessInstance;
}

export default DesignHarness;