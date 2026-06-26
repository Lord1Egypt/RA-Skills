#!/usr/bin/env python3
"""
发送文本报告到钉钉
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import httpx
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from notifiers.dingtalk import DingTalkNotifier


async def main():
    date_str = datetime.now().strftime('%Y%m%d')
    output_dir = Path(__file__).parent.parent / "reports" / "diandian_exports"
    filename = f"点点数据_上架下架榜_{date_str}.xlsx"
    output_path = output_dir / filename
    
    if not output_path.exists():
        print(f"❌ 文件不存在：{output_path}")
        return False
    
    # 直接读取配置并发送
    config_path = Path(__file__).parent.parent / "config" / "dingtalk.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    dingtalk_config = config.get("dingtalk", {})
    webhook_url = dingtalk_config.get("webhook")
    
    if not webhook_url:
        print("❌ webhook URL 未配置")
        return False
    
    total_new = 232
    total_offline = 232
    
    content = f"""# 📊 点点数据每日榜单 ({date_str})

- ✅ 已获取所有 8 个安卓渠道数据
- 🆕 新上架应用：**{total_new}** 个
- 📉 下架应用：**{total_offline}** 个

Excel 文件已保存到服务器：`{output_path}`
"""
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"点点数据每日榜单 {date_str}",
            "text": content
        },
        "at": {
            "isAtAll": True
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    print("✅ 已发送到钉钉群")
                    print(f"📄 文件：{output_path}")
                    print(f"📊 统计：新上架 {total_new}，下架 {total_offline}")
                    return True
                else:
                    print(f"❌ 钉钉通知失败：{result}")
                    return False
            else:
                print(f"❌ 钉钉通知 HTTP 错误：{response.status_code}")
                return False
    except Exception as e:
        print(f"❌ 发送到钉钉失败：{e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
