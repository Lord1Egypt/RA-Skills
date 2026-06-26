#!/usr/bin/env python3
"""
MySQL Support for Database Ops
需要: pip install pymysql
"""

try:
    import pymysql
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("MySQL support requires: pip install pymysql")


class MySQLConnection:
    """MySQL连接"""
    
    def __init__(self, host='localhost', port=3306, user='root', 
                 password='', database=''):
        if not MYSQL_AVAILABLE:
            raise ImportError('pymysql not installed')
        
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.connect()
    
    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def execute(self, sql, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
    
    def execute_many(self, sql, params_list):
        with self.conn.cursor() as cursor:
            cursor.executemany(sql, params_list)
            self.conn.commit()
            return cursor.rowcount
    
    def insert(self, table: str, data: dict) -> int:
        """插入数据"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            return cursor.lastrowid
    
    def insert_many(self, table: str, rows: list) -> int:
        """批量插入"""
        if not rows:
            return 0
        
        columns = ', '.join(rows[0].keys())
        placeholders = ', '.join(['%s'] * len(rows[0]))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        
        values = [tuple(row.values()) for row in rows]
        
        with self.conn.cursor() as cursor:
            cursor.executemany(sql, values)
            self.conn.commit()
            return cursor.rowcount
    
    def update(self, table: str, data: dict, where: str, params: tuple = None) -> int:
        """更新数据"""
        set_clause = ', '.join([f'{k} = %s' for k in data.keys()])
        sql = f'UPDATE {table} SET {set_clause} WHERE {where}'
        
        values = tuple(data.values()) + (params or ())
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, values)
            self.conn.commit()
            return cursor.rowcount
    
    def delete(self, table: str, where: str, params: tuple = None) -> int:
        """删除数据"""
        sql = f'DELETE FROM {table} WHERE {where}'
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            self.conn.commit()
            return cursor.rowcount
    
    def query(self, sql, params=None):
        """查询"""
        return self.execute(sql, params)
    
    def fetch_one(self, sql, params=None):
        """获取单条"""
        results = self.execute(sql, params)
        return results[0] if results else None
    
    def fetch_value(self, sql, params=None):
        """获取单个值"""
        row = self.fetch_one(sql, params)
        return list(row.values())[0] if row else None
    
    def get_tables(self):
        """获取所有表"""
        return self.execute('SHOW TABLES')
    
    def get_columns(self, table: str):
        """获取列名"""
        result = self.execute(f'DESCRIBE {table}')
        return [r['Field'] for r in result]
    
    def get_table_info(self, table: str):
        """获取表结构"""
        return self.execute(f'DESCRIBE {table}')
    
    def count(self, table: str, where: str = None) -> int:
        """统计行数"""
        sql = f'SELECT COUNT(*) as cnt FROM {table}'
        if where:
            sql += f' WHERE {where}'
        return self.fetch_value(sql) or 0
    
    def stats(self, table: str) -> dict:
        """表统计"""
        columns = self.get_columns(table)
        row_count = self.count(table)
        
        return {
            'table': table,
            'columns': len(columns),
            'rows': row_count
        }
    
    def backup(self, backup_path: str):
        """备份(导出SQL)"""
        # 表结构
        create_sql = self.execute(f'SHOW CREATE TABLE {table}')
        
        # 数据
        data = self.execute(f'SELECT * FROM {table}')
        
        return {
            'create': create_sql,
            'data': data
        }
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def mysql_query(host, port, user, password, database, sql, params=None):
    """快速MySQL查询"""
    with MySQLConnection(host, port, user, password, database) as conn:
        return conn.execute(sql, params)


# 便捷函数
def create_mysql_pool(host='localhost', port=3306, user='root', 
                     password='', database='', pool_size=5):
    """创建连接池(需要DBUtils)"""
    try:
        from DBUtils import PooledDB
        import pymysql
        
        pool = PooledDB(
            creator=pymysql,
            maxconnections=pool_size,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return pool
    except ImportError:
        print("Connection pool requires: pip install dbutils")
        return None


if __name__ == '__main__':
    print('MySQL Support loaded')
    print(f'pymysql available: {MYSQL_AVAILABLE}')