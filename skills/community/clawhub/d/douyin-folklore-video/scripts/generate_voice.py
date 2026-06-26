"""
生成配音脚本
使用阿里云百炼 qwen3-tts-flash 模型
"""

import http.client
import json
import urllib.request
import os
import sys

API_KEY = os.environ.get('DASHSCOPE_API_KEY', '')

def generate_voice(story_text, output_dir):
    """
    生成配音
    
    Args:
        story_text: 故事文案
        output_dir: 输出目录
    
    Returns:
        dict: {'voice_path': str, 'duration': float}
    """
    if not API_KEY:
        raise Exception('请设置环境变量 DASHSCOPE_API_KEY')
    
    os.makedirs(output_dir, exist_ok=True)
    
    conn = http.client.HTTPSConnection('dashscope.aliyuncs.com')
    
    payload = json.dumps({
        'model': 'qwen3-tts-flash',
        'input': {
            'text': story_text,
            'voice': 'Cherry',
            'language_type': 'Chinese'
        }
    })
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    conn.request('POST', '/api/v1/services/aigc/multimodal-generation/generation', payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode('utf-8'))
    
    if 'output' in result and 'audio' in result['output']:
        audio_info = result['output']['audio']
        audio_url = audio_info['url'] if isinstance(audio_info, dict) else audio_info
        
        voice_path = os.path.join(output_dir, 'voice.wav')
        urllib.request.urlretrieve(audio_url, voice_path)
        
        # 计算时长
        file_size = os.path.getsize(voice_path)
        duration = (file_size - 44) / 48000
        
        # 保存时长
        with open(os.path.join(output_dir, 'duration.txt'), 'w') as f:
            f.write(str(round(duration, 2)))
        
        return {'voice_path': voice_path, 'duration': round(duration, 2)}
    
    raise Exception(f'生成配音失败: {result}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python generate_voice.py <story_text> <output_dir>')
        sys.exit(1)
    
    story_text = sys.argv[1]
    output_dir = sys.argv[2]
    
    result = generate_voice(story_text, output_dir)
    print(f"配音已生成: {result['voice_path']}")
    print(f"配音时长: {result['duration']}秒")