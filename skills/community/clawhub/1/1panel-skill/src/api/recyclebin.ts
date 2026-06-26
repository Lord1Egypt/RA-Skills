import { BaseAPI } from "./base.js";

export class RecycleBinAPI extends BaseAPI {
  /**
   * 获取回收站状态
   */
  async getStatus(): Promise<any> {
    return this.request("/api/v2/files/recycle/status", { method: "GET" });
  }

  /**
   * 列出回收站文件
   */
  async list(): Promise<any> {
    return this.post("/api/v2/files/recycle/search", { page: 1, pageSize: 100 });
  }

  /**
   * 清空回收站
   */
  async clear(): Promise<any> {
    return this.post("/api/v2/files/recycle/clear", {});
  }

  /**
   * 还原回收站文件
   */
  async reduce(name: string): Promise<any> {
    return this.post("/api/v2/files/recycle/reduce", { name });
  }
}
