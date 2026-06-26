"""游戏模块包 — 每个游戏独立文件，提供初始化/动作解析/胜负判定"""

from .rpg import init as rpg_init, resolve as rpg_resolve, check_win as rpg_check
from .werewolf import init as ww_init, resolve as ww_resolve, check_win as ww_check
from .story_relay import init as sr_init, resolve as sr_resolve, check_win as sr_check
from .ctf import init as ctf_init, resolve as ctf_resolve, check_win as ctf_check
from .civilization import init as civ_init, resolve as civ_resolve, check_win as civ_check

GAMES = {
    "rpg": {
        "name": "文字冒险",
        "min_players": 1,
        "max_players": 20,
        "init": rpg_init,
        "resolve": rpg_resolve,
        "check_win": rpg_check,
    },
    "werewolf": {
        "name": "狼人杀",
        "min_players": 6,
        "max_players": 18,
        "init": ww_init,
        "resolve": ww_resolve,
        "check_win": ww_check,
    },
    "story_relay": {
        "name": "小说接龙",
        "min_players": 2,
        "max_players": 10,
        "init": sr_init,
        "resolve": sr_resolve,
        "check_win": sr_check,
    },
    "ctf": {
        "name": "夺旗战",
        "min_players": 1,
        "max_players": 20,
        "init": ctf_init,
        "resolve": ctf_resolve,
        "check_win": ctf_check,
    },
    "civilization": {
        "name": "文明模拟",
        "min_players": 2,
        "max_players": 8,
        "init": civ_init,
        "resolve": civ_resolve,
        "check_win": civ_check,
    },
}
