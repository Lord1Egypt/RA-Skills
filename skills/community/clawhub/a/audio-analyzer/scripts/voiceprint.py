#!/usr/bin/env python3
"""
声纹提取与匹配工具
用法:
  python3 voiceprint.py extract <audio_file> <raw_json> [--db <voice_db_path>]
  python3 voiceprint.py enroll <name> <audio_file> [--db <voice_db_path>]
  python3 voiceprint.py identify <audio_file> [--db <voice_db_path>]

extract: 从 AssemblyAI 转写结果中提取每个 speaker 的声纹并匹配
enroll:  手动注册一个人的声纹
identify: 识别单个音频片段中的说话人
"""

import sys
import os
import json
import argparse
import numpy as np

# ─── 配置 ───────────────────────────────────────────────

MODEL_PATH = os.environ.get(
    "WESPEAKER_MODEL",
    os.path.join(os.path.dirname(__file__), "..", "models", "cnceleb_resnet34_LM.onnx")
)
DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "references", "voice-db.json")
SAMPLE_RATE = 16000
N_MELS = 80
WIN_LENGTH_MS = 25
HOP_LENGTH_MS = 10
PREEMPHASIS = 0.97

# 匹配阈值（余弦相似度）
THRESHOLD_AUTO = 0.55     # >= 此值: 自动匹配
THRESHOLD_MAYBE = 0.40    # >= 此值: "可能是XXX"
# < THRESHOLD_MAYBE: 未知

MIN_AUDIO_SECONDS = 1.0   # speaker 音频最少秒数，太短则跳过
MAX_SPEAKER_SECONDS = 30  # 每个 speaker 最多取 30 秒用于声纹提取


# ─── 音频预处理 ─────────────────────────────────────────

def extract_speaker_audio(audio_path, segments, sr=SAMPLE_RATE, max_seconds=MAX_SPEAKER_SECONDS):
    """用 ffmpeg 直接从音频中切出指定片段并拼接，避免加载整个文件。
    segments: [{"start": ms, "end": ms}, ...]
    返回: numpy array (mono, target sr)
    """
    import subprocess
    import tempfile
    import librosa

    # 限制总时长，只取前 N 秒的片段
    selected = []
    total_ms = 0
    for seg in segments:
        dur = seg["end"] - seg["start"]
        if total_ms + dur > max_seconds * 1000:
            remaining = max_seconds * 1000 - total_ms
            if remaining > 500:  # 至少 0.5 秒
                selected.append({"start": seg["start"], "end": seg["start"] + remaining})
            break
        selected.append(seg)
        total_ms += dur

    if not selected:
        return np.array([], dtype=np.float32)

    # 构建 ffmpeg filter: 切多个片段并拼接
    filter_parts = []
    for i, seg in enumerate(selected):
        start_sec = seg["start"] / 1000
        end_sec = seg["end"] / 1000
        filter_parts.append(
            f"[0:a]atrim=start={start_sec:.3f}:end={end_sec:.3f},asetpts=PTS-STARTPTS[s{i}]"
        )
    concat_inputs = "".join(f"[s{i}]" for i in range(len(selected)))
    filter_str = ";".join(filter_parts) + f";{concat_inputs}concat=n={len(selected)}:v=0:a=1[out]"

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", audio_path,
                "-filter_complex", filter_str,
                "-map", "[out]",
                "-ar", str(sr), "-ac", "1",
                "-f", "wav", tmp.name,
            ],
            capture_output=True, check=True, timeout=30,
        )
        audio, _ = librosa.load(tmp.name, sr=sr, mono=True)
        return audio
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        err = getattr(e, "stderr", b"")
        if err:
            print(f"ffmpeg 错误: {err.decode()[:200]}", file=sys.stderr)
        return np.array([], dtype=np.float32)
    finally:
        os.unlink(tmp.name)


