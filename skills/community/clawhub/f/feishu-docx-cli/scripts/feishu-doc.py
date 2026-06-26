#!/usr/bin/env python3
"""
Feishu Doc CLI - 飞书文档管理工具

支持：创建文档、读写内容、上传图片、权限管理
"""

import argparse
import json
import os
import sys
import requests

FEISHU_API = "https://open.feishu.cn/open-apis"

def get_token():
    """获取 tenant_access_token"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(config_path) as f:
        config = json.load(f)
    
    app_id = config['channels']['feishu']['appId']
    app_secret = config['channels']['feishu']['appSecret']
    
    resp = requests.post(f"{FEISHU_API}/auth/v3/tenant_access_token/internal",
        json={'app_id': app_id, 'app_secret': app_secret})
    return resp.json()['tenant_access_token']

def api(method, path, token, **kwargs):
    """调用 Feishu API"""
    url = f"{FEISHU_API}{path}"
    headers = kwargs.pop('headers', {})
    headers['Authorization'] = f'Bearer {token}'
    resp = requests.request(method, url, headers=headers, **kwargs)
    try:
        return resp.json()
    except:
        return {'code': -1, 'msg': f'HTTP {resp.status_code}'}

def cmd_create(args, token):
    """创建文档"""
    data = {'title': args.title}
    if args.folder:
        data['folder_token'] = args.folder
    
    result = api('POST', '/docx/v1/documents', token, json=data)
    
    if result['code'] == 0:
        doc = result['data']['document']
        print(f"✅ 文档创建成功")
        print(f"   标题: {doc['title']}")
        print(f"   Token: {doc['document_id']}")
        print(f"   链接: https://feishu.cn/docx/{doc['document_id']}")
    else:
        print(f"❌ 创建失败: {result.get('msg')}")

def cmd_read(args, token):
    """读取文档"""
    # 获取内容
    result = api('GET', f'/docx/v1/documents/{args.doc_token}/raw_content', token)
    
    if result['code'] == 0:
        print(result['data'].get('content', ''))
    else:
        print(f"❌ 读取失败: {result.get('msg')}")

def cmd_write(args, token):
    """写入文档（覆盖）"""
    # 读取文件
    with open(args.file) as f:
        content = f.read()
    
    # 转换为 blocks
    result = api('POST', '/docx/v1/documents/convert', token, json={
        'content_type': 'markdown',
        'content': content
    })
    
    if result['code'] != 0:
        print(f"❌ 转换失败: {result.get('msg')}")
        return
    
    blocks = result['data'].get('blocks', [])
    
    # 清空现有内容
    blocks_result = api('GET', f'/docx/v1/documents/{args.doc_token}/blocks/{args.doc_token}/children', token)
    if blocks_result['code'] == 0:
        items = blocks_result['data'].get('items', [])
        child_count = len([b for b in items if b.get('block_type') != 1])
        if child_count > 0:
            api('DELETE', f'/docx/v1/documents/{args.doc_token}/blocks/{args.doc_token}/children/batch_delete', token,
                json={'start_index': 0, 'end_index': child_count})
    
    # 写入新内容
    result = api('POST', f'/docx/v1/documents/{args.doc_token}/blocks/{args.doc_token}/children', token, json={'children': blocks})
    
    if result['code'] == 0:
        print(f"✅ 写入成功: {len(blocks)} 个 blocks")
    else:
        print(f"❌ 写入失败: {result.get('msg')}")

def cmd_upload_image(args, token):
    """上传图片"""
    if not os.path.exists(args.image):
        print(f"❌ 文件不存在: {args.image}")
        return
    
    # 如果没有指定 block_id，找第一个空的图片 block
    block_id = args.block_id
    if not block_id:
        result = api('GET', f'/docx/v1/documents/{args.doc_token}/blocks/{args.doc_token}/children', token)
        if result['code'] == 0:
            for item in result['data'].get('items', []):
                if item.get('block_type') == 27 and not item.get('image', {}).get('token'):
                    block_id = item['block_id']
                    break
        
        if not block_id:
            print("❌ 没有找到空的图片 block")
            print("   请先创建图片 block: feishu-doc append <doc_token> '![描述](path)'")
            return
    
    # 上传图片
    file_name = os.path.basename(args.image)
    file_size = os.path.getsize(args.image)
    
    url = f"{FEISHU_API}/drive/v1/medias/upload_all"
    headers = {'Authorization': f'Bearer {token}'}
    
    with open(args.image, 'rb') as f:
        files = {'file': (file_name, f, 'application/octet-stream')}
        data = {
            'file_name': file_name,
            'parent_type': 'docx_image',
            'parent_node': block_id,
            'size': str(file_size),
        }
        resp = requests.post(url, headers=headers, files=files, data=data)
        result = resp.json()
    
    if result['code'] != 0:
        print(f"❌ 上传失败: {result.get('msg')}")
        return
    
    file_token = result['data']['file_token']
    
    # 更新 block
    result = api('PATCH', f'/docx/v1/documents/{args.doc_token}/blocks/{block_id}', token,
        json={'replace_image': {'token': file_token}})
    
    if result['code'] == 0:
        print(f"✅ 图片上传成功")
        print(f"   Block: {block_id[:30]}...")
    else:
        print(f"❌ 更新失败: {result.get('msg')}")

def cmd_permissions(args, token):
    """管理权限"""
    if args.action == 'list':
        result = api('GET', f'/docx/v1/documents/{args.doc_token}/permission/member/list', token)
        if result['code'] == 0:
            members = result['data'].get('items', [])
            print(f"共有 {len(members)} 个协作者:")
            for m in members:
                print(f"  - {m.get('member_id', 'unknown')}: {m.get('perm', 'unknown')}")
        else:
            print(f"❌ 查询失败: {result.get('msg')}")
    
    elif args.action == 'add':
        result = api('POST', f'/docx/v1/documents/{args.doc_token}/permission/member/create', token, json={
            'member_type': 'openid',
            'member_id': args.member_id,
            'perm': args.perm
        })
        if result['code'] == 0:
            print(f"✅ 已添加权限: {args.member_id} -> {args.perm}")
        else:
            print(f"❌ 添加失败: {result.get('msg')}")
    
    elif args.action == 'remove':
        result = api('DELETE', f'/docx/v1/documents/{args.doc_token}/permission/member/delete', token,
            params={'member_type': 'openid', 'member_id': args.member_id})
        if result['code'] == 0:
            print(f"✅ 已移除权限: {args.member_id}")
        else:
            print(f"❌ 移除失败: {result.get('msg')}")

def main():
    parser = argparse.ArgumentParser(description='Feishu Doc CLI - 飞书文档管理工具')
    subparsers = parser.add_subparsers(dest='command')
    
    # create
    create = subparsers.add_parser('create', help='创建文档')
    create.add_argument('title', help='文档标题')
    create.add_argument('--folder', help='父文件夹 token')
    
    # read
    read = subparsers.add_parser('read', help='读取文档内容')
    read.add_argument('doc_token', help='文档 token')
    
    # write
    write = subparsers.add_parser('write', help='写入文档（覆盖）')
    write.add_argument('doc_token', help='文档 token')
    write.add_argument('file', help='Markdown 文件路径')
    
    # append
    append = subparsers.add_parser('append', help='追加内容')
    append.add_argument('doc_token', help='文档 token')
    append.add_argument('content', help='Markdown 内容')
    
    # upload-image
    upload = subparsers.add_parser('upload-image', help='上传图片')
    upload.add_argument('doc_token', help='文档 token')
    upload.add_argument('image', help='图片路径')
    upload.add_argument('--block-id', help='指定图片 block ID')
    
    # permissions
    perm = subparsers.add_parser('permissions', help='权限管理')
    perm.add_argument('action', choices=['list', 'add', 'remove'], help='操作')
    perm.add_argument('doc_token', help='文档 token')
    perm.add_argument('member_id', nargs='?', help='成员 ID (add/remove 时需要)')
    perm.add_argument('--perm', choices=['view', 'edit', 'full_access'], default='view', help='权限类型')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        token = get_token()
    except Exception as e:
        print(f"❌ 认证失败: {e}")
        sys.exit(1)
    
    # 执行命令
    commands = {
        'create': cmd_create,
        'read': cmd_read,
        'write': cmd_write,
        'upload-image': cmd_upload_image,
        'permissions': cmd_permissions,
    }
    
    if args.command in commands:
        commands[args.command](args, token)
    elif args.command == 'append':
        # 简单实现 append
        result = api('POST', '/docx/v1/documents/convert', token, json={
            'content_type': 'markdown',
            'content': args.content
        })
        if result['code'] == 0:
            blocks = result['data'].get('blocks', [])
            result = api('POST', f'/docx/v1/documents/{args.doc_token}/blocks/{args.doc_token}/children', token, json={'children': blocks})
            if result['code'] == 0:
                print(f"✅ 追加成功: {len(blocks)} 个 blocks")
            else:
                print(f"❌ 追加失败: {result.get('msg')}")
        else:
            print(f"❌ 转换失败: {result.get('msg')}")
    else:
        print(f"未知命令: {args.command}")

if __name__ == '__main__':
    main()
