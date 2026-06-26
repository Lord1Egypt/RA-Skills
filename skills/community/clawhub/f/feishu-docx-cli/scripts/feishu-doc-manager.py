#!/usr/bin/env python3
"""
Feishu Doc Manager - Complete CLI for Feishu Document Management
"""

import argparse
import json
import os
import sys
import requests
from typing import Optional, List, Dict

FEISHU_API = "https://open.feishu.cn/open-apis"

class FeishuClient:
    """Feishu API Client"""
    
    def __init__(self):
        self.app_id, self.app_secret = self._get_credentials()
        self.token = self._get_token()
    
    def _get_credentials(self) -> tuple:
        """Get credentials from OpenClaw config"""
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        if not os.path.exists(config_path):
            raise Exception("OpenClaw config not found. Please run: openclaw configure --section feishu")
        
        with open(config_path) as f:
            config = json.load(f)
        
        feishu = config.get('channels', {}).get('feishu', {})
        app_id = feishu.get('appId')
        app_secret = feishu.get('appSecret')
        
        if not app_id:
            raise Exception("Feishu app_id not configured")
        
        return app_id, app_secret
    
    def _get_token(self) -> str:
        """Get tenant access token"""
        resp = requests.post(f"{FEISHU_API}/auth/v3/tenant_access_token/internal", json={
            'app_id': self.app_id,
            'app_secret': self.app_secret
        })
        result = resp.json()
        if result.get('code') != 0:
            raise Exception(f"Auth failed: {result.get('msg')}")
        return result['tenant_access_token']
    
    def request(self, method: str, path: str, **kwargs) -> dict:
        """Make authenticated request"""
        url = f"{FEISHU_API}{path}"
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {self.token}'
        
        resp = requests.request(method, url, headers=headers, **kwargs)
        
        try:
            return resp.json()
        except:
            return {'code': -1, 'msg': f'HTTP {resp.status_code}: {resp.text[:200]}'}


