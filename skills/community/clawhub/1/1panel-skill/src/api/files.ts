import { BaseAPI } from "./base.js";

export interface CompressRequest {
  files: string[];
  dst: string;
  name: string;
  type: "zip" | "tar" | "tar.gz";
  replace?: boolean;
  secret?: string;
}

export interface DecompressRequest {
  path: string;
  dst: string;
  type: "zip" | "tar" | "tar.gz";
  secret?: string;
}

export interface MoveRequest {
  from: string;
  to: string;
  overwrite?: boolean;
}

export interface RenameRequest {
  path: string;
  name: string;
}

export interface ChmodRequest {
  path: string;
  mode: string;
  sub?: boolean;
}

export interface ChownRequest {
  path: string;
  user: string;
  group: string;
  sub?: boolean;
}

export interface UploadRequest {
  path: string;
  filename: string;
  content: string;
}

export interface FileSearchRequest {
  path: string;
  page?: number;
  pageSize?: number;
  search?: string;
  sort?: string;
}

/**
 * File Management API
 */
export class FileAPI extends BaseAPI {
  // ==================== List & Search ====================

  /** List files */
  async list(path: string, page = 1, pageSize = 100): Promise<any> {
    return this.post("/api/v2/files/search", { path, page, pageSize });
  }

  /** Search files */
  async search(params: FileSearchRequest): Promise<any> {
    return this.post("/api/v2/files/search", { page: 1, pageSize: 100, ...params });
  }

  /** Load files tree */
  async getTree(path: string): Promise<any> {
    return this.post("/api/v2/files/tree", { path });
  }

  /** Page file */
  async pageFiles(params: any): Promise<any> {
    return this.post("/api/v2/files/upload/search", params);
  }

  // ==================== File Content ====================

  /** Load file content */
  async getContent(path: string): Promise<any> {
    return this.post("/api/v2/files/content", { path });
  }

  /** Create file */
  async create(path: string, content = ""): Promise<any> {
    return this.post("/api/v2/files", { path, content });
  }

  /** Update file content */
  async save(path: string, content: string): Promise<any> {
    return this.post("/api/v2/files/save", { path, content });
  }

  /** Preview file content */
  async preview(path: string): Promise<any> {
    return this.post("/api/v2/files/preview", { path });
  }

  /** Read file by Line */
  async readByLine(params: any): Promise<any> {
    return this.post("/api/v2/files/read", params);
  }

  // ==================== File Operations ====================

  /** Check file exist */
  async check(path: string): Promise<any> {
    return this.post("/api/v2/files/check", { path });
  }

  /** Batch check file exist */
  async batchCheck(paths: string[]): Promise<any> {
    return this.post("/api/v2/files/batch/check", { paths });
  }

  /** Delete file or directory */
  async delete(path: string, forceDelete = false): Promise<any> {
    return this.post("/api/v2/files/del", { path, forceDelete });
  }

  /** Batch delete file */
  async batchDelete(paths: string[]): Promise<any> {
    return this.post("/api/v2/files/batch/del", { paths });
  }

  /** Create directory */
  async createDir(path: string): Promise<any> {
    return this.post("/api/v2/files/dir", { path });
  }

  /** Move file/ directory */
  async move(params: MoveRequest): Promise<any> {
    return this.post("/api/v2/files/move", params);
  }

  /** Change file name */
  async rename(params: RenameRequest): Promise<any> {
    return this.post("/api/v2/files/rename", params);
  }

  /** Change file mode (chmod) */
  async chmod(params: ChmodRequest): Promise<any> {
    return this.post("/api/v2/files/mode", params);
  }

  /** Change file owner (chown) */
  async chown(params: ChownRequest): Promise<any> {
    return this.post("/api/v2/files/owner", params);
  }

  /** Batch change file mode and owner */
  async batchChmodChown(params: any): Promise<any> {
    return this.post("/api/v2/files/batch/role", params);
  }

  // ==================== Compress & Decompress ====================

  /** Compress file/ directory */
  async compress(params: CompressRequest): Promise<any> {
    return this.post("/api/v2/files/compress", params);
  }

  /** Decompress file */
  async decompress(params: DecompressRequest): Promise<any> {
    return this.post("/api/v2/files/decompress", params);
  }

  // ==================== Upload & Download ====================

  /** Upload file */
  async upload(params: UploadRequest): Promise<any> {
    return this.post("/api/v2/files/upload", params);
  }

  /** ChunkUpload file */
  async chunkUpload(params: any): Promise<any> {
    return this.post("/api/v2/files/chunkupload", params);
  }

  /** Download file */
  async download(path: string): Promise<any> {
    return this.post("/api/v2/files/download", { path });
  }

  /** Chunk Download file */
  async chunkDownload(params: any): Promise<any> {
    return this.post("/api/v2/files/chunkdownload", params);
  }

  /** Wget file */
  async wget(url: string, path: string, ignoreCertificate = false): Promise<any> {
    return this.post("/api/v2/files/wget", { url, path, ignoreCertificate });
  }

  // ==================== File Info ====================

  /** Load file size */
  async getSize(path: string): Promise<any> {
    return this.post("/api/v2/files/size", { path });
  }

  /** Multi file size */
  async getMultiSize(paths: string[]): Promise<any> {
    return this.post("/api/v2/files/depth/size", { paths });
  }

  /** Batch get file remarks */
  async getRemarks(paths: string[]): Promise<any> {
    return this.post("/api/v2/files/remarks", { paths });
  }

  /** Set file remark */
  async setRemark(path: string, remark: string): Promise<any> {
    return this.post("/api/v2/files/remark", { path, remark });
  }

  // ==================== Convert ====================

  /** Convert file */
  async convert(params: any): Promise<any> {
    return this.post("/api/v2/files/convert", params);
  }

  /** Convert file log */
  async convertLog(params: any): Promise<any> {
    return this.post("/api/v2/files/convert/log", params);
  }

  // ==================== Favorites ====================

  /** List favorites */
  async listFavorites(): Promise<any> {
    return this.post("/api/v2/files/favorite/search", {});
  }

  /** Create favorite */
  async addFavorite(path: string): Promise<any> {
    return this.post("/api/v2/files/favorite", { path });
  }

  /** Delete favorite */
  async removeFavorite(path: string): Promise<any> {
    return this.post("/api/v2/files/favorite/del", { path });
  }

  // ==================== System ====================

  /** system mount */
  async mount(params: any): Promise<any> {
    return this.post("/api/v2/files/mount", params);
  }

  /** system user and group */
  async getUserGroup(): Promise<any> {
    return this.post("/api/v2/files/user/group", {});
  }

  // ==================== Backup Files ====================

  /** List files from backup accounts */
  async listBackupFiles(params: any): Promise<any> {
    return this.post("/api/v2/backups/search/files", params);
  }

  // ==================== System Logs ====================

  /** Load system log files */
  async listSystemLogFiles(): Promise<any> {
    return this.get("/api/v2/logs/system/files");
  }
}
