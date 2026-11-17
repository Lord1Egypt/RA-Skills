#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze.py — 桌宠摄像头分析脚本（pet-camera-vision Skill 的分析部分）

职责（三种模式，可组合）：
  1. --local           本地辅助检测：人脸级联（有没有人）+ PIL 主色提取（什么颜色），离线可用
  2. （默认）           生成多模态模型的提示词（打印到 stdout，供 OpenClaw 喂给视觉模型）
  3. --model-output    把多模态模型的回答规范化为严格 JSON（容错提取 + 字段校验 + 兜底默认值）

设计遵循项目约定：Skill 负责"执行"（截图、规范化），OpenClaw/大模型负责"思考"（表情识别）。

用法示例：
  python3 analyze.py --image captures/xxx.jpg --local
  python3 analyze.py --image captures/xxx.jpg > prompt.txt
  python3 analyze.py --image captures/xxx.jpg --model-output model_answer.txt
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8), "CST")

# 允许的情绪集合（与反馈 Skill 的表情一一对应）
ALLOWED_EMOTIONS = [
    "happy", "sad", "angry", "surprised",
    "fearful", "disgusted", "neutral", "worried", "sleepy", "excited",
]

# 常见颜色名（用于本地主色提取）
COLOR_TABLE = [
    ("红色", (220, 20, 60)), ("橙色", (255, 140, 0)), ("黄色", (255, 215, 0)),
    ("绿色", (34, 139, 34)), ("青色", (0, 200, 200)), ("蓝色", (30, 110, 220)),
    ("紫色", (138, 43, 226)), ("粉色", (255, 105, 180)), ("白色", (245, 245, 245)),
    ("灰色", (128, 128, 128)), ("黑色", (25, 25, 25)), ("棕色", (139, 90, 43)),
]

PROMPT_TEMPLATE = """你是一个桌宠系统的视觉感知模块。请分析这张图片，只输出 JSON，不要输出任何其他内容。

要求：
1. present（bool）：画面中是否有人（人脸）。
2. emotion（string）：画面中人的情绪，只允许取以下值之一：happy, sad, angry, surprised, fearful, disgusted, neutral, worried, sleepy, excited。如果没人，取 "neutral"。
3. emotion_confidence（float）：对情绪的置信度，0 到 1。
4. colors（array）：画面中占比最高的 3 种颜色，每项为 {"name": "<中文颜色名>", "hex": "#RRGGBB", "ratio": <0到1的占比>}。

输出格式（严格）：
{"present": true, "emotion": "happy", "emotion_confidence": 0.9, "colors": [{"name": "蓝色", "hex": "#1E6EDC", "ratio": 0.4}]}
"""


def now_str():
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S%z")


# ---------- 本地检测 ----------

def local_presence(image_path):
    """基于 OpenCV 人脸级联判断有没有人；无 cv2 时返回 unknown。"""
    try:
        import cv2
    except ImportError:
        return None, "opencv-python not installed"
    img = cv2.imread(image_path)
    if img is None:
        return None, "cannot read image"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade_path = os.path.join(
        os.path.dirname(cv2.__file__), "data", "haarcascade_frontalface_default.xml")
    if not os.path.exists(cascade_path):
        return None, "haarcascade data missing"
    cascade = cv2.CascadeClassifier(cascade_path)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    return len(faces) > 0, "cascade"


def local_colors(image_path, top_n=3):
    """基于 PIL 提取主色；无 Pillow 时返回空列表。"""
    try:
        from PIL import Image
    except ImportError:
        return []
    img = Image.open(image_path).convert("RGB").resize((64, 64))
    quantized = img.quantize(colors=8, method=Image.MEDIANCUT).convert("RGB")
    counts = {}
    for pixel in quantized.getdata():
        counts[pixel] = counts.get(pixel, 0) + 1
    total = sum(counts.values())
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])[:top_n]
    result = []
    for (r, g, b), cnt in ranked:
        name, hex_code = nearest_color((r, g, b))
        result.append({"name": name, "hex": hex_code, "ratio": round(cnt / total, 3)})
    return result


