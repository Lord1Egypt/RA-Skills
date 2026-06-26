"""
API路由
"""

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.responses import StreamingResponse, JSONResponse
import uuid
import json

from .config import get_settings
from .database import db
from .models import User, UserCreate, UserResponse, UsageQuery, UsageReport
from .proxy import proxy

# 创建FastAPI应用
app = FastAPI(
    title="阿里百炼用量统计代理",
    description="多人共享账号场景下的精细化用量统计方案",
    version="1.0.0"
)


async def verify_api_key(x_api_key: str = Header(...)) -> User:
    """验证API Key"""
    user = await db.get_user_by_api_key(x_api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return user


# ============ OpenAI兼容API ============

@app.post("/v1/chat/completions")
async def chat_completions(
    request: dict,
    user: User = Depends(verify_api_key)
):
    """
    OpenAI兼容的聊天完成API
    
    与OpenAI API格式完全兼容，支持流式和非流式响应
    """
    stream = request.get("stream", False)
    
    if stream:
        # 流式响应
        async def generate():
            async for chunk in proxy.forward_request(user.id, request, stream=True):
                yield chunk
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    else:
        # 非流式响应
        async def generate():
            async for chunk in proxy.forward_request(user.id, request, stream=False):
                yield chunk
        
        content = b""
        async for chunk in generate():
            content += chunk
        
        return JSONResponse(content=json.loads(content))


@app.post("/v1/completions")
async def completions(
    request: dict,
    user: User = Depends(verify_api_key)
):
    """文本完成API（兼容OpenAI）"""
    # 转发到chat/completions
    return await chat_completions(request, user)


@app.post("/v1/embeddings")
async def embeddings(
    request: dict,
    user: User = Depends(verify_api_key)
):
    """Embedding API（兼容OpenAI）"""
    # TODO: 实现embedding转发
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Embeddings not yet implemented"
    )


@app.get("/v1/models")
async def list_models(user: User = Depends(verify_api_key)):
    """列出可用模型"""
    return {
        "object": "list",
        "data": [
            {"id": "qwen-turbo", "object": "model"},
            {"id": "qwen-plus", "object": "model"},
            {"id": "qwen-max", "object": "model"},
            {"id": "qwen-max-longcontext", "object": "model"},
        ]
    }


# ============ 管理API ============

@app.post("/admin/users", response_model=UserResponse)
async def create_user(user_create: UserCreate):
    """创建用户"""
    # 生成唯一ID和API Key
    user_id = f"user_{uuid.uuid4().hex[:16]}"
    api_key = f"bl-{uuid.uuid4().hex}"
    
    user = User(
        id=user_id,
        name=user_create.name,
        department=user_create.department,
        api_key=api_key,
        daily_limit=user_create.daily_limit,
        monthly_limit=user_create.monthly_limit
    )
    
    await db.create_user(user)
    return user


@app.get("/admin/users", response_model=List[UserResponse])
async def list_users(department: Optional[str] = None):
    """列出所有用户"""
    users = await db.list_users(department)
    return users


@app.get("/admin/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """获取用户信息"""
    user = await db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ============ 用量统计API ============

@app.get("/admin/usage/today")
async def get_today_usage(user_id: Optional[str] = None):
    """获取今日用量"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if user_id:
        # 单个用户
        user = await db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        usage = await db.get_user_daily_usage(user_id, today)
        return {
            "user_id": user_id,
            "user_name": user.name,
            "date": today,
            "usage": usage,
            "limit": user.daily_limit,
            "remaining": max(0, user.daily_limit - usage)
        }
    else:
        # 所有用户
        users = await db.list_users()
        result = []
        for user in users:
            usage = await db.get_user_daily_usage(user.id, today)
            result.append({
                "user_id": user.id,
                "user_name": user.name,
                "department": user.department,
                "usage": usage,
                "limit": user.daily_limit,
                "remaining": max(0, user.daily_limit - usage)
            })
        return {"date": today, "users": result}


@app.get("/admin/usage/report")
async def get_usage_report(
    user_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """获取用量报表"""
    # 默认最近7天
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    logs = await db.query_usage_logs(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        limit=10000
    )
    
    # 汇总统计
    total_requests = len(logs)
    total_input_tokens = sum(log.input_tokens for log in logs)
    total_output_tokens = sum(log.output_tokens for log in logs)
    total_tokens = sum(log.total_tokens for log in logs)
    
    # 按模型分组
    model_stats = {}
    for log in logs:
        model = log.model
        if model not in model_stats:
            model_stats[model] = {"requests": 0, "tokens": 0}
        model_stats[model]["requests"] += 1
        model_stats[model]["tokens"] += log.total_tokens
    
    return {
        "period": f"{start_date} to {end_date}",
        "total_requests": total_requests,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_tokens,
        "model_breakdown": model_stats,
        "daily_logs": [
            {
                "date": log.request_date,
                "user_id": log.user_id,
                "model": log.model,
                "input_tokens": log.input_tokens,
                "output_tokens": log.output_tokens,
                "total_tokens": log.total_tokens,
                "response_time_ms": log.response_time_ms
            }
            for log in logs[:100]  # 限制返回数量
        ]
    }


@app.get("/admin/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
