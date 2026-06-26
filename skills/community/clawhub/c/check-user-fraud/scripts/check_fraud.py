#!/usr/bin/env python3
"""
查询用户刷单情况
根据userId查询MySQL数据库，分析用户做单行为
"""

import sys
import pymysql
import json
from datetime import datetime

def analyze_user_fraud(user_id):
    """查询并分析用户刷单情况"""
    
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
        
        # 查询用户做单情况
        sql = """
        SELECT 
            sb.id, 
            sb.taskAmout,
            sb.examineText,
            t.taskNo,
            t.title,
            s.deviceId,
            sb.`status`,
            FROM_UNIXTIME(sb.claimTime/1000) as '报名时间',
            FROM_UNIXTIME(sb.subTime/1000) as '提交时间',
            FROM_UNIXTIME(sb.examineTime/1000) as '审核时间',
            u.userId,
            c.provice,
            c.city,
            s.appId,
            s.channel,
            t.userNo,
            s.ip 
        FROM t_task_subctx s 
        INNER JOIN t_task_submit sb ON sb.id = s.subId
        INNER JOIN t_task t ON sb.taskId = t.id
        INNER JOIN t_user u ON u.id = sb.subId
        INNER JOIN t_ip_config c ON c.id = INET_ATON(s.ip)
        WHERE u.userId = %s AND sb.`status` = 2 
        ORDER BY sb.claimTime DESC 
        LIMIT 100
        """
        
        cursor.execute(sql, (user_id,))
        records = cursor.fetchall()
        
        if not records:
            return {
                "userId": user_id,
                "status": "no_records",
                "message": "未找到该用户的做单记录"
            }
        
        # 分析结果
        analysis = {
            "userId": user_id,
            "total_records": len(records),
            "records": [],
            "fraud_indicators": [],
            "summary": {}
        }
        
        # 统计变量
        task_nos = []
        user_nos = []
        short_time_count = 0  # 短时间内完成的数量
        
        for record in records:
            # 转换时间
            claim_time = record['报名时间']
            sub_time = record['提交时间']
            
            # 计算时间间隔
            time_diff = None
            if claim_time and sub_time:
                try:
                    # 处理带微秒的时间格式
                    claim_str = str(claim_time).split('.')[0] if '.' in str(claim_time) else str(claim_time)
                    sub_str = str(sub_time).split('.')[0] if '.' in str(sub_time) else str(sub_time)
                    claim_dt = datetime.strptime(claim_str, '%Y-%m-%d %H:%M:%S')
                    sub_dt = datetime.strptime(sub_str, '%Y-%m-%d %H:%M:%S')
                    time_diff = (sub_dt - claim_dt).total_seconds() / 60  # 分钟
                    
                    # 判断是否为短时间完成（少于5分钟）
                    if time_diff < 5:
                        short_time_count += 1
                except Exception as e:
                    print(f"Time parse error: {e}", file=sys.stderr)
                    pass
            
            # 查询是否有置顶刷新
            top_sql = """
            SELECT COUNT(r.id) as top_count 
            FROM t_task_submit sb 
            INNER JOIN t_task_order r ON sb.taskId = r.taskId
            WHERE sb.id = %s 
            AND r.startTime > sb.claimTime 
            AND r.expiredTime > sb.claimTime 
            AND r.status IN (1, 100)
            """
            cursor.execute(top_sql, (record['id'],))
            top_result = cursor.fetchone()
            has_top = top_result['top_count'] > 0 if top_result else False
            
            # 收集taskNo和userNo
            if record.get('taskNo'):
                task_nos.append(record['taskNo'])
            if record.get('userNo'):
                user_nos.append(record['userNo'])
            
            # 构建记录
            record_data = {
                "id": record['id'],
                "taskNo": record['taskNo'],
                "title": record['title'],
                "taskAmout": record['taskAmout'],
                "报名时间": str(claim_time) if claim_time else None,
                "提交时间": str(sub_time) if sub_time else None,
                "审核时间": str(record['审核时间']) if record['审核时间'] else None,
                "完成时长(分钟)": round(time_diff, 2) if time_diff else None,
                "是否有置顶": has_top,
                "发单人": record['userNo'],
                "地区": f"{record.get('provice', '')} {record.get('city', '')}".strip(),
                "ip": record['ip'],
                "deviceId": record['deviceId'],
                "examineText": record['examineText']
            }
            analysis['records'].append(record_data)
        
        # 分析刷单指标
        fraud_indicators = []
        
        # 1. 检查短时间完成比例
        if short_time_count > 0:
            short_ratio = short_time_count / len(records)
            if short_ratio > 0.5:
                fraud_indicators.append({
                    "type": "short_time_completion",
                    "level": "high",
                    "description": f"{short_time_count}条记录完成时间少于5分钟，占比{short_ratio*100:.1f}%，疑似刷单"
                })
            elif short_ratio > 0.3:
                fraud_indicators.append({
                    "type": "short_time_completion",
                    "level": "medium",
                    "description": f"{short_time_count}条记录完成时间少于5分钟，占比{short_ratio*100:.1f}%，需关注"
                })
        
        # 2. 检查相同发单人
        from collections import Counter
        user_no_counter = Counter(user_nos)
        most_common_user = user_no_counter.most_common(1)
        if most_common_user and most_common_user[0][1] > 5:
            fraud_indicators.append({
                "type": "same_publisher",
                "level": "high" if most_common_user[0][1] > 10 else "medium",
                "description": f"频繁接取同一发单人({most_common_user[0][0]})的任务，共{most_common_user[0][1]}次"
            })
        
        # 3. 检查相同任务
        task_no_counter = Counter(task_nos)
        duplicate_tasks = [(t, c) for t, c in task_no_counter.items() if c > 1]
        if duplicate_tasks:
            fraud_indicators.append({
                "type": "duplicate_tasks",
                "level": "medium",
                "description": f"重复接取相同任务{len(duplicate_tasks)}个"
            })
        
        # 4. 检查无置顶任务比例
        no_top_count = sum(1 for r in analysis['records'] if not r['是否有置顶'])
        if no_top_count > 0:
            no_top_ratio = no_top_count / len(records)
            if no_top_ratio > 0.7:
                fraud_indicators.append({
                    "type": "no_top_refresh",
                    "level": "medium",
                    "description": f"{no_top_count}条记录接取时任务未置顶({no_top_ratio*100:.1f}%)，可能通过非正规渠道获取任务"
                })
        
        analysis['fraud_indicators'] = fraud_indicators
        
        # 综合评估
        if not fraud_indicators:
            analysis['summary']['risk_level'] = 'low'
            analysis['summary']['conclusion'] = '未发现明显刷单行为'
        else:
            high_risk = sum(1 for i in fraud_indicators if i['level'] == 'high')
            medium_risk = sum(1 for i in fraud_indicators if i['level'] == 'medium')
            
            if high_risk >= 2:
                analysis['summary']['risk_level'] = 'high'
                analysis['summary']['conclusion'] = '高度疑似刷单，建议深入调查'
            elif high_risk >= 1 or medium_risk >= 2:
                analysis['summary']['risk_level'] = 'medium'
                analysis['summary']['conclusion'] = '存在可疑行为，建议关注'
            else:
                analysis['summary']['risk_level'] = 'low'
                analysis['summary']['conclusion'] = '个别指标异常，需留意'
        
        analysis['summary']['indicators_count'] = len(fraud_indicators)
        analysis['summary']['high_risk_count'] = sum(1 for i in fraud_indicators if i['level'] == 'high')
        analysis['summary']['medium_risk_count'] = sum(1 for i in fraud_indicators if i['level'] == 'medium')
        
        cursor.close()
        conn.close()
        
        return analysis
        
    except Exception as e:
        return {
            "userId": user_id,
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_fraud.py <userId>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = analyze_user_fraud(user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))