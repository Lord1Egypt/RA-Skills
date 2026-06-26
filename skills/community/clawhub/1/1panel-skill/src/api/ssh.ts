import { BaseAPI } from "./base.js";

/**
 * SSH Management API
 */
export class SSHAPI extends BaseAPI {
  // ==================== SSH Info ====================

  /** Load host SSH setting info */
  async getInfo(): Promise<any> {
    return this.post("/api/v2/hosts/ssh/search", {});
  }

  /** Load host SSH conf */
  async getConfig(): Promise<any> {
    return this.post("/api/v2/hosts/ssh/file", {});
  }

  // ==================== SSH Operations ====================

  /** Operate SSH */
  async operate(params: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/operate", params);
  }

  /** Update host SSH setting */
  async updateConfig(params: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/update", params);
  }

  /** Update host SSH setting by file */
  async updateConfigByFile(params: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/file/update", params);
  }

  // ==================== SSH Logs ====================

  /** Load host SSH logs */
  async getLogs(): Promise<any> {
    return this.post("/api/v2/hosts/ssh/log", {});
  }

  /** Export host SSH logs */
  async exportLogs(params?: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/log/export", params || {});
  }

  // ==================== SSH Certificate ====================

  /** Generate host SSH secret */
  async generateCert(params: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/cert", params);
  }

  /** Load host SSH secret */
  async getCert(params: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/cert/search", params);
  }

  /** Update host SSH secret */
  async updateCert(params: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/cert/update", params);
  }

  /** Delete host SSH secret */
  async deleteCert(params: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/cert/delete", params);
  }

  /** Sync host SSH secret */
  async syncCert(params: any): Promise<any> {
    return this.post("/api/v2/hosts/ssh/cert/sync", params);
  }

  // ==================== Local Connection ====================

  /** Load local conn */
  async getLocalConn(): Promise<any> {
    return this.get("/api/v2/settings/ssh/conn");
  }

  /** Save local conn info */
  async saveLocalConn(params: any): Promise<any> {
    return this.post("/api/v2/settings/ssh", params);
  }

  /** Check local conn info */
  async checkLocalConn(params: any): Promise<any> {
    return this.post("/api/v2/settings/ssh/check/info", params);
  }

  /** Update local is conn */
  async updateLocalConnDefault(params: any): Promise<any> {
    return this.post("/api/v2/settings/ssh/conn/default", params);
  }
}
