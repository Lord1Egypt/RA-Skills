#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
泛微 E10 API 调用工具
支持流程创建、待办查询、审批提交、流程退回等操作
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path

# 配置
TOKEN_CACHE_FILE = Path.home() / ".weaver-e10" / "token.json"
ENV_FILE = Path("/ollama/workspace/.env/weaver-e10.env")

class WeaverE10API:
    def __init__(self):
        self.api_base = os.getenv("WEAVER_API_BASE")
        self.app_key = os.getenv("WEAVER_APP_KEY")
        self.app_secret = os.getenv("WEAVER_APP_SECRET")
        self.corpid = os.getenv("WEAVER_CORPID")
        
        # 验证必需的环境变量
        missing = []
        if not self.api_base:
            missing.append("WEAVER_API_BASE")
        if not self.app_key:
            missing.append("WEAVER_APP_KEY")
        if not self.app_secret:
            missing.append("WEAVER_APP_SECRET")
        if not self.corpid:
            missing.append("WEAVER_CORPID")
        
        if missing:
            raise EnvironmentError(
                f"缺少必需的环境变量：{', '.join(missing)}\n"
                f"请在 .env/weaver-e10.env 中配置这些变量"
            )
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        
        # 加载环境变量
        self._load_env_file()
        # 加载缓存 token
        self._load_token_cache()
    
    def _load_env_file(self):
        """加载 .env 文件"""
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            
            # 重新读取
            self.api_base = os.getenv("WEAVER_API_BASE", self.api_base)
            self.app_key = os.getenv("WEAVER_APP_KEY", self.app_key)
            self.app_secret = os.getenv("WEAVER_APP_SECRET", self.app_secret)
            self.corpid = os.getenv("WEAVER_CORPID", self.corpid)
    
    def _load_token_cache(self):
        """加载缓存的 token"""
        if TOKEN_CACHE_FILE.exists():
            try:
                with open(TOKEN_CACHE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.access_token = data.get('access_token')
                    self.refresh_token = data.get('refresh_token')
                    expires_at = data.get('expires_at')
                    if expires_at:
                        self.token_expires_at = datetime.fromisoformat(expires_at)
            except Exception as e:
                print(f"⚠️ 加载 token 缓存失败：{e}", file=sys.stderr)
    
    def _save_token_cache(self):
        """保存 token 到缓存"""
        TOKEN_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None
            }, f, indent=2, ensure_ascii=False)
    
    def _is_token_expired(self):
        """检查 token 是否过期（提前 5 分钟）"""
        if not self.token_expires_at:
            return True
        return datetime.now() >= (self.token_expires_at - timedelta(minutes=5))
    
    def get_code(self):
        """获取授权 code"""
        url = f"{self.api_base}/papi/openapi/oauth2/authorize"
        params = {
            'corpid': self.corpid,
            'response_type': 'code',
            'state': 'weaver-e10-api'
        }
        
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('errcode') != '0':
            raise Exception(f"获取 code 失败：{data.get('errmsg')}")
        
        return data['code']
    
    def get_access_token(self, code):
        """用 code 换取 access_token"""
        url = f"{self.api_base}/papi/openapi/oauth2/access_token"
        payload = {
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'grant_type': 'authorization_code',
            'code': code
        }
        
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('errcode') != '0':
            raise Exception(f"获取 access_token 失败：{data.get('errmsg')}")
        
        self.access_token = data['accessToken']
        self.refresh_token = data.get('refreshToken')
        expires_in = data.get('expires_in', 7200)
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        self._save_token_cache()
        return self.access_token
    
    def refresh_access_token(self):
        """刷新 access_token"""
        if not self.refresh_token:
            raise Exception("没有 refresh_token，请重新授权")
        
        url = f"{self.api_base}/papi/openapi/oauth2/refresh_token"
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('errcode') != '0':
            raise Exception(f"刷新 token 失败：{data.get('errmsg')}")
        
        self.access_token = data['accessToken']
        self.refresh_token = data.get('refreshToken')
        expires_in = data.get('expires_in', 7200)
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        self._save_token_cache()
        return self.access_token
    
    def ensure_token(self):
        """确保有有效的 token"""
        if not self.access_token or self._is_token_expired():
            if self.refresh_token and not self._is_token_expired():
                # 尝试刷新
                try:
                    return self.refresh_access_token()
                except:
                    pass
            
            # 重新获取
            code = self.get_code()
            return self.get_access_token(code)
        
        return self.access_token
    
    def create_request(self, userid, workflow_id, form_data=None, title=None, next_flow=False):
        """创建新流程"""
        url = f"{self.api_base}/papi/openapi/api/workflow/core/paService/v1/doCreateRequest"
        access_token = self.ensure_token()
        
        payload = {
            'access_token': access_token,
            'userid': userid,
            'workflowId': workflow_id
        }
        
        if title:
            payload['requestname'] = title
        
        if form_data:
            payload['formData'] = form_data
        
        if next_flow:
            payload['otherParams'] = {'isnextflow': 1}
        
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        message = data.get('message', {})
        if message.get('errcode') != '0':
            raise Exception(f"创建流程失败：{message.get('errmsg')}")
        
        return {
            'requestId': message.get('requestId'),
            'errcode': message.get('errcode'),
            'errmsg': message.get('errmsg')
        }
    
    def get_todos(self, userid, page=1, size=20):
        """获取待办列表"""
        url = f"{self.api_base}/papi/openapi/workflow/v2/getTodoData"
        access_token = self.ensure_token()
        
        params = {
            'access_token': access_token,
            'userid': userid,
            'pageNo': page,
            'pageSize': size
        }
        
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        message = data.get('message', {})
        if message.get('errcode') != '0':
            raise Exception(f"查询待办失败：{message.get('errmsg')}")
        
        return {
            'requests': data.get('requests', []),
            'pageNo': data.get('pageNo'),
            'pageSize': data.get('pageSize'),
            'nextPage': data.get('nextPage')
        }
    
    def approve_request(self, userid, request_id, remark=None):
        """提交/批准流程"""
        url = f"{self.api_base}/papi/openapi/api/workflow/core/paService/v1/submitRequest"
        access_token = self.ensure_token()
        
        payload = {
            'access_token': access_token,
            'userid': userid,
            'requestId': request_id
        }
        
        if remark:
            payload['remark'] = remark
        
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        message = data.get('message', {})
        if message.get('errcode') != '0':
            raise Exception(f"提交审批失败：{message.get('errmsg')}")
        
        return {
            'requestId': message.get('requestId'),
            'errcode': message.get('errcode'),
            'errmsg': message.get('errmsg')
        }
    
    def reject_request(self, userid, request_id, reject_type=1, remark=None):
        """退回流程"""
        url = f"{self.api_base}/papi/openapi/api/workflow/core/paService/v1/rejectRequest"
        access_token = self.ensure_token()
        
        payload = {
            'access_token': access_token,
            'userid': userid,
            'requestId': request_id,
            'RejectToType': reject_type
        }
        
        if remark:
            payload['remark'] = remark
        
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        message = data.get('message', {})
        if message.get('errcode') != '0':
            raise Exception(f"退回流程失败：{message.get('errmsg')}")
        
        return {
            'requestId': message.get('requestId'),
            'errcode': message.get('errcode'),
            'errmsg': message.get('errmsg')
        }


