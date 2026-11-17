"""
VLM Visual QA — 可选叠加层，不替代启发式验证。

在 OpenCV 验证通过后，可选调用 VLM（视觉语言模型）做语义级 QA：
  - 角色图是否与 character_card 描述一致
  - 首帧构图是否符合 shot description
  - 场景图是否匹配 scene_card 描述

仅当 `--vlm` 或 `--premium` 参数指定时启用。
VLM 结果作为 extra 字段叠加到验证结果中，不影响原有 pass/fail。
"""

import base64, json, os, sys
from typing import Any, Optional

from modules.config import _script_path, _log, get


# ── 默认配置 ──────────────────────────────────────────

_DEFAULT_VLM_CONFIG = {
    "api_base": "https://api.openai.com/v1",
    "model": "gpt-4o-mini",
    "max_tokens": 512,
    "temperature": 0.1,
}


# ── VLM 客户端 ────────────────────────────────────────

class VlmClient:
    """通用 OpenAI 兼容 VLM 客户端。

    需在 config/config.toml 中配置 [vlm] 段：
        [vlm]
        api_key = "sk-..."              # VLM provider 的 API Key
        api_base = "https://api.openai.com/v1"  # 可省略（默认 OpenAI）
        model = "gpt-4o-mini"                      # 可省略

    支持任意 OpenAI 兼容的 chat/completions API（GPT-4o / Gemini / Qwen-VL 等）。
    """

    def __init__(self, config: dict | None = None):
        cfg = {**_DEFAULT_VLM_CONFIG, **(config or {})}
        self.api_base = cfg.get("api_base", _DEFAULT_VLM_CONFIG["api_base"]).rstrip("/")
        self.api_key = cfg.get("api_key", "") or os.environ.get("VLM_API_KEY", "")
        self.model = cfg.get("model", _DEFAULT_VLM_CONFIG["model"])
        self.max_tokens = cfg.get("max_tokens", _DEFAULT_VLM_CONFIG["max_tokens"])
        self.temperature = cfg.get("temperature", _DEFAULT_VLM_CONFIG["temperature"])
        self._session = None

    @classmethod
    def from_config(cls, skill_root: str) -> Optional["VlmClient"]:
        """从配置读取 VLM 设置。需在 [vlm] 段配置 api_key，否则静默跳过。"""
        try:
            from _shared_tools import load_config
            cfg = load_config(skill_root)
            vlm_cfg = cfg.get("vlm", {})
            if not vlm_cfg or not vlm_cfg.get("api_key"):
                _log("  [VLM] ⏭️ 未配置 [vlm] api_key，跳过 VLM QA")
                _log("  [VLM] 在 config/config.toml 中添加 [vlm] 段即可启用：")
                _log("  [VLM]   [vlm]")
                _log("  [VLM]   api_key = \"sk-...\"")
                _log("  [VLM]   model = \"gpt-4o-mini\"")
                return None
            return cls(vlm_cfg)
        except Exception as e:
            _log(f"  [VLM] ⏭️ 配置读取失败: {e}")
            return None

    def _ensure_session(self):
        """延迟导入 requests 并创建 session。"""
        if self._session is not None:
            return
        import requests
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def _encode_image(self, image_path: str) -> str | None:
        """读取图片并编码为 base64 data URI。"""
        if not os.path.isfile(image_path):
            _log(f"  [VLM] ⚠️ 图片不存在: {image_path}")
            return None
        try:
            with open(image_path, "rb") as f:
                data = f.read()
            ext = os.path.splitext(image_path)[1].lower().lstrip(".")
            mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                    "webp": "image/webp"}.get(ext, "image/png")
            return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"
        except Exception as e:
            _log(f"  [VLM] ⚠️ 图片编码失败: {e}")
            return None

    def ask(self, prompt: str, image_path: str | None = None,
            system: str = "") -> dict:
        """向 VLM 提问，支持可选图片。

        Args:
            prompt: 用户提示词（问题）。
            image_path: 可选图片路径。
            system: 系统提示词。

        Returns:
            {"success": bool, "content": str, "error": str|None}
        """
        self._ensure_session()
        if self._session is None:
            return {"success": False, "content": "", "error": "requests 未安装"}

        messages: list[dict] = []
        if system:
            messages.append({"role": "system", "content": system})

        user_content: list[dict] = []
        if image_path:
            b64 = self._encode_image(image_path)
            if b64 is None:
                return {"success": False, "content": "", "error": "图片编码失败"}
            user_content.append({
                "type": "image_url",
                "image_url": {"url": b64, "detail": "low"},
            })
        user_content.append({"type": "text", "text": prompt})
        messages.append({"role": "user", "content": user_content})

        try:
            r = self._session.post(
                f"{self.api_base}/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                },
                timeout=60,
            )
            if r.status_code != 200:
                return {
                    "success": False,
                    "content": "",
                    "error": f"HTTP {r.status_code}: {r.text[:200]}",
                }
            data = r.json()
            content = data["choices"][0]["message"]["content"]
            return {"success": True, "content": content, "error": None}
        except Exception as e:
            return {"success": False, "content": "", "error": str(e)}


