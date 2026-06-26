#!/usr/bin/env python3
"""
错误智慧库时效性管理模块 (Error Wisdom Timeliness Manager)

功能：
- 三重衰减机制：时间衰减、场景变化衰减、反例衰减
- 置信度动态计算
- 状态转换管理：active → deprecated → archived
- 周期性审计与清理

基于：error_wisdom_spec.md 规范
"""

import os
import json
import math
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== 枚举与数据结构 ====================

class TimelinessStatus(Enum):
    """时效性状态"""
    ACTIVE = "active"        # 置信度 > 0.7，正常使用
    DEPRECATED = "deprecated" # 置信度 0.3-0.7，仅作参考
    ARCHIVED = "archived"    # 置信度 < 0.3，存档不再使用


@dataclass
class DecayEvent:
    """衰减事件记录"""
    timestamp: str
    event_type: str         # time_decay / scene_change / counterexample
    confidence_before: float
    confidence_after: float
    reason: str
    details: Dict[str, Any]


@dataclass
class TimelinessMetadata:
    """时效性元数据"""
    current_confidence: float
    status: str
    base_confidence: float
    creation_time: str
    last_decay_check: str
    last_validation: str
    counterexample_count: int
    scene_changes_detected: int
    decay_events: List[Dict[str, Any]]


# ==================== 时效性管理器 ====================

