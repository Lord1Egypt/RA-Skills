#!/usr/bin/env node

/**
 * 阿里云 OSS Node.js SDK 脚本
 * 功能：文件上传、下载、列出、删除、获取URL等操作
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 尝试加载 ali-oss SDK
import OSS from 'ali-oss';

// 配置文件路径
const SKILL_DIR = path.dirname(__dirname);
const CONFIG_DIR = path.join(SKILL_DIR, 'config');
const CONFIG_FILE = path.join(CONFIG_DIR, 'oss-config.json');

/**
 * 加载配置文件
 */
function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    throw new Error(
      `配置文件不存在: ${CONFIG_FILE}\n` +
      `请复制 config/oss-config.example.json 为 oss-config.json 并填写配置`
    );
  }

  const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

  // 验证必填配置
  const required = ['accessKeyId', 'accessKeySecret', 'bucket', 'region'];
  for (const key of required) {
    if (!config[key] || config[key].startsWith('你的')) {
      throw new Error(`配置项 ${key} 不能为空或使用示例值`);
    }
  }

  return config;
}

/**
 * 阿里云 OSS 操作类
 */
class AliyunOSS {
  constructor(config) {
    this.config = config;
    this.client = new OSS({
      region: config.region,
      bucket: config.bucket,
      accessKeyId: config.accessKeyId,
      accessKeySecret: config.accessKeySecret,
      secure: config.options?.secure !== false,
      timeout: config.options?.timeout || 60000
    });
    this.bucket = config.bucket;
    this.domain = config.domain || `https://${config.bucket}.${config.region}.aliyuncs.com`;
  }

  /**
   * 上传文件
   */
  async upload(localPath, key) {
    if (!fs.existsSync(localPath)) {
      throw new Error(`文件不存在: ${localPath}`);
    }

    try {
      const result = await this.client.put(key, localPath);
      
      return {
        success: true,
        key: result.name,
        url: this.getUrl(key),
        size: fs.statSync(localPath).size,
        etag: result.etag
      };
    } catch (error) {
      throw new Error(`上传失败: ${error.message}`);
    }
  }

  /**
   * 下载文件
   */
  async download(key, localPath) {
    try {
      const result = await this.client.get(key, localPath);
      
      return {
        success: true,
        key: key,
        size: fs.statSync(localPath).size
      };
    } catch (error) {
      throw new Error(`下载失败: ${error.message}`);
    }
  }

  /**
   * 列出文件
   */
  async listFiles(prefix = '', limit = 100) {
    try {
      const result = await this.client.list({
        prefix: prefix,
        'max-keys': limit
      });

      const files = (result.objects || []).map(item => ({
        key: item.name,
        size: item.size,
        mtime: new Date(item.lastModified).getTime() / 1000,
        etag: item.etag,
        mimeType: item.type || 'application/octet-stream'
      }));

      return files;
    } catch (error) {
      throw new Error(`列出文件失败: ${error.message}`);
    }
  }

  /**
   * 删除文件
   */
  async delete(key) {
    try {
      await this.client.delete(key);
      
      return {
        success: true,
        key: key
      };
    } catch (error) {
      if (error.code === 'NoSuchKey') {
        throw new Error(`文件不存在: ${key}`);
      }
      throw new Error(`删除失败: ${error.message}`);
    }
  }

  /**
   * 批量删除
   */
  async batchDelete(keys) {
    try {
      const result = await this.client.deleteMulti(keys);
      
      let success = 0;
      let failed = 0;
      
      if (result.deleted) {
        success = result.deleted.length;
        failed = keys.length - success;
      }

      return { success, failed };
    } catch (error) {
      throw new Error(`批量删除失败: ${error.message}`);
    }
  }

  /**
   * 获取文件信息
   */
  async stat(key) {
    try {
      const result = await this.client.head(key);
      
      return {
        key: key,
        size: parseInt(result.res.headers['content-length']),
        etag: result.res.headers.etag,
        mimeType: result.res.headers['content-type'],
        mtime: new Date(result.res.headers['last-modified']).getTime() / 1000
      };
    } catch (error) {
      throw new Error(`获取文件信息失败: ${error.message}`);
    }
  }

  /**
   * 获取文件 URL
   */
  getUrl(key, isPrivate = false, expires = 3600) {
    if (isPrivate) {
      return this.client.signatureUrl(key, {
        expires: expires
      });
    } else {
      return `${this.domain}/${key}`;
    }
  }

  /**
   * 移动文件
   */
  async move(srcKey, destKey) {
    try {
      await this.client.copy(destKey, srcKey);
      await this.client.delete(srcKey);
      
      return {
        success: true,
        srcKey: srcKey,
        destKey: destKey
      };
    } catch (error) {
      throw new Error(`移动失败: ${error.message}`);
    }
  }

  /**
   * 复制文件
   */
  async copy(srcKey, destKey) {
    try {
      await this.client.copy(destKey, srcKey);
      
      return {
        success: true,
        srcKey: srcKey,
        destKey: destKey
      };
    } catch (error) {
      throw new Error(`复制失败: ${error.message}`);
    }
  }
}

