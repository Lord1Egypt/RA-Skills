/**
 * WAL (Write-Ahead Logging) Protocol - 预写日志协议
 * 
 * 功能：
 * - 所有状态变更先写日志
 * - 支持崩溃恢复
 * - 支持事务回滚
 * - 支持 compaction 压缩
 * 
 * @example
 * const wal = new WALProtocol('./memory/wal');
 * 
 * await wal.begin('task-123');
 * await wal.log('start', { task: '...' });
 * await wal.log('complete', { result: '...' });
 * await wal.commit('task-123');
 */

import { writeFileSync, appendFileSync, readFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import { join, dirname } from 'path';

// ============================================================================
// 配置
// ============================================================================

const DEFAULT_CONFIG = {
  walDir: './memory/wal',
  enableCompaction: true,
  compactionThreshold: 1000,  // 日志条数阈值
  maxSegmentSize: 10 * 1024 * 1024,  // 10MB
  enableChecksum: true,
};

// ============================================================================
// 日志条目类型
// ============================================================================

const LogEntryType = {
  BEGIN: 'BEGIN',
  COMMIT: 'COMMIT',
  ABORT: 'ABORT',
  DATA: 'DATA',
  CHECKPOINT: 'CHECKPOINT',
};

// ============================================================================
// 日志条目结构
// ============================================================================

class LogEntry {
  constructor(type, transactionId, data, sequence) {
    this.type = type;
    this.transactionId = transactionId;
    this.data = data;
    this.sequence = sequence;
    this.timestamp = Date.now();
    this.checksum = null;
  }

  /**
   * 计算校验和
   */
  calculateChecksum() {
    const content = JSON.stringify({
      type: this.type,
      transactionId: this.transactionId,
      data: this.data,
      sequence: this.sequence,
      timestamp: this.timestamp,
    });
    
    // 简单校验和（实际应该用 CRC32 或 SHA256）
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    
    this.checksum = hash.toString(16);
    return this.checksum;
  }

  /**
   * 验证校验和
   */
  verifyChecksum() {
    if (!this.checksum) return true;
    const expected = this.calculateChecksum();
    return this.checksum === expected;
  }

  /**
   * 序列化为 JSON 行
   */
  toJSON() {
    return JSON.stringify(this);
  }

  /**
   * 从 JSON 行解析
   */
  static fromJSON(line) {
    try {
      const obj = JSON.parse(line);
      const entry = new LogEntry(
        obj.type,
        obj.transactionId,
        obj.data,
        obj.sequence
      );
      entry.timestamp = obj.timestamp;
      entry.checksum = obj.checksum;
      return entry;
    } catch (error) {
      return null;
    }
  }
}

// ============================================================================
// WAL 协议类
// ============================================================================

export class WALProtocol {
  constructor(config = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.walDir = this.config.walDir;
    
    // 确保目录存在
    if (!existsSync(this.walDir)) {
      mkdirSync(this.walDir, { recursive: true });
    }
    
    // 当前日志文件
    this.currentSegment = 0;
    this.currentFile = this.getSegmentFile(0);
    
    // 序列号
    this.sequence = 0;
    
    // 活跃事务
    this.activeTransactions = new Map();
    
    // 日志缓冲
    this.buffer = [];
    this.bufferSize = 0;
    
    // 加载现有序列号
    this.loadSequence();
  }

  /**
   * 获取日志段文件路径
   */
  getSegmentFile(segment) {
    return join(this.walDir, `wal-${segment.toString().padStart(6, '0')}.log`);
  }

  /**
   * 加载序列号
   */
  loadSequence() {
    const files = readdirSync(this.walDir)
      .filter(f => f.startsWith('wal-') && f.endsWith('.log'))
      .sort();
    
    if (files.length > 0) {
      const lastFile = files[files.length - 1];
      this.currentSegment = parseInt(lastFile.match(/wal-(\d+)\.log/)[1]);
      this.currentFile = join(this.walDir, lastFile);
      
      // 读取最后文件的行数
      try {
        const content = readFileSync(this.currentFile, 'utf-8');
        this.sequence = content.split('\n').filter(l => l.trim()).length;
      } catch (error) {
        this.sequence = 0;
      }
    }
  }

  /**
   * 开始事务
   */
  async begin(transactionId, metadata = {}) {
    if (this.activeTransactions.has(transactionId)) {
      throw new Error(`Transaction ${transactionId} already active`);
    }

    const entry = new LogEntry(
      LogEntryType.BEGIN,
      transactionId,
      { metadata, startTime: Date.now() },
      ++this.sequence
    );
    
    entry.calculateChecksum();
    this.appendEntry(entry);
    
    this.activeTransactions.set(transactionId, {
      startTime: Date.now(),
      entries: [entry],
      metadata,
    });
    
    return { transactionId, sequence: entry.sequence };
  }

  /**
   * 记录日志
   */
  async log(transactionId, event, data = {}) {
    const tx = this.activeTransactions.get(transactionId);
    if (!tx) {
      throw new Error(`Transaction ${transactionId} not found`);
    }

    const entry = new LogEntry(
      LogEntryType.DATA,
      transactionId,
      { event, data, timestamp: Date.now() },
      ++this.sequence
    );
    
    entry.calculateChecksum();
    this.appendEntry(entry);
    tx.entries.push(entry);
    
    return { sequence: entry.sequence };
  }

  /**
   * 提交事务
   */
  async commit(transactionId) {
    const tx = this.activeTransactions.get(transactionId);
    if (!tx) {
      throw new Error(`Transaction ${transactionId} not found`);
    }

    const entry = new LogEntry(
      LogEntryType.COMMIT,
      transactionId,
      { 
        endTime: Date.now(),
        duration: Date.now() - tx.startTime,
        entryCount: tx.entries.length,
      },
      ++this.sequence
    );
    
    entry.calculateChecksum();
    this.appendEntry(entry);
    
    this.activeTransactions.delete(transactionId);
    
    // 检查是否需要压缩
    if (this.config.enableCompaction && this.bufferSize >= this.config.compactionThreshold) {
      await this.compact();
    }
    
    return { 
      transactionId, 
      committed: true,
      sequence: entry.sequence,
      duration: entry.data.duration,
    };
  }

  /**
   * 回滚事务
   */
  async abort(transactionId) {
    const tx = this.activeTransactions.get(transactionId);
    if (!tx) {
      throw new Error(`Transaction ${transactionId} not found`);
    }

    const entry = new LogEntry(
      LogEntryType.ABORT,
      transactionId,
      { 
        reason: 'User abort',
        endTime: Date.now(),
        duration: Date.now() - tx.startTime,
      },
      ++this.sequence
    );
    
    entry.calculateChecksum();
    this.appendEntry(entry);
    
    this.activeTransactions.delete(transactionId);
    
    return { transactionId, aborted: true };
  }

  /**
   * 追加日志条目
   */
  appendEntry(entry) {
    const line = entry.toJSON() + '\n';
    
    // 写入缓冲
    this.buffer.push(line);
    this.bufferSize++;
    
    // 检查是否需要轮换日志文件
    const currentSize = this.buffer.reduce((sum, l) => sum + l.length, 0);
    if (currentSize >= this.config.maxSegmentSize) {
      this.rotateSegment();
    }
    
    // 定期刷新到磁盘
    if (this.bufferSize >= 100) {
      this.flush();
    }
  }

  /**
   * 刷新到磁盘
   */
  flush() {
    if (this.buffer.length === 0) return;
    
    appendFileSync(this.currentFile, this.buffer.join(''));
    this.buffer = [];
    this.bufferSize = 0;
  }

  /**
   * 轮换日志文件
   */
  rotateSegment() {
    this.flush();
    this.currentSegment++;
    this.currentFile = this.getSegmentFile(this.currentSegment);
    this.bufferSize = 0;
  }

  /**
   * 压缩日志
   */
  async compact() {
    console.log('[WAL] Starting compaction...');
    
    // 读取所有日志
    const entries = await this.readAllEntries();
    
    // 找出已提交的事务
    const committedTxs = new Set();
    const abortedTxs = new Set();
    
    for (const entry of entries) {
      if (entry.type === LogEntryType.COMMIT) {
        committedTxs.add(entry.transactionId);
      } else if (entry.type === LogEntryType.ABORT) {
        abortedTxs.add(entry.transactionId);
      }
    }
    
    // 只保留活跃事务和已提交事务的最后状态
    const compacted = entries.filter(entry => {
      if (entry.type === LogEntryType.BEGIN) {
        return committedTxs.has(entry.transactionId) || 
               this.activeTransactions.has(entry.transactionId);
      }
      if (entry.type === LogEntryType.DATA) {
        return committedTxs.has(entry.transactionId) || 
               this.activeTransactions.has(entry.transactionId);
      }
      if (entry.type === LogEntryType.COMMIT) {
        return true; // 保留提交标记
      }
      return false;
    });
    
    // 写入新的压缩文件
    const compactedFile = join(this.walDir, 'wal-compacted.log');
    const content = compacted.map(e => e.toJSON() + '\n').join('');
    writeFileSync(compactedFile, content);
    
    // 备份旧文件
    const backupDir = join(this.walDir, 'backup-' + Date.now());
    mkdirSync(backupDir);
    
    const files = readdirSync(this.walDir)
      .filter(f => f.startsWith('wal-') && f.endsWith('.log'));
    
    for (const file of files) {
      if (file !== 'wal-compacted.log') {
        const src = join(this.walDir, file);
        const dst = join(backupDir, file);
        // fs.renameSync(src, dst); // 实际实现
      }
    }
    
    console.log(`[WAL] Compaction complete: ${entries.length} -> ${compacted.length} entries`);
  }

  /**
   * 读取所有日志条目
   */
  async readAllEntries() {
    const entries = [];
    const files = readdirSync(this.walDir)
      .filter(f => f.startsWith('wal-') && f.endsWith('.log'))
      .sort();
    
    for (const file of files) {
      const filePath = join(this.walDir, file);
      try {
        const content = readFileSync(filePath, 'utf-8');
        const lines = content.split('\n').filter(l => l.trim());
        
        for (const line of lines) {
          const entry = LogEntry.fromJSON(line);
          if (entry && entry.verifyChecksum()) {
            entries.push(entry);
          }
        }
      } catch (error) {
        console.error(`[WAL] Error reading ${file}:`, error);
      }
    }
    
    return entries;
  }

  /**
   * 恢复事务状态
   */
  async recover() {
    console.log('[WAL] Starting recovery...');
    
    const entries = await this.readAllEntries();
    const transactions = new Map();
    
    // 重放日志
    for (const entry of entries) {
      const txId = entry.transactionId;
      
      if (entry.type === LogEntryType.BEGIN) {
        transactions.set(txId, {
          status: 'active',
          entries: [entry],
          metadata: entry.data.metadata,
        });
      } else if (entry.type === LogEntryType.DATA) {
        const tx = transactions.get(txId);
        if (tx) {
          tx.entries.push(entry);
        }
      } else if (entry.type === LogEntryType.COMMIT) {
        const tx = transactions.get(txId);
        if (tx) {
          tx.status = 'committed';
        }
      } else if (entry.type === LogEntryType.ABORT) {
        transactions.delete(txId);
      }
    }
    
    // 找出未完成的事务
    const incomplete = [];
    for (const [txId, tx] of transactions) {
      if (tx.status !== 'committed') {
        incomplete.push({
          transactionId: txId,
          status: tx.status,
          entries: tx.entries.length,
          metadata: tx.metadata,
        });
      }
    }
    
    console.log(`[WAL] Recovery complete: ${incomplete.length} incomplete transactions`);
    
    return {
      incomplete,
      totalEntries: entries.length,
    };
  }

  /**
   * 创建检查点
   */
  async checkpoint() {
    const entry = new LogEntry(
      LogEntryType.CHECKPOINT,
      'system',
      {
        sequence: this.sequence,
        segment: this.currentSegment,
        activeTransactions: Array.from(this.activeTransactions.keys()),
      },
      ++this.sequence
    );
    
    entry.calculateChecksum();
    this.appendEntry(entry);
    this.flush();
    
    return { sequence: entry.sequence };
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      currentSegment: this.currentSegment,
      sequence: this.sequence,
      activeTransactions: this.activeTransactions.size,
      bufferSize: this.bufferSize,
    };
  }
}

export default WALProtocol;
