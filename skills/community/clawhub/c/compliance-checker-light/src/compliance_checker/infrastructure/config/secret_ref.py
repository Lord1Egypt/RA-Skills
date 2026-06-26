"""
SecretRef 配置解析模块

支持 OpenClaw 框架的 SecretRef 规范，用于安全管理敏感信息。
SecretRef 格式: { "source": "env" | "file" | "exec", "provider": "default", "id": "..." }

架构原则：
- SecretRef 解析属于 I/O 操作，归属于 Infrastructure 层
- Domain 层不直接导入 secret_ref，配置通过 Application 层注入
"""

import os
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, Union


@dataclass
class SecretRef:
    """
    SecretRef 配置对象
    
    Attributes:
        source: 密钥来源类型 ("env", "file", "exec")
        provider: 提供者名称
        id: 密钥标识符
    """
    source: str
    provider: str
    id: str
    
    def __post_init__(self):
        """验证 SecretRef 格式"""
        if self.source not in ("env", "file", "exec"):
            raise ValueError(f"Invalid source: {self.source}. Must be 'env', 'file', or 'exec'")
        
        # provider 必须匹配 ^[a-z][a-z0-9_-]{0,63}$
        if not self.provider or not self.provider[0].islower():
            raise ValueError(f"Invalid provider: {self.provider}. Must start with lowercase letter")
        
        if not all(c.isalnum() or c in '_-' for c in self.provider):
            raise ValueError(f"Invalid provider: {self.provider}. Must contain only alphanumeric, underscore, or hyphen")
        
        if len(self.provider) > 64:
            raise ValueError(f"Invalid provider: {self.provider}. Must be 64 characters or less")
        
        # id 验证
        if not self.id:
            raise ValueError("id cannot be empty")


