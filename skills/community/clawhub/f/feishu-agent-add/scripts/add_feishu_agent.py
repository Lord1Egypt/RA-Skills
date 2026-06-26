#!/usr/bin/env python3
"""
OpenClaw Feishu Agent Configurator

One execution core with two entry styles:
- direct CLI flags for advanced users
- interactive prompts for users who want guided setup
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from string import Template
from typing import Any


def default_config_path() -> Path:
    if sys.platform == "win32":
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return appdata / "openclaw" / "openclaw.json"
    return Path.home() / ".openclaw" / "openclaw.json"


def slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = normalized.replace("_", "-")
    normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "-", normalized)
    normalized = normalized.strip("-")
    if re.search(r"[a-z0-9]", normalized):
        normalized = re.sub(r"-{2,}", "-", normalized)
        return normalized
    return "agent"


def prompt_text(label: str, default: str | None = None, secret: bool = False) -> str:
    prompt = f"{label}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    if secret:
        import getpass

        value = getpass.getpass(prompt)
    else:
        value = input(prompt)
    value = value.strip()
    if not value and default is not None:
        return default
    return value


def prompt_bool(label: str, default: bool) -> bool:
    suffix = "Y/n" if default else "y/N"
    while True:
        value = input(f"{label} [{suffix}]: ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Please answer y or n.")


@dataclass
class AgentRequest:
    agent_id: str
    agent_name: str
    purpose: str
    app_id: str
    app_secret: str
    config_path: str
    workspace_path: str
    model: str | None
    enable_agent_to_agent: bool
    create_workspace: bool
    workspace_mode: str
    init_templates: bool
    group_policy: str | None
    domain: str
    dry_run: bool
    json_output: bool


class ConfigError(Exception):
    pass


class FeishuAgentConfigurator:
    def __init__(self, request: AgentRequest, script_dir: Path):
        self.request = request
        self.script_dir = script_dir
        self.config_path = Path(request.config_path).expanduser()
        self.workspace_path = Path(request.workspace_path).expanduser()
        self.config: dict[str, Any] | None = None
        self.summary: dict[str, Any] = {
            "agent_id": request.agent_id,
            "agent_name": request.agent_name,
            "workspace_path": str(self.workspace_path),
            "config_path": str(self.config_path),
            "dry_run": request.dry_run,
            "changes": [],
            "warnings": [],
            "next_steps": [],
        }
        self.workspace_created_via_cli = False

    def note(self, applied: str, dry_run: str | None = None) -> None:
        if self.request.dry_run:
            self.summary["changes"].append(dry_run or f"Dry run only: {applied}")
            return
        self.summary["changes"].append(applied)

    def load_config(self) -> dict[str, Any]:
        if not self.config_path.exists():
            raise ConfigError(f"OpenClaw config not found: {self.config_path}")
        with self.config_path.open("r", encoding="utf-8") as handle:
            self.config = json.load(handle)
        return self.config

    def config_or_raise(self) -> dict[str, Any]:
        if self.config is None:
            raise ConfigError("Configuration has not been loaded.")
        return self.config

    def existing_agent_ids(self) -> set[str]:
        config = self.config_or_raise()
        return {item.get("id") for item in config.get("agents", {}).get("list", []) if item.get("id")}

    def validate_request(self) -> None:
        if not self.request.agent_name:
            raise ConfigError("Agent name is required.")
        if not self.request.agent_id:
            raise ConfigError("Agent ID is required.")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", self.request.agent_id):
            raise ConfigError("Agent ID must contain only lowercase letters, numbers, and hyphens.")
        if not self.request.app_id:
            raise ConfigError("Feishu App ID is required.")
        if not self.request.app_secret:
            raise ConfigError("Feishu App Secret is required.")
        existing_ids = self.existing_agent_ids()
        if self.request.agent_id in existing_ids:
            raise ConfigError(f"Agent ID '{self.request.agent_id}' already exists.")
        if self.workspace_path.exists():
            self.summary["warnings"].append(
                f"Workspace already exists and will be reused: {self.workspace_path}"
            )
        self.warn_on_missing_default_account()

    def warn_on_missing_default_account(self) -> None:
        config = self.config_or_raise()
        feishu = config.get("channels", {}).get("feishu", {})
        accounts = feishu.get("accounts", {})
        if not isinstance(accounts, dict):
            return
        account_count = len(accounts)
        will_have_multiple_accounts = account_count >= 1
        has_default = bool(feishu.get("defaultAccount")) or (
            isinstance(accounts.get("default"), dict)
        )
        if will_have_multiple_accounts and not has_default:
            self.summary["warnings"].append(
                "Multiple Feishu accounts will exist without an explicit defaultAccount. "
                "Consider setting channels.feishu.defaultAccount to avoid fallback routing surprises."
            )

    def resolve_model(self) -> str:
        config = self.config_or_raise()
        if self.request.model:
            return self.request.model
        return (
            config.get("agents", {})
            .get("defaults", {})
            .get("model", {})
            .get("primary", "custom-model-glm/glm-4.7")
        )

    def resolve_group_policy(self) -> str:
        config = self.config_or_raise()
        if self.request.group_policy:
            return self.request.group_policy
        return (
            config.get("channels", {})
            .get("feishu", {})
            .get("groupPolicy", "open")
        )

    def preview(self) -> dict[str, Any]:
        model = self.resolve_model()
        group_policy = self.resolve_group_policy()
        return {
            "agent": {
                "id": self.request.agent_id,
                "name": self.request.agent_name,
                "workspace": str(self.workspace_path),
                "model": model,
            },
            "feishu_account": {
                "appId": self.request.app_id,
                "appSecret": "***hidden***",
                "domain": self.request.domain,
                "groupPolicy": group_policy,
            },
            "binding": {
                "agentId": self.request.agent_id,
                "match": {
                    "channel": "feishu",
                    "accountId": self.request.agent_id,
                },
            },
            "enable_agent_to_agent": self.request.enable_agent_to_agent,
            "create_workspace": self.request.create_workspace,
            "init_templates": self.request.init_templates,
        }

    def apply(self) -> dict[str, Any]:
        config = self.config_or_raise()
        preview = self.preview()
        model = preview["agent"]["model"]
        group_policy = preview["feishu_account"]["groupPolicy"]

        agents = config.setdefault("agents", {}).setdefault("list", [])
        agents.append(
            {
                "id": self.request.agent_id,
                "name": self.request.agent_name,
                "workspace": str(self.workspace_path),
                "model": model,
            }
        )
        self.note(
            f"Added agent '{self.request.agent_id}' to agents.list",
            f"would add agent '{self.request.agent_id}' to agents.list",
        )

        feishu = config.setdefault("channels", {}).setdefault("feishu", {})
        accounts = feishu.setdefault("accounts", {})
        if self.request.agent_id in accounts:
            raise ConfigError(f"Feishu account '{self.request.agent_id}' already exists.")
        accounts[self.request.agent_id] = {
            "appId": self.request.app_id,
            "appSecret": self.request.app_secret,
            "domain": self.request.domain,
            "groupPolicy": group_policy,
        }
        self.note(
            f"Added Feishu account '{self.request.agent_id}' to channels.feishu.accounts",
            f"would add Feishu account '{self.request.agent_id}' to channels.feishu.accounts",
        )

        bindings = config.setdefault("bindings", [])
        for binding in bindings:
            if binding.get("agentId") == self.request.agent_id:
                raise ConfigError(f"Binding for agent '{self.request.agent_id}' already exists.")
        bindings.append(
            {
                "agentId": self.request.agent_id,
                "match": {
                    "channel": "feishu",
                    "accountId": self.request.agent_id,
                },
            }
        )
        self.note(
            f"Added binding for '{self.request.agent_id}'",
            f"would add binding for '{self.request.agent_id}'",
        )

        if self.request.enable_agent_to_agent:
            allow = (
                config.setdefault("tools", {})
                .setdefault("agentToAgent", {})
                .setdefault("allow", [])
            )
            config["tools"]["agentToAgent"]["enabled"] = True
            if self.request.agent_id not in allow:
                allow.append(self.request.agent_id)
                self.note(
                    f"Added '{self.request.agent_id}' to tools.agentToAgent.allow",
                    f"would add '{self.request.agent_id}' to tools.agentToAgent.allow",
                )

        if self.request.create_workspace:
            self.ensure_workspace()

        if self.request.init_templates:
            self.write_templates()

        if not self.request.dry_run:
            self.save_config()
        else:
            self.summary["changes"].append("Dry run only: configuration file was not modified")

        self.summary["next_steps"] = [
            "Restart OpenClaw after applying the config changes.",
            f"Open {self.workspace_path / 'SOUL.md'} to refine the agent identity if needed.",
            "Send a message to the new Feishu bot to verify the binding works.",
        ]
        if any("defaultAccount" in item for item in self.summary["warnings"]):
            self.summary["next_steps"].append(
                "If you use multiple Feishu bots, consider setting channels.feishu.defaultAccount."
            )
        return self.summary

    def save_config(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = self.config_path.with_name(f"{self.config_path.stem}.bak.{timestamp}.json")
        shutil.copy2(self.config_path, backup_path)
        with self.config_path.open("w", encoding="utf-8") as handle:
            json.dump(self.config, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        self.summary["changes"].append(f"Backed up config to {backup_path}")
        self.summary["changes"].append(f"Wrote config to {self.config_path}")

    def ensure_workspace(self) -> None:
        if self.workspace_path.exists():
            self.summary["changes"].append(f"Reused workspace {self.workspace_path}")
            return

        mode = self.request.workspace_mode
        if mode == "auto":
            mode = "cli" if shutil.which("openclaw") else "mkdir"

        if mode == "cli":
            self.create_workspace_via_openclaw()
        else:
            if not self.request.dry_run:
                self.workspace_path.mkdir(parents=True, exist_ok=True)
                self.summary["changes"].append(f"Created workspace directory {self.workspace_path}")
            else:
                self.summary["changes"].append(
                    f"Dry run only: would create workspace directory {self.workspace_path}"
                )

    def create_workspace_via_openclaw(self) -> None:
        command = [
            "openclaw",
            "agents",
            "add",
            "--workspace",
            str(self.workspace_path),
            self.request.agent_id,
        ]
        if self.request.dry_run:
            self.summary["changes"].append(f"Dry run only: would run {' '.join(command)}")
            return
        try:
            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise ConfigError("openclaw command not found. Use --workspace-mode mkdir.") from exc
        except subprocess.CalledProcessError as exc:
            raise ConfigError(
                f"Workspace creation failed: {exc.stderr.strip() or exc.stdout.strip()}"
            ) from exc
        self.summary["changes"].append(f"Created workspace via OpenClaw CLI: {self.workspace_path}")
        self.workspace_created_via_cli = True
        stdout = completed.stdout.strip()
        if stdout:
            self.summary["warnings"].append(stdout)

    def write_templates(self) -> None:
        if self.workspace_created_via_cli:
            self.summary["warnings"].append(
                "Workspace was created by OpenClaw CLI, so starter templates were left as generated by OpenClaw."
            )
            return
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        template_dir = self.script_dir.parent / "templates"
        variables = {
            "agent_id": self.request.agent_id,
            "agent_name": self.request.agent_name,
            "purpose": self.request.purpose or "待补充",
            "workspace_path": str(self.workspace_path),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        for src_name, dest_name in [
            ("SOUL.template.md", "SOUL.md"),
            ("BOOTSTRAP.template.md", "BOOTSTRAP.md"),
        ]:
            src_path = template_dir / src_name
            dest_path = self.workspace_path / dest_name
            if dest_path.exists():
                self.summary["warnings"].append(f"Template skipped because file exists: {dest_path}")
                continue
            content = Template(src_path.read_text(encoding="utf-8")).safe_substitute(variables)
            if not self.request.dry_run:
                dest_path.write_text(content, encoding="utf-8")
                self.summary["changes"].append(f"Initialized {dest_path.name} in workspace")
            else:
                self.summary["changes"].append(
                    f"Dry run only: would initialize {dest_path.name} in workspace"
                )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Add an OpenClaw Feishu agent with either direct flags or guided prompts."
    )
    parser.add_argument("--agent-id", help="Stable ID such as trader or xiaohongshu")
    parser.add_argument("--agent-name", help="Display name for the new agent")
    parser.add_argument("--purpose", help="What the agent is for")
    parser.add_argument("--app-id", help="Feishu App ID")
    parser.add_argument("--app-secret", help="Feishu App Secret")
    parser.add_argument("--model", help="Override the model for this agent")
    parser.add_argument("--config-path", default=str(default_config_path()), help="Path to openclaw.json")
    parser.add_argument("--workspace-path", help="Workspace path for the agent")
    parser.add_argument(
        "--workspace-mode",
        choices=["auto", "cli", "mkdir"],
        default="auto",
        help="How to create the workspace",
    )
    parser.add_argument("--group-policy", help="Override the Feishu groupPolicy for this account")
    parser.add_argument("--domain", default="feishu", help="Feishu domain field, defaults to feishu")
    parser.add_argument(
        "--enable-agent-to-agent",
        dest="enable_agent_to_agent",
        action="store_true",
        help="Add the agent to tools.agentToAgent.allow",
    )
    parser.add_argument(
        "--disable-agent-to-agent",
        dest="enable_agent_to_agent",
        action="store_false",
        help="Do not touch tools.agentToAgent.allow",
    )
    parser.set_defaults(enable_agent_to_agent=True)
    parser.add_argument(
        "--create-workspace",
        dest="create_workspace",
        action="store_true",
        help="Create the workspace if it does not exist",
    )
    parser.add_argument(
        "--no-create-workspace",
        dest="create_workspace",
        action="store_false",
        help="Skip workspace creation",
    )
    parser.set_defaults(create_workspace=True)
    parser.add_argument(
        "--init-templates",
        dest="init_templates",
        action="store_true",
        help="Write BOOTSTRAP.md and SOUL.md templates into the workspace",
    )
    parser.add_argument(
        "--no-init-templates",
        dest="init_templates",
        action="store_false",
        help="Skip writing workspace templates",
    )
    parser.set_defaults(init_templates=True)
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--json-output", action="store_true", help="Print machine-readable JSON summary")
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the final confirmation prompt when not all args are provided interactively",
    )
    return parser


def collect_request(args: argparse.Namespace) -> AgentRequest:
    interactive = not all(
        [args.agent_id, args.agent_name, args.purpose, args.app_id, args.app_secret]
    )

    agent_name = args.agent_name or prompt_text("Agent name（Agent 名称）")
    purpose = args.purpose or prompt_text("Agent purpose（Agent 人设及简介）")
    suggested_id = args.agent_id or slugify(agent_name)
    agent_id = args.agent_id or prompt_text("Agent ID（唯一标识）", default=suggested_id)
    config_path = args.config_path
    default_workspace = args.workspace_path or str(Path(config_path).expanduser().parent / f"workspace-{agent_id}")
    workspace_path = args.workspace_path or (
        prompt_text("Workspace path（工作区路径）", default=default_workspace) if interactive else default_workspace
    )
    app_id = args.app_id or prompt_text("Feishu App ID（飞书应用 ID）")
    app_secret = args.app_secret or prompt_text("Feishu App Secret（飞书应用密钥）", secret=True)

    enable_agent_to_agent = args.enable_agent_to_agent
    init_templates = args.init_templates
    create_workspace = args.create_workspace
    model = args.model
    group_policy = args.group_policy

    if interactive:
        if args.model is None:
            model_input = prompt_text("Model override（模型覆盖，留空则使用默认值）", default="")
            model = model_input or None
        if args.group_policy is None:
            group_policy_input = prompt_text(
                "Feishu groupPolicy override（群策略覆盖，留空则继承现有配置）",
                default="",
            )
            group_policy = group_policy_input or None
        if "--disable-agent-to-agent" not in sys.argv and "--enable-agent-to-agent" not in sys.argv:
            enable_agent_to_agent = prompt_bool(
                "Enable agent-to-agent collaboration for this agent（是否加入多 Agent 协作）",
                True,
            )
        if "--no-create-workspace" not in sys.argv and "--create-workspace" not in sys.argv:
            create_workspace = prompt_bool("Create workspace now（现在创建工作区）", True)
        if "--no-init-templates" not in sys.argv and "--init-templates" not in sys.argv:
            init_templates = prompt_bool(
                "Write starter SOUL.md and BOOTSTRAP.md files（写入初始化模板文件）",
                True,
            )

    return AgentRequest(
        agent_id=agent_id.strip(),
        agent_name=agent_name.strip(),
        purpose=purpose.strip(),
        app_id=app_id.strip(),
        app_secret=app_secret.strip(),
        config_path=config_path,
        workspace_path=workspace_path,
        model=model.strip() if model else None,
        enable_agent_to_agent=enable_agent_to_agent,
        create_workspace=create_workspace,
        workspace_mode=args.workspace_mode,
        init_templates=init_templates,
        group_policy=group_policy.strip() if group_policy else None,
        domain=args.domain.strip(),
        dry_run=args.dry_run,
        json_output=args.json_output,
    )


def print_preview(preview: dict[str, Any]) -> None:
    print("\nPlanned changes:")
    print(json.dumps(preview, indent=2, ensure_ascii=False))


def print_summary(summary: dict[str, Any]) -> None:
    print("\nConfiguration complete.\n")
    for item in summary["changes"]:
        print(f"- {item}")
    if summary["warnings"]:
        print("\nWarnings:")
        for item in summary["warnings"]:
            print(f"- {item}")
    if summary["next_steps"]:
        print("\nNext steps:")
        for item in summary["next_steps"]:
            print(f"- {item}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not all([args.agent_id, args.agent_name, args.purpose, args.app_id, args.app_secret]):
        print("Interactive example（填写示例）:")
        print("- Agent name（Agent 名称）: 投研助手")
        print("- Agent purpose（Agent 用途）: 港股分析和日报生成")
        print("- Agent ID（唯一标识）: research")
        print("- Workspace path（工作区路径）: 直接回车使用默认值即可")
        print("- Feishu App ID（飞书应用 ID）: cli_xxx")
        print("- Feishu App Secret（飞书应用密钥）: secret_xxx")
        print("")
    request = collect_request(args)
    configurator = FeishuAgentConfigurator(request, Path(__file__).resolve().parent)

    try:
        configurator.load_config()
        configurator.validate_request()
        preview = configurator.preview()
        if not request.json_output:
            print_preview(preview)
        if not args.yes and not request.dry_run:
            confirmed = prompt_bool("Apply these changes", True)
            if not confirmed:
                print("Cancelled.")
                return 1
        summary = configurator.apply()
        if request.json_output:
            payload = {
                "request": asdict(request) | {"app_secret": "***hidden***"},
                "preview": preview,
                "summary": summary,
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print_summary(summary)
        return 0
    except (ConfigError, json.JSONDecodeError) as exc:
        if request.json_output:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
