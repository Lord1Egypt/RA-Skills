#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data-query 技能知识库生成脚本
功能：从 ACM 数据库一键重生成技能知识库文件

用法：
    python generate.py --dry-run          # 预览差异
    python generate.py --apply            # 执行同步
    python generate.py --target tables    # 只生成指定文件
    python generate.py --target all       # 全部重新生成
    python generate.py --db-type dm       # 指定数据库类型

支持的数据库类型：
    mysql   : MySQL (使用 pymysql)
    dm      : 达梦数据库 (使用 dmPython 或 pyodbc)
    oracle  : Oracle (使用 oracledb)
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# ============================================================
# 配置
# ============================================================

SKILL_DIR = Path(__file__).parent.parent.parent.resolve()
KNOWLEDGE_BASE = SKILL_DIR / 'knowledge'

# 按 db-type 分离的子目录
DB_TYPES = ['mysql', 'dm', 'oracle']

def get_db_knowledge_dir(db_type):
    """返回指定 db_type 的知识库子目录"""
    return KNOWLEDGE_BASE / db_type

# 默认 db_type 为 mysql
DB_TYPE = os.getenv('ACM_DB_TYPE', 'mysql')

DB_CONFIG = {
    "host": os.getenv('ACM_DB_HOST', '192.168.3.25' if DB_TYPE == 'mysql' else '192.168.3.11'),
    "port": int(os.getenv('ACM_DB_PORT', '3306' if DB_TYPE == 'mysql' else '5236')),
    "user": os.getenv('ACM_DB_USER', 'root' if DB_TYPE == 'mysql' else 'ACM_CLOUD_AVIC_100'),
    "password": os.getenv('ACM_DB_PASSWORD', 'Wisdom83248380' if DB_TYPE == 'mysql' else 'ACM_CLOUD_AVIC_100'),
    "database": os.getenv('ACM_DB_NAME', 'acm_cloud_acm' if DB_TYPE == 'mysql' else 'DM'),
    "charset": "utf8mb4"
}

# 数据库无 DEL 字段的表（查询时不加 DEL 条件）
NO_DEL_TABLES = {
    'wsd_risk_register', 'wsd_base_dict',
    'wsd_comu_meeting', 'wsd_comu_meetingaction',
    'wsd_plan_taskrsrc'
}

# 模块前缀映射
MODULE_MAPPING = {
    "wsd_sys": {"name": "系统管理", "code": "sys"},
    "wsd_plan": {"name": "计划管理", "code": "plan"},
    "wsd_wf": {"name": "工作流", "code": "wf"},
    "wsd_doc": {"name": "文档管理", "code": "doc"},
    "wsd_risk": {"name": "风险管理", "code": "risk"},
    "wsd_comu": {"name": "沟通交流", "code": "comu"},
    "wsd_dashboard": {"name": "仪表盘", "code": "dashboard"},
    "wsd_cntc": {"name": "联系人", "code": "cntc"},
    "wsd_rsrc": {"name": "资源管理", "code": "rsrc"},
    "wsd_base": {"name": "基础数据", "code": "base"},
    "wsd_adp": {"name": "敏捷开发", "code": "adp"},
    "wsd_cost": {"name": "成本管理", "code": "cost"},
    "wsd_ipd": {"name": "IPD管理", "code": "ipd"},
}

# ============================================================
# 驱动管理
# ============================================================

