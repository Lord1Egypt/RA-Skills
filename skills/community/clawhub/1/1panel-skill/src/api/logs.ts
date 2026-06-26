import { BaseAPI } from "./base.js";

/**
 * Logs API
 */
export class LogsAPI extends BaseAPI {
  // ==================== Operation Logs ====================

  /** Page operation logs */
  async listOperation(params?: any): Promise<any> {
    return this.post("/api/v2/core/logs/operation", params || { page: 1, pageSize: 100 });
  }

  /** Clean operation logs */
  async cleanOperation(): Promise<any> {
    return this.post("/api/v2/core/logs/clean", {});
  }

  // ==================== Login Logs ====================

  /** Page login logs */
  async listLogin(params?: any): Promise<any> {
    return this.post("/api/v2/core/logs/login", params || { page: 1, pageSize: 100 });
  }

  // ==================== System Logs ====================

  /** Load system log files */
  async listSystemFiles(): Promise<any> {
    return this.get("/api/v2/logs/system/files");
  }

  // ==================== Task Logs ====================

  /** Get the number of executing tasks */
  async getExecutingTaskCount(): Promise<any> {
    return this.get("/api/v2/logs/tasks/executing/count");
  }

  /** Page task logs */
  async listTasks(params?: any): Promise<any> {
    return this.post("/api/v2/logs/tasks/search", params || { page: 1, pageSize: 100 });
  }
}
