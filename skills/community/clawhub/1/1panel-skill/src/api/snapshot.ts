import { BaseAPI } from "./base.js";

export interface SnapshotCreateRequest {
  /** 名称 */
  name: string;
  /** 描述 */
  description?: string;
  /** 是否包含 Docker */
  withDocker?: boolean;
}

export interface SnapshotImportRequest {
  /** 来源 */
  from: string;
  /** 名称列表 */
  names: string[];
}

/**
 * Snapshot API
 */
export class SnapshotAPI extends BaseAPI {
  // ==================== Snapshot Management ====================

  /** Page system snapshot */
  async list(params?: any): Promise<any> {
    return this.post("/api/v2/settings/snapshot/search", params || { page: 1, pageSize: 100 });
  }

  /** Create system snapshot */
  async create(params: SnapshotCreateRequest): Promise<any> {
    return this.post("/api/v2/settings/snapshot", params);
  }

  /** Delete system backup */
  async remove(ids: number[]): Promise<any> {
    return this.post("/api/v2/settings/snapshot/del", { ids });
  }

  /** Update snapshot description */
  async updateDescription(id: number, description: string): Promise<any> {
    return this.post("/api/v2/settings/snapshot/description/update", { id, description });
  }

  // ==================== Snapshot Operations ====================

  /** Import system snapshot */
  async import(params: SnapshotImportRequest): Promise<any> {
    return this.post("/api/v2/settings/snapshot/import", params);
  }

  /** Load system snapshot data */
  async load(id: number): Promise<any> {
    return this.get(`/api/v2/settings/snapshot/load/${id}`);
  }

  /** Recover system backup */
  async recover(id: number, isNewSnapshot: boolean = false): Promise<any> {
    return this.post("/api/v2/settings/snapshot/recover", { id, isNewSnapshot });
  }

  /** Recreate system snapshot */
  async recreate(id: number): Promise<any> {
    return this.post("/api/v2/settings/snapshot/recreate", { id });
  }

  /** Rollback system backup */
  async rollback(params: any): Promise<any> {
    return this.post("/api/v2/settings/snapshot/rollback", params);
  }
}
