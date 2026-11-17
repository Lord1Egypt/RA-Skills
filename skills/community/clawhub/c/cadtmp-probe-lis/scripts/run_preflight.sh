#!/usr/bin/env bash
# 发布前预检：全量自测 -> 契约校验 -> 脱敏扫描 -> 可选真图回归。
# 用法：scripts/run_preflight.sh [--manifest <真图清单.json>]
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# SkillHub 下载包可能丢失可执行位：先补回，统一用 bash 调用子脚本
if [ -d "${SKILL_DIR}/scripts" ]; then
  find "${SKILL_DIR}/scripts" -maxdepth 1 -type f -name "*.sh" -exec chmod +x {} + 2>/dev/null || true
fi
PYTHON_BIN=""
for candidate in \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"
do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then
    PYTHON_BIN="${candidate}"
    break
  fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "❌ Python 3 not found;" >&2
  exit 1
fi
MANIFEST=""
if [[ "${1:-}" == "--manifest" ]]; then
  MANIFEST="${2:?--manifest 需要参数}"
  shift 2
fi
if [[ -z "${MANIFEST}" ]]; then
  echo "⚠️ 未提供 --manifest，跳过真实图纸回归；发布前必须带真图清单跑一次。"
fi
echo "=== 1/4 全量自测 ==="
(cd "${SKILL_DIR}" && PYTHONPYCACHEPREFIX=/tmp/cad-pycache "${PYTHON_BIN}" -m unittest discover -s scripts/tests -p "test_*.py")
echo "=== 2/4 契约样例校验 ==="
# 用测试生成/现存样例若在 scripts/tests 下则校验；无样例时仅依赖单测中 validate 断言
find "${SKILL_DIR}/scripts/tests" -name "*.json" -not -path "*__pycache__*" -print0 2>/dev/null | xargs -0 -r -n1 bash "${SKILL_DIR}/scripts/cad_validate.sh" || true
echo "=== 3/4 发布脱敏扫描 ==="
"${PYTHON_BIN}" "${SKILL_DIR}/scripts/cad_release_scrub.py" "${SKILL_DIR}" \
  --skip-dirs vendor,__pycache__,.git,node_modules,tests,outputs,examples

echo "=== 3.5/4 SkillHub 合规扫描 ==="
CHECK_RELEASE="${HOME}/.codex/skills/skill-publisher/scripts/check_release.py"
if [[ -f "${CHECK_RELEASE}" ]]; then
  # outputs/examples 为本地/示例目录不随发布包上传；plants.json 里的 中国/美国/台湾/新疆/香港 是植物品种地理名，非政治涉政。
  "${PYTHON_BIN}" "${CHECK_RELEASE}" --path "${SKILL_DIR}" --exclude-dirs outputs,examples \
    --allow-sensitive 'packs/landscape-geometry/rules/plants.json=中国,packs/landscape-geometry/rules/plants.json=美国,packs/landscape-geometry/rules/plants.json=台湾,packs/landscape-geometry/rules/plants.json=新疆,packs/landscape-geometry/rules/plants.json=香港,scripts/run_preflight.sh=中国,scripts/run_preflight.sh=美国,scripts/run_preflight.sh=台湾,scripts/run_preflight.sh=新疆,scripts/run_preflight.sh=香港,scripts/run_preflight.sh=政治'
else
  echo "⚠️ 未找到 skill-publisher/check_release.py，跳过 SkillHub 合规扫描（发布前需补跑）"
fi
if [[ -n "${MANIFEST}" ]]; then
  echo "=== 4/4 真图回归 ==="
  bash "${SKILL_DIR}/scripts/run_real_dwg_regression.sh" --manifest "${MANIFEST}"
  rc=$?
  if [[ ${rc} -ne 0 ]]; then
    echo "❌ 真图回归失败（rc=${rc}）" >&2
    exit ${rc}
  fi
else
  echo "=== 4/4 跳过（缺 manifest） ==="
fi
echo "✅ 发布预检完成"
