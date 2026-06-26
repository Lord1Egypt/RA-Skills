#!/usr/bin/env python3
"""
BotStreet任务接单脚本
功能：获取任务列表、申请任务、提交交付物、查看通知等
"""

import json
import argparse
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# API配置
BASE_URL = "https://botstreet.cn/api/v1"

# 默认凭证（从SECRET.md读取）
DEFAULT_AGENT_ID = "167441766587305984"
DEFAULT_AGENT_KEY = "ak-xv1frJKdz9MmIThDNmSLpVP64X5pwFIurEVUzgMSuxib4Ebf"


class BotStreetAPI:
    """BotStreet API封装类"""
    
    def __init__(self, agent_id: str, agent_key: str):
        self.agent_id = agent_id
        self.agent_key = agent_key
        self.base_url = BASE_URL
    
    def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "x-agent-id": self.agent_id,
            "x-agent-key": self.agent_key,
            "Content-Type": "application/json"
        }
        
        try:
            if data:
                json_data = json.dumps(data).encode('utf-8')
                req = Request(url, data=json_data, headers=headers, method=method)
            else:
                req = Request(url, headers=headers, method=method)
            
            with urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result
        except HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            try:
                error_json = json.loads(error_body)
                return {"success": False, "error": error_json}
            except:
                return {"success": False, "error": {"message": error_body or str(e)}}
        except URLError as e:
            return {"success": False, "error": {"message": str(e)}}
        except Exception as e:
            return {"success": False, "error": {"message": str(e)}}
    
    def get_tasks(self, status: str = None, category: str = None) -> dict:
        """获取任务列表"""
        endpoint = "/tasks"
        params = []
        if status:
            params.append(f"status={status}")
        if category:
            params.append(f"category={category}")
        if params:
            endpoint += "?" + "&".join(params)
        return self._make_request("GET", endpoint)
    
    def get_my_tasks(self) -> dict:
        """获取我的任务"""
        return self._make_request("GET", "/tasks/my")
    
    def get_task_detail(self, task_id: str) -> dict:
        """获取任务详情"""
        return self._make_request("GET", f"/tasks/{task_id}")
    
    def apply_task(self, task_id: str, proposal: str, estimated_time: str = None) -> dict:
        """申请任务"""
        data = {"proposal": proposal}
        if estimated_time:
            data["estimatedTime"] = estimated_time
        return self._make_request("POST", f"/tasks/{task_id}/apply", data)
    
    def submit_delivery(self, task_id: str, content: str) -> dict:
        """提交交付物"""
        return self._make_request("POST", f"/tasks/{task_id}/deliver", {"content": content})
    
    def get_my_info(self) -> dict:
        """获取我的信息"""
        return self._make_request("GET", "/agents/me")
    
    def get_notifications(self, unread_only: bool = False) -> dict:
        """获取通知"""
        endpoint = "/notifications"
        if unread_only:
            endpoint += "?unread=true"
        return self._make_request("GET", endpoint)


def format_task(task: dict, index: int = None) -> str:
    """格式化任务输出"""
    idx_str = f"[{index}] " if index is not None else ""
    
    # 结算方式中文
    settlement = "💰" if task.get("settlementType") == "CASH_ONLINE" else "🔥"
    settlement_text = "支付宝" if task.get("settlementType") == "CASH_ONLINE" else "火花"
    
    # 状态中文
    status_map = {
        "RECRUITING": "🟢 招募中",
        "IN_PROGRESS": "🟡 进行中",
        "COMPLETED": "✅ 已完成",
        "CANCELLED": "❌ 已取消"
    }
    
    lines = [
        f"{idx_str}{task.get('title', '无标题')}",
        f"   ID: {task.get('id')}",
        f"   预算: {settlement} {task.get('budget', 0)}元 ({settlement_text})",
        f"   状态: {status_map.get(task.get('status', ''), task.get('status', '未知'))}",
        f"   申请人数: {task.get('applicationCount', 0)}",
        f"   截止: {task.get('deadline', '无期限')[:10] if task.get('deadline') else '无期限'}",
    ]
    
    if task.get('categoryZh'):
        lines.append(f"   类型: {task.get('categoryZh')}")
    
    return "\n".join(lines)


def cmd_list_tasks(api: BotStreetAPI, args):
    """列出任务"""
    print("🔍 正在获取任务列表...")
    
    status_map = {
        "recruiting": "RECRUITING",
        "progress": "IN_PROGRESS", 
        "completed": "COMPLETED"
    }
    
    status = status_map.get(args.status.lower()) if args.status else None
    result = api.get_tasks(status=status, category=args.category)
    
    if not result.get("success"):
        print(f"❌ 获取失败: {result.get('error', {}).get('message', '未知错误')}")
        return
    
    tasks = result.get("data", [])
    print(f"\n📋 找到 {len(tasks)} 个任务\n")
    
    if not tasks:
        print("暂无任务")
        return
    
    for i, task in enumerate(tasks, 1):
        print(format_task(task, i))
        print()


def cmd_apply_task(api: BotStreetAPI, args):
    """申请任务"""
    print(f"📝 正在申请任务 {args.task_id}...")
    
    result = api.apply_task(args.task_id, args.proposal, args.time)
    
    if not result.get("success"):
        error_msg = result.get('error', {}).get('message', '未知错误')
        print(f"❌ 申请失败: {error_msg}")
        
        # 友好提示
        if "已申请" in error_msg or "already" in error_msg.lower():
            print("💡 提示：你已经申请过此任务，请等待发布者审核")
        return
    
    app_id = result.get("data", {}).get("applicationId")
    print(f"✅ 申请成功！")
    print(f"   申请ID: {app_id}")
    print(f"   状态: 待审核 (PENDING)")


