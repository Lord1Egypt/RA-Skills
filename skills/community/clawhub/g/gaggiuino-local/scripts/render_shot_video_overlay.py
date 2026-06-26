#!/usr/bin/env python3
"""Video overlay: high-performance FFmpeg-native compositing.

Uses FFmpeg filter_complex to perform stacking/overlaying, keeping video
data out of Python. Python only generates the 10fps graph sequence.
"""
import os
os.environ.setdefault('PYTHONNOUSERSITE', '1')

import sys

# Re-exec with a clean env if user-site packages are active (matches the graph renderer).
if 'site' in sys.modules:
    import site
    if getattr(site, 'ENABLE_USER_SITE', False) and os.environ.get('_OVERLAY_REEXEC') != '1':
        env = os.environ.copy()
        env['PYTHONNOUSERSITE'] = '1'
        env['_OVERLAY_REEXEC'] = '1'
        os.execvpe(sys.executable, [sys.executable] + sys.argv, env)

# Prevent graph renderer module-level re-exec when imported.
os.environ['_GAGGIUINO_GRAPH_REEXEC'] = '1'

import argparse
import json
import math
import shutil
import subprocess
from typing import Any, Dict

import numpy as np

# Import graph renderer from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_shot_graph import ContextRenderer, load_shot_from_id, load_shot_from_file

import matplotlib.pyplot as plt


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_video_info(path: str) -> Dict[str, Any]:
    """Get video metadata via ffprobe."""
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json',
           '-show_streams', '-show_format', path]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    for stream in data['streams']:
        if stream['codec_type'] == 'video':
            w = int(stream['width'])
            h = int(stream['height'])
            
            # Rotation detection (FFmpeg auto-rotates by default in filters)
            rotation = 0
            for side_data in stream.get('side_data_list', []):
                if 'rotation' in side_data:
                    rotation = int(side_data['rotation'])
            
            # Fallback for older ffprobe
            if not rotation:
                rotation = int(stream.get('tags', {}).get('rotate', 0))
                
            if abs(rotation) in (90, 270):
                # FFmpeg will display it as rotated, so we swap for layout logic
                w, h = h, w
                
            parts = stream['r_frame_rate'].split('/')
            num, den = int(parts[0]), int(parts[1]) if len(parts) > 1 else 1
            fps = num / den if den else 30.0
            dur = float(stream.get('duration', 0)) or float(data['format'].get('duration', 0))
            return {'width': w, 'height': h, 'fps': fps, 'duration': dur}
    raise RuntimeError(f'No video stream found in {path}')


def _even(n: int) -> int:
    """Round down to nearest even integer."""
    return n - (n % 2)


# ─── Audio sync helpers ───────────────────────────────────────────────────────


def moving_average(x: np.ndarray, win: int) -> np.ndarray:
    """Simple centered moving average."""
    if win <= 1 or x.size == 0:
        return x
    kernel = np.ones(win, dtype=np.float32) / float(win)
    return np.convolve(x, kernel, mode='same')



def safe_normalize(value: float, scale: float, clip: float = 3.0) -> float:
    """Normalize a positive score safely into a bounded range."""
    if scale <= 1e-8:
        return 0.0
    return max(0.0, min(float(clip), float(value) / float(scale)))



