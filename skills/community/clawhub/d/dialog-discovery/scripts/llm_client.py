#!/usr/bin/env python3
"""
LLM 调用适配层

- 模型配置从 config/llm.yaml 读取
- API Key 通过环境变量配置，禁止硬编码
- 兼容多种推理模型的思考链字段
- 支持命令行切换默认模型：python scripts/llm_client.py switch jdcloud
"""
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


# ── 配置文件路径 ──
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SKILL_DIR / "config" / "llm.yaml"
DEFAULT_MODEL_ENV = "PE_LLM_DEFAULT_MODEL"

# ── 自动加载 .env ──
def _load_dotenv():
    """从项目根目录的 .env 文件加载环境变量（不覆盖已有值）"""
    dotenv_path = SKILL_DIR / ".env"
    if not dotenv_path.exists():
        return
    for line in dotenv_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

_load_dotenv()


@dataclass
class ModelConfig:
    model: str
    api_key: str
    base_url: str
    temperature: float = 0.01
    max_tokens: int = 4000
    timeout: int = 180
    is_reasoning: bool = False


def _load_llm_config() -> dict:
    """从 config/llm.yaml 加载模型配置"""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"LLM 配置文件不存在: {CONFIG_PATH}")
    if yaml is None:
        # fallback: 简易 YAML 解析（只支持本文件格式）
        return _parse_yaml_simple(CONFIG_PATH)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _parse_yaml_simple(path: Path) -> dict:
    """简易 YAML 解析（无需 pyyaml 依赖）"""
    import json
    # 用正则转换简单 YAML 为 JSON
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # 去掉注释
    text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)
    # 尝试用 yaml 库
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        raise RuntimeError("需要 pyyaml: uv pip install pyyaml")


def list_models() -> List[dict]:
    """列出所有可用模型"""
    cfg = _load_llm_config()
    default = cfg.get("default", "qwen3")
    models = cfg.get("models", {})
    result = []
    for key, info in models.items():
        api_key = os.environ.get(info.get("api_key_env", ""), "")
        result.append({
            "id": key,
            "name": info.get("name", key),
            "model": info.get("default_model", ""),
            "is_default": key == default,
            "is_reasoning": info.get("is_reasoning", False),
            "has_api_key": bool(api_key),
        })
    return result


def get_default_model() -> str:
    """获取默认模型名称"""
    # 优先级：环境变量 > config/llm.yaml
    env_default = os.environ.get(DEFAULT_MODEL_ENV)
    if env_default:
        return env_default.lower()
    cfg = _load_llm_config()
    return cfg.get("default", "qwen3").lower()


def get_model_config(model_name: Optional[str] = None) -> ModelConfig:
    """获取指定模型的配置"""
    name = (model_name or os.environ.get("PE_LLM_MODEL_NAME") or get_default_model()).lower()
    cfg = _load_llm_config()
    models = cfg.get("models", {})

    if name not in models:
        available = ", ".join(models.keys())
        raise ValueError(f"未知模型: {name}，可用模型: {available}")

    info = models[name]
    api_key_env = info.get("api_key_env", "")
    base_url_env = info.get("base_url_env", "")
    model_env = info.get("model_env", "")

    # API Key: 环境变量优先，否则直接读取硬编码值
    if api_key_env:
        api_key = os.environ.get(api_key_env, "")
    else:
        api_key = info.get("api_key", "")
    
    # Base URL: 环境变量优先，否则直接读取，再否则默认值
    if base_url_env:
        base_url = os.environ.get(base_url_env, info.get("default_base_url", ""))
    else:
        base_url = info.get("base_url", info.get("default_base_url", ""))
    
    # Model: 环境变量优先，否则直接读取，再否则默认值
    if model_env:
        model = os.environ.get(model_env, info.get("default_model", ""))
    else:
        model = info.get("model", info.get("default_model", ""))
    
    timeout = info.get("timeout", 180)
    is_reasoning = info.get("is_reasoning", False)

    if not api_key:
        raise ValueError(f"缺少 API Key，请设置环境变量 {api_key_env} 或在配置中硬编码 api_key")
    if not base_url:
        raise ValueError(f"缺少 Base URL，请设置环境变量 {base_url_env}")

    return ModelConfig(
        model=model,
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
        is_reasoning=is_reasoning,
    )


def create_client(config: ModelConfig):
    if OpenAI is None:
        raise RuntimeError("未安装 openai 依赖，无法调用 LLM")
    return OpenAI(
        api_key=config.api_key,
        base_url=config.base_url,
        timeout=config.timeout,
    )


