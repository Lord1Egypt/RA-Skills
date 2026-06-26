import { BaseAPI } from "./base.js";

/**
 * Dashboard API
 */
export class DashboardAPI extends BaseAPI {
  // ==================== Dashboard Info ====================

  /** Load dashboard base info */
  async getBaseInfo(ioOption?: string, netOption?: string): Promise<any> {
    if (ioOption && netOption) {
      return this.get(`/api/v2/dashboard/base/${ioOption}/${netOption}`);
    }
    return this.get("/api/v2/dashboard/base");
  }

  /** Load os info */
  async getOSInfo(): Promise<any> {
    return this.get("/api/v2/dashboard/base/os");
  }

  /** Load dashboard current info */
  async getCurrentInfo(ioOption?: string, netOption?: string): Promise<any> {
    if (ioOption && netOption) {
      return this.get(`/api/v2/dashboard/current/${ioOption}/${netOption}`);
    }
    return this.get("/api/v2/dashboard/current");
  }

  /** Load dashboard current info for node */
  async getCurrentInfoForNode(): Promise<any> {
    return this.get("/api/v2/dashboard/current/node");
  }

  /** Load top cpu processes */
  async getTopCPU(): Promise<any> {
    return this.get("/api/v2/dashboard/current/top/cpu");
  }

  /** Load top memory processes */
  async getTopMemory(): Promise<any> {
    return this.get("/api/v2/dashboard/current/top/mem");
  }

  // ==================== App Launcher ====================

  /** Load app launcher */
  async getAppLauncher(): Promise<any> {
    return this.get("/api/v2/dashboard/app/launcher");
  }

  /** Load app launcher options */
  async getAppLauncherOptions(): Promise<any> {
    return this.post("/api/v2/dashboard/app/launcher/option", {});
  }

  /** Update app Launcher */
  async updateAppLauncher(params: any): Promise<any> {
    return this.post("/api/v2/dashboard/app/launcher/show", params);
  }

  // ==================== Quick Jump ====================

  /** Load quick jump options */
  async getQuickJumpOptions(): Promise<any> {
    return this.get("/api/v2/dashboard/quick/option");
  }

  /** Update quick jump */
  async updateQuickJump(params: any): Promise<any> {
    return this.post("/api/v2/dashboard/quick/change", params);
  }

  // ==================== System ====================

  /** System restart */
  async systemRestart(operation: string): Promise<any> {
    return this.post(`/api/v2/dashboard/system/restart/${operation}`, {});
  }

  // ==================== Memo ====================

  /** Load dashboard memo */
  async getMemo(): Promise<any> {
    return this.get("/api/v2/dashboard/memo");
  }

  /** Update dashboard memo */
  async updateMemo(content: string): Promise<any> {
    return this.post("/api/v2/dashboard/memo", { content });
  }
}