def nearest_color(rgb):
    best, best_dist = "未知", 1e9
    for name, ref in COLOR_TABLE:
        dist = sum((a - b) ** 2 for a, b in zip(rgb, ref))
        if dist < best_dist:
            best, best_dist = name, dist
    return best, "#%02X%02X%02X" % rgb


# ---------- 模型输出规范化 ----------

def extract_json(text):
    """从模型回答中容错提取 JSON 对象（支持代码块、前后缀杂文）。"""
    if not text:
        return None
    # 去掉 markdown 代码块围栏
    text = re.sub(r"```(?:json)?", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        # 尝试修复常见的尾逗号
        fixed = re.sub(r",\s*([}\]])", r"\1", text[start:end + 1])
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            return None


def normalize(data, image_path):
    """校验并补全字段，保证输出永远是严格 JSON。"""
    emotion = data.get("emotion", "neutral")
    if emotion not in ALLOWED_EMOTIONS:
        emotion = "neutral"
    try:
        conf = float(data.get("emotion_confidence", 0.5))
        conf = max(0.0, min(1.0, conf))
    except (TypeError, ValueError):
        conf = 0.5
    colors = data.get("colors", [])
    if not isinstance(colors, list):
        colors = []
    colors = [c for c in colors if isinstance(c, dict)][:3]
    return {
        "present": bool(data.get("present", False)),
        "present_method": data.get("present_method", "multimodal"),
        "emotion": emotion,
        "emotion_confidence": conf,
        "colors": colors,
        "image_path": image_path,
        "timestamp": now_str(),
    }


def main():
    ap = argparse.ArgumentParser(description="桌宠摄像头分析")
    ap.add_argument("--image", required=True, help="图片路径")
    ap.add_argument("--local", action="store_true", help="本地辅助检测（人脸级联 + 主色），离线可用")
    ap.add_argument("--model-output", default=None,
                    help="多模态模型回答文件路径；给出时规范化输出严格 JSON")
    args = ap.parse_args()

    if not os.path.exists(args.image):
        print(json.dumps({"status": "error", "message": "图片不存在: %s" % args.image}, ensure_ascii=False))
        return 1

    # 模式 3：规范化模型输出
    if args.model_output:
        if not os.path.exists(args.model_output):
            print(json.dumps({"status": "error", "message": "模型回答文件不存在: %s" % args.model_output}, ensure_ascii=False))
            return 1
        with open(args.model_output, "r", encoding="utf-8") as f:
            raw = f.read()
        parsed = extract_json(raw)
        if parsed is None:
            parsed = {"present": False, "emotion": "neutral", "emotion_confidence": 0.0,
                      "colors": [], "present_method": "unknown"}
        result = normalize(parsed, args.image)
        # 本地在场检测作为补充（模型没判断时）
        if result["present_method"] == "unknown":
            present, method = local_presence(args.image)
            if present is not None:
                result["present"] = present
                result["present_method"] = method
        print(json.dumps(result, ensure_ascii=False))
        return 0

    # 模式 2：本地检测（--local）
    if args.local:
        present, method = local_presence(args.image)
        colors = local_colors(args.image)
        result = {
            "status": "ok",
            "present": present,
            "present_method": method if present is not None else "unknown",
            "colors": colors,
            "image_path": args.image,
            "timestamp": now_str(),
            "note": "本地检测结果（离线）；表情识别请交给多模态模型",
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0

    # 模式 1：打印提示词
    print(PROMPT_TEMPLATE)
    print("# 将上面提示词与图片一起交给多模态模型，"
          "把回答保存到文件后运行：analyze.py --image %s --model-output <回答文件>" % args.image)
    return 0


if __name__ == "__main__":
    sys.exit(main())
