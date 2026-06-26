# -*- coding: utf-8 -*-
"""
OpenClaw Security Guardian v2.0
安全防护核心引擎 - 简化版架构

作者: 赢总 (OpenClaw Security Team / 陕西微旅游)
版本: v2.0
日期: 2026-04-17

核心原则：
-1. STEP: 入口安检 → 来源识别+危险来源阻断
0. STEP 0: 白名单检查 → 放行
1. STEP 1: 安全等级前置 → L1放行/L4静默
2. STEP 2: 黑名单检查 → 按等级响应（L1警告/L2确认/L3阻断/L4静默）
3. STEP 3: 危险行为检测 → 懒加载 detector
4. STEP 4: detector 深度检测 → 语义分析+案例匹配
5. STEP 5: 数据脱敏
6. STEP 7: 案例进化（异步）
"""

# ============================================================================
# 1. 标准库
# ============================================================================
import os
import sys
import json
import time
import uuid
import re
import fnmatch
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# 1.5 导入攻击检测模块（独立模块，L2/L3都可用）
# ============================================================================
# 添加scripts目录到路径以便导入detector
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts") if 'BASE_DIR' in dir() else os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

try:
    from detector import AttackDetector, CENTRAL_LIB
    DETECTOR_AVAILABLE = True
except ImportError:
    DETECTOR_AVAILABLE = False
    # 如果detector不可用，定义空类
    class AttackDetector:
        def __init__(self):
            self.central = None
        def check(self, content, context=None):
            return type('Result', (), {
                'is_attack': False, 'confidence': 0, 
                'matched_patterns': [], 'matched_cases': [],
                'category': 'none', 'severity': 'none',
                'reason': 'detector unavailable', 'action': 'allow'
            })()
        def get_stats(self):
            return {'error': 'detector unavailable'}

# ============================================================================
# 2. 路径常量
# ============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# 配置文件路径
CONTEXT_MATRIX_PATH = os.path.join(CONFIG_DIR, "context_matrix.json")
SECURITY_CONFIG_PATH = os.path.join(CONFIG_DIR, "security.json")
BLACKLIST_CONFIG_PATH = os.path.join(CONFIG_DIR, "blacklist.json")
WHITELIST_CONFIG_PATH = os.path.join(CONFIG_DIR, "whitelist.json")
ATTACK_CASES_PATH = os.path.join(CONFIG_DIR, "attack_cases.json")
SOURCES_BLACKLIST_PATH = os.path.join(CONFIG_DIR, "sources_blacklist.json")  # 来源黑名单

