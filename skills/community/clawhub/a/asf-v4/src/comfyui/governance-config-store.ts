/**
 * 治理配置持久化存储
 * 
 * 层级：Layer 8.5 - Governance Control Plane
 * 功能：治理配置持久化、版本管理、热更新
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { GovernanceConfig, SandboxConfig } from './comfyui-workflow-orchestrator';
import { QualityGuardConfig, RollbackConfig } from './video-quality-guard';
import { MCPBusConfig } from './mcp-video-bus';

// ============== 类型定义 ==============

/**
 * 配置版本
 */
export interface ConfigVersion {
  /** 版本号 */
  version: string;
  /** 创建时间 */
  createdAt: number;
  /** 创建者 */
  createdBy: string;
  /** 变更说明 */
  changeDescription?: string;
}

/**
 * 配置快照
 */
export interface ConfigSnapshot {
  /** 配置 ID */
  id: string;
  /** 配置版本 */
  version: ConfigVersion;
  /** 治理配置 */
  governance: GovernanceConfig;
  /** 沙箱配置 */
  sandbox: SandboxConfig;
  /** 质量门禁配置 */
  qualityGuard: QualityGuardConfig;
  /** 回滚配置 */
  rollback: RollbackConfig;
  /** MCP 总线配置 */
  mcpBus: MCPBusConfig;
  /** 是否激活 */
  isActive: boolean;
}

/**
 * 配置存储接口
 */
export interface ConfigStore {
  /** 保存配置 */
  save(snapshot: ConfigSnapshot): Promise<void>;
  /** 获取配置 */
  get(id: string): Promise<ConfigSnapshot | undefined>;
  /** 获取激活配置 */
  getActive(): Promise<ConfigSnapshot | undefined>;
  /** 激活配置 */
  activate(id: string): Promise<void>;
  /** 列出所有配置 */
  list(): Promise<ConfigSnapshot[]>;
  /** 删除配置 */
  delete(id: string): Promise<void>;
}

/**
 * 配置验证结果
 */
export interface ConfigValidationResult {
  /** 是否有效 */
  valid: boolean;
  /** 错误信息 */
  errors: string[];
  /** 警告信息 */
  warnings: string[];
}

// ============== 默认配置 ==============

const DEFAULT_GOVERNANCE_CONFIG: GovernanceConfig = {
  maxDurationSeconds: 10,
  maxResolution: '1080P',
  maxGenerationTimeSeconds: 60,
  minQualityScore: 0.7,
  maxCostPerRequest: 0.1,
  requestsPerMinute: 10,
  dailyQuota: 100,
};

const DEFAULT_SANDBOX_CONFIG: SandboxConfig = {
  memoryLimitMB: 512,
  timeoutSeconds: 60,
  gpuIsolated: true,
  allowedApis: ['video_generate'],
  deniedApis: ['external_upload'],
};

const DEFAULT_QUALITY_GUARD_CONFIG: QualityGuardConfig = {
  minPassScore: 0.7,
  retryThreshold: 0.5,
  maxRetries: 3,
  manualReviewThreshold: 0.6,
  enabledChecks: [
    'resolution',
    'duration',
    'aspectRatio',
    'visualQuality',
    'audioQuality',
    'contentSafety',
    'brandConsistency',
  ],
  criticalChecks: ['resolution', 'contentSafety'],
};

const DEFAULT_ROLLBACK_CONFIG: RollbackConfig = {
  enabled: true,
  triggerConditions: {
    qualityScoreBelow: 0.5,
    criticalCheckFailed: true,
    consecutiveFailures: 3,
  },
  actions: {
    notifyAdmin: true,
    markAsHighRisk: true,
    pauseAutoDeploy: true,
  },
};

const DEFAULT_MCP_BUS_CONFIG: MCPBusConfig = {
  defaultTTLSeconds: 300,
  maxRetries: 3,
  retryIntervalMs: 1000,
  enableTracing: true,
  enableIdempotency: true,
};

