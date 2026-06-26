#!/usr/bin/env python3
"""
查询用户详细信息
包含用户基本信息、实名认证、会员等级、邀请关系等
"""

import sys
import pymysql
import json
from datetime import datetime

def query_user_detail(user_id):
    """查询用户详细信息"""
    
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
        
        # 查询用户详细信息
        sql = """
        SELECT 
            u.id,
            u.mobile,
            IFNULL(u.alipayNo, '') as alipayNo,
            IFNULL(p.userId, '') as parentId,
            IFNULL(i.idNo, ip.idNo) as idNo,
            i.`name` as realName,
            u.regTime,
            u.truename,
            IFNULL(ip.status, 0) as proStatus,
            u.level,
            u.levelExpired,
            u.memberType,
            IFNULL(c.dataStatus, -1) as dataStatus,
            c.remarker,
            u.inviteCode,
            IFNULL(r.refreshTimes, 0) as refreshTimes
        FROM t_user u 
        LEFT JOIN t_user p ON u.refereeId = p.id
        LEFT JOIN t_user_identity i ON i.userId = u.id
        LEFT JOIN t_user_identitypro ip ON ip.id = u.id
        LEFT JOIN t_invite_usercmpdata c ON c.id = u.id
        LEFT JOIN t_task_refreshtimes r ON r.userId = u.id
        WHERE u.userId = %s
        """
        
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return {
                "userId": user_id,
                "status": "not_found",
                "message": "未找到该用户"
            }
        
        # 格式化结果
        result = {
            "userId": user_id,
            "status": "success",
            "user_info": {
                "基本信息": {
                    "用户ID": user['id'],
                    "手机号": user['mobile'],
                    "支付宝账号": user['alipayNo'] if user['alipayNo'] else '未绑定',
                    "邀请码": user['inviteCode'],
                    "注册时间": datetime.fromtimestamp(user['regTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S') if user['regTime'] else '未知'
                },
                "实名信息": {
                    "真实姓名": user['realName'] if user['realName'] else user['truename'] if user['truename'] else '未实名',
                    "身份证号": user['idNo'][:6] + '********' + user['idNo'][-4:] if user['idNo'] and len(user['idNo']) > 10 else '未认证',
                    "高级实名状态": "已认证" if user['proStatus'] == 1 else "未认证"
                },
                "会员信息": {
                    "会员等级": "普通用户" if user['level'] == 1 else "会员" if user['level'] == 2 else "未知",
                    "会员类型": get_member_type(user['memberType']),
                    "会员过期时间": datetime.fromtimestamp(user['levelExpired'] / 1000).strftime('%Y-%m-%d %H:%M:%S') if user['levelExpired'] else '无'
                },
                "邀请关系": {
                    "上级ID": user['parentId'] if user['parentId'] else '无',
                    "徒弟状态": get_data_status(user['dataStatus']),
                    "备注": user['remarker'] if user['remarker'] else '无'
                },
                "任务信息": {
                    "剩余刷新次数": user['refreshTimes']
                }
            }
        }
        
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

def get_member_type(member_type):
    """获取会员类型描述"""
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

def get_data_status(data_status):
    """获取徒弟状态描述"""
    if data_status == -1:
        return "无数据"
    elif data_status == 0:
        return "无效"
    elif data_status == 1:
        return "有效"
    else:
        return f"未知({data_status})"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_user_detail.py <userId>")
        print("Example: python3 query_user_detail.py 124BAA0")
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = query_user_detail(user_id)
    
    # 美化输出
    if result['status'] == 'success':
        print('=' * 80)
        print(f'用户详细信息 - {user_id}')
        print('=' * 80)
        print()
        
        for category, fields in result['user_info'].items():
            print(f'【{category}】')
            for key, value in fields.items():
                print(f'  {key}: {value}')
            print()
        
        print('=' * 80)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))