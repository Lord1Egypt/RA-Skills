/**
 * Memory System Skill - 入口文件
 * 注册工具和 hooks
 */

import { memorySearch } from './search.js';
import { memoryGet } from './get.js';
import { memoryWrite } from './write.js';
import { memoryFlush } from './flush.js';
import { setupAutoLoad } from './autoLoad.js';

export interface MemorySystemConfig {
  memoryDir: string;
  flushMode: 'safeguard' | 'manual' | 'disabled';
  softThresholdTokens: number;
  vectorEnabled: boolean;
  embeddingModel: string;
}

const DEFAULT_CONFIG: MemorySystemConfig = {
  memoryDir: '~/.openclaw/workspace/memory',
  flushMode: 'safeguard',
  softThresholdTokens: 300000,
  vectorEnabled: true,
  embeddingModel: 'nomic-embed-text'
};

/**
 * 获取配置
 */
function getConfig(): MemorySystemConfig {
  // 从 OpenClaw 配置读取
  try {
    const userConfig = globalThis.openclaw?.config?.get?.('skills.memory-system');
    return { ...DEFAULT_CONFIG, ...userConfig };
  } catch {
    return DEFAULT_CONFIG;
  }
}

/**
 * Skill 入口 - 注册所有工具和 hooks
 */
export function registerMemorySystem() {
  const config = getConfig();

  console.log('[MemorySystem] 注册记忆系统工具...');

  // 注册工具
  const tools = {
    memory_search: {
      description: '语义搜索记忆',
      parameters: {
        query: { type: 'string', required: true },
        topK: { type: 'number', default: 5 },
        group: { type: 'string', required: false }
      },
      handler: async (params: { query: string; topK?: number; group?: string }) => {
        return await memorySearch(params.query, params.topK || 5, params.group, config);
      }
    },
    memory_get: {
      description: '读取记忆文件',
      parameters: {
        path: { type: 'string', required: true },
        from: { type: 'number', required: false },
        lines: { type: 'number', required: false }
      },
      handler: async (params: { path: string; from?: number; lines?: number }) => {
        return await memoryGet(params.path, params.from, params.lines, config);
      }
    },
    memory_write: {
      description: '写入记忆文件',
      parameters: {
        path: { type: 'string', required: true },
        content: { type: 'string', required: true },
        mode: { type: 'string', default: 'append' }
      },
      handler: async (params: { path: string; content: string; mode?: string }) => {
        return await memoryWrite(params.path, params.content, params.mode || 'append', config);
      }
    },
    memory_flush: {
      description: '手动触发 flush',
      parameters: {
        force: { type: 'boolean', default: false }
      },
      handler: async (params: { force?: boolean }) => {
        return await memoryFlush(params.force || false, config);
      }
    }
  };

  // 注册 hooks
  const hooks = {
    onSessionStart: {
      description: '会话启动时自动加载记忆',
      handler: async (context: { sessionType: string; groupId?: string }) => {
        return await setupAutoLoad(context, config);
      }
    }
  };

  return { tools, hooks, config };
}

/**
 * 启动检查
 */
export async function initMemorySystem() {
  const config = getConfig();
  
  console.log('[MemorySystem] 初始化记忆系统...');
  console.log(`[MemorySystem] 记忆目录: ${config.memoryDir}`);
  console.log(`[MemorySystem] Flush 模式: ${config.flushMode}`);
  console.log(`[MemorySystem] 向量搜索: ${config.vectorEnabled ? '启用' : '禁用'}`);

  // 检查 Ollama 是否运行
  if (config.vectorEnabled) {
    try {
      const { checkOllama } = await import('./embed.js');
      const ollamaStatus = await checkOllama();
      if (!ollamaStatus) {
        console.warn('[MemorySystem] ⚠️ Ollama 未运行，向量搜索将不可用');
      }
    } catch (e) {
      console.warn('[MemorySystem] ⚠️ 无法检查 Ollama 状态');
    }
  }
}

export default { register: registerMemorySystem, init: initMemorySystem };
