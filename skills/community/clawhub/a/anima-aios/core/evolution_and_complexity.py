"""
Evolution Strategy Engine + Complexity Assessor
7 evolution strategies + 6-dimension complexity assessment
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime
from pathlib import Path
import json


# ============================================================
# Evolution Strategy Engine
# ============================================================

class EvolutionStrategy(Enum):
    """Evolution strategies"""
    BALANCED = "balanced"           # Balanced: stable improvement
    INNOVATE = "innovate"           # Innovate: explore new methods
    HARDEN = "harden"               # Harden: prevent degradation
    REPAIR = "repair"               # Repair: fix failures
    SPECIALIZE = "specialize"       # Specialize: deepen expertise
    GENERALIZE = "generalize"       # Generalize: expand scope
    RESTART = "restart"            # Restart: start fresh


@dataclass
class EvolutionConfig:
    """Evolution configuration"""
    strategy: EvolutionStrategy
    intensity: float = 0.5           # 0-1
    focus_areas: List[str] = field(default_factory=list)
    constraints: Dict = field(default_factory=dict)


class EvolutionStrategyEngine:
    """
    Evolution Strategy Engine
    
    Selects appropriate evolution strategy based on context.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = Path(storage_path) if storage_path else Path("~/.anima/data/evolution").expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.current_strategy = EvolutionStrategy.BALANCED
        self.strategy_history: List[EvolutionConfig] = []
        self.performance_tracker = StrategyPerformanceTracker(storage_path=self.storage_path)
        
        self._load_history()
    
    def _load_history(self):
        """Load strategy history"""
        history_file = self.storage_path / "strategy_history.json"
        
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    item['strategy'] = EvolutionStrategy(item['strategy'])
                    config = EvolutionConfig(**item)
                    self.strategy_history.append(config)
            except Exception:
                pass
    
    def _save_history(self):
        """Save strategy history"""
        history_file = self.storage_path / "strategy_history.json"
        
        data = [
            {
                'strategy': c.strategy.value,
                'intensity': c.intensity,
                'focus_areas': c.focus_areas,
                'constraints': c.constraints
            }
            for c in self.strategy_history
        ]
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def select_strategy(self, context: Dict) -> EvolutionConfig:
        """
        Select evolution strategy based on context
        
        Args:
            context: Context containing:
                - recent_performance: List of recent scores
                - error_rate: Current error rate
                - task_complexity: low/medium/high
                - goal: Current goal
                
        Returns:
            Selected evolution configuration
        """
        recent_perf = context.get("recent_performance", [])
        error_rate = context.get("error_rate", 0.0)
        task_complexity = context.get("task_complexity", "medium")
        task_type = context.get("task_type", "general")
        
        # Decision tree for strategy selection
        if error_rate > 0.3:
            strategy = EvolutionStrategy.REPAIR
        elif error_rate > 0.15:
            strategy = EvolutionStrategy.HARDEN
        elif task_complexity == "high":
            strategy = EvolutionStrategy.SPECIALIZE
        elif task_complexity == "low" and len(recent_perf) >= 3 and recent_perf[-1] >= 8.0:
            strategy = EvolutionStrategy.INNOVATE
        elif self._is_performance_declining(recent_perf):
            strategy = EvolutionStrategy.REPAIR
        elif self._is_performance_stable(recent_perf) and len(recent_perf) >= 5:
            strategy = EvolutionStrategy.BALANCED
        else:
            strategy = EvolutionStrategy.BALANCED
        
        # Calculate intensity
        intensity = self._calculate_intensity(strategy, context)
        
        # Identify focus areas
        focus_areas = self._identify_focus_areas(context)
        
        # Get constraints
        constraints = self._get_constraints(strategy)
        
        config = EvolutionConfig(
            strategy=strategy,
            intensity=intensity,
            focus_areas=focus_areas,
            constraints=constraints
        )
        
        self.current_strategy = strategy
        self.strategy_history.append(config)
        self._save_history()
        
        return config
    
    def _is_performance_declining(self, recent_perf: List[float]) -> bool:
        """Check if performance is declining"""
        if len(recent_perf) < 3:
            return False
        return recent_perf[-1] < recent_perf[-3] - 1.0
    
    def _is_performance_stable(self, recent_perf: List[float]) -> bool:
        """Check if performance is stable"""
        if len(recent_perf) < 3:
            return True
        variance = sum((x - sum(recent_perf)/len(recent_perf))**2 for x in recent_perf) / len(recent_perf)
        return variance < 0.5
    
    def _calculate_intensity(self, strategy: EvolutionStrategy, context: Dict) -> float:
        """Calculate strategy intensity"""
        base = 0.5
        
        if strategy == EvolutionStrategy.HARDEN:
            return 0.8
        elif strategy == EvolutionStrategy.REPAIR:
            return 0.7
        elif strategy == EvolutionStrategy.INNOVATE:
            return 0.6
        elif strategy == EvolutionStrategy.SPECIALIZE:
            return 0.65
        elif strategy == EvolutionStrategy.RESTART:
            return 1.0
        
        return base
    
    def _identify_focus_areas(self, context: Dict) -> List[str]:
        """Identify focus areas based on context"""
        areas = []
        
        if context.get("error_rate", 0) > 0.1:
            areas.append("error_reduction")
        
        if context.get("task_complexity") == "high":
            areas.append("complex_task_handling")
        
        if context.get("efficiency", 1.0) < 0.8:
            areas.append("efficiency_improvement")
        
        if context.get("domain"):
            areas.append(f"domain_{context['domain']}")
        
        return areas
    
    def _get_constraints(self, strategy: EvolutionStrategy) -> Dict:
        """Get strategy constraints"""
        constraints = {
            "max_changes": 3,
            "preserve_core_behavior": True
        }
        
        if strategy == EvolutionStrategy.HARDEN:
            constraints["preserve_all"] = True
            constraints["max_changes"] = 1
        elif strategy == EvolutionStrategy.REPAIR:
            constraints["prioritize_stability"] = True
        elif strategy == EvolutionStrategy.RESTART:
            constraints["preserve_learning"] = True
        
        return constraints
    
    def apply_strategy(
        self,
        config: EvolutionConfig,
        learning_data: List[Dict]
    ) -> List[Dict]:
        """Apply evolution strategy to learning data"""
        strategy = config.strategy
        intensity = config.intensity
        
        if strategy == EvolutionStrategy.BALANCED:
            return self._apply_balanced(learning_data, intensity)
        elif strategy == EvolutionStrategy.INNOVATE:
            return self._apply_innovate(learning_data, intensity)
        elif strategy == EvolutionStrategy.HARDEN:
            return self._apply_harden(learning_data, intensity)
        elif strategy == EvolutionStrategy.REPAIR:
            return self._apply_repair(learning_data, intensity)
        elif strategy == EvolutionStrategy.SPECIALIZE:
            return self._apply_specialize(learning_data, intensity)
        elif strategy == EvolutionStrategy.GENERALIZE:
            return self._apply_generalize(learning_data, intensity)
        elif strategy == EvolutionStrategy.RESTART:
            return self._apply_restart(learning_data)
        
        return []
    
    def _apply_balanced(self, data: List[Dict], intensity: float) -> List[Dict]:
        """Apply balanced strategy"""
        suggestions = []
        for item in data:
            confidence = item.get("confidence", 0)
            if confidence > 0.7 - (1 - intensity) * 0.3:
                suggestions.append({
                    "action": "adopt",
                    "item": item,
                    "priority": "high" if confidence > 0.85 else "medium"
                })
        return suggestions
    
    def _apply_innovate(self, data: List[Dict], intensity: float) -> List[Dict]:
        """Apply innovate strategy"""
        suggestions = []
        for item in data:
            novelty = item.get("novelty", 0)
            if novelty > 0.5 - (1 - intensity) * 0.2:
                suggestions.append({
                    "action": "experiment",
                    "item": item,
                    "priority": "high"
                })
        return suggestions
    
    def _apply_harden(self, data: List[Dict], intensity: float) -> List[Dict]:
        """Apply harden strategy"""
        suggestions = []
        for item in data:
            if item.get("failure_count", 0) > 0 or item.get("risk_level", 0) > 0.5:
                suggestions.append({
                    "action": "fix",
                    "item": item,
                    "priority": "critical"
                })
        return suggestions
    
    def _apply_repair(self, data: List[Dict], intensity: float) -> List[Dict]:
        """Apply repair strategy"""
        suggestions = []
        for item in data:
            if item.get("recent_failure", False):
                suggestions.append({
                    "action": "repair",
                    "item": item,
                    "priority": "critical"
                })
        return suggestions
    
    def _apply_specialize(self, data: List[Dict], intensity: float) -> List[Dict]:
        """Apply specialize strategy"""
        suggestions = []
        for item in data:
            expertise = item.get("domain_expertise", 0)
            if expertise > 0.6 - (1 - intensity) * 0.2:
                suggestions.append({
                    "action": "deepen",
                    "item": item,
                    "priority": "high"
                })
        return suggestions
    
    def _apply_generalize(self, data: List[Dict], intensity: float) -> List[Dict]:
        """Apply generalize strategy"""
        suggestions = []
        for item in data:
            if item.get("specific_to_general", False):
                suggestions.append({
                    "action": "generalize",
                    "item": item,
                    "priority": "medium"
                })
        return suggestions
    
    def _apply_restart(self, data: List[Dict]) -> List[Dict]:
        """Apply restart strategy"""
        return [{"action": "reset", "item": None, "priority": "critical"}]
    
    def record_performance(self, strategy: EvolutionStrategy, performance: float):
        """Record strategy performance"""
        self.performance_tracker.record(strategy, performance)
    
    def get_best_strategy(self) -> EvolutionStrategy:
        """Get best performing strategy"""
        return self.performance_tracker.get_best_strategy()


