#!/usr/bin/env python3
"""
Database Operations Tool
SQLite/MySQL数据库操作: 查询/更新/备份
"""

import os
import sqlite3
import json
import shutil
from typing import Union, List, Dict, Any, Optional, Tuple
from datetime import datetime
from contextlib import contextmanager


class DatabaseOps:
    """数据库操作类"""
    
    def __init__(self, db_path: str = None, db_type: str = 'sqlite'):
        self.db_path = db_path
        self.db_type = db_type
        self.conn = None
        
        if db_path:
            self.connect()
    
    def connect(self):
        """连接数据库"""
        if self.db_type == 'sqlite':
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        # MySQL support can be added later
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    @contextmanager
    def get_cursor(self):
        """获取游标"""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    # ============== 查询 ==============
    def execute(self, sql: str, params: tuple = None) -> List[Dict]:
        """执行SQL查询"""
        with self.get_cursor() as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            # 获取列名
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            
            # 获取结果
            rows = cursor.fetchall()
            
            # 转为字典
            result = []
            for row in rows:
                if isinstance(row, sqlite3.Row):
                    result.append(dict(row))
                else:
                    result.append(dict(zip(columns, row)))
            
            return result
    
    def query(self, sql: str, params: tuple = None) -> List[Dict]:
        """查询别名"""
        return self.execute(sql, params)
    
    def fetch_one(self, sql: str, params: tuple = None) -> Optional[Dict]:
        """获取单条记录"""
        results = self.execute(sql, params)
        return results[0] if results else None
    
    def fetch_value(self, sql: str, params: tuple = None) -> Any:
        """获取单个值"""
        row = self.fetch_one(sql, params)
        if row:
            return list(row.values())[0]
        return None
    
    # ============== 插入/更新/删除 ==============
    def insert(self, table: str, data: Dict) -> int:
        """插入数据"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        
        with self.get_cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            return cursor.lastrowid
    
    def insert_many(self, table: str, rows: List[Dict]) -> int:
        """批量插入"""
        if not rows:
            return 0
        
        columns = ', '.join(rows[0].keys())
        placeholders = ', '.join(['?' for _ in rows[0]])
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        
        values = [tuple(row.values()) for row in rows]
        
        with self.get_cursor() as cursor:
            cursor.executemany(sql, values)
            return cursor.rowcount
    
    def update(self, table: str, data: Dict, where: str, 
               params: tuple = None) -> int:
        """更新数据"""
        set_clause = ', '.join([f'{k} = ?' for k in data.keys()])
        sql = f'UPDATE {table} SET {set_clause} WHERE {where}'
        
        values = tuple(data.values()) + (params or ())
        
        with self.get_cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.rowcount
    
    def delete(self, table: str, where: str, params: tuple = None) -> int:
        """删除数据"""
        sql = f'DELETE FROM {table} WHERE {where}'
        
        with self.get_cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.rowcount
    
    # ============== 表结构 ==============
    def get_tables(self) -> List[str]:
        """获取所有表"""
        if self.db_type == 'sqlite':
            sql = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        else:
            sql = "SHOW TABLES"
        
        results = self.execute(sql)
        return [list(r.values())[0] for r in results]
    
    def get_table_info(self, table: str) -> List[Dict]:
        """获取表结构"""
        if self.db_type == 'sqlite':
            sql = f"PRAGMA table_info({table})"
        else:
            sql = f"DESCRIBE {table}"
        
        return self.execute(sql)
    
    def get_columns(self, table: str) -> List[str]:
        """获取列名"""
        info = self.get_table_info(table)
        if self.db_type == 'sqlite':
            return [r['name'] for r in info]
        else:
            return [r['Field'] for r in info]
    
    # ============== 统计 ==============
    def count(self, table: str, where: str = None) -> int:
        """统计行数"""
        sql = f'SELECT COUNT(*) as cnt FROM {table}'
        if where:
            sql += f' WHERE {where}'
        
        return self.fetch_value(sql) or 0
    
    def stats(self, table: str) -> Dict:
        """表统计信息"""
        info = self.get_table_info(table)
        row_count = self.count(table)
        
        return {
            'table': table,
            'columns': len(info),
            'rows': row_count,
            'structure': info
        }
    
    # ============== 备份 ==============
    def backup(self, backup_path: str = None) -> str:
        """备份数据库"""
        if self.db_type != 'sqlite':
            raise NotImplementedError('Only SQLite backup supported')
        
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = os.path.splitext(os.path.basename(self.db_path))[0]
            backup_path = f'{name}_{timestamp}.db'
        
        self.close()
        shutil.copy2(self.db_path, backup_path)
        self.connect()
        
        return backup_path
    
    # ============== 执行脚本 ==============
    def execute_script(self, script: str):
        """执行SQL脚本"""
        with self.get_cursor() as cursor:
            cursor.executescript(script)
    
    # ============== 事务 ==============
    def begin(self):
        """开始事务"""
        self.conn.execute('BEGIN')
    
    def commit(self):
        """提交事务"""
        self.conn.commit()
    
    def rollback(self):
        """回滚事务"""
        self.conn.rollback()
    
    # ============== 便捷方法 ==============
    @staticmethod
    def from_path(db_path: str) -> 'DatabaseOps':
        """从路径创建数据库操作对象"""
        return DatabaseOps(db_path)


# ============== SQLite 快速操作 ==============
def sqlite_query(db_path: str, sql: str, params: tuple = None) -> List[Dict]:
    """快速SQLite查询"""
    with DatabaseOps(db_path) as db:
        return db.execute(sql, params)


def sqlite_execute(db_path: str, sql: str, params: tuple = None) -> int:
    """快速SQLite执行"""
    with DatabaseOps(db_path) as db:
        with db.get_cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.rowcount


def sqlite_backup(db_path: str, backup_path: str = None) -> str:
    """快速SQLite备份"""
    with DatabaseOps(db_path) as db:
        return db.backup(backup_path)


# ============== 数据导入导出 ==============
def export_to_json(db_path: str, table: str, output_path: str = None) -> str:
    """导出表到JSON"""
    with DatabaseOps(db_path) as db:
        data = db.execute(f'SELECT * FROM {table}')
    
    if output_path is None:
        output_path = f'{table}.json'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return output_path


def import_from_json(db_path: str, table: str, json_path: str) -> int:
    """从JSON导入数据"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        return 0
    
    with DatabaseOps(db_path) as db:
        return db.insert_many(table, data)


# ============== 测试 ==============
if __name__ == '__main__':
    print('Database toolkit loaded')
    
    # 示例数据库路径
    example_db = 'example.db'
    
    # 创建示例表
    with DatabaseOps(example_db) as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY,
                code TEXT,
                name TEXT,
                price REAL,
                change_pct REAL,
                update_time TEXT
            )
        ''')
        
        # 插入示例数据
        db.insert('stocks', {
            'code': '000001',
            'name': '平安银行',
            'price': 12.34,
            'change_pct': 1.23,
            'update_time': datetime.now().isoformat()
        })
        
        # 查询
        results = db.execute('SELECT * FROM stocks LIMIT 10')
        print(f'Found {len(results)} records')
        
        # 统计
        count = db.count('stocks')
        print(f'Total: {count}')
        
        # 删除测试表
        db.execute('DROP TABLE stocks')
    
    print('Test completed')