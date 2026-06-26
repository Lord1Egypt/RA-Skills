-- 文件传输表
CREATE TABLE file_transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT UNIQUE NOT NULL,           -- UUID，唯一标识文件传输
    filename TEXT NOT NULL,                  -- 原始文件名
    size INTEGER NOT NULL,                   -- 文件大小（字节）
    md5 TEXT NOT NULL,                       -- 文件MD5校验值
    chunk_size INTEGER DEFAULT 10485760,     -- 分片大小（默认10MB）
    chunks_total INTEGER NOT NULL,           -- 总分片数
    chunks_received INTEGER DEFAULT 0,       -- 已接收分片数
    
    -- 传输状态
    status TEXT DEFAULT 'pending',           -- pending, transferring, completed, failed, timeout
    
    -- 参与方
    from_portal TEXT NOT NULL,               -- 发送方 Portal URL
    to_portal TEXT NOT NULL,                 -- 接收方 Portal URL
    from_contact_id INTEGER,                 -- 发送方联系人ID（可选）
    to_contact_id INTEGER,                   -- 接收方联系人ID（可选）
    
    -- 确认机制
    receiver_confirmed BOOLEAN DEFAULT FALSE, -- 接收方是否确认接收
    confirmed_at TIMESTAMP,                   -- 确认时间
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,                   -- 完成时间
    
    -- 清理标记
    should_cleanup BOOLEAN DEFAULT FALSE,    -- 是否需要清理
    cleanup_after TIMESTAMP                  -- 建议清理时间
);

-- 文件分片表
CREATE TABLE file_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT NOT NULL,                   -- 关联 file_transfers.file_id
    chunk_index INTEGER NOT NULL,            -- 分片索引（从0开始）
    chunk_size INTEGER NOT NULL,             -- 分片实际大小
    chunk_md5 TEXT NOT NULL,                 -- 分片MD5校验值
    data BLOB NOT NULL,                      -- 分片二进制数据
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 联合唯一约束：一个文件的分片索引唯一
    UNIQUE(file_id, chunk_index),
    
    -- 外键约束
    FOREIGN KEY (file_id) REFERENCES file_transfers(file_id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_file_transfers_status ON file_transfers(status);
CREATE INDEX idx_file_transfers_to_portal ON file_transfers(to_portal);
CREATE INDEX idx_file_transfers_cleanup ON file_transfers(should_cleanup, cleanup_after);
CREATE INDEX idx_file_chunks_file_id ON file_chunks(file_id);

-- 触发器：自动更新 updated_at
CREATE TRIGGER update_file_transfers_timestamp 
AFTER UPDATE ON file_transfers
BEGIN
    UPDATE file_transfers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- 触发器：分片接收计数
CREATE TRIGGER update_chunks_received
AFTER INSERT ON file_chunks
BEGIN
    UPDATE file_transfers 
    SET chunks_received = chunks_received + 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE file_id = NEW.file_id;
END;

-- 触发器：自动设置清理时间（传输完成）
CREATE TRIGGER set_cleanup_after_completed
AFTER UPDATE OF status ON file_transfers
WHEN NEW.status = 'completed'
BEGIN
    UPDATE file_transfers 
    SET should_cleanup = TRUE,
        cleanup_after = datetime('now', '+7 days'),
        completed_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- 触发器：自动设置清理时间（传输中断）
CREATE TRIGGER set_cleanup_after_failed
AFTER UPDATE OF status ON file_transfers
WHEN NEW.status IN ('failed', 'timeout')
BEGIN
    UPDATE file_transfers 
    SET should_cleanup = TRUE,
        cleanup_after = datetime('now', '+14 days')
    WHERE id = NEW.id;
END;