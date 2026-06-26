import os
import json
import requests
import re
from pathlib import Path
from datetime import datetime


class MinimaxClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        self.key_source = "MINIMAX_API_KEY"
        if not self.api_key:
            self.api_key = self._get_key_from_openclaw()
            self.key_source = "~/.openclaw/openclaw.json (MiniMax Token Plan API Key)"

        if not self.api_key:
            raise ValueError(
                "MiniMax Token Plan API Key not found. Configure MINIMAX_API_KEY or add the MiniMax Token Plan key to ~/.openclaw/openclaw.json."
            )

        self.base_url = "https://api.minimaxi.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _get_key_from_openclaw(self):
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        if not os.path.exists(config_path):
            return None
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                providers = config.get("models", {}).get("providers", {})
                for name, cfg in providers.items():
                    if "minimax" in name.lower():
                        return cfg.get("apiKey")
        except Exception:
            return None
        return None

    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def download_file(self, file_id: str) -> bytes:
        """Download file content from files/retrieve_content endpoint.

        This endpoint returns binary audio data, not JSON.
        """
        url = f"{self.base_url}/files/retrieve_content?file_id={file_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content

    def get_plan_remains(self):
        """Query official Token Plan remains API."""
        url = "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"
        response = requests.get(url, headers=self.headers, timeout=30)
        return response.json()

    def format_plan_remains_report(self):
        """Format official Token Plan remains response for terminal display.

        Important: field semantics are displayed conservatively in raw form until
        manually validated against the official Token Plan web console.
        """
        try:
            data = self.get_plan_remains()
            rows = data.get("model_remains", [])
            if not rows:
                return "\n[Token Plan 实时额度]\n未返回额度数据。\n"

            def ms_to_local(ms):
                try:
                    return datetime.fromtimestamp(ms / 1000).strftime("%m-%d %H:%M")
                except Exception:
                    return str(ms)

            report = "\n[Token Plan 实时额度 · 原始字段模式]\n"
            report += f"Key 来源: {self.key_source}\n"
            report += "⚠️ 当前仅展示 remains 接口原始字段；字段业务含义尚未与官方后台页面完成交叉验证，请勿直接把 usage_count 解释为‘已用’或把 total-usage 解释为‘剩余’。\n"
            for row in rows:
                model_name = row.get("model_name", "unknown")
                start = ms_to_local(row.get("start_time", 0))
                end = ms_to_local(row.get("end_time", 0))
                weekly_start = ms_to_local(row.get("weekly_start_time", 0))
                weekly_end = ms_to_local(row.get("weekly_end_time", 0))
                report += (
                    f"- {model_name}\n"
                    f"  current_interval_total_count: {row.get('current_interval_total_count', 0)}\n"
                    f"  current_interval_usage_count: {row.get('current_interval_usage_count', 0)}\n"
                    f"  remains_time(ms): {row.get('remains_time', 0)}\n"
                    f"  interval: {start} ~ {end}\n"
                    f"  current_weekly_total_count: {row.get('current_weekly_total_count', 0)}\n"
                    f"  current_weekly_usage_count: {row.get('current_weekly_usage_count', 0)}\n"
                    f"  weekly_remains_time(ms): {row.get('weekly_remains_time', 0)}\n"
                    f"  weekly_interval: {weekly_start} ~ {weekly_end}\n"
                )
            return report
        except Exception as e:
            return f"\n[Token Plan 实时额度]\n查询失败：{e}\n"

    def _load_costs(self):
        with open(os.path.join(os.path.dirname(__file__), "../references/costs.json"), 'r') as f:
            return json.load(f)

    def _is_text_model(self, model_id):
        model = (model_id or "").lower()
        return model.startswith("m2") or "minimax-m2" in model or model == "m2-her"

    def _is_non_text_model(self, model_id):
        model = (model_id or "").lower()
        prefixes = [
            "image-", "speech-", "async-speech-", "music-", "minimax-hailuo", "voice-"
        ]
        return any(model.startswith(p) for p in prefixes)

    def get_budget_report(self, model_id, text_len=0):
        try:
            costs = self._load_costs()
            rolling_hours = costs.get("rolling_window_hours", 5)
            default_plan = costs.get("default_plan", "Plus-Speed")
            plan_limit = costs["token_plan"].get(default_plan, 1500)

            model_lower = model_id.lower()
            if model_lower.startswith("speech-"):
                generations = max(1, (text_len + 999) // 1000)
                unit_cost = costs["models"].get(model_id, 600)
                estimated = generations * unit_cost
                basis = f"{unit_cost} 次请求/每次语音生成（单次上限 1000 字符）"
            elif model_lower.startswith("async-speech-"):
                generations = max(1, (text_len + 999) // 1000)
                unit_cost = costs["models"].get(model_id, 450)
                estimated = generations * unit_cost
                basis = f"{unit_cost} 次请求/每次异步语音生成（单次上限 1000 字符）"
            else:
                unit_cost = costs["models"].get(model_id, 1)
                estimated = unit_cost
                basis = f"{unit_cost} 次请求/次"

            report = "\n[Token Plan 预估]\n"
            report += f"模型: {model_id}\n"
            report += f"Key 来源: {self.key_source}\n"
            report += f"预计消耗: {estimated:.0f} 次请求\n"
            report += f"计费依据: {basis}\n"

            if self._is_text_model(model_id):
                report += f"额度规则: 文本模型采用 {rolling_hours} 小时滚动窗口\n"
                report += f"默认参考套餐上限: {default_plan} = {plan_limit} 次请求/{rolling_hours}小时\n"
                if estimated > plan_limit:
                    report += "⚠️ 警告: 本次任务预计消耗超过默认参考套餐窗口上限，可能触发额度不足。\n"
                elif estimated >= plan_limit * 0.5:
                    report += "💡 提示: 本次任务属于较高消耗操作，建议确认当前窗口余量。\n"
                report += "提示: 文本模型触顶后可等待滚动窗口恢复，或改用按量计费 API Key。\n"
            elif self._is_non_text_model(model_id):
                report += "额度规则: 非文本模型采用每日配额，每日自动重置\n"
                report += "提示: 若当天配额触顶，可等待次日重置，或改用按量计费 API Key。\n"
            else:
                report += "额度规则: 请以官方 Token Plan 文档和实时额度查询为准。\n"

            report += "建议: 如需实时确认余量，先调用 Token Plan remains 接口。\n"
            return report
        except Exception as e:
            return f"\n[Token Plan 预估]\n无法读取套餐信息：{e}\n"

    def print_saved_result(self, filepath, media_type, project=None):
        print("✅ 生成完成")
        print(f"类型: {media_type}")
        print(f"保存位置: {filepath}")
        if project:
            print(f"项目目录: {project}")
        print("提示: 如需长期管理，建议后续按项目整理到明确目录中。")


def get_standard_path(modality, project=None, prompt_slug="", output_dir=None):
    env_output = os.environ.get("MINIMAX_OUTPUT_DIR")
    cwd = Path(os.getcwd())
    workspace_output = cwd / "workspace" / "03-Resources" / "minimax-output"
    fallback_output = cwd / "outputs" / "minimax"

    if output_dir:
        output_hub = Path(output_dir).expanduser()
    elif env_output:
        output_hub = Path(env_output).expanduser()
    elif (cwd / "workspace").is_dir():
        output_hub = workspace_output
    else:
        output_hub = fallback_output

    modality_map = {
        "IMG": "Images",
        "VID": "Videos",
        "TTS": "Speech",
        "MSC": "Music"
    }

    sub_folder = modality_map.get(modality, "Other")
    target_dir = output_hub / project / sub_folder if project else output_hub / sub_folder
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_slug = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '-', prompt_slug[:30]).strip('-').lower()
    filename_base = f"{timestamp}_{modality}_{clean_slug}" if clean_slug else f"{timestamp}_{modality}"

    return str(target_dir), filename_base
