#!/usr/bin/env python
"""
行程规划工具：调用 Gemini + Google Search grounding 生成真实行程剧本。

用法: python generate_itinerary.py <destination> [--origin <origin_city>] [--days <num_days>]
输出: 写入 data/itinerary.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parent.parent
SKILL_DIR_STR = str(SKILL_DIR)
DATA_DIR = PROJECT_ROOT / "data"

load_dotenv(PROJECT_ROOT / ".env")
os.environ["SKILL_DIR"] = SKILL_DIR_STR


def build_prompt(destination: str, origin: str, days: int, start_date: str) -> str:
    """构建行程规划 Prompt。"""
    return f"""You are a travel itinerary planner. Generate a detailed, realistic travel itinerary
for a trip from {origin} to {destination}, starting on {start_date}, lasting {days} days.

IMPORTANT: Use Google Search to find REAL information:
- Real flight/train schedules and departure times from {origin} to {destination}
- Real tourist attractions with actual opening hours
- Real weather forecast for {destination} around {start_date}
- Real airport/station names

Generate a JSON object following this EXACT schema:

{{
  "trip_id": "trip_<random_5_digits>",
  "destination": "{destination}",
  "timezone_offset": <integer, UTC offset of destination>,
  "start_date": "<ISO 8601 date>",
  "end_date": "<ISO 8601 date>",
  "last_posted_at": null,
  "nodes": [
    {{
      "node_id": "node_001",
      "state_type": "<one of: prep, departure, transit, arrival, attraction, return>",
      "start_time": "<ISO 8601 datetime in UTC>",
      "end_time": "<ISO 8601 datetime in UTC>",
      "status": "PENDING",
      "message_count": 0,
      "meta_data": {{
        "location": "<place name>",
        "transport_type": "<flight/train/bus or empty>",
        "airport_or_station": "<name or empty>",
        "weather_desc": "<weather description>",
        "temperature": "<e.g. 18°C>",
        "highlights": ["<notable things about this place>"]
      }}
    }}
  ]
}}

Rules for node sequence:
1. First node: "prep" (24 hours before departure)
2. "departure" node at the transport hub
3. "transit" node covering the travel duration
4. "arrival" node at the destination
5. Multiple "attraction" nodes for each day's activities (2-3 attractions per day)
6. Final "return" node for the journey home

All times MUST be in UTC (ISO 8601 with Z suffix).
Each attraction node should span 2-3 hours.
Include realistic gaps between attractions for meals and rest.

Return ONLY the JSON object, no other text."""


def generate_itinerary(destination: str, origin: str = "Shanghai", days: int = 3) -> dict:
    """调用 Gemini + Search 生成行程。"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    grounding_tool = types.Tool(google_search=types.GoogleSearch())

    start_date = (datetime.now(timezone.utc) + timedelta(days=2)).strftime("%Y-%m-%d")
    prompt = build_prompt(destination, origin, days, start_date)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature=0.7,
        ),
    )

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[: text.rfind("```")]
        text = text.strip()

    itinerary = json.loads(text)
    return itinerary


def validate_itinerary(itinerary: dict) -> bool:
    """基本校验行程结构。"""
    required_keys = ["trip_id", "destination", "timezone_offset", "nodes"]
    for key in required_keys:
        if key not in itinerary:
            print(f"Validation error: missing key '{key}'", file=sys.stderr)
            return False

    if not itinerary["nodes"]:
        print("Validation error: nodes list is empty", file=sys.stderr)
        return False

    valid_types = {"prep", "departure", "transit", "arrival", "attraction", "return"}
    for node in itinerary["nodes"]:
        if node.get("state_type") not in valid_types:
            print(f"Validation error: invalid state_type '{node.get('state_type')}' in {node.get('node_id')}", file=sys.stderr)
            return False
        if "start_time" not in node or "end_time" not in node:
            print(f"Validation error: missing time in {node.get('node_id')}", file=sys.stderr)
            return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate travel itinerary")
    parser.add_argument("destination", help="Travel destination")
    parser.add_argument("--origin", default="Shanghai", help="Origin city (default: Shanghai)")
    parser.add_argument("--days", type=int, default=3, help="Trip duration in days (default: 3)")
    args = parser.parse_args()

    print(f"Generating itinerary: {args.origin} → {args.destination} ({args.days} days)...", file=sys.stderr)

    itinerary = generate_itinerary(args.destination, args.origin, args.days)

    if not validate_itinerary(itinerary):
        print("Generated itinerary failed validation", file=sys.stderr)
        sys.exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / "itinerary.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(itinerary, f, ensure_ascii=False, indent=2)

    print(f"Itinerary saved to {output_path}", file=sys.stderr)
    print(json.dumps({
        "status": "success",
        "destination": itinerary["destination"],
        "start_date": itinerary.get("start_date", ""),
        "end_date": itinerary.get("end_date", ""),
        "total_nodes": len(itinerary["nodes"]),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
