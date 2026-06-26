import { BaseAPI } from "./base.js";

export interface MonitorDataRequest {
  /** 开始时间 */
  startTime?: string;
  /** 结束时间 */
  endTime?: string;
}

/**
 * Monitor API
 */
export class MonitorAPI extends BaseAPI {
  // ==================== Monitor Data ====================

  /** Load monitor data */
  async getData(params: MonitorDataRequest = {}): Promise<any> {
    return this.post("/api/v2/hosts/monitor/search", params);
  }

  /** Load monitor data (GPU) */
  async getGPUData(params: MonitorDataRequest = {}): Promise<any> {
    return this.post("/api/v2/hosts/monitor/gpu/search", params);
  }

  // ==================== Monitor Settings ====================

  /** Load monitor setting */
  async getSetting(): Promise<any> {
    return this.get("/api/v2/hosts/monitor/setting");
  }

  /** Update monitor setting */
  async updateSetting(params: any): Promise<any> {
    return this.post("/api/v2/hosts/monitor/setting/update", params);
  }

  // ==================== Monitor Operations ====================

  /** Clean monitor data */
  async cleanData(): Promise<any> {
    return this.post("/api/v2/hosts/monitor/clean", {});
  }
}