# ── QA 检查函数 ───────────────────────────────────────

def _parse_vlm_verdict(content: str) -> dict:
    """解析 VLM 返回的文本，提取判定和理由。

    VLM 应该返回形如：
      PASS|FAIL
      理由：...

    或包含 JSON：
      {"verdict": "PASS"|"FAIL"|"UNCERTAIN", "reason": "..."}
    """
    content = content.strip()
    # 尝试 JSON 解析
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "verdict" in data:
            return {
                "passed": data["verdict"].upper() == "PASS",
                "uncertain": data["verdict"].upper() == "UNCERTAIN",
                "reason": data.get("reason", ""),
            }
    except (json.JSONDecodeError, ValueError):
        pass

    # 文本解析：看第一行是不是 PASS/FAIL
    first_line = content.split("\n")[0].strip().upper()
    verdict = "UNCERTAIN"
    if first_line.startswith("PASS"):
        verdict = "PASS"
    elif first_line.startswith("FAIL"):
        verdict = "FAIL"

    return {
        "passed": verdict == "PASS",
        "uncertain": verdict == "UNCERTAIN",
        "reason": content[:300],
    }


def check_character_image(
    image_path: str,
    char_name: str,
    char_description: str,
    view: str,
    client: VlmClient,
) -> dict:
    """检查角色图是否与 character_card 描述一致。

    返回:
        {"passed": bool, "uncertain": bool, "reason": str,
         "checks": {"view_match": bool|None, "appearance_match": bool|None}}
    """
    prompt = (
        f"请判断这张图片是否符合以下角色描述，只回答 PASS 或 FAIL 然后换行写理由。\n\n"
        f"角色名: {char_name}\n"
        f"视图: {view}\n"
        f"描述: {char_description}\n\n"
        f"检查点：\n"
        f"1. 人物服饰、发型、体型是否与描述一致\n"
        f"2. 如果是 {view} 视图（正面/侧面/背面/面部），是否匹配该视角\n"
        f"3. 如果视图是 face（面部特写），检查面部特征是否与描述一致\n\n"
        f"格式:\n"
        f"PASS\n"
        f"理由：...\n"
        f"或者\n"
        f"FAIL\n"
        f"理由：..."
    )
    system = "你是一个严格的视觉质量检查员。请基于图片内容客观判断，不要脑补不存在的信息。"
    result = client.ask(prompt, image_path=image_path, system=system)

    if not result["success"]:
        return {"passed": False, "uncertain": True, "reason": result["error"],
                "checks": {"view_match": None, "appearance_match": None}}

    verdict = _parse_vlm_verdict(result["content"])
    return {
        "passed": verdict["passed"],
        "uncertain": verdict["uncertain"],
        "reason": verdict["reason"],
        "checks": {"view_match": None, "appearance_match": None},
    }


def check_first_frame(
    image_path: str,
    shot: dict,
    client: VlmClient,
) -> dict:
    """检查首帧图是否匹配 shot description。

    返回:
        {"passed": bool, "uncertain": bool, "reason": str,
         "checks": {"composition_match": bool|None, "mood_match": bool|None}}
    """
    desc = shot.get("description", "")
    camera = shot.get("camera", "")
    mood = shot.get("mood", "")
    characters = shot.get("characters", [])

    prompt = (
        f"请判断这张首帧图是否符合以下镜头描述，只回答 PASS 或 FAIL 然后换行写理由。\n\n"
        f"镜头描述: {desc}\n"
        f"运镜: {camera}\n"
        f"情绪: {mood}\n"
        f"角色: {', '.join(characters) if characters else '无'}\n\n"
        f"检查点：\n"
        f"1. 画面构图是否与描述匹配（景别、人物位置、空间关系）\n"
        f"2. 情绪氛围（光线、色调）是否与描述的情绪一致\n"
        f"3. 主要角色是否出现在画面中\n\n"
        f"格式:\n"
        f"PASS\n"
        f"理由：...\n"
        f"或者\n"
        f"FAIL\n"
        f"理由：..."
    )
    system = "你是一个严格的视觉质量检查员。请基于图片内容客观判断，不要脑补不存在的信息。"
    result = client.ask(prompt, image_path=image_path, system=system)

    if not result["success"]:
        return {"passed": False, "uncertain": True, "reason": result["error"],
                "checks": {"composition_match": None, "mood_match": None}}

    verdict = _parse_vlm_verdict(result["content"])
    return {
        "passed": verdict["passed"],
        "uncertain": verdict["uncertain"],
        "reason": verdict["reason"],
        "checks": {"composition_match": None, "mood_match": None},
    }


