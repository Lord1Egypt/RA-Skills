#!/usr/bin/env python3

import re
import sys

def validate_table_name(table_name: str) -> bool:
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    if not re.match(pattern, table_name):
        print(f"Error: Invalid table name: {table_name}", file=sys.stderr)
        return False
    return True


"""
数据合规检查脚本
支持敏感数据检测、隐私合规、访问控制检查
Usage: 
  python compliance_check.py --table users --db sqlite:///data.db
  python compliance_check.py --table users --db mysql://user:pass@localhost:3306/db --check-type all
"""

import argparse
import json
from typing import Dict, List, Any, Set
from urllib.parse import urlparse


# 敏感字段模式
SENSITIVE_PATTERNS = {
    'password': '密码',
    'pwd': '密码',
    'passwd': '密码',
    'secret': '密钥',
    'token': '令牌',
    'api_key': 'API密钥',
    'apikey': 'API密钥',
    'access_token': '访问令牌',
    'refresh_token': '刷新令牌',
    'session_id': '会话ID',
    'cookie': 'Cookie',
    'auth': '认证信息',
    
    # 个人信息
    'ssn': '身份证号',
    'social_security': '社保号',
    'id_card': '身份证',
    'card_no': '卡号',
    'bank_card': '银行卡号',
    'credit_card': '信用卡号',
    'cvv': 'CVV',
    'security_code': '安全码',
    
    # 联系信息
    'phone': '电话',
    'mobile': '手机',
    'tel': '电话',
    'email': '邮箱',
    'address': '地址',
    'ip': 'IP地址',
    'ip_address': 'IP地址',
    
    # 金融信息
    'salary': '薪资',
    'income': '收入',
    'bank': '银行',
    'account': '账户',
    'balance': '余额',
    
    # 健康信息
    'medical': '医疗',
    'health': '健康',
    'disease': '疾病',
    'diagnosis': '诊断',
    
    # 生物识别
    'biometric': '生物识别',
    'fingerprint': '指纹',
    'face': '人脸',
    'voice': '声纹',
}

# 必需脱敏字段
MASK_FIELDS = {
    'password': '******',
    'token': '****',
    'ssn': '***-**-****',
    'id_card': '**************1234',
    'phone': '138****1234',
    'email': 'a***@domain.com',
    'bank_card': '**** **** **** 1234',
}


def parse_connection_string(conn_str: str) -> Dict[str, str]:
    if conn_str.startswith('sqlite'):
        return {'type': 'sqlite', 'path': conn_str.replace('sqlite:///', '')}
    
    parsed = urlparse(conn_str)
    return {
        'type': parsed.scheme,
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or (3306 if parsed.scheme == 'mysql' else 5432),
        'user': parsed.username or 'root',
        'password': parsed.password or '',
        'database': parsed.path.lstrip('/') if parsed.path else ''
    }


def get_connection(conn_str: str):
    config = parse_connection_string(conn_str)
    
    if config['type'] == 'sqlite':
        import sqlite3
        return sqlite3.connect(config['path'])
    
    elif config['type'] in ('mysql', 'mysql+pymysql'):
        import pymysql
        return pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            cursorclass=pymysql.cursors.DictCursor
        )
    
    elif config['type'] in ('postgresql', 'postgres'):
        import psycopg2
        return psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
    
    else:
        raise ValueError(f"Unsupported database: {config['type']}")


def get_table_schema(conn, table_name: str) -> List[Dict]:
    cursor = conn.cursor()
    schema = []
    
    try:
        cursor.execute(f'PRAGMA table_info(`{table_name}`)')
        for row in cursor.fetchall():
            schema.append({
                'name': row[1],
                'type': row[2],
            })
    except:
        pass
    
    if not schema:
        try:
            cursor.execute(f'DESCRIBE `{table_name}`')
            for row in cursor.fetchall():
                schema.append({
                    'name': row['Field'],
                    'type': row['Type'],
                })
        except:
            pass
    
    cursor.close()
    return schema