def compute_fbank(audio, sr=SAMPLE_RATE):
    """计算 80 维 log Mel filterbank 特征"""
    import librosa

    # 预加重
    emphasized = np.append(audio[0], audio[1:] - PREEMPHASIS * audio[:-1])

    # Mel spectrogram
    win_length = int(WIN_LENGTH_MS * sr / 1000)
    hop_length = int(HOP_LENGTH_MS * sr / 1000)

    mel_spec = librosa.feature.melspectrogram(
        y=emphasized,
        sr=sr,
        n_fft=512,
        win_length=win_length,
        hop_length=hop_length,
        n_mels=N_MELS,
        fmin=20,
        fmax=sr // 2,
    )

    # log + 数值稳定
    log_mel = np.log(np.maximum(mel_spec, 1e-10))

    # CMN (Cepstral Mean Normalization)
    log_mel = log_mel - np.mean(log_mel, axis=1, keepdims=True)

    # 转置: (n_mels, time) → (time, n_mels)
    return log_mel.T.astype(np.float32)


# ─── 模型推理 ──────────────────────────────────────────

_session = None

def get_session():
    """懒加载 ONNX 模型（单例）"""
    global _session
    if _session is None:
        import onnxruntime as ort
        if not os.path.exists(MODEL_PATH):
            print(f"错误: 模型文件不存在: {MODEL_PATH}", file=sys.stderr)
            sys.exit(1)
        opts = ort.SessionOptions()
        opts.inter_op_num_threads = 1
        opts.intra_op_num_threads = 2
        _session = ort.InferenceSession(MODEL_PATH, sess_options=opts)
    return _session


def extract_embedding(audio, sr=SAMPLE_RATE):
    """从音频提取 256 维声纹向量"""
    if len(audio) < int(MIN_AUDIO_SECONDS * sr):
        return None

    fbank = compute_fbank(audio, sr)

    # ONNX 输入: (batch=1, time, n_mels)
    fbank_input = np.expand_dims(fbank, axis=0)

    session = get_session()
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: fbank_input})

    embedding = outputs[0].flatten()

    # L2 归一化
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm

    return embedding


# ─── 声纹库操作 ─────────────────────────────────────────

def load_db(db_path):
    """加载声纹库"""
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 将列表还原为 numpy 数组
        return {name: np.array(vec) for name, vec in data.items()}
    return {}


