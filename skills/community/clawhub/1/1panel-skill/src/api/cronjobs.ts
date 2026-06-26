import { BaseAPI } from "./base.js";

/**
 * Cronjob API
 */
export class CronjobAPI extends BaseAPI {
  // ==================== Cronjob Management ====================

  /** Page cronjobs */
  async list(params?: any): Promise<any> {
    return this.post("/api/v2/cronjobs/search", params || { page: 1, pageSize: 100 });
  }

  /** Create cronjob */
  async create(job: any): Promise<any> {
    return this.post("/api/v2/cronjobs", job);
  }

  /** Update cronjob */
  async update(job: any): Promise<any> {
    return this.post("/api/v2/cronjobs/update", job);
  }

  /** Delete cronjob */
  async remove(id: number): Promise<any> {
    return this.post("/api/v2/cronjobs/del", { id });
  }

  /** Update cronjob status */
  async updateStatus(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/status", params);
  }

  /** Handle cronjob once */
  async handle(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/handle", params);
  }

  /** Handle stop job */
  async stop(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/stop", params);
  }

  /** Load cronjob info */
  async loadInfo(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/load/info", params);
  }

  /** Load cronjob spec time */
  async getNextTime(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/next", params);
  }

  // ==================== Cronjob Group ====================

  /** Update cronjob group */
  async updateGroup(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/group/update", params);
  }

  // ==================== Import/Export ====================

  /** Export cronjob list */
  async export(params?: any): Promise<any> {
    return this.post("/api/v2/cronjobs/export", params || {});
  }

  /** Import cronjob list */
  async import(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/import", params);
  }

  // ==================== Script Options ====================

  /** Load script options */
  async getScriptOptions(): Promise<any> {
    return this.get("/api/v2/cronjobs/script/options");
  }

  // ==================== Job Records ====================

  /** Page job records */
  async listRecords(params?: any): Promise<any> {
    return this.post("/api/v2/cronjobs/search/records", params || { page: 1, pageSize: 100 });
  }

  /** Clean job records */
  async cleanRecords(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/records/clean", params);
  }

  /** Load Cronjob record log */
  async getRecordLog(params: any): Promise<any> {
    return this.post("/api/v2/cronjobs/records/log", params);
  }
}
