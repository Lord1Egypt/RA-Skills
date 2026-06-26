#!/usr/bin/env python3
"""Database Enhanced - 更多数据库支持"""

import os


# ==================== Redis支持 ====================
class RedisConn:
    """Redis连接"""
    
    def __init__(self, host="localhost", port=6379, password=None, db=0):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.client = None
        try:
            import redis
            self.client = redis.Redis(host=host, port=port, password=password, db=db, decode_responses=True)
            self.client.ping()
            self.connected = True
        except ImportError:
            self.connected = False
        except:
            self.connected = False
    
    def is_connected(self):
        return self.connected
    
    def get(self, key):
        if self.client:
            return self.client.get(key)
        return None
    
    def set(self, key, value, ex=None):
        if self.client:
            return self.client.set(key, value, ex=ex)
        return None
    
    def delete(self, key):
        if self.client:
            return self.client.delete(key)
        return 0
    
    def exists(self, key):
        if self.client:
            return self.client.exists(key)
        return 0
    
    def expire(self, key, seconds):
        if self.client:
            return self.client.expire(key, seconds)
        return False
    
    def hget(self, name, key):
        if self.client:
            return self.client.hget(name, key)
        return None
    
    def hset(self, name, key, value):
        if self.client:
            return self.client.hset(name, key, value)
        return 0
    
    def hgetall(self, name):
        if self.client:
            return self.client.hgetall(name)
        return {}
    
    def lpush(self, key, *values):
        if self.client:
            return self.client.lpush(key, *values)
        return 0
    
    def rpop(self, key):
        if self.client:
            return self.client.rpop(key)
        return None
    
    def incr(self, key, amount=1):
        if self.client:
            return self.client.incrby(key, amount)
        return None
    
    def keys(self, pattern="*"):
        if self.client:
            return self.client.keys(pattern)
        return []
    
    def flushdb(self):
        if self.client:
            return self.client.flushdb()
        return False
    
    def close(self):
        if self.client:
            self.client.close()


class ConnectionPool:
    """连接池"""
    
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.available = []
        self.in_use = []
    
    def acquire(self):
        if self.available:
            conn = self.available.pop()
            self.in_use.append(conn)
            return conn
        return None
    
    def release(self, conn):
        if conn in self.in_use:
            self.in_use.remove(conn)
            self.available.append(conn)
    
    def close_all(self):
        for conn in self.available + self.in_use:
            try:
                conn.close()
            except:
                pass
        self.available.clear()
        self.in_use.clear()


# ==================== Redis缓存 ====================
class RedisCache:
    """Redis缓存"""
    
    def __init__(self, redis_conn):
        self.redis = redis_conn
    
    def get(self, key):
        import json
        value = self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except:
                return value
        return None
    
    def set(self, key, value, ttl=3600):
        import json
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return self.redis.set(key, value, ex=ttl)
    
    def delete(self, key):
        return self.redis.delete(key)
    
    def clear_pattern(self, pattern):
        keys = self.redis.keys(pattern)
        return self.redis.delete(*keys) if keys else 0


# ==================== 会话管理 ====================
class SessionManager:
    """会话管理"""
    
    def __init__(self, redis_conn):
        self.redis = redis_conn
        self.prefix = "session:"
    
    def create(self, session_id, data, ttl=3600):
        import json
        key = f"{self.prefix}{session_id}"
        self.redis.set(key, json.dumps(data), ex=ttl)
        return session_id
    
    def get(self, session_id):
        import json
        key = f"{self.prefix}{session_id}"
        value = self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except:
                return None
        return None
    
    def update(self, session_id, data, ttl=3600):
        return self.create(session_id, data, ttl)
    
    def delete(self, session_id):
        key = f"{self.prefix}{session_id}"
        return self.redis.delete(key)
    
    def refresh(self, session_id, ttl=3600):
        key = f"{self.prefix}{session_id}"
        return self.redis.expire(key, ttl)


# ==================== 分布式锁 ====================
class DistributedLock:
    """分布式锁"""
    
    def __init__(self, redis_conn, lock_name, timeout=10):
        self.redis = redis_conn
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout
        self.locked = False
    
    def acquire(self, blocking=True, blocking_timeout=5):
        import time
        start = time.time()
        while True:
            result = self.redis.set(self.lock_name, "1", nx=True, ex=self.timeout)
            if result:
                self.locked = True
                return True
            if not blocking:
                return False
            if time.time() - start > blocking_timeout:
                return False
            time.sleep(0.1)
    
    def release(self):
        if self.locked:
            self.redis.delete(self.lock_name)
            self.locked = False
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, *args):
        self.release()


# ==================== 消息队列 ====================
class RedisQueue:
    """Redis消息队列"""
    
    def __init__(self, redis_conn, queue_name):
        self.redis = redis_conn
        self.queue_name = f"queue:{queue_name}"
    
    def push(self, message):
        import json
        if isinstance(message, (dict, list)):
            message = json.dumps(message)
        return self.redis.lpush(self.queue_name, message)
    
    def pop(self, blocking=False, timeout=0):
        if blocking:
            import time
            start = time.time()
            while True:
                result = self.redis.rpop(self.queue_name)
                if result:
                    return result
                if timeout and time.time() - start > timeout:
                    return None
                time.sleep(0.1)
        return self.redis.rpop(self.queue_name)
    
    def size(self):
        return self.redis.client.llen(self.queue_name) if self.redis.client else 0


# ==================== 限流器 ====================
class RateLimiterRedis:
    """基于Redis的限流"""
    
    def __init__(self, redis_conn, key, max_calls, period):
        self.redis = redis_conn
        self.key = f"ratelimit:{key}"
        self.max_calls = max_calls
        self.period = period
    
    def allow(self):
        import time
        now = time.time()
        key_with_time = f"{self.key}:{int(now)}"
        
        count = self.redis.incr(key_with_time)
        if count == 1:
            self.redis.expire(key_with_time, self.period)
        
        return count <= self.max_calls


if __name__ == "__main__":
    print("Database Enhanced loaded")