"""
AI 自动化测试平台 - 主应用入口

使用 FastAPI 构建后端服务
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.dependencies import AuthInterceptorMiddleware
from app.api import auth, admin, generate, api_test, execute, ui_test, report, execution, system

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="AI 自动化测试平台",
    description="基于 LangChain+DeepSeek 的AI自动化测试平台",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加授权拦截中间件
app.add_middleware(AuthInterceptorMiddleware)

# 注册路由
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(generate.router, prefix="/api")
app.include_router(api_test.router, prefix="/api")
app.include_router(execute.router, prefix="/api")
app.include_router(ui_test.router, prefix="/api")
app.include_router(report.router, prefix="/api")
app.include_router(execution.router, prefix="/api")
app.include_router(system.router, prefix="/api")

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-test-platform"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Test Platform API",
        "docs": "/docs",
        "health": "/health"
    }

# 启动事件
@app.on_event("startup")
async def startup_event():
    logger.info("AI 自动化测试平台启动中...")
    logger.info("API 文档地址: http://localhost:8000/docs")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI 自动化测试平台关闭中...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
