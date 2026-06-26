import { BaseAPI } from "./base.js";

export interface FTPCreateRequest {
  /** 用户名 */
  userName: string;
  /** 密码 */
  password: string;
  /** 根目录 */
  path: string;
  /** 描述 */
  description?: string;
}

export interface FTPUpdateRequest {
  /** 用户ID */
  id: number;
  /** 密码 (可选) */
  password?: string;
  /** 根目录 */
  path?: string;
  /** 描述 */
  description?: string;
}

export interface FTPDeleteRequest {
  /** 用户ID */
  id: number;
}

export class FTPAPI extends BaseAPI {
  /**
   * 列出 FTP 用户
   */
  async list(): Promise<any> {
    return this.post("/api/v2/toolbox/ftp/search", { page: 1, pageSize: 100 });
  }

  /**
   * 获取 FTP 基础信息
   */
  async getBaseInfo(): Promise<any> {
    return this.request("/api/v2/toolbox/ftp/base", { method: "GET" });
  }

  /**
   * 创建 FTP 用户
   */
  async create(params: FTPCreateRequest): Promise<any> {
    return this.post("/api/v2/toolbox/ftp", params);
  }

  /**
   * 更新 FTP 用户
   */
  async update(params: FTPUpdateRequest): Promise<any> {
    return this.post("/api/v2/toolbox/ftp/update", params);
  }

  /**
   * 删除 FTP 用户
   */
  async remove(id: number): Promise<any> {
    return this.post("/api/v2/toolbox/ftp/del", { id });
  }

  /**
   * 操作 FTP (启动/停止/重启)
   */
  async operate(operation: "start" | "stop" | "restart"): Promise<any> {
    return this.post("/api/v2/toolbox/ftp/operate", { operation });
  }

  /**
   * 同步 FTP 用户
   */
  async sync(): Promise<any> {
    return this.post("/api/v2/toolbox/ftp/sync", {});
  }

  /**
   * 获取 FTP 操作日志
   */
  async getLogs(): Promise<any> {
    return this.request("/api/v2/toolbox/ftp/log", { method: "GET" });
  }

  /**
   * 加载 FTP 操作日志
   */
  async searchLogs(params?: any): Promise<any> {
    return this.post("/api/v2/toolbox/ftp/log/search", params || { page: 1, pageSize: 100 });
  }
}
