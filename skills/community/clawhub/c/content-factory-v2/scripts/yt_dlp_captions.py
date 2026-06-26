#!/usr/bin/env python3
"""
Download YouTube subtitles via yt-dlp and optionally run local Whisper transcription.

Examples:
  python3 scripts/yt_dlp_captions.py "https://www.youtube.com/watch?v=VIDEO_ID"
  python3 scripts/yt_dlp_captions.py "https://youtu.be/VIDEO_ID" --langs en,zh-Hans
  python3 scripts/yt_dlp_captions.py "URL" --whisper-if-missing --whisper-model base
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys


def ensure_command(name):
  if shutil.which(name) is None:
    sys.stderr.write(
      f'Missing dependency: {name}. Install it and retry.\n'
    )
    raise SystemExit(1)


def get_ytdlp_cmd():
  if shutil.which('yt-dlp'):
    return ['yt-dlp']
  return [sys.executable, '-m', 'yt_dlp']


def run_cmd(cmd):
  proc = subprocess.run(cmd, capture_output=True, text=True)
  if proc.returncode != 0:
    sys.stderr.write(proc.stderr)
    raise SystemExit(proc.returncode)
  return proc.stdout


def get_video_id(url):
  cmd = get_ytdlp_cmd() + [
    '--skip-download',
    '--no-playlist',
    '--print',
    '%(id)s',
    url,
  ]
  output = run_cmd(cmd)
  for line in output.splitlines():
    line = line.strip()
    if line:
      return line
  raise SystemExit('Unable to resolve video id.')


def download_subs(url, out_dir, video_id, langs, sub_format, subs_mode):
  os.makedirs(out_dir, exist_ok=True)
  output_tpl = os.path.join(out_dir, video_id, f'{video_id}.%(ext)s')
  cmd = get_ytdlp_cmd() + [
    '--skip-download',
    '--no-playlist',
    '--sub-format',
    sub_format,
    '--sub-langs',
    langs,
    '--output',
    output_tpl,
  ]
  if subs_mode in ('manual', 'both'):
    cmd.append('--write-subs')
  if subs_mode in ('auto', 'both'):
    cmd.append('--write-auto-subs')
  cmd.append(url)
  run_cmd(cmd)


def find_caption_files(out_dir, video_id):
  patterns = [
    os.path.join(out_dir, video_id, f'{video_id}*.vtt'),
    os.path.join(out_dir, video_id, f'{video_id}*.srt'),
  ]
  files = []
  for pattern in patterns:
    files.extend(glob.glob(pattern))
  return sorted(set(files))


def download_audio(url, out_dir, video_id, audio_format):
  os.makedirs(out_dir, exist_ok=True)
  output_tpl = os.path.join(out_dir, video_id, f'{video_id}.%(ext)s')
  cmd = get_ytdlp_cmd() + [
    '--no-playlist',
    '-x',
    '--audio-format',
    audio_format,
    '--output',
    output_tpl,
    url,
  ]
  run_cmd(cmd)
  audio_path = os.path.join(out_dir, video_id, f'{video_id}.{audio_format}')
  if not os.path.exists(audio_path):
    raise SystemExit(f'Audio file not found: {audio_path}')
  return audio_path


def run_whisper(audio_path, out_dir, model, language, task, output_format):
  ensure_command('whisper')
  cmd = [
    'whisper',
    audio_path,
    '--model',
    model,
    '--output_dir',
    out_dir,
    '--output_format',
    output_format,
  ]
  if language:
    cmd.extend(['--language', language])
  if task:
    cmd.extend(['--task', task])
  run_cmd(cmd)


def main():
  parser = argparse.ArgumentParser(
    description='Download YouTube subtitles via yt-dlp and optionally run Whisper.'
  )
  parser.add_argument('url', help='YouTube URL')
  parser.add_argument('--out-dir', default='outputs', help='Output directory')
  parser.add_argument(
    '--langs',
    default='en,zh,zh-Hans,zh-Hant',
    help='Comma-separated subtitle languages',
  )
  parser.add_argument(
    '--sub-format',
    default='vtt',
    help='Subtitle format (vtt or srt)',
  )
  parser.add_argument(
    '--subs',
    choices=['manual', 'auto', 'both'],
    default='both',
    help='Subtitle type to download',
  )
  parser.add_argument(
    '--whisper',
    action='store_true',
    help='Run Whisper regardless of subtitle availability',
  )
  parser.add_argument(
    '--whisper-if-missing',
    action='store_true',
    help='Run Whisper only if no subtitles were found',
  )
  parser.add_argument(
    '--whisper-model',
    default='base',
    help='Whisper model name (tiny, base, small, medium, large)',
  )
  parser.add_argument(
    '--whisper-lang',
    default='',
    help='Force Whisper language (e.g., en, zh)',
  )
  parser.add_argument(
    '--whisper-task',
    default='',
    help='Whisper task (transcribe or translate)',
  )
  parser.add_argument(
    '--whisper-format',
    default='txt',
    help='Whisper output format (txt, srt, vtt, json)',
  )
  parser.add_argument(
    '--audio-format',
    default='mp3',
    help='Audio format for Whisper input',
  )
  args = parser.parse_args()

  if args.whisper and args.whisper_if_missing:
    raise SystemExit('Use either --whisper or --whisper-if-missing, not both.')

  video_id = get_video_id(args.url)
  download_subs(
    args.url,
    args.out_dir,
    video_id,
    args.langs,
    args.sub_format,
    args.subs,
  )
  caption_files = find_caption_files(args.out_dir, video_id)
  if caption_files:
    print('Downloaded subtitle files:')
    for path in caption_files:
      print(path)
  else:
    print('No subtitle files found.')

  should_run_whisper = args.whisper or (
    args.whisper_if_missing and not caption_files
  )
  if should_run_whisper:
    audio_path = download_audio(
      args.url,
      args.out_dir,
      video_id,
      args.audio_format,
    )
    run_whisper(
      audio_path,
      os.path.join(args.out_dir, video_id),
      args.whisper_model,
      args.whisper_lang,
      args.whisper_task,
      args.whisper_format,
    )
    print('Whisper output saved in:', os.path.join(args.out_dir, video_id))


if __name__ == '__main__':
  main()
