#!/usr/bin/env python3
"""
AI 自动化测试平台 - 数据库初始化脚本

创建所有必要的数据库表结构
"""

import pymysql
from pymysql import Error

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root123',
    'charset': 'utf8mb4'
}

DATABASE_NAME = 'ai_test_platform'

# SQL语句：创建数据库
CREATE_DATABASE_SQL = f"""
CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;
"""

# SQL语句：创建授权码表
CREATE_AUTH_CODES_TABLE = """
CREATE TABLE IF NOT EXISTS auth_codes (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    code VARCHAR(100) UNIQUE NOT NULL COMMENT '授权码（加密后）',
    permission VARCHAR(20) NOT NULL COMMENT '权限类型：all/generate/execute',
    expire_time DATETIME NOT NULL COMMENT '过期时间',
    use_count INT DEFAULT 0 COMMENT '已使用次数',
    max_count INT NOT NULL COMMENT '最大使用次数',
    is_active TINYINT DEFAULT 1 COMMENT '启用状态：1启用/0禁用',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_code (code),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='授权码表';
"""

# SQL语句：创建测试用例表
CREATE_TEST_CASES_TABLE = """
CREATE TABLE IF NOT EXISTS test_cases (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    title VARCHAR(255) NOT NULL COMMENT '用例标题',
    content TEXT NOT NULL COMMENT '用例详情',
    type VARCHAR(10) NOT NULL COMMENT '类型：api/ui',
    created_by VARCHAR(50) COMMENT '创建者（授权码）',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_type (type),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试用例表';
"""

# SQL语句：创建自动化脚本表
CREATE_AUTO_SCRIPTS_TABLE = """
CREATE TABLE IF NOT EXISTS auto_scripts (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    name VARCHAR(255) NOT NULL COMMENT '脚本名称',
    content TEXT NOT NULL COMMENT '脚本代码',
    type VARCHAR(10) NOT NULL COMMENT '类型：api/ui',
    status VARCHAR(10) DEFAULT 'active' COMMENT '状态：active/archived',
    created_by VARCHAR(50) COMMENT '创建者',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='自动化脚本表';
"""

# SQL语句：创建执行记录表
CREATE_EXECUTE_RECORDS_TABLE = """
CREATE TABLE IF NOT EXISTS execute_records (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    script_id INT NOT NULL COMMENT '脚本ID',
    auth_code VARCHAR(50) COMMENT '执行者授权码',
    result VARCHAR(10) NOT NULL COMMENT '结果：success/fail',
    log TEXT COMMENT '执行日志',
    execute_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '执行时间',
    duration INT COMMENT '执行耗时（秒）',
    INDEX idx_script_id (script_id),
    INDEX idx_result (result),
    INDEX idx_execute_time (execute_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='执行记录表';
"""

# SQL语句：创建测试报告表
CREATE_TEST_REPORTS_TABLE = """
CREATE TABLE IF NOT EXISTS test_reports (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    record_id INT NOT NULL COMMENT '执行记录ID',
    report_content TEXT COMMENT '报告内容（JSON/HTML）',
    file_path VARCHAR(255) COMMENT '报告文件路径',
    ai_analysis TEXT COMMENT 'AI分析结果',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_record_id (record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试报告表';
"""

# SQL语句：创建任务进度表
CREATE_TASK_PROGRESS_TABLE = """
CREATE TABLE IF NOT EXISTS task_progress (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    task_id VARCHAR(100) UNIQUE NOT NULL COMMENT '任务ID',
    task_type VARCHAR(20) NOT NULL COMMENT '任务类型：generate/execute',
    status VARCHAR(20) NOT NULL COMMENT '状态：pending/processing/completed/failed',
    progress INT DEFAULT 0 COMMENT '进度百分比',
    message VARCHAR(255) COMMENT '进度消息',
    result_data TEXT COMMENT '结果数据（JSON）',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_task_id (task_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务进度表';
"""

def create_database():
    """创建数据库"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print(f"正在创建数据库: {DATABASE_NAME}")
        cursor.execute(CREATE_DATABASE_SQL)
        print(f"数据库 {DATABASE_NAME} 创建成功或已存在")

        cursor.close()
    except Error as e:
        print(f"创建数据库失败: {e}")
        raise
    finally:
        if connection:
            connection.close()

def create_tables():
    """创建数据表"""
    # 连接到指定数据库
    config = DB_CONFIG.copy()
    config['database'] = DATABASE_NAME

    connection = None
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        tables = [
            ('auth_codes', CREATE_AUTH_CODES_TABLE),
            ('test_cases', CREATE_TEST_CASES_TABLE),
            ('auto_scripts', CREATE_AUTO_SCRIPTS_TABLE),
            ('execute_records', CREATE_EXECUTE_RECORDS_TABLE),
            ('test_reports', CREATE_TEST_REPORTS_TABLE),
            ('task_progress', CREATE_TASK_PROGRESS_TABLE)
        ]

        for table_name, create_sql in tables:
            print(f"正在创建表: {table_name}")
            cursor.execute(create_sql)
            print(f"表 {table_name} 创建成功或已存在")

        connection.commit()
        print("\n所有数据表创建完成！")

        cursor.close()
    except Error as e:
        print(f"创建数据表失败: {e}")
        raise
    finally:
        if connection:
            connection.close()

def verify_tables():
    """验证表结构"""
    config = DB_CONFIG.copy()
    config['database'] = DATABASE_NAME

    connection = None
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        print("\n验证数据表结构:")
        print("-" * 80)

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()

            print(f"\n表名: {table_name}")
            print(f"{'字段':<20} {'类型':<20} {'允许空':<10} {'键':<10}")
            print("-" * 80)
            for column in columns:
                print(f"{column[0]:<20} {column[1]:<20} {column[2]:<10} {column[3] or '':<10}")

        cursor.close()
    except Error as e:
        print(f"验证表结构失败: {e}")
        raise
    finally:
        if connection:
            connection.close()

def main():
    """主函数"""
    print("=" * 80)
    print("AI 自动化测试平台 - 数据库初始化")
    print("=" * 80)
    print()

    try:
        # 步骤1：创建数据库
        print("[步骤 1/3] 创建数据库")
        create_database()
        print()

        # 步骤2：创建数据表
        print("[步骤 2/3] 创建数据表")
        create_tables()
        print()

        # 步骤3：验证表结构
        print("[步骤 3/3] 验证表结构")
        verify_tables()
        print()

        print("=" * 80)
        print("数据库初始化完成！")
        print("=" * 80)

    except Exception as e:
        print(f"\n初始化失败: {str(e)}")
        return 1

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
