#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法大大电子签客户端封装
用于发起单个/批量签署任务、查询状态、下载合同等操作
"""

import requests
import hashlib
import time
import uuid
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional


class FaDaDaClient:
    """法大大电子签客户端"""

    def __init__(self, app_id: str, app_secret: str, open_corp_id: str,
                 server_url: str = 'https://uat-dev.fadada.com/'):
        """
        初始化法大大客户端

        Args:
            app_id: 应用ID
            app_secret: 应用密钥
            open_corp_id: 企业ID
            server_url: 服务器地址（默认沙箱环境）
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.open_corp_id = open_corp_id
        self.server_url = server_url.rstrip('/') + '/'
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    def _generate_signature(self) -> Dict[str, str]:
        """生成签名"""
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4())
        signature_str = self.app_id + timestamp + nonce + self.app_secret
        signature = hashlib.md5(signature_str.encode()).hexdigest()

        return {
            'timestamp': timestamp,
            'nonce': nonce,
            'signature': signature
        }

    def _make_request(self, endpoint: str, data: Dict, method: str = 'POST') -> Dict:
        """
        发起 API 请求

        Args:
            endpoint: API 端点
            data: 请求数据
            method: HTTP 方法（GET/POST）

        Returns:
            API 响应字典
        """
        url = self.server_url + endpoint
        signature_data = self._generate_signature()

        headers = {
            'X-APP-ID': self.app_id,
            'X-TIMESTAMP': signature_data['timestamp'],
            'X-NONCE': signature_data['nonce'],
            'X-SIGNATURE': signature_data['signature']
        }

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=data, headers=headers, timeout=30)
            else:
                response = self.session.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                'code': -1,
                'msg': f'请求失败: {str(e)}',
                'data': None
            }

    def upload_file(self, file_path: str) -> Dict:
        """
        上传文件

        Args:
            file_path: 本地文件路径

        Returns:
            上传结果，包含 fileUrl
        """
        url = self.server_url + 'api/file/upload'
        signature_data = self._generate_signature()

        headers = {
            'X-APP-ID': self.app_id,
            'X-TIMESTAMP': signature_data['timestamp'],
            'X-NONCE': signature_data['nonce'],
            'X-SIGNATURE': signature_data['signature']
        }

        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = self.session.post(url, files=files, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {
                'code': -1,
                'msg': f'文件上传失败: {str(e)}',
                'data': None
            }

    def create_sign_task(self, doc_title: str, file_url: str,
                        signers: List[Dict], sign_flow: int = 0,
                        doc_description: str = '') -> Dict:
        """
        创建签署任务

        Args:
            doc_title: 合同标题
            file_url: 文件URL（已上传）
            signers: 签署人列表
            sign_flow: 签署流程（0: 同时签, 1: 顺序签）
            doc_description: 合同描述

        Returns:
            签署任务结果
        """
        data = {
            'openCorpId': self.open_corp_id,
            'docTitle': doc_title,
            'fileUrl': file_url,
            'signers': signers,
            'signFlow': str(sign_flow)
        }

        if doc_description:
            data['docDescription'] = doc_description

        return self._make_request('api/signTask/createSignTask', data)

    def get_sign_url(self, sign_task_id: str, signer_type: int,
                    mobile: str) -> Dict:
        """
        获取参与方签署链接

        Args:
            sign_task_id: 签署任务ID
            signer_type: 签署人类型（1: 个人, 2: 企业）
            mobile: 签署人手机号

        Returns:
            签署链接结果
        """
        data = {
            'openCorpId': self.open_corp_id,
            'signTaskId': sign_task_id,
            'signerType': str(signer_type),
            'mobile': mobile
        }

        return self._make_request('api/sign/getSignUrl', data)

    def query_sign_status(self, sign_task_id: str) -> Dict:
        """
        查询签署任务状态

        Args:
            sign_task_id: 签署任务ID

        Returns:
            任务状态信息
        """
        data = {
            'openCorpId': self.open_corp_id,
            'signTaskId': sign_task_id
        }

        return self._make_request('api/sign/querySignStatus', data, method='GET')

    def download_signed_contract(self, sign_task_id: str,
                                  save_path: Optional[str] = None) -> Dict:
        """
        下载已签署的合同

        Args:
            sign_task_id: 签署任务ID
            save_path: 保存路径（可选）

        Returns:
            下载结果
        """
        data = {
            'openCorpId': self.open_corp_id,
            'signTaskId': sign_task_id
        }

        result = self._make_request('api/sign/downloadContract', data, method='GET')

        if result.get('code') == 200 and result.get('data'):
            # 如果需要保存文件
            if save_path:
                # 假设返回的是文件下载链接
                file_url = result['data'].get('downloadUrl')
                if file_url:
                    response = self.session.get(file_url, stream=True)
                    if response.status_code == 200:
                        with open(save_path, 'wb') as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        result['data']['savePath'] = save_path

        return result

    def cancel_sign_task(self, sign_task_id: str) -> Dict:
        """
        撤销签署任务

        Args:
            sign_task_id: 签署任务ID

        Returns:
            撤销结果
        """
        data = {
            'openCorpId': self.open_corp_id,
            'signTaskId': sign_task_id
        }

        return self._make_request('api/sign/cancelSignTask', data)


def parse_excel_signers(excel_path: str) -> List[Dict]:
    """
    解析 Excel 文件获取签署人信息

    Args:
        excel_path: Excel 文件路径

    Returns:
        签署人列表
    """
    try:
        df = pd.read_excel(excel_path)
        signers = []
        for index, row in df.iterrows():
            signer = {
                'signerType': 1,  # 默认为个人签署
            }

            # 尝试多种列名格式
            name = row.get('姓名') or row.get('Name') or row.get('name')
            mobile = row.get('手机号') or row.get('Mobile') or row.get('手机') or row.get('mobile')
            email = row.get('邮箱') or row.get('Email') or row.get('email')

            if pd.isna(name) or pd.isna(mobile):
                continue

            signer['name'] = str(name).strip()
            signer['mobile'] = str(mobile).strip()

            if not pd.isna(email):
                signer['email'] = str(email).strip()

            signers.append(signer)

        return signers
    except Exception as e:
        return []


def create_single_sign_task(client: FaDaDaClient, file_path: str,
                            doc_title: str, signer_name: str, signer_mobile: str,
                            doc_description: str = '', sign_flow: int = 0) -> Dict:
    """
    创建单个签署任务

    Args:
        client: FaDaDaClient 实例
        file_path: 合同文件路径
        doc_title: 合同标题
        signer_name: 签署人姓名
        signer_mobile: 签署人手机号
        doc_description: 合同描述
        sign_flow: 签署流程（0: 同时签, 1: 顺序签）

    Returns:
        操作结果，包含任务ID和签署链接
    """
    # 上传文件
    upload_result = client.upload_file(file_path)
    if upload_result.get('code') != 200:
        return upload_result

    file_url = upload_result['data'].get('fileUrl')
    if not file_url:
        return {'code': -1, 'msg': '未能获取文件URL', 'data': None}

    # 构建签署人列表
    signer = {
        'signerType': 1,
        'name': signer_name,
        'mobile': signer_mobile
    }
    signers = [signer]

    # 创建签署任务
    task_result = client.create_sign_task(
        doc_title=doc_title,
        file_url=file_url,
        signers=signers,
        sign_flow=sign_flow,
        doc_description=doc_description
    )

    if task_result.get('code') != 200:
        return task_result

    # 获取签署链接
    sign_task_id = task_result['data'].get('signTaskId')
    url_result = client.get_sign_url(
        sign_task_id=sign_task_id,
        signer_type=1,
        mobile=signer_mobile
    )

    if url_result.get('code') == 200:
        sign_url = url_result['data'].get('signUrl')
        task_result['data']['signUrl'] = sign_url

    return task_result


def create_batch_sign_tasks_from_excel(client: FaDaDaClient, file_path: str,
                                       excel_path: str, doc_title: str,
                                       doc_description: str = '',
                                       sign_flow: int = 0) -> Dict:
    """
    基于Excel文件批量创建签署任务

    Args:
        client: FaDaDaClient 实例
        file_path: 合同文件路径
        excel_path: Excel文件路径
        doc_title: 合同标题
        doc_description: 合同描述
        sign_flow: 签署流程

    Returns:
        操作结果
    """
    # 解析签署人
    signers = parse_excel_signers(excel_path)
    if not signers:
        return {'code': -1, 'msg': '未能解析到签署人信息', 'data': None}

    # 上传文件
    upload_result = client.upload_file(file_path)
    if upload_result.get('code') != 200:
        return upload_result

    file_url = upload_result['data'].get('fileUrl')
    if not file_url:
        return {'code': -1, 'msg': '未能获取文件URL', 'data': None}

    # 创建签署任务
    task_result = client.create_sign_task(
        doc_title=doc_title,
        file_url=file_url,
        signers=signers,
        sign_flow=sign_flow,
        doc_description=doc_description
    )

    if task_result.get('code') != 200:
        return task_result

    # 获取所有签署链接
    sign_task_id = task_result['data'].get('signTaskId')
    sign_links = []

    for signer in signers:
        url_result = client.get_sign_url(
            sign_task_id=sign_task_id,
            signer_type=signer['signerType'],
            mobile=signer['mobile']
        )

        if url_result.get('code') == 200:
            sign_links.append({
                'name': signer['name'],
                'mobile': signer['mobile'],
                'signUrl': url_result['data'].get('signUrl')
            })

    task_result['data']['signLinks'] = sign_links

    return task_result
