"""The speech engines the narration can use: the local Qwen3-TTS on an NVIDIA GPU, the local Kokoro on any CPU, and
remote services over HTTP (OpenAI's audio speech endpoint and the many services that copy it, ElevenLabs, Alibaba
DashScope Qwen-TTS).

Qwen is the only one that clones a voice from a reference clip, and demo_voice.py drives it through its own steps
(anchor, trial, takes). The other two speak each line in a built-in voice; demo_voice.py asks them for the same
anchor clip first, so every engine has a reference to check the voice against.

Every engine gives float samples at 24000 a second, mono, so what comes after (measure, fit, level, mix) does not
care which one spoke.
"""
from __future__ import annotations

import base64
import contextlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import demo_common

RATE = 24000

# what each engine is called in messages, what it can do, and the languages it can speak in
ENGINES = {
    'qwen': dict(name='Qwen3-TTS 1.7B', place='本机 GPU', clone=True,
                 languages=['zh', 'en', 'ja', 'ko', 'de', 'fr', 'es', 'it', 'pt', 'ru']),
    'kokoro': dict(name='Kokoro', place='本机 CPU', clone=False, languages=['zh', 'en']),
    'openai': dict(name='OpenAI 语音接口', place='远程', clone=False, languages=['zh', 'en', 'ja', 'ko', 'de', 'fr', 'es', 'it', 'pt', 'ru']),
    'compatible': dict(name='OpenAI 兼容接口', place='远程', clone=False, languages=['zh', 'en', 'ja', 'ko', 'de', 'fr', 'es', 'it', 'pt', 'ru']),
    'elevenlabs': dict(name='ElevenLabs', place='远程', clone=False, languages=['zh', 'en', 'ja', 'ko', 'de', 'fr', 'es', 'it', 'pt', 'ru']),
    'dashscope': dict(name='阿里百炼 Qwen-TTS', place='远程', clone=False, languages=['zh', 'en', 'ja', 'ko', 'de', 'fr', 'es', 'it', 'pt', 'ru']),
}

# ---------- the voices ----------
# Qwen3-TTS 1.7B CustomVoice: the nine speakers the model itself has (the ids are what the model knows: lower case, underscores)
QWEN_SPEAKERS = [('serena', '女声，温和'), ('vivian', '女声，清冷'), ('ono_anna', '女声，俏皮'), ('sohee', '女声，韩语感'),
                 ('uncle_fu', '男声，低沉'), ('ryan', '男声，昂扬'), ('aiden', '男声，美式'), ('eric', '四川话'), ('dylan', '北京话')]

# Kokoro: the names of the voices, in the order of the model's voices.bin (what sherpa-onnx calls sid)
KOKORO_V1_0 = ['af_alloy', 'af_aoede', 'af_bella', 'af_heart', 'af_jessica', 'af_kore', 'af_nicole', 'af_nova', 'af_river', 'af_sarah', 'af_sky',
               'am_adam', 'am_echo', 'am_eric', 'am_fenrir', 'am_liam', 'am_michael', 'am_onyx', 'am_puck', 'am_santa',
               'bf_alice', 'bf_emma', 'bf_isabella', 'bf_lily', 'bm_daniel', 'bm_fable', 'bm_george', 'bm_lewis',
               'ef_dora', 'em_alex', 'ff_siwis', 'hf_alpha', 'hf_beta', 'hm_omega', 'hm_psi', 'if_sara', 'im_nicola',
               'jf_alpha', 'jf_gongitsune', 'jf_nezumi', 'jf_tebukuro', 'jm_kumo', 'pf_dora', 'pm_alex', 'pm_santa',
               'zf_xiaobei', 'zf_xiaoni', 'zf_xiaoxiao', 'zf_xiaoyi', 'zm_yunjian', 'zm_yunxi', 'zm_yunxia', 'zm_yunyang', 'em_santa']
