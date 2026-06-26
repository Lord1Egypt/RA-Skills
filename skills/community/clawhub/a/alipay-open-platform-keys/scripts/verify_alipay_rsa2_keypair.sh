#!/usr/bin/env bash
# 校验 RSA2 私钥与公钥是否为同一密钥对（比较 modulus）。依赖 openssl，无需 Python。
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  verify_alipay_rsa2_keypair.sh <私钥.pem> <公钥.pem>

两个参数顺序可互换（根据 PEM 头自动识别私钥/公钥）。

退出码: 0 匹配，1 不匹配或解析失败，2 参数错误。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "未知参数: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -ne 2 ]]; then
  usage >&2
  exit 2
fi

A=$1
B=$2

for f in "$A" "$B"; do
  if [[ ! -f "$f" ]]; then
    echo "错误: 文件不存在: $f" >&2
    exit 1
  fi
done

h1=$(head -1 "$A")
h2=$(head -1 "$B")
PRIV=""
PUB=""

if [[ "$h1" == *"PRIVATE"* ]] && [[ "$h2" == *"PUBLIC"* ]]; then
  PRIV=$A
  PUB=$B
elif [[ "$h1" == *"PUBLIC"* ]] && [[ "$h2" == *"PRIVATE"* ]]; then
  PRIV=$B
  PUB=$A
else
  echo "错误: 无法从 PEM 头区分私钥与公钥，请确保一个为 PRIVATE KEY、一个为 PUBLIC KEY" >&2
  exit 1
fi

if ! openssl rsa -in "$PRIV" -check -noout &>/dev/null; then
  echo "错误: 私钥无法解析或 openssl rsa -check 失败: $PRIV" >&2
  exit 1
fi

if ! openssl rsa -pubin -in "$PUB" -text -noout &>/dev/null; then
  echo "错误: 公钥无法解析: $PUB" >&2
  exit 1
fi

m1=$(openssl rsa -in "$PRIV" -noout -modulus 2>/dev/null | openssl md5)
m2=$(openssl rsa -pubin -in "$PUB" -noout -modulus 2>/dev/null | openssl md5)

if [[ "$m1" == "$m2" ]]; then
  echo "匹配: 私钥与公钥为同一 RSA 密钥对"
  exit 0
fi

echo "不匹配: modulus 不一致（可能混用了不同目录下的密钥，或一方已轮换）" >&2
exit 1
