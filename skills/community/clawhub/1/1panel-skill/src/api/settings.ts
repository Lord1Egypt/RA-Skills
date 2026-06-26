import { BaseAPI } from "./base.js";

/**
 * System Settings API
 */
export class SettingsAPI extends BaseAPI {
  // ==================== General Settings ====================

  /** Get all settings */
  async getAll(): Promise<any> {
    return this.get("/api/v2/settings/search");
  }

  /** Load system setting by key */
  async getByKey(key: string): Promise<any> {
    return this.post("/api/v2/settings/by", { key });
  }

  /** Update settings */
  async update(settings: any): Promise<any> {
    return this.post("/api/v2/settings/update", settings);
  }

  /** Update system setting */
  async updateMenu(params: any): Promise<any> {
    return this.post("/api/v2/settings/menu/update", params);
  }

  /** Default menu */
  async defaultMenu(): Promise<any> {
    return this.post("/api/v2/settings/menu/default", {});
  }

  // ==================== Auth Settings ====================

  /** Get Setting For Login */
  async getAuthSetting(): Promise<any> {
    return this.get("/api/v2/core/auth/setting");
  }

  /** Update system password */
  async updatePassword(oldPassword: string, newPassword: string): Promise<any> {
    return this.post("/api/v2/settings/password/update", { oldPassword, newPassword });
  }

  /** Reset system password expired */
  async resetPasswordExpired(): Promise<any> {
    return this.post("/api/v2/settings/expired/handle", {});
  }

  // ==================== MFA ====================

  /** Load mfa info */
  async getMFAInfo(): Promise<any> {
    return this.post("/api/v2/settings/mfa", {});
  }

  /** Bind mfa */
  async bindMFA(params: any): Promise<any> {
    return this.post("/api/v2/settings/mfa/bind", params);
  }

  // ==================== Passkey ====================

  /** List passkeys */
  async listPasskeys(): Promise<any> {
    return this.get("/api/v2/core/settings/passkey/list");
  }

  /** Begin passkey registration */
  async beginPasskeyRegister(): Promise<any> {
    return this.post("/api/v2/core/settings/passkey/register/begin", {});
  }

  /** Finish passkey registration */
  async finishPasskeyRegister(params: any): Promise<any> {
    return this.post("/api/v2/core/settings/passkey/register/finish", params);
  }

  /** Delete passkey */
  async deletePasskey(id: number): Promise<any> {
    return this.request(`/api/v2/core/settings/passkey/${id}`, { method: "DELETE" });
  }

  // ==================== API Config ====================

  /** generate api key */
  async generateAPIKey(): Promise<any> {
    return this.post("/api/v2/core/settings/api/config/generate/key", {});
  }

  /** Update api config */
  async updateAPIConfig(params: any): Promise<any> {
    return this.post("/api/v2/core/settings/api/config/update", params);
  }

  // ==================== System Bind ====================

  /** Update system bind info */
  async updateBind(params: any): Promise<any> {
    return this.post("/api/v2/core/settings/bind/update", params);
  }

  /** Load system address */
  async getInterface(): Promise<any> {
    return this.get("/api/v2/core/settings/interface");
  }

  // ==================== Dashboard Memo ====================

  /** Load dashboard memo */
  async getMemo(): Promise<any> {
    return this.get("/api/v2/core/settings/memo");
  }

  /** Update dashboard memo */
  async updateMemo(content: string): Promise<any> {
    return this.post("/api/v2/core/settings/memo", { content });
  }

  // ==================== App Store ====================

  /** Get appstore config */
  async getAppStoreConfig(): Promise<any> {
    return this.get("/api/v2/core/settings/apps/store/config");
  }

  /** Update appstore config */
  async updateAppStoreConfig(params: any): Promise<any> {
    return this.post("/api/v2/core/settings/apps/store/update", params);
  }

  // ==================== Snapshot ====================

  /** Load snapshot status */
  async getSnapshotStatus(): Promise<any> {
    return this.get("/api/v2/settings/snapshot/status");
  }

  /** Interrupt snapshot */
  async interruptSnapshot(): Promise<any> {
    return this.post("/api/v2/settings/snapshot/interrupt", {});
  }

