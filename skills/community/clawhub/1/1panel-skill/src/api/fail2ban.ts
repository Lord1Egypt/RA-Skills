import { BaseAPI } from "./base.js";

export interface Fail2BanOperateRequest {
  /** 操作: start, stop, restart */
  operation: "start" | "stop" | "restart";
}

export interface Fail2BanSSHOperateRequest {
  /** 操作: start, stop, restart */
  operation: "start" | "stop" | "restart";
}

export interface Fail2BanUpdateRequest {
  /** 配置键 */
  key: string;
  /** 配置值 */
  value: string;
}

export interface Fail2BanSearchRequest {
  /** 页码 */
  page?: number;
  /** 每页数量 */
  pageSize?: number;
}

export class Fail2BanAPI extends BaseAPI {
  /**
   * 获取 Fail2ban 基础信息
   */
  async getBaseInfo(): Promise<any> {
    return this.request("/api/v2/toolbox/fail2ban/base", { method: "GET" });
  }

  /**
   * 获取 Fail2ban 配置
   */
  async getConf(): Promise<any> {
    return this.request("/api/v2/toolbox/fail2ban/load/conf", { method: "GET" });
  }

  /**
   * 操作 Fail2ban (启动/停止/重启)
   */
  async operate(params: Fail2BanOperateRequest): Promise<any> {
    return this.post("/api/v2/toolbox/fail2ban/operate", params);
  }

  /**
   * 操作 Fail2ban SSH (启动/停止/重启)
   */
  async operateSSH(params: Fail2BanSSHOperateRequest): Promise<any> {
    return this.post("/api/v2/toolbox/fail2ban/operate/sshd", params);
  }

  /**
   * 搜索被封禁的 IP 列表
   */
  async searchBannedIPs(params: Fail2BanSearchRequest = {}): Promise<any> {
    return this.post("/api/v2/toolbox/fail2ban/search", {
      page: 1,
      pageSize: 100,
      ...params,
    });
  }

  /**
   * 更新 Fail2ban 配置
   */
  async updateConf(params: Fail2BanUpdateRequest): Promise<any> {
    return this.post("/api/v2/toolbox/fail2ban/update", params);
  }

  /**
   * 通过文件更新 Fail2ban 配置
   */
  async updateConfByFile(content: string): Promise<any> {
    return this.post("/api/v2/toolbox/fail2ban/update/byconf", { content });
  }
}
