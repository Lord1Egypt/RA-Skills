#!/usr/bin/env python3
"""
查询用户最近登录记录
包含登录IP、时间、设备、地理位置等信息
"""

import sys
import pymysql
import json
from datetime import datetime

def query_user_login_logs(user_id):
    """查询用户最近登录记录"""
    
    # 数据库配置
    db_config = {
        'host': 'rr-wz97dxha81orq30j0eo.mysql.rds.aliyuncs.com',
        'port': 3389,
        'user': 'oc_gw',
        'password': 'm83KkZVLQp2Wg7HgDVb5cRjQ',
        'database': 'yc_db',
        'charset': 'utf8mb4'
    }
    
    try:
        # 连接数据库
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 查询用户最近登录记录
        sql = """
        SELECT DISTINCT(l.ip),
            loginTime,
            u.userId,
            deviceId,
            u.id,
            l.appId,
            l.channel,
            u.truename,
            l.loginId,
            a.`name` as appName,
            l.loginMethod,
            c.provice,
            c.city,
            l.fversion
        FROM t_user_loginlogs_2022 l
        INNER JOIN t_user u ON l.userId = u.id
        INNER JOIN t_sys_app a ON a.`code` = l.appId
        INNER JOIN t_ip_config c ON c.id = INET_ATON(l.ip)
        WHERE u.userId = %s
        ORDER BY loginTime DESC
        LIMIT 10
        """
        
        cursor.execute(sql, (user_id,))
        logs = cursor.fetchall()
        
        if not logs:
            return {
                "userId": user_id,
                "status": "no_records",
                "message": "未找到该用户的登录记录"
            }
        
        # 格式化结果
        result = {
            "userId": user_id,
            "status": "success",
            "total_records": len(logs),
            "login_logs": []
        }
        
        for log in logs:
            log_info = {
                "loginTime": log['loginTime'].strftime('%Y-%m-%d %H:%M:%S') if log['loginTime'] else '未知',
                "ip": log['ip'],
                "地理位置": f"{log['provice']} {log['city']}".strip(),
                "deviceId": log['deviceId'] if log['deviceId'] else '未知',
                "应用": log['appName'] if log['appName'] else '未知',
                "appId": log['appId'],
                "渠道": log['channel'] if log['channel'] else '未知',
                "登录方式": get_login_method(log['loginMethod']),
                "版本": log['fversion'] if log['fversion'] else '未知'
            }
            result['login_logs'].append(log_info)
        
        # 统计IP分布
        ip_counter = {}
        for log in logs:
            ip = log['ip']
            if ip not in ip_counter:
                ip_counter[ip] = {
                    "count": 0,
                    "location": f"{log['provice']} {log['city']}".strip()
                }
            ip_counter[ip]["count"] += 1
        
        result['ip_statistics'] = ip_counter
        
        cursor.close()
        conn.close()
        
        return result
        
    except Exception as e:
        import traceback
        return {
            "userId": user_id,
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }

def get_login_method(method):
    """获取登录方式描述"""
    if method == 1:
        return "密码登录"
    elif method == 2:
        return "验证码登录"
    elif method == 3:
        return "第三方登录"
    elif method == 4:
        return "自动登录"
    else:
        return f"未知({method})"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_user_login_logs.py <userId>")
        print("Example: python3 query_user_login_logs.py 124BAA0")
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = query_user_login_logs(user_id)
    
    # 美化输出
    if result['status'] == 'success':
        print('=' * 80)
        print(f'用户最近登录记录 - {user_id}')
        print('=' * 80)
        print(f'总记录数: {result["total_records"]} 条')
        print()
        
        print('【登录详情】')
        for i, log in enumerate(result['login_logs'], 1):
            print(f'{i}. 登录时间: {log["loginTime"]}')
            print(f'   IP地址: {log["ip"]}')
            print(f'   地理位置: {log["地理位置"]}')
            print(f'   设备ID: {log["deviceId"]}')
            print(f'   应用: {log["应用"]} ({log["appId"]})')
            print(f'   渠道: {log["渠道"]}')
            print(f'   登录方式: {log["登录方式"]}')
            print(f'   版本: {log["版本"]}')
            print()
        
        print('【IP分布统计】')
        for ip, stats in result['ip_statistics'].items():
            print(f'  {ip}: {stats["count"]} 次 ({stats["location"]})')
        print()
        
        print('=' * 80)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))