#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投诉处理技能主入口
基于《C+基础保障服务手册》第十三章客户投诉处理规程
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from scripts.complaint_handler import ComplaintHandler

def main():
    """主函数"""
    handler = ComplaintHandler()
    
    # 根据命令行参数执行不同任务
    if len(sys.argv) > 1:
        task = sys.argv[1]
        
        if task == 'create':
            # 创建投诉记录
            print("创建投诉记录功能（需传入参数）")
        
        elif task == 'respond':
            # 响应投诉
            if len(sys.argv) > 3:
                complaint_id = sys.argv[2]
                handler_name = sys.argv[3]
                handler.respond_complaint(complaint_id, handler_name)
            else:
                print("用法: python main.py respond <投诉ID> <处理人姓名>")
        
        elif task == 'reply':
            # 回复投诉
            if len(sys.argv) > 3:
                complaint_id = sys.argv[2]
                reply_content = sys.argv[3]
                handler.reply_complaint(complaint_id, reply_content)
            else:
                print("用法: python main.py reply <投诉ID> <回复内容>")
        
        elif task == 'close':
            # 关闭投诉
            if len(sys.argv) > 3:
                complaint_id = sys.argv[2]
                close_result = sys.argv[3]
                handler.close_complaint(complaint_id, close_result)
            else:
                print("用法: python main.py close <投诉ID> <关闭结果>")
        
        elif task == 'followup':
            # 回访投诉
            if len(sys.argv) > 3:
                complaint_id = sys.argv[2]
                satisfaction = sys.argv[3]
                handler.follow_up_complaint(complaint_id, satisfaction)
            else:
                print("用法: python main.py followup <投诉ID> <满意度>")
        
        elif task == 'check':
            # 检查逾期投诉
            handler.check_overdue_complaints()
        
        elif task == 'report':
            # 生成投诉报告
            start_date = sys.argv[2] if len(sys.argv) > 2 else "2024-01-01"
            end_date = sys.argv[3] if len(sys.argv) > 3 else "2026-12-31"
            handler.generate_complaint_report(start_date, end_date)
        
        elif task == 'daily':
            # 执行每日任务
            handler.run_daily_task()
        
        else:
            print(f"未知任务: {task}")
            print_usage()
    
    else:
        # 默认执行每日任务
        handler.run_daily_task()

def print_usage():
    """打印使用说明"""
    print("""
投诉处理技能使用说明:

1. 创建投诉记录:
   python main.py create

2. 响应投诉:
   python main.py respond <投诉ID> <处理人姓名>

3. 回复投诉:
   python main.py reply <投诉ID> <回复内容>

4. 关闭投诉:
   python main.py close <投诉ID> <关闭结果>

5. 回访投诉:
   python main.py followup <投诉ID> <满意度>

6. 检查逾期投诉:
   python main.py check

7. 生成投诉报告:
   python main.py report [开始日期] [结束日期]
   示例: python main.py report 2026-01-01 2026-12-31

8. 执行每日任务:
   python main.py daily
""")

if __name__ == "__main__":
    main()