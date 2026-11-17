#!/usr/bin/env python3
"""
企服助手 - SQLite数据库初始化脚本
从腾讯文档同步数据到本地SQLite，实现超快查询+零token消耗
"""

import sqlite3
import json
import os
from pathlib import Path

# 数据库路径
DB_PATH = Path.home() / ".workbuddy" / "workspace" / "enterprise-service-assistant" / "local_db.sqlite"

def init_database():
    """初始化SQLite数据库，创建所有表结构"""
    
    # 确保目录存在
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # ==================== 1. 客户管理表 ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT,                    -- 项目
        unit_type TEXT,                 -- 单元类型
        building_area REAL,             -- 建筑面积
        rent_area REAL,                 -- 计租面积
        unit_no TEXT UNIQUE,            -- 单元号（主键）
        tenant_name TEXT,               -- 租户名
        contract_no TEXT,               -- 合同编号
        salesperson TEXT,               -- 招商
        start_date TEXT,                -- 开始日期
        end_date TEXT,                  -- 截至日期
        status TEXT,                    -- 状态
        contact_person TEXT,            -- 租户联系人
        phone TEXT,                     -- 电话
        level TEXT,                     -- 等级
        enterprise_type TEXT,            -- 企业类型
        business_scope TEXT,            -- 经营范围
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==================== 2. 费用收缴表 ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_no TEXT,                   -- 单元号
        tenant_name TEXT,               -- 租户名
        fee_type TEXT,                  -- 费项项目
        receivable_date TEXT,           -- 应收到期日
        receivable_amount REAL,         -- 应收金额
        received_amount REAL,           -- 实收金额
        overdue_days INTEGER,           -- 逾期天数（计算字段）
        status TEXT,                    -- 状态
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==================== 3. 报修情况汇总表 ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS repair_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_no TEXT,                   -- 楼层/单元
        urgency TEXT,                   -- 紧急程度
        description TEXT,               -- 报修细节描述
        report_time TEXT,               -- 报修时间
        assignee TEXT,                  -- 维修人员
        status TEXT,                    -- 维修跟进状态
        result TEXT,                    -- 跟进状态及结果描述
        cost REAL,                      -- 维修费用
        complete_time TEXT,             -- 维修完成时间
        duration_days INTEGER,          -- 维修用时天数
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==================== 4. 库存管理表 ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,               -- 名称
        spec TEXT,                      -- 规格/单位
        current_stock REAL,             -- 现库存
        monthly_usage REAL,             -- 月使用量
        available_months REAL,          -- 可用月数（计算字段）
        status TEXT,                    -- 状态（缺货/预警/关注/正常）
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==================== 5. C+服务记录表 ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cservice_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_name TEXT,               -- 租户名
        visit_time TEXT,                -- 走访时间
        visitor TEXT,                   -- 走访管家
        mood TEXT,                      -- 客户情绪
        deal_status TEXT,               -- 成交情况
        service_type TEXT,              -- 服务类别
        deal_amount REAL,               -- 成交金额
        detail TEXT,                    -- 详情记录
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==================== 6. 认股权台账表 ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equity_warrants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,              -- 企业名称
        unit_no TEXT,                   -- 单元号
        warrant_ratio REAL,             -- 认股权比例
        valuation_cap REAL,             -- 估值上限
        discount REAL,                  -- 行权折扣
        grant_date TEXT,                -- 授予日期
        expiry_date TEXT,               -- 到期日期
        status TEXT,                    -- 状态
        concession_amount REAL,         -- 让利金额
        financing_progress TEXT,        -- 融资进展
        remarks TEXT,                   -- 备注
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # ==================== 7. 同步日志表 ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sync_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT,                -- 表名
        sync_time TEXT,                 -- 同步时间
        record_count INTEGER,           -- 同步记录数
        status TEXT,                    -- 状态（success/failed）
        error_msg TEXT,                 -- 错误信息
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_customers_unit ON customers(unit_no)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(tenant_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fees_unit ON fees(unit_no)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fees_status ON fees(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_repair_status ON repair_orders(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cservice_name ON cservice_records(tenant_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cservice_time ON cservice_records(visit_time)")
    
    conn.commit()
    conn.close()
    
    print(f"✅ 数据库初始化成功：{DB_PATH}")
    return str(DB_PATH)

if __name__ == "__main__":
    init_database()
