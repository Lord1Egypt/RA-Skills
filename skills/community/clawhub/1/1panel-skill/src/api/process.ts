import { BaseAPI } from "./base.js";

/**
 * Process Management API
 */
export class ProcessAPI extends BaseAPI {
  // ==================== Process List ====================

  /** Get process list */
  async list(): Promise<any> {
    return this.post("/api/v2/process", {});
  }

  /** Get Process Info By PID */
  async getByPid(pid: number): Promise<any> {
    return this.get(`/api/v2/process/${pid}`);
  }

  /** Get Listening Process */
  async getListening(): Promise<any> {
    return this.post("/api/v2/process/listening", {});
  }

  // ==================== Process Operations ====================

  /** Kill process */
  async kill(pid: number): Promise<any> {
    return this.post("/api/v2/process/kill", { pid });
  }

  /** Stop Process */
  async stop(params: any): Promise<any> {
    return this.post("/api/v2/process/stop", params);
  }

  // ==================== Supervisor ====================

  /** Get Supervisor process config */
  async getSupervisorConfig(): Promise<any> {
    return this.get("/api/v2/hosts/tool/supervisor/process");
  }

  /** Create Supervisor process */
  async createSupervisorProcess(params: any): Promise<any> {
    return this.post("/api/v2/hosts/tool/supervisor/process", params);
  }

  /** Get Supervisor process config file */
  async getSupervisorConfigFile(params: any): Promise<any> {
    return this.post("/api/v2/hosts/tool/supervisor/process/file", params);
  }
}
