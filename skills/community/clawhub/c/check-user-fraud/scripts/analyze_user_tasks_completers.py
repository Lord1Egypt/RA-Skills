#!/usr/bin/env python3
"""
分析用户所做任务的做单人分布
查询用户做的所有任务，然后分析每个任务的做单人情况
"""

import sys
import pymysql
import json
from datetime import datetime
from collections import Counter

def analyze_user_tasks_completers(user_id):
    """分析用户所做任务的做单人分布"""
    
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
        
        # 第一步：查询用户做的所有任务
        user_tasks_sql = """
        SELECT DISTINCT
            t.taskNo,
            t.title,
            sb.taskAmout,
            FROM_UNIXTIME(sb.claimTime/1000) as '报名时间',
            FROM_UNIXTIME(sb.subTime/1000) as '提交时间'
        FROM t_task_submit sb 
        INNER JOIN t_user u ON u.id = sb.subId
        INNER JOIN t_task t ON sb.taskId = t.id
        WHERE u.userId = %s AND sb.`status` = 2
        ORDER BY sb.claimTime DESC
        LIMIT 100
        """
        
        cursor.execute(user_tasks_sql, (user_id,))
        user_tasks = cursor.fetchall()
        
        if not user_tasks:
            return {
                "userId": user_id,
                "status": "no_records",
                "message": "未找到该用户的做单记录"
            }
        
        # 分析结果
        analysis = {
            "userId": user_id,
            "total_tasks": len(user_tasks),
            "tasks_analysis": [],
            "summary": {}
        }
        
        # 第二步：对每个任务查询做单人情况
        for task in user_tasks:
            task_no = task['taskNo']
            
            # 查询该任务的所有做单人
            completers_sql = """
            SELECT 
                sb.id,
                u.regTime,
                u.userId as userNo,
                sb.claimTime,
                sb.subTime,
                sb.examineTime,
                u.refereeId,
                FROM_UNIXTIME(u.regTime/1000) as '注册时间',
                FROM_UNIXTIME(sb.claimTime/1000) as '报名时间',
                FROM_UNIXTIME(sb.subTime/1000) as '提交时间',
                FROM_UNIXTIME(sb.examineTime/1000) as '审核时间'
            FROM t_task_submit sb 
            INNER JOIN t_user u ON u.id = sb.subId
            INNER JOIN t_task t ON sb.taskId = t.id
            WHERE t.taskNo = %s AND sb.`status` = 2 
            ORDER BY sb.examineTime DESC 
            LIMIT 100
            """
            
            cursor.execute(completers_sql, (task_no,))
            completers = cursor.fetchall()
            
            # 分析该任务的做单人
            task_analysis = {
                "taskNo": task_no,
                "title": task['title'],
                "taskAmout": task['taskAmout'],
                "user_claim_time": str(task['报名时间']),
                "total_completers": len(completers),
                "completers": [],
                "registration_stats": {},
                "referee_stats": {}
            }
            
            # 统计变量
            current_time = datetime.now()
            recent_reg_count = 0
            has_referee_count = 0
            reg_times = []
            
            for c in completers:
                reg_time_ms = c.get('regTime')
                referee_id = c.get('refereeId')
                
                # 判断是否为最近注册（7天内）
                is_recent_reg = False
                if reg_time_ms:
                    try:
                        reg_time = datetime.fromtimestamp(reg_time_ms / 1000)
                        days_since_reg = (current_time - reg_time).days
                        is_recent_reg = days_since_reg <= 7
                        if is_recent_reg:
                            recent_reg_count += 1
                        reg_times.append(reg_time)
                    except:
                        pass
                
                # 判断是否有推荐人
                has_referee = referee_id and referee_id > 0
                if has_referee:
                    has_referee_count += 1
                
                # 构建做单人记录
                completer_data = {
                    "id": c['id'],
                    "userNo": c['userNo'],
                    "注册时间": str(c['注册时间']) if c['注册时间'] else None,
                    "是否最近注册(7天内)": is_recent_reg,
                    "refereeId": referee_id,
                    "是否有推荐人": has_referee,
                    "报名时间": str(c['报名时间']) if c['报名时间'] else None,
                    "提交时间": str(c['提交时间']) if c['提交时间'] else None
                }
                task_analysis['completers'].append(completer_data)
            
            # 注册时间统计
            if reg_times:
                task_analysis['registration_stats'] = {
                    "total_with_reg_time": len(reg_times),
                    "recent_reg_count": recent_reg_count,
                    "recent_reg_ratio": round(recent_reg_count / len(reg_times) * 100, 2),
                    "oldest_reg": str(min(reg_times)),
                    "newest_reg": str(max(reg_times))
                }
            
            # 推荐人统计
            task_analysis['referee_stats'] = {
                "total_with_referee": has_referee_count,
                "has_referee_ratio": round(has_referee_count / len(completers) * 100, 2) if completers else 0,
                "no_referee_count": len(completers) - has_referee_count,
                "no_referee_ratio": round((len(completers) - has_referee_count) / len(completers) * 100, 2) if completers else 0
            }
            
            # 判断风险等级
            recent_with_referee = sum(1 for c in task_analysis['completers'] 
                                      if c['是否最近注册(7天内)'] and c['是否有推荐人'])
            recent_with_referee_ratio = recent_with_referee / len(completers) if completers else 0
            
            if recent_with_referee >= 5 and recent_with_referee_ratio > 0.15:
                task_analysis['risk_level'] = 'high'
                task_analysis['risk_desc'] = f'{recent_with_referee}个做单人({recent_with_referee_ratio*100:.1f}%)最近注册且有推荐人，疑似批量注册'
            elif recent_with_referee >= 3:
                task_analysis['risk_level'] = 'medium'
                task_analysis['risk_desc'] = f'{recent_with_referee}个做单人最近注册且有推荐人，占比{recent_with_referee_ratio*100:.1f}%，需关注'
            else:
                task_analysis['risk_level'] = 'low'
                task_analysis['risk_desc'] = '未发现明显异常'
            
            analysis['tasks_analysis'].append(task_analysis)
        
        # 综合分析
        high_risk_tasks = sum(1 for t in analysis['tasks_analysis'] if t['risk_level'] == 'high')
        medium_risk_tasks = sum(1 for t in analysis['tasks_analysis'] if t['risk_level'] == 'medium')
        low_risk_tasks = sum(1 for t in analysis['tasks_analysis'] if t['risk_level'] == 'low')
        
        analysis['summary'] = {
            "total_tasks": len(user_tasks),
            "high_risk_tasks": high_risk_tasks,
            "medium_risk_tasks": medium_risk_tasks,
            "low_risk_tasks": low_risk_tasks,
            "risk_distribution": f"高风险:{high_risk_tasks}, 中风险:{medium_risk_tasks}, 低风险:{low_risk_tasks}"
        }
        
        # 整体评估
        if high_risk_tasks > 0:
            analysis['summary']['overall_risk'] = 'high'
            analysis['summary']['conclusion'] = f'用户做的{high_risk_tasks}个任务存在高风险，建议深入调查'
        elif medium_risk_tasks > 0:
            analysis['summary']['overall_risk'] = 'medium'
            analysis['summary']['conclusion'] = f'用户做的{medium_risk_tasks}个任务存在中风险，建议关注'
        else:
            analysis['summary']['overall_risk'] = 'low'
            analysis['summary']['conclusion'] = '用户做的任务整体风险较低'
        
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
        print("Usage: python3 analyze_user_tasks_completers.py <userId>")
        print("Example: python3 analyze_user_tasks_completers.py 124BAA0")
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = analyze_user_tasks_completers(user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))