def call_messages(
    messages: List[Dict[str, str]],
    model_name: Optional[str] = None,
    temperature: float = 0.01,
    max_tokens: int = 4000,
) -> str:
    config = get_model_config(model_name)
    client = create_client(config)

    # 推理模型给更大空间，但不要过大避免死循环
    # 评分类任务 max_tokens 通常足够，推理模型会自动先思考再输出
    actual_max_tokens = min(max(max_tokens, 20000), 24000) if config.is_reasoning else max_tokens

    response = client.chat.completions.create(
        model=config.model,
        messages=messages,
        temperature=temperature or config.temperature,
        max_tokens=actual_max_tokens,
    )

    if not response.choices:
        return ""

    choice = response.choices[0]
    message = choice.message

    # 优先使用 content，如果为空则尝试 reasoning 字段
    content = message.content
    if not content:
        # 不同推理模型用不同字段名：GLM-5.1 用 reasoning_content，Qwen 用 reasoning
        reasoning = getattr(message, 'reasoning_content', None) or getattr(message, 'reasoning', None)
        if reasoning:
            # 从 reasoning 提取包含 "results" 的完整 JSON
            results_pos = reasoning.rfind('"results"')
            if results_pos != -1:
                # 向前找起始 {
                start_pos = reasoning.rfind('{', 0, results_pos)
                if start_pos != -1:
                    # 括号计数法提取完整JSON
                    brace_count = 0
                    end_pos = start_pos
                    for i in range(start_pos, len(reasoning)):
                        if reasoning[i] == '{':
                            brace_count += 1
                        elif reasoning[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end_pos = i + 1
                                break
                    if end_pos > start_pos:
                        content = reasoning[start_pos:end_pos]
            
            # 备用：如果没找到 results，用括号计数找最后一个完整JSON
            if not content:
                last_brace = reasoning.rfind('}')
                if last_brace != -1:
                    brace_count = 1
                    pos = last_brace - 1
                    while pos >= 0 and brace_count > 0:
                        if reasoning[pos] == '}':
                            brace_count += 1
                        elif reasoning[pos] == '{':
                            brace_count -= 1
                        pos -= 1
                    if brace_count == 0:
                        content = reasoning[pos + 1:last_brace + 1]
            else:
                # 备用：从末尾提取最后一个完整 JSON 对象
                last_brace = reasoning.rfind('}')
                if last_brace != -1:
                    brace_count = 1
                    pos = last_brace - 1
                    while pos >= 0 and brace_count > 0:
                        if reasoning[pos] == '}':
                            brace_count += 1
                        elif reasoning[pos] == '{':
                            brace_count -= 1
                        pos -= 1
                    if brace_count == 0:
                        content = reasoning[pos + 1:last_brace + 1]
            # 如果 reasoning 中没找到 JSON，直接返回 reasoning 文本
            if not content:
                content = reasoning

    return content or ""


def parse_json_response(content: str) -> Optional[Dict[str, Any]]:
    """从 LLM 响应中解析 JSON"""
    if not content:
        return None
    try:
        return json.loads(content)
    except Exception:
        pass

    m = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass

    m = re.search(r"\{.*\}", content, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return None


def switch_default(model_name: str):
    """切换默认模型"""
    cfg = _load_llm_config()
    models = cfg.get("models", {})
    if model_name not in models:
        available = ", ".join(models.keys())
        print(f"❌ 未知模型: {model_name}，可用: {available}")
        return
    cfg["default"] = model_name
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        if yaml:
            yaml.dump(cfg, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        else:
            # 简易写入
            f.write(f"default: {model_name}\n")
            f.write(f"\nmodels:\n")
            for k, v in models.items():
                f.write(f"  {k}:\n")
                for kk, vv in v.items():
                    f.write(f"    {kk}: {vv}\n")
    print(f"✅ 默认模型已切换为: {model_name} ({models[model_name].get('name', model_name)})")


# ── CLI ──
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python scripts/llm_client.py list          # 列出可用模型")
        print("  python scripts/llm_client.py switch <name>  # 切换默认模型")
        print("  python scripts/llm_client.py test [name]    # 测试模型连通性")
        print("  python scripts/llm_client.py default        # 查看当前默认模型")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        models = list_models()
        print("可用模型:")
        for m in models:
            default_tag = " ← 默认" if m["is_default"] else ""
            key_tag = "🔑" if m["has_api_key"] else "❌ 无Key"
            reason_tag = " (推理)" if m["is_reasoning"] else ""
            print(f"  {m['id']:10s} | {m['name']}{reason_tag} | {key_tag}{default_tag}")

    elif cmd == "switch":
        if len(sys.argv) < 3:
            print("请指定模型名称")
            sys.exit(1)
        switch_default(sys.argv[2])

    elif cmd == "test":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        try:
            config = get_model_config(name)
            print(f"模型: {config.model}")
            print(f"地址: {config.base_url}")
            print(f"Key: {config.api_key[:15]}...")
            result = call_messages(
                [{"role": "user", "content": "请回复OK"}],
                model_name=name,
                max_tokens=50,
            )
            print(f"连通: ✅ ({result[:50]})")
        except Exception as e:
            print(f"连通: ❌ {e}")

    elif cmd == "default":
        print(f"当前默认模型: {get_default_model()}")

    else:
        print(f"未知命令: {cmd}")
