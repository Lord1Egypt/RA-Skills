import { BaseAPI } from "./base.js";

/**
 * App Store API
 */
export class AppAPI extends BaseAPI {
  // ==================== App Store ====================

  /** List apps */
  async list(params?: any): Promise<any> {
    return this.post("/api/v2/apps/search", params || { page: 1, pageSize: 100 });
  }

  /** Search app by key */
  async getByKey(key: string): Promise<any> {
    return this.get(`/api/v2/apps/${key}`);
  }

  /** Get app list update */
  async checkUpdate(): Promise<any> {
    return this.get("/api/v2/apps/checkupdate");
  }

  /** Get app detail by id */
  async getDetail(id: string | number): Promise<any> {
    return this.get(`/api/v2/apps/details/${id}`);
  }

  /** Search app detail by appid */
  async getDetailByAppId(appId: string, version: string, type: string): Promise<any> {
    return this.get(`/api/v2/apps/detail/${appId}/${version}/${type}`);
  }

  /** Search app detail by appkey and version */
  async getDetailByAppKey(appKey: string, version: string): Promise<any> {
    return this.get(`/api/v2/apps/detail/node/${appKey}/${version}`);
  }

  /** Get app icon by app_id */
  async getIcon(key: string): Promise<any> {
    return this.get(`/api/v2/apps/icon/${key}`);
  }

  /** Search app service by key */
  async getServices(key: string): Promise<any> {
    return this.get(`/api/v2/apps/services/${key}`);
  }

  /** Sync local app list */
  async syncLocal(): Promise<any> {
    return this.post("/api/v2/apps/sync/local", {});
  }

  /** Sync remote app list */
  async syncRemote(): Promise<any> {
    return this.post("/api/v2/apps/sync/remote", {});
  }

  // ==================== Install ====================

  /** Install app */
  async install(params: any): Promise<any> {
    return this.post("/api/v2/apps/install", params);
  }

  // ==================== Ignored Apps ====================

  /** List Upgrade Ignored App */
  async listIgnored(): Promise<any> {
    return this.get("/api/v2/apps/ignored/detail");
  }

  /** Cancel Ignore Upgrade App */
  async cancelIgnored(params: any): Promise<any> {
    return this.post("/api/v2/apps/ignored/cancel", params);
  }

  // ==================== Installed Apps ====================

  /** List installed apps */
  async listInstalled(params?: any): Promise<any> {
    return this.post("/api/v2/apps/installed/list", params || {});
  }

  /** Get installed app info */
  async getInstalledInfo(appInstallId: string | number): Promise<any> {
    return this.get(`/api/v2/apps/installed/info/${appInstallId}`);
  }

  /** Check installed app */
  async checkInstalled(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/check", params);
  }

  /** Check before delete installed app */
  async checkDeleteInstalled(appInstallId: string | number): Promise<any> {
    return this.get(`/api/v2/apps/installed/delete/check/${appInstallId}`);
  }

  /** Ignore installed app upgrade */
  async ignoreUpgrade(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/ignore", params);
  }

  /** Load installed app config */
  async loadConfig(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/conf", params);
  }

  /** Update installed app config */
  async updateConfig(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/config/update", params);
  }

  /** Load installed app connection info */
  async loadConnInfo(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/conninfo", params);
  }

  /** Load installed app port */
  async loadPort(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/loadport", params);
  }

  /** Search installed apps with pagination */
  async searchInstalled(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/search", params);
  }

  /** Sync installed apps */
  async syncInstalled(): Promise<any> {
    return this.post("/api/v2/apps/installed/sync", {});
  }

  /** Get installed app params */
  async getInstalledParams(appInstallId: string | number): Promise<any> {
    return this.get(`/api/v2/apps/installed/params/${appInstallId}`);
  }

  /** Update installed app params */
  async updateInstalledParams(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/params/update", params);
  }

  /** Update installed app port */
  async updateInstalledPort(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/port/change", params);
  }

  /** Operate installed app */
  async operateInstalled(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/op", params);
  }

  /** Update installed app */
  async updateInstalled(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/update", params);
  }

  /** Search installed app update version */
  async searchUpdateVersion(params: any): Promise<any> {
    return this.post("/api/v2/apps/installed/update/versions", params);
  }
}
