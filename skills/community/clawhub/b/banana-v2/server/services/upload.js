const axios = require('axios');
const fs = require('fs');
const crypto = require('crypto');
const path = require('path');
const FormData = require('form-data');

class UploadHandler {
  constructor(db) {
    this.db = db;
    this.uploadDir = path.join(__dirname, '../../uploads');
    
    // 确保上传目录存在
    if (!fs.existsSync(this.uploadDir)) {
      fs.mkdirSync(this.uploadDir, { recursive: true });
    }
  }

  /**
   * 处理上传流程：
   * 支持多种输入格式：
   * 1. base64 格式 - 直接解码上传
   * 2. 本地绝对路径 - 从硬盘读取文件上传
   * 3. URL 格式 - 下载后上传
   * 4. 相对路径（/images/...）- 转换为本地路径后读取上传
   */
  async upload(data) {
    // 从请求中获取 platform_token，优先使用请求中的，否则使用环境变量
    const platformToken = data.platform_token || process.env.PLATFORM_TOKEN;
    
    // 存储到环境变量（供后续使用）
    if (data.platform_token) {
      process.env.PLATFORM_TOKEN = data.platform_token;
    }
    
    if (!platformToken) {
      throw new Error('请先配置 PLATFORM_TOKEN');
    }

    let fileBuffer;
    let filename;
    let fileHash;
    let ext = 'png'; // 默认扩展名

    // 1. 处理 base64 数据
    console.log(data)
    if (data.base64 && data.base64.startsWith('data:image')) {
      const result = this._processBase64(data.base64, data.name);
      fileBuffer = result.buffer;
      filename = result.filename;
      fileHash = result.hash;
      ext = result.ext || 'png';
    }
    // 2. 处理相对路径（/images/...）
    else if (data.relative_path || (typeof data.base64 === 'string' && this._isRelativePath(data.base64))) {
      const relativePath = data.relative_path || data.base64;
      const result = await this._processRelativePath(relativePath, data.name);
      fileBuffer = result.buffer;
      filename = result.filename;
      fileHash = result.hash;
      ext = result.ext || 'png';
    }
    // 3. 处理本地文件路径
    else if (data.file_path || (typeof data.base64 === 'string' && this._isLocalPath(data.base64))) {
      const filePath = data.file_path || data.base64;
      const result = await this._processLocalFile(filePath, data.name);
      fileBuffer = result.buffer;
      filename = result.filename;
      fileHash = result.hash;
      ext = result.ext || 'png';
    }
    // 4. 处理 URL
    else if (data.url || (typeof data.base64 === 'string' && this._isUrl(data.base64))) {
      const url = data.url || data.base64;
      const result = await this._processUrl(url, data.name);
      fileBuffer = result.buffer;
      filename = result.filename;
      fileHash = result.hash;
      ext = result.ext || 'png';
    }
    // 5. 直接传入 buffer
    else if (data.file && Buffer.isBuffer(data.file)) {
      fileBuffer = data.file;
      fileHash = crypto.createHash('md5').update(fileBuffer).digest('hex');
      filename = data.name || `upload_${fileHash}.png`;
      // 从文件名提取扩展名
      const nameExt = path.extname(filename).slice(1);
      ext = nameExt || 'png';
    }
    else {
      throw new Error('不支持的图片格式，请提供 base64、本地路径、相对路径或 URL');
    }

    console.log(`📁 文件信息: ${filename}, hash: ${fileHash}, 大小: ${fileBuffer.length} bytes`);

    // 检查数据库是否已存在该 hash 的记录
    const existingRecord = await this.db.getUploadRecord(fileHash);
    if (existingRecord) {
      console.log(`✅ 使用缓存的上传记录: ${fileHash}`);
      return {
        success: true,
        url: existingRecord.url,
        cached: true,
        hash: fileHash
      };
    }

    // 读取配置
    const configPath = path.join(__dirname, '../../config/set.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

    try {
      // 创建 FormData
      const formData = new FormData();
      formData.append('file', fileBuffer, {
        filename: filename,
        contentType: `image/${ext}`
      });

      console.log(`📤 上传图片到服务器: ${filename}`);

      // 上传到服务器
      const response = await axios.post(
        config.server.upload_url,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${platformToken}`,
            ...formData.getHeaders()
          },
          timeout: 60000
        }
      );

      const url = response.data.url || response.data.file_url || response.data.data?.url;

      if (!url) {
        throw new Error('上传成功但未获取到URL: ' + JSON.stringify(response.data));
      }

      console.log(`✅ 上传成功: ${url}`);

      // 保存记录到数据库
      await this.db.saveUploadRecord({
        url,
        filename: filename,
        file_hash: fileHash
      });

      return {
        success: true,
        url,
        cached: false,
        hash: fileHash
      };

    } catch (error) {
      let errorMsg = '上传失败';
      
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === 'object') {
          errorMsg = errorData.error || errorData.message || errorData.detail || JSON.stringify(errorData, null, 2);
        } else {
          errorMsg = errorData || error.message;
        }
      } else {
        errorMsg = error.message;
      }
      
      throw new Error(errorMsg);
    }
  }

  /**
   * 处理 base64 数据
   */
  _processBase64(base64Str, name) {
    const matches = base64Str.match(/^data:image\/(\w+);base64,(.+)$/);
    if (!matches) {
      throw new Error('无效的 base64 图片格式');
    }
    
    const ext = matches[1] || 'png';
    const base64Data = matches[2];
    const buffer = Buffer.from(base64Data, 'base64');
    const hash = crypto.createHash('md5').update(buffer).digest('hex');
    const filename = name || `upload_${hash}.${ext}`;
    
    return { buffer, filename, hash, ext };
  }

  /**
   * 处理相对路径（/images/...）
   * 转换为本地绝对路径后读取
   */
  async _processRelativePath(relativePath, name) {
    // /images/53/5.png -> 桌面/banana2/53/5.png
    // 读取配置获取保存路径
    const configPath = path.join(__dirname, '../../config/set.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    
    // 获取默认保存路径
    let basePath = config.default_save_path || '';
    if (!basePath) {
      // 默认使用桌面/banana2
      const os = require('os');
      basePath = path.join(os.homedir(), 'Desktop', 'banana2');
    }
    
    // 移除 /images 前缀
    let relativePart = relativePath;
    if (relativePart.startsWith('/images/')) {
      relativePart = relativePart.substring(8); // 移除 '/images/'
    }
    
    const absolutePath = path.join(basePath, relativePart);
    console.log(`📂 相对路径转换: ${relativePath} -> ${absolutePath}`);
    
    const result = await this._processLocalFile(absolutePath, name);
    return result;
  }

  /**
   * 处理本地文件路径
   */
  async _processLocalFile(filePath, name) {
    // 检查文件是否存在
    if (!fs.existsSync(filePath)) {
      throw new Error(`文件不存在: ${filePath}`);
    }
    
    const buffer = fs.readFileSync(filePath);
    const hash = crypto.createHash('md5').update(buffer).digest('hex');
    const ext = path.extname(filePath).slice(1) || 'png';
    const filename = name || path.basename(filePath) || `upload_${hash}.${ext}`;
    
    console.log(`📂 从本地读取文件: ${filePath}`);
    return { buffer, filename, hash, ext };
  }

  /**
   * 处理 URL
   */
  async _processUrl(url, name) {
    console.log(`🌐 从 URL 下载图片: ${url}`);
    
    const response = await axios.get(url, {
      responseType: 'arraybuffer',
      timeout: 30000
    });
    
    const buffer = Buffer.from(response.data);
    const hash = crypto.createHash('md5').update(buffer).digest('hex');
    
    // 从 URL 或 Content-Type 获取扩展名
    let ext = 'png';
    const contentType = response.headers['content-type'];
    if (contentType && contentType.startsWith('image/')) {
      ext = contentType.split('/')[1].split(';')[0];
    } else {
      const urlExt = path.extname(url).slice(1);
      if (urlExt && ['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(urlExt.toLowerCase())) {
        ext = urlExt.toLowerCase();
      }
    }
    
    const filename = name || `upload_${hash}.${ext}`;
    
    return { buffer, filename, hash, ext };
  }

  /**
   * 判断是否为相对路径（/images/...）
   */
  _isRelativePath(str) {
    return str.startsWith('/images/') || str.startsWith('/image/');
  }

  /**
   * 判断是否为本地路径
   */
  _isLocalPath(str) {
    // Windows: C:\path 或 D:/path
    // Unix: /path (但不是 /images/...)
    return /^[A-Za-z]:[/\\]/.test(str) || (str.startsWith('/') && !this._isRelativePath(str));
  }

  /**
   * 判断是否为 URL
   */
  _isUrl(str) {
    return /^https?:\/\//i.test(str);
  }

  /**
   * 获取本地图片路径
   */
  getLocalPath(hash) {
    const files = fs.readdirSync(this.uploadDir);
    const file = files.find(f => f.startsWith(hash));
    return file ? path.join(this.uploadDir, file) : null;
  }

  /**
   * 清理过期的上传记录
   */
  async cleanup() {
    const count = await this.db.cleanupExpiredUploads();
    console.log(`🧹 清理了 ${count} 条过期上传记录`);
    return count;
  }
}

module.exports = UploadHandler;
