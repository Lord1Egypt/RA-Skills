import { BaseAPI } from "./base.js";

// ==================== Domain ====================
export interface DomainCreateRequest {
  websiteId: number;
  domain: string;
  port?: number;
}

export interface DomainDeleteRequest {
  id: number;
}

export interface DomainUpdateRequest {
  id: number;
  websiteId: number;
  domain?: string;
  port?: number;
}

// ==================== SSL ====================
export interface SSLObtainRequest {
  ID: number;
  domains: string[];
  keyType: string;
  time?: number;
  unit?: string;
  autoRenew?: boolean;
}

export interface SSLRenewRequest {
  ID: number;
}

export interface SSLApplyRequest {
  websiteId: number;
  websiteSSLId?: number;
  type: "existed" | "auto" | "manual";
  enable: boolean;
  httpConfig?: "HTTPSOnly" | "HTTPAlso" | "HTTPToHTTPS";
  privateKey?: string;
  certificate?: string;
  algorithm?: string;
  hsts?: boolean;
  hstsIncludeSubDomains?: boolean;
  http3?: boolean;
  httpsPorts?: number[];
}

export interface NginxUpdateRequest {
  id: number;
  content: string;
}

export class WebsiteAPI extends BaseAPI {
  // ==================== Website Core ====================

  /** List websites */
  async list(): Promise<any> {
    return this.request("/api/v2/websites/list", { method: "GET" });
  }

  /** List all websites */
  async listAll(): Promise<any> {
    return this.request("/api/v2/websites/list", { method: "GET" });
  }

  /** Search websites with pagination */
  async search(params: any): Promise<any> {
    return this.post("/api/v2/websites/search", params);
  }

  /** Get website by ID */
  async getById(id: number): Promise<any> {
    return this.request(`/api/v2/websites/${id}`, { method: "GET" });
  }

  /** Get website detail */
  async getDetail(id: number): Promise<any> {
    return this.request(`/api/v2/websites/${id}`, { method: "GET" });
  }

  /** Create website */
  async create(site: any): Promise<any> {
    return this.post("/api/v2/websites", site);
  }

  /** Update website */
  async update(site: any): Promise<any> {
    return this.post("/api/v2/websites/update", site);
  }

  /** Delete website */
  async remove(id: number): Promise<any> {
    return this.post("/api/v2/websites/del", { id });
  }

  /** Check before create website */
  async check(params: any): Promise<any> {
    return this.post("/api/v2/websites/check", params);
  }

  /** Operate website */
  async operate(params: any): Promise<any> {
    return this.post("/api/v2/websites/operate", params);
  }

  /** Get website config */
  async getConfig(id: number, type: string): Promise<any> {
    return this.request(`/api/v2/websites/${id}/config/${type}`, { method: "GET" });
  }

  /** Update website config */
  async updateConfig(params: any): Promise<any> {
    return this.post("/api/v2/websites/config/update", params);
  }

  /** Get website resource */
  async getResource(id: number): Promise<any> {
    return this.request(`/api/v2/websites/resource/${id}`, { method: "GET" });
  }

  /** Get website dir */
  async getDir(params: any): Promise<any> {
    return this.post("/api/v2/websites/dir", params);
  }

  /** Update website dir */
  async updateDir(params: any): Promise<any> {
    return this.post("/api/v2/websites/dir/update", params);
  }

  /** Update site dir permission */
  async updateDirPermission(params: any): Promise<any> {
    return this.post("/api/v2/websites/dir/permission", params);
  }

  /** List website names */
  async listOptions(): Promise<any> {
    return this.post("/api/v2/websites/options", {});
  }

  /** Operate website log */
  async operateLog(params: any): Promise<any> {
    return this.post("/api/v2/websites/log", params);
  }

  // ==================== Batch Operations ====================

  /** Batch set website group */
  async batchSetGroup(params: any): Promise<any> {
    return this.post("/api/v2/websites/batch/group", params);
  }

  /** Batch set HTTPS for websites */
  async batchSetHTTPS(params: any): Promise<any> {
    return this.post("/api/v2/websites/batch/https", params);
  }

  /** Batch operate websites */
  async batchOperate(params: any): Promise<any> {
    return this.post("/api/v2/websites/batch/operate", params);
  }

  // ==================== Domain ====================

  async listDomains(websiteId: number): Promise<any> {
    return this.request(`/api/v2/websites/domains/${websiteId}`, { method: "GET" });
  }

  async createDomain(params: DomainCreateRequest): Promise<any> {
    return this.post("/api/v2/websites/domains", params);
  }

  async deleteDomain(params: DomainDeleteRequest): Promise<any> {
    return this.post("/api/v2/websites/domains/del", params);
  }

  async updateDomain(params: DomainUpdateRequest): Promise<any> {
    return this.post("/api/v2/websites/domains/update", params);
  }

  // ==================== SSL ====================

  async listCertificates(): Promise<any> {
    return this.post("/api/v2/websites/ssl/search", { page: 1, pageSize: 100 });
  }

  async getCertificate(id: number): Promise<any> {
    return this.request(`/api/v2/websites/ssl/${id}`, { method: "GET" });
  }

