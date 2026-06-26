#!/usr/bin/env python3
"""
分析任务做单人情况
查询特定任务的所有做单人，分析注册时间和推荐人关系
"""

import sys
import pymysql
import json
from datetime import datetime
from collections import Counter

def analyze_task_completers(task_no):
    """分析任务做单人情况"""
    
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
        
        # 查询任务做单人情况
        sql = """
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
        
        cursor.execute(sql, (task_no,))
        records = cursor.fetchall()
        
        if not records:
            return {
                "taskNo": task_no,
                "status": "no_records",
                "message": "未找到该任务的做单记录"
            }
        
        # 分析结果
        analysis = {
            "taskNo": task_no,
            "total_completers": len(records),
            "completers": [],
            "registration_analysis": {},
            "referee_analysis": {},
            "risk_indicators": [],
            "summary": {}
        }
        
        # 统计变量
        recent_reg_count = 0  # 最近注册的数量
        has_referee_count = 0  # 有推荐人的数量
        reg_times = []
        referee_ids = []
        
        # 获取当前时间用于计算
        current_time = datetime.now()
        
        for record in records:
            reg_time_ms = record.get('regTime')
            referee_id = record.get('refereeId')
            
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
                referee_ids.append(referee_id)
            
            # 构建记录
            completer_data = {
                "id": record['id'],
                "userNo": record['userNo'],
                "注册时间": str(record['注册时间']) if record['注册时间'] else None,
                "是否最近注册(7天内)": is_recent_reg,
                "refereeId": referee_id,
                "是否有推荐人": has_referee,
                "报名时间": str(record['报名时间']) if record['报名时间'] else None,
                "提交时间": str(record['提交时间']) if record['提交时间'] else None,
                "审核时间": str(record['审核时间']) if record['审核时间'] else None
            }
            analysis['completers'].append(completer_data)
        
        # 注册时间分析
        if reg_times:
            analysis['registration_analysis'] = {
                "total_with_reg_time": len(reg_times),
                "recent_reg_count": recent_reg_count,
                "recent_reg_ratio": round(recent_reg_count / len(reg_times) * 100, 2),
                "oldest_reg": str(min(reg_times)),
                "newest_reg": str(max(reg_times))
            }
        
        # 推荐人分析
        referee_counter = Counter(referee_ids)
        top_referees = referee_counter.most_common(5)
        
        analysis['referee_analysis'] = {
            "total_with_referee": has_referee_count,
            "has_referee_ratio": round(has_referee_count / len(records) * 100, 2),
            "no_referee_count": len(records) - has_referee_count,
            "no_referee_ratio": round((len(records) - has_referee_count) / len(records) * 100, 2),
            "top_referees": [
                {"refereeId": ref_id, "count": count} for ref_id, count in top_referees
            ]
        }
        
        # 风险指标
        risk_indicators = []
        
        # 1. 最近注册占比过高
        if recent_reg_count > 0:
            recent_ratio = recent_reg_count / len(reg_times) if reg_times else 0
            if recent_ratio > 0.5:
                risk_indicators.append({
                    "type": "recent_registration",
                    "level": "high",
                    "description": f"{recent_reg_count}个做单人最近7天内注册，占比{recent_ratio*100:.1f}%，疑似批量注册账号"
                })
            elif recent_ratio > 0.3:
                risk_indicators.append({
                    "type": "recent_registration",
                    "level": "medium",
                    "description": f"{recent_reg_count}个做单人最近7天内注册，占比{recent_ratio*100:.1f}%，需关注"
                })
        
        # 2. 推荐人集中度
        if top_referees and top_referees[0][1] >= 5:
            risk_indicators.append({
                "type": "referee_concentration",
                "level": "high",
                "description": f"推荐人{top_referees[0][0]}推荐了{top_referees[0][1]}个做单人，疑似团伙操作"
            })
        elif top_referees and top_referees[0][1] >= 3:
            risk_indicators.append({
                "type": "referee_concentration",
                "level": "medium",
                "description": f"推荐人{top_referees[0][0]}推荐了{top_referees[0][1]}个做单人"
            })
        
        # 3. 无推荐人占比过高
        no_referee_ratio = analysis['referee_analysis']['no_referee_ratio']
        if no_referee_ratio > 70:
            risk_indicators.append({
                "type": "no_referee",
                "level": "medium",
                "description": f"{analysis['referee_analysis']['no_referee_count']}个做单人无推荐人，占比{no_referee_ratio:.1f}%"
            })
        
        # 4. 最近注册且有推荐人（只有当占比超过15%时才标记为高风险）
        recent_with_referee = sum(1 for c in analysis['completers'] 
                                  if c['是否最近注册(7天内)'] and c['是否有推荐人'])
        recent_with_referee_ratio = recent_with_referee / len(records) if records else 0
        
        if recent_with_referee >= 5 and recent_with_referee_ratio > 0.15:
            risk_indicators.append({
                "type": "recent_with_referee",
                "level": "high",
                "description": f"{recent_with_referee}个做单人({recent_with_referee_ratio*100:.1f}%)最近注册且有推荐人，疑似批量注册+邀请刷量"
            })
        elif recent_with_referee >= 3:
            risk_indicators.append({
                "type": "recent_with_referee",
                "level": "medium",
                "description": f"{recent_with_referee}个做单人最近注册且有推荐人，占比{recent_with_referee_ratio*100:.1f}%，需关注"
            })
        
        analysis['risk_indicators'] = risk_indicators
        
        # 综合评估
        if not risk_indicators:
            analysis['summary']['risk_level'] = 'low'
            analysis['summary']['conclusion'] = '未发现明显异常'
        else:
            high_risk = sum(1 for i in risk_indicators if i['level'] == 'high')
            medium_risk = sum(1 for i in risk_indicators if i['level'] == 'medium')
            
            if high_risk >= 2:
                analysis['summary']['risk_level'] = 'high'
                analysis['summary']['conclusion'] = '高度疑似刷量任务，建议深入调查'
            elif high_risk >= 1 or medium_risk >= 2:
                analysis['summary']['risk_level'] = 'medium'
                analysis['summary']['conclusion'] = '存在可疑模式，建议关注'
            else:
                analysis['summary']['risk_level'] = 'low'
                analysis['summary']['conclusion'] = '个别指标异常'
        
        analysis['summary']['indicators_count'] = len(risk_indicators)
        analysis['summary']['high_risk_count'] = sum(1 for i in risk_indicators if i['level'] == 'high')
        analysis['summary']['medium_risk_count'] = sum(1 for i in risk_indicators if i['level'] == 'medium')
        
        cursor.close()
        conn.close()
        
        return analysis
        
    except Exception as e:
        import traceback
        return {
            "taskNo": task_no,
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_task_completers.py <taskNo>")
        print("Example: python3 analyze_task_completers.py 21007864")
        sys.exit(1)
    
    task_no = sys.argv[1]
    result = analyze_task_completers(task_no)
    print(json.dumps(result, ensure_ascii=False, indent=2))