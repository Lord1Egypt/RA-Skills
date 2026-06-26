import { BaseAPI } from "./base.js";

export class NodeAPI extends BaseAPI {
  /**
   * 获取 Node 模块
   */
  async getModules(id: number): Promise<any> {
    return this.request(`/api/v2/runtimes/node/${id}/modules`, { method: "GET" });
  }

  /**
   * 操作 Node 模块
   */
  async operateModule(id: number, params: any): Promise<any> {
    return this.post(`/api/v2/runtimes/node/${id}/modules/operate`, params);
  }

  /**
   * 获取 Node 包脚本
   */
  async getPackageScripts(id: number, params: any): Promise<any> {
    return this.post(`/api/v2/runtimes/node/${id}/package`, params);
  }
}
