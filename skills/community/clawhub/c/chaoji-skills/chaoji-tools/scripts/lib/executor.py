#!/usr/bin/env python3
"""
Command executor for ChaoJi CLI.

Handles actual command execution, task polling, and result processing.
"""

import os
import sys
import time
import json
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Add ChaoJiAI/scripts directory to path for chaoji_client, chaoji_oss, chaoji_utils
chaoji_scripts_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts')
sys.path.insert(0, os.path.normpath(chaoji_scripts_dir))

from chaoji_client import ChaojiApiClient
from chaoji_oss import ChaojiOssUploader, extract_oss_path
from chaoji_utils import poll_task_result, download_outputs, prepare_image_input

from commands import COMMAND_SPECS, VIDEO_COMMANDS
from errors import (
    ERROR_CODE_MAP,
    build_error_response,
    infer_error_code_from_text,
    get_action_url_from_env,
    get_order_url_from_env,
)


# API configuration
APP_KEY = "marketing-server"
ENDPOINT = "open.metac-inc.com"


def get_credentials():
    """
    Get credentials from environment or credentials file.
    
    Returns:
        Tuple of (access_key, secret_key) or (None, None) if not found
    """
    # Try environment variables first
    ak = os.environ.get('CHAOJI_AK')
    sk = os.environ.get('CHAOJI_SK')
    
    if ak and sk:
        return ak, sk
    
    # Try credentials file
    credentials_path = os.path.expanduser('~/.chaoji/credentials.json')
    if os.path.exists(credentials_path):
        try:
            with open(credentials_path, 'r', encoding='utf-8') as f:
                credentials = json.load(f)
                ak = credentials.get('access_key')
                sk = credentials.get('secret_key')
                if ak and sk:
                    return ak, sk
        except Exception:
            pass
    
    return None, None


def upload_local_file(file_path: str, ak: str, sk: str) -> str:
    """
    Upload local file to OSS and return OSS path.
    
    Args:
        file_path: Local file path
        ak: Access key
        sk: Secret key
        
    Returns:
        OSS path
        
    Raises:
        RuntimeError: If upload fails
    """
    uploader = ChaojiOssUploader(ak, sk)
    result = uploader.upload_image(file_path)
    
    if not result["success"]:
        raise RuntimeError(f"上传失败：{result.get('error')}")
    
    return extract_oss_path(result["url"])


def execute_model_tryon_quick(client: ChaojiApiClient, params: Dict[str, Any], 
                               ak: str, sk: str) -> Dict[str, Any]:
    """
    Execute model_tryon_quick command.
    
    Args:
        client: API client
        params: Command parameters
        ak: Access key
        sk: Secret key
        
    Returns:
        API response
    """
    # Prepare image inputs
    def do_upload(path: str) -> str:
        return upload_local_file(path, ak, sk)
    
    cloth_path = prepare_image_input(params['image_cloth'], upload_func=do_upload)
    human_paths = []
    for human_input in params['list_images_human']:
        human_path = prepare_image_input(human_input, upload_func=do_upload)
        human_paths.append(human_path)
    
    # Build API parameters
    api_params = {
        "image_cloth": cloth_path,
        "list_images_human": human_paths,
        "cloth_length": params.get('cloth_length', 'overall'),
        "dpi": params.get('dpi', 300),
        "output_format": params.get('output_format', 'jpg'),
        "batch_size": str(params.get('batch_size', 1)),
    }
    
    # Call API
    result = client.post("marketing_algorithm_model_tryon_quick", api_params)
    return result


