#!/usr/bin/env python3
"""
测试钉钉文件上传功能
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from notifiers.dingtalk import DingTalkNotifier

async def test_dingtalk_upload():
    """测试钉钉上传"""
    dingtalk = DingTalkNotifier()
    
    # 创建一个测试文件
    test_file = Path("/tmp/test_dingtalk_upload.csv")
    test_file.write_text("测试内容\n渠道，应用数\n华为，100\n小米，80\n")
    
    print(f"📄 测试文件：{test_file}")
    print(f"📤 开始上传到钉钉...")
    
    success = await dingtalk.send_file(
        file_path=str(test_file),
        title="测试文件上传",
        message="这是一个测试文件"
    )
    
    if success:
        print("✅ 上传成功！")
    else:
        print("❌ 上传失败")
    
    # 清理测试文件
    test_file.unlink()
    
    return success


if __name__ == "__main__":
    success = asyncio.run(test_dingtalk_upload())
    sys.exit(0 if success else 1)
