-- 创建任务表
CREATE TABLE IF NOT EXISTS creat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    state INTEGER DEFAULT 1,
    task_id TEXT,
    prompt TEXT,
    size TEXT,
    quality TEXT,
    task_response TEXT,
    task_times INTEGER DEFAULT 0,
    cut INTEGER DEFAULT 1,
    path TEXT,
    filename TEXT,
    ext TEXT,
    error TEXT,
    last_request INTEGER,
    model TEXT,
    ratio TEXT,
    request_data TEXT,
    respond TEXT
);

-- 创建上传表
CREATE TABLE IF NOT EXISTS upload (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    state INTEGER DEFAULT 1,
    timeout INTEGER,
    url TEXT,
    filename TEXT,
    file_hash TEXT
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_creat_state ON creat(state);
CREATE INDEX IF NOT EXISTS idx_creat_task_id ON creat(task_id);
CREATE INDEX IF NOT EXISTS idx_upload_timeout ON upload(timeout);
CREATE INDEX IF NOT EXISTS idx_upload_file_hash ON upload(file_hash);
