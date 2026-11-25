"""Give a demo video a spoken narration: its captions, read in the language the captions are in.

The picture is not touched and the video keeps its length. Every line starts just after its caption
appears and ends before the next caption does; a line that would run over is said a little faster,
never the other way round. One short reference clip fixes the voice, its pitch and its pace, and
every line is spoken as a continuation of that same clip (Qwen) or in the same built-in voice (Kokoro,
remote services), so the voice does not drift from line to line.

    PY=~/.cache/auto-demo-recording/venv/bin/python
    $PY demo_voice.py lines --work path/to/work        # the lines as they will be said and the time each has; needs no model
    $PY demo_voice.py --work path/to/work              # all steps; writes <the rendered video>-<配音版 | narrated>.mp4 next to it
    $PY demo_voice.py build --work path/to/work        # only choose, fit and mix again (after changing settings)
    $PY demo_voice.py anchor 2-5 --work path/to/work   # another reference clip (they are in work/voice/anchor); then all steps again

The engine comes from VOICE['engine'] in the story file or work/voice/settings.json (see references/engines.md):
qwen (local GPU, clones the reference voice), kokoro (local CPU, Chinese and English), or a remote service
(openai, compatible, elevenlabs, dashscope). The language comes from VOICE['language'] or the story's LANGUAGE.

The steps: anchor (the reference clip of the voice) - trial (only Qwen: a few lines after each candidate; the one
whose lines fit their captions and move least in pitch is taken) - takes (each line several times) - hear (a speech
recogniser writes down what was said, a speaker model tells how close the voice is) - build (choose a take per
line, fit, level, mix, put under the picture) - check (the finished file, in numbers: same picture, same length,
every line inside its caption and said right). What is done is kept: a step that is run again only does what is
missing or has changed.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

import demo_common
import demo_text
import demo_tts
from demo_common import need, where

HERE = Path(__file__).resolve().parent
RATE = 24000   # what every engine gives (or is brought to)
SAMPLING = dict(do_sample=True, temperature=0.6, top_p=0.88, top_k=32, repetition_penalty=1.08)  # little is left to chance: one line sounds like the next
SAME = 0.65   # two clips count as the same voice from this likeness on (the speaker model gives 0.8 to 0.95 for one voice, 0.2 to 0.6 for two)
HOW = f'运行 python3 {HERE / "demo_env.py"} 看缺什么、怎么补'
DEFAULTS = {
    'engine': None,          # qwen, kokoro, openai, compatible, elevenlabs, dashscope; left empty: the first that can speak here
    'language': None,        # zh, en, ja, ko, de, fr, es, it, pt, ru; left empty: the story's LANGUAGE, else the captions themselves
    'speaker': None,         # the voice: a Qwen speaker, a Kokoro voice ('zf_062' or 86), or a remote voice id; left empty: the engine's usual one
    'model': None,           # remote: the model id (openai: gpt-4o-mini-tts; dashscope: qwen3-tts-flash; elevenlabs: eleven_multilingual_v2)
    'base_url': None,        # remote: another endpoint (a proxy, a self-hosted service, the international region)
    'api_key': None,         # remote: usually from the environment or demo_env.py key, not written in the story
    'language_code': None,   # remote: the service's name for the language where it takes one (dashscope takes it by itself)
    'instructions': None,    # remote: a style instruction, where the service takes one (OpenAI's instructions)
    'styles': ['用标准普通话做软件功能讲解。语气平稳、客观，不带情绪起伏，音高和音量保持均匀，语速中等，吐字清楚，句末自然收音。',
               '用标准普通话做软件功能讲解。语气平稳、沉着，像在念一份说明，音高起伏很小，语速中等偏快，吐字清楚。',
               '用标准普通话做软件功能讲解。语气平稳、客观，不带情绪起伏，音高和音量保持均匀，语速稍慢，吐字清楚，句末自然收音。',
               '用标准普通话做软件功能讲解。语气平稳、沉着，像在念一份说明，音高起伏很小，语速偏慢，从容不迫，吐字清楚。'],   # Qwen: the deliveries the reference clips are tried in
    'candidates': 8,         # Qwen: reference clips made in each style
    'anchor_text': None,     # what the reference clip says; left empty: the title and the first captions
    'anchor': None,          # Qwen: the reference clip to take, e.g. '3-6'; left empty: the one the trial finds
    'say': {},               # how to say what the rules get wrong: {'WPS 365': 'W P S 三六五'} (demo_text.spoken)
    'pace': None,            # units a second the narration should have where the captions leave it the choice; left empty: what the language takes (4.3 字/秒 for Mandarin)
    'takes': None,           # times each line is spoken; left empty: 6 for Qwen, 4 for Kokoro, 2 for a remote service
    'lead': 0.25, 'gap': 0.30,           # a line starts this long after its caption appears, and ends at least this long before the next one
    'lead_min': 0.10, 'gap_min': 0.15,   # what these give way to where a line has little time
    'fastest': 1.12,         # no line should be sped up by more than this (never slowed down)
    'loudness': -16.0, 'peak': -1.5,     # LUFS of the whole narration, and the highest peak in dB
}
cfg = SimpleNamespace()


def configure(work, video=None, out=None):
    """The settings and the files of one video."""
    if not (work / 'timeline.json').is_file():
        raise SystemExit(f'{work} 里没有 timeline.json：先录制')
    timeline = json.loads((work / 'timeline.json').read_text(encoding='utf-8'))
    own = work / 'voice' / 'settings.json'
    chosen = {**DEFAULTS, **(timeline.get('voice') or {}), **(json.loads(own.read_text(encoding='utf-8')) if own.is_file() else {})}
    unknown = sorted(set(chosen) - set(DEFAULTS))
    if unknown:
        raise SystemExit(f'配音设置里有不认识的项：{"、".join(unknown)}；能设的是 {"、".join(DEFAULTS)}')
    captions = [event['text'] for event in timeline.get('events') or [] if event['type'] == 'caption' and event.get('text')]
    tongue = demo_text.language(chosen.get('language') or timeline.get('language')) or demo_text.guess(captions or [timeline.get('title') or ''])
    engine = demo_tts.choose(chosen['engine'], chosen['api_key'], chosen['base_url'])
    if tongue not in demo_tts.ENGINES[engine]['languages']:
        raise SystemExit(f'{demo_tts.ENGINES[engine]["name"]} 不说 {demo_text.LANGUAGES[tongue]["name"]}；能做的是 '
                         f'{"、".join(demo_text.LANGUAGES[code]["name"] for code in demo_tts.ENGINES[engine]["languages"])}。换一个引擎，或换一种语言')
    speaker = chosen['speaker'] or demo_tts.default_voice(engine, tongue)
    if engine == 'qwen':
        speaker = demo_tts.qwen_speaker(speaker)
    if engine == 'elevenlabs' and not speaker:
        raise SystemExit('ElevenLabs 要用 voice id：在 VOICE 里写 speaker（例如 21m00Tcm4TlvDq8ikWAM 是公开示例音色 Rachel）')
    if engine != 'qwen':
        try:  # the voice is checked now, before any step spends time on it
            demo_tts.make(engine, tongue, speaker=speaker, model=chosen['model'], base_url=chosen['base_url'],
                          api_key=chosen['api_key'], language_code=chosen['language_code'])
        except demo_tts.TTSError as error:
            raise SystemExit(str(error))
    plan = {'qwen': 6, 'kokoro': 4}.get(engine, 2)
    pace = float(chosen['pace'] or demo_text.LANGUAGES[tongue]['pace'])
    rendered = work / 'render.json'
    if not video and rendered.is_file():
        video = Path(json.loads(rendered.read_text(encoding='utf-8'))['out'])
    cfg.__dict__.update(chosen, work=work, folder=work / 'voice', timeline=timeline, title=timeline.get('title') or '', video=video,
                        tongue=tongue, engine=engine, speaker=speaker, pace=pace, takes=int(chosen['takes'] or plan),
                        qwen_language=demo_text.LANGUAGES[tongue]['qwen'], unit=demo_text.LANGUAGES[tongue]['unit'],
                        out=out or (video.with_name(video.stem + '-' + demo_text.LANGUAGES[tongue]['narrated'] + '.mp4') if video else None))


# ---------- the lines ----------
def spoken(text):
    return demo_text.spoken(text, cfg.say, cfg.tongue)


def units(text):
    return demo_text.units(text, cfg.tongue)


def lines():
    """The captions that are said: when each appears, how long it has until the next one, and how it is said."""
    captions = sorted((event for event in cfg.timeline['events'] if event['type'] == 'caption'), key=lambda event: event['t'])
    out = []
    for index, caption in enumerate(captions):
        say = spoken(caption['text'])
        if units(say):
            end = captions[index + 1]['t'] if index + 1 < len(captions) else cfg.timeline['duration']
            out.append({'n': len(out) + 1, 'start': caption['t'], 'window': end - caption['t'], 'text': caption['text'], 'say': say, 'units': units(say)})
    return out, cfg.timeline['duration']


def show_lines():
    """Each line as it will be said, with the pace it needs; where numbers or letters were turned into words, the caption below it."""
    script, _ = lines()
    print(f'参考音要说的话：{anchor_text()}')
    tight = 0
    for line in script:
        room, least = line['window'] - cfg.lead - cfg.gap, line['window'] - cfg.lead_min - cfg.gap_min
        needs = line['units'] / room if room > 0 else 99.0
        flag = ''
        if least <= 0 or line['units'] / (least * cfg.fastest) > cfg.pace + 0.6:
            flag, tight = '  ← 多半放不下：改短字幕，或重录时让它多停一会儿', tight + 1
        elif needs > cfg.pace + 0.5:
            flag = '  ← 偏紧'
        print(f'{line["n"]:3d} {line["start"]:7.2f} {line["window"]:5.2f}s {line["units"]:3d}{cfg.unit} 需 {needs:.2f}{cfg.unit}/秒  {line["say"]}{flag}')
        if re.sub(r'\s', '', line['say']) != re.sub(r'\s', '', line['text']):
            print(f'{"":35s}字幕原文：{line["text"]}')
    print(f'共 {len(script)} 句' + (f'，其中 {tight} 句多半放不下' if tight else '') + '。数字和字母的念法不对时，在 VOICE 的 say 里写明')


# ---------- sound ----------
def trim(samples, before=0.04, after=0.09):
    """Without the silence around it."""
    samples = np.asarray(samples, dtype=np.float32).reshape(-1)
    level = np.abs(samples)
    loud = np.flatnonzero(level > max(0.004, 0.03 * level.max()))
    if not loud.size:
        raise ValueError('没有声音')
    return samples[max(0, loud[0] - round(before * RATE)):min(len(samples), loud[-1] + round(after * RATE))].copy()


def at_rate(samples, rate):
    """Samples at the rate everything here is measured at."""
    if rate == RATE:
        return np.asarray(samples, dtype=np.float32).reshape(-1)
    import soxr
    return np.ascontiguousarray(soxr.resample(np.asarray(samples, dtype=np.float32).reshape(-1), rate, RATE, quality='HQ'), dtype=np.float32)


def write_wav(path, samples, rate=RATE):
    import soundfile
    soundfile.write(str(path), np.clip(samples, -1, 1), rate, subtype='PCM_16')


def read_wav(path):
    import soundfile
    samples, rate = soundfile.read(str(path), dtype='float32', always_2d=False)
    return samples, rate


def pitch_of(samples):
    """The pitch of a clip, frame by frame (Hz), and which frames were voiced. librosa where it is installed; else the
    same measurement by autocorrelation, so that the engines that do not need the speech Python are not made to need it."""
    try:
        import librosa
        low = librosa.resample(samples, orig_sr=RATE, target_sr=16000)
        pitch, voiced, _ = librosa.pyin(low, fmin=90, fmax=420, sr=16000, frame_length=1024, hop_length=160)
        return pitch[voiced & np.isfinite(pitch)]
    except ImportError:
        import soxr
        low = soxr.resample(samples, RATE, 16000, quality='HQ').astype(np.float32) if len(samples) > 1600 else np.zeros(1600, dtype=np.float32)
        frame, hop = 1024, 160
        count = max(0, (len(low) - frame) // hop + 1)
        if not count:
            return np.zeros(0)
        frames = np.lib.stride_tricks.as_strided(low, shape=(count, frame), strides=(low.strides[0] * hop, low.strides[0])).copy()
        energy = np.sqrt((frames ** 2).mean(axis=1))
        frames = frames * np.hanning(frame)
        spectrum = np.fft.rfft(frames, n=2 * frame, axis=1)
        autocorrelation = np.fft.irfft(np.abs(spectrum) ** 2, axis=1)[:, :frame]
        autocorrelation /= autocorrelation[:, :1] + 1e-12
        low_lag, high_lag = round(16000 / 420), min(frame - 1, round(16000 / 90))
        window = autocorrelation[:, low_lag:high_lag]
        best = np.argmax(window, axis=1)
        strength = window[np.arange(count), best]
        voiced = (strength > 0.3) & (energy > max(0.004, 0.05 * energy.max()))
        return 16000 / (best[voiced] + low_lag)


def measure(samples):
    """How a clip sounds, in numbers: its pitch (median, and how far it moves, in semitones), its level and its pauses."""
    pitch = pitch_of(samples)
    frames = samples[:len(samples) // 480 * 480].reshape(-1, 480)
    levels = np.sqrt((frames ** 2).mean(axis=1))
    active = levels[levels > 0.01]
    median = float(np.median(pitch)) if pitch.size else 0.0
    silences = np.diff(np.flatnonzero(np.concatenate(([True], levels >= 0.01, [True])))) - 1
    return {'seconds': round(len(samples) / RATE, 3), 'pitch': round(median, 1),
            'pitch_moves': round(float(np.std(12 * np.log2(pitch / median))), 2) if pitch.size else 0.0,
            'pitch_span': round(float(np.subtract(*np.percentile(12 * np.log2(pitch / median), [95, 5]))), 2) if pitch.size else 0.0,
            'level': round(float(20 * np.log10(np.sqrt((active ** 2).mean()))), 2) if active.size else -99.0,
            'pauses': round(float((levels < 0.01).mean()), 3), 'longest_pause': round(float(silences.max()) * 480 / RATE, 2)}


def tempo(samples, factor):
    """Said faster (factor above one) at the same pitch."""
    out = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(RATE), '-ac', '1', '-i', 'pipe:0', '-af', f'atempo={factor:.6f}', '-f', 'f32le', 'pipe:1'],
                         input=samples.astype('<f4').tobytes(), stdout=subprocess.PIPE, check=True).stdout
    return np.frombuffer(out, dtype='<f4').copy()


# ---------- Qwen: the local speech model ----------
def load(model_folder, max_seq_len=896):
    free = subprocess.run(['nvidia-smi', '--query-gpu=memory.free', '--format=csv,noheader,nounits'], capture_output=True, text=True)
    free = max((int(value) for value in free.stdout.split() if value.isdigit()), default=None) if free.returncode == 0 else None
    if free is not None and free < 6500:
        raise SystemExit(f'显存不够：空闲 {free / 1024:.1f} GB，语音模型要 6 GB 多。等占着显卡的程序退出后再运行同一条命令，做完的部分不会重做')
    import torch
    from faster_qwen3_tts import FasterQwen3TTS
    torch.set_num_threads(4)
    return FasterQwen3TTS.from_pretrained(str(model_folder), device='cuda', dtype=torch.bfloat16, attn_implementation='sdpa', max_seq_len=max_seq_len)


def speaker(model):
    """How close a clip is to a reference clip by the speech model's own measure of a voice (what is used where the speaker model is missing)."""
    import torch
    kept = {}
    of = lambda samples: torch.nn.functional.normalize(model.model.model.extract_speaker_embedding(audio=samples, sr=RATE).float().flatten(), dim=0)

    def close(samples, reference):
        if str(reference) not in kept:
            kept[str(reference)] = of(read_wav(reference)[0])
        return round(float(of(samples) @ kept[str(reference)]), 3)
    return close


