#!/usr/bin/env python3
import argparse
from datetime import datetime
import json
import shutil
import sys
from pathlib import Path
from typing import Any


HOME = Path.home()
DEFAULT_OPENCLAW_PATH = HOME / ".openclaw" / "openclaw.json"


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def backup_config(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    backup_path = path.with_name(f"{path.name}.{stamp}.bak")
    shutil.copy2(path, backup_path)
    return backup_path


def save_config(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_config(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def ensure_model_alias(defaults: dict, model_id: str) -> None:
    defaults.setdefault("models", {})
    defaults["models"].setdefault(model_id, {"alias": model_id.split("/", 1)[-1]})


def split_model_ref(model_ref: str) -> tuple[str, str]:
    if "/" not in model_ref:
        raise SystemExit("model ref must be provider/model")
    provider_id, model_id = model_ref.split("/", 1)
    if not provider_id or not model_id:
        raise SystemExit("model ref must be provider/model")
    return provider_id, model_id


def get_model_primary(model_value):
    if isinstance(model_value, dict):
        return model_value.get("primary")
    if isinstance(model_value, str):
        return model_value
    return None


def summarize(data: dict) -> dict:
    defaults = data.get("agents", {}).get("defaults", {})
    agents = data.get("agents", {}).get("list", [])
    providers = data.get("models", {}).get("providers", {})
    return {
        "providers": sorted(providers.keys()),
        "providerModels": {
            provider_id: [
                model.get("id")
                for model in provider.get("models", [])
                if isinstance(model, dict) and model.get("id")
            ]
            for provider_id, provider in sorted(providers.items())
            if isinstance(provider, dict)
        },
        "defaultModel": defaults.get("model", {}).get("primary"),
        "memorySearchEnabled": defaults.get("memorySearch", {}).get("enabled"),
        "agentModels": {
            agent.get("id"): get_model_primary(agent.get("model"))
            for agent in agents
            if isinstance(agent, dict) and agent.get("id")
        },
    }


def set_memory_search(data: dict, enabled: bool) -> None:
    defaults = data.setdefault("agents", {}).setdefault("defaults", {})
    memory_search = defaults.setdefault("memorySearch", {})
    memory_search["enabled"] = enabled


def set_openai_provider(
    data: dict,
    base_url: str | None,
    api_key: str | None,
) -> None:
    providers = data.setdefault("models", {}).setdefault("providers", {})
    provider = providers.get("openai")
    if not isinstance(provider, dict):
        raise SystemExit("provider not found: openai")
    if base_url is None and api_key is None:
        raise SystemExit("pass --base-url and/or --api-key")
    if base_url is not None:
        provider["baseUrl"] = base_url
    if api_key is not None:
        provider["apiKey"] = api_key


def add_model(
    data: dict,
    provider_id: str,
    model_id: str,
    name: str | None,
    context_window: int | None,
    max_tokens: int | None,
    reasoning: bool,
    allowlist: bool,
    set_default: bool,
    input_types: list[str] | None,
    base_url: str | None = None,
    api_key: str | None = None,
    api: str | None = None,
    auth_header: bool | None = None,
) -> None:
    models = data.setdefault("models", {})
    providers = models.setdefault("providers", {})
    provider = providers.get(provider_id)

    if provider is None:
        provider = {}
        providers[provider_id] = provider
    if not isinstance(provider, dict):
        raise SystemExit(f"provider config is not an object: {provider_id}")

    if base_url is not None:
        provider["baseUrl"] = base_url
    if api_key is not None:
        provider["apiKey"] = api_key
    if api is not None:
        provider["api"] = api
    if auth_header is not None:
        provider["authHeader"] = auth_header

    if "baseUrl" not in provider or "api" not in provider:
        raise SystemExit(
            "provider must exist with baseUrl and api, or pass --base-url and --api"
        )

    catalog = provider.setdefault("models", [])
    if not isinstance(catalog, list):
        raise SystemExit("provider models must be a list")

    model_entry: dict[str, Any] | None = None
    for item in catalog:
        if isinstance(item, dict) and item.get("id") == model_id:
            model_entry = item
            break
    if model_entry is None:
        model_entry = {"id": model_id}
        catalog.append(model_entry)

    model_entry["name"] = name or model_id
    model_entry["reasoning"] = reasoning
    model_entry["input"] = input_types or model_entry.get("input") or ["text"]
    model_entry["cost"] = model_entry.get("cost") or {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0,
    }
    if context_window is not None:
        model_entry["contextWindow"] = context_window
    if max_tokens is not None:
        model_entry["maxTokens"] = max_tokens

    full_model_id = f"{provider_id}/{model_id}"
    defaults = data.setdefault("agents", {}).setdefault("defaults", {})
    if allowlist or set_default:
        ensure_model_alias(defaults, full_model_id)
    if set_default:
        defaults.setdefault("model", {})["primary"] = full_model_id



def add_openai_model(
    data: dict,
    provider_id: str,
    base_url: str,
    api_key: str,
    api: str,
    model_id: str,
    name: str | None,
    context_window: int | None,
    max_tokens: int | None,
    reasoning: bool,
    allowlist: bool,
    set_default: bool,
) -> None:
    add_model(
        data,
        provider_id=provider_id,
        model_id=model_id,
        name=name,
        context_window=context_window,
        max_tokens=max_tokens,
        reasoning=reasoning,
        allowlist=allowlist,
        set_default=set_default,
        input_types=["text"],
        base_url=base_url,
        api_key=api_key,
        api=api,
    )


def set_default_model(data: dict, model_id: str) -> None:
    defaults = data.setdefault("agents", {}).setdefault("defaults", {})
    defaults.setdefault("model", {})["primary"] = model_id
    ensure_model_alias(defaults, model_id)


def set_agent_model(data: dict, agent_id: str, model_id: str) -> None:
    agents = data.setdefault("agents", {}).setdefault("list", [])
    for agent in agents:
        if isinstance(agent, dict) and agent.get("id") == agent_id:
            if isinstance(agent.get("model"), str):
                agent["model"] = model_id
            else:
                agent.setdefault("model", {})["primary"] = model_id
            return
    raise SystemExit(f"agent not found: {agent_id}")


def find_references(node, needle: str, path: str = "$"):
    refs = []
    if isinstance(node, dict):
        for key, value in node.items():
            refs.extend(find_references(value, needle, f"{path}.{key}"))
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            refs.extend(find_references(value, needle, f"{path}[{idx}]"))
    elif isinstance(node, str) and needle in node:
        refs.append(path)
    return refs


def find_exact_references(node, needle: str, path: str = "$"):
    refs = []
    if isinstance(node, dict):
        for key, value in node.items():
            refs.extend(find_exact_references(value, needle, f"{path}.{key}"))
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            refs.extend(find_exact_references(value, needle, f"{path}[{idx}]"))
    elif node == needle:
        refs.append(path)
    return refs


def find_provider_usage_references(data: dict, provider_id: str) -> list[str]:
    refs: list[str] = []
    prefix = f"{provider_id}/"

    auth_profiles = data.get("auth", {}).get("profiles", {})
    if isinstance(auth_profiles, dict):
        for profile_key, profile in auth_profiles.items():
            if isinstance(profile, dict) and profile.get("provider") == provider_id:
                refs.append(f"$.auth.profiles.{profile_key}.provider")

    defaults = data.get("agents", {}).get("defaults", {})
    default_model = get_model_primary(defaults.get("model"))
    if isinstance(default_model, str) and default_model.startswith(prefix):
        refs.append("$.agents.defaults.model.primary")

    model_aliases = defaults.get("models")
    if isinstance(model_aliases, dict):
        for model_ref in model_aliases.keys():
            if isinstance(model_ref, str) and model_ref.startswith(prefix):
                refs.append(
                    f"$.agents.defaults.models[{json.dumps(model_ref, ensure_ascii=False)}]"
                )

    agents = data.get("agents", {}).get("list", [])
    if isinstance(agents, list):
        for idx, agent in enumerate(agents):
            if not isinstance(agent, dict):
                continue
            model_ref = get_model_primary(agent.get("model"))
            if isinstance(model_ref, str) and model_ref.startswith(prefix):
                refs.append(f"$.agents.list[{idx}].model.primary")

            model_node = agent.get("model")
            if isinstance(model_node, dict):
                fallbacks = model_node.get("fallbacks")
                if isinstance(fallbacks, list):
                    for fallback_idx, fallback in enumerate(fallbacks):
                        if isinstance(fallback, str) and fallback.startswith(prefix):
                            refs.append(
                                f"$.agents.list[{idx}].model.fallbacks[{fallback_idx}]"
                            )

    return refs


def cleanup_model_alias(defaults: dict, model_ref: str) -> None:
    model_map = defaults.get("models")
    if isinstance(model_map, dict):
        model_map.pop(model_ref, None)



def set_model_alias(data: dict, model_ref: str, alias: str | None) -> None:
    defaults = data.setdefault("agents", {}).setdefault("defaults", {})
    defaults.setdefault("models", {})
    if alias is None:
        defaults["models"].pop(model_ref, None)
    else:
        defaults["models"][model_ref] = {"alias": alias}


def remove_model(data: dict, model_ref: str) -> list[str]:
    provider_id, model_id = split_model_ref(model_ref)
    providers = data.setdefault("models", {}).setdefault("providers", {})
    provider = providers.get(provider_id)
    if not isinstance(provider, dict):
        raise SystemExit(f"provider not found: {provider_id}")
    catalog = provider.get("models")
    if not isinstance(catalog, list):
        raise SystemExit(f"provider has no model catalog: {provider_id}")

    remaining = [
        item
        for item in catalog
        if not (isinstance(item, dict) and item.get("id") == model_id)
    ]
    if len(remaining) == len(catalog):
        raise SystemExit(f"model not found: {model_ref}")
    provider["models"] = remaining

    defaults = data.get("agents", {}).get("defaults", {})
    if get_model_primary(defaults.get("model")) == model_ref:
        return ["$.agents.defaults.model.primary"]

    refs = [
        ref
        for ref in find_exact_references(data, model_ref)
        if ref != "$.agents.defaults.model.primary"
    ]
    if refs:
        return refs

    cleanup_model_alias(defaults, model_ref)
    return []


def remove_provider(data: dict, provider_id: str) -> list[str]:
    providers = data.setdefault("models", {}).setdefault("providers", {})
    if provider_id not in providers:
        raise SystemExit(f"provider not found: {provider_id}")
    providers.pop(provider_id)
    return find_provider_usage_references(data, provider_id)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("summary")

    add_model_parser = sub.add_parser("add-model")
    add_model_parser.add_argument("--provider-id", required=True)
    add_model_parser.add_argument("--model-id", required=True)
    add_model_parser.add_argument("--name")
    add_model_parser.add_argument("--context-window", type=int)
    add_model_parser.add_argument("--max-tokens", type=int)
    add_model_parser.add_argument(
        "--reasoning", action=argparse.BooleanOptionalAction, default=True
    )
    add_model_parser.add_argument("--allowlist", action="store_true")
    add_model_parser.add_argument("--set-default", action="store_true")
    add_model_parser.add_argument(
        "--input",
        dest="input_types",
        action="append",
        help="Repeatable input type (for example: --input text --input image)",
    )
    add_model_parser.add_argument("--base-url")
    add_model_parser.add_argument("--api-key")
    add_model_parser.add_argument("--api")
    add_model_parser.add_argument(
        "--auth-header", action=argparse.BooleanOptionalAction, default=None
    )

    add_openai_model_parser = sub.add_parser("add-openai-model")
    add_openai_model_parser.add_argument("--provider-id", required=True)
    add_openai_model_parser.add_argument("--base-url", required=True)
    add_openai_model_parser.add_argument("--api-key", required=True)
    add_openai_model_parser.add_argument("--api", default="openai-responses")
    add_openai_model_parser.add_argument("--model-id", required=True)
    add_openai_model_parser.add_argument("--name")
    add_openai_model_parser.add_argument("--context-window", type=int)
    add_openai_model_parser.add_argument("--max-tokens", type=int)
    add_openai_model_parser.add_argument(
        "--reasoning", action=argparse.BooleanOptionalAction, default=True
    )
    add_openai_model_parser.add_argument("--allowlist", action="store_true")
    add_openai_model_parser.add_argument("--set-default", action="store_true")

    provider = sub.add_parser("set-openai-provider")
    provider.add_argument("--base-url")
    provider.add_argument("--api-key")

    memory = sub.add_parser("set-memory-search")
    memory.add_argument("enabled", choices=["on", "off"])

    default_model = sub.add_parser("set-default-model")
    default_model.add_argument("model_id")

    agent_model = sub.add_parser("set-agent-model")
    agent_model.add_argument("agent_id")
    agent_model.add_argument("model_id")

    remove = sub.add_parser("remove-provider")
    remove.add_argument("provider_id")

    remove_model_parser = sub.add_parser("remove-model")
    remove_model_parser.add_argument("model_ref")

    set_alias = sub.add_parser("set-model-alias")
    set_alias.add_argument("model_ref")
    set_alias.add_argument("alias", nargs="?", default=None)

    args = parser.parse_args()

    path = Path(args.file).expanduser() if args.file else DEFAULT_OPENCLAW_PATH

    data = load_config(path)

    if args.cmd == "summary":
        print(json.dumps(summarize(data), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "add-model":
        add_model(
            data,
            provider_id=args.provider_id,
            model_id=args.model_id,
            name=args.name,
            context_window=args.context_window,
            max_tokens=args.max_tokens,
            reasoning=args.reasoning,
            allowlist=args.allowlist,
            set_default=args.set_default,
            input_types=args.input_types,
            base_url=args.base_url,
            api_key=args.api_key,
            api=args.api,
            auth_header=args.auth_header,
        )
        save_config(path, data)
        return 0

    if args.cmd == "add-openai-model":
        add_openai_model(
            data,
            provider_id=args.provider_id,
            base_url=args.base_url,
            api_key=args.api_key,
            api=args.api,
            model_id=args.model_id,
            name=args.name,
            context_window=args.context_window,
            max_tokens=args.max_tokens,
            reasoning=args.reasoning,
            allowlist=args.allowlist,
            set_default=args.set_default,
        )
        save_config(path, data)
        return 0

    if args.cmd == "set-openai-provider":
        set_openai_provider(data, args.base_url, args.api_key)
        save_config(path, data)
        return 0

    if args.cmd == "set-memory-search":
        set_memory_search(data, args.enabled == "on")
        save_config(path, data)
        return 0

    if args.cmd == "set-default-model":
        set_default_model(data, args.model_id)
        save_config(path, data)
        return 0

    if args.cmd == "set-agent-model":
        set_agent_model(data, args.agent_id, args.model_id)
        save_config(path, data)
        return 0

    if args.cmd == "set-model-alias":
        set_model_alias(data, args.model_ref, args.alias)
        save_config(path, data)
        return 0

    if args.cmd == "remove-provider":
        refs = remove_provider(data, args.provider_id)
        if refs:
            print(
                json.dumps(
                    {"error": "provider still referenced", "references": refs},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 2
        save_config(path, data)
        return 0

    if args.cmd == "remove-model":
        refs = remove_model(data, args.model_ref)
        if refs:
            print(
                json.dumps(
                    {"error": "model still referenced", "references": refs},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 2
        save_config(path, data)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