class DatabaseDriver:
    """数据库驱动管理器"""
    
    def __init__(self, db_type):
        self.db_type = db_type
        self.driver = None
        self.driver_type = None
        self.errors = []
    
    def detect(self):
        """检测并加载合适的数据库驱动"""
        if self.db_type == 'mysql':
            return self._detect_mysql()
        elif self.db_type == 'dm':
            return self._detect_dm()
        elif self.db_type == 'oracle':
            return self._detect_oracle()
        else:
            self.errors.append(f"不支持的数据库类型: {self.db_type}")
            return False
    
    def _detect_mysql(self):
        """检测 MySQL 驱动"""
        try:
            import pymysql
            self.driver = pymysql
            self.driver_type = 'pymysql'
            return True
        except ImportError as e:
            self.errors.append(f"pymysql: {e}")
            print("❌ 未找到 pymysql 驱动")
            print("   安装命令: pip install pymysql")
            return False
    
    def _detect_dm(self):
        """检测达梦数据库驱动（支持 dmPython 和 pyodbc）"""
        # 1. 尝试 dmPython（性能最好）
        try:
            import dmPython
            self.driver = dmPython
            self.driver_type = 'dmpython'
            print("✅ 使用驱动: dmPython")
            return True
        except ImportError as e:
            self.errors.append(f"dmPython: {e}")
        
        # 2. 尝试 pyodbc（跨平台兼容性好）
        try:
            import pyodbc
            # 检查是否有达梦 ODBC 驱动
            drivers = pyodbc.drivers()
            dm_drivers = [d for d in drivers if 'DM' in d.upper() or '达梦' in d]
            if dm_drivers:
                self.driver = pyodbc
                self.driver_type = 'pyodbc'
                print(f"✅ 使用驱动: pyodbc (ODBC驱动: {dm_drivers[0]})")
                return True
            else:
                self.errors.append("pyodbc: 未找到达梦 ODBC 驱动")
        except ImportError as e:
            self.errors.append(f"pyodbc: {e}")
        
        # 都不可用
        print("❌ 未找到可用的达梦数据库驱动")
        print("\n可能的解决方案：")
        print("\n1. 安装 dmPython（推荐用于 Linux/Windows）：")
        print("   • 安装达梦数据库客户端（https://www.dameng.com/）")
        print("   • 配置环境变量: export DM_HOME=/opt/dmdbms")
        print("   • pip install dmPython")
        print("\n2. 安装 pyodbc（推荐用于 macOS）：")
        print("   • pip install pyodbc")
        print("   • 安装达梦 ODBC 驱动")
        print("\n3. 使用转换方案（无需驱动，推荐）：")
        print("   • 步骤1: 使用达梦 DM Manager 导出表结构为 SQL 或 CSV 文件")
        print("   • 步骤2: 运行转换脚本生成知识库")
        print("   • 示例: cd scripts/knowledge && python3 convert_knowledge.py --input structure.sql --mapping")
        print("\n4. 手动创建知识库：")
        print("   参考 knowledge/mysql/tables.json 格式手动创建")
        return False
    
    def _detect_oracle(self):
        """检测 Oracle 驱动"""
        try:
            import oracledb
            self.driver = oracledb
            self.driver_type = 'oracledb'
            return True
        except ImportError as e:
            self.errors.append(f"oracledb: {e}")
            print("❌ 未找到 oracledb 驱动")
            print("   安装命令: pip install oracledb")
            return False
    
    def connect(self, config):
        """建立数据库连接"""
        if self.db_type == 'mysql':
            return self._connect_mysql(config)
        elif self.db_type == 'dm':
            return self._connect_dm(config)
        elif self.db_type == 'oracle':
            return self._connect_oracle(config)
        else:
            raise ValueError(f"不支持的数据库类型: {self.db_type}")
    
    def _connect_mysql(self, config):
        """连接 MySQL"""
        return self.driver.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config.get('charset', 'utf8mb4'),
            cursorclass=self.driver.cursors.DictCursor
        )
    
    def _connect_dm(self, config):
        """连接达梦数据库"""
        if self.driver_type == 'dmpython':
            conn = self.driver.connect(
                user=config['user'],
                password=config['password'],
                server=config['host'],
                port=config['port']
            )
            # 设置 schema
            cursor = conn.cursor()
            cursor.execute(f"SET SCHEMA {config['database']}")
            cursor.close()
            return conn
        elif self.driver_type == 'pyodbc':
            conn_str = (
                f"DRIVER={{DM8 ODBC DRIVER}};"
                f"SERVER={config['host']};"
                f"PORT={config['port']};"
                f"DATABASE={config['database']};"
                f"UID={config['user']};"
                f"PWD={config['password']};"
            )
            return self.driver.connect(conn_str)
        else:
            raise ValueError(f"未知的达梦驱动类型: {self.driver_type}")
    
    def _connect_oracle(self, config):
        """连接 Oracle"""
        dsn = f"{config['host']}:{config['port']}/{config.get('serviceName', 'ORCL')}"
        return self.driver.connect(
            user=config['user'],
            password=config['password'],
            dsn=dsn
        )
    
    def create_cursor(self, conn):
        """创建游标"""
        if self.db_type == 'mysql':
            return conn.cursor()
        elif self.db_type == 'dm':
            if self.driver_type == 'dmpython':
                return conn.cursor()
            else:  # pyodbc
                return conn.cursor()
        elif self.db_type == 'oracle':
            return conn.cursor()
    
    def execute(self, cursor, sql, params=None):
        """执行 SQL"""
        # 根据数据库类型转换参数占位符
        if self.db_type == 'mysql':
            # MySQL 使用 %s 作为占位符
            sql = sql.replace('?', '%s')
        
        if params:
            return cursor.execute(sql, params)
        return cursor.execute(sql)
    
    def fetchall(self, cursor):
        """获取所有结果"""
        if self.db_type == 'mysql':
            return cursor.fetchall()
        elif self.db_type == 'dm':
            if self.driver_type == 'dmpython':
                return cursor.fetchall()
            else:  # pyodbc
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        elif self.db_type == 'oracle':
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