def check_scene_image(
    image_path: str,
    scene_name: str,
    scene_description: str,
    client: VlmClient,
) -> dict:
    """检查场景图是否匹配 scene_card 描述。

    返回:
        {"passed": bool, "uncertain": bool, "reason": str}
    """
    prompt = (
        f"请判断这张场景图是否符合以下描述，只回答 PASS 或 FAIL 然后换行写理由。\n\n"
        f"场景名: {scene_name}\n"
        f"描述: {scene_description}\n\n"
        f"检查点：\n"
        f"1. 画面中的场景类型（室内/室外/战斗/城镇等）是否与描述一致\n"
        f"2. 场景应该没有人物（除非描述中明确包含人物）\n"
        f"3. 光线、色调、氛围是否匹配\n\n"
        f"格式:\n"
        f"PASS\n"
        f"理由：...\n"
        f"或者\n"
        f"FAIL\n"
        f"理由：..."
    )
    system = "你是一个严格的视觉质量检查员。请基于图片内容客观判断，不要脑补不存在的信息。"
    result = client.ask(prompt, image_path=image_path, system=system)

    if not result["success"]:
        return {"passed": False, "uncertain": True, "reason": result["error"]}

    verdict = _parse_vlm_verdict(result["content"])
    return {
        "passed": verdict["passed"],
        "uncertain": verdict["uncertain"],
        "reason": verdict["reason"],
    }


# ── 批量运行入口 ──────────────────────────────────────

def run_vlm_qa(project: str, skill_root: str,
               check_characters: bool = True,
               check_first_frames: bool = True,
               check_scenes: bool = True) -> dict:
    """批量运行 VLM QA，返回汇总结果。

    Returns:
        {
            "characters": [{"name": str, "passed": bool, ...}, ...],
            "first_frames": [{"shot_id": int, "passed": bool, ...}, ...],
            "scenes": [{"name": str, "passed": bool, ...}, ...],
            "summary": {"total": int, "passed": int, "failed": int, "uncertain": int},
        }
    """
    client = VlmClient.from_config(skill_root)
    if client is None:
        return {"characters": [], "first_frames": [], "scenes": [],
                "summary": {"total": 0, "passed": 0, "failed": 0, "uncertain": 0}}

    script = {}
    sp = _script_path(project)
    if os.path.isfile(sp):
        with open(sp, "r", encoding="utf-8") as f:
            script = json.load(f)

    results: list[dict] = []
    char_dir = os.path.join(project, "images", "characters")
    scene_dir = os.path.join(project, "images", "scenes")
    storyboard_dir = os.path.join(project, "images", "storyboard")

    # 角色 QA
    if check_characters:
        chars = script.get("character_cards", [])
        for c in chars:
            name = c.get("name", "?")
            desc = c.get("appearance", "") or c.get("description", "")
            for view in ("front", "face", "side", "back"):
                img = os.path.join(char_dir, f"{name.replace(' ', '_')}_{view}.png")
                if not os.path.isfile(img):
                    continue
                _log(f"  [VLM] 检查角色: {name} ({view})...")
                r = check_character_image(img, name, desc, view, client)
                r["name"] = name
                r["view"] = view
                r["image"] = img
                results.append(r)

    # 首帧图 QA
    if check_first_frames:
        shots = script.get("shots", [])
        for s in shots:
            sid = s["id"]
            # 支持多种命名模式
            patterns = [
                f"shot_{sid:02d}_first_frame*.png",
                f"shot_{sid:02d}_first_frame.png",
            ]
            img = None
            import glob
            for pat in patterns:
                matches = glob.glob(os.path.join(storyboard_dir, pat))
                if matches:
                    img = matches[0]
                    break
            if not img:
                continue
            _log(f"  [VLM] 检查首帧: shot_{sid:02d}...")
            r = check_first_frame(img, s, client)
            r["shot_id"] = sid
            r["image"] = img
            results.append(r)

    # 场景 QA
    if check_scenes:
        scenes = script.get("scene_cards", [])
        for s in scenes:
            name = s.get("name", "?")
            desc = s.get("description", "")
            safe_name = name.replace(" ", "_").replace("/", "_")
            patterns = [
                f"{safe_name}_*.png",
                f"{safe_name}.png",
            ]
            images = []
            import glob
            for pat in patterns:
                images.extend(sorted(glob.glob(os.path.join(scene_dir, pat))))
            for img in images[:3]:  # 最多检查 3 张
                view = os.path.basename(img).replace(".png", "").split("_")[-1]
                _log(f"  [VLM] 检查场景: {name} ({view})...")
                r = check_scene_image(img, name, desc, client)
                r["name"] = name
                r["view"] = view
                r["image"] = img
                results.append(r)

    # 汇总
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    failed = sum(1 for r in results if not r.get("passed") and not r.get("uncertain"))
    uncertain = sum(1 for r in results if r.get("uncertain"))

    return {
        "checks": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "uncertain": uncertain,
        },
    }
