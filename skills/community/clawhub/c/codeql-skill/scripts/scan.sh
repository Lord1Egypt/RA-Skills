#!/usr/bin/env bash
# [SCAN] CodeQL 静态扫描脚本
# 用法: ./scan.sh <repo_path> [language] [output_sarif]
# language 可选: java | javascript | python | cpp | auto (默认 auto)
# 示例: ./scan.sh ./my-project java results.sarif

set -euo pipefail

REPO="${1:-.}"
LANG="${2:-auto}"
OUTPUT="${3:-results.sarif}"
DB_PATH="./codeql-db"

# ── 1. 自动检测语言 ──────────────────────────────────────────────
detect_language() {
  local counts=()
  [[ $(find "$REPO" -name "*.java" -o -name "*.kt" 2>/dev/null | wc -l) -gt 0 ]] && counts+=("java")
  [[ $(find "$REPO" -name "*.js" -o -name "*.ts" 2>/dev/null | wc -l) -gt 0 ]]   && counts+=("javascript")
  [[ $(find "$REPO" -name "*.py" 2>/dev/null | wc -l) -gt 0 ]]                    && counts+=("python")
  [[ $(find "$REPO" -name "*.c" -o -name "*.cpp" 2>/dev/null | wc -l) -gt 0 ]]   && counts+=("cpp")

  if [[ ${#counts[@]} -eq 0 ]]; then
    echo "ERROR: 未检测到支持的语言" >&2; exit 1
  fi

  # 多语言时用逗号拼接
  IFS=','; echo "${counts[*]}"
}

if [[ "$LANG" == "auto" ]]; then
  LANG=$(detect_language)
  echo "✔ 检测到语言: $LANG"
fi

# ── 2. 选择构建命令 ──────────────────────────────────────────────
build_cmd=""
case "$LANG" in
  java)
    if [[ -f "$REPO/pom.xml" ]]; then
      build_cmd="mvn clean install -DskipTests -f $REPO/pom.xml"
    elif [[ -f "$REPO/build.gradle" ]]; then
      build_cmd="gradle build -x test -p $REPO"
    fi
    ;;
  cpp)
    [[ -f "$REPO/Makefile" ]] && build_cmd="make -C $REPO"
    ;;
  javascript|python)
    build_cmd=""  # 无需构建
    ;;
esac

# ── 3. 创建 CodeQL 数据库 ────────────────────────────────────────
echo "⏳ 创建 CodeQL 数据库 (语言: $LANG)..."
codeql_args=(database create "$DB_PATH"
  --language="$LANG"
  --source-root="$REPO"
  --overwrite
)
[[ -n "$build_cmd" ]] && codeql_args+=(--command="$build_cmd")

codeql "${codeql_args[@]}"
echo "✔ 数据库创建完成: $DB_PATH"

# ── 4. 选择查询套件 ──────────────────────────────────────────────
declare -A SUITES=(
  [java]="codeql/java-queries:codeql-suites/java-security-extended.qls"
  [javascript]="codeql/javascript-queries:codeql-suites/javascript-security-extended.qls"
  [python]="codeql/python-queries:codeql-suites/python-security-extended.qls"
  [cpp]="codeql/cpp-queries:codeql-suites/cpp-security-extended.qls"
)

# 多语言时取第一个（分析主语言）
PRIMARY_LANG="${LANG%%,*}"
SUITE="${SUITES[$PRIMARY_LANG]}"

# ── 5. 运行分析 → SARIF ──────────────────────────────────────────
echo "⏳ 运行安全查询套件..."
codeql database analyze "$DB_PATH" \
  --format=sarifv2.1.0 \
  --output="$OUTPUT" \
  "$SUITE"

echo "✅ 扫描完成 → $OUTPUT"
echo "   下一步: python3 scripts/audit.py $OUTPUT"
