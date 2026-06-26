#!/usr/bin/env python3
"""
飞书任务对接 - 待办事项处理器 (清理版)
移除了所有个人信息和敏感配置
"""

import json
import os
import sys
import requests
from datetime import datetime, date

class TodoHandlerV2:
    def __init__(self):
        self.todo_file = 'todo_data.json'
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.todo_file):
            with open(self.todo_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {'todos': [], 'completed': [], 'current_date': str(date.today())}
    
    def save_data(self):
        with open(self.todo_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def process_command(self, message):
        """处理todo命令"""
        message = message.strip()
        
        if message == 'todo':
            return self.show_all()
        elif message.startswith('todo'):
            content = message[4:].strip()
            if content:
                return self.add_todo(content)
            else:
                return self.show_all()
        elif message.startswith('done'):
            try:
                todo_id = int(message[4:].strip())
                return self.complete_todo(todo_id)
            except ValueError:
                return "❌ 无效的任务序号"
        else:
            return "❌ 未知命令"
    
    def add_todo(self, content):
        """添加待办事项"""
        today = str(date.today())
        
        # 新的一天重置序号
        if self.data['current_date'] != today:
            self.data['current_date'] = today
            old_todos = self.data['todos']
            self.data['todos'] = []
            for i, todo in enumerate(old_todos):
                if not todo['completed']:
                    self.data['todos'].append({
                        'id': i,
                        'content': todo['content'],
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'completed': False
                    })
        
        todo_id = len(self.data['todos'])
        
        # 解析截止时间
        due_date = self.parse_due_date(content)
        
        # 尝试添加到飞书任务
        feishu_result = self.add_to_feishu_task(content, due_date)
        
        new_todo = {
            'id': todo_id,
            'content': content,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completed': False,
            'feishu_task_id': feishu_result.get('task_id'),
            'feishu_guid': feishu_result.get('guid'),
            'feishu_status': feishu_result.get('status', 'failed')
        }
        self.data['todos'].append(new_todo)
        self.save_data()
        
        if feishu_result.get('success'):
            return f"✅ 待办事项已添加并同步到飞书任务，ID: {feishu_result['task_id']}"
        else:
            return f"✅ 待办事项已添加（飞书同步待配置），序号：{todo_id}"
    
    def parse_due_date(self, content):
        """解析截止时间"""
        import time
        import re
        from datetime import datetime, timedelta
        
        # 检查是否包含时间关键词
        content_lower = content.lower()
        
        # 今天
        if '今天' in content_lower:
            return int(time.time() * 1000)
        
        # 明天
        elif '明天' in content_lower:
            tomorrow = datetime.now() + timedelta(days=1)
            return int(tomorrow.timestamp() * 1000)
        
        # 本周
        elif '本周' in content_lower:
            # 计算本周日
            today = datetime.now()
            days_to_sunday = 6 - today.weekday()
            this_week = today + timedelta(days=days_to_sunday)
            return int(this_week.timestamp() * 1000)
        
        # 下周
        elif '下周' in content_lower:
            # 计算下周日
            today = datetime.now()
            days_to_next_sunday = 13 - today.weekday()
            next_week = today + timedelta(days=days_to_next_sunday)
            return int(next_week.timestamp() * 1000)
        
        # 本月
        elif '本月' in content_lower:
            # 计算本月最后一天
            today = datetime.now()
            if today.month == 12:
                last_day = datetime(today.year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
            return int(last_day.timestamp() * 1000)
        
        # 默认3天后
        else:
            default_due = datetime.now() + timedelta(days=3)
            return int(default_due.timestamp() * 1000)
    
    def add_to_feishu_task(self, content, due_date=None):
        """添加到飞书任务"""
        try:
            from feishu_task_integration import FeishuTaskManager
            import requests
            
            manager = FeishuTaskManager()
            
            # 直接调用API创建任务并获取完整响应
            if not manager.get_tenant_access_token():
                return {
                    'success': False,
                    'task_id': None,
                    'guid': None,
                    'status': 'auth_failed'
                }
            
            url = "https://open.feishu.cn/open-apis/task/v2/tasks"
            headers = {
                "Authorization": f"Bearer {manager.tenant_access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "summary": content,
                "description": f"来自待办事项助手的任务\n创建时间: {self.get_current_time()}"
            }
            
            # 添加截止时间（如果提供了的话）
            if due_date:
                data["due"] = {"timestamp": due_date}
            
            # 根据飞书API示例，使用members字段设置负责人
            members = []
            
            # 使用指定的负责人用户ID
            if hasattr(manager, 'assignee_user_id') and manager.assignee_user_id:
                members.append({
                    "id": manager.assignee_user_id,
                    "type": "user",
                    "role": "assignee"
                })
            else:
                # 默认使用当前用户
                members.append({
                    "id": manager.current_user_id,
                    "type": "user", 
                    "role": "assignee"
                })
            
            data["members"] = members
            
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if result.get('code') == 0:
                task_data = result['data']['task']
                task_id = task_data.get('task_id')
                guid = task_data.get('guid')
                
                return {
                    'success': True,
                    'task_id': task_id,
                    'guid': guid,
                    'status': 'created_successfully'
                }
            else:
                return {
                    'success': False,
                    'task_id': None,
                    'guid': None,
                    'status': 'creation_failed'
                }
                
        except Exception as e:
            print(f"飞书任务创建异常: {e}")
            return {
                'success': False,
                'task_id': None,
                'guid': None,
                'status': 'error'
            }
    
    def complete_todo(self, todo_id):
        """完成待办事项"""
        for todo in self.data['todos']:
            if todo['id'] == todo_id and not todo['completed']:
                todo['completed'] = True
                todo['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # 尝试同步到飞书任务
                if todo.get('feishu_task_id'):
                    feishu_guid = todo.get('feishu_guid')
                    self.complete_feishu_task(todo['feishu_task_id'], feishu_guid)
                
                self.data['completed'].append(todo.copy())
                self.save_data()
                return f"✅ 待办事项 {todo_id} 已标记为完成"
        return f"❌ 未找到待办事项 {todo_id}"
    
    def complete_feishu_task(self, task_id, guid=None):
        """完成飞书任务"""
        try:
            from feishu_task_integration import FeishuTaskManager
            
            manager = FeishuTaskManager()
            
            # 优先使用guid，如果没有则使用task_id
            task_identifier = guid if guid else task_id
            success = manager.complete_task(task_identifier)
            
            if success:
                print(f"✅ 飞书任务 {task_id} 已完成")
                return True
            else:
                print(f"❌ 飞书任务 {task_id} 完成失败")
                return False
                
        except Exception as e:
            print(f"飞书任务完成异常: {e}")
            return False
    
    def get_current_time(self):
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def show_all(self):
        """显示所有待办和已完成事项"""
        pending = [todo for todo in self.data['todos'] if not todo['completed']]
        today = str(date.today())
        completed_today = [todo for todo in self.data['completed'] 
                          if todo.get('completed_at', '').startswith(today)]
        
        response = f"📋 **待办事项报告** | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        if pending:
            response += "📌 **待办事项**\n"
            for todo in pending:
                feishu_status = "" if todo.get('feishu_status') == 'failed' else " 📌飞书"
                response += f"{todo['id']}. {todo['content']}{feishu_status}\n"
        else:
            response += "✅ **暂无待办事项**\n"
        
        if completed_today:
            response += "\n🎉 **今日已完成**\n"
            for todo in completed_today:
                response += f"✅ {todo['content']}\n"
        
        response += "\n🤖 **待办事项助手** | 飞书任务集成"
        return response

def main():
    if len(sys.argv) > 1:
        handler = TodoHandlerV2()
        result = handler.process_command(sys.argv[1])
        print(result)
    else:
        print("需要提供命令参数")

if __name__ == '__main__':
    main()