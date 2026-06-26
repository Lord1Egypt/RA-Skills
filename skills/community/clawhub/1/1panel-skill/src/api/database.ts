import { BaseAPI } from "./base.js";

/**
 * Database Management API
 * Supports MySQL, PostgreSQL, Redis
 */
export class DatabaseAPI extends BaseAPI {
  // ==================== MySQL ====================

  /** Create MySQL database */
  async createMysql(params: any): Promise<any> {
    return this.post("/api/v2/databases", params);
  }

  /** Delete MySQL database */
  async deleteMysql(params: any): Promise<any> {
    return this.post("/api/v2/databases/del", params);
  }

  /** Check before delete MySQL database */
  async checkDeleteMysql(params: any): Promise<any> {
    return this.post("/api/v2/databases/del/check", params);
  }

  /** Search MySQL databases with pagination */
  async searchMysql(params: any): Promise<any> {
    return this.post("/api/v2/databases/search", params);
  }

  /** Bind user to MySQL database */
  async bindMysqlUser(params: any): Promise<any> {
    return this.post("/api/v2/databases/bind", params);
  }

  /** Change MySQL access */
  async changeMysqlAccess(params: any): Promise<any> {
    return this.post("/api/v2/databases/change/access", params);
  }

  /** Change MySQL password */
  async changeMysqlPassword(params: any): Promise<any> {
    return this.post("/api/v2/databases/change/password", params);
  }

  /** Update MySQL database description */
  async updateMysqlDescription(params: any): Promise<any> {
    return this.post("/api/v2/databases/description/update", params);
  }

  /** Load MySQL database from remote */
  async loadMysqlFromRemote(params: any): Promise<any> {
    return this.post("/api/v2/databases/load", params);
  }

  /** List MySQL database format collation options */
  async listMysqlFormatOptions(): Promise<any> {
    return this.post("/api/v2/databases/format/options", {});
  }

  /** Load MySQL remote access */
  async loadMysqlRemoteAccess(params: any): Promise<any> {
    return this.post("/api/v2/databases/remote", params);
  }

  /** Load MySQL status info */
  async getMysqlStatus(): Promise<any> {
    return this.post("/api/v2/databases/status", {});
  }

  /** Load MySQL variables info */
  async getMysqlVariables(): Promise<any> {
    return this.post("/api/v2/databases/variables", {});
  }

  /** Update MySQL variables */
  async updateMysqlVariables(params: any): Promise<any> {
    return this.post("/api/v2/databases/variables/update", params);
  }

  // ==================== Generic Database ====================

  /** Create database */
  async create(params: any): Promise<any> {
    return this.post("/api/v2/databases/db", params);
  }

  /** Get databases by name */
  async getByName(name: string): Promise<any> {
    return this.request(`/api/v2/databases/db/${name}`, { method: "GET" });
  }

  /** Check database */
  async check(params: any): Promise<any> {
    return this.post("/api/v2/databases/db/check", params);
  }

  /** Delete database */
  async remove(params: any): Promise<any> {
    return this.post("/api/v2/databases/db/del", params);
  }

  /** Check before delete remote database */
  async checkDeleteRemote(params: any): Promise<any> {
    return this.post("/api/v2/databases/db/del/check", params);
  }

  /** List databases by type */
  async listByType(type: string): Promise<any> {
    return this.request(`/api/v2/databases/db/item/${type}`, { method: "GET" });
  }

  /** List databases */
  async listAll(type: string): Promise<any> {
    return this.request(`/api/v2/databases/db/list/${type}`, { method: "GET" });
  }

  /** Search databases with pagination */
  async search(params: any): Promise<any> {
    return this.post("/api/v2/databases/db/search", params);
  }

  /** Update database */
  async update(params: any): Promise<any> {
    return this.post("/api/v2/databases/db/update", params);
  }

  // ==================== Common Database ====================

  /** Load base info */
  async getCommonInfo(): Promise<any> {
    return this.post("/api/v2/databases/common/info", {});
  }

  /** Load Database conf */
  async loadConfigFile(): Promise<any> {
    return this.post("/api/v2/databases/common/load/file", {});
  }

  /** Update conf by upload file */
  async updateConfigByFile(params: any): Promise<any> {
    return this.post("/api/v2/databases/common/update/conf", params);
  }

  // ==================== PostgreSQL ====================

  /** Create PostgreSQL database */
  async createPostgresql(params: any): Promise<any> {
    return this.post("/api/v2/databases/pg", params);
  }

  /** Load PostgreSQL database from remote */
  async loadPostgresqlFromRemote(database: string, params: any): Promise<any> {
    return this.post(`/api/v2/databases/pg/${database}/load`, params);
  }

  /** Bind PostgreSQL user */
  async bindPostgresqlUser(params: any): Promise<any> {
    return this.post("/api/v2/databases/pg/bind", params);
  }

  /** Delete PostgreSQL database */
  async deletePostgresql(params: any): Promise<any> {
    return this.post("/api/v2/databases/pg/del", params);
  }

  /** Check before delete PostgreSQL database */
  async checkDeletePostgresql(params: any): Promise<any> {
    return this.post("/api/v2/databases/pg/del/check", params);
  }

  /** Update PostgreSQL database description */
  async updatePostgresqlDescription(params: any): Promise<any> {
    return this.post("/api/v2/databases/pg/description", params);
  }

  /** Change PostgreSQL password */
  async changePostgresqlPassword(params: any): Promise<any> {
    return this.post("/api/v2/databases/pg/password", params);
  }

  /** Change PostgreSQL privileges */
  async changePostgresqlPrivileges(params: any): Promise<any> {
    return this.post("/api/v2/databases/pg/privileges", params);
  }

  /** Search PostgreSQL databases with pagination */
  async searchPostgresql(params: any): Promise<any> {
    return this.post("/api/v2/databases/pg/search", params);
  }

  // ==================== Redis ====================

  /** Load Redis conf */
  async getRedisConf(params: any): Promise<any> {
    return this.post("/api/v2/databases/redis/conf", params);
  }

  /** Update Redis conf */
  async updateRedisConf(params: any): Promise<any> {
    return this.post("/api/v2/databases/redis/conf/update", params);
  }

  /** Install redis-cli */
  async installRedisCli(): Promise<any> {
    return this.post("/api/v2/databases/redis/install/cli", {});
  }

  /** Change Redis password */
  async changeRedisPassword(params: any): Promise<any> {
    return this.post("/api/v2/databases/redis/password", params);
  }

  /** Load Redis persistence conf */
  async getRedisPersistenceConf(): Promise<any> {
    return this.post("/api/v2/databases/redis/persistence/conf", {});
  }

  /** Update Redis persistence conf */
  async updateRedisPersistenceConf(params: any): Promise<any> {
    return this.post("/api/v2/databases/redis/persistence/update", params);
  }

  /** Load Redis status info */
  async getRedisStatus(): Promise<any> {
    return this.post("/api/v2/databases/redis/status", {});
  }
}
