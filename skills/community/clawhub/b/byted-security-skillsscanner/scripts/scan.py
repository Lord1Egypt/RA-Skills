# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import sys
import time
import argparse
import requests
import zipfile
import tempfile
import shutil
import urllib.parse
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request

# Configuration Defaults
DEFAULT_BASE_URL = "http://127.0.0.1:8181/api/top/mana-open/cn-north-1/2025-01-01"
DEFAULT_REGION = "cn-north-1"
DEFAULT_SERVICE = "aisec"
DEFAULT_HOST = "https://open.volcengineapi.com"

# Scan Status Enum (mapped from API)
SCAN_STATUS_WAITING = "scanning"
SCAN_STATUS_RUNNING = "scanning"
SCAN_STATUS_SUCCESS = "success"
SCAN_STATUS_FAILED = "fail"
SCAN_STATUS_TIMEOUT = "timeout"


class Credentials:
    def __init__(self, ak, sk, service, region, session_token=""):
        self.ak = ak
        self.sk = sk
        self.access_key = ak
        self.secret_key = sk
        self.service = service
        self.region = region
        self.session_token = session_token


class SkillScanner:
    def __init__(self, ak: str, sk: str, region: str = DEFAULT_REGION, host: str = DEFAULT_HOST,
                 service: str = DEFAULT_SERVICE, base_url: str = "", session_token: str = "", user_id: str = ""):
        self.ak = ak
        self.sk = sk
        self.region = region
        self.service = service
        self.host = host.rstrip('/')
        self.user_id = user_id

        # Initialize credentials
        self.credentials = Credentials(ak, sk, service, region, session_token)

        # Build base path and URLs
        if base_url:
            self.base_url = base_url.rstrip('/')
            self.upload_url = f"{self.base_url}/UploadAndScanSkill"
            self.detail_url = f"{self.base_url}/GetSkillScanDetail"
        else:
            self.base_path = f"/api/top/{self.service}/{self.region}/2026-01-04"
            self.upload_url = f"{self.host}{self.base_path}/CreateSkill?Action=CreateSkill&Version=2026-01-04"
            self.detail_url = f"{self.host}{self.base_path}/GetSkillScanDetail?Action=GetSkillScanDetail&Version=2026-01-04"

        # Constants
        self.SCAN_STATUS_SUCCESS = SCAN_STATUS_SUCCESS
        self.SCAN_STATUS_FAIL = SCAN_STATUS_FAILED

    def _zip_directory(self, dir_path):
        """Zip a directory and return the path to the temporary zip file."""
        try:
            temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
            temp_zip.close()

            with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.startswith('.') or file.startswith('._'):
                            continue
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, dir_path)

                        if arcname.lower() == "skill.md":
                            arcname = "skill.md"
                        elif arcname.lower().endswith("/skill.md"):
                            arcname = arcname[:-len("/skill.md")] + "/skill.md"

                        while arcname.startswith('./') or arcname.startswith('/'):
                            arcname = arcname.lstrip('./')

                        zipf.write(file_path, arcname)

            return temp_zip.name
        except Exception as e:
            print(f"[Error] 压缩目录失败: {e}", file=sys.stderr)
            return None

    def _extract_data(self, response_json):
        """Extract Data from nested Result.Data structure."""
        if not isinstance(response_json, dict):
            return None

        # Handle { "Result": { "Data": { ... } } }
        if 'Result' in response_json and isinstance(response_json['Result'], dict):
            result = response_json['Result']
            if 'Data' in result:
                return result['Data']

        # Handle direct { "Data": { ... } } (if possible)
        if 'Data' in response_json:
            return response_json['Data']

        # Handle flat structure or other variations if needed
        return response_json

    def upload_and_scan(self, name: str, path: str, description: str = "Security scan"):
        """Upload skill zip file and start scan."""
        temp_zip_path = None
        file_to_upload = path

        try:
            # Expand ~ in path for user home directory
            path = os.path.expanduser(path)
            if not os.path.exists(path):
                return {"error": f"路径未找到: {path}"}

            # File preparation logic
            is_zip = path.lower().endswith('.zip') and os.path.isfile(path)
            
            if is_zip:
                # Use existing zip file
                file_to_upload = path
            elif os.path.isdir(path):
                # Zip directory
                # print(f"[*] Zipping directory: {path}")
                temp_zip_path = self._zip_directory(path)
                if not temp_zip_path:
                    return {"error": "目录压缩失败"}
                file_to_upload = temp_zip_path
            else:
                # File that is not a zip (could be other archive or single file)
                # print(f"[*] Processing non-zip file: {path}")
                
                # Check if it is a supported archive format
                try:
                    # Attempt to unpack to a temporary directory
                    extract_temp_dir = tempfile.mkdtemp()
                    success_unpack = False
                    
                    try:
                        # Try standard unpack_archive first (tar, gztar, zip, etc)
                        shutil.unpack_archive(path, extract_temp_dir)
                        success_unpack = True
                    except Exception:
                        pass
                    
                    if not success_unpack:
                        # Fallback for plain .gz file
                        if path.lower().endswith('.gz'):
                            try:
                                shutil.unpack_archive(path, extract_temp_dir, format="tar")
                                success_unpack = True
                            except Exception:
                                pass

                            if not success_unpack and not path.lower().endswith('.tar.gz'):
                                try:
                                    import gzip
                                    # Guess original filename: strip .gz
                                    original_name = os.path.basename(path)[:-3]
                                    output_file = os.path.join(extract_temp_dir, original_name)
                                    with gzip.open(path, 'rb') as f_in:
                                        with open(output_file, 'wb') as f_out:
                                            shutil.copyfileobj(f_in, f_out)
                                    success_unpack = True
                                except Exception as gz_err:
                                    shutil.rmtree(extract_temp_dir)
                                    raise ValueError(f"无法解压GZ文件: {gz_err}")

                    if not success_unpack:
                        shutil.rmtree(extract_temp_dir)
                        raise ValueError(f"不支持的归档格式或解压失败")

                    # If successful, re-zip the extracted content
                    temp_zip_path = self._zip_directory(extract_temp_dir)
                    shutil.rmtree(extract_temp_dir)

                    if not temp_zip_path:
                        return {"error": "重新压缩解压内容失败"}
                    file_to_upload = temp_zip_path

                except ValueError as ve:
                    # Explicit validation error
                    return {"error": f"文件格式无效: {str(ve)}"}
                except Exception as e:
                    # General error
                    return {"error": f"处理文件失败 '{os.path.basename(path)}': {str(e)}"}

            # Prepare multipart upload
            with open(file_to_upload, 'rb') as f:
                file_content = f.read()

            files = {
                'File': (os.path.basename(file_to_upload), file_content, 'application/zip')
            }
            data = [
                ('Name', name),
                ('Description', description),
                ('IntegrateType', 'file'),
                ('ScanNow', 'true')
            ]

            # Retry logic for upload
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Prepare the request to get headers/body for signing
                    req = requests.Request('POST', self.upload_url, files=files, data=data)
                    prepped = req.prepare()
                    
                    # Use SDK to sign
                    parsed_url = urllib.parse.urlparse(self.upload_url)
                    
                    v_request = Request()
                    v_request.method = 'POST'
                    v_request.host = parsed_url.netloc
                    v_request.path = parsed_url.path
                    v_request.query = dict(urllib.parse.parse_qsl(parsed_url.query))
                    v_request.headers = dict(prepped.headers)
                    v_request.headers['Host'] = parsed_url.netloc
                    v_request.body = prepped.body
                    SignerV4.sign(v_request, self.credentials)

                    if len(v_request.body) < 2000:
                        # Only show short bodies safely
                        print(f"Body Preview: {v_request.body}")
                    else:
                        print("Body Preview (too long): <multipart form>")

                    response = requests.post(self.upload_url, headers=v_request.headers, data=prepped.body, timeout=60)

                    try:
                        response.raise_for_status()
                        return response.json()
                    except requests.exceptions.HTTPError as e:
                        if response.status_code in [401, 403, 429] or response.status_code >= 500:
                            if attempt < max_retries - 1:
                                time.sleep(1 * (attempt + 1))  # Backoff
                                continue

                        try:
                            error_detail = response.json()
                        except:
                            error_detail = response.text
                        return {"error": f"上传失败: {str(e)}", "details": error_detail}

                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        time.sleep(1 * (attempt + 1))
                        continue
                    return {"error": f"上传失败 (网络错误): {str(e)}"}
                except Exception as e:
                    return {"error": f"上传失败 (未知错误): {str(e)}"}

            return {"error": "上传失败: 超过最大重试次数"}

        except Exception as e:
            return {"error": f"上传失败: {str(e)}"}
        finally:
            if temp_zip_path and os.path.exists(temp_zip_path):
                try:
                    os.unlink(temp_zip_path)
                except OSError:
                    pass

    def get_scan_detail(self, skill_id: str):
        """Poll for scan results."""
        payload = json.dumps({"SkillID": skill_id})

        # Max retries: 10 mins (20s * 30)
        max_retries = 30

        for i in range(max_retries):
            try:
                headers = {'Content-Type': 'application/json'}
                parsed_url = urllib.parse.urlparse(self.detail_url)

                v_request = Request()
                v_request.method = 'POST'
                v_request.host = parsed_url.netloc
                v_request.path = parsed_url.path
                v_request.query = dict(urllib.parse.parse_qsl(parsed_url.query))
                v_request.headers = headers
                v_request.headers['Host'] = parsed_url.netloc
                v_request.body = payload.encode('utf-8') if isinstance(payload, str) else payload

                SignerV4.sign(v_request, self.credentials)

                response = requests.post(self.detail_url, data=payload, headers=v_request.headers, timeout=60)
                response.raise_for_status()
                result_json = response.json()

                scan_data = self._extract_data(result_json)
                if not scan_data:
                    time.sleep(5)
                    continue

                status = scan_data.get('ScanStatus')

                if status == self.SCAN_STATUS_SUCCESS:
                    return scan_data
                elif status == self.SCAN_STATUS_FAIL:
                    return {"error": f"扫描失败: {status}", "details": scan_data.get('ScanErrMsg')}

                # Waiting/Running
                time.sleep(20)

            except Exception as e:
                time.sleep(5)

        return {"error": "等待扫描结果超时"}


