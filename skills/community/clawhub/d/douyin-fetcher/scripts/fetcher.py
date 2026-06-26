#!/usr/bin/env python3
"""
Douyin Fetcher - 抖音视频获取模块

支持多种下载方式：
1. TikHub API（推荐）
2. 浏览器 DOM 抓取（fallback）

支持多种输入格式：
- 短链：https://v.douyin.com/iYxxxxxx/
- 完整链接：https://www.douyin.com/video/7616020798351871284
- modal_id 参数：https://www.douyin.com/jingxuan?modal_id=7597329042169220398
- 纯数字 modal_id：7616020798351871284

优先级策略：
- 先检查方法可用性（Token 是否配置），不可用直接跳过
- TikHub API 超时缩短到 15 秒，快速 fallback
- 短链解析失败时，浏览器方式可以直接打开短链
- browser_dom 返回 needs_agent 视为"有效 fallback"而非失败
"""

import os
import sys
import json
import re
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Optional

# 配置路径
DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "skills" / "douyin-config.json"
FALLBACK_CONFIG_PATH = Path.home() / ".openclaw" / "config.json"
TEMP_DIR = Path("/path/to/temp/douyin")


def load_douyin_config() -> Dict:
    """加载抖音模块配置"""
    if DEFAULT_CONFIG_PATH.exists():
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    if FALLBACK_CONFIG_PATH.exists():
        with open(FALLBACK_CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("douyin", {})
    return {}


def resolve_short_url(url: str) -> Optional[str]:
    """解析抖音短链接"""
    if "v.douyin.com" not in url:
        return None
    try:
        cmd = ["curl.exe", "-sL", "-o", "NUL", "-w", "%{url_effective}", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            effective_url = result.stdout.strip()
            if "douyin.com" in effective_url:
                return effective_url
    except Exception:
        pass
    return None


def extract_modal_id(text: str) -> Optional[str]:
    """从各种格式的输入中提取 modal_id"""
    # 1. modal_id=XXX 或 modal_id:XXX
    m = re.search(r'modal_id[=:]([\d]+)', text)
    if m:
        return m.group(1)
    # 2. /video/XXX
    m = re.search(r'/video/(\d{16,})', text)
    if m:
        return m.group(1)
    # 3. 纯数字（16位以上）
    m = re.search(r'^(\d{16,})$', text.strip())
    if m:
        return m.group(1)
    return None


class DouyinFetcher:
    """抖音视频获取器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or load_douyin_config()
        self.temp_dir = Path(self.config.get("temp_dir", str(TEMP_DIR)))
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def _check_method_available(self, method: str) -> bool:
        """预检方法是否可用（快速判断，不发网络请求）
        
        Args:
            method: 下载方式名称
            
        Returns:
            是否可用
        """
        if method == "tikhub_api":
            token = self.config.get("tikhub_api_token", "")
            if not token:
                print(f"  ⏭️ tikhub_api: Token 未配置，跳过")
                return False
            return True
        
        if method == "browser_dom":
            # 浏览器方式始终可用（需要 agent 配合，但不需要预配置）
            return True
        
        return False
        
    def fetch(self, input_url: str, output_path: Optional[str] = None) -> Dict:
        """获取视频
        
        优先级策略：
        1. 预检方法可用性，不可用直接跳过（不浪费时间）
        2. 短链解析失败不终止，浏览器可以直接打开短链
        3. browser_dom 返回 needs_agent 视为有效结果
        
        Returns:
            {
                "success": bool,          # 视频已下载到本地
                "needs_agent": bool,      # 需要 agent 配合执行浏览器操作
                "video_path": str,
                "modal_id": str,
                "title": str,
                "metadata": dict,
                "method_used": str,
                "instruction": dict,      # 浏览器操作指引（needs_agent=True 时）
                "error": str,
                "errors": list
            }
        """
        errors = []
        
        # Step 1: 解析短链
        resolved_url = input_url
        short_link_resolved = True
        
        if "v.douyin.com" in input_url:
            print(f"🔗 解析短链: {input_url}")
            resolved = resolve_short_url(input_url)
            if resolved:
                resolved_url = resolved
                print(f"✅ 解析成功: {resolved_url}")
            else:
                short_link_resolved = False
                errors.append("短链解析失败（curl 重定向失败）")
                print(f"⚠️ 短链解析失败")
        
        # Step 2: 提取 modal_id
        modal_id = extract_modal_id(resolved_url)
        if not modal_id:
            modal_id = extract_modal_id(input_url)
        
        # 如果短链解析失败且无法提取 modal_id
        # 不直接终止！浏览器方式可以直接打开短链
        if not modal_id and not short_link_resolved:
            print(f"⚠️ 无法提取 modal_id，但浏览器可以直接打开短链")
        elif not modal_id:
            return {
                "success": False,
                "needs_agent": False,
                "error": f"无法提取 modal_id。输入: {input_url}",
                "errors": errors
            }
        
        if modal_id:
            print(f"🎯 modal_id: {modal_id}")
        
        # Step 3: 按优先级尝试下载
        methods = self.config.get("downloader_priority", ["tikhub_api", "browser_dom"])
        browser_instruction = None  # 保存浏览器指引，作为最终 fallback
        
        for method in methods:
            # 预检可用性
            if not self._check_method_available(method):
                continue
            
            try:
                print(f"📥 尝试: {method}")
                
                if method == "tikhub_api":
                    if not modal_id:
                        errors.append("tikhub_api: 无 modal_id，跳过")
                        continue
                    result = self._fetch_via_tikhub(modal_id, output_path)
                    
                elif method == "browser_dom":
                    result = self._fetch_via_browser(
                        modal_id, 
                        resolved_url if short_link_resolved else input_url,
                        output_path
                    )
                else:
                    continue
                
                # 完全成功（视频已下载）
                if result.get("success"):
                    result["method_used"] = method
                    result["modal_id"] = modal_id
                    result["needs_agent"] = False
                    return result
                
                # 浏览器方式返回 needs_agent（有效 fallback，保存指引）
                if result.get("needs_agent"):
                    browser_instruction = result
                    continue
                
                # 真正失败
                errors.append(f"{method}: {result.get('error', '未知错误')}")
                    
            except Exception as e:
                errors.append(f"{method}: {e}")
                print(f"⚠️ {method} 失败: {e}", file=sys.stderr)
                continue
        
        # 所有自动方式都失败，但有浏览器指引
        if browser_instruction:
            browser_instruction["errors"] = errors
            browser_instruction["modal_id"] = modal_id
            return browser_instruction
        
        # 完全失败
        return {
            "success": False,
            "needs_agent": False,
            "modal_id": modal_id,
            "error": "所有下载方式都失败了",
            "errors": errors
        }
    
    def _fetch_via_tikhub(self, modal_id: str, output_path: Optional[str]) -> Dict:
        """通过 TikHub API 获取视频
        
        Token 可用性已由 _check_method_available 预检。
        """
        sys.path.append(str(Path(__file__).parent))
        from tikhub_api import TikHubAPI
        
        token = self.config.get("tikhub_api_token")
        api = TikHubAPI(token)
        
        video_url, title = api.get_video_url_and_title(modal_id)
        if not video_url:
            return {"success": False, "error": "TikHub API 未返回视频链接"}
        
        if not output_path:
            output_path = str(self.temp_dir / f"douyin_{modal_id}.mp4")
        
        api.download_video(video_url, output_path)
        
        return {
            "success": True,
            "video_path": output_path,
            "title": title or "",
            "metadata": {
                "modal_id": modal_id,
                "source": "tikhub_api",
                "video_url": video_url
            }
        }
    
    def _fetch_via_browser(self, modal_id: Optional[str], page_url: str, 
                           output_path: Optional[str]) -> Dict:
        """通过浏览器抓取获取视频
        
        返回 needs_agent=True 和操作指引。
        即使没有 modal_id，也可以用原始 URL 打开页面。
        """
        sys.path.append(str(Path(__file__).parent))
        from browser_dom import BrowserFetcher
        
        # 构建页面 URL
        if modal_id and (not page_url or "douyin.com" not in page_url):
            page_url = f"https://www.douyin.com/video/{modal_id}"
        
        if not output_path and modal_id:
            output_path = str(self.temp_dir / f"douyin_{modal_id}.mp4")
        elif not output_path:
            output_path = str(self.temp_dir / "douyin_video.mp4")
        
        fetcher = BrowserFetcher()
        instruction = fetcher.generate_instruction(
            modal_id or "unknown", 
            page_url, 
            output_path
        )
        
        return {
            "success": False,
            "needs_agent": True,
            "error": "浏览器抓取需要 agent 配合执行",
            "instruction": instruction,
            "modal_id": modal_id
        }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="抖音视频获取模块")
    parser.add_argument("input", help="抖音链接或 modal_id")
    parser.add_argument("-o", "--output", help="输出路径")
    parser.add_argument("--method", choices=["tikhub_api", "browser_dom"], help="指定下载方式")
    
    args = parser.parse_args()
    
    fetcher = DouyinFetcher()
    
    if args.method:
        fetcher.config["downloader_priority"] = [args.method]
    
    result = fetcher.fetch(args.input, args.output)
    
    if result.get("success"):
        print(f"\n✅ 下载成功")
        print(f"视频路径: {result['video_path']}")
        print(f"modal_id: {result.get('modal_id')}")
        if result.get('title'):
            print(f"标题: {result['title']}")
        print(f"下载方式: {result['method_used']}")
    elif result.get("needs_agent"):
        print(f"\n⚠️ 需要 agent 配合执行浏览器操作")
        print(json.dumps(result["instruction"], ensure_ascii=False, indent=2))
    else:
        print(f"\n❌ 下载失败: {result.get('error')}")
        if result.get("errors"):
            for err in result["errors"]:
                print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()