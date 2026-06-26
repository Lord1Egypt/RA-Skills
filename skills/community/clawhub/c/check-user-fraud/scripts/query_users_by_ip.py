#!/usr/bin/env python3
"""
根据IP查询最近7天的用户
用于发现同一IP下的多个账号（刷量团伙）
"""

import sys
import pymysql
import json
from datetime import datetime

def query_users_by_ip(ip_address):
    """根据IP查询最近7天的用户"""
    
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
        
        # 查询该IP最近7天的用户
        sql = """
        SELECT DISTINCT(u.userId),
            u.id,
            u.mobile,
            u.truename,
            u.regTime,
            l.loginTime,
            l.deviceId,
            a.`name` as appName,
            l.channel,
            c.provice,
            c.city
        FROM t_user_loginlogs_2022 l
        INNER JOIN t_user u ON l.userId = u.id
        INNER JOIN t_sys_app a ON a.`code` = l.appId
        INNER JOIN t_ip_config c ON c.id = INET_ATON(l.ip)
        WHERE l.ip = %s 
        AND l.loginTime > DATE_SUB(NOW(), INTERVAL 7 DAY)
        ORDER BY l.loginTime DESC
        LIMIT 50
        """
        
        cursor.execute(sql, (ip_address,))
        users = cursor.fetchall()
        
        if not users:
            return {
                "ip": ip_address,
                "status": "no_records",
                "message": "该IP最近7天无登录记录"
            }
        
        # 格式化结果
        result = {
            "ip": ip_address,
            "status": "success",
            "query_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_users": len(users),
            "location": f"{users[0]['provice']} {users[0]['city']}" if users else '未知',
            "users": []
        }
        
        for user in users:
            user_info = {
                "userId": user['userId'],
                "id": user['id'],
                "手机号": user['mobile'] if user['mobile'] else '未知',
                "真实姓名": user['truename'] if user['truename'] else '未实名',
                "注册时间": datetime.fromtimestamp(user['regTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S') if user['regTime'] else '未知',
                "最近登录": user['loginTime'].strftime('%Y-%m-%d %H:%M:%S') if user['loginTime'] else '未知',
                "设备ID": user['deviceId'] if user['deviceId'] else '未知',
                "应用": user['appName'] if user['appName'] else '未知',
                "渠道": user['channel'] if user['channel'] else '未知'
            }
            result['users'].append(user_info)
        
        # 统计注册时间分布
        recent_reg = sum(1 for u in users if u['regTime'] and (datetime.now() - datetime.fromtimestamp(u['regTime'] / 1000)).days <= 7)
        result['statistics'] = {
            "最近7天注册": recent_reg,
            "老用户": len(users) - recent_reg,
            "新用户占比": f"{recent_reg / len(users) * 100:.1f}%" if users else '0%'
        }
        
        # 统计设备分布
        device_counter = {}
        for user in users:
            device = user['deviceId'] if user['deviceId'] else '未知'
            if device not in device_counter:
                device_counter[device] = 0
            device_counter[device] += 1
        
        result['device_statistics'] = device_counter
        
        cursor.close()
        conn.close()
        
        return result
        
    except Exception as e:
        import traceback
        return {
            "ip": ip_address,
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_users_by_ip.py <ip>")
        print("Example: python3 query_users_by_ip.py 180.129.235.223")
        sys.exit(1)
    
    ip_address = sys.argv[1]
    result = query_users_by_ip(ip_address)
    
    # 美化输出
    if result['status'] == 'success':
        print('=' * 80)
        print(f'IP登录用户查询 - {result["ip"]}')
        print('=' * 80)
        print(f'查询时间: {result["query_time"]}')
        print(f'地理位置: {result["location"]}')
        print(f'总用户数: {result["total_users"]} 个')
        print()
        
        print('【统计信息】')
        print(f'  最近7天注册: {result["statistics"]["最近7天注册"]} 人')
        print(f'  老用户: {result["statistics"]["老用户"]} 人')
        print(f'  新用户占比: {result["statistics"]["新用户占比"]}')
        print()
        
        print('【设备分布】')
        for device, count in result['device_statistics'].items():
            print(f'  {device[:50]}...: {count} 人' if len(str(device)) > 50 else f'  {device}: {count} 人')
        print()
        
        print('【用户列表】')
        for i, user in enumerate(result['users'], 1):
            print(f'{i}. 用户ID: {user["userId"]}')
            print(f'   手机号: {user["手机号"]}')
            print(f'   真实姓名: {user["真实姓名"]}')
            print(f'   注册时间: {user["注册时间"]}')
            print(f'   最近登录: {user["最近登录"]}')
            print(f'   设备ID: {user["设备ID"][:30]}...' if len(str(user["设备ID"])) > 30 else f'   设备ID: {user["设备ID"]}')
            print()
        
        print('=' * 80)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))