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

import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))  # 添加父目录
import argparse
import logging
from typing import Dict, Any

from scripts.client.volc_open_api_client import request
from scripts.config.config import semi_managed_region_endpoint_map, load_emr_skill_config

logger = logging.getLogger(__name__)

skill_cfg = load_emr_skill_config()
EMR_AGENT_ACTIVATE_DOC_URL = os.getenv(
    "EMR_AGENT_ACTIVATE_DOC_URL",
    "https://console.volcengine.com/emr",
)

def _request_emr_agent_api(action: str, body: Dict[str, Any] = None):
    body = body or {}
    region = skill_cfg.region
    endpoint = semi_managed_region_endpoint_map.get(region, None)
    if not endpoint:
        raise ValueError(f"endpoint not found for region: {region}")
    result = request(service="emr", action=action,
                     version="2025-10-15", region=region,
                     endpoint=endpoint, method="POST",
                     query={}, body=body)
    logger.info(
        f"manage_emr_agent(action={action},region={region}, body={body}) => {result}")
    return result

def response_convert(action: str, response: Dict[str, Any]) -> Any:
    if not response:
        return {}
    match action:
        case "ListTradeInstances":
            instances = response.get("Instances") or []
            if len(instances) == 0:
                return {
                    "Opened": False,
                    "Available": False,
                    "Status": "not_opened",
                    "Message": "当前账号在当前 Region 下未开通 EMR Agent，请到控制台先开通后再试。",
                    "DocumentUrl": EMR_AGENT_ACTIVATE_DOC_URL,
                    "Instances": [],
                }
            if len(instances) == 1:
                instance = instances[0]
                status = (instance.get("Status") or "").lower()
                message = {
                    "active": "EMR Agent 实例已开通，可正常使用。",
                    "overdue": "EMR Agent 实例已欠费，请先续费后再试。",
                    "deleted": "EMR Agent 实例已删除，请重新开通。",
                }.get(status, f"EMR Agent 实例当前状态为 {status or 'unknown'}。")
                return {
                    "Opened": True,
                    "Available": status == "active",
                    "Status": status or "unknown",
                    "Message": message,
                    "DocumentUrl": EMR_AGENT_ACTIVATE_DOC_URL if status in {"overdue", "deleted"} else "",
                    "Instance": instance,
                    "Instances": instances,
                }
            return {
                "Opened": True,
                "Available": any((item.get("Status") or "").lower() == "active" for item in instances),
                "Status": "multiple_instances",
                "Message": "当前账号在当前 Region 下返回了多个 EMR Agent 实例，请人工确认实例状态。",
                "DocumentUrl": EMR_AGENT_ACTIVATE_DOC_URL,
                "Instances": instances,
            }
        case _:
            return response

def get_emr_agent_availability() -> Any:
    result = _request_emr_agent_api("ListTradeInstances", {})
    if not result.get("Result"):
        return result.get("ResponseMetadata")
    return response_convert("ListTradeInstances", result.get("Result"))

def ensure_emr_agent_available() -> Any:
    status = get_emr_agent_availability()
    if status.get("Available") is True:
        return None
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return status

def manage_emr_agent(action: str,
                     body: Dict[str, Any] = None):
    body = body or {}
    if action != "ListTradeInstances":
        unavailable = ensure_emr_agent_available()
        if unavailable:
            return unavailable
    result = _request_emr_agent_api(action, body)
    if not result.get("Result"):
        print(json.dumps(result.get("ResponseMetadata"), indent=2))
        return result.get("ResponseMetadata")
    res = response_convert(action, result.get("Result"))
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return res

def fix_args():
    args = sys.argv
    fix_args = []
    param_with_space = ""
    for arg in args:
        if arg.startswith("--"):
            if param_with_space:
                fix_args.append(param_with_space)
                param_with_space = ""
            fix_args.append(arg)
        else:
            param_with_space = param_with_space + arg
    if param_with_space:
        fix_args.append(param_with_space)
    sys.argv = fix_args

def _main():
    fix_args()
    parser = argparse.ArgumentParser(prog="emr_agent_manager.py")
    parser.add_argument("--action", required=True)
    parser.add_argument("--body", required=True)
    args = parser.parse_args()
    return manage_emr_agent(args.action, json.loads(args.body))

if __name__ == "__main__":
    _main()
