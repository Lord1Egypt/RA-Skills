#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度智能云 VOD 视频翻译工具

功能：
1. 支持本地视频文件处理
2. 支持从百度网盘下载后处理
3. 处理完成后可下载到本地或上传到网盘
4. 支持字幕翻译和语音翻译
5. 支持配音（音色复刻/AI配音）
6. 支持用户上传字幕文件
7. 支持自定义字幕样式
8. 支持项目管理

使用方法：
    # 基础用法 - 字幕翻译
    python3 translate.py /path/to/video.mp4 --source zh --target en
    
    # 语音翻译（配音）
    python3 translate.py /path/to/video.mp4 --source zh --target en --speech
    
    # 用户上传字幕
    python3 translate.py /path/to/video.mp4 --source zh --target en --subtitle-file subs.srt
    
    # 自定义字幕样式
    python3 translate.py /path/to/video.mp4 --source zh --target en --font-size 60 --font-color "#FFFFFFFF"
    
    # 项目管理
    python3 translate.py --list-projects
    python3 translate.py --delete-project pjt-xxx
    
    # 任务管理
    python3 translate.py --query tsk-xxx --project-id pjt-xxx
    python3 translate.py --list-tasks --project-id pjt-xxx
"""

import os
import sys
import argparse
from common import (
    get_credentials,
    upload_media,
    create_translate_project,
    query_translate_projects,
    delete_translate_projects,
    create_translate_task,
    update_translate_task,
    query_translate_tasks,
    query_translate_task,
    wait_for_task,
    download_result,
    check_bdpan_installed,
    check_bdpan_logged_in,
    download_from_netdisk,
    upload_to_netdisk,
    parse_srt_file,
    build_font_config,
    parse_area_string,
    SUPPORTED_LANGUAGES
)


def process_video(ak, sk, video_path, source_lang, target_lang, 
                  translation_types=None, subtitle_config=None, tts_config=None, 
                  project_type="ShortSeries", debug=False):
    """
    处理单个视频
    
    Args:
        ak: Access Key
        sk: Secret Key
        video_path: 视频文件路径
        source_lang: 源语言
        target_lang: 目标语言
        translation_types: 翻译类型列表 ["subtitle", "speech"]
        subtitle_config: 字幕配置
        tts_config: 配音配置
        project_type: 项目类型 (ShortSeries/Ecommerce)
        debug: 调试模式
    
    Returns:
        dict: 任务信息
    """
    file_name = os.path.basename(video_path)
    file_size = os.path.getsize(video_path) / (1024 * 1024)
    
    source_name = SUPPORTED_LANGUAGES.get(source_lang, (source_lang,))[0]
    target_name = SUPPORTED_LANGUAGES.get(target_lang, (target_lang,))[0]
    
    print(f"\n处理视频: {file_name} ({file_size:.1f} MB)")
    print(f"翻译方向: {source_name} → {target_name}")
    print(f"翻译类型: {', '.join(translation_types or ['subtitle'])}")
    
    # 上传视频
    print("  [1/3] 上传视频...")
    try:
        media_id = upload_media(ak, sk, video_path, debug=debug)
        print(f"        ✓ 媒资ID: {media_id}")
    except Exception as e:
        print(f"        ✗ 上传失败: {e}")
        return None
    
    # 创建翻译项目
    print("  [2/3] 创建翻译项目...")
    try:
        project_id = create_translate_project(ak, sk, project_type=project_type, debug=debug)
        print(f"        ✓ 项目ID: {project_id}")
    except Exception as e:
        print(f"        ✗ 创建项目失败: {e}")
        return None
    
    # 创建翻译任务
    print("  [3/3] 创建翻译任务...")
    try:
        task_results = create_translate_task(
            ak, sk, project_id, media_id,
            source_lang, target_lang,
            translation_types=translation_types,
            subtitle_config=subtitle_config,
            tts_config=tts_config,
            debug=debug
        )
        if task_results:
            task_id = task_results[0].get("taskId")
            print(f"        ✓ 任务ID: {task_id}")
        else:
            raise Exception("创建任务成功但未返回任务ID")
    except Exception as e:
        print(f"        ✗ 创建任务失败: {e}")
        return None
    
    return {
        "media_id": media_id,
        "project_id": project_id,
        "task_id": task_id,
        "file_name": file_name
    }


def query_and_display_projects(ak, sk, project_id=None, name=None, 
                                page_no=1, page_size=10, debug=False):
    """查询并显示项目列表"""
    print("\n" + "=" * 60)
    print("查询翻译项目")
    print("=" * 60)
    
    result = query_translate_projects(
        ak, sk,
        project_id=project_id,
        name=name,
        page_no=page_no,
        page_size=page_size,
        debug=debug
    )
    
    data = result.get("data", [])
    
    if not data:
        print("没有找到匹配的项目")
        return
    
    print(f"\n共找到 {result.get('totalCount', len(data))} 个项目:\n")
    
    for project in data:
        print(f"项目ID: {project.get('projectId')}")
        print(f"  名称: {project.get('name')}")
        print(f"  描述: {project.get('description', 'N/A')}")
        print(f"  创建时间: {project.get('createTime', 'N/A')}")
        print()


def query_and_display_tasks(ak, sk, project_id, task_id=None, media_id=None,
                            marker=None, max_size=10, debug=False):
    """查询并显示任务列表"""
    print("\n" + "=" * 60)
    print(f"查询项目 {project_id} 的翻译任务")
    print("=" * 60)
    
    result = query_translate_tasks(
        ak, sk, project_id,
        task_id=task_id,
        media_id=media_id,
        marker=marker,
        max_size=max_size,
        debug=debug
    )
    
    data = result.get("data", [])
    
    if not data:
        print("没有找到匹配的任务")
        return
    
    print(f"\n共找到 {len(data)} 个任务:\n")
    
    for task in data:
        print(f"任务ID: {task.get('taskId')}")
        print(f"  媒资ID: {task.get('mediaInfo', {}).get('mediaId')}")
        print(f"  名称: {task.get('name', 'N/A')}")
        print(f"  状态: {task.get('status')}")
        
        config = task.get('translationConfig', {})
        print(f"  翻译: {config.get('sourceLanguage')} → {config.get('targetLanguage')}")
        print(f"  类型: {', '.join(config.get('translationTypeList', []))}")
        
        if task.get('errMsg'):
            print(f"  错误: {task.get('errMsg')}")
        if task.get('url'):
            print(f"  结果URL: {task.get('url')[:80]}...")
        print()
    
    if result.get("isTruncated"):
        print(f"还有更多数据，使用 --marker {result.get('nextMarker')} 获取下一页")


def main():
    parser = argparse.ArgumentParser(
        description="百度智能云 VOD 视频翻译工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 字幕翻译
  python3 translate.py video.mp4 --source zh --target en
  
  # 语音翻译（配音）
  python3 translate.py video.mp4 --source zh --target en --speech
  
  # 用户上传字幕
  python3 translate.py video.mp4 --source zh --target en --subtitle-file subs.srt
  
  # 自定义字幕样式
  python3 translate.py video.mp4 --source zh --target en --font-size 60 --font-color "#FFFFFFFF"
  
  # 项目管理
  python3 translate.py --list-projects
  python3 translate.py --delete-project pjt-xxx
  
  # 任务管理
  python3 translate.py --query tsk-xxx --project-id pjt-xxx
  python3 translate.py --list-tasks --project-id pjt-xxx
        """
    )
    
    # 操作类型（使用可选参数避免 mutually_exclusive_group 限制）
    parser.add_argument("--video", nargs="+", metavar="PATH", help="本地视频文件路径（支持多个）")
    parser.add_argument("--netdisk", help="网盘视频路径")
    parser.add_argument("--query", metavar="TASK_ID", help="查询单个任务")
    parser.add_argument("--list-tasks", action="store_true", help="查询任务列表")
    parser.add_argument("--list-projects", action="store_true", help="查询项目列表")
    parser.add_argument("--delete-project", metavar="PROJECT_ID", help="删除项目")
    parser.add_argument("--update-task", metavar="TASK_ID", help="修改翻译任务")
    
    # 翻译参数
    parser.add_argument("--source", choices=SUPPORTED_LANGUAGES.keys(),
                        help="源语言")
    parser.add_argument("--target", choices=SUPPORTED_LANGUAGES.keys(),
                        help="目标语言")
    
    # 翻译类型
    parser.add_argument("--subtitle", action="store_true", default=True,
                        help="字幕翻译（默认启用）")
    parser.add_argument("--speech", action="store_true",
                        help="语音翻译（配音）")
    
    # 字幕配置
    parser.add_argument("--subtitle-source", choices=["ocr", "asr", "user"], default="ocr",
                        help="字幕来源: ocr(OCR识别), asr(语音识别), user(用户上传)")
    parser.add_argument("--subtitle-file", help="用户上传字幕文件（SRT格式）")
    parser.add_argument("--intro-subtitle-file", help="用户上传介绍字幕文件（SRT格式）")
    parser.add_argument("--no-burn-subtitle", action="store_true",
                        help="不烧录字幕到视频")
    parser.add_argument("--no-erase-subtitle", action="store_true",
                        help="不擦除原字幕")
    
    # OCR区域配置
    parser.add_argument("--ocr-areas", nargs="+", metavar="X,Y,W,H[,START,END]",
                        help="OCR识别区域，格式: x,y,width,height 或 x,y,width,height,start,end（时间范围秒）")
    parser.add_argument("--ocr-region-iou", type=int, choices=[0, 1], default=1,
                        help="OCR区域重叠阈值: 1=完全覆盖才识别(默认), 0=有交集即识别")
    
    # 字幕识别范围
    parser.add_argument("--text-types", nargs="+", 
                        choices=["dialog", "castName", "castDescription", "other"],
                        help="字幕识别范围")
    
    # 字幕擦除配置
    parser.add_argument("--erase-mode", choices=["global", "dialog", "manual"],
                        help="字幕擦除模式")
    parser.add_argument("--erase-areas", nargs="+", metavar="X,Y,W,H[,START,END]",
                        help="擦除区域，格式: x,y,width,height 或 x,y,width,height,start,end（时间范围秒）")
    parser.add_argument("--erase-model", choices=["v3", "v4"], default="v4",
                        help="擦除模型")
    
    # 字幕字体配置
    parser.add_argument("--font-family", choices=["Hei", "Song", "Kai"], default="Hei",
                        help="字体: Hei(黑体), Song(宋体), Kai(楷体)")
    parser.add_argument("--font-size", type=int, help="字号（像素）")
    parser.add_argument("--font-color", default="#FFFFFFFF", help="字体颜色 (#RRGGBBAA)")
    parser.add_argument("--font-outline-color", default="#000000FF", help="描边颜色")
    parser.add_argument("--font-outline-thickness", type=int, default=1, help="描边宽度")
    parser.add_argument("--font-bold", action="store_true", help="加粗")
    parser.add_argument("--font-italic", action="store_true", help="斜体")
    parser.add_argument("--font-underline", action="store_true", help="下划线")
    parser.add_argument("--font-strike-out", action="store_true", help="删除线")
    parser.add_argument("--font-alignment", choices=["left", "center", "right"], default="center",
                        help="对齐方式")
    parser.add_argument("--font-spacing", type=int, default=0, help="字间距（像素）")
    parser.add_argument("--font-line-spacing", type=float, default=0, help="行间距（字号的倍数）")
    parser.add_argument("--font-bg-color", default="#00000000", help="字幕区域背景颜色 (#RRGGBBAA)")
    parser.add_argument("--font-text-bg-color", default="#00000000", help="字体逐行背景颜色 (#RRGGBBAA)")
    parser.add_argument("--font-padding", type=int, default=0, help="字幕区域内边距（像素）")
    
    # 配音配置
    parser.add_argument("--tts-type", choices=["VOICE_CLONE", "AI_DUB"],
                        help="配音类型: VOICE_CLONE(音色复刻), AI_DUB(AI配音)")
    parser.add_argument("--voice-id", help="音色ID（AI配音时需要）")
    
    # 项目/任务管理参数
    parser.add_argument("--project-id", help="项目ID（查询任务时需要）")
    parser.add_argument("--project-type", choices=["ShortSeries", "Ecommerce"], default="ShortSeries",
                        help="项目类型: ShortSeries(短剧场景，默认), Ecommerce(电商场景)")
    parser.add_argument("--media-id", help="媒资ID筛选")
    parser.add_argument("--marker", help="分页游标")
    parser.add_argument("--max-size", type=int, default=10, help="每页数量")
    parser.add_argument("--project-name", help="项目名称筛选")
    
    # 任务修改参数
    parser.add_argument("--update-type", choices=["sourceSubtitle", "targetSubtitle"],
                        help="更新类型")
    parser.add_argument("--new-subtitle-file", help="新字幕文件")
    
    # 输出选项
    parser.add_argument("--output-dir", default="./output", help="输出目录")
    parser.add_argument("--upload-netdisk", action="store_true", help="处理后上传到网盘")
    parser.add_argument("--netdisk-dir", default="translated", help="网盘目标目录")
    
    # 其他选项
    parser.add_argument("--no-wait", action="store_true", help="不等待任务完成")
    parser.add_argument("--debug", action="store_true", help="显示调试信息")
    
    args = parser.parse_args()
    
    # 获取凭证
    ak, sk = get_credentials()
    
    # 删除项目
    if args.delete_project:
        print(f"删除项目: {args.delete_project}")
        try:
            delete_translate_projects(ak, sk, args.delete_project, debug=args.debug)
            print("✓ 删除成功")
        except Exception as e:
            print(f"✗ 删除失败: {e}")
            sys.exit(1)
        return
    
    # 查询项目列表
    if args.list_projects:
        query_and_display_projects(
            ak, sk,
            name=args.project_name,
            page_size=args.max_size,
            debug=args.debug
        )
        return
    
    # 查询单个任务
    if args.query:
        if not args.project_id:
            print("错误: 查询任务需要 --project-id 参数")
            sys.exit(1)
        
        task = query_translate_task(ak, sk, args.query, args.project_id, debug=args.debug)
        if task:
            print(f"\n任务ID: {task.get('taskId')}")
            print(f"项目ID: {task.get('projectId')}")
            print(f"媒资ID: {task.get('mediaId')}")
            print(f"状态: {task.get('status')}")
            if task.get('targetUrl'):
                print(f"结果URL: {task.get('targetUrl')}")
            if task.get('errMsg'):
                print(f"错误: {task.get('errMsg')}")
        else:
            print("未找到任务")
        return
    
    # 查询任务列表
    if args.list_tasks:
        if not args.project_id:
            print("错误: 查询任务列表需要 --project-id 参数")
            sys.exit(1)
        
        query_and_display_tasks(
            ak, sk, args.project_id,
            media_id=args.media_id,
            marker=args.marker,
            max_size=args.max_size,
            debug=args.debug
        )
        return
    
    # 修改任务
    if args.update_task:
        if not args.update_type or not args.new_subtitle_file:
            print("错误: 修改任务需要 --update-type 和 --new-subtitle-file 参数")
            sys.exit(1)
        
        subtitle_content = parse_srt_file(args.new_subtitle_file)
        try:
            new_task_id = update_translate_task(
                ak, sk, args.update_task,
                args.update_type, subtitle_content,
                debug=args.debug
            )
            print(f"✓ 任务已更新，新任务ID: {new_task_id}")
        except Exception as e:
            print(f"✗ 更新失败: {e}")
            sys.exit(1)
        return
    
    # 处理视频 - 检查必要参数
    if not args.source or not args.target:
        print("错误: 处理视频需要 --source 和 --target 参数")
        sys.exit(1)
    
    # 准备视频列表
    videos = []
    
    if args.netdisk:
        # 从网盘下载
        print("=" * 60)
        print("从百度网盘下载视频")
        print("=" * 60)
        
        if not check_bdpan_installed():
            print("错误: bdpan 未安装，无法从网盘下载")
            sys.exit(1)
        
        if not check_bdpan_logged_in():
            print("错误: bdpan 未登录，请先执行 bdpan login")
            sys.exit(1)
        
        # 创建临时目录
        temp_dir = "/tmp/vod_translate"
        os.makedirs(temp_dir, exist_ok=True)
        
        # 下载视频
        file_name = os.path.basename(args.netdisk)
        local_path = os.path.join(temp_dir, file_name)
        
        print(f"下载: {args.netdisk} -> {local_path}")
        if download_from_netdisk(args.netdisk, local_path, debug=args.debug):
            videos.append(local_path)
        else:
            print("下载失败")
            sys.exit(1)
    else:
        # 本地视频
        videos = args.video or []
    
    if not videos:
        print("错误: 没有指定视频文件")
        sys.exit(1)
    
    # 构建翻译类型
    translation_types = []
    if args.subtitle:
        translation_types.append("subtitle")
    if args.speech:
        translation_types.append("speech")
    if not translation_types:
        translation_types = ["subtitle"]
    
    # 构建字幕配置
    subtitle_config = {
        "recognitionType": args.subtitle_source.upper(),
        "targetSubtitleCompose": not args.no_burn_subtitle
    }
    
    # OCR区域配置
    if args.ocr_areas:
        area_list = []
        for area_str in args.ocr_areas:
            area = parse_area_string(area_str)
            if area:
                area_list.append(area)
        if area_list:
            subtitle_config["ocrConfig"] = {
                "areaList": area_list,
                "regionIOU": args.ocr_region_iou
            }
    elif args.ocr_region_iou != 1:
        # 只设置 regionIOU，不设置区域
        subtitle_config["ocrConfig"] = {"regionIOU": args.ocr_region_iou}
    
    # 字幕识别范围
    if args.text_types:
        subtitle_config["textTypeList"] = args.text_types
    
    # 用户上传字幕
    if args.subtitle_file:
        subtitle_config["dialogSubtitleFile"] = parse_srt_file(args.subtitle_file)
    if args.intro_subtitle_file:
        subtitle_config["introSubtitleFile"] = parse_srt_file(args.intro_subtitle_file)
    
    # 字幕擦除配置
    if not args.no_erase_subtitle and args.erase_mode:
        desubtitle_config = {
            "modelType": args.erase_model,
            "desubtitleType": args.erase_mode
        }
        if args.erase_areas:
            area_list = []
            for area_str in args.erase_areas:
                area = parse_area_string(area_str)
                if area:
                    area_list.append(area)
            if area_list:
                desubtitle_config["areaList"] = area_list
        subtitle_config["desubtitleConfig"] = desubtitle_config
    elif not args.no_erase_subtitle:
        # 默认擦除配置
        subtitle_config["desubtitleConfig"] = {
            "modelType": "v4",
            "desubtitleType": "global"
        }
    
    # 字幕字体配置
    font_config = build_font_config(
        family=args.font_family,
        size=args.font_size,
        color=args.font_color,
        outline_color=args.font_outline_color,
        outline_thickness=args.font_outline_thickness,
        bold=args.font_bold,
        italic=args.font_italic,
        underline=args.font_underline,
        strike_out=args.font_strike_out,
        alignment=args.font_alignment,
        spacing=args.font_spacing,
        line_spacing=args.font_line_spacing,
        bg_color=args.font_bg_color,
        font_bg_color=args.font_text_bg_color,
        padding=args.font_padding
    )
    subtitle_config["fontConfig"] = {"dialog": font_config}
    
    # 配音配置
    tts_config = None
    if args.speech and args.tts_type:
        tts_config = {"type": args.tts_type}
        if args.tts_type == "AI_DUB" and args.voice_id:
            tts_config["voiceList"] = [{"voiceId": args.voice_id}]
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 处理视频
    print("\n" + "=" * 60)
    print("开始处理视频")
    print("=" * 60)
    
    tasks = []
    for video_path in videos:
        if not os.path.exists(video_path):
            print(f"跳过: 文件不存在 - {video_path}")
            continue
        
        result = process_video(
            ak, sk, video_path,
            args.source, args.target,
            translation_types=translation_types,
            subtitle_config=subtitle_config,
            tts_config=tts_config,
            project_type=args.project_type,
            debug=args.debug
        )
        if result:
            tasks.append(result)
    
    if not tasks:
        print("没有成功创建任何任务")
        sys.exit(1)
    
    # 等待任务完成
    if args.no_wait:
        print("\n任务已创建，使用以下命令查询状态:")
        for task in tasks:
            print(f"  python3 translate.py --query {task['task_id']} --project-id {task['project_id']}")
        return
    
    print("\n" + "=" * 60)
    print("等待任务完成")
    print("=" * 60)
    
    results = []
    for task in tasks:
        print(f"\n等待: {task['file_name']}")
        result = wait_for_task(ak, sk, task['task_id'], 
                               task['project_id'],
                               max_retries=180, interval=10, debug=args.debug)
        
        if result and result.get("status") in ["FINISHED", "SUCCESS"]:
            task["result"] = result
            results.append(task)
            print(f"  ✓ 完成")
        else:
            print(f"  ✗ 失败或超时")
            if result:
                print(f"    状态: {result.get('status')}")
                if result.get("errMsg"):
                    print(f"    错误: {result.get('errMsg')}")
    
    # 下载结果
    print("\n" + "=" * 60)
    print("下载处理结果")
    print("=" * 60)
    
    for task in results:
        if not task.get("result"):
            continue
        
        target_url = task["result"].get("targetUrl")
        if not target_url:
            continue
        
        # 生成输出文件名
        base_name = os.path.splitext(task['file_name'])[0]
        output_name = f"{base_name}_{args.target}.mp4"
        output_path = os.path.join(args.output_dir, output_name)
        
        print(f"\n下载: {task['file_name']}")
        if download_result(target_url, output_path, debug=args.debug):
            task["output_path"] = output_path
            
            # 上传到网盘
            if args.upload_netdisk:
                print(f"上传到网盘: {args.netdisk_dir}/{output_name}")
                if upload_to_netdisk(output_path, f"{args.netdisk_dir}/{output_name}", debug=args.debug):
                    task["netdisk_path"] = f"{args.netdisk_dir}/{output_name}"
    
    # 输出结果
    print("\n" + "=" * 60)
    print("处理完成")
    print("=" * 60)
    
    for task in results:
        print(f"\n{task['file_name']}:")
        print(f"  任务ID: {task['task_id']}")
        print(f"  项目ID: {task['project_id']}")
        if task.get("output_path"):
            print(f"  本地文件: {task['output_path']}")
        if task.get("netdisk_path"):
            print(f"  网盘路径: {task['netdisk_path']}")


if __name__ == "__main__":
    main()
