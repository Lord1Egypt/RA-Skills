"""
Learning Signals Detector - Detects learning opportunities from feedback and events
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime
from pathlib import Path
import re
import json


class LearningSignalType(Enum):
    """Learning signal types"""
    CORRECTION = "correction"           # Correction signal
    PREFERENCE = "preference"           # Preference signal
    ERROR = "error"                   # Error signal
    SUCCESS = "success"               # Success signal
    KNOWLEDGE_GAP = "knowledge_gap"  # Knowledge gap signal


class Confidence(Enum):
    """Confidence level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class LearningSignal:
    """Learning signal data structure"""
    id: str
    signal_type: LearningSignalType
    confidence: Confidence
    source: str                           # user, system, pattern
    content: str                           # Signal content
    context: Dict                          # Context information
    suggested_action: Optional[str] = None  # Suggested action
    created_at: datetime = field(default_factory=datetime.now)
    processed: bool = False               # Whether has been processed
    category: str = ""                   # Category area


class LearningSignalsDetector:
    """
    Learning Signals Detector
    
    Detects learning signals from user feedback, system events, and task outcomes.
    """
    
    # Correction patterns (Chinese + English)
    CORRECTION_PATTERNS = [
        r"纠正[:：]\s*(.+?)(?:\n|$)",
        r"不对[:：]\s*(.+?)(?:\n|$)",
        r"应该[:：]\s*(.+?)(?:\n|$)",
        r"正确的是[:：]\s*(.+?)(?:\n|$)",
        r"❌\s*(.+?)(?:\n|$)",
        r"correction[:：]\s*(.+?)(?:\n|$)",
        r"wrong[:：]\s*(.+?)(?:\n|$)",
        r"incorrect[:：]\s*(.+?)(?:\n|$)",
    ]
    
    # Preference patterns
    PREFERENCE_PATTERNS = [
        r"更喜欢\s*(.+?)(?:\n|$)",
        r"偏好\s*(.+?)(?:\n|$)",
        r"通常\s*(.+?)(?:\n|$)",
        r"一般会\s*(.+?)(?:\n|$)",
        r"👍\s*(.+?)(?:\n|$)",
        r"prefer\s*(.+?)(?:\n|$)",
        r"usually\s*(.+?)(?:\n|$)",
    ]
    
    # Error patterns
    ERROR_PATTERNS = [
        r"错误[:：]\s*(.+?)(?:\n|$)",
        r"失败[:：]\s*(.+?)(?:\n|$)",
        r"不对[:：]\s*(.+?)(?:\n|$)",
        r"Bug[:：]\s*(.+?)(?:\n|$)",
        r"❌\s*(.+?)(?:\n|$)",
        r"error[:：]\s*(.+?)(?:\n|$)",
        r"failed[:：]\s*(.+?)(?:\n|$)",
    ]
    
    # Success patterns
    SUCCESS_PATTERNS = [
        r"对了[:：]\s*(.+?)(?:\n|$)",
        r"正确[:：]\s*(.+?)(?:\n|$)",
        r"成功[:：]\s*(.+?)(?:\n|$)",
        r"很好[:：]\s*(.+?)(?:\n|$)",
        r"✅\s*(.+?)(?:\n|$)",
        r"👍\s*(.+?)(?:\n|$)",
        r"correct[:：]\s*(.+?)(?:\n|$)",
        r"success[:：]\s*(.+?)(?:\n|$)",
    ]
    
    # Knowledge gap patterns
    KNOWLEDGE_GAP_PATTERNS = [
        r"不知道\s*(.+?)(?:\n|$)",
        r"不了解\s*(.+?)(?:\n|$)",
        r"不清楚\s*(.+?)(?:\n|$)",
        r"不确定\s*(.+?)(?:\n|$)",
        r"missing\s*(.+?)(?:\n|$)",
        r"unknown\s*(.+?)(?:\n|$)",
        r"如何\s*(.+?)(?:\n|$)",
    ]
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize Learning Signals Detector
        
        Args:
            storage_path: Path to store signals (default: ~/.anima/data/learning_signals/)
        """
        self.storage_path = Path(storage_path) if storage_path else Path("~/.anima/data/learning_signals").expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.signals: List[LearningSignal] = []
        self.signal_history: List[LearningSignal] = []
        
        # Compile patterns
        self._compile_patterns()
        
        # Load existing signals
        self._load_signals()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficiency"""
        self.correction_regex = [re.compile(p, re.MULTILINE | re.DOTALL) for p in self.CORRECTION_PATTERNS]
        self.preference_regex = [re.compile(p, re.MULTILINE | re.DOTALL) for p in self.PREFERENCE_PATTERNS]
        self.error_regex = [re.compile(p, re.MULTILINE | re.DOTALL) for p in self.ERROR_PATTERNS]
        self.success_regex = [re.compile(p, re.MULTILINE | re.DOTALL) for p in self.SUCCESS_PATTERNS]
        self.knowledge_gap_regex = [re.compile(p, re.MULTILINE | re.DOTALL) for p in self.KNOWLEDGE_GAP_PATTERNS]
    
    def _generate_id(self) -> str:
        """Generate unique signal ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _load_signals(self):
        """Load existing signals from storage"""
        signals_file = self.storage_path / "signals.json"
        
        if signals_file.exists():
            try:
                with open(signals_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for item in data:
                    item['created_at'] = datetime.fromisoformat(item['created_at'])
                    item['signal_type'] = LearningSignalType(item['signal_type'])
                    item['confidence'] = Confidence(item['confidence'])
                    signal = LearningSignal(**item)
                    self.signals.append(signal)
                    self.signal_history.append(signal)
            except Exception:
                pass  # If loading fails, start fresh
    
    def _save_signals(self):
        """Save signals to storage"""
        signals_file = self.storage_path / "signals.json"
        
        data = []
        for signal in self.signals:
            data.append({
                'id': signal.id,
                'signal_type': signal.signal_type.value,
                'confidence': signal.confidence.value,
                'source': signal.source,
                'content': signal.content,
                'context': signal.context,
                'suggested_action': signal.suggested_action,
                'created_at': signal.created_at.isoformat(),
                'processed': signal.processed,
                'category': signal.category
            })
        
        with open(signals_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def detect_from_feedback(self, feedback: str, source: str = "user") -> List[LearningSignal]:
        """
        Detect learning signals from feedback
        
        Args:
            feedback: User feedback content
            source: Source type (user/system/pattern)
            
        Returns:
            List of detected learning signals
        """
        signals = []
        
        # Detect all signal types
        signals.extend(self._detect_corrections(feedback, source))
        signals.extend(self._detect_preferences(feedback, source))
        signals.extend(self._detect_errors(feedback, source))
        signals.extend(self._detect_successes(feedback, source))
        signals.extend(self._detect_knowledge_gaps(feedback, source))
        
        # Add to history
        self.signal_history.extend(signals)
        
        # Save updated signals
        self._save_signals()
        
        return signals
    
    def _detect_corrections(self, text: str, source: str) -> List[LearningSignal]:
        """Detect correction signals"""
        signals = []
        
        for pattern in self.correction_regex:
            matches = pattern.findall(text)
            for match in matches:
                content = match.strip() if isinstance(match, str) else match[0].strip()
                
                if len(content) < 3:  # Filter too short matches
                    continue
                
                signal = LearningSignal(
                    id=self._generate_id(),
                    signal_type=LearningSignalType.CORRECTION,
                    confidence=self._assess_confidence(text, content),
                    source=source,
                    content=content[:500],  # Limit length
                    context={"original_text": text[:1000]},
                    suggested_action="Review and update knowledge base",
                    category=self._detect_category(text)
                )
                signals.append(signal)
                self.signals.append(signal)
        
        return signals
    
    def _detect_preferences(self, text: str, source: str) -> List[LearningSignal]:
        """Detect preference signals"""
        signals = []
        
        for pattern in self.preference_regex:
            matches = pattern.findall(text)
            for match in matches:
                content = match.strip() if isinstance(match, str) else match[0].strip()
                
                if len(content) < 3:
                    continue
                
                signal = LearningSignal(
                    id=self._generate_id(),
                    signal_type=LearningSignalType.PREFERENCE,
                    confidence=self._assess_confidence(text, content),
                    source=source,
                    content=content[:500],
                    context={"original_text": text[:1000]},
                    suggested_action="Record to preferences",
                    category=self._detect_category(text)
                )
                signals.append(signal)
                self.signals.append(signal)
        
        return signals
    
    def _detect_errors(self, text: str, source: str) -> List[LearningSignal]:
        """Detect error signals"""
        signals = []
        
        for pattern in self.error_regex:
            matches = pattern.findall(text)
            for match in matches:
                content = match.strip() if isinstance(match, str) else match[0].strip()
                
                if len(content) < 3:
                    continue
                
                signal = LearningSignal(
                    id=self._generate_id(),
                    signal_type=LearningSignalType.ERROR,
                    confidence=self._assess_confidence(text, content),
                    source=source,
                    content=content[:500],
                    context={"original_text": text[:1000]},
                    suggested_action="Log error and prevent recurrence",
                    category=self._detect_category(text)
                )
                signals.append(signal)
                self.signals.append(signal)
        
        return signals
    
    def _detect_successes(self, text: str, source: str) -> List[LearningSignal]:
        """Detect success signals"""
        signals = []
        
        for pattern in self.success_regex:
            matches = pattern.findall(text)
            for match in matches:
                content = match.strip() if isinstance(match, str) else match[0].strip()
                
                if len(content) < 3:
                    continue
                
                signal = LearningSignal(
                    id=self._generate_id(),
                    signal_type=LearningSignalType.SUCCESS,
                    confidence=self._assess_confidence(text, content),
                    source=source,
                    content=content[:500],
                    context={"original_text": text[:1000]},
                    suggested_action="Extract best practice",
                    category=self._detect_category(text)
                )
                signals.append(signal)
                self.signals.append(signal)
        
        return signals
    
    def _detect_knowledge_gaps(self, text: str, source: str) -> List[LearningSignal]:
        """Detect knowledge gap signals"""
        signals = []
        
        for pattern in self.knowledge_gap_regex:
            matches = pattern.findall(text)
            for match in matches:
                content = match.strip() if isinstance(match, str) else match[0].strip()
                
                if len(content) < 3:
                    continue
                
                signal = LearningSignal(
                    id=self._generate_id(),
                    signal_type=LearningSignalType.KNOWLEDGE_GAP,
                    confidence=self._assess_confidence(text, content),
                    source=source,
                    content=content[:500],
                    context={"original_text": text[:1000]},
                    suggested_action="Research and fill gap",
                    category=self._detect_category(text)
                )
                signals.append(signal)
                self.signals.append(signal)
        
        return signals
    
    def _assess_confidence(self, text: str, match: str) -> Confidence:
        """Assess signal confidence"""
        match_lower = match.lower()
        text_lower = text.lower()
        
        # Very high confidence: explicit correction/preference indicators
        very_high_indicators = [
            "纠正", "不对", "应该", "更喜欢", "偏好",
            "correct", "wrong", "incorrect", "prefer"
        ]
        for indicator in very_high_indicators:
            if indicator in text_lower:
                return Confidence.VERY_HIGH
        
        # High confidence: explicit markers
        high_indicators = [
            "错误", "失败", "不对", "成功", "很好",
            "error", "failed", "wrong", "success", "correct"
        ]
        for indicator in high_indicators:
            if indicator in text_lower:
                return Confidence.HIGH
        
        # Medium confidence: general indicators
        medium_indicators = [
            "❌", "✅", "👍", "通常", "一般", "可能",
            "usually", "sometimes", "maybe", "perhaps"
        ]
        for indicator in medium_indicators:
            if indicator in text:
                return Confidence.MEDIUM
        
        return Confidence.LOW
    
    def _detect_category(self, text: str) -> str:
        """Detect content category"""
        category_keywords = {
            "code": ["代码", "code", "函数", "function", "class", "变量", "variable"],
            "design": ["设计", "design", "架构", "architecture", "模式", "pattern"],
            "performance": ["性能", "performance", "优化", "optimize", "速度", "speed"],
            "security": ["安全", "security", "漏洞", "vulnerability", "权限", "permission"],
            "api": ["api", "接口", "endpoint", "request", "response"],
            "database": ["数据库", "database", "sql", "query", "表", "table"],
            "documentation": ["文档", "doc", "注释", "comment", "readme"],
            "testing": ["测试", "test", "单元测试", "unit test", "集成测试"],
        }
        
        text_lower = text.lower()
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return "general"
    
    def get_unprocessed_signals(self) -> List[LearningSignal]:
        """Get unprocessed learning signals"""
        return [s for s in self.signals if not s.processed]
    
    def mark_processed(self, signal_id: str) -> bool:
        """Mark a signal as processed"""
        for signal in self.signals:
            if signal.id == signal_id:
                signal.processed = True
                self._save_signals()
                return True
        return False
    
    def get_signals_by_type(self, signal_type: LearningSignalType) -> List[LearningSignal]:
        """Get signals by type"""
        return [s for s in self.signals if s.signal_type == signal_type]
    
    def get_signals_by_source(self, source: str) -> List[LearningSignal]:
        """Get signals by source"""
        return [s for s in self.signals if s.source == source]
    
    def get_signals_by_category(self, category: str) -> List[LearningSignal]:
        """Get signals by category"""
        return [s for s in self.signals if s.category == category]
    
    def get_recent_signals(self, limit: int = 10) -> List[LearningSignal]:
        """Get recent signals"""
        return sorted(self.signals, key=lambda s: s.created_at, reverse=True)[:limit]
    
    def get_signal_stats(self) -> Dict:
        """Get signal statistics"""
        total = len(self.signals)
        by_type = {}
        by_source = {}
        by_category = {}
        by_confidence = {}
        processed = sum(1 for s in self.signals if s.processed)
        
        for signal in self.signals:
            # By type
            type_name = signal.signal_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
            
            # By source
            by_source[signal.source] = by_source.get(signal.source, 0) + 1
            
            # By category
            by_category[signal.category] = by_category.get(signal.category, 0) + 1
            
            # By confidence
            conf_name = signal.confidence.value
            by_confidence[conf_name] = by_confidence.get(conf_name, 0) + 1
        
        return {
            "total": total,
            "processed": processed,
            "unprocessed": total - processed,
            "by_type": by_type,
            "by_source": by_source,
            "by_category": by_category,
            "by_confidence": by_confidence
        }
    
    def clear_processed_signals(self) -> int:
        """Clear processed signals from memory (keep in history)"""
        before_count = len(self.signals)
        self.signals = [s for s in self.signals if not s.processed]
        after_count = len(self.signals)
        return before_count - after_count
