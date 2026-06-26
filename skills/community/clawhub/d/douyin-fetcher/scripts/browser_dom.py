#!/usr/bin/env python3
"""
Browser DOM - 浏览器 DOM 抓取

通过浏览器打开抖音页面，从 DOM 中提取视频 CDN 地址。

注意：此模块无法独立完成全部流程。
- 短链解析和 modal_id 提取由上层 fetcher.py 统一处理
- 浏览器操作需要 OpenClaw agent 配合执行 browser 工具
- 本模块提供：操作指引（instruction）和辅助函数（下载）
"""

import json
import subprocess
import re
import platform
from pathlib import Path
from typing import Dict, Optional


# curl 命令（跨平台）
CURL_CMD = "curl.exe" if platform.system() == "Windows" else "curl"


class BrowserFetcher:
    """浏览器抓取器
    
    由于浏览器操作需要 OpenClaw browser 工具，
    本类主要提供操作指引和辅助函数。
    """
    
    # 提取视频 URL 的 JavaScript 代码
    GET_VIDEO_URL_JS = """(() => {
    const videos = document.querySelectorAll('video');
    const results = [];
    for (const v of videos) {
        const src = v.currentSrc || v.src;
        if (src && src.startsWith('http') && !src.includes('uuu_265')) {
            results.push(src);
        }
    }
    // 优先返回非 blob 的地址
    for (const url of results) {
        if (!url.startsWith('blob:')) return url;
    }
    return results.length > 0 ? results[0] : null;
})()"""

    # 提取音频流 URL 的 JavaScript（DASH 格式）
    GET_AUDIO_URL_JS = """(() => {
    const audios = document.querySelectorAll('audio');
    for (const a of audios) {
        const src = a.currentSrc || a.src;
        if (src && src.startsWith('http')) return src;
    }
    // 尝试从 performance entries 获取
    const entries = performance.getEntriesByType('resource');
    for (const e of entries) {
        if (e.name.includes('.m4a') || e.name.includes('audio')) {
            return e.name;
        }
    }
    return null;
})()"""

    # 提取页面标题的 JavaScript
    GET_TITLE_JS = """(() => {
    // 方式1：meta 标签
    const meta = document.querySelector('meta[name="description"]');
    if (meta && meta.content) return meta.content;
    // 方式2：页面标题
    const title = document.title;
    if (title) return title.replace(/ - 抖音$/, '').trim();
    return null;
})()"""
    
    def __init__(self):
        pass
    
    def generate_instruction(self, modal_id: str, page_url: Optional[str] = None, 
                              output_path: Optional[str] = None) -> Dict:
        """生成浏览器操作指引
        
        供 OpenClaw agent 按步骤执行。
        
        Args:
            modal_id: 视频 ID
            page_url: 视频页面 URL
            output_path: 视频输出路径
            
        Returns:
            包含操作步骤的指引字典
        """
        if not page_url:
            page_url = f"https://www.douyin.com/video/{modal_id}"
        
        if not output_path:
            output_path = f"/path/to/temp/douyin\\douyin_{modal_id}.mp4"
        
        return {
            "needs_agent": True,
            "modal_id": modal_id,
            "page_url": page_url,
            "output_path": output_path,
            "steps": [
                {
                    "step": 1,
                    "description": "打开抖音视频页面",
                    "tool_call": f"browser(action='open', profile='openclaw', targetUrl='{page_url}')"
                },
                {
                    "step": 2,
                    "description": "等待页面加载（5秒）",
                    "tool_call": "browser(action='act', kind='wait', timeMs=5000)"
                },
                {
                    "step": 3,
                    "description": "提取页面标题",
                    "tool_call": f"browser(action='act', kind='evaluate', fn={json.dumps(self.GET_TITLE_JS)})",
                    "note": "记录标题用于文件命名"
                },
                {
                    "step": 4,
                    "description": "提取视频 CDN 地址",
                    "tool_call": f"browser(action='act', kind='evaluate', fn={json.dumps(self.GET_VIDEO_URL_JS)})",
                    "retry": {
                        "condition": "返回 null 或含 uuu_265",
                        "action": "等待 3 秒后重试，最多 3 次"
                    }
                },
                {
                    "step": 5,
                    "description": "下载视频",
                    "command": f'{CURL_CMD} -L -H "Referer: https://www.douyin.com/" -o "{output_path}" "<CDN_URL>"',
                    "note": "将 <CDN_URL> 替换为 Step 4 获取的地址"
                },
                {
                    "step": 6,
                    "description": "验证下载（检查文件大小）",
                    "note": "文件应大于 100KB，否则可能下载失败"
                }
            ],
            "dash_fallback": {
                "description": "如果视频没有声音（DASH 格式），需要单独下载音频",
                "steps": [
                    {
                        "description": "提取音频流 URL",
                        "tool_call": f"browser(action='act', kind='evaluate', fn={json.dumps(self.GET_AUDIO_URL_JS)})"
                    },
                    {
                        "description": "下载音频流",
                        "command": f'{CURL_CMD} -L -H "Referer: https://www.douyin.com/" -o "/path/to/temp/douyin\\audio_{modal_id}.m4a" "<AUDIO_URL>"'
                    },
                    {
                        "description": "合并音视频（可选）",
                        "command": f'ffmpeg -i "{output_path}" -i "/path/to/temp/douyin\\audio_{modal_id}.m4a" -c copy "/path/to/temp/douyin\\merged_{modal_id}.mp4" -y'
                    }
                ]
            },
            "troubleshooting": [
                "JS 返回 null → 页面未加载完，等待 3-5 秒重试",
                "返回含 uuu_265 → 占位视频，等待重试",
                "返回 blob: → 流式加载，等待真实 URL 出现",
                "下载 403 → 检查 Referer 头；链接可能过期，重新获取",
                "视频没声音 → DASH 格式，执行 dash_fallback 步骤",
                "登录弹窗 → 直接关闭或忽略，视频列表通常仍可获取"
            ]
        }
    
    def download_video(self, video_url: str, output_path: str) -> bool:
        """下载视频（辅助函数）
        
        Args:
            video_url: 视频 CDN 地址
            output_path: 输出路径
            
        Returns:
            是否成功
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            CURL_CMD, "-L",
            "-H", "Referer: https://www.douyin.com/",
            "-o", output_path,
            video_url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                return False
            
            # 验证文件大小
            file_size = Path(output_path).stat().st_size
            if file_size < 1024:
                print(f"⚠️ 下载文件过小 ({file_size} bytes)，可能不是有效视频")
                return False
            
            return True
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return False


# 测试代码
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python browser_dom.py <modal_id> [page_url]")
        print("\n此脚本生成浏览器操作指引，供 OpenClaw agent 执行。")
        sys.exit(1)
    
    modal_id = sys.argv[1]
    page_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    fetcher = BrowserFetcher()
    instruction = fetcher.generate_instruction(modal_id, page_url)
    
    print(json.dumps(instruction, ensure_ascii=False, indent=2))