#!/usr/bin/env python3
"""
阿里云盘 Python SDK 封装
使用 aliyunpan 3.0.9+ (pip install aliyunpan)
"""
import sys
import json
import os
import argparse

sys.path.insert(0, '/tmp/venv/lib/python3.8/site-packages')

from aliyunpan.api.core import AliyunPan
from aliyunpan.api.utils import get_sha1, get_proof_code, get_file_byte


def get_pan(token: str) -> AliyunPan:
    """
    创建并登录 AliyunPan 实例

    SDK 本身的 token_refresh() 对新 API 响应解析有 bug，
    这里直接调 auth API 拿到 access_token/drive_id，再绑定到实例。
    """
    import requests

    pan = AliyunPan(refresh_token=token)

    # 直接调 auth API 绕过 SDK bug
    resp = requests.post(
        'https://auth.aliyundrive.com/v2/account/token',
        json={"refresh_token": token, "grant_type": "refresh_token"},
        timeout=10
    ).json()

    # 手动注入到 SDK 实例，绕过后续所有 API 调用
    pan._access_token = resp['access_token']
    pan._refresh_token = resp.get('refresh_token', token)
    pan._drive_id = resp.get('default_drive_id', '')

    # 让 SDK 的 GLOBAL_VAR 也同步，避免某些内部逻辑读不到
    import aliyunpan.api.core as core_module
    core_module.GLOBAL_VAR.access_token = resp['access_token']
    core_module.GLOBAL_VAR.drive_id = resp.get('default_drive_id', '')
    core_module.GLOBAL_VAR.refresh_token = resp.get('refresh_token', token)

    return pan


def upload_file(pan: AliyunPan, file_path: str, target_folder: str = None, parent_id: str = 'root') -> dict:
    """上传文件"""
    path = os.path.abspath(file_path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在: {path}")

    # 查找或创建目标文件夹
    if target_folder:
        parent_id = ensure_folder(pan, target_folder, parent_id)

    # 上传
    result = pan.upload_file(parent_file_id=parent_id, path=path)
    
    # upload_file 可能返回: str(file_id), False, None, 或 Response 对象
    if isinstance(result, str):
        # 快速上传成功或缓存命中，返回 file_id
        return {'file_id': result, 'name': os.path.basename(path), 'rapid': True}
    elif result is None or result is False:
        # 需要重新获取文件信息
        files = pan.get_file_list(parent_id)
        fname = os.path.basename(path)
        for f in files:
            if f.get('name') == fname:
                return {'file_id': f.get('file_id'), 'name': fname, 'rapid': False}
        raise RuntimeError('Upload completed but file not found')
    else:
        # Response 对象
        data = result.json() if hasattr(result, 'json') else result
        if isinstance(data, dict):
            return data
        raise RuntimeError(f'Unexpected upload result type: {type(data)}')


def ensure_folder(pan: AliyunPan, name: str, parent_id: str = 'root') -> str:
    """确保文件夹存在，返回 folder_id"""
    # 先搜索
    files = pan.get_file_list(parent_id)
    for f in files:
        if f.get('name') == name and f.get('type') == 'folder':
            return f['file_id']
    # 不存在则创建
    result = pan.create_file(file_name=name, parent_file_id=parent_id, file_type=False)
    return result.json()['file_id']


def list_files(pan: AliyunPan, parent_id: str = 'root') -> list:
    """列出文件"""
    files = pan.get_file_list(parent_id)
    return [{'name': f.get('name'), 'file_id': f.get('file_id'), 
             'type': f.get('type'), 'size': f.get('size')} for f in files]


def search_file(pan: AliyunPan, name: str, parent_id: str = 'root') -> list:
    """搜索文件（只搜索指定目录，不递归）"""
    results = []
    try:
        files = pan.get_file_list(parent_id)
        for f in files:
            if name in f.get('name', ''):
                results.append({'name': f.get('name'), 'file_id': f.get('file_id'),
                               'type': f.get('type'), 'size': f.get('size')})
    except Exception as e:
        pass
    return results


def create_share(pan: AliyunPan, file_id: str) -> str:
    """创建分享链接"""
    share_info = pan.share_link([file_id])
    return share_info


def delete_file(pan: AliyunPan, file_id: str) -> bool:
    """删除文件"""
    pan.delete_file(file_id)
    return True


def get_download_url(pan: AliyunPan, file_id: str) -> str:
    """获取下载链接"""
    return pan.get_download_url(file_id)


def get_user_info(pan: AliyunPan) -> dict:
    """获取用户信息"""
    return {
        'drive_id': pan.drive_id,
        'username': pan._username
    }


def main():
    parser = argparse.ArgumentParser(description='阿里云盘操作工具')
    parser.add_argument('action', choices=['upload', 'list', 'create_folder', 'search', 
                                          'share', 'delete', 'download_url', 'user_info'])
    parser.add_argument('--token', required=True)
    parser.add_argument('--file-path', help='上传文件路径')
    parser.add_argument('--target-folder', help='目标文件夹名称')
    parser.add_argument('--parent-id', default='root')
    parser.add_argument('--name', help='文件夹名称或搜索关键词')
    parser.add_argument('--file-id', help='文件ID')
    parser.add_argument('--save-token', help='保存新token到文件')

    args = parser.parse_args()

    try:
        pan = get_pan(args.token)
        
        # 保存新refresh_token
        new_token = pan._refresh_token
        if args.save_token and new_token:
            with open(args.save_token, 'r') as f:
                env = f.read()
            import re
            env = re.sub(r'ALIYUN_DRIVE_REFRESH_TOKEN="[^"]*"', 
                        f'ALIYUN_DRIVE_REFRESH_TOKEN="{new_token}"', env)
            with open(args.save_token, 'w') as f:
                f.write(env)

        if args.action == 'upload':
            if not args.file_path:
                print(json.dumps({'error': 'file_path required'}))
                sys.exit(1)
            result = upload_file(pan, args.file_path, args.target_folder, args.parent_id)
            print(json.dumps({'success': True, 'file_id': result.get('file_id'), 
                             'name': result.get('name'), 'size': result.get('size')}))

        elif args.action == 'list':
            files = list_files(pan, args.parent_id)
            print(json.dumps({'success': True, 'files': files}))

        elif args.action == 'create_folder':
            if not args.name:
                print(json.dumps({'error': 'name required'}))
                sys.exit(1)
            fid = ensure_folder(pan, args.name, args.parent_id)
            print(json.dumps({'success': True, 'file_id': fid}))

        elif args.action == 'search':
            if not args.name:
                print(json.dumps({'error': 'name required'}))
                sys.exit(1)
            results = search_file(pan, args.name)
            print(json.dumps({'success': True, 'results': results}))

        elif args.action == 'share':
            if not args.file_id:
                print(json.dumps({'error': 'file_id required'}))
                sys.exit(1)
            url = create_share(pan, args.file_id)
            print(json.dumps({'success': True, 'share_url': url}))

        elif args.action == 'delete':
            if not args.file_id:
                print(json.dumps({'error': 'file_id required'}))
                sys.exit(1)
            delete_file(pan, args.file_id)
            print(json.dumps({'success': True}))

        elif args.action == 'download_url':
            if not args.file_id:
                print(json.dumps({'error': 'file_id required'}))
                sys.exit(1)
            url = get_download_url(pan, args.file_id)
            print(json.dumps({'success': True, 'url': url}))

        elif args.action == 'user_info':
            info = get_user_info(pan)
            print(json.dumps({'success': True, **info}))

    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()