class DocManager:
    """Document Management Operations"""
    
    def __init__(self, client: FeishuClient):
        self.client = client
    
    # ==================== Document CRUD ====================
    
    def create(self, title: str, folder_token: Optional[str] = None) -> dict:
        """Create new document"""
        data = {'title': title}
        if folder_token:
            data['folder_token'] = folder_token
        
        result = self.client.request('POST', '/docx/v1/documents', json=data)
        
        if result.get('code') == 0:
            doc = result['data']['document']
            return {
                'success': True,
                'doc_token': doc['document_id'],
                'title': doc['title'],
                'url': f"https://feishu.cn/docx/{doc['document_id']}"
            }
        
        return {'success': False, 'error': result.get('msg')}
    
    def read(self, doc_token: str) -> dict:
        """Read document content"""
        # Get basic info
        info = self.client.request('GET', f'/docx/v1/documents/{doc_token}')
        if info.get('code') != 0:
            return {'success': False, 'error': info.get('msg')}
        
        # Get raw content
        content = self.client.request('GET', f'/docx/v1/documents/{doc_token}/raw_content')
        if content.get('code') != 0:
            return {'success': False, 'error': content.get('msg')}
        
        doc = info['data']['document']
        return {
            'success': True,
            'title': doc['title'],
            'doc_token': doc['document_id'],
            'revision_id': doc.get('revision_id'),
            'url': f"https://feishu.cn/docx/{doc_token}",
            'content': content['data'].get('content', ''),
        }
    
    def write(self, doc_token: str, markdown: str) -> dict:
        """Write markdown content (replaces all)"""
        # Convert markdown to blocks
        result = self.client.request('POST', '/docx/v1/documents/convert', json={
            'content_type': 'markdown',
            'content': markdown
        })
        
        if result.get('code') != 0:
            return {'success': False, 'error': f"Convert failed: {result.get('msg')}"}
        
        blocks = result['data'].get('blocks', [])
        
        # Clear existing content
        self._clear_document(doc_token)
        
        # Insert new blocks
        result = self.client.request('POST', f'/docx/v1/documents/{doc_token}/blocks/{doc_token}/children', json={
            'children': blocks
        })
        
        if result.get('code') == 0:
            return {'success': True, 'blocks_added': len(blocks)}
        
        return {'success': False, 'error': result.get('msg')}
    
    def append(self, doc_token: str, markdown: str) -> dict:
        """Append markdown content"""
        result = self.client.request('POST', '/docx/v1/documents/convert', json={
            'content_type': 'markdown',
            'content': markdown
        })
        
        if result.get('code') != 0:
            return {'success': False, 'error': f"Convert failed: {result.get('msg')}"}
        
        blocks = result['data'].get('blocks', [])
        
        result = self.client.request('POST', f'/docx/v1/documents/{doc_token}/blocks/{doc_token}/children', json={
            'children': blocks
        })
        
        if result.get('code') == 0:
            return {'success': True, 'blocks_added': len(blocks)}
        
        return {'success': False, 'error': result.get('msg')}
    
    def _clear_document(self, doc_token: str):
        """Clear all document content"""
        # Get existing blocks
        result = self.client.request('GET', f'/docx/v1/documents/{doc_token}/blocks/{doc_token}/children')
        if result.get('code') != 0:
            return
        
        items = result['data'].get('items', [])
        child_ids = [b['block_id'] for b in items if b.get('block_type') != 1]
        
        if child_ids:
            self.client.request('DELETE', f'/docx/v1/documents/{doc_token}/blocks/{doc_token}/children/batch_delete', json={
                'start_index': 0,
                'end_index': len(child_ids)
            })
    
    def list_blocks(self, doc_token: str) -> dict:
        """List all blocks in document"""
        result = self.client.request('GET', f'/docx/v1/documents/{doc_token}/blocks/{doc_token}/children')
        
        if result.get('code') == 0:
            items = result['data'].get('items', [])
            blocks = []
            for item in items:
                block = {
                    'block_id': item['block_id'],
                    'type': self._get_block_type_name(item.get('block_type', 0)),
                    'type_code': item.get('block_type')
                }
                blocks.append(block)
            return {'success': True, 'blocks': blocks, 'count': len(blocks)}
        
        return {'success': False, 'error': result.get('msg')}
    
    def _get_block_type_name(self, type_code: int) -> str:
        """Get human-readable block type name"""
        names = {
            1: 'Page', 2: 'Text', 3: 'Heading1', 4: 'Heading2', 5: 'Heading3',
            12: 'Bullet', 13: 'Ordered', 14: 'Code', 15: 'Quote',
            22: 'Divider', 27: 'Image', 31: 'Table'
        }
        return names.get(type_code, f'Unknown({type_code})')
    
    # ==================== Image Operations ====================
    
    def upload_image(self, doc_token: str, image_path: str, block_id: Optional[str] = None) -> dict:
        """Upload image to document"""
        if not os.path.exists(image_path):
            return {'success': False, 'error': f'File not found: {image_path}'}
        
        # Find target block
        if not block_id:
            blocks = self.list_blocks(doc_token)
            if not blocks['success']:
                return blocks
            
            for block in blocks['blocks']:
                if block['type'] == 'Image':
                    block_id = block['block_id']
                    break
            
            if not block_id:
                return {'success': False, 'error': 'No image block found. Create one first with: ![desc](path)'}
        
        # Upload image
        file_name = os.path.basename(image_path)
        file_size = os.path.getsize(image_path)
        
        url = f"{FEISHU_API}/drive/v1/medias/upload_all"
        headers = {'Authorization': f'Bearer {self.client.token}'}
        
        with open(image_path, 'rb') as f:
            files = {'file': (file_name, f, 'application/octet-stream')}
            data = {
                'file_name': file_name,
                'parent_type': 'docx_image',
                'parent_node': block_id,
                'size': str(file_size),
            }
            
            resp = requests.post(url, headers=headers, files=files, data=data)
            result = resp.json()
        
        if result.get('code') != 0:
            return {'success': False, 'error': f"Upload failed: {result.get('msg')}"}
        
        file_token = result['data']['file_token']
        
        # Update block
        result = self.client.request('PATCH', f'/docx/v1/documents/{doc_token}/blocks/{block_id}', json={
            'replace_image': {'token': file_token}
        })
        
        if result.get('code') == 0:
            return {'success': True, 'block_id': block_id, 'file_token': file_token}
        
        return {'success': False, 'error': result.get('msg')}
    
    # ==================== Permission Operations ====================
    
    def list_permissions(self, doc_token: str) -> dict:
        """List document permissions"""
        result = self.client.request('GET', f'/docx/v1/documents/{doc_token}/permission/member/list')
        
        if result.get('code') == 0:
            members = result['data'].get('items', [])
            return {'success': True, 'members': members, 'count': len(members)}
        
        return {'success': False, 'error': result.get('msg')}
    
    def add_permission(self, doc_token: str, member_id: str, perm: str = 'view') -> dict:
        """Add permission for user/group
        
        Args:
            member_id: Open ID or email
            perm: 'view', 'edit', or 'full_access'
        """
        data = {
            'member_type': 'openid',  # or 'email'
            'member_id': member_id,
            'perm': perm
        }
        
        result = self.client.request('POST', f'/docx/v1/documents/{doc_token}/permission/member/create', json=data)
        
        if result.get('code') == 0:
            return {'success': True}
        
        return {'success': False, 'error': result.get('msg')}
    
    def remove_permission(self, doc_token: str, member_id: str) -> dict:
        """Remove permission"""
        result = self.client.request('DELETE', f'/docx/v1/documents/{doc_token}/permission/member/delete', params={
            'member_type': 'openid',
            'member_id': member_id
        })
        
        if result.get('code') == 0:
            return {'success': True}
        
        return {'success': False, 'error': result.get('msg')}


