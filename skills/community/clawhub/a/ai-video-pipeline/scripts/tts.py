"""火山播客API TTS (Action 3 单人模式)"""
import os, json, uuid, struct, asyncio
import websockets


# ============================================================
# 帧协议 (火山播客API WebSocket)
# ============================================================
def _build_frame(event_type, payload, session_id=""):
    frame = struct.pack('>BBBB', 0x11, 0x14, 0x10, 0x00)
    frame += struct.pack('>I', event_type)
    frame += struct.pack('>I', len(session_id))
    frame += session_id.encode()
    frame += struct.pack('>I', len(payload))
    frame += payload
    return frame

def _parse_frame(data):
    if len(data) < 8:
        return data[0] if data else 0, 0, "", data
    byte1 = data[1]
    flags = byte1 & 0x0F
    has_event = bool(flags & 0x04)
    pos = 4
    event_type = 0
    if has_event and pos + 4 <= len(data):
        event_type = struct.unpack('>I', data[pos:pos+4])[0]
        pos += 4
    session_id = ""
    if pos + 4 <= len(data):
        sid_len = struct.unpack('>I', data[pos:pos+4])[0]
        pos += 4
        if sid_len > 0 and pos + sid_len <= len(data):
            session_id = data[pos:pos+sid_len].decode('utf-8', errors='replace')
            pos += sid_len
    if pos + 4 <= len(data):
        payload_len = struct.unpack('>I', data[pos:pos+4])[0]
        pos += 4
        payload = data[pos:pos+payload_len]
    else:
        payload = data[pos:]
    return byte1, event_type, session_id, payload

def _strip_id3(data):
    if data[:3] != b'ID3' or len(data) < 10:
        return b'', data
    tag_bytes = data[6:10]
    id3_size = 10 + ((tag_bytes[0] << 21) | (tag_bytes[1] << 14) | (tag_bytes[2] << 7) | tag_bytes[3])
    return data[:id3_size], data[id3_size:]


# ============================================================
# WebSocket TTS
# ============================================================
async def _podcast_tts_async(paragraphs, output_audio, voice, work_dir, verbose=True):
    app_id = os.environ.get("VOLC_APP_ID", "")
    access_key = os.environ.get("VOLC_ACCESS_KEY", "")
    wss_url = "wss://openspeech.bytedance.com/api/v3/sami/podcasttts"

    if not app_id or not access_key:
        raise ValueError("环境变量 VOLC_APP_ID 和 VOLC_ACCESS_KEY 未设置\n"
                         "请在 ~/.config/openclaw/gateway.env 中配置")

    sid = uuid.uuid4().hex[:12]
    headers = {
        "X-Api-App-Id": app_id,
        "X-Api-Access-Key": access_key,
        "X-Api-Resource-Id": "volc.service_type.10050",
        "X-Api-App-Key": os.environ.get("VOLC_APP_KEY", ""),
        "X-Api-Request-Id": str(uuid.uuid4()),
    }

    nlp_texts = [{"speaker": voice, "text": p} for p in paragraphs]
    payload = json.dumps({
        "action": 3,
        "use_head_music": False,
        "audio_config": {"format": "mp3", "sample_rate": 24000},
        "nlp_texts": nlp_texts,
    }).encode()

    frame = _build_frame(100, payload, sid)
    id3_tag = bytearray()
    mp3_frames = bytearray()
    rounds_info = []
    total_tokens = 0

    recv_timeout = 30
    async with websockets.connect(wss_url, additional_headers=headers, max_size=10*1024*1024) as ws:
        await ws.send(frame)
        while True:
            try:
                data = await asyncio.wait_for(ws.recv(), timeout=recv_timeout)
            except asyncio.TimeoutError:
                break
            except websockets.exceptions.ConnectionClosed:
                break
            if not isinstance(data, bytes) or len(data) < 4:
                continue
            byte1, evt, rsid, pd = _parse_frame(data)
            if byte1 == 0x94:
                try:
                    j = json.loads(pd)
                except:
                    continue
                if evt == 360:
                    rounds_info.append((j.get("round_id"), j.get("speaker", ""), j.get("text", ""), 0))
                elif evt == 362:
                    dur = j.get("audio_duration", 0)
                    if rounds_info:
                        rounds_info[-1] = (*rounds_info[-1][:3], dur)
                elif evt == 154:
                    total_tokens = j.get("usage", {}).get("total_tokens", 0)
                    recv_timeout = 5
                elif evt == 363:
                    break
                elif evt == 152:
                    break
            elif byte1 == 0xb4:
                tag, audio = _strip_id3(pd)
                if tag and not id3_tag:
                    id3_tag.extend(tag)
                mp3_frames.extend(audio)

    if mp3_frames:
        with open(output_audio, 'wb') as f:
            if id3_tag: f.write(id3_tag)
            f.write(mp3_frames)

    subs = []
    current_time = 0.3
    for rid, spk, txt, dur in rounds_info:
        if dur > 0:
            subs.append({"text": txt, "start": current_time, "end": current_time + dur})
            current_time += dur + 0.2
        else:
            subs.append({"text": txt, "start": current_time, "end": current_time + 3.0})
            current_time += 3.2

    return subs, total_tokens


def generate_tts(script, output_audio, voice="zh_male_dayixiansheng_v2_saturn_bigtts",
                 work_dir="/tmp/video-poc", verbose=True, skip_if_exists=False):
    """火山播客API Action 3 单人模式 → 返回字幕时间轴

    Args:
        skip_if_exists: 若 voice.mp3 + subs.json 都存在，直接加载缓存跳过 TTS
    """
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(os.path.dirname(output_audio) or ".", exist_ok=True)
    subs_json_path = os.path.join(work_dir, "subs.json")

    # 缓存: 跳过 TTS
    if skip_if_exists and os.path.exists(output_audio) and os.path.exists(subs_json_path):
        try:
            with open(subs_json_path, 'r', encoding='utf-8') as f:
                cached_subs = json.load(f)
            if cached_subs and isinstance(cached_subs, list):
                total_dur = sum(s["end"] - s["start"] for s in cached_subs)
                size_kb = os.path.getsize(output_audio) // 1024
                if verbose:
                    print(f"  ⏭️ 跳过 TTS (缓存): {output_audio} ({size_kb}KB, {total_dur:.1f}s)")
                return cached_subs
        except (json.JSONDecodeError, KeyError, TypeError):
            pass  # 缓存损坏，重新生成

    paragraphs = [p.strip() for p in script.split("\n\n") if p.strip()]
    if verbose:
        print(f"  🔊 播客API合成中 ({len(paragraphs)}段)...")
    subs, tokens = asyncio.run(_podcast_tts_async(paragraphs, output_audio, voice, work_dir, verbose))

    # 持久化 subs.json
    try:
        with open(subs_json_path, 'w', encoding='utf-8') as f:
            json.dump(subs, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 写入失败不影响主流程

    total_dur = sum(s["end"] - s["start"] for s in subs)
    size_kb = os.path.getsize(output_audio) // 1024
    if verbose:
        print(f"  ✅ 音频: {output_audio} ({size_kb}KB, {total_dur:.1f}s)")
        print(f"     字幕: {len(subs)}段, 消耗: {tokens} tokens")
    return subs
