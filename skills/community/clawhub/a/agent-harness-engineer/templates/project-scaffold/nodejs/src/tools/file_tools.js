/**
 * ============================================
 * 类型: 核心框架
 * 模块: tools.file_tools
 * 说明: 文件操作工具实现
 * 修改建议: 如需扩展，添加新的工具方法并注册
 * ============================================

const fs = require('fs');
const path = require('path');

class FileTools {
  constructor() {
    this.readFileSchema = {
      type: 'object',
      properties: {
        path: { type: 'string', description: '文件路径' },
        offset: { type: 'integer', description: '起始行号（1-based）', minimum: 1 },
        limit: { type: 'integer', description: '最大读取行数', minimum: 1, maximum: 2000 }
      },
      required: ['path']
    };
    
    this.writeFileSchema = {
      type: 'object',
      properties: {
        path: { type: 'string', description: '文件路径' },
        content: { type: 'string', description: '文件内容' }
      },
      required: ['path', 'content']
    };
    
    this.listFilesSchema = {
      type: 'object',
      properties: {
        path: { type: 'string', description: '目录路径' },
        recursive: { type: 'boolean', description: '是否递归' },
        pattern: { type: 'string', description: '文件匹配模式' }
      },
      required: ['path']
    };
  }
  
  readFile(inputData) {
    const filePath = inputData.path;
    const offset = inputData.offset || 1;
    const limit = inputData.limit || 2000;
    
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.split('\n');
      const start = Math.max(0, offset - 1);
      const end = Math.min(start + limit, lines.length);
      return lines.slice(start, end).join('\n');
    } catch (error) {
      return `Error: ${error.message}`;
    }
  }
  
  writeFile(inputData) {
    const filePath = inputData.path;
    const content = inputData.content;
    
    try {
      const dir = path.dirname(filePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(filePath, content, 'utf-8');
      return `Successfully wrote to ${filePath}`;
    } catch (error) {
      return `Error: ${error.message}`;
    }
  }
  
  listFiles(inputData) {
    const dirPath = inputData.path;
    const recursive = inputData.recursive || false;
    const pattern = inputData.pattern;
    
    try {
      if (recursive) {
        const results = [];
        const walk = (dir) => {
          const items = fs.readdirSync(dir);
          for (const item of items) {
            const fullPath = path.join(dir, item);
            const stat = fs.statSync(fullPath);
            if (stat.isDirectory()) {
              walk(fullPath);
            } else {
              if (!pattern || item.match(pattern)) {
                results.push(fullPath);
              }
            }
          }
        };
        walk(dirPath);
        return results;
      } else {
        return fs.readdirSync(dirPath).filter(item => {
          if (!pattern) return true;
          return item.match(pattern);
        });
      }
    } catch (error) {
      return [`Error: ${error.message}`];
    }
  }
}

module.exports = { FileTools };
