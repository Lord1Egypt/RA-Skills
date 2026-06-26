const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

class Database {
  constructor() {
    this.dbPath = path.join(__dirname, '../../database/works.db');
    this.db = null;
  }

  async init() {
    return new Promise((resolve, reject) => {
      const dbDir = path.dirname(this.dbPath);
      if (!fs.existsSync(dbDir)) {
        fs.mkdirSync(dbDir, { recursive: true });
      }

      // 检查数据库文件是否存在
      const dbExists = fs.existsSync(this.dbPath);

      this.db = new sqlite3.Database(this.dbPath, async (err) => {
        if (err) {
          console.error('数据库连接失败:', err);
          reject(err);
        } else {
          console.log('✅ 数据库连接成功');
          
          // 如果数据库是新创建的，重置迁移版本
          if (!dbExists) {
            const infoPath = path.join(__dirname, '../../database/info.txt');
            if (fs.existsSync(infoPath)) {
              fs.writeFileSync(infoPath, '0');
              console.log('✅ 数据库新创建，重置迁移版本');
            }
          }
          
          await this.runMigrations();
          resolve();
        }
      });
    });
  }

  async runMigrations() {
    const migrationsDir = path.join(__dirname, '../../database');
    const infoPath = path.join(migrationsDir, 'info.txt');
    let currentVersion = 0;

    if (fs.existsSync(infoPath)) {
      currentVersion = parseInt(fs.readFileSync(infoPath, 'utf-8')) || 0;
    }

    const files = fs.readdirSync(migrationsDir)
      .filter(f => f.endsWith('.sql'))
      .sort((a, b) => {
        const numA = parseInt(a);
        const numB = parseInt(b);
        return numA - numB;
      });

    for (const file of files) {
      const version = parseInt(file);
      if (version > currentVersion) {
        const sql = fs.readFileSync(path.join(migrationsDir, file), 'utf-8');
        
        // 分割多条 SQL 语句并逐个执行
        const statements = sql.split(';').filter(s => s.trim());
        for (const statement of statements) {
          if (statement.trim()) {
            await this.run(statement);
          }
        }
        
        console.log(`✅ 执行迁移: ${file}`);
        currentVersion = version;
      }
    }

    fs.writeFileSync(infoPath, currentVersion.toString());
  }

  run(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.run(sql, params, (err) => {
        if (err) reject(err);
        else resolve();
      });
    });
  }

  get(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.get(sql, params, (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  }

  all(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.all(sql, params, (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });
  }

  // 创建任务
  async createWork(data) {
    const sql = `INSERT INTO creat (
      date, state, task_id, prompt, size, quality, cut, path, model, ratio, 
      request_data, callback_url, poll_count, last_request
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;

    const now = Date.now();
    const params = [
      new Date().toISOString(),
      1, // pending
      data.task_id || null,
      data.prompt,
      data.size,
      data.quality,
      data.cut || 1,
      data.path || '',
      data.model,
      data.ratio,
      JSON.stringify(data.request_data || {}),
      data.callback_url || '',
      0,
      now + 60000 // 1分钟后开始轮询
    ];

    return new Promise((resolve, reject) => {
      this.db.run(sql, params, function(err) {
        if (err) reject(err);
        else resolve(this.lastID);
      });
    });
  }

  // 获取所有作品
  async getAllWorks() {
    const sql = `SELECT * FROM creat WHERE state >= 0 ORDER BY date DESC LIMIT 50`;
    return await this.all(sql);
  }

  // 分页获取作品
  async getWorksPaginated(page = 1, pageSize = 30, keyword = '') {
    const offset = (page - 1) * pageSize;
    
    // 构建搜索条件
    let whereClause = 'state >= 0';
    const params = [];
    
    if (keyword) {
      whereClause += ' AND prompt LIKE ?';
      params.push(`%${keyword}%`);
    }
    
    // 获取总数
    const countSql = `SELECT COUNT(*) as total FROM creat WHERE ${whereClause}`;
    const countResult = await this.get(countSql, params);
    const total = countResult?.total || 0;
    
    // 获取分页数据
    const sql = `SELECT * FROM creat WHERE ${whereClause} ORDER BY date DESC LIMIT ? OFFSET ?`;
    params.push(pageSize, offset);
    const works = await this.all(sql, params);
    
    return {
      works,
      page,
      pageSize,
      total,
      totalPages: Math.ceil(total / pageSize)
    };
  }

  // 获取单个作品
  async getWorkById(id) {
    const sql = `SELECT * FROM creat WHERE id = ?`;
    return await this.get(sql, [id]);
  }

  // 更新任务状态
  async updateWorkState(id, state, error) {
    const sql = `UPDATE creat SET state = ?, error = ? WHERE id = ?`;
    await this.run(sql, [state, error || null, id]);
  }

  // 更新任务信息
  async updateWork(id, data) {
    const fields = [];
    const values = [];

    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'object') {
        fields.push(`${key} = ?`);
        values.push(JSON.stringify(value));
      } else {
        fields.push(`${key} = ?`);
        values.push(value);
      }
    }

    values.push(id);
    const sql = `UPDATE creat SET ${fields.join(', ')} WHERE id = ?`;
    await this.run(sql, values);
  }

  // 删除任务
  async deleteWork(id) {
    const sql = `UPDATE creat SET state = -1 WHERE id = ?`;
    await this.run(sql, [id]);
  }

  // 获取待轮询任务
  async getPendingTasks() {
    const sql = `SELECT * FROM creat WHERE state = 1 AND task_id IS NOT NULL AND last_request <= ?`;
    const now = Date.now();
    return await this.all(sql, [now]);
  }

  // 更新轮询信息
  async updatePollInfo(id, pollCount, nextPollTime) {
    const sql = `UPDATE creat SET poll_count = ?, last_request = ? WHERE id = ?`;
    await this.run(sql, [pollCount, nextPollTime, id]);
  }

  // 保存上传记录
  async saveUploadRecord(data) {
    const sql = `INSERT INTO upload (date, state, timeout, url, filename, file_hash)
                 VALUES (?, ?, ?, ?, ?, ?)`;

    const timeout = Date.now() + (24 * 60 * 60 * 1000); // 24小时后超时

    const params = [
      new Date().toISOString(),
      1,
      timeout,
      data.url,
      data.filename,
      data.file_hash
    ];

    return new Promise((resolve, reject) => {
      this.db.run(sql, params, function(err) {
        if (err) reject(err);
        else resolve(this.lastID);
      });
    });
  }

  // 获取上传记录
  async getUploadRecord(fileHash) {
    const sql = `SELECT * FROM upload WHERE file_hash = ? AND timeout > ? AND state = 1`;
    const now = Date.now();
    return await this.get(sql, [fileHash, now]);
  }

  // 清理过期上传记录
  async cleanupExpiredUploads() {
    const sql = `UPDATE upload SET state = 0 WHERE timeout < ? AND state = 1`;
    const now = Date.now();
    return new Promise((resolve, reject) => {
      this.db.run(sql, [now], function(err) {
        if (err) reject(err);
        else resolve(this.changes);
      });
    });
  }
}

module.exports = Database;
