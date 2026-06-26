#!/usr/bin/env python3
"""
B站学术视频分析器 - 主入口

功能:
- 检查登录状态
- 下载视频
- 转录字幕
- LLM 分析
- 截取关键画面
- 生成学习报告
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Optional

# 导入 bilibili_dl 模块
try:
    from bilibili_dl.auth import BilibiliAuth
    from bilibili_dl.parser import BilibiliParser
except ImportError:
    print("❌ 未找到 bilibili_dl 模块")
    print("\n请先安装:")
    print("  pip install railgun-bili-tools")
    print("\n详细安装说明见: https://github.com/railgun9983/bilibili-download")
    sys.exit(1)

# 导入本地模块
from srt_parser import parse_srt_file, get_full_transcript
from screenshot_tool import check_ffmpeg, batch_capture
from llm_analyzer import interactive_analyze, save_analysis_result
from report_generator import generate_markdown


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         B站学术视频分析器  v1.0.0                             ║
║                                                              ║
║         自动提取知识点 · 生成学习报告                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_login_status() -> Optional[Dict]:
    """检查登录状态,未登录则引导登录
    
    Returns:
        Optional[Dict]: 登录凭证,包含 cookies 和 user_info
    """
    print("\n[步骤 1/7] 检查登录状态...")
    print("-" * 60)
    
    auth = BilibiliAuth()
    credentials = auth.load_credentials()
    
    if credentials:
        username = credentials['user_info']['username']
        print(f"✅ 已登录用户: {username}")
        return credentials['cookies']
    else:
        print("⚠️  检测到未登录")
        print("\n请使用 B站 App 扫描二维码登录:")
        
        # 调用登录流程
        try:
            auth.login()
            credentials = auth.load_credentials()
            if credentials:
                print("✅ 登录成功!")
                return credentials['cookies']
            else:
                raise Exception("登录失败")
        except KeyboardInterrupt:
            print("\n\n❌ 用户取消登录")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ 登录失败: {e}")
            print("\n提示: 如果扫码登录失败,可以使用手动导入Cookie方式")
            print("     参考文档: README.md")
            sys.exit(1)


def parse_video_info(video_url: str, cookies: Optional[Dict]) -> Dict:
    """解析视频信息
    
    Args:
        video_url: 视频链接或 BV 号
        cookies: 登录 cookies
    
    Returns:
        Dict: 视频信息
    """
    print("\n[步骤 2/7] 解析视频信息...")
    print("-" * 60)
    
    try:
        parser = BilibiliParser(cookies)
        bvid = parser.extract_bvid(video_url)
        
        print(f"正在获取视频信息: {bvid}")
        video_info = parser.get_video_info(bvid)
        
        print(f"\n✅ 视频解析成功:")
        print(f"  标题: {video_info['title']}")
        print(f"  UP主: {video_info['owner']['name']}")
        print(f"  时长: {video_info['duration']}秒")
        
        return video_info
        
    except Exception as e:
        print(f"\n❌ 视频解析失败: {e}")
        sys.exit(1)


def download_video(video_url: str, output_dir: Path) -> Path:
    """下载视频
    
    Args:
        video_url: 视频链接或 BV 号
        output_dir: 输出目录
    
    Returns:
        Path: 下载的视频文件路径
    """
    print("\n[步骤 3/7] 下载视频...")
    print("-" * 60)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 使用 bili-dl 命令行工具
    cmd = [
        'bili-dl', 'download', video_url,
        '--quality', '1080p',
        '--output', str(output_dir)
    ]
    
    print(f"执行命令: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            # 查找下载的视频文件
            video_files = list(output_dir.rglob("*.mp4"))
            
            if not video_files:
                raise Exception("未找到下载的视频文件")
            
            # 使用最新的视频文件
            video_path = max(video_files, key=lambda p: p.stat().st_mtime)
            
            print(f"\n✅ 视频已下载: {video_path}")
            return video_path
        else:
            raise Exception(f"下载失败,退出码: {result.returncode}")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 视频下载失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


def transcribe_video(video_path: Path) -> Path:
    """转录视频生成字幕
    
    Args:
        video_path: 视频文件路径
    
    Returns:
        Path: SRT 字幕文件路径
    """
    print("\n[步骤 4/7] 转录视频生成字幕...")
    print("-" * 60)
    
    video_path = Path(video_path)
    
    # 使用 bili-dl 命令行工具
    cmd = [
        'bili-dl', 'transcribe',
        str(video_path),
        '--model', 'medium',
        '--srt'
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    print("\n提示: 转录过程可能需要较长时间,请耐心等待...")
    print("      首次使用需要下载 Whisper medium 模型(约769MB)\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            # SRT 文件应该和视频在同一目录
            srt_path = video_path.parent / f"{video_path.stem}.srt"
            
            if not srt_path.exists():
                raise Exception("未找到生成的 SRT 文件")
            
            print(f"\n✅ 字幕已生成: {srt_path}")
            return srt_path
        else:
            raise Exception(f"转录失败,退出码: {result.returncode}")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 字幕转录失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


def analyze_with_llm(video_info: Dict, srt_path: Path) -> Dict:
    """使用 LLM 分析字幕内容
    
    Args:
        video_info: 视频信息
        srt_path: SRT 字幕文件路径
    
    Returns:
        Dict: 分析结果
    """
    print("\n[步骤 5/7] LLM 分析字幕内容...")
    print("-" * 60)
    
    try:
        # 读取 SRT 内容
        srt_content = srt_path.read_text(encoding='utf-8')
        
        # 交互式分析
        analysis_result = interactive_analyze(video_info, srt_content)
        
        # 保存分析结果
        analysis_json_path = srt_path.parent / f"{srt_path.stem}_analysis.json"
        save_analysis_result(analysis_result, analysis_json_path)
        
        return analysis_result
        
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消分析")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ LLM 分析失败: {e}")
        sys.exit(1)


def capture_screenshots(video_path: Path, analysis_result: Dict, output_dir: Path) -> Dict[float, Path]:
    """截取关键画面
    
    Args:
        video_path: 视频文件路径
        analysis_result: LLM 分析结果
        output_dir: 输出目录
    
    Returns:
        Dict[float, Path]: 时间戳到截图路径的映射
    """
    print("\n[步骤 6/7] 截取关键画面...")
    print("-" * 60)
    
    try:
        # 准备截图目录
        screenshots_dir = output_dir / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        # 提取时间戳列表
        key_screenshots = analysis_result['key_screenshots']
        
        print(f"需要截取 {len(key_screenshots)} 张关键画面")
        
        # 批量截图
        screenshot_mapping = batch_capture(
            video_path=video_path,
            timestamps=key_screenshots,
            output_dir=screenshots_dir,
            quality=2,
            max_workers=4,
            show_progress=True
        )
        
        return screenshot_mapping
        
    except Exception as e:
        print(f"\n❌ 截图失败: {e}")
        print("提示: 请确保 FFmpeg 已正确安装")
        sys.exit(1)


def generate_report(
    video_info: Dict,
    analysis_result: Dict,
    screenshot_mapping: Dict[float, Path],
    srt_path: Path,
    output_dir: Path
) -> Path:
    """生成 Markdown 报告
    
    Args:
        video_info: 视频信息
        analysis_result: LLM 分析结果
        screenshot_mapping: 截图映射
        srt_path: SRT 字幕文件路径
        output_dir: 输出目录
    
    Returns:
        Path: 生成的报告路径
    """
    print("\n[步骤 7/7] 生成 Markdown 报告...")
    print("-" * 60)
    
    try:
        # 读取完整字幕
        srt_content = srt_path.read_text(encoding='utf-8')
        
        # 生成报告
        report_path = generate_markdown(
            video_info=video_info,
            analysis=analysis_result,
            screenshots=screenshot_mapping,
            srt_content=srt_content,
            output_dir=output_dir
        )
        
        return report_path
        
    except Exception as e:
        print(f"\n❌ 报告生成失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='B站学术视频分析器 - 自动提取知识点并生成学习报告',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s BV1ms4y1Y76i
  %(prog)s https://www.bilibili.com/video/BV1ms4y1Y76i
  %(prog)s BV1ms4y1Y76i --output ./my_reports

更多信息见: README.md
        """
    )
    
    parser.add_argument(
        'video_url',
        help='B站视频链接或BV号'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='./reports',
        help='报告输出目录 (默认: ./reports)'
    )
    
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    try:
        # 环境检查
        print("检查运行环境...")
        check_ffmpeg()
        print()
        
        # 执行分析流程
        output_dir = Path(args.output)
        
        # 1. 检查登录状态
        cookies = check_login_status()
        
        # 2. 解析视频信息
        video_info = parse_video_info(args.video_url, cookies)
        
        # 3. 下载视频
        video_path = download_video(args.video_url, output_dir)
        
        # 4. 转录字幕
        srt_path = transcribe_video(video_path)
        
        # 5. LLM 分析
        analysis_result = analyze_with_llm(video_info, srt_path)
        
        # 6. 截取关键画面
        screenshot_mapping = capture_screenshots(video_path, analysis_result, output_dir)
        
        # 7. 生成报告
        report_path = generate_report(
            video_info,
            analysis_result,
            screenshot_mapping,
            srt_path,
            output_dir
        )
        
        # 完成
        print("\n" + "=" * 60)
        print("🎉 分析完成!")
        print("=" * 60)
        print(f"\n📄 报告路径: {report_path}")
        print(f"📸 截图目录: {output_dir / 'screenshots'}")
        print(f"📝 字幕文件: {srt_path}")
        print("\n提示: 可以使用 Markdown 编辑器(如 Typora、VS Code)查看报告")
        print()
        
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
