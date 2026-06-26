"""
事件池管理模块
"""
import json
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from i18n import get_event_text, get_choice_text, get_current_language


@dataclass
class Choice:
    """选项"""
    text: str                           # 选项文本
    requires: Dict[str, Any] = field(default_factory=dict)  # 需要的条件
    effects: Dict[str, Any] = field(default_factory=dict)   # 效果
    next_event_id: Optional[str] = None  # 下一事件ID
    add_checkpoint: Optional[str] = None  # 击败怪物后创建存档（怪物名称）
    load_checkpoint: Optional[int] = None  # 读取存档（存档索引，1-based）
    hidden: bool = False                # 是否隐藏（不显示给玩家，但可通过命令触发）
    event_id: str = ""                   # 所属事件ID（用于翻译）
    choice_index: int = 0                # 选项索引（用于翻译）

    @classmethod
    def from_dict(cls, data: dict, event_id: str = "", choice_index: int = 0) -> 'Choice':
        return cls(
            text=data['text'],
            requires=data.get('requires', {}),
            effects=data.get('effects', {}),
            next_event_id=data.get('next_event_id'),
            add_checkpoint=data.get('add_checkpoint'),
            load_checkpoint=data.get('load_checkpoint'),
            hidden=data.get('hidden', False),
            event_id=event_id,
            choice_index=choice_index
        )

    def get_translated_text(self) -> str:
        """获取翻译后的选项文本"""
        translated = get_choice_text(self.event_id, str(self.choice_index))
        # 如果翻译键不存在，返回原始文本
        if translated == f"events.{self.event_id}.choices.{self.choice_index}":
            return self.text
        return translated


@dataclass
class Event:
    """事件"""
    id: str
    category: str                       # good / bad / monster / fixed
    floor_range: List[int]              # 可出现的楼层范围 [min, max]
    weight: int = 1                     # 权重
    one_time: bool = False              # 是否单次触发
    conditions: Dict[str, Any] = field(default_factory=dict)  # 触发条件
    description: str = ""               # 事件描述
    choices: List[Choice] = field(default_factory=list)       # 可选行动

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        choices = [Choice.from_dict(c, data['id'], i) for i, c in enumerate(data.get('choices', []))]
        return cls(
            id=data['id'],
            category=data['category'],
            floor_range=data.get('floor_range', [0, 25]),
            weight=data.get('weight', 1),
            one_time=data.get('one_time', False),
            conditions=data.get('conditions', {}),
            description=data.get('description', ''),
            choices=choices
        )

    def get_translated_description(self) -> str:
        """获取翻译后的事件描述"""
        translated = get_event_text(self.id, 'description')
        return translated if translated != f"events.{self.id}.description" else self.description

    def get_translated_choice_text(self, choice_index: int) -> str:
        """获取翻译后的选项文本"""
        if choice_index < 0 or choice_index >= len(self.choices):
            return ""
        return self.choices[choice_index].get_translated_text()

    def in_floor_range(self, floor: str) -> bool:
        """检查楼层是否在范围内"""
        try:
            floor_num = int(floor)
            return self.floor_range[0] <= floor_num <= self.floor_range[1]
        except ValueError:
            # 非数字楼层，不在范围内
            return False


