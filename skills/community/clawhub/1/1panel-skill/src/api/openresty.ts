import { BaseAPI } from "./base.js";

export class OpenRestyAPI extends BaseAPI {
  /**
   * 获取 OpenResty 配置
   */
  async getConf(): Promise<any> {
    return this.request("/api/v2/openresty/conf", { method: "GET" });
  }

  /**
   * 构建 OpenResty
   */
  async build(params: any): Promise<any> {
    return this.post("/api/v2/openresty/build", params);
  }

  /**
   * 通过文件更新 OpenResty 配置
   */
  async updateByFile(content: string): Promise<any> {
    return this.post("/api/v2/openresty/file", { content });
  }

  /**
   * 获取 OpenResty 模块
   */
  async getModules(): Promise<any> {
    return this.request("/api/v2/openresty/modules", { method: "GET" });
  }

  /**
   * 更新 OpenResty 模块
   */
  async updateModule(params: any): Promise<any> {
    return this.post("/api/v2/openresty/modules", params);
  }

  /**
   * 获取部分 OpenResty 配置
   */
  async getPartialConf(): Promise<any> {
    return this.request("/api/v2/openresty/partial", { method: "GET" });
  }

  /**
   * 获取 OpenResty 状态
   */
  async getStatus(): Promise<any> {
    return this.request("/api/v2/openresty/status", { method: "GET" });
  }

  /**
   * 更新 OpenResty 配置
   */
  async updateConf(params: any): Promise<any> {
    return this.post("/api/v2/openresty/update", params);
  }
}
