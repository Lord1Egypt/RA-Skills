import { BaseAPI } from "./base.js";

export interface FileInfo {
  name: string;
  path: string;
  size: number;
  isDir: boolean;
  isSymlink: boolean;
  mode: string;
  user: string;
  group: string;
  modTime: string;
}

export interface CompressRequest {
  /** 目标目录路径 */
  dst: string;
  /** 要压缩的文件路径列表 */
  files: string[];
  /** 压缩包名称 */
  name: string;
  /** 是否替换已存在的文件 */
  replace?: boolean;
  /** 压缩密码 (可选) */
  secret?: string;
  /** 压缩类型: zip, tar, tar.gz */
  type: "zip" | "tar" | "tar.gz";
}

export interface DecompressRequest {
  /** 解压目标目录 */
  dst: string;
  /** 压缩包路径 */
  path: string;
  /** 解压密码 (可选) */
  secret?: string;
  /** 压缩类型: zip, tar, tar.gz */
  type: "zip" | "tar" | "tar.gz";
}

export interface MoveRequest {
  /** 源文件/目录路径 */
  from: string;
  /** 目标路径 */
  to: string;
  /** 是否覆盖 */
  overwrite?: boolean;
}

export interface RenameRequest {
  /** 原文件路径 */
  path: string;
  /** 新名称 */
  name: string;
}

export interface ChmodRequest {
  /** 权限模式 (如: 755, 644) */
  mode: string;
  /** 文件/目录路径 */
  path: string;
  /** 是否递归修改子目录 */
  sub?: boolean;
}

export interface ChownRequest {
  /** 所属组 */
  group: string;
  /** 文件/目录路径 */
  path: string;
  /** 是否递归修改子目录 */
  sub?: boolean;
  /** 所属用户 */
  user: string;
}

export interface UploadRequest {
  /** 目标路径 */
  path: string;
  /** 文件名 */
  filename: string;
  /** 文件内容 (base64) */
  content: string;
}

export interface DownloadRequest {
  /** 文件路径 */
  path: string;
}

export interface FileSearchRequest {
  /** 搜索路径 */
  path: string;
  /** 页码 */
  page?: number;
  /** 每页数量 */
  pageSize?: number;
  /** 搜索关键词 */
  search?: string;
  /** 排序方式 */
  sort?: string;
}

export class FileAPI extends BaseAPI {
  /**
   * 列出目录内容
   */
  async list(path: string, page = 1, pageSize = 100): Promise<any> {
    return this.post("/api/v2/files/search", { path, page, pageSize });
  }

  /**
   * 搜索文件
   */
  async search(params: FileSearchRequest): Promise<any> {
    return this.post("/api/v2/files/search", {
      page: 1,
      pageSize: 100,
      ...params,
    });
  }

  /**
   * 获取文件内容
   */
  async getContent(path: string): Promise<any> {
    return this.post("/api/v2/files/content", { path });
  }

  /**
   * 保存文件内容
   */
  async save(path: string, content: string): Promise<any> {
    return this.post("/api/v2/files", { path, content });
  }

  /**
   * 删除文件或目录
   */
  async delete(path: string, forceDelete = false): Promise<any> {
    return this.post("/api/v2/files/del", { path, forceDelete });
  }

  /**
   * 创建目录
   */
  async createDir(path: string): Promise<any> {
    return this.post("/api/v2/files/dir", { path });
  }

  /**
   * 创建文件
   */
  async createFile(path: string): Promise<any> {
    return this.post("/api/v2/files", { path, content: "" });
  }

  /**
   * 压缩文件/目录
   */
  async compress(params: CompressRequest): Promise<any> {
    return this.post("/api/v2/files/compress", params);
  }

  /**
   * 解压文件
   */
  async decompress(params: DecompressRequest): Promise<any> {
    return this.post("/api/v2/files/decompress", params);
  }

  /**
   * 移动文件/目录
   */
  async move(params: MoveRequest): Promise<any> {
    return this.post("/api/v2/files/move", params);
  }

  /**
   * 重命名文件/目录
   */
  async rename(params: RenameRequest): Promise<any> {
    return this.post("/api/v2/files/rename", params);
  }

  /**
   * 修改文件权限 (chmod)
   */
  async chmod(params: ChmodRequest): Promise<any> {
    return this.post("/api/v2/files/mode", params);
  }

  /**
   * 修改文件所有者 (chown)
   */
  async chown(params: ChownRequest): Promise<any> {
    return this.post("/api/v2/files/owner", params);
  }

  /**
   * 检查文件是否存在
   */
  async check(path: string): Promise<any> {
    return this.post("/api/v2/files/check", { path });
  }

  /**
   * 获取文件大小
   */
  async getSize(path: string): Promise<any> {
    return this.post("/api/v2/files/size", { path });
  }

  /**
   * 获取目录树
   */
  async getTree(path: string): Promise<any> {
    return this.post("/api/v2/files/tree", { path });
  }

  /**
   * 下载文件 (返回下载链接)
   */
  async download(path: string): Promise<any> {
    return this.post("/api/v2/files/download", { path });
  }

  /**
   * 上传文件
   */
  async upload(params: UploadRequest): Promise<any> {
    return this.post("/api/v2/files/upload", params);
  }

  /**
   * 通过 URL 下载文件到服务器
   */
  async wget(url: string, path: string, ignoreCertificate = false): Promise<any> {
    return this.post("/api/v2/files/wget", { url, path, ignoreCertificate });
  }
}
