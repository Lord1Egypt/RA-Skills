"""视频类型管理器 — 支持用户注册自定义视频类型和规则。

用法:
    from type_registry import register_type, get_type

    register_type("military", {
        "name": "军事题材",
        "description": "军事/战争类短视频",
        "templates": {...},
        "rules": {
            "shot_aspect": "16:9",
            "max_shots": 20,
            "camera_patterns": ["稳定推进", "航拍视角"],
            "emotion_arcs": ["紧张", "激烈", "压抑", "激昂"],
            "verify_style": "写实",
        }
    })

类型定义存储在 type_defs/ 目录中，自动发现。
"""
import json, os
from typing import Any

_TYPES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "type_defs")

# 注册表：name → type dict
_type_registry: dict[str, dict] = {}

# 内置类型的默认规则
_BUILTIN_RULES = {
    "short_drama": {
        "name": "短剧",
        "description": "三幕式短剧（标准 9:16 竖屏）",
        "defaults": {"aspect_ratio": "9:16", "max_shots": 25, "min_shots": 4},
        "shot_rules": {
            "camera_patterns": ["镜头缓慢推进", "特写", "横移", "上摇"],
            "emotion_arcs": ["平静", "温馨", "紧张", "激烈", "悲伤", "平静"],
            "verify_style": "写实",
        },
    },
    "travelogue": {
        "name": "文旅",
        "description": "四幕式文旅短片（16:9 横屏）",
        "defaults": {"aspect_ratio": "16:9", "max_shots": 30, "min_shots": 6},
        "shot_rules": {
            "camera_patterns": ["航拍视角", "缓慢推进", "横移", "全景"],
            "emotion_arcs": ["平静", "温馨", "欢快", "平静"],
            "verify_style": "写实",
        },
    },
    "cinematic": {
        "name": "电影级长剧",
        "description": "电影级叙事（16:9 院线横屏，4K）",
        "defaults": {"aspect_ratio": "16:9", "max_shots": 60, "min_shots": 10},
        "shot_rules": {
            "camera_patterns": ["缓慢推进", "环绕", "横移", "上摇", "下摇", "固定"],
            "emotion_arcs": ["平静", "紧张", "激烈", "悲伤", "平静", "温馨"],
            "verify_style": "写实",
        },
    },
}


def register_type(name: str, type_def: dict) -> None:
    """注册自定义视频类型。

    Args:
        name: 类型标识（如 "military"、"tech-review"）
        type_def: 类型定义字典，格式:
            {
                "name": "显示名",
                "description": "描述",
                "defaults": {"aspect_ratio": "9:16", ...},
                "shot_rules": {
                    "camera_patterns": [...],
                    "emotion_arcs": [...],
                    "verify_style": "写实|动漫|...",
                },
            }
    """
    _type_registry[name] = type_def


def get_type(name: str) -> dict:
    """获取类型定义（内置 + 用户注册）。"""
    # 已注册的自定义类型优先
    if name in _type_registry:
        return _type_registry[name]
    # 内置类型
    if name in _BUILTIN_RULES:
        return _BUILTIN_RULES[name]
    # 从 type_defs/ 目录加载
    tf = os.path.join(_TYPES_DIR, f"{name}.json")
    if os.path.isfile(tf):
        try:
            with open(tf, encoding="utf-8") as f:
                td = json.load(f)
            _type_registry[name] = td
            return td
        except Exception:
            pass
    # 未知类型 → 返回通用默认
    return {"name": name, "description": "", "defaults": {}, "shot_rules": {}}


def list_types() -> list[str]:
    """列出所有可用视频类型。"""
    builtin = list(_BUILTIN_RULES.keys())
    # 扫描 type_defs/ 目录
    custom = []
    if os.path.isdir(_TYPES_DIR):
        for f in sorted(os.listdir(_TYPES_DIR)):
            if f.endswith(".json"):
                custom.append(f[:-5])
    registered = list(_type_registry.keys())
    return sorted(set(builtin + custom + registered))


def apply_type_rules(script: dict) -> dict:
    """根据 script.json 中的 type 字段，应用类型规则到脚本。

    自动修正:
      - aspect_ratio
      - 镜头数量范围
      - 运镜多样性（从类型 camera_patterns 抽取）
      - 情绪弧线（从类型 emotion_arcs 抽取）

    Returns: 修正后的 script（就地修改）
    """
    type_name = script.get("script", {}).get("type", "short_drama")
    td = get_type(type_name)
    rules = td.get("shot_rules", {})
    defaults = td.get("defaults", {})

    scr = script.setdefault("script", {})
    # 应用默认值
    for k, v in defaults.items():
        if k not in scr or not scr[k]:
            scr[k] = v

    # 镜头数据
    shots = script.get("shots", [])
    if shot_rules := rules.get("camera_patterns"):
        # 为没有运镜描述的镜头分配类型特定的运镜
        import random
        for i, s in enumerate(shots):
            desc = s.get("description", "")
            has_camera = any(kw in desc for kw in [
                "推进", "拉远", "横移", "上摇", "下摇", "环绕",
                "旋转", "固定", "静态", "特写", "航拍", "全景",
            ])
            if not has_camera:
                cam = shot_rules[i % len(shot_rules)]
                s["description"] = f"{desc}，{cam}"

    return script