# ============================================================
# 数据库操作
# ============================================================

def get_table_module(table_name):
    """获取表所属模块"""
    t = table_name.lower()
    for prefix, info in MODULE_MAPPING.items():
        if t.startswith(prefix.lower()):
            return info["code"]
    return "other"

# ============================================================
# 生成器
# ============================================================

def generate_tables(driver, conn) -> dict:
    """生成表结构信息"""
    tables = {}
    cursor = driver.create_cursor(conn)
    
    try:
        if driver.db_type == 'mysql':
            # MySQL 系统表查询
            driver.execute(cursor, """
                SELECT
                    c.TABLE_NAME,
                    c.COLUMN_NAME,
                    c.COLUMN_TYPE,
                    c.IS_NULLABLE,
                    c.COLUMN_KEY,
                    c.COLUMN_DEFAULT,
                    c.COLUMN_COMMENT,
                    t.TABLE_COMMENT
                FROM information_schema.COLUMNS c
                JOIN information_schema.TABLES t
                  ON c.TABLE_NAME = t.TABLE_NAME AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
                WHERE c.TABLE_SCHEMA = %s
                  AND t.TABLE_TYPE = 'BASE TABLE'
                ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION
            """, (DB_CONFIG['database'],))
        elif driver.db_type == 'dm':
            # 达梦数据库系统表查询
            driver.execute(cursor, """
                SELECT 
                    c.TABLE_NAME,
                    c.COLUMN_NAME,
                    c.DATA_TYPE as COLUMN_TYPE,
                    c.NULLABLE as IS_NULLABLE,
                    c.DATA_DEFAULT as COLUMN_DEFAULT,
                    c.COMMENTS as COLUMN_COMMENT,
                    t.COMMENTS as TABLE_COMMENT
                FROM USER_TAB_COLUMNS c
                JOIN USER_TABLES t ON c.TABLE_NAME = t.TABLE_NAME
                ORDER BY c.TABLE_NAME, c.COLUMN_ID
            """)
        elif driver.db_type == 'oracle':
            # Oracle 系统表查询
            driver.execute(cursor, """
                SELECT 
                    c.TABLE_NAME,
                    c.COLUMN_NAME,
                    c.DATA_TYPE as COLUMN_TYPE,
                    c.NULLABLE as IS_NULLABLE,
                    c.DATA_DEFAULT as COLUMN_DEFAULT,
                    c.COMMENTS as COLUMN_COMMENT,
                    t.COMMENTS as TABLE_COMMENT
                FROM USER_TAB_COLUMNS c
                JOIN USER_TABLES t ON c.TABLE_NAME = t.TABLE_NAME
                ORDER BY c.TABLE_NAME, c.COLUMN_ID
            """)
        
        rows = driver.fetchall(cursor)
        print(f"  数据库共 {len(rows)} 条字段记录")
        
        for row in rows:
            table_name = row['TABLE_NAME']
            if table_name not in tables:
                tables[table_name] = {
                    "comment": row['TABLE_COMMENT'] or '',
                    "module": get_table_module(table_name),
                    "fields": {}
                }
            
            tables[table_name]["fields"][row['COLUMN_NAME']] = {
                "type": row['COLUMN_TYPE'],
                "nullable": row['IS_NULLABLE'] == 'YES' if driver.db_type == 'mysql' else row['IS_NULLABLE'] == 'Y',
                "key": row.get('COLUMN_KEY') or None,
                "default": row['COLUMN_DEFAULT'],
                "comment": row['COLUMN_COMMENT'] or ''
            }
        
        print(f"  共提取 {len(tables)} 个表")
        
    finally:
        cursor.close()
    
    return tables

