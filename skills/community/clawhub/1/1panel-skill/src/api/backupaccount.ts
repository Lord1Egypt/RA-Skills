import { BaseAPI } from "./base.js";

/**
 * Backup Account API
 */
export class BackupAccountAPI extends BaseAPI {
  // ==================== Account Management ====================

  /** Search backup accounts with page */
  async list(params?: any): Promise<any> {
    return this.post("/api/v2/backups/search", params || { page: 1, pageSize: 100 });
  }

  /** Create backup account */
  async create(params: any): Promise<any> {
    return this.post("/api/v2/backups", params);
  }

  /** Create backup account (core) */
  async createCore(params: any): Promise<any> {
    return this.post("/api/v2/core/backups", params);
  }

  /** Update backup account */
  async update(params: any): Promise<any> {
    return this.post("/api/v2/backups/update", params);
  }

  /** Update backup account (core) */
  async updateCore(params: any): Promise<any> {
    return this.post("/api/v2/core/backups/update", params);
  }

  /** Delete backup account */
  async remove(type: string): Promise<any> {
    return this.post("/api/v2/backups/del", { type });
  }

  /** Delete backup account (core) */
  async removeCore(type: string): Promise<any> {
    return this.post("/api/v2/core/backups/del", { type });
  }

  /** Check backup account */
  async check(params: any): Promise<any> {
    return this.post("/api/v2/backups/check", params);
  }

  /** Load backup account base info */
  async getClientInfo(clientType: string): Promise<any> {
    return this.get(`/api/v2/core/backups/client/${clientType}`);
  }

  /** Load backup account options */
  async getOptions(): Promise<any> {
    return this.get("/api/v2/backups/options");
  }

  /** get local backup dir */
  async getLocalDir(): Promise<any> {
    return this.get("/api/v2/backups/local");
  }

  /** Refresh token */
  async refreshToken(params: any): Promise<any> {
    return this.post("/api/v2/backups/refresh/token", params);
  }

  /** Refresh token (core) */
  async refreshTokenCore(params: any): Promise<any> {
    return this.post("/api/v2/core/backups/refresh/token", params);
  }

  /** List buckets */
  async listBuckets(params: any): Promise<any> {
    return this.post("/api/v2/backups/buckets", params);
  }

  /** List files from backup accounts */
  async listFiles(params: any): Promise<any> {
    return this.post("/api/v2/backups/search/files", params);
  }

  // ==================== Backup Operations ====================

  /** Backup system data */
  async backup(params: any): Promise<any> {
    return this.post("/api/v2/backups/backup", params);
  }

  /** Recover system data */
  async recover(params: any): Promise<any> {
    return this.post("/api/v2/backups/recover", params);
  }

  /** Recover system data by upload */
  async recoverByUpload(params: any): Promise<any> {
    return this.post("/api/v2/backups/recover/byupload", params);
  }

  /** Upload file for recover */
  async uploadForRecover(params: any): Promise<any> {
    return this.post("/api/v2/backups/upload", params);
  }

  // ==================== Backup Records ====================

  /** Page backup records */
  async listRecords(params?: any): Promise<any> {
    return this.post("/api/v2/backups/record/search", params || { page: 1, pageSize: 100 });
  }

  /** Page backup records by cronjob */
  async listRecordsByCronjob(params: any): Promise<any> {
    return this.post("/api/v2/backups/record/search/bycronjob", params);
  }

  /** Delete backup record */
  async deleteRecord(params: any): Promise<any> {
    return this.post("/api/v2/backups/record/del", params);
  }

  /** Update backup record description */
  async updateRecordDescription(params: any): Promise<any> {
    return this.post("/api/v2/backups/record/description/update", params);
  }

  /** Download backup record */
  async downloadRecord(params: any): Promise<any> {
    return this.post("/api/v2/backups/record/download", params);
  }

  /** Load backup record size */
  async getRecordSize(params: any): Promise<any> {
    return this.post("/api/v2/backups/record/size", params);
  }
}
