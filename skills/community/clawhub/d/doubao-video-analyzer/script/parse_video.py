import os
import sys
import argparse
import base64
from volcenginesdkarkruntime import AsyncArk
import asyncio

api_key = os.getenv('ARK_API_KEY')

def parse_args():
    parser = argparse.ArgumentParser(description='Parse video content using AI model')
    parser.add_argument('--prompt', type=str, required=True, help='The prompt text to send to the model')
    parser.add_argument('--video', type=str, required=True, help='Path to the local video file or remote video URL')
    parser.add_argument('--remote', action='store_true', help='Treat --video as a remote video URL instead of local file')
    return parser.parse_args()

def encode_video_to_base64(video_path):
    with open(video_path, 'rb') as video_file:
        return base64.b64encode(video_file.read()).decode('utf-8')

def get_video_mime_type(video_path):
    ext = os.path.splitext(video_path)[1].lower()
    mime_types = {
        '.mp4': 'video/mp4',
        '.avi': 'video/x-msvideo',
        '.mov': 'video/quicktime',
        '.mkv': 'video/x-matroska',
        '.webm': 'video/webm',
        '.flv': 'video/x-flv',
        '.wmv': 'video/x-ms-wmv',
    }
    return mime_types.get(ext, 'video/mp4')

async def main(args):
    client = AsyncArk(
        base_url='https://ark.cn-beijing.volces.com/api/v3',
        api_key=os.getenv('ARK_API_KEY')
    )
    if args.remote:
        video_url = args.video
        params = {
            "type": "input_video",
            "video_url": video_url,
            "fps":1
        }
    else:
        if not os.path.exists(args.video):
            print(f"Error: Video file not found: {args.video}", file=sys.stderr)
            sys.exit(1)
        
        file = await client.files.create(
            # replace with your local video path
            file=open(args.video, "rb"),
            purpose="user_data",
            preprocess_configs={
                "video": {
                    "fps": 1,  # define the sampling fps of the video, default is 1.0
                }
            }
        )
        await client.files.wait_for_processing(file.id)
        params = {
            "type": "input_video",
            "file_id": file.id
        }

    response = await client.responses.create(
        model="doubao-seed-2-0-pro-260215",
        input=[
            {
                "role": "system",
                "content": args.prompt
            },
            {
                "role": "user",
                "content": [params]
            }
        ]
    )
    
    print(response)

if __name__ == '__main__':
    args = parse_args()
    
    asyncio.run(main(args))