KOKORO_V1_1 = ['af_maple', 'af_sol', 'bf_vale',
               'zf_001', 'zf_002', 'zf_003', 'zf_004', 'zf_005', 'zf_006', 'zf_007', 'zf_008', 'zf_017', 'zf_018', 'zf_019',
               'zf_021', 'zf_022', 'zf_023', 'zf_024', 'zf_026', 'zf_027', 'zf_028', 'zf_032', 'zf_036', 'zf_038', 'zf_039',
               'zf_040', 'zf_042', 'zf_043', 'zf_044', 'zf_046', 'zf_047', 'zf_048', 'zf_049', 'zf_051', 'zf_059', 'zf_060',
               'zf_067', 'zf_070', 'zf_071', 'zf_072', 'zf_073', 'zf_074', 'zf_075', 'zf_076', 'zf_077', 'zf_078', 'zf_079',
               'zf_083', 'zf_084', 'zf_085', 'zf_086', 'zf_087', 'zf_088', 'zf_090', 'zf_092', 'zf_093', 'zf_094', 'zf_099',
               'zm_009', 'zm_010', 'zm_011', 'zm_012', 'zm_013', 'zm_014', 'zm_015', 'zm_016', 'zm_020', 'zm_025', 'zm_029',
               'zm_030', 'zm_031', 'zm_033', 'zm_034', 'zm_035', 'zm_037', 'zm_041', 'zm_045', 'zm_050', 'zm_052', 'zm_053',
               'zm_054', 'zm_055', 'zm_056', 'zm_057', 'zm_058', 'zm_061', 'zm_062', 'zm_063', 'zm_064', 'zm_065', 'zm_066',
               'zm_068', 'zm_069', 'zm_080', 'zm_081', 'zm_082', 'zm_089', 'zm_091', 'zm_095', 'zm_096', 'zm_097', 'zm_098', 'zm_100']

# the voice each engine speaks a language in when the story does not choose one
DEFAULTS = {
    'qwen': {'zh': 'serena', 'en': 'ryan', 'ja': 'ono_anna', 'ko': 'sohee', 'de': 'ryan', 'fr': 'ryan', 'es': 'ryan',
             'it': 'ryan', 'pt': 'ryan', 'ru': 'ryan'},
    'kokoro': {'zh': ('zf_039', 'zf_xiaoyi'), 'en': ('af_maple', 'af_bella')},   # (v1.1, v1.0): the voices a recogniser heard right most often
    'openai': {'zh': 'marin', 'en': 'cedar', 'ja': 'marin', 'ko': 'marin', 'de': 'marin', 'fr': 'marin', 'es': 'marin', 'it': 'marin', 'pt': 'marin', 'ru': 'marin'},
    'compatible': {'zh': 'marin', 'en': 'cedar', 'ja': 'marin', 'ko': 'marin', 'de': 'marin', 'fr': 'marin', 'es': 'marin', 'it': 'marin', 'pt': 'marin', 'ru': 'marin'},
    'dashscope': {'zh': 'Cherry', 'en': 'Ethan', 'ja': 'Ono Anna', 'ko': 'Sohee', 'de': 'Lenn', 'fr': 'Emilien', 'es': 'Sonrisa',
                  'it': 'Dolce', 'pt': 'Cherry', 'ru': 'Cherry'},
    'elevenlabs': {},   # a voice id is the user's own: there is no default
}
OPENAI_VOICES = ['alloy', 'ash', 'ballad', 'coral', 'echo', 'fable', 'nova', 'onyx', 'sage', 'shimmer', 'verse', 'marin', 'cedar']
DASHSCOPE_VOICES = ['Cherry', 'Serena', 'Ethan', 'Chelsie', 'Momo', 'Vivian', 'Moon', 'Maia', 'Kai', 'Nofish', 'Bella', 'Jennifer', 'Ryan', 'Katerina',
                    'Aiden', 'Eldric Sage', 'Mia', 'Mochi', 'Bellona', 'Vincent', 'Bunny', 'Neil', 'Elias', 'Arthur', 'Nini', 'Seren', 'Pip', 'Stella',
                    'Bodega', 'Sonrisa', 'Alek', 'Dolce', 'Sohee', 'Ono Anna', 'Lenn', 'Emilien', 'Andre', 'Radio Gol', 'Jada', 'Dylan', 'Li', 'Marcus',
                    'Roy', 'Peter', 'Sunny', 'Eric', 'Rocky', 'Kiki']
QWEN_MODELS = {'qwen': 'Qwen3-TTS-12Hz-1.7B-CustomVoice', 'dashscope': 'qwen3-tts-flash', 'openai': 'gpt-4o-mini-tts',
               'compatible': 'tts-1', 'elevenlabs': 'eleven_multilingual_v2'}