def save_db(db, db_path):
    """保存声纹库"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    serializable = {name: vec.tolist() for name, vec in db.items()}
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)


def cosine_similarity(a, b):
    """余弦相似度（输入已 L2 归一化，直接点积）"""
    return float(np.dot(a, b))


def match_speaker(embedding, db):
    """
    将声纹向量与库中所有人比对
    返回: (name, similarity, confidence_level)
      confidence_level: "auto" / "maybe" / "unknown"
    """
    if not db:
        return None, 0.0, "unknown"

    best_name = None
    best_sim = -1.0

    for name, stored_emb in db.items():
        sim = cosine_similarity(embedding, stored_emb)
        if sim > best_sim:
            best_sim = sim
            best_name = name

    if best_sim >= THRESHOLD_AUTO:
        return best_name, best_sim, "auto"
    elif best_sim >= THRESHOLD_MAYBE:
        return best_name, best_sim, "maybe"
    else:
        return best_name, best_sim, "unknown"


# ─── 命令: extract ──────────────────────────────────────

def cmd_extract(args):
    """从 AssemblyAI 转写结果中提取每个 speaker 的声纹并匹配"""
    audio_path = args.audio_file
    raw_json_path = args.raw_json
    db_path = args.db

    # 加载 AssemblyAI 原始结果
    with open(raw_json_path, "r", encoding="utf-8") as f:
        transcript = json.load(f)

    utterances = transcript.get("utterances", [])
    if not utterances:
        print(json.dumps({"error": "转写结果中无 utterances"}, ensure_ascii=False))
        sys.exit(1)

    # 按 speaker 分组
    speaker_segments = {}
    for utt in utterances:
        spk = utt["speaker"]
        if spk not in speaker_segments:
            speaker_segments[spk] = []
        speaker_segments[spk].append({"start": utt["start"], "end": utt["end"]})

    # 加载声纹库
    db = load_db(db_path)

    results = []

    for spk, segments in sorted(speaker_segments.items()):
        # 用 ffmpeg 直接切片段（不加载整个文件）
        combined = extract_speaker_audio(audio_path, segments)

        if len(combined) == 0:
            results.append({
                "speaker": spk,
                "match": None,
                "confidence": "skip",
                "reason": "无有效音频片段"
            })
            continue

        total_seconds = len(combined) / SAMPLE_RATE

        if total_seconds < MIN_AUDIO_SECONDS:
            results.append({
                "speaker": spk,
                "match": None,
                "confidence": "skip",
                "duration_seconds": round(total_seconds, 1),
                "reason": f"音频不足{MIN_AUDIO_SECONDS}秒"
            })
            continue

        # 提取声纹
        embedding = extract_embedding(combined)
        if embedding is None:
            results.append({
                "speaker": spk,
                "match": None,
                "confidence": "error",
                "reason": "声纹提取失败"
            })
            continue

        # 匹配
        name, similarity, confidence = match_speaker(embedding, db)

        result = {
            "speaker": spk,
            "duration_seconds": round(total_seconds, 1),
            "confidence": confidence,
            "similarity": round(similarity, 4),
        }

        if confidence == "auto":
            result["match"] = name
            result["message"] = f"自动识别为 {name}（相似度 {similarity:.1%}）"
        elif confidence == "maybe":
            result["match"] = name
            result["message"] = f"可能是 {name}（相似度 {similarity:.1%}），请确认"
        else:
            result["match"] = None
            result["message"] = "未知说话人，请告知姓名"

        # 暂存 embedding 供后续 enroll
        result["_embedding"] = embedding.tolist()

        results.append(result)

    # 输出
    output = {
        "audio_file": os.path.basename(audio_path),
        "speakers_found": len(speaker_segments),
        "db_size": len(db),
        "results": results,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


# ─── 命令: enroll ───────────────────────────────────────

def cmd_enroll(args):
    """注册一个人的声纹到库中"""
    name = args.name
    db_path = args.db

    db = load_db(db_path)

    # 如果传入的是 JSON（从 extract 结果中取 _embedding）
    if args.audio_file.endswith(".json"):
        with open(args.audio_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        embedding = np.array(data)
    else:
        # 构造一个覆盖全部时长的 segment
        fake_seg = [{"start": 0, "end": MAX_SPEAKER_SECONDS * 1000}]
        audio = extract_speaker_audio(args.audio_file, fake_seg)
        embedding = extract_embedding(audio)
        if embedding is None:
            print(json.dumps({"error": "音频太短，无法提取声纹"}, ensure_ascii=False))
            sys.exit(1)

    db[name] = embedding
    save_db(db, db_path)

    print(json.dumps({
        "action": "enrolled",
        "name": name,
        "db_size": len(db),
        "db_path": db_path,
    }, ensure_ascii=False, indent=2))


# ─── 命令: identify ─────────────────────────────────────

def cmd_identify(args):
    """识别单个音频中的说话人"""
    db_path = args.db
    db = load_db(db_path)

    fake_seg = [{"start": 0, "end": MAX_SPEAKER_SECONDS * 1000}]
    audio = extract_speaker_audio(args.audio_file, fake_seg)
    embedding = extract_embedding(audio)

    if embedding is None:
        print(json.dumps({"error": "音频太短，无法提取声纹"}, ensure_ascii=False))
        sys.exit(1)

    name, similarity, confidence = match_speaker(embedding, db)

    print(json.dumps({
        "match": name if confidence != "unknown" else None,
        "similarity": round(similarity, 4),
        "confidence": confidence,
        "db_size": len(db),
    }, ensure_ascii=False, indent=2))


# ─── CLI ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="声纹提取与匹配工具")
    sub = parser.add_subparsers(dest="command")

    # extract
    p_ext = sub.add_parser("extract", help="从 AssemblyAI 结果提取声纹并匹配")
    p_ext.add_argument("audio_file", help="原始音频文件路径")
    p_ext.add_argument("raw_json", help="AssemblyAI _raw.json 路径")
    p_ext.add_argument("--db", default=DEFAULT_DB, help="声纹库路径")
    p_ext.set_defaults(func=cmd_extract)

    # enroll
    p_enr = sub.add_parser("enroll", help="注册声纹")
    p_enr.add_argument("name", help="说话人姓名")
    p_enr.add_argument("audio_file", help="音频文件或 embedding JSON")
    p_enr.add_argument("--db", default=DEFAULT_DB, help="声纹库路径")
    p_enr.set_defaults(func=cmd_enroll)

    # identify
    p_id = sub.add_parser("identify", help="识别单个音频")
    p_id.add_argument("audio_file", help="音频文件路径")
    p_id.add_argument("--db", default=DEFAULT_DB, help="声纹库路径")
    p_id.set_defaults(func=cmd_identify)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
