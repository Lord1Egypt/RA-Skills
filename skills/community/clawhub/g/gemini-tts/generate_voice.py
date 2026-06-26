import os
import urllib.request
import json
import argparse
import base64

def generate_voice(text, voice_id):
    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": "Puck"
                    }
                }
            }
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # 打印详细的返回结构，看看是不是有 inline_data 和 mime_type
            part = result['candidates'][0]['content']['parts'][0]
            if 'inlineData' in part:
                mime_type = part['inlineData']['mimeType']
                print(f"MIME Type: {mime_type}")
                audio_data = part['inlineData']['data']
                audio_bytes = base64.b64decode(audio_data)
                
                # 根据返回的 mime type 动态确定扩展名
                ext = mime_type.split('/')[-1]
                filename = f"output_voice.{ext}"
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                return filename
            else:
                print("No inlineData found in response.")
                return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--voice", default="little-claw-persona")
    args = parser.parse_args()
    
    output = generate_voice(args.text, args.voice)
    print(f"Output saved to {output}")
