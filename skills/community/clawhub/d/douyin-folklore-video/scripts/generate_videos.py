"""
生成视频脚本
使用阿里云百炼 wan2.2-kf2v-flash 模型
按顺序推进，不回退
"""

import http.client
import json
import urllib.request
import os
import sys
import time
import ftplib

API_KEY = os.environ.get('DASHSCOPE_API_KEY', '')

FTP_HOST = os.environ.get('FTP_HOST', '')
FTP_PORT = int(os.environ.get('FTP_PORT', '21'))
FTP_USER = os.environ.get('FTP_USER', '')
FTP_PASS = os.environ.get('FTP_PASS', '')
FTP_BASE_URL = os.environ.get('FTP_BASE_URL', '')


def upload_to_ftp(file_path, remote_name):
    """上传文件到FTP"""
    if not FTP_HOST:
        raise Exception('请设置 FTP 环境变量 (FTP_HOST, FTP_USER, FTP_PASS, FTP_BASE_URL)')
    
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    
    with open(file_path, 'rb') as f:
        ftp.storbinary(f'STOR {remote_name}', f)
    
    ftp.quit()
    return f'{FTP_BASE_URL}{remote_name}'


def generate_videos(image_paths, output_dir, prompts=None):
    """
    生成视频段
    
    Args:
        image_paths: 图片路径列表
        output_dir: 输出目录
        prompts: 每段视频的提示词
    
    Returns:
        list: 生成的视频路径列表
    """
    if not API_KEY:
        raise Exception('请设置环境变量 DASHSCOPE_API_KEY')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 上传图片到FTP
    img_urls = []
    for i, img_path in enumerate(image_paths, 1):
        remote_name = f'video_img_{int(time.time())}_{i}.png'
        url = upload_to_ftp(img_path, remote_name)
        img_urls.append(url)
        print(f'上传图片: {url}')
    
    # 计算视频段数（每段5秒）
    num_segments = len(img_urls) - 1 if len(img_urls) > 1 else 1
    
    # 生成默认提示词
    if not prompts:
        prompts = ['视频画面缓缓过渡'] * num_segments
    
    video_paths = []
    
    for i in range(num_segments):
        print(f'\n生成视频 {i+1}/{num_segments}')
        
        # 首尾帧
        first_url = img_urls[i]
        last_url = img_urls[min(i+1, len(img_urls)-1)]
        
        conn = http.client.HTTPSConnection('dashscope.aliyuncs.com')
        
        payload = json.dumps({
            'model': 'wan2.2-kf2v-flash',
            'input': {
                'first_frame_url': first_url,
                'last_frame_url': last_url,
                'prompt': prompts[i] if i < len(prompts) else '视频画面过渡'
            },
            'parameters': {
                'resolution': '720P',
                'prompt_extend': True,
                'watermark': False
            }
        })
        
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'X-DashScope-Async': 'enable'
        }
        
        conn.request('POST', '/api/v1/services/aigc/image2video/video-synthesis', payload, headers)
        res = conn.getresponse()
        data = res.read()
        result = json.loads(data.decode('utf-8'))
        
        if 'output' in result and 'task_id' in result['output']:
            task_id = result['output']['task_id']
            
            # 轮询等待
            while True:
                time.sleep(15)
                
                conn2 = http.client.HTTPSConnection('dashscope.aliyuncs.com')
                conn2.request('GET', f'/api/v1/tasks/{task_id}', '', {'Authorization': f'Bearer {API_KEY}'})
                res2 = conn2.getresponse()
                data2 = res2.read()
                result2 = json.loads(data2.decode('utf-8'))
                
                status = result2.get('output', {}).get('task_status', 'UNKNOWN')
                print(f'状态: {status}')
                
                if status == 'SUCCEEDED':
                    video_url = result2['output']['video_url']
                    video_path = os.path.join(output_dir, f'v{i+1}.mp4')
                    urllib.request.urlretrieve(video_url, video_path)
                    video_paths.append(video_path)
                    print(f'已保存: v{i+1}.mp4')
                    break
                elif status == 'FAILED':
                    raise Exception(f'视频生成失败: {result2}')
        else:
            raise Exception(f'创建任务失败: {result}')
    
    return video_paths


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python generate_videos.py <image_paths_json> <output_dir>')
        print('Example: python generate_videos.py \'["img1.png","img2.png"]\' output')
        sys.exit(1)
    
    image_paths = json.loads(sys.argv[1])
    output_dir = sys.argv[2]
    
    paths = generate_videos(image_paths, output_dir)
    print(f"\n生成了 {len(paths)} 个视频")