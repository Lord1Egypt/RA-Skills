import { BaseAPI } from "./base.js";

export class PHPAPI extends BaseAPI {
  /**
   * 获取 PHP 运行环境列表
   */
  async list(): Promise<any> {
    return this.post("/api/v2/runtimes/php", { page: 1, pageSize: 100 });
  }

  /**
   * 获取 PHP 配置
   */
  async getConf(id: number): Promise<any> {
    return this.request(`/api/v2/runtimes/php/${id}/conf`, { method: "GET" });
  }

  /**
   * 更新 PHP 配置
   */
  async updateConf(id: number, content: string): Promise<any> {
    return this.post(`/api/v2/runtimes/php/${id}/conf`, { content });
  }

  /**
   * 获取 PHP 扩展列表
   */
  async listExtensions(id: number): Promise<any> {
    return this.request(`/api/v2/runtimes/php/${id}/extensions`, { method: "GET" });
  }

  /**
   * 安装 PHP 扩展
   */
  async installExtension(id: number, extension: string): Promise<any> {
    return this.post(`/api/v2/runtimes/php/${id}/extensions/install`, { extension });
  }

  /**
   * 卸载 PHP 扩展
   */
  async uninstallExtension(id: number, extension: string): Promise<any> {
    return this.post(`/api/v2/runtimes/php/${id}/extensions/uninstall`, { extension });
  }

  /**
   * 获取 PHP 配置文件
   */
  async getConfFile(id: number, type: string): Promise<any> {
    return this.request(`/api/v2/runtimes/php/${id}/conffile?type=${type}`, { method: "GET" });
  }

  /**
   * 更新 PHP 配置文件
   */
  async updateConfFile(id: number, type: string, content: string): Promise<any> {
    return this.post(`/api/v2/runtimes/php/${id}/conffile`, { type, content });
  }

  /**
   * 更新 PHP 版本
   */
  async updateVersion(id: number, version: string): Promise<any> {
    return this.post(`/api/v2/runtimes/php/${id}/version`, { version });
  }
}
