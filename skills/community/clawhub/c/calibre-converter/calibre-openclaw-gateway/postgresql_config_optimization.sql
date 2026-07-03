-- PostgreSQL Configuration Optimization for Calibre OpenClaw Server
-- REQUIRES SUPERUSER ACCESS
-- Run as postgres user: sudo -u postgres psql -f postgresql_config_optimization.sql
-- Then restart PostgreSQL: sudo systemctl restart postgresql

-- Based on 15GB RAM system with 18GB database

-- 1. Increase shared_buffers (25% of RAM = ~4GB)
-- Default: 128MB (16384 * 8kB)
ALTER SYSTEM SET shared_buffers = '4GB';

-- 2. Increase effective_cache_size (45% of RAM = ~6.75GB)
-- Default: 4GB (524288 * 8kB)
ALTER SYSTEM SET effective_cache_size = '6.75GB';

-- 3. Increase work_mem for complex queries (64MB per operation)
-- Default: 32MB (4096 * 8kB)
ALTER SYSTEM SET work_mem = '64MB';

-- 4. Increase maintenance_work_mem for maintenance operations (1GB)
-- Default: 512MB (65536 * 8kB)
ALTER SYSTEM SET maintenance_work_mem = '1GB';

-- 5. Increase max_connections for concurrent access
-- Default: 100
ALTER SYSTEM SET max_connections = 200;

-- 6. Improve query planning for SSD storage
ALTER SYSTEM SET random_page_cost = 1.1;  -- Default: 4.0 (HDD assumption)
ALTER SYSTEM SET effective_io_concurrency = 200;  -- Default: 1

-- 7. Enable parallel query processing
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;  -- Default: 2
ALTER SYSTEM SET max_parallel_workers = 8;  -- Default: 8
ALTER SYSTEM SET max_worker_processes = 8;  -- Default: 8

-- After applying changes, reload config:
-- SELECT pg_reload_conf();
-- Or restart: sudo systemctl restart postgresql
