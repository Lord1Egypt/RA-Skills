#!/usr/bin/env python3
"""
音频和弦分析工具
使用 librosa 提取和弦走向、调性和歌曲结构
"""

import numpy as np
import librosa
import librosa.display
from collections import Counter

# 音程到和弦名称的映射（简化版）
CHORDS = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E',
    5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A',
    10: 'A#', 11: 'B'
}

# 大调和小调音阶的半音模式
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]  # 大调
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]  # 小调

def get_chord_name(root, is_minor=False, is_seventh=False, is_diminished=False):
    """获取和弦名称"""
    name = CHORDS[root]
    if is_minor:
        name += 'm'
    if is_diminished:
        name += 'dim'
    if is_seventh and not is_diminished:
        name += '7'
    elif is_diminished and is_seventh:
        name += '7'
    return name

def detect_key(chromagram):
    """检测调性"""
    # 计算 12 个音的平均能量
    avg_energy = np.mean(chromagram, axis=1)

    # 尝试 24 个调性（12 大调 + 12 小调）
    best_key = None
    best_score = -float('inf')

    for root in range(12):
        # 大调：检查音阶内的音符
        major_tones = [(root + note) % 12 for note in MAJOR_SCALE]
        major_score = sum(avg_energy[t] for t in major_tones)
        if major_score > best_score:
            best_score = major_score
            best_key = (root, 'major')

        # 小调：检查音阶内的音符
        minor_tones = [(root + note) % 12 for note in MINOR_SCALE]
        minor_score = sum(avg_energy[t] for t in minor_tones)
        if minor_score > best_score:
            best_score = minor_score
            best_key = (root, 'minor')

    root_note, mode = best_key
    key_name = CHORDS[root_note]
    if mode == 'minor':
        key_name += 'm'
    return key_name, best_key

def detect_chord(chroma_slice):
    """从 chroma 特征检测单个和弦"""
    # 找到最强的根音
    energy_by_root = np.zeros(12)
    for root in range(12):
        # 大调三和弦能量（根音、大三度、纯五度）
        major_third = (root + 4) % 12
        perfect_fifth = (root + 7) % 12
        energy_by_root[root] = chroma_slice[root] + chroma_slice[major_third] + chroma_slice[perfect_fifth]

        # 小调三和弦能量（根音、小三度、纯五度）
        minor_third = (root + 3) % 12
        minor_energy = chroma_slice[root] + chroma_slice[minor_third] + chroma_slice[perfect_fifth]

        # 减三和弦
        diminished_fifth = (root + 6) % 12
        diminished_energy = chroma_slice[root] + chroma_slice[minor_third] + chroma_slice[diminished_fifth]

        # 更新最大值
        if minor_energy > energy_by_root[root]:
            energy_by_root[root] = minor_energy
        if diminished_energy > energy_by_root[root]:
            energy_by_root[root] = diminished_energy

    best_root = np.argmax(energy_by_root)

    # 判断是大调还是小调
    major_third = (best_root + 4) % 12
    minor_third = (best_root + 3) % 12
    perfect_fifth = (best_root + 7) % 12
    diminished_fifth = (best_root + 6) % 12

    major_score = chroma_slice[major_third] + chroma_slice[perfect_fifth]
    minor_score = chroma_slice[minor_third] + chroma_slice[perfect_fifth]
    diminished_score = chroma_slice[minor_third] + chroma_slice[diminished_fifth]

    if diminished_score > major_score and diminished_score > minor_score:
        is_minor = True
        is_diminished = True
    elif minor_score > major_score:
        is_minor = True
        is_diminished = False
    else:
        is_minor = False
        is_diminished = False

    return get_chord_name(best_root, is_minor, is_diminished=is_diminished)

