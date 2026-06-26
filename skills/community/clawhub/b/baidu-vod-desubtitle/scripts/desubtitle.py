#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度智能云 VOD 字幕擦除工具

功能：
1. 支持本地视频文件处理
2. 支持从百度网盘下载后处理
3. 处理完成后可下载到本地或上传到网盘
4. 支持全局/对白/自定义区域三种擦除模式
5. 支持时间范围擦除
6. 支持任务查询和删除

使用方法：
    # 基础用法 - 全局擦除
    python3 desubtitle.py /path/to/video.mp4 --mode global
    
    # 对白字幕擦除
    python3 desubtitle.py /path/to/video.mp4 --mode dialog
    
    # 自定义区域擦除
    python3 desubtitle.py /path/to/video.mp4 --mode manual --areas "60,500,100,100" "60,100,100,100"
    
    # 带时间范围的区域擦除
    python3 desubtitle.py /path/to/video.mp4 --mode manual --areas "60,500,100,100" --time-range 0 10000
    
    # 从网盘下载处理
    python3 desubtitle.py --netdisk /apps/bdpan/video.mp4 --mode global
    
    # 处理后上传到网盘
    python3 desubtitle.py /path/to/video.mp4 --mode global --upload-netdisk
    
    # 查询任务
    python3 desubtitle.py --query tsk-xxx
    python3 desubtitle.py --list --status RUNNING
    python3 desubtitle.py --list --media-id mda-xxx
    
    # 删除任务
    python3 desubtitle.py --delete tsk-xxx tsk-yyy
