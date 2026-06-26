#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Endless Downstairs - Endless Downstairs
Horror-style text adventure game
"""
import sys
import os
import json
import random
from pathlib import Path

# Windows 终端 UTF-8 支持
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from engine import GameState, EventPool, ChoiceHandler
from i18n import get_ui_text, set_language, get_current_language, get_item_text, get_event_text, load_saved_language

# 从配置文件加载保存的语言设置
saved_lang = load_saved_language()
set_language(saved_lang, save=False)


class Game:
    """游戏主类"""

    SAVE_FILE = "save.json"
    ITEMS_FILE = Path(__file__).parent / "data" / "items.json"

    def __init__(self):
        self.state = GameState()
        self.event_pool = EventPool()
        self.handler = None
        self.current_event = None
        self._load_items_data()

    def _load_items_data(self):
        """加载物品数据"""
        with open(self.ITEMS_FILE, 'r', encoding='utf-8') as f:
            self.items_data = {item['id']: item for item in json.load(f)}

    def new_game(self):
        """开始新游戏"""
        # 清空存档点
        GameState.clear_checkpoints()

        # 检查是否已看完开头剧情
        skip_prologue = False
        if os.path.exists(self.SAVE_FILE):
            try:
                old_state = GameState.load(self.SAVE_FILE)
                if "start_4" in old_state.triggered_events:
                    skip_prologue = True
            except Exception:
                pass

        self.state = GameState()
        self.handler = ChoiceHandler(self.state)

        # 从配置文件读取保存的语言设置
        saved_lang = load_saved_language()
        self.state.set_language(saved_lang)

        # 如果已看完开头剧情，直接从 start_choice 开始
        if skip_prologue:
            # 标记开头剧情事件为已触发
            self.state.triggered_events.update(["start_1", "start_2", "start_3", "start_4"])
            self.current_event = self.event_pool.get_event_by_id("start_choice")
        else:
            self.current_event = self.event_pool.get_event_by_id("language_select")

        self.state.current_event_id = self.current_event.id
        self.display_event()
        self.save()

    def load_game(self) -> bool:
        """加载存档"""
        if os.path.exists(self.SAVE_FILE):
            try:
                self.state = GameState.load(self.SAVE_FILE)
                self.handler = ChoiceHandler(self.state)
                return True
            except Exception as e:
                print(f"{get_ui_text('load_failed')}: {e}")
                return False
        return False

    def save(self):
        """保存游戏"""
        self.state.save(self.SAVE_FILE)

    def get_next_event(self):
        """获取下一个事件"""
        self.current_event = self.event_pool.draw_event(self.state)
        self.state.current_event_id = self.current_event.id if self.current_event else None
        return self.current_event

    def display_event(self):
        """显示当前事件"""
        if not self.current_event:
            self.get_next_event()

        if self.current_event:
            print("\n" + self.handler.format_choices(self.current_event))

    def make_choice(self, choice_str: str) -> bool:
        """做出选择，返回是否成功"""
        if self.state.game_over:
            print(get_ui_text("game_over"))
            return False

        if not self.current_event:
            self.get_next_event()

        try:
            display_index = int(choice_str) - 1
        except ValueError:
            print(get_ui_text("invalid_number"))
            return False

        # 将显示序号转换为原始索引
        choice_index = self.handler.get_original_index(self.current_event, display_index)
        if choice_index < 0:
            print(get_ui_text("invalid_choice"))
            return False

        success, message = self.handler.process_choice(self.current_event, choice_index)

        if success:
            if message:
                print(f"\n{message}")

            # 处理概率事件
            if self.current_event and choice_index < len(self.current_event.choices):
                choice = self.current_event.choices[choice_index]
                if 'chance' in choice.effects:
                    chance = choice.effects['chance']
                    success_event_id = choice.effects.get('success_event')
                    fail_event_id = choice.effects.get('fail_event')

                    if random.randint(1, 100) <= chance:
                        if success_event_id:
                            self.state.pending_event_id = success_event_id
                            print(get_ui_text("success"))
                    else:
                        if fail_event_id:
                            self.state.pending_event_id = fail_event_id
                            print(get_ui_text("fail"))

            self.save()

            # 获取下一个事件
            if not self.state.game_over:
                self.get_next_event()
            return True
        else:
            print(message)
            return False

    def show_status(self):
        """显示状态"""
        print(self.state.get_status_text())

    def show_inventory(self):
        """显示物品详情"""
        if not self.state.items:
            print(get_ui_text("no_items"))
            return

        print(f"\n=== {get_ui_text('item_details')} ===")
        for item_id in self.state.items:
            item = self.items_data.get(item_id)
            if item:
                print(f"\n【{item['name']}】{item['description']}\n")

    def show_help(self):
        """显示帮助"""
        help_text = f"""
{get_ui_text('help_commands')}
  new         - {get_ui_text('help_new')}
  choose N    - {get_ui_text('help_choose')}
  status      - {get_ui_text('help_status')}
  inventory   - {get_ui_text('help_inventory')}
  continue    - {get_ui_text('help_continue')}
  input <text> - {get_ui_text('help_input')}
  help        - {get_ui_text('help_help')}
  quit        - {get_ui_text('help_quit')}
