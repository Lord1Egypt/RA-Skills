# FunAsrTranscriber.py
import os
import traceback
import logging
from funasr import AutoModel
import tempfile
import wave
import io
import numpy as np
import asyncio

# 配置日志
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# 热词配置
HOT_WORDS = ["吴晓阳", "统账结合", "单建统筹", "个账", "异地", "门特", "大爱无疆",
             "共济账户", "共济定点", "门诊共济", "家庭共济", "零星报销"]


class AsrTranscriber:
    def __init__(self):
        """初始化FunASR模型"""
        try:
            self.model = AutoModel(
                model="../models/Fun-ASR-Nano-2512",
                trust_remote_code=True,
                remote_code="./FunASRNano.py",
                device="cpu",  # VMware 环境使用 CPU
                disable_update=True,
            )
            logger.info("✅ ASR转录器初始化成功")
        except Exception as e:
            logger.warning(f"❌ ASR转录器初始化失败: {e}请确保模型文件存在于models/Fun-ASR-Nano-2512目录中")
            raise

    def transcribe_sync(self, audio_file):
        """同步处理音频文件"""
        try:
            # 进行语音识别
            res = self.model.generate(
                input=audio_file,
                cache={},
                batch_size=1,
                batch_size_s=0,
                hotwords=HOT_WORDS,
                itn=True,
            )

            # 提取识别结果
            result_text = self._extract_result(res)
            return result_text

        except Exception as e:
            error_msg = f"处理音频时出错: {str(e)}"
            logger.warning(error_msg)
            traceback.print_exc()
            return error_msg

    @staticmethod
    def _extract_result(res):
        """从识别结果中提取文本"""
        if not res or len(res) == 0:
            return "识别失败，未获得结果"

        result_item = res[0]
        if isinstance(result_item, dict):
            text = result_item.get('text', '识别结果为空')
            return text.strip()
        elif isinstance(result_item, str):
            return result_item.strip()
        else:
            return str(result_item).strip()

# 删除记录的临时录音文件
def _clr_rec_files(audio_files):
    """安全清理临时文件"""
    if not audio_files:
        return []
    remain_files = []
    logger.debug(f"清理临时文件: {audio_files}")

    i = len(audio_files) - 1
    while i >= 0:
        audio_file = audio_files[i]
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
                logger.debug(f"已删除音频文件: {audio_file}")
                # 成功删除后，从列表中移除
                audio_files.pop(i)
            else:
                logger.debug(f"文件不存在，跳过: {audio_file}")
                # 可选：是否也从列表中移除？根据你的需求
                # 如果“不存在”也算“清理完成”，可以 pop；否则保留
                # audio_files.pop(i)
        except Exception as e:
            logger.warning(f"清理临时文件时出错: {str(e)}")
            remain_files.append(audio_file)
            traceback.print_exc()
            # 出错时不 pop，保留在 audio_files 中（或按需处理）
        i -= 1

def ensure_wav_format(audio_data, sample_rate=16000):
    """
    确保音频数据是WAV格式
    """
    # 如果已经是WAV格式的字节数据，直接返回
    if isinstance(audio_data, bytes) and audio_data[:4] == b'RIFF':
        return audio_data

    logger.debug("非Wav格式，转换中...")
    # 否则假设是原始PCM数据，转换为WAV格式
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)

        # 确保数据是字节格式
        if isinstance(audio_data, np.ndarray):
            audio_bytes = audio_data.tobytes()
        elif isinstance(audio_data, bytes):
            audio_bytes = audio_data
        else:
            # 尝试转换为numpy数组再转字节
            try:
                audio_array = np.array(audio_data, dtype=np.int16)
                audio_bytes = audio_array.tobytes()
            except:
                raise ValueError("无法处理的音频格式")

        wav_file.writeframes(audio_bytes)

    wav_buffer.seek(0)
    logger.debug("Wav格式转换完成")
    return wav_buffer.read()

async def speech_to_text_local(transcriber, audio_data, audio_files):
    """
    使用本地FunASR模型进行语音转文字
    """
    if transcriber is None:
        return "ASR转录器未初始化，请检查模型文件"

    # 创建临时文件保存音频
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_path = temp_file.name

        try:
            # 确保音频格式正确
            wav_data = ensure_wav_format(audio_data, sample_rate=16000)

            # 写入WAV文件
            with open(temp_path, 'wb') as f:
                f.write(wav_data)

            # 使用异步方式调用ASR转录
            result_text = await asyncio.to_thread(
                transcriber.transcribe_sync,
                audio_file=temp_path,
            )
            # 添加识别过的录音文件
            audio_files.append(temp_path)
            # 提取文本结果
            if isinstance(result_text, tuple):
                text_result = result_text[0]
            else:
                text_result = result_text

            return text_result

        except Exception as e:
            logger.error(f"语音识别失败: {str(e)}")
            return f"语音识别失败: {str(e)}"
