"""
生成图片脚本
使用阿里云百炼 wan2.6-t2i 模型
根据故事文案自动生成 5-6 张场景图片
"""

import http.client
import json
import urllib.request
import os
import sys
import time

API_KEY = os.environ.get('DASHSCOPE_API_KEY', '')

# 默认图片描述模板（可根据故事自动调整）
DEFAULT_PROMPTS = [
    "Dark horror comic style, Chinese rural horror. Night scene with mysterious atmosphere. Mist and shadows. Cinematic lighting, 9:16 aspect ratio.",
    "Dark horror comic style, Chinese rural horror. Main character silhouette in mysterious setting. Eerie atmosphere. Cinematic lighting, 9:16 aspect ratio.",
    "Dark horror comic style, Chinese rural horror. Key moment in the story, dramatic scene. Cinematic lighting, 9:16 aspect ratio.",
    "Dark horror comic style, Chinese rural horror. Climax scene, tension and mystery. Cinematic lighting, 9:16 aspect ratio.",
    "Dark horror comic style, Chinese rural horror. Resolution or aftermath scene. Lingering mystery. Cinematic lighting, 9:16 aspect ratio.",
]


def generate_images(output_dir, num_images=5, custom_prompts=None):
    """
    生成图片
    
    Args:
        output_dir: 输出目录
        num_images: 图片数量
        custom_prompts: 自定义提示词列表
    
    Returns:
        list: 生成的图片路径列表
    """
    if not API_KEY:
        raise Exception('请设置环境变量 DASHSCOPE_API_KEY')
    
    os.makedirs(output_dir, exist_ok=True)
    
    prompts = custom_prompts if custom_prompts else DEFAULT_PROMPTS[:num_images]
    image_paths = []
    
    for i, prompt in enumerate(prompts, 1):
        print(f'生成图片 {i}/{len(prompts)}...')
        
        conn = http.client.HTTPSConnection('dashscope.aliyuncs.com')
        
        payload = json.dumps({
            'model': 'wan2.6-t2i',
            'input': {
                'messages': [{
                    'role': 'user',
                    'content': [{'text': prompt}]
                }]
            },
            'parameters': {
                'size': '720*1280',
                'n': 1,
                'prompt_extend': True,
                'watermark': False
            }
        })
        
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'X-DashScope-Async': 'enable'
        }
        
        conn.request('POST', '/api/v1/services/aigc/image-generation/generation', payload, headers)
        res = conn.getresponse()
        data = res.read()
        result = json.loads(data.decode('utf-8'))
        
        if 'output' in result and 'task_id' in result['output']:
            task_id = result['output']['task_id']
            
            # 轮询等待
            while True:
                time.sleep(10)
                
                conn2 = http.client.HTTPSConnection('dashscope.aliyuncs.com')
                conn2.request('GET', f'/api/v1/tasks/{task_id}', '', {'Authorization': f'Bearer {API_KEY}'})
                res2 = conn2.getresponse()
                data2 = res2.read()
                result2 = json.loads(data2.decode('utf-8'))
                
                status = result2.get('output', {}).get('task_status', 'UNKNOWN')
                
                if status == 'SUCCEEDED':
                    image_url = result2['output']['choices'][0]['message']['content'][0]['image']
                    image_path = os.path.join(output_dir, f'img{i}.png')
                    urllib.request.urlretrieve(image_url, image_path)
                    image_paths.append(image_path)
                    print(f'已保存: img{i}.png')
                    break
                elif status == 'FAILED':
                    raise Exception(f'图片生成失败: {result2}')
        else:
            raise Exception(f'创建任务失败: {result}')
    
    return image_paths


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python generate_images.py <output_dir> [num_images]')
        sys.exit(1)
    
    output_dir = sys.argv[1]
    num_images = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    paths = generate_images(output_dir, num_images)
    print(f"\n生成了 {len(paths)} 张图片")