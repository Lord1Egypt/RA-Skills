#!/usr/bin/env python3
"""
B站视频音频下载工具 - 下载B站视频的音频文件
"""

import sys
import json
import os
import re
import argparse
import requests

# ==================== 工具函数 ====================

def format_duration(seconds):
    """格式化时长"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f'{mins}分{secs}秒'

# ==================== B站 API 封装 ====================

def get_video_info(bvid):
    """获取视频信息"""
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.bilibili.com'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if data['code'] == 0 and 'data' in data:
            info = data['data']
            return {
                'ok': True,
                'bvid': info['bvid'],
                'title': info['title'],
                'duration': info['duration'],
                'durationText': format_duration(info['duration']),
                'cover': info['pic'],
                'desc': info['desc'],
                'owner': info['owner']['name']
            }
        else:
            return {
                'ok': False,
                'error': 'INFO_FAILED',
                'message': data.get('message', '获取视频信息失败')
            }
    except Exception as e:
        return {
            'ok': False,
            'error': 'INFO_FAILED',
            'message': str(e)
        }

def download_audio(bvid, output_path):
    """下载B站视频音频"""
    try:
        # 获取视频信息
        info_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.bilibili.com'
        }
        
        response = requests.get(info_url, headers=headers, timeout=10)
        info_data = response.json()
        
        if info_data['code'] != 0:
            return {
                'ok': False,
                'error': 'DOWNLOAD_FAILED',
                'message': info_data.get('message', '获取视频信息失败')
            }
        
        info = info_data['data']
        cid = info['cid']
        
        # 获取播放地址
        play_url = f'https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&fnval=16&fnver=0&fourk=1'
        response = requests.get(play_url, headers=headers, timeout=10)
        play_data = response.json()
        
        if play_data['code'] != 0 or 'dash' not in play_data.get('data', {}):
            return {
                'ok': False,
                'error': 'DOWNLOAD_FAILED',
                'message': '获取播放地址失败'
            }
        
        # 选择最高码率音频
        audio_streams = play_data['data']['dash']['audio']
        best_audio = max(audio_streams, key=lambda x: x['bandwidth'])
        audio_url = best_audio['baseUrl']
        
        # 下载音频
        audio_response = requests.get(audio_url, headers=headers, stream=True, timeout=60)
        audio_response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in audio_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # 获取文件信息
        file_size = os.path.getsize(output_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        duration = info['duration']
        duration_sec = duration % 60
        
        return {
            'ok': True,
            'bvid': bvid,
            'audioPath': output_path,
            'title': info['title'],
            'duration': duration,
            'durationSec': duration_sec,
            'fileSize': file_size,
            'fileSizeMB': file_size_mb
        }
        
    except Exception as e:
        return {
            'ok': False,
            'error': 'DOWNLOAD_FAILED',
            'message': str(e)
        }

# ==================== 主命令处理 ====================

def cmd_init():
    """环境初始化"""
    import subprocess
    
    # 检查 Python 3
    try:
        subprocess.run(['python3', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        output_result({'ok': False, 'error': 'PYTHON_VERSION_2', 'message': '需要 Python 3'})
        return
    
    # 检查 requests
    try:
        import requests
    except ImportError:
        try:
            subprocess.run(['python3', '-m', 'pip', 'install', 'requests'], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError:
            output_result({'ok': False, 'error': 'INSTALL_FAILED', 'message': '依赖安装失败'})
            return
    
    output_result({'ok': True, 'skill_dir': os.path.dirname(os.path.abspath(__file__))})

def cmd_info(bvid):
    """获取视频信息"""
    if not bvid:
        output_result({'ok': False, 'error': 'MISSING_BVID', 'message': '请提供 BVID'})
        return
    
    result = get_video_info(bvid)
    output_result(result)

def cmd_download(bvid, output):
    """下载音频"""
    if not bvid:
        output_result({'ok': False, 'error': 'MISSING_BVID', 'message': '请提供 BVID'})
        return
    
    output_path = output or os.path.join(os.getcwd(), f'{bvid}.m4a')
    result = download_audio(bvid, output_path)
    output_result(result)

def output_result(result):
    """输出 JSON 结果"""
    print(json.dumps(result, ensure_ascii=False))

# ==================== 命令行入口 ====================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='B站视频音频下载工具')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # init 命令
    subparsers.add_parser('init', help='环境初始化')
    
    # info 命令
    info_parser = subparsers.add_parser('info', help='获取视频信息')
    info_parser.add_argument('--bvid', required=True, help='B站视频 BVID')
    
    # download 命令
    download_parser = subparsers.add_parser('download', help='下载音频')
    download_parser.add_argument('--bvid', required=True, help='B站视频 BVID')
    download_parser.add_argument('--output', help='输出路径')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        cmd_init()
    elif args.command == 'info':
        cmd_info(args.bvid)
    elif args.command == 'download':
        cmd_download(args.bvid, args.output)
    else:
        parser.print_help()
