# -*- coding: utf-8 -*-
"""
审计日志记录器

职责：
1. 记录所有操作轨迹（谁、什么时候、做了什么）
2. 支持多种输出目标（文件、stdout、远程API）
3. 结构化日志格式，便于查询和分析

设计思路：
- 日志即代码的"黑匣子"，必须可靠
- 结构化输出 > 文本输出，便于后续分析
- 敏感信息脱敏处理
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class AuditEntry:
    """审计日志条目"""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    module: str = ""      # 模块名 (vault, pipeline, wordpress)
    action: str = ""      # 动作 (get, set, request, error)
    actor: str = "system" # 操作者
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


class AuditLogger:
    """
    审计日志记录器
    
    特性：
    - 结构化JSON日志
    - 多输出目标
    - 敏感信息脱敏
    """
    
    def __init__(self, config):
        self.config = config
        self._outputs = []
        self._setup_outputs()
    
    def _setup_outputs(self):
        """初始化日志输出"""
        if not self.config.audit.enabled:
            return
        
        # 文件输出
        log_dir = Path(self.config.audit.log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"audit_{today}.jsonl"
        
        self._file_handle = open(log_file, "a", encoding="utf-8")
        self._outputs.append("file")
        
        # STDOUT输出 (debug模式)
        if self.config.audit.verbose or self.config.debug:
            self._outputs.append("stdout")
    
    def log(self, module: str, action: str, details: Dict[str, Any] = None, actor: str = "system"):
        """
        记录审计日志
        
        Args:
            module: 模块名
            action: 动作
            details: 详情
            actor: 操作者
        """
        entry = AuditEntry(
            module=module,
            action=action,
            actor=actor,
            details=self._sanitize(details or {})
        )
        
        # 输出到各个目标
        json_str = entry.to_json()
        
        if "file" in self._outputs and hasattr(self, "_file_handle"):
            self._file_handle.write(json_str + "\n")
            self._file_handle.flush()
        
        if "stdout" in self._outputs:
            print(f"[AUDIT] {json_str}")
    
    def _sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """脱敏处理 - 移除敏感信息"""
        sensitive_keys = {"password", "token", "secret", "key", "auth"}
        result = {}
        for k, v in data.items():
            if any(s in k.lower() for s in sensitive_keys):
                result[k] = "***REDACTED***"
            elif isinstance(v, dict):
                result[k] = self._sanitize(v)
            else:
                result[k] = v
        return result
    
    def query(self, module: Optional[str] = None, 
              action: Optional[str] = None,
              actor: Optional[str] = None,
              limit: int = 100) -> list[AuditEntry]:
        """
        查询审计日志
        
        TODO: 实现真正的日志查询
        """
        entries = []
        # 简化实现：读取最近的日志文件
        if hasattr(self, "_file_handle"):
            self._file_handle.flush()
        
        log_dir = Path(self.config.audit.log_dir)
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"audit_{today}.jsonl"
        
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry_data = json.loads(line.strip())
                        # 简单过滤
                        if module and entry_data.get("module") != module:
                            continue
                        if action and entry_data.get("action") != action:
                            continue
                        if actor and entry_data.get("actor") != actor:
                            continue
                        entries.append(AuditEntry(**entry_data))
                        if len(entries) >= limit:
                            break
                    except json.JSONDecodeError:
                        continue
        
        return entries
    
    def close(self):
        """关闭日志文件"""
        if hasattr(self, "_file_handle"):
            self._file_handle.close()
    
    def __del__(self):
        self.close()