class SecretRefResolver:
    """
    SecretRef 解析器
    
    支持三种来源：
    - env: 从环境变量读取
    - file: 从文件读取（支持 JSON 指针路径）
    - exec: 从外部命令执行结果读取
    """
    
    def __init__(self, providers: Optional[Dict[str, Any]] = None):
        """
        初始化解析器
        
        Args:
            providers: 提供者配置字典，格式为 {provider_name: provider_config}
        """
        self.providers = providers or {}
        self._cache: Dict[str, str] = {}
    
    def resolve(self, ref: Union[SecretRef, Dict[str, str], str]) -> Optional[str]:
        """
        解析 SecretRef 获取密钥值
        
        Args:
            ref: SecretRef 对象、字典或普通字符串
            
        Returns:
            解析后的密钥值，如果解析失败则返回 None
        """
        # 如果已经是普通字符串，直接返回
        if isinstance(ref, str):
            return ref
        
        # 转换为 SecretRef 对象
        if isinstance(ref, dict):
            try:
                ref = SecretRef(
                    source=ref.get("source", ""),
                    provider=ref.get("provider", "default"),
                    id=ref.get("id", "")
                )
            except ValueError as e:
                raise SecretRefError(f"Invalid SecretRef format: {e}")
        
        # 检查缓存
        cache_key = f"{ref.source}:{ref.provider}:{ref.id}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # 根据 source 类型解析
        if ref.source == "env":
            value = self._resolve_env(ref)
        elif ref.source == "file":
            value = self._resolve_file(ref)
        elif ref.source == "exec":
            value = self._resolve_exec(ref)
        else:
            raise SecretRefError(f"Unsupported source type: {ref.source}")
        
        # 缓存结果
        if value is not None:
            self._cache[cache_key] = value
        
        return value
    
    def _resolve_env(self, ref: SecretRef) -> Optional[str]:
        """
        从环境变量解析密钥
        
        Args:
            ref: SecretRef 对象
            
        Returns:
            环境变量值，未设置则返回 None
        """
        # id 必须匹配 ^[A-Z][A-Z0-9_]{0,127}$
        if not ref.id[0].isupper():
            raise SecretRefError(f"Env ref id must start with uppercase letter: {ref.id}")
        
        if not all(c.isupper() or c.isdigit() or c == '_' for c in ref.id):
            raise SecretRefError(f"Env ref id must contain only uppercase letters, digits, or underscore: {ref.id}")
        
        if len(ref.id) > 128:
            raise SecretRefError(f"Env ref id must be 128 characters or less: {ref.id}")
        
        value = os.getenv(ref.id)
        if value is None or value == "":
            return None
        
        return value
    
    def _resolve_file(self, ref: SecretRef) -> Optional[str]:
        """
        从文件解析密钥
        
        Args:
            ref: SecretRef 对象，id 为 JSON 指针路径
            
        Returns:
            文件中的密钥值
        """
        # id 必须是绝对 JSON 指针路径 (/...)
        if not ref.id.startswith("/"):
            raise SecretRefError(f"File ref id must be an absolute JSON pointer path starting with '/': {ref.id}")
        
        # 获取提供者配置
        provider_config = self.providers.get(ref.provider, {})
        file_path = provider_config.get("path")
        
        if not file_path:
            raise SecretRefError(f"File provider '{ref.provider}' not configured or missing 'path'")
        
        # 展开路径中的 ~
        file_path = os.path.expanduser(file_path)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise SecretRefError(f"Secret file not found: {file_path}")
        
        mode = provider_config.get("mode", "json")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if mode == "singleValue":
                    # 单值模式，直接返回文件内容
                    if ref.id != "/value":
                        raise SecretRefError(f"SingleValue mode only supports '/value' as id: {ref.id}")
                    return f.read().strip()
                else:
                    # JSON 模式，解析 JSON 指针
                    data = json.load(f)
                    return self._get_json_pointer(data, ref.id)
        except json.JSONDecodeError as e:
            raise SecretRefError(f"Invalid JSON in secret file {file_path}: {e}")
        except Exception as e:
            raise SecretRefError(f"Failed to read secret file {file_path}: {e}")
    
    def _resolve_exec(self, ref: SecretRef) -> Optional[str]:
        """
        从外部命令执行结果解析密钥
        
        Args:
            ref: SecretRef 对象
            
        Returns:
            命令输出的密钥值
        """
        # id 必须匹配 ^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$
        if not ref.id[0].isalnum():
            raise SecretRefError(f"Exec ref id must start with alphanumeric character: {ref.id}")
        
        if not all(c.isalnum() or c in '._:/-' for c in ref.id):
            raise SecretRefError(f"Exec ref id contains invalid characters: {ref.id}")
        
        if len(ref.id) > 256:
            raise SecretRefError(f"Exec ref id must be 256 characters or less: {ref.id}")
        
        # 获取提供者配置
        provider_config = self.providers.get(ref.provider, {})
        command = provider_config.get("command")
        
        if not command:
            raise SecretRefError(f"Exec provider '{ref.provider}' not configured or missing 'command'")
        
        args = provider_config.get("args", [])
        pass_env = provider_config.get("passEnv", [])
        json_only = provider_config.get("jsonOnly", True)
        timeout = provider_config.get("timeout", 30)
        
        # 构建环境变量
        env = os.environ.copy()
        if pass_env:
            env = {k: v for k, v in env.items() if k in pass_env}
        
        try:
            if json_only:
                # JSON 协议模式
                request_payload = {
                    "protocolVersion": 1,
                    "provider": ref.provider,
                    "ids": [ref.id]
                }
                
                result = subprocess.run(
                    [command] + args,
                    input=json.dumps(request_payload),
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env
                )
                
                if result.returncode != 0:
                    raise SecretRefError(f"Exec provider returned non-zero exit code: {result.stderr}")
                
                response = json.loads(result.stdout)
                
                # 检查错误
                if "errors" in response and ref.id in response["errors"]:
                    error = response["errors"][ref.id]
                    raise SecretRefError(f"Exec provider error: {error.get('message', 'Unknown error')}")
                
                # 返回值
                if "values" in response and ref.id in response["values"]:
                    return response["values"][ref.id]
                
                raise SecretRefError(f"Exec provider did not return value for id: {ref.id}")
            
            else:
                # 纯文本模式
                result = subprocess.run(
                    [command] + args,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env
                )
                
                if result.returncode != 0:
                    raise SecretRefError(f"Exec provider returned non-zero exit code: {result.stderr}")
                
                return result.stdout.strip()
        
        except subprocess.TimeoutExpired:
            raise SecretRefError(f"Exec provider timed out after {timeout} seconds")
        except json.JSONDecodeError as e:
            raise SecretRefError(f"Invalid JSON response from exec provider: {e}")
        except Exception as e:
            raise SecretRefError(f"Failed to execute secret provider: {e}")
    
    def _get_json_pointer(self, data: Any, pointer: str) -> Optional[str]:
        """
        根据 JSON 指针路径获取值
        
        Args:
            data: JSON 数据对象
            pointer: JSON 指针路径 (如 "/providers/openai/apiKey")
            
        Returns:
            指针指向的值
        """
        if pointer == "/":
            return str(data) if not isinstance(data, (dict, list)) else None
        
        # 分割路径并处理转义
        # RFC6901: ~ => ~0, / => ~1
        parts = pointer[1:].split("/")
        
        current = data
        for part in parts:
            # 解码转义字符
            part = part.replace("~1", "/").replace("~0", "~")
            
            if isinstance(current, dict):
                if part not in current:
                    raise SecretRefError(f"JSON pointer path not found: {pointer}")
                current = current[part]
            elif isinstance(current, list):
                try:
                    index = int(part)
                    if index < 0 or index >= len(current):
                        raise SecretRefError(f"JSON pointer array index out of bounds: {part}")
                    current = current[index]
                except ValueError:
                    raise SecretRefError(f"Invalid JSON pointer array index: {part}")
            else:
                raise SecretRefError(f"Cannot traverse JSON pointer path: {pointer}")
        
        return str(current) if not isinstance(current, (dict, list)) else None


class SecretRefError(Exception):
    """SecretRef 解析错误"""
    pass


def parse_secret_ref(value: Union[str, Dict[str, str]]) -> Optional[SecretRef]:
    """
    解析 SecretRef 字符串或字典
    
    Args:
        value: SecretRef 字符串（JSON 格式）或字典
        
    Returns:
        SecretRef 对象，如果解析失败则返回 None
    """
    if isinstance(value, str):
        try:
            data = json.loads(value)
            if not isinstance(data, dict):
                return None
            return SecretRef(
                source=data.get("source", ""),
                provider=data.get("provider", "default"),
                id=data.get("id", "")
            )
        except (json.JSONDecodeError, ValueError):
            return None
    elif isinstance(value, dict):
        try:
            return SecretRef(
                source=value.get("source", ""),
                provider=value.get("provider", "default"),
                id=value.get("id", "")
            )
        except ValueError:
            return None
    return None


def resolve_secret(value: Union[str, Dict[str, str], SecretRef], 
                   providers: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """
    便捷函数：解析 SecretRef 或返回原值
    
    Args:
        value: SecretRef 对象、字典、JSON 字符串或普通字符串
        providers: 提供者配置
        
    Returns:
        解析后的密钥值
    """
    # 如果是普通字符串，先尝试解析为 SecretRef
    if isinstance(value, str):
        ref = parse_secret_ref(value)
        if ref is None:
            # 不是 SecretRef 格式，直接返回原值
            return value
        value = ref
    
    # 解析 SecretRef
    resolver = SecretRefResolver(providers)
    return resolver.resolve(value)