# ---------- step 1: the reference clip ----------
def anchor_text():
    """What the reference clips say. Once there are clips, it is what they say."""
    listing = cfg.folder / 'anchor' / 'candidates.json'
    if listing.is_file():
        return json.loads(listing.read_text(encoding='utf-8'))['text']
    if cfg.anchor_text:
        return spoken(cfg.anchor_text)
    facts = demo_text.LANGUAGES[cfg.tongue]
    least, most = facts['anchor']
    text = spoken(facts['title_demo'].format(title=cfg.title) if cfg.title else facts['demo'])
    for line in lines()[0]:  # goes on with the first captions that are plain sentences, until it is long enough to carry a voice
        if units(text) >= least:
            break
        plain = not re.search(r'\d', line['say']) and (cfg.tongue != 'zh' or not re.search('[A-Za-z]', line['say']))
        if plain and line['say'][-1:] in '。！？.!?' and units(text + line['say']) <= most:
            text += ('' if cfg.tongue == 'zh' or text.endswith(' ') else ' ') + line['say']
    return text if units(text) >= least else text + ('' if cfg.tongue == 'zh' else ' ') + facts['stock']


def candidates():
    """The model's own speaker says one text a number of times in each of the styles. One of these clips becomes the reference for every line."""
    import torch
    folder = cfg.folder / 'anchor'
    listing = folder / 'candidates.json'
    if listing.is_file():
        made = json.loads(listing.read_text(encoding='utf-8'))
        if made.get('speaker') != cfg.speaker or (cfg.anchor_text and spoken(cfg.anchor_text) != made['text']):
            raise SystemExit(f'{folder} 里的参考音是按别的设置做的（{made.get("speaker")}：{made["text"]}）。要按现在的设置重做，先删掉 {folder}、anchor.wav 和 anchor.json')
    folder.mkdir(parents=True, exist_ok=True)
    text = anchor_text()
    model, count, rows = None, units(text), []
    for style_index, style in enumerate(cfg.styles):
        for seed in range(cfg.candidates):
            path = folder / f'{style_index}-{seed}.wav'
            if not path.is_file():
                model = model or load(need('tts_custom', HOW), 768)
                torch.manual_seed(1000 + seed)
                wavs, rate = model.generate_custom_voice(text=text, speaker=cfg.speaker, language=cfg.qwen_language, instruct=style,
                                                         max_new_tokens=math.ceil(count / 2.4 * 12.5) + 40, **{**SAMPLING, 'temperature': 0.7})
                assert rate == RATE and len(wavs) == 1
                path.with_suffix('.heard.json').unlink(missing_ok=True)
                try:
                    write_wav(path, trim(wavs[0]))
                except ValueError:
                    continue
            samples, _ = read_wav(path)
            rows.append({'file': path.name, 'style': style_index, 'seed': seed, 'pace': round(count / (len(samples) / RATE), 2), **measure(samples)})
            print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    listing.write_text(json.dumps({'text': text, 'speaker': cfg.speaker, 'rows': rows}, ensure_ascii=False, indent=1), encoding='utf-8')


