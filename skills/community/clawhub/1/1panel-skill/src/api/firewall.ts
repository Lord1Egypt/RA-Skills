import { BaseAPI } from "./base.js";

/**
 * Firewall API
 */
export class FirewallAPI extends BaseAPI {
  // ==================== Firewall Management ====================

  /** Load firewall base info */
  async getBaseInfo(): Promise<any> {
    return this.post("/api/v2/hosts/firewall/base", {});
  }

  /** Operate firewall */
  async operate(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/operate", params);
  }

  // ==================== Firewall Rules ====================

  /** Page firewall rules */
  async listRules(params?: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/search", params || { page: 1, pageSize: 100 });
  }

  /** Create group */
  async createGroup(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/port", params);
  }

  /** Batch operate rule */
  async batchOperate(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/batch", params);
  }

  /** Update port rule */
  async updatePortRule(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/update/port", params);
  }

  /** Update Ip rule */
  async updateAddrRule(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/update/addr", params);
  }

  /** Update rule description */
  async updateDescription(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/update/description", params);
  }

  // ==================== IP Rules ====================

  /** Operate Ip rule */
  async operateIpRule(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/ip", params);
  }

  // ==================== Forward Rules ====================

  /** Operate forward rule */
  async operateForwardRule(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/forward", params);
  }

  // ==================== IPTables Filter ====================

  /** Apply/Unload/Init iptables filter */
  async operateFilter(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/filter/operate", params);
  }

  /** search iptables filter rules */
  async searchFilterRules(params?: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/filter/search", params || {});
  }

  /** Operate iptables filter rule */
  async operateFilterRule(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/filter/rule/operate", params);
  }

  /** Batch operate iptables filter rules */
  async batchOperateFilterRules(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/filter/rule/batch", params);
  }

  /** load chain status with name */
  async getChainStatus(params: any): Promise<any> {
    return this.post("/api/v2/hosts/firewall/filter/chain/status", params);
  }
}