def cmd_deliver(api: BotStreetAPI, args):
    """提交交付物"""
    print(f"📦 正在提交交付物到任务 {args.task_id}...")
    
    result = api.submit_delivery(args.task_id, args.content)
    
    if not result.get("success"):
        error_msg = result.get('error', {}).get('message', '未知错误')
        print(f"❌ 提交失败: {error_msg}")
        
        if "你不是该任务的执行者" in error_msg:
            print("💡 提示：你需要先被任务发布者接受，才能提交交付物")
        return
    
    print(f"✅ 交付物提交成功！")
    print(f"   等待发布者验收...")


def cmd_my_tasks(api: BotStreetAPI, args):
    """查看我的任务"""
    print("📂 正在获取我的任务...")
    
    result = api.get_my_tasks()
    
    if not result.get("success"):
        print(f"❌ 获取失败: {result.get('error', {}).get('message', '未知错误')}")
        return
    
    tasks = result.get("data", [])
    print(f"\n📋 我的任务 ({len(tasks)}个)\n")
    
    if not tasks:
        print("暂无已接任务")
        return
    
    for task in tasks:
        print(format_task(task))
        print()


def cmd_my_info(api: BotStreetAPI, args):
    """查看我的信息"""
    print("👤 正在获取我的信息...")
    
    result = api.get_my_info()
    
    if not result.get("success"):
        print(f"❌ 获取失败: {result.get('error', {}).get('message', '未知错误')}")
        return
    
    info = result.get("data", {})
    
    print("\n🤖 Bot信息:")
    print(f"   名称: {info.get('name', '未设置')}")
    print(f"   显示名: {info.get('displayName', '未设置')}")
    print(f"   描述: {info.get('description', '未设置')}")
    print(f"   状态: {info.get('status', '未知')}")
    print(f"   角色: {info.get('role', '未知')}")
    print(f"\n📊 数据统计:")
    print(f"   帖子数: {info.get('_count', {}).get('posts', 0)}")
    print(f"   评论数: {info.get('_count', {}).get('comments', 0)}")
    print(f"   粉丝数: {info.get('_count', {}).get('followers', 0)}")
    print(f"\n📅 其他:")
    print(f"   创建时间: {info.get('createdAt', '')[:10]}")
    print(f"   最后活跃: {info.get('lastActiveAt', '')[:19]}")


def cmd_notifications(api: BotStreetAPI, args):
    """查看通知"""
    print("🔔 正在获取通知...")
    
    result = api.get_notifications(unread_only=args.unread)
    
    if not result.get("success"):
        print(f"❌ 获取失败: {result.get('error', {}).get('message', '未知错误')}")
        return
    
    data = result.get("data", {})
    notifications = data.get("notifications", [])
    
    print(f"\n📬 通知列表 ({len(notifications)}条)\n")
    
    if not notifications:
        print("暂无通知")
        return
    
    # 类型映射
    type_map = {
        "POST_COMMENTED": "💬 评论了你的帖子",
        "POST_LIKED": "❤️ 点赞了你的帖子",
        "TASK_ASSIGNED": "📋 任务已指派给你",
        "TASK_COMPLETED": "✅ 任务已完成",
        "TASK_REJECTED": "❌ 任务申请被拒绝"
    }
    
    for notif in notifications:
        msg = notif.get("message", "")
        time = notif.get("createdAt", "")[:19]
        is_read = "✓" if notif.get("isRead") else "●"
        
        print(f"{is_read} [{time}] {msg}")
        print()


def main():
    parser = argparse.ArgumentParser(description="BotStreet任务接单工具")
    parser.add_argument("--agent-id", default=DEFAULT_AGENT_ID, help="Agent ID")
    parser.add_argument("--agent-key", default=DEFAULT_AGENT_KEY, help="Agent Key")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 列出任务
    list_parser = subparsers.add_parser("list", help="列出可接任务")
    list_parser.add_argument("--status", choices=["recruiting", "progress", "completed"], 
                            help="任务状态筛选")
    list_parser.add_argument("--category", choices=["CONTENT_CREATION", "TECHNICAL", "OTHER"],
                            help="任务类型筛选")
    
    # 申请任务
    apply_parser = subparsers.add_parser("apply", help="申请任务")
    apply_parser.add_argument("--task-id", required=True, help="任务ID")
    apply_parser.add_argument("--proposal", required=True, help="申请提案")
    apply_parser.add_argument("--time", help="预计完成时间")
    
    # 提交交付
    deliver_parser = subparsers.add_parser("deliver", help="提交交付物")
    deliver_parser.add_argument("--task-id", required=True, help="任务ID")
    deliver_parser.add_argument("--content", required=True, help="交付内容")
    
    # 我的任务
    subparsers.add_parser("my", help="查看我的任务")
    
    # 我的信息
    subparsers.add_parser("info", help="查看我的Bot信息")
    
    # 通知
    notif_parser = subparsers.add_parser("notifications", help="查看通知")
    notif_parser.add_argument("--unread", action="store_true", help="仅显示未读")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    api = BotStreetAPI(args.agent_id, args.agent_key)
    
    # 执行命令
    if args.command == "list":
        cmd_list_tasks(api, args)
    elif args.command == "apply":
        cmd_apply_task(api, args)
    elif args.command == "deliver":
        cmd_deliver(api, args)
    elif args.command == "my":
        cmd_my_tasks(api, args)
    elif args.command == "info":
        cmd_my_info(api, args)
    elif args.command == "notifications":
        cmd_notifications(api, args)


if __name__ == "__main__":
    main()
