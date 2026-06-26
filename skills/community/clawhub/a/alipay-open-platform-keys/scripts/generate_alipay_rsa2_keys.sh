#!/usr/bin/env bash
# 支付宝开放平台 RSA2（2048）：PKCS#8 私钥 + SPKI 公钥 PEM；可选证书模式 CSR（PEM）。
# 依赖：openssl（无需 Python）。
set -euo pipefail

PRINT_KEYS=1
PARENT_DIR="."
CERT_MODE=0
CSR_SUBJ=""

usage() {
  cat <<'EOF'
用法:
  generate_alipay_rsa2_keys.sh [选项] [父目录]

  在「父目录」下创建 alipay_keys_<UTC时间戳>/，写入:
    app_private_key.pem  app_public_key.pem
  证书模式（--cert）额外写入:
    app.csr   （上传至开放平台申请应用公钥证书，CSR 的 DN 以官方文档为准）

选项:
  -d, --dir DIR     父目录（默认当前目录）
  --cert            证书模式：在密钥对之外生成 app.csr（需配置 Subject，见下）
  -S, --subj STR    CSR 的 -subj 字符串（证书模式强烈建议显式传入；见 openssl req 格式）
                    也可通过环境变量 ALIPAY_CSR_SUBJ 提供（--subj 优先）
  --no-print        只生成文件，不在终端打印 PEM
  -h, --help        显示说明

证书模式 Subject:
  字段须符合开放平台当前文档（如 https://opendocs.alipay.com/common/02kipl ）。
  示例（请按主体资质修改，勿照抄）:
    -S '/C=CN/ST=Shanghai/L=Shanghai/O=Example Corp/CN=example.com'

示例:
  ./generate_alipay_rsa2_keys.sh
  ./generate_alipay_rsa2_keys.sh --cert -S '/CN=MyCompany'
  ALIPAY_CSR_SUBJ='/CN=Demo' ./generate_alipay_rsa2_keys.sh --cert
  ./generate_alipay_rsa2_keys.sh --no-print .
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-print)
      PRINT_KEYS=0
      shift
      ;;
    --cert)
      CERT_MODE=1
      shift
      ;;
    -S|--subj)
      CSR_SUBJ="${2:?}"
      shift 2
      ;;
    -d|--dir)
      PARENT_DIR="${2:?}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "未知参数: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      PARENT_DIR="$1"
      shift
      ;;
  esac
done

if ! command -v openssl >/dev/null 2>&1; then
  echo "错误: 未找到 openssl，请先安装并加入 PATH。" >&2
  exit 1
fi

if [[ "$CERT_MODE" -eq 1 ]]; then
  if [[ -z "$CSR_SUBJ" ]]; then
    CSR_SUBJ="${ALIPAY_CSR_SUBJ:-}"
  fi
  if [[ -z "$CSR_SUBJ" ]]; then
    CSR_SUBJ="/CN=Alipay-Open-Platform-CSR-REPLACE-ME"
    echo "警告: 未提供 --subj 或 ALIPAY_CSR_SUBJ，已使用占位 Subject:" >&2
    echo "  $CSR_SUBJ" >&2
    echo "请按开放平台文档改为真实主体信息后再上传 CSR，否则可能被拒。" >&2
  fi
fi

STAMP=$(date -u +"%Y%m%dT%H%M%SZ")
OUT_NAME="alipay_keys_${STAMP}"
mkdir -p "$PARENT_DIR"
OUT="$PARENT_DIR/$OUT_NAME"
mkdir -p "$OUT"

PRIV="$OUT/app_private_key.pem"
PUB="$OUT/app_public_key.pem"

openssl genpkey -algorithm RSA -out "$PRIV" -pkeyopt rsa_keygen_bits:2048
openssl pkey -in "$PRIV" -pubout -out "$PUB"
chmod 600 "$PRIV"
chmod 644 "$PUB"

CSR=""
if [[ "$CERT_MODE" -eq 1 ]]; then
  CSR="$OUT/app.csr"
  openssl req -new -sha256 -key "$PRIV" -out "$CSR" -subj "$CSR_SUBJ"
  chmod 644 "$CSR"
fi

ABS=$(cd "$OUT" && pwd -P)

echo ""
echo "=========================================="
if [[ "$CERT_MODE" -eq 1 ]]; then
  echo "Alipay RSA2 密钥对 + CSR 已生成（2048 位，证书模式）"
else
  echo "Alipay RSA2 密钥对已生成（2048 位，PEM，公钥模式）"
fi
echo "目录（绝对路径）: $ABS"
echo "=========================================="
echo ""

if [[ "$PRINT_KEYS" -eq 1 ]]; then
  if [[ "$CERT_MODE" -eq 1 ]]; then
    echo "--- CSR（上传至开放平台「开发信息」申请应用公钥证书，以页面说明为准）---"
    cat "$CSR"
    echo ""
  else
    echo "--- 应用公钥（公钥模式：上传到开放平台 → 应用 → 开发信息 → 应用公钥）---"
    cat "$PUB"
    echo ""
  fi
  echo "--- 应用私钥（请求加签；仅本机/服务端配置，禁止提交仓库、勿发聊天/邮件）---"
  cat "$PRIV"
  echo ""
fi

echo "文件:"
echo "  $ABS/app_private_key.pem"
echo "  $ABS/app_public_key.pem"
if [[ "$CERT_MODE" -eq 1 ]]; then
  echo "  $ABS/app.csr"
else
  echo "（公钥模式）上传 app_public_key.pem 或其中 Base64 段至控制台。"
fi
echo ""
echo "注意事项:"
echo "  - 私钥泄露须立即在控制台轮换并重新生成。"
echo "  - 项目根目录请将 alipay_keys_*/、*.pem、*.csr 保持已在 .gitignore 中。"
if [[ "$CERT_MODE" -eq 1 ]]; then
  echo "  - 控制台「接口加签方式」须选证书模式，并与 SDK/代码配置一致。"
  echo "  - CSR 被拒时核对开放平台文档中的 Subject/扩展项要求；勿使用占位 Subject 上线。"
else
  echo "  - 控制台「接口加签方式」须与代码一致（本输出为公钥模式密钥文件）。"
fi
echo ""
echo "下一步:"
if [[ "$CERT_MODE" -eq 1 ]]; then
  echo "  1. 登录 https://open.alipay.com → 你的应用 → 开发信息 → 证书模式。"
  echo "  2. 上传 app.csr，按页面流程获取并下载：应用公钥证书、支付宝公钥证书、（若提供）支付宝根证书。"
  echo "  3. 将应用私钥与各证书路径配置到 SDK/环境变量（与文档一致）。"
  echo "  4. 联调：请求加签成功 + 回调按证书验签通过。"
else
  echo "  1. 登录 https://open.alipay.com → 你的应用 → 开发信息。"
  echo "  2. 上传应用公钥（按页面要求粘贴整段 PEM 或仅 Base64，以页面为准）。"
  echo "  3. 保存控制台提供的「支付宝公钥」，写入环境变量或文件，用于回调验签。"
  echo "  4. 将应用私钥配置为 ALIPAY_APP_PRIVATE_KEY 或代码/SDK 所需路径/变量。"
  echo "  5. 联调：请求加签成功 + 回调验签通过。"
  echo "  （若需证书模式：使用同一脚本加参数  --cert -S '你的Subject'  重新生成目录。）"
fi
echo ""
