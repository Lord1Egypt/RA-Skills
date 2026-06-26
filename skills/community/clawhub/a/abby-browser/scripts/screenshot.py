#!/usr/bin/env python3
"""
Abby Browser - 截图

封装 openclaw browser screenshot 命令
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path


def screenshot(full_page: bool = False, output_dir: str = None) -> dict:
    """
    截图
    
    Args:
        full_page: 是否截取整个页面
        output_dir: 输出目录
    
    Returns:
        dict: 结果 {'success': bool, 'message': str, 'path': str}
    """
    if output_dir is None:
        output_dir = os.path.expanduser('~/Downloads')
    
    # 生成文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'abby_screenshot_{timestamp}.png'
    filepath = os.path.join(output_dir, filename)
    
    cmd = ['openclaw', 'browser', 'screenshot']
    
    if full_page:
        cmd.append('--full-page')
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # 提取文件路径
            output = result.stdout.strip()
            if 'MEDIA:' in output:
                path = output.split('MEDIA:')[1].strip()
                return {
                    'success': True,
                    'message': f'📸 截图已保存',
                    'path': path
                }
            else:
                return {
                    'success': True,
                    'message': f'📸 截图完成',
                    'path': output
                }
        else:
            return {
                'success': False,
                'message': f'截图失败: {result.stderr}',
                'path': None
            }
    
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'message': '截图超时',
            'path': None
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'错误: {str(e)}',
            'path': None
        }


def main():
    """命令行入口"""
    full_page = '--full-page' in sys.argv
    
    result = screenshot(full_page=full_page)
    
    if result['success']:
        print(f"✅ {result['message']}")
        if result['path']:
            print(f"   路径: {result['path']}")
    else:
        print(f"❌ {result['message']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
