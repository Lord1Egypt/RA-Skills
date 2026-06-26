#!/usr/bin/env python3
"""
DigitalSalesClaw - db.py
MySQL 统一连接管理
"""
import mysql.connector
from mysql.connector import pooling
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent


_POOL = None


def _get_pool():
    global _POOL
    if _POOL is None:
        _POOL = pooling.MySQLConnectionPool(
            pool_name="dsc_main",
            pool_size=10,
            host="localhost",
            port=3306,
            user="ontology",
            password="ontology",
            database="digitalsalesclaw",
            charset="utf8mb4",
            use_unicode=True,
        )
    return _POOL


def get_conn():
    """获取 MySQL 连接（唯一出口）"""
    pool = _get_pool()
    conn = pool.get_connection()
    conn.autocommit = False
    return conn


def close_conn(conn):
    """关闭连接（归还连接池）"""
    try:
        conn.close()
    except Exception:
        pass


def query_all(sql: str, params: tuple = None) -> list:
    """快捷查询所有行"""
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        close_conn(conn)


def query_one(sql: str, params: tuple = None) -> dict:
    """快捷查询单行"""
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        row = cur.fetchone()
        cur.close()
        return row
    finally:
        close_conn(conn)


def execute(sql: str, params: tuple = None) -> int:
    """执行写操作，返回 affected_rows"""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        affected = cur.rowcount
        cur.close()
        return affected
    except Exception:
        conn.rollback()
        raise
    finally:
        close_conn(conn)


def executemany(sql: str, params_list: list) -> int:
    """批量执行"""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.executemany(sql, params_list)
        conn.commit()
        affected = cur.rowcount
        cur.close()
        return affected
    except Exception:
        conn.rollback()
        raise
    finally:
        close_conn(conn)


def test_connection() -> dict:
    """测试 MySQL 连接"""
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT 1 as test, @@hostname as host, @@version as version, @@socket as socket")
        row = cur.fetchone()
        cur.close()
        close_conn(conn)
        return {"status": "ok", "host": row["host"], "version": row["version"], "socket": row["socket"]}
    except Exception as e:
        return {"status": "error", "reason": str(e)}