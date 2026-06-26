#!/usr/bin/env python3
"""
Volcengine ATA Subtitle Tool (火山引擎 ATA 自动打轴)

Generate subtitles with automatic time alignment using Volcengine's ATA API.

Usage:
    python3 volc_ata.py --audio audio.wav --text subtitle.txt --output final.srt

Config:
    - Environment variables: VOLC_ATA_APP_ID, VOLC_ATA_TOKEN, VOLC_ATA_API_BASE
    - Or config file: ~/.volcengine_ata.conf
"""

import os
import sys
import json
import base64
import time
import argparse
import configparser
from pathlib import Path
from typing import Optional, Dict, Any

import requests


class VolcATASubtitle:
    """Volcengine ATA Subtitle Generator"""
    
    def __init__(
        self,
        app_id: str = None,
        token: str = None,
        api_base: str = None,
        config_file: str = None
    ):
        # Load from config file first
        if config_file is None:
            config_file = os.path.expanduser('~/.volcengine_ata.conf')
        
        self.config = self._load_config(config_file)
        
        # Override with parameters or environment variables
        self.app_id = app_id or os.environ.get('VOLC_ATA_APP_ID') or self.config.get('credentials', 'appid', fallback=None)
        self.token = token or os.environ.get('VOLC_ATA_TOKEN') or self.config.get('credentials', 'access_token', fallback=None)
        self.api_base = api_base or os.environ.get('VOLC_ATA_API_BASE') or self.config.get('api', 'base_url', fallback='https://openspeech.bytedance.com')
        
        self.submit_path = self.config.get('api', 'submit_path', fallback='/api/v1/vc/ata/submit')
        self.query_path = self.config.get('api', 'query_path', fallback='/api/v1/vc/ata/query')
        
        if not self.app_id or not self.token:
            print("⚠️  Warning: ATA credentials not configured")
            print("   Set VOLC_ATA_APP_ID and VOLC_ATA_TOKEN environment variables")
            print("   Or create ~/.volcengine_ata.conf config file")
            print("   Running in demo mode...\n")
    
    def _load_config(self, config_file: str) -> configparser.ConfigParser:
        """Load configuration from file"""
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
        return config
    
    def create_subtitle(
        self,
        audio_file: str,
        text_file: str,
        output_file: str,
        format: str = 'srt',
        language: str = 'zh-CN'
    ) -> Dict[str, Any]:
        """
        Create time-aligned subtitles
        
        Args:
            audio_file: Path to audio file (WAV, 16kHz mono)
            text_file: Path to text file (plain text, one sentence per line)
            output_file: Path to output subtitle file
            format: Output format ('srt' or 'ass')
            language: Language code (default: zh-CN)
        
        Returns:
            Result dictionary with status and metadata
        """
        # Validate input files
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        if not os.path.exists(text_file):
            raise FileNotFoundError(f"Text file not found: {text_file}")
        
        # Read audio file
        print(f"📤 Reading audio: {audio_file}")
        with open(audio_file, 'rb') as f:
            audio_data = base64.b64encode(f.read()).decode('utf-8')
        print(f"   Audio size: {len(audio_data)} bytes")
        
        # Read text file
        print(f"📖 Reading text: {text_file}")
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"   Text length: {len(text)} characters")
        
        # Check if credentials are configured
        if not self.app_id or not self.token:
            # Demo mode - create mock subtitle
            print("\n⚠️  Running in demo mode (no API credentials)")
            print("   Creating mock subtitle file...")
            self._create_mock_subtitle(output_file, text)
            return {
                "status": "mock",
                "message": "Demo mode - replace with real API call",
                "output": output_file
            }
        
        # Submit ATA task
        print("\n📤 Submitting ATA task...")
        task_id = self._submit_task(audio_data, text, format, language)
        print(f"   Task ID: {task_id}")
        
        # Poll for completion
        print("   Waiting for processing...")
        result = self._wait_for_completion(task_id)
        
        # Download subtitle
        if result.get('status') == 'completed' and result.get('subtitle'):
            print(f"\n📥 Saving subtitle to: {output_file}")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result['subtitle'])
            print(f"✅ Done! Output: {output_file}")
            return {
                "status": "completed",
                "task_id": task_id,
                "output": output_file
            }
        else:
            print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
            return {
                "status": "failed",
                "task_id": task_id,
                "error": result.get('error')
            }
    
    def _submit_task(
        self,
        audio_data: str,
        text: str,
        format: str,
        language: str
    ) -> str:
        """Submit ATA task to API"""
        url = f"{self.api_base}{self.submit_path}"
        
        payload = {
            "app": {
                "appid": self.app_id
            },
            "audio": audio_data,
            "text": text,
            "format": format,
            "language": language
        }
        
        headers = {
            "Authorization": f"Bearer; {self.token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        return result.get('id')
    
    def _wait_for_completion(
        self,
        task_id: str,
        timeout: int = 300,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """Poll task status until completion"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                result = self._query_task(task_id)
                status = result.get('status')
                
                elapsed = int(time.time() - start_time)
                print(f"   Status: {status} ({elapsed}s)")
                
                if status == 'completed':
                    return result
                elif status == 'failed':
                    return {
                        "status": "failed",
                        "error": result.get('error', 'Unknown error')
                    }
                
                time.sleep(poll_interval)
                
            except Exception as e:
                print(f"   Query error: {e}")
                time.sleep(poll_interval)
        
        return {
            "status": "timeout",
            "error": f"Task did not complete within {timeout} seconds"
        }
    
    def _query_task(self, task_id: str) -> Dict[str, Any]:
        """Query task status"""
        url = f"{self.api_base}{self.query_path}"
        
        payload = {
            "id": task_id
        }
        
        headers = {
            "Authorization": f"Bearer; {self.token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def _create_mock_subtitle(self, output_file: str, text: str):
        """Create a mock subtitle file for demo mode"""
        lines = text.strip().split('\n')
        srt_content = ""
        
        for i, line in enumerate(lines, 1):
            start_time = (i - 1) * 2000  # 2 seconds per line
            end_time = i * 2000
            
            start_str = self._ms_to_srt_time(start_time)
            end_str = self._ms_to_srt_time(end_time)
            
            srt_content += f"{i}\n"
            srt_content += f"{start_str} --> {end_str}\n"
            srt_content += f"{line}\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(srt_content)
    
    def _ms_to_srt_time(self, ms: int) -> str:
        """Convert milliseconds to SRT time format"""
        hours = ms // 3600000
        minutes = (ms % 3600000) // 60000
        seconds = (ms % 60000) // 1000
        milliseconds = ms % 1000
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def main():
    parser = argparse.ArgumentParser(
        description='Volcengine ATA Subtitle Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 volc_ata.py --audio audio.wav --text subtitle.txt --output final.srt
  python3 volc_ata.py --audio audio.wav --text subtitle.txt --output final.ass --format ass
  python3 volc_ata.py --audio audio.wav --text subtitle.txt --output final.srt --app-id 123456 --token xxx
        """
    )
    
    parser.add_argument('--audio', required=True, help='Input audio file (WAV, 16kHz mono)')
    parser.add_argument('--text', required=True, help='Input text file (plain text)')
    parser.add_argument('--output', required=True, help='Output subtitle file')
    parser.add_argument('--format', default='srt', choices=['srt', 'ass'], help='Output format (default: srt)')
    parser.add_argument('--language', default='zh-CN', help='Language code (default: zh-CN)')
    parser.add_argument('--app-id', help='Volcengine App ID (overrides env/config)')
    parser.add_argument('--token', help='Volcengine API Token (overrides env/config)')
    parser.add_argument('--api-base', help='API base URL (overrides env/config)')
    parser.add_argument('--config', help='Config file path (default: ~/.volcengine_ata.conf)')
    
    args = parser.parse_args()
    
    # Create processor
    processor = VolcATASubtitle(
        app_id=args.app_id,
        token=args.token,
        api_base=args.api_base,
        config_file=args.config
    )
    
    # Generate subtitle
    try:
        result = processor.create_subtitle(
            audio_file=args.audio,
            text_file=args.text,
            output_file=args.output,
            format=args.format,
            language=args.language
        )
        
        print("\n📋 Result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
