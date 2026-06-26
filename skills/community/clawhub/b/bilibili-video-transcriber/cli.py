#!/usr/bin/env python3
"""
B站视频转录专家 - 命令行工具
"""

import os
import sys
import json
import time
import argparse
import logging
from pathlib import Path
from typing import List, Optional

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from bilibili_transcriber import BilibiliTranscriber, ProcessingResult
from cookie_manager import (
    save_cookie, load_cookie, check_cookie_valid,
    needs_cookie_refresh, COOKIE_ACTIVE_PATH,
    BilibiliQRLogin, send_qr_via_feishu
)

def setup_logging(verbose: bool = False, debug: bool = False):
    """设置日志"""
    level = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('bilibili_transcriber.log')
        ]
    )

def print_result(result: ProcessingResult, show_transcript: bool = False):
    """打印处理结果"""
    if result.success:
        print("\n" + "="*60)
        print("✅ 处理成功！")
        print("="*60)
        
        if result.video_info:
            print(f"📺 视频标题: {result.video_info.title}")
            print(f"🔗 BV号: {result.video_info.bvid}")
            print(f"⏱️ 时长: {result.video_info.duration}秒")
            print(f"👤 UP主: {result.video_info.up_name}")
        
        if result.transcript_path:
            print(f"📄 转录文件: {result.transcript_path}")
        
        if result.audio_path:
            print(f"🎵 音频文件: {result.audio_path}")
        
        if result.feishu_doc_url:
            print(f"📄 飞书文档: {result.feishu_doc_url}")
        
        if result.processing_time:
            print(f"⏰ 处理时间: {result.processing_time:.2f}秒")
        
        # 显示评论信息
        if result.comments:
            hot_count = len([c for c in result.comments if not c.reply_to])
            reply_count = len([c for c in result.comments if c.reply_to])
            print(f"💬 评论: 获取 {hot_count} 条热评 + {reply_count} 条回复")
            if show_transcript or True:  # 默认展示前3条热评
                print("\n💬 热门评论（前3条）:")
                shown = 0
                for c in result.comments:
                    if not c.reply_to and shown < 3:
                        msg_preview = c.message[:80] + ("..." if len(c.message) > 80 else "")
                        print(f"  0001F44D{C.LIKE} [{C.USER}] {MSG_PREVIEW}")
                        shown += 1
        
        if result.transcript and show_transcript:
            print("\n📝 转录内容（前5段）:")
            for i, seg in enumerate(result.transcript[:5]):
                print(f"  [{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")
            
            if len(result.transcript) > 5:
                print(f"  ... 还有 {len(result.transcript) - 5} 段")
        
        if result.warnings:
            print("\n⚠️ 警告:")
            for warning in result.warnings:
                print(f"  - {warning}")
        
        print("="*60)
        
    else:
        print("\n" + "="*60)
        print("❌ 处理失败！")
        print("="*60)
        print(f"错误: {result.error}")
        print("="*60)

def process_single(
    bvid: str,
    cookie_file: Optional[str],
    model: str,
    output_dir: str,
    output_format: str,
    keep_audio: bool,
    verbose: bool,
    debug: bool
) -> bool:
    """处理单个视频"""
    try:
        # 初始化转录器
        transcriber = BilibiliTranscriber(
            cookie_file=cookie_file,
            model_name=model,
            output_dir=output_dir,
            keep_audio=keep_audio
        )
        
        # 处理视频
        result = transcriber.process(
            bvid=bvid,
            output_format=output_format,
            validate=True
        )
        
        # 打印结果
        print_result(result, show_transcript=verbose)
        
        return result.success
        
    except Exception as e:
        logging.error(f"处理失败: {e}")
        print(f"\n❌ 处理失败: {e}")
        return False