def generate_field_mapping(driver, conn) -> dict:
    """生成字段映射"""
    mapping = {
        "_comment": "LLM SQL生成 - 字段映射表（中文注释 + 枚举值）",
        "_source": "从 wsd_base_dict 表提取",
        "_updated": datetime.now().strftime("%Y-%m-%d"),
        "字段→中文名": {},
        "枚举值映射": {}
    }
    
    cursor = driver.create_cursor(conn)
    
    # 确保 cursor 被正确创建
    if cursor is None:
        print("  ⚠️  创建游标失败")
        return mapping
    
    try:
        driver.execute(cursor, "SELECT DISTINCT type_code FROM wsd_base_dict WHERE enable_ = 1 ORDER BY type_code")
        dict_types = driver.fetchall(cursor)
        
        for dt_row in dict_types:
            # 处理不同数据库列名大小写不一致的问题
            dict_type = dt_row.get('TYPE_CODE') or dt_row.get('type_code')
            if dict_type is None:
                continue
            
            driver.execute(
                cursor,
                "SELECT dict_code, dict_name FROM wsd_base_dict WHERE enable_ = 1 AND type_code = ? ORDER BY sort_num",
                (dict_type,)
            )
            items = driver.fetchall(cursor)
            mapping["枚举值映射"][dict_type] = {}
            for it in items:
                dict_code = it.get('DICT_CODE') or it.get('dict_code')
                dict_name = it.get('DICT_NAME') or it.get('dict_name')
                mapping["枚举值映射"][dict_type][str(dict_code)] = dict_name
        
    except Exception as e:
        print(f"  ⚠️  字段映射生成失败: {e}")
    finally:
        if cursor:
            cursor.close()
    
    return mapping

# ============================================================
# 差异化对比
# ============================================================

def load_local(path: Path) -> tuple:
    """加载本地文件"""
    if not path.exists():
        return None, None
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f) if path.suffix == '.json' else f.read()
    mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
    return data, mtime

def diff_summary(local: dict, remote: dict, name: str) -> str:
    """生成差异摘要"""
    if local is None:
        return f"  → 本地不存在，将创建"
    
    local_keys = set(local.keys()) - {'_comment', '_source', '_updated'}
    remote_keys = set(remote.keys()) - {'_comment', '_source', '_updated'}
    
    added = remote_keys - local_keys
    removed = local_keys - remote_keys
    same = local_keys & remote_keys
    
    lines = []
    if added:
        lines.append(f"  + {len(added)} 新条目: {sorted(added)[:5]}{'...' if len(added)>5 else ''}")
    if removed:
        lines.append(f"  - {len(removed)} 移除条目")
    if same:
        lines.append(f"  ~ {len(same)} 共同条目（内容变化未检测）")
    if not lines:
        lines.append(f"  = 完全一致")
    
    return '\n'.join(lines)

# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='data-query 技能知识库生成脚本')
    parser.add_argument('--dry-run', action='store_true', help='预览差异，不写入文件')
    parser.add_argument('--apply', action='store_true', help='执行同步，写入文件')
    parser.add_argument('--target', choices=['tables', 'field_mapping', 'all'],
                        default='all', help='指定生成目标')
    parser.add_argument('--db-type', choices=DB_TYPES, default=DB_TYPE,
                        help=f'指定数据库类型（默认: {DB_TYPE}）')
    args = parser.parse_args()
    
    if not args.dry_run and not args.apply:
        parser.print_help()
        print(f"\n请指定 --dry-run（预览）或 --apply（执行）")
        return
    
    db_type = args.db_type
    KNOWLEDGE_DIR = get_db_knowledge_dir(db_type)
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"=== [{db_type}] 知识库生成 ===\n")
    
    # 检测驱动
    driver = DatabaseDriver(db_type)
    if not driver.detect():
        return
    
    print(f"连接数据库 {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}\n")
    
    try:
        conn = driver.connect(DB_CONFIG)
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return
    
    # 生成目标
    targets = ['tables', 'field_mapping'] if args.target == 'all' else [args.target]
    
    print(f"目标: {', '.join(targets)}\n")
    
    results = {}
    
    # ---- tables.json ----
    if 'tables' in targets:
        print("=== tables.json ===")
        path = KNOWLEDGE_DIR / 'tables.json'
        
        local_data, local_mtime = load_local(path)
        print(f"  本地: {local_mtime}, {'无' if local_data is None else str(len(local_data)) + ' 表'}")
        
        print("  正在从数据库提取...")
        remote = generate_tables(driver, conn)
        print(f"  数据库: {datetime.now().strftime('%Y-%m-%d %H:%M')}, {len(remote)} 表")
        
        if local_data is None:
            print("  → 本地不存在")
            action = args.apply
        else:
            local_keys = set(k for k in local_data.keys() if not k.startswith('_'))
            remote_keys = set(remote.keys())
            added = len(remote_keys - local_keys)
            removed = len(local_keys - remote_keys)
            print(f"  差异: +{added} 表, -{removed} 表")
            action = args.apply and (added > 0 or removed > 0)
        
        if action:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(remote, f, ensure_ascii=False, indent=2)
            print(f"  ✅ 已写入 {path}")
        elif args.apply:
            print(f"  ⏭️  无变化，跳过")
        else:
            print(f"  💡 建议: python generate.py --apply --target tables --db-type {db_type}")
        print()
        results['tables'] = action
    
    # ---- field_mapping.json ----
    if 'field_mapping' in targets:
        print("=== field_mapping.json ===")
        path = KNOWLEDGE_DIR / 'field_mapping.json'
        
        local_data, local_mtime = load_local(path)
        print(f"  本地: {local_mtime}")
        
        print("  正在从 wsd_base_dict 提取...")
        remote = generate_field_mapping(driver, conn)
        
        local_dict_count = len([k for k in (local_data or {}).keys() if not k.startswith('_')])
        remote_dict_count = len([k for k in remote.keys() if not k.startswith('_')])
        print(f"  本地字典类型: {local_dict_count}, 数据库字典类型: {remote_dict_count}")
        
        action = args.apply and remote_dict_count != local_dict_count
        if action:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(remote, f, ensure_ascii=False, indent=2)
            print(f"  ✅ 已写入 {path}")
        elif args.apply:
            print(f"  ⏭️  无变化，跳过")
        else:
            print(f"  💡 建议: python generate.py --apply --target field_mapping --db-type {db_type}")
        print()
        results['field_mapping'] = action
    
    # 关闭连接
    conn.close()
    
    print("\n=== 完成 ===")
    for target, updated in results.items():
        status = "✅ 已更新" if updated else "⏭️  无变化"
        print(f"  {target}: {status}")

if __name__ == '__main__':
    main()
