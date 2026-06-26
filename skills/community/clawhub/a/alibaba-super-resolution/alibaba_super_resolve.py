#!/usr/bin/env python3
"""
Alibaba Cloud Super Resolution Tool (阿里云视频超分辨率)

Upscale low-resolution videos to higher resolution using Alibaba Cloud's video enhancement API.

Usage:
    python3 alibaba_super_resolve.py --input input.mp4 --output output.mp4
"""

import os
import sys
import json
import time
import io
import argparse
import requests
from typing import Optional, Dict, Any

# Import Alibaba Cloud SDK
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_videoenhan20200320.client import Client
from alibabacloud_videoenhan20200320.models import (
    SuperResolveVideoAdvanceRequest,
    GetAsyncJobResultRequest
)


class AlibabaSuperResolve:
    """Alibaba Cloud Video Super Resolution Processor"""
    
    def __init__(
        self,
        access_key_id: str = None,
        access_key_secret: str = None,
        endpoint: str = 'videoenhan.cn-shanghai.aliyuncs.com',
        region_id: str = 'cn-shanghai'
    ):
        # Load credentials from environment variables
        self.access_key_id = access_key_id or os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')
        self.access_key_secret = access_key_secret or os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
        
        if not self.access_key_id or not self.access_key_secret:
            print("⚠️  Warning: Alibaba Cloud credentials not configured")
            print("   Set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables")
            print("   Running in demo mode...\n")
        
        # Initialize client
        self.client = None
        if self.access_key_id and self.access_key_secret:
            config = Config(
                access_key_id=self.access_key_id,
                access_key_secret=self.access_key_secret,
                endpoint=endpoint,
                region_id=region_id
            )
            self.client = Client(config)
    
    def super_resolve_video(
        self,
        input_file: str,
        output_file: Optional[str] = None,
        bit_rate: int = 5,
        wait: bool = True,
        timeout: int = 1200
    ) -> Dict[str, Any]:
        """
        Upscale video using super resolution API
        
        Args:
            input_file: Path to input video file (local)
            output_file: Path to save output video file (optional)
            bit_rate: Bit rate for output (1-10, default: 5)
            wait: Whether to wait for completion (default: True)
            timeout: Timeout in seconds (default: 1200)
        
        Returns:
            Result dictionary with status and metadata
        """
        # Validate input
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        file_size = os.path.getsize(input_file) / (1024 * 1024)
        print(f"📤 Processing file: {input_file}")
        print(f"   File size: {file_size:.2f} MB")
        
        if file_size > 2000:
            raise ValueError("File exceeds 2GB limit. Use OSS URL for larger files.")
        
        # Demo mode
        if not self.client:
            print("⚠️  Running in demo mode (no API credentials)")
            print("   Simulating super resolution process...")
            time.sleep(3)
            
            if output_file:
                print(f"📥 Copying input to output (demo): {output_file}")
                import shutil
                shutil.copy(input_file, output_file)
            
            return {
                "status": "mock",
                "message": "Demo mode - replace with real API call",
                "input": input_file,
                "output": output_file
            }
        
        # Read file into memory
        print("   Loading file to memory...")
        with open(input_file, 'rb') as f:
            video_data = io.BytesIO(f.read())
        
        # Submit task
        print("\n📤 Submitting task to Alibaba Cloud...")
        request = SuperResolveVideoAdvanceRequest()
        request.video_url_object = video_data
        request.bit_rate = bit_rate
        
        runtime = RuntimeOptions()
        response = self.client.super_resolve_video_advance(request, runtime)
        result = response.body.to_map()
        
        job_id = result.get('RequestId')
        print(f"✅ Task submitted successfully")
        print(f"   Request ID: {job_id}")
        
        if not wait:
            return {
                "status": "submitted",
                "job_id": job_id,
                "input": input_file
            }
        
        # Wait for completion
        print(f"\n⌛ Waiting for processing (timeout: {timeout}s)...")
        final_result = self.wait_for_completion(job_id, timeout)
        
        # Download result
        if output_file and final_result.get('status') == 'succeeded' and final_result.get('output_url'):
            print(f"\n📥 Downloading result to: {output_file}")
            self._download_file(final_result['output_url'], output_file)
            print(f"✅ Done! Output: {output_file}")
            final_result['output'] = output_file
        
        return final_result
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a submitted job"""
        if not self.client:
            return {
                "status": "error",
                "error": "Client not initialized (no credentials)"
            }
        
        request = GetAsyncJobResultRequest()
        request.job_id = job_id
        runtime = RuntimeOptions()
        
        response = self.client.get_async_job_result_with_options(request, runtime)
        result = response.body.to_map()
        
        if 'Data' in result:
            job_data = result['Data']
            status = job_data.get('Status')
            
            # Normalize status
            if status == 'PROCESS_SUCCESS':
                status = 'succeeded'
            elif status == 'PROCESS_FAILED':
                status = 'failed'
            
            output_url = job_data.get('OutputUrl') or job_data.get('OutputFileUrl')
            
            # Parse Result field if available
            if not output_url and 'Result' in job_data:
                try:
                    result_json = json.loads(job_data['Result'])
                    output_url = result_json.get('VideoUrl')
                except:
                    pass
            
            return {
                "job_id": job_id,
                "status": status,
                "progress": job_data.get('Progress', 0),
                "output_url": output_url,
                "error": job_data.get('ErrorMessage') if status == 'failed' else None,
                "raw_data": job_data
            }
        
        return {
            "job_id": job_id,
            "status": "unknown",
            "raw_result": result
        }
    
    def wait_for_completion(
        self,
        job_id: str,
        timeout: int = 1200,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """Wait for job to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_job_status(job_id)
            current_status = status.get('status')
            elapsed = int(time.time() - start_time)
            
            print(f"   Status: {current_status} ({elapsed}s)", end='\r')
            
            if current_status == 'succeeded':
                print(f"\n✅ Processing completed!")
                if status.get('output_url'):
                    print(f"   Output URL: {status['output_url']}")
                return status
            
            elif current_status == 'failed':
                print(f"\n❌ Processing failed: {status.get('error', 'Unknown error')}")
                return status
            
            time.sleep(poll_interval)
        
        print(f"\n⚠️  Timeout: Task did not complete within {timeout} seconds")
        return {
            "job_id": job_id,
            "status": "timeout",
            "elapsed": elapsed
        }
    
    def _download_file(self, url: str, output_path: str):
        """Download file from URL to local path"""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"   Download progress: {progress:.1f}%", end='\r')
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Alibaba Cloud Video Super Resolution Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python3 alibaba_super_resolve.py --input input.mp4 --output output.mp4
  
  # Custom bit rate (higher = better quality)
  python3 alibaba_super_resolve.py --input input.mp4 --output output.mp4 --bit-rate 8
  
  # Submit and don't wait
  python3 alibaba_super_resolve.py --input input.mp4 --no-wait
  
  # Check job status
  python3 alibaba_super_resolve.py --status <JOB_ID>
  
  # Wait for job and download
  python3 alibaba_super_resolve.py --wait <JOB_ID> --output output.mp4
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--input', help='Input video file path')
    group.add_argument('--status', help='Get status of job ID')
    group.add_argument('--wait', help='Wait for job ID to complete')
    
    parser.add_argument('--output', help='Output video file path')
    parser.add_argument('--bit-rate', type=int, default=5, help='Bit rate (1-10, default: 5)')
    parser.add_argument('--no-wait', action='store_true', help='Do not wait for completion')
    parser.add_argument('--timeout', type=int, default=1200, help='Timeout in seconds (default: 1200)')
    parser.add_argument('--access-key-id', help='Alibaba Cloud Access Key ID (overrides env)')
    parser.add_argument('--access-key-secret', help='Alibaba Cloud Access Key Secret (overrides env)')
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = AlibabaSuperResolve(
        access_key_id=args.access_key_id,
        access_key_secret=args.access_key_secret
    )
    
    try:
        if args.status:
            # Get job status
            result = processor.get_job_status(args.status)
            print("\n📋 Job Status:")
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        
        elif args.wait:
            # Wait for job completion
            result = processor.wait_for_completion(args.wait, args.timeout)
            
            if args.output and result.get('status') == 'succeeded' and result.get('output_url'):
                print(f"\n📥 Downloading result to: {args.output}")
                processor._download_file(result['output_url'], args.output)
                print(f"✅ Done! Output: {args.output}")
                result['output'] = args.output
            
            print("\n📋 Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        
        else:
            # Process video
            result = processor.super_resolve_video(
                input_file=args.input,
                output_file=args.output,
                bit_rate=args.bit_rate,
                wait=not args.no_wait,
                timeout=args.timeout
            )
            
            print("\n📋 Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
