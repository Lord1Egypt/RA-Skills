#!/usr/bin/env python3
"""
AI Video Prompt Builder Script - 多段视频拼接版
AI视频Prompt构建辅助脚本 - 支持生成长视频（30秒/60秒）

Usage:
    python prompt_builder.py --interactive
    python prompt_builder.py --duration 30 --segments 6 --lang zh
"""

import argparse
import json
from typing import Dict, List, Optional, Tuple

def build_keyframe_prompt(segment_num: int, total_segments: int, 
                         subject: str, appearance: str, clothing: str,
                         expression: str, pose: str, prop: str,
                         environment: str, lighting: str) -> str:
    """
    构建关键帧Prompt
    """
    time_point = segment_num * 5
    
    # 确定是首帧、中间帧还是尾帧
    if segment_num == 0:
        frame_type = "首帧"
    elif segment_num == total_segments:
        frame_type = "尾帧"
    else:
        frame_type = f"关键帧{chr(65+segment_num)}"  # B, C, D...
    
    return (
        f"中景固定镜头，{subject}，{appearance}，"
        f"穿{clothing}，{expression}，{pose}，"
        f"{prop}，在{environment}，"
        f"{lighting}，8K"
    )

def build_segment_video_prompt(segment_num: int, start_desc: str, 
                              end_desc: str, transition: str) -> str:
    """
    构建每段5秒视频Prompt
    """
    start_time = segment_num * 5
    end_time = start_time + 5
    
    return (
        f"5秒视频：{start_desc}（第1-2秒）。"
        f"{transition}（第3-4秒）。"
        f"{end_desc}（第4-5秒）。"
        f"镜头跟随移动，自然光，真实运动，平滑过渡"
    )

def check_consistency(prev_frame: str, next_frame: str) -> List[str]:
    """
    检查相邻关键帧一致性
    """
    issues = []
    
    # 检查主体一致性
    if "同个" not in next_frame and "同一个" not in next_frame:
        issues.append("缺少'同个'标识，主体可能不一致")
    
    return issues

def generate_negative_prompt() -> str:
    """
    生成负面约束Prompt
    """
    return (
        "无变形，无扭曲，无多余肢体，面部稳定，角色一致，"
        "无闪烁，无突然变色，运动平滑，真实表情，"
        "符合物理规律，外貌一致，服装一致，道具逻辑连贯"
    )

def interactive_builder_long_video():
    """
    交互式长视频Prompt构建
    """
    print("=" * 70)
    print("AI视频Prompt构建助手 - 多段视频拼接版")
    print("=" * 70)
    print("\n本工具支持生成长视频（30秒/60秒/更长）")
    print("通过多段5秒视频拼接实现")
    print("=" * 70)
    
    # 基本信息
    duration = int(input("\n1. 目标总时长（秒，建议30或60）: ") or "30")
    num_segments = duration // 5
    num_keyframes = num_segments + 1
    
    print(f"\n将生成：{num_segments}段 × 5秒 = {duration}秒")
    print(f"需要：{num_keyframes}张关键帧图片")
    
    # 主体信息
    print("\n【主体信息】")
    subject = input("2. 主体身份 (如: 可爱的周岁宝宝): ")
    appearance = input("3. 外貌细节 (如: 圆脸，粉嫩脸颊，黑发稀疏，大眼睛): ")
    clothing = input("4. 服装 (如: 白色连体衣): ")
    
    # 为每段收集信息
    segments = []
    
    print(f"\n【为每段收集信息，共{num_segments}段】")
    
    for i in range(num_segments):
        print(f"\n--- 第{i+1}段：{i*5}-{(i+1)*5}秒 ---")
        
        expression_start = input(f"  开始表情: ")
        expression_end = input(f"  结束表情: ")
        prop_state = input(f"  道具状态: ")
        transition = input(f"  变化过程: ")
        
        segments.append({
            "start_time": i * 5,
            "end_time": (i + 1) * 5,
            "expression_start": expression_start,
            "expression_end": expression_end,
            "prop_state": prop_state,
            "transition": transition
        })
    
    # 生成关键帧
    print("\n" + "=" * 70)
    print("生成的关键帧Prompt")
    print("=" * 70)
    
    keyframes = []
    
    for i in range(num_keyframes):
        if i == 0:
            # 首帧
            frame = build_keyframe_prompt(
                i, num_segments, subject, appearance, clothing,
                segments[i]["expression_start"], "初始姿势", segments[i]["prop_state"],
                "医院环境", "自然光"
            )
        elif i == num_segments:
            # 尾帧
            frame = build_keyframe_prompt(
                i, num_segments, subject, appearance, clothing,
                segments[i-1]["expression_end"], "结束姿势", segments[i-1]["prop_state"],
                "医院环境", "柔和光"
            )
        else:
            # 中间帧（衔接帧）
            frame = build_keyframe_prompt(
                i, num_segments, f"同个{subject}", appearance, clothing,
                segments[i-1]["expression_end"], "过渡姿势", segments[i-1]["prop_state"],
                "医院环境", "自然光"
            )
        
        keyframes.append(frame)
        
        frame_label = chr(65 + i)
        print(f"\n【关键帧{frame_label}（{i*5}秒）】")
        print(frame)
    
    # 生成视频Prompt
    print("\n" + "=" * 70)
    print("生成的视频Prompt")
    print("=" * 70)
    
    for i, seg in enumerate(segments):
        video_prompt = build_segment_video_prompt(
            i,
            f"表情{seg['expression_start']}",
            f"表情{seg['expression_end']}",
            seg['transition']
        )
        
        start_label = chr(65 + i)
        end_label = chr(65 + i + 1)
        
        print(f"\n【第{i+1}段：{seg['start_time']}-{seg['end_time']}秒】")
        print(f"首帧：{start_label} | 尾帧：{end_label}")
        print(video_prompt)
    
    # 一致性检查
    print("\n" + "=" * 70)
    print("衔接一致性检查")
    print("=" * 70)
    
    all_passed = True
    for i in range(len(keyframes) - 1):
        issues = check_consistency(keyframes[i], keyframes[i+1])
        
        start_label = chr(65 + i)
        end_label = chr(65 + i + 1)
        
        if issues:
            print(f"\n⚠️ {start_label} → {end_label}:")
            for issue in issues:
                print(f"  - {issue}")
            all_passed = False
        else:
            print(f"\n✅ {start_label} → {end_label}: 检查通过")
    
    if all_passed:
        print("\n✅ 所有衔接点检查通过！")
    else:
        print("\n⚠️ 请修正上述问题后再生成")
    
    # 负面约束
    print("\n【负面约束】")
    print(generate_negative_prompt())
    
    # 使用建议
    print("\n" + "=" * 70)
    print("在即梦平台的操作步骤")
    print("=" * 70)
    print(f"\n1. 生成{num_keyframes}张关键帧图片（按A→B→C...顺序）")
    print(f"2. 生成{num_segments}段5秒视频")
    print("3. 使用剪映/PR拼接成完整视频")

