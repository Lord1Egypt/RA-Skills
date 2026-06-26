#!/usr/bin/env python3
"""
AiriLab API 调用

整合原 api-list 技能的核心功能：
1. 提交任务（MJ 渲染、创意放大、氛围转换）
2. 自动处理认证和项目配置
3. 统一的错误处理
"""

import requests
import json
from typing import Dict, Any, List

try:
    from .config import AiriLabConfig
    from .auth import AiriLabAuth
    from .upload import AiriLabUpload
except ImportError:  # pragma: no cover
    from config import AiriLabConfig
    from auth import AiriLabAuth
    from upload import AiriLabUpload

# API 端点
GENERATE_URL = "https://cn.airilab.com/api/Universal/Generate"
WORKFLOW_MJ = 0
WORKFLOW_UPSCALE = 16
WORKFLOW_ATMOSPHERE = 13

# 请求头模板
DEFAULT_HEADERS = {
    "accept": "text/plain",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "origin": "https://cn.airilab.com",
    "user-agent": "Mozilla/5.0"
}


class AiriLabAPI:
    """AiriLab API 调用器"""
    
    def __init__(self, config: AiriLabConfig = None):
        """
        初始化 API 调用器
        
        参数:
            config: 配置管理器实例
        """
        self.config = config or AiriLabConfig()
        self.auth = AiriLabAuth(self.config)
        self.upload = AiriLabUpload(self.config)
    
    def _ensure_ready(self) -> Dict[str, Any]:
        """
        确保已准备好（认证 + 项目配置）
        
        返回:
            dict: {
                'ready': bool,
                'needs_auth': bool,
                'needs_project': bool,
                'token': str | None,
                'project': dict | None,
                'message': str
            }
        """
        # 检查认证
        auth_result = self.auth.ensure_authenticated()
        
        if not auth_result['authenticated']:
            return {
                'ready': False,
                'needs_auth': True,
                'needs_project': False,
                'token': None,
                'project': None,
                'message': auth_result['message']
            }
        
        # 检查项目配置
        project = self.config.get_project()
        
        if not project:
            return {
                'ready': False,
                'needs_auth': False,
                'needs_project': True,
                'token': auth_result['token'],
                'project': None,
                'message': '需要选择项目'
            }
        
        return {
            'ready': True,
            'needs_auth': False,
            'needs_project': False,
            'token': auth_result['token'],
            'project': project,
            'message': '就绪'
        }
    
    def _build_payload(self, workflow_id: int, project: Dict[str, Any], 
                       base_image: str = None, prompt: str = "",
                       reference_images: List[str] = None, image_count: int = 4,
                       **kwargs) -> Dict[str, Any]:
        """
        构建请求 payload
        
        参数:
            workflow_id: 工作流 ID
            project: 项目配置
            base_image: 基图 URL（可选）
            prompt: 提示词（可选）
            reference_images: 参考图 URL 列表（可选）
            image_count: 生成图片数量
            **kwargs: 其他参数
        
        返回:
            dict: 请求 payload
        """
        # MJ 创意渲染工作流 (workflowId: 4)
        if workflow_id == WORKFLOW_MJ:
            payload = {
                "model": 0,
                "orientation": 0,
                "imageRatio": 0,
                "referenceImage": [
                    {"url": url, "type": 0} for url in (reference_images or [])[:3]
                ] if reference_images else [],
                "prompt": prompt,
                "workflowId": WORKFLOW_MJ,
                "additionalPrompt": prompt,
                "designLibraryName": "No Style",
                "designLibraryId": 99,
                "firstTierName": "No Style",
                "firstTierId": 9999,
                "secondTierName": "No Style",
                "secondTierId": 9999,
                "styleId": 9999,
                "cameraViewName": "No Camera",
                "cameraViewId": 9999,
                "graphicStyleId": 9999,
                "atmosphereId": 99,
                "atmosphereType": "",
                "additionalNegativePrompt": "",
                "imageType": "",
                "inputFidelityLevel": 0,
                "controlLevel": 0,
                "baseImage": "",
                "maskImage": "",
                "originalImage": "",
                "initialCNImage": "",
                "horizontalPercentage": 0,
                "verticalPercentage": 0,
                "firstFrame": "",
                "imageTail": "",
                "videoPrompt": 0,
                "timeLapse": 0,
                "cameraSpeed": 0,
                "privateModel": "",
                "height": 0,
                "width": 0,
                "megapixels": 2.25,
                "angleIndex": 0,
                "imageCount": image_count,
                "language": "chs",
                "teamId": project['teamId'],
                "projectId": project['projectId'],
                "projectName": project['projectName']
            }
        
        # 创意放大工作流 (workflowId: 16)
        elif workflow_id == WORKFLOW_UPSCALE:
            payload = {
                "initialCNImage": None,
                "baseImage": base_image or "",
                "workflowId": WORKFLOW_UPSCALE,
                "additionalPrompt": "",
                "referenceImage": [],
                "designLibraryName": "No Style",
                "designLibraryId": 99,
                "firstTierName": "No Style",
                "firstTierId": 9999,
                "secondTierName": "No Style",
                "secondTierId": 9999,
                "styleId": 9999,
                "cameraViewName": "No Camera",
                "cameraViewId": 9999,
                "graphicStyleId": 9999,
                "atmosphereId": 99,
                "atmosphereType": "",
                "additionalNegativePrompt": "",
                "imageType": "",
                "inputFidelityLevel": 0,
                "controlLevel": 0,
                "maskImage": "",
                "originalImage": "",
                "horizontalPercentage": 0,
                "verticalPercentage": 0,
                "firstFrame": "",
                "imageTail": "",
                "videoPrompt": 0,
                "timeLapse": 0,
                "cameraSpeed": 0,
                "prompt": "",
                "privateModel": "",
                "height": kwargs.get('height', 816),
                "width": kwargs.get('width', 1288),
                "angleIndex": 0,
                "imageCount": 1,
                "language": "chs",
                "teamId": project['teamId'],
                "projectId": project['projectId'],
                "projectName": project['projectName']
            }
        
        # 氛围转换工作流 (workflowId: 13)
        elif workflow_id == WORKFLOW_ATMOSPHERE:
            payload = {
                "workflowId": WORKFLOW_ATMOSPHERE,
                "baseImage": base_image or "",
                "prompt": prompt,
                "additionalPrompt": prompt,
                "referenceImage": [
                    {"url": reference_images[0], "type": 0}
                ] if reference_images and len(reference_images) > 0 else [],
                "imageCount": image_count,
                "language": "chs",
                "teamId": project['teamId'],
                "projectId": project['projectId'],
                "projectName": project['projectName']
            }
        
        else:
            # 默认简化的 payload
            payload = {
                "workflowId": workflow_id,
                "imageCount": image_count,
                "language": "chs",
                "teamId": project['teamId'],
                "projectId": project['projectId'],
                "projectName": project['projectName']
            }
        
        return payload

    def _build_headers(self, token: str, project_id: int) -> Dict[str, str]:
        headers = DEFAULT_HEADERS.copy()
        headers["Authorization"] = f"Bearer {token}"
        headers["referer"] = f"https://cn.airilab.com/stdio/workspace/{project_id}"
        return headers

    
    def submit_task(self, workflow_id: int, **kwargs) -> Dict[str, Any]:
        """
        提交生成任务
        
        参数:
            workflow_id: 工作流 ID (0=MJ, 16=创意放大，13=氛围转换)
            **kwargs: 工作流特定参数
        
        返回:
            dict: {
                'success': bool,
                'job_id': str | None,
                'message': str,
                'needs_auth': bool,
                'needs_project': bool
            }
        """
        # 确保已准备好
        ready = self._ensure_ready()
        
        if not ready['ready']:
            return {
                'success': False,
                'job_id': None,
                'message': ready['message'],
                'needs_auth': ready['needs_auth'],
                'needs_project': ready['needs_project']
            }
        
        # 构建 payload
        payload = self._build_payload(
            workflow_id,
            ready['project'],
            **kwargs
        )
        
        # 提交任务
        headers = self._build_headers(
            token=ready['token'],
            project_id=ready['project']['projectId']
        )
        
        try:
            response = requests.post(
                GENERATE_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            result = response.json()
            
            if result.get("status") == 200:
                data = result.get("data", {})
                job_id = data.get("jobId")
                
                return {
                    'success': True,
                    'job_id': job_id,
                    'message': f'Job submitted: {job_id}. This round is complete. You will be notified when background processing finishes.',
                    'needs_auth': False,
                    'needs_project': False
                }
            else:
                return {
                    'success': False,
                    'job_id': None,
                    'message': result.get('message', '提交失败'),
                    'needs_auth': False,
                    'needs_project': False
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'job_id': None,
                'message': f'网络错误：{str(e)}',
                'needs_auth': False,
                'needs_project': False
            }
    
    # ==================== 快捷方法 ====================
    
    def mj_render(self, prompt: str, reference_images: List[str] = None, 
                  image_count: int = 4) -> Dict[str, Any]:
        """
        提交 MJ 创意渲染任务
        
        参数:
            prompt: 提示词
            reference_images: 参考图 URL 列表（最多 3 张）
            image_count: 生成图片数量
        
        返回:
            dict: 提交结果
        """
        return self.submit_task(
            workflow_id=WORKFLOW_MJ,
            prompt=prompt,
            reference_images=reference_images,
            image_count=image_count
        )
    
    def upscale(self, base_image: str, width: int = 1288, 
                height: int = 816) -> Dict[str, Any]:
        """
        提交创意放大任务
        
        参数:
            base_image: 基图 URL
            width: 目标宽度
            height: 目标高度
        
        返回:
            dict: 提交结果
        """
        return self.submit_task(
            workflow_id=WORKFLOW_UPSCALE,
            base_image=base_image,
            width=width,
            height=height
        )
    
    def atmosphere_transform(self, base_image: str, prompt: str,
                             reference_image: str = None,
                             image_count: int = 4) -> Dict[str, Any]:
        """
        提交氛围转换任务
        
        参数:
            base_image: 基图 URL
            prompt: 氛围描述
            reference_image: 参考图 URL（最多 1 张）
            image_count: 生成图片数量
        
        返回:
            dict: 提交结果
        """
        reference_images = [reference_image] if reference_image else None
        
        return self.submit_task(
            workflow_id=WORKFLOW_ATMOSPHERE,
            base_image=base_image,
            prompt=prompt,
            reference_images=reference_images,
            image_count=image_count
        )


# ==================== 命令行入口 ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AiriLab API 调用")
    parser.add_argument("--tool", required=True, 
                       choices=["mj", "upscale", "atmosphere"],
                       help="工具类型")
    parser.add_argument("--prompt", help="提示词（用于 MJ 和 atmosphere）")
    parser.add_argument("--base-image", help="基图 URL（用于创意放大和 atmosphere）")
    parser.add_argument("--image-count", type=int, default=4, help="生成图片数量")
    
    args = parser.parse_args()
    
    config = AiriLabConfig()
    api = AiriLabAPI(config)
    
    if args.tool == "mj":
        if not args.prompt:
            print("❌ 错误：MJ 模式需要 --prompt 参数")
        else:
            result = api.mj_render(args.prompt, image_count=args.image_count)
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
    
    elif args.tool == "upscale":
        if not args.base_image:
            print("❌ 错误：创意放大需要 --base-image 参数")
        else:
            result = api.upscale(args.base_image)
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
    
    elif args.tool == "atmosphere":
        if not args.base_image or not args.prompt:
            print("❌ 错误：atmosphere 需要 --base-image 和 --prompt 参数")
        else:
            result = api.atmosphere_transform(
                args.base_image,
                args.prompt,
                image_count=args.image_count
            )
            if result['success']:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
