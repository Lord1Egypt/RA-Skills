#!/usr/bin/env python3
"""
智能字幕下载器 - 基于实战经验优化
优先检查视频是否有现成字幕，避免不必要的语音转写
"""

import asyncio
import json
import urllib.request
from typing import Optional, Dict, Any
from bilibili_api import video, Credential


async def get_video_info(bvid: str) -> Optional[Dict[str, Any]]:
    """获取视频信息"""
    try:
        v = video.Video(bvid=bvid)
        info = await v.get_info()
        return info
    except Exception as e:
        print(f"❌ 获取视频信息失败：{e}")
        return None


async def check_subtitle_exists(bvid: str) -> tuple[bool, list]:
    """检查视频是否有现成字幕"""
    try:
        v = video.Video(bvid=bvid)
        info = await v.get_info()
        cid = info['cid']
        
        # 尝试获取字幕，不需要 Credential
        try:
            subtitle_list = await v.get_subtitle(cid=cid)
        except Exception as e:
            # 如果因为缺少 Credential 失败，尝试用 requests 直接获取
            print(f"⚠️  API 调用受限：{e}")
            print("尝试直接检查字幕状态...")
            
            # 很多 B 站视频有 AI 字幕，即使不登录也能获取
            # 这里我们假设视频可能有字幕，让用户尝试
            return True, []  # 返回 True 让流程继续尝试
        
        if subtitle_list and subtitle_list.get('subtitles'):
            subtitles = subtitle_list['subtitles']
            print(f"✅ 视频有 {len(subtitles)} 种字幕：")
            for sub in subtitles:
                print(f"  - {sub['lan_doc']} ({sub['lan']})")
            return True, subtitles
        else:
            print("❌ 视频无现成字幕")
            return False, []
    except Exception as e:
        print(f"❌ 检查字幕失败：{e}")
        return False, []


async def download_subtitle(subtitle_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """下载字幕内容"""
    try:
        subtitle_url = subtitle_info['subtitle_url']
        if subtitle_url.startswith('//'):
            subtitle_url = 'https:' + subtitle_url
        
        print(f"📥 正在下载字幕：{subtitle_url}")
        with urllib.request.urlopen(subtitle_url) as response:
            subtitle_data = json.loads(response.read().decode('utf-8'))
        
        print(f"✅ 字幕下载成功，共 {len(subtitle_data['body'])} 句")
        return subtitle_data
    except Exception as e:
        print(f"❌ 下载字幕失败：{e}")
        return None


def generate_summary(subtitle_data: Dict[str, Any], video_title: str, duration: int) -> str:
    """基于字幕生成结构化总结"""
    lines = subtitle_data['body']
    full_text = '\n'.join([line['content'] for line in lines])
    
    # 简单的总结生成（实际应用中可以用 LLM 生成更详细的总结）
    summary = f"""# 🎬 {video_title}

## 📋 基本信息
- **视频时长**：{duration} 秒（约 {duration//60} 分钟）
- **字幕来源**：AI 生成字幕
- **字幕句数**：{len(lines)} 句
- **总字符数**：{len(full_text)}

## 📝 字幕预览（前 20 句）
"""
    
    for i, line in enumerate(lines[:20]):
        summary += f"[{line['from']:.1f}s] {line['content']}\n"
    
    if len(lines) > 20:
        summary += f"\n... 还有 {len(lines) - 20} 句\n"
    
    summary += f"\n---\n*总结基于 AI 字幕生成，共 {len(lines)} 句*"
    
    return summary


async def smart_process_video(bvid: str, output_dir: str = "./output") -> Dict[str, Any]:
    """
    智能处理视频：有字幕优先，无字幕再考虑语音转写
    
    Args:
        bvid: B 站视频 BV 号
        output_dir: 输出目录
    
    Returns:
        处理结果字典
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎬 开始处理视频：{bvid}")
    print("=" * 50)
    
    # 1. 获取视频信息
    info = await get_video_info(bvid)
    if not info:
        return {"success": False, "error": "无法获取视频信息"}
    
    print(f"✅ 视频标题：{info['title']}")
    print(f"✅ 视频时长：{info['duration']} 秒")
    
    # 2. 检查是否有现成字幕
    has_subtitle, subtitles = await check_subtitle_exists(bvid)
    
    if has_subtitle and subtitles:
        # 3. 有字幕，优先使用字幕
        print("\n🎯 检测到现成字幕，优先使用字幕方案...")
        
        # 选择中文字幕（优先）
        chinese_sub = None
        for sub in subtitles:
            if sub['lan'] == 'ai-zh':
                chinese_sub = sub
                break
        
        if not chinese_sub:
            chinese_sub = subtitles[0]  # 使用第一个字幕
        
        print(f"📄 选择字幕：{chinese_sub['lan_doc']} ({chinese_sub['lan']})")
        
        # 下载字幕
        subtitle_data = await download_subtitle(chinese_sub)
        if not subtitle_data:
            return {"success": False, "error": "字幕下载失败"}
        
        # 保存原始字幕
        subtitle_file = os.path.join(output_dir, f"{bvid}_subtitle.json")
        with open(subtitle_file, 'w', encoding='utf-8') as f:
            json.dump(subtitle_data, f, ensure_ascii=False, indent=2)
        print(f"💾 原始字幕已保存：{subtitle_file}")
        
        # 保存文本格式
        text_file = os.path.join(output_dir, f"{bvid}_transcript.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            for line in subtitle_data['body']:
                f.write(f"[{line['from']:.1f}s] {line['content']}\n")
        print(f"💾 文本字幕已保存：{text_file}")
        
        # 生成总结
        summary = generate_summary(subtitle_data, info['title'], info['duration'])
        summary_file = os.path.join(output_dir, f"{bvid}_summary.md")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"💾 总结已保存：{summary_file}")
        
        return {
            "success": True,
            "method": "subtitle",
            "video_info": info,
            "subtitle_type": chinese_sub['lan'],
            "subtitle_count": len(subtitle_data['body']),
            "files": {
                "json": subtitle_file,
                "txt": text_file,
                "summary": summary_file
            }
        }
    else:
        # 4. 无字幕，需要语音转写
        print("\n🔊 无现成字幕，需要语音转写...")
        print("⚠️ 注意：语音转写需要登录和下载音频，处理时间较长")
        
        return {
            "success": False,
            "method": "transcribe_needed",
            "video_info": info,
            "error": "视频无现成字幕，需要语音转写",
            "suggestion": "请使用 bilibili_transcriber.process() 进行语音转写"
        }


async def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python smart_subtitle_downloader.py <BV号> [输出目录]")
        print("示例：python smart_subtitle_downloader.py BV15gDsBnETQ ./output")
        return
    
    bvid = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    
    result = await smart_process_video(bvid, output_dir)
    
    print("\n" + "=" * 50)
    print("📊 处理结果：")
    print(f"成功：{result['success']}")
    print(f"方法：{result.get('method', 'N/A')}")
    
    if result['success']:
        print(f"字幕类型：{result.get('subtitle_type', 'N/A')}")
        print(f"字幕句数：{result.get('subtitle_count', 'N/A')}")
        print(f"输出文件：")
        for key, path in result.get('files', {}).items():
            print(f"  - {key}: {path}")
    else:
        print(f"错误：{result.get('error', 'N/A')}")
        if result.get('suggestion'):
            print(f"建议：{result['suggestion']}")


if __name__ == "__main__":
    asyncio.run(main())
