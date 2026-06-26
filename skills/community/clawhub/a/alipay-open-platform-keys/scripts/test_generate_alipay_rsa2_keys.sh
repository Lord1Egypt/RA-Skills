#!/usr/bin/env bash
# 测试 generate_alipay_rsa2_keys.sh（需 openssl，无需额外测试框架）
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
GEN="${SCRIPT_DIR}/generate_alipay_rsa2_keys.sh"
VERIFY="${SCRIPT_DIR}/verify_alipay_rsa2_keypair.sh"

RED='\033[0;31m'
GRN='\033[0;32m'
NC='\033[0m'

pass=0
fail=0

ok() {
  echo -e "${GRN}OK${NC} $*"
  pass=$((pass + 1))
}

bad() {
  echo -e "${RED}FAIL${NC} $*"
  fail=$((fail + 1))
}

cleanup() {
  [[ -n "${TMPDIR:-}" && -d "${TMPDIR:-}" ]] && rm -rf "$TMPDIR"
}
trap cleanup EXIT

TMPDIR=$(mktemp -d)
export TMPDIR

# --- help ---
if bash "$GEN" --help >/dev/null 2>&1; then
  ok "--help 退出码 0"
else
  bad "--help 应成功"
fi

# --- unknown flag ---
if ! bash "$GEN" --not-a-real-flag 2>/dev/null; then
  ok "非法参数非 0 退出"
else
  bad "非法参数应失败"
fi

# --- public key mode ---
bash "$GEN" --no-print "$TMPDIR" &>/dev/null
PUB_DIR=$(find "$TMPDIR" -maxdepth 1 -type d -name 'alipay_keys_*' | head -1)
PRIV="${PUB_DIR}/app_private_key.pem"
PUB="${PUB_DIR}/app_public_key.pem"
if [[ -f "$PRIV" && -f "$PUB" && ! -f "${PUB_DIR}/app.csr" ]]; then
  ok "公钥模式生成 app_private_key.pem + app_public_key.pem，无 app.csr"
else
  bad "公钥模式文件不完整或存在 app.csr"
fi

if openssl rsa -in "$PRIV" -check -noout &>/dev/null; then
  ok "私钥通过 openssl rsa -check"
else
  bad "私钥校验失败"
fi

m1=$(openssl rsa -in "$PRIV" -noout -modulus 2>/dev/null | openssl md5)
m2=$(openssl rsa -pubin -in "$PUB" -noout -modulus 2>/dev/null | openssl md5)
if [[ "$m1" == "$m2" ]]; then
  ok "公私钥 modulus 一致"
else
  bad "公私钥 modulus 不一致"
fi

if bash "$VERIFY" "$PRIV" "$PUB" &>/dev/null && bash "$VERIFY" "$PUB" "$PRIV" &>/dev/null; then
  ok "verify_alipay_rsa2_keypair.sh 匹配（正序/反序）"
else
  bad "verify_alipay_rsa2_keypair.sh 应成功"
fi

if head -1 "$PRIV" | grep -q "BEGIN PRIVATE KEY"; then
  ok "私钥为 PKCS#8（BEGIN PRIVATE KEY）"
else
  bad "私钥格式非预期 PKCS#8"
fi

rm -rf "$PUB_DIR"

# --- cert mode with subject ---
bash "$GEN" --cert --no-print -S '/CN=UnitTestCSR' "$TMPDIR" &>/dev/null
CERT_DIR=$(find "$TMPDIR" -maxdepth 1 -type d -name 'alipay_keys_*' | head -1)
if [[ -f "${CERT_DIR}/app.csr" ]]; then
  ok "证书模式生成 app.csr"
else
  bad "证书模式缺少 app.csr"
fi

sub=$(openssl req -in "${CERT_DIR}/app.csr" -noout -subject 2>/dev/null || true)
if [[ "$sub" == *"CN=UnitTestCSR"* ]]; then
  ok "CSR Subject 含 CN=UnitTestCSR"
else
  bad "CSR Subject 不符: $sub"
fi

rm -rf "$CERT_DIR"

# --- cert mode placeholder subject (stderr) ---
OUT=$(mktemp)
ERR=$(mktemp)
bash "$GEN" --cert --no-print "$TMPDIR" >"$OUT" 2>"$ERR"
PLACE_DIR=$(find "$TMPDIR" -maxdepth 1 -type d -name 'alipay_keys_*' | head -1)
if grep -q 'REPLACE-ME\|占位\|警告' "$ERR" 2>/dev/null || grep -q 'REPLACE-ME' "$ERR" 2>/dev/null; then
  ok "无 --subj 时 stderr 含占位/警告提示"
else
  # 兼容英文 openssl 环境：至少 CSR 仍生成且 subject 为占位 CN
  if openssl req -in "${PLACE_DIR}/app.csr" -noout -subject 2>/dev/null | grep -q 'Alipay-Open-Platform-CSR-REPLACE-ME'; then
    ok "无 --subj 时 CSR 使用占位 CN"
  else
    bad "未检测到占位 Subject 警告或 CSR 占位 CN"
  fi
fi
rm -f "$OUT" "$ERR"
rm -rf "$PLACE_DIR"

echo ""
echo "----------------------------------------"
if [[ "$fail" -eq 0 ]]; then
  echo -e "${GRN}全部通过${NC} (${pass} 条)"
  exit 0
else
  echo -e "${RED}失败 ${fail} 条${NC}，通过 ${pass} 条"
  exit 1
fi
