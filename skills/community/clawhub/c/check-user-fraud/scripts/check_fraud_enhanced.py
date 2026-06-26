#!/usr/bin/env python3
"""
查询用户刷单情况 - 增强版
根据userId查询MySQL数据库，分析用户做单行为，并分析发单人账单
"""

import sys
import pymysql
import json
from datetime import datetime
from collections import Counter

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
            sb.claimTime,
            sb.subTime,
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
            "publisher_analysis": {},  # 发单人分析
            "fraud_indicators": [],
            "summary": {}
        }
        
        # 统计变量
        task_nos = []
        user_nos = []
        short_time_count = 0
        
        for record in records:
            # 转换时间
            claim_time = record['报名时间']
            sub_time = record['提交时间']
            claim_time_ms = record['claimTime']  # 毫秒时间戳
            
            # 计算时间间隔
            time_diff = None
            if claim_time and sub_time:
                try:
                    claim_str = str(claim_time).split('.')[0] if '.' in str(claim_time) else str(claim_time)
                    sub_str = str(sub_time).split('.')[0] if '.' in str(sub_time) else str(sub_time)
                    claim_dt = datetime.strptime(claim_str, '%Y-%m-%d %H:%M:%S')
                    sub_dt = datetime.strptime(sub_str, '%Y-%m-%d %H:%M:%S')
                    time_diff = (sub_dt - claim_dt).total_seconds() / 60
                    
                    if time_diff < 5:
                        short_time_count += 1
                except Exception as e:
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
            
            # 查询发单人账单（置顶推荐刷新消费）
            # inFlag: 0=消费, 1=充值; status: 4和6才是成功状态
            # payTime: 日期格式，无需FROM_UNIXTIME转换
            # accoutType: 1000=任务余额, 1001=保证金, 1002=收入分红, 1003=推广收入
            # 置顶/推荐/刷新只能使用1000任务余额账户
            publisher_bills = []
            if record.get('taskNo') and record.get('userNo') and claim_time_ms:
                bill_sql = """
                SELECT 
                    a.id,
                    a.transDetail,
                    a.amount,
                    a.inFlag,
                    a.status,
                    a.transType,
                    a.accoutType,
                    a.payTime
                FROM t_accout_trans a 
                INNER JOIN t_task t ON a.userId = t.userId
                WHERE t.taskNo = %s 
                AND a.inFlag = 0
                AND a.status IN (4, 6)
                AND a.subTime < %s 
                ORDER BY a.subTime DESC 
                LIMIT 10
                """
                cursor.execute(bill_sql, (record['taskNo'], claim_time_ms))
                bills = cursor.fetchall()
                
                for bill in bills:
                    publisher_bills.append({
                        "id": bill['id'],
                        "transDetail": bill['transDetail'],
                        "amount": bill['amount'],
                        "payTime": str(bill['payTime']) if bill['payTime'] else None
                    })
            
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
                "发单人账单": publisher_bills,
                "地区": f"{record.get('provice', '')} {record.get('city', '')}".strip(),
                "ip": record['ip'],
                "deviceId": record['deviceId'],
                "examineText": record['examineText']
            }
            analysis['records'].append(record_data)
        
        # 分析发单人账单
        publisher_spending = {}
        for record in analysis['records']:
            publisher = record['发单人']
            if publisher not in publisher_spending:
                publisher_spending[publisher] = {
                    "task_count": 0,
                    "total_spending": 0,
                    "top_refresh_count": 0,
                    "bills": []
                }
            
            publisher_spending[publisher]["task_count"] += 1
            
            for bill in record.get('发单人账单', []):
                publisher_spending[publisher]["bills"].append(bill)
                publisher_spending[publisher]["total_spending"] += bill.get('amount', 0)
                
                # 判断是否为置顶刷新消费
                trans_detail = bill.get('transDetail', '') or ''
                if '置顶' in trans_detail or '刷新' in trans_detail or '推荐' in trans_detail:
                    publisher_spending[publisher]["top_refresh_count"] += 1
        
        analysis['publisher_analysis'] = publisher_spending
        
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
        
        # 5. 检查发单人消费异常
        for publisher, data in publisher_spending.items():
            if data['top_refresh_count'] == 0 and data['task_count'] >= 3:
                fraud_indicators.append({
                    "type": "publisher_no_spending",
                    "level": "high",
                    "description": f"发单人{publisher}发布{data['task_count']}个任务但无置顶刷新消费，疑似内部账号"
                })
            elif data['top_refresh_count'] < data['task_count'] / 2:
                fraud_indicators.append({
                    "type": "publisher_low_spending",
                    "level": "medium",
                    "description": f"发单人{publisher}置顶刷新消费比例偏低({data['top_refresh_count']}/{data['task_count']})"
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
        import traceback
        return {
            "userId": user_id,
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_fraud_enhanced.py <userId>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = analyze_user_fraud(user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))