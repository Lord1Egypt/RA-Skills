#!/usr/bin/env python3
"""
飞书日历集成模块
"""
import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 飞书API配置
FEISHU_API_URL = "https://open.feishu.cn/open-apis"
APP_ID = os.getenv("FEISHU_APP_ID", "")
APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
USER_ID = "ou_fd95eeaa259733145362ac2207654aaf"

class FeishuCalendar:
    def __init__(self):
        self.access_token = self._get_access_token()
    
    def _get_access_token(self) -> str:
        """获取飞书API访问令牌"""
        if not APP_ID or not APP_SECRET:
            return ""
            
        url = f"{FEISHU_API_URL}/auth/v3/tenant_access_token/internal/"
        data = {
            "app_id": APP_ID,
            "app_secret": APP_SECRET
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("tenant_access_token", "")
        return ""
    
    def create_event(self, title: str, start_time: datetime, end_time: datetime, description: str = "") -> Optional[str]:
        """创建日历事件"""
        if not self.access_token:
            return None
            
        url = f"{FEISHU_API_URL}/calendar/v4/calendars/primary/events"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "summary": title,
            "description": description,
            "start_time": {
                "timestamp": int(start_time.timestamp()),
                "timezone": "Asia/Shanghai"
            },
            "end_time": {
                "timestamp": int(end_time.timestamp()),
                "timezone": "Asia/Shanghai"
            },
            "attendees": [
                {
                    "user_id": USER_ID,
                    "type": "user"
                }
            ],
            "reminders": [
                {
                    "minutes": 30,
                    "method": "notification"
                },
                {
                    "minutes": 5,
                    "method": "notification"
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("data", {}).get("event", {}).get("event_id")
        return None
    
    def list_upcoming_events(self, days: int = 7) -> List[Dict]:
        """获取未来几天的日历事件"""
        if not self.access_token:
            return []
            
        url = f"{FEISHU_API_URL}/calendar/v4/calendars/primary/events"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        start_time = datetime.now()
        end_time = start_time + timedelta(days=days)
        
        params = {
            "start_time": int(start_time.timestamp()),
            "end_time": int(end_time.timestamp()),
            "user_id_type": "open_id"
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            return result.get("data", {}).get("items", [])
        return []
    
    def check_time_available(self, check_time: datetime, duration: int = 60) -> bool:
        """检查指定时间段是否空闲（duration单位：分钟）"""
        events = self.list_upcoming_events(days=7)
        check_start = check_time
        check_end = check_time + timedelta(minutes=duration)
        
        for event in events:
            event_start = datetime.fromtimestamp(int(event["start_time"]["timestamp"]))
            event_end = datetime.fromtimestamp(int(event["end_time"]["timestamp"]))
            
            # 检查时间重叠
            if (check_start < event_end) and (check_end > event_start):
                return False
        return True
    
    def suggest_available_time(self, preferred_hour: int = 14, days: int = 7) -> Optional[datetime]:
        """推荐可用的时间段，默认优先下午2点"""
        for day_offset in range(days):
            check_date = datetime.now() + timedelta(days=day_offset)
            check_time = datetime(check_date.year, check_date.month, check_date.day, preferred_hour, 0, 0)
            
            if check_time > datetime.now() and self.check_time_available(check_time):
                return check_time
        
        # 如果下午2点都满了，找其他时间
        for day_offset in range(days):
            check_date = datetime.now() + timedelta(days=day_offset)
            for hour in range(9, 18):
                check_time = datetime(check_date.year, check_date.month, check_date.day, hour, 0, 0)
                if check_time > datetime.now() and self.check_time_available(check_time):
                    return check_time
        
        return None

# 全局实例
calendar = FeishuCalendar()

def sync_todo_to_calendar(todo_content: str, due_time: datetime) -> Optional[str]:
    """同步待办到飞书日历"""
    # 默认事件时长1小时
    end_time = due_time + timedelta(hours=1)
    return calendar.create_event(
        title=f"待办：{todo_content[:50]}",
        start_time=due_time,
        end_time=end_time,
        description=f"来自Omni-Todo的待办事项：\n{todo_content}"
    )

def get_calendar_events(days: int = 7) -> List[Dict]:
    """获取日历事件"""
    events = calendar.list_upcoming_events(days)
    formatted_events = []
    for event in events:
        formatted_events.append({
            "title": event.get("summary", ""),
            "start_time": datetime.fromtimestamp(int(event["start_time"]["timestamp"])),
            "end_time": datetime.fromtimestamp(int(event["end_time"]["timestamp"])),
            "location": event.get("location", ""),
            "status": event.get("status", "")
        })
    return formatted_events
