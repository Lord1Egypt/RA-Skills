#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Repair Tool for XI Stock System
羲股票监控系统数据修复工具

This script repairs common issues found in the stock database and data files.
本脚本修复股票数据库和数据文件中发现的常见问题。
"""

import os
import sys
import sqlite3
import shutil
from datetime import datetime, timedelta
import argparse

# Fix encoding for Windows console
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configuration
DB_PATH = "D:\\xistock\\stock.db"
DATA_DIRS = {
    "day": "D:\\xistock\\day",
    "week": "D:\\xistock\\week",
    "month": "D:\\xistock\\month"
}
BACKUP_DIR = "D:\\xistock\\backup"

def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DB_PATH):
        print(f"- 数据库未找到: {DB_PATH}")
        print("  请先运行 init_db.py 和 fetch_stocks.py!")
        exit(1)
    return sqlite3.connect(DB_PATH)

def create_backup():
    """Create backup of database before repair"""
    print("=" * 70)
    print("创建数据库备份")
    print("=" * 70)
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f"stock_backup_{timestamp}.db")
    
    try:
        shutil.copy2(DB_PATH, backup_file)
        print(f"✅ 数据库备份已创建: {backup_file}")
        print(f"   原始文件: {DB_PATH}")
        print(f"   备份大小: {os.path.getsize(backup_file):,} 字节")
        return backup_file
    except Exception as e:
        print(f"❌ 备份创建失败: {e}")
        return None

def repair_database_structure():
    """Repair database structure issues"""
    print("\n" + "=" * 70)
    print("修复数据库结构")
    print("=" * 70)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    repairs = []
    
    try:
        # 1. Check if table exists, create if not
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stocks'")
        if not cursor.fetchone():
            print("⚠️  表 'stocks' 不存在，正在创建...")
            cursor.execute('''
                CREATE TABLE stocks (
                    code TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    market TEXT NOT NULL,
                    day_get TIMESTAMP,
                    week_get TIMESTAMP,
                    month_get TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            repairs.append("✅ 创建表 'stocks'")
        
        # 2. Check and add missing columns
        cursor.execute("PRAGMA table_info(stocks)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        required_columns = [
            ('code', 'TEXT PRIMARY KEY'),
            ('name', 'TEXT NOT NULL'),
            ('market', 'TEXT NOT NULL'),
            ('day_get', 'TIMESTAMP'),
            ('week_get', 'TIMESTAMP'),
            ('month_get', 'TIMESTAMP'),
            ('status', 'TEXT DEFAULT "active"'),
            ('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
        ]
        
        for col_name, col_type in required_columns:
            if col_name not in existing_columns:
                print(f"⚠️  缺少列 '{col_name}'，正在添加...")
                try:
                    cursor.execute(f"ALTER TABLE stocks ADD COLUMN {col_name} {col_type}")
                    repairs.append(f"✅ 添加列 '{col_name}'")
                except Exception as e:
                    repairs.append(f"❌ 添加列 '{col_name}' 失败: {e}")
        
        # 3. Create indexes if missing
        indexes = [
            ("idx_market", "CREATE INDEX idx_market ON stocks(market)"),
            ("idx_status", "CREATE INDEX idx_status ON stocks(status)"),
            ("idx_day_get", "CREATE INDEX idx_day_get ON stocks(day_get)"),
            ("idx_week_get", "CREATE INDEX idx_week_get ON stocks(week_get)"),
            ("idx_month_get", "CREATE INDEX idx_month_get ON stocks(month_get)")
        ]
        
        for idx_name, idx_sql in indexes:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='index' AND name='{idx_name}'")
            if not cursor.fetchone():
                print(f"⚠️  缺少索引 '{idx_name}'，正在创建...")
                try:
                    cursor.execute(idx_sql)
                    repairs.append(f"✅ 创建索引 '{idx_name}'")
                except Exception as e:
                    repairs.append(f"❌ 创建索引 '{idx_name}' 失败: {e}")
        
        conn.commit()
        
    except Exception as e:
        repairs.append(f"❌ 数据库结构修复错误: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    return repairs

def repair_duplicate_stocks():
    """Remove duplicate stock entries"""
    print("\n" + "=" * 70)
    print("修复重复股票记录")
    print("=" * 70)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    repairs = []
    
    try:
        # Find duplicates
        cursor.execute("""
            SELECT code, COUNT(*) as cnt, 
                   GROUP_CONCAT(rowid) as ids
            FROM stocks 
            GROUP BY code 
            HAVING COUNT(*) > 1
        """)
        
        duplicates = cursor.fetchall()
        
        if not duplicates:
            repairs.append("✅ 无重复股票记录")
            return repairs
        
        print(f"发现 {len(duplicates)} 个重复股票代码")
        
        for code, count, ids in duplicates:
            id_list = ids.split(',')
            keep_id = id_list[0]  # Keep the first record
            delete_ids = id_list[1:]  # Delete the rest
            
            print(f"🔄 处理重复股票: {code} (出现 {count} 次)")
            print(f"   保留记录: {keep_id}")
            print(f"   删除记录: {', '.join(delete_ids)}")
            
            # Delete duplicate records
            placeholders = ','.join(['?'] * len(delete_ids))
            cursor.execute(f"DELETE FROM stocks WHERE rowid IN ({placeholders})", delete_ids)
            
            repairs.append(f"✅ 删除重复股票 {code}: 保留1条，删除{len(delete_ids)}条")
        
        conn.commit()
        
    except Exception as e:
        repairs.append(f"❌ 重复记录修复错误: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    return repairs

def repair_missing_timestamps():
    """Set NULL timestamps for old records"""
    print("\n" + "=" * 70)
    print("修复缺失的时间戳")
    print("=" * 70)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    repairs = []
    current_time = datetime.now()
    
    try:
        # Define thresholds for each frequency
        thresholds = [
            ('day_get', timedelta(days=1)),
            ('week_get', timedelta(days=7)),
            ('month_get', timedelta(days=30))
        ]
        
        for field, threshold in thresholds:
            # Count records with NULL or old timestamps
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM stocks 
                WHERE {field} IS NULL OR {field} < ?
            """, (current_time - threshold,))
            
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"🔄 修复 {field}: {count} 条记录需要更新")
                
                # Set NULL for old timestamps
                cursor.execute(f"""
                    UPDATE stocks 
                    SET {field} = NULL 
                    WHERE {field} < ?
                """, (current_time - threshold,))
                
                repairs.append(f"✅ 修复 {field}: 重置 {count} 条过时记录")
        
        conn.commit()
        
    except Exception as e:
        repairs.append(f"❌ 时间戳修复错误: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    return repairs

def repair_data_files():
    """Repair data file issues"""
    print("\n" + "=" * 70)
    print("修复数据文件")
    print("=" * 70)
    
    repairs = []
    
    for frequency, data_dir in DATA_DIRS.items():
        print(f"\n检查 {frequency}线数据目录: {data_dir}")
        
        if not os.path.exists(data_dir):
            print(f"⚠️  目录不存在，正在创建: {data_dir}")
            os.makedirs(data_dir)
            repairs.append(f"✅ 创建目录: {data_dir}")
            continue
        
        # Check for empty files
        empty_files = []
        corrupted_files = []
        
        for filename in os.listdir(data_dir):
            if not filename.endswith('.txt'):
                continue
            
            filepath = os.path.join(data_dir, filename)
            
            try:
                # Check if file is empty
                if os.path.getsize(filepath) == 0:
                    empty_files.append(filename)
                    continue
                
                # Check file content
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    if len(lines) < 2:  # Less than header + 1 data line
                        corrupted_files.append(filename)
                    else:
                        # Check header
                        if lines[0].strip() != "date,open,close,high,low,change_pct":
                            corrupted_files.append(filename)
            
            except Exception:
                corrupted_files.append(filename)
        
        # Report and repair
        if empty_files:
            print(f"⚠️  发现 {len(empty_files)} 个空文件")
            for filename in empty_files[:5]:  # Show first 5
                print(f"   - {filename}")
            
            # Option to delete empty files
            if len(empty_files) > 0:
                repair = input(f"\n删除 {len(empty_files)} 个空文件? (y/n): ")
                if repair.lower() == 'y':
                    for filename in empty_files:
                        filepath = os.path.join(data_dir, filename)
                        os.remove(filepath)
                    repairs.append(f"✅ 删除 {len(empty_files)} 个空文件 ({frequency}线)")
        
        if corrupted_files:
            print(f"⚠️  发现 {len(corrupted_files)} 个损坏文件")
            for filename in corrupted_files[:5]:
                print(f"   - {filename}")
            
            # Option to delete corrupted files
            if len(corrupted_files) > 0:
                repair = input(f"\n删除 {len(corrupted_files)} 个损坏文件? (y/n): ")
                if repair.lower() == 'y':
                    for filename in corrupted_files:
                        filepath = os.path.join(data_dir, filename)
                        os.remove(filepath)
                    repairs.append(f"✅ 删除 {len(corrupted_files)} 个损坏文件 ({frequency}线)")
        
        if not empty_files and not corrupted_files:
            repairs.append(f"✅ {frequency}线数据文件正常")
    
    return repairs

def sync_database_with_files():
    """Sync database with existing data files"""
    print("\n" + "=" * 70)
    print("同步数据库与数据文件")
    print("=" * 70)
    
    repairs = []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get all stocks from database
        cursor.execute("SELECT code, name FROM stocks WHERE status = 'active'")
        db_stocks = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Check each frequency directory
        for frequency, data_dir in DATA_DIRS.items():
            if not os.path.exists(data_dir):
                continue
            
            files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
            file_codes = set()
            
            for filename in files:
                # Extract code from filename
                try:
                    if '_' in filename:
                        code = filename.split('_')[-1].replace('.txt', '')
                        file_codes.add(code)
                except:
                    pass
            
            # Find stocks in database but missing files
            missing_files = set(db_stocks.keys()) - file_codes
            
            if missing_files:
                print(f"🔄 {frequency}线: {len(missing_files)} 只股票缺少数据文件")
                
                # Mark these stocks as needing update
                placeholders = ','.join(['?'] * len(missing_files))
                cursor.execute(f"""
                    UPDATE stocks 
                    SET {frequency}_get = NULL 
                    WHERE code IN ({placeholders})
                """, list(missing_files))
                
                repairs.append(f"✅ 标记 {len(missing_files)} 只股票需要更新{frequency}线数据")
        
        conn.commit()
        
    except Exception as e:
        repairs.append(f"❌ 同步修复错误: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    return repairs

def generate_repair_report(repairs, backup_file=None):
    """Generate repair report"""
    print("\n" + "=" * 70)
    print("修复报告")
    print("=" * 70)
    
    if backup_file:
        print(f"📂 备份文件: {backup_file}")
    
    if not repairs:
        print("✅ 无需修复，系统状态良好")
        return
    
    print(f"完成 {len(repairs)} 项修复:")
    print("-" * 70)
    
    for i, repair in enumerate(repairs, 1):
        print(f"{i}. {repair}")
    
    print("-" * 70)
    
    successful = len([r for r in repairs if r.startswith('✅')])
    failed = len([r for r in repairs if r.startswith('❌')])
    
    print(f"✅ 成功: {successful} 项")
    if failed > 0:
        print(f"❌ 失败: {failed} 项")
    
    # Save report
    report_file = f"repair_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"XI Stock System Repair Report\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"备份文件: {backup_file or '无'}\n")
        f.write(f"修复项数: {len(repairs)}\n\n")
        
        if repairs:
            f.write("修复记录:\n")
            for i, repair in enumerate(repairs, 1):
                f.write(f"{i}. {repair}\n")
        
        f.write(f"\n总结:\n")
        f.write(f"  成功: {successful} 项\n")
        f.write(f"  失败: {failed} 项\n")
    
    print(f"\n📄 修复报告已保存: {report_file}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Data Repair Tool for XI Stock System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  data_repair.py --fix-all          - 修复所有问题（推荐）
  data_repair.py --fix-db           - 只修复数据库问题
  data_repair.py --fix-files        - 只修复数据文件问题
  data_repair.py --fix-timestamps   - 只修复时间戳问题
  data_repair.py --fix-duplicates   - 只修复重复记录
  
安全提示:
  1. 修复前会自动创建数据库备份
  2. 数据文件修复需要确认
  3. 建议先运行 data_validation.py 检查问题
        """
    )
    
    parser.add_argument('--fix-all', action='store_true',
                       help='修复所有问题')
    parser.add_argument('--fix-db', action='store_true',
                       help='修复数据库结构问题')
    parser.add_argument('--fix-files', action='store_true',
                       help='修复数据文件问题')
    parser.add_argument('--fix-timestamps', action='store_true',
                       help='修复时间戳问题')
    parser.add_argument('--fix-duplicates', action='store_true',
                       help='修复重复记录问题')
    parser.add_argument('--fix-sync', action='store_true',
                       help='修复数据库与文件同步问题')
    parser.add_argument('--no-backup', action='store_true',
                       help='不创建备份（不推荐）')
    
    args = parser.parse_args()
    
    # If no specific fix specified, default to all
    if not any([args.fix_all, args.fix_db, args.fix_files, 
                args.fix_timestamps, args.fix_duplicates, args.fix_sync]):
        args.fix_all = True
    
    all_repairs = []
    
    try:
        print("=" * 70)
        print("XI Stock System Data Repair Tool")
        print("羲股票监控系统数据修复工具")
        print("=" * 70)
        
        # Create backup unless disabled
        backup_file = None
        if not args.no_backup:
            backup_file = create_backup()
            if not backup_file:
                print("⚠️  备份失败，继续修复? (y/n): ")
                if input().lower() != 'y':
                    return 1
        else:
            print("⚠️  警告: 未创建备份，直接进行修复")
            confirm = input("继续? (y/n): ")
            if confirm.lower() != 'y':
                return 1
        
        # Perform repairs based on arguments
        if args.fix_all or args.fix_db:
            repairs = repair_database_structure()
            all_repairs.extend(repairs)
        
        if args.fix_all or args.fix_duplicates:
            repairs = repair_duplicate_stocks()
            all_repairs.extend(repairs)
        
        if args.fix_all or args.fix_timestamps:
            repairs = repair_missing_timestamps()
            all_repairs.extend(repairs)
        
        if args.fix_all or args.fix_files:
            repairs = repair_data_files()
            all_repairs.extend(repairs)
        
        if args.fix_all or args.fix_sync:
            repairs = sync_database_with_files()
            all_repairs.extend(repairs)
        
        # Generate report
        generate_repair_report(all_repairs, backup_file)
        
        print("\n🎉 修复完成!")
        print("建议运行以下命令验证修复效果:")
        print("  python data_validation.py all")
        
    except KeyboardInterrupt:
        print("\n\n- 用户中断")
        return 1
    except Exception as e:
        print(f"\n- 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())