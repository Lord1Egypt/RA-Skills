#!/usr/bin/env python3
"""
快速提取指定抖音视频文案
"""
import asyncio
import sys
sys.path.insert(0, '.')
from extractor import DouyinExtractor

async def main():
    raw_input = sys.argv[1] if len(sys.argv) > 1 else "https://v.douyin.com/B1YYg8Ao1sg/"
    
    # 智能提取其中的 URL (支持直接黏贴整个带有文字的抖音分享口令)
    import re
    url_match = re.search(r'https?://[^\s一-龥]+', raw_input)
    if url_match:
        url = url_match.group(0).strip('/')
    else:
        print("❌ 未在输入文本中检测到有效的链接！")
        sys.exit(1)
        
    print(f"✅ 从口令中识别目标链接: {url}")
    
    extractor = DouyinExtractor(
        whisper_model="base",
        segment_minutes=10
    )
    
    try:
        # 获取文案和元数据
        text, info = await extractor.extract(url)
        
        print("\n" + "=" * 60)
        print("提取到的文案:")
        print("=" * 60)
        print(text[:500] + "..." if len(text) > 500 else text)
        print(f"\n总字数: {len(text)}")
        
        # 1. 准备保存路径
        import os
        from datetime import datetime
        
        # 用户指定的默认路径
        base_dir = r"E:\icloud\iCloudDrive\iCloud~md~obsidian\myobsidian"
        if not os.path.exists(base_dir):
            try:
                os.makedirs(base_dir, exist_ok=True)
            except:
                print(f"⚠️ 无法创建目标目录 {base_dir}，将保存回当前目录。")
                base_dir = "."

        # 2. 文件名脱敏与构建
        def sanitize_filename(name):
            return re.sub(r'[\\/:\*\?"<>|]', '_', name).strip()
            
        clean_title = sanitize_filename(info.title if info.title else "未命名视频")
        filename = f"{clean_title}.md"
        full_path = os.path.join(base_dir, filename)

        # 3. 生成 YAML Frontmatter
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration_min = info.duration // 60
        duration_sec = info.duration % 60
        
        yaml_header = (
            "---\n"
            f"标题: {info.title}\n"
            f"作者: {info.author}\n"
            f"链接: {url}\n"
            f"时长: {duration_min}分{duration_sec}秒\n"
            f"提取时间: {current_time}\n"
            "---\n\n"
        )

        # 4. 格式化正文
        md_text = yaml_header + text
        md_text = md_text.replace("。", "。\n\n")
        md_text = md_text.replace("？", "？\n\n")
        
        # 简单的加粗优化
        md_text = re.sub(r"([一二三四五六七八九十]+、)", r"**\1**", md_text)
        md_text = re.sub(r"(第[一二三四五六七八九十]+[^，。 \n]+)", r"**\1**", md_text)

        # 5. 执行保存
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(md_text)
            
        print(f"\n✨ 处理完成！")
        print(f"📄 文件名: {filename}")
        print(f"📂 路径: {full_path}")
        
    except Exception as e:
        print(f"提取失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        extractor.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