"""

import os
import sys
import argparse
from common import (
    get_credentials,
    upload_media,
    create_desubtitle_task,
    query_desubtitle_tasks,
    query_desubtitle_task,
    delete_desubtitle_tasks,
    wait_for_task,
    download_result,
    check_bdpan_installed,
    check_bdpan_logged_in,
    download_from_netdisk,
    upload_to_netdisk,
    parse_area_string
)


def process_video(ak, sk, video_path, mode="global", model_type="v4", 
                  areas=None, time_range=None, debug=False):
    """
    处理单个视频
    
    Args:
        ak: Access Key
        sk: Secret Key
        video_path: 视频文件路径
        mode: 擦除模式 (global/dialog/manual)
        model_type: 模型类型 (v3/v4)
        areas: 区域列表 ["x,y,w,h" 或 "x,y,w,h,start,end"]
        time_range: 时间范围 (start_ms, end_ms)
        debug: 调试模式
    
    Returns:
        dict: 任务信息
    """
    file_name = os.path.basename(video_path)
    file_size = os.path.getsize(video_path) / (1024 * 1024)
    
    print(f"\n处理视频: {file_name} ({file_size:.1f} MB)")
    print(f"擦除模式: {mode}")
    print(f"模型类型: {model_type}")
    
    # 上传视频
    print("  [1/2] 上传视频...")
    try:
        media_id = upload_media(ak, sk, video_path, debug=debug)
        print(f"        ✓ 媒资ID: {media_id}")
    except Exception as e:
        print(f"        ✗ 上传失败: {e}")
        return None
    
    # 构建擦除参数
    desubtitle_params = None
    
    if mode == "global" and time_range and not areas:
        print("        ✗ global 模式单独指定 --time-range 不支持，请改用 manual 模式")
        print("           或通过 --areas 指定区域后配合 --time-range 使用")
        return None

    if mode == "manual" or (mode == "global" and areas):
        # 自定义区域擦除或全局模式带区域
        if not areas:
            print("        ✗ manual 模式需要指定 --areas 参数")
            return None

        # 按是否带内嵌时间戳分组
        timed_areas = []   # 有内嵌时间戳的区域 → 各自独立成 param
        global_areas = []  # 无内嵌时间戳的区域 → 归入同一个 param

        for area_str in areas:
            area = parse_area_string(area_str)
            if area:
                if area.pop("has_time"):
                    timed_areas.append(area)
                else:
                    global_areas.append(area)

        desubtitle_params = []

        # 无时间戳区域归入一个 param（可叠加顶层 time_range）
        if global_areas:
            param = {"areaList": global_areas}
            if time_range:
                param["startTimeInMillisecond"] = time_range[0]
                param["endTimeInMillisecond"] = time_range[1]
            desubtitle_params.append(param)

        # 每个带时间戳的区域各自独立成 param
        for area in timed_areas:
            param = {"areaList": [area]}
            desubtitle_params.append(param)

        if not desubtitle_params:
            print("        ✗ 区域参数解析失败")
            return None
        
    elif time_range:
        # 仅时间范围
        desubtitle_params = [{
            "startTimeInMillisecond": time_range[0],
            "endTimeInMillisecond": time_range[1]
        }]
    
    # 创建任务
    print("  [2/2] 创建字幕擦除任务...")
    try:
        task_id = create_desubtitle_task(
            ak, sk, media_id, 
            subtitle_type=mode,
            model_type=model_type,
            desubtitle_params=desubtitle_params,
            debug=debug
        )
        print(f"        ✓ 任务ID: {task_id}")
    except Exception as e:
        print(f"        ✗ 创建任务失败: {e}")
        return None
    
    return {
        "media_id": media_id,
        "task_id": task_id,
        "file_name": file_name
    }


def query_and_display(ak, sk, task_id=None, media_id=None, status=None,
                      marker=None, max_size=10, debug=False):
    """查询并显示任务列表"""
    print("\n" + "=" * 60)
    print("查询字幕擦除任务")
    print("=" * 60)
    
    result = query_desubtitle_tasks(
        ak, sk,
        task_id=task_id,
        media_id=media_id,
        status=status,
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
        print(f"  媒资ID: {task.get('mediaId')}")
        print(f"  名称: {task.get('name', 'N/A')}")
        print(f"  状态: {task.get('status')}")
        print(f"  擦除类型: {task.get('subtitleType')}")
        print(f"  时长: {task.get('durationInSeconds', 'N/A')}s")
        print(f"  创建时间: {task.get('createTime', 'N/A')}")
        
        if task.get('targetUrl'):
            print(f"  结果URL: {task.get('targetUrl')[:80]}...")
        print()
    
    if result.get("isTruncated"):
        print(f"还有更多数据，使用 --marker {result.get('marker')} 获取下一页")


def main():
    parser = argparse.ArgumentParser(
        description="百度智能云 VOD 字幕擦除工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 全局擦除
  python3 desubtitle.py video.mp4 --mode global
  
  # 对白擦除
  python3 desubtitle.py video.mp4 --mode dialog
  
  # 自定义区域擦除
  python3 desubtitle.py video.mp4 --mode manual --areas "60,500,100,100"
  
  # 带时间范围
  python3 desubtitle.py video.mp4 --mode global --time-range 0 30000
  
  # 查询任务
  python3 desubtitle.py --query tsk-xxx
  python3 desubtitle.py --list --status RUNNING
  
  # 删除任务
  python3 desubtitle.py --delete tsk-xxx
        """
    )
    
    # 操作类型（使用可选参数避免 mutually_exclusive_group 限制）
    parser.add_argument("--video", nargs="+", metavar="PATH", help="本地视频文件路径（支持多个）")
    parser.add_argument("--netdisk", help="网盘视频路径")
    parser.add_argument("--query", metavar="TASK_ID", help="查询单个任务")
    parser.add_argument("--list", action="store_true", help="查询任务列表")
    parser.add_argument("--delete", nargs="+", metavar="TASK_ID", help="删除任务")
    
    # 处理参数
    parser.add_argument("--mode", choices=["global", "dialog", "manual"], default="global",
                        help="擦除模式: global(全局), dialog(对白), manual(自定义区域)")
    parser.add_argument("--model", choices=["v3", "v4"], default="v4",
                        help="模型类型: v3(快速), v4(效果好，默认)")
    parser.add_argument("--areas", nargs="+", metavar="X,Y,W,H",
                        help="自定义区域，格式: x,y,width,height（时间范围通过 --time-range 指定）")
    parser.add_argument("--time-range", nargs=2, type=int, metavar=("START_MS", "END_MS"),
                        help="时间范围（毫秒）")
    
    # 查询参数
    parser.add_argument("--media-id", help="按媒资ID筛选")
    parser.add_argument("--status", choices=["READY", "RUNNING", "FINISHED"],
                        help="按状态筛选")
    parser.add_argument("--marker", help="分页游标")
    parser.add_argument("--max-size", type=int, default=10,
                        help="每页数量 (1-100，默认10)")
    
    # 输出选项
    parser.add_argument("--output-dir", default="./output", help="输出目录")
    parser.add_argument("--upload-netdisk", action="store_true", help="处理后上传到网盘")
    parser.add_argument("--netdisk-dir", default="desubtitled", help="网盘目标目录")
    
    # 其他选项
    parser.add_argument("--no-wait", action="store_true", help="不等待任务完成")
    parser.add_argument("--debug", action="store_true", help="显示调试信息")
    
    args = parser.parse_args()
    
    # 获取凭证
    ak, sk = get_credentials()
    
    # 删除任务
    if args.delete:
        print(f"删除任务: {args.delete}")
        try:
            delete_desubtitle_tasks(ak, sk, args.delete, debug=args.debug)
            print("✓ 删除成功")
        except Exception as e:
            print(f"✗ 删除失败: {e}")
            sys.exit(1)
        return
    
    # 查询单个任务
    if args.query:
        task = query_desubtitle_task(ak, sk, args.query, debug=args.debug)
        if task:
            print(f"\n任务ID: {task.get('taskId')}")
            print(f"媒资ID: {task.get('mediaId')}")
            print(f"状态: {task.get('status')}")
            print(f"擦除类型: {task.get('subtitleType')}")
            if task.get('targetUrl'):
                print(f"结果URL: {task.get('targetUrl')}")
        else:
            print("未找到任务")
        return
    
    # 查询任务列表
    if args.list:
        query_and_display(
            ak, sk,
            media_id=args.media_id,
            status=args.status,
            marker=args.marker,
            max_size=args.max_size,
            debug=args.debug
        )
        return
    
    # 处理视频
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
        temp_dir = "/tmp/vod_desubtitle"
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
            mode=args.mode,
            model_type=args.model,
            areas=args.areas,
            time_range=args.time_range,
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
            print(f"  python3 desubtitle.py --query {task['task_id']}")
        return
    
    print("\n" + "=" * 60)
    print("等待任务完成")
    print("=" * 60)
    
    results = []
    for task in tasks:
        print(f"\n等待: {task['file_name']}")
        result = wait_for_task(ak, sk, task['task_id'], 
                               max_retries=180, interval=10, debug=args.debug)
        
        if result and result.get("status") in ["FINISHED", "SUCCESS"]:
            task["result"] = result
            results.append(task)
            print(f"  ✓ 完成")
        else:
            print(f"  ✗ 失败或超时")
            if result:
                print(f"    状态: {result.get('status')}")
    
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
        
        output_name = f"desubtitled_{task['file_name']}"
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
        print(f"  媒资ID: {task['media_id']}")
        if task.get("output_path"):
            print(f"  本地文件: {task['output_path']}")
        if task.get("netdisk_path"):
            print(f"  网盘路径: {task['netdisk_path']}")


if __name__ == "__main__":
    main()
