"""
多段合成引擎 — 台词分段合成 + 音频拼接
基于 Fish Speech API，支持情绪分段 + 停顿控制
"""

import os
import sys
import base64
import requests
import tempfile
from typing import List, Optional, Dict
from pathlib import Path
from dataclasses import dataclass

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from text_analyzer import TextAnalyzer, SegmentAnalysis

# 尝试导入 pydub（音频处理）
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("警告: pydub 未安装，音频后处理功能不可用。安装: pip install pydub", file=sys.stderr)


@dataclass
class SynthesisResult:
    """合成结果"""
    segment_index: int
    text: str
    audio_path: str
    duration_ms: float
    emotion: str
    success: bool
    error: Optional[str] = None


class MultiSegmentSynthesizer:
    """
    多段合成器
    
    功能：
    1. 将长文本按句子分割
    2. 对每段进行情绪分析
    3. 分别合成（可指定不同参考音频）
    4. 拼接为完整音频
    5. 插入停顿
    """
    
    def __init__(
        self,
        api_base: str = "http://127.0.0.1:18791",
        output_dir: str = "output",
        default_format: str = "mp3",
        ffmpeg_path: Optional[str] = None
    ):
        self.api_base = api_base
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.default_format = default_format
        self.analyzer = TextAnalyzer()
        
        # 设置 ffmpeg（pydub 需要）
        if ffmpeg_path and PYDUB_AVAILABLE:
            AudioSegment.converter = ffmpeg_path
        
        # 检查 API
        if not self._check_api():
            raise RuntimeError(
                f"Fish Speech API 未运行或无法访问: {api_base}\n"
                "请先启动 API Server:\n"
                "  cd E:\\fish-speech && .venv\\Scripts\\activate\n"
                "  python tools/api_server.py --llama-checkpoint-path checkpoints/s2-pro \\\n"
                "    --decoder-checkpoint-path checkpoints/s2-pro/codec.pth \\\n"
                "    --device cuda --half --listen 127.0.0.1:18791"
            )
    
    def _check_api(self) -> bool:
        """检查 API 是否可用"""
        try:
            r = requests.get(f"{self.api_base}/v1/health", timeout=5)
            return r.status_code == 200
        except:
            return False
    
    def synthesize_with_analysis(
        self,
        text: str,
        output_path: str,
        ref_audio: Optional[str] = None,
        voice_id: Optional[str] = None,
        context: Optional[Dict] = None,
        add_silence: bool = True,
        silence_duration_ms: int = 500
    ) -> List[SynthesisResult]:
        """
        带情绪分析的多段合成
        
        Args:
            text: 要合成的文本
            output_path: 最终输出路径
            ref_audio: 参考音频（声音克隆）
            voice_id: 已注册的音色 ID
            context: 上下文信息（角色、场景等）
            add_silence: 是否在段落间插入停顿
            silence_duration_ms: 停顿时长（毫秒）
        
        Returns:
            List[SynthesisResult]: 每段的合成结果
        """
        # 1. 分割文本
        segments = self.analyzer.split_into_segments(text)
        print(f"文本已分割为 {len(segments)} 段")
        
        # 2. 分析并合成每段
        results = []
        temp_files = []
        
        for i, segment_text in enumerate(segments):
            print(f"\n处理第 {i + 1}/{len(segments)} 段: {segment_text[:50]}...")
            
            # 分析
            analysis = self.analyzer.analyze(segment_text, context)
            
            # 生成临时输出路径
            temp_path = self.output_dir / f"temp_seg_{i:03d}.{self.default_format}"
            
            # 合成
            success = self._synthesize_single(
                text=segment_text,
                output_path=str(temp_path),
                ref_audio=ref_audio,
                voice_id=voice_id,
                params=analysis.voice_params
            )
            
            if success:
                # 获取音频时长
                duration_ms = self._get_audio_duration(str(temp_path))
                results.append(SynthesisResult(
                    segment_index=i,
                    text=segment_text,
                    audio_path=str(temp_path),
                    duration_ms=duration_ms,
                    emotion=analysis.emotion.emotion,
                    success=True
                ))
                temp_files.append(str(temp_path))
                
                # 如果需要停顿且不是最后一段
                if add_silence and i < len(segments) - 1:
                    silence_path = self.output_dir / f"temp_silence_{i:03d}.{self.default_format}"
                    self._create_silence(str(silence_path), silence_duration_ms)
                    temp_files.append(str(silence_path))
            else:
                results.append(SynthesisResult(
                    segment_index=i,
                    text=segment_text,
                    audio_path="",
                    duration_ms=0,
                    emotion=analysis.emotion.emotion,
                    success=False,
                    error="合成失败"
                ))
        
        # 3. 拼接所有音频
        if temp_files and PYDUB_AVAILABLE:
            self._concatenate_audio(temp_files, output_path)
            print(f"\n✅ 完整音频已生成: {output_path}")
        elif temp_files:
            # 如果没有 pydub，直接复制第一段
            import shutil
            shutil.copy(temp_files[0], output_path)
            print(f"\n⚠️ pydub 未安装，只保留了第一段: {output_path}")
        
        # 4. 清理临时文件
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except:
                pass
        
        return results
    
    def _synthesize_single(
        self,
        text: str,
        output_path: str,
        ref_audio: Optional[str] = None,
        voice_id: Optional[str] = None,
        params: Optional[Dict] = None
    ) -> bool:
        """合成单段音频"""
        payload = {
            "text": text,
            "format": self.default_format,
            "normalize": True,
            "max_new_tokens": 2048,
            "chunk_length": 200,
            "top_p": 0.8,
            "repetition_penalty": 1.1,
            "temperature": 0.7,
            "streaming": False,
        }
        
        # 应用情绪参数
        if params:
            payload.update(params)
        
        # 参考音频
        if ref_audio:
            if not os.path.exists(ref_audio):
                print(f"错误: 参考音频不存在: {ref_audio}", file=sys.stderr)
                return False
            with open(ref_audio, "rb") as f:
                audio_data = f.read()
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            payload["references"] = [{
                "audio": audio_b64,
                "text": ""
            }]
        
        # 已注册音色
        if voice_id:
            payload["reference_id"] = voice_id
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # 调用 API
        try:
            headers = {"Content-Type": "application/json"}
            r = requests.post(
                f"{self.api_base}/v1/tts",
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if r.status_code == 200:
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                size_kb = os.path.getsize(output_path) / 1024
                print(f"  ✅ 生成成功: {output_path} ({size_kb:.1f} KB)")
                return True
            else:
                print(f"  ❌ 合成失败 ({r.status_code}): {r.text[:200]}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"  ❌ 请求异常: {e}", file=sys.stderr)
            return False
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """获取音频时长（毫秒）"""
        if PYDUB_AVAILABLE:
            try:
                audio = AudioSegment.from_file(audio_path)
                return len(audio)
            except:
                pass
        
        # 回退：通过文件大小估算（不准确）
        try:
            size_bytes = os.path.getsize(audio_path)
            # MP3: 约 128kbps = 16KB/s
            return (size_bytes / 16000) * 1000
        except:
            return 0
    
    def _create_silence(self, output_path: str, duration_ms: int):
        """创建静音片段"""
        if PYDUB_AVAILABLE:
            silence = AudioSegment.silent(duration=duration_ms)
            silence.export(output_path, format=self.default_format)
        else:
            # 创建空文件
            with open(output_path, "wb") as f:
                f.write(b"")
    
    def _concatenate_audio(self, audio_files: List[str], output_path: str):
        """拼接多个音频文件"""
        if not PYDUB_AVAILABLE:
            return
        
        combined = AudioSegment.empty()
        for audio_file in audio_files:
            try:
                audio = AudioSegment.from_file(audio_file)
                combined += audio
            except Exception as e:
                print(f"警告: 无法读取 {audio_file}: {e}", file=sys.stderr)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        combined.export(output_path, format=self.default_format)


class SimpleSynthesizer:
    """
    简单合成器（向后兼容）
    
    用于不需要情绪分析的快速合成场景
    """
    
    def __init__(
        self,
        api_base: str = "http://127.0.0.1:18791",
        default_format: str = "mp3"
    ):
        self.api_base = api_base
        self.default_format = default_format
        
        # 检查 API
        try:
            r = requests.get(f"{self.api_base}/v1/health", timeout=5)
            if r.status_code != 200:
                raise RuntimeError(f"API 返回 {r.status_code}")
        except Exception as e:
            raise RuntimeError(
                f"Fish Speech API 未运行或无法访问: {api_base}\n"
                f"错误: {e}\n"
                "请先启动 API Server"
            )
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        ref_audio: Optional[str] = None,
        voice_id: Optional[str] = None,
        **kwargs
    ) -> bool:
        """简单合成（无情绪分析）"""
        payload = {
            "text": text,
            "format": self.default_format,
            "normalize": True,
            "max_new_tokens": 2048,
            "chunk_length": 200,
            "top_p": 0.8,
            "repetition_penalty": 1.1,
            "temperature": 0.7,
            "streaming": False,
        }
        
        # 应用额外参数
        payload.update(kwargs)
        
        # 参考音频
        if ref_audio:
            if not os.path.exists(ref_audio):
                print(f"错误: 参考音频不存在: {ref_audio}", file=sys.stderr)
                return False
            with open(ref_audio, "rb") as f:
                audio_data = f.read()
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            payload["references"] = [{
                "audio": audio_b64,
                "text": ""
            }]
        
        # 已注册音色
        if voice_id:
            payload["reference_id"] = voice_id
        
        # 调用 API
        try:
            headers = {"Content-Type": "application/json"}
            r = requests.post(
                f"{self.api_base}/v1/tts",
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if r.status_code == 200:
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                size_kb = os.path.getsize(output_path) / 1024
                print(f"✅ 音频已生成: {output_path} ({size_kb:.1f} KB)")
                return True
            else:
                print(f"错误: TTS 失败 ({r.status_code}): {r.text[:500]}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"错误: 请求异常: {e}", file=sys.stderr)
            return False


if __name__ == "__main__":
    # 测试
    print("测试多段合成器...")
    
    try:
        synth = MultiSegmentSynthesizer(output_dir="test_output")
        
        test_text = "你好！今天天气真好。我们出去玩吧？太好了，我很开心！"
        
        results = synth.synthesize_with_analysis(
            text=test_text,
            output_path="test_output/combined.mp3",
            add_silence=True,
            silence_duration_ms=500
        )
        
        print(f"\n合成完成，共 {len(results)} 段")
        for r in results:
            print(f"  段 {r.segment_index}: {r.emotion} - {'成功' if r.success else '失败'}")
    
    except Exception as e:
        print(f"测试失败: {e}", file=sys.stderr)
