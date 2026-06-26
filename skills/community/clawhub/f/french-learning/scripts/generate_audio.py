#!/usr/bin/env python3

import subprocess
import json
import os
import time

# --- Config (from Skill's references/config.md) ---
TARGET_SHEET_ID = "1Nnwv4DbbUgfiNDiJdgCvnyxH6oPBis_99fm-2voehl4"
TARGET_SHEET_NAME = "Sheet1"
AUDIO_FOLDER_ID = "1F7J7u5agTCma4ra1ZcvaD8iQS_HoowlV"

# 1. Fetch data from Google Sheet
def get_sentences() -> list:
    cmd = ["gog", "sheets", "get", TARGET_SHEET_ID, f"{TARGET_SHEET_NAME}!A2:E1000", "--json"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout).get("values", [])
        
        sentences = []
        for row in data:
            if row and len(row) >= 5: # Assuming Column E is "Example Sentence (FR)"
                # Index is row[0], Sentence is row[4]
                sentences.append({"index": row[0], "text": row[4]})
        return sentences
    except subprocess.CalledProcessError as e:
        print(f"Error fetching sheet: {e.stderr}")
        return []

# 2. Generate Audio in Chunks
def generate_and_upload_audio(sentences: list, folder_id: str):
    chunk_size = 20
    
    # Process in chunks of 20
    for i in range(0, len(sentences), chunk_size):
        chunk = sentences[i:i + chunk_size]
        if not chunk: continue
        
        # Combine text for the chunk, adding pauses
        # Using a simple pause (e.g., 1 second) between sentences
        # ElevenLabs respects basic punctuation for pauses.
        combined_text = " ... ".join([s["text"] for s in chunk if s["text"].strip()])
        
        if not combined_text.strip(): continue

        start_idx = chunk[0]["index"]
        end_idx = chunk[-1]["index"]
        filename = f"{start_idx}-{end_idx}.mp3"
        output_path = f"/tmp/{filename}"
        
        print(f"Generating audio for {filename}...")
        
        # 3. Call 'sag' skill to generate audio
        # The 'sag' skill likely has a CLI interface once installed. 
        # We need to format the command properly based on 'sag' docs.
        # Assuming `sag` takes a text string and output path:
        # sag "text" --output output.mp3 --voice "Rachel" (or specific French voice)
        # Note: Need to specify a French voice ID if possible, or rely on ElevenLabs Multilingual model.
        
        try:
            # Use eleven_multilingual_v2 for French support; --output disables playback
            cmd_sag = [
                "sag", "speak",
                "--model-id", "eleven_multilingual_v2",
                "--voice", "XrExE9yKIg1WjnnlVkGX",  # Matilda
                "--output", output_path,
                combined_text,
            ]

            res = subprocess.run(cmd_sag, capture_output=True, text=True, check=True)
            print(f"Audio generated at {output_path}")
            
            # 4. Upload to Google Drive
            print(f"Uploading {filename} to Google Drive...")
            cmd_upload = ["gog", "drive", "upload", output_path, "--parent", folder_id, "--json"]
            subprocess.run(cmd_upload, capture_output=True, text=True, check=True)
            
            print(f"Uploaded {filename} successfully.")
            
            # Optional: Clean up temp file
            os.remove(output_path)
            
            # Sleep briefly to avoid rate limits if many chunks
            time.sleep(2)
            
        except subprocess.CalledProcessError as e:
             print(f"Error processing chunk {filename}: {e.stderr}")

if __name__ == "__main__":
    sentences = get_sentences()
    if sentences:
        print(f"Found {len(sentences)} sentences. Generating audio...")
        generate_and_upload_audio(sentences, AUDIO_FOLDER_ID)
        print("Done.")
    else:
        print("No sentences found or error fetching data.")
