"""
授权拦截器中间件
"""

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.services.auth import AuthCodeService
from app.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

# 不需要授权的路径白名单
PUBLIC_PATHS = [
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/auth/verify",
    "/admin/add_auth",
    "/admin/create_auth",
    "/generate/progress",  # 查询进度的接口不需要授权
]


class AuthInterceptorMiddleware(BaseHTTPMiddleware):
    """授权拦截中间件"""

    async def dispatch(self, request: Request, call_next):
        # 检查是否在白名单中
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # 检查是否是 OPTIONS 请求（CORS预检）
        if request.method == "OPTIONS":
            return await call_next(request)

        # 从请求头或查询参数中获取授权码
        auth_code = request.headers.get("Authorization") or request.query_params.get("auth_code")

        if not auth_code:
            return JSONResponse(
                status_code=401,
                content={
                    "code": 401,
                    "msg": "未提供授权码",
                    "data": None
                }
            )

        # 去除 Bearer 前缀（如果有）
        if auth_code.startswith("Bearer "):
            auth_code = auth_code[7:]

        # 确定需要的权限类型
        required_permission = self._get_required_permission(request.url.path)

        # 验证授权码
        db = SessionLocal()
        try:
            auth_service = AuthCodeService(db)
            result = auth_service.verify_auth_code(auth_code, required_permission)

            if not result.valid:
                return JSONResponse(
                    status_code=403,
                    content={
                        "code": 403,
                        "msg": result.message,
                        "data": {
                            "permission": result.permission,
                            "remaining_count": result.remaining_count
                        }
                    }
                )

            # 将授权信息添加到请求状态中
            request.state.auth_code = auth_code
            request.state.permission = result.permission

            return await call_next(request)

        except Exception as e:
            logger.error(f"授权验证失败: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "code": 500,
                    "msg": "授权验证失败",
                    "data": None
                }
            )
        finally:
            db.close()

    def _get_required_permission(self, path: str) -> str:
        """
        根据路径确定需要的权限类型

        Args:
            path: 请求路径

        Returns:
            权限类型
        """
        if "/generate/" in path or "/case" in path:
            return "generate"
        elif "/execute/" in path or "/script/" in path:
            return "execute"
        else:
            return None  # 不需要特定权限检查
