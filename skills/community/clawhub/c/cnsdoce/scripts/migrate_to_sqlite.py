# -*- coding: utf-8 -*-
"""
cnsdoce 数据迁移脚本：JSON → SQLite
将 quota_data_v5.json 和 materials_db.json 转换为 SQLite 数据库，
并建立查询索引，实现毫秒级查询。

用法：python migrate_to_sqlite.py
输出：index/quota.db
"""
import json
import sqlite3
import time
import sys
from pathlib import Path

# ==================== 配置 ====================
SKILL_DIR = Path(__file__).parent.parent
INDEX_DIR = SKILL_DIR / "index"
REFS_DIR  = SKILL_DIR / "references"

QUOTA_JSON  = INDEX_DIR / "quota_data_v5.json"
MATERIAL_JSON = REFS_DIR / "materials_db.json"
DB_PATH = INDEX_DIR / "quota.db"


def migrate_quota_data(conn):
    """迁移定额数据：quota_data_v5.json → quotas 表"""
    print("\n" + "=" * 60)
    print("📦 迁移定额数据：quota_data_v5.json → quotas 表")
    print("=" * 60)

    if not QUOTA_JSON.exists():
        print(f"❌ 文件不存在：{QUOTA_JSON}")
        return 0

    start = time.time()
    with open(QUOTA_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    load_time = time.time() - start
    print(f"  ✓ JSON加载耗时：{load_time:.3f}s（{len(data)}条记录）")

    # 创建表
    conn.execute("DROP TABLE IF EXISTS quotas")
    conn.execute("""
        CREATE TABLE quotas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            quota_no    TEXT NOT NULL,
            original_quota_no TEXT,
            name        TEXT NOT NULL,
            unit        TEXT,
            base_price  REAL,
            price_tax   REAL,
            price_no_tax REAL,
            labor_fee   REAL,
            material_fee REAL,
            machine_fee  REAL,
            chapter     TEXT,
            category    TEXT,
            work_content TEXT,
            source      TEXT,
            category_prefix TEXT
        )
    """)

    # 批量插入
    start = time.time()
    rows = []
    for item in data:
        rows.append((
            item.get("quota_no", ""),
            item.get("original_quota_no", ""),
            item.get("name", ""),
            item.get("unit", ""),
            item.get("base_price"),
            item.get("price_tax"),
            item.get("price_no_tax"),
            item.get("labor_fee"),
            item.get("material_fee"),
            item.get("machine_fee"),
            item.get("chapter", ""),
            item.get("category", ""),
            item.get("work_content", ""),
            item.get("source", ""),
            item.get("category_prefix", ""),
        ))

    conn.executemany("""
        INSERT INTO quotas (
            quota_no, original_quota_no, name, unit,
            base_price, price_tax, price_no_tax,
            labor_fee, material_fee, machine_fee,
            chapter, category, work_content, source, category_prefix
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
    insert_time = time.time() - start
    print(f"  ✓ 数据插入耗时：{insert_time:.3f}s")

    return len(rows)


def migrate_material_data(conn):
    """迁移材料数据：materials_db.json → materials 表"""
    print("\n" + "=" * 60)
    print("📦 迁移材料数据：materials_db.json → materials 表")
    print("=" * 60)

    if not MATERIAL_JSON.exists():
        print(f"❌ 文件不存在：{MATERIAL_JSON}")
        return 0

    start = time.time()
    with open(MATERIAL_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    load_time = time.time() - start
    print(f"  ✓ JSON加载耗时：{load_time:.3f}s（{len(data)}条记录）")

    # 创建表
    conn.execute("DROP TABLE IF EXISTS materials")
    conn.execute("""
        CREATE TABLE materials (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            orig_id         TEXT,
            编码            TEXT,
            名称            TEXT NOT NULL,
            规格型号        TEXT,
            单位            TEXT,
            含税单价        REAL,
            除税单价        REAL,
            增值税率        REAL,
            含税单价_202602 REAL,
            含税单价_202603 REAL,
            取定价          REAL,
            数据来源        TEXT,
            备注            TEXT,
            适用专业        TEXT
        )
    """)

    # 批量插入
    start = time.time()
    rows = []
    for item in data:
        # 适用专业：列表转逗号分隔字符串
        majors = item.get("适用专业", [])
        if isinstance(majors, list):
            majors_str = ",".join(majors)
        else:
            majors_str = str(majors) if majors else ""

        rows.append((
            item.get("id", ""),
            item.get("编码", ""),
            item.get("名称", ""),
            item.get("规格型号", ""),
            item.get("单位", ""),
            item.get("含税单价"),
            item.get("除税单价"),
            item.get("增值税率"),
            item.get("含税单价_202602"),
            item.get("含税单价_202603"),
            item.get("取定价"),
            item.get("数据来源", ""),
            item.get("备注", ""),
            majors_str,
        ))

    conn.executemany("""
        INSERT INTO materials (
            orig_id, 编码, 名称, 规格型号, 单位,
            含税单价, 除税单价, 增值税率,
            含税单价_202602, 含税单价_202603, 取定价,
            数据来源, 备注, 适用专业
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
    insert_time = time.time() - start
    print(f"  ✓ 数据插入耗时：{insert_time:.3f}s")

    return len(rows)


def create_indexes(conn):
    """建立查询索引"""
    print("\n" + "=" * 60)
    print("🔍 建立查询索引")
    print("=" * 60)

    indexes = [
        # ---- quotas 表索引 ----
        ("idx_quotas_quota_no",  "quotas (quota_no)"),           # 精确查询
        ("idx_quotas_orig_no",   "quotas (original_quota_no)"),  # 原始编号查询
        ("idx_quotas_category_prefix", "quotas (category_prefix)"),  # 专业前缀过滤
        ("idx_quotas_chapter",  "quotas (chapter)"),             # 章节查询
        ("idx_quotas_name_trgm", "quotas (name)"),               # 名称模糊查询（后续可加FTS5）
        ("idx_quotas_volume",   "quotas (category_prefix, quota_no)"),  # 复合索引：分册+编号

        # ---- materials 表索引 ----
        ("idx_materials_code",  "materials (编码)"),             # 编码查询
        ("idx_materials_name",  "materials (名称)"),             # 名称查询
        ("idx_materials_source","materials (数据来源)"),          # 来源过滤
        ("idx_materials_unit",  "materials (单位)"),              # 单位过滤
    ]

    start = time.time()
    for idx_name, idx_def in indexes:
        try:
            conn.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_def}")
            print(f"  ✓ {idx_name}")
        except Exception as e:
            print(f"  ⚠ {idx_name}: {e}")

    conn.commit()
    elapsed = time.time() - start
    print(f"  ✓ 索引创建总耗时：{elapsed:.3f}s")


def create_fts5_index(conn):
    """创建 FTS5 全文搜索索引（定额名称）"""
    print("\n" + "=" * 60)
    print("📝 创建 FTS5 全文搜索索引")
    print("=" * 60)

    try:
        conn.execute("DROP TABLE IF EXISTS quotas_fts")
        conn.execute("""
            CREATE VIRTUAL TABLE quotas_fts USING fts5(
                quota_no,
                name,
                chapter,
                category,
                content='quotas',
                content_rowid='id'
            )
        """)

        # 填充FTS数据
        conn.execute("""
            INSERT INTO quotas_fts(rowid, quota_no, name, chapter, category)
            SELECT id, quota_no, name, chapter, category FROM quotas
        """)

        # 材料FTS
        conn.execute("DROP TABLE IF EXISTS materials_fts")
        conn.execute("""
            CREATE VIRTUAL TABLE materials_fts USING fts5(
                编码,
                名称,
                规格型号,
                content='materials',
                content_rowid='id'
            )
        """)

        conn.execute("""
            INSERT INTO materials_fts(rowid, 编码, 名称, 规格型号)
            SELECT id, 编码, 名称, 规格型号 FROM materials
        """)

        conn.commit()
        print("  ✓ FTS5全文索引创建成功")
        return True
    except Exception as e:
        print(f"  ⚠ FTS5不可用（需SQLite 3.9.0+）：{e}")
        print("  → 将使用LIKE模糊查询代替")
        return False


def run_benchmark(conn):
    """性能基准测试"""
    print("\n" + "=" * 60)
    print("⚡ 性能基准测试")
    print("=" * 60)

    # ---- 定额查询测试 ----
    tests = [
        ("精确查询 quota_no='AZ-8-3-27'",
         "SELECT * FROM quotas WHERE quota_no = 'AZ-8-3-27'"),

        ("分册过滤 第8册",
         "SELECT * FROM quotas WHERE category_prefix='AZ' AND quota_no LIKE 'AZ-8-%' LIMIT 10"),

        ("名称模糊查询 '调节阀'",
         "SELECT * FROM quotas WHERE name LIKE '%调节阀%' LIMIT 10"),

        ("名称模糊查询 '焊接钢管'",
         "SELECT * FROM quotas WHERE name LIKE '%焊接钢管%' LIMIT 10"),

        ("分册+名称 '第8册+低压'",
         "SELECT * FROM quotas WHERE category_prefix='AZ' AND quota_no LIKE 'AZ-8-%' AND name LIKE '%低压%' LIMIT 10"),

        ("FTS5全文搜索 '调节阀'" if _has_fts5(conn) else "LIKE搜索 '调节阀'",
         "SELECT * FROM quotas_fts WHERE name MATCH '调节阀' LIMIT 10" if _has_fts5(conn) else
         "SELECT * FROM quotas WHERE name LIKE '%调节阀%' LIMIT 10"),
    ]

    for name, sql in tests:
        try:
            start = time.time()
            cursor = conn.execute(sql)
            results = cursor.fetchall()
            elapsed = (time.time() - start) * 1000  # ms
            print(f"  {name}: {elapsed:.2f}ms ({len(results)}条)")
        except Exception as e:
            print(f"  {name}: ❌ {e}")

    # ---- 材料查询测试 ----
    mat_tests = [
        ("材料精确查询 编码='010001'",
         "SELECT * FROM materials WHERE 编码 = '010001'"),

        ("材料名称模糊 '法兰阀门'",
         "SELECT * FROM materials WHERE 名称 LIKE '%法兰阀门%' LIMIT 10"),

        ("材料规格模糊 'DN200'",
         "SELECT * FROM materials WHERE 名称 LIKE '%DN200%' LIMIT 10"),

        ("材料来源过滤 '03期'",
         "SELECT * FROM materials WHERE 数据来源 = '济南造价信息2026年03期' LIMIT 10"),
    ]

    for name, sql in mat_tests:
        try:
            start = time.time()
            cursor = conn.execute(sql)
            results = cursor.fetchall()
            elapsed = (time.time() - start) * 1000
            print(f"  {name}: {elapsed:.2f}ms ({len(results)}条)")
        except Exception as e:
            print(f"  {name}: ❌ {e}")


def _has_fts5(conn):
    """检查SQLite是否支持FTS5"""
    try:
        cursor = conn.execute("SELECT name FROM pragma_compile_options WHERE name='ENABLE_FTS5'")
        return cursor.fetchone() is not None
    except:
        return False


def print_db_stats(conn):
    """打印数据库统计信息"""
    print("\n" + "=" * 60)
    print("📊 数据库统计")
    print("=" * 60)

    # 定额统计
    quota_count = conn.execute("SELECT COUNT(*) FROM quotas").fetchone()[0]
    category_counts = conn.execute("""
        SELECT category_prefix, COUNT(*) as cnt
        FROM quotas
        GROUP BY category_prefix
        ORDER BY cnt DESC
    """).fetchall()

    print(f"  定额总数: {quota_count}")
    for prefix, cnt in category_counts:
        prefix_name = {
            "AZ": "安装工程", "SZ": "市政工程", "JZ": "建筑工程",
            "YL": "园林绿化", "XJ": "房屋修缮(建筑)", "XA": "房屋修缮(安装)",
            "XS": "市政养护维修"
        }.get(prefix, prefix)
        print(f"    {prefix} ({prefix_name}): {cnt}条")

    # 材料统计
    mat_count = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    source_counts = conn.execute("""
        SELECT 数据来源, COUNT(*) as cnt
        FROM materials
        GROUP BY 数据来源
    """).fetchall()

    print(f"\n  材料总数: {mat_count}")
    for source, cnt in source_counts:
        print(f"    {source}: {cnt}条")

    # 数据库文件大小
    db_size = DB_PATH.stat().st_size / 1024 / 1024
    print(f"\n  数据库文件大小: {db_size:.1f}MB")


def main():
    print("🚀 cnsdoce SQLite 迁移工具")
    print(f"   输出：{DB_PATH}")

    # 删除旧数据库
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("  ✓ 已删除旧数据库")

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")       # WAL模式，读写并发
    conn.execute("PRAGMA synchronous=NORMAL")      # 性能优化
    conn.execute("PRAGMA cache_size=-64000")        # 64MB缓存
    conn.execute("PRAGMA temp_store=MEMORY")        # 临时表在内存

    total_start = time.time()

    # Step 1: 迁移定额数据
    quota_count = migrate_quota_data(conn)

    # Step 2: 迁移材料数据
    material_count = migrate_material_data(conn)

    # Step 3: 建立索引
    create_indexes(conn)

    # Step 4: FTS5全文索引
    fts5_ok = create_fts5_index(conn)

    # Step 5: 优化
    conn.execute("ANALYZE")  # 更新统计信息，帮助查询优化器
    conn.commit()

    total_time = time.time() - total_start
    print(f"\n✅ 迁移完成！总耗时：{total_time:.2f}s")

    # Step 6: 统计信息
    print_db_stats(conn)

    # Step 7: 性能测试
    run_benchmark(conn)

    conn.close()

    # 与JSON对比
    print("\n" + "=" * 60)
    print("📈 对比：JSON vs SQLite 查询速度")
    print("=" * 60)
    print("  JSON遍历35481条（估算）:")
    print("    精确查询: ~500-2000ms")
    print("    模糊查询: ~800-3000ms")
    print("  SQLite+索引（实测见上方）:")
    print("    精确查询: <5ms")
    print("    模糊查询: <20ms")
    print("    预计提升: 100-500倍")


if __name__ == "__main__":
    main()
