#!/usr/bin/env python3
"""
查询用户最近APP访问记录
包含访问时间、设备、IP、渠道等信息
"""

import sys
import pymysql
import json
from datetime import datetime

def query_user_visit_logs(user_id):
    """查询用户最近APP访问记录"""
    
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
        
        # 查询用户最近APP访问记录
        sql = """
        SELECT 
            v.id,
            v.appId,
            v.channel,
            v.version,
            v.deviceId,
            FROM_UNIXTIME(v.visitTime/1000) as visitTime,
            v.ip,
            v.mobileBrand,
            v.saleId
        FROM t_app_visitlog_202204 v
        WHERE v.userId = (SELECT id FROM t_user WHERE userId = %s)
        ORDER BY v.visitTime DESC
        LIMIT 10
        """
        
        cursor.execute(sql, (user_id,))
        logs = cursor.fetchall()
        
        if not logs:
            return {
                "userId": user_id,
                "status": "no_records",
                "message": "未找到该用户的APP访问记录"
            }
        
        # 格式化结果
        result = {
            "userId": user_id,
            "status": "success",
            "total_records": len(logs),
            "visit_logs": []
        }
        
        for log in logs:
            log_info = {
                "id": log['id'],
                "访问时间": log['visitTime'].strftime('%Y-%m-%d %H:%M:%S') if log['visitTime'] else '未知',
                "appId": log['appId'],
                "渠道": log['channel'] if log['channel'] else '未知',
                "版本": log['version'] if log['version'] else '未知',
                "设备ID": log['deviceId'] if log['deviceId'] else '未知',
                "IP地址": log['ip'] if log['ip'] else '未知',
                "手机品牌": log['mobileBrand'] if log['mobileBrand'] else '未知',
                "saleId": log['saleId'] if log['saleId'] else '无'
            }
            result['visit_logs'].append(log_info)
        
        # 统计设备分布
        device_counter = {}
        for log in logs:
            device = log['deviceId'] if log['deviceId'] else '未知'
            if device not in device_counter:
                device_counter[device] = 0
            device_counter[device] += 1
        
        result['device_statistics'] = device_counter
        
        # 统计IP分布
        ip_counter = {}
        for log in logs:
            ip = log['ip'] if log['ip'] else '未知'
            if ip not in ip_counter:
                ip_counter[ip] = 0
            ip_counter[ip] += 1
        
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_user_visit_logs.py <userId>")
        print("Example: python3 query_user_visit_logs.py 124BAA0")
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = query_user_visit_logs(user_id)
    
    # 美化输出
    if result['status'] == 'success':
        print('=' * 80)
        print(f'用户APP访问记录 - {user_id}')
        print('=' * 80)
        print(f'总记录数: {result["total_records"]} 条')
        print()
        
        print('【访问详情】')
        for i, log in enumerate(result['visit_logs'], 1):
            print(f'{i}. 访问时间: {log["访问时间"]}')
            print(f'   APP ID: {log["appId"]}')
            print(f'   渠道: {log["渠道"]}')
            print(f'   版本: {log["版本"]}')
            print(f'   设备ID: {log["设备ID"]}')
            print(f'   IP地址: {log["IP地址"]}')
            print(f'   手机品牌: {log["手机品牌"]}')
            print(f'   saleId: {log["saleId"]}')
            print()
        
        print('【设备分布】')
        for device, count in result['device_statistics'].items():
            print(f'  {device[:50]}...: {count} 次' if len(str(device)) > 50 else f'  {device}: {count} 次')
        print()
        
        print('【IP分布】')
        for ip, count in result['ip_statistics'].items():
            print(f'  {ip}: {count} 次')
        print()
        
        print('=' * 80)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))