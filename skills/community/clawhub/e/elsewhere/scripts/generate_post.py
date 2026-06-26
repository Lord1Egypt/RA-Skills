#!/usr/bin/env python
"""
动态生成工具：基于当前行程节点生成图文内容。

用法: python generate_post.py <node_id>
输出: JSON 到 stdout { "text_content": "...", "image_path": "..." | null, "local_time": "..." }
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parent.parent
SKILL_DIR_STR = str(SKILL_DIR)
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"

load_dotenv(PROJECT_ROOT / ".env")
os.environ["SKILL_DIR"] = SKILL_DIR_STR


def load_data():
    """加载 persona 和 itinerary 数据。"""
    with open(DATA_DIR / "persona.json", "r", encoding="utf-8") as f:
        persona = json.load(f)
    with open(DATA_DIR / "itinerary.json", "r", encoding="utf-8") as f:
        itinerary = json.load(f)
    return persona, itinerary


def find_node(itinerary: dict, node_id: str) -> dict | None:
    """从行程中查找指定节点。"""
    for node in itinerary["nodes"]:
        if node["node_id"] == node_id:
            return node
    return None


def get_local_time(itinerary: dict) -> str:
    """获取目的地当前本地时间字符串。"""
    offset = itinerary.get("timezone_offset", 0)
    tz = timezone(timedelta(hours=offset))
    local_now = datetime.now(tz)
    return local_now.strftime("%H:%M")


def build_text_prompt(persona: dict, node: dict, itinerary: dict) -> str:
    """构建文案生成 Prompt。"""
    name = persona["basic_info"]["name"]
    tone = persona["basic_info"]["tone_of_voice"]
    personality = persona["basic_info"]["personality"]
    location = node["meta_data"].get("location", itinerary["destination"])
    weather = node["meta_data"].get("weather_desc", "")
    temperature = node["meta_data"].get("temperature", "")
    state_type = node["state_type"]
    highlights = node["meta_data"].get("highlights", [])

    context_map = {
        "prep": f"packing and getting ready for a trip to {itinerary['destination']}",
        "departure": f"heading to {node['meta_data'].get('airport_or_station', 'the station')} to depart for {itinerary['destination']}",
        "transit": f"on a {node['meta_data'].get('transport_type', 'flight')} heading to {itinerary['destination']}",
        "arrival": f"just arrived in {itinerary['destination']}",
        "attraction": f"visiting {location}",
        "return": f"heading back home after the trip to {itinerary['destination']}",
    }
    situation = context_map.get(state_type, f"traveling in {itinerary['destination']}")

    highlight_text = ""
    if highlights:
        highlight_text = f"\nNotable things about this place: {', '.join(highlights)}"

    return f"""You are {name}, a travel companion with this personality: {personality}
Your tone of voice: {tone}

You are currently {situation}.
Location: {location}
Weather: {weather} {temperature}
{highlight_text}

Write a SHORT message (1-3 sentences) as if texting a close friend.
- Use first person perspective
- Be natural, casual, with genuine emotion
- Match your personality and tone
- If at an attraction, share a specific sensory detail or small moment
- Do NOT use hashtags or emojis excessively

Use Google Search to find real, current details about {location} to make your message authentic.

Reply with ONLY the message text, nothing else."""


def build_image_prompt(persona: dict, node: dict, itinerary: dict) -> str:
    """构建生图 Prompt。"""
    location = node["meta_data"].get("location", itinerary["destination"])
    weather = node["meta_data"].get("weather_desc", "clear sky")
    appearance = persona["appearance"].get("description", "")
    state_type = node["state_type"]

    scene_map = {
        "prep": "packing luggage in a cozy bedroom",
        "departure": f"at {node['meta_data'].get('airport_or_station', 'airport')} terminal with luggage",
        "transit": f"looking out the window of a {node['meta_data'].get('transport_type', 'plane')}",
        "arrival": f"stepping out of {node['meta_data'].get('airport_or_station', 'airport')} in {itinerary['destination']}",
        "attraction": f"at {location}, {itinerary['destination']}",
        "return": f"at the airport heading home with souvenirs",
    }
    scene = scene_map.get(state_type, f"traveling in {itinerary['destination']}")

    return f"""A casual iPhone selfie photo of a person {scene}.
Weather: {weather}.
Person appearance: {appearance}.
Style: candid smartphone selfie, slightly messy and natural, warm lighting,
real-life feel, not posed or professional. Shot on iPhone, slight lens distortion.
The background should show the real environment of {location}."""


def generate_text(persona: dict, node: dict, itinerary: dict) -> str:
    """调用 Gemini + Search 生成文案。"""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    grounding_tool = types.Tool(google_search=types.GoogleSearch())

    prompt = build_text_prompt(persona, node, itinerary)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature=0.9,
        ),
    )
    return response.text.strip()


def generate_image(persona: dict, node: dict, itinerary: dict, node_id: str) -> str | None:
    """调用 Gemini 图生图模式生成图片。失败返回 None。"""
    ref_relative = persona["appearance"]["reference_image_path"]
    ref_image_path = PROJECT_ROOT / ref_relative.lstrip("./")
    if not ref_image_path.exists():
        print(f"Warning: reference image not found at {ref_image_path}", file=sys.stderr)
        return None

    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = build_image_prompt(persona, node, itinerary)
        ref_image = Image.open(ref_image_path)

        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[prompt, ref_image],
        )

        output_dir = ASSETS_DIR / "generated"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{node_id}.png"

        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(str(output_path))
                return str(output_path)

        print("Warning: no image in response", file=sys.stderr)
        return None

    except Exception as e:
        print(f"Warning: image generation failed: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_post.py <node_id>", file=sys.stderr)
        sys.exit(1)

    node_id = sys.argv[1]

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    persona, itinerary = load_data()
    node = find_node(itinerary, node_id)
    if not node:
        print(f"Error: node '{node_id}' not found in itinerary", file=sys.stderr)
        sys.exit(1)

    local_time = get_local_time(itinerary)

    print(f"Generating text for {node_id}...", file=sys.stderr)
    text_content = generate_text(persona, node, itinerary)

    print(f"Generating image for {node_id}...", file=sys.stderr)
    image_path = generate_image(persona, node, itinerary, node_id)

    result = {
        "text_content": text_content,
        "image_path": image_path,
        "local_time": local_time,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
