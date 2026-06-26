"""
选项处理模块
"""
import random
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from i18n import get_ui_text, set_language
from .game_state import GameState
from .event_pool import Event, Choice


class ChoiceHandler:
    """选项处理器"""

    def __init__(self, state: GameState):
        self.state = state

    def process_choice(self, event: Event, choice_index: int) -> Tuple[bool, str]:
        """
        处理玩家选择
        返回: (是否成功, 消息)
        """
        if choice_index < 0 or choice_index >= len(event.choices):
            return False, get_ui_text("cannot_do_action")

        choice = event.choices[choice_index]

        # 检查选项是否可用
        if not self._check_requirements(choice):
            return False, get_ui_text("requirements_not_met")

        # 记录选择
        self.state.add_choice(choice.text)

        # 标记事件已触发
        self.state.trigger_event(event.id)

        # 处理读取存档（优先级最高，直接返回）
        if choice.load_checkpoint:
            new_state = GameState.load_from_checkpoint(choice.load_checkpoint - 1)
            if new_state:
                self.state.floor_index = new_state.floor_index
                self.state.floor_list = new_state.floor_list
                self.state.items = new_state.items
                self.state.abilities = new_state.abilities
                self.state.sanity = new_state.sanity
                self.state.sanity_max = new_state.sanity_max
                self.state.debuffs = new_state.debuffs
                self.state.triggered_events = new_state.triggered_events
                self.state.choice_history = new_state.choice_history
                self.state.floor_history = new_state.floor_history
                self.state.current_event_id = new_state.current_event_id
                self.state.knock_count = new_state.knock_count
                self.state.phase = new_state.phase
                self.state.game_over = False
                self.state.pending_event_id = new_state.pending_event_id
                return True, get_ui_text("checkpoint_loaded")
            return False, get_ui_text("checkpoint_load_failed")

        # 处理效果
        message = self._apply_effects(choice.effects)

        # 优先级0: 读取存档
        if choice.next_event_id  and choice.next_event_id=='load_checkpoints':
            self.state.pending_event_id = choice.next_event_id
            return True, message

        # 优先级1: 检查敲门次数是否超过12次
        if self.state.knock_count > 12:
            self.state.pending_event_id = 'door_death'
            return True, message

        # 优先级2: 检查理智值是否导致游戏结束
        if self.state.sanity <= 0:
            self.state.pending_event_id = 'sanity_zero_fake_human'
            return True, message

        # 优先级3: 检查回头检测
        if self.state.has_debuff('strange_sound') and self.state.check_returning():
            self.state.pending_event_id = 'strange_sound_death'
            return True, message

        # 优先级4: 设置下一个事件（如果有）
        if choice.next_event_id:
            self.state.pending_event_id = choice.next_event_id

        # 创建存档点（击败怪物，在设置 pending_event_id 之后）
        if choice.add_checkpoint:
            self.state.create_checkpoint(choice.add_checkpoint)

        return True, message

    def _check_requirements(self, choice: Choice) -> bool:
        """检查选项要求"""
        for key, value in choice.requires.items():
            if key == 'has_item':
                if not all(self.state.has_item(item) for item in value):
                    return False
            elif key == 'missing_item':
                if any(self.state.has_item(item) for item in value):
                    return False
            elif key == 'has_ability':
                if not all(self.state.has_ability(ability) for ability in value):
                    return False
            elif key == 'missing_ability':
                if any(self.state.has_ability(ability) for ability in value):
                    return False
            elif key == 'has_debuff':
                if not all(self.state.has_debuff(d) for d in value):
                    return False
            elif key == 'missing_debuff':
                if any(self.state.has_debuff(d) for d in value):
                    return False
            elif key == 'sanity_max':
                if self.state.sanity > value:
                    return False
            elif key == 'sanity_min':
                if self.state.sanity < value:
                    return False
            elif key == 'has_checkpoint':
                if not GameState.has_checkpoints():
                    return False
            elif key == 'checkpoint_count_min':
                if GameState.checkpoint_count() < value:
                    return False
            elif key == 'has_checkpoint_at':
                # 检查指定位置是否有存档（1-based）
                if not GameState.has_checkpoint_at(value - 1):
                    return False
        return True

    def _apply_effects(self, effects: Dict[str, Any]) -> str:
        """应用效果，返回描述消息"""
        messages = []

        for key, value in effects.items():
            if key == 'add_item':
                self.state.add_item(value)
            elif key == 'remove_item':
                if self.state.remove_item(value):
                    messages.append(f"{get_ui_text('lost_item')}: {value}")
            elif key == 'add_ability':
                self.state.add_ability(value)
            elif key == 'sanity':
                # Dedication 能力：理智减少时变为75%
                if value < 0 and self.state.has_ability('Dedication'):
                    value = round(value * 0.75)
                self.state.modify_sanity(value)
            elif key == 'increase_sanity_max':
                self.state.increase_sanity_max(value)
            elif key == 'decrease_sanity_max':
                self.state.decrease_sanity_max(value)
            elif key == 'add_debuff':
                self.state.add_debuff(value)
            elif key == 'remove_debuff':
                self.state.remove_debuff(value)
            elif key == 'clear_debuffs':
                self.state.debuffs.clear()
            elif key == 'go_down':
                self.state.go_down(value)
                messages.append(f"{get_ui_text('floor')}: {self.state.floor}F")

            elif key == 'go_up':
                self.state.go_up(value)
                messages.append(f"{get_ui_text('floor')}: {self.state.floor}F")
            elif key == 'set_floor':
                self.state.set_floor(str(value))
                messages.append(f"{get_ui_text('floor')}: {self.state.floor}F")
            elif key == 'chance':
                # 概率事件，value 包含概率和成功/失败的效果
                pass  # 在 next_event_id 中处理
            elif key == 'game_over':
                self.state.game_over = True
                messages.append(get_ui_text('game_over_restart'))
            elif key == 'win':
                self.state.game_over = True
                messages.append(get_ui_text('game_win'))
            elif key == 'set_phase':
                self.state.set_phase(value)
            elif key == 'knock':
                self.state.knock_count += value
            elif key == 'set_language':
                self.state.set_language(value)
                set_language(value)

            elif key == 'load_checkpoint':
                # 已废弃，使用 choice.load_checkpoint 代替
                pass

        return '\n'.join(messages) if messages else ""

    def get_available_choices(self, event: Event, include_hidden: bool = False) -> list:
        """获取当前事件的可用选项

        Args:
            event: 事件对象
            include_hidden: 是否包含隐藏选项（默认不包含）
        """
        # 如果玩家有 Innovation 能力，自动包含隐藏选项
        if self.state.has_ability('Innovation'):
            include_hidden = True

        available = []
        for i, choice in enumerate(event.choices):
            # 跳过隐藏选项（除非明确要求包含）
            if choice.hidden and not include_hidden:
                continue
            if self._check_requirements(choice):
                available.append((i, choice))
        return available

    def format_choices(self, event: Event) -> str:
        """格式化选项显示"""
        lines = [event.get_translated_description(), ""]
        available = self.get_available_choices(event)

        for display_index, (original_index, choice) in enumerate(available, 1):
            req_text = self._get_requirement_text(choice)
            if req_text:
                lines.append(f"  [{display_index}] {choice.get_translated_text()} ({req_text})")
            else:
                lines.append(f"  [{display_index}] {choice.get_translated_text()}")

        return '\n'.join(lines)

    def get_original_index(self, event: Event, display_index: int) -> int:
        """将显示序号转换为原始索引

        注意：隐藏选项虽然不显示，但玩家仍可通过输入数字选择
        """
        # 获取所有可选选项（包含隐藏选项，用于索引映射）
        all_selectable = self._get_all_selectable_choices(event)

        if display_index < 0 or display_index >= len(all_selectable):
            return -1
        return all_selectable[display_index][0]

    def _get_all_selectable_choices(self, event: Event) -> list:
        """获取所有可选选项（包含隐藏选项，用于索引映射）"""
        available = []
        for i, choice in enumerate(event.choices):
            if self._check_requirements(choice):
                available.append((i, choice))
        return available

    def _get_requirement_text(self, choice: Choice) -> str:
        """获取需求描述文本"""
        reqs = []
        for key, value in choice.requires.items():
            if key == 'has_item':
                reqs.append(f"{get_ui_text('requires_item')}: {', '.join(value)}")
            elif key == 'has_ability':
                reqs.append(f"{get_ui_text('requires_ability')}: {', '.join(value)}")
            elif key == 'has_debuff':
                reqs.append(f"{get_ui_text('requires_debuff')}: {', '.join(value)}")
        return ', '.join(reqs)