// ============== 核心类 ==============

/**
 * 内存配置存储 (生产环境可替换为数据库存储)
 */
export class InMemoryConfigStore implements ConfigStore {
  private store: Map<string, ConfigSnapshot> = new Map();
  private activeConfigId: string | null = null;

  async save(snapshot: ConfigSnapshot): Promise<void> {
    // 验证配置
    const validation = this.validateConfig(snapshot);
    if (!validation.valid) {
      throw new Error(`Invalid config: ${validation.errors.join(', ')}`);
    }

    this.store.set(snapshot.id, snapshot);
    console.log(`[Config Store] 💾 Config saved: ${snapshot.id} (v${snapshot.version.version})`);
  }

  async get(id: string): Promise<ConfigSnapshot | undefined> {
    return this.store.get(id);
  }

  async getActive(): Promise<ConfigSnapshot | undefined> {
    if (!this.activeConfigId) {
      return undefined;
    }
    return this.store.get(this.activeConfigId);
  }

  async activate(id: string): Promise<void> {
    const snapshot = this.store.get(id);
    if (!snapshot) {
      throw new Error(`Config not found: ${id}`);
    }

    // 更新激活状态
    this.store.forEach(s => {
      s.isActive = false;
    });
    snapshot.isActive = true;
    this.activeConfigId = id;

    console.log(`[Config Store] ✅ Config activated: ${id}`);
  }

  async list(): Promise<ConfigSnapshot[]> {
    return Array.from(this.store.values()).sort(
      (a, b) => b.version.createdAt - a.version.createdAt
    );
  }

  async delete(id: string): Promise<void> {
    if (this.activeConfigId === id) {
      throw new Error('Cannot delete active config');
    }
    this.store.delete(id);
    console.log(`[Config Store] 🗑️ Config deleted: ${id}`);
  }

  /**
   * 创建默认配置快照
   */
  createDefaultSnapshot(createdBy: string = 'system'): ConfigSnapshot {
    const now = Date.now();
    return {
      id: `config_default_${now}`,
      version: {
        version: '1.0.0',
        createdAt: now,
        createdBy,
        changeDescription: 'Initial default configuration',
      },
      governance: { ...DEFAULT_GOVERNANCE_CONFIG },
      sandbox: { ...DEFAULT_SANDBOX_CONFIG },
      qualityGuard: { ...DEFAULT_QUALITY_GUARD_CONFIG },
      rollback: { ...DEFAULT_ROLLBACK_CONFIG },
      mcpBus: { ...DEFAULT_MCP_BUS_CONFIG },
      isActive: false,
    };
  }

  /**
   * 验证配置
   */
  private validateConfig(snapshot: ConfigSnapshot): ConfigValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // 治理配置验证
    if (snapshot.governance.maxDurationSeconds > 60) {
      errors.push('maxDurationSeconds cannot exceed 60s');
    }
    if (snapshot.governance.dailyQuota < 1) {
      errors.push('dailyQuota must be at least 1');
    }
    if (snapshot.governance.requestsPerMinute < 1) {
      errors.push('requestsPerMinute must be at least 1');
    }

    // 沙箱配置验证
    if (snapshot.sandbox.memoryLimitMB < 128) {
      warnings.push('memoryLimitMB below 128MB may cause issues');
    }
    if (snapshot.sandbox.timeoutSeconds > 300) {
      errors.push('timeoutSeconds cannot exceed 300s');
    }

    // 质量门禁配置验证
    if (snapshot.qualityGuard.minPassScore < 0 || snapshot.qualityGuard.minPassScore > 1) {
      errors.push('minPassScore must be between 0 and 1');
    }
    if (snapshot.qualityGuard.retryThreshold >= snapshot.qualityGuard.minPassScore) {
      errors.push('retryThreshold must be less than minPassScore');
    }

    // MCP 总线配置验证
    if (snapshot.mcpBus.defaultTTLSeconds < 60) {
      warnings.push('defaultTTLSeconds below 60s may cause premature expiration');
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings,
    };
  }
}

