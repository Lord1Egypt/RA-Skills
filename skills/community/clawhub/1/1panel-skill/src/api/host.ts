import { BaseAPI } from "./base.js";

export interface HostCreateRequest {
  /** 主机名 */
  name: string;
  /** 主机地址 */
  addr: string;
  /** 端口 */
  port?: number;
  /** 用户名 */
  user?: string;
  /** 认证方式: password, key */
  authMode?: "password" | "key";
  /** 密码 */
  password?: string;
  /** 私钥 */
  privateKey?: string;
  /** 分组ID */
  groupID?: number;
  /** 描述 */
  description?: string;
}

export interface HostUpdateRequest {
  /** ID */
  id: number;
  /** 主机名 */
  name?: string;
  /** 主机地址 */
  addr?: string;
  /** 端口 */
  port?: number;
  /** 用户名 */
  user?: string;
  /** 分组ID */
  groupID?: number;
  /** 描述 */
  description?: string;
}

export interface GroupCreateRequest {
  /** 分组名 */
  name: string;
  /** 默认分组 */
  isDefault?: boolean;
}

export interface GroupUpdateRequest {
  /** ID */
  id: number;
  /** 分组名 */
  name?: string;
  /** 默认分组 */
  isDefault?: boolean;
}

/**
 * Host Management API
 */
export class HostAPI extends BaseAPI {
  // ==================== Host ====================

  /** Page host */
  async list(params?: any): Promise<any> {
    return this.post("/api/v2/core/hosts/search", params || { page: 1, pageSize: 100 });
  }

  /** Get host info */
  async getHost(id: number): Promise<any> {
    return this.post("/api/v2/core/hosts/info", { id });
  }

  /** Create host */
  async create(params: HostCreateRequest): Promise<any> {
    return this.post("/api/v2/core/hosts", params);
  }

  /** Update host */
  async update(params: HostUpdateRequest): Promise<any> {
    return this.post("/api/v2/core/hosts/update", params);
  }

  /** Delete host */
  async remove(id: number): Promise<any> {
    return this.post("/api/v2/core/hosts/del", { id });
  }

  /** Test host conn by host id */
  async testConnection(id: number): Promise<any> {
    return this.post(`/api/v2/core/hosts/test/byid/${id}`, {});
  }

  /** Test host conn by info */
  async testConnectionByInfo(params: HostCreateRequest): Promise<any> {
    return this.post("/api/v2/core/hosts/test/byinfo", params);
  }

  /** Load host tree */
  async getTree(): Promise<any> {
    return this.post("/api/v2/core/hosts/tree", {});
  }

  /** Update host group */
  async updateHostGroup(params: any): Promise<any> {
    return this.post("/api/v2/core/hosts/update/group", params);
  }

  // ==================== Group ====================

  /** List host groups */
  async listHostGroups(): Promise<any> {
    return this.request("/api/v2/hosts/groups", { method: "GET" });
  }

  /** Create host group */
  async createHostGroup(params: GroupCreateRequest): Promise<any> {
    return this.post("/api/v2/hosts/groups", params);
  }

  /** Update host group */
  async updateHostGroupByID(params: GroupUpdateRequest): Promise<any> {
    return this.post("/api/v2/hosts/groups/update", params);
  }

  /** Delete host group */
  async deleteHostGroup(id: number): Promise<any> {
    return this.post("/api/v2/hosts/groups/del", { id });
  }

  // ==================== SSH ====================

  /** Generate host SSH secret */
  async generateSSHKey(id: number): Promise<any> {
    return this.post("/api/v2/hosts/secret", { id });
  }

  /** Get host SSH secret */
  async getSSHKey(id: number): Promise<any> {
    return this.request(`/api/v2/hosts/secret/${id}`, { method: "GET" });
  }

  /** Delete host SSH secret */
  async deleteSSHKey(id: number): Promise<any> {
    return this.post("/api/v2/hosts/secret/del", { id });
  }

  /** Sync host SSH secret */
  async syncSSHKey(id: number): Promise<any> {
    return this.post("/api/v2/hosts/secret/sync", { id });
  }

  /** Update host SSH secret */
  async updateSSHKey(id: number, authMode: string, password?: string, privateKey?: string): Promise<any> {
    return this.post("/api/v2/hosts/secret/update", { id, authMode, password, privateKey });
  }

  /** Get host SSH conf */
  async getSSHConf(): Promise<any> {
    return this.request("/api/v2/hosts/ssh/conf", { method: "GET" });
  }

  /** Get host SSH logs */
  async getSSHLogs(): Promise<any> {
    return this.post("/api/v2/hosts/ssh/log", { page: 1, pageSize: 100 });
  }
}