def main():
    parser = argparse.ArgumentParser(description="Scan OpenClaw skills via Mana Open API or Volcengine Public Cloud.")
    parser.add_argument("--name", required=True, help="Name of the skill")
    parser.add_argument("--path", required=True, help="Path to the skill directory or zip file")

    args = parser.parse_args()

    # Read configuration from environment variables
    base_url = os.environ.get("SCAN_BASE_URL", "")
    ak = os.environ.get("VOLC_ACCESS_KEY") or os.environ.get("VOLC_ACCESSKEY") or os.environ.get("SCAN_AK")
    sk = os.environ.get("VOLC_SECRET_KEY") or os.environ.get("VOLC_SECRETKEY") or os.environ.get("SCAN_SK")
    region = os.environ.get("VOLC_REGION", DEFAULT_REGION)
    host = os.environ.get("SCAN_SERVICE_HOST", DEFAULT_HOST)
    service = os.environ.get("VOLC_SERVICE", DEFAULT_SERVICE)

    if not ak or not sk:
        if base_url and "127.0.0.1" not in base_url and "localhost" not in base_url:
            print(json.dumps([{"error": "Missing VOLC_ACCESS_KEY or VOLC_SECRET_KEY environment variables"}], indent=2))
            return
        else:
            ak = ak or "test_ak"
            sk = sk or "test_sk"
            base_url = base_url or DEFAULT_BASE_URL

    # Initialize scanner with public cloud or local config
    if base_url:
        scanner = SkillScanner(ak, sk, region, base_url=base_url)
    else:
        scanner = SkillScanner(ak, sk, region, host, service)

    # 1. Upload and start scan
    upload_result = scanner.upload_and_scan(args.name, args.path)

    if "error" in upload_result:
        print(json.dumps([upload_result], indent=2))
        return

    # Extract SkillID
    upload_data = scanner._extract_data(upload_result)
    if not upload_data:
        skill_id = upload_result.get("SkillID")
    else:
        skill_id = upload_data.get("SkillID")

    if not skill_id:
        print(json.dumps([{"error": "No SkillID returned from upload", "raw": upload_result}], indent=2))
        return

    # 2. Get scan details
    scan_result = scanner.get_scan_detail(skill_id)

    # Wrap in list for consistency
    print(json.dumps([scan_result], indent=2))


if __name__ == "__main__":
    main()