def detect_sensitive_fields(schema: List[Dict]) -> Dict[str, Any]:
    """检测敏感字段"""
    sensitive_fields = []
    
    for col in schema:
        col_name = col['name'].lower()
        col_type = col.get('type', '').upper()
        
        matched_patterns = []
        for pattern, desc in SENSITIVE_PATTERNS.items():
            if pattern in col_name:
                matched_patterns.append(desc)
        
        if matched_patterns:
            sensitive_fields.append({
                'field': col['name'],
                'type': col.get('type', 'unknown'),
                'patterns': matched_patterns,
                'risk_level': 'HIGH' if 'password' in col_name or 'token' in col_name else 'MEDIUM'
            })
    
    return {
        'total_sensitive': len(sensitive_fields),
        'high_risk': len([f for f in sensitive_fields if f['risk_level'] == 'HIGH']),
        'fields': sensitive_fields
    }


def check_encryption(schema: List[Dict]) -> Dict[str, Any]:
    """检查是否加密存储"""
    encryption_patterns = ['encrypt', 'encrypted', 'hash', 'hashed', 'salt']
    
    unencrypted_sensitive = []
    for col in schema:
        col_name = col['name'].lower()
        
        for pattern in SENSITIVE_PATTERNS:
            if pattern in col_name:
                is_encrypted = any(enc in col_name for enc in encryption_patterns)
                if not is_encrypted:
                    unencrypted_sensitive.append(col['name'])
                break
    
    return {
        'risk': 'HIGH' if unencrypted_sensitive else 'LOW',
        'unencrypted_fields': unencrypted_sensitive,
        'recommendation': '敏感字段应加密存储' if unencrypted_sensitive else '未发现明显风险'
    }


def check_access_control(schema: List[Dict]) -> Dict[str, Any]:
    """检查访问控制相关字段"""
    acl_fields = []
    
    for col in schema:
        col_name = col['name'].lower()
        
        if any(p in col_name for p in ['role', 'permission', 'access', 'privilege', 'level', 'admin']):
            acl_fields.append({
                'field': col['name'],
                'type': col.get('type', 'unknown'),
            })
    
    return {
        'has_acl': len(acl_fields) > 0,
        'fields': acl_fields,
        'recommendation': '建议定期审查访问权限配置' if acl_fields else '未发现访问控制字段，建议添加'
    }


def check_data_retention(schema: List[Dict]) -> Dict[str, Any]:
    """检查数据留存相关字段"""
    retention_fields = []
    
    for col in schema:
        col_name = col['name'].lower()
        
        if any(p in col_name for p in ['created_at', 'updated_at', 'delete_at', 'expire', 'expired', 'valid_until']):
            retention_fields.append({
                'field': col['name'],
                'type': col.get('type', 'unknown'),
            })
    
    return {
        'has_retention_policy': len(retention_fields) > 0,
        'fields': retention_fields,
        'recommendation': '建议配置数据过期策略' if not retention_fields else '数据留存字段已配置'
    }


def check_gdpr_compliance(schema: List[Dict]) -> Dict[str, Any]:
    """GDPR 合规检查"""
    issues = []
    
    # 检查是否有删除相关字段
    has_delete_flag = any(
        'delete' in col['name'].lower() or 'is_deleted' in col['name'].lower() or 'active' in col['name'].lower()
        for col in schema
    )
    
    if not has_delete_flag:
        issues.append('缺少软删除字段（GDPR"被遗忘权"）')
    
    # 检查是否有数据主体标识
    has_subject_id = any(
        'user_id' in col['name'].lower() or 'customer_id' in col['name'].lower()
        for col in schema
    )
    
    if not has_subject_id:
        issues.append('缺少数据主体标识字段')
    
    return {
        'compliant': len(issues) == 0,
        'issues': issues,
        'recommendation': '建议添加数据删除机制和数据主体标识' if issues else '基本符合GDPR要求'
    }