def known():
    """The reference clips there are, each with what was measured and what was heard of it."""
    listing = cfg.folder / 'anchor' / 'candidates.json'
    if not listing.is_file():
        raise SystemExit('还没有参考音：demo_voice.py anchor')
    data = json.loads(listing.read_text(encoding='utf-8'))
    for row in data['rows']:
        facts = (listing.parent / row['file']).with_suffix('.heard.json')
        if facts.is_file():
            row.update(json.loads(facts.read_text(encoding='utf-8')))
    return data


def take_anchor(name):
    """One of the clips becomes the reference for every line."""
    data = known()
    row = next((row for row in data['rows'] if row['file'] == f'{name}.wav'), None)
    if not row:
        raise SystemExit(f'没有这条参考音：{name}；有的是 {"、".join(row["file"][:-4] for row in data["rows"])}')
    facts = cfg.folder / 'anchor.json'
    before = json.loads(facts.read_text(encoding='utf-8')).get('file') if facts.is_file() else None
    shutil.copyfile(cfg.folder / 'anchor' / row['file'], cfg.folder / 'anchor.wav')
    facts.write_text(json.dumps({'text': data['text'], 'speaker': data.get('speaker', cfg.speaker), 'said_as': cfg.styles[row['style']], **row}, ensure_ascii=False, indent=1), encoding='utf-8')
    other = bool(before) and before != row['file']
    if other:
        shutil.rmtree(cfg.folder / 'takes', ignore_errors=True)  # spoken after another reference: of no use any more
    print(f'参考音：{name}（语速 {row["pace"]} 字/秒，音高 {row["pitch"]} Hz，起伏 {row["pitch_moves"]} 个半音）' + ('；按别的参考音录的句子已清掉' if other else ''), flush=True)
    if not usual(row, data['rows']):
        print('注意：这一条的音色和多数候选不是同一个（模型的同一个说话人，各次出来的音色不总一样）', flush=True)


def said_already(path, line):
    """Spoken already, and with the words the caption has now, and by the engine as it is set now."""
    facts = path.with_suffix('.json')
    if not (facts.is_file() and path.is_file()):
        return False
    remembered = json.loads(facts.read_text(encoding='utf-8'))
    return remembered.get('say') == line['say'] and remembered.get('signature', signature()) == signature()


def clone(model, close, line, reference, reference_text, path, seed):
    """One line said as a continuation of a reference clip, with what can be measured of it. None when nothing came out."""
    import torch
    for old in (path, path.with_suffix('.json'), path.with_suffix('.heard.json')):
        old.unlink(missing_ok=True)
    torch.manual_seed(seed)
    wavs, rate = model.generate_voice_clone(text=line['say'], language=cfg.qwen_language, ref_audio=str(reference), ref_text=reference_text,
                                            xvec_only=False, append_silence=True, non_streaming_mode=True,
                                            max_new_tokens=math.ceil(line['units'] / 2.2 * 12.5) + 40, **SAMPLING)
    assert rate == RATE and len(wavs) == 1
    try:
        samples = trim(wavs[0])
    except ValueError:
        return None
    write_wav(path, samples)
    facts = {**measure(samples), 'pace': round(line['units'] / (len(samples) / RATE), 2), 'same_voice': close(samples, reference), 'n': line['n'], 'say': line['say'],
             'signature': signature()}
    facts['speaking'] = round(facts['pace'] / (1 - facts['pauses']), 2)  # the pace without the pauses at the commas: what a listener takes as the speed
    path.with_suffix('.json').write_text(json.dumps(facts, ensure_ascii=False), encoding='utf-8')
    return facts


# ---------- step 1 (other engines): the reference clip ----------
def signature():
    """What a take depends on: the engine, the voice, the model, the speed of the voice, the language. A take made under
    another signature is not the same voice and is spoken again."""
    return {'engine': cfg.engine, 'speaker': cfg.speaker, 'model': cfg.model or '', 'base_url': cfg.base_url or '', 'language': cfg.tongue}


def plain_engine():
    return demo_tts.make(cfg.engine, cfg.tongue, speaker=cfg.speaker, model=cfg.model, base_url=cfg.base_url, api_key=cfg.api_key,
                         language_code=cfg.language_code)


