#!/usr/bin/env python3
"""PostgreSQL Connection"""
import os

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


class PostgreSQLConn:
    """PostgreSQL连接"""
    
    def __init__(self, host="localhost", port=5432, user="postgres", password="", database="postgres"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        if POSTGRES_AVAILABLE:
            try:
                self.conn = psycopg2.connect(
                    host=host, port=port, user=user,
                    password=password, database=database
                )
                self.connected = True
            except:
                self.connected = False
        else:
            self.connected = False
    
    def is_connected(self):
        return self.connected
    
    def execute(self, sql, params=None):
        if not self.conn:
            return []
        cursor = self.conn.cursor()
        cursor.execute(sql, params or None)
        if sql.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        self.conn.commit()
        return []
    
    def get_tables(self):
        return [r[0] for r in self.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")]
    
    def get_columns(self, table):
        return [r[0] for r in self.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}'")]
    
    def close(self):
        if self.conn:
            self.conn.close()


try:
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False


class MongoDBConn:
    """MongoDB连接"""
    
    def __init__(self, host="localhost", port=27017, database="test"):
        self.host = host
        self.port = port
        self.database = database
        self.client = None
        self.db = None
        if MONGODB_AVAILABLE:
            try:
                self.client = MongoClient(host, port)
                self.db = self.client[database]
                self.connected = True
            except:
                self.connected = False
        else:
            self.connected = False
    
    def is_connected(self):
        return self.connected
    
    def insert_one(self, collection, data):
        if self.db:
            return self.db[collection].insert_one(data).inserted_id
        return None
    
    def insert_many(self, collection, data):
        if self.db:
            return self.db[collection].insert_many(data).inserted_ids
        return []
    
    def find(self, collection, query=None):
        if self.db:
            return list(self.db[collection].find(query or {}))
        return []
    
    def update(self, collection, query, data):
        if self.db:
            return self.db[collection].update_many(query, {"$set": data}).modified_count
        return 0
    
    def delete(self, collection, query):
        if self.db:
            return self.db[collection].delete_many(query).deleted_count
        return 0
    
    def close(self):
        if self.client:
            self.client.close()


if __name__ == "__main__":
    print("PostgreSQL:", POSTGRES_AVAILABLE)
    print("MongoDB:", MONGODB_AVAILABLE)