class TimelinessManager:
    """
    时效性管理器
    
    实现错误智慧库的三重衰减机制：
    1. 时间衰减：自然过期，每日衰减1%
    2. 场景变化衰减：环境变化导致失效
    3. 反例衰减：预防策略失效
    """
    
    # 衰减参数
    TIME_DECAY_LAMBDA = 0.01      # 每天衰减1%
    SCENE_CHANGE_DECAY = 0.35     # 场景变化降低35%
    COUNTEREXAMPLE_DECAY = 0.30   # 每个反例降低30%
    
    # 状态阈值
    ACTIVE_THRESHOLD = 0.70
    DEPRECATED_THRESHOLD = 0.30
    
    # 审计周期（秒）
    AUDIT_INTERVAL = 86400  # 24小时
    
    def __init__(self, memory_dir: str = "./agi_memory"):
        """
        初始化
        
        Args:
            memory_dir: 记忆存储目录
        """
        self.memory_dir = memory_dir
        
        # 时效性状态文件
        self.timeliness_file = os.path.join(memory_dir, "error_wisdom_timeliness.json")
        
        # 加载时效性数据
        self.timeliness_data = self._load_timeliness_data()
        
        # 场景变更检测配置
        self.scene_change_events = []
        self.last_audit_time = time.time()
    
    def _load_timeliness_data(self) -> Dict[str, Any]:
        """加载时效性数据"""
        if os.path.exists(self.timeliness_file):
            try:
                with open(self.timeliness_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load timeliness data: {e}")
        
        return {
            "entries": {},          # entry_id -> TimelinessMetadata
            "metadata": {
                "last_audit": datetime.now().isoformat(),
                "total_active": 0,
                "total_deprecated": 0,
                "total_archived": 0
            }
        }
    
    def _save_timeliness_data(self):
        """保存时效性数据"""
        try:
            os.makedirs(os.path.dirname(self.timeliness_file), exist_ok=True)
            with open(self.timeliness_file, 'w', encoding='utf-8') as f:
                json.dump(self.timeliness_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save timeliness data: {e}")
    
    # ==================== 时间衰减 ====================
    
    def calculate_time_decay(
        self,
        base_confidence: float,
        creation_time: str
    ) -> Tuple[float, float]:
        """
        计算时间衰减
        
        公式：confidence = base * e^(-lambda * days)
        
        Args:
            base_confidence: 基础置信度
            creation_time: 创建时间（ISO格式）
        
        Returns:
            (衰减后置信度, 衰减天数)
        """
        try:
            creation_dt = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
            now = datetime.now(creation_dt.tzinfo) if creation_dt.tzinfo else datetime.now()
            days_since_creation = (now - creation_dt).days
        except:
            days_since_creation = 0
        
        decayed_confidence = base_confidence * math.exp(-self.TIME_DECAY_LAMBDA * days_since_creation)
        
        return decayed_confidence, days_since_creation
    
    # ==================== 场景变化衰减 ====================
    
    def register_scene_change(
        self,
        change_type: str,
        change_description: str,
        affected_patterns: List[str] = None
    ):
        """
        注册场景变化事件
        
        Args:
            change_type: 变化类型（knowledge_update / model_upgrade / tool_change / domain_shift）
            change_description: 变化描述
            affected_patterns: 受影响的错误模式ID列表
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "change_type": change_type,
            "description": change_description,
            "affected_patterns": affected_patterns or []
        }
        
        self.scene_change_events.append(event)
        
        # 对受影响的条目应用场景衰减
        if affected_patterns:
            for pattern_id in affected_patterns:
                if pattern_id in self.timeliness_data["entries"]:
                    self._apply_scene_decay(pattern_id, change_description)
        
        logger.info(f"Scene change registered: {change_type} - {change_description}")
    
    def _apply_scene_decay(self, entry_id: str, reason: str):
        """应用场景变化衰减"""
        if entry_id not in self.timeliness_data["entries"]:
            return
        
        entry_data = self.timeliness_data["entries"][entry_id]
        current_confidence = entry_data.get("current_confidence", 0.85)
        
        # 应用衰减
        new_confidence = current_confidence * (1 - self.SCENE_CHANGE_DECAY)
        
        # 记录衰减事件
        decay_event = DecayEvent(
            timestamp=datetime.now().isoformat(),
            event_type="scene_change",
            confidence_before=current_confidence,
            confidence_after=new_confidence,
            reason=reason,
            details={"scene_change": True}
        )
        
        # 更新条目
        entry_data["current_confidence"] = new_confidence
        entry_data["scene_changes_detected"] = entry_data.get("scene_changes_detected", 0) + 1
        entry_data["decay_events"].append(asdict(decay_event))
        
        # 更新状态
        self._update_status(entry_id, new_confidence)
        
        self._save_timeliness_data()
    
    # ==================== 反例衰减 ====================
    
    def register_counterexample(
        self,
        entry_id: str,
        counterexample_description: str
    ):
        """
        注册反例（预防策略失效）
        
        Args:
            entry_id: 错误智慧条目ID
            counterexample_description: 反例描述
        """
        if entry_id not in self.timeliness_data["entries"]:
            # 如果条目不存在，初始化
            self._initialize_entry(entry_id, base_confidence=0.85)
        
        entry_data = self.timeliness_data["entries"][entry_id]
        current_confidence = entry_data.get("current_confidence", 0.85)
        counterexample_count = entry_data.get("counterexample_count", 0) + 1
        
        # 应用反例衰减：每个反例降低30%
        decay_factor = (1 - self.COUNTEREXAMPLE_DECAY) ** counterexample_count
        new_confidence = entry_data.get("base_confidence", 0.85) * decay_factor
        
        # 记录衰减事件
        decay_event = DecayEvent(
            timestamp=datetime.now().isoformat(),
            event_type="counterexample",
            confidence_before=current_confidence,
            confidence_after=new_confidence,
            reason=f"Counterexample #{counterexample_count}: {counterexample_description}",
            details={"counterexample_count": counterexample_count}
        )
        
        # 更新条目
        entry_data["current_confidence"] = new_confidence
        entry_data["counterexample_count"] = counterexample_count
        entry_data["decay_events"].append(asdict(decay_event))
        
        # 更新状态
        self._update_status(entry_id, new_confidence)
        
        self._save_timeliness_data()
        
        logger.warning(f"Counterexample registered for {entry_id}: confidence {current_confidence:.3f} → {new_confidence:.3f}")
    
    # ==================== 状态管理 ====================
    
    def _update_status(self, entry_id: str, confidence: float):
        """更新条目状态"""
        if entry_id not in self.timeliness_data["entries"]:
            return
        
        entry_data = self.timeliness_data["entries"][entry_id]
        
        # 确定状态
        if confidence >= self.ACTIVE_THRESHOLD:
            new_status = TimelinessStatus.ACTIVE.value
        elif confidence >= self.DEPRECATED_THRESHOLD:
            new_status = TimelinessStatus.DEPRECATED.value
        else:
            new_status = TimelinessStatus.ARCHIVED.value
        
        old_status = entry_data.get("status", "active")
        entry_data["status"] = new_status
        entry_data["last_decay_check"] = datetime.now().isoformat()
        
        # 更新统计
        if old_status != new_status:
            metadata = self.timeliness_data["metadata"]
            if old_status == "active":
                metadata["total_active"] = max(0, metadata.get("total_active", 0) - 1)
            elif old_status == "deprecated":
                metadata["total_deprecated"] = max(0, metadata.get("total_deprecated", 0) - 1)
            
            if new_status == "active":
                metadata["total_active"] = metadata.get("total_active", 0) + 1
            elif new_status == "deprecated":
                metadata["total_deprecated"] = metadata.get("total_deprecated", 0) + 1
            elif new_status == "archived":
                metadata["total_archived"] = metadata.get("total_archived", 0) + 1
            
            logger.info(f"Status changed for {entry_id}: {old_status} → {new_status}")
    
    def _initialize_entry(self, entry_id: str, base_confidence: float = 0.85):
        """初始化条目时效性数据"""
        now = datetime.now().isoformat()
        
        self.timeliness_data["entries"][entry_id] = {
            "current_confidence": base_confidence,
            "status": TimelinessStatus.ACTIVE.value,
            "base_confidence": base_confidence,
            "creation_time": now,
            "last_decay_check": now,
            "last_validation": now,
            "counterexample_count": 0,
            "scene_changes_detected": 0,
            "decay_events": []
        }
        
        self.timeliness_data["metadata"]["total_active"] = \
            self.timeliness_data["metadata"].get("total_active", 0) + 1
    
    # ==================== 综合计算 ====================
    
    def get_confidence(self, entry_id: str, entry_data: Dict = None) -> float:
        """
        获取条目的当前置信度
        
        综合考虑三种衰减因素
        
        Args:
            entry_id: 条目ID
            entry_data: 条目数据（可选，包含创建时间等）
        
        Returns:
            当前置信度
        """
        # 如果时效性数据中存在，直接返回
        if entry_id in self.timeliness_data["entries"]:
            return self.timeliness_data["entries"][entry_id].get("current_confidence", 0.85)
        
        # 如果条目数据存在，计算时间衰减
        if entry_data and "timestamp" in entry_data:
            base_confidence = entry_data.get("元数据", {}).get("置信度", 0.85)
            decayed, _ = self.calculate_time_decay(base_confidence, entry_data["timestamp"])
            
            # 初始化时效性数据
            self._initialize_entry(entry_id, decayed)
            
            return decayed
        
        # 默认值
        return 0.85
    
    def get_status(self, entry_id: str) -> str:
        """获取条目状态"""
        if entry_id in self.timeliness_data["entries"]:
            return self.timeliness_data["entries"][entry_id].get("status", "active")
        return "active"
    
    def is_usable(self, entry_id: str) -> bool:
        """判断条目是否可用（非archived）"""
        status = self.get_status(entry_id)
        return status != TimelinessStatus.ARCHIVED.value
    
    # ==================== 周期性审计 ====================
    
    def run_audit(self, entries_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        运行时效性审计
        
        Args:
            entries_data: 错误智慧库条目数据（用于同步时间衰减）
        
        Returns:
            审计报告
        """
        now = time.time()
        audit_report = {
            "timestamp": datetime.now().isoformat(),
            "entries_checked": 0,
            "status_changes": [],
            "expired_entries": [],
            "recommendations": []
        }
        
        # 检查所有条目
        for entry_id, timeliness_entry in self.timeliness_data["entries"].items():
            audit_report["entries_checked"] += 1
            
            # 获取原始条目数据
            original_entry = None
            if entries_data and entry_id in entries_data:
                original_entry = entries_data[entry_id]
            
            # 重新计算时间衰减
            base_confidence = timeliness_entry.get("base_confidence", 0.85)
            creation_time = timeliness_entry.get("creation_time", datetime.now().isoformat())
            
            time_decayed, days = self.calculate_time_decay(base_confidence, creation_time)
            
            # 考虑反例衰减
            counterexample_count = timeliness_entry.get("counterexample_count", 0)
            counterexample_factor = (1 - self.COUNTEREXAMPLE_DECAY) ** counterexample_count
            
            # 综合置信度
            current_confidence = timeliness_entry.get("current_confidence", time_decayed)
            new_confidence = time_decayed * counterexample_factor
            
            # 如果差异显著，更新
            if abs(new_confidence - current_confidence) > 0.01:
                old_status = timeliness_entry.get("status", "active")
                timeliness_entry["current_confidence"] = new_confidence
                self._update_status(entry_id, new_confidence)
                new_status = timeliness_entry.get("status", "active")
                
                if old_status != new_status:
                    audit_report["status_changes"].append({
                        "entry_id": entry_id,
                        "old_status": old_status,
                        "new_status": new_status,
                        "confidence": new_confidence
                    })
            
            # 标记过期条目
            if new_confidence < self.DEPRECATED_THRESHOLD:
                audit_report["expired_entries"].append(entry_id)
        
        # 更新审计时间
        self.timeliness_data["metadata"]["last_audit"] = datetime.now().isoformat()
        self.last_audit_time = now
        
        # 保存
        self._save_timeliness_data()
        
        # 生成建议
        if audit_report["entries_checked"] > 0:
            expired_rate = len(audit_report["expired_entries"]) / audit_report["entries_checked"]
            if expired_rate > 0.2:
                audit_report["recommendations"].append(
                    f"过期条目比例过高({expired_rate:.1%})，建议清理或重新验证"
                )
        
        logger.info(f"Audit completed: {audit_report['entries_checked']} entries checked")
        
        return audit_report
    
    # ==================== 验证反馈 ====================
    
    def record_validation_result(
        self,
        entry_id: str,
        validation_success: bool,
        validation_context: str = ""
    ):
        """
        记录验证结果
        
        Args:
            entry_id: 条目ID
            validation_success: 验证是否成功
            validation_context: 验证上下文
        """
        if entry_id not in self.timeliness_data["entries"]:
            self._initialize_entry(entry_id)
        
        entry_data = self.timeliness_data["entries"][entry_id]
        
        if validation_success:
            # 成功验证提升置信度（最多恢复到base）
            current = entry_data.get("current_confidence", 0.85)
            base = entry_data.get("base_confidence", 0.85)
            new_confidence = min(base, current + 0.05)
            entry_data["current_confidence"] = new_confidence
            entry_data["last_validation"] = datetime.now().isoformat()
        else:
            # 失败则注册反例
            self.register_counterexample(entry_id, validation_context)
        
        self._save_timeliness_data()
    
    # ==================== 查询接口 ====================
    
    def get_active_entries(self) -> List[str]:
        """获取所有活跃条目ID"""
        return [
            entry_id for entry_id, data in self.timeliness_data["entries"].items()
            if data.get("status") == TimelinessStatus.ACTIVE.value
        ]
    
    def get_deprecated_entries(self) -> List[str]:
        """获取所有deprecated条目ID"""
        return [
            entry_id for entry_id, data in self.timeliness_data["entries"].items()
            if data.get("status") == TimelinessStatus.DEPRECATED.value
        ]
    
    def get_archived_entries(self) -> List[str]:
        """获取所有archived条目ID"""
        return [
            entry_id for entry_id, data in self.timeliness_data["entries"].items()
            if data.get("status") == TimelinessStatus.ARCHIVED.value
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取时效性统计"""
        return {
            "total_entries": len(self.timeliness_data["entries"]),
            "active_count": self.timeliness_data["metadata"].get("total_active", 0),
            "deprecated_count": self.timeliness_data["metadata"].get("total_deprecated", 0),
            "archived_count": self.timeliness_data["metadata"].get("total_archived", 0),
            "last_audit": self.timeliness_data["metadata"].get("last_audit", "N/A"),
            "scene_changes_recorded": len(self.scene_change_events)
        }


# ==================== 命令行接口 ====================

def main():
    """命令行测试接口"""
    print("=== 错误智慧库时效性管理模块（测试模式） ===\n")
    
    manager = TimelinessManager("./agi_memory")
    
    # 测试1：初始化条目
    print("测试1：初始化条目")
    manager._initialize_entry("ew_test_001", base_confidence=0.90)
    confidence = manager.get_confidence("ew_test_001")
    status = manager.get_status("ew_test_001")
    print(f"  置信度: {confidence:.3f}")
    print(f"  状态: {status}\n")
    
    # 测试2：时间衰减计算
    print("测试2：时间衰减计算")
    from datetime import datetime, timedelta
    old_time = (datetime.now() - timedelta(days=30)).isoformat()
    decayed, days = manager.calculate_time_decay(0.90, old_time)
    print(f"  原始置信度: 0.90")
    print(f"  经过天数: {days}")
    print(f"  衰减后置信度: {decayed:.3f}\n")
    
    # 测试3：反例衰减
    print("测试3：反例衰减")
    manager.register_counterexample("ew_test_001", "预防策略在实际场景中失效")
    new_confidence = manager.get_confidence("ew_test_001")
    print(f"  反例后的置信度: {new_confidence:.3f}\n")
    
    # 测试4：场景变化衰减
    print("测试4：场景变化衰减")
    manager._initialize_entry("ew_test_002", base_confidence=0.85)
    manager.register_scene_change(
        change_type="model_upgrade",
        change_description="模型升级到新版本",
        affected_patterns=["ew_test_002"]
    )
    confidence_002 = manager.get_confidence("ew_test_002")
    print(f"  场景变化后的置信度: {confidence_002:.3f}\n")
    
    # 测试5：状态转换
    print("测试5：状态转换测试")
    # 注册多个反例使条目降级
    for i in range(5):
        manager.register_counterexample("ew_test_003", f"反例 #{i+1}")
    final_confidence = manager.get_confidence("ew_test_003")
    final_status = manager.get_status("ew_test_003")
    print(f"  最终置信度: {final_confidence:.3f}")
    print(f"  最终状态: {final_status}\n")
    
    # 测试6：统计信息
    print("测试6：统计信息")
    stats = manager.get_statistics()
    print(f"  总条目数: {stats['total_entries']}")
    print(f"  活跃: {stats['active_count']}")
    print(f"  已弃用: {stats['deprecated_count']}")
    print(f"  已存档: {stats['archived_count']}\n")
    
    print("=== 所有测试完成 ===")


if __name__ == "__main__":
    main()
