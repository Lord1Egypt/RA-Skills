"""
代理核心逻辑
"""

import time
import uuid
from datetime import datetime
from typing import Optional, AsyncGenerator
import httpx
from fastapi import HTTPException, status

from .config import get_settings
from .database import db
from .models import UsageLog


class BailianProxy:
    """阿里百炼代理"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(
            base_url=self.settings.bailian_base_url,
            headers={"Authorization": f"Bearer {self.settings.bailian_api_key}"},
            timeout=60.0
        )
    
    async def forward_request(
        self,
        user_id: str,
        request_data: dict,
        stream: bool = False
    ) -> AsyncGenerator[bytes, None]:
        """
        转发请求到阿里百炼并记录用量
        
        Args:
            user_id: 用户ID
            request_data: 请求数据
            stream: 是否流式响应
        """
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # 检查用户日限额
            today = datetime.now().strftime("%Y-%m-%d")
            daily_usage = await db.get_user_daily_usage(user_id, today)
            user = await db.get_user_by_id(user_id)
            
            if user and daily_usage >= user.daily_limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Daily limit exceeded: {daily_usage}/{user.daily_limit} tokens"
                )
            
            # 转发请求
            if stream:
                # 流式响应
                async with self.client.stream(
                    "POST",
                    "/chat/completions",
                    json=request_data
                ) as response:
                    response.raise_for_status()
                    
                    # 收集完整响应用于统计
                    full_response = []
                    input_tokens = 0
                    output_tokens = 0
                    model = request_data.get("model", "unknown")
                    
                    async for chunk in response.aiter_bytes():
                        full_response.append(chunk)
                        yield chunk
                    
                    # 解析用量（简化版，实际需要解析SSE格式）
                    response_text = b"".join(full_response).decode('utf-8')
                    # TODO: 准确解析token用量
                    
                    # 估算token数（粗略估计）
                    input_text = request_data.get("messages", [{}])[0].get("content", "")
                    input_tokens = len(input_text) // 4  # 粗略估计
                    output_tokens = len(response_text) // 4
                    
                    # 记录用量
                    await self._log_usage(
                        user_id=user_id,
                        request_id=request_id,
                        model=model,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        request_type="chat.completion",
                        status_code=response.status_code,
                        response_time_ms=int((time.time() - start_time) * 1000)
                    )
            else:
                # 非流式响应
                response = await self.client.post(
                    "/chat/completions",
                    json=request_data
                )
                response.raise_for_status()
                
                result = response.json()
                
                # 提取用量信息
                usage = result.get("usage", {})
                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)
                model = result.get("model", request_data.get("model", "unknown"))
                
                # 记录用量
                await self._log_usage(
                    user_id=user_id,
                    request_id=request_id,
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    request_type="chat.completion",
                    status_code=response.status_code,
                    response_time_ms=int((time.time() - start_time) * 1000)
                )
                
                yield response.content
                
        except httpx.HTTPStatusError as e:
            # 记录错误
            await self._log_usage(
                user_id=user_id,
                request_id=request_id,
                model=request_data.get("model", "unknown"),
                input_tokens=0,
                output_tokens=0,
                request_type="chat.completion",
                status_code=e.response.status_code,
                response_time_ms=int((time.time() - start_time) * 1000)
            )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Bailian API error: {e.response.text}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    async def _log_usage(
        self,
        user_id: str,
        request_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        request_type: str,
        status_code: int,
        response_time_ms: int
    ):
        """记录用量日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        log = UsageLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            request_id=request_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            request_type=request_type,
            status_code=status_code,
            response_time_ms=response_time_ms,
            request_date=today
        )
        
        await db.log_usage(log)
        
        # 更新每日统计
        await self._update_daily_stats(user_id, today, log)
    
    async def _update_daily_stats(self, user_id: str, stats_date: str, log: UsageLog):
        """更新每日统计"""
        stats = await db.get_daily_stats(user_id, stats_date)
        
        if stats:
            # 累加统计
            await db.update_daily_stats(
                user_id=user_id,
                stats_date=stats_date,
                total_requests=stats.total_requests + 1,
                total_input_tokens=stats.total_input_tokens + log.input_tokens,
                total_output_tokens=stats.total_output_tokens + log.output_tokens,
                total_tokens=stats.total_tokens + log.total_tokens
            )
        else:
            # 创建新统计
            await db.update_daily_stats(
                user_id=user_id,
                stats_date=stats_date,
                total_requests=1,
                total_input_tokens=log.input_tokens,
                total_output_tokens=log.output_tokens,
                total_tokens=log.total_tokens
            )


# 全局代理实例
proxy = BailianProxy()