def plain_anchor():
    """One clip of the voice, from the same text the Qwen reference says: what 'the same voice' means for the rest, and
    the pace the voice comes out at (so that each line is asked for at the pace the video wants)."""
    facts_path, clip = cfg.folder / 'anchor.json', cfg.folder / 'anchor.wav'
    if facts_path.is_file() and clip.is_file() and json.loads(facts_path.read_text(encoding='utf-8')).get('signature') == signature():
        print(f'参考音已经有了：{clip}', flush=True)
        return
    text = anchor_text()
    try:
        engine = plain_engine()
        samples, rate = engine.speak(text, seed=4242, speed=1.0, instruct=cfg.instructions)
    except demo_tts.TTSError as error:
        raise SystemExit(f'参考音没有念出来：{error}')
    samples = trim(at_rate(samples, rate))
    write_wav(clip, samples)
    facts = {**measure(samples), 'text': text, 'signature': signature(), 'speaker': cfg.speaker, 'file': 'anchor.wav', 'n': None}
    facts['pace'] = round(units(text) / (len(samples) / RATE), 2)
    if getattr(engine, 'takes_speed', True):
        facts['speed'] = round(min(1.35, max(0.8, cfg.pace / max(0.5, facts['pace']))), 3)   # the engine is asked to speak this much faster than it does by itself
    else:
        facts['speed'] = 1.0   # this one tells its own pace; a line that does not fit is sped up at the mixing, and check says when it is too much
    facts_path.write_text(json.dumps(facts, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'参考音：{cfg.speaker}（{demo_tts.ENGINES[cfg.engine]["name"]}；自身语速 {facts["pace"]} {cfg.unit}/秒，音高 {facts["pitch"]} Hz'
          + (f'，念出来按 {facts["speed"]} 倍速' if getattr(engine, 'takes_speed', True) else '；这个服务没有语速参数，放不下时在混音时加快')
          + '）', flush=True)
    if cfg.engine == 'kokoro':
        engine.load()
        missing = engine.unknown(' '.join([text] + [line['say'] for line in lines()[0]]), cfg.tongue)
        if missing:
            print('注意：Kokoro 的词表里没有这些词，念的时候会跳过：' + '、'.join(missing[:20]) + ('…' if len(missing) > 20 else '') +
                  '。在 VOICE 的 say 里写它们的念法，例如 {"API": "A P I"}', flush=True)


def plain_takes(count, only=None):
    """Every line, spoken by the engine again and again; what can be measured and what it is to say is written next to it."""
    facts_path = cfg.folder / 'anchor.json'
    if not facts_path.is_file():
        raise SystemExit('还没有参考音：demo_voice.py anchor')
    reference = json.loads(facts_path.read_text(encoding='utf-8'))
    if reference.get('signature') != signature():
        raise SystemExit('参考音是按别的音色做的：删掉 voice/anchor.wav、voice/anchor.json 和 voice/takes，或运行 demo_voice.py anchor')
    speed = float(reference.get('speed', 1.0))
    folder = cfg.folder / 'takes'
    folder.mkdir(parents=True, exist_ok=True)
    wanted = [(line, take) for line in lines()[0] if not only or line['n'] in only for take in range(count) if not said_already(folder / f'{line["n"]:03d}-{take}.wav', line)]
    if not wanted:
        return
    engine = plain_engine()
    failures = 0
    for done, (line, take) in enumerate(wanted, 1):
        try:
            samples, rate = engine.speak(line['say'], seed=7000 + 37 * line['n'] + take, speed=speed, instruct=cfg.instructions)
            samples = trim(at_rate(samples, rate))
        except demo_tts.TTSError as error:
            failures += 1
            print(f'[{done}/{len(wanted)}] 第 {line["n"]} 句第 {take} 遍没有念出来：{error}', flush=True)
            if failures >= max(3, len(wanted) // 4):
                raise SystemExit('多半的句子都念不出来：看上面的原因，改好后再运行同一条命令，做完的部分不会重做')
            continue
        path = folder / f'{line["n"]:03d}-{take}.wav'
        for old in (path, path.with_suffix('.json'), path.with_suffix('.heard.json')):
            old.unlink(missing_ok=True)
        write_wav(path, samples)
        facts = {**measure(samples), 'pace': round(line['units'] / (len(samples) / RATE), 2), 'same_voice': 1.0, 'n': line['n'], 'say': line['say'],
                 'signature': signature()}
        facts['speaking'] = round(facts['pace'] / (1 - facts['pauses']), 2)
        path.with_suffix('.json').write_text(json.dumps(facts, ensure_ascii=False), encoding='utf-8')
        print(f'[{done}/{len(wanted)}] {line["n"]:03d}-{take} ' + json.dumps({key: value for key, value in facts.items() if key not in ('say', 'n', 'signature')}, ensure_ascii=False), flush=True)


# ---------- step 2: which reference clip (Qwen) ----------
def wanted_pace(script):
    """The pace the narration should have, and what the captions of this video ask for: the first, or the second where that is more."""
    needed = float(np.median([line['units'] / max(0.3, line['window'] - cfg.lead - cfg.gap) for line in script]))
    return max(cfg.pace, needed), needed


def usual(row, rows):
    """Is this clip in the voice the speaker usually has? The model's speaker does not come out as the same voice every time:
    some clips are in another voice altogether. Told by the speaker model (how close a clip is to most of the others); without it, by the pitch."""
    if 'voice' in row:
        return row['voice'] >= SAME
    middle = float(np.median([other['pitch'] for other in rows if other['pitch'] > 0] or [1.0]))
    return row['pitch'] > 0 and abs(12 * math.log2(row['pitch'] / middle)) <= 3


def shortlist(rows, target, count=4):
    """A few clips to try: of those that say the text right in the speaker's usual voice and are not faster than the pace wanted
    (what is spoken after a clip comes out faster than the clip itself), the one that moves least in pitch at each of the paces there are."""
    right = sorted([row for row in rows if not row.get('wrong') and row.get('longest_pause', 0) <= 1.1 and usual(row, rows)] or rows, key=lambda row: row['pace'])
    slow = [row for row in right if row['pace'] <= target]
    right = slow if len(slow) >= count else right[:count]
    low, step = right[0]['pace'], (right[-1]['pace'] - right[0]['pace']) / count or 1.0
    groups = [[row for row in right if min(count - 1, int((row['pace'] - low) / step)) == i] for i in range(count)]
    return [min(group, key=lambda row: row['pitch_moves']) for group in groups if group]


def trial_lines(script):
    """The lines a reference clip is tried on: the three with the least time for what they say, and three ordinary ones."""
    needs = lambda line: line['units'] / max(0.3, line['window'] - cfg.lead - cfg.gap)
    order = sorted([line for line in script if line['units'] >= 8] or script, key=needs)
    middle = len(order) // 2
    return sorted({line['n']: line for line in order[-3:] + order[max(0, middle - 1):middle + 2]}.values(), key=lambda line: line['n'])


def trial(per=2):
    """Lines spoken after one reference clip come out faster than the clip itself, and by how much is not known before it is tried."""
    folder, data = cfg.folder / 'trial', known()
    folder.mkdir(parents=True, exist_ok=True)
    script = lines()[0]
    wanted = [(row, line, take) for row in shortlist(data['rows'], wanted_pace(script)[0]) for line in trial_lines(script) for take in range(per)
              if not said_already(folder / f'{row["file"][:-4]}_{line["n"]:03d}-{take}.wav', line)]
    if not wanted:
        return
    model = load(need('tts_base', HOW))
    close = speaker(model)
    for done, (row, line, take) in enumerate(wanted, 1):
        name = f'{row["file"][:-4]}_{line["n"]:03d}-{take}'
        facts = clone(model, close, line, cfg.folder / 'anchor' / row['file'], data['text'], folder / f'{name}.wav', 7000 + 37 * line['n'] + take)
        if facts:
            print(f'[{done}/{len(wanted)}] {name} 语速 {facts["pace"]} 起伏 {facts["pitch_moves"]}', flush=True)


def fit(line, seconds):
    """How a clip of this length goes into the time its caption has: how much of the usual pauses around it has to go, and how much faster it has to be."""
    slack = line['window'] - seconds
    squeezed = min(1.0, max(0.0, (cfg.lead + cfg.gap - slack) / (cfg.lead + cfg.gap - cfg.lead_min - cfg.gap_min)))
    return squeezed, max(1.0, seconds / max(0.4, line['window'] - cfg.lead_min - cfg.gap_min))


def compare():
    """The trial in numbers: one row for each reference clip that was tried, the best first."""
    script = {line['n']: line for line in lines()[0]}
    known_rows = {row['file'][:-4]: row for row in known()['rows']}
    target, needed = wanted_pace(list(script.values()))
    rows = []
    for name in sorted({path.stem.partition('_')[0] for path in (cfg.folder / 'trial').glob('*.wav')}):
        clips = []
        for path in sorted((cfg.folder / 'trial').glob(f'{name}_*.wav')):
            facts = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
            line = script.get(facts.get('n'))
            if line and line['say'] == facts['say'] and path.with_suffix('.heard.json').is_file():
                squeezed, faster = fit(line, facts['seconds'])
                clips.append({**facts, **heard(path), 'squeezed': squeezed, 'faster': faster})
        if not clips or name not in known_rows:
            continue
        median, mean = (lambda key: float(np.median([clip[key] for clip in clips]))), (lambda key: float(np.mean([clip[key] for clip in clips])))
        row = {'candidate': name, 'own_pace': known_rows[name]['pace'], 'clips': len(clips), 'wrong': round(mean('wrong'), 4), 'squeezed': round(mean('squeezed'), 3),
               'faster': round(max(clip['faster'] for clip in clips), 3), 'sped_up': sum(clip['faster'] > 1.001 for clip in clips), 'pace': round(median('pace'), 2),
               'speaking': round(median('speaking'), 2), 'pitch': round(median('pitch'), 1), 'pitch_moves': round(median('pitch_moves'), 2),
               'voice': round(median('voice'), 3) if all('voice' in clip for clip in clips) else None}
        row['cost'] = round(40 * row['wrong'] + 2 * row['squeezed'] + float(np.mean([25 * (clip['faster'] - 1) + 100 * max(0.0, clip['faster'] - cfg.fastest) for clip in clips]))
                            + 3 * abs(math.log(row['pace'] / target)) + 0.6 * row['pitch_moves'] + (8 * (1 - row['voice']) if row['voice'] is not None else 0.0), 3)
        rows.append(row)
    rows.sort(key=lambda row: row['cost'])
    if not rows:
        raise SystemExit('试念没有结果：demo_voice.py trial')
    (cfg.folder / 'trial.json').write_text(json.dumps({'pace_wanted': round(target, 2), 'lines': sorted({clip_n for clip_n in script if list((cfg.folder / 'trial').glob(f'*_{clip_n:03d}-*.wav'))}), 'rows': rows},
                                                      ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'想要的语速 {target:.2f} {cfg.unit}/秒（字幕留出的时间折合 {needed:.2f}）', flush=True)
    for row in rows:
        print(f'{row["candidate"]:>5s}  自身语速 {row["own_pace"]:.2f} → 念出来 {row["pace"]:.2f} {cfg.unit}/秒（净 {row["speaking"]:.2f}）  要加快的 {row["sped_up"]}/{row["clips"]}（最多 {row["faster"]:.3f} 倍）  '
              f'起伏 {row["pitch_moves"]:.2f}  念错 {row["wrong"]:.3f}  同声 {row["voice"]}  代价 {row["cost"]}', flush=True)
    return rows


# ---------- step 3: every line, several times ----------
def takes(count, only=None):
    if cfg.engine != 'qwen':
        return plain_takes(count, only)
    reference = json.loads((cfg.folder / 'anchor.json').read_text(encoding='utf-8'))
    folder = cfg.folder / 'takes'
    folder.mkdir(parents=True, exist_ok=True)
    wanted = [(line, take) for line in lines()[0] if not only or line['n'] in only for take in range(count) if not said_already(folder / f'{line["n"]:03d}-{take}.wav', line)]
    if not wanted:
        return
    model = load(need('tts_base', HOW))
    close = speaker(model)
    for done, (line, take) in enumerate(wanted, 1):
        facts = clone(model, close, line, cfg.folder / 'anchor.wav', reference['text'], folder / f'{line["n"]:03d}-{take}.wav', 7000 + 37 * line['n'] + take)
        if facts:
            print(f'[{done}/{len(wanted)}] {line["n"]:03d}-{take} ' + json.dumps({key: value for key, value in facts.items() if key not in ('say', 'n', 'signature')}, ensure_ascii=False), flush=True)


# ---------- step 4: what was said, and in whose voice ----------
def voice_print():
    """Turns a clip into what tells one speaker from another (a speaker-verification model, not the speech model's own measure); None where it is not installed."""
    model_file = where('voiceprint')
    if not model_file or importlib.util.find_spec('sherpa_onnx') is None:
        return None
    import sherpa_onnx
    model = sherpa_onnx.SpeakerEmbeddingExtractor(sherpa_onnx.SpeakerEmbeddingExtractorConfig(model=str(model_file), num_threads=4, provider='cpu'))

    def of(path):
        samples = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout, dtype='<f4')
        stream = model.create_stream()
        stream.accept_waveform(sample_rate=16000, waveform=samples)
        stream.input_finished()
        vector = np.array(model.compute(stream), dtype=np.float64)
        return vector / np.linalg.norm(vector)
    return of


def told(path, script):
    """What a clip was to say and the clip whose voice it should have, by the folder it is in. No text: the line is gone."""
    if path.parent.name == 'anchor':
        return anchor_text(), None
    if path.parent.name == 'trial':
        name, _, rest = path.stem.partition('_')
        return script.get(int(rest[:3])), cfg.folder / 'anchor' / f'{name}.wav'
    return script.get(int(path.stem[:3])), cfg.folder / 'anchor.wav'   # takes and the clips cut from the finished file carry the number of their line


def as_heard(path):
    """A clip the way the recogniser takes it: one channel, 16000 samples a second (read here, so that nothing depends on how the recogniser opens files)."""
    import soxr
    samples, rate = read_wav(path)
    samples = samples.mean(axis=1) if samples.ndim == 2 else samples
    return np.ascontiguousarray(samples if rate == 16000 else soxr.resample(samples, rate, 16000, quality='HQ'), dtype=np.float32)


WHISPER_PROMPTS = {'zh': '以下是普通话的句子，介绍{title}。', 'en': 'This is a narration that introduces {title}.', 'ja': 'これは{title}の機能紹介です。',
                   'ko': '이것은 {title} 기능 소개입니다.', 'de': 'Dies ist eine Vorstellung von {title}.', 'fr': 'Ceci présente {title}.',
                   'es': 'Esto presenta {title}.', 'it': 'Questa è una presentazione di {title}.', 'pt': 'Esta é uma apresentação de {title}.',
                   'ru': 'Это презентация {title}.'}


def hear(files):
    """Writes next to each clip what is heard in it, how much of what was to be said differs, and how close the voice is to its reference clip."""
    files = [Path(path) for path in files if not Path(path).with_suffix('.heard.json').is_file()]
    if not files:
        return
    from faster_whisper import WhisperModel
    whisper = str(need('whisper', f'python3 {HERE / "demo_env.py"} setup --models'))
    try:
        model = WhisperModel(whisper, device='cuda', compute_type='float16')
        list(model.transcribe(np.zeros(16000, dtype=np.float32), language=cfg.tongue)[0])
    except Exception:
        model = WhisperModel(whisper, device='cpu', compute_type='int8', cpu_threads=8)
    script = {line['n']: line['say'] for line in lines()[0]}
    prompt = WHISPER_PROMPTS.get(cfg.tongue, '{title}').format(title=cfg.title or 'an app')
    print_of, prints = voice_print(), {}
    for path in files:
        said, reference = told(path, script)
        if not said:
            continue
        parts, _ = model.transcribe(as_heard(path), language=cfg.tongue, beam_size=5, temperature=0.0, condition_on_previous_text=False, initial_prompt=prompt)
        text = ''.join(part.text for part in parts).strip()
        differs, total = demo_text.differs(said, text, cfg.tongue, cfg.say)
        facts = {'heard': text, 'differs': differs, 'wrong': round(differs / max(1, total), 4)}
        if print_of and reference and reference.is_file():
            if reference not in prints:
                prints[reference] = print_of(reference)
            facts['voice'] = round(float(print_of(path) @ prints[reference]), 3)
        path.with_suffix('.heard.json').write_text(json.dumps(facts, ensure_ascii=False), encoding='utf-8')
    if print_of and any(path.parent.name == 'anchor' for path in files):  # the reference clips against each other: which of them are in the voice most of them have
        made = [path for path in clips('anchor') if path.with_suffix('.heard.json').is_file()]
        prints = np.stack([print_of(path) for path in made])
        for path, close in zip(made, prints @ prints.T):
            facts = {**heard(path), 'voice': round(float(np.median(np.sort(close)[:-1])), 3)}
            path.with_suffix('.heard.json').write_text(json.dumps(facts, ensure_ascii=False), encoding='utf-8')


def heard(path):
    """What the recogniser wrote for a clip, and how much of the line differs."""
    return json.loads(path.with_suffix('.heard.json').read_text(encoding='utf-8'))


# ---------- step 5: choose, fit, level, mix ----------
def table(script):
    """Every take of every line that says what the caption says now, with what was measured and heard of it."""
    out = {}
    for line in script:
        for path in sorted((cfg.folder / 'takes').glob(f'{line["n"]:03d}-*.wav')):
            if said_already(path, line) and path.with_suffix('.heard.json').is_file():
                out.setdefault(line['n'], []).append((path, {**json.loads(path.with_suffix('.json').read_text(encoding='utf-8')), **heard(path)}))
    return out


def choose(script):
    """For each line, of the takes that say the text, the one that fits its caption and is closest to all the others in pace and pitch."""
    rows_of = table(script)
    right = [facts for rows in rows_of.values() for _, facts in rows if facts['wrong'] <= 0.05]
    if not right:
        raise SystemExit('没有一句录音念对了：听一下 voice/takes 里的文件，看 demo_voice.py lines 里的念法')
    typical = {key: float(np.median([facts[key] for facts in right])) for key in ('speaking', 'pace', 'pitch', 'pitch_moves')}
    chosen = {}
    for line in script:
        rows = rows_of.get(line['n'], [])
        if not rows:
            raise SystemExit(f'第 {line["n"]} 句没有录音：demo_voice.py takes，再 demo_voice.py hear')
        least = min(facts['wrong'] for _, facts in rows)

        def cost(facts):
            squeezed, faster = fit(line, facts['seconds'])
            return (2 * squeezed + 25 * (faster - 1) + 100 * max(0.0, faster - cfg.fastest)
                    + 3 * abs(math.log(facts['speaking'] / typical['speaking']))
                    + 0.25 * abs(12 * math.log2(facts['pitch'] / typical['pitch']))
                    + 0.6 * max(0.0, facts['pitch_moves'] - typical['pitch_moves'])
                    + (8 * (1 - facts['voice']) if 'voice' in facts else 30 * (1 - facts['same_voice']))
                    + 3 * max(0.0, facts['longest_pause'] - 0.8))
        path, facts = min((row for row in rows if row[1]['wrong'] <= least + 1e-9), key=lambda row: cost(row[1]))  # what is said comes first
        chosen[line['n']] = (path, {**facts, 'of': len(rows), 'as_right': sum(other['wrong'] <= least + 1e-9 for _, other in rows)})
    return chosen, typical


def seconds_of(path, stream='v:0'):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', stream, '-show_entries', 'stream=duration', '-of', 'csv=p=0', str(path)], capture_output=True, text=True, check=True).stdout
    return float(out.split()[0].strip(','))


def whole_of(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)], capture_output=True, text=True, check=True).stdout)


