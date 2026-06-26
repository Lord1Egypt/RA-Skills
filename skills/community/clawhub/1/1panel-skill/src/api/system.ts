import { BaseAPI } from "./base.js";

export class SystemAPI extends BaseAPI {
  async getInfo(): Promise<any> {
    return this.post("/api/v2/toolbox/device/base", {});
  }

  async getMonitor(): Promise<any> {
    return this.post("/api/v2/toolbox/device/monitor", {});
  }
}