QWEN_BASES = {'中国内地': 'https://dashscope.aliyuncs.com', '国际': 'https://dashscope-intl.aliyuncs.com'}
QWEN_LANGUAGES = {'zh': 'Chinese', 'en': 'English', 'ja': 'Japanese', 'ko': 'Korean', 'de': 'German', 'fr': 'French',
                  'es': 'Spanish', 'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian'}


class TTSError(RuntimeError):
    """The engine could not speak a line."""


def engine(name):
    """The code of an engine named by its code or its name ('Kokoro', '阿里百炼')."""
    known = str(name or '').strip().lower()
    for code, facts in ENGINES.items():
        if known in (code, facts['name'].lower()):
            return code
    short = {'local': 'qwen', 'local gpu': 'qwen', 'qwen3': 'qwen', 'qwen3-tts': 'qwen', 'cpu': 'kokoro', 'local cpu': 'kokoro',
             'openai-compatible': 'compatible', 'openai compatible': 'compatible', 'dashscope': 'dashscope', 'qwen-tts': 'dashscope',
             '阿里百炼': 'dashscope', '百炼': 'dashscope', '本地': 'qwen', '远程': None}
    if known in short and short[known]:
        return short[known]
    raise SystemExit(f'不认识这个配音引擎：{name}；能用的是 {"、".join(ENGINES)}')


def qwen_speaker(name):
    """A Qwen speaker as the model knows it: 'Ono Anna', 'ONO_ANNA' and 'ono anna' all become 'ono_anna'."""
    known = str(name or 'serena').strip().lower().replace(' ', '_').replace('-', '_')
    if known not in [speaker for speaker, _ in QWEN_SPEAKERS]:
        raise SystemExit(f'本机的 Qwen3-TTS 只有这些音色：{"、".join(speaker for speaker, _ in QWEN_SPEAKERS)}；没有 {name}')
    return known


def default_voice(engine_code, tongue):
    """The voice an engine speaks a language in unless the story chooses one."""
    chosen = DEFAULTS.get(engine_code, {}).get(tongue)
    if isinstance(chosen, tuple):   # Kokoro: (v1.1 name, v1.0 name), by the model there is
        return chosen[0] if demo_common.where('kokoro') and 'v1_1' in demo_common.where('kokoro').name else chosen[1]
    return chosen


def voices(engine_code, tongue):
    """The voices an engine can speak a language in, each with a short note: [(voice, note)]."""
    if engine_code == 'qwen':
        return [(name, note) for name, note in QWEN_SPEAKERS]
    if engine_code == 'kokoro':
        folder = demo_common.where('kokoro')
        names = KOKORO_V1_0 if folder and 'v1_0' in folder.name else KOKORO_V1_1
        if tongue == 'zh':
            return [(name, '女声' if name.startswith('zf') else '男声') for name in names if name.startswith(('zf_', 'zm_'))]
        return [(name, '英文' if name.startswith(('af_', 'am_', 'bf_', 'bm_')) else '') for name in names if name.startswith(('af_', 'am_', 'bf_', 'bm_'))]
    if engine_code in ('openai', 'compatible'):
        return [(name, '') for name in OPENAI_VOICES]
    if engine_code == 'dashscope':
        return [(name, '') for name in DASHSCOPE_VOICES]
    return []


# ---------- the local CPU engine ----------
@contextlib.contextmanager
def quiet():
    """sherpa-onnx writes one line to stderr for every word its lexicon does not have; the caller says those itself."""
    try:
        saved = os.dup(2)
        with open(os.devnull, 'wb') as sink:
            os.dup2(sink.fileno(), 2)
            yield
    except (OSError, ValueError):
        yield
    finally:
        with contextlib.suppress(OSError, ValueError, UnboundLocalError):
            os.dup2(saved, 2)
            os.close(saved)


