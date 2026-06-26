"""
管理后台Web界面
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

from .config import get_settings
from .database import db

# 创建管理后台应用
admin_app = FastAPI(title="阿里百炼用量统计管理后台")

# 模板目录
templates = Jinja2Templates(directory="templates")


@admin_app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """仪表盘首页"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 获取今日概览
    users = await db.list_users()
    total_users = len(users)
    
    # 计算今日总用量
    total_usage = 0
    active_users = 0
    for user in users:
        usage = await db.get_user_daily_usage(user.id, today)
        if usage > 0:
            active_users += 1
            total_usage += usage
    
    # 最近7天趋势
    dates = []
    usages = []
    for i in range(6, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date[5:])  # MM-DD
        day_usage = 0
        for user in users:
            day_usage += await db.get_user_daily_usage(user.id, date)
        usages.append(day_usage)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "today": today,
        "total_users": total_users,
        "active_users": active_users,
        "total_usage": total_usage,
        "dates": dates,
        "usages": usages
    })


@admin_app.get("/users", response_class=HTMLResponse)
async def users_list(request: Request, department: Optional[str] = None):
    """用户列表"""
    users = await db.list_users(department)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 添加今日用量
    user_list = []
    for user in users:
        usage = await db.get_user_daily_usage(user.id, today)
        user_list.append({
            "id": user.id,
            "name": user.name,
            "department": user.department,
            "api_key": user.api_key[:20] + "...",
            "daily_limit": user.daily_limit,
            "monthly_limit": user.monthly_limit,
            "today_usage": usage,
            "remaining": max(0, user.daily_limit - usage)
        })
    
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": user_list,
        "department": department
    })


@admin_app.get("/users/{user_id}", response_class=HTMLResponse)
async def user_detail(request: Request, user_id: str):
    """用户详情"""
    user = await db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 获取最近30天用量
    dates = []
    usages = []
    for i in range(29, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date[5:])
        usage = await db.get_user_daily_usage(user.id, date)
        usages.append(usage)
    
    # 获取最近日志
    logs = await db.query_usage_logs(user_id=user_id, limit=50)
    
    return templates.TemplateResponse("user_detail.html", {
        "request": request,
        "user": user,
        "dates": dates,
        "usages": usages,
        "logs": logs
    })


@admin_app.get("/usage", response_class=HTMLResponse)
async def usage_report(
    request: Request,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """用量报表"""
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    logs = await db.query_usage_logs(
        start_date=start_date,
        end_date=end_date,
        limit=10000
    )
    
    # 汇总统计
    total_requests = len(logs)
    total_input = sum(log.input_tokens for log in logs)
    total_output = sum(log.output_tokens for log in logs)
    total_tokens = sum(log.total_tokens for log in logs)
    
    # 按模型分组
    model_stats = {}
    for log in logs:
        model = log.model
        if model not in model_stats:
            model_stats[model] = {"requests": 0, "tokens": 0}
        model_stats[model]["requests"] += 1
        model_stats[model]["tokens"] += log.total_tokens
    
    # 按日期分组
    daily_stats = {}
    for log in logs:
        date = log.request_date
        if date not in daily_stats:
            daily_stats[date] = 0
        daily_stats[date] += log.total_tokens
    
    return templates.TemplateResponse("usage.html", {
        "request": request,
        "start_date": start_date,
        "end_date": end_date,
        "total_requests": total_requests,
        "total_input": total_input,
        "total_output": total_output,
        "total_tokens": total_tokens,
        "model_stats": model_stats,
        "daily_stats": daily_stats
    })
