#!/usr/bin/env python3
"""
OpenClaw Configuration JSON Schema Definition
对齐 OpenClaw 官方发布的 JSON 语法，用于语法检查和验证

基于 OpenClaw 2026.4.1 版本的 runtime-schema 定义
"""

from typing import Dict, Any, List, Optional, Union
import re

# =============================================================================
# OpenClaw JSON Schema 定义 (对齐官方发布)
# =============================================================================

# Agent Identity Schema
AGENT_IDENTITY_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "theme": {"type": "string"},
        "emoji": {"type": "string"},
        "avatar": {"type": "string"}
    }
}

# Subagents Schema
SUBAGENTS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "allowAgents": {
            "type": "array",
            "items": {"type": "string"}
        },
        "maxConcurrent": {
            "type": "integer",
            "exclusiveMinimum": 0
        },
        "model": {
            "anyOf": [
                {"type": "string"},
                {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "primary": {"type": "string"},
                        "fallbacks": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            ]
        },
        "thinking": {"type": "string"},
        "requireAgentId": {"type": "boolean"}
    }
}

# Model Config Schema
MODEL_CONFIG_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "primary": {"type": "string"},
        "fallbacks": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

# Agent List Item Schema
AGENT_LIST_ITEM_SCHEMA = {
    "type": "object",
    "required": ["id"],
    "additionalProperties": False,
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "default": {"type": "boolean"},
        "name": {"type": "string"},
        "workspace": {"type": "string"},
        "agentDir": {"type": "string"},
        "model": {
            "anyOf": [
                {"type": "string"},
                MODEL_CONFIG_SCHEMA
            ]
        },
        "thinkingDefault": {
            "type": "string",
            "enum": ["off", "minimal", "low", "medium", "high", "xhigh", "adaptive"]
        },
        "reasoningDefault": {
            "type": "string",
            "enum": ["on", "off", "stream"]
        },
        "fastModeDefault": {"type": "boolean"},
        "skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "identity": AGENT_IDENTITY_SCHEMA,
        "subagents": SUBAGENTS_SCHEMA
    }
}

# Agents Config Schema
AGENTS_CONFIG_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "defaults": {
            "type": "object",
            "additionalProperties": True,  # 允许额外属性如 compaction, models
            "properties": {
                "model": {
                    "anyOf": [
                        {"type": "string"},
                        MODEL_CONFIG_SCHEMA
                    ]
                },
                "models": {
                    "type": "object",
                    "additionalProperties": True  # 允许 model 特定配置
                },
                "workspace": {"type": "string"},
                "repoRoot": {"type": "string"},
                "maxConcurrent": {
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "subagents": {
                    "type": "object",
                    "additionalProperties": True,
                    "properties": {
                        "maxConcurrent": {
                            "type": "integer",
                            "exclusiveMinimum": 0
                        }
                    }
                },
                "compaction": {"type": "object"},
                "thinkingDefault": {"type": "string"},
                "reasoningDefault": {"type": "string"},
                "fastModeDefault": {"type": "boolean"},
                "verboseDefault": {"type": "string"},
                "elevatedDefault": {"type": "string"},
                "llm": {"type": "object"},
                "memorySearch": {"type": "object"},
                "contextPruning": {"type": "object"},
                "sandbox": {"type": "object"},
                "params": {"type": "object"},
                "tools": {"type": "object"}
            }
        },
        "list": {
            "type": "array",
            "items": AGENT_LIST_ITEM_SCHEMA
        }
    }
}

# Meta Schema
META_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "lastTouchedVersion": {"type": "string"},
        "lastTouchedAt": {"type": "string"}
    }
}

# Auth Profile Schema
AUTH_PROFILE_SCHEMA = {
    "type": "object",
    "required": ["provider", "mode"],
    "additionalProperties": False,
    "properties": {
        "provider": {"type": "string"},
        "mode": {
            "type": "string",
            "enum": ["api_key", "oauth", "token"]
        },
        "email": {"type": "string"},
        "displayName": {"type": "string"}
    }
}

# Auth Schema
AUTH_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "profiles": {
            "type": "object",
            "additionalProperties": AUTH_PROFILE_SCHEMA
        }
    }
}

# Model Provider Schema
MODEL_PROVIDER_SCHEMA = {
    "type": "object",
    "required": ["baseUrl", "models"],
    "additionalProperties": False,
    "properties": {
        "baseUrl": {"type": "string", "minLength": 1},
        "apiKey": {"type": "string"},
        "api": {"type": "string"},
        "auth": {"type": "string"},
        "authHeader": {"type": "boolean"},
        "models": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name"],
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "name": {"type": "string", "minLength": 1},
                    "api": {"type": "string"},
                    "reasoning": {"type": "boolean"},
                    "input": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["text", "image", "audio"]
                        }
                    },
                    "cost": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "input": {"type": "number"},
                            "output": {"type": "number"},
                            "cacheRead": {"type": "number"},
                            "cacheWrite": {"type": "number"}
                        }
                    },
                    "contextWindow": {"type": "number"},
                    "maxTokens": {"type": "number"}
                }
            }
        }
    }
}

