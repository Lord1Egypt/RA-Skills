#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Validation and Integrity Check for XI Stock System
羲股票监控系统数据验证与完整性检查

This script validates data integrity and checks for issues in the stock database and data files.
本脚本验证数据完整性并检查股票数据库和数据文件的问题。
"""

import os
import sys
import sqlite3
import json
import csv
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

def get_db_connection():
    """Get database connection"""
    if not os.path.exists(DB_PATH):
        print(f"- 数据库未找到: {DB_PATH}")
        print("  请先运行 init_db.py 和 fetch_stocks.py!")
        exit(1)
    return sqlite3.connect(DB_PATH)

def check_database_integrity():
    """Check database integrity and structure"""
    print("=" * 70)
    print("数据库完整性检查")
    print("=" * 70)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    issues = []
    
    try:
        # 1. Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stocks'")
        if not cursor.fetchone():
            issues.append("❌ 表 'stocks' 不存在")
        else:
            print("✅ 表 'stocks' 存在")
        
        # 2. Check table structure
        cursor.execute("PRAGMA table_info(stocks)")
        columns = [row[1] for row in cursor.fetchall()]
        required_columns = ['code', 'name', 'market', 'day_get', 'week_get', 'month_get', 'status', 'created_at']
        
        for col in required_columns:
            if col not in columns:
                issues.append(f"❌ 缺少列: {col}")
            else:
                print(f"✅ 列 '{col}' 存在")
        
        # 3. Check total records
        cursor.execute("SELECT COUNT(*) FROM stocks")
        total = cursor.fetchone()[0]
        print(f"📊 总股票记录: {total}")
        
        if total == 0:
            issues.append("⚠️  数据库中没有股票记录")
        
        # 4. Check active stocks
        cursor.execute("SELECT COUNT(*) FROM stocks WHERE status = 'active'")
        active = cursor.fetchone()[0]
        print(f"📈 活跃股票: {active} ({active/total*100:.1f}%)")
        
        # 5. Check timestamp fields
        timestamp_fields = ['day_get', 'week_get', 'month_get']
        for field in timestamp_fields:
            cursor.execute(f"SELECT COUNT(*) FROM stocks WHERE {field} IS NOT NULL")
            updated = cursor.fetchone()[0]
            print(f"🕒 {field}: {updated} 已更新 ({updated/total*100:.1f}%)")
        
        # 6. Check for duplicate codes
        cursor.execute("SELECT code, COUNT(*) FROM stocks GROUP BY code HAVING COUNT(*) > 1")
        duplicates = cursor.fetchall()
        if duplicates:
            for code, count in duplicates:
                issues.append(f"❌ 重复股票代码: {code} (出现 {count} 次)")
        else:
            print("✅ 无重复股票代码")
        
        # 7. Check for invalid market codes
        cursor.execute("SELECT DISTINCT market FROM stocks")
        markets = [row[0] for row in cursor.fetchall()]
        print(f"🏢 市场类型: {', '.join(markets)}")
        
        invalid_markets = [m for m in markets if m not in ['00', '30', '60']]
        if invalid_markets:
            issues.append(f"❌ 无效市场类型: {invalid_markets}")
        
    except Exception as e:
        issues.append(f"❌ 数据库检查错误: {e}")
    finally:
        conn.close()
    
    return issues

def check_data_files(frequency):
    """Check data files for specific frequency"""
    print(f"\n{'='*70}")
    print(f"{frequency}线数据文件检查")
    print(f"{'='*70}")
    
    data_dir = DATA_DIRS.get(frequency)
    if not data_dir or not os.path.exists(data_dir):
        return [f"❌ 数据目录不存在: {data_dir or frequency}"]
    
    issues = []
    
    try:
        # Count files
        files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
        print(f"📁 数据文件数量: {len(files)}")
        
        if len(files) == 0:
            issues.append(f"⚠️  {frequency}线数据目录为空")
            return issues
        
        # Check first 5 files for format
        sample_files = files[:5] if len(files) > 5 else files
        for filename in sample_files:
            filepath = os.path.join(data_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    # Check header
                    header = f.readline().strip()
                    if header != "date,open,close,high,low,change_pct":
                        issues.append(f"❌ 文件头格式错误: {filename}")
                        continue
                    
                    # Check data lines
                    lines = f.readlines()
                    if not lines:
                        issues.append(f"⚠️  空数据文件: {filename}")
                        continue
                    
                    # Check line format
                    for i, line in enumerate(lines[:10], 1):  # Check first 10 lines
                        parts = line.strip().split(',')
                        if len(parts) != 6:
                            issues.append(f"❌ 数据行格式错误 {filename}:{i}")
                            break
                        
                        # Check if values can be parsed
                        try:
                            date_str = parts[0]
                            float(parts[1])  # open
                            float(parts[2])  # close
                            float(parts[3])  # high
                            float(parts[4])  # low
                            float(parts[5])  # change_pct
                        except ValueError:
                            issues.append(f"❌ 数据值解析错误 {filename}:{i}")
                            break
                
                print(f"✅ 文件检查通过: {filename}")
                
            except Exception as e:
                issues.append(f"❌ 文件读取错误 {filename}: {e}")
        
        # Check file naming consistency
        for filename in files[:20]:  # Check first 20 files
            if '_' not in filename:
                issues.append(f"❌ 文件名格式错误: {filename}")
                break
        
        print(f"✅ 文件命名格式检查通过")
        
    except Exception as e:
        issues.append(f"❌ 数据文件检查错误: {e}")
    
    return issues

def check_database_files_sync():
    """Check synchronization between database and data files"""
    print(f"\n{'='*70}")
    print("数据库与文件同步检查")
    print(f"{'='*70}")
    
    issues = []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get all active stocks from database
        cursor.execute("SELECT code, name FROM stocks WHERE status = 'active'")
        db_stocks = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Check each frequency directory
        for frequency, data_dir in DATA_DIRS.items():
            if not os.path.exists(data_dir):
                print(f"⚠️  目录不存在: {data_dir}")
                continue
            
            files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
            file_codes = set()
            
            for filename in files:
                # Extract code from filename (format: 名称_代码.txt)
                try:
                    if '_' in filename:
                        code = filename.split('_')[-1].replace('.txt', '')
                        file_codes.add(code)
                except:
                    pass
            
            # Find missing files
            missing_files = set(db_stocks.keys()) - file_codes
            if missing_files:
                sample_missing = list(missing_files)[:5]
                issues.append(f"⚠️  {frequency}线缺失文件: {len(missing_files)} 只股票 (示例: {', '.join(sample_missing)})")
            
            # Find extra files (not in database)
            extra_files = file_codes - set(db_stocks.keys())
            if extra_files:
                sample_extra = list(extra_files)[:5]
                issues.append(f"⚠️  {frequency}线多余文件: {len(extra_files)} 个文件 (示例: {', '.join(sample_extra)})")
            
            print(f"📊 {frequency}线: 数据库 {len(db_stocks)} 只股票, 文件 {len(files)} 个")
        
    except Exception as e:
        issues.append(f"❌ 同步检查错误: {e}")
    finally:
        conn.close()
    
    return issues

def check_timestamp_consistency():
    """Check timestamp consistency and freshness"""
    print(f"\n{'='*70}")
    print("时间戳一致性检查")
    print(f"{'='*70}")
    
    issues = []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        current_time = datetime.now()
        
        # Check each timestamp field
        timestamp_fields = [
            ('day_get', '日线', timedelta(days=1)),
            ('week_get', '周线', timedelta(days=7)),
            ('month_get', '月线', timedelta(days=30))
        ]
        
        for field, name, threshold in timestamp_fields:
            # Get oldest timestamp
            cursor.execute(f"""
                SELECT code, name, {field} 
                FROM stocks 
                WHERE {field} IS NOT NULL 
                ORDER BY {field} ASC 
                LIMIT 5
            """)
            oldest = cursor.fetchall()
            
            if oldest:
                oldest_date = datetime.strptime(oldest[0][2], '%Y-%m-%d %H:%M:%S')
                age_days = (current_time - oldest_date).days
                
                print(f"📅 {name}最旧数据: {oldest[0][0]} {oldest[0][1]} ({oldest_date})")
                print(f"   数据年龄: {age_days} 天")
                
                if age_days > threshold.days:
                    issues.append(f"⚠️  {name}数据过旧: {age_days} 天")
            
            # Count stocks needing update
            cursor.execute(f"SELECT COUNT(*) FROM stocks WHERE {field} IS NULL OR {field} < ?", 
                          (current_time - threshold,))
            need_update = cursor.fetchone()[0]
            
            print(f"🔄 需要更新{name}: {need_update} 只股票")
        
    except Exception as e:
        issues.append(f"❌ 时间戳检查错误: {e}")
    finally:
        conn.close()
    
    return issues

def generate_report(issues):
    """Generate validation report"""
    print(f"\n{'='*70}")
    print("验证报告")
    print(f"{'='*70}")
    
    if not issues:
        print("🎉 所有检查通过！系统健康状态良好。")
        return True
    
    print(f"发现 {len(issues)} 个问题:")
    print("-" * 70)
    
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
    
    print("-" * 70)
    
    # Categorize issues
    critical = [i for i in issues if i.startswith('❌')]
    warning = [i for i in issues if i.startswith('⚠️')]
    
    if critical:
        print(f"❌ 严重问题: {len(critical)} 个")
        print("   建议立即处理这些问题")
    
    if warning:
        print(f"⚠️  警告: {len(warning)} 个")
        print("   建议在方便时处理这些警告")
    
    return len(critical) == 0

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Data Validation and Integrity Check for XI Stock System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  data_validation.py all          - 运行所有检查
  data_validation.py db          - 只检查数据库
  data_validation.py files       - 只检查数据文件
  data_validation.py sync        - 检查数据库与文件同步
  data_validation.py timestamps  - 检查时间戳一致性
        """
    )
    
    parser.add_argument('check_type', 
                       choices=['all', 'db', 'files', 'sync', 'timestamps'],
                       default='all',
                       help='检查类型')
    
    args = parser.parse_args()
    
    all_issues = []
    
    try:
        if args.check_type in ['all', 'db']:
            issues = check_database_integrity()
            all_issues.extend(issues)
        
        if args.check_type in ['all', 'files']:
            for frequency in ['day', 'week', 'month']:
                issues = check_data_files(frequency)
                all_issues.extend(issues)
        
        if args.check_type in ['all', 'sync']:
            issues = check_database_files_sync()
            all_issues.extend(issues)
        
        if args.check_type in ['all', 'timestamps']:
            issues = check_timestamp_consistency()
            all_issues.extend(issues)
        
        # Generate final report
        is_healthy = generate_report(all_issues)
        
        # Save report to file
        report_file = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"XI Stock System Validation Report\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"检查类型: {args.check_type}\n")
            f.write(f"发现问题: {len(all_issues)} 个\n\n")
            
            if all_issues:
                f.write("问题列表:\n")
                for i, issue in enumerate(all_issues, 1):
                    f.write(f"{i}. {issue}\n")
            else:
                f.write("✅ 所有检查通过，系统健康状态良好。\n")
        
        print(f"\n📄 报告已保存: {report_file}")
        
        if not is_healthy:
            print(f"\n⚠️  系统存在严重问题，建议运行修复脚本:")
            print("   python data_repair.py --fix-all")
            return 1
        
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