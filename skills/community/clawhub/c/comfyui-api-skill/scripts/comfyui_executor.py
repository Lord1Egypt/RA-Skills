#!/usr/bin/env python3
"""
ComfyUI 工作流执行器

功能：
1. 提交工作流到 ComfyUI 服务
2. 轮询执行状态
3. 下载生成的图像
4. 支持从配置文件读取配置

使用示例：
    python comfyui_executor.py --workflow ./workflow.json --output-dir ./output --timeout 300
    python comfyui_executor.py --workflow ./workflow.json  # 使用配置文件中的默认值
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import requests
except ImportError:
    print("错误：缺少 requests 库，请运行：pip install requests>=2.28.0")
    sys.exit(1)

# 导入配置加载器
try:
    from config_loader import get_config
except ImportError:
    # 如果导入失败，使用相对路径
    sys.path.insert(0, str(Path(__file__).parent))
    from config_loader import get_config


class ComfyUIExecutor:
    """ComfyUI 工作流执行器"""
    
    def __init__(
        self,
        server_url: str = None,
        api_key: str = None,
        timeout: int = None,
        poll_interval: int = None,
        auto_detect_timeout: bool = True
    ):
        """
        初始化执行器
        
        Args:
            server_url: ComfyUI 服务地址
            api_key: API 密钥（可选）
            timeout: 超时时间（秒）
            poll_interval: 轮询间隔（秒）
            auto_detect_timeout: 是否根据工作流自动检测超时时间
        """
        # 加载配置
        config = get_config()
        
        # 使用配置优先级：参数 > 配置文件 > 环境变量 > 默认值
        self.server_url = config.get_server_url(cli_value=server_url)
        self.api_key = config.get_api_key(cli_value=api_key)
        self.timeout = timeout  # 稍后在 execute 时确定
        self.default_timeout = config.get_timeout()
        self.video_timeout = config.get_timeout(for_video=True)
        self.poll_interval = poll_interval or config.get('execution.poll_interval', default=2)
        self.auto_detect_timeout = auto_detect_timeout
        
        self.session = requests.Session()
        
        # 设置请求头
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
    
    def detect_workflow_type(self, workflow: Dict[str, Any]) -> str:
        """
        检测工作流类型（图像/视频）
        
        Args:
            workflow: 工作流 JSON
            
        Returns:
            工作流类型：'video' 或 'image'
        """
        # 检查是否包含视频相关节点
        video_node_types = {
            'VHS_VideoCombine',
            'VHS_LoadVideo',
            'VHS_LoadVideoPath',
            'SaveVideo',
            'VideoCombine',
            'AnimateDiff',
            'AnimateDiffCombine',
            'ADE_AnimateDiffCombine',
            'ADE_AnimateDiffSampler'
        }
        
        for node_id, node_data in workflow.items():
            if isinstance(node_data, dict):
                class_type = node_data.get('class_type', '')
                if class_type in video_node_types:
                    return 'video'
        
        # 检查输出类型
        # 如果有大量帧数或视频相关参数，也可能是视频
        for node_id, node_data in workflow.items():
            if isinstance(node_data, dict):
                inputs = node_data.get('inputs', {})
                # 检查帧数参数
                if 'frame_count' in inputs or 'frames' in inputs:
                    return 'video'
        
        return 'image'
    
    def get_timeout_for_workflow(self, workflow: Dict[str, Any]) -> int:
        """
        根据工作流类型获取合适的超时时间
        
        Args:
            workflow: 工作流 JSON
            
        Returns:
            超时时间（秒）
        """
        if self.timeout is not None:
            # 用户明确指定了超时时间
            return self.timeout
        
        if not self.auto_detect_timeout:
            # 不自动检测，使用默认超时
            return self.default_timeout
        
        # 自动检测工作流类型
        workflow_type = self.detect_workflow_type(workflow)
        
        if workflow_type == 'video':
            print(f"ℹ️ 检测到视频工作流，使用视频超时时间：{self.video_timeout} 秒（{self.video_timeout/60:.1f} 分钟）")
            return self.video_timeout
        else:
            print(f"ℹ️ 使用默认超时时间：{self.default_timeout} 秒（{self.default_timeout/60:.1f} 分钟）")
            return self.default_timeout
    
    def submit_workflow(self, workflow: Dict[str, Any]) -> str:
        """
        提交工作流
        
        Args:
            workflow: 工作流 JSON 对象
            
        Returns:
            prompt_id: 任务 ID
            
        Raises:
            Exception: 提交失败时抛出异常
        """
        url = f"{self.server_url}/prompt"
        
        try:
            response = self.session.post(url, json={"prompt": workflow}, timeout=30)
            
            if response.status_code >= 400:
                raise Exception(f"提交工作流失败: HTTP {response.status_code}, {response.text}")
            
            data = response.json()
            
            if "error" in data:
                raise Exception(f"工作流错误: {data['error']}")
            
            prompt_id = data.get("prompt_id")
            if not prompt_id:
                raise Exception("未获取到 prompt_id")
            
            return prompt_id
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def poll_status(self, prompt_id: str) -> Dict[str, Any]:
        """
        轮询执行状态
        
        Args:
            prompt_id: 任务 ID
            
        Returns:
            执行历史记录
            
        Raises:
            Exception: 超时或执行失败时抛出异常
        """
        url = f"{self.server_url}/history/{prompt_id}"
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            
            if elapsed > self.timeout:
                raise Exception(f"执行超时（{self.timeout} 秒）")
            
            try:
                response = self.session.get(url, timeout=10)
                
                if response.status_code >= 400:
                    raise Exception(f"查询状态失败: HTTP {response.status_code}")
                
                data = response.json()
                
                # 检查是否完成
                if prompt_id in data:
                    history = data[prompt_id]
                    
                    # 检查是否有错误
                    if "error" in history:
                        raise Exception(f"工作流执行错误: {history['error']}")
                    
                    # 检查是否完成
                    outputs = history.get("outputs", {})
                    if outputs:
                        return history
                
                # 显示进度（单行更新）
                print(f"\r⏳ 执行中... {int(elapsed)} 秒", end='', flush=True)
                time.sleep(self.poll_interval)
                
            except requests.exceptions.RequestException as e:
                time.sleep(self.poll_interval)
    
    def download_outputs(
        self,
        history: Dict[str, Any],
        output_dir: str
    ) -> Dict[str, List[str]]:
        """
        下载所有输出文件（支持图像、视频、音频等多种类型）
        
        Args:
            history: 执行历史记录
            output_dir: 输出目录
            
        Returns:
            按类型分组的文件路径字典，例如：
            {
                "images": ["output/image1.png"],
                "videos": ["output/video1.mp4"],
                "audio": ["output/audio1.wav"],
                "files": ["output/data.json"]
            }
            
        Raises:
            Exception: 下载失败时抛出异常
        """
        outputs = history.get("outputs", {})
        if not outputs:
            print("⚠️ 没有输出文件")
            return {}
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 按类型分组存储下载的文件
        downloaded = {
            "images": [],
            "videos": [],
            "audio": [],
            "files": []  # 其他类型的文件
        }
        
        for node_id, node_output in outputs.items():
            # 1. 下载图像
            images = node_output.get("images", [])
            for image_info in images:
                file_path = self._download_file(
                    output_path,
                    image_info.get("filename"),
                    image_info.get("subfolder", ""),
                    image_info.get("type", "output")
                )
                if file_path:
                    downloaded["images"].append(file_path)
            
            # 2. 下载视频
            videos = node_output.get("videos", [])
            for video_info in videos:
                file_path = self._download_file(
                    output_path,
                    video_info.get("filename"),
                    video_info.get("subfolder", ""),
                    video_info.get("type", "output")
                )
                if file_path:
                    downloaded["videos"].append(file_path)
            
            # 3. 下载音频
            audio = node_output.get("audio", [])
            for audio_info in audio:
                file_path = self._download_file(
                    output_path,
                    audio_info.get("filename"),
                    audio_info.get("subfolder", ""),
                    audio_info.get("type", "output")
                )
                if file_path:
                    downloaded["audio"].append(file_path)
            
            # 4. 下载其他文件（GIF、3D模型等）
            files = node_output.get("files", [])
            for file_info in files:
                file_path = self._download_file(
                    output_path,
                    file_info.get("filename"),
                    file_info.get("subfolder", ""),
                    file_info.get("type", "output")
                )
                if file_path:
                    downloaded["files"].append(file_path)
        
        # 打印下载摘要
        self._print_download_summary(downloaded)
        
        return downloaded
    
    def _download_file(
        self,
        output_path: Path,
        filename: str,
        subfolder: str,
        file_type: str
    ) -> Optional[str]:
        """
        下载单个文件
        
        Args:
            output_path: 输出目录
            filename: 文件名
            subfolder: 子文件夹
            file_type: 文件类型
            
        Returns:
            下载的文件路径，失败返回 None
        """
        if not filename:
            return None
        
        # 构建下载 URL
        params = {
            "filename": filename,
            "type": file_type,
            "subfolder": subfolder
        }
        
        url = f"{self.server_url}/view"
        
        try:
            response = self.session.get(url, params=params, timeout=120)
            
            if response.status_code >= 400:
                return None
            
            # 保存文件
            output_file = output_path / filename
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            return str(output_file)
            
        except Exception as e:
            return None
    
    def _print_download_summary(self, downloaded: Dict[str, List[str]]):
        """
        打印下载摘要（简洁版）
        
        Args:
            downloaded: 按类型分组的文件字典
        """
        total = sum(len(files) for files in downloaded.values())
        
        if total == 0:
            return
        
        # 单行显示摘要
        parts = []
        if downloaded["images"]:
            parts.append(f"图像 {len(downloaded['images'])} 个")
        if downloaded["videos"]:
            parts.append(f"视频 {len(downloaded['videos'])} 个")
        if downloaded["audio"]:
            parts.append(f"音频 {len(downloaded['audio'])} 个")
        if downloaded["files"]:
            parts.append(f"其他 {len(downloaded['files'])} 个")
        
        print(f"\n✓ 已下载 {total} 个文件：{', '.join(parts)}")
    
    def execute(
        self,
        workflow: Dict[str, Any],
        output_dir: str
    ) -> Dict[str, Any]:
        """
        执行完整的工作流（提交→轮询→下载）
        
        Args:
            workflow: 工作流 JSON 对象
            output_dir: 输出目录
            
        Returns:
            执行结果，包含 prompt_id、history 和按类型分组的文件列表
        """
        # 0. 确定超时时间
        self.timeout = self.get_timeout_for_workflow(workflow)
        
        # 1. 提交工作流
        prompt_id = self.submit_workflow(workflow)
        
        # 2. 轮询状态
        history = self.poll_status(prompt_id)
        
        # 3. 下载输出
        downloaded_files = self.download_outputs(history, output_dir)
        
        return {
            "prompt_id": prompt_id,
            "history": history,
            "outputs": downloaded_files
        }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="ComfyUI 工作流执行器（支持自动检测视频工作流）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 自动检测工作流类型并选择合适的超时时间
  python comfyui_executor.py --workflow ./workflow.json
  
  # 指定超时时间（10 分钟 = 600 秒，15 分钟 = 900 秒）
  python comfyui_executor.py --workflow ./workflow.json --timeout 900
  
  # 使用 workflows 目录中的工作流
  python comfyui_executor.py --workflow my_video_workflow.json
  
  # 显式指定输出目录
  python comfyui_executor.py --workflow ./workflow.json --output-dir ./output

超时说明：
  - 图像工作流：默认 300 秒（5 分钟）
  - 视频工作流：默认 900 秒（15 分钟）
  - 支持自动检测视频工作流并使用合适的超时时间
        """
    )
    
    parser.add_argument(
        "--workflow",
        required=True,
        help="工作流 JSON 文件路径"
    )
    
    parser.add_argument(
        "--output-dir",
        help="输出目录（默认：使用配置文件中的值）"
    )
    
    parser.add_argument(
        "--server-url",
        help="ComfyUI 服务地址（默认：使用配置文件中的值）"
    )
    
    parser.add_argument(
        "--api-key",
        help="API 密钥（可选）"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        help="超时时间（秒）。不指定则自动检测：图像 5 分钟，视频 15 分钟"
    )
    
    parser.add_argument(
        "--poll-interval",
        type=int,
        help="轮询间隔（秒，默认：2）"
    )
    
    parser.add_argument(
        "--no-auto-detect",
        action="store_true",
        help="禁用自动超时检测，始终使用默认超时时间"
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = get_config()
    
    # 确定输出目录
    output_dir = args.output_dir
    if not output_dir:
        output_dir = str(config.get_output_dir())
    
    # 读取工作流文件
    workflow_path = Path(args.workflow)
    
    # 如果是相对路径且不是以 workflows 开头，尝试从 workflows 目录查找
    if not workflow_path.is_absolute() and not str(workflow_path).startswith('workflows'):
        workflows_dir = config.get_workflows_dir()
        workflow_in_dir = workflows_dir / workflow_path
        if workflow_in_dir.exists():
            workflow_path = workflow_in_dir
    
    if not workflow_path.exists():
        print(f"错误：工作流文件不存在: {workflow_path}")
        sys.exit(1)
    
    try:
        with open(workflow_path, "r", encoding="utf-8") as f:
            workflow = json.load(f)
    except Exception as e:
        print(f"错误：无法读取工作流文件: {str(e)}")
        sys.exit(1)
    
    # 创建执行器
    executor = ComfyUIExecutor(
        server_url=args.server_url,
        api_key=args.api_key,
        timeout=args.timeout,
        poll_interval=args.poll_interval,
        auto_detect_timeout=not args.no_auto_detect
    )
    
    # 执行工作流
    try:
        result = executor.execute(workflow, output_dir)
        
        print(f"✓ 任务完成: {result['prompt_id']}")
        
        # 显示输出文件路径（简洁列表）
        outputs = result['outputs']
        if outputs:
            all_files = []
            for file_type, files in outputs.items():
                all_files.extend(files)
            
            if all_files:
                print(f"\n输出文件：")
                for file_path in all_files:
                    print(f"  {file_path}")
        
    except Exception as e:
        print(f"\n✗ 执行失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