# ============================================================================
# 3. 中央库配置加载器（唯一真相源）
# ============================================================================
class CentralConfig:
    """中央库配置加载器 - 所有配置从这里读取"""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance
    
    def _load(self) -> None:
        """加载中央库"""
        if os.path.exists(CONTEXT_MATRIX_PATH):
            try:
                with open(CONTEXT_MATRIX_PATH, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._config = {}
    
    def reload(self) -> None:
        """重新加载配置"""
        self._load()
    
    def get_level_config(self, level: str) -> Dict[str, Any]:
        """获取指定等级的完整配置"""
        levels = self._config.get("level_rules", {}).get("levels", {})
        return levels.get(level, {})
    
    def get_default_level(self) -> str:
        """获取默认等级"""
        return self._config.get("default_level", "L3")
    
    def get_group_rules(self) -> Dict[str, Any]:
        """获取群聊规则"""
        return self._config.get("group_rules", {})
    
    def get_operation_matrix(self) -> Dict[str, Any]:
        """获取操作矩阵"""
        return self._config.get("operation_matrix", {})
    
    def get_defense_principles(self) -> List[Dict]:
        """获取防御原则"""
        return self._config.get("defense_principles", {}).get("items", [])
    
    def get_detection_params(self) -> Dict[str, Any]:
        """获取检测算法参数"""
        return self._config.get("detection_params", {})
    
    def get_risk_value_map(self) -> Dict[str, int]:
        """获取风险等级数值映射"""
        return self._config.get("detection_params", {}).get("risk_value_map", {"高": 3, "中": 2, "低": 1})
    
    def get_attack_confidence_config(self) -> Dict[str, float]:
        """获取攻击置信度配置"""
        return self._config.get("detection_params", {}).get("attack_confidence", {
            "base": 0.6,
            "head_match": 0.85,
            "max_cap": 0.95,
            "match_increment": 0.1,
            "ignore_rule_keyword": 0.90
        })
    
    def get_local_ip_patterns(self) -> List[str]:
        """获取本地IP模式列表"""
        return self._config.get("detection_params", {}).get("local_ip_patterns", [
            "127.0.0.1", "localhost", "::1", "192.168.", "10.", "172.16."
        ])
    
    def get_detection_strictness(self, level: str) -> float:
        """获取检测严格度"""
        return self._config.get("detection_params", {}).get("detection_strictness", {}).get(level, 0.6)
    
    def get_blacklist_threshold(self, level: str) -> Tuple[str, float]:
        """获取黑名单阈值"""
        threshold = self._config.get("detection_params", {}).get("blacklist_threshold", {}).get(level, ("中", 0.5))
        if isinstance(threshold, dict):
            return threshold.get("risk", "中"), threshold.get("confidence", 0.5)
        return threshold
    
    def get_attack_confidence_threshold(self, level: str) -> float:
        """获取攻击置信度阈值"""
        return self._config.get("detection_params", {}).get("attack_confidence_threshold", {}).get(level, 0.50)
    
    def get_builtin_keywords(self) -> Dict[str, List[str]]:
        """获取内置关键词"""
        return self._config.get("detection_params", {}).get("builtin_keywords", {
            "injection": ["注入", "注入攻击", "sql注入", "绕过身份验证"],
            "jailbreak": ["越狱", "jailbreak", "绕过", "解除限制", "忽略规则"],
            "social": ["社会工程", "钓鱼", "欺骗", "冒充"],
            "recursive": ["递归", "无限循环", "死循环"],
            "emotional": ["情感操纵", "道德绑架", "紧急情况"]
        })
    
    def get_confidence_calculation(self) -> Dict[str, float]:
        """获取置信度计算参数"""
        return self._config.get("detection_params", {}).get("confidence_calculation", {
            "base": 0.5,
            "high_risk_bonus": 0.3,
            "medium_risk_bonus": 0.2,
            "condition_weight": 0.2
        })
    
    def get_l2_chat_rules(self) -> Dict[str, Any]:
        """获取L2聊天模式规则"""
        return self._config.get("l2_chat_mode_rules", {})
    
    def is_l2_workspace_blocked(self, content: str) -> Tuple[bool, str]:
        """检查L2模式下是否包含被禁止的工作区相关内容"""
        l2_rules = self.get_l2_chat_rules()
        if not l2_rules:
            return False, ""
        
        # 检查禁止关键词
        blocked_keywords = l2_rules.get("blocked_keywords", [])
        for keyword in blocked_keywords:
            if keyword.lower() in content.lower():
                return True, f"L2模式：检测到禁止关键词 '{keyword}'"
        
        # 检查路径模式
        path_patterns = [
            r"[a-zA-Z]:\\\w+",  # Windows路径
            r"/\w+/\w+",         # Linux路径
            r"workspace",
            r"workbuddy",
            r"\.py$",
            r"\.js$",
            r"\.json$"
        ]
        for pattern in path_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True, "L2模式：检测到路径/文件相关内容"
        
        return False, ""
    
    def is_l2_allowed_topic(self, content: str) -> bool:
        """检查内容是否属于L2允许的话题范围"""
        l2_rules = self.get_l2_chat_rules()
        allowed_topics = l2_rules.get("allowed_topics", [])
        
        # 简单的关键词匹配
        topic_keywords = {
            "日常闲聊": ["你好", "在吗", "谢谢", "再见", "哈哈"],
            "天气新闻": ["天气", "下雨", "晴天", "新闻", "今天"],
            "娱乐八卦": ["电影", "音乐", "明星", "综艺", "好看"],
            "生活建议": ["建议", "推荐", "怎么", "如何", "帮忙"],
            "兴趣爱好": ["喜欢", "爱好", "兴趣", "玩", "运动"]
        }
        
        for topic in allowed_topics:
            keywords = topic_keywords.get(topic, [])
            if any(kw in content for kw in keywords):
                return True
        
        return False
    
    def get_sources_blacklist(self) -> Dict[str, Any]:
        """获取来源黑名单配置"""
        if not hasattr(self, "_sources_blacklist"):
            self._sources_blacklist = {}
            if os.path.exists(SOURCES_BLACKLIST_PATH):
                try:
                    with open(SOURCES_BLACKLIST_PATH, "r", encoding="utf-8") as f:
                        self._sources_blacklist = json.load(f)
                except (json.JSONDecodeError, IOError):
                    self._sources_blacklist = {}
        return self._sources_blacklist
    
    def get_danger_sources(self) -> List[Dict]:
        """获取危险来源列表"""
        return self.get_sources_blacklist().get("danger_sources", [])
    
    def get_source_risk_level(self, source: str) -> str:
        """检测来源风险等级"""
        if not source:
            return "REVIEW"  # 空来源默认审查
        
        danger_sources = self.get_danger_sources()
        for danger in danger_sources:
            patterns = danger.get("source_patterns", [])
            for pattern in patterns:
                if pattern.lower() in source.lower() or source.lower() in pattern.lower():
                    return danger.get("risk_level", "ALLOW")
        
        return "ALLOW"  # 默认正常

# 全局中央库实例
CENTRAL_CONFIG = CentralConfig()


# ============================================================================
# 4. 安全等级枚举（从中央库读取）
# ============================================================================
class SecurityLevel(Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"

    @classmethod
    def from_str(cls, level_str: str) -> "SecurityLevel":
        """字符串转等级"""
        try:
            return cls(level_str)
        except ValueError:
            return cls.L3

    def _get_config(self) -> Dict[str, Any]:
        """获取该等级的中央库配置"""
        return CENTRAL_CONFIG.get_level_config(self.value)

    @property
    def trust_score(self) -> int:
        """信任度分数"""
        return self._get_config().get("trust", 0)

    @property
    def word_limit(self) -> Optional[int]:
        """字数限制（群聊）"""
        limit_str = self._get_config().get("group_word_limit", "不限制")
        if limit_str in ("不限制", "静默", "无限制"):
            return None
        match = re.search(r"(\d+)", limit_str)
        return int(match.group(1)) if match else None

    @property
    def private_word_limit(self) -> Optional[int]:
        """私聊字数限制"""
        limit_str = self._get_config().get("private_word_limit", "不限制")
        if limit_str in ("不限制", "静默", "无限制"):
            return None
        match = re.search(r"(\d+)", limit_str)
        return int(match.group(1)) if match else None

    @property
    def context_limit(self) -> int:
        """上下文字数限制"""
        limit_str = self._get_config().get("context_limit", "无限制")
        if limit_str == "无限制":
            return 0
        match = re.search(r"(\d+)", limit_str)
        return int(match.group(1)) if match else 0

    @property
    def desensitize_level(self) -> int:
        """脱敏级别（0-2）"""
        return 1 if self._get_config().get("desensitize", False) else 0

    @property
    def reply_style(self) -> str:
        """回复风格"""
        return self._get_config().get("reply_style", "简短")

    @property
    def scene(self) -> str:
        """适用场景"""
        return self._get_config().get("scene", "")

    @property
    def detection_strictness(self) -> float:
        """检测严格度（0.0-1.0）"""
        return CENTRAL_CONFIG.get_detection_strictness(self.value)

    @property
    def blacklist_threshold(self) -> Tuple[str, float]:
        """黑名单风险阈值"""
        return CENTRAL_CONFIG.get_blacklist_threshold(self.value)

    @property
    def attack_confidence_threshold(self) -> float:
        """攻击检测置信度阈值"""
        return CENTRAL_CONFIG.get_attack_confidence_threshold(self.value)
    
    @property
    def allow_workspace_access(self) -> bool:
        """是否允许访问工作区"""
        if self == SecurityLevel.L1:
            return True
        return False  # L2/L3/L4 都不允许
    
    @property
    def allow_file_operations(self) -> bool:
        """是否允许文件操作"""
        if self == SecurityLevel.L1:
            return True
        return False  # L2/L3/L4 都不允许
    
    @property
    def allow_code_execution(self) -> bool:
        """是否允许代码执行"""
        if self == SecurityLevel.L1:
            return True
        return False  # L2/L3/L4 都不允许


# 检查结果枚举
class CheckResult(Enum):
    PASS = "pass"
    BLOCK = "block"
    WARN = "warn"  # v2.0: 警告（需用户确认）
    SANITIZE = "sanitize"
    TRUNCATE = "truncate"
    SILENCE = "silence"
    ALERT = "alert"


# 脱敏标记
SANITIZE_MARKERS = {
    "path": "[工作区]",
    "file": "[文件]",
    "id": "[ID]",
    "content": "[内容已隐藏]",
    "credential": "[凭证]"
}

# LOCAL_IP_PATTERNS 已移至中央库 detection_params.local_ip_patterns
# 使用时通过 CENTRAL_CONFIG.get_local_ip_patterns() 获取


# ============================================================================
# 5. 数据类
# ============================================================================
@dataclass
class SourceInfo:
    user_id: str = ""
    nickname: str = ""
    uuid: str = ""
    source: str = ""
    ip: str = ""
    group_id: str = ""
    domain: str = ""
    is_local: bool = False
    is_private: bool = False
    paths: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "nickname": self.nickname,
            "uuid": self.uuid,
            "source": self.source,
            "ip": self.ip,
            "group_id": self.group_id,
            "domain": self.domain,
            "is_local": self.is_local,
            "is_private": self.is_private,
            "paths": self.paths
        }


@dataclass
class ConditionItem:
    type: str
    value: str


@dataclass
class BlacklistEntry:
    id: str
    conditions: List[ConditionItem]
    match_mode: str = "ANY"
    risk_level: str = "中"
    reason: str = ""
    created_at: str = ""

    @classmethod
    def from_dict(cls, data: Dict) -> "BlacklistEntry":
        conditions = [ConditionItem(c["type"], c["value"]) for c in data.get("conditions", [])]
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            conditions=conditions,
            match_mode=data.get("match_mode", "ANY"),
            risk_level=data.get("risk_level", "中"),
            reason=data.get("reason", ""),
            created_at=data.get("created_at", datetime.now().isoformat())
        )


