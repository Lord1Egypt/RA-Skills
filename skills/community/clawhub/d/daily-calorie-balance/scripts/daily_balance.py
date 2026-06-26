#!/usr/bin/env python3
"""
Daily Calorie Balance - 每日卡路里平衡总结
合并 Calorie Visualizer 摄入数据与 Garmin 消耗数据
"""

import sys
import os
import sqlite3
import json
from datetime import datetime, timedelta

# 确定技能根目录
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.abspath(os.path.join(SKILL_DIR, '..', '..'))

# 依赖技能路径（相对 workspace）
CALORIE_VISUALIZER_DIR = os.path.join(WORKSPACE_DIR, 'skills', 'calorie-visualizer')
CLAWHEALTH_GARMIN_DIR = os.path.join(WORKSPACE_DIR, 'skills', 'clawhealth-garmin')

def check_dependencies():
    """检查依赖技能是否安装"""
    missing = []
    
    if not os.path.exists(CALORIE_VISUALIZER_DIR):
        missing.append('calorie-visualizer')
    
    if not os.path.exists(CLAWHEALTH_GARMIN_DIR):
        missing.append('clawhealth-garmin')
    
    if missing:
        print("❌ 缺少依赖技能：")
        for skill in missing:
            print(f"  • {skill}")
        print("\n请先安装以下依赖技能：")
        for skill in missing:
            print(f"  clawhub install {skill}")
        sys.exit(1)
    
    return True

# 检查依赖
check_dependencies()

# 添加 clawhealth 到路径
clawhealth_venv = os.path.join(CLAWHEALTH_GARMIN_DIR, '.venv', 'lib', 'python3.13', 'site-packages')
if os.path.exists(clawhealth_venv):
    sys.path.insert(0, clawhealth_venv)

# 设置环境变量（必须在导入 garth 之前）
os.environ['CLAWHEALTH_DB'] = os.path.join(CLAWHEALTH_GARMIN_DIR, 'data', 'health.db')
os.environ['CLAWHEALTH_CONFIG_DIR'] = os.path.join(CLAWHEALTH_GARMIN_DIR, 'config')

# 导入 garth 并配置中国区
try:
    import garth
    garth.configure(domain='garmin.cn')
except ImportError:
    print("❌ 错误：clawhealth-garmin 技能未正确安装或缺少依赖")
    print("请运行：cd skills/clawhealth-garmin && pip install -r requirements.txt")
    sys.exit(1)

def parse_date(date_str):
    """解析日期字符串"""
    now = datetime.now()
    if date_str.lower() in ['today', '今天', '今日', '']:
        return now.strftime('%Y-%m-%d')
    elif date_str.lower() in ['yesterday', '昨天', '昨日']:
        return (now - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            return now.strftime('%Y-%m-%d')

def get_calorie_intake(date_str):
    """从 Calorie Visualizer 获取食物摄入"""
    db_path = os.path.join(CALORIE_VISUALIZER_DIR, 'calorie_data.db')
    
    if not os.path.exists(db_path):
        print(f"⚠️ 警告：Calorie Visualizer 数据库不存在 ({db_path})")
        print("   请先使用 calorie-visualizer 技能记录一些食物数据")
        return 0, []
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT food_name, calories, protein 
            FROM entries 
            WHERE date = ? 
            ORDER BY created_at
        """, (date_str,))
        
        rows = cursor.fetchall()
        conn.close()
        
        total_calories = sum(row[1] for row in rows)
        foods = [row[0] for row in rows]
        
        return total_calories, foods
    except Exception:
        return 0, []

def get_garmin_expenditure(date_str):
    """从 clawhealth-garmin 获取 Garmin 消耗数据"""
    try:
        from clawhealth.cli import main
        import io
        from contextlib import redirect_stdout
        
        # 捕获输出
        f = io.StringIO()
        old_argv = sys.argv
        sys.argv = ['clawhealth', 'daily-summary', '--date', date_str, '--json']
        
        try:
            with redirect_stdout(f):
                main()
        finally:
            sys.argv = old_argv
        
        output = f.getvalue()
        data = json.loads(output)
        
        if data.get('ok'):
            summary = data
            total_calories = summary.get('calories_total', 0)
            return total_calories, total_calories * 0.3  # 估算活动消耗约 30%
        
        return 0, 0
    except Exception as e:
        print(f"Garmin 数据读取错误：{e}")
        return 0, 0

def calculate_balance(intake, expenditure):
    """计算卡路里平衡"""
    net = intake - expenditure
    
    if net > 500:
        status = "明显盈余"
        advice = "盈余较多，明天可增加运动或减少摄入"
        overall = "需注意"
    elif net > 100:
        status = "轻微盈余"
        advice = "略有盈余，保持当前节奏即可"
        overall = "积极"
    elif net < -500:
        status = "明显赤字"
        advice = "赤字较大，减脂效果好，注意不要过度节食"
        overall = "优秀"
    elif net < -100:
        status = "轻微赤字"
        advice = "赤字良好，继续保持"
        overall = "优秀"
    else:
        status = "平衡"
        advice = "摄入消耗平衡，保持当前状态"
        overall = "积极"
    
    return net, status, advice, overall

def generate_summary(date_str, auto_mode=False):
    """生成卡路里平衡总结"""
    # 获取数据
    intake, foods = get_calorie_intake(date_str)
    total_expenditure, active_expenditure = get_garmin_expenditure(date_str)
    
    # 计算平衡
    net, status, advice, overall = calculate_balance(intake, total_expenditure)
    
    # 生成输出
    output = []
    output.append(f"📊 今日卡路里平衡总结（{date_str} 北京时间）")
    output.append("")
    
    # 食物摄入
    if intake > 0:
        foods_str = "、".join(foods[:3]) + ("..." if len(foods) > 3 else "")
        output.append(f"🍽️ 食物摄入：{intake} kcal")
        output.append(f"（主要餐食：{foods_str}）")
    else:
        output.append("🍽️ 食物摄入：无记录")
    output.append("")
    
    # Garmin 消耗
    if total_expenditure > 0:
        output.append(f"🔥 Garmin 消耗：{int(total_expenditure)} kcal")
        output.append(f"（活动消耗约 {int(active_expenditure)} kcal | 总消耗 {int(total_expenditure)} kcal）")
    else:
        output.append("🔥 Garmin 消耗：无数据")
    output.append("")
    
    # 净卡路里
    net_str = f"+{net}" if net > 0 else str(net)
    output.append(f"⚖️ 净卡路里：{net_str} kcal")
    output.append(f"（{status}）")
    output.append("")
    
    # 建议
    output.append("💡 今日建议：")
    output.append(f"• {advice}")
    output.append(f"• 整体状态：{overall}")
    
    result = "\n".join(output)
    
    if auto_mode:
        # 自动模式：通过 message 工具发送
        try:
            from openclaw import message
            message.send(
                channel="qqbot",
                to="D5EF2AE19BFAF72D2CE64E860CE46F95",
                message=result
            )
            print("✅ 总结已发送")
        except Exception as e:
            print(f"发送失败：{e}")
            print(result)
    else:
        # 手动模式：直接输出
        print(result)
    
    return result

def main():
    if len(sys.argv) < 2:
        print("用法：python3 daily_balance.py <日期> [--auto]")
        print("日期：today/今天/yesterday/昨天/2026-03-29")
        sys.exit(1)
    
    date_str = sys.argv[1]
    auto_mode = '--auto' in sys.argv
    
    date = parse_date(date_str)
    generate_summary(date, auto_mode)

if __name__ == '__main__':
    main()
