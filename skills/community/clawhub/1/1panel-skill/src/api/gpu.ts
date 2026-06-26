import { BaseAPI } from "./base.js";

export class GPUAPI extends BaseAPI {
  /**
   * 获取 GPU/XPU 信息
   */
  async getInfo(): Promise<any> {
    return this.request("/api/v2/ai/gpu/load", { method: "GET" });
  }

  /**
   * 获取 GPU 监控数据
   */
  async getMonitorData(params: any): Promise<any> {
    return this.post("/api/v2/hosts/monitor/gpu/search", params);
  }
}
