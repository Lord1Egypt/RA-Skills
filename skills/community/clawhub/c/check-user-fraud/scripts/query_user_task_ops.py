#!/usr/bin/env python3
"""
查询用户最近任务操作记录
包含提交、上架、下架、置顶等操作
"""

import sys
import pymysql
import json
from datetime import datetime

def query_user_task_ops(user_id):
    """查询用户最近任务操作记录"""
    
    # 数据库配置
    db_config = {
        'host': 'rr-wz97dxha81orq30j0eo.mysql.rds.aliyuncs.com',
        'port': 3389,
        'user': 'oc_gw',
        'password': 'm83KkZVLQp2Wg7HgDVb5cRjQ',
        'database': 'yc_db',
        'charset': 'utf8mb4'
    }
    
    # 操作类型映射
    ops_map = {
        1: "提交",
        2: "撤销",
        3: "暂停",
        4: "上架",
        5: "加价",
        6: "加量",
        7: "下架",
        8: "删除",
        9: "上架极速",
        10: "下架极速",
        11: "置顶",
        12: "推荐"
    }
    
    try:
        # 连接数据库
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 查询用户最近任务操作记录
        sql = """
        SELECT 
            l.taskId,
            l.ops,
            l.optime,
            l.ip,
            l.deviceId,
            l.id
        FROM t_task_opdetaillogs l
        INNER JOIN t_user u ON l.userId = u.id
        WHERE u.userId = %s
        ORDER BY l.optime DESC
        LIMIT 20
        """
        
        cursor.execute(sql, (user_id,))
        logs = cursor.fetchall()
        
        if not logs:
            return {
                "userId": user_id,
                "status": "no_records",
                "message": "未找到该用户的任务操作记录"
            }
        
        # 查询任务信息（补充标题）
        task_ids = list(set([log['taskId'] for log in logs if log['taskId']]))
        task_info_map = {}
        
        if task_ids:
            format_ids = ','.join(['%s'] * len(task_ids))
            cursor.execute(f'''
            SELECT id, taskNo, title
            FROM t_task
            WHERE id IN ({format_ids})
            ''', tuple(task_ids))
            
            tasks = cursor.fetchall()
            for task in tasks:
                task_info_map[task['id']] = {
                    'taskNo': task['taskNo'],
                    'title': task['title']
                }
        
        # 格式化结果
        result = {
            "userId": user_id,
            "status": "success",
            "total_records": len(logs),
            "operation_logs": []
        }
        
        for log in logs:
            ops_code = log['ops']
            task_id = log['taskId']
            
            # 处理操作时间
            optime = log['optime']
            if isinstance(optime, datetime):
                optime_str = optime.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(optime, int):
                optime_str = datetime.fromtimestamp(optime / 1000).strftime('%Y-%m-%d %H:%M:%S')
            else:
                optime_str = '未知'
            
            log_info = {
                "id": log['id'],
                "操作类型": f"{ops_code} - {ops_map.get(ops_code, '未知')}",
                "操作时间": optime_str,
                "taskId": task_id,
                "任务编号": task_info_map.get(task_id, {}).get('taskNo', '未知'),
                "任务标题": task_info_map.get(task_id, {}).get('title', '未知'),
                "IP地址": log['ip'] if log['ip'] else '未知',
                "设备ID": log['deviceId'] if log['deviceId'] else '未知'
            }
            result['operation_logs'].append(log_info)
        
        # 统计操作类型
        ops_counter = {}
        for log in logs:
            ops_code = log['ops']
            ops_name = ops_map.get(ops_code, f'未知({ops_code})')
            if ops_name not in ops_counter:
                ops_counter[ops_name] = 0
            ops_counter[ops_name] += 1
        
        result['ops_statistics'] = ops_counter
        
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
        print("Usage: python3 query_user_task_ops.py <userId>")
        print("Example: python3 query_user_task_ops.py D444AD")
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = query_user_task_ops(user_id)
    
    # 美化输出
    if result['status'] == 'success':
        print('=' * 80)
        print(f'用户任务操作记录 - {user_id}')
        print('=' * 80)
        print(f'总记录数: {result["total_records"]} 条')
        print()
        
        print('【操作统计】')
        for ops_name, count in sorted(result['ops_statistics'].items(), key=lambda x: x[1], reverse=True):
            print(f'  {ops_name}: {count} 次')
        print()
        
        print('【操作详情】')
        for i, log in enumerate(result['operation_logs'], 1):
            print(f'{i}. {log["操作时间"]}')
            print(f'   操作: {log["操作类型"]}')
            print(f'   任务: {log["任务编号"]} - {log["任务标题"]}')
            print(f'   IP: {log["IP地址"]}')
            print(f'   设备: {log["设备ID"][:30]}...' if len(str(log["设备ID"])) > 30 else f'   设备: {log["设备ID"]}')
            print()
        
        print('=' * 80)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))