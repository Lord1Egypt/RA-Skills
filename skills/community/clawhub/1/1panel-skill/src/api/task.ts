import { BaseAPI } from "./base.js";

export class TaskAPI extends BaseAPI {
  /**
   * 获取执行中任务数量
   */
  async getExecutingCount(): Promise<any> {
    return this.request("/api/v2/tasks/count", { method: "GET" });
  }

  /**
   * 获取任务日志
   */
  async getLogs(): Promise<any> {
    return this.post("/api/v2/tasks/search", { page: 1, pageSize: 100 });
  }
}
