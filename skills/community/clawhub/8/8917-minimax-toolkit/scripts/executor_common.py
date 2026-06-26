#!/usr/bin/env python3
"""
Common execution logic for MiniMax Toolkit modalities.

This module provides standardized execution patterns for all modalities,
reducing code duplication across individual scripts.
"""

import base64
import mimetypes
import os
import sys
import io
import tarfile
import requests
import time
from typing import Optional, Dict, Any


def _download_and_save(url: str, filepath: str) -> bool:
    """Download content from URL and save to filepath."""
    try:
        data = requests.get(url).content
        with open(filepath, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Download failed: {e}", file=sys.stderr)
        return False


def _file_to_data_url(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    mime = mime or "application/octet-stream"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def _upload_file(client, file_path: str, purpose: Optional[str] = None):
    data = {"purpose": purpose} if purpose else None
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        resp = requests.post(
            f"{client.base_url}/files/upload",
            headers={"Authorization": f"Bearer {client.api_key}"},
            data=data,
            files=files,
        )
    payload = resp.json()
    file_obj = payload.get("file") or payload.get("data") or {}
    return payload, file_obj.get("file_id")


def execute_image(client, prompt_or_text: str, model: str, project: Optional[str],
                  output_dir: Optional[str], estimate_only: bool,
                  extra_args: Dict[str, Any]) -> Dict[str, Any]:
    from minimax_client import get_standard_path

    print(client.get_budget_report(model))
    if estimate_only:
        return {"estimate_only": True}

    data = {
        "model": model,
        "prompt": prompt_or_text,
        "aspect_ratio": extra_args.get("ratio", "1:1"),
        "n": 1,
        "response_format": "url"
    }

    print(f"Generating image: {prompt_or_text}...")
    resp = client.post("image_generation", data)

    if resp.get("base_resp", {}).get("status_code") == 0:
        url = resp["data"]["image_urls"][0]
        target_dir, filename_base = get_standard_path("IMG", project=project,
                                                       prompt_slug=prompt_or_text,
                                                       output_dir=output_dir)
        filepath = os.path.join(target_dir, f"{filename_base}.jpg")
        if _download_and_save(url, filepath):
            client.print_saved_result(filepath, "Image", project=project)
            return {"filepath": filepath}
    return {"error": resp}


def execute_i2i(client, prompt_or_text: str, model: str, project: Optional[str],
                output_dir: Optional[str], estimate_only: bool,
                extra_args: Dict[str, Any]) -> Dict[str, Any]:
    """Official i2i now uses subject_reference with URL/Data URL."""
    from minimax_client import get_standard_path

    ref_path = extra_args.get("ref")
    if not ref_path:
        return {"error": "--ref is required for i2i"}

    print(client.get_budget_report(model))
    if estimate_only:
        return {"estimate_only": True}

    print(f"Preparing reference image: {ref_path}")
    image_file = _file_to_data_url(ref_path)
    data = {
        "model": model,
        "prompt": prompt_or_text,
        "aspect_ratio": extra_args.get("ratio", "1:1"),
        "response_format": "url",
        "subject_reference": [
            {"type": "character", "image_file": image_file}
        ]
    }

    print(f"Transforming: {prompt_or_text}...")
    resp = client.post("image_generation", data)
    if resp.get("base_resp", {}).get("status_code") == 0:
        url = resp["data"]["image_urls"][0]
        target_dir, filename_base = get_standard_path("IMG", project=project,
                                                       prompt_slug=prompt_or_text,
                                                       output_dir=output_dir)
        filepath = os.path.join(target_dir, f"{filename_base}.jpg")
        if _download_and_save(url, filepath):
            client.print_saved_result(filepath, "Image", project=project)
            return {"filepath": filepath}
    return {"error": resp}


def execute_video(client, prompt_or_text: str, model: str, project: Optional[str],
                  output_dir: Optional[str], estimate_only: bool,
                  extra_args: Dict[str, Any]) -> Dict[str, Any]:
    from minimax_client import get_standard_path

    print(client.get_budget_report(model))
    if estimate_only:
        return {"estimate_only": True}

    data = {
        "model": model,
        "prompt": prompt_or_text,
        "response_format": "url"
    }

    print(f"Creating video task: {prompt_or_text}...")
    print("⚠️ Video link expires in 9 hours - download immediately after completion!")
    resp = client.post("video_generation", data)
    if resp.get("base_resp", {}).get("status_code") != 0:
        return {"error": resp}

    task_id = resp.get("task_id")
    print(f"Task created! ID: {task_id}")
    print("Polling for completion (this may take minutes)...")

    while True:
        time.sleep(30)
        status_resp = client.get(f"query_video_generation?task_id={task_id}")
        if status_resp.get("base_resp", {}).get("status_code") != 0:
            return {"error": status_resp}
        file_id = status_resp.get("file_id")
        if file_id:
            video_url = status_resp.get("video_url")
            if video_url:
                target_dir, filename_base = get_standard_path("VID", project=project,
                                                               prompt_slug=prompt_or_text,
                                                               output_dir=output_dir)
                filepath = os.path.join(target_dir, f"{filename_base}.mp4")
                if _download_and_save(video_url, filepath):
                    client.print_saved_result(filepath, "Video", project=project)
                    return {"filepath": filepath}
            break
        print("Still processing...")
    return {"error": "Video generation failed or timed out"}


def execute_video_template(client, prompt_or_text: str, model: str, project: Optional[str],
                           output_dir: Optional[str], estimate_only: bool,
                           extra_args: Dict[str, Any]) -> Dict[str, Any]:
    from minimax_client import get_standard_path

    TEMPLATES = {
        "diving": {"id": "392753057216684038", "name": "跳水", "media_required": True, "text_required": False},
        "rings": {"id": "393881433990066176", "name": "吊环", "media_required": True, "text_required": False},
        "pubg": {"id": "393769180141805569", "name": "绝地求生", "media_required": True, "text_required": True},
        "labubu": {"id": "394246956137422856", "name": "万物皆可 labubu", "media_required": True, "text_required": False},
        "mcdonalds": {"id": "393879757702918151", "name": "麦当劳宠物外卖员", "media_required": True, "text_required": False},
        "tibetan": {"id": "393766210733957121", "name": "藏族风写真", "media_required": True, "text_required": False},
        "dead": {"id": "394125185182695432", "name": "生无可恋", "media_required": False, "text_required": True},
        "love_letter": {"id": "393857704283172864", "name": "情书写真", "media_required": True, "text_required": False},
        "female_model": {"id": "393866076583718914", "name": "女模特试穿广告", "media_required": True, "text_required": False},
        "four_seasons": {"id": "398574688191234048", "name": "四季写真", "media_required": True, "text_required": False},
        "male_model": {"id": "393876118804459526", "name": "男模特试穿广告", "media_required": True, "text_required": False}
    }

    template_name = extra_args.get("template") or prompt_or_text
    if template_name not in TEMPLATES:
        return {"error": f"Unknown template '{template_name}'. Available: {', '.join(TEMPLATES.keys())}"}
    tmpl = TEMPLATES[template_name]
    media_path = extra_args.get("media")
    text_value = extra_args.get("text")
    if tmpl["media_required"] and not media_path:
        return {"error": f"Template '{tmpl['name']}' requires --media"}
    if tmpl["text_required"] and not text_value:
        return {"error": f"Template '{tmpl['name']}' requires --text"}

    print(client.get_budget_report("MiniMax-Hailuo-02-512P-6s"))
    if estimate_only:
        return {"estimate_only": True}

    data = {"template_id": tmpl["id"]}
    if media_path:
        media_value = _file_to_data_url(media_path)
        data["media_inputs"] = [{"value": media_value}]
    if text_value:
        data["text_inputs"] = [{"value": text_value}]

    print(f"Creating video template task: {tmpl['name']}...")
    resp = client.post("video_template_generation", data)
    if resp.get("base_resp", {}).get("status_code") == 0:
        task_id = resp.get("task_id")
        target_dir, filename_base = get_standard_path("VID", project=project,
                                                       prompt_slug=template_name,
                                                       output_dir=output_dir)
        suggested_path = os.path.join(target_dir, f"{filename_base}.mp4")
        return {"task_id": task_id, "suggested_path": suggested_path}
    return {"error": resp}


def execute_speech(client, prompt_or_text: str, model: str, project: Optional[str],
                   output_dir: Optional[str], estimate_only: bool,
                   extra_args: Dict[str, Any]) -> Dict[str, Any]:
    from minimax_client import get_standard_path

    print(client.get_budget_report(model, text_len=len(prompt_or_text)))
    if estimate_only:
        return {"estimate_only": True}

    voice = extra_args.get("voice", "male-qn-qingse")
    data = {
        "model": model,
        "text": prompt_or_text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice,
            "speed": extra_args.get("speed", 1.0),
            "vol": 1.0,
            "pitch": 0
        },
        "output_format": "url"
    }

    print("Synthesizing speech...")
    resp = client.post("t2a_v2", data)
    if resp.get("base_resp", {}).get("status_code") == 0:
        url = resp["data"]["audio"]
        target_dir, filename_base = get_standard_path("TTS", project=project,
                                                       prompt_slug=prompt_or_text[:20],
                                                       output_dir=output_dir)
        filepath = os.path.join(target_dir, f"{filename_base}.mp3")
        if _download_and_save(url, filepath):
            client.print_saved_result(filepath, "Speech", project=project)
            return {"filepath": filepath}
    return {"error": resp}


def execute_async_speech(client, prompt_or_text: str, model: str, project: Optional[str],
                         output_dir: Optional[str], estimate_only: bool,
                         extra_args: Dict[str, Any]) -> Dict[str, Any]:
    from minimax_client import get_standard_path

    text_or_file = prompt_or_text
    if os.path.isfile(text_or_file):
        with open(text_or_file, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"Loaded text from file: {text_or_file} ({len(text)} chars)")
        text_file_id = None
    else:
        text = text_or_file
        text_file_id = None

    print(client.get_budget_report("async-speech-2.8-hd", text_len=len(text)))
    if estimate_only:
        return {"estimate_only": True}

    voice = extra_args.get("voice", "male-qn-qingse")
    audio_format = extra_args.get("format", "mp3")
    data = {
        "model": model,
        "voice_setting": {
            "voice_id": voice,
            "speed": extra_args.get("speed", 1.0),
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "format": audio_format,
            "audio_sample_rate": 32000,
            "bitrate": 128000,
            "channel": 1
        }
    }
    if text_file_id:
        data["text_file_id"] = text_file_id
    else:
        data["text"] = text[:50000]

    print("Creating async speech task...")
    resp = client.post("t2a_async_v2", data)
    if resp.get("base_resp", {}).get("status_code") != 0:
        return {"error": resp}

    task_id = resp.get("task_id")
    print(f"Async task created: {task_id}")
    while True:
        time.sleep(20)
        status_resp = client.get(f"query/t2a_async_query_v2?task_id={task_id}")
        status = (status_resp.get("status") or "").lower()
        if status == "success":
            file_id = status_resp.get("file_id")
            print(f"Task completed. Downloading file bundle (file_id={file_id})...")
            try:
                bundle_data = client.download_file(file_id)
                target_dir, filename_base = get_standard_path("TTS", project=project,
                                                               prompt_slug="async_speech",
                                                               output_dir=output_dir)
                filepath = os.path.join(target_dir, f"{filename_base}.{audio_format}")

                # MiniMax async speech returns a tar bundle containing .mp3/.titles/.extra files.
                tar_stream = io.BytesIO(bundle_data)
                try:
                    with tarfile.open(fileobj=tar_stream, mode='r:*') as tf:
                        audio_member = next((m for m in tf.getmembers() if m.isfile() and m.name.endswith(f'.{audio_format}')), None)
                        if not audio_member:
                            audio_member = next((m for m in tf.getmembers() if m.isfile() and m.name.endswith('.mp3')), None)
                        if not audio_member:
                            raise RuntimeError('async speech bundle missing audio file')
                        extracted = tf.extractfile(audio_member)
                        if not extracted:
                            raise RuntimeError('failed to extract async speech audio file')
                        with open(filepath, 'wb') as f:
                            f.write(extracted.read())
                except tarfile.ReadError:
                    # Fallback: provider returned raw audio directly
                    with open(filepath, 'wb') as f:
                        f.write(bundle_data)

                client.print_saved_result(filepath, "Speech", project=project)
                return {"filepath": filepath}
            except Exception as e:
                return {"error": f"Download failed: {e}", "status_resp": status_resp}
        if status in {"failed", "expired"}:
            return {"error": status_resp}
        print(f"Processing... (task_id={task_id})")


def execute_voice_clone(client, prompt_or_text: str, model: str, project: Optional[str],
                        output_dir: Optional[str], estimate_only: bool,
                        extra_args: Dict[str, Any]) -> Dict[str, Any]:
    audio_path = prompt_or_text
    voice_id = extra_args.get("voice_id")
    prompt_audio = extra_args.get("prompt_audio")
    prompt_text = extra_args.get("prompt_text")
    preview_text = extra_args.get("preview_text")
    if not voice_id:
        return {"error": "--voice-id is required for voice-clone"}
    if not os.path.isfile(audio_path):
        return {"error": f"Audio file not found: {audio_path}"}
    if prompt_audio and not os.path.isfile(prompt_audio):
        return {"error": f"Prompt audio file not found: {prompt_audio}"}

    print("[MiniMax Voice Clone]")
    print("⚠️ 克隆音色若 7 天内未正式调用，会被系统删除")
    if estimate_only:
        return {"estimate_only": True}

    upload_payload, file_id = _upload_file(client, audio_path, purpose="voice_clone")
    if upload_payload.get("base_resp", {}).get("status_code") != 0 or not file_id:
        return {"error": upload_payload}

    clone_data = {
        "file_id": file_id,
        "voice_id": voice_id,
    }

    if prompt_audio:
        prompt_payload, prompt_file_id = _upload_file(client, prompt_audio, purpose="prompt_audio")
        if prompt_payload.get("base_resp", {}).get("status_code") != 0 or not prompt_file_id:
            return {"error": prompt_payload}
        if not prompt_text:
            return {"error": "--prompt-text is required when --prompt-audio is provided"}
        clone_data["clone_prompt"] = {
            "prompt_audio": prompt_file_id,
            "prompt_text": prompt_text,
        }

    if preview_text:
        clone_data["text"] = preview_text
        clone_data["model"] = model or "speech-2.8-hd"

    resp = requests.post(
        f"{client.base_url}/voice_clone",
        headers={"Authorization": f"Bearer {client.api_key}", "Content-Type": "application/json"},
        json=clone_data,
    ).json()

    if resp.get("base_resp", {}).get("status_code") == 0:
        return {"voice_id": voice_id, "demo_audio": resp.get("demo_audio")}
    return {"error": resp}


def execute_voice_design(client, prompt_or_text: str, model: str, project: Optional[str],
                         output_dir: Optional[str], estimate_only: bool,
                         extra_args: Dict[str, Any]) -> Dict[str, Any]:
    description = prompt_or_text
    voice_id = extra_args.get("voice_id")
    preview_text = extra_args.get("preview_text")
    if not preview_text:
        return {"error": "--preview-text is required for voice-design"}

    print("[MiniMax Voice Design]")
    if estimate_only:
        return {"estimate_only": True}

    data = {
        "prompt": description,
        "preview_text": preview_text,
    }
    if voice_id:
        data["voice_id"] = voice_id

    resp = requests.post(
        f"{client.base_url}/voice_design",
        headers={"Authorization": f"Bearer {client.api_key}", "Content-Type": "application/json"},
        json=data,
    ).json()

    if resp.get("base_resp", {}).get("status_code") == 0:
        return {"voice_id": resp.get("voice_id") or voice_id, "trial_audio": resp.get("trial_audio")}
    return {"error": resp}


def execute_music(client, prompt_or_text: str, model: str, project: Optional[str],
                  output_dir: Optional[str], estimate_only: bool,
                  extra_args: Dict[str, Any]) -> Dict[str, Any]:
    from minimax_client import get_standard_path

    print(client.get_budget_report(model))
    if estimate_only:
        return {"estimate_only": True}

    data = {
        "model": model,
        "prompt": prompt_or_text,
        "is_instrumental": extra_args.get("instrumental", False),
        "output_format": "url"
    }
    lyrics = extra_args.get("lyrics")
    if lyrics:
        data["lyrics"] = lyrics
    elif not extra_args.get("instrumental", False):
        data["lyrics_optimizer"] = True

    print(f"Generating music: {prompt_or_text}...")
    resp = client.post("music_generation", data)
    if resp.get("base_resp", {}).get("status_code") == 0:
        url = resp["data"]["audio"]
        target_dir, filename_base = get_standard_path("MSC", project=project,
                                                       prompt_slug=prompt_or_text,
                                                       output_dir=output_dir)
        filepath = os.path.join(target_dir, f"{filename_base}.mp3")
        if _download_and_save(url, filepath):
            client.print_saved_result(filepath, "Music", project=project)
            return {"filepath": filepath}
    return {"error": resp}
