import { BaseAPI } from "./base.js";

/**
 * Device Management API
 */
export class DeviceAPI extends BaseAPI {
  // ==================== Device Info ====================

  /** Load device base info */
  async getBaseInfo(): Promise<any> {
    return this.post("/api/v2/toolbox/device/base", {});
  }

  /** load conf */
  async getConf(): Promise<any> {
    return this.post("/api/v2/toolbox/device/conf", {});
  }

  /** Load user list */
  async getUsers(): Promise<any> {
    return this.get("/api/v2/toolbox/device/users");
  }

  /** list time zone options */
  async getZoneOptions(): Promise<any> {
    return this.get("/api/v2/toolbox/device/zone/options");
  }

  // ==================== Device Operations ====================

  /** Update device */
  async update(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/device/update/conf", params);
  }

  /** Update device conf by file */
  async updateByFile(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/device/update/byconf", params);
  }

  /** Update device hosts */
  async updateHosts(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/device/update/host", params);
  }

  /** Update device passwd */
  async updatePassword(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/device/update/passwd", params);
  }

  /** Update device swap */
  async updateSwap(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/device/update/swap", params);
  }

  /** Check device DNS conf */
  async checkDNS(params: any): Promise<any> {
    return this.post("/api/v2/toolbox/device/check/dns", params);
  }
}