def loudness(source, rate=48000):
    """Loudness (LUFS), its range and the highest peak (dB) of a file or of samples."""
    if isinstance(source, np.ndarray):
        text = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-f', 'f32le', '-ar', str(rate), '-ac', str(source.shape[1] if source.ndim == 2 else 1), '-i', 'pipe:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                              input=source.astype('<f4').tobytes(), capture_output=True).stderr.decode('utf-8', 'replace')
    else:
        text = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(source), '-map', '0:a:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    text = text[text.rindex('Summary:'):]
    return {'lufs': float(re.search(r'I:\s*(-?[\d.]+) LUFS', text)[1]), 'range': float(re.search(r'LRA:\s*(-?[\d.]+) LU', text)[1]), 'peak': float(re.search(r'Peak:\s*(-?[\d.]+) dBFS', text)[1])}


def limit(samples, rate, ceiling, reach=0.012):
    """Peaks above the ceiling are turned down, gently: the gain goes down before a peak and comes back after it, over a few hundredths of a second."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    width = 2 * round(reach * rate) + 1
    gain = minimum_filter1d(np.minimum(1.0, ceiling / np.maximum(np.abs(samples), 1e-9)), size=2 * width, mode='nearest')
    gain = uniform_filter1d(uniform_filter1d(gain, size=width, mode='nearest'), size=width, mode='nearest')
    return (samples * gain).astype(np.float32), gain


def the_video():
    """The video the narration goes under: the whole one drawn from this timeline."""
    if not cfg.video or not cfg.video.is_file():
        raise SystemExit('没有要配音的视频：先渲染整片（demo_render.py --work … --out …），或用 --video 指明')
    length = seconds_of(cfg.video)
    if abs(length - cfg.timeline['duration']) > 0.5:
        raise SystemExit(f'{cfg.video} 长 {length:.1f} 秒，时间线是 {cfg.timeline["duration"]:.1f} 秒：这个视频不是按这份时间线渲染的整片')
    return length


def build():
    import soxr
    script, _ = lines()
    length = the_video() - 0.02  # never longer than the picture
    chosen, typical = choose(script)
    track = np.zeros(int(length * RATE), dtype=np.float32)
    report = []
    for line in script:
        path, facts = chosen[line['n']]
        samples, _ = read_wav(path)
        room = max(0.4, line['window'] - cfg.lead_min - cfg.gap_min)
        slack, faster = line['window'] - len(samples) / RATE, 1.0
        if slack >= cfg.lead + cfg.gap:
            lead = cfg.lead
        elif slack >= cfg.lead_min + cfg.gap_min:  # tight: first the pauses around the line give way
            lead = cfg.lead_min + (slack - cfg.lead_min - cfg.gap_min) * (cfg.lead - cfg.lead_min) / (cfg.lead + cfg.gap - cfg.lead_min - cfg.gap_min)
        else:                                      # then the pace
            lead, faster = cfg.lead_min, len(samples) / RATE / room
            samples = tempo(samples, faster)[:int(room * RATE)]
        samples = samples[:max(0, len(track) - round((line['start'] + lead) * RATE))]
        report.append({'n': line['n'], 'take': path.stem, 'takes': facts['of'], 'as_right': facts['as_right'], 'caption': round(line['start'], 2), 'window': round(line['window'], 2),
                       'start': round(line['start'] + lead, 3), 'seconds': round(len(samples) / RATE, 3), 'after': round(line['window'] - lead - len(samples) / RATE, 3),
                       'faster': round(faster, 3), 'pace': round(line['units'] / (len(samples) / RATE), 2), 'speaking': round(facts['speaking'] * faster, 2),
                       'pitch': facts['pitch'], 'pitch_moves': facts['pitch_moves'], 'same_voice': facts.get('voice', facts['same_voice']), 'longest_pause': facts['longest_pause'],
                       'level': loudness(samples, RATE)['lufs'], 'wrong': round(facts['wrong'], 3), 'say': line['say'], 'heard': facts['heard'], 'samples': samples})
    middle = float(np.median([row['level'] for row in report]))
    fade = round(0.008 * RATE)
    for row in report:
        samples = row.pop('samples') * 10 ** (max(-6.0, min(6.0, middle - row['level'])) / 20)  # every line as loud as every other
        samples[:fade] *= np.linspace(0, 1, fade)
        samples[-fade:] *= np.linspace(1, 0, fade)
        begin = round(row['start'] * RATE)
        track[begin:begin + len(samples)] = samples
    side = soxr.resample(track, RATE, 48000, quality='VHQ').astype(np.float32)  # the file is stereo, with the same in both channels
    both = lambda samples: np.stack([samples, samples], axis=1)
    before = loudness(both(side))
    side *= 10 ** ((cfg.loudness - before['lufs']) / 20)  # one gain for the whole narration
    ceiling, plain = 10 ** (cfg.peak / 20), side
    for again in range(4):  # only if a peak would go over the ceiling: the highest peaks give way, the rest is left as it is
        side, _ = limit(side, 48000, ceiling)
        after = loudness(both(side))
        if abs(after['lufs'] - cfg.loudness) < 0.05 or again == 3:
            break
        side = side * 10 ** ((cfg.loudness - after['lufs']) / 20)
    held = 20 * np.log10(np.maximum(np.abs(side), 1e-9) / np.maximum(np.abs(plain), 1e-9))[np.abs(plain) > 1e-4]
    peaks = {'most': round(float(max(0.0, -held.min())), 2), 'share_of_speech': round(float((held < -0.1).mean()), 4)}  # how far the highest peak was turned down, and how much of the speech was touched at all
    write_wav(cfg.folder / 'voice.wav', both(side), 48000)
    cfg.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(cfg.video), '-i', str(cfg.folder / 'voice.wav'), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(cfg.out)], check=True)
    reference = json.loads((cfg.folder / 'anchor.json').read_text(encoding='utf-8'))
    (cfg.folder / 'report.json').write_text(json.dumps({'video': str(cfg.video), 'out': str(cfg.out), 'engine': cfg.engine, 'speaker': cfg.speaker, 'language': cfg.tongue,
                                                        'reference': reference.get('file'), 'typical': typical, 'loudness': after,
                                                        'gain': round(cfg.loudness - before['lufs'], 2), 'peaks_turned_down': peaks, 'lines': report}, ensure_ascii=False, indent=1), encoding='utf-8')
    return report, typical, after


# ---------- step 6: the finished file, in numbers ----------
def packets(path):
    """What identifies the picture: every video packet with its time stamps, unread and undecoded."""
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0', '-c', 'copy', '-f', 'framemd5', '-'], capture_output=True, check=True).stdout
    return hashlib.md5(out).hexdigest(), out.count(b'\n0,')


def sound_of(path, rate):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0', '-ar', str(rate), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, dtype='<f4').reshape(-1, 2)


def check():
    the_video()
    script, _ = lines()
    report = {row['n']: row for row in json.loads((cfg.folder / 'report.json').read_text(encoding='utf-8'))['lines']}
    problems, facts = [], {}
    silent, dubbed = packets(cfg.video), packets(cfg.out)
    before, whole = whole_of(cfg.video), whole_of(cfg.out)
    facts['画面'] = {'逐包相同': silent == dubbed, '帧数': dubbed[1], '无声版时长': seconds_of(cfg.video), '配音版时长': seconds_of(cfg.out), '配音版声音时长': seconds_of(cfg.out, 'a:0'),
                   '无声版文件时长': before, '配音版文件时长': whole}
    if silent != dubbed:
        problems.append('画面和无声版不是逐包相同')
    if abs(whole - before) > 0.001:
        problems.append(f'文件时长变了：{before} → {whole}')
    sound = sound_of(cfg.out, RATE)
    facts['画面']['两声道相差'] = round(float(np.abs(sound[:, 0] - sound[:, 1]).max()), 5)
    sound = sound[:, 0]
    hop = RATE // 100
    levels = np.sqrt((sound[:len(sound) // hop * hop].reshape(-1, hop) ** 2).mean(axis=1))
    loud = levels > 0.004
    spoken_frames = np.zeros(len(levels), dtype=bool)
    folder = cfg.folder / 'final'
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    rows = []
    for line in script:
        planned = report.get(line['n'])
        if not planned or planned['say'] != line['say']:
            problems.append(f'第 {line["n"]} 句的字幕在混音之后改过：重新 build')
            continue
        first, last = round(line['start'] * 100), min(len(levels), round((line['start'] + line['window']) * 100))
        inside = np.flatnonzero(loud[first:last])
        if not inside.size:
            problems.append(f'第 {line["n"]} 句的字幕时间里没有声音')
            continue
        begins, ends = line['start'] + inside[0] / 100, line['start'] + (inside[-1] + 1) / 100
        spoken_frames[first + inside[0]:first + inside[-1] + 1] = True
        row = {'n': line['n'], 'begins': round(begins - line['start'], 2), 'ends_before': round(line['start'] + line['window'] - ends, 2), 'seconds': round(ends - begins, 2),
               'pace': round(line['units'] / (ends - begins), 2), 'faster': planned['faster']}
        rows.append(row)
        if row['begins'] < cfg.lead_min - 0.03 or row['ends_before'] < cfg.gap_min - 0.03:
            problems.append(f'第 {line["n"]} 句贴着字幕的边：字幕出现后 {row["begins"]} 秒开口，下一条字幕前 {row["ends_before"]} 秒收住')
        if planned['faster'] > cfg.fastest + 0.005:
            problems.append(f'第 {line["n"]} 句（{line["start"]:.1f} 秒）加快到 {planned["faster"]:.2f} 倍才放下，超过上限 {cfg.fastest}：改短这条字幕，或重录时让它多停一会儿')
        due = planned['start'], planned['start'] + planned['seconds']
        if not (due[0] - 0.03 <= begins <= due[0] + 0.2 and due[1] - 0.3 <= ends <= due[1] + 0.05):  # a soft first or last sound is under what counts as sound here
            problems.append(f'第 {line["n"]} 句在成片里的位置和安排的不一样：{begins:.2f}–{ends:.2f} 秒，安排 {due[0]:.2f}–{due[1]:.2f} 秒')
        clip = sound[max(0, round((begins - 0.2) * RATE)):round((ends + 0.3) * RATE)]
        row['lufs'] = loudness(np.stack([clip, clip], axis=1), RATE)['lufs']
        write_wav(folder / f'{line["n"]:03d}.wav', clip)
    stray = loud & ~spoken_frames
    if stray.any():
        problems.append(f'字幕之外有声音：{np.flatnonzero(stray)[0] / 100:.2f} 秒处')
    run('hear', *sorted(folder.glob('*.wav')), python=sys.executable)
    by_number, misheard = {line['n']: line for line in script}, []
    for row in rows:
        line = by_number[row['n']]
        row.update(heard(folder / f'{line["n"]:03d}.wav'))
        if row['differs']:
            misheard.append({'n': line['n'], 'at': round(line['start'], 1), 'say': line['say'], 'heard': row['heard'], 'differs': row['differs']})
    facts['声音'] = loudness(cfg.out)
    from scipy.signal import correlate
    mixed, in_file = read_wav(cfg.folder / 'voice.wav')[0][:, 0], sound_of(cfg.out, 48000)[:, 0]
    reach = 4800
    first = max(reach, round(script[0]['start'] * 48000))
    span = min(30 * 48000, len(mixed) - first, len(in_file) - first - reach)
    match = correlate(in_file[first - reach:first + span + reach], mixed[first:first + span], mode='valid', method='fft')
    facts['声音']['比混音轨晚（毫秒）'] = round((int(np.argmax(match)) - reach) / 48, 2)  # the sound in the file against the track that went in: the encoder must not have shifted it
    common = min(len(mixed), len(in_file))
    facts['声音']['与混音轨的相关'] = round(float(np.corrcoef(mixed[:common], in_file[:common])[0, 1]), 4)
    if abs(facts['声音']['比混音轨晚（毫秒）']) > 5 or facts['声音']['与混音轨的相关'] < 0.98:
        problems.append('成片里的声音和混音轨对不上')
    if rows:
        spread = lambda key: [min(row[key] for row in rows), float(np.median([row[key] for row in rows])), max(row[key] for row in rows)]
        facts['句子'] = {'句数': len(rows), '听写逐音节一致': len(rows) - len(misheard), f'成片语速（{cfg.unit}/秒）': spread('pace'), '加快过的句数': sum(row['faster'] > 1.001 for row in rows),
                       '最多加快到': max(row['faster'] for row in rows), '开口距字幕出现（秒）': [min(row['begins'] for row in rows), max(row['begins'] for row in rows)],
                       '收住距下一条字幕（秒）最少': min(row['ends_before'] for row in rows), '各句响度（LUFS）': [min(row['lufs'] for row in rows), max(row['lufs'] for row in rows)]}
        if all('voice' in row for row in rows):
            facts['句子']['与参考音的声纹相似度'] = spread('voice')
            problems += [f'第 {row["n"]} 句的音色和参考音差得多（声纹相似度 {row["voice"]}）：demo_voice.py takes {row["n"]} 之前先删掉它在 voice/takes 里的录音' for row in rows if row['voice'] < SAME]
    (cfg.folder / 'check.json').write_text(json.dumps({'video': str(cfg.video), 'out': str(cfg.out), 'facts': facts, 'problems': problems, 'misheard': misheard, 'lines': rows}, ensure_ascii=False, indent=1), encoding='utf-8')
    return facts, problems, misheard


def show_check():
    facts, problems, misheard = check()
    print(json.dumps(facts, ensure_ascii=False, indent=1))
    for row in misheard:
        print(f'听写有出入 第 {row["n"]} 句（{row["at"]} 秒，差 {row["differs"]} 个{cfg.unit}）\n    稿：{row["say"]}\n    听：{row["heard"]}')
    print('\n'.join(problems) or '没有发现问题')


def show_build():
    report, typical, sound = build()
    print(json.dumps({**typical, 'engine': cfg.engine, 'speaker': cfg.speaker, **sound}, ensure_ascii=False))
    for row in report:
        print(f'{row["n"]:3d} {row["take"]} {row["start"]:7.2f} {row["seconds"]:5.2f}/{row["window"]:5.2f}s 加快 {row["faster"]:.3f} 语速 {row["pace"]:.2f} 净 {row["speaking"]:.2f} 音高 {row["pitch"]:5.1f} '
              f'起伏 {row["pitch_moves"]:.2f} 同声 {row["same_voice"]:.3f} 错 {row["wrong"]:.3f} 可选 {row["as_right"]}/{row["takes"]}')


# ---------- the steps in order ----------
def run(step, *arguments, python):
    """One step of this script as a program of its own: the speech model may have its own Python, and what a step loads onto the graphics card is gone when it ends."""
    quiet = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1', 'TOKENIZERS_PARALLELISM': 'false'}
    command = [str(python), __file__, step, *(str(argument) for argument in arguments), '--work', str(cfg.work)]
    command += (['--video', str(cfg.video)] if cfg.video else []) + (['--out', str(cfg.out)] if cfg.out else [])
    if subprocess.run(command, env=quiet).returncode:
        raise SystemExit(f'这一步没有做成：{step}')


def clips(folder):
    return sorted((cfg.folder / folder).glob('*.wav'))


def everything(speaks):
    the_video()
    if not lines()[0]:
        raise SystemExit('时间线里没有要念的字幕')
    qwen = cfg.engine == 'qwen'
    print(f'配音：{demo_tts.ENGINES[cfg.engine]["name"]}（{demo_tts.ENGINES[cfg.engine]["place"]}），{demo_text.LANGUAGES[cfg.tongue]["name"]}，音色 {cfg.speaker}', flush=True)
    show_lines()
    chosen = cfg.folder / 'anchor.json'
    runner = speaks() if qwen else sys.executable
    if qwen:
        if cfg.anchor and chosen.is_file() and json.loads(chosen.read_text(encoding='utf-8')).get('file') != f'{cfg.anchor}.wav':
            take_anchor(cfg.anchor)
        if not chosen.is_file():
            run('_candidates', python=runner)
            run('hear', *clips('anchor'), python=sys.executable)
            if cfg.anchor:
                take_anchor(cfg.anchor)
            else:
                run('_trial', python=runner)
                run('hear', *clips('trial'), python=sys.executable)
                take_anchor(compare()[0]['candidate'])
    elif not chosen.is_file() or json.loads(chosen.read_text(encoding='utf-8')).get('signature') != signature():
        run('_anchor_plain', python=runner)
        run('hear', *clips('anchor'), python=sys.executable)
    run('_takes', cfg.takes, python=runner)
    run('hear', *clips('takes'), python=sys.executable)
    script = lines()[0]
    again = [line['n'] for line in script if min((facts['wrong'] for _, facts in table(script).get(line['n'], [])), default=1) > 0]
    if again:  # no take of these says the text right: once more, as many times again
        print(f'没有一遍念对的句子：{again}，各再念 {cfg.takes} 遍', flush=True)
        run('_takes', 2 * cfg.takes, *again, python=runner)
        run('hear', *clips('takes'), python=sys.executable)
    show_build()
    show_check()
    reference = json.loads(chosen.read_text(encoding='utf-8'))
    print(f'\n配音版：{cfg.out}\n参考音：{reference.get("file") or reference.get("speaker")}（{cfg.folder / "anchor.wav"}），引擎 {cfg.engine}，音色 {cfg.speaker}，语言 {cfg.tongue}\n'
          f'每句取了哪一遍、怎么放的：{cfg.folder / "report.json"}；核验：{cfg.folder / "check.json"}；成片里切出来的每一句：{cfg.folder / "final"}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('step', nargs='?', default='all', metavar='step', choices=['all', 'lines', 'anchor', 'trial', 'takes', 'hear', 'build', 'check', '_candidates', '_trial', '_takes', '_anchor_plain'],
                        help='all (default), lines, anchor [name], trial, takes [line numbers], hear [files], build, check')
    parser.add_argument('rest', nargs='*')
    parser.add_argument('--work', type=Path, required=True, help='the working folder of the recording')
    parser.add_argument('--video', type=Path, help='the video to narrate (default: the one demo_render.py wrote last)')
    parser.add_argument('--out', type=Path, help='the narrated video (default: next to the video, its name with -配音版 / -narrated)')
    options = parser.parse_args()
    inner = options.step.startswith('_')
    if not inner and any(importlib.util.find_spec(module) is None for module in ('soundfile', 'soxr', 'scipy', 'faster_whisper', 'pypinyin')):
        own = where('python')  # started with some other Python: go on with the skill's own
        if not own or Path(sys.prefix).resolve() == Path(own).parent.parent.resolve():
            raise SystemExit(f'缺混音和听写用的包。{HOW}')
        os.execv(str(own), [str(own), __file__, *sys.argv[1:]])
    configure(options.work.resolve(), options.video.resolve() if options.video else None, options.out.resolve() if options.out else None)
    cfg.folder.mkdir(parents=True, exist_ok=True)
    speaks = lambda: need('tts_python', HOW)
    if options.step == 'lines':
        show_lines()
    elif options.step == 'anchor':
        if cfg.engine != 'qwen':
            plain_anchor()
            run('hear', *clips('anchor'), python=sys.executable)
        elif options.rest:
            take_anchor(options.rest[0])
        else:
            run('_candidates', python=speaks())
            run('hear', *clips('anchor'), python=sys.executable)
            for row in sorted(known()['rows'], key=lambda row: row['pace']):
                print(f'{row["file"][:-4]:>5s}  语速 {row["pace"]:.2f} {cfg.unit}/秒  音高 {row["pitch"]:5.1f} Hz  起伏 {row["pitch_moves"]:.2f}  最长停顿 {row["longest_pause"]:.2f}s  念错 {row.get("wrong", "?")}  '
                      f'与多数候选的声纹相似度 {row.get("voice", "?")}' + ('' if usual(row, known()['rows']) else '  ← 不是通常的音色'))
    elif options.step == 'trial':
        if cfg.engine != 'qwen':
            raise SystemExit('试念只在 Qwen 上有：别的引擎用固定的音色，不需要挑参考音')
        run('hear', *clips('anchor'), python=sys.executable)
        run('_trial', python=speaks())
        run('hear', *clips('trial'), python=sys.executable)
        print(f'代价最小的排在最前：demo_voice.py anchor {compare()[0]["candidate"]} --work …')
    elif options.step == 'takes':
        run('_takes', cfg.takes, *options.rest, python=speaks() if cfg.engine == 'qwen' else sys.executable)
    elif options.step == 'hear':
        hear(options.rest or clips('takes'))
    elif options.step == 'build':
        show_build()
    elif options.step == 'check':
        show_check()
    elif options.step == '_candidates':
        candidates()
    elif options.step == '_trial':
        trial()
    elif options.step == '_takes':
        takes(int(options.rest[0]), [int(number) for number in options.rest[1:]] or None)
    elif options.step == '_anchor_plain':
        plain_anchor()
    else:
        everything(speaks)
