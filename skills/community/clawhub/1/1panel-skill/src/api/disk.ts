import { BaseAPI } from "./base.js";

export interface DiskMountRequest {
  /** 设备路径 */
  path: string;
  /** 挂载点 */
  mountPoint: string;
  /** 文件系统类型 */
  fsType?: string;
  /** 选项 */
  options?: string;
}

export interface DiskPartitionRequest {
  /** 设备路径 */
  path: string;
  /** 分区类型 */
  type?: string;
}

/**
 * Disk Management API
 */
export class DiskAPI extends BaseAPI {
  /**
   * Get complete disk information
   */
  async list(): Promise<any> {
    return this.get("/api/v2/hosts/disks");
  }

  /**
   * Mount disk
   */
  async mount(params: DiskMountRequest): Promise<any> {
    return this.post("/api/v2/hosts/disks/mount", params);
  }

  /**
   * Partition disk
   */
  async partition(params: DiskPartitionRequest): Promise<any> {
    return this.post("/api/v2/hosts/disks/partition", params);
  }

  /**
   * Unmount disk
   */
  async unmount(mountPoint: string): Promise<any> {
    return this.post("/api/v2/hosts/disks/unmount", { path: mountPoint });
  }
}
