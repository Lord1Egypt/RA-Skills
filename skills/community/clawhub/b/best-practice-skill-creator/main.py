#!/usr/bin/env python3
"""Best Practice Skill Creator - Generate OpenClaw skills from video/image demos."""

import argparse
import sys
from pathlib import Path

from src.config import load_config
from src.mllm import create_provider
from src.media import extract_frames_from_video, load_image_sequence
from src.analyzer import analyze_best_practice, parse_analysis
from src.skill_generator import generate_skill

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".webm", ".mkv"}


def detect_input_type(input_path: str) -> str:
    """Detect whether input is a video file, image file, or image directory."""
    p = Path(input_path)
    if p.is_dir():
        return "image_dir"
    if p.is_file():
        if p.suffix.lower() in VIDEO_EXTENSIONS:
            return "video"
        return "image_file"
    raise FileNotFoundError(f"Input path not found: {input_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Create OpenClaw skills from best practice videos or image sequences.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # From a video
  python main.py --input demo.mp4 --description "How to deploy with Docker" --output ./skills/docker-deploy

  # From a screenshot directory
  python main.py --input ./screenshots/ --description "Setting up CI/CD" --output ./skills/ci-cd

  # Using Gemini provider
  python main.py --input demo.mp4 --description "Task description" --provider gemini --output ./skills/my-skill
""",
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to video file, image file, or directory of images.",
    )
    parser.add_argument(
        "--description", "-d",
        required=True,
        help="Text description of what the task accomplishes.",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output directory for the generated skill.",
    )
    parser.add_argument(
        "--provider", "-p",
        choices=["openai", "gemini"],
        default=None,
        help="MLLM provider to use (overrides config file).",
    )
    parser.add_argument(
        "--config", "-c",
        default=None,
        help="Path to config.yaml (default: config.yaml in project root).",
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)
    if args.provider:
        config.provider = args.provider
        # Re-load provider config from file for the selected provider
        import yaml
        config_path = args.config or str(Path(__file__).parent / "config.yaml")
        with open(config_path) as f:
            raw = yaml.safe_load(f)
        pconf = raw.get("providers", {}).get(args.provider, {})
        import os
        from src.config import ProviderConfig
        config.provider_config = ProviderConfig(
            api_key=os.environ.get("MLLM_API_KEY", pconf.get("api_key", "")),
            base_url=os.environ.get("MLLM_BASE_URL", pconf.get("base_url", "")),
            model=os.environ.get("MLLM_MODEL", pconf.get("model", "")),
        )

    # Create MLLM provider
    print(f"[*] Using provider: {config.provider} ({config.provider_config.model})")
    provider = create_provider(config.provider, config.provider_config)

    # Process input media
    input_type = detect_input_type(args.input)
    print(f"[*] Input type: {input_type}")

    if input_type == "video":
        print(f"[*] Extracting frames from video: {args.input}")
        images_b64 = extract_frames_from_video(
            args.input,
            max_frames=config.video.max_frames,
            frame_interval_sec=config.video.frame_interval_sec,
            max_resolution=config.video.max_resolution,
        )
    else:
        print(f"[*] Loading images from: {args.input}")
        images_b64 = load_image_sequence(
            args.input,
            supported_formats=config.image.supported_formats,
            max_resolution=config.image.max_resolution,
        )

    print(f"[*] Loaded {len(images_b64)} image(s)")

    # Analyze with MLLM
    print("[*] Analyzing best practice with MLLM (this may take a minute)...")
    response = analyze_best_practice(provider, images_b64, args.description)
    print(f"[*] Analysis complete (model: {response.model})")

    # Parse the structured response
    analysis = parse_analysis(response.text)
    task_name = analysis.get("task_name", "unknown")
    print(f"[*] Detected task: {task_name}")

    # Generate the skill
    skill_path = generate_skill(analysis, args.output, config.skill)
    print(f"[+] Skill generated: {skill_path}")
    print(f"[+] To install: cp -r {args.output} ~/.openclaw/skills/")
    print(f"[+] Or publish: cd {args.output} && clawhub publish")

    return 0


if __name__ == "__main__":
    sys.exit(main())