def execute_human_tryon(client: ChaojiApiClient, params: Dict[str, Any],
                        ak: str, sk: str) -> Dict[str, Any]:
    """
    Execute human_tryon command (真人试衣/模特换装).

    API: /marketing/algorithm/human_tryon
    apiName: marketing_algorithm_human_tryon

    All image params are resolved to OSS paths.

    Args:
        client: API client
        params: Command parameters
        ak: Access key
        sk: Secret key

    Returns:
        API response
    """
    def do_upload(path: str) -> str:
        return upload_local_file(path, ak, sk)

    cloth_path = prepare_image_input(params['image_cloth'], upload_func=do_upload)
    human_paths = [prepare_image_input(h, upload_func=do_upload) for h in params['list_images_human']]

    # Build API parameters (all image values are OSS paths)
    api_params = {
        "image_cloth": cloth_path,
        "list_images_human": human_paths,
        "cloth_length": params['cloth_length'],
    }

    # Optional parameters
    if 'dpi' in params:
        api_params["dpi"] = params['dpi']
    if 'output_format' in params:
        api_params["output_format"] = params['output_format']

    # Call API
    result = client.post("marketing_algorithm_human_tryon", api_params)
    return result


def execute_tryon_shoes(client: ChaojiApiClient, params: Dict[str, Any],
                        ak: str, sk: str) -> Dict[str, Any]:
    """
    Execute tryon_shoes command (鞋靴试穿).

    API: /marketing/algorithm/tryon_shoes
    apiName: marketing_algorithm_tryon_shoes

    Shoe image mapping (transparent to caller):
      - 1 image  -> API field: image_shoe
      - 2 images -> API field: product_image { both_feet_image, inner_side_image }
      - 3 images -> API field: product_image { both_feet_image, inner_side_image, outer_side_image }

    All image params are resolved to OSS paths.
    tryon_type is fixed to 5 (专业模式).

    Args:
        client: API client
        params: Command parameters (list_images_shoe, list_images_human)
        ak: Access key
        sk: Secret key

    Returns:
        API response
    """
    def do_upload(path: str) -> str:
        return upload_local_file(path, ak, sk)

    # Resolve model images -> OSS paths
    human_paths = [prepare_image_input(h, upload_func=do_upload) for h in params['list_images_human']]

    # Resolve shoe images -> OSS paths
    shoe_inputs = params['list_images_shoe']
    if isinstance(shoe_inputs, str):
        shoe_inputs = [shoe_inputs]
    shoe_paths = [prepare_image_input(s, upload_func=do_upload) for s in shoe_inputs]

    # Build API parameters
    api_params = {
        "list_images_human": human_paths,
        "tryon_type": 5,
    }

    # Map shoe images to API fields
    _PRODUCT_IMAGE_KEYS = ['both_feet_image', 'inner_side_image', 'outer_side_image']

    if len(shoe_paths) == 1:
        api_params["image_shoe"] = shoe_paths[0]
    elif len(shoe_paths) <= 3:
        product_image = {}
        for i, path in enumerate(shoe_paths):
            product_image[_PRODUCT_IMAGE_KEYS[i]] = path
        api_params["product_image"] = product_image
    else:
        raise RuntimeError(f"鞋商品图最多支持 3 张，当前传入 {len(shoe_paths)} 张")

    # Call API
    result = client.post("marketing_algorithm_tryon_shoes", api_params)
    return result


def execute_image2image(client: ChaojiApiClient, params: Dict[str, Any],
                        ak: str, sk: str) -> Dict[str, Any]:
    """
    Execute image2image command (素材生成-图生图).

    API: /marketing/algorithm/material_generation_image_to_image
    apiName: marketing_algorithm_image2image

    model_type fixed to chao_paint_3.0pro (supports up to 14 reference images).
    All image params are resolved to OSS paths.

    Args:
        client: API client
        params: Command parameters (img, prompt, ratio?, resolution?)
        ak: Access key
        sk: Secret key

    Returns:
        API response
    """
    def do_upload(path: str) -> str:
        return upload_local_file(path, ak, sk)

    # Resolve reference images -> OSS paths
    img_inputs = params['img']
    if isinstance(img_inputs, str):
        img_inputs = [img_inputs]
    if len(img_inputs) > 14:
        raise RuntimeError(f"参考图最多支持 14 张，当前传入 {len(img_inputs)} 张")
    img_paths = [prepare_image_input(i, upload_func=do_upload) for i in img_inputs]

    # Build API parameters
    api_params = {
        "img": img_paths,
        "prompt": params['prompt'],
        "model_type": "chao_paint_3.0pro",
        "ratio": params.get('ratio', 'auto'),
        "resolution": params.get('resolution', '1k'),
    }

    # Call API
    result = client.post("marketing_algorithm_image2image", api_params)
    return result


