"""
钉钉机器人通知
"""

import httpx
from pathlib import Path
from typing import Optional
import yaml

from utils.logger import setup_logger

logger = setup_logger()

# 向前兼容：App 类型引用（旧代码残留）
# 这个类在 v5.0 中已移除，这里只是为了让代码编译通过
class App:
    name: str = ""
    platform: str = ""
    package_name: str = ""
    last_checked: str = ""
    url: str = ""


class DingTalkNotifier:
    """钉钉机器人通知器"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # 尝试多个可能的配置路径
            possible_paths = [
                Path(__file__).parent.parent.parent / "config" / "dingtalk.yaml",
                Path(__file__).parent.parent / "config" / "dingtalk.yaml",
                Path(__file__).parent / "config" / "dingtalk.yaml",
            ]
            
            for path in possible_paths:
                if path.exists():
                    config_path = path
                    break
        
        self.webhook_url = None
        self.secret = None
        self.client_id = None
        self.client_secret = None
        self.chat_id = None
        
        if config_path and config_path.exists():
            logger.info(f"📄 读取钉钉配置：{config_path}")
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                
                # 企业应用配置（用于文件上传）
                dingtalk_config = config.get("dingtalk", {})
                self.webhook_url = dingtalk_config.get("webhook")
                self.secret = dingtalk_config.get("secret")
                self.client_id = dingtalk_config.get("client_id")
                self.client_secret = dingtalk_config.get("client_secret")
                self.chat_id = dingtalk_config.get("chat_id")
                
                logger.info(f"✅ 配置加载成功：client_id={self.client_id}, chat_id={self.chat_id}")
        else:
            logger.warning(f"❌ 钉钉配置文件不存在：{config_path}")
    
    async def send_offline_alert(self, app: App, result: dict):
        """发送下架告警"""
        if not self.webhook_url:
            logger.error("钉钉 webhook 未配置")
            return
        
        content = {
            "msgtype": "markdown",
            "markdown": {
                "title": f"⚠️ APP 下架告警 - {app.name}",
                "text": self._build_offline_message(app, result)
            },
            "at": {
                "isAtAll": True
            }
        }
        
        await self._send(content)
    
    async def send_recovery_alert(self, app: App):
        """发送恢复通知"""
        if not self.webhook_url:
            return
        
        content = {
            "msgtype": "markdown",
            "markdown": {
                "title": f"✓ APP 恢复通知 - {app.name}",
                "text": self._build_recovery_message(app)
            },
            "at": {
                "isAtAll": False
            }
        }
        
        await self._send(content)
    
    def _build_offline_message(self, app: App, result: dict) -> str:
        """构建下架消息"""
        return f"""## ⚠️ APP 下架告警 [下架]

**【下架】** APP 下架告警

- **应用名称**: {app.name}
- **平台**: {self._platform_name(app.platform)}
- **包名**: `{app.package_name}`
- **状态**: 🔴 已下架
- **检测时间**: {app.last_checked}
- **错误信息**: {result.get('error', '未知')}

[查看应用链接]({app.url})

> 请立即检查应用状态！"""
    
    async def send_file(self, file_path: str, title: str = "文件上传", message: str = ""):
        """
        发送文件通知到钉钉（Markdown 格式）
        
        Args:
            file_path: 文件路径
            title: 文件标题
            message: 附加消息
        """
        if not self.webhook_url:
            logger.error("钉钉 webhook 未配置")
            return False
        
        try:
            from datetime import datetime
            
            # 构建文件信息
            file_name = Path(file_path).name
            file_size = Path(file_path).stat().st_size / 1024  # KB
            
            # 发送 Markdown 消息
            content = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": f"""## 📊 数据文件导出

**{title}**

- **文件名称**: `{file_name}`
- **文件大小**: {file_size:.1f} KB
- **导出时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{message}

---
⚠️ 文件已下载到本地，请查看下载目录：`{file_path}`"""
                },
                "at": {
                    "isAtAll": True
                }
            }
            
            return await self._send(content)
            
        except Exception as e:
            logger.error(f"❌ 钉钉文件通知异常：{e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def send_text_message(self, message: str, at_all: bool = False):
        """发送文本消息到钉钉"""
        if not self.webhook_url:
            logger.error("钉钉 webhook 未配置")
            return False
        
        content = {
            "msgtype": "text",
            "text": {
                "content": message
            },
            "at": {
                "isAtAll": at_all
            }
        }
        
        return await self._send(content)
    
    def _build_recovery_message(self, app: App) -> str:
        """构建恢复消息"""
        return f"""## ✓ APP 恢复通知 [恢复]

**【恢复】** APP 已重新上架

- **应用名称**: {app.name}
- **平台**: {self._platform_name(app.platform)}
- **包名**: `{app.package_name}`
- **状态**: 🟢 已恢复

[查看应用链接]({app.url})

> 应用已重新上架"""
    
    def _platform_name(self, platform: str) -> str:
        """平台名称映射"""
        mapping = {
            "huawei": "华为应用市场",
            "xiaomi": "小米应用商店",
            "tencent": "应用宝",
            "wandoujia": "豌豆荚"
        }
        return mapping.get(platform, platform)
    
    async def _send(self, content: dict):
        """发送消息"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.webhook_url,
                    json=content,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("errcode") == 0:
                        logger.info("钉钉通知发送成功")
                    else:
                        logger.error(f"钉钉通知失败：{result}")
                else:
                    logger.error(f"钉钉通知 HTTP 错误：{response.status_code}")
                    
        except Exception as e:
            logger.error(f"钉钉通知异常：{e}")