def quick_build_30s_example():
    """
    快速生成30秒宝宝打疫苗示例
    """
    print("=" * 70)
    print("30秒宝宝打疫苗 - 完整Prompt方案")
    print("=" * 70)
    
    result = {
        "关键帧": {
            "A（0s）": "中景固定镜头，可爱的周岁宝宝，圆脸，粉嫩脸颊，稀疏柔软的黑发，明亮好奇的大眼睛，穿白色连体衣，被妈妈抱着走进医院大门，表情好奇东张西望，手里无玩具，医院明亮大厅，自然光，温馨，8K",
            
            "B（5s）": "中景固定镜头，同个可爱的周岁宝宝，圆脸，粉嫩脸颊，稀疏柔软的黑发，明亮好奇的大眼睛，穿白色连体衣，被妈妈抱着坐在候诊区椅子上，表情好奇观察周围环境，手里抓着彩色玩具（玩具在手中），医院候诊区，其他小朋友在远处，自然光，8K",
            
            "C（10s）": "中景固定镜头，同个可爱的周岁宝宝，圆脸，粉嫩脸颊，稀疏柔软的黑发，明亮好奇的大眼睛，穿白色连体衣，坐在妈妈腿上，表情紧张眉头微皱，看向诊室方向，手里玩具掉落（玩具不在手中，掉在腿上），医院候诊区，自然光，8K",
            
            "D（15s）": "特写固定镜头，同个可爱的周岁宝宝，圆脸，粉嫩脸颊，稀疏柔软的黑发，明亮的大眼睛，穿白色连体衣，表情害怕眼睛睁大嘴巴微张，看到护士拿着针管，身体向后缩，手里无玩具（玩具在妈妈包里），诊室环境，clinical light，8K",
            
            "E（20s）": "特写固定镜头，同个可爱的周岁宝宝，圆脸变红，黑发微乱，明亮的大眼睛紧闭流泪，穿白色连体衣，表情痛苦嘴巴大张哭泣，眼泪流下脸颊，小拳头紧握挥舞，手里无玩具，诊室环境，clinical light，8K",
            
            "F（25s）": "中景固定镜头，同个可爱的周岁宝宝，圆脸仍然泛红，黑发微乱，明亮的大眼睛流泪，穿白色连体衣，坐在妈妈腿上，表情痛苦但开始减弱，眼泪减少，小拳头松开，妈妈手轻拍背部安抚，手里无玩具，诊室环境，clinical light转柔和光，8K",
            
            "G（30s）": "中景固定镜头，同个可爱的周岁宝宝，圆脸恢复粉嫩，黑发整齐，明亮好奇的大眼睛，穿白色连体衣，靠在妈妈怀里，表情委屈但平静，小手放松，手里无玩具，妈妈温柔安抚，柔和光，8K"
        },
        
        "视频段": {
            "第1段（0-5s）": {
                "首帧": "A", "尾帧": "B",
                "prompt": "5秒视频：宝宝被妈妈抱着走进医院，好奇地东张西望，转头看医院环境，手指向彩色装饰，妈妈给宝宝玩具，宝宝坐在妈妈腿上玩玩具，镜头跟随移动，自然光，真实运动，平滑过渡"
            },
            "第2段（5-10s）": {
                "首帧": "B", "尾帧": "C",
                "prompt": "5秒视频：宝宝玩着玩具，突然听到叫号声表情变化，转头看向诊室方向，眉头微皱开始紧张，小手抓紧妈妈衣服，玩具从手中掉落，镜头缓慢推进到宝宝脸部，自然光，真实情绪变化，平滑过渡"
            },
            "第3段（10-15s）": {
                "首帧": "C", "尾帧":