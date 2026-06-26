#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path-to-input-json>")
        print("Example: python main.py examples/netflix_input.json")
        print("\nRequired: OPENAI_API_KEY environment variable")
        sys.exit(1)

    # Explicit env loading with warning
    env_path = Path(".env")
    if env_path.exists():
        print("⚠️  Loading .env file from current directory...")
        print("⚠️  Ensure no unrelated secrets are stored in this .env file.")
        load_dotenv(dotenv_path=env_path, override=False)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found.")
        print("Set it as environment variable or create a .env file.")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        user_input = json.load(f)

    from src.runner import ClaimbackRadar
    radar = ClaimbackRadar(api_key=api_key)
    result = radar.run(user_input)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()