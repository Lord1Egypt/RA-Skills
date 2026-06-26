#!/usr/bin/env python3
"""冰箱数据存储模块，支持本地文件和数据库两种模式"""

import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"


def load_config():
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        return None
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_storage_backend():
    """获取存储后端"""
    config = load_config()
    if not config:
        raise ValueError("配置未初始化，请先运行初始化")

    storage_type = config.get("storage_type", "local")

    if storage_type == "local":
        return LocalStorage(config.get("local_path", "./fridge_data.json"))
    else:
        db_config = config.get("database", {})
        db_type = db_config.get("type", "mysql")

        if db_type == "mysql":
            return MySQLStorage(db_config)
        elif db_type == "postgres":
            return PostgreSQLStorage(db_config)
        elif db_type == "mongodb":
            return MongoDBStorage(db_config)
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")


class LocalStorage:
    """本地文件存储"""

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self._ensure_file()

    def _ensure_file(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self._write({"items": []})

    def _read(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_items(self):
        data = self._read()
        return data.get("items", [])

    def save_item(self, item):
        data = self._read()
        data["items"].append(item)
        self._write(data)
        return item

    def update_item(self, item_id, updates):
        data = self._read()
        for i, item in enumerate(data["items"]):
            if item["id"] == item_id:
                data["items"][i].update(updates)
                self._write(data)
                return data["items"][i]
        return None

    def delete_item(self, item_id):
        data = self._read()
        data["items"] = [item for item in data["items"] if item["id"] != item_id]
        self._write(data)
        return True


class DatabaseStorage:
    """数据库存储基类"""

    def load_items(self):
        raise NotImplementedError

    def save_item(self, item):
        raise NotImplementedError

    def update_item(self, item_id, updates):
        raise NotImplementedError

    def delete_item(self, item_id):
        raise NotImplementedError


class MySQLStorage(DatabaseStorage):
    """MySQL存储"""

    def __init__(self, config):
        self.config = config
        try:
            import mysql.connector
        except ImportError:
            raise ImportError("请安装 mysql-connector-python: pip install mysql-connector-python")

    def _get_connection(self):
        import mysql.connector
        return mysql.connector.connect(
            host=self.config.get("host", "localhost"),
            port=self.config.get("port", 3306),
            user=self.config.get("username"),
            password=self.config.get("password"),
            database=self.config.get("database")
        )

    def load_items(self):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fridge_items WHERE status = 'active'")
        result = cursor.fetchall()
        conn.close()
        return result

    def save_item(self, item):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO fridge_items
               (id, name, quantity, unit, storage_location, inbound_time, shelf_life_days, expire_time, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (item["id"], item["name"], item["quantity"], item["unit"],
             item["storage_location"], item["inbound_time"], item["shelf_life_days"],
             item["expire_time"], item["status"])
        )
        conn.commit()
        conn.close()
        return item

    def update_item(self, item_id, updates):
        conn = self._get_connection()
        cursor = conn.cursor()
        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        cursor.execute(
            f"UPDATE fridge_items SET {set_clause} WHERE id = %s",
            list(updates.values()) + [item_id]
        )
        conn.commit()
        conn.close()
        return item_id

    def delete_item(self, item_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fridge_items WHERE id = %s", (item_id,))
        conn.commit()
        conn.close()
        return True


class PostgreSQLStorage(DatabaseStorage):
    """PostgreSQL存储"""

    def __init__(self, config):
        self.config = config
        try:
            import psycopg2
        except ImportError:
            raise ImportError("请安装 psycopg2: pip install psycopg2")

    def _get_connection(self):
        import psycopg2
        return psycopg2.connect(
            host=self.config.get("host", "localhost"),
            port=self.config.get("port", 5432),
            user=self.config.get("username"),
            password=self.config.get("password"),
            dbname=self.config.get("database")
        )

    def load_items(self):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fridge_items WHERE status = 'active'")
        result = cursor.fetchall()
        conn.close()
        return result

    def save_item(self, item):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO fridge_items
               (id, name, quantity, unit, storage_location, inbound_time, shelf_life_days, expire_time, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (item["id"], item["name"], item["quantity"], item["unit"],
             item["storage_location"], item["inbound_time"], item["shelf_life_days"],
             item["expire_time"], item["status"])
        )
        conn.commit()
        conn.close()
        return item

    def update_item(self, item_id, updates):
        conn = self._get_connection()
        cursor = conn.cursor()
        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        cursor.execute(
            f"UPDATE fridge_items SET {set_clause} WHERE id = %s",
            list(updates.values()) + [item_id]
        )
        conn.commit()
        conn.close()
        return item_id

    def delete_item(self, item_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fridge_items WHERE id = %s", (item_id,))
        conn.commit()
        conn.close()
        return True


class MongoDBStorage(DatabaseStorage):
    """MongoDB存储"""

    def __init__(self, config):
        self.config = config
        try:
            import pymongo
        except ImportError:
            raise ImportError("请安装 pymongo: pip install pymongo")

        client = pymongo.MongoClient(
            host=self.config.get("host", "localhost"),
            port=self.config.get("port", 27017),
            username=self.config.get("username"),
            password=self.config.get("password")
        )
        db = client[self.config.get("database", "fridge")]
        self.collection = db["items"]

    def load_items(self):
        return list(self.collection.find({"status": "active"}))

    def save_item(self, item):
        self.collection.insert_one(item)
        return item

    def update_item(self, item_id, updates):
        self.collection.update_one({"id": item_id}, {"$set": updates})
        return item_id

    def delete_item(self, item_id):
        self.collection.delete_one({"id": item_id})
        return True


# 便捷函数
def create_food_item(name, quantity, unit, storage_location, shelf_life_days):
    """创建食物条目"""
    now = datetime.utcnow()
    expire_time = now + timedelta(days=shelf_life_days)
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "quantity": quantity,
        "unit": unit,
        "storage_location": storage_location,
        "inbound_time": now.isoformat() + "Z",
        "shelf_life_days": shelf_life_days,
        "expire_time": expire_time.isoformat() + "Z",
        "status": "active"
    }


if __name__ == "__main__":
    # 测试代码
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 创建测试配置
        test_config = {
            "storage_type": "local",
            "local_path": "./test_fridge.json",
            "expiry_warning_days": 3
        }
        save_config(test_config)

        storage = get_storage_backend()

        # 测试添加
        item = create_food_item("鸡蛋", 12, "个", "冷藏室", 14)
        storage.save_item(item)
        print(f"添加成功: {item['name']}")

        # 测试读取
        items = storage.load_items()
        print(f"当前食物: {len(items)} 项")

        # 测试更新
        storage.update_item(item["id"], {"status": "consumed"})
        print("更新成功")

        # 测试删除
        storage.delete_item(item["id"])
        print("删除成功")

        # 清理测试文件
        Path("./test_fridge.json").unlink(missing_ok=True)
        print("测试完成")