def detection_fail(reason: str, method: str,
                   confidence: float = 0.0,
                   details: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Build a standard failed detection result."""
    payload = {'reason': reason}
    if details:
        payload.update(details)
    return {
        'detected': False,
        'offset': 0.0,
        'confidence': float(confidence),
        'event_type': 'unknown',
        'method': method,
        'details': payload,
    }



def extract_audio_mono_s16le(video_path: str,
                             sample_rate: int = 16000) -> tuple[np.ndarray, int]:
    """Extract mono PCM audio from video via ffmpeg and return float32 samples."""
    cmd = [
        'ffmpeg', '-v', 'error',
        '-i', video_path,
        '-vn',
        '-ac', '1',
        '-ar', str(sample_rate),
        '-f', 's16le',
        'pipe:1',
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError('audio_extract_failed')
    if not proc.stdout:
        raise RuntimeError('audio_empty')

    raw = np.frombuffer(proc.stdout, dtype=np.int16)
    if raw.size == 0:
        raise RuntimeError('audio_empty')

    samples = raw.astype(np.float32) / 32768.0
    return samples, sample_rate



def compute_audio_features(samples: np.ndarray, sr: int,
                           frame_ms: int = 20,
                           hop_ms: int = 10) -> Dict[str, np.ndarray]:
    """Compute frame-level features for switch/pump onset detection."""
    frame_len = max(1, int(sr * frame_ms / 1000))
    hop_len = max(1, int(sr * hop_ms / 1000))

    samples = samples.astype(np.float32, copy=False)
    if samples.size == 0:
        return {
            'times': np.array([], dtype=np.float32),
            'rms': np.array([], dtype=np.float32),
            'delta_rms': np.array([], dtype=np.float32),
            'peak': np.array([], dtype=np.float32),
        }

    samples = samples - np.mean(samples)
    if samples.size < frame_len:
        pad = np.zeros(frame_len - samples.size, dtype=np.float32)
        samples = np.concatenate([samples, pad])

    times = []
    rms_values = []
    peak_values = []
    for start in range(0, samples.size - frame_len + 1, hop_len):
        frame = samples[start:start + frame_len]
        rms = np.sqrt(np.mean(frame * frame) + 1e-12)
        peak = np.max(np.abs(frame))
        t = (start + frame_len / 2) / sr
        times.append(t)
        rms_values.append(rms)
        peak_values.append(peak)

    rms = moving_average(np.asarray(rms_values, dtype=np.float32), 3)
    peak = moving_average(np.asarray(peak_values, dtype=np.float32), 3)
    delta_rms = np.diff(rms, prepend=rms[0] if rms.size else 0.0)

    return {
        'times': np.asarray(times, dtype=np.float32),
        'rms': rms,
        'delta_rms': delta_rms.astype(np.float32, copy=False),
        'peak': peak,
    }



def robust_baseline(values: np.ndarray, times: np.ndarray,
                    baseline_sec: float = 0.8) -> tuple[float, float]:
    """Estimate baseline level and spread from early audio using robust stats."""
    if values.size == 0:
        return 0.0, 1e-4

    mask = times <= baseline_sec
    ref = values[mask] if np.any(mask) else values[:max(5, min(len(values), 20))]
    if ref.size == 0:
        ref = values

    baseline = float(np.percentile(ref, 20))
    med = float(np.median(ref))
    spread = float(np.median(np.abs(ref - med)) * 1.4826)
    return baseline, max(spread, 1e-4)



def score_to_confidence(score: float, strong_score: float = 1.5) -> float:
    """Map heuristic score into a 0-1 confidence."""
    if strong_score <= 1e-8:
        return 0.0
    return max(0.0, min(1.0, float(score) / float(strong_score)))



def detect_switch_start(samples: np.ndarray, sr: int,
                        debug: bool = False) -> Dict[str, Any]:
    """Detect switch onset as the earliest confident transient event."""
    feats = compute_audio_features(samples, sr)
    times = feats['times']
    rms = feats['rms']
    delta = feats['delta_rms']
    peak = feats['peak']

    mask = times <= 5.0
    times = times[mask]
    rms = rms[mask]
    delta = delta[mask]
    peak = peak[mask]

    if times.size < 5:
        return detection_fail('audio_too_short', 'switch-transient-v1')

    baseline_rms, spread_rms = robust_baseline(rms, times, baseline_sec=0.8)
    baseline_peak, spread_peak = robust_baseline(peak, times, baseline_sec=0.8)

    early_delta = delta[:max(5, min(delta.size, 30))]
    delta_scale = max(float(np.std(early_delta)), 0.003)
    peak_scale = max(4.0 * spread_peak, 0.03)
    sharp_scale = max(2.0 * spread_peak, 0.02)
    sustain_thresh = baseline_rms + max(2.5 * spread_rms, 0.006)

    best_idx = None
    best_score = -1.0
    best_sustain_ratio = 0.0
    best_sharpness = 0.0
    for i in range(2, max(2, times.size - 2)):
        if delta[i] < max(3.5 * delta_scale, 0.003):
            continue
        if peak[i] < baseline_peak + peak_scale:
            continue

        local_pre = float(np.mean(rms[max(0, i - 2):i])) if i > 0 else float(rms[i])
        local_post = float(np.mean(rms[i + 1:min(times.size, i + 3)])) if i + 1 < times.size else float(rms[i])
        sharpness = float(peak[i] - max(local_pre, local_post))
        future = rms[i + 1:min(times.size, i + 21)]
        sustain_ratio = float(np.mean(future > sustain_thresh)) if future.size else 0.0

        score = (
            0.38 * safe_normalize(float(delta[i]), delta_scale) +
            0.34 * safe_normalize(float(peak[i] - baseline_peak), peak_scale) +
            0.23 * safe_normalize(sharpness, sharp_scale) -
            0.22 * sustain_ratio -
            0.04 * float(times[i])
        )
        if score > best_score:
            best_score = score
            best_idx = i
            best_sustain_ratio = sustain_ratio
            best_sharpness = sharpness

    if best_idx is None:
        return detection_fail(
            'no_switch_transient',
            'switch-transient-v1',
            details={
                'baseline_rms': baseline_rms,
                'baseline_peak': baseline_peak,
            },
        )

    confidence = score_to_confidence(best_score, strong_score=2.2)
    return {
        'detected': True,
        'offset': float(times[best_idx]),
        'confidence': confidence,
        'event_type': 'switch',
        'method': 'switch-transient-v1',
        'details': {
            'candidate_index': int(best_idx),
            'candidate_time': float(times[best_idx]),
            'score': float(best_score),
            'baseline_rms': baseline_rms,
            'baseline_peak': baseline_peak,
            'sharpness': float(best_sharpness),
            'sustain_ratio': float(best_sustain_ratio),
        },
    }



def detect_pump_start(samples: np.ndarray, sr: int,
                      debug: bool = False) -> Dict[str, Any]:
    """Detect pump onset as a sustained rise in audio energy."""
    feats = compute_audio_features(samples, sr)
    times = feats['times']
    rms = feats['rms']
    delta = feats['delta_rms']

    mask = times <= 8.0
    times = times[mask]
    rms = rms[mask]
    delta = delta[mask]

    if times.size < 5:
        return detection_fail('audio_too_short', 'pump-sustain-v1')

    baseline, spread = robust_baseline(rms, times, baseline_sec=0.8)
    rise_scale = max(4.0 * spread, 0.01)
    delta_scale = max(float(np.std(delta[:max(5, min(delta.size, 30))])), 0.002)
    hold_frames = min(max(3, int(round(300 / 10))), max(1, times.size - 1))

    best_idx = None
    best_score = -1.0
    best_hold_ratio = 0.0
    for i in range(0, max(0, times.size - hold_frames)):
        if rms[i] < baseline + rise_scale:
            continue
        future = rms[i:i + hold_frames]
        hold_thresh = baseline + max(3.0 * spread, 0.008)
        hold_ratio = float(np.mean(future > hold_thresh)) if future.size else 0.0
        if hold_ratio < 0.7:
            continue
        score = (
            0.50 * safe_normalize(float(rms[i] - baseline), rise_scale) +
            0.20 * safe_normalize(float(delta[i]), delta_scale) +
            0.30 * hold_ratio
        )
        if score > best_score:
            best_score = score
            best_idx = i
            best_hold_ratio = hold_ratio

    if best_idx is None:
        return detection_fail(
            'no_pump_sustain',
            'pump-sustain-v1',
            details={
                'baseline_rms': baseline,
            },
        )

    confidence = score_to_confidence(best_score, strong_score=1.8)
    return {
        'detected': True,
        'offset': float(times[best_idx]),
        'confidence': confidence,
        'event_type': 'pump',
        'method': 'pump-sustain-v1',
        'details': {
            'candidate_index': int(best_idx),
            'candidate_time': float(times[best_idx]),
            'score': float(best_score),
            'hold_ratio': float(best_hold_ratio),
            'baseline_rms': baseline,
        },
    }



def detect_extraction_start_from_audio(samples: np.ndarray, sr: int,
                                       mode: str = 'auto',
                                       debug: bool = False) -> Dict[str, Any]:
    """Detect extraction start from audio. Auto prefers switch, then pump."""
    if mode == 'switch':
        return detect_switch_start(samples, sr, debug=debug)
    if mode == 'pump':
        return detect_pump_start(samples, sr, debug=debug)

    switch_res = detect_switch_start(samples, sr, debug=debug)
    pump_res = detect_pump_start(samples, sr, debug=debug)

    switch_ok = switch_res['detected'] and switch_res.get('confidence', 0.0) >= 0.45
    pump_ok = pump_res['detected'] and pump_res.get('confidence', 0.0) >= 0.40

    if switch_ok:
        return switch_res
    if pump_ok:
        pump_res = dict(pump_res)
        details = dict(pump_res.get('details') or {})
        details['switch_fallback_reason'] = switch_res.get('details', {}).get('reason', 'switch_low_confidence')
        pump_res['details'] = details
        return pump_res

    return detection_fail(
        'no_confident_detection',
        'auto-switch-first-v1',
        confidence=max(float(switch_res.get('confidence', 0.0)), float(pump_res.get('confidence', 0.0))),
        details={
            'switch': switch_res,
            'pump': pump_res,
        },
    )



def resolve_offset(video_path: str,
                   manual_offset: float | None,
                   audio_sync_mode: str = 'auto',
                   debug: bool = False) -> Dict[str, Any]:
    """Resolve final overlay offset: manual > auto-detect > fallback."""
    if manual_offset is not None:
        if debug:
            print(f'Audio sync: manual offset={manual_offset:.2f}s', file=sys.stderr)
        return {
            'offset': float(manual_offset),
            'offset_source': 'manual',
            'confidence': 1.0,
            'event_type': 'manual',
            'method': 'manual',
            'warning': None,
            'details': None,
        }

    try:
        samples, sr = extract_audio_mono_s16le(video_path)
        switch_res = detect_switch_start(samples, sr, debug=debug)
        pump_res = detect_pump_start(samples, sr, debug=debug)

        if audio_sync_mode == 'switch':
            detected = switch_res
        elif audio_sync_mode == 'pump':
            detected = pump_res
        else:
            switch_ok = switch_res['detected'] and switch_res.get('confidence', 0.0) >= 0.55
            pump_ok = pump_res['detected'] and pump_res.get('confidence', 0.0) >= 0.45

            switch_time = float(switch_res.get('offset', 0.0)) if switch_res.get('detected') else None
            pump_time = float(pump_res.get('offset', 0.0)) if pump_res.get('detected') else None
            switch_sustain = float(switch_res.get('details', {}).get('sustain_ratio', 0.0))
            pump_gap = None if switch_time is None or pump_time is None else pump_time - switch_time
            merged_candidate = (
                switch_ok and (
                    (switch_sustain >= 0.75 and pump_gap is not None and abs(pump_gap) <= 0.35) or
                    (switch_sustain >= 0.90)
                )
            )

            if merged_candidate:
                detected = dict(switch_res)
                details = dict(detected.get('details') or {})
                details['pump_candidate_time'] = pump_time
                details['pump_gap'] = pump_gap
                details['classification'] = 'switch_pump_merged'
                detected['details'] = details
                detected['event_type'] = 'switch_pump_merged'
                detected['method'] = 'machine-start-onset-v2'
            elif switch_ok:
                detected = dict(switch_res)
                details = dict(detected.get('details') or {})
                details['classification'] = 'switch'
                details['pump_candidate_time'] = pump_time
                details['pump_gap'] = pump_gap
                detected['details'] = details
                detected['event_type'] = 'switch'
                detected['method'] = 'machine-start-onset-v2'
            elif pump_ok:
                detected = dict(pump_res)
                details = dict(detected.get('details') or {})
                details['switch_fallback_reason'] = switch_res.get('details', {}).get('reason', 'switch_low_confidence')
                details['switch_candidate_time'] = switch_time
                details['classification'] = 'pump'
                detected['details'] = details
                detected['event_type'] = 'pump'
                detected['method'] = 'machine-start-onset-v2'
            else:
                detected = detection_fail(
                    'no_confident_detection',
                    'machine-start-onset-v2',
                    confidence=max(float(switch_res.get('confidence', 0.0)), float(pump_res.get('confidence', 0.0))),
                    details={
                        'switch': switch_res,
                        'pump': pump_res,
                    },
                )
    except Exception as exc:
        switch_res = None
        pump_res = None
        detected = detection_fail(str(exc), 'auto-switch-first-v1')

    if debug:
        print(f'Audio sync mode: {audio_sync_mode} (prefer switch, fallback pump)', file=sys.stderr)
        if switch_res is not None:
            print(
                f"Switch candidate: {switch_res.get('offset', 0.0):.2f}s, "
                f"score={switch_res.get('details', {}).get('score', 0.0):.2f}, "
                f"confidence={switch_res.get('confidence', 0.0):.2f}, "
                f"sustain={switch_res.get('details', {}).get('sustain_ratio', 0.0):.2f}, "
                f"detected={switch_res.get('detected', False)}",
                file=sys.stderr,
            )
        if pump_res is not None:
            print(
                f"Pump candidate:   {pump_res.get('offset', 0.0):.2f}s, "
                f"score={pump_res.get('details', {}).get('score', 0.0):.2f}, "
                f"confidence={pump_res.get('confidence', 0.0):.2f}, "
                f"detected={pump_res.get('detected', False)}",
                file=sys.stderr,
            )

    if detected.get('detected'):
        warning = None
        if detected.get('event_type') == 'pump':
            warning = 'Switch onset not confidently detected; fell back to pump onset'
        if debug:
            print(
                f"Selected event: {detected.get('event_type')} @ {detected.get('offset', 0.0):.2f}s, "
                f"confidence={detected.get('confidence', 0.0):.2f}",
                file=sys.stderr,
            )
        return {
            'offset': float(detected['offset']),
            'offset_source': 'auto',
            'confidence': float(detected.get('confidence', 0.0)),
            'event_type': str(detected.get('event_type', 'unknown')),
            'method': str(detected.get('method', 'unknown')),
            'warning': warning,
            'details': detected.get('details'),
        }

    if debug:
        print('Auto audio sync failed; falling back to offset=0.0', file=sys.stderr)

    return {
        'offset': 0.0,
        'offset_source': 'fallback',
        'confidence': float(detected.get('confidence', 0.0)),
        'event_type': 'unknown',
        'method': str(detected.get('method', 'auto-switch-first-v1')),
        'warning': 'Auto audio sync failed; fell back to offset=0.0',
        'details': detected.get('details'),
    }


# ─── Main pipeline ───────────────────────────────────────────────────────────

def render_overlay(shot: Dict[str, Any], video_path: str, out_path: str,
                    offset: float = 0.0, alpha: float = 0.65,
                    position: str = 'top', graph_fps: int = 10) -> Dict[str, Any]:
    """Composite graph animation onto user video using FFmpeg filters.

    Python only outputs the 10fps graph sequence. FFmpeg handles the heavy lifting.
    """
    if not shutil.which('ffmpeg'):
        raise RuntimeError('ffmpeg not found in PATH')
    if not shutil.which('ffprobe'):
        raise RuntimeError('ffprobe not found in PATH')

    # ── Video info ──
    vinfo = get_video_info(video_path)
    vid_w = _even(vinfo['width'])
    vid_h = _even(vinfo['height'])
    vid_fps = vinfo['fps']
    vid_duration = vinfo['duration']
    is_landscape = vid_w >= vid_h

    # ── Graph renderer ──
    renderer = ContextRenderer(shot)
    graph_w, graph_h = renderer.out_w, renderer.out_h
    graph_duration = renderer.duration
    
    # Calc scaled graph height for filter string
    scaled_graph_h = _even(int(graph_h * (vid_w / graph_w))) if graph_w else 0

    # ── Timing & Padding ──
    # Total frames to output from Python at graph_fps
    # We must match the full video duration
    total_output_frames = max(1, int(vid_duration * graph_fps))
    
    # ── Start encoder with complex filter ──
    # [0:v] is the 10fps pipe, [1:v] is the original video
    # ── Start encoder with complex filter ──
    # [0:v] is the 10fps rawvideo pipe from Python
    # [1:v] is the original user video (source)
    # Both are forced to vid_fps (Constant Frame Rate) to avoid sync-drift
    
    if is_landscape:
        # vstack: Scale graph to vid_w, move to target fps and format.
        filter_complex = (
            f'[0:v]scale={vid_w}:{scaled_graph_h},fps=fps={vid_fps},format=yuv420p[g];'
            f'[1:v]fps=fps={vid_fps},format=yuv420p[v];'
            f'[g][v]vstack'
        )
    else:
        # overlay: Scale graph to vid_w, set alpha, and overlay at top or bottom.
        y_pos = 0 if position == 'top' else vid_h - scaled_graph_h
        filter_complex = (
            f'[0:v]scale={vid_w}:{scaled_graph_h},fps=fps={vid_fps},format=rgba,colorchannelmixer=aa={alpha}[g];'
            f'[1:v]fps=fps={vid_fps},format=yuv420p[v];'
            f'[v][g]overlay=x=0:y={y_pos}'
        )

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    encode_cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', f'{graph_w}x{graph_h}', '-pix_fmt', 'rgb24',
        '-r', str(graph_fps), '-i', 'pipe:0',
        '-i', video_path,
        '-filter_complex', filter_complex,
        '-map', 'a?',  # Try to grab audio from video_path input
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-c:a', 'copy',
        '-preset', 'fast', '-crf', '23',
        '-movflags', '+faststart',
        '-shortest',
        out_path,
    ]
    
    print(f'Overlay architecture: filter-based compositing', file=sys.stderr)
    print(f'Video:  {vid_w}x{vid_h} @ {vid_fps:.1f}fps, {vid_duration:.1f}s', file=sys.stderr)
    print(f'Graph:  {graph_w}x{graph_h} (10fps) → scaled to {vid_w}', file=sys.stderr)
    print(f'Output: {"landscape-stack" if is_landscape else "portrait-overlay"}', file=sys.stderr)

    encoder = subprocess.Popen(encode_cmd, stdin=subprocess.PIPE,
                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    # ── Pre-render padding frames ──
    renderer.update(0.0)
    first_frame = renderer.get_frame()
    
    renderer.update(graph_duration)
    renderer.graph_ctx['v_cursor'].set_visible(False)
    last_frame = renderer.get_frame()

    # ── Frame loop (Only 10 steps per second!) ──
    frames_written = 0
    try:
        for i in range(total_output_frames):
            t_video = i / graph_fps
            t_graph = t_video - offset
            
            if t_graph <= 0:
                frame_rgb = first_frame
            elif t_graph >= graph_duration:
                frame_rgb = last_frame
            else:
                renderer.update(t_graph)
                frame_rgb = renderer.get_frame()
            
            encoder.stdin.write(frame_rgb)
            frames_written += 1
            
            if frames_written % 20 == 0:
                print(f'  Graph Progress: {frames_written}/{total_output_frames}', file=sys.stderr)

    except BrokenPipeError:
        pass
    finally:
        if encoder.stdin:
            encoder.stdin.close()
        rc = encoder.wait()
        plt.close(renderer.fig)

        if rc != 0:
            err = (encoder.stderr.read().decode('utf-8', errors='replace')
                   if encoder.stderr else '')
            raise RuntimeError(f'Encoder ffmpeg exited {rc}: {err[-500:]}')

    return {
        'ok': True,
        'mode': 'filter-based',
        'out': os.path.abspath(out_path),
        'frames': frames_written,
        'fps_python': graph_fps,
        'offset': offset,
    }


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Overlay Gaggiuino shot graph animation onto user video')
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--shot-id', type=int)
    src.add_argument('--input')
    parser.add_argument('--video', required=True)
    parser.add_argument('--out', help='Output file path (default: standard archive dir with shot ID)')
    parser.add_argument(
        '--offset',
        type=float,
        default=None,
        help='Manual sync offset in seconds. If omitted, auto-detect from audio.'
    )
    parser.add_argument(
        '--audio-sync-mode',
        choices=['auto', 'switch', 'pump'],
        default='auto',
        help='Audio sync strategy. auto prefers switch and falls back to pump.'
    )
    parser.add_argument(
        '--audio-debug',
        action='store_true',
        help='Print audio sync detection details to stderr.'
    )
    parser.add_argument('--alpha', type=float, default=0.65)
    parser.add_argument('--position', choices=['top', 'bottom'], default='top')
    parser.add_argument('--graph-fps', type=int, default=10)
    args = parser.parse_args()

    # ── Default output and naming logic ──
    if not args.out:
        base_dir = os.path.expanduser('~/.openclaw/workspace/gaggiuino-output')
        os.makedirs(base_dir, exist_ok=True)
        
        # Get video info early to determine naming suffix
        vinfo = get_video_info(args.video)
        layout_suffix = 'landscape' if vinfo['width'] >= vinfo['height'] else 'portrait'
        
        name_part = f'shot{args.shot_id}' if args.shot_id else 'shot'
        args.out = os.path.join(base_dir, f'{name_part}_overlay_{layout_suffix}.mp4')
    else:
        args.out = os.path.expanduser(args.out)
    
    # Ensure parents exist for custom paths
    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    try:
        shot = (load_shot_from_id(args.shot_id) if args.shot_id is not None
                else load_shot_from_file(args.input))
        offset_info = resolve_offset(
            video_path=args.video,
            manual_offset=args.offset,
            audio_sync_mode=args.audio_sync_mode,
            debug=args.audio_debug,
        )
        result = render_overlay(
            shot, args.video, args.out,
            offset=offset_info['offset'],
            alpha=args.alpha,
            position=args.position,
            graph_fps=args.graph_fps,
        )
        result.update({
            'offset_source': offset_info['offset_source'],
            'offset_confidence': offset_info.get('confidence', 0.0),
            'sync_event': offset_info.get('event_type', 'unknown'),
            'sync_method': offset_info.get('method', 'unknown'),
        })
        if offset_info.get('warning'):
            result['warning'] = offset_info['warning']
        if args.audio_debug and offset_info.get('details') is not None:
            result['sync_details'] = offset_info['details']
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
