-- 添加新字段到creat表
ALTER TABLE creat ADD COLUMN callback_url TEXT;
ALTER TABLE creat ADD COLUMN poll_count INTEGER DEFAULT 0;
ALTER TABLE creat ADD COLUMN response_data TEXT;