class Kokoro:
    """Kokoro on the CPU, through sherpa-onnx: Chinese and English; v1.1 has 100 Mandarin voices and 3 English ones."""

    takes_speed = True   # the engine can be asked to speak slower or faster (GenerationConfig.speed)

    def __init__(self, folder=None, speaker=None, threads=None):
        self.folder = Path(folder) if folder else demo_common.where('kokoro')
        if not self.folder or not (self.folder / 'model.onnx').is_file():
            raise TTSError(f'没有 Kokoro 模型：{demo_common.HOME / "models/kokoro-multi-lang-v1_1"}；用 python3 scripts/demo_env.py setup --kokoro 下载')
        if importlib.util.find_spec('sherpa_onnx') is None:
            raise TTSError('缺 sherpa-onnx：运行 python3 scripts/demo_env.py setup')
        self.names = KOKORO_V1_0 if 'v1_0' in self.folder.name else KOKORO_V1_1
        self.speaker = self.name_of(speaker)
        self.threads = threads or max(2, min(8, os.cpu_count() or 4))
        self._tts = None
        self._lexicon = None

    def name_of(self, speaker):
        """A voice as its name ('zf_062') or number (86)."""
        if speaker is None or speaker == '':
            return self.names[0]
        text = str(speaker).strip()
        if text.isdigit():
            number = int(text)
            if not 0 <= number < len(self.names):
                raise TTSError(f'Kokoro 只有 0 到 {len(self.names) - 1} 号音色，没有 {number}')
            return self.names[number]
        if text in self.names:
            return text
        raise TTSError(f'这个 Kokoro 模型里没有 {text}；有 {len(self.names)} 个，如 {"、".join(self.names[:6])}')

    def sid(self):
        return self.names.index(self.speaker)

    def load(self):
        if self._tts is not None:
            return self._tts
        import sherpa_onnx
        files = lambda name: self.folder / name
        lexicons = [files(name) for name in ('lexicon-us-en.txt', 'lexicon-zh.txt') if files(name).is_file()]
        rules = [files(name) for name in ('date-zh.fst', 'phone-zh.fst', 'number-zh.fst') if files(name).is_file()]
        config = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                model=str(files('model.onnx')), voices=str(files('voices.bin')), tokens=str(files('tokens.txt')),
                lexicon=','.join(str(path) for path in lexicons)), num_threads=self.threads, provider='cpu'),
            rule_fsts=','.join(str(path) for path in rules), max_num_sentences=1)
        if not config.validate():
            raise TTSError(f'Kokoro 的配置不对：{self.folder}')
        self._lexicon = lexicons
        with quiet():
            self._tts = sherpa_onnx.OfflineTts(config)
        return self._tts

    def speak(self, text, seed=0, speed=1.0, instruct=None):
        import sherpa_onnx
        tts = self.load()
        generation = sherpa_onnx.GenerationConfig()
        generation.sid, generation.speed, generation.silence_scale = self.sid(), float(max(0.5, min(2.0, speed))), 0.2
        with quiet():
            audio = tts.generate(text, generation)
        samples = np.asarray(audio.samples, dtype=np.float32).reshape(-1)
        if not samples.size:
            raise TTSError(f'Kokoro 没有出声：{text[:40]}')
        return samples, RATE

    def unknown(self, text, tongue):
        """The words of an English caption the model's lexicon does not have: they would be skipped silently."""
        if tongue != 'en' or not self._lexicon:
            return []
        known = set()
        for path in self._lexicon:
            if path.name == 'lexicon-us-en.txt':
                known = {line.split(' ', 1)[0].lower() for line in path.read_text(encoding='utf-8', errors='replace').splitlines()}
        return sorted({word.lower() for word in re.findall(r"[A-Za-z][A-Za-z'’-]*", text) if word.lower() not in known})


# ---------- the remote services ----------
def _http():
    import httpx
    # the environment's proxy settings are honoured: a machine behind one reaches the services only through it
    return httpx.Client(timeout=httpx.Timeout(120.0, connect=20.0), trust_env=True, headers={'User-Agent': 'autoRecording/2.0'})