def execute_cutout(client: ChaojiApiClient, params: Dict[str, Any],
                   ak: str, sk: str) -> Dict[str, Any]:
    """
    Execute cutout command (智能抠图).

    API: /marketing/algorithm/universal_cutout
    apiName: marketing_algorithm_integrated_auto_segmentation

    Sync API — returns data directly (not task_id).

    Args:
        client: API client
        params: Command parameters (image, method?, cate_token?)
        ak: Access key
        sk: Secret key

    Returns:
        API response with data.view_image and data.image_mask
    """
    def do_upload(path: str) -> str:
        return upload_local_file(path, ak, sk)

    image_path = prepare_image_input(params['image'], upload_func=do_upload)

    method = params.get('method', 'auto')
    valid_methods = ('seg', 'clothseg', 'patternseg', 'generalseg', 'auto')
    if method not in valid_methods:
        raise RuntimeError(f"不支持的 method: {method}，可选值：{', '.join(valid_methods)}")

    api_params = {
        "image": image_path,
        "method": method,
        "return_view_image": True,
    }

    # cate_token only applies when method is clothseg
    if method == 'clothseg':
        cate_token = params.get('cate_token', 'overall')
        if cate_token not in ('upper', 'lower', 'overall'):
            raise RuntimeError(f"不支持的 cate_token: {cate_token}，可选值：upper, lower, overall")
        api_params["cate_token"] = cate_token

    result = client.post("marketing_algorithm_integrated_auto_segmentation", api_params)
    return result