  async createCertificate(cert: any): Promise<any> {
    return this.post("/api/v2/websites/ssl", cert);
  }

  async deleteCertificate(id: number): Promise<any> {
    return this.post("/api/v2/websites/ssl/del", { id });
  }

  async obtainSSL(params: SSLObtainRequest): Promise<any> {
    return this.post("/api/v2/websites/ssl/obtain", params);
  }

  async renewSSL(params: SSLRenewRequest): Promise<any> {
    return this.post("/api/v2/websites/ssl/renew", params);
  }

  async resolveSSL(params: { websiteSSLId: number }): Promise<any> {
    return this.post("/api/v2/websites/ssl/resolve", params);
  }

  async uploadSSL(params: any): Promise<any> {
    return this.post("/api/v2/websites/ssl/upload", params);
  }

  async uploadSSLFile(params: any): Promise<any> {
    return this.post("/api/v2/websites/ssl/upload/file", params);
  }

  async downloadSSL(params: any): Promise<any> {
    return this.post("/api/v2/websites/ssl/download", params);
  }

  async getWebsiteSSL(websiteId: number): Promise<any> {
    return this.request(`/api/v2/websites/ssl/website/${websiteId}`, { method: "GET" });
  }

  async listSSL(): Promise<any> {
    return this.post("/api/v2/websites/ssl/list", {});
  }

  async updateSSL(params: any): Promise<any> {
    return this.post("/api/v2/websites/ssl/update", params);
  }

  // ==================== HTTPS ====================

  async getHTTPS(id: number): Promise<any> {
    return this.request(`/api/v2/websites/${id}/https`, { method: "GET" });
  }

  async updateHTTPS(params: SSLApplyRequest): Promise<any> {
    return this.post(`/api/v2/websites/${params.websiteId}/https`, params);
  }

  async applySSL(params: SSLApplyRequest): Promise<any> {
    return this.post("/api/v2/websites/ssl/apply", params);
  }

  // ==================== Nginx ====================

  async getNginxConf(id: number): Promise<any> {
    return this.request(`/api/v2/websites/nginx/${id}`, { method: "GET" });
  }

  async updateNginxConf(params: NginxUpdateRequest): Promise<any> {
    return this.post("/api/v2/websites/nginx/update", params);
  }

  // ==================== CORS ====================

  async getCORS(id: number): Promise<any> {
    return this.request(`/api/v2/websites/cors/${id}`, { method: "GET" });
  }

  async updateCORS(params: any): Promise<any> {
    return this.post("/api/v2/websites/cors/update", params);
  }

  // ==================== Auth ====================

  async getAuths(): Promise<any> {
    return this.post("/api/v2/websites/auths", {});
  }

  async getAuthsByPath(params: any): Promise<any> {
    return this.post("/api/v2/websites/auths/path", params);
  }

  async updateAuths(params: any): Promise<any> {
    return this.post("/api/v2/websites/auths/update", params);
  }

  async updateAuthsByPath(params: any): Promise<any> {
    return this.post("/api/v2/websites/auths/path/update", params);
  }

  // ==================== Database ====================

  async getDatabases(): Promise<any> {
    return this.request("/api/v2/websites/databases", { method: "GET" });
  }

  async changeDatabase(params: any): Promise<any> {
    return this.post("/api/v2/websites/databases", params);
  }

  // ==================== PHP ====================

  async getPHPConfig(id: number): Promise<any> {
    return this.request(`/api/v2/websites/php/config/${id}`, { method: "GET" });
  }

  async updatePHPConfig(id: number, params: any): Promise<any> {
    return this.post(`/api/v2/websites/php/config/${id}`, params);
  }

  async updatePHPVersion(params: any): Promise<any> {
    return this.post("/api/v2/websites/php/version", params);
  }

  // ==================== Default HTML ====================

  async getDefaultHtml(type: string): Promise<any> {
    return this.request(`/api/v2/websites/default/html/${type}`, { method: "GET" });
  }

  async updateDefaultHtml(params: any): Promise<any> {
    return this.post("/api/v2/websites/default/html/update", params);
  }

  async changeDefaultServer(params: any): Promise<any> {
    return this.post("/api/v2/websites/default/server", params);
  }

  // ==================== Load Balance ====================

  async getLoadBalance(): Promise<any> {
    return this.request("/api/v2/websites/lbs", { method: "GET" });
  }

  async createLoadBalance(params: any): Promise<any> {
    return this.post("/api/v2/websites/lbs/create", params);
  }

  async deleteLoadBalance(params: any): Promise<any> {
    return this.post("/api/v2/websites/lbs/del", params);
  }

  async updateLoadBalance(params: any): Promise<any> {
    return this.post("/api/v2/websites/lbs/update", params);
  }

  async updateLoadBalanceFile(params: any): Promise<any> {
    return this.post("/api/v2/websites/lbs/file", params);
  }

  // ==================== Proxy ====================

  async getProxies(params: any): Promise<any> {
    return this.post("/api/v2/websites/proxies", params);
  }

  async updateProxy(params: any): Promise<any> {
    return this.post("/api/v2/websites/proxies/update", params);
  }

