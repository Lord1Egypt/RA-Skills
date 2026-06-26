#!/usr/bin/env python3
"""
DataWorks Task Instance Log Fetcher using Official Alibaba Cloud SDK

Usage:
    python3 fetch_instance_log.py <instance_id> [options]
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from alibabacloud_credentials.client import Client as CredentialClient
    from alibabacloud_dataworks_public20240518.client import Client as DataWorksClient
    from alibabacloud_tea_openapi import models as open_api_models
    from alibabacloud_dataworks_public20240518 import models as dataworks_models
    from alibabacloud_tea_util import models as util_models
except ImportError:
    print("❌ Alibaba Cloud SDK not installed", file=sys.stderr)
    print("\nInstall with:", file=sys.stderr)
    print("  pip3 install alibabacloud_dataworks_public20240518 alibabacloud_credentials", file=sys.stderr)
    sys.exit(1)


def load_credentials():
    """Load Alibaba Cloud credentials from environment or config file"""
    import os
    
    # Try environment variables first
    access_key = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
    access_secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    
    if access_key and access_secret:
        return access_key, access_secret
    
    # Try config file
    config_path = Path.home() / '.alibabacloud' / 'credentials'
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            return config.get('access_key_id'), config.get('access_key_secret')
        except Exception:
            pass
    
    # Try current directory credentials.json
    config_path = Path('credentials.json')
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            return config.get('access_key_id'), config.get('access_key_secret')
        except Exception:
            pass
    
    return None, None


def fetch_log(instance_id, region='cn-hangzhou', access_key=None, access_secret=None):
    """
    Fetch task instance log from DataWorks API using official SDK
    
    API: https://api.aliyun.com/api/dataworks-public/2024-05-18/GetTaskInstanceLog
    """
    # Load credentials if not provided
    if not access_key or not access_secret:
        access_key, access_secret = load_credentials()
        if not access_key or not access_secret:
            print("❌ Error: Alibaba Cloud credentials not found", file=sys.stderr)
            print("\nPlease set credentials using one of these methods:", file=sys.stderr)
            print("  1. Environment variables:", file=sys.stderr)
            print("     export ALIBABA_CLOUD_ACCESS_KEY_ID=your_key", file=sys.stderr)
            print("     export ALIBABA_CLOUD_ACCESS_KEY_SECRET=your_secret", file=sys.stderr)
            print("  2. Config file: ~/.alibabacloud/credentials", file=sys.stderr)
            print("  3. Local file: credentials.json", file=sys.stderr)
            return None
    
    try:
        # Create credential
        os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'] = access_key
        os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'] = access_secret
        credential = CredentialClient()
        
        # Create client config
        config = open_api_models.Config(credential=credential)
        config.endpoint = f'dataworks.{region}.aliyuncs.com'
        
        # Create client
        client = DataWorksClient(config)
        
        # Create request - Note: parameter is 'id' not 'InstanceId'
        request = dataworks_models.GetTaskInstanceLogRequest(id=int(instance_id))
        
        # Set runtime options
        runtime = util_models.RuntimeOptions()
        
        # Send request
        response = client.get_task_instance_log_with_options(request, runtime)
        
        # Convert response to dict
        return response.to_map()
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if hasattr(e, 'data') and e.data:
            print(f"   Recommend: {e.data.get('Recommend', '')}", file=sys.stderr)
        return None


def format_log_output(response, verbose=False):
    """Format API response for display"""
    if not response:
        return None
    
    # Navigate response structure
    body = response.get('body', {})
    data = body.get('Data', {})
    
    log_content = data.get('LogContent', '')
    instance_status = data.get('InstanceStatus', 'Unknown')
    cycle_time = data.get('CycleTime', 'N/A')
    
    output = []
    output.append("=" * 60)
    output.append("📋 DataWorks Task Instance Log")
    output.append("=" * 60)
    output.append(f"Status: {instance_status}")
    output.append(f"Cycle Time: {cycle_time}")
    output.append("-" * 60)
    output.append("Log Content:")
    output.append("-" * 60)
    
    if log_content:
        if verbose:
            output.append(log_content)
        else:
            lines = log_content.split('\n')
            if len(lines) > 50:
                output.append(f"... ({len(lines) - 50} lines omitted)")
                output.extend(lines[-50:])
            else:
                output.extend(lines)
    else:
        output.append("(No log content available)")
    
    output.append("=" * 60)
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch DataWorks task instance log using official SDK",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 12345678
  %(prog)s 12345678 --region cn-shanghai
  %(prog)s 12345678 --json
  %(prog)s 12345678 --verbose
        """
    )
    
    parser.add_argument("instance_id", help="Task instance ID")
    parser.add_argument("--region", "-r", default='cn-hangzhou',
                       help="Alibaba Cloud region (default: cn-hangzhou)")
    parser.add_argument("--access-key", help="Access Key ID")
    parser.add_argument("--access-secret", help="Access Key Secret")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show full log (default: last 50 lines)")
    
    args = parser.parse_args()
    
    # Fetch log
    response = fetch_log(
        args.instance_id,
        region=args.region,
        access_key=args.access_key,
        access_secret=args.access_secret
    )
    
    if response is None:
        sys.exit(1)
    
    # Output
    if args.json:
        print(json.dumps(response, indent=2, ensure_ascii=False, default=str))
    else:
        formatted = format_log_output(response, args.verbose)
        if formatted:
            print(formatted)


if __name__ == "__main__":
    main()
