#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' "此操作会把指定飞书自建应用配置给 lark-cli，并使用 bot-only 身份。"
read -r -p "App ID: " invoice_bot_app_id
read -r -s -p "App Secret（输入不会回显）: " invoice_bot_app_secret
printf '\n'

if [[ -z "$invoice_bot_app_id" || -z "$invoice_bot_app_secret" ]]; then
  printf '%s\n' "App ID 和 App Secret 都不能为空。" >&2
  exit 2
fi

printf '%s' "$invoice_bot_app_secret" | lark-cli config init \
  --app-id "$invoice_bot_app_id" \
  --app-secret-stdin \
  --brand feishu

unset invoice_bot_app_secret
printf '%s\n' "lark-cli 应用配置完成。"