  async deleteProxy(params: any): Promise<any> {
    return this.post("/api/v2/websites/proxies/delete", params);
  }

  async updateProxyStatus(params: any): Promise<any> {
    return this.post("/api/v2/websites/proxies/status", params);
  }

  async updateProxyFile(params: any): Promise<any> {
    return this.post("/api/v2/websites/proxies/file", params);
  }

  async getProxyCacheConfig(id: number): Promise<any> {
    return this.request(`/api/v2/websites/proxy/config/${id}`, { method: "GET" });
  }

  async updateProxyCacheConfig(params: any): Promise<any> {
    return this.post("/api/v2/websites/proxy/config", params);
  }

  async clearProxyCache(params: any): Promise<any> {
    return this.post("/api/v2/websites/proxy/clear", params);
  }

  // ==================== Real IP ====================

  async getRealIPConfig(id: number): Promise<any> {
    return this.request(`/api/v2/websites/realip/config/${id}`, { method: "GET" });
  }

  async setRealIP(params: any): Promise<any> {
    return this.post("/api/v2/websites/realip/config", params);
  }

  // ==================== Redirect ====================

  async getRedirect(params: any): Promise<any> {
    return this.post("/api/v2/websites/redirect", params);
  }

  async updateRedirect(params: any): Promise<any> {
    return this.post("/api/v2/websites/redirect/update", params);
  }

  async updateRedirectFile(params: any): Promise<any> {
    return this.post("/api/v2/websites/redirect/file", params);
  }

  // ==================== Rewrite ====================

  async getRewrite(params: any): Promise<any> {
    return this.post("/api/v2/websites/rewrite", params);
  }

  async getRewriteCustom(): Promise<any> {
    return this.request("/api/v2/websites/rewrite/custom", { method: "GET" });
  }

  async operateRewriteCustom(params: any): Promise<any> {
    return this.post("/api/v2/websites/rewrite/custom", params);
  }

  async updateRewrite(params: any): Promise<any> {
    return this.post("/api/v2/websites/rewrite/update", params);
  }

  // ==================== ACME ====================

  async getAcmeAccounts(): Promise<any> {
    return this.post("/api/v2/websites/acme", {});
  }

  async searchAcmeAccounts(params: any): Promise<any> {
    return this.post("/api/v2/websites/acme/search", params);
  }

  async createAcmeAccount(params: any): Promise<any> {
    return this.post("/api/v2/websites/acme", params);
  }

  async updateAcmeAccount(params: any): Promise<any> {
    return this.post("/api/v2/websites/acme/update", params);
  }

  async deleteAcmeAccount(params: any): Promise<any> {
    return this.post("/api/v2/websites/acme/del", params);
  }

  // ==================== CA ====================

  async getCAList(): Promise<any> {
    return this.request("/api/v2/websites/ca", { method: "GET" });
  }

  async getCA(id: number): Promise<any> {
    return this.request(`/api/v2/websites/ca/${id}`, { method: "GET" });
  }

  async searchCA(params: any): Promise<any> {
    return this.post("/api/v2/websites/ca/search", params);
  }

  async createCA(params: any): Promise<any> {
    return this.post("/api/v2/websites/ca", params);
  }

  async deleteCA(params: any): Promise<any> {
    return this.post("/api/v2/websites/ca/del", params);
  }

  async obtainCASSL(params: any): Promise<any> {
    return this.post("/api/v2/websites/ca/obtain", params);
  }

  async renewCASSL(params: any): Promise<any> {
    return this.post("/api/v2/websites/ca/renew", params);
  }

  async downloadCA(params: any): Promise<any> {
    return this.post("/api/v2/websites/ca/download", params);
  }

  // ==================== DNS ====================

  async getDNSConfig(): Promise<any> {
    return this.request("/api/v2/websites/dns", { method: "GET" });
  }

  async searchDNS(params: any): Promise<any> {
    return this.post("/api/v2/websites/dns/search", params);
  }

  async createDNS(params: any): Promise<any> {
    return this.post("/api/v2/websites/dns", params);
  }

  async updateDNSConfig(params: any): Promise<any> {
    return this.post("/api/v2/websites/dns", params);
  }

  async deleteDNS(params: any): Promise<any> {
    return this.post("/api/v2/websites/dns/del", params);
  }

  async getDNSResolve(): Promise<any> {
    return this.request("/api/v2/websites/dns/resolve", { method: "GET" });
  }

  // ==================== Cross Site ====================

  async operateCrossSite(params: any): Promise<any> {
    return this.post("/api/v2/websites/crosssite", params);
  }

  // ==================== Stream ====================

  async updateStreamConfig(params: any): Promise<any> {
    return this.post("/api/v2/websites/stream/update", params);
  }

  // ==================== AntiLeech (XPack) ====================

  async getAntiLeechConf(websiteId: number): Promise<any> {
    return this.request(`/api/v2/websites/leech/${websiteId}`, { method: "GET" });
  }

  async updateAntiLeech(params: any): Promise<any> {
    return this.post("/api/v2/websites/leech/update", params);
  }
}
