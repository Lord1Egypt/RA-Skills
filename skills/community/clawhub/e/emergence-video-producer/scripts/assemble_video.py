import os
import subprocess
import argparse
from PIL import Image, ImageSequence

def extract_frames(webp_path, output_dir):
    print(f"Opening {webp_path}...")
    img = Image.open(webp_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    count = 0
    for i, frame in enumerate(ImageSequence.Iterator(img)):
        frame.save(os.path.join(output_dir, f"frame_{i:04d}.png"))
        count += 1
    print(f"✓ Extracted {count} frames.")
    return count

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())

def assemble_mp4(frame_dir, audio_path, output_path, fps):
    print(f"Assembling MP4 at {fps} FPS...")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(frame_dir, "frame_%04d.png"),
        "-i", audio_path,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"✓ Video assembled: {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--webp", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--output", default="final_video.mp4")
    args = parser.parse_args()
    
    temp_frame_dir = "temp_frames"
    frame_count = extract_frames(args.webp, temp_frame_dir)
    audio_duration = get_audio_duration(args.audio)
    
    fps = frame_count / audio_duration
    assemble_mp4(temp_frame_dir, args.audio, args.output, fps)

if __name__ == "__main__":
    main()
