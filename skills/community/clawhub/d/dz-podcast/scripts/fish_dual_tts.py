#!/usr/bin/env python3
"""
Dual-voice podcast TTS via Fish Audio API.
Usage: python3 fish_dual_tts.py <script.txt> <output.mp3>
"""

import sys, os, json, requests, tempfile

API_KEY = "YOUR_FISH_API_KEY"
API_URL = "https://api.fish.audio/v1/tts"

VOICES = {
    "HostA": "YOUR_VOICE_A_ID",  # Voice A
    "HostB": "YOUR_VOICE_B_ID",  # Voice B
}

def parse_script(path):
    segments = []
    speaker = None
    lines = []
    import re
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^\[(\w+)\]\s*(.*)', line)
            if m:
                if speaker and lines:
                    segments.append((speaker, ' '.join(lines)))
                speaker = m.group(1)
                lines = []
                if m.group(2):
                    lines.append(m.group(2))
            else:
                lines.append(line)
    if speaker and lines:
        segments.append((speaker, ' '.join(lines)))
    return segments

def tts(text, voice_id, output):
    resp = requests.post(API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "reference_id": voice_id,
            "format": "mp3"
        })
    if resp.status_code != 200:
        print(f"  ❌ Error: {resp.status_code} {resp.text[:100]}")
        return False
    with open(output, 'wb') as f:
        f.write(resp.content)
    return True

def main():
    script_path = sys.argv[1]
    output_path = sys.argv[2]
    
    segments = parse_script(script_path)
    print(f"Parsed {len(segments)} segments")
    
    tmpdir = tempfile.mkdtemp()
    seg_files = []
    
    for i, (speaker, text) in enumerate(segments):
        voice = VOICES.get(speaker, VOICES["HostA"])
        seg_file = os.path.join(tmpdir, f"seg_{i:03d}.mp3")
        print(f"  [{speaker}] {text[:40]}...")
        if tts(text, voice, seg_file):
            seg_files.append(seg_file)
        else:
            print(f"  ⚠️ Skipping segment {i}")
    
    # Concatenate
    with open(output_path, 'wb') as outf:
        for sf in seg_files:
            with open(sf, 'rb') as inf:
                outf.write(inf.read())
    
    # Cleanup
    for sf in seg_files:
        os.remove(sf)
    os.rmdir(tmpdir)
    
    size = os.path.getsize(output_path)
    print(f"✅ Output: {output_path} ({size} bytes)")

if __name__ == "__main__":
    main()
