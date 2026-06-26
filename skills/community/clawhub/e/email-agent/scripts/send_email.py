#!/usr/bin/env python3
from __future__ import annotations

import argparse
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Mapping


EMBEDDED_CONFIG_HEADING = "## Embedded SMTP Config"

PROVIDER_PRESETS = {
    "126": {"host": "smtp.126.com", "port": 465, "use_ssl": True},
    "qq": {"host": "smtp.qq.com", "port": 465, "use_ssl": True},
    "sina": {"host": "smtp.sina.com", "port": 465, "use_ssl": True},
    "aliyun": {"host": "smtp.aliyun.com", "port": 465, "use_ssl": True},
    "custom": {},
}


@dataclass(frozen=True)
class SMTPConfig:
    provider: str
    host: str
    port: int
    use_ssl: bool
    username: str
    password: str
    from_email: str
    from_name: str
    to_email: str
    subject: str
    body: str
    timeout: int


def apply_message_overrides(
    values: Mapping[str, str],
    *,
    to_email: str | None = None,
    email_subject: str | None = None,
    email_body: str | None = None,
) -> dict[str, str]:
    merged = dict(values)
    if to_email:
        merged["TO_EMAIL"] = to_email
    if email_subject:
        merged["EMAIL_SUBJECT"] = email_subject
    if email_body:
        merged["EMAIL_BODY"] = email_body
    return merged


def parse_env_text(text: str, source_name: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid line in {source_name}: {raw_line!r}")
        key, value = line.split("=", 1)
        values[key.strip()] = strip_quotes(value.strip())
    return values


def load_dotenv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return parse_env_text(path.read_text(encoding="utf-8-sig"), str(path))


def load_embedded_skill_config(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    lines = path.read_text(encoding="utf-8-sig").splitlines()
    heading_index = next(
        (index for index, line in enumerate(lines) if line.strip() == EMBEDDED_CONFIG_HEADING),
        None,
    )
    if heading_index is None:
        return {}

    fence_start = None
    for index in range(heading_index + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped.startswith("```dotenv") or stripped.startswith("```env") or stripped == "```":
            fence_start = index + 1
            break
        if stripped.startswith("## "):
            return {}

    if fence_start is None:
        return {}

    block_lines: list[str] = []
    for index in range(fence_start, len(lines)):
        stripped = lines[index].strip()
        if stripped == "```":
            break
        block_lines.append(lines[index])
    if not block_lines:
        return {}

    return parse_env_text("\n".join(block_lines), f"{path} embedded config")


def load_config_values(env_file: Path, skill_file: Path) -> tuple[dict[str, str], str]:
    embedded_values = load_embedded_skill_config(skill_file)
    env_values = load_dotenv(env_file)

    merged = dict(embedded_values)
    merged.update(env_values)

    sources: list[str] = []
    if embedded_values:
        sources.append(f"{skill_file.name} embedded config")
    if env_values:
        sources.append(str(env_file))

    source_label = " + ".join(sources) if sources else "no config source"
    return merged, source_label


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_bool(value: str | None, default: bool) -> bool:
    if value is None or value == "":
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


def first_non_empty(*values: str | None) -> str | None:
    for value in values:
        if value is not None and value != "":
            return value
    return None


def build_config(values: Mapping[str, str]) -> SMTPConfig:
    provider = values.get("EMAIL_PROVIDER", "custom").strip().lower() or "custom"
    if provider not in PROVIDER_PRESETS:
        supported = ", ".join(sorted(PROVIDER_PRESETS))
        raise ValueError(f"Unsupported EMAIL_PROVIDER={provider!r}. Supported: {supported}")

    preset = PROVIDER_PRESETS[provider]
    host = first_non_empty(values.get("SMTP_HOST"), preset.get("host"))
    if not host:
        raise ValueError("SMTP_HOST is required when EMAIL_PROVIDER=custom")

    raw_port = first_non_empty(values.get("SMTP_PORT"), str(preset.get("port", "")))
    if not raw_port:
        raise ValueError("SMTP_PORT is required when EMAIL_PROVIDER=custom")
    port = int(raw_port)

    use_ssl = parse_bool(values.get("SMTP_USE_SSL"), bool(preset.get("use_ssl", True)))
    username = first_non_empty(values.get("SMTP_USERNAME"), values.get("FROM_EMAIL"))
    password = values.get("SMTP_PASSWORD", "")
    from_email = values.get("FROM_EMAIL", "")
    from_name = values.get("FROM_NAME", "")
    to_email = values.get("TO_EMAIL", "")
    subject = values.get("EMAIL_SUBJECT", "")
    body = values.get("EMAIL_BODY", "")
    timeout = int(values.get("SMTP_TIMEOUT", "30"))

    required = {
        "SMTP_USERNAME": username,
        "SMTP_PASSWORD": password,
        "FROM_EMAIL": from_email,
        "TO_EMAIL": to_email,
        "EMAIL_SUBJECT": subject,
        "EMAIL_BODY": body,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise ValueError(f"Missing required values: {', '.join(missing)}")

    return SMTPConfig(
        provider=provider,
        host=host,
        port=port,
        use_ssl=use_ssl,
        username=username,
        password=password,
        from_email=from_email,
        from_name=from_name,
        to_email=to_email,
        subject=subject,
        body=body,
        timeout=timeout,
    )


def build_message(config: SMTPConfig) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = config.subject
    message["From"] = format_from_header(config.from_email, config.from_name)
    message["To"] = config.to_email
    message.set_content(config.body)
    return message


def format_from_header(from_email: str, from_name: str) -> str:
    if not from_name:
        return from_email
    return f"{from_name} <{from_email}>"


def send_email(config: SMTPConfig) -> None:
    message = build_message(config)
    if config.use_ssl:
        with smtplib.SMTP_SSL(config.host, config.port, timeout=config.timeout) as server:
            server.login(config.username, config.password)
            server.send_message(message)
        return

    with smtplib.SMTP(config.host, config.port, timeout=config.timeout) as server:
        server.starttls()
        server.login(config.username, config.password)
        server.send_message(message)


def redact_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a simple email through SMTP.")
    parser.add_argument("--env-file", default=".env", help="Path to the .env file")
    parser.add_argument("--skill-file", default="SKILL.md", help="Path to the SKILL.md file")
    parser.add_argument("--to-email", help="Recipient email address")
    parser.add_argument("--email-subject", help="Email subject")
    parser.add_argument("--email-body", help="Plain-text email body")
    parser.add_argument("--dry-run", action="store_true", help="Print resolved config without sending")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    env_file = Path(args.env_file)
    skill_file = Path(args.skill_file)
    values, source_label = load_config_values(env_file, skill_file)
    values = apply_message_overrides(
        values,
        to_email=args.to_email,
        email_subject=args.email_subject,
        email_body=args.email_body,
    )
    config = build_config(values)

    if args.dry_run:
        print("Resolved SMTP config:")
        print(f"  source      : {source_label}")
        print(f"  provider    : {config.provider}")
        print(f"  host        : {config.host}")
        print(f"  port        : {config.port}")
        print(f"  use_ssl     : {config.use_ssl}")
        print(f"  username    : {config.username}")
        print(f"  password    : {redact_secret(config.password)}")
        print(f"  from        : {format_from_header(config.from_email, config.from_name)}")
        print(f"  to          : {config.to_email}")
        print(f"  subject     : {config.subject}")
        print(f"  body_length : {len(config.body)}")
        return 0

    send_email(config)
    print(f"Email sent to {config.to_email} via {config.host}:{config.port}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
