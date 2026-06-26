#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书语音识别ASR - 使用本地Whisper模型
离线免费，不需要注册，不需要联网

依赖:
    pip install torch transformers soundfile

首次运行会自动下载模型（75MB-3GB）
"""

import os
import sys
import tempfile

# 国内镜像，解决网络问题
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

import torch
import soundfile as sf
from transformers import WhisperForConditionalGeneration, WhisperProcessor, WhisperFeatureExtractor


def convert_audio(input_path, output_path=None):
    """转换音频为16kHz WAV格式"""
    audio, sr = sf.read(input_path)
    
    # 立体声转单声道
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)
    
    # 重采样到16kHz
    if sr != 16000:
        import resampy
        audio = resampy.resample(audio, sr, 16000)
    
    if output_path:
        sf.write(output_path, audio, 16000)
        return output_path
    else:
        return audio, 16000


def recognize_audio(audio_path, model_size='tiny'):
    """识别音频文件"""
    model_name = f'openai/whisper-{model_size}'
    
    print(f'Loading {model_size} model...')
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    feature_extractor = WhisperFeatureExtractor.from_pretrained(model_name)
    
    # 读取并处理音频
    audio, sr = sf.read(audio_path)
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)
    
    input_features = feature_extractor(audio, sampling_rate=16000, return_tensors='pt').input_features
    
    print('Transcribing...')
    with torch.no_grad():
        predicted_ids = model.generate(input_features)
    
    result = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return result


def recognize_voice(voice_file_path):
    """主函数：识别语音文件"""
    # 转换音频格式
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        convert_audio(voice_file_path, tmp_path)
        result = recognize_audio(tmp_path)
        return result
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python recognize.py <语音文件路径>')
        print('示例: python recognize.py voice.ogg')
        sys.exit(1)
    
    voice_file = sys.argv[1]
    if not os.path.exists(voice_file):
        print(f'错误: 文件不存在: {voice_file}')
        sys.exit(1)
    
    try:
        result = recognize_voice(voice_file)
        print(f'识别结果: {result}')
    except Exception as e:
        print(f'错误: {e}')
        sys.exit(1)