"""
        print(help_text)

def main():
    """主入口"""
    game = Game()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'new':
            game.new_game()
            game.save()
        elif command == 'choose':
            if len(sys.argv) > 2:
                if game.load_game():
                    game.handler = ChoiceHandler(game.state)
                    # 从存档恢复当前事件
                    if game.state.current_event_id:
                        game.current_event = game.event_pool.get_event_by_id(game.state.current_event_id)
                    success = game.make_choice(sys.argv[2])
                    if success and not game.state.game_over:
                        game.display_event()
                    game.save()
            else:
                print(get_ui_text("usage_choose"))
        elif command == 'status':
            if game.load_game():
                game.show_status()
            else:
                print(get_ui_text("no_save"))
        elif command == 'inventory':
            if game.load_game():
                game.show_inventory()
            else:
                print(get_ui_text("no_save"))
        elif command == 'continue':
            if game.load_game():
                game.handler = ChoiceHandler(game.state)
                game.get_next_event()
                game.display_event()
            else:
                print(get_ui_text("no_save_new"))
        elif command == 'lang':
            # 语言切换命令
            if len(sys.argv) > 2:
                lang = sys.argv[2]
                if lang in ['zh', 'en']:
                    if game.load_game():
                        game.state.set_language(lang)
                        game.save()
                    else:
                        set_language(lang)
                    print(f"Language set to: {lang}")
                else:
                    print("Usage: python game.py lang [zh|en]")
            else:
                print(f"Current language: {get_current_language()}")
                print("Usage: python game.py lang [zh|en]")
        elif command == 'input':
            if len(sys.argv) > 2:
                if game.load_game():
                    # 检查上一个事件是否是 final_2
                    if game.state.current_event_id != "final_2" and game.state.current_event_id != "final_3":
                        print(get_ui_text("cannot_do"))
                    else:
                        game.handler = ChoiceHandler(game.state)
                        text = sys.argv[2]
                        if text.lower() == "coding":
                            target_event = "final_4"
                        else:
                            target_event = "final_3"
                        game.current_event = game.event_pool.get_event_by_id(target_event)
                        game.state.current_event_id = target_event
                        game.display_event()
                        game.save()
                else:
                    print(get_ui_text("no_save"))
            else:
                print(get_ui_text("usage_input"))
        else:
            print(f"{get_ui_text('unknown_command')}: {command}")
            print(get_ui_text("usage"))
    else:
        # 无参数时显示当前状态，不进入交互模式
        if game.load_game():
            game.handler = ChoiceHandler(game.state)
            game.show_status()
            if game.state.current_event_id:
                game.display_event()
        else:
            game.new_game()
            game.save()


if __name__ == '__main__':
    import random
    main()
