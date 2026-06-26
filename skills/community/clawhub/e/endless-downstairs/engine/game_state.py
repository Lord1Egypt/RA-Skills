"""
游戏状态管理模块
"""
import json
from dataclasses import dataclass, field
from typing import Set, List, Optional
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from i18n import get_ui_text, get_current_language, set_language


# 存档系统常量
CHECKPOINTS_FILE = "checkpoints.json"
MONSTER_CHECKPOINT_INDEX = {
    '末影人': 0,
    '恶灵': 1,
    '伪人': 2
}


def _default_floor_list() -> List[str]:
    """默认楼层列表 (0-25层，7楼缺失)"""
    return [str(i) for i in range(26) if i != 7]


def _load_floors_data() -> dict:
    """加载floors.json数据"""
    filepath = Path(__file__).parent.parent / 'data' / 'floors.json'
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def _get_floor_list_for_phase(phase: int) -> List[str]:
    """获取指定阶段的楼层列表"""
    floors_data = _load_floors_data()
    phase_key = f"phase{phase}"
    if phase_key in floors_data:
        phase_data = floors_data[phase_key]
        # 提取楼层号并按数值排序
        floor_nums = [int(k) for k in phase_data.keys() if k.isdigit() or (k.startswith('-') and k[1:].isdigit())]
        floor_nums.sort()
        return [str(f) for f in floor_nums]
    return _default_floor_list()


