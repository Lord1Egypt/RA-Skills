import { BaseAPI } from "./base.js";

export class OllamaAPI extends BaseAPI {
  /**
   * 列出 Ollama 模型
   */
  async list(): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/search", { page: 1, pageSize: 100 });
  }

  /**
   * 创建 Ollama 模型
   */
  async create(name: string): Promise<any> {
    return this.post("/api/v2/ai/ollama/model", { name });
  }

  /**
   * 删除 Ollama 模型
   */
  async remove(ids: number[]): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/del", { ids });
  }

  /**
   * 加载 Ollama 模型
   */
  async load(name: string): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/load", { name });
  }

  /**
   * 重新创建 Ollama 模型
   */
  async recreate(name: string): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/recreate", { name });
  }

  /**
   * 同步 Ollama 模型列表
   */
  async sync(): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/sync", {});
  }

  /**
   * 关闭 Ollama 模型连接
   */
  async close(name: string): Promise<any> {
    return this.post("/api/v2/ai/ollama/close", { name });
  }
}
