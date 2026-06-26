#!/usr/bin/env python3
"""Render wedding package templates into a standard prompt package."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGES_DIR = ROOT / "assets" / "packages"

SCENE_PRESETS = {
    "mountain": {
        "summary_note": "整体表达已偏向山地自然光婚纱摄影，强调晨光、地形层次与远景环境叙事。",
        "prompt_note": "画面重点转向山地环境、云雾层次、草坡地形与自然光下的纵深感。",
        "frame_hint": "构图更强调自然地貌、远景呼吸感与环境叙事。",
    },
    "beach": {
        "summary_note": "整体表达已偏向海边婚纱摄影，强调海风、海平线、湿沙反光与更松弛的互动感。",
        "prompt_note": "画面重点转向海风动态、海岸线节奏、湿沙反光与落日海景氛围。",
        "frame_hint": "构图更强调海岸线、人物走动与轻盈自然的海边互动。",
    },
    "studio": {
        "summary_note": "整体表达已偏向棚拍婚纱肖像，强调布光控制、主体塑形与画面秩序感。",
        "prompt_note": "画面重点转向棚灯塑形、人物姿态控制、背景秩序与正式肖像表达。",
        "frame_hint": "构图更强调主体控制、姿态稳定与背景层次的可控性。",
    },
    "chinese_traditional": {
        "summary_note": "整体表达已偏向中式礼仪婚纱照，强调东方秩序感、服饰纹样与克制庄重的情绪。",
        "prompt_note": "画面重点转向中式礼仪气质、服饰刺绣细节、头饰结构与庄重仪式感。",
        "frame_hint": "构图更强调对称、礼仪姿态与东方审美中的稳定秩序。",
    },
}

SCENE_KEYWORDS = {
    "mountain": ["山", "山地", "山坡", "草坡", "云雾", "日照金山", "晨光", "山体", "远山"],
    "beach": ["海", "海边", "海岸", "海风", "沙滩", "湿沙", "海浪", "海平线", "晚霞"],
    "studio": ["影棚", "棚拍", "布光", "背景层", "屏风", "案几", "棚灯"],
    "chinese_traditional": ["中式", "秀禾", "凤冠", "团扇", "婚书", "礼仪", "刺绣"],
}

SCENE_DEFAULTS = {
    "beach": {
        "scene_location": {"country": "中国", "province": "海南", "city": "三亚", "spot": "海边沙滩"},
        "summary_style": "高端海边婚纱照套系",
        "summary_features": "强调海风、海平线、湿沙反光与情侣间松弛自然的亲密互动，适合输出具有度假婚礼感、自由浪漫气质与轻奢海岛氛围的成组作品。",
        "time": "黄昏日落时段",
        "effect": "落日余晖映照海面与湿沙反光",
        "lighting": ["夕阳侧逆光", "温暖轮廓光", "柔和海面反射光"],
        "color_temperature": "5200K",
        "tone": ["温暖", "轻盈", "通透", "自由"],
        "camera_body": "Canon EOS R5",
        "lens": "50mm prime lens, f/1.4",
        "image_style": ["natural shallow depth of field", "balanced environmental context", "soft highlight rolloff", "realistic skin texture", "elegant fabric detail"],
        "mood_keywords": ["浪漫", "自由", "轻盈", "海岛度假感", "自然亲密"],
        "location_defaults": {
            "foreground": "细白沙滩与湿润沙面反光",
            "midground": "海风吹动头纱与裙摆的情侣互动区",
            "background": "海平线、晚霞与蓝绿色海面",
        },
        "wardrobe_defaults": {
            "bride": {"makeup": "通透精致的海岛婚礼妆", "hair": "自然披发或低扎发，带轻微海风吹拂感", "dress": "象牙白缎面鱼尾婚纱", "veil": "轻盈长款薄纱头纱"},
            "groom": {"hair_policy": "保持原图发型", "suit": "米白色定制西装", "shirt": "白色衬衫", "bow_tie": "无领结，整体更自然高级"},
        },
        "props_defaults": {"bouquet": {"description": "白色与浅香槟色玫瑰搭配少量绿色叶材的海边婚礼手捧花"}},
        "negative_prompt": "lowres, blurry face, asymmetrical eyes, distorted hands, extra fingers, broken wrists, warped veil, deformed wedding dress, unnatural wet sand reflection, broken waves, bad feet, incorrect shoreline perspective, stiff pose, awkward expression, over-retouched skin, duplicated person, mismatched gaze, oversaturated sunset, cheap travel-photo look, cartoon style, low-detail fabric, incorrect body ratio, messy wind-blown hair, unnatural sea background",
    },
    "mountain": {
        "scene_location": {"country": "中国", "province": "云南", "city": "大理", "spot": "苍山草坡"},
        "summary_style": "高端山地自然光婚纱照套系",
        "summary_features": "强调晨光、山体层次、云雾与开阔远景中的真实亲密互动，适合输出具有电影感、自然纪实感与主海报气质的成组作品。",
        "time": "日出黄金时段",
        "effect": "晨光照亮山体与云雾层次",
        "lighting": ["柔和逆光", "金色轮廓光", "阴影柔和"],
        "color_temperature": "5500K",
        "tone": ["温暖", "通透", "高级", "电影感"],
        "camera_body": "Canon EOS R5",
        "lens": "85mm prime lens, f/1.8",
        "image_style": ["subject tack sharp", "shallow depth of field", "creamy bokeh background", "subtle 35mm film grain", "realistic skin texture"],
        "mood_keywords": ["浪漫", "真实幸福", "自然亲密", "高级", "电影感"],
        "location_defaults": {
            "foreground": "自然草坡与起伏地形",
            "midground": "山间云雾与情侣互动区",
            "background": "远山轮廓与晨光天空",
        },
        "wardrobe_defaults": {
            "bride": {"makeup": "精致自然婚礼妆", "hair": "长波浪卷发", "dress": "无肩带白色蕾丝蓬蓬婚纱", "veil": "长款刺绣头纱"},
            "groom": {"hair_policy": "保持原图发型", "suit": "黑色定制西装", "shirt": "白色衬衫", "bow_tie": "黑色领结"},
        },
        "props_defaults": {"bouquet": {"description": "15朵浅粉色玫瑰搭配绿叶组成的手捧花"}},
        "negative_prompt": "lowres, blurry face, asymmetrical eyes, distorted hands, extra fingers, fused arms, broken bouquet, deformed wedding dress, bad veil structure, unrealistic anatomy, stiff pose, awkward expression, over-retouched skin, heavy makeup, duplicated person, mismatched gaze, bad perspective, warped background, oversaturated colors, fake smile, cheap travel-photo look, cartoon style, low-detail fabric, incorrect body ratio",
    },
    "studio": {
        "scene_location": {"country": "中国", "province": "高定影棚", "city": "室内棚拍场景", "spot": "极简背景层"},
        "summary_style": "高端影棚婚纱肖像套系",
        "summary_features": "强调布光控制、主体塑形、背景秩序与正式肖像感，适合输出具有杂志封面气质与稳定高级感的棚拍作品。",
        "time": "棚拍控制光环境",
        "effect": "棚灯塑形与背景层次分离",
        "lighting": ["soft studio key light", "gentle front-side lighting", "layered background light"],
        "color_temperature": "4300K",
        "tone": ["克制", "正式", "精致", "高级"],
        "camera_body": "Canon EOS R5",
        "lens": "85mm prime lens, f/1.8",
        "image_style": ["controlled studio depth of field", "subject tack sharp", "clean background hierarchy", "realistic skin texture", "premium portrait finish"],
        "mood_keywords": ["端庄", "克制", "正式", "高级肖像感", "仪式感"],
        "location_defaults": {
            "foreground": "干净棚拍地面与少量前景层次",
            "midground": "情侣主体与正式姿态区域",
            "background": "背景层、屏风或简洁影棚布景",
        },
        "wardrobe_defaults": {
            "bride": {"makeup": "精致高级婚礼妆", "hair": "利落盘发或柔顺披发", "dress": "高定缎面或蕾丝主婚纱", "veil": "精致长头纱"},
            "groom": {"hair_policy": "保持原图发型", "suit": "黑色或白色高定西装", "shirt": "正式衬衫", "bow_tie": "简洁领结或无领结"},
        },
        "props_defaults": {"bouquet": {"description": "克制高级的白色系婚礼手捧花"}},
        "negative_prompt": "lowres, blurry face, asymmetrical eyes, distorted hands, extra fingers, broken wrists, warped veil, deformed dress structure, cheap backdrop, stage-light look, plastic skin, stiff pose, awkward expression, duplicated person, mismatched gaze, low-detail fabric, messy background clutter, cartoon style, incorrect body ratio",
    },
    "chinese_traditional": {
        "scene_location": {"country": "中国", "province": "中式影棚", "city": "室内礼仪场景", "spot": "中式婚礼布景"},
        "summary_style": "高端中式婚礼样片套系",
        "summary_features": "强调东方秩序感、礼仪感、服饰纹样与克制庄重的情绪，适合输出精品中式婚礼样片与秀禾写真。",
        "time": "中式棚拍控制光环境",
        "effect": "庄重暖光与服饰纹样层次表现",
        "lighting": ["soft studio key light", "warm front-side lighting", "controlled background separation"],
        "color_temperature": "4300K",
        "tone": ["庄重", "喜庆", "典雅", "东方气质"],
        "camera_body": "Canon EOS R5",
        "lens": "85mm prime lens, f/1.8",
        "image_style": ["rich embroidery detail", "controlled studio depth of field", "subject tack sharp", "realistic skin texture", "premium red and gold fabric rendering"],
        "mood_keywords": ["庄重", "含蓄喜悦", "礼仪感", "东方典雅", "高级"],
        "location_defaults": {
            "foreground": "案几、红绸与服饰下摆层次",
            "midground": "人物主体与团扇婚书等动作元素",
            "background": "中式屏风、背景层与克制喜字元素",
        },
        "wardrobe_defaults": {
            "bride": {"makeup": "精致东方婚礼妆，强调端庄与通透肤感", "hair": "中式低盘发或传统盘发，搭配凤冠或中式金饰头饰", "dress": "红金色刺绣秀禾服", "veil": "无西式头纱，使用中式头饰体系"},
            "groom": {"hair_policy": "保持原图发型，整体利落正式", "suit": "红金色中式男款礼服", "shirt": "中式内搭领口结构", "bow_tie": "无领结，采用中式礼服完整造型"},
        },
        "props_defaults": {"fan": {"description": "小型中式团扇或绣面折扇"}, "marriage_document": {"description": "传统婚书或红色卷轴式喜庆文书"}},
        "negative_prompt": "lowres, blurry face, asymmetrical eyes, distorted hands, extra fingers, broken wrists, warped embroidery, deformed headdress, messy gold ornament, cheap banquet backdrop, stage-light look, over-saturated red, plastic skin, stiff western pose, vulgar expression, duplicated person, mismatched gaze, low-detail fabric, broken sleeve structure, cartoon style, incorrect body ratio, messy background clutter",
    },
}

FRAME_REWRITES = {
    "studio": [
        {
            "match": ["行走", "踏浪", "海岸", "海风", "抓拍", "回头", "海边"],
            "name": "正式棚拍肖像",
            "purpose": "用于强化棚拍主肖像、布光塑形与稳定构图",
            "prompt": "拍摄一张正式棚拍婚纱肖像。情侣以稳定站姿或坐姿出镜，人物关系自然亲近但不过分夸张，重点突出受控布光、正式姿态、服装质地与背景秩序，整体呈现高级影棚婚纱摄影的干净、集中与精致感。",
        }
    ],
    "chinese_traditional": [
        {
            "match": ["行走", "踏浪", "海岸", "海风", "抓拍", "回头", "海边", "头纱"],
            "name": "中式礼仪肖像",
            "purpose": "用于强化中式礼仪感、服饰细节与克制庄重的姿态表达",
            "prompt": "拍摄一张中式礼仪婚纱肖像。情侣以克制稳定的站姿或并肩构图出镜，新娘可持团扇或婚书，新郎保持守护式姿态。重点表现秀禾或中式礼服纹样、头饰结构、面部神态与东方秩序感，整体庄重、典雅、具有精品中式样片气质。",
        }
    ],
}


def load_package(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Package file is not a mapping: {path}")
    return data


def resolve_package(package_ref: str) -> Path:
    candidate = Path(package_ref)
    if candidate.is_file():
        return candidate

    if candidate.suffix:
        direct = PACKAGES_DIR / candidate.name
        if direct.is_file():
            return direct
    else:
        for option in (f"{package_ref}.yml", f"{package_ref}.yaml"):
            direct = PACKAGES_DIR / option
            if direct.is_file():
                return direct

    matches = sorted(PACKAGES_DIR.glob(f"{package_ref}*.y*ml"))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise ValueError(f"Ambiguous package reference '{package_ref}': {names}")

    raise FileNotFoundError(f"Could not find package '{package_ref}'")


def parse_scalar(value: str) -> Any:
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def set_nested_value(data: dict[str, Any], dotted_path: str, raw_value: str) -> None:
    parts = dotted_path.split(".")
    target: Any = data
    for part in parts[:-1]:
        if isinstance(target, list):
            index = int(part)
            target = target[index]
            continue
        next_target = target.get(part)
        if next_target is None:
            next_target = {}
            target[part] = next_target
        target = next_target
    leaf = parts[-1]
    value = parse_scalar(raw_value)
    if isinstance(target, list):
        target[int(leaf)] = value
    else:
        target[leaf] = value


def apply_overrides(package: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    updated = copy.deepcopy(package)
    for override in overrides:
        if "=" not in override:
            raise ValueError(f"Invalid override '{override}'. Expected path=value")
        path, raw_value = override.split("=", 1)
        set_nested_value(updated, path, raw_value)
    return updated


def replace_terms(text: str, replacements: list[tuple[str, str]]) -> str:
    updated = text
    for old, new in replacements:
        if old:
            updated = updated.replace(old, new)
    return updated


def apply_smart_adaptations(original: dict[str, Any], package: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    updated = copy.deepcopy(package)
    override_paths = {item.split("=", 1)[0] for item in overrides if "=" in item}

    original_camera = original.get("camera_language", {}) if isinstance(original.get("camera_language"), dict) else {}
    current_camera = updated.get("camera_language", {}) if isinstance(updated.get("camera_language"), dict) else {}
    original_wardrobe = original.get("wardrobe", {}) if isinstance(original.get("wardrobe"), dict) else {}
    current_wardrobe = updated.get("wardrobe", {}) if isinstance(updated.get("wardrobe"), dict) else {}

    text_fields = ["summary", "base_prompt", "negative_prompt"]
    frame_fields = ["name", "purpose", "prompt"]
    target_scene_type = infer_scene_type(updated, override_paths)

    scene_type_only = "scene_type" in override_paths and not any(path.startswith("location.") for path in override_paths)
    if target_scene_type and (
        any(path.startswith("location.") for path in override_paths)
        or "scene_type" in override_paths
    ):
        rewrite_package_for_scene(updated, target_scene_type, force_scene_location=scene_type_only)

    if any(path.startswith("camera_language.lens") for path in override_paths):
        old_lens = str(original_camera.get("lens", ""))
        new_lens = str(current_camera.get("lens", ""))
        if old_lens and new_lens and old_lens != new_lens:
            replacements = [(old_lens, new_lens)]
            for field in text_fields:
                if isinstance(updated.get(field), str):
                    updated[field] = replace_terms(updated[field], replacements)
            frames = updated.get("frames", [])
            for frame in frames:
                if isinstance(frame, dict):
                    for field in frame_fields:
                        if isinstance(frame.get(field), str):
                            frame[field] = replace_terms(frame[field], replacements)

            lens_lower = new_lens.lower()
            if "35mm" in lens_lower:
                updated["summary"] = append_note(updated.get("summary", ""), "镜头语言偏向更强的环境叙事与纪实感。")
            elif "85mm" in lens_lower:
                updated["summary"] = append_note(updated.get("summary", ""), "镜头语言偏向更集中的肖像表现与服装细节刻画。")

    if any(path.startswith("wardrobe.") for path in override_paths):
        wardrobe_pairs = collect_wardrobe_replacements(original_wardrobe, current_wardrobe)
        for field in text_fields:
            if isinstance(updated.get(field), str):
                updated[field] = replace_terms(updated[field], wardrobe_pairs)
        frames = updated.get("frames", [])
        for frame in frames:
            if isinstance(frame, dict):
                for field in frame_fields:
                    if isinstance(frame.get(field), str):
                        frame[field] = replace_terms(frame[field], wardrobe_pairs)

    scene_type = target_scene_type
    if isinstance(scene_type, str) and scene_type in SCENE_PRESETS:
        preset = SCENE_PRESETS[scene_type]
        updated["summary"] = append_note(updated.get("summary", ""), preset["summary_note"])
        updated["base_prompt"] = append_note(updated.get("base_prompt", ""), preset["prompt_note"])
        frames = updated.get("frames", [])
        for frame in frames:
            if isinstance(frame, dict):
                frame["purpose"] = append_note(str(frame.get("purpose", "")), preset["frame_hint"])
        apply_frame_rewrites(updated, scene_type)

    updated["summary"] = clean_spacing(updated.get("summary", ""))
    updated["base_prompt"] = clean_spacing(updated.get("base_prompt", ""))
    updated["negative_prompt"] = clean_spacing(updated.get("negative_prompt", ""))
    frames = updated.get("frames", [])
    for frame in frames:
        if isinstance(frame, dict):
            for field in frame_fields:
                if isinstance(frame.get(field), str):
                    frame[field] = clean_spacing(frame[field])

    return updated


def apply_frame_rewrites(package: dict[str, Any], scene_type: str) -> None:
    rewrites = FRAME_REWRITES.get(scene_type, [])
    if not rewrites:
        return
    frames = package.get("frames", [])
    for frame in frames:
        if not isinstance(frame, dict):
            continue
        combined = " ".join(str(frame.get(key, "")) for key in ("name", "purpose", "prompt"))
        for rewrite in rewrites:
            if any(keyword in combined for keyword in rewrite["match"]):
                frame["name"] = rewrite["name"]
                frame["purpose"] = rewrite["purpose"]
                frame["prompt"] = rewrite["prompt"]
                break


def infer_scene_type(package: dict[str, Any], override_paths: set[str]) -> str | None:
    explicit = package.get("scene_type")
    if isinstance(explicit, str) and explicit in SCENE_PRESETS:
        return explicit

    location = package.get("location")
    if isinstance(location, dict):
        location_text = " ".join(str(value) for value in location.values() if isinstance(value, str))
        keyword_priority = [
            ("beach", ["海", "沙滩", "海边", "海岸", "海平线"]),
            ("studio", ["影棚", "棚拍", "室内"]),
            ("chinese_traditional", ["中式", "秀禾", "凤冠"]),
            ("mountain", ["山", "草坡", "云雾", "远山"]),
        ]
        for scene_type, keywords in keyword_priority:
            if any(keyword in location_text for keyword in keywords):
                return scene_type

    haystacks = []
    summary = package.get("summary")
    base_prompt = package.get("base_prompt")
    if isinstance(summary, str):
        haystacks.append(summary)
    if isinstance(base_prompt, str):
        haystacks.append(base_prompt)
    if isinstance(location, dict):
        haystacks.extend(str(value) for value in location.values() if isinstance(value, str))
    combined = " ".join(haystacks)
    scores: dict[str, int] = {}
    for scene_type, keywords in SCENE_KEYWORDS.items():
        score = sum(combined.count(keyword) for keyword in keywords)
        if score:
            scores[scene_type] = score
    if scores:
        return max(scores, key=scores.get)
    return None


def hydrate_scene_defaults(package: dict[str, Any], scene_type: str, force: bool = False) -> None:
    defaults = SCENE_DEFAULTS.get(scene_type)
    if not defaults:
        return

    location = package.setdefault("location", {})
    if isinstance(location, dict):
        for key, value in defaults["location_defaults"].items():
            if force or not location.get(key):
                location[key] = value

    wardrobe = package.setdefault("wardrobe", {})
    if isinstance(wardrobe, dict):
        for side, side_defaults in defaults.get("wardrobe_defaults", {}).items():
            side_map = wardrobe.setdefault(side, {})
            if isinstance(side_map, dict):
                for key, value in side_defaults.items():
                    if force or not side_map.get(key):
                        side_map[key] = value

    props = package.setdefault("props", {})
    if isinstance(props, dict):
        for key, value in defaults.get("props_defaults", {}).items():
            if force or not props.get(key):
                props[key] = copy.deepcopy(value)

    time_and_light = package.setdefault("time_and_light", {})
    if isinstance(time_and_light, dict):
        if force or not time_and_light.get("time"):
            time_and_light["time"] = defaults["time"]
        if force or not time_and_light.get("effect"):
            time_and_light["effect"] = defaults["effect"]
        if force or not time_and_light.get("lighting"):
            time_and_light["lighting"] = copy.deepcopy(defaults["lighting"])
        if force or not time_and_light.get("color_temperature"):
            time_and_light["color_temperature"] = defaults["color_temperature"]
        if force or not time_and_light.get("tone"):
            time_and_light["tone"] = copy.deepcopy(defaults["tone"])

    camera_language = package.setdefault("camera_language", {})
    if isinstance(camera_language, dict):
        if force or not camera_language.get("camera_body"):
            camera_language["camera_body"] = defaults["camera_body"]
        if force or not camera_language.get("lens"):
            camera_language["lens"] = defaults["lens"]
        if force or not camera_language.get("image_style"):
            camera_language["image_style"] = copy.deepcopy(defaults["image_style"])

    if force or not package.get("mood_keywords"):
        package["mood_keywords"] = copy.deepcopy(defaults["mood_keywords"])

    if force or not package.get("negative_prompt"):
        package["negative_prompt"] = defaults["negative_prompt"]


def build_summary(package: dict[str, Any], scene_type: str) -> str:
    defaults = SCENE_DEFAULTS[scene_type]
    location = package.get("location", {}) if isinstance(package.get("location"), dict) else {}
    location_name = "".join(
        part for part in (
            str(location.get("country", "")).strip(),
            str(location.get("province", "")).strip(),
            str(location.get("city", "")).strip(),
            str(location.get("spot", "")).strip(),
        ) if part
    )
    if not location_name:
        location_name = str(package.get("name_zh", "婚纱照场景")).strip()
    return f"以{location_name}为核心场景的{defaults['summary_style']}。{defaults['summary_features']}"


def build_base_prompt(package: dict[str, Any], scene_type: str) -> str:
    location = package.get("location", {}) if isinstance(package.get("location"), dict) else {}
    wardrobe = package.get("wardrobe", {}) if isinstance(package.get("wardrobe"), dict) else {}
    bride = wardrobe.get("bride", {}) if isinstance(wardrobe.get("bride"), dict) else {}
    groom = wardrobe.get("groom", {}) if isinstance(wardrobe.get("groom"), dict) else {}
    bouquet = ""
    props = package.get("props")
    if isinstance(props, dict):
        bouquet_info = props.get("bouquet")
        if isinstance(bouquet_info, dict):
            bouquet = str(bouquet_info.get("description", "")).strip()

    time_and_light = package.get("time_and_light", {}) if isinstance(package.get("time_and_light"), dict) else {}
    camera_language = package.get("camera_language", {}) if isinstance(package.get("camera_language"), dict) else {}

    location_line = build_location_lines(location).get("full", "")
    lighting = "、".join(time_and_light.get("lighting", [])) if isinstance(time_and_light.get("lighting"), list) else str(time_and_light.get("lighting", ""))
    tones = "、".join(time_and_light.get("tone", [])) if isinstance(time_and_light.get("tone", []), list) else str(time_and_light.get("tone", ""))
    image_style = "，".join(camera_language.get("image_style", [])) if isinstance(camera_language.get("image_style", []), list) else str(camera_language.get("image_style", ""))

    prompt_parts = [
        "中国年轻情侣婚纱照，25-30岁，真实自然的中国面孔，保留人物原本五官特征与年龄感。",
        f"新娘造型为{str(bride.get('dress', '高定婚纱')).strip()}，搭配{str(bride.get('veil', '精致配饰')).strip()}，妆发风格{str(bride.get('makeup', '精致自然婚礼妆')).strip()}。",
        f"新郎造型为{str(groom.get('suit', '定制礼服')).strip()}，内搭{str(groom.get('shirt', '正式衬衫')).strip()}，发型要求为{str(groom.get('hair_policy', '利落自然')).strip()}。",
    ]
    if bouquet:
        prompt_parts.append(f"道具以{bouquet}为主，保持婚礼氛围与画面精致度。")
    if location_line:
        prompt_parts.append(location_line)
    prompt_parts.append(
        f"拍摄时间为{str(time_and_light.get('time', '')).strip()}，光效重点为{str(time_and_light.get('effect', '')).strip()}，光线特征包括{lighting}，整体色调{tones}。"
    )
    prompt_parts.append(
        f"摄影风格使用{str(camera_language.get('camera_body', 'Canon EOS R5')).strip()}，镜头语言{str(camera_language.get('lens', '')).strip()}，画面风格{image_style}。"
    )
    prompt_parts.append("要求人物互动自然亲密，情绪真实，服装结构完整，皮肤与手部细节真实，不要廉价摆拍感。")
    return " ".join(part for part in prompt_parts if part)


def build_frame_templates(scene_type: str) -> list[dict[str, str]]:
    templates = {
        "beach": [
            {"name": "远景海岸主片", "purpose": "用于建立海边婚礼场景与整套气质", "prompt": "远景全身构图，情侣站在海岸线与湿沙交界处，完整呈现海平线、晚霞、海风与轻盈头纱动态，适合作为主视觉海报。"},
            {"name": "海边对望中景", "purpose": "用于表现情侣关系感与松弛互动", "prompt": "中景竖版构图，情侣在海边自然对望，海风吹动发丝与头纱，背景保留晚霞与海面层次。"},
            {"name": "迎风头纱照", "purpose": "用于突出头纱、裙摆与海风动态", "prompt": "以新娘迎风动态为主，新郎在后侧守护，突出头纱线条、婚纱质感与落日轮廓光。"},
            {"name": "牵手踏浪互动照", "purpose": "用于表现海边行走与真实互动感", "prompt": "情侣牵手沿浅浅海浪边缘缓慢行走，突出脚步、牵手动作、湿沙反光与自然笑意。"},
            {"name": "海风贴近特写", "purpose": "用于相册内页的细腻情绪特写", "prompt": "近景特写，情侣面部距离很近，海风带来发丝与头纱的自然动势，突出真实肤质与温柔情绪。"},
            {"name": "沿海岸线行走抓拍照", "purpose": "用于制造松弛感与度假婚礼纪实感", "prompt": "沿海岸线抓拍，保留更多环境空间，让人物、海平线、晚霞与湿沙形成完整节奏。"},
            {"name": "背影望海照", "purpose": "用于丰富叙事感与环境层次", "prompt": "情侣面向海平线站立或缓步前行，微微回头，突出背影线条、拖尾与开阔海景。"},
            {"name": "封面级半身肖像", "purpose": "用于封面、海报与高质感主视觉", "prompt": "半身肖像，情侣靠近站立，落日光勾勒面部轮廓与服装细节，整体克制而高级。"},
        ],
        "mountain": [
            {"name": "远景环境主片", "purpose": "用于主海报与整套场景定调", "prompt": "远景全身婚纱照，情侣站在山地草坡或山景前景区域，完整呈现山体、云雾与晨光层次。"},
            {"name": "中景对望照", "purpose": "用于表现情侣关系感与情绪交流", "prompt": "中景竖版构图，情侣自然对望，背景保留山体和云雾虚化层次，突出情感交流。"},
            {"name": "新娘主导动作照", "purpose": "用于突出婚纱与新娘动态美感", "prompt": "新娘在前景轻撩头纱或裙摆，新郎后侧守护，突出婚纱层次、风感与晨光穿透效果。"},
            {"name": "递花互动照", "purpose": "用于表现互动细节与亲密氛围", "prompt": "以递花或轻触动作表现自然互动，突出手部动作、面部神态与衣料细节。"},
            {"name": "贴近特写情绪照", "purpose": "用于相册内页的高情绪密度特写", "prompt": "近景特写，突出真实肤质、眼神交流、头纱或发丝细节与柔和晨光氛围。"},
            {"name": "动态行走抓拍照", "purpose": "用于制造纪实感与自然流动感", "prompt": "情侣在山地草坡或步道上缓慢行走，保留自然风感与环境叙事。"},
            {"name": "背影回头照", "purpose": "用于丰富构图层次与叙事感", "prompt": "情侣面向远山站立或行走，回头看向镜头，突出背影线条、环境纵深与故事感。"},
            {"name": "封面级半身主肖像", "purpose": "用于封面、海报与高质感主视觉", "prompt": "半身肖像，情侣靠近站立，晨光与浅景深塑造高级感与杂志封面气质。"},
        ],
        "studio": [
            {"name": "正式双人主肖像", "purpose": "用于建立整套棚拍婚纱样片的主视觉气质", "prompt": "正式双人棚拍主肖像，姿态稳定克制，强调布光塑形、服装质感与背景秩序。"},
            {"name": "对称式并肩全身照", "purpose": "用于突出服装完整结构与秩序感构图", "prompt": "对称式并肩全身照，完整呈现婚纱与礼服轮廓，强调高级棚拍秩序感。"},
            {"name": "新娘半身主肖像", "purpose": "用于突出新娘妆发、婚纱细节与高级肖像感", "prompt": "以新娘为视觉中心的半身棚拍肖像，重点刻画妆容、发饰、婚纱纹理与面部层次。"},
            {"name": "新郎守护式站姿照", "purpose": "用于表现新郎稳定正式的气质", "prompt": "新郎位于新娘侧后方或并肩守护，人物关系克制自然，突出正式礼服结构。"},
            {"name": "双人对视互动照", "purpose": "用于表现含蓄情绪与真实关系感", "prompt": "双人对视互动中景，突出面部神态、上半身服装细节与高级棚拍氛围。"},
            {"name": "端坐仪式感肖像", "purpose": "用于增强画面稳定性与正式感", "prompt": "端坐式棚拍肖像，人物姿态得体，强调座椅、背景层次与仪式感。"},
            {"name": "背身回眸照", "purpose": "用于丰富画面变化与造型展示", "prompt": "人物轻微转身或回眸，突出婚纱拖尾、背部线条与控制光影。"},
            {"name": "封面级近景肖像", "purpose": "用于海报、封面与精修主视觉", "prompt": "封面级近景肖像，面部与服装质感清晰，背景简洁，整体具有杂志封面感。"},
        ],
        "chinese_traditional": [
            {"name": "正式双人主肖像", "purpose": "用于建立整套中式婚礼样片的主视觉气质", "prompt": "正式双人中式婚纱主肖像，姿态稳定克制，突出秀禾服纹样、头饰细节与礼仪秩序。"},
            {"name": "对称式并肩全身照", "purpose": "用于突出服装完整结构与东方秩序感", "prompt": "对称式并肩全身照，完整呈现秀禾服和中式礼服轮廓，强调端庄礼仪感。"},
            {"name": "新娘持团扇半身照", "purpose": "用于突出新娘造型、头饰与中式温婉气质", "prompt": "新娘手持团扇或婚书，姿态端庄，重点刻画凤冠头饰、妆容与刺绣细节。"},
            {"name": "新郎守护式站姿照", "purpose": "用于表现新郎稳定、正式的中式婚礼气质", "prompt": "新郎站姿挺括自然，位于新娘身侧或后侧半步，突出中式礼服结构与关系感。"},
            {"name": "双人对视互动照", "purpose": "用于表现含蓄喜悦与真实关系感", "prompt": "双人对视互动中景，动作克制自然，营造含蓄而温暖的喜庆氛围。"},
            {"name": "端坐仪式感肖像", "purpose": "用于增强中式礼仪感与画面稳定性", "prompt": "端坐式中式婚礼肖像，人物姿态得体，可加入婚书、团扇、案几等礼仪元素。"},
            {"name": "回眸礼仪照", "purpose": "用于丰富画面变化与东方气质表达", "prompt": "人物轻微侧身或回眸，突出服饰纹样、袖口结构与中式背景层次。"},
            {"name": "封面级近景肖像", "purpose": "用于海报、封面与高质感主视觉", "prompt": "封面级近景肖像，突出面部神态、凤冠秀禾细节与庄重柔和的暖光氛围。"},
        ],
    }
    return copy.deepcopy(templates[scene_type])


def rewrite_package_for_scene(package: dict[str, Any], scene_type: str, force_scene_location: bool = False) -> None:
    defaults = SCENE_DEFAULTS[scene_type]
    if force_scene_location:
        location = package.setdefault("location", {})
        if isinstance(location, dict):
            for key, value in defaults.get("scene_location", {}).items():
                location[key] = value

    hydrate_scene_defaults(package, scene_type, force=True)
    package["summary"] = build_summary(package, scene_type)
    package["base_prompt"] = build_base_prompt(package, scene_type)
    package["frames"] = build_frame_templates(scene_type)


def collect_wardrobe_replacements(original: dict[str, Any], current: dict[str, Any]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for side in ("bride", "groom"):
        old_side = original.get(side, {}) if isinstance(original.get(side), dict) else {}
        new_side = current.get(side, {}) if isinstance(current.get(side), dict) else {}
        for key in ("dress", "veil", "suit", "shirt", "bow_tie"):
            old_value = old_side.get(key)
            new_value = new_side.get(key)
            if isinstance(old_value, str) and isinstance(new_value, str) and old_value != new_value:
                pairs.append((old_value, new_value))
    return pairs


def build_location_lines(location: dict[str, Any]) -> dict[str, str]:
    country = str(location.get("country", "")).strip()
    province = str(location.get("province", "")).strip()
    city = str(location.get("city", "")).strip()
    spot = str(location.get("spot", "")).strip()
    foreground = str(location.get("foreground", "")).strip()
    midground = str(location.get("midground", "")).strip()
    background = str(location.get("background", "")).strip()

    summary_parts = [part for part in (country, province, city, spot) if part]
    summary_text = "".join(summary_parts)

    hierarchy_parts = [part for part in (country, province, city, spot) if part]
    hierarchy_text = "，".join(hierarchy_parts)

    detail_parts = []
    if foreground:
        detail_parts.append(f"前景为{foreground}")
    if midground:
        detail_parts.append(f"中景为{midground}")
    if background:
        detail_parts.append(f"背景为{background}")

    full_parts = []
    if hierarchy_text:
        full_parts.append(f"拍摄地点为{hierarchy_text}")
    if detail_parts:
        full_parts.append("，".join(detail_parts))

    return {
        "summary": summary_text,
        "full": "，".join(full_parts) + "。" if full_parts else "",
    }


def replace_summary_location(text: str, original_location: dict[str, Any], current_location: dict[str, Any]) -> str:
    if not text:
        return text
    old_phrase = "".join(
        part for part in (
            str(original_location.get("country", "")).strip(),
            str(original_location.get("province", "")).strip(),
            str(original_location.get("city", "")).strip(),
            str(original_location.get("spot", "")).strip(),
        ) if part
    )
    new_phrase = "".join(
        part for part in (
            str(current_location.get("country", "")).strip(),
            str(current_location.get("province", "")).strip(),
            str(current_location.get("city", "")).strip(),
            str(current_location.get("spot", "")).strip(),
        ) if part
    )
    if old_phrase and new_phrase and old_phrase in text:
        return text.replace(old_phrase, new_phrase, 1)

    updated, count = re.subn(
        r"以.*?景观为核心背景的",
        f"以{new_phrase}景观为核心背景的",
        text,
        count=1,
    )
    if count:
        return updated

    if new_phrase:
        updated, count = re.subn(r"以.*?为核心背景的", f"以{new_phrase}为核心背景的", text, count=1)
        if count:
            return updated
    return text


def replace_location_sentence(text: str, replacement_sentence: str) -> str:
    if not text or not replacement_sentence:
        return text
    updated, count = re.subn(r"拍摄地点为.*?整体氛围", replacement_sentence + "整体氛围", text, count=1)
    if count:
        return updated
    updated, count = re.subn(r"拍摄地点为.*?[。；;]", replacement_sentence, text, count=1)
    if count:
        return updated
    return append_note(text, replacement_sentence)


def build_location_change_notes(
    original_location: dict[str, Any], current_location: dict[str, Any], override_paths: set[str]
) -> list[str]:
    notes: list[str] = []
    field_labels = {
        "location.country": "国家/地区",
        "location.province": "区域",
        "location.city": "城市",
        "location.spot": "场景点位",
        "location.foreground": "前景",
        "location.midground": "中景",
        "location.background": "背景",
    }
    for path, label in field_labels.items():
        if path not in override_paths:
            continue
        key = path.split(".")[-1]
        new_value = str(current_location.get(key, "")).strip()
        old_value = str(original_location.get(key, "")).strip()
        if new_value and new_value != old_value:
            notes.append(f"{label}{new_value}")
    return notes


def append_note(text: str, note: str) -> str:
    text = text.strip()
    if not text:
        return note
    if note in text:
        return text
    return f"{text} {note}"


def clean_spacing(text: str) -> str:
    text = re.sub(r"[\x00-\x1f\x7f]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def render_text(package: dict[str, Any], package_path: Path, overrides: list[str]) -> str:
    lines: list[str] = []
    name_zh = package.get("name_zh", "Unknown Package")
    name_en = package.get("name_en", "Unknown Package")
    category = package.get("category", "unknown")
    summary = package.get("summary", "").strip()
    base_prompt = package.get("base_prompt", "").strip()
    negative_prompt = package.get("negative_prompt", "").strip()
    frames = package.get("frames", [])
    if not isinstance(frames, list):
        raise ValueError("frames must be a list")

    lines.append(f"Package: {name_zh} / {name_en}")
    lines.append(f"ID: {package.get('id', 'unknown')}")
    lines.append(f"Category: {category}")
    lines.append(f"Source: {package_path}")
    if overrides:
        lines.append(f"Overrides: {', '.join(overrides)}")
    lines.append("")

    if summary:
        lines.append("Style Summary")
        lines.append(summary)
        lines.append("")

    if base_prompt:
        lines.append("Base Prompt")
        lines.append(base_prompt)
        lines.append("")

    if negative_prompt:
        lines.append("Negative Prompt")
        lines.append(negative_prompt)
        lines.append("")

    lines.append("8-Shot Prompt Set")
    for index, frame in enumerate(frames, start=1):
        if not isinstance(frame, dict):
            raise ValueError(f"frame #{index} is not a mapping")
        name = frame.get("name", f"Shot {index}")
        purpose = frame.get("purpose", "")
        prompt = frame.get("prompt", "").strip()
        lines.append(f"{index}. {name}")
        if purpose:
            lines.append(f"Purpose: {purpose}")
        if prompt:
            lines.append(f"Prompt: {prompt}")
        lines.append("")

    lines.append("Usage Notes")
    lines.append("- Test identity consistency with one or two shots before batch generation.")
    lines.append("- Generate multiple candidates for interaction-heavy shots and compare hands, gaze, and fabric integrity.")
    lines.append("- Prioritize selected shots for later retouch, upscale, or local inpainting workflows.")
    return "\n".join(lines).rstrip() + "\n"


def list_packages() -> list[Path]:
    return sorted(PACKAGES_DIR.glob("*.y*ml"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render ai-wedding-studio package templates into a standard prompt package."
    )
    parser.add_argument(
        "package",
        nargs="?",
        help="Package file path, package id, or package stem under assets/packages/",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available package templates",
    )
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="PATH=VALUE",
        help="Override a dotted package field, for example location.country=日本",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        for package in list_packages():
            print(package.name)
        return 0

    if not args.package:
        parser.error("package is required unless --list is used")

    try:
        package_path = resolve_package(args.package)
        original_package = load_package(package_path)
        package = apply_overrides(original_package, args.set)
        package = apply_smart_adaptations(original_package, package, args.set)
        sys.stdout.write(render_text(package, package_path, args.set))
    except Exception as exc:  # pragma: no cover - simple CLI error path
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