def main():
    parser = argparse.ArgumentParser(description='泛微 E10 API 调用工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # auth 命令
    auth_parser = subparsers.add_parser('auth', help='获取/刷新 token')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建新流程')
    create_parser.add_argument('--userid', type=int, required=True, help='用户 ID')
    create_parser.add_argument('--workflow-id', type=str, required=True, help='工作流 ID')
    create_parser.add_argument('--title', type=str, help='流程标题')
    create_parser.add_argument('--form-data', type=str, help='表单数据（JSON）')
    create_parser.add_argument('--next-flow', action='store_true', help='是否流转到下一节点')
    
    # todos 命令
    todos_parser = subparsers.add_parser('todos', help='查询待办列表')
    todos_parser.add_argument('--userid', type=int, required=True, help='用户 ID')
    todos_parser.add_argument('--page', type=int, default=1, help='页码')
    todos_parser.add_argument('--size', type=int, default=20, help='每页数量')
    
    # approve 命令
    approve_parser = subparsers.add_parser('approve', help='提交/批准流程')
    approve_parser.add_argument('--userid', type=int, required=True, help='用户 ID')
    approve_parser.add_argument('--request-id', type=int, required=True, help='流程 ID')
    approve_parser.add_argument('--remark', type=str, help='审批意见')
    
    # reject 命令
    reject_parser = subparsers.add_parser('reject', help='退回流程')
    reject_parser.add_argument('--userid', type=int, required=True, help='用户 ID')
    reject_parser.add_argument('--request-id', type=int, required=True, help='流程 ID')
    reject_parser.add_argument('--reject-type', type=int, default=1, help='退回类型：0=自由，1=逐级，2=指定，3=按出口')
    reject_parser.add_argument('--remark', type=str, help='退回意见')
    
    args = parser.parse_args()
    api = WeaverE10API()
    
    try:
        if args.command == 'auth':
            token = api.ensure_token()
            print(json.dumps({
                'access_token': token,
                'expires_at': api.token_expires_at.isoformat() if api.token_expires_at else None
            }, indent=2, ensure_ascii=False))
        
        elif args.command == 'create':
            form_data = json.loads(args.form_data) if args.form_data else None
            result = api.create_request(
                userid=args.userid,
                workflow_id=args.workflow_id,
                form_data=form_data,
                title=args.title,
                next_flow=args.next_flow
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'todos':
            result = api.get_todos(
                userid=args.userid,
                page=args.page,
                size=args.size
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'approve':
            result = api.approve_request(
                userid=args.userid,
                request_id=args.request_id,
                remark=args.remark
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'reject':
            result = api.reject_request(
                userid=args.userid,
                request_id=args.request_id,
                reject_type=args.reject_type,
                remark=args.remark
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