def analyze_audio(audio_path):
    """分析音频文件"""
    print(f"\n🎵 分析文件: {audio_path}")
    print("=" * 60)

    # 加载音频
    print("⏳ 加载音频...")
    y, sr = librosa.load(audio_path, sr=22050)
    duration = len(y) / sr
    print(f"   时长: {duration:.2f} 秒 | 采样率: {sr} Hz")

    # 提取 chroma 特征（和弦分析的核心）
    print("⏳ 提取和弦特征...")
    chromagram = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=2048)
    print(f"   Chroma 矩阵形状: {chromagram.shape}")

    # 检测调性
    print("\n🎼 调性分析...")
    key_name, best_key = detect_key(chromagram)
    print(f"   调性: {key_name}")

    # 检测节拍和速度
    print("\n⏱️  节拍分析...")
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(tempo) if isinstance(tempo, np.ndarray) else tempo
    print(f"   速度: {tempo:.1f} BPM")
    print(f"   拍数: {len(beat_frames)} 拍")

    # 检测节奏型（简单判断）
    if 60 <= tempo < 80:
        rhythm = "慢板 (Slow)"
    elif 80 <= tempo < 120:
        rhythm = "中板 (Moderato)"
    elif 120 <= tempo < 140:
        rhythm = "快板 (Allegro)"
    elif 140 <= tempo < 180:
        rhythm = "极快板 (Vivace)"
    else:
        rhythm = "极慢/极快"
    print(f"   节奏型: {rhythm}")

    # 每小节的拍数（假设）
    beats_per_measure = 4
    frames_per_beat = len(chromagram[0]) // len(beat_frames)

    # 分析和弦走向（每小节取一个和弦）
    print("\n🎸 和弦走向分析...")
    chords = []
    chord_durations = []

    # 每小节（约 4 拍）采样一次
    samples_per_measure = frames_per_beat * beats_per_measure

    for i in range(0, len(chromagram[0]), samples_per_measure):
        # 取当前小节的平均 chroma
        end_idx = min(i + samples_per_measure, len(chromagram[0]))
        slice_chroma = np.mean(chromagram[:, i:end_idx], axis=1)

        # 检测和弦
        chord = detect_chord(slice_chroma)
        chords.append(chord)
        chord_durations.append((end_idx - i) * 2048 / sr)

    # 合并连续相同的和弦
    merged_chords = []
    merged_durations = []
    for chord, duration in zip(chords, chord_durations):
        if not merged_chords or merged_chords[-1] != chord:
            merged_chords.append(chord)
            merged_durations.append(duration)
        else:
            merged_durations[-1] += duration

    print(f"\n   检测到 {len(merged_chords)} 个不同的和弦段落:")

    # 输出和弦走向
    output_lines = []
    output_lines.append(f"\n📋 和弦走向:")
    output_lines.append("-" * 60)

    for i, (chord, dur) in enumerate(zip(merged_chords, merged_durations)):
        bar_num = i + 1
        time_pos = 0  # 简化，不累加时间
        output_lines.append(f"小节 {bar_num:2d}: {chord:>8s}  (持续 ~{dur:.1f}s)")

        # 每 4 小节换行显示，方便阅读
        if (bar_num % 4 == 0) and bar_num < len(merged_chords):
            output_lines.append("")

    output_lines.append("-" * 60)

    # 简化表示（去重复）
    simplified = []
    for chord in merged_chords:
        if not simplified or simplified[-1] != chord:
            simplified.append(chord)

    output_lines.append(f"\n🎯 简化和弦序列: {' → '.join(simplified[:16])}")
    if len(simplified) > 16:
        output_lines.append(f"   ... (共 {len(simplified)} 个不同的和弦)")

    # 统计和弦使用频率
    chord_counts = Counter(merged_chords)
    top_chords = chord_counts.most_common(5)
    output_lines.append(f"\n📊 主要和弦使用:")
    for chord, count in top_chords:
        percentage = (count / len(merged_chords)) * 100
        output_lines.append(f"   {chord:>8s}: {count:2d} 次 ({percentage:.1f}%)")

    # 检测歌曲结构（通过能量变化）
    print("\n🏗️  歌曲结构分析...")
    # 使用 onset strength 检测能量变化
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)

    # 简单的结构分段（前、中、后三段）
    section_size = len(merged_chords) // 3
    sections = []
    if section_size > 0:
        intro = ' → '.join(merged_chords[:section_size])
        verse = ' → '.join(merged_chords[section_size:2*section_size])
        outro = ' → '.join(merged_chords[2*section_size:])

        output_lines.append(f"\n   前段: {intro}")
        output_lines.append(f"   中段: {verse}")
        output_lines.append(f"   后段: {outro}")

    print("\n✅ 分析完成!\n")

    # 返回所有结果
    return {
        'key': key_name,
        'tempo': tempo,
        'rhythm': rhythm,
        'chords': merged_chords,
        'durations': merged_durations,
        'simplified': simplified,
        'top_chords': top_chords
    }

if __name__ == "__main__":
    audio_path = "/Users/chentiewen/Music/网易云音乐/花儿乐队 - 别针.mp3"

    try:
        result = analyze_audio(audio_path)

        # 打印格式化结果
        print("\n" + "=" * 60)
        print("📝 最终分析报告")
        print("=" * 60)

        # 调性和速度
        print(f"\n调性: {result['key']}")
        print(f"速度: {result['tempo']:.1f} BPM")
        print(f"节奏: {result['rhythm']}")

        # 和弦走向
        print(f"\n和弦走向:")
        chord_str = ' → '.join(result['simplified'])
        print(chord_str)

        # 主要和弦
        print(f"\n主要和弦:")
        for chord, count in result['top_chords']:
            print(f"  {chord}: {count}次")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