def print_json(data: dict):
    """Print formatted JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='Feishu Doc Manager - Complete CLI for Feishu Documents')
    parser.add_argument('--format', choices=['json', 'table'], default='table', help='Output format')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create
    create_parser = subparsers.add_parser('create', help='Create new document')
    create_parser.add_argument('title', help='Document title')
    create_parser.add_argument('--folder', help='Parent folder token')
    
    # Read
    read_parser = subparsers.add_parser('read', help='Read document')
    read_parser.add_argument('doc_token', help='Document token')
    
    # Write
    write_parser = subparsers.add_parser('write', help='Write markdown content (replaces all)')
    write_parser.add_argument('doc_token', help='Document token')
    write_parser.add_argument('file', help='Markdown file path')
    
    # Append
    append_parser = subparsers.add_parser('append', help='Append markdown content')
    append_parser.add_argument('doc_token', help='Document token')
    append_parser.add_argument('file', help='Markdown file path')
    
    # List blocks
    subparsers.add_parser('list-blocks', help='List all blocks')
    
    # Upload image
    img_parser = subparsers.add_parser('upload-image', help='Upload image to document')
    img_parser.add_argument('doc_token', help='Document token')
    img_parser.add_argument('image_path', help='Image file path')
    img_parser.add_argument('--block-id', help='Target image block ID')
    
    # Permissions
    perm_parser = subparsers.add_parser('permissions', help='Manage permissions')
    perm_sub = perm_parser.add_subparsers(dest='perm_cmd')
    
    # List permissions
    perm_sub.add_parser('list', help='List permissions')
    
    # Add permission
    add_perm = perm_sub.add_parser('add', help='Add permission')
    add_perm.add_argument('doc_token', help='Document token')
    add_perm.add_argument('member_id', help='Member ID (open_id or email)')
    add_perm.add_argument('--perm', choices=['view', 'edit', 'full_access'], default='view')
    
    # Remove permission
    rm_perm = perm_sub.add_parser('remove', help='Remove permission')
    rm_perm.add_argument('doc_token', help='Document token')
    rm_perm.add_argument('member_id', help='Member ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        client = FeishuClient()
        doc = DocManager(client)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Execute command
    if args.command == 'create':
        result = doc.create(args.title, args.folder)
        if result['success']:
            print(f"✅ Document created: {result['title']}")
            print(f"   Token: {result['doc_token']}")
            print(f"   URL: {result['url']}")
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)
    
    elif args.command == 'read':
        result = doc.read(args.doc_token)
        if result['success']:
            print(f"📄 {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"\n{result['content'][:500]}...")
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)
    
    elif args.command == 'write':
        with open(args.file) as f:
            content = f.read()
        result = doc.write(args.doc_token, content)
        if result['success']:
            print(f"✅ Written {result['blocks_added']} blocks")
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)
    
    elif args.command == 'append':
        with open(args.file) as f:
            content = f.read()
        result = doc.append(args.doc_token, content)
        if result['success']:
            print(f"✅ Appended {result['blocks_added']} blocks")
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)
    
    elif args.command == 'list-blocks':
        # This needs doc_token - should be a positional arg
        print("Usage: feishu-doc list-blocks <doc_token>")
        sys.exit(1)
    
    elif args.command == 'upload-image':
        result = doc.upload_image(args.doc_token, args.image_path, args.block_id)
        if result['success']:
            print(f"✅ Image uploaded to block {result['block_id'][:20]}...")
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)
    
    elif args.command == 'permissions':
        if not args.perm_cmd:
            perm_parser.print_help()
            sys.exit(1)
        
        # Handle permission subcommands
        print("Permission commands need doc_token parameter fix")


if __name__ == '__main__':
    main()