def generate_compliance_report(table_name: str, results: Dict) -> str:
    """生成合规报告"""
    report = f"""## 数据合规检查报告 - {table_name}

### 1. 敏感字段检测
- 敏感字段总数: {results['sensitive']['total_sensitive']}
- 高风险字段: {results['sensitive']['high_risk']}
"""
    
    if results['sensitive']['fields']:
        report += "\n| 字段 | 类型 | 风险等级 | 匹配模式 |\n"
        report += "|------|------|----------|----------|\n"
        for f in results['sensitive']['fields']:
            report += f"| {f['field']} | {f['type']} | {f['risk_level']} | {', '.join(f['patterns'])} |\n"
    
    report += f"""
### 2. 加密存储检查
- 风险等级: {results['encryption']['risk']}
- 未加密字段: {len(results['encryption']['unencrypted_fields'])}
- 建议: {results['encryption']['recommendation']}

### 3. 访问控制检查
- 是否有ACL字段: {'是' if results['access_control']['has_acl'] else '否'}
- 建议: {results['access_control']['recommendation']}

### 4. 数据留存检查
- 是否配置过期策略: {'是' if results['retention']['has_retention_policy'] else '否'}
- 建议: {results['retention']['recommendation']}

### 5. GDPR 合规检查
- 是否合规: {'✅ 是' if results['gdpr']['compliant'] else '❌ 否'}
"""
    
    if results['gdpr']['issues']:
        report += "\n| 问题 |\n"
        report += "|------|\n"
        for issue in results['gdpr']['issues']:
            report += f"| {issue} |\n"
    
    report += f"\n### 建议\n{results['gdpr']['recommendation']}"
    
    return report


def main():
    parser = argparse.ArgumentParser(description='数据合规检查')
    parser.add_argument('--table', required=True, help='表名')
    parser.add_argument('--db-type', required=True, choices=['sqlite', 'mysql', 'postgresql'],
                       help='数据库类型')
    parser.add_argument('--check-type', choices=['all', 'sensitive', 'encryption', 'gdpr'], 
                       default='all', help='检查类型')
    args = parser.parse_args()
    
    # 验证表名
    if not validate_table_name(args.table):
        sys.exit(1)
    
    # 仅从环境变量获取连接
    import os
    conn = None
    try:
        if args.db_type == 'sqlite':
            import sqlite3
            conn = sqlite3.connect(os.getenv('DB_PATH', 'data.db'))
        elif args.db_type == 'mysql':
            import pymysql
            conn = pymysql.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER', ''),
                password=os.getenv('DB_PASS', ''),
                database=os.getenv('DB_NAME', ''),
                cursorclass=pymysql.cursors.DictCursor
            )
        elif args.db_type in ('postgresql', 'postgres'):
            import psycopg2
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 5432)),
                user=os.getenv('DB_USER', ''),
                password=os.getenv('DB_PASS', ''),
                database=os.getenv('DB_NAME', '')
            )
        
        if not conn:
            print("❌ 请设置环境变量: DB_HOST, DB_USER, DB_PASS, DB_NAME", file=sys.stderr)
            sys.exit(1)
        
        print(f"✅ 已连接到数据库")
        
        schema = get_table_schema(conn, args.table)
        print(f"✅ 已获取 {len(schema)} 个字段")
        
        conn.close()
        
        results = {}
        
        if args.check_type in ('all', 'sensitive'):
            results['sensitive'] = detect_sensitive_fields(schema)
        
        if args.check_type in ('all', 'encryption'):
            results['encryption'] = check_encryption(schema)
        
        if args.check_type in ('all', 'gdpr'):
            results['access_control'] = check_access_control(schema)
            results['retention'] = check_data_retention(schema)
            results['gdpr'] = check_gdpr_compliance(schema)
        
        print(generate_compliance_report(args.table, results))
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请安装: pip install pymysql psycopg2-binary")
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == '__main__':
    main()
