#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Duwi 智能家居 API 客户端
基于 Duwi 开放平台接口文档实现
"""

import requests
import hashlib
import time
import json
import os
from typing import Optional, Dict, List, Any
from datetime import datetime


class DuwiAPIError(Exception):
    """Duwi API 异常"""

    def __init__(self, message: str, code: str = ""):
        self.message = message
        self.code = code
        super().__init__(f"[{code}] {message}" if code else message)


class DuwiClient:
    """Duwi 智能家居 API 客户端"""

    BASE_URL = "https://openapi.duwi.com.cn/homeApi/v1"

    def __init__(
        self,
        appkey: str,
        secret: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        token_expire_time: Optional[int] = None,
        token_file: Optional[str] = None,
    ):
        """
        初始化客户端

        Args:
            appkey: 应用 key
            secret: 应用密钥
            access_token: 访问令牌（可选）
            refresh_token: 刷新令牌（可选）
            token_expire_time: token 过期时间戳（毫秒）
            token_file: token 缓存文件路径（可选）
        """
        self.appkey = appkey
        self.secret = secret
        self.access_token = access_token
        self.token_expire_time = token_expire_time
        self.refresh_token = refresh_token
        self.token_file = token_file
        self.house_no: Optional[str] = None
        self._refreshing = False
        self._use_file_cache = True
        self._cache_ttl = 300

    def _get_timestamp(self) -> str:
        """获取 13 位时间戳"""
        return str(int(time.time() * 1000))

    def _is_token_expired(self) -> bool:
        """检查 token 是否过期"""
        if not self.token_expire_time:
            return True
        current_time = int(time.time() * 1000)
        return current_time >= self.token_expire_time

    def _generate_sign(
        self, params: Dict[str, Any], method: str = "GET", body: str = ""
    ) -> str:
        """
        生成签名

        Args:
            params: 请求参数
            method: 请求方法
            body: 请求体（POST/PUT/DELETE 时使用）

        Returns:
            MD5 签名（小写）
        """
        timestamp = self._get_timestamp()

        if method == "GET":
            # 去除所有空串、制表符、回车换行符等空白字符
            filtered_params = {}
            for k, v in params.items():
                if v not in ["", None]:
                    # 转换为字符串并去除空白字符
                    cleaned_value = str(v).replace('\b', '').replace('\t', '').replace('\r', '').replace('\n', '').strip()
                    if cleaned_value:  # 去除空白后不为空才保留
                        filtered_params[k] = cleaned_value
            
            # 按参数的字母顺序排序
            sorted_keys = sorted(filtered_params.keys())
            # 按照 key1=value1&key2=value2 的方式拼接
            param_str = "&".join([f"{k}={filtered_params[k]}" for k in sorted_keys])
        else:
            # POST/PUT/DELETE: 使用请求体的 JSON 字符串
            # 去除空白字符，保留 {} 内的 json 字符串
            if body:
                # 去除空白字符
                param_str = body.replace('\b', '').replace('\t', '').replace('\r', '').replace('\n', '').replace(' ', '')
            else:
                param_str = "{}"

        # 签名算法：sign=MD5(待签名字符串+secret+time)
        sign_str = f"{param_str}{self.secret}{timestamp}"
        return hashlib.md5(sign_str.encode("utf-8")).hexdigest().lower()

    def _get_headers(
        self, method: str = "GET", body: str = "", params: Optional[Dict] = None
    ) -> Dict[str, str]:
        """获取请求头"""
        timestamp = self._get_timestamp()

        if method == "GET":
            sign = self._generate_sign(params or {}, method, "")
        else:
            sign = self._generate_sign({}, method, body)

        headers = {
            "appkey": self.appkey,
            "time": timestamp,
            "sign": sign,
            "appVersion": "1.0.0",
            "clientVersion": "1.0.0",
            "Content-Type": "application/json",
            "clientModel":"openclaw-skill",
        }

        if self.access_token:
            headers["accessToken"] = self.access_token

        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        skip_auth_refresh: bool = False,
    ) -> Dict[str, Any]:
        """
        发送 HTTP 请求

        Args:
            method: 请求方法
            endpoint: API 端点
            params: URL 参数
            json_data: JSON 请求体
            skip_auth_refresh: 是否跳过自动刷新 token（防止递归）

        Returns:
            API 响应数据
        """
        url = f"{self.BASE_URL}{endpoint}"
        body = json.dumps(json_data) if json_data else ""
        headers = self._get_headers(method, body, params)

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == "POST":
                response = requests.post(
                    url, headers=headers, json=json_data, timeout=10
                )
            elif method == "PUT":
                response = requests.put(
                    url, headers=headers, json=json_data, timeout=10
                )
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise DuwiAPIError(f"不支持的请求方法：{method}")

            result = response.json()
            code = result.get("code", "")

            if code != "10000":
                error_msg = result.get("message", "未知错误")
                if code == "10002" and self.refresh_token and not skip_auth_refresh:
                    if self._refreshing:
                        raise DuwiAPIError("Token 刷新中，请稍后重试", code)
                    self._refreshing = True
                    try:
                        # Token 刷新重试机制（最多 2 次）
                        max_retries = 2
                        for attempt in range(max_retries):
                            try:
                                self.refresh_auth()
                                break
                            except DuwiAPIError as refresh_error:
                                if attempt == max_retries - 1:
                                    raise refresh_error
                                time.sleep(1)  # 等待 1 秒后重试
                        
                        return self._request(method, endpoint, params, json_data, skip_auth_refresh=True)
                    finally:
                        self._refreshing = False
                raise DuwiAPIError(error_msg, code)

            return result

        except requests.exceptions.RequestException as e:
            raise DuwiAPIError(f"网络请求失败：{str(e)}")

    def _request_no_check_result(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict] = None,
            json_data: Optional[Dict] = None,
            skip_auth_refresh: bool = False,
    ) -> Dict[str, Any]:
        """
        发送 HTTP 请求,不做返回码校验

        Args:
            method: 请求方法
            endpoint: API 端点
            params: URL 参数
            json_data: JSON 请求体
            skip_auth_refresh: 是否跳过自动刷新 token（防止递归）

        Returns:
            API 响应数据
        """
        url = f"{self.BASE_URL}{endpoint}"
        body = json.dumps(json_data) if json_data else ""
        headers = self._get_headers(method, body, params)

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == "POST":
                response = requests.post(
                    url, headers=headers, json=json_data, timeout=10
                )
            elif method == "PUT":
                response = requests.put(
                    url, headers=headers, json=json_data, timeout=10
                )
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise DuwiAPIError(f"不支持的请求方法：{method}")

            result = response.json()

            return result

        except requests.exceptions.RequestException as e:
            raise DuwiAPIError(f"网络请求失败：{str(e)}")

    def _parse_expire_time(self, expire_time_str: str) -> int:
        """解析过期时间字符串为时间戳"""
        if not expire_time_str:
            return 0
        try:
            dt = datetime.strptime(expire_time_str, "%Y-%m-%d %H:%M:%S")
            return int(dt.timestamp() * 1000)
        except:
            try:
                return int(expire_time_str)
            except:
                return 0

    def _save_token_file(self):
        """保存 token 到文件"""
        if not self.token_file:
            return
        try:
            token_info = {
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "access_token_expire": self.token_expire_time,
            }
            with open(self.token_file, "w", encoding="utf-8") as f:
                json.dump(token_info, f, indent=2, ensure_ascii=False)
            os.chmod(self.token_file, 0o600)
        except Exception as e:
            import warnings
            warnings.warn(f"Token 文件保存失败：{e}")

    def login(self, phone: str, password: str) -> Dict[str, Any]:
        """
        账户登录

        Args:
            phone: 手机号
            password: 密码

        Returns:
            登录结果（包含 accessToken 等）
        """
        json_data = {"phone": phone, "password": password}
        result = self._request("POST", "/account/login", json_data=json_data)
        data = result.get("data", {})

        self.access_token = data.get("accessToken")
        self.refresh_token = data.get("refreshToken")
        self.token_expire_time = self._parse_expire_time(
            data.get("accessTokenExpireTime", "")
        )
        self._save_token_file()

        return data

    def logout(self) -> bool:
        """账户退出"""
        try:
            self._request("POST", "/account/logout")
        except:
            pass
        self.access_token = None
        self.refresh_token = None
        self.token_expire_time = None
        if self.token_file and os.path.exists(self.token_file):
            try:
                os.remove(self.token_file)
            except:
                pass
        return True

    def refresh_auth(self) -> Dict[str, Any]:
        """
        刷新 Token

        Returns:
            刷新结果
        """
        if not self.refresh_token:
            raise DuwiAPIError("没有 refresh token，请重新登录")

        json_data = {"refreshToken": self.refresh_token}
        result = self._request("PUT", "/account/token", json_data=json_data)
        data = result.get("data", {})

        self.access_token = data.get("accessToken")
        self.refresh_token = data.get("refreshToken")
        self.token_expire_time = self._parse_expire_time(
            data.get("accessTokenExpireTime", "")
        )
        self._save_token_file()

        return data

    def get_houses(self) -> List[Dict[str, Any]]:
        """获取房屋列表"""
        result = self._request("GET", "/house/infos")
        return result.get("data", {}).get("houseInfos", [])

    def get_house_info(self, house_no: str) -> Dict[str, Any]:
        """获取房屋信息"""
        result = self._request("GET", "/house/info", params={"houseNo": house_no})
        return result.get("data", {})

    def get_floors(self, house_no: str, force_refresh: bool = True) -> List[Dict[str, Any]]:
        """
        获取楼层列表
        
        Args:
            house_no: 房屋编号
            force_refresh: 是否强制刷新（默认为 True，总是从 API 获取；False 时优先使用缓存）
        
        Returns:
            楼层列表
        """
        try:
            from cache import get, set
            cache_key = f"floors:{house_no}"

            # 非强制刷新时，优先使用缓存
            if not force_refresh:
                cached = get(cache_key)
                if cached:
                    return cached
            
            # 强制刷新或缓存未命中时，从 API 获取
            result = self._request("GET", "/floor/infos", params={"houseNo": house_no})
            floors = result.get("data", {}).get("floors", [])
            
            # 更新缓存
            set(cache_key, floors, ttl=self._cache_ttl)
            return floors
        except ImportError:
            result = self._request("GET", "/floor/infos", params={"houseNo": house_no})
            return result.get("data", {}).get("floors", [])

    def get_rooms(self, house_no: str, force_refresh: bool = True) -> List[Dict[str, Any]]:
        """
        获取房间列表
        
        Args:
            house_no: 房屋编号
            force_refresh: 是否强制刷新（默认为 True，总是从 API 获取；False 时优先使用缓存）
        
        Returns:
            房间列表
        """
        try:
            from cache import get, set
            cache_key = f"rooms:{house_no}"
            
            # 非强制刷新时，优先使用缓存
            if not force_refresh:
                cached = get(cache_key)
                if cached:
                    return cached
            
            # 强制刷新或缓存未命中时，从 API 获取
            result = self._request("GET", "/room/infos", params={"houseNo": house_no})
            rooms = result.get("data", {}).get("rooms", [])
            
            # 更新缓存
            set(cache_key, rooms, ttl=self._cache_ttl)
            return rooms
        except ImportError:
            result = self._request("GET", "/room/infos", params={"houseNo": house_no})
            return result.get("data", {}).get("rooms", [])

    def get_floors_and_rooms(self, house_no: str, force_refresh: bool = True) -> Dict[str, Any]:
        """
        获取楼层和房间信息
        
        Args:
            house_no: 房屋编号
            force_refresh: 是否强制刷新（默认为 True，总是从 API 获取；False 时优先使用缓存）
        
        Returns:
            楼层和房间信息
        """
        try:
            from cache import get, set
            cache_key = f"floors_rooms:{house_no}"
            
            # 非强制刷新时，优先使用缓存
            if not force_refresh:
                cached = get(cache_key)
                if cached:
                    return cached
            
            # 强制刷新或缓存未命中时，从 API 获取
            result = self._request("GET", "/floor/floorsAndRooms", params={"houseNo": house_no})
            data = result.get("data", {})
            
            # 更新缓存
            set(cache_key, data, ttl=self._cache_ttl)
            return data
        except ImportError:
            result = self._request("GET", "/floor/floorsAndRooms", params={"houseNo": house_no})
            return result.get("data", {})

    def get_terminals(self, house_no: str) -> List[Dict[str, Any]]:
        """获取控制器列表"""
        result = self._request("GET", "/terminal/infos", params={"houseNo": house_no})
        return result.get("data", {}).get("terminals", [])

    def get_terminal_info(self, terminal_sequence: str) -> Dict[str, Any]:
        """获取控制器信息"""
        result = self._request(
            "GET", "/terminal/info", params={"terminalSequence": terminal_sequence}
        )
        return result.get("data", {})

    def get_devices(self, house_no: str, force_refresh: bool = True) -> List[Dict[str, Any]]:
        """
        获取房屋下设备列表
        
        Args:
            house_no: 房屋编号
            force_refresh: 是否强制刷新（默认为 True，总是从 API 获取；False 时优先使用缓存）
        
        Returns:
            设备列表
        """
        try:
            from cache import get, set
            cache_key = f"devices:{house_no}"
            
            # 非强制刷新时，优先使用缓存
            if not force_refresh:
                cached = get(cache_key)
                if cached:
                    return cached
            
            # 强制刷新或缓存未命中时，从 API 获取
            result = self._request("GET", "/device/infos", params={"houseNo": house_no})
            devices = result.get("data", {}).get("devices", [])
            
            # 更新缓存
            set(cache_key, devices, ttl=self._cache_ttl)
            return devices
        except ImportError:
            result = self._request("GET", "/device/infos", params={"houseNo": house_no})
            return result.get("data", {}).get("devices", [])

    def get_terminal_devices(self, terminal_sequence: str) -> List[Dict[str, Any]]:
        """获取控制器下设备列表"""
        result = self._request(
            "GET", "/device/detailInfos", params={"terminalSequence": terminal_sequence}
        )
        return result.get("data", {}).get("devices", [])

    def get_device_info(self, device_no: str) -> Dict[str, Any]:
        """获取单个设备信息"""
        result = self._request("GET", "/device/info", params={"deviceNo": device_no})
        return result.get("data", {})

    def get_device_value(self, device_no: str) -> Dict[str, Any]:
        """获取设备值（状态）"""
        result = self._request("GET", "/device/value", params={"deviceNo": device_no})
        return result.get("data", {}).get("value", {})

    def device_command(
        self, house_no: str, device_no: str, commands: List[Dict[str, Any]]
    ) -> bool:
        """
        设备指令操作

        Args:
            house_no: 房屋编号
            device_no: 设备编号
            commands: 指令列表，如 [{"code": "switch", "value": "on"}]
        
        Returns:
            操作结果
        """
        json_data = {"houseNo": house_no, "deviceNo": device_no, "commands": commands}
        self._request("POST", "/device/batchCommandOperate", json_data=json_data)
        return True

    def get_groups(self, house_no: str, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        获取群组列表（优先缓存，降低接口调用频率）
        
        Args:
            house_no: 房屋编号
            force_refresh: 是否强制刷新（默认为 False，优先使用缓存）
        
        Returns:
            群组列表
        """
        try:
            from cache import get, set
            cache_key = f"groups:{house_no}"
            
            if not force_refresh:
                cached = get(cache_key)
                if cached:
                    return cached
            
            result = self._request("GET", "/deviceGroup/infos", params={"houseNo": house_no})
            groups = result.get("data", {}).get("deviceGroups", [])
            
            set(cache_key, groups, ttl=self._cache_ttl)
            return groups
        except ImportError:
            result = self._request("GET", "/deviceGroup/infos", params={"houseNo": house_no})
            return result.get("data", {}).get("deviceGroups", [])

    def group_command(
        self, house_no: str, group_no: str, commands: List[Dict[str, Any]]
    ) -> bool:
        """群组多指令操作"""
        json_data = {
            "houseNo": house_no,
            "deviceGroupNo": group_no,
            "commands": commands,
        }
        self._request("POST", "/deviceGroup/batchCommandOperate", json_data=json_data)
        return True

    def get_scenes(self, house_no: str, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        获取场景列表（优先缓存，降低接口调用频率）
        
        Args:
            house_no: 房屋编号
            force_refresh: 是否强制刷新（默认为 False，优先使用缓存）
        
        Returns:
            场景列表
        """
        try:
            from cache import get, set
            cache_key = f"scenes:{house_no}"
            
            if not force_refresh:
                cached = get(cache_key)
                if cached:
                    return cached
            
            result = self._request("GET", "/scene/infos", params={"houseNo": house_no})
            scenes = result.get("data", {}).get("scenes", [])
            
            set(cache_key, scenes, ttl=self._cache_ttl)
            return scenes
        except ImportError:
            result = self._request("GET", "/scene/infos", params={"houseNo": house_no})
            return result.get("data", {}).get("scenes", [])

    def execute_scene(self, house_no: str, scene_no: str) -> bool:
        """执行场景"""
        json_data = {"houseNo": house_no, "sceneNo": scene_no}
        self._request("POST", "/scene/execute", json_data=json_data)
        return True

    def get_sensor_stats(
        self,
        house_no: str,
        device_no: str,
        record_type: int,
        start_time: str,
        end_time: str,
        sensor_type: int = 1,
    ) -> Dict[str, Any]:
        """
        获取传感器统计数据

        Args:
            house_no: 房屋编号
            device_no: 传感器设备编号
            record_type: 记录类型 (1=年，2=月，3=日，4=小时)
            start_time: 开始时间
            end_time: 结束时间
            sensor_type: 传感器类型 (1=温度，2=湿度，3=光照度...)
        """
        params = {
            "houseNo": house_no,
            "deviceNo": device_no,
            "recordType": record_type,
            "startTime": start_time,
            "endTime": end_time,
            "type": sensor_type,
        }
        result = self._request("GET", "/statistics/sensorInfos", params=params)
        return result.get("data", {})

    def get_elec_stats(
        self,
        house_no: str,
        record_type: int,
        start_time: str,
        end_time: str,
        device_no: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取电量统计

        Args:
            house_no: 房屋编号
            record_type: 记录类型 (1=年，2=月，3=日，4=小时)
            start_time: 开始时间
            end_time: 结束时间
            device_no: 设备编号（可选，不传则获取房屋总用电量）
        """
        params = {
            "houseNo": house_no,
            "recordType": record_type,
            "startTime": start_time,
            "endTime": end_time,
        }
        if device_no:
            params["deviceNo"] = device_no
        result = self._request("GET", "/statistics/elecInfos", params=params)
        return result.get("data", {})

    def clear_cache(self):
        """清除设备缓存"""
        try:
            from cache import clear
            clear()
        except ImportError:
            pass

    def verify_credentials(self) -> bool:
        """验证凭证"""
        try:
            self.access_token="credentials_test"
            result = self._request_no_check_result("GET", "/house/infos")
            code = result.get("code", "")
            if code == "10003" or code == "99001":
                return False
            return True
        except Exception:
            return False


if __name__ == "__main__":
    print("Duwi 智能家居 API 客户端")
    print("请在代码中配置 appkey 和 secret 后使用")
