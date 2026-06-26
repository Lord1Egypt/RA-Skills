/**
 * ANFSF V1.5.0 - 内存模块依赖配置说明
 * 
 * 需要手动安装的依赖:
 * 
 * 1. @xenova/transformers - 本地向量嵌入模型
 *    npm install @xenova/transformers@latest
 * 
 * 2. langchain - 文本分割支持
 *    npm install langchain
 * 
 * 3. sqlite3 - 时间知识图谱存储
 *    npm install sqlite3
 * 
 * 4. 如果出现 sharp 安装问题:
 *    - 方案 A: 安装系统依赖
 *      sudo apt-get update && sudo apt-get install -y build-essential
 *    - 方案 B: 跳过 sharp
 *      npm install --ignore-scripts
 */

// ============================================================================
// 替代方案: 使用 OpenAI Embeddings (现有配置)
// ============================================================================

/**
 * 由于本地嵌入器安装依赖的复杂性，
 * 建议在中国大陆环境下使用 OpenAI Embeddings (已有配置)
 * 
 * 已有配置:
 * - Model: text-embedding-v2
 * - Provider: OpenAI
 * - Enabled: true
 */

import { 
  OpenAIEmbeddings 
} from '@langchain/openai';

/**
 * 使用 OpenAI 的嵌入器（替代 LocalEmbedder）
 */
export class OpenAIEmbeddingAdapter {
  private embeddings: OpenAIEmbeddings;

  constructor() {
    this.embeddings = new OpenAIEmbeddings({
      apiKey: process.env.ALGER_BAILIAN_API_KEY,
      model: 'text-embedding-v2'
    });
  }

  async embed(text: string): Promise<number[]> {
    return this.embeddings.embed(text);
  }

  async embedBatch(texts: string[]): Promise<number[][]> {
    return this.embeddings.embedDocuments(texts);
  }
}

/**
 * 在内存检索器中使用 OpenAI 嵌入
 */
export class HierarchicalMemoryRetriever {
  // ... (其他代码保持不变)
  
  private async embedContent(text: string): Promise<number[]> {
    // 使用 OpenAI 嵌入（生产环境推荐）
    const adapter = new OpenAIEmbeddingAdapter();
    return adapter.embed(text);
    
    // 或使用本地嵌入（开发/离线环境）
    // const localEmbedder = new LocalEmbedder();
    // return localEmbedder.embed(text);
  }

  // ... (其余代码)
}

// ============================================================================
// 推荐部署方案
// ============================================================================

/**
 * 方案 A: OpenAI Embeddings (推荐)
 * ✅ 零配置
 * ✅ 高质量
 * ⚠️ 需要 API Key
 * 
 * 适用场景:
 * - 生产环境
 * - 云部署
 * - API 通行情况好
 */

/**
 * 方案 B: 本地嵌入器
 * ✅ 完全本地
 * ✅ 无 API 依赖
 * ⚠️ 需要安装依赖
 * ⚠️ 首次运行需要下载模型
 * 
 * 适用场景:
 * - 本地开发
 * - 离线环境
 * - 数据隐私要求高
 */

/**
 * 集成说明:
 * 
 * 1. 在内存检索器中添加条件判断
 * 2. 根据环境变量选择嵌入器
 * 3. 提供降级策略
 */

export const getEmbedder = () => {
  const useLocal = process.env.USE_LOCAL_EMBEDDER === 'true';
  
  if (useLocal) {
    return new LocalEmbedder();
  }
  return new OpenAIEmbeddingAdapter();
};
