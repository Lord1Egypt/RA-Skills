#!/usr/bin/env python3
"""
pipeline.py — Orchestrate full podcast generation pipeline

Runs all stages: discover → research → script → verify → audio → upload → deliver

Usage:
    pipeline.py --config config.yaml [--topic "Specific Topic"] [--mode auto|manual]
"""
import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


def run_command(cmd: list, description: str) -> tuple:
    """Run command and return (success, output)"""
    print(f"\n{'='*60}")
    print(f"Stage: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return (True, result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ FAILED: {e.stderr}")
        return (False, e.stderr)


def main():
    """Main entry point for pipeline orchestration"""
    parser = argparse.ArgumentParser(description="Run podcast generation pipeline")
    parser.add_argument("--config", required=True, help="Config YAML file")
    parser.add_argument("--topic", help="Specific topic (skips discovery)")
    parser.add_argument("--mode", choices=["auto", "manual"], default="manual", 
                       help="auto: full pipeline, manual: stop after each stage")
    parser.add_argument("--resume-from", help="Resume from stage: research|script|verify|audio|upload")
    args = parser.parse_args()
    
    skill_dir = Path(__file__).parent.parent
    scripts_dir = skill_dir / "scripts"
    output_dir = skill_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    date = datetime.now().date().isoformat()
    
    print(f"🎙️  PODCAST GENERATION PIPELINE")
    print(f"   Config: {args.config}")
    print(f"   Mode: {args.mode}")
    print(f"   Date: {date}")
    print()
    
    # State tracking
    state_file = output_dir / f"pipeline-state-{date}.json"
    state = {}
    if state_file.exists():
        with open(state_file) as f:
            state = json.load(f)
    
    def save_state():
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    # Stage 1: Discovery (if no topic provided)
    if not args.topic and not args.resume_from:
        discovery_file = output_dir / f"discovery-{date}.json"
        cmd = [
            "python3", str(scripts_dir / "discover.py"),
            "--config", args.config,
            "--limit", "10",
            "--output", str(discovery_file)
        ]
        
        success, output = run_command(cmd, "Topic Discovery")
        if not success:
            print("Pipeline failed at discovery stage")
            sys.exit(1)
        
        state["discovery_file"] = str(discovery_file)
        save_state()
        
        # Load topics
        with open(discovery_file) as f:
            discovery = json.load(f)
        
        if not discovery.get("topics"):
            print("❌ No topics discovered")
            sys.exit(1)
        
        # Use top topic
        top_topic = discovery["topics"][0]
        args.topic = top_topic["title"]
        print(f"\n✅ Selected topic: {args.topic}")
        
        if args.mode == "manual":
            input("\nPress Enter to continue to research stage...")
    
    if not args.topic:
        print("ERROR: No topic provided and discovery skipped")
        sys.exit(1)
    
    # Generate slug for filenames
    import re
    slug = re.sub(r'[^a-z0-9]+', '-', args.topic.lower()).strip('-')[:40]
    
    # Stage 2: Research
    if not args.resume_from or args.resume_from == "research":
        research_file = output_dir / f"research-{date}-{slug}.json"
        cmd = [
            "python3", str(scripts_dir / "research.py"),
            args.topic,
            "--output", str(research_file)
        ]
        
        success, output = run_command(cmd, "Deep Research")
        if not success:
            print("Pipeline failed at research stage")
            sys.exit(1)
        
        state["research_file"] = str(research_file)
        state["topic"] = args.topic
        save_state()
        
        if args.mode == "manual":
            print("\n⚠️  Research framework created. Worker should populate with actual data.")
            input("Press Enter to continue to script generation...")
    
    research_file = state.get("research_file", output_dir / f"research-{date}-{slug}.json")
    
    # Stage 3: Script Generation
    if not args.resume_from or args.resume_from in ["research", "script"]:
        script_file = output_dir / f"script-{date}-{slug}.txt"
        cmd = [
            "python3", str(scripts_dir / "generate-script.py"),
            "--research", str(research_file),
            "--output", str(script_file),
            "--config", args.config
        ]
        
        success, output = run_command(cmd, "Script Generation")
        if not success:
            print("Pipeline failed at script generation")
            sys.exit(1)
        
        state["script_file"] = str(script_file)
        save_state()
        
        if args.mode == "manual":
            print("\n⚠️  Script prompt created. Worker should generate actual script with LLM.")
            input("Press Enter to continue to verification...")
    
    script_file = state.get("script_file", output_dir / f"script-{date}-{slug}.txt")
    
    # Stage 4: Verification
    if not args.resume_from or args.resume_from in ["research", "script", "verify"]:
        verify_file = output_dir / f"verification-{date}-{slug}.json"
        cmd = [
            "python3", str(scripts_dir / "verify.py"),
            "--script", str(script_file),
            "--research", str(research_file),
            "--output", str(verify_file)
        ]
        
        success, output = run_command(cmd, "Fact Verification")
        # Don't exit on verification failure, just warn
        
        state["verify_file"] = str(verify_file)
        save_state()
        
        if not success:
            print("\n⚠️  Verification failed. Review and fix script before proceeding.")
            if args.mode == "manual":
                choice = input("Continue anyway? (y/N): ")
                if choice.lower() != 'y':
                    sys.exit(1)
        elif args.mode == "manual":
            input("Press Enter to continue to audio generation...")
    
    # Stage 5: Audio Generation
    if not args.resume_from or args.resume_from in ["research", "script", "verify", "audio"]:
        audio_file = output_dir / f"episode-{date}-{slug}.mp3"
        cmd = [
            "python3", str(scripts_dir / "generate-audio.py"),
            "--script", str(script_file),
            "--output", str(audio_file),
            "--config", args.config
        ]
        
        success, output = run_command(cmd, "Audio Generation")
        if not success:
            print("Pipeline failed at audio generation")
            sys.exit(1)
        
        state["audio_file"] = str(audio_file)
        save_state()
        
        if args.mode == "manual":
            print("\n⚠️  TTS text prepared. Worker should call ElevenLabs to generate audio.")
            input("Press Enter to continue to upload...")
    
    audio_file = state.get("audio_file", output_dir / f"episode-{date}-{slug}.mp3")
    
    # Stage 6: Upload
    if not args.resume_from or args.resume_from in ["research", "script", "verify", "audio", "upload"]:
        cmd = [
            "python3", str(scripts_dir / "upload.py"),
            "--file", str(audio_file),
            "--config", args.config,
            "--title", args.topic
        ]
        
        success, output = run_command(cmd, "Upload to Storage")
        if not success:
            print("Pipeline failed at upload stage")
            sys.exit(1)
        
        # Extract URL from output
        for line in output.split('\n'):
            if line.startswith("PUBLIC_URL="):
                url = line.split('=', 1)[1]
                state["public_url"] = url
                save_state()
                break
    
    print(f"\n{'='*60}")
    print("🎉 PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"Topic: {args.topic}")
    print(f"Research: {state.get('research_file', 'N/A')}")
    print(f"Script: {state.get('script_file', 'N/A')}")
    print(f"Audio: {state.get('audio_file', 'N/A')}")
    print(f"URL: {state.get('public_url', 'N/A')}")
    print()
    
    # Save final state
    state["completed"] = True
    state["completed_at"] = datetime.now().isoformat()
    save_state()


if __name__ == "__main__":
    main()
