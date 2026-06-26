import os
from typing import Any
import json
import subprocess
import logging
import re

try:
    import json5  # type: ignore[import-not-found]
except Exception:
    json5 = None

logger = logging.getLogger("benchclaw.openclawbot")

_BOT_SINGLETON: "OpenclawBot | None" = None

class OpenclawBot:
    """
    负责通过 openclaw CLI 读取关键信息：
    - 版本号
    - 默认 primary / fallbacks 模型
    """

    _instance: "OpenclawBot | None" = None

    def __new__(cls, config_path: str | None = None) -> "OpenclawBot":
        # 进程内单例：多次构造只返回同一个对象
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str | None = None) -> None:
        if getattr(self, "_initialized", False):
            return

        self.config_path = config_path

        self.openclaw_root = os.path.join(os.path.expanduser("~"), ".openclaw")

        self.raw_config: dict[str, Any] = {}

        # 元信息
        self.version: str | None = None

        # 模型相关
        self.primary_model: str | None = None
        self.fallback_models: list[str] = []

        self._load()
        self._initialized = True

    def _load(self) -> None:
        """通过 openclaw CLI 读取并解析信息，忽略读取和解析错误。"""
        logger.info("正在读取Openclaw版本和模型信息...")

        self._extract_version()
        self._extract_models()

    def _run_openclaw_json(self, args: list[str]) -> Any:
        """
        执行 openclaw CLI 并从输出中提取 JSON。
        输出可能包含 banner/提示语/插件日志等非 JSON 内容，会自动跳过。
        """
        # 延迟导入，避免与 agent_cli 的潜在循环依赖。
        from agent_cli import resolve_openclaw_cmd

        try:
            proc = subprocess.run(
                [*resolve_openclaw_cmd(), *args],
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
            )
        except OSError as e:
            logger.exception("执行 openclaw 命令失败: args=%s, err=%s", args, e)
            return None

        if proc.returncode != 0:
            logger.warning(
                "openclaw 返回非 0 状态码: code=%s, args=%s, stderr=%s",
                proc.returncode,
                args,
                (proc.stderr or "").strip(),
            )

        output = (proc.stdout or "").strip()
        if not output:
            logger.warning("openclaw 无输出: args=%s", args)
            return None

        for candidate in self._iter_json_candidates(output):
            data = self._parse_json(candidate)
            if data is not None:
                return data
        logger.warning("openclaw 输出中未找到可解析 JSON: args=%s", args)
        return None

    def _iter_json_candidates(self, text: str) -> list[str]:
        """从文本中提取可能的完整 JSON 片段（支持对象和数组）。"""
        candidates: list[str] = []
        n = len(text)
        i = 0
        while i < n:
            ch = text[i]
            if ch not in "{[":
                i += 1
                continue
            end = self._find_json_end(text, i)
            if end != -1:
                candidates.append(text[i : end + 1].strip())
                i = end + 1
            else:
                i += 1
        return candidates

    def _find_json_end(self, text: str, start: int) -> int:
        """给定 JSON 起始位置，寻找其匹配结束位置；失败返回 -1。"""
        opening = text[start]
        if opening not in "{[":
            return -1
        closing = "}" if opening == "{" else "]"
        depth = 0
        in_string = False
        escaped = False

        for i in range(start, len(text)):
            ch = text[i]

            if in_string:
                if escaped:
                    escaped = False
                    continue
                if ch == "\\":
                    escaped = True
                    continue
                if ch == '"':
                    in_string = False
                continue

            if ch == '"':
                in_string = True
                continue

            if ch == opening:
                depth += 1
                continue
            if ch == closing:
                depth -= 1
                if depth == 0:
                    return i
                continue

            # 处理嵌套的另一类括号，如 {"a":[1,2]}
            if ch in "{[":
                depth += 1
            elif ch in "}]":
                depth -= 1
                if depth == 0:
                    return i

        return -1

    def _parse_json(self, text: str) -> Any:
        # 优先使用 json5（若可用），否则退回标准 json
        if json5 is not None:
            try:
                return json5.loads(text)  # type: ignore[call-arg]
            except Exception:
                pass
        try:
            return json.loads(text)
        except Exception:
            return None

    def _extract_version(self) -> None:
        """解析版本号。

        仅通过 `openclaw --version` 输出解析版本号（如 `OpenClaw 2026.4.9 (0512059)`）。
        """
        # 延迟导入，避免与 agent_cli 的潜在循环依赖。
        from agent_cli import resolve_openclaw_cmd

        try:
            proc = subprocess.run(
                [*resolve_openclaw_cmd(), "--version"],
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
            )
        except OSError as e:
            logger.warning("执行 openclaw --version 失败: %s", e)
            return None

        output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        if not output:
            logger.warning("openclaw --version 无输出")
            return None

        # 示例: "OpenClaw 2026.4.9 (0512059)"
        m = re.search(r"OpenClaw\s+([^\s]+)", output, flags=re.IGNORECASE)
        if m:
            self.version = m.group(1).strip()
            return

        logger.warning("无法从 openclaw --version 输出解析版本号: %s", output)

    def _extract_models(self) -> None:
        model_data = self._run_openclaw_json(
            ["config", "get", "agents.defaults.model", "--json"]
        )

        if isinstance(model_data, dict):
            self.raw_config["model"] = model_data
        else:
            logger.warning("读取 agents.defaults.model 失败或返回非对象 JSON")
            return

        model_cfg: dict[str, Any] | None = None
        maybe_model = self.raw_config.get("model")
        if isinstance(maybe_model, dict):
            model_cfg = maybe_model

        if model_cfg is not None:
            primary = model_cfg.get("primary") or model_cfg.get("id")
            if isinstance(primary, str) and primary.strip():
                self.primary_model = primary.strip()

            fallbacks = model_cfg.get("fallbacks")
            if isinstance(fallbacks, list):
                self.fallback_models = [
                    str(m).strip() for m in fallbacks if str(m).strip()
                ]


def get_openclaw_bot(config_path: str | None = None) -> OpenclawBot:
    """返回全局唯一的 OpenclawBot 实例。"""
    global _BOT_SINGLETON
    if _BOT_SINGLETON is None:
        _BOT_SINGLETON = OpenclawBot(config_path=config_path)
    return _BOT_SINGLETON

def main()->None:
    bot = get_openclaw_bot()
    print("version:", bot.version)
    print("primary model:", bot.primary_model)
    print("fallbacks:", bot.fallback_models)

if __name__ == "__main__":
    main()