  /** Load snapshot description */
  async getSnapshotDescription(): Promise<any> {
    return this.get("/api/v2/settings/snapshot/description");
  }

  // ==================== SSL ====================

  /** Load SSL info */
  async getSSLInfo(): Promise<any> {
    return this.get("/api/v2/settings/ssl/info");
  }

  /** Update SSL */
  async updateSSL(params: any): Promise<any> {
    return this.post("/api/v2/settings/ssl/update", params);
  }

  /** Download SSL */
  async downloadSSL(): Promise<any> {
    return this.post("/api/v2/settings/ssl/download", {});
  }

  /** Load SSL status */
  async getSSLStatus(): Promise<any> {
    return this.get("/api/v2/settings/ssl/status");
  }

  /** Update SSL status */
  async updateSSLStatus(enable: boolean): Promise<any> {
    return this.post("/api/v2/settings/ssl/status", { enable });
  }

  /** Load SSL log */
  async getSSLLog(): Promise<any> {
    return this.get("/api/v2/settings/ssl/log");
  }

  // ==================== Port ====================

  /** Update port */
  async updatePort(port: number): Promise<any> {
    return this.post("/api/v2/settings/port/update", { port });
  }

  /** Update port setting */
  async updatePortSetting(params: any): Promise<any> {
    return this.post("/api/v2/settings/port/update", params);
  }

  // ==================== Entrance ====================

  /** Update entrance */
  async updateEntrance(entrance: string): Promise<any> {
    return this.post("/api/v2/settings/entrance", { entrance });
  }

  /** Update entrance setting */
  async updateEntranceSetting(params: any): Promise<any> {
    return this.post("/api/v2/settings/entrance/update", params);
  }

  // ==================== Title ====================

  /** Update title */
  async updateTitle(title: string): Promise<any> {
    return this.post("/api/v2/settings/title", { title });
  }

  /** Update title setting */
  async updateTitleSetting(params: any): Promise<any> {
    return this.post("/api/v2/settings/title/update", params);
  }

  // ==================== Language ====================

  /** Update language */
  async updateLanguage(language: string): Promise<any> {
    return this.post("/api/v2/settings/language", { language });
  }

  /** Update language setting */
  async updateLanguageSetting(params: any): Promise<any> {
    return this.post("/api/v2/settings/language/update", params);
  }

  // ==================== Theme ====================

  /** Update theme */
  async updateTheme(theme: string): Promise<any> {
    return this.post("/api/v2/settings/theme", { theme });
  }

  /** Update theme setting */
  async updateThemeSetting(params: any): Promise<any> {
    return this.post("/api/v2/settings/theme/update", params);
  }

  // ==================== Session ====================

  /** Update session timeout */
  async updateSessionTimeout(timeout: number): Promise<any> {
    return this.post("/api/v2/settings/session", { timeout });
  }

  /** Update session setting */
  async updateSessionSetting(params: any): Promise<any> {
    return this.post("/api/v2/settings/session/update", params);
  }

  // ==================== JWT ====================

  /** Update JWT settings */
  async updateJWT(params: any): Promise<any> {
    return this.post("/api/v2/settings/jwt/update", params);
  }

  // ==================== Message ====================

  /** Update message settings */
  async updateMessage(params: any): Promise<any> {
    return this.post("/api/v2/settings/message/update", params);
  }

  // ==================== Backup ====================

  /** Update local backup dir */
  async updateLocalBackupDir(path: string): Promise<any> {
    return this.post("/api/v2/settings/backup/local", { path });
  }

  /** Update local backup dir setting */
  async updateLocalBackupDirSetting(params: any): Promise<any> {
    return this.post("/api/v2/settings/backup/local/update", params);
  }

  // ==================== Clean ====================

  /** Clean system cache */
  async cleanCache(): Promise<any> {
    return this.post("/api/v2/settings/clean", {});
  }

  /** Clean system cache setting */
  async cleanCacheSetting(params: any): Promise<any> {
    return this.post("/api/v2/settings/clean/update", params);
  }
}
