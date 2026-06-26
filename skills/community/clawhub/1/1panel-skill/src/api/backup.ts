import { BaseAPI } from "./base.js";

export class BackupAPI extends BaseAPI {
  async list(): Promise<any> {
    return this.post("/api/v2/settings/backup/search", { page: 1, pageSize: 100 });
  }

  async create(backup: any): Promise<any> {
    return this.post("/api/v2/settings/backup", backup);
  }

  async restore(id: number): Promise<any> {
    return this.post("/api/v2/settings/backup/restore", { id });
  }

  async remove(id: number): Promise<any> {
    return this.post("/api/v2/settings/backup/del", { id });
  }
}