def process_batch(
    bvid_file: str,
    cookie_file: Optional[str],
    model: str,
    output_dir: str,
    output_format: str,
    keep_audio: bool,
    parallel: int,
    verbose: bool,
    debug: bool
) -> bool:
    """批量处理视频"""
    try:
        # 读取BV号列表
        with open(bvid_file, 'r') as f:
            lines = f.readlines()
        
        bvids = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # 提取BV号
                if 'BV' in line:
                    # 从URL中提取BV号
                    import re
                    match = re.search(r'BV[0-9A-Za-z]{10}', line)
                    if match:
                        bvids.append(match.group(0))
                    else:
                        bvids.append(line)
                else:
                    bvids.append(line)
        
        if not bvids:
            print("❌ 未找到有效的BV号")
            return False
        
        print(f"📋 找到 {len(bvids)} 个视频需要处理")
        
        # 初始化转录器
        transcriber = BilibiliTranscriber(
            cookie_file=cookie_file,
            model_name=model,
            output_dir=output_dir,
            keep_audio=keep_audio
        )
        
        success_count = 0
        fail_count = 0
        
        # 顺序处理
        for i, bvid in enumerate(bvids, 1):
            print(f"\n📊 处理进度: {i}/{len(bvids)} ({bvid})")
            
            try:
                result = transcriber.process(
                    bvid=bvid,
                    output_format=output_format,
                    validate=True
                )
                
                if result.success:
                    success_count += 1
                    print(f"✅ 成功: {bvid}")
                else:
                    fail_count += 1
                    print(f"❌ 失败: {bvid} - {result.error}")
                    
            except Exception as e:
                fail_count += 1
                print(f"❌ 异常: {bvid} - {e}")
        
        # 打印统计
        print("\n" + "="*60)
        print("📊 批量处理完成")
        print("="*60)
        print(f"✅ 成功: {success_count}")
        print(f"❌ 失败: {fail_count}")
        print(f"📈 成功率: {success_count/len(bvids)*100:.1f}%")
        print("="*60)
        
        return fail_count == 0
        
    except Exception as e:
        logging.error(f"批量处理失败: {e}")
        print(f"\n❌ 批量处理失败: {e}")
        return False

def check_cookie(cookie_file: Optional[str]) -> bool:
    """检查Cookie状态"""
    try:
        from bilibili_api import sync, Credential
        
        # 尝试加载Cookie
        if cookie_file and Path(cookie_file).exists():
            with open(cookie_file, 'r') as f:
                cookie_str = f.read().strip()
            
            # 解析Cookie
            cookies = {}
            for item in cookie_str.split('; '):
                if '=' in item:
                    k, v = item.split('=', 1)
                    cookies[k] = v
            
            # 创建凭证
            credential = Credential(
                sessdata=cookies.get('SESSDATA', ''),
                bili_jct=cookies.get('bili_jct', ''),
                buvid3=cookies.get('buvid3', '')
            )
            
            # 测试凭证
            from bilibili_api import user
            u = user.User(credential=credential)
            info = sync(u.get_user_info())
            
            print("✅ Cookie有效")
            print(f"👤 用户: {info.get('name', '未知')}")
            print(f"📧 邮箱: {info.get('email', '未设置')}")
            print(f"📱 手机: {info.get('mobile', '未设置')}")
            
            return True
            
        else:
            print("❌ Cookie文件不存在")
            return False
            
    except Exception as e:
        print(f"❌ Cookie检查失败: {e}")
        return False

def update_cookie(cookie_file: str, cookie_str: str) -> bool:
    """更新Cookie"""
    try:
        # 确保目录存在
        Path(cookie_file).parent.mkdir(parents=True, exist_ok=True)
        
        # 保存Cookie
        with open(cookie_file, 'w') as f:
            f.write(cookie_str.strip())
        
        print(f"✅ Cookie已更新: {cookie_file}")
        
        # 验证Cookie
        return check_cookie(cookie_file)
        
    except Exception as e:
        print(f"❌ 更新Cookie失败: {e}")
        return False

