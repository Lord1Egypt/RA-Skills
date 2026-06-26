#!/usr/bin/env python3
"""
查询用户发单记录并分析任务接单人分布
"""

import sys
import pymysql
import json
from datetime import datetime
from collections import Counter

def analyze_user_publisher_tasks(user_id):
    """查询用户发单记录并分析任务接单人分布"""
    
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
        
        # 查询用户最近发单记录
        tasks_sql = """
        SELECT 
            t.taskNo,
            t.title,
            t.amount,
            t.tagName,
            t.refreshTime,
            FROM_UNIXTIME(t.refreshTime/1000) as '刷新时间'
        FROM t_task t 
        INNER JOIN t_user u ON t.userId = u.id
        WHERE u.userId = %s 
        ORDER BY t.refreshTime DESC
        LIMIT 10
        """
        
        cursor.execute(tasks_sql, (user_id,))
        tasks = cursor.fetchall()
        
        if not tasks:
            return {
                "userId": user_id,
                "status": "no_records",
                "message": "未找到该用户的发单记录"
            }
        
        # 分析结果
        analysis = {
            "userId": user_id,
            "total_tasks": len(tasks),
            "tasks": [],
            "summary": {}
        }
        
        current_time = datetime.now()
        
        for task in tasks:
            task_no = task['taskNo']
            
            # 查询该任务的接单人情况
            completers_sql = """
            SELECT 
                sb.id,
                u.userId as userNo,
                u.regTime,
                u.refereeId,
                FROM_UNIXTIME(u.regTime/1000) as '注册时间',
                FROM_UNIXTIME(sb.claimTime/1000) as '报名时间',
                FROM_UNIXTIME(sb.subTime/1000) as '提交时间'
            FROM t_task_submit sb 
            INNER JOIN t_user u ON u.id = sb.subId
            INNER JOIN t_task t ON sb.taskId = t.id
            WHERE t.taskNo = %s AND sb.`status` = 2
            ORDER BY sb.examineTime DESC
            LIMIT 100
            """
            
            cursor.execute(completers_sql, (task_no,))
            completers = cursor.fetchall()
            
            # 分析接单人
            task_analysis = {
                "taskNo": task_no,
                "title": task['title'],
                "amount": task['amount'],
                "tagName": task['tagName'],
                "refreshTime": str(task['刷新时间']),
                "total_completers": len(completers),
                "completer_analysis": {}
            }
            
            # 统计注册时间
            recent_reg_count = 0
            has_referee_count = 0
            
            for c in completers:
                reg_time_ms = c.get('regTime')
                referee_id = c.get('refereeId')
                
                # 判断是否为最近注册（7天内）
                if reg_time_ms:
                    try:
                        reg_time = datetime.fromtimestamp(reg_time_ms / 1000)
                        days_since_reg = (current_time - reg_time).days
                        if days_since_reg <= 7:
                            recent_reg_count += 1
                    except:
                        pass
                
                # 判断是否有推荐人
                if referee_id and referee_id > 0:
                    has_referee_count += 1
            
            # 接单人分析统计
            if completers:
                task_analysis['completer_analysis'] = {
                    "recent_reg_count": recent_reg_count,
                    "recent_reg_ratio": round(recent_reg_count / len(completers) * 100, 2),
                    "has_referee_count": has_referee_count,
                    "has_referee_ratio": round(has_referee_count / len(completers) * 100, 2),
                    "no_referee_count": len(completers) - has_referee_count,
                    "no_referee_ratio": round((len(completers) - has_referee_count) / len(completers) * 100, 2)
                }
                
                # 风险判断
                recent_with_referee = sum(1 for c in completers 
                                          if c.get('regTime') and c.get('refereeId', 0) > 0
                                          and (current_time - datetime.fromtimestamp(c['regTime'] / 1000)).days <= 7)
                recent_with_referee_ratio = recent_with_referee / len(completers)
                
                if recent_with_referee >= 5 and recent_with_referee_ratio > 0.15:
                    task_analysis['risk_level'] = 'high'
                    task_analysis['risk_desc'] = f'{recent_with_referee}个接单人({recent_with_referee_ratio*100:.1f}%)最近注册且有推荐人'
                elif recent_with_referee >= 3:
                    task_analysis['risk_level'] = 'medium'
                    task_analysis['risk_desc'] = f'{recent_with_referee}个接单人最近注册且有推荐人，占比{recent_with_referee_ratio*100:.1f}%'
                else:
                    task_analysis['risk_level'] = 'low'
                    task_analysis['risk_desc'] = '未发现明显异常'
            else:
                task_analysis['risk_level'] = 'low'
                task_analysis['risk_desc'] = '暂无接单人'
            
            analysis['tasks'].append(task_analysis)
        
        # 综合分析
        high_risk = sum(1 for t in analysis['tasks'] if t['risk_level'] == 'high')
        medium_risk = sum(1 for t in analysis['tasks'] if t['risk_level'] == 'medium')
        low_risk = sum(1 for t in analysis['tasks'] if t['risk_level'] == 'low')
        
        analysis['summary'] = {
            "total_tasks": len(tasks),
            "high_risk_tasks": high_risk,
            "medium_risk_tasks": medium_risk,
            "low_risk_tasks": low_risk,
            "risk_distribution": f"高风险:{high_risk}, 中风险:{medium_risk}, 低风险:{low_risk}"
        }
        
        if high_risk > 0:
            analysis['summary']['overall_risk'] = 'high'
            analysis['summary']['conclusion'] = f'发布的{high_risk}个任务存在高风险，疑似刷量'
        elif medium_risk > 0:
            analysis['summary']['overall_risk'] = 'medium'
            analysis['summary']['conclusion'] = f'发布的{medium_risk}个任务存在中风险'
        else:
            analysis['summary']['overall_risk'] = 'low'
            analysis['summary']['conclusion'] = '发布的任务整体风险较低'
        
        cursor.close()
        conn.close()
        
        return analysis
        
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
        print("Usage: python3 analyze_user_publisher_tasks.py <userId>")
        print("Example: python3 analyze_user_publisher_tasks.py D444AD")
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = analyze_user_publisher_tasks(user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))