# Models Schema
MODELS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "mode": {
            "type": "string",
            "enum": ["merge", "replace"]
        },
        "providers": {
            "type": "object",
            "additionalProperties": MODEL_PROVIDER_SCHEMA
        }
    }
}

# Gateway Schema
GATEWAY_SCHEMA = {
    "type": "object",
    "additionalProperties": True,  # 允许额外属性
    "properties": {
        "port": {"type": "integer"},
        "mode": {"type": "string"},
        "bind": {"type": "string"},
        "auth": {
            "type": "object",
            "additionalProperties": True,
            "properties": {
                "mode": {"type": "string"},
                "token": {"type": "string"}
            }
        },
        "controlUi": {"type": "object"},
        "remote": {"type": "object"},
        "tailscale": {"type": "object"},
        "push": {"type": "object"}
    }
}

# Tools Schema
TOOLS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "profile": {
            "type": "string",
            "enum": ["minimal", "coding", "messaging", "full"]
        },
        "allow": {
            "type": "array",
            "items": {"type": "string"}
        },
        "deny": {
            "type": "array",
            "items": {"type": "string"}
        },
        "agentToAgent": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "enabled": {"type": "boolean"},
                "allow": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "exec": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "host": {
                    "type": "string",
                    "enum": ["auto", "sandbox", "gateway", "node"]
                },
                "security": {"type": "string"},
                "ask": {"type": "string"}
            }
        }
    }
}

# Skills Schema
SKILLS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "install": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "nodeManager": {"type": "string"}
            }
        },
        "entries": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean"}
                }
            }
        }
    }
}

# Plugins Schema
PLUGINS_SCHEMA = {
    "type": "object",
    "additionalProperties": True,  # 允许额外属性
    "properties": {
        "entries": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean"}
                }
            }
        },
        "installs": {"type": "object"}  # 插件安装信息
    }
}

# Main OpenClaw Config Schema
OPENCLAW_CONFIG_SCHEMA = {
    "type": "object",
    "additionalProperties": True,  # 允许额外的顶层属性
    "properties": {
        "meta": META_SCHEMA,
        "auth": AUTH_SCHEMA,
        "models": MODELS_SCHEMA,
        "agents": AGENTS_CONFIG_SCHEMA,
        "tools": TOOLS_SCHEMA,
        "gateway": GATEWAY_SCHEMA,
        "skills": SKILLS_SCHEMA,
        "plugins": PLUGINS_SCHEMA,
        "channels": {"type": "object"},
        "wizard": {"type": "object"},
        "acp": {"type": "object"},
        "messages": {"type": "object"},
        "commands": {"type": "object"},
        "session": {"type": "object"},
        "hooks": {"type": "object"},
        "env": {"type": "object"},
        "diagnostics": {"type": "object"},
        "logging": {"type": "object"},
        "cron": {"type": "object"},
        "talk": {"type": "object"},
        "audio": {"type": "object"}
    }
}


# =============================================================================
# 非法命名元素检查规则
# =============================================================================

# 保留字列表 (OpenClaw 内部使用)
RESERVED_KEYWORDS = {
    # OpenClaw 核心保留字
    "openclaw", "config", "settings", "default", "system", "internal",
    "__proto__", "constructor", "prototype", "toString", "valueOf",
    # 可能冲突的 JavaScript/Python 关键字
    "null", "undefined", "true", "false", "NaN", "Infinity",
    "class", "function", "var", "let", "const", "return", "if", "else",
    "for", "while", "do", "switch", "case", "break", "continue", "try",
    "catch", "finally", "throw", "new", "this", "super", "extends",
    "import", "export", "default", "async", "await", "yield"
}

# Agent ID 命名规则
AGENT_ID_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]*$')
AGENT_ID_MAX_LENGTH = 64

# 非法字符模式
ILLEGAL_CHARACTERS_PATTERN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


class OpenClawSchemaValidator:
    """OpenClaw JSON Schema 验证器"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证 OpenClaw 配置
        
        Returns:
            {"valid": bool, "errors": [], "warnings": []}
        """
        self.errors = []
        self.warnings = []
        
        # 1. 验证基本结构
        self._validate_type(config, "root", OPENCLAW_CONFIG_SCHEMA)
        
        # 2. 验证 agents 配置
        if "agents" in config:
            self._validate_agents(config["agents"])
        
        # 3. 验证 models 配置
        if "models" in config:
            self._validate_models(config["models"])
        
        # 4. 验证非法命名元素
        self._validate_naming(config)
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors.copy(),
            "warnings": self.warnings.copy()
        }
    
    def _validate_type(self, value: Any, path: str, schema: Dict[str, Any]) -> bool:
        """验证值类型是否符合 schema"""
        schema_type = schema.get("type")
        
        if schema_type == "object":
            if not isinstance(value, dict):
                self.errors.append(f"'{path}' 必须是对象类型")
                return False
            
            # 检查 additionalProperties
            additional = schema.get("additionalProperties")
            if additional is False:
                allowed = set(schema.get("properties", {}).keys())
                actual = set(value.keys())
                illegal = actual - allowed
                if illegal:
                    self.errors.append(f"'{path}' 包含非法属性: {sorted(illegal)}")
            
            # 验证 properties
            properties = schema.get("properties", {})
            for key, prop_schema in properties.items():
                if key in value:
                    self._validate_type(value[key], f"{path}.{key}", prop_schema)
            
            # 验证 required
            required = schema.get("required", [])
            for key in required:
                if key not in value:
                    self.errors.append(f"'{path}' 缺少必需属性: '{key}'")
            
            return True
        
        elif schema_type == "array":
            if not isinstance(value, list):
                self.errors.append(f"'{path}' 必须是数组类型")
                return False
            
            items_schema = schema.get("items")
            if items_schema:
                for i, item in enumerate(value):
                    self._validate_type(item, f"{path}[{i}]", items_schema)
            
            return True
        
        elif schema_type == "string":
            if not isinstance(value, str):
                self.errors.append(f"'{path}' 必须是字符串类型")
                return False
            
            # 检查 minLength
            min_len = schema.get("minLength")
            if min_len is not None and len(value) < min_len:
                self.errors.append(f"'{path}' 长度不能小于 {min_len}")
            
            # 检查 enum
            enum = schema.get("enum")
            if enum is not None and value not in enum:
                self.errors.append(f"'{path}' 值必须是其中之一: {enum}")
            
            return True
        
        elif schema_type == "integer":
            if not isinstance(value, int) or isinstance(value, bool):
                self.errors.append(f"'{path}' 必须是整数类型")
                return False
            
            # 检查范围
            minimum = schema.get("minimum")
            if minimum is not None and value < minimum:
                self.errors.append(f"'{path}' 不能小于 {minimum}")
            
            exclusive_min = schema.get("exclusiveMinimum")
            if exclusive_min is not None and value <= exclusive_min:
                self.errors.append(f"'{path}' 必须大于 {exclusive_min}")
            
            return True
        
        elif schema_type == "boolean":
            if not isinstance(value, bool):
                self.errors.append(f"'{path}' 必须是布尔类型")
                return False
            return True
        
        elif schema_type == "number":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                self.errors.append(f"'{path}' 必须是数字类型")
                return False
            return True
        
        # anyOf 处理
        if "anyOf" in schema:
            for sub_schema in schema["anyOf"]:
                # 创建临时验证器来测试
                temp_validator = OpenClawSchemaValidator()
                temp_validator._validate_type(value, path, sub_schema)
                if not temp_validator.errors:
                    return True
            # 如果所有 anyOf 都不匹配，记录错误
            self.errors.append(f"'{path}' 不符合 anyOf 中的任何一个类型")
            return False
        
        return True
    
    def _validate_agents(self, agents: Dict[str, Any]) -> None:
        """验证 agents 配置"""
        if not isinstance(agents, dict):
            self.errors.append("'agents' 必须是对象类型")
            return
        
        # 验证 list
        agent_list = agents.get("list", [])
        if not isinstance(agent_list, list):
            self.errors.append("'agents.list' 必须是数组类型")
            return
        
        # 检查重复的 agent ID
        seen_ids = set()
        for i, agent in enumerate(agent_list):
            if not isinstance(agent, dict):
                self.errors.append(f"'agents.list[{i}]' 必须是对象类型")
                continue
            
            agent_id = agent.get("id")
            if agent_id:
                if agent_id in seen_ids:
                    self.errors.append(f"重复的 agent ID: '{agent_id}'")
                seen_ids.add(agent_id)
                
                # 验证 agent ID 命名
                self._validate_agent_id(agent_id, f"agents.list[{i}].id")
    
    def _validate_agent_id(self, agent_id: str, path: str) -> None:
        """验证 agent ID 是否合法"""
        # 检查长度
        if len(agent_id) > AGENT_ID_MAX_LENGTH:
            self.errors.append(f"'{path}' 长度不能超过 {AGENT_ID_MAX_LENGTH} 字符")
        
        # 检查命名规则
        if not AGENT_ID_PATTERN.match(agent_id):
            self.errors.append(
                f"'{path}' ('{agent_id}') 命名不合法: "
                f"必须以字母开头，只能包含字母、数字、连字符(-)和下划线(_)"
            )
        
        # 检查保留字
        if agent_id.lower() in RESERVED_KEYWORDS:
            self.errors.append(f"'{path}' ('{agent_id}') 是保留字，不能使用")
        
        # 检查非法字符
        if ILLEGAL_CHARACTERS_PATTERN.search(agent_id):
            self.errors.append(f"'{path}' ('{agent_id}') 包含非法字符")
    
    def _validate_models(self, models: Dict[str, Any]) -> None:
        """验证 models 配置"""
        if not isinstance(models, dict):
            self.errors.append("'models' 必须是对象类型")
            return
        
        providers = models.get("providers", {})
        if not isinstance(providers, dict):
            self.errors.append("'models.providers' 必须是对象类型")
            return
        
        # 检查 provider 命名
        for provider_name in providers.keys():
            if not re.match(r'^[a-z][a-z0-9_-]*$', provider_name):
                self.warnings.append(
                    f"Provider 名称 '{provider_name}' 建议使用小写字母开头，"
                    f"仅包含小写字母、数字、连字符和下划线"
                )
    
    def _validate_naming(self, config: Dict[str, Any], path: str = "") -> None:
        """
        递归验证所有键名是否合法
        """
        # 允许包含冒号的特定路径模式 (如 auth.profiles, models.providers)
        ALLOWED_COLON_PATHS = [
            "auth.profiles",
            "models.providers",
            "agents.defaults.models"
        ]
        
        if isinstance(config, dict):
            for key, value in config.items():
                current_path = f"{path}.{key}" if path else key
                
                # 检查是否允许冒号 (profile/provider 名称)
                allows_colon = any(current_path.startswith(allowed) for allowed in ALLOWED_COLON_PATHS)
                
                # 检查键名是否包含非法字符（根据上下文）
                if allows_colon:
                    # 允许冒号，但仍检查其他非法字符
                    test_key = key.replace(":", "").replace("/", "")
                else:
                    test_key = key
                
                if ILLEGAL_CHARACTERS_PATTERN.search(test_key):
                    self.errors.append(f"键名 '{current_path}' 包含非法字符")
                
                # 检查是否使用保留字作为键名（非 openclaw 标准属性）
                if key.lower() in RESERVED_KEYWORDS and key not in {
                    "default", "true", "false", "null", "enabled", "disabled"
                }:
                    self.warnings.append(f"键名 '{current_path}' 可能与系统保留字冲突")
                
                # 递归验证
                if isinstance(value, (dict, list)):
                    self._validate_naming(value, current_path)
        
        elif isinstance(config, list):
            for i, item in enumerate(config):
                current_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    self._validate_naming(item, current_path)
    
    def validate_agent_config(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证单个 agent 配置
        
        Returns:
            {"valid": bool, "errors": [], "warnings": []}
        """
        self.errors = []
        self.warnings = []
        
        self._validate_type(agent_config, "agent", AGENT_LIST_ITEM_SCHEMA)
        
        # 额外验证
        if "id" in agent_config:
            self._validate_agent_id(agent_config["id"], "id")
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors.copy(),
            "warnings": self.warnings.copy()
        }


# 全局验证器实例
_validator_instance: Optional[OpenClawSchemaValidator] = None


def get_validator() -> OpenClawSchemaValidator:
    """获取全局验证器实例"""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = OpenClawSchemaValidator()
    return _validator_instance


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    快捷函数：验证 OpenClaw 配置
    
    Returns:
        {"valid": bool, "errors": [], "warnings": []}
    """
    return get_validator().validate(config)


def validate_agent_config(agent_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    快捷函数：验证单个 agent 配置
    
    Returns:
        {"valid": bool, "errors": [], "warnings": []}
    """
    return get_validator().validate_agent_config(agent_config)


if __name__ == "__main__":
    # 测试验证器
    test_config = {
        "agents": {
            "list": [
                {
                    "id": "test-agent",
                    "name": "Test Agent",
                    "identity": {
                        "name": "测试助手",
                        "emoji": "🤖"
                    },
                    "subagents": {
                        "allowAgents": ["helper"],
                        "maxConcurrent": 4
                    }
                }
            ]
        }
    }
    
    result = validate_config(test_config)
    print("验证结果:", result)