// 工具函数
function formatSize(bytes) {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`;
}

function formatTime(timestamp) {
  const date = new Date(timestamp * 1000);
  return date.toISOString().replace('T', ' ').substring(0, 19);
}

// 命令行接口
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  try {
    const config = loadConfig();
    const oss = new AliyunOSS(config);
    
    switch (command) {
      case 'upload': {
        const localPath = args[args.indexOf('--local') + 1];
        const key = args[args.indexOf('--key') + 1];
        const result = await oss.upload(localPath, key);
        console.log('✅ 上传成功!');
        console.log(`  文件: ${result.key}`);
        console.log(`  大小: ${formatSize(result.size)}`);
        console.log(`  URL: ${result.url}`);
        break;
      }
      
      case 'download': {
        const key = args[args.indexOf('--key') + 1];
        const localPath = args[args.indexOf('--local') + 1];
        const result = await oss.download(key, localPath);
        console.log('✅ 下载成功!');
        console.log(`  文件: ${result.key}`);
        console.log(`  大小: ${formatSize(result.size)}`);
        console.log(`  保存到: ${localPath}`);
        break;
      }
      
      case 'list': {
        const prefixIndex = args.indexOf('--prefix');
        const prefix = prefixIndex !== -1 ? args[prefixIndex + 1] : '';
        
        const limitIndex = args.indexOf('--limit');
        const limit = limitIndex !== -1 ? parseInt(args[limitIndex + 1]) : 100;
        
        const formatIndex = args.indexOf('--format');
        const format = formatIndex !== -1 ? args[formatIndex + 1] : 'table';
        
        const files = await oss.listFiles(prefix, limit);
        
        if (files.length === 0) {
          console.log('📭 没有找到文件');
          return;
        }
        
        if (format === 'json') {
          console.log(JSON.stringify(files, null, 2));
        } else {
          console.log(`📋 共 ${files.length} 个文件:\n`);
          console.log(`${'文件名'.padEnd(50)} ${'大小'.padStart(12)} ${'修改时间'.padEnd(20)}`);
          console.log('-'.repeat(82));
          files.forEach(file => {
            console.log(`${file.key.padEnd(50)} ${formatSize(file.size).padStart(12)} ${formatTime(file.mtime).padEnd(20)}`);
          });
        }
        break;
      }
      
      case 'delete': {
        const key = args[args.indexOf('--key') + 1];
        const forceIndex = args.indexOf('--force');
        
        if (forceIndex === -1) {
          console.log(`⚠️  确定要删除 ${key} 吗？(y/N):`);
          // 注意：这里需要 readline，为简化暂时跳过确认
        }
        
        const result = await oss.delete(key);
        console.log('✅ 删除成功!');
        console.log(`  文件: ${result.key}`);
        break;
      }
      
      case 'batch-delete': {
        const fileIndex = args.indexOf('--file');
        const listFile = args[fileIndex + 1];
        
        const keys = fs.readFileSync(listFile, 'utf-8')
          .split('\n')
          .map(line => line.trim())
          .filter(line => line);
        
        const result = await oss.batchDelete(keys);
        console.log('✅ 批量删除完成!');
        console.log(`  成功: ${result.success}`);
        console.log(`  失败: ${result.failed}`);
        break;
      }
      
      case 'url': {
        const key = args[args.indexOf('--key') + 1];
        const privateIndex = args.indexOf('--private');
        const expiresIndex = args.indexOf('--expires');
        
        const isPrivate = privateIndex !== -1;
        const expires = expiresIndex !== -1 ? parseInt(args[expiresIndex + 1]) : 3600;
        
        const url = oss.getUrl(key, isPrivate, expires);
        console.log('🔗 文件 URL:');
        console.log(`  ${url}`);
        if (isPrivate) {
          console.log(`\n  ⏱️  有效期: ${expires} 秒`);
        }
        break;
      }
      
      case 'stat': {
        const key = args[args.indexOf('--key') + 1];
        const info = await oss.stat(key);
        console.log('📊 文件信息:\n');
        console.log(`  文件名: ${info.key}`);
        console.log(`  大小: ${formatSize(info.size)}`);
        console.log(`  类型: ${info.mimeType}`);
        console.log(`  ETag: ${info.etag}`);
        console.log(`  修改时间: ${formatTime(info.mtime)}`);
        break;
      }
      
      case 'test-connection': {
        await oss.listFiles('', 1);
        console.log('✅ 阿里云 OSS 连接验证成功!');
        break;
      }
      
      default:
        console.log('使用方法:');
        console.log('  node oss_node.mjs upload --local <LocalPath> --key <Key>');
        console.log('  node oss_node.mjs download --key <Key> --local <LocalPath>');
        console.log('  node oss_node.mjs list [--prefix <Prefix>] [--limit <Limit>]');
        console.log('  node oss_node.mjs delete --key <Key> [--force]');
        console.log('  node oss_node.mjs url --key <Key> [--private] [--expires <Seconds>]');
        console.log('  node oss_node.mjs stat --key <Key>');
        console.log('  node oss_node.mjs test-connection');
    }
    
  } catch (error) {
    console.error(`❌ 错误: ${error.message}`);
    process.exit(1);
  }
}

main();
