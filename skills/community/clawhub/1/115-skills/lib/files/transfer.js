const HttpClient = require('../client/http-client');
const fs = require('fs');
const path = require('path');

/**
 * 115 文件上传下载 API
 * 
 * 功能：
 * - 文件上传（支持大文件分片）
 * - 文件下载
 * - 断点续传
 * - 进度跟踪
 */
class FileTransfer {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.apiBase = 'https://uplb.115.com';
  }

  /**
   * 上传文件
   * @param {string} filePath - 本地文件路径
   * @param {string} targetCid - 目标目录 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 上传结果
   */
  async uploadFile(filePath, targetCid = '0', options = {}) {
    const { onProgress = null } = options;

    // 检查文件
    if (!fs.existsSync(filePath)) {
      return { success: false, message: `文件不存在：${filePath}` };
    }

    const fileStat = fs.statSync(filePath);
    const fileSize = fileStat.size;

    // 小文件直接上传
    if (fileSize < 10 * 1024 * 1024) { // 10MB
      return this._uploadSmallFile(filePath, targetCid, onProgress);
    }

    // 大文件分片上传
    return this._uploadLargeFile(filePath, targetCid, onProgress);
  }

  /**
   * 上传小文件
   * @private
   */
  async _uploadSmallFile(filePath, targetCid, onProgress) {
    const fileName = path.basename(filePath);
    const fileContent = fs.readFileSync(filePath);

    const FormData = require('form-data');
    const form = new FormData();
    form.append('file', fileContent, { filename: fileName });
    form.append('target', targetCid);

    const response = await this.http.request(`${this.apiBase}/3.0/file/upload`, {
      method: 'POST',
      data: form,
      headers: form.getHeaders()
    });

    if (!response.state) {
      return { success: false, message: response.error || '上传失败', fileId: null };
    }

    onProgress?.({ percent: 100, uploaded: fileContent.length, total: fileContent.length });

    return {
      success: true,
      fileId: response.file_id,
      fileName,
      fileSize: fileContent.length,
      targetCid
    };
  }

  /**
   * 上传大文件（分片）
   * @private
   */
  async _uploadLargeFile(filePath, targetCid, onProgress) {
    const fileName = path.basename(filePath);
    const fileSize = fs.statSync(filePath).size;
    const chunkSize = 5 * 1024 * 1024; // 5MB per chunk
    const totalChunks = Math.ceil(fileSize / chunkSize);

    // 1. 初始化上传
    const initResponse = await this.http.post('/upload/init', {
      filename: fileName,
      filesize: fileSize,
      target: targetCid
    });

    const uploadId = initResponse.upload_id;

    // 2. 分片上传
    let uploaded = 0;
    for (let i = 0; i < totalChunks; i++) {
      const start = i * chunkSize;
      // fs.readFileSync 的 end 是包含的，所以需要减 1
      const end = Math.min(start + chunkSize, fileSize) - 1;
      const chunk = fs.readFileSync(filePath, { start, end });

      await this.http.post('/upload/chunk', {
        upload_id: uploadId,
        chunk_index: i,
        chunk_size: chunk.length,
        chunk_data: chunk.toString('base64')
      });

      uploaded += chunk.length;
      onProgress?.({
        percent: Math.round((uploaded / fileSize) * 100),
        uploaded,
        total: fileSize,
        chunk: i + 1,
        totalChunks
      });

      await this.http.sleep(500); // 避免速率限制
    }

    // 3. 完成上传
    const completeResponse = await this.http.post('/upload/complete', {
      upload_id: uploadId
    });

    return {
      success: true,
      fileId: completeResponse.file_id,
      fileName,
      fileSize,
      targetCid
    };
  }

  /**
   * 下载文件
   * @param {string} fileId - 文件 ID
   * @param {string} savePath - 保存路径
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 下载结果
   */
  async downloadFile(fileId, savePath, options = {}) {
    const { onProgress = null } = options;

    // 1. 获取下载链接
    const urlResponse = await this.http.get('/files/download', {
      fid: fileId,
      _: Date.now()
    });

    if (!urlResponse.state) {
      return { success: false, message: urlResponse.error || '获取下载链接失败', downloadUrl: null };
    }

    const downloadUrl = urlResponse.data.url;
    const fileName = urlResponse.data.file_name;
    const fileSize = urlResponse.data.file_size;

    // 2. 下载文件
    const axios = require('axios');
    const writer = fs.createWriteStream(savePath);

    const response = await axios({
      url: downloadUrl,
      method: 'GET',
      responseType: 'stream'
    });

    let downloaded = 0;
    response.data.on('data', chunk => {
      downloaded += chunk.length;
      onProgress?.({
        percent: Math.round((downloaded / fileSize) * 100),
        downloaded,
        total: fileSize
      });
    });

    await new Promise((resolve, reject) => {
      response.data.pipe(writer);
      writer.on('finish', resolve);
      writer.on('error', reject);
    });

    return {
      success: true,
      fileId,
      fileName,
      fileSize,
      savePath
    };
  }

  /**
   * 批量上传
   * @param {Array<string>} filePaths - 文件路径数组
   * @param {string} targetCid - 目标目录 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 上传结果
   */
  async batchUpload(filePaths, targetCid = '0', options = {}) {
    const { onProgress = null } = options;
    const results = {
      total: filePaths.length,
      success: 0,
      failed: 0,
      details: []
    };

    for (let i = 0; i < filePaths.length; i++) {
      try {
        const result = await this.uploadFile(filePaths[i], targetCid, {
          onProgress: (progress) => {
            onProgress?.({
              file: filePaths[i],
              index: i + 1,
              total: filePaths.length,
              ...progress
            });
          }
        });
        results.success++;
        results.details.push({ success: true, file: filePaths[i], ...result });
      } catch (error) {
        results.failed++;
        results.details.push({ success: false, file: filePaths[i], error: error.message });
      }
    }

    return results;
  }

  /**
   * 获取上传配额
   * @returns {Promise<Object>} 配额信息
   */
  async getUploadQuota() {
    const response = await this.http.get('/upload/quota');

    if (!response.state) {
      return { success: false, message: response.error || '获取配额失败', quota: null };
    }

    return {
      success: true,
      quota: response.data || {}
    };
  }
}

module.exports = FileTransfer;