class StrategyPerformanceTracker:
    """Track strategy performance"""
    
    def __init__(self, storage_path: Path = None):
        self.storage_path = storage_path or Path("~/.anima/data/evolution").expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.performance_data: Dict[EvolutionStrategy, List[float]] = {
            s: [] for s in EvolutionStrategy
        }
        
        self._load_data()
    
    def _load_data(self):
        """Load performance data"""
        data_file = self.storage_path / "performance_data.json"
        
        if data_file.exists():
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for strategy_value, performances in data.items():
                    strategy = EvolutionStrategy(strategy_value)
                    self.performance_data[strategy] = performances[-20:]  # Keep last 20
            except Exception:
                pass
    
    def _save_data(self):
        """Save performance data"""
        data_file = self.storage_path / "performance_data.json"
        
        data = {
            s.value: p for s, p in self.performance_data.items()
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def record(self, strategy: EvolutionStrategy, performance: float):
        """Record performance for strategy"""
        self.performance_data[strategy].append(performance)
        
        # Keep only last 20 records
        if len(self.performance_data[strategy]) > 20:
            self.performance_data[strategy] = self.performance_data[strategy][-20:]
        
        self._save_data()
    
    def get_best_strategy(self) -> EvolutionStrategy:
        """Get best performing strategy by average"""
        best_strategy = EvolutionStrategy.BALANCED
        best_avg = 0.0
        
        for strategy, performances in self.performance_data.items():
            if performances:
                avg = sum(performances) / len(performances)
                if avg > best_avg:
                    best_avg = avg
                    best_strategy = strategy
        
        return best_strategy


# ============================================================
# Complexity Assessor
# ============================================================

class ComplexityLevel(Enum):
    """Complexity levels"""
    TRIVIAL = "trivial"       # Simple Q&A
    LOW = "low"              # Simple task
    MEDIUM = "medium"        # Standard task
    HIGH = "high"            # Complex task
    VERY_HIGH = "very_high"  # Extremely complex


@dataclass
class ComplexityScore:
    """Complexity assessment result"""
    total_score: float
    dimensions: Dict[str, float]
    level: ComplexityLevel
    reasoning_recommended: bool
    reasoning_type: str  # none, standard, chain_of_thought, tree_of_thought


class ComplexityAssessor:
    """
    Complexity Assessor
    
    Assesses task complexity across 6 dimensions:
    1. Task Length
    2. Domain Diversity
    3. Reasoning Depth
    4. Uncertainty
    5. Context Dependency
    6. Output Constraints
    """
    
    # Dimension weights
    DIMENSION_WEIGHTS = {
        "task_length": 0.15,
        "domain_diversity": 0.15,
        "reasoning_depth": 0.25,
        "uncertainty": 0.20,
        "context_dependency": 0.15,
        "output_constraints": 0.10
    }
    
    # Complexity thresholds
    COMPLEXITY_THRESHOLDS = {
        ComplexityLevel.TRIVIAL: (0, 2.0),
        ComplexityLevel.LOW: (2.0, 3.5),
        ComplexityLevel.MEDIUM: (3.5, 5.5),
        ComplexityLevel.HIGH: (5.5, 7.5),
        ComplexityLevel.VERY_HIGH: (7.5, 10.0)
    }
    
    # Reasoning thresholds
    REASONING_THRESHOLDS = {
        "none": (0, 2.5),
        "standard": (2.5, 4.5),
        "chain_of_thought": (4.5, 6.5),
        "tree_of_thought": (6.5, 10.0)
    }
    
    def assess(self, task: str, context: Dict) -> ComplexityScore:
        """
        Assess task complexity
        
        Args:
            task: Task description
            context: Context containing:
                - conversation_history: List of previous exchanges
                - detected_domains: List of domain keywords found
                - user_preferences: User preference hints
                
        Returns:
            Complexity score with level and reasoning recommendation
        """
        # Assess each dimension
        dimensions = {
            "task_length": self._assess_task_length(task),
            "domain_diversity": self._assess_domain_diversity(task, context),
            "reasoning_depth": self._assess_reasoning_depth(task),
            "uncertainty": self._assess_uncertainty(task, context),
            "context_dependency": self._assess_context_dependency(task, context),
            "output_constraints": self._assess_output_constraints(task)
        }
        
        # Calculate weighted total
        total_score = sum(
            dimensions[dim] * weight
            for dim, weight in self.DIMENSION_WEIGHTS.items()
        )
        
        # Determine level
        level = self._determine_level(total_score)
        
        # Determine reasoning recommendation
        reasoning_recommended = dimensions["reasoning_depth"] > 3.0
        reasoning_type = self._determine_reasoning_type(dimensions["reasoning_depth"])
        
        return ComplexityScore(
            total_score=total_score,
            dimensions=dimensions,
            level=level,
            reasoning_recommended=reasoning_recommended,
            reasoning_type=reasoning_type
        )
    
    def _assess_task_length(self, task: str) -> float:
        """Assess task length complexity"""
        words = len(task.split())
        
        if words < 10:
            return 1.0
        elif words < 50:
            return 2.5
        elif words < 200:
            return 4.5
        elif words < 500:
            return 6.5
        else:
            return 8.5
    
    def _assess_domain_diversity(self, task: str, context: Dict) -> float:
        """Assess domain diversity"""
        # Count domain switches
        domains = context.get("detected_domains", [])
        diversity = len(set(domains)) if domains else 1
        
        # Check for multiple domains
        multi_domain_indicators = ["和", "与", "以及", "同时", "and", "or"]
        has_multiple = any(ind in task.lower() for ind in multi_domain_indicators)
        
        if has_multiple:
            diversity += 1
        
        # Score
        if diversity >= 4:
            return 8.0
        elif diversity == 3:
            return 6.0
        elif diversity == 2:
            return 4.0
        else:
            return 3.0
    
    def _assess_reasoning_depth(self, task: str) -> float:
        """Assess required reasoning depth"""
        score = 3.0  # Base score
        
        # Simple reasoning indicators
        simple_keywords = ["因为", "所以", "如果", "when", "because", "so"]
        for kw in simple_keywords:
            if kw in task.lower():
                score += 0.5
        
        # Medium reasoning indicators
        medium_keywords = ["分析", "比较", "推理", "analyze", "compare", "reason"]
        for kw in medium_keywords:
            if kw in task.lower():
                score += 1.0
        
        # Complex reasoning indicators
        complex_keywords = ["证明", "推导", "论证", "设计", "创造", "prove", "derive", "design", "create"]
        for kw in complex_keywords:
            if kw in task.lower():
                score += 1.5
        
        return min(10.0, max(0.0, score))
    
    def _assess_uncertainty(self, task: str, context: Dict) -> float:
        """Assess uncertainty level"""
        score = 3.0  # Base
        
        uncertainty_keywords = {
            "可能": 0.5, "也许": 0.5, "大概": 0.5, "或许": 0.5,
            "不确定": 1.0, "未知": 1.0, "不清楚": 1.0,
            "完全未知": 2.0, "无法确定": 2.0,
            "maybe": 0.5, "perhaps": 0.5, "uncertain": 1.0, "unknown": 1.0
        }
        
        task_lower = task.lower()
        for keyword, delta in uncertainty_keywords.items():
            if keyword in task_lower:
                score += delta
        
        return min(10.0, max(0.0, score))
    
    def _assess_context_dependency(self, task: str, context: Dict) -> float:
        """Assess context dependency"""
        score = 3.0
        
        # History length
        history_length = len(context.get("conversation_history", []))
        if history_length > 10:
            score += 2.0
        elif history_length > 5:
            score += 1.0
        
        # Dependency keywords
        dependency_keywords = ["之前", "上面", "刚才", "前述", "根据", "before", "above", "previous", "according"]
        for kw in dependency_keywords:
            if kw in task.lower():
                score += 1.0
        
        return min(10.0, max(0.0, score))
    
    def _assess_output_constraints(self, task: str) -> float:
        """Assess output constraints"""
        score = 3.0
        
        constraint_keywords = {
            "必须": 0.5, "只能": 0.5, "限制": 0.5, "只能": 0.5,
            "JSON": 1.0, "XML": 1.0, "表格": 1.0, "格式": 1.0,
            "严格按照": 1.5, "不能超过": 1.5, "exactly": 1.0, "must be": 1.0
        }
        
        task_lower = task.lower()
        for keyword, delta in constraint_keywords.items():
            if keyword in task_lower:
                score += delta
        
        return min(10.0, max(0.0, score))
    
    def _determine_level(self, total_score: float) -> ComplexityLevel:
        """Determine complexity level from score"""
        for level, (low, high) in self.COMPLEXITY_THRESHOLDS.items():
            if low <= total_score < high:
                return level
        return ComplexityLevel.VERY_HIGH
    
    def _determine_reasoning_type(self, reasoning_score: float) -> str:
        """Determine recommended reasoning type"""
        for rtype, (low, high) in self.REASONING_THRESHOLDS.items():
            if low <= reasoning_score < high:
                return rtype
        return "tree_of_thought"
