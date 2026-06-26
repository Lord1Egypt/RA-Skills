#!/usr/bin/env python3
"""
系统性用户刷单分析工具
整合所有查询功能，提供一站式刷单分析
"""

import sys
import pymysql
import json
import socket
import struct
from datetime import datetime, timedelta
from collections import Counter

# 数据库配置
DB_CONFIG = {
    'host': 'rr-wz97dxha81orq30j0eo.mysql.rds.aliyuncs.com',
    'port': 3389,
    'user': 'oc_gw',
    'password': 'm83KkZVLQp2Wg7HgDVb5cRjQ',
    'database': 'yc_db',
    'charset': 'utf8mb4'
}

class FraudAnalyzer:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
    
    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def int_to_ip(self, ip_int):
        """将整数IP转换为点分十进制"""
        try:
            return socket.inet_ntoa(struct.pack('!I', ip_int))
        except:
            return str(ip_int)
    
    def analyze_user(self, user_id):
        """系统性分析用户刷单情况"""
        result = {
            "userId": user_id,
            "analysis_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "user_info": self._get_user_info(user_id),
            "login_analysis": self._analyze_login(user_id),
            "task_analysis": self._analyze_tasks(user_id),
            "publisher_analysis": self._analyze_as_publisher(user_id),
            "fraud_indicators": [],
            "risk_level": "low",
            "conclusion": ""
        }
        
        # 计算风险指标
        result["fraud_indicators"] = self._calculate_risk_indicators(result)
        result["risk_level"] = self._determine_risk_level(result["fraud_indicators"])
        result["conclusion"] = self._generate_conclusion(result)
        
        return result
    
    def _get_user_info(self, user_id):
        """获取用户基本信息"""
        self.cursor.execute('''
        SELECT u.id, u.mobile, u.truename, u.regTime, u.inviteCode,
               IFNULL(p.userId, '') as parentId,
               IFNULL(i.idNo, ip.idNo) as idNo,
               IFNULL(ip.status, 0) as proStatus,
               u.level, u.memberType,
               IFNULL(c.dataStatus, -1) as dataStatus,
               c.remarker
        FROM t_user u
        LEFT JOIN t_user p ON u.refereeId = p.id
        LEFT JOIN t_user_identity i ON i.userId = u.id
        LEFT JOIN t_user_identitypro ip ON ip.id = u.id
        LEFT JOIN t_invite_usercmpdata c ON c.id = u.id
        WHERE u.userId = %s
        ''', (user_id,))
        
        user = self.cursor.fetchone()
        if not user:
            return None
        
        return {
            "id": user['id'],
            "mobile": user['mobile'],
            "truename": user['truename'],
            "regTime": datetime.fromtimestamp(user['regTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S') if user['regTime'] else '未知',
            "inviteCode": user['inviteCode'],
            "parentId": user['parentId'] if user['parentId'] else '无',
            "idNo": user['idNo'][:6] + '********' + user['idNo'][-4:] if user['idNo'] and len(user['idNo']) > 10 else '未认证',
            "proStatus": "已认证" if user['proStatus'] == 1 else "未认证",
            "level": "普通" if user['level'] == 1 else "会员" if user['level'] == 2 else "未知",
            "memberType": self._get_member_type(user['memberType']),
            "dataStatus": self._get_data_status(user['dataStatus']),
            "remarker": user['remarker'] if user['remarker'] else '无'
        }
    
    def _analyze_login(self, user_id):
        """分析登录记录"""
        self.cursor.execute('''
        SELECT l.ip, c.provice, c.city, l.loginTime, l.deviceId
        FROM t_user_loginlogs_2022 l
        INNER JOIN t_user u ON l.userId = u.id
        INNER JOIN t_ip_config c ON c.id = INET_ATON(l.ip)
        WHERE u.userId = %s
        ORDER BY l.loginTime DESC
        LIMIT 10
        ''', (user_id,))
        
        logs = self.cursor.fetchall()
        
        return {
            "total_logins": len(logs),
            "recent_location": f"{logs[0]['provice']} {logs[0]['city']}" if logs else '未知',
            "recent_ip": logs[0]['ip'] if logs else '未知',
            "recent_device": logs[0]['deviceId'][:30] + '...' if logs and logs[0]['deviceId'] and len(logs[0]['deviceId']) > 30 else (logs[0]['deviceId'] if logs else '未知'),
            "login_history": [
                {
                    "time": log['loginTime'].strftime('%Y-%m-%d %H:%M:%S') if log['loginTime'] else '未知',
                    "ip": log['ip'],
                    "location": f"{log['provice']} {log['city']}".strip()
                } for log in logs[:5]
            ]
        }
    
    def _analyze_tasks(self, user_id):
        """分析任务接单情况"""
        self.cursor.execute('''
        SELECT t.taskNo, t.title, t.amount, t.userNo as publisher,
               sb.claimTime, sb.subTime, sb.examineTime, s.ip, s.deviceId
        FROM t_task_submit sb
        INNER JOIN t_task t ON sb.taskId = t.id
        INNER JOIN t_task_subctx s ON s.subId = sb.id
        INNER JOIN t_user u ON u.id = sb.subId
        WHERE u.userId = %s AND sb.status = 2
        ORDER BY sb.claimTime DESC
        LIMIT 20
        ''', (user_id,))
        
        tasks = self.cursor.fetchall()
        
        if not tasks:
            return {"total": 0, "tasks": []}
        
        # 分析完成时间
        short_time_count = 0
        for task in tasks:
            if task['claimTime'] and task['subTime']:
                try:
                    claim = datetime.fromtimestamp(task['claimTime'] / 1000)
                    submit = datetime.fromtimestamp(task['subTime'] / 1000)
                    if (submit - claim).total_seconds() < 300:  # 5分钟内
                        short_time_count += 1
                except:
                    pass
        
        return {
            "total": len(tasks),
            "short_time_count": short_time_count,
            "short_time_ratio": f"{short_time_count / len(tasks) * 100:.1f}%" if tasks else '0%',
            "tasks": [
                {
                    "taskNo": task['taskNo'],
                    "title": task['title'],
                    "amount": task['amount'],
                    "publisher": task['publisher'],
                    "ip": task['ip']
                } for task in tasks[:10]
            ]
        }
    
    def _analyze_as_publisher(self, user_id):
        """分析作为发单人的情况"""
        self.cursor.execute('''
        SELECT COUNT(*) as task_count
        FROM t_task t
        INNER JOIN t_user u ON t.userId = u.id
        WHERE u.userId = %s
        ''', (user_id,))
        
        task_count = self.cursor.fetchone()['task_count']
        
        # 查询置顶/刷新消费
        # inFlag: 0=消费, 1=充值; status: 4和6才是成功状态
        # payTime: 日期格式，无需FROM_UNIXTIME转换
        self.cursor.execute("""
        SELECT COUNT(*) as top_count
        FROM t_accout_trans a
        WHERE a.userId = (SELECT id FROM t_user WHERE userId = %s)
        AND a.inFlag = 0
        AND a.status IN (4, 6)
        AND (a.transDetail LIKE '%%置顶%%' OR a.transDetail LIKE '%%刷新%%' OR a.transDetail LIKE '%%推荐%%')
        """, (user_id,))
        
        top_count = self.cursor.fetchone()['top_count']
        
        return {
            "is_publisher": task_count > 0,
            "task_count": task_count,
            "top_refresh_count": top_count
        }
    
    def _calculate_risk_indicators(self, result):
        """计算风险指标"""
        indicators = []
        
        user_info = result.get("user_info")
        login_analysis = result.get("login_analysis")
        task_analysis = result.get("task_analysis")
        
        if not user_info:
            return indicators
        
        # 1. 注册时间检查
        if user_info.get("regTime"):
            try:
                reg_time = datetime.strptime(user_info["regTime"], '%Y-%m-%d %H:%M:%S')
                if (datetime.now() - reg_time).days <= 7:
                    indicators.append({
                        "type": "recent_registration",
                        "level": "medium",
                        "desc": "最近7天内注册"
                    })
            except:
                pass
        
        # 2. 系统备注检查
        if user_info.get("remarker") and "刷单" in user_info["remarker"]:
            indicators.append({
                "type": "system_flagged",
                "level": "high",
                "desc": f"系统已标记: {user_info['remarker']}"
            })
        
        # 3. 快速完成任务
        if task_analysis and task_analysis.get("short_time_ratio"):
            ratio = float(task_analysis["short_time_ratio"].rstrip('%'))
            if ratio > 50:
                indicators.append({
                    "type": "fast_completion",
                    "level": "high",
                    "desc": f"{ratio:.0f}%的任务在5分钟内完成"
                })
            elif ratio > 30:
                indicators.append({
                    "type": "fast_completion",
                    "level": "medium",
                    "desc": f"{ratio:.0f}%的任务在5分钟内完成"
                })
        
        # 4. 发单人无置顶消费
        publisher = result.get("publisher_analysis")
        if publisher and publisher.get("is_publisher") and publisher.get("top_refresh_count", 0) == 0:
            indicators.append({
                "type": "no_top_spending",
                "level": "medium",
                "desc": "发单人但无置顶/刷新消费"
            })
        
        return indicators
    
    def _determine_risk_level(self, indicators):
        """确定风险等级"""
        high_count = sum(1 for i in indicators if i["level"] == "high")
        medium_count = sum(1 for i in indicators if i["level"] == "medium")
        
        if high_count >= 2 or (high_count >= 1 and medium_count >= 2):
            return "high"
        elif high_count >= 1 or medium_count >= 2:
            return "medium"
        else:
            return "low"
    
    def _generate_conclusion(self, result):
        """生成结论"""
        risk_level = result.get("risk_level")
        indicators = result.get("fraud_indicators", [])
        
        if risk_level == "high":
            return "高度疑似刷单，建议立即冻结并深入调查"
        elif risk_level == "medium":
            return "存在可疑行为，建议关注并进一步监控"
        else:
            return "未发现明显异常"
    
    def _get_member_type(self, member_type):
        if member_type == -1:
            return "不是会员"
        elif member_type == 0:
            return "月会员"
        elif member_type == 5:
            return "季会员"
        elif member_type == 10:
            return "年会员"
        else:
            return f"未知({member_type})"
    
    def _get_data_status(self, data_status):
        if data_status == -1:
            return "无数据"
        elif data_status == 0:
            return "无效"
        elif data_status == 1:
            return "有效"
        else:
            return f"未知({data_status})"

def print_report(result):
    """打印分析报告"""
    print('=' * 80)
    print(f'用户刷单分析报告 - {result["userId"]}')
    print('=' * 80)
    print(f'分析时间: {result["analysis_time"]}')
    print(f'风险等级: {result["risk_level"].upper()}')
    print(f'结论: {result["conclusion"]}')
    print('=' * 80)
    print()
    
    user_info = result.get("user_info")
    if user_info:
        print('【基本信息】')
        print(f'  手机号: {user_info["mobile"]}')
        print(f'  真实姓名: {user_info["truename"] if user_info["truename"] else "未实名"}')
        print(f'  注册时间: {user_info["regTime"]}')
        print(f'  上级ID: {user_info["parentId"]}')
        print(f'  系统备注: {user_info["remarker"]}')
        print()
    
    login = result.get("login_analysis")
    if login:
        print('【登录分析】')
        print(f'  最近登录地点: {login["recent_location"]}')
        print(f'  最近IP: {login["recent_ip"]}')
        print(f'  登录次数: {login["total_logins"]}')
        print()
    
    tasks = result.get("task_analysis")
    if tasks:
        print('【任务分析】')
        print(f'  完成任务: {tasks["total"]} 个')
        print(f'  快速完成: {tasks["short_time_count"]} 个 ({tasks["short_time_ratio"]})')
        print()
    
    publisher = result.get("publisher_analysis")
    if publisher and publisher["is_publisher"]:
        print('【发单分析】')
        print(f'  发布任务: {publisher["task_count"]} 个')
        print(f'  置顶/刷新: {publisher["top_refresh_count"]} 次')
        print()
    
    indicators = result.get("fraud_indicators")
    if indicators:
        print('【风险指标】')
        for i, ind in enumerate(indicators, 1):
            emoji = '🔴' if ind["level"] == "high" else '🟡'
            print(f'{i}. {emoji} {ind["desc"]}')
        print()
    
    print('=' * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fraud_analyzer.py <userId>")
        print("Example: python3 fraud_analyzer.py 124BAA0")
        sys.exit(1)
    
    user_id = sys.argv[1]
    analyzer = FraudAnalyzer()
    
    try:
        result = analyzer.analyze_user(user_id)
        print_report(result)
        
        # 同时输出JSON格式（可选）
        # print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        analyzer.close()