def interactive_login() -> bool:
    """
    交互式扫码登录
    生成二维码并输出到文件/飞书信号
    """
    print("\n" + "="*60)
    print("📱 B 站扫码登录")
    print("="*60)
    
    login = BilibiliQRLogin()
    
    # 生成二维码
    print("\n⏳ 正在生成二维码...")
    qr_path = login.generate_qr_code()
    print(f"✅ 二维码已生成")
    print(f"🖼️  图片路径: {qr_path}")
    
    # 通过飞书发送二维码
    print("📨 正在通过飞书发送二维码...")
    sent = send_qr_via_feishu(qr_path)
    if sent:
        print("✅ 二维码已通过飞书发送，请查看飞书消息扫码")
        print("   扫码后请回复「已扫码」")
    else:
        print("⚠️ 飞书发送失败，请手动打开二维码图片扫码")
        print(f"   二维码图片: {qr_path}")
    
    # 轮询等待
    print("\n⏳ 等待扫码中（180秒超时）...")
    result = login.poll_login(timeout_seconds=180)
    
    if result.get('success'):
        print(f"\n✅ 登录成功！")
        print(f"👤 用户: {result.get('username')}")
        print(f"🏆 大会员: {'✅' if result.get('is_vip') else '❌'}")
        print(f"💾 Cookie 已自动保存到冗余存储")
        return True
    else:
        print(f"\n❌ 登录失败: {result.get('error', '超时')}")
        print("请重新运行 --login 再试")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='B站视频转录专家 - 专业处理B站视频字幕问题',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 处理单个视频
  %(prog)s BV1txQGByERW
  
  # 扫码登录
  %(prog)s --login
  
  # 检查Cookie状态
  %(prog)s --check-cookie
  
  # 更新Cookie
  %(prog)s --update-cookie "SESSDATA=xxx; bili_jct=xxx"
  
  # 指定Cookie文件
  %(prog)s BV1txQGByERW --cookie ~/.bilibili_cookie.txt
  
  # 批量处理
  %(prog)s --batch bv_list.txt
        """
    )
    
    # 视频参数（改为非必填）
    parser.add_argument(
        'bvid',
        nargs='?',
        help='B站视频BV号'
    )
    parser.add_argument(
        '--batch',
        metavar='FILE',
        help='批量处理，指定包含BV号列表的文件'
    )
    
    # 功能参数
    parser.add_argument(
        '--login',
        action='store_true',
        help='扫码登录B站（推荐）'
    )
    parser.add_argument(
        '--check-cookie',
        action='store_true',
        help='检查Cookie状态'
    )
    parser.add_argument(
        '--update-cookie',
        metavar='COOKIE_STRING',
        help='更新Cookie'
    )
    
    # 配置参数
    parser.add_argument(
        '--cookie',
        metavar='FILE',
        help='Cookie文件路径（默认由 cookie_manager 管理）'
    )
    parser.add_argument(
        '--model',
        choices=['base', 'small', 'medium'],
        default='base',
        help='Whisper模型（默认: base）'
    )
    parser.add_argument(
        '--output',
        metavar='DIR',
        default='./bilibili_transcripts',
        help='输出目录（默认: ./bilibili_transcripts）'
    )
    parser.add_argument(
        '--format',
        choices=['txt', 'json', 'markdown'],
        default='txt',
        help='输出格式（默认: txt）'
    )
    parser.add_argument(
        '--keep-audio',
        action='store_true',
        help='保留音频文件'
    )
    parser.add_argument(
        '--parallel',
        type=int,
        default=1,
        help='并行处理数量（默认: 1）'
    )
    
    # 调试参数
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='详细输出'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='调试模式'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='B站视频转录专家 v2.0 - Cookie管理增强版'
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.verbose, args.debug)
    
    # 处理不同模式
    try:
        if args.login:
            # 扫码登录模式
            success = interactive_login()
            sys.exit(0 if success else 1)
        
        elif args.check_cookie:
            # 检查 Cookie 状态
            print("\n📋 Cookie 状态检查")
            print("=" * 60)
            
            cookie_str = load_cookie()
            if cookie_str:
                check = check_cookie_valid(cookie_str)
                if check["valid"]:
                    print(f"✅ Cookie 有效")
                    print(f"👤 用户: {check.get('username')}")
                    print(f"🏆 大会员: {'✅' if check.get('is_vip') else '❌'}")
                else:
                    print(f"❌ Cookie 已失效: {check.get('error')}")
                    print(f"   请运行 '{sys.argv[0]} --login' 重新登录")
                print(f"📂 存储路径: {COOKIE_ACTIVE_PATH}")
            else:
                print(f"❌ Cookie 文件不存在")
                print(f"   请运行 '{sys.argv[0]} --login' 进行扫码登录")
            
            sys.exit(0 if (cookie_str and check.get('valid')) else 1)
        
        elif args.update_cookie:
            # 更新Cookie
            success = save_cookie(args.update_cookie)
            if success:
                check = check_cookie_valid(args.update_cookie)
                if check["valid"]:
                    print(f"✅ Cookie 已更新，用户: {check['username']}")
                else:
                    print(f"⚠️ Cookie 已保存但可能无效: {check.get('error')}")
            else:
                print("❌ 保存 Cookie 失败")
            sys.exit(0 if success else 1)
        
        elif args.batch:
            # 批量处理模式
            success = process_batch(
                bvid_file=args.batch,
                cookie_file=args.cookie,
                model=args.model,
                output_dir=args.output,
                output_format=args.format,
                keep_audio=args.keep_audio,
                parallel=args.parallel,
                verbose=args.verbose,
                debug=args.debug
            )
            sys.exit(0 if success else 1)
        
        elif args.bvid:
            # 单个视频处理模式
            success = process_single(
                bvid=args.bvid,
                cookie_file=args.cookie,
                model=args.model,
                output_dir=args.output,
                output_format=args.format,
                keep_audio=args.keep_audio,
                verbose=args.verbose,
                debug=args.debug
            )
            sys.exit(0 if success else 1)
        
        else:
            parser.print_help()
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断")
        sys.exit(130)
    
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()