#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大华云开放平台 - 基础通用套件客户端

该脚本提供基础通用套件的完整客户端实现，包括：
- 认证与签名
- 设备管理
- SD卡管理
- 设备配置
- 消息订阅

Required environment variables:
  - DAHUA_CLOUD_PRODUCT_ID: AppID from Dahua Cloud
  - DAHUA_CLOUD_AK: Access Key from Dahua Cloud
  - DAHUA_CLOUD_SK: Secret Key from Dahua Cloud

Required dependency:
  - requests (pip install requests)
  - pycryptodome (仅 AES256 加密时需要，Base64 无需此依赖)

Usage:
  python dahua_iot_client.py --help
"""

import sys
import os
import argparse
import io
import json
import base64
import hashlib
import hmac
import time
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
import requests


# ============================================================================
# Constants
# ============================================================================

DEFAULT_API_BASE_URL = 'https://open.cloud-dahua.com/'
TOKEN_EXPIRY_SECONDS = 604800  # 7天

# API Endpoints - 鉴权认证
API_AUTH_TOKEN = '/open-api/api-base/auth/getAppAccessToken'

# API Endpoints - 设备管理
API_ADD_DEVICE = '/open-api/api-iot/device/addDevice'
API_ADD_GB_DEVICE = '/open-api/api-iot/device/addGbDevice'
API_DELETE_DEVICE = '/open-api/api-iot/device/deleteDevice'
API_GET_DEVICE_LIST = '/open-api/api-iot/device/getDeviceList'
API_LIST_DEVICE_DETAILS = '/open-api/api-iot/device/listDeviceDetailsByIds'
API_DEVICE_ONLINE = '/open-api/api-iot/device/deviceOnline'
API_CHECK_DEVICE_BIND = '/open-api/api-iot/device/checkDeviceBindInfo'
API_GET_CATEGORY = '/open-api/api-iot/device/getCategory'

# API Endpoints - 国标设备
API_LIST_GB_CODE = '/open-api/api-iot/device/listGbCode'
API_GET_SIP_INFO = '/open-api/api-iot/device/getSipInfo'
API_GB_DEVICE_INFO_DETAIL = '/open-api/api-iot/device/deviceInfoDetailAll'
API_MODIFY_GB_DEVICE = '/open-api/api-iot/device/modifyGbDevice'

# API Endpoints - 设备配置
API_MODIFY_DEVICE_NAME = '/open-api/api-iot/device/modifyDeviceName'
API_MODIFY_DEV_CODE = '/open-api/api-iot/device/modifyDevCode'
API_VERIFY_DEV_CODE = '/open-api/api-iot/device/verifyDevCode'
API_GET_ABILITY_STATUS = '/open-api/api-iot/device/getAbilityStatus'
API_SET_ABILITY_STATUS = '/open-api/api-iot/device/setAbilityStatus'
API_SET_CURRENT_UTC = '/open-api/api-aiot/device/setCurrentUTC'

# API Endpoints - SD卡管理
API_FORMAT_SD_CARD = '/open-api/api-aiot/device/formatSDCard'
API_GET_SD_CARD_STATUS = '/open-api/api-aiot/device/getSDCardStatus'
API_GET_SD_CARD_STORAGE = '/open-api/api-aiot/device/getSDCardStorage'
API_LIST_SD_CARD_STORAGE = '/open-api/api-aiot/device/listSDCardStorage'
API_GET_DEVICE_CHANNEL_INFO = '/open-api/api-aiot/device/getDeviceChannelInfo'

# API Endpoints - 铃音配置
API_ADD_CUSTOM_RING = '/open-api/api-aiot/device/addCustomRing'
API_DELETE_CUSTOM_RING = '/open-api/api-aiot/device/deleteCustomRing'
API_LIST_CUSTOM_RING = '/open-api/api-aiot/device/listCustomRing'
API_SET_CUSTOM_RING = '/open-api/api-aiot/device/setCustomRing'

# API Endpoints - 网络配置
API_WIFI_AROUND = '/open-api/api-aiot/device/wifiAround'
API_CURRENT_DEVICE_WIFI = '/open-api/api-aiot/device/currentDeviceWifi'
API_CONTROL_DEVICE_WIFI = '/open-api/api-aiot/device/controlDeviceWifi'

# API Endpoints - 消息订阅
API_ADD_CALLBACK_CONFIG = '/open-api/api-message/addCallbackConfig'
API_GET_ALL_CALLBACK_CONFIG = '/open-api/api-message/getAllCallbackConfigId'
API_MESSAGE_SUBSCRIBE = '/open-api/api-message/messageSubscribeByDeviceIds'
API_GET_MESSAGE_TYPE_PAGE = '/open-api/api-message/getMessageTypePage'
API_GET_SUBSCRIBE_INFO = '/open-api/api-message/getMessageSubscribeInfoByDeviceId'
API_UPDATE_SUBSCRIBE_BY_CALLBACK = '/open-api/api-message/updateSubscribeByCallbackConfigId'
API_UPDATE_BY_CALLBACK_CONFIG = '/open-api/api-message/updateByCallbackConfigId'
API_DELETE_CALLBACK_ID = '/open-api/api-message/deleteCallbackId'
API_GET_INFO_BY_CALLBACK_CONFIG = '/open-api/api-message/getInfoByCallbackConfigId'
API_GET_SUBSCRIBE_INFO_BY_CALLBACK = '/open-api/api-message/getSubscribeInfoByCallbackConfigId'

# API Endpoints - 图片解密
API_IMAGE_DECRYPTO = '/open-api/api-decrypto/image/decrypto'

# API Endpoints - SIM
API_GET_SIM_SIGNAL_STRENGTH = '/open-api/api-aiot/device/getSimSignalStrength'

# HTTP Timeouts (seconds)
TIMEOUT_AUTH = 60
TIMEOUT_DEVICE = 60
TIMEOUT_CONFIG = 60
TIMEOUT_SD_CARD = 60
TIMEOUT_FORMAT_SD = 120  # 格式化SD卡可能较慢

# Environment Variable Names
ENV_CLOUD_ID = 'DAHUA_CLOUD_PRODUCT_ID'
ENV_CLOUD_AK = 'DAHUA_CLOUD_AK'
ENV_CLOUD_SK = 'DAHUA_CLOUD_SK'


def fix_encoding():
    """Fix encoding for Windows PowerShell/CMD to ensure proper display"""
    if sys.platform == 'win32':
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# ============================================================================
# Signature Functions
# ============================================================================

def get_token_sign(access_key: str, timestamp: str, nonce: str, secret: str) -> str:
    """
    Auth API signature (for getting Token)
    Signature factor: access_key + timestamp + nonce
    """
    auth_factor = f'{access_key}{timestamp}{nonce}'
    return hmac.new(
        secret.encode('utf-8'),
        auth_factor.encode('utf-8'),
        hashlib.sha512
    ).hexdigest().upper()


def business_api_sign(access_key: str, app_access_token: str, timestamp: str, nonce: str, secret: str) -> str:
    """
    Business API signature (for all device management APIs)
    Signature factor: access_key + app_access_token + timestamp + nonce
    """
    auth_factor = f'{access_key}{app_access_token}{timestamp}{nonce}'
    return hmac.new(
        secret.encode('utf-8'),
        auth_factor.encode('utf-8'),
        hashlib.sha512
    ).hexdigest().upper()


# ============================================================================
# Device Code Encryption
# ============================================================================

class DeviceCodeEncryptor:
    """设备密码加密工具类"""
    
    # AES加密的固定IV值
    IV = b'86E2DB6D77B5E9CD'
    
    def __init__(self, secret_access_key: str, device_id: Optional[str] = None):
        """
        初始化加密工具
        
        Args:
            secret_access_key: 产品的SecretAccessKey
            device_id: 设备序列号（可选）
        """
        self.secret_access_key = secret_access_key
        self.device_id = device_id
    
    def _generate_aes_key(self) -> bytes:
        """
        生成AES密钥
        算法：Cut32(UpperCase(MD5-32位(UpperCase(sk))))
        """
        # 计算MD5-32位
        md5_hash = hashlib.md5(self.secret_access_key.upper().encode('utf-8')).hexdigest().upper()
        # 截取前32位
        aes_key = md5_hash[:32]
        return aes_key.encode('utf-8')
    
    def encrypt_base64(self, device_password: str) -> str:
        """
        方式一：Base64加密设备密码
        格式："Dolynk_" + Base64(设备密码)
        """
        encoded = base64.b64encode(device_password.encode('utf-8')).decode('utf-8')
        return f"Dolynk_{encoded}"
    
    def encrypt_aes256(self, device_password: str) -> str:
        """
        方式二：AES256加密设备密码
        格式：Base64(Aes256(待加密内容, AesKey, IV初始向量))
        加密算法：Aes256/CBC/PKCS7
        需要 pycryptodome 库：pip install pycryptodome
        """
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import pad
        except ImportError:
            raise RuntimeError(
                'AES256 加密需要 pycryptodome 库。请执行: pip install pycryptodome\n'
                '若无法安装，可使用 Base64 加密: python dahua_iot_client.py add -d <设备ID> -p <密码> -e base64'
            )
        # 生成AES密钥
        aes_key = self._generate_aes_key()
        # 创建AES加密器（CBC模式）
        cipher = AES.new(aes_key, AES.MODE_CBC, self.IV)
        # PKCS7填充并加密
        encrypted = cipher.encrypt(pad(device_password.encode('utf-8'), AES.block_size))
        # Base64编码
        encoded = base64.b64encode(encrypted).decode('utf-8')
        return encoded


# ============================================================================
# Dahua IoT Client
# ============================================================================

class DahuaIoTClient:
    """大华云开放平台 - 基础通用套件客户端"""
    
    def __init__(
        self,
        app_id: str,
        access_key: str,
        secret_key: str,
        api_base_url: str = DEFAULT_API_BASE_URL,
        verbose: bool = True
    ):
        """
        初始化客户端
        
        Args:
            app_id: 产品ID (ProductId)
            access_key: 访问密钥 (AccessKey)
            secret_key: 密钥 (SecretKey)
            api_base_url: API基础地址
            verbose: 是否打印API调用日志（SDK集成时建议设为False）
        """
        self.config = {
            'app_id': app_id,
            'access_key': access_key,
            'secret_key': secret_key,
            'api_base_url': api_base_url.rstrip('/'),
            'verbose': verbose
        }
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        self.token_expiry: int = 0
        self.encryptor = DeviceCodeEncryptor(secret_key)
    
    def _log(self, *args, **kwargs):
        """条件打印（verbose=True时输出）"""
        if self.config.get('verbose', True):
            print(*args, **kwargs)

    def _get_app_access_token(self) -> Optional[str]:
        """获取AppAccessToken"""
        self._log("[Auth] Getting AppAccessToken...")
        
        try:
            timestamp = str(int(time.time() * 1000))
            nonce = str(uuid.uuid4())
            trace_id = f"tid-{int(time.time())}"
            
            # 生成签名
            signature = get_token_sign(
                self.config['access_key'],
                timestamp,
                nonce,
                self.config['secret_key']
            )
            
            headers = {
                'Content-Type': 'application/json',
                'Accept-Language': 'zh-CN',
                'AccessKey': self.config['access_key'],
                'Timestamp': timestamp,
                'Nonce': nonce,
                'Sign': signature,
                'ProductId': self.config['app_id'],
                'X-TraceId-Header': trace_id,
                'Version': 'V1',
                'Sign-Type': 'simple'
            }
            
            payload = {'productId': self.config['app_id']}
            
            url = self.config['api_base_url'] + API_AUTH_TOKEN
            response = self.session.post(url, headers=headers, json=payload, timeout=TIMEOUT_AUTH)
            
            result = response.json()
            
            if result.get('success'):
                self.access_token = result.get('data', {}).get('appAccessToken')
                self.token_expiry = int(time.time()) + TOKEN_EXPIRY_SECONDS
                self._log(f"[OK] Token obtained successfully (expires in {TOKEN_EXPIRY_SECONDS}s)")
                return self.access_token
            else:
                self._log(f"[ERROR] Failed to get token: {result.get('msg')}")
                return None
                
        except Exception as e:
            self._log(f"[EXCEPTION] Auth failed: {e}")
            return None
    
    def _ensure_token(self) -> bool:
        """确保Token有效"""
        current_time = int(time.time())
        if not self.access_token or current_time > self.token_expiry:
            return self._get_app_access_token() is not None
        return True
    
    def _build_headers(self) -> Dict[str, str]:
        """构建业务API请求头"""
        if not self._ensure_token():
            raise ValueError("Failed to get access token")
        
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4())
        trace_id = f"tid-{int(time.time())}"
        
        # 生成签名
        signature = business_api_sign(
            self.config['access_key'],
            self.access_token,
            timestamp,
            nonce,
            self.config['secret_key']
        )
        
        return {
            'Content-Type': 'application/json',
            'Accept-Language': 'zh-CN',
            'AccessKey': self.config['access_key'],
            'Timestamp': timestamp,
            'Nonce': nonce,
            'Sign': signature,
            'ProductId': self.config['app_id'],
            'X-TraceId-Header': trace_id,
            'Version': 'V1',
            'Sign-Type': 'simple',
            'AppAccessToken': self.access_token
        }
    
    def _request(self, endpoint: str, data: Dict[str, Any], timeout: int = TIMEOUT_DEVICE) -> Dict[str, Any]:
        """
        发送API请求
        
        Args:
            endpoint: API端点
            data: 请求数据
            timeout: 超时时间
            
        Returns:
            API响应
        """
        try:
            headers = self._build_headers()
            url = self.config['api_base_url'] + endpoint
            
            self._log(f"[API] POST {endpoint}")
            self._log(f"[DATA] {json.dumps(data, ensure_ascii=False)}")
            
            response = self.session.post(url, headers=headers, json=data, timeout=timeout)
            result = response.json()
            
            resp_preview = json.dumps(result, ensure_ascii=False)
            self._log(f"[RESP] {resp_preview[:200]}{'...' if len(resp_preview) > 200 else ''}")
            
            return result
            
        except Exception as e:
            self._log(f"[EXCEPTION] Request failed: {e}")
            return {'success': False, 'msg': str(e)}
    
    # ========================================================================
    # 设备管理
    # ========================================================================
    
    def add_device(
        self,
        device_id: str,
        device_password: str,
        category_code: str = 'IPC',
        encrypt_method: str = 'base64'
    ) -> Dict[str, Any]:
        """
        添加设备
        
        Args:
            device_id: 设备序列号
            device_password: 设备密码（明文）
            category_code: 设备品类编码
            encrypt_method: 加密方式 ('base64' 或 'aes256')
            
        Returns:
            API响应
        """
        self._log(f"\n[Device] Adding device: {device_id}")
        
        # 加密设备密码
        if encrypt_method == 'aes256':
            dev_code = self.encryptor.encrypt_aes256(device_password)
        else:
            dev_code = self.encryptor.encrypt_base64(device_password)
        
        data = {
            'deviceId': device_id,
            'devCode': dev_code,
            'categoryCode': category_code
        }
        
        return self._request(API_ADD_DEVICE, data)
    
    def delete_device(self, device_id: str) -> Dict[str, Any]:
        """
        删除设备
        
        Args:
            device_id: 设备序列号
            
        Returns:
            API响应
        """
        self._log(f"\n[Device] Deleting device: {device_id}")
        
        data = {'deviceId': device_id}
        return self._request(API_DELETE_DEVICE, data)
    
    def verify_device_password(
        self,
        device_id: str,
        device_password: str,
        encrypt_method: str = 'base64'
    ) -> Dict[str, Any]:
        """
        验证设备密码是否正确
        
        Args:
            device_id: 设备序列号
            device_password: 设备密码（明文）
            encrypt_method: 加密方式 ('base64' 或 'aes256')
            
        Returns:
            API响应，success 为 True 表示密码正确
        """
        self._log(f"\n[Device] Verifying password for: {device_id}")
        
        if encrypt_method == 'aes256':
            dev_code = self.encryptor.encrypt_aes256(device_password)
        else:
            dev_code = self.encryptor.encrypt_base64(device_password)
        
        data = {'deviceId': device_id, 'devCode': dev_code}
        return self._request(API_VERIFY_DEV_CODE, data)
    
    def get_device_list(
        self,
        page_num: int = 1,
        page_size: int = 10,
        device_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        查询设备列表
        
        Args:
            page_num: 页码
            page_size: 每页条数
            device_id: 设备序列号（支持模糊查询）
            
        Returns:
            API响应
        """
        self._log(f"\n[Device] Getting device list (page {page_num}, size {page_size})")
        
        data = {
            'pageNum': page_num,
            'pageSize': page_size
        }
        
        if device_id:
            data['deviceId'] = device_id
        
        return self._request(API_GET_DEVICE_LIST, data)
    
    def get_device_online(self, device_id: str) -> Dict[str, Any]:
        """
        获取设备在线状态
        
        Args:
            device_id: 设备序列号
            
        Returns:
            API响应
        """
        self._log(f"\n[Device] Getting online status: {device_id}")
        
        data = {'deviceId': device_id}
        return self._request(API_DEVICE_ONLINE, data)
    
    def check_device_bind(self, device_id: str) -> Dict[str, Any]:
        """
        查询设备绑定状态
        
        Args:
            device_id: 设备序列号
            
        Returns:
            API响应，含 bindStatus、deviceExist、status
        """
        self._log(f"\n[Device] Checking bind status: {device_id}")
        
        data = {'deviceId': device_id}
        return self._request(API_CHECK_DEVICE_BIND, data)
    
    def list_device_details(self, device_ids: List[str]) -> Dict[str, Any]:
        """
        批量查询设备详细信息
        
        Args:
            device_ids: 设备序列号列表（最多100个）
            
        Returns:
            API响应
        """
        self._log(f"\n[Device] Getting details for {len(device_ids)} devices")
        
        data = {
            'deviceList': [{'deviceId': did} for did in device_ids]
        }
        
        return self._request(API_LIST_DEVICE_DETAILS, data)
    
    def get_device_channel_info(self, device_id: str) -> Dict[str, Any]:
        """
        获取设备通道信息
        
        查询设备通道下挂载设备的序列号、设备大类、设备型号信息。
        
        Args:
            device_id: 设备序列号
            
        Returns:
            API响应，含 channels 通道列表
        """
        self._log(f"\n[Device] Getting channel info: {device_id}")
        
        data = {'deviceId': device_id}
        return self._request(API_GET_DEVICE_CHANNEL_INFO, data)
    
    def get_category(
        self,
        primary_category_code: Optional[str] = None,
        second_category_code: Optional[str] = None,
        device_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        查询设备品类
        
        Args:
            primary_category_code: 1级设备类别代码
            second_category_code: 2级设备类别代码（如 IPC）
            device_model: 设备型号（仅支持每次传一个）
            
        Returns:
            API响应，含 categoryList
        """
        self._log(f"\n[Device] Getting device category list")
        
        data: Dict[str, Any] = {}
        if primary_category_code:
            data['primaryCategoryCode'] = primary_category_code
        if second_category_code:
            data['secondCategoryCode'] = second_category_code
        if device_model:
            data['deviceModel'] = device_model
        
        return self._request(API_GET_CATEGORY, data)
    
    # ========================================================================
    # 国标设备
    # ========================================================================
    
    def list_gb_code(
        self,
        count: int = 10,
        prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取国标码列表
        
        Args:
            count: 单次查询数量（1-10000）
            prefix: 自定义国标码前缀（长度必须13位）
            
        Returns:
            API响应，含 minGbCode、maxGbCode
        """
        self._log(f"\n[GB] Getting GB code list (count={count})")
        
        data = {'count': count}
        if prefix:
            data['prefix'] = prefix
        
        return self._request(API_LIST_GB_CODE, data)
    
    def get_sip_info(self) -> Dict[str, Any]:
        """
        获取国标设备注册信息（Sip服务器IP和端口号）
        
        Returns:
            API响应，含 sipServerIp
        """
        self._log(f"\n[GB] Getting SIP registration info")
        
        return self._request(API_GET_SIP_INFO, {})
    
    def add_gb_device(
        self,
        gb_code: str,
        channel_number: int,
        device_password: Optional[str] = None,
        dev_code: Optional[str] = None,
        encrypt_method: str = 'base64',
        manufacturer: Optional[str] = None,
        gb_stream_model: Optional[str] = None,
        device_class: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        添加国标设备
        
        Args:
            gb_code: 国标码
            channel_number: 通道总数
            device_password: 设备注册密码（明文），与 dev_code 二选一
            dev_code: 已加密的注册密码，与 device_password 二选一
            encrypt_method: 密码加密方式（device_password 时有效，base64/aes256）
            manufacturer: 厂商（Dahua、HIKVSION、UNKNOW）
            gb_stream_model: 拉流协议（TCP 或 UDP，默认 UDP）
            device_class: 设备类型（NVR 或 IPC，默认 NVR）
            
        Returns:
            API响应，含 deviceId 等
        """
        self._log(f"\n[GB] Adding GB device: {gb_code}")
        
        if dev_code:
            enc = dev_code
        elif device_password:
            if encrypt_method == 'aes256':
                enc = self.encryptor.encrypt_aes256(device_password)
            else:
                enc = self.encryptor.encrypt_base64(device_password)
        else:
            raise ValueError('必须提供 device_password 或 dev_code')
        
        data = {
            'gbCode': gb_code,
            'devCode': enc,
            'channelNumber': channel_number
        }
        if manufacturer:
            data['manufacturer'] = manufacturer
        if gb_stream_model:
            data['gbStreamModel'] = gb_stream_model
        if device_class:
            data['deviceClass'] = device_class
        
        return self._request(API_ADD_GB_DEVICE, data)
    
    def list_gb_device_details(self, device_ids: List[str]) -> Dict[str, Any]:
        """
        查询国标设备详细信息
        
        Args:
            device_ids: 设备序列号列表
            
        Returns:
            API响应，含国标设备详细信息和通道信息
        """
        self._log(f"\n[GB] Getting details for {len(device_ids)} GB device(s)")
        
        data = {'deviceIds': device_ids}
        return self._request(API_GB_DEVICE_INFO_DETAIL, data)
    
    def modify_gb_device(
        self,
        device_id: str,
        device_password: Optional[str] = None,
        dev_code: Optional[str] = None,
        encrypt_method: str = 'base64',
        gb_stream_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        修改国标设备信息
        
        Args:
            device_id: 设备序列号
            device_password: 新密码（明文），与 dev_code 二选一
            dev_code: 已加密的新密码，与 device_password 二选一
            encrypt_method: 密码加密方式（device_password 时有效）
            gb_stream_model: 拉流协议（TCP 或 UDP）
            
        Returns:
            API响应
        """
        self._log(f"\n[GB] Modifying GB device: {device_id}")
        
        data = {'deviceId': device_id}
        
        if dev_code:
            data['devCode'] = dev_code
        elif device_password:
            if encrypt_method == 'aes256':
                data['devCode'] = self.encryptor.encrypt_aes256(device_password)
            else:
                data['devCode'] = self.encryptor.encrypt_base64(device_password)
        
        if gb_stream_model:
            data['gbStreamModel'] = gb_stream_model
        
        return self._request(API_MODIFY_GB_DEVICE, data)
    
    # ========================================================================
    # SD卡管理
    # ========================================================================
    
    def get_sd_card_status(self, device_id: str, index: Optional[int] = None) -> Dict[str, Any]:
        """
        获取SD卡状态
        
        Args:
            device_id: 设备序列号
            index: SD卡编号（多卡设备需要）
            
        Returns:
            API响应
        """
        self._log(f"\n[SD Card] Getting status for device: {device_id}")
        
        data = {'deviceId': device_id}
        if index is not None:
            data['index'] = index
        
        return self._request(API_GET_SD_CARD_STATUS, data)
    
    def get_sd_card_storage(self, device_id: str, index: Optional[int] = None) -> Dict[str, Any]:
        """
        查询SD卡容量
        
        Args:
            device_id: 设备序列号
            index: SD卡编号（多卡设备需要）
            
        Returns:
            API响应
        """
        self._log(f"\n[SD Card] Getting storage for device: {device_id}")
        
        data = {'deviceId': device_id}
        if index is not None:
            data['index'] = index
        
        return self._request(API_GET_SD_CARD_STORAGE, data)
    
    def format_sd_card(self, device_id: str, index: Optional[int] = None) -> Dict[str, Any]:
        """
        格式化SD卡
        
        Args:
            device_id: 设备序列号
            index: SD卡编号（多卡设备需要）
            
        Returns:
            API响应
        """
        self._log(f"\n[SD Card] Formatting SD card for device: {device_id}")
        
        data = {'deviceId': device_id}
        if index is not None:
            data['index'] = index
        
        return self._request(API_FORMAT_SD_CARD, data, timeout=TIMEOUT_FORMAT_SD)
    
    def list_sd_card_storage(self, device_id: str) -> Dict[str, Any]:
        """获取设备SD卡列表（多卡设备）"""
        self._log(f"\n[SD Card] Getting SD card list for device: {device_id}")
        data = {'deviceId': device_id}
        return self._request(API_LIST_SD_CARD_STORAGE, data)
    
    # ========================================================================
    # 铃音配置
    # ========================================================================
    
    def add_custom_ring(
        self,
        device_id: str,
        name: str,
        url: str,
        ring_type: str,
        channel_id: Optional[str] = None,
        relate_type: Optional[str] = None,
        language: Optional[str] = None,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """新增自定义铃声"""
        self._log(f"\n[Ring] Adding custom ring: {name}")
        data = {'deviceId': device_id, 'name': name, 'url': url, 'type': ring_type}
        if channel_id:
            data['channelId'] = channel_id
        if relate_type:
            data['relateType'] = relate_type
        if language:
            data['language'] = language
        if version:
            data['version'] = version
        return self._request(API_ADD_CUSTOM_RING, data)
    
    def delete_custom_ring(
        self,
        device_id: str,
        index: str,
        relate_type: str
    ) -> Dict[str, Any]:
        """删除自定义铃声"""
        self._log(f"\n[Ring] Deleting custom ring: {index}")
        data = {'deviceId': device_id, 'index': index, 'relateType': relate_type}
        return self._request(API_DELETE_CUSTOM_RING, data)
    
    def list_custom_ring(
        self,
        device_id: str,
        relate_type: str
    ) -> Dict[str, Any]:
        """获取铃声列表"""
        self._log(f"\n[Ring] Getting custom ring list for device: {device_id}")
        data = {'deviceId': device_id, 'relateType': relate_type}
        return self._request(API_LIST_CUSTOM_RING, data)
    
    def set_custom_ring(
        self,
        device_id: str,
        index: str,
        relate_type: str,
        channel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """设置铃声"""
        self._log(f"\n[Ring] Setting custom ring: {index}")
        data = {'deviceId': device_id, 'index': index, 'relateType': relate_type}
        if channel_id:
            data['channelId'] = channel_id
        return self._request(API_SET_CUSTOM_RING, data)
    
    # ========================================================================
    # 网络配置
    # ========================================================================
    
    def wifi_around(self, device_id: str) -> Dict[str, Any]:
        """获取设备周边热点信息"""
        self._log(f"\n[WiFi] Getting wifi around for device: {device_id}")
        data = {'deviceId': device_id}
        return self._request(API_WIFI_AROUND, data)
    
    def current_device_wifi(self, device_id: str) -> Dict[str, Any]:
        """获取设备当前连接的热点信息"""
        self._log(f"\n[WiFi] Getting current wifi for device: {device_id}")
        data = {'deviceId': device_id}
        return self._request(API_CURRENT_DEVICE_WIFI, data)
    
    def control_device_wifi(
        self,
        device_id: str,
        ssid: str,
        bssid: Optional[str] = None,
        password: Optional[str] = None,
        link_enable: Optional[bool] = None,
        channel_sn: Optional[str] = None
    ) -> Dict[str, Any]:
        """修改设备连接热点"""
        self._log(f"\n[WiFi] Controlling device wifi: {device_id}")
        data = {'deviceId': device_id, 'ssid': ssid}
        if bssid:
            data['bssid'] = bssid
        if password:
            data['password'] = password
        if link_enable is not None:
            data['linkEnable'] = link_enable
        if channel_sn:
            data['channelSn'] = channel_sn
        return self._request(API_CONTROL_DEVICE_WIFI, data)
    
    def get_sim_signal_strength(self, device_id: str) -> Dict[str, Any]:
        """获取SIM信号强度"""
        self._log(f"\n[Device] Getting SIM signal strength: {device_id}")
        data = {'deviceId': device_id}
        return self._request(API_GET_SIM_SIGNAL_STRENGTH, data)
    
    # ========================================================================
    # 设备配置
    # ========================================================================
    
    def modify_device_name(
        self,
        device_id: str,
        name: str,
        channel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        修改设备或通道名称
        
        Args:
            device_id: 设备序列号
            name: 新名称
            channel_id: 通道号（修改通道名称时需要）
            
        Returns:
            API响应
        """
        self._log(f"\n[Config] Modifying name for device: {device_id}")
        
        data = {
            'deviceId': device_id,
            'name': name
        }
        
        if channel_id:
            data['channelId'] = channel_id
        
        return self._request(API_MODIFY_DEVICE_NAME, data)
    
    def get_ability_status(
        self,
        device_id: str,
        ability_type: str,
        channel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取设备使能开关状态
        
        Args:
            device_id: 设备序列号
            ability_type: 使能类型
            channel_id: 通道号（通道级使能需要）
            
        Returns:
            API响应
        """
        self._log(f"\n[Config] Getting ability status: {ability_type}")
        
        data = {
            'deviceId': device_id,
            'abilityType': ability_type
        }
        
        if channel_id:
            data['channelId'] = channel_id
        
        return self._request(API_GET_ABILITY_STATUS, data)
    
    def set_ability_status(
        self,
        device_id: str,
        ability_type: str,
        status: str,
        channel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        设置设备使能开关
        
        Args:
            device_id: 设备序列号
            ability_type: 使能类型
            status: 状态 ('on' 或 'off')
            channel_id: 通道号（通道级使能需要）
            
        Returns:
            API响应
        """
        self._log(f"\n[Config] Setting ability {ability_type} to {status}")
        
        data = {
            'deviceId': device_id,
            'abilityType': ability_type,
            'status': status
        }
        
        if channel_id:
            data['channelId'] = channel_id
        
        return self._request(API_SET_ABILITY_STATUS, data)
    
    def modify_dev_code(
        self,
        device_id: str,
        old_password: str,
        new_password: str,
        encrypt_method: str = 'base64'
    ) -> Dict[str, Any]:
        """修改设备密码"""
        self._log(f"\n[Config] Modifying device password: {device_id}")
        if encrypt_method == 'aes256':
            old_code = self.encryptor.encrypt_aes256(old_password)
            new_code = self.encryptor.encrypt_aes256(new_password)
        else:
            old_code = self.encryptor.encrypt_base64(old_password)
            new_code = self.encryptor.encrypt_base64(new_password)
        data = {'deviceId': device_id, 'oldDevCode': old_code, 'newDevCode': new_code}
        return self._request(API_MODIFY_DEV_CODE, data)
    
    def set_current_utc(
        self,
        device_id: str,
        utc: int,
        tolerance: int = 5
    ) -> Dict[str, Any]:
        """设备校时"""
        self._log(f"\n[Config] Setting device time: {device_id}")
        data = {'deviceId': device_id, 'utc': utc, 'tolerance': tolerance}
        return self._request(API_SET_CURRENT_UTC, data)
    
    # ========================================================================
    # 消息订阅
    # ========================================================================
    
    def add_callback_config(
        self,
        callback_url: str,
        is_push: bool = True
    ) -> Dict[str, Any]:
        """
        添加回调配置
        
        Args:
            callback_url: 回调地址
            is_push: 是否开启推送
            
        Returns:
            API响应
        """
        self._log(f"\n[Message] Adding callback config: {callback_url}")
        
        data = {
            'callbackUrl': callback_url,
            'isPush': is_push
        }
        
        return self._request(API_ADD_CALLBACK_CONFIG, data)
    
    def message_subscribe(
        self,
        device_ids: List[str],
        message_type_codes: List[str],
        category_code: str,
        callback_config_id: int
    ) -> Dict[str, Any]:
        """
        订阅设备消息
        
        Args:
            device_ids: 设备序列号列表（最多50个）
            message_type_codes: 消息类型列表
            category_code: 设备品类编码
            callback_config_id: 回调配置ID
            
        Returns:
            API响应
        """
        self._log(f"\n[Message] Subscribing {len(device_ids)} devices to {len(message_type_codes)} message types")
        
        data = {
            'deviceIds': device_ids,
            'messageTypeCodes': message_type_codes,
            'categoryCode': category_code,
            'callbackConfigId': callback_config_id
        }
        
        return self._request(API_MESSAGE_SUBSCRIBE, data)
    
    def get_all_callback_config(
        self,
        page_num: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """分页获取回调配置ID和回调配置地址"""
        self._log(f"\n[Message] Getting callback config list (page {page_num})")
        data = {'pageNum': page_num, 'pageSize': page_size}
        return self._request(API_GET_ALL_CALLBACK_CONFIG, data)
    
    def get_subscribe_info_by_device(self, device_id: str) -> Dict[str, Any]:
        """根据设备ID查询消息订阅信息"""
        self._log(f"\n[Message] Getting subscribe info for device: {device_id}")
        data = {'deviceId': device_id}
        return self._request(API_GET_SUBSCRIBE_INFO, data)
    
    def get_message_type_page(
        self,
        category_code: str,
        page_num: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """按设备品类获取可订阅的消息类型"""
        self._log(f"\n[Message] Getting message types for category: {category_code}")
        data = {'categoryCode': category_code, 'pageNum': page_num, 'pageSize': page_size}
        return self._request(API_GET_MESSAGE_TYPE_PAGE, data)
    
    def update_subscribe_by_callback_config(
        self,
        callback_config_id: int,
        device_id: str,
        message_type_codes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """根据回调配置ID更新设备订阅消息"""
        self._log(f"\n[Message] Updating subscribe for callback {callback_config_id}")
        data = {'callbackConfigId': callback_config_id, 'deviceId': device_id}
        if message_type_codes:
            data['messageTypeCodes'] = message_type_codes
        return self._request(API_UPDATE_SUBSCRIBE_BY_CALLBACK, data)
    
    def update_callback_config(
        self,
        callback_config_id: int,
        callback_url: Optional[str] = None,
        is_push: Optional[bool] = None
    ) -> Dict[str, Any]:
        """按回调配置ID更新回调配置"""
        self._log(f"\n[Message] Updating callback config: {callback_config_id}")
        data = {'callbackConfigId': callback_config_id}
        if callback_url is not None:
            data['callbackUrl'] = callback_url
        if is_push is not None:
            data['isPush'] = is_push
        return self._request(API_UPDATE_BY_CALLBACK_CONFIG, data)
    
    def delete_callback_config(self, callback_config_ids: List[int]) -> Dict[str, Any]:
        """删除回调配置及相关订阅消息"""
        self._log(f"\n[Message] Deleting callback configs: {callback_config_ids}")
        data = {'callbackConfigIds': callback_config_ids}
        return self._request(API_DELETE_CALLBACK_ID, data)
    
    def get_callback_config_info(self, callback_config_id: int) -> Dict[str, Any]:
        """按回调配置ID搜索回调配置信息"""
        self._log(f"\n[Message] Getting callback config info: {callback_config_id}")
        data = {'callbackConfigId': callback_config_id}
        return self._request(API_GET_INFO_BY_CALLBACK_CONFIG, data)
    
    def get_subscribe_info_by_callback_config(
        self,
        callback_config_id: int
    ) -> Dict[str, Any]:
        """根据回调配置ID搜索已订阅的设备消息"""
        self._log(f"\n[Message] Getting subscribe info for callback: {callback_config_id}")
        data = {'callbackConfigId': callback_config_id}
        return self._request(API_GET_SUBSCRIBE_INFO_BY_CALLBACK, data)
    
    def image_decrypt(
        self,
        device_id: str,
        image_url: str,
        dev_code: Optional[str] = None,
        is_tcm_device: Optional[bool] = None
    ) -> Dict[str, Any]:
        """图片解密"""
        self._log(f"\n[Decrypto] Decrypting image for device: {device_id}")
        data = {'deviceId': device_id, 'imageUrl': image_url}
        if dev_code:
            data['devCode'] = dev_code
        if is_tcm_device is not None:
            data['isTcmDevice'] = is_tcm_device
        return self._request(API_IMAGE_DECRYPTO, data)


# ============================================================================
# Helper Functions
# ============================================================================

def create_client_from_env(verbose: bool = True) -> DahuaIoTClient:
    """从环境变量创建客户端"""
    app_id = os.environ.get(ENV_CLOUD_ID)
    access_key = os.environ.get(ENV_CLOUD_AK)
    secret_key = os.environ.get(ENV_CLOUD_SK)
    
    if not all([app_id, access_key, secret_key]):
        raise ValueError(
            f'Missing required environment variables!\n'
            f'Please set:\n'
            f'  {ENV_CLOUD_ID}\n'
            f'  {ENV_CLOUD_AK}\n'
            f'  {ENV_CLOUD_SK}'
        )
    
    return DahuaIoTClient(app_id, access_key, secret_key, verbose=verbose)


# ============================================================================
# Command Line Interface
# ============================================================================

def get_client(args):
    """获取客户端实例（仅当同时提供全部凭证参数时使用，否则使用环境变量）"""
    pid = getattr(args, 'product_id', None)
    ak = getattr(args, 'access_key', None)
    sk = getattr(args, 'secret_key', None)
    if pid and ak and sk:
        return DahuaIoTClient(app_id=pid, access_key=ak, secret_key=sk, verbose=True)
    return create_client_from_env(verbose=True)


def cmd_add_device(args):
    """添加设备命令"""
    client = get_client(args)
    result = client.add_device(
        device_id=args.device_id,
        device_password=args.password,
        category_code=args.category,
        encrypt_method=args.encrypt
    )
    print_result(result)


def cmd_add_gb_device(args):
    """添加国标设备命令"""
    client = get_client(args)
    result = client.add_gb_device(
        gb_code=args.gb_code,
        channel_number=args.channels,
        device_password=args.password,
        encrypt_method=args.encrypt,
        manufacturer=args.manufacturer,
        gb_stream_model=args.stream_model,
        device_class=args.device_class
    )
    print_result(result)


def cmd_delete_device(args):
    """删除设备命令"""
    client = get_client(args)
    result = client.delete_device(args.device_id)
    print_result(result)


def cmd_verify_device_password(args):
    """验证设备密码命令"""
    client = get_client(args)
    result = client.verify_device_password(
        device_id=args.device_id,
        device_password=args.password,
        encrypt_method=args.encrypt
    )
    print_result(result)
    if result.get('success'):
        print("\n✓ 密码正确")
    else:
        print("\n✗ 密码错误或验证失败")


def cmd_list_devices(args):
    """查询设备列表命令"""
    client = get_client(args)
    result = client.get_device_list(
        page_num=args.page,
        page_size=args.size,
        device_id=args.device_id
    )
    print_result(result)


def cmd_list_device_details(args):
    """查询设备详细信息命令"""
    client = get_client(args)
    result = client.list_device_details(args.device_ids)
    print_result(result)


def cmd_get_category(args):
    """查询设备品类命令"""
    client = get_client(args)
    result = client.get_category(
        primary_category_code=args.primary,
        second_category_code=args.second,
        device_model=args.model
    )
    print_result(result)


def cmd_device_online(args):
    """查询设备在线状态命令"""
    client = get_client(args)
    result = client.get_device_online(args.device_id)
    print_result(result)


def cmd_check_device_bind(args):
    """查询设备绑定状态命令"""
    client = get_client(args)
    result = client.check_device_bind(args.device_id)
    print_result(result)


def cmd_get_device_channel_info(args):
    """获取设备通道信息命令"""
    client = get_client(args)
    result = client.get_device_channel_info(args.device_id)
    print_result(result)


def cmd_get_ability_status(args):
    """获取设备使能状态命令"""
    client = get_client(args)
    result = client.get_ability_status(
        device_id=args.device_id,
        ability_type=args.ability_type,
        channel_id=args.channel_id
    )
    print_result(result)


def cmd_list_gb_code(args):
    """获取国标码列表命令"""
    client = get_client(args)
    result = client.list_gb_code(
        count=args.count,
        prefix=args.prefix
    )
    print_result(result)


def cmd_get_sip_info(args):
    """获取国标设备注册信息命令"""
    client = get_client(args)
    result = client.get_sip_info()
    print_result(result)


def cmd_list_gb_device_details(args):
    """查询国标设备详细信息命令"""
    client = get_client(args)
    result = client.list_gb_device_details(args.device_ids)
    print_result(result)


def cmd_modify_gb_device(args):
    """修改国标设备信息命令"""
    client = get_client(args)
    result = client.modify_gb_device(
        device_id=args.device_id,
        device_password=args.password,
        encrypt_method=args.encrypt,
        gb_stream_model=args.stream_model
    )
    print_result(result)


def cmd_encrypt_password(args):
    """加密设备密码命令"""
    encryptor = DeviceCodeEncryptor(args.secret_key, args.device_id)
    
    print(f"\n{'='*60}")
    print("Device Password Encryption")
    print(f"{'='*60}")
    print(f"Original Password: {args.password}")
    
    if args.method == 'aes256':
        encrypted = encryptor.encrypt_aes256(args.password)
        print(f"AES256 Encrypted: {encrypted}")
    else:
        encrypted = encryptor.encrypt_base64(args.password)
        print(f"Base64 Encrypted: {encrypted}")


def print_result(result: Dict[str, Any]):
    """打印API结果"""
    print(f"\n{'='*60}")
    print("API Result")
    print(f"{'='*60}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def add_credential_args(parser):
    """添加凭证参数（可选，优先使用环境变量）"""
    parser.add_argument('--product-id', help='产品ID (可选项，优先使用环境变量)')
    parser.add_argument('--access-key', help='访问密钥 (可选项，优先使用环境变量)')
    parser.add_argument('--secret-key', help='密钥 (可选项，优先使用环境变量)')


def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(
        description='大华云开放平台 - 基础通用套件客户端',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用环境变量（推荐）
  export DAHUA_CLOUD_PRODUCT_ID='xxx'
  export DAHUA_CLOUD_AK='xxx'
  export DAHUA_CLOUD_SK='xxx'
  python dahua_iot_client.py add -d AA08904PHA88879 -p admin123

  # 直接传递凭证
  python dahua_iot_client.py add -d AA08904PHA88879 -p admin123 --product-id xxx --access-key xxx --secret-key xxx
        """
    )
    
    # 添加全局凭证参数
    add_credential_args(parser)
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 添加设备
    add_parser = subparsers.add_parser('add', help='添加设备')
    add_parser.add_argument('--device-id', '-d', required=True, help='设备序列号')
    add_parser.add_argument('--password', '-p', required=True, help='设备密码')
    add_parser.add_argument('--category', '-c', default='IPC', help='设备品类编码')
    add_parser.add_argument('--encrypt', '-e', default='base64', choices=['base64', 'aes256'],
                           help='加密方式（默认 base64，无需 pycryptodome）')
    add_parser.set_defaults(func=cmd_add_device)
    
    # 添加国标设备
    add_gb_parser = subparsers.add_parser('add-gb', help='添加国标设备')
    add_gb_parser.add_argument('--gb-code', '-g', required=True, help='国标码')
    add_gb_parser.add_argument('--password', '-p', required=True, help='设备注册密码')
    add_gb_parser.add_argument('--channels', '-c', type=int, required=True, help='通道总数')
    add_gb_parser.add_argument('--encrypt', '-e', default='base64', choices=['base64', 'aes256'],
                              help='密码加密方式（默认 base64）')
    add_gb_parser.add_argument('--manufacturer', '-m', help='厂商（Dahua、HIKVSION、UNKNOW）')
    add_gb_parser.add_argument('--stream-model', '-s', choices=['TCP', 'UDP'],
                              help='拉流协议（TCP 或 UDP）')
    add_gb_parser.add_argument('--device-class', '-d', choices=['NVR', 'IPC'],
                              help='设备类型（NVR 或 IPC）')
    add_gb_parser.set_defaults(func=cmd_add_gb_device)
    
    # 删除设备
    delete_parser = subparsers.add_parser('delete', help='删除设备')
    delete_parser.add_argument('--device-id', '-d', required=True, help='设备序列号')
    delete_parser.set_defaults(func=cmd_delete_device)
    
    # 验证设备密码
    verify_parser = subparsers.add_parser('verify', help='验证设备密码是否正确')
    verify_parser.add_argument('--device-id', '-d', required=True, help='设备序列号')
    verify_parser.add_argument('--password', '-p', required=True, help='设备密码')
    verify_parser.add_argument('--encrypt', '-e', default='base64', choices=['base64', 'aes256'],
                              help='加密方式')
    verify_parser.set_defaults(func=cmd_verify_device_password)
    
    # 查询设备列表
    list_parser = subparsers.add_parser('list', help='查询设备列表')
    list_parser.add_argument('--page', '-p', type=int, default=1, help='页码')
    list_parser.add_argument('--size', '-s', type=int, default=10, help='每页条数')
    list_parser.add_argument('--device-id', '-d', help='设备序列号（模糊查询）')
    list_parser.set_defaults(func=cmd_list_devices)
    
    # 查询设备详细信息
    details_parser = subparsers.add_parser('details', help='查询设备详细信息')
    details_parser.add_argument('device_ids', nargs='+', help='设备序列号（可多个）')
    details_parser.set_defaults(func=cmd_list_device_details)
    
    # 查询设备品类
    category_parser = subparsers.add_parser('category', help='查询设备品类')
    category_parser.add_argument('--primary', '-p', help='1级设备类别代码')
    category_parser.add_argument('--second', '-s', help='2级设备类别代码（如 IPC）')
    category_parser.add_argument('--model', '-m', help='设备型号')
    category_parser.set_defaults(func=cmd_get_category)
    
    # 查询设备在线状态
    online_parser = subparsers.add_parser('online', help='查询设备在线状态')
    online_parser.add_argument('--device-id', '-d', required=True, help='设备序列号')
    online_parser.set_defaults(func=cmd_device_online)
    
    # 查询设备绑定状态
    bind_parser = subparsers.add_parser('bind', help='查询设备绑定状态')
    bind_parser.add_argument('--device-id', '-d', required=True, help='设备序列号')
    bind_parser.set_defaults(func=cmd_check_device_bind)
    
    # 获取设备通道信息
    channel_parser = subparsers.add_parser('channels', help='获取设备通道信息')
    channel_parser.add_argument('--device-id', '-d', required=True, help='设备序列号')
    channel_parser.set_defaults(func=cmd_get_device_channel_info)
    
    # 获取设备使能状态
    ability_parser = subparsers.add_parser('ability', help='获取设备使能状态')
    ability_parser.add_argument('--device-id', '-d', required=True, help='设备序列号')
    ability_parser.add_argument('--ability-type', '-a', required=True,
                               help='使能类型，如 localRecord、motionDetect、faceCapture 等')
    ability_parser.add_argument('--channel-id', '-c', help='通道号（通道级使能需传）')
    ability_parser.set_defaults(func=cmd_get_ability_status)
    
    # 获取国标码列表
    gb_parser = subparsers.add_parser('gb-code', help='获取国标码列表')
    gb_parser.add_argument('--count', '-c', type=int, default=10, help='查询数量（1-10000，默认10）')
    gb_parser.add_argument('--prefix', '-p', help='国标码前缀（长度必须13位）')
    gb_parser.set_defaults(func=cmd_list_gb_code)
    
    # 获取国标设备注册信息
    sip_parser = subparsers.add_parser('sip-info', help='获取国标设备注册信息（Sip服务器IP和端口）')
    sip_parser.set_defaults(func=cmd_get_sip_info)
    
    # 查询国标设备详细信息
    gb_details_parser = subparsers.add_parser('gb-details', help='查询国标设备详细信息')
    gb_details_parser.add_argument('device_ids', nargs='+', help='设备序列号（可多个）')
    gb_details_parser.set_defaults(func=cmd_list_gb_device_details)
    
    # 修改国标设备信息
    modify_gb_parser = subparsers.add_parser('modify-gb', help='修改国标设备信息')
    modify_gb_parser.add_argument('--device-id', '-d', required=True, help='设备序列号')
    modify_gb_parser.add_argument('--password', '-p', help='新设备密码')
    modify_gb_parser.add_argument('--encrypt', '-e', default='base64', choices=['base64', 'aes256'],
                                 help='密码加密方式')
    modify_gb_parser.add_argument('--stream-model', '-s', choices=['TCP', 'UDP'],
                                 help='拉流协议（TCP 或 UDP）')
    modify_gb_parser.set_defaults(func=cmd_modify_gb_device)
    
    # 加密设备密码
    encrypt_parser = subparsers.add_parser('encrypt', help='加密设备密码')
    encrypt_parser.add_argument('--password', '-p', required=True, help='设备密码')
    encrypt_parser.add_argument('--secret-key', '-s', required=True, help='SecretKey')
    encrypt_parser.add_argument('--device-id', '-d', help='设备序列号')
    encrypt_parser.add_argument('--method', '-m', default='base64', choices=['base64', 'aes256'],
                               help='加密方式（默认 base64）')
    encrypt_parser.set_defaults(func=cmd_encrypt_password)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except ValueError as e:
        print(f'\n[ERROR] {e}')
        sys.exit(1)
    except Exception as e:
        print(f'\n[ERROR] Unexpected error: {e}')
        sys.exit(1)


if __name__ == "__main__":
    fix_encoding()
    main()
