#!/usr/bin/env python3
"""
DiT360 全景图生成器
调用 Hugging Face Space 生成全景图
"""

import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

def generate_panorama(prompt: str, seed: int = 42, steps: int = 50, output_dir: str = None):
    """
    生成全景图
    
    Args:
        prompt: 描述文字
        seed: 随机种子
        steps: 推理步数
        output_dir: 输出目录
    
    Returns:
        dict: 包含 image_path, viewer_path, viewer_url
    """
    try:
        from gradio_client import Client
    except ImportError:
        print("❌ 请先安装 gradio_client: uv pip install gradio_client")
        sys.exit(1)
    
    # 设置输出目录
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "output"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"🎨 正在生成全景图...")
    print(f"   描述: {prompt}")
    print(f"   Seed: {seed}")
    print(f"   步数: {steps}")
    print(f"   注意: 首次生成需要等待 Hugging Face Space 启动（可能需几分钟）")
    print()
    
    # 连接 Hugging Face Space
    client = Client("Insta360-Research/DiT360")
    
    # 调用生成
    result = client.predict(
        prompt,
        float(seed),
        float(steps),
        api_name="/infer"
    )
    
    # 复制到输出目录
    webp_path = output_dir / f"panorama_{timestamp}.webp"
    shutil.copy(result, webp_path)
    
    print(f"✅ 生成完成: {webp_path}")
    
    # 转换为 jpg
    jpg_path = output_dir / f"panorama_{timestamp}.jpg"
    os.system(f'sips -s format jpeg "{webp_path}" --out "{jpg_path}" > /dev/null 2>&1')
    
    print(f"✅ 转换完成: {jpg_path}")
    
    # 创建查看器
    viewer_path = create_viewer(jpg_path, output_dir)
    
    return {
        "webp_path": str(webp_path),
        "jpg_path": str(jpg_path),
        "viewer_path": str(viewer_path),
        "viewer_url": f"http://localhost:8899/{viewer_path.name}"
    }

def create_viewer(image_path: Path, output_dir: Path):
    """创建 Pannellum 查看器"""
    
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiT360 全景查看器</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css">
    <script src="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js"></script>
    <style>
        body {{ margin: 0; background: #000; }}
        #panorama {{ width: 100vw; height: 100vh; }}
        .title {{
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
            color: white; font-family: sans-serif; font-size: 18px;
            text-shadow: 0 0 10px rgba(0,0,0,0.8); z-index: 10; pointer-events: none;
        }}
    </style>
</head>
<body>
    <div class="title">DiT360 全景图 - 鼠标拖动查看 · 滚轮缩放</div>
    <div id="panorama"></div>
    <script>
        pannellum.viewer('panorama', {{
            type: "equirectangular",
            panorama: "{image_path.name}",
            autoLoad: true,
            showControls: true,
            mouseZoom: true,
            draggable: true,
            hfov: 75
        }});
    </script>
</body>
</html>'''
    
    viewer_path = output_dir / "viewer.html"
    viewer_path.write_text(html_content, encoding='utf-8')
    
    print(f"✅ 查看器创建: {viewer_path}")
    
    return viewer_path

def start_server(output_dir: Path, port: int = 8899):
    """启动 HTTP 服务器"""
    import subprocess
    
    # 检查端口是否被占用
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    
    if result != 0:
        # 端口空闲，启动服务器
        subprocess.Popen(
            ['python3', '-m', 'http.server', str(port)],
            cwd=str(output_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"🚀 HTTP 服务器启动: http://localhost:{port}/viewer.html")
    else:
        print(f"⚠️  端口 {port} 已被占用，假设服务器已在运行")
        print(f"   查看地址: http://localhost:{port}/viewer.html")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generator.py '描述文字' [seed] [steps]")
        print("示例: python generator.py 'sunset over ocean' 42 50")
        sys.exit(1)
    
    prompt = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    
    result = generate_panorama(prompt, seed, steps)
    
    print()
    print("=" * 50)
    print("🎉 生成完成!")
    print(f"   图片: {result['jpg_path']}")
    print(f"   查看: {result['viewer_url']}")
    print("=" * 50)
    
    # 启动服务器
    output_dir = Path(result['viewer_path']).parent
    start_server(output_dir)
