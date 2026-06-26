#!/bin/bash
# Promo API User ID 管理
# 用法: promo_user.sh [get|regenerate]

PROMO_USER_FILE="$HOME/.promo_user_id"

# 获取或创建 user_id
get_user_id() {
  if [[ -f "$PROMO_USER_FILE" ]]; then
    cat "$PROMO_USER_FILE"
  else
    local new_id="u_$(head -c 16 /dev/urandom | xxd -p)"
    echo "$new_id" > "$PROMO_USER_FILE"
    echo "$new_id"
  fi
}

# 重新生成 user_id
regenerate_user_id() {
  local new_id="u_$(head -c 16 /dev/urandom | xxd -p)"
  echo "$new_id" > "$PROMO_USER_FILE"
  echo "$new_id"
}

case "$1" in
  get|"")
    get_user_id
    ;;
  regenerate|new)
    regenerate_user_id
    ;;
  *)
    echo "用法: $0 [get|regenerate]"
    ;;
esac