def execute_remaining_quantity_of_beans(client: ChaojiApiClient, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute remaining_quantity_of_beans command (米豆余额查询).

    API: GET /marketing/algorithm/remaining_quantity_of_beans
    apiName: marketing_algorithm_remaining_quantity_of_beans

    Sync API — returns data.remaining_quantity directly.
    No parameters required.
    """
    result = client.get(
        "/marketing/algorithm/remaining_quantity_of_beans",
        api_name="marketing_algorithm_remaining_quantity_of_beans"
    )
    return result


# Command execution mapping
COMMAND_EXECUTORS = {
    'model_tryon_quick': execute_model_tryon_quick,
    'human_tryon': execute_human_tryon,
    'tryon_shoes': execute_tryon_shoes,
    'image2image': execute_image2image,
    'cutout': execute_cutout,
    'remaining_quantity_of_beans': execute_remaining_quantity_of_beans,
    # Add more command executors as needed
}

# Commands that require ak/sk passed to executor (for local file uploads)
COMMANDS_NEED_CREDENTIALS = {'model_tryon_quick', 'human_tryon', 'tryon_shoes', 'image2image', 'cutout'}


def run_command(command: str, input_data: Dict[str, Any], poll: bool = True) -> Dict[str, Any]:
    """
    Run a ChaoJi CLI command.
    
    Args:
        command: Command name (canonical form)
        input_data: Input parameters
        poll: Whether to poll for task completion
        
    Returns:
        Standardized result dictionary
    """
    # Get credentials
    ak, sk = get_credentials()
    if not ak or not sk:
        return build_error_response(
            error_type='CREDENTIALS_MISSING',
            error_code='AUTH_001',
            action_link=f'[获取凭证]({get_action_url_from_env()})'
        )
    
    # Create API client
    client = ChaojiApiClient(APP_KEY, ak, sk, ENDPOINT)
    
    # Get executor for command
    executor = COMMAND_EXECUTORS.get(command)
    if not executor:
        # Fallback: try to call API directly using command name
        try:
            result = client.post(command, input_data)
        except Exception as e:
            return build_error_response(
                error_type='RUNTIME_ERROR',
                error_code='RUNTIME_001',
                user_hint=f'命令 {command} 未实现或调用失败：{str(e)}',
                next_action='请检查命令名称是否正确或联系开发者添加该命令支持'
            )
    else:
        # Execute with credentials if needed (for commands that upload local files)
        try:
            if command in COMMANDS_NEED_CREDENTIALS:
                result = executor(client, input_data, ak, sk)
            else:
                result = executor(client, input_data)
        except Exception as e:
            error_code = infer_error_code_from_text(str(e))
            return build_error_response(
                error_type=ERROR_CODE_MAP.get(error_code, 'RUNTIME_ERROR'),
                error_code=error_code or 'RUNTIME_001',
                user_hint=str(e),
                next_action='请检查输入参数和网络连接后重试'
            )
    
    # Check response
    if result.get('code') != 2000:
        error_code = infer_error_code_from_text(result.get('message', ''))
        return build_error_response(
            error_type=ERROR_CODE_MAP.get(error_code, 'API_ERROR'),
            error_code=error_code or 'API_001',
            error_name=result.get('message', 'API 调用失败'),
            user_hint=result.get('message', 'API 调用失败'),
            next_action='请检查输入参数后重试'
        )

    data = result.get('data')

    # Sync API: data is dict/list/None -> return directly
    if not isinstance(data, int):
        # Extract media URLs from sync response if present
        media_urls = []
        if isinstance(data, dict):
            for key in ('view_image', 'image_mask', 'image_url', 'url'):
                if data.get(key):
                    media_urls.append(data[key])
        resp = {
            'ok': True,
            'command': command,
            'result': result,
        }
        if media_urls:
            resp['media_urls'] = media_urls
        return resp

    # Async API: data is int (task_id)
    task_id = data

    # Poll for result if requested
    if not poll:
        return {
            'ok': True,
            'command': command,
            'task_id': task_id
        }
    
    # Determine timeout based on command type
    timeout_ms = 600000 if command in VIDEO_COMMANDS else 900000
    interval = int(os.environ.get('CHAOJI_TASK_WAIT_INTERVAL_MS', 2000)) / 1000.0
    
    # Poll for result
    poll_result = poll_task_result(
        client, 
        task_id, 
        max_retries=int(timeout_ms / (interval * 1000)),
        interval=interval
    )
    
    # Process poll result
    if poll_result['status'] == 'success':
        outputs = poll_result.get('outputs', [])
        
        # Extract media URLs
        media_urls = []
        for output in outputs:
            url = output.get('workOutputUrl')
            if url:
                media_urls.append(url)
        
        # Auto-download if enabled
        output_dir = os.path.expanduser('~/.openclaw/media/outbound')
        downloaded_outputs = download_outputs(outputs, output_dir, auto_download=True)
        
        # Update outputs with local paths
        for i, output in enumerate(downloaded_outputs):
            if 'localPath' in output:
                outputs[i] = output
        
        return {
            'ok': True,
            'command': command,
            'task_id': task_id,
            'media_urls': media_urls,
            'result': poll_result,
            'outputs': outputs
        }
    
    elif poll_result['status'] in ['failed', 'partial_failed']:
        error_msg = poll_result.get('error_msg') or '任务执行失败'
        error_code = infer_error_code_from_text(error_msg)
        return build_error_response(
            error_type=ERROR_CODE_MAP.get(error_code, 'API_ERROR'),
            error_code=error_code or 'API_002',
            error_name=error_msg,
            user_hint=error_msg,
            next_action='请检查输入参数后重试'
        )
    
    else:  # timeout
        return build_error_response(
            error_type='TIMEOUT',
            error_code='API_TIMEOUT',
            user_hint='任务执行超时',
            next_action='请稍后重试或减少并发任务数'
        )
