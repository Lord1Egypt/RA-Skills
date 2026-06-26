import { BaseAPI } from "./base.js";

/**
 * ClamAV Antivirus API
 */
export class ClamAPI extends BaseAPI {
  // ==================== Clam Info ====================

  /** Load clam base info */
  async getBaseInfo(): Promise<any> {
    return this.post("/api/v2/toolbox/clam/base", {});
  }

  /** Page clam */
  async list(params?: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/search", params || { page: 1, pageSize: 100 });
  }

  // ==================== Clam Operations ====================

  /** Create clam */
  async create(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam", params);
  }

  /** Update clam */
  async update(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/update", params);
  }

  /** Delete clam */
  async remove(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/del", params);
  }

  /** Operate Clam */
  async operate(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/operate", params);
  }

  /** Update clam status */
  async updateStatus(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/status/update", params);
  }

  // ==================== Clam Scan ====================

  /** Handle clam scan */
  async handleScan(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/handle", params);
  }

  // ==================== Clam File ====================

  /** Load clam file */
  async getFile(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/file/search", params);
  }

  /** Update clam file */
  async updateFile(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/file/update", params);
  }

  // ==================== Clam Records ====================

  /** Page clam record */
  async listRecords(params?: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/record/search", params || { page: 1, pageSize: 100 });
  }

  /** Clean clam record */
  async cleanRecords(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/clam/record/clean", params);
  }
}