class EventPool:
    """事件池管理器"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.events: Dict[str, Event] = {}      # 所有事件，按ID索引
        self.events_by_category: Dict[str, List[Event]] = {
            'good': [],
            'bad': [],
            'monster': [],
            'normal': [],
            'fixed': []
        }
        self.floors_data: Dict[str, Dict] = {}  # 完整的floors.json数据（按阶段）
        self._load_all()

    def _load_all(self):
        """加载所有数据"""
        self._load_events()
        self._load_floors_data()

    def _load_events(self):
        """加载所有事件"""
        events_dir = self.data_dir / "events"
        if not events_dir.exists():
            return

        for category in ['good', 'bad', 'monster', 'normal', 'fixed', 'ending']:
            filepath = events_dir / f"{category}.json"
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for event_data in data:
                        event = Event.from_dict(event_data)
                        self.events[event.id] = event
                        self.events_by_category[category].append(event)

    def _load_floors_data(self):
        """加载楼层配置（完整数据）"""
        filepath = self.data_dir / "floors.json"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                self.floors_data = json.load(f)

    def get_floor_config(self, floor: str, phase: int = 1) -> Dict[str, int]:
        """获取指定楼层和阶段的配置"""
        phase_key = f"phase{phase}"
        if phase_key in self.floors_data:
            phase_data = self.floors_data[phase_key]
            if floor in phase_data:
                return phase_data[floor]
        return {'good': 25, 'bad': 25, 'monster': 25, 'normal': 24, 'ending': 1}

    def get_event_by_id(self, event_id: str) -> Optional[Event]:
        """根据ID获取事件"""
        return self.events.get(event_id)

    def check_conditions(self, conditions: Dict[str, Any], state) -> bool:
        """检查事件触发条件"""
        if not conditions:
            return True

        for key, value in conditions.items():
            if key == 'has_item':
                if not all(state.has_item(item) for item in value):
                    return False
            elif key == 'missing_item':
                if any(state.has_item(item) for item in value):
                    return False
            elif key == 'has_ability':
                if not all(state.has_ability(ability) for ability in value):
                    return False
            elif key == 'missing_ability':
                if any(state.has_ability(ability) for ability in value):
                    return False
            elif key == 'has_debuff':
                if not all(state.has_debuff(d) for d in value):
                    return False
            elif key == 'missing_debuff':
                if any(state.has_debuff(d) for d in value):
                    return False
            elif key == 'sanity_min':
                if state.sanity < value:
                    return False
            elif key == 'sanity_max':
                if state.sanity > value:
                    return False
            elif key == 'items_count_min':
                if len(state.items) < value:
                    return False
            elif key == 'abilities_count_min':
                if len(state.abilities) < value:
                    return False
            elif key == 'phase':
                # 精确匹配阶段（支持单个数字或列表）
                if isinstance(value, list):
                    if state.phase not in value:
                        return False
                else:
                    if state.phase != value:
                        return False
            elif key == 'phase_min':
                if state.phase < value:
                    return False
            elif key == 'phase_max':
                if state.phase > value:
                    return False

        return True

    def check_choice_requirements(self, choice: Choice, state) -> bool:
        """检查选项是否可用"""
        return self.check_conditions(choice.requires, state)

    def _get_available_events(self, state, category: str) -> List[Event]:
        """获取指定类型中所有可用的事件"""
        floor = state.floor
        available = []

        for event in self.events_by_category.get(category, []):
            # 检查楼层范围
            if not event.in_floor_range(floor):
                continue
            # 检查触发条件
            if not self.check_conditions(event.conditions, state):
                continue
            # 检查是否已触发（单次事件）
            if event.one_time and state.has_triggered(event.id):
                continue
            # 排除上一个发生的事件（phase3 除外，因为 phase3 的 fixed 事件覆盖多个楼层）
            if state.phase != 3:
                if state.current_event_id and event.id == state.current_event_id:
                    continue
            available.append(event)

        return available

    def draw_event(self, state) -> Optional[Event]:
        """从事件池中抽取一个事件（两阶段选择）"""
        # 优先处理事件链
        if state.pending_event_id:
            event = self.get_event_by_id(state.pending_event_id)
            state.pending_event_id = None
            if event:
                return event
            return self._get_default_event(state)

        # 获取当前楼层的权重配置（根据当前阶段）
        floor = state.floor
        phase = getattr(state, 'phase', 1)
        floor_config = self.get_floor_config(floor, phase)

        # 第一阶段：根据类型权重选择事件类型
        # 构建可用类型及其有效权重（只有存在可用事件的类型才参与）
        category_weights = []
        categories = []

        for category in ['good', 'bad', 'monster', 'normal', 'fixed']:
            weight = floor_config.get(category, 0)
            if weight > 0:
                available = self._get_available_events(state, category)
                if available:  # 只有该类型有可用事件时才加入候选
                    category_weights.append(weight)
                    categories.append(category)

        if not categories:
            return self._get_default_event(state)

        # 加权随机选择类型
        total_weight = sum(category_weights)
        r = random.randint(1, total_weight)
        selected_category = None
        cumulative = 0
        for i, weight in enumerate(category_weights):
            cumulative += weight
            if r <= cumulative:
                selected_category = categories[i]
                break

        # 第二阶段：在选定类型内部，根据事件权重选择具体事件
        available_events = self._get_available_events(state, selected_category)
        if not available_events:
            return self._get_default_event(state)

        # 构建事件权重池
        event_pool = []
        for event in available_events:
            if event.weight > 0:
                event_pool.extend([event] * event.weight)

        if not event_pool:
            return self._get_default_event(state)

        return random.choice(event_pool)

    def _get_default_event(self, state) -> Optional[Event]:
        """获取默认事件（当事件池为空时）"""
        # 从 normal 类型中获取可用事件（考虑楼层、条件、单次触发）
        available = self._get_available_events(state, 'normal')
        if available:
            # 根据权重选择
            event_pool = []
            for event in available:
                if event.weight > 0:
                    event_pool.extend([event] * event.weight)
            if event_pool:
                return random.choice(event_pool)
        return self.get_event_by_id("quiet_corridor")
