import { BaseAPI } from "./base.js";

/**
 * Runtime Environment API
 */
export class RuntimeAPI extends BaseAPI {
  // ==================== Runtime Management ====================

  /** List runtimes */
  async list(params?: any): Promise<any> {
    return this.post("/api/v2/runtimes/search", params || { page: 1, pageSize: 100 });
  }

  /** Get runtime */
  async getById(id: number): Promise<any> {
    return this.get(`/api/v2/runtimes/${id}`);
  }

  /** Create runtime */
  async create(params: any): Promise<any> {
    return this.post("/api/v2/runtimes", params);
  }

  /** Update runtime */
  async update(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/update", params);
  }

  /** Delete runtime */
  async remove(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/del", params);
  }

  /** Delete runtime check */
  async checkDelete(id: number): Promise<any> {
    return this.get(`/api/v2/runtimes/installed/delete/check/${id}`);
  }

  /** Operate runtime */
  async operate(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/operate", params);
  }

  /** Sync runtime status */
  async sync(): Promise<any> {
    return this.post("/api/v2/runtimes/sync", {});
  }

  /** Update runtime remark */
  async updateRemark(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/remark", params);
  }

  // ==================== PHP Runtime ====================

  /** Get php runtime extension */
  async getPHPExtensions(id: number): Promise<any> {
    return this.get(`/api/v2/runtimes/php/${id}/extensions`);
  }

  /** Load php runtime conf */
  async getPHPConfig(id: number): Promise<any> {
    return this.get(`/api/v2/runtimes/php/config/${id}`);
  }

  /** Update runtime php conf */
  async updatePHPConfig(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/config", params);
  }

  /** Get PHP container config */
  async getPHPContainerConfig(id: number): Promise<any> {
    return this.get(`/api/v2/runtimes/php/container/${id}`);
  }

  /** Update PHP container config */
  async updatePHPContainerConfig(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/container/update", params);
  }

  /** Get php conf file */
  async getPHPConfFile(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/file", params);
  }

  /** Update php conf file */
  async updatePHPConfFile(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/update", params);
  }

  /** Get fpm config */
  async getFPMConfig(id: number): Promise<any> {
    return this.get(`/api/v2/runtimes/php/fpm/config/${id}`);
  }

  /** Update fpm config */
  async updateFPMConfig(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/fpm/config", params);
  }

  /** Get PHP runtime status */
  async getPHPStatus(id: number): Promise<any> {
    return this.get(`/api/v2/runtimes/php/fpm/status/${id}`);
  }

  // ==================== PHP Extensions ====================

  /** Page Extensions */
  async listExtensions(params?: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/extensions/search", params || { page: 1, pageSize: 100 });
  }

  /** Create Extensions */
  async createExtension(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/extensions", params);
  }

  /** Update Extensions */
  async updateExtension(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/extensions/update", params);
  }

  /** Delete Extensions */
  async deleteExtension(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/extensions/del", params);
  }

  /** Install php extension */
  async installExtension(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/extensions/install", params);
  }

  /** UnInstall php extension */
  async uninstallExtension(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/php/extensions/uninstall", params);
  }

  // ==================== Node Runtime ====================

  /** Get Node modules */
  async getNodeModules(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/node/modules", params);
  }

  /** Operate Node modules */
  async operateNodeModules(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/node/modules/operate", params);
  }

  /** Get Node package scripts */
  async getNodePackageScripts(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/node/package", params);
  }

  // ==================== Supervisor ====================

  /** Get supervisor process */
  async getSupervisorProcess(id: number): Promise<any> {
    return this.get(`/api/v2/runtimes/supervisor/process/${id}`);
  }

  /** Operate supervisor process */
  async operateSupervisorProcess(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/supervisor/process", params);
  }

  /** Operate supervisor process file */
  async operateSupervisorProcessFile(params: any): Promise<any> {
    return this.post("/api/v2/runtimes/supervisor/process/file", params);
  }
}