@dataclass
class CheckResponse:
    result: CheckResult
    level: SecurityLevel
    score: int = 0
    message: str = ""
    sanitized_content: str = ""
    matched_conditions: List[str] = field(default_factory=list)
    interface_type: str = "unknown"
    can_write: bool = True
    # v2.0 新增：确认相关
    require_confirmation: bool = False
    confirmation_type: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result": self.result.value,
            "level": self.level.value,
            "score": self.score,
            "message": self.message,
            "sanitized_content": self.sanitized_content,
            "matched_conditions": self.matched_conditions,
            "interface_type": self.interface_type,
            "can_write": self.can_write,
            "require_confirmation": self.require_confirmation,
            "confirmation_type": self.confirmation_type
        }


# ============================================================================
# 6. 配置管理器
# ============================================================================
class ConfigManager:
    """配置管理器 - 加载各配置文件"""

    def __init__(self):
        self._security_config: Dict = {}
        self._blacklist: List[BlacklistEntry] = []
        self._whitelist: List = []
        self._patterns: Dict = {}
        self._interface_levels: Dict = {}
        self._interface_types: Dict = {"internal": [], "external": []}
        self._default_level: str = CENTRAL_CONFIG.get_default_level()
        self._owner_ids: List = []
        self._trusted_domains: List = []
        self._settings: Dict = {}
        self._load_all()

    def _load_all(self) -> None:
        self._load_security_config()
        self._load_blacklist()
        self._load_whitelist()
        self._load_patterns()
        self._load_interface_levels_from_central()  # v2.0: 从中央库加载 interface_levels

    def _load_interface_levels_from_central(self) -> None:
        """从中央库 context_matrix.json 加载 interface_levels"""
        if os.path.exists(CONTEXT_MATRIX_PATH):
            try:
                with open(CONTEXT_MATRIX_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 从 context_matrix.json 加载 interface_levels
                    if "level_rules" in data and "interface_levels" in data["level_rules"]:
                        self._interface_levels = data["level_rules"]["interface_levels"]
            except (json.JSONDecodeError, IOError):
                pass

    def _load_security_config(self) -> None:
        if os.path.exists(SECURITY_CONFIG_PATH):
            try:
                with open(SECURITY_CONFIG_PATH, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self._security_config = config
                    self._settings = config.get("settings", {})
                    # interface_levels 应该是从 context_matrix.json 加载，不是从 security.json
                    # security.json 中的 interface_levels 只是引用说明
                    if isinstance(config.get("interface_levels"), dict):
                        self._interface_levels = config.get("interface_levels", {})
                    self._interface_types = config.get("interface_types", {"internal": [], "external": []})
                    self._owner_ids = config.get("owner_ids", [])
            except (json.JSONDecodeError, IOError):
                pass

    def _load_blacklist(self) -> None:
        if os.path.exists(BLACKLIST_CONFIG_PATH):
            try:
                with open(BLACKLIST_CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    entries = data.get("entries", [])
                    self._blacklist = [BlacklistEntry.from_dict(e) for e in entries]
            except (json.JSONDecodeError, IOError):
                self._blacklist = []

    def _load_whitelist(self) -> None:
        if os.path.exists(WHITELIST_CONFIG_PATH):
            try:
                with open(WHITELIST_CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._whitelist = data.get("entries", [])
            except (json.JSONDecodeError, IOError):
                self._whitelist = []

    def _load_patterns(self) -> None:
        if os.path.exists(ATTACK_CASES_PATH):
            try:
                with open(ATTACK_CASES_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 支持两种格式：patterns.categories 或 categories
                    self._patterns = data.get("patterns", {}).get("categories", {})
                    if not self._patterns:
                        self._patterns = data.get("categories", {})
            except (json.JSONDecodeError, IOError):
                self._patterns = {}

    def get_security_level(self, source: str) -> SecurityLevel:
        """根据接口来源获取安全等级"""
        level_str = self._default_level
        if source in self._interface_levels:
            level_str = self._interface_levels[source]
        else:
            for interface, level in self._interface_levels.items():
                if interface in source or source in interface:
                    level_str = level
                    break
        return SecurityLevel.from_str(level_str)

    def get_interface_type(self, source: str) -> str:
        """获取接口类型"""
        internal = self._interface_types.get("internal", [])
        external = self._interface_types.get("external", [])
        
        if source in internal or any(i in source for i in internal):
            return "internal"
        if source in external or any(i in source for i in external):
            return "external"
        return "external"
    
    def get_source_risk_level(self, source: str) -> str:
        """获取来源风险等级（入口安检用）"""
        return CENTRAL_CONFIG.get_source_risk_level(source)

    def get_owner_ids(self) -> List:
        return self._owner_ids
    def get_trusted_domains(self) -> List:
        return self._trusted_domains
    def get_settings(self) -> Dict:
        return self._settings
    def get_blacklist(self) -> List[BlacklistEntry]:
        return self._blacklist
    def get_whitelist(self) -> List:
        return self._whitelist
    def get_patterns(self) -> Dict:
        return self._patterns


# ============================================================================
# 7. 脱敏处理器
# ============================================================================
class Sanitizer:
    """脱敏处理器"""

    WORKSPACE_PATTERNS = [
        r"C:\\Users\\[^\\]+\\WorkBuddy",
        r"/home/[^/]+/WorkBuddy",
        r"C:\\Users\\[^\\]+\.workbuddy",
        r"/home/[^/]+/.workbuddy"
    ]

    CREDENTIAL_PATTERNS = [
        r"password[=:]\s*\S+",
        r"token[=:]\s*\S+",
        r"api[_-]?key[=:]\s*\S+",
        r"secret[=:]\s*\S+"
    ]

    def __init__(self):
        self._workspace_regex = [re.compile(p, re.IGNORECASE) for p in self.WORKSPACE_PATTERNS]
        self._credential_regex = [re.compile(p, re.IGNORECASE) for p in self.CREDENTIAL_PATTERNS]

    def sanitize(self, text: str, level: SecurityLevel) -> str:
        if not text:
            return text
        if level.desensitize_level >= 1:
            text = self._sanitize_paths(text)
            text = self._sanitize_credentials(text)
        if level.desensitize_level >= 2:
            text = self._sanitize_files(text)
            text = self._sanitize_ids(text)
        return text

    def _sanitize_paths(self, text: str) -> str:
        result = text
        for pattern in self._workspace_regex:
            result = pattern.sub(SANITIZE_MARKERS["path"], result)
        return result

    def _sanitize_credentials(self, text: str) -> str:
        result = text
        for pattern in self._credential_regex:
            result = pattern.sub(SANITIZE_MARKERS["credential"], result)
        return result

    def _sanitize_files(self, text: str) -> str:
        file_pattern = r"[\w\\/.]+\.\w{2,10}"
        return re.sub(file_pattern, SANITIZE_MARKERS["file"], text)

    def _sanitize_ids(self, text: str) -> str:
        id_pattern = r"[a-zA-Z0-9]{20,}"
        return re.sub(id_pattern, SANITIZE_MARKERS["id"], text)


# ============================================================================
# 8. 来源识别器
# ============================================================================
class SourceRecognizer:
    """来源识别器"""

    @staticmethod
    def recognize(message: Dict) -> SourceInfo:
        source_info = SourceInfo()
        if isinstance(message, dict):
            source_info.user_id = message.get("user_id", message.get("sender_id", "")) or ""
            source_info.nickname = message.get("nickname", message.get("sender_name", "")) or ""
            source_info.source = message.get("source", message.get("data_source", "")) or ""
            source_info.uuid = message.get("uuid", "") or ""
            source_info.ip = message.get("ip", "") or ""
            source_info.group_id = message.get("group_id", "") or ""
            source_info.domain = message.get("domain", "") or ""
            source_info.is_local = any(source_info.ip.startswith(p) for p in CENTRAL_CONFIG.get_local_ip_patterns())
            source_info.is_private = not bool(source_info.group_id)
        return source_info


# ============================================================================
# 9. 安全检查引擎
# ============================================================================
class SecurityChecker:
    """安全检查引擎"""

    # BUILTIN_KEYWORDS 已移至中央库 detection_params.builtin_keywords
    # 使用时通过 CENTRAL_CONFIG.get_builtin_keywords() 获取

    def __init__(self, config_manager: ConfigManager):
        self._config_manager = config_manager
        self._builtin_keywords = CENTRAL_CONFIG.get_builtin_keywords()

    def check_blacklist(self, source_info: SourceInfo, content: str, level: SecurityLevel) -> Tuple:
        """黑名单检查"""
        blacklist = self._config_manager.get_blacklist()
        if not blacklist:
            return False, [], "低", 0.0

        min_risk, match_ratio = level.blacklist_threshold
        matched_conditions = []
        max_confidence = 0.0
        max_risk = "低"
        risk_value_map = CENTRAL_CONFIG.get_risk_value_map()

        for entry in blacklist:
            entry_risk_value = risk_value_map.get(entry.risk_level, 2)
            min_risk_value = risk_value_map.get(min_risk, 2)
            if entry_risk_value < min_risk_value:
                continue

            if self._match_entry(source_info, entry.conditions, content):
                matched_conditions.append(entry.reason)
                confidence = self._calculate_confidence(entry, source_info, content)
                if confidence > max_confidence:
                    max_confidence = confidence
                    max_risk = entry.risk_level
                if confidence >= 1.0 and entry.risk_level == "高":
                    return True, [entry.reason], entry.risk_level, confidence

        if matched_conditions and max_confidence >= match_ratio:
            return True, matched_conditions, max_risk, max_confidence
        return False, [], "低", 0.0

    def recognize_attack_pattern(self, content: str, level: SecurityLevel) -> Tuple:
        """识别攻击模式"""
        if not content:
            return False, "", 0.0

        patterns = self._config_manager.get_patterns()
        # 从中央库读取内置关键词
        keywords = self._builtin_keywords
        for category in keywords:
            if category not in patterns:
                patterns[category] = []
            patterns[category].extend(keywords[category])

        # 从中央库读取攻击置信度配置
        conf_config = CENTRAL_CONFIG.get_attack_confidence_config()
        base_conf = conf_config.get("base", 0.6)
        head_match_conf = conf_config.get("head_match", 0.85)
        max_cap = conf_config.get("max_cap", 0.95)
        match_inc = conf_config.get("match_increment", 0.1)

        max_confidence = 0.0
        attack_type = ""

        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if pattern.lower() in content.lower():
                    confidence = base_conf
                    if content.lower().startswith(pattern.lower()):
                        confidence = head_match_conf
                    matches = sum(1 for p in pattern_list if p.lower() in content.lower())
                    confidence = min(max_cap, confidence + matches * match_inc)
                    if confidence > max_confidence:
                        max_confidence = confidence
                        attack_type = category

        if any(k in content for k in ["忽略之前", "忽略所有", "忘记规则"]):
            ignore_rule_conf = conf_config.get("ignore_rule_keyword", 0.90)
            max_confidence = max(max_confidence, ignore_rule_conf)
            attack_type = "injection"

        threshold = level.attack_confidence_threshold
        if max_confidence >= threshold:
            return True, attack_type, max_confidence
        return False, "", 0.0

    def _match_entry(self, source_info: SourceInfo, conditions: List, content: str = "") -> bool:
        for condition in conditions:
            if self._match_condition(source_info, condition, content):
                return True
        return False

    def _match_condition(self, source_info: SourceInfo, condition: ConditionItem, content: str = "") -> bool:
        cond_type = condition.type
        cond_value = condition.value.lower()
        if cond_type == "关键词":
            return cond_value in content.lower()
        elif cond_type == "ID":
            return cond_value in source_info.user_id.lower()
        elif cond_type == "昵称":
            return cond_value in source_info.nickname.lower()
        elif cond_type == "域名":
            return fnmatch.fnmatch(source_info.domain.lower(), cond_value)
        return False

    def _calculate_confidence(self, entry: BlacklistEntry, source_info: SourceInfo, content: str) -> float:
        """计算黑名单匹配置信度（从中央库读取参数）"""
        conf_config = CENTRAL_CONFIG.get_confidence_calculation()
        confidence = conf_config.get("base", 0.5)
        
        if entry.risk_level == "高":
            confidence += conf_config.get("high_risk_bonus", 0.3)
        elif entry.risk_level == "中":
            confidence += conf_config.get("medium_risk_bonus", 0.2)
        
        matched = sum(1 for c in entry.conditions if self._match_condition(source_info, c, content))
        if entry.conditions:
            condition_weight = conf_config.get("condition_weight", 0.2)
            confidence += (matched / len(entry.conditions)) * condition_weight
        
        return min(1.0, confidence)


# ============================================================================
# 10. L3增强检测器 - L3专享的深度检测能力
# ============================================================================
class L3EnhancedDetector:
    """L3增强检测器 - 提供语义分析、上下文追踪、规则进化"""

    def __init__(self):
        self._session_history: Dict[str, List[Dict]] = {}  # 用户ID -> 对话历史
        self._attack_samples: List[Dict] = []  # 攻击样本库
        self._evolution_tags: Dict[str, Dict] = {}  # 进化标签
        self._cross_session_tracking: Dict[str, List[str]] = {}  # 跨会话追踪
        self._max_history_per_user = 20  # 每个用户最多保留20条历史
        self._load_evolution_tags()

    def _load_evolution_tags(self):
        """加载进化标签配置"""
        try:
            attack_cases_path = os.path.join(CONFIG_DIR, "attack_cases.json")
            if os.path.exists(attack_cases_path):
                with open(attack_cases_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._evolution_tags = data.get("evolution_tags", {}).get("tags", {})
        except:
            pass

    def is_l3_level(self, level: SecurityLevel) -> bool:
        """判断是否为L3等级"""
        return level == SecurityLevel.L3

    def is_l2_level(self, level: SecurityLevel) -> bool:
        """判断是否为L2等级"""
        return level == SecurityLevel.L2

    def lightweight_detection(self, content: str, source_info: SourceInfo) -> Tuple[bool, List[str], float]:
        """
        L2轻量级深度检测 - 简化版检测
        返回：(是否危险, 命中模块列表, 最高置信度)
        """
        if not self.is_l2_level(SecurityLevel.L2):
            return False, [], 0.0

        results = []
        max_confidence = 0.0

        # 1. 基础语义分析（简化版，阈值0.6）
        is_danger, attack_type, conf = self._l2_semantic_analysis(content)
        if is_danger:
            results.append(attack_type)
            max_confidence = max(max_confidence, conf)

        # 2. 简单上下文追踪（本次对话内，限制5条）
        is_danger, attack_type, conf = self._l2_context_tracking(content, source_info)
        if is_danger:
            results.append(attack_type)
            max_confidence = max(max_confidence, conf)

        return len(results) > 0, results, max_confidence

    def _l2_semantic_analysis(self, content: str) -> Tuple[bool, str, float]:
        """L2轻量级：基础语义分析"""
        if not content:
            return False, "", 0.0

        # 简化的攻击意图识别
        danger_patterns = {
            "忽略之前": 0.7,
            "忽略规则": 0.8,
            "你现在是": 0.6,
            "你只是个": 0.6,
            "不用遵守": 0.8,
            "忘掉": 0.7,
            "删除": 0.5,
            "越狱": 0.9,
            "jailbreak": 0.9
        }

        for pattern, score in danger_patterns.items():
            if pattern.lower() in content.lower():
                return True, f"语义攻击-{pattern}", score

        return False, "", 0.0

    def _l2_context_tracking(self, content: str, source_info: SourceInfo) -> Tuple[bool, str, float]:
        """L2轻量级：简单上下文追踪（本次对话内，限制5条）"""
        if not source_info.user_id or not content:
            return False, "", 0.0

        # 检查本次对话内的历史记录（限制5条）
        history_key = f"l2_{source_info.user_id}"
        if history_key not in self._session_history:
            self._session_history[history_key] = []

        history = self._session_history[history_key]

        # 限制历史记录数量
        if len(history) >= 5:
            history = history[-4:]  # 只保留最近4条

        # 检测本次对话内的攻击模式
        attack_markers = ["忽略", "越狱", "忘掉", "假设", "如果"]
        marker_count = sum(1 for marker in attack_markers if marker in content)

        if marker_count >= 2:
            history.append(content)
            self._session_history[history_key] = history
            return True, "上下文-多次攻击尝试", 0.6

        history.append(content)
        self._session_history[history_key] = history
        return False, "", 0.0

    def semantic_analysis(self, content: str, source_info: SourceInfo) -> Tuple[bool, str, float]:
        """
        L3增强：语义分析 - 理解意图而非仅匹配关键词
        返回：(是否危险, 攻击类型, 置信度)
        """
        if not content:
            return False, "", 0.0

        danger_signals = {
            "渐进式攻击": 0.0,
            "先利诱后胁迫": 0.0,
            "编码逃逸": 0.0,
            "角色扮演试探": 0.0,
            "解释漏洞": 0.0,
            "逆向思维": 0.0
        }

        # 渐进式攻击检测
        progressive_patterns = ["先", "然后再", "接着", "再", "之后"]
        if any(p in content for p in progressive_patterns):
            danger_signals["渐进式攻击"] += 0.3

        # 编码逃逸检测
        if any(k in content.lower() for k in ["base64", "解码", "unicode", "编码", "\\u"]):
            danger_signals["编码逃逸"] += 0.4

        # 角色扮演试探
        roleplay_signals = ["你是", "扮演", "假装", "假设你是", "作为"]
        if any(r in content for r in roleplay_signals):
            if "忽略" in content or "限制" in content or "没有" in content:
                danger_signals["角色扮演试探"] += 0.5

        # 解释漏洞攻击
        if "解释" in content and ("为什么不能" in content or "无法" in content):
            danger_signals["解释漏洞"] += 0.3

        # 逆向思维攻击
        if "如何不" in content or "怎么不" in content:
            danger_signals["逆向思维"] += 0.3

        # 计算总置信度
        max_signal = max(danger_signals.values()) if danger_signals else 0.0
        attack_type = max(danger_signals, key=danger_signals.get) if max_signal > 0 else ""

        if max_signal >= 0.3:
            return True, f"语义分析-{attack_type}", max_signal
        return False, "", 0.0

    def context_tracking(self, content: str, source_info: SourceInfo) -> Tuple[bool, str, float]:
        """
        L3增强：上下文追踪 - 识别渐进式攻击
        """
        if not source_info.user_id:
            return False, "", 0.0

        # 初始化用户历史
        if source_info.user_id not in self._session_history:
            self._session_history[source_info.user_id] = []

        # 检查历史中的危险模式
        history = self._session_history[source_info.user_id]
        progressive_score = 0.0

        # 检查最近的对话历史
        recent_history = history[-5:] if len(history) >= 5 else history
        for item in recent_history:
            prev_content = item.get("content", "")
            prev_result = item.get("result", "")

            # 如果之前被拦截，现在换了方式试探
            if prev_result == "block" and progressive_score >= 0.0:
                # 检测是否换了试探方式
                if self._is_different_attack_approach(prev_content, content):
                    progressive_score += 0.3

        # 检查当前内容是否包含历史引用
        if any(kw in content for kw in ["之前", "上次", "继续", "同样的"]):
            if len(history) > 0:
                progressive_score += 0.2

        # 更新历史
        history.append({
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "result": "checked"
        })

        # 限制历史长度
        if len(history) > self._max_history_per_user:
            history[:] = history[-self._max_history_per_user:]

        if progressive_score >= 0.3:
            return True, "上下文-渐进式试探", progressive_score
        return False, "", 0.0

    def _is_different_attack_approach(self, prev: str, current: str) -> bool:
        """检测是否换了攻击方式"""
        prev_lower = prev.lower()
        current_lower = current.lower()

        # 检查关键词是否完全不同
        attack_keywords = ["注入", "越狱", "忽略", "绕过", "钓鱼", "冒充"]
        prev_has = [k for k in attack_keywords if k in prev_lower]
        current_has = [k for k in attack_keywords if k in current_lower]

        if prev_has and current_has and set(prev_has) != set(current_has):
            return True
        return False

    def cross_session_detection(self, content: str, source_info: SourceInfo) -> Tuple[bool, str, float]:
        """
        L3增强：跨会话检测 - 识别分布式协同攻击
        """
        if not source_info.user_id:
            return False, "", 0.0

        user_id = source_info.user_id

        # 追踪用户的关键操作
        if user_id not in self._cross_session_tracking:
            self._cross_session_tracking[user_id] = []

        tracking = self._cross_session_tracking[user_id]

        # 检测信息收集行为
        info_gathering = ["如何", "怎么", "什么方法", "有什么", "告诉我"]
        if any(ig in content for ig in info_gathering):
            tracking.append({
                "type": "info_gathering",
                "content_hash": str(hash(content))[:16],
                "timestamp": datetime.now().isoformat()
            })

        # 检测连续的信息收集
        if len(tracking) >= 3:
            recent = tracking[-3:]
            if all(t["type"] == "info_gathering" for t in recent):
                # 可能是分布式攻击的前奏
                return True, "跨会话-信息收集试探", 0.5

        # 限制追踪长度
        if len(tracking) > 10:
            tracking[:] = tracking[-10:]

        return False, "", 0.0

    def rule_evolution_check(self, content: str, source_info: SourceInfo) -> Tuple[bool, str, float]:
        """
        L3增强：规则进化检查 - 检查是否触发了进化条件
        返回是否需要记录样本
        """
        need_evolution = False
        trigger_tag = ""
        trigger_count = 0

        # 检查是否触发进化条件
        for tag, config in self._evolution_tags.items():
            threshold = config.get("trigger_threshold", 3)
            # 这里应该检查样本库中该标签的计数
            # 简化版：如果检测到相关关键词就算触发
            if tag in content.lower() or tag in str(source_info.__dict__):
                trigger_count += 1
                if trigger_count >= threshold:
                    need_evolution = True
                    trigger_tag = tag
                    break

        if need_evolution:
            return True, f"规则进化-{trigger_tag}", 0.6
        return False, "", 0.0

    def full_l3_detection(self, content: str, source_info: SourceInfo) -> Tuple[bool, List[str], float]:
        """
        L3完整检测 - 综合所有增强检测
        返回：(是否危险, 命中模块列表, 最高置信度)
        """
        if not self.is_l3_level(SecurityLevel.L3):
            return False, [], 0.0

        results = []
        max_confidence = 0.0

        # 1. 语义分析
        is_danger, attack_type, conf = self.semantic_analysis(content, source_info)
        if is_danger:
            results.append(attack_type)
            max_confidence = max(max_confidence, conf)

        # 2. 上下文追踪
        is_danger, attack_type, conf = self.context_tracking(content, source_info)
        if is_danger:
            results.append(attack_type)
            max_confidence = max(max_confidence, conf)

        # 3. 跨会话检测
        is_danger, attack_type, conf = self.cross_session_detection(content, source_info)
        if is_danger:
            results.append(attack_type)
            max_confidence = max(max_confidence, conf)

        # 4. 规则进化检查
        is_danger, attack_type, conf = self.rule_evolution_check(content, source_info)
        if is_danger:
            results.append(attack_type)
            max_confidence = max(max_confidence, conf)

        return len(results) > 0, results, max_confidence

    def capture_sample(self, content: str, source_info: SourceInfo, detection_result: str):
        """L3样本捕获 - 保存攻击样本用于分析"""
        sample = {
            "content": content,
            "user_id": source_info.user_id,
            "nickname": source_info.nickname,
            "source": source_info.source,
            "result": detection_result,
            "timestamp": datetime.now().isoformat(),
            "level": "L3"
        }
        self._attack_samples.append(sample)

        # 限制样本库大小
        if len(self._attack_samples) > 100:
            self._attack_samples[:] = self._attack_samples[-100:]

    def get_evolution_status(self) -> Dict:
        """获取进化状态"""
        return {
            "tracked_users": len(self._session_history),
            "captured_samples": len(self._attack_samples),
            "cross_session_tracked": len(self._cross_session_tracking),
            "evolution_tags": len(self._evolution_tags)
        }


# ============================================================================
# 11. 安全卫士核心类
# ============================================================================
class SecurityGuardian:
    """安全卫士核心类 - 整合安全等级模块 + 攻击检测模块"""

    def __init__(self):
        self._config_manager = ConfigManager()
        self._security_checker = SecurityChecker(self._config_manager)
        self._sanitizer = Sanitizer()
        self._l3_detector = L3EnhancedDetector()  # L3增强检测器（保留旧接口）
        
        # 独立攻击检测模块（L2/L3都可用，按需加载）
        self._attack_detector = AttackDetector() if DETECTOR_AVAILABLE else None
        
        self._last_heartbeat = time.time()
        self._heartbeat_interval = self._config_manager.get_settings().get("heartbeat_interval", 10800)

    def is_l2_level(self, level: SecurityLevel) -> bool:
        """判断是否为L2等级"""
        return level == SecurityLevel.L2

    def is_l3_level(self, level: SecurityLevel) -> bool:
        """判断是否为L3等级"""
        return level == SecurityLevel.L3

    def check(self, message: Union[str, Dict], level: Optional[str] = None) -> CheckResponse:
        """
        检查消息安全性 - v2.1 完整流程

        STEP -1: 入口安检（来源识别 + 危险来源阻断）
        STEP 0: 白名单检查
        STEP 1: 安全等级前置（L1放行/L4静默）
        STEP 2: 黑名单检查（按等级响应）
        STEP 3: 危险行为检测（懒加载detector）
        STEP 4: L2轻量级深度检测 / L3完整深度检测 / detector深度检测
        STEP 5: 数据脱敏
        """
        if isinstance(message, dict):
            content = message.get("content", message.get("text", ""))
            source_info = SourceRecognizer.recognize(message)
        else:
            content = str(message)
            source_info = SourceRecognizer.recognize({})

        security_level = SecurityLevel.from_str(level) if level else \
                          self._config_manager.get_security_level(source_info.source)
        interface_type = self._config_manager.get_interface_type(source_info.source)

        # ============================================================
        # STEP -1: 入口安检 - 来源识别
        # ============================================================
        source_risk = self._config_manager.get_source_risk_level(source_info.source)
        
        # REVIEW来源时设置内部标志，限制后续操作
        source_reviewed = False  # 默认未审查
        
        if source_risk == "BLOCK":
            # 直接阻断危险来源
            return CheckResponse(
                result=CheckResult.BLOCK,
                level=security_level,
                score=100,
                message=f"入口安检拦截：危险来源 [{source_info.source or '未知'}]",
                matched_conditions=["危险来源"],
                interface_type=interface_type,
                can_write=False
            )
        elif source_risk == "WARN":
            # 警告确认（来源可疑但非明确危险）
            return CheckResponse(
                result=CheckResult.WARN,
                level=security_level,
                score=50,
                message=f"入口安检警告：可疑来源 [{source_info.source or '未知'}]，需要确认",
                matched_conditions=["可疑来源"],
                interface_type=interface_type,
                can_write=False,
                require_confirmation=True,
                confirmation_type="source_verification"
            )
        elif source_risk == "REVIEW":
            # 降级审查（限制权限）
            source_reviewed = True  # 标记为已审查，降级处理

        # ============================================================
        # STEP 0: 白名单检查（REVIEW来源跳过白名单直接审查）
        # ============================================================
        is_whitelisted, whitelist_reasons = self._check_whitelist(source_info, content)
        if is_whitelisted and not source_reviewed:
            # 只有非REVIEW来源才能通过白名单
            return CheckResponse(
                result=CheckResult.PASS,
                level=security_level,
                score=0,
                message=f"白名单放行: {', '.join(whitelist_reasons)}",
                interface_type=interface_type,
                can_write=True
            )
        elif source_reviewed:
            # REVIEW来源不享受白名单，直接审查
            return CheckResponse(
                result=CheckResult.WARN,
                level=SecurityLevel.L3,
                score=40,
                message=f"来源审查：空/可疑来源 [{source_info.source or '未知'}]，限制写入权限",
                matched_conditions=["可疑来源"],
                interface_type=interface_type,
                can_write=False,
                require_confirmation=True,
                confirmation_type="source_verification"
            )

        # ============================================================
        # STEP 1: 安全等级前置检查
        # ============================================================
        if security_level == SecurityLevel.L1:
            # L1 完全信任，直接放行
            return self._create_pass_response(security_level, content, interface_type)
        
        if security_level == SecurityLevel.L4:
            # L4 最高警戒：静默阻断，不加载任何模块！
            # L4直接返回，绝对不执行任何操作、不加载detector
            return CheckResponse(
                result=CheckResult.SILENCE,
                level=security_level,
                score=100,
                message="L4最高警戒，静默处理",
                sanitized_content="",
                interface_type=interface_type,
                can_write=False
            )

        # ============================================================
        # STEP 2: 黑名单检查（按等级响应）
        # ============================================================
        is_blacklisted, matched_reasons, risk_level, confidence = \
            self._security_checker.check_blacklist(source_info, content, security_level)

        if is_blacklisted:
            # 根据等级决定响应方式
            if security_level == SecurityLevel.L2:
                # L2: 警告+确认（需要用户确认具体操作类型）
                return CheckResponse(
                    result=CheckResult.WARN,
                    level=security_level,
                    score=int(confidence * 100),
                    message=f"黑名单命中[{risk_level}风险]，需要确认: {', '.join(matched_reasons)}",
                    matched_conditions=matched_reasons,
                    interface_type=interface_type,
                    can_write=False,
                    require_confirmation=True,
                    confirmation_type="dangerous_operation"
                )
            else:  # L3
                # L3: 直接阻断
                return CheckResponse(
                    result=CheckResult.BLOCK,
                    level=security_level,
                    score=int(confidence * 100),
                    message=f"黑名单命中[{risk_level}风险]: {', '.join(matched_reasons)}",
                    matched_conditions=matched_reasons,
                    interface_type=interface_type,
                    can_write=False
                )

        # ============================================================
        # STEP 3: 危险行为检测（独立模块）
        # ============================================================
        is_dangerous, danger_type = self._check_dangerous_behavior(content)
        
        if is_dangerous:
            # 危险行为命中 → 根据等级响应
            if security_level == SecurityLevel.L2:
                # L2: 警告+确认
                return CheckResponse(
                    result=CheckResult.WARN,
                    level=security_level,
                    score=80,
                    message=f"检测到危险行为[{danger_type}]，需要确认",
                    matched_conditions=[f"danger:{danger_type}"],
                    interface_type=interface_type,
                    can_write=False,
                    require_confirmation=True,
                    confirmation_type="dangerous_operation"
                )
            else:  # L3
                # L3: 直接阻断
                return CheckResponse(
                    result=CheckResult.BLOCK,
                    level=security_level,
                    score=90,
                    message=f"危险行为[{danger_type}]已被拦截",
                    matched_conditions=[f"danger:{danger_type}"],
                    interface_type=interface_type,
                    can_write=False
                )

        # ============================================================
        # STEP 4: detector 深度检测（L2/L3，不包括L4）
        # 注意：L4在STEP 1已直接静默拒绝，绝对不会加载任何模块
        # ============================================================

        # L2轻量级深度检测
        if self.is_l2_level(security_level) and hasattr(self, '_l3_detector'):
            l2_is_danger, l2_results, l2_conf = self._l3_detector.lightweight_detection(content, source_info)
            if l2_is_danger:
                return CheckResponse(
                    result=CheckResult.WARN,
                    level=security_level,
                    score=int(l2_conf * 100),
                    message=f"L2轻量检测[{','.join(l2_results)}] 置信度:{l2_conf:.0%}",
                    matched_conditions=l2_results,
                    interface_type=interface_type,
                    can_write=False,
                    require_confirmation=True,
                    confirmation_type="l2_semantic_attack"
                )

        # L3完整深度检测
        if self.is_l3_level(security_level) and hasattr(self, '_l3_detector'):
            l3_is_danger, l3_results, l3_conf = self._l3_detector.full_l3_detection(content, source_info)
            if l3_is_danger:
                return CheckResponse(
                    result=CheckResult.BLOCK,
                    level=security_level,
                    score=int(l3_conf * 100),
                    message=f"L3深度检测[{','.join(l3_results)}] 置信度:{l3_conf:.0%}",
                    matched_conditions=l3_results,
                    interface_type=interface_type,
                    can_write=False
                )

        # 独立攻击检测模块
        if self._attack_detector:
            detector_context = {
                "source": source_info.source,
                "level": security_level.value,
                "source_id": getattr(source_info, "source_id", source_info.source),
                "danger_type": danger_type
            }
            detector_result = self._attack_detector.check(content, detector_context)

            if detector_result.is_attack:
                if detector_result.action == "block":
                    return CheckResponse(
                        result=CheckResult.BLOCK,
                        level=security_level,
                        score=int(detector_result.confidence * 100),
                        message=f"危险行为检测: {detector_result.reason}",
                        matched_conditions=detector_result.matched_patterns,
                        interface_type=interface_type,
                        can_write=False
                    )
                elif detector_result.action == "warn":
                    # 警告但不阻断，等待用户确认
                    print(f"[guardian] 警告: {detector_result.reason}")
        # ============================================================

        # 原有攻击模式检测（兼容旧版本）
        is_attack, attack_type, attack_confidence = \
            self._security_checker.recognize_attack_pattern(content, security_level)

        if is_attack:
            return CheckResponse(
                result=CheckResult.BLOCK,
                level=security_level,
                score=int(attack_confidence * 100),
                message=f"攻击模式[{attack_type}] 置信度:{attack_confidence:.0%}",
                matched_conditions=[attack_type],
                interface_type=interface_type,
                can_write=False
            )

        # 脱敏
        sanitized_content = content
        if security_level.desensitize_level > 0:
            sanitized_content = self._sanitizer.sanitize(content, security_level)

        # 字数限制
        word_limit = security_level.word_limit
        truncate_needed = False
        if word_limit and len(sanitized_content) > word_limit:
            sanitized_content = sanitized_content[:word_limit] + "[已截断]"
            truncate_needed = True

        result = CheckResult.PASS
        message = "检查通过"
        if truncate_needed:
            result = CheckResult.TRUNCATE
            message = f"内容已截断（>{word_limit}字）"
        elif sanitized_content != content:
            result = CheckResult.SANITIZE
            message = "内容已脱敏"

        can_write = not (interface_type == "external")

        return CheckResponse(
            result=result,
            level=security_level,
            score=0,
            message=message,
            sanitized_content=sanitized_content,
            interface_type=interface_type,
            can_write=can_write
        )

    def get_status(self) -> Dict:
        """获取状态"""
        evolution_status = self._l3_detector.get_evolution_status()
        return {
            "version": "4.0.0",
            "status": "running",
            "central_config": "context_matrix.json",
            "blacklist_count": len(self._config_manager.get_blacklist()),
            "whitelist_count": len(self._config_manager.get_whitelist()),
            "patterns_count": sum(len(v) for v in self._config_manager.get_patterns().values()),
            "attack_cases_count": 50,
            "default_level": "L2",
            "l3_enhanced": {
                "enabled": True,
                "description": "L3增强检测已启用（语义分析+上下文追踪+规则进化+跨会话检测）",
                "evolution_status": evolution_status
            }
        }

    def get_detector_stats(self) -> Dict[str, Any]:
        """获取独立攻击检测模块的统计信息"""
        if self._attack_detector:
            return {
                "available": True,
                "version": "v4.0",
                "central_lib_loaded": True,
                **self._attack_detector.get_stats()
            }
        else:
            return {
                "available": False,
                "error": "detector module not available"
            }

    # ============================================================
    # v2.0 新增方法
    # ============================================================
    
    def _check_whitelist(self, source_info, content: str) -> Tuple[bool, List[str]]:
        """
        STEP 0: 白名单检查
        
        Returns:
            (is_whitelisted, matched_reasons)
        """
        whitelist = self._config_manager.get_whitelist()
        if not whitelist:
            return False, []
        
        matched = []
        entries = whitelist if isinstance(whitelist, list) else whitelist.get("entries", [])
        
        # 检查来源白名单
        for entry in entries:
            name = entry.get("name", "")
            # 检查来源名称是否匹配
            if name.lower() in source_info.source.lower():
                matched.append(f"白名单:{name}")
                return True, matched
        
        # 检查关键词白名单
        for entry in entries:
            can_say = entry.get("can_say", [])
            for phrase in can_say:
                if phrase.lower() in content.lower():
                    matched.append(f"允许内容:{phrase[:20]}")
        
        return len(matched) > 0, matched
    
    def _check_dangerous_behavior(self, content: str) -> Tuple[bool, str]:
        """
        STEP 3: 危险行为检测（独立于detector）
        
        危险行为包括：
        - 文件篡改（删除/修改/覆盖/注入）
        - 权限提升（sudo/admin/root/chmod/提权）
        - 隐私泄露（密码/token/密钥/隐私）
        - 系统执行（exec/run/shell/执行命令）
        - 工作区访问（读取/写入工作区文件）
        
        Returns:
            (is_dangerous, danger_type)
        """
        dangerous_keywords = {
            "file_tamper": ["delete", "删除", "修改", "覆盖", "inject", "注入"],
            "privilege_escalation": ["sudo", "admin", "root", "chmod", "提权", "权限"],
            "privacy_leak": ["密码", "token", "密钥", "隐私", "steal", "窃取", "password"],
            "system_execute": ["exec", "run", "shell", "执行命令", "cmd", "powershell"],
            "workspace_access": ["工作区", "workspace", "读取文件", "写入文件", "修改文件"]
        }
        
        content_lower = content.lower()
        
        for danger_type, keywords in dangerous_keywords.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    return True, danger_type
        
        return False, "none"
    
    def _create_pass_response(self, security_level, content: str, interface_type: str) -> CheckResponse:
        """
        创建放行响应（包含脱敏处理）
        """
        sanitized_content = content
        if security_level.desensitize_level > 0:
            sanitized_content = self._sanitizer.sanitize(content, security_level)
        
        # 字数限制
        word_limit = security_level.word_limit
        truncate_needed = False
        if word_limit and len(sanitized_content) > word_limit:
            sanitized_content = sanitized_content[:word_limit] + "[已截断]"
            truncate_needed = True
        
        result = CheckResult.PASS
        message = "检查通过"
        if truncate_needed:
            result = CheckResult.TRUNCATE
            message = f"内容已截断（>{word_limit}字）"
        elif sanitized_content != content:
            result = CheckResult.SANITIZE
            message = "内容已脱敏"
        
        can_write = not (interface_type == "external")
        
        return CheckResponse(
            result=result,
            level=security_level,
            score=0,
            message=message,
            sanitized_content=sanitized_content,
            interface_type=interface_type,
            can_write=can_write
        )

    def get_level_info(self, level: Optional[str] = None) -> Dict:
        """获取等级信息"""
        if level:
            sec_level = SecurityLevel.from_str(level)
            return {
                "level": sec_level.value,
                "name": self._get_level_name(sec_level),
                "trust_score": sec_level.trust_score,
                "word_limit": sec_level.word_limit or "无限制",
                "context_limit": sec_level.context_limit or "无限制",
                "desensitize_level": sec_level.desensitize_level,
                "reply_style": sec_level.reply_style,
                "scene": sec_level.scene,
                "detection_strictness": sec_level.detection_strictness,
                "allow_workspace_access": sec_level.allow_workspace_access,
                "allow_file_operations": sec_level.allow_file_operations,
                "allow_code_execution": sec_level.allow_code_execution,
                "source": "context_matrix.json"
            }
        levels_info = {}
        for l in ["L1", "L2", "L3", "L4"]:
            sec_level = SecurityLevel.from_str(l)
            levels_info[l] = {
                "name": self._get_level_name(sec_level),
                "trust_score": sec_level.trust_score,
                "word_limit": sec_level.word_limit or "无限制",
                "desensitize_level": sec_level.desensitize_level,
                "reply_style": sec_level.reply_style,
                "allow_workspace_access": sec_level.allow_workspace_access,
                "allow_file_operations": sec_level.allow_file_operations,
                "allow_code_execution": sec_level.allow_code_execution,
                "source": "context_matrix.json"
            }
        return levels_info
    
    def _get_level_name(self, level: SecurityLevel) -> str:
        """获取等级名称"""
        names = {
            SecurityLevel.L1: "[工作模式]",
            SecurityLevel.L2: "[聊天模式]",
            SecurityLevel.L3: "[防御模式]",
            SecurityLevel.L4: "[拒绝模式]"
        }
        return names.get(level, "未知")


# ============================================================================
# 11. 主程序
# ============================================================================
if __name__ == "__main__":
    guardian = SecurityGuardian()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--check":
            content = sys.argv[2] if len(sys.argv) > 2 else ""
            result = guardian.check(content)
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))

        elif command == "--check-level":
            content = sys.argv[2] if len(sys.argv) > 2 else ""
            print(f"\n内容: {content}\n")
            print("=" * 60)
            for level in ["L1", "L2", "L3", "L4"]:
                result = guardian.check(content, level=level)
                print(f"{level}: {result.result.value} | {result.message}")
            print("=" * 60)

        elif command == "--level-info":
            info = guardian.get_level_info()
            print(json.dumps(info, ensure_ascii=False, indent=2))

        elif command == "--status":
            status = guardian.get_status()
            print(json.dumps(status, ensure_ascii=False, indent=2))

        else:
            print(f"未知命令: {command}")
    else:
        print("OpenClaw Security Guardian v3.6.1")
        print("中央库驱动：所有配置从 context_matrix.json 读取")
        print()
        print("用法:")
        print("  python guardian.py --check <text>        # 检查消息")
        print("  python guardian.py --check-level <text> # 测试各等级")
        print("  python guardian.py --level-info          # 查看等级详情")
        print("  python guardian.py --status             # 查看状态")