@dataclass
class GameState:
    """玩家游戏状态"""
    floor_index: int = 12              # 当前楼层索引（index=12代表13楼）
    floor_list: List[str] = field(default_factory=_default_floor_list)  # 楼层列表（支持不连续）
    items: Set[str] = field(default_factory=set)           # 已收集物品
    abilities: Set[str] = field(default_factory=set)       # 已获得能力
    sanity: int = 70                   # 理智值
    sanity_max: int = 100              # 理智值上限
    debuffs: List[str] = field(default_factory=list)       # 负面状态
    triggered_events: Set[str] = field(default_factory=set)  # 已触发事件
    choice_history: List[str] = field(default_factory=list)  # 选择历史
    floor_history: List[int] = field(default_factory=list)  # 楼层索引历史（用于回头检测）
    pending_event_id: Optional[str] = None   # 待触发的事件ID（事件链）
    current_event_id: Optional[str] = None   # 当前事件ID
    game_over: bool = False            # 游戏是否结束
    phase: int = 1                     # 游戏阶段（1-3）
    knock_count: int = 1               # 敲门次数（隐藏属性，13次触发结局）
    language: str = 'zh'               # 游戏语言

    def set_language(self, lang: str):
        """设置游戏语言"""
        if lang in ['zh', 'en']:
            self.language = lang
            set_language(lang)

    @property
    def floor(self) -> str:
        """获取当前楼层（字符串）"""
        return self.floor_list[self.floor_index]

    def add_item(self, item_id: str) -> bool:
        """添加物品"""
        if item_id not in self.items:
            self.items.add(item_id)
            return True
        return False

    def remove_item(self, item_id: str) -> bool:
        """移除物品"""
        if item_id in self.items:
            self.items.remove(item_id)
            return True
        return False

    def has_item(self, item_id: str) -> bool:
        """检查是否拥有物品"""
        return item_id in self.items

    def add_ability(self, ability_id: str) -> bool:
        """添加能力"""
        if ability_id not in self.abilities:
            self.abilities.add(ability_id)
            return True
        return False

    def has_ability(self, ability_id: str) -> bool:
        """检查是否拥有能力"""
        return ability_id in self.abilities

    def add_debuff(self, debuff_id: str) -> bool:
        """添加负面状态"""
        if debuff_id not in self.debuffs:
            self.debuffs.append(debuff_id)
            return True
        return False

    def remove_debuff(self, debuff_id: str) -> bool:
        """移除负面状态"""
        if debuff_id in self.debuffs:
            self.debuffs.remove(debuff_id)
            return True
        return False

    def has_debuff(self, debuff_id: str) -> bool:
        """检查是否有负面状态"""
        return debuff_id in self.debuffs

    def modify_sanity(self, amount: int) -> int:
        """修改理智值，返回实际变化量"""
        old_sanity = self.sanity
        self.sanity = max(0, min(self.sanity_max, self.sanity + amount))
        return self.sanity - old_sanity

    def increase_sanity_max(self, amount: int) -> int:
        """增加理智值上限，返回实际上限变化量"""
        old_max = self.sanity_max
        self.sanity_max += amount
        return self.sanity_max - old_max

    def decrease_sanity_max(self, amount: int) -> int:
        """减少理智值上限（最低为1），返回实际上限变化量"""
        old_max = self.sanity_max
        self.sanity_max = max(1, self.sanity_max - amount)
        # 如果当前理智超过新上限，则降低到上限
        if self.sanity > self.sanity_max:
            self.sanity = self.sanity_max
        return old_max - self.sanity_max

    def trigger_event(self, event_id: str):
        """记录已触发事件"""
        self.triggered_events.add(event_id)

    def has_triggered(self, event_id: str) -> bool:
        """检查事件是否已触发"""
        return event_id in self.triggered_events

    def add_choice(self, choice_text: str):
        """记录选择历史"""
        self.choice_history.append(f"[{self.floor}F] {choice_text}")

    def go_down(self, floors: int = 1) -> str:
        """下楼，返回新楼层"""
        old_index = self.floor_index
        self.floor_index = max(0, self.floor_index - floors)
        self.floor_history.append(old_index)
        return self.floor

    def go_up(self, floors: int = 1) -> str:
        """上楼，返回新楼层"""
        old_index = self.floor_index
        self.floor_index = min(len(self.floor_list) - 1, self.floor_index + floors)
        self.floor_history.append(old_index)
        return self.floor

    def set_floor(self, num: int) -> str:
        """直接传送到指定楼层号，不存在则保持当前楼层"""
        key = str(num)
        if key in self.floor_list:
            old_index = self.floor_index
            self.floor_index = self.floor_list.index(key)
            self.floor_history.append(old_index)
        return self.floor

    def check_returning(self) -> bool:
        """检查是否回到了刚走过的楼层"""
        if len(self.floor_history) < 2:
            return False
        return self.floor_index == self.floor_history[-2]

    def set_phase(self, new_phase: int) -> bool:
        """设置游戏阶段，返回是否成功切换"""
        if new_phase < 1 or new_phase > 3 or new_phase == self.phase:
            return False

        self.phase = new_phase

        # 获取新阶段的楼层列表
        new_floor_list = _get_floor_list_for_phase(new_phase)
        if not new_floor_list:
            return False

        # 保存当前楼层号
        current_floor = self.floor

        # 更新楼层列表
        self.floor_list = new_floor_list

        # 尝试保持当前楼层位置
        if current_floor in self.floor_list:
            self.floor_index = self.floor_list.index(current_floor)
        else:
            # 当前楼层不存在于新阶段，重置到起始位置
            self.floor_index = 12

        return True

    # ==================== 存档系统 ====================

    @classmethod
    def _load_checkpoints(cls) -> List[dict]:
        """加载所有存档"""
        if Path(CHECKPOINTS_FILE).exists():
            try:
                with open(CHECKPOINTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    @classmethod
    def _save_checkpoints(cls, checkpoints: List[dict]):
        """保存所有存档"""
        with open(CHECKPOINTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(checkpoints, f, ensure_ascii=False, indent=2)

    def create_checkpoint(self, monster_name: str = "") -> bool:
        """创建存档点，根据怪物名称固定位置，返回是否成功创建"""
        # 获取该怪物对应的存档索引
        index = MONSTER_CHECKPOINT_INDEX.get(monster_name)
        if index is None:
            return False

        checkpoints = self._load_checkpoints()

        # 完整拷贝当前游戏状态（与 save.json 结构一致）
        checkpoint = self.to_dict()
        checkpoint['monster_name'] = monster_name

        # 确保列表足够长
        while len(checkpoints) <= index:
            checkpoints.append(None)

        # 更新对应位置的存档
        checkpoints[index] = checkpoint
        self._save_checkpoints(checkpoints)
        return True

    @classmethod
    def get_checkpoints(cls) -> List[dict]:
        """获取所有存档（过滤掉 None）"""
        return [cp for cp in cls._load_checkpoints() if cp is not None]

    @classmethod
    def has_checkpoints(cls) -> bool:
        """检查是否有存档"""
        return any(cp is not None for cp in cls._load_checkpoints())

    @classmethod
    def checkpoint_count(cls) -> int:
        """获取有效存档数量"""
        return sum(1 for cp in cls._load_checkpoints() if cp is not None)

    @classmethod
    def has_checkpoint_at(cls, index: int) -> bool:
        """检查指定位置是否有存档"""
        checkpoints = cls._load_checkpoints()
        return index < len(checkpoints) and checkpoints[index] is not None

    @classmethod
    def clear_checkpoints(cls):
        """清空所有存档"""
        cls._save_checkpoints([])

    @classmethod
    def load_from_checkpoint(cls, index: int) -> Optional['GameState']:
        """从存档点加载，返回新的 GameState"""
        checkpoints = cls._load_checkpoints()
        if index < 0 or index >= len(checkpoints):
            return None

        checkpoint = checkpoints[index]

        # 使用 from_dict 完整恢复状态
        state = cls.from_dict(checkpoint)
        state.game_over = False  # 加载后重置游戏结束状态

        # 保留该存档及之前的所有存档，删除之后的存档
        cls._save_checkpoints(checkpoints[:index + 1])

        return state

    def to_dict(self) -> dict:
        """序列化为字典"""
        return {
            'floor_index': self.floor_index,
            'floor_list': self.floor_list,
            'items': list(self.items),
            'abilities': list(self.abilities),
            'sanity': self.sanity,
            'sanity_max': self.sanity_max,
            'debuffs': self.debuffs,
            'triggered_events': list(self.triggered_events),
            'choice_history': self.choice_history,
            'floor_history': self.floor_history,
            'pending_event_id': self.pending_event_id,
            'current_event_id': self.current_event_id,
            'game_over': self.game_over,
            'phase': self.phase,
            'knock_count': self.knock_count,
            'language': self.language
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GameState':
        """从字典反序列化"""
        state = cls(
            floor_index=data.get('floor_index', 13),
            floor_list=data.get('floor_list', _default_floor_list()),
            items=set(data.get('items', [])),
            abilities=set(data.get('abilities', [])),
            sanity=data.get('sanity', 100),
            sanity_max=data.get('sanity_max', 100),
            debuffs=data.get('debuffs', []),
            triggered_events=set(data.get('triggered_events', [])),
            choice_history=data.get('choice_history', []),
            floor_history=data.get('floor_history', []),
            pending_event_id=data.get('pending_event_id'),
            current_event_id=data.get('current_event_id'),
            game_over=data.get('game_over', False),
            phase=data.get('phase', 1),
            knock_count=data.get('knock_count', 0)
        )
        # 恢复语言设置
        lang = data.get('language', 'zh')
        state.language = lang
        set_language(lang)
        return state

    def save(self, filepath: str):
        """保存状态到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, filepath: str) -> 'GameState':
        """从文件加载状态"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_dict(json.load(f))

    def get_status_text(self) -> str:
        """获取状态文本描述，理智值隐藏"""
        lines = [
            f"{get_ui_text('status_title')}",
            f"{get_ui_text('status_floor')}: {self.floor}F",
            f"{get_ui_text('status_items')} ({len(self.items)}): {', '.join(self.items) if self.items else get_ui_text('status_none')}",
            f"{get_ui_text('status_abilities')} ({len(self.abilities)}): {', '.join(self.abilities) if self.abilities else get_ui_text('status_none')}",
        ]
        # 理智状态描述
        if self.sanity > 85:
            sanity_desc = get_ui_text('sanity_stable')
        elif self.sanity > 60:
            sanity_desc = get_ui_text('sanity_unstable')
        elif self.sanity > 35:
            sanity_desc = get_ui_text('sanity_damaged')
        else:
            sanity_desc = get_ui_text('sanity_collapsing')
        lines.append(f"{sanity_desc}")
        lines.append(f"\n{get_ui_text('advice_title')}\n{get_ui_text('advice_full')}\n")
        return '\n'.join(lines)