/**
 * 配置管理器
 */
export class ConfigManager {
  private store: ConfigStore;
  private changeListeners: Array<(snapshot: ConfigSnapshot) => void> = [];

  constructor(store: ConfigStore = new InMemoryConfigStore()) {
    this.store = store;
  }

  /**
   * 初始化默认配置
   */
  async initialize(createdBy: string = 'system'): Promise<ConfigSnapshot> {
    const existing = await this.store.getActive();
    if (existing) {
      console.log('[Config Manager] ✅ Active config already exists');
      return existing;
    }

    const defaultConfig = (this.store as InMemoryConfigStore).createDefaultSnapshot(createdBy);
    await this.store.save(defaultConfig);
    await this.store.activate(defaultConfig.id);

    console.log('[Config Manager] 🎉 Default config initialized');
    return defaultConfig;
  }

  /**
   * 获取当前配置
   */
  async getCurrentConfig(): Promise<ConfigSnapshot> {
    const active = await this.store.getActive();
    if (!active) {
      throw new Error('No active configuration. Call initialize() first.');
    }
    return active;
  }

  /**
   * 创建配置副本
   */
  async cloneConfig(baseId: string, newVersion: string, changeDescription: string): Promise<ConfigSnapshot> {
    const base = await this.store.get(baseId);
    if (!base) {
      throw new Error(`Config not found: ${baseId}`);
    }

    const now = Date.now();
    const cloned: ConfigSnapshot = {
      ...base,
      id: `config_${now}`,
      version: {
        version: newVersion,
        createdAt: now,
        createdBy: 'admin',
        changeDescription,
      },
      isActive: false,
    };

    await this.store.save(cloned);
    console.log(`[Config Manager] 📋 Config cloned: ${cloned.id} from ${baseId}`);
    return cloned;
  }

  /**
   * 更新配置
   */
  async updateConfig(
    id: string,
    updates: Partial<ConfigSnapshot>
  ): Promise<ConfigSnapshot> {
    const config = await this.store.get(id);
    if (!config) {
      throw new Error(`Config not found: ${id}`);
    }

    const updated: ConfigSnapshot = {
      ...config,
      ...updates,
      version: {
        ...config.version,
        version: `${config.version.version}-updated`,
      },
    };

    await this.store.save(updated);
    console.log(`[Config Manager] ✏️ Config updated: ${id}`);

    // 通知监听器
    this.notifyChangeListeners(updated);

    return updated;
  }

  /**
   * 激活配置
   */
  async activateConfig(id: string): Promise<void> {
    await this.store.activate(id);
    const config = await this.store.get(id);
    if (config) {
      this.notifyChangeListeners(config);
    }
  }

  /**
   * 列出所有配置
   */
  async listConfigs(): Promise<ConfigSnapshot[]> {
    return this.store.list();
  }

  /**
   * 注册配置变更监听器
   */
  onChange(listener: (snapshot: ConfigSnapshot) => void): void {
    this.changeListeners.push(listener);
  }

  /**
   * 导出配置为 JSON
   */
  async exportConfig(id: string): Promise<string> {
    const config = await this.store.get(id);
    if (!config) {
      throw new Error(`Config not found: ${id}`);
    }
    return JSON.stringify(config, null, 2);
  }

  /**
   * 从 JSON 导入配置
   */
  async importConfig(json: string): Promise<ConfigSnapshot> {
    const config: ConfigSnapshot = JSON.parse(json);
    await this.store.save(config);
    console.log(`[Config Manager] 📥 Config imported: ${config.id}`);
    return config;
  }

  private notifyChangeListeners(snapshot: ConfigSnapshot): void {
    this.changeListeners.forEach(listener => {
      try {
        listener(snapshot);
      } catch (error) {
        console.error('[Config Manager] Listener error:', error);
      }
    });
  }
}

// ============== 导出 ==============

export default ConfigManager;