def _decoded(content, content_type=''):
    """Samples and their rate from what a service answered: a WAV file, MP3 audio, or raw 16-bit PCM at 24000 a second."""
    if content[:4] == b'RIFF' or 'wav' in content_type:
        import soundfile
        samples, rate = soundfile.read(io.BytesIO(content), dtype='float32', always_2d=False)
        return np.asarray(samples, dtype=np.float32).reshape(-1), int(rate)
    if content[:3] == b'ID3' or content[:2] in (b'\xff\xfb', b'\xff\xf3', b'\xff\xf2') or 'mpeg' in content_type or 'mp3' in content_type:
        done = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-f', 'f32le', '-ac', '1', '-ar', str(RATE), 'pipe:1'],
                              input=content, capture_output=True)
        if done.returncode:
            raise TTSError('这条回答不是能听的音频：' + done.stderr.decode('utf-8', 'replace')[:200])
        return np.frombuffer(done.stdout, dtype='<f4').copy(), RATE
    if content[:4] == b'OggS' or 'ogg' in content_type:
        done = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-f', 'f32le', '-ac', '1', '-ar', str(RATE), 'pipe:1'],
                              input=content, capture_output=True)
        if done.returncode:
            raise TTSError('这条回答不是能听的音频：' + done.stderr.decode('utf-8', 'replace')[:200])
        return np.frombuffer(done.stdout, dtype='<f4').copy(), RATE
    samples = np.frombuffer(content[:len(content) // 2 * 2], dtype='<i2').astype(np.float32) / 32768.0   # raw PCM, 16 bit, little endian
    if not samples.size:
        raise TTSError(f'这条回答是空的（{content_type or "没有说明类型"}）：{content[:60]!r}')
    return samples, RATE


class Remote:
    """A speech service over HTTP. The three shapes here are the ones in use: OpenAI's audio endpoint (and the many
    services that copy it), ElevenLabs, and Alibaba DashScope's Qwen-TTS."""

    takes_speed = True   # openai, compatible and elevenlabs take a speed; DashScope's Qwen-TTS does not (see __init__)

    def __init__(self, provider, model=None, speaker=None, base_url=None, api_key=None, language_code=None, retries=3):
        self.provider, self.speaker, self.retries = provider, speaker, retries
        self.takes_speed = provider != 'dashscope'   # Qwen-TTS speaks at its own pace: what does not fit is sped up at the mixing
        self.api_key = api_key or demo_common.key(provider)
        self.base_url = (base_url or {'openai': 'https://api.openai.com/v1', 'elevenlabs': 'https://api.elevenlabs.io/v1/text-to-speech',
                                      'dashscope': QWEN_BASES['中国内地'], 'compatible': 'https://api.openai.com/v1'}[provider]).rstrip('/')
        self.model = model or QWEN_MODELS.get(provider)
        self.language_code = language_code
        if provider in ('openai', 'compatible', 'dashscope') and not self.api_key and not base_url:
            raise TTSError(f'没有 {provider} 的密钥：demo_env.py key {provider}=…，或设 DEMO_TTS_API_KEY')
        if provider == 'elevenlabs' and not self.speaker:
            raise TTSError('ElevenLabs 要用 voice id：在 VOICE 里写 speaker（例如 21m00Tcm4TlvDq8ikWAM 是公开示例音色 Rachel）')

    def _call(self, build):
        """Send the request, retrying what is worth retrying; a final failure carries what the service said."""
        import httpx
        problem = None
        for attempt in range(self.retries):
            try:
                with _http() as client:
                    answer = build(client)
                if answer.status_code < 400:
                    return answer
                if answer.status_code in (408, 409, 429) or answer.status_code >= 500:
                    problem = f'{answer.status_code} {answer.text[:200]}'
                    wait = float(answer.headers.get('retry-after') or 0) or 2.0 * (attempt + 1)
                    time.sleep(min(wait, 30))
                    continue
                raise TTSError(f'服务拒绝了这次请求：{answer.status_code} {answer.text[:300]}')
            except httpx.TransportError as error:
                problem = str(error) or type(error).__name__
                time.sleep(1.5 * (attempt + 1))
        raise TTSError(f'连不上服务：{problem}')

    def speak(self, text, seed=0, speed=1.0, instruct=None):
        if self.provider in ('openai', 'compatible'):
            body = {'model': self.model, 'voice': self.speaker, 'input': text, 'response_format': 'wav'}
            if instruct:
                body['instructions'] = instruct
            if abs(speed - 1.0) > 1e-3:
                body['speed'] = round(float(min(4.0, max(0.25, speed))), 3)
            answer = self._call(lambda client: client.post(f'{self.base_url}/audio/speech', json=body,
                                                           headers={'Authorization': f'Bearer {self.api_key}'}))
            return _decoded(answer.content, answer.headers.get('content-type', ''))
        if self.provider == 'elevenlabs':
            body = {'text': text, 'model_id': self.model, 'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75, 'style': 0.0,
                                                                              'use_speaker_boost': True, 'speed': round(float(min(1.2, max(0.7, speed))), 3)}}
            if self.language_code:
                body['language_code'] = self.language_code
            answer = self._call(lambda client: client.post(f'{self.base_url}/{self.speaker}', params={'output_format': 'pcm_24000'}, json=body,
                                                           headers={'xi-api-key': self.api_key}))
            return _decoded(answer.content, 'audio/pcm')
        if self.provider == 'dashscope':
            body = {'model': self.model, 'input': {'text': text, 'voice': self.speaker, 'language_type': self.language_code or 'Auto'}}
            answer = self._call(lambda client: client.post(f'{self.base_url}/api/v1/services/aigc/multimodal-generation/generation', json=body,
                                                           headers={'Authorization': f'Bearer {self.api_key}'}))
            data = answer.json()
            if data.get('code'):
                raise TTSError(f'百炼拒绝了这次请求：{data.get("code")} {data.get("message")}')
            audio = ((data.get('output') or {}).get('audio')) or {}
            if audio.get('data'):
                return _decoded(base64.b64decode(audio['data']), 'audio/wav')
            if audio.get('url'):
                with _http() as client:
                    got = client.get(audio['url'])
                if got.status_code >= 400:
                    raise TTSError(f'取不回合成的音频：{got.status_code}')
                return _decoded(got.content, got.headers.get('content-type', ''))
            raise TTSError('百炼的回答里没有音频：' + json.dumps(data, ensure_ascii=False)[:300])
        raise TTSError(f'不知道怎样调用 {self.provider}')


# ---------- what is there, and what one engine is ----------
def usable(code):
    """Whether an engine can speak on this machine: (yes, what is missing or where it is)."""
    if code == 'qwen':
        if sys.platform == 'darwin':
            return False, 'macOS 没有 CUDA：用 kokoro（本机 CPU）或远程服务'
        python, custom, base = demo_common.where('tts_python'), demo_common.where('tts_custom'), demo_common.where('tts_base')
        if not (python and custom and base):
            return False, '缺语音模型的 Python 或两个 Qwen3-TTS 模型（references/environment.md）'
        return True, str(python)
    if code == 'kokoro':
        folder = demo_common.where('kokoro')
        if not folder:
            return False, '缺 Kokoro 模型（demo_env.py setup --kokoro）'
        if importlib.util.find_spec('sherpa_onnx') is None:
            return False, '缺 sherpa-onnx（demo_env.py setup）'
        return True, str(folder)
    if code == 'elevenlabs':
        return (True, '有密钥') if demo_common.key('elevenlabs') else (False, '缺 ELEVENLABS_API_KEY 或 demo_env.py key 记下的密钥')
    if code in ('openai', 'dashscope', 'compatible'):
        has = demo_common.key(code) or demo_common.key('openai' if code == 'compatible' else code)
        return (True, '有密钥') if has else (False, f'缺密钥：demo_env.py key {code}=…（或环境变量）')
    return False, '不认识的引擎'


def choose(asked=None, api_key=None, base_url=None):
    """The engine to speak with: the one asked for, else the first that can: Qwen on the GPU, then Kokoro on the CPU, then a
    remote service with a key. A service without an environment key is still usable when the settings carry a key or a
    base_url (a local or in-house endpoint)."""
    if asked:
        code = engine(asked)
        ok, detail = usable(code)
        if not ok and code in ('openai', 'compatible', 'elevenlabs', 'dashscope') and (api_key or base_url):
            ok, detail = True, '按设置里的密钥或地址'
        if not ok:
            raise TTSError(f'{ENGINES[code]["name"]} 现在用不了：{detail}')
        return code
    for code in ('qwen', 'kokoro', 'openai', 'dashscope', 'elevenlabs', 'compatible'):
        if usable(code)[0]:
            return code
    raise TTSError('没有能用的配音引擎：demo_env.py 看缺什么；不配音也可以，成片是无声的')


def make(code, tongue, speaker=None, model=None, base_url=None, api_key=None, language_code=None, threads=None):
    """One engine, ready to speak a language in one voice."""
    speaker = speaker or default_voice(code, tongue)
    if code == 'kokoro':
        return Kokoro(speaker=speaker, threads=threads)
    if code in ('openai', 'compatible', 'elevenlabs', 'dashscope'):
        return Remote(code, model=model, speaker=speaker, base_url=base_url, api_key=api_key,
                      language_code=language_code or (QWEN_LANGUAGES.get(tongue) if code == 'dashscope' else None))
    raise TTSError(f'{code} 不走这里（Qwen 由 demo_voice.py 自己的步骤运行）')
