"""
UI自动化测试相关的 Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class UiScriptCreate(BaseModel):
    """创建UI脚本请求"""
    name: str = Field(..., description="脚本名称")
    content: str = Field(..., description="脚本代码")
    type: str = Field(default="ui", description="脚本类型：ui")


class UiScriptUpdate(BaseModel):
    """更新UI脚本请求"""
    name: Optional[str] = Field(None, description="脚本名称")
    content: Optional[str] = Field(None, description="脚本代码")
    status: Optional[str] = Field(None, description="状态：active/archived")


class BrowserConfig(BaseModel):
    """浏览器配置"""
    browser_type: str = Field(default="chromium", description="浏览器类型：chromium/webkit/firefox")
    headless: bool = Field(default=True, description="是否无头模式")
    viewport: Optional[Dict[str, int]] = Field(default={"width": 1920, "height": 1080}, description="视口大小")
    slow_mo: Optional[int] = Field(default=0, description="操作延迟（毫秒）")


class UiExecuteRequest(BaseModel):
    """UI执行请求"""
    script_id: int = Field(..., description="脚本ID")
    browser_config: Optional[BrowserConfig] = Field(None, description="浏览器配置")
    timeout: Optional[int] = Field(default=600, description="超时时间（秒）")


class UiExecuteBatchRequest(BaseModel):
    """UI批量执行请求"""
    script_ids: List[int] = Field(..., description="脚本ID列表")
    browser_config: Optional[BrowserConfig] = Field(None, description="浏览器配置")
    timeout: Optional[int] = Field(default=1200, description="总超时时间（秒）")


class UiExecuteResult(BaseModel):
    """UI执行结果"""
    script_id: int
    script_name: str
    result: str  # success/fail
    duration: int  # 执行耗时（秒）
    screenshot_count: int  # 截图数量
    trace_path: Optional[str] = None  # Trace文件路径
    log: str
