#!/usr/bin/env python3
import json
import requests
import os
from datetime import datetime, date
import sys

class FeishuTaskManager:
    def __init__(self):
        # 尝试从环境变量获取，如果没有则使用默认值
        self.app_id = os.environ.get('FEISHU_APP_ID')
        self.app_secret = os.environ.get('FEISHU_APP_SECRET')
        
        # 如果没有环境变量，尝试从配置文件读取
        if not self.app_id or not self.app_secret:
            self.load_config_from_file()
        
        self.tenant_access_token = None
        self.user_access_token = None
        
        # 用户信息
        self.yangbin_user_id = None
        self.current_user_id = "ou_19c0ea5e1a6d3e318b52f4978684bd03"  # 当前用户ID
        
        self.load_yangbin_info()
    
    def load_config_from_file(self):
        """从配置文件加载凭证"""
        config_file = '/home/gary/.openclaw/workspace/feishu_config.json'
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.app_id = config.get('app_id')
                    self.app_secret = config.get('app_secret')
        except Exception as e:
            print(f"读取配置文件失败: {e}")
        
        # 如果还是没有，使用占位符（仅用于测试）
        if not self.app_id:
            self.app_id = 'cli_a6b5d8c9e0f1g2h3'  # 占位符
        if not self.app_secret:
            self.app_secret = 'your_app_secret'  # 占位符
    
    def load_yangbin_info(self):
        """加载用户信息"""
        config_file = '/home/gary/.openclaw/workspace/feishu_config.json'
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.yangbin_user_id = config.get('yangbin_user_id')
                    self.assignee_user_id = config.get('assignee_user_id')
                    
                    if self.yangbin_user_id:
                        print(f"✅ 已加载杨彬用户ID: {self.yangbin_user_id}")
                    else:
                        print("⚠️  配置文件中未找到杨彬用户ID")
                        
                    if self.assignee_user_id:
                        print(f"✅ 已加载负责人用户ID: {self.assignee_user_id}")
                    else:
                        print("⚠️  配置文件中未找到负责人用户ID")
        except Exception as e:
            print(f"读取用户信息失败: {e}")
        
    def get_tenant_access_token(self):
        """获取租户访问令牌"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if result.get('code') == 0:
                self.tenant_access_token = result['tenant_access_token']
                return True
            else:
                print(f"获取tenant_access_token失败: {result}")
                return False
        except Exception as e:
            print(f"获取tenant_access_token异常: {e}")
            return False
    
    def get_user_access_token(self, code):
        """获取用户访问令牌"""
        url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
        headers = {"Authorization": f"Bearer {self.tenant_access_token}", "Content-Type": "application/json"}
        data = {
            "grant_type": "authorization_code",
            "code": code
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if result.get('code') == 0:
                self.user_access_token = result['data']['access_token']
                return True
            else:
                print(f"获取user_access_token失败: {result}")
                return False
        except Exception as e:
            print(f"获取user_access_token异常: {e}")
            return False
    
    def create_task(self, title, description="", due_date=None, followers=None, assignees=None, add_yangbin=True, add_current_user=True):
        """创建任务
        
        Args:
            title: 任务标题
            description: 任务描述
            due_date: 截止日期（时间戳）
            followers: 关注人列表，格式 [{"id": "用户open_id"}]
            assignees: 负责人列表，格式 [{"id": "用户open_id"}]
            add_yangbin: 是否自动添加杨彬为关注人和负责人
            add_current_user: 是否自动添加当前用户为执行人和关注者
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return None
        
        url = "https://open.feishu.cn/open-apis/task/v2/tasks"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "summary": title,
            "description": description
        }
        
        if due_date:
            data["due"] = {"timestamp": due_date}
        
        # 处理关注人
        final_followers = followers or []
        
        # 添加当前用户为关注者
        if add_current_user and self.current_user_id:
            current_user_follower = {"id": self.current_user_id}
            if current_user_follower not in final_followers:
                final_followers.append(current_user_follower)
        
        # 添加杨彬为关注人
        if add_yangbin and self.yangbin_user_id:
            yangbin_follower = {"id": self.yangbin_user_id}
            if yangbin_follower not in final_followers:
                final_followers.append(yangbin_follower)
        
        # 处理负责人
        final_assignees = assignees or []
        
        # 添加当前用户为负责人（执行人）
        if add_current_user and self.current_user_id:
            current_user_assignee = {"id": self.current_user_id}
            if current_user_assignee not in final_assignees:
                final_assignees.append(current_user_assignee)
        
        # 添加杨彬为负责人
        if add_yangbin and self.yangbin_user_id:
            yangbin_assignee = {"id": self.yangbin_user_id}
            if yangbin_assignee not in final_assignees:
                final_assignees.append(yangbin_assignee)
        
        # 添加关注人和负责人到请求数据
        if final_followers:
            data["followers"] = final_followers
        if final_assignees:
            data["assignees"] = final_assignees
        
        print(f"📋 创建任务: {title}")
        print(f"   关注人: {len(final_followers)}")
        print(f"   负责人: {len(final_assignees)}")
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            print(f"创建任务响应: {result}")
            if result.get('code') == 0:
                # 修复：使用正确的字段名获取任务ID
                task_data = result['data']['task']
                task_id = task_data.get('task_id') or task_data.get('id') or task_data.get('guid')
                if task_id:
                    print(f"✅ 任务创建成功，ID: {task_id}")
                    return task_id
                else:
                    print(f"❌ 无法获取任务ID，响应数据: {task_data}")
                    return None
            else:
                print(f"❌ 创建任务失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 创建任务异常: {e}")
            return None
    
    def complete_task(self, task_id):
        """完成任务 - 使用PATCH方法更新任务状态
        
        Args:
            task_id: 可以是task_id（t开头）或guid（uuid格式）
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return False
        
        # 如果task_id是task_id格式（t开头），需要转换为guid
        task_guid = task_id
        if task_id.startswith('t'):
            # 尝试从task_id获取guid
            task_guid = self.get_task_guid_from_id(task_id)
            if not task_guid:
                print(f"❌ 无法获取任务 {task_id} 的guid")
                return False
        
        url = f"https://open.feishu.cn/open-apis/task/v2/tasks/{task_guid}"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }
        
        import time
        data = {
            "task": {
                "completed_at": str(int(time.time() * 1000))  # 当前时间戳（毫秒）
            },
            "update_fields": ["completed_at"]
        }
        
        try:
            response = requests.patch(url, headers=headers, json=data)
            response_text = response.text
            print(f"完成任务API响应: {response_text}")
            
            if response.status_code != 200:
                print(f"HTTP错误: {response.status_code}")
                return False
            
            try:
                result = response.json()
                if result.get('code') == 0:
                    print("✅ 任务完成成功")
                    return True
                else:
                    print(f"完成任务失败: {result}")
                    return False
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                return False
        except Exception as e:
            print(f"完成任务异常: {e}")
            return False
    
    def get_task_guid_from_id(self, task_id):
        """从task_id获取guid - 通过创建临时任务来获取映射关系"""
        # 这是一个临时的解决方案
        # 在实际应用中，应该维护一个task_id到guid的映射表
        print(f"⚠️  需要task_id到guid的映射，暂时返回None")
        return None
    
    def get_user_tasks(self, user_id, completed=False):
        """获取用户任务 - 使用正确的API端点"""
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return []
        
        # 使用正确的任务列表API端点
        url = "https://open.feishu.cn/open-apis/task/v2/tasks"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "page_size": 50
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response_text = response.text
            print(f"API响应: {response_text}")
            
            if response.status_code != 200:
                print(f"HTTP错误: {response.status_code}")
                return []
            
            result = response.json()
            if result.get('code') == 0:
                all_tasks = result['data']['items'] or []
                # 根据完成状态过滤任务
                filtered_tasks = []
                for task in all_tasks:
                    task_completed = task.get('completed', False)
                    if completed and task_completed:
                        filtered_tasks.append(task)
                    elif not completed and not task_completed:
                        filtered_tasks.append(task)
                return filtered_tasks
            else:
                print(f"获取任务失败: {result}")
                return []
        except Exception as e:
            print(f"获取任务异常: {e}")
            return []
    
    def get_tasks_completed_today(self, user_id):
        """获取今天完成的任务"""
        all_tasks = self.get_user_tasks(user_id, completed=True)
        today = date.today().isoformat()
        
        completed_today = []
        for task in all_tasks:
            completed_at = task.get('completed_at', '')
            if completed_at and completed_at.startswith(today):
                completed_today.append(task)
        
        return completed_today
    
    def get_pending_tasks(self, user_id):
        """获取未完成的任务"""
        return self.get_user_tasks(user_id, completed=False)
    
    def get_user_id(self):
        """获取当前用户ID"""
        # 这里应该使用飞书的用户信息API
        # 暂时返回固定的用户ID
        return "ou_19c0ea5e1a6d3e318b52f4978684bd03"

def main():
    manager = FeishuTaskManager()
    
    if len(sys.argv) < 2:
        print("Usage: feishu_task_integration.py [create|complete|list|pending|completed_today] [args...]")
        return
    
    action = sys.argv[1]
    
    if action == 'create' and len(sys.argv) > 2:
        title = sys.argv[2]
        task_id = manager.create_task(title)
        if task_id:
            print(f"任务创建成功，ID: {task_id}")
        else:
            print("任务创建失败")
    
    elif action == 'complete' and len(sys.argv) > 2:
        task_id = sys.argv[2]
        if manager.complete_task(task_id):
            print(f"任务 {task_id} 已完成")
        else:
            print(f"任务 {task_id} 完成失败")
    
    elif action == 'pending':
        user_id = manager.get_user_id()
        tasks = manager.get_pending_tasks(user_id)
        print(f"待办任务 ({len(tasks)}):")
        for task in tasks:
            print(f"- {task['summary']} (ID: {task['id']})")
    
    elif action == 'completed_today':
        user_id = manager.get_user_id()
        tasks = manager.get_tasks_completed_today(user_id)
        print(f"今日已完成 ({len(tasks)}):")
        for task in tasks:
            print(f"- {task['summary']} (ID: {task['id']})")
    
    elif action == 'list':
        user_id = manager.get_user_id()
        pending = manager.get_pending_tasks(user_id)
        completed = manager.get_tasks_completed_today(user_id)
        
        print(f"📋 任务概览 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"\n📌 待办任务 ({len(pending)}):")
        for task in pending:
            print(f"- {task['summary']} (ID: {task['id']})")
        
        print(f"\n🎉 今日已完成 ({len(completed)}):")
        for task in completed:
            print(f"- {task['summary']} (ID: {task['id']})")
    
    else:
        print("无效的命令")

if __name__ == '__main__':
    main()