-- PostgreSQL Optimization for Calibre OpenClaw Server
-- Based on 15GB RAM system with 18GB database

-- 1. Increase shared_buffers (25% of RAM = ~4GB)
ALTER SYSTEM SET shared_buffers = '4GB';

-- 2. Increase effective_cache_size (75% of RAM = ~12GB)
ALTER SYSTEM SET effective_cache_size = '12GB';

-- 3. Increase work_mem for complex queries (64MB per operation)
ALTER SYSTEM SET work_mem = '64MB';

-- 4. Increase maintenance_work_mem for maintenance operations (1GB)
ALTER SYSTEM SET maintenance_work_mem = '1GB';

-- 5. Increase max_connections for concurrent access
ALTER SYSTEM SET max_connections = 200;

-- 6. Improve query planning
ALTER SYSTEM SET random_page_cost = 1.1;  -- SSD assumption
ALTER SYSTEM SET effective_io_concurrency = 200;

-- 7. Enable parallel query processing
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
ALTER SYSTEM SET max_parallel_workers = 8;
ALTER SYSTEM SET max_worker_processes = 8;

-- 8. Add partial index for faster COUNT queries on book_chunks
-- This index only covers rows with embeddings, making COUNT(* WHERE embedding IS NOT NULL) much faster
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_book_chunks_embedding_exists 
ON book_chunks (book_id) 
WHERE embedding IS NOT NULL;

-- 9. Add index for books.created_at for activity queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_books_created_at 
ON books (created_at);

-- 10. Add index for processing_queue status queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_processing_queue_status 
ON processing_queue (status);

-- 11. Add index for download_queue status queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_download_queue_status 
ON download_queue (status);

-- Note: Changes require PostgreSQL restart to take effect
-- Run: sudo systemctl restart postgresql
