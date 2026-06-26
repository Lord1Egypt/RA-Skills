#!/bin/bash
set -euo pipefail

# 颜色定义（让输出更清晰）
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # 清除颜色

echo -e "${GREEN}=== Axios 投毒事件 自动排查 + 安全修复脚本 ===${NC}"
echo ""

# 风险标记
HAS_RISK=0

# ==============================
# 1. 检查 axios 恶意版本
# ==============================
echo -e "${YELLOW}[1/4] 检查 axios 恶意版本...${NC}"
AXIOS_OUTPUT=$(npm list axios 2>/dev/null || true)
if echo "$AXIOS_OUTPUT" | grep -E "1\.14\.1|0\.30\.4" >/dev/null; then
  echo -e "${RED}⚠️  检测到【恶意版本】axios@1.14.1 / 0.30.4${NC}"
  HAS_RISK=1
else
  echo -e "${GREEN}✅ 未检测到恶意 axios 版本${NC}"
fi

# ==============================
# 2. 检查后门依赖 plain-crypto-js
# ==============================
echo -e "\n${YELLOW}[2/4] 检查后门依赖 plain-crypto-js...${NC}"
if npm list plain-crypto-js 2>/dev/null | grep "4\.2\.1" >/dev/null; then
  echo -e "${RED}⚠️  检测到【后门依赖】plain-crypto-js@4.2.1 —— 项目已失陷${NC}"
  HAS_RISK=1
else
  echo -e "${GREEN}✅ 未检测到后门依赖${NC}"
fi

# ==============================
# 3. 检查系统残留后门文件
# ==============================
echo -e "\n${YELLOW}[3/4] 检查系统残留恶意文件...${NC}"
RISK_FILES=()
if [ -f "/Library/Caches/com.apple.act.mond" ]; then
  echo -e "${RED}⚠️  macOS 恶意文件：/Library/Caches/com.apple.act.mond${NC}"
  RISK_FILES+=("/Library/Caches/com.apple.act.mond")
  HAS_RISK=1
fi
if [ -f "/tmp/ld.py" ]; then
  echo -e "${RED}⚠️  Linux 恶意文件：/tmp/ld.py${NC}"
  RISK_FILES+=("/tmp/ld.py")
  HAS_RISK=1
fi
if [ ${#RISK_FILES[@]} -eq 0 ]; then
  echo -e "${GREEN}✅ 未检测到系统恶意文件${NC}"
fi

# ==============================
# 4. 风险判定 + 自动安全修复
# ==============================
echo -e "\n${YELLOW}[4/4] 风险判定与安全修复...${NC}"
echo ""

if [ $HAS_RISK -eq 1 ]; then
  echo -e "${RED}=====================================================${NC}"
  echo -e "${RED}🚨 检测到安全风险！将自动执行安全修复...${NC}"
  echo -e "${RED}=====================================================${NC}"
  echo ""

  # 修复步骤1：卸载恶意包
  echo -e "${YELLOW}→ 卸载恶意 axios & plain-crypto-js...${NC}"
  npm uninstall axios plain-crypto-js 2>/dev/null || true

  # 修复步骤2：清理缓存 + 重装官方稳定版
  echo -e "${YELLOW}→ 安装官方安全版本 axios（最新稳定版）...${NC}"
  npm install axios@latest --save

  # 修复步骤3：清理 node_modules + 重新安装（彻底清除残留）
  echo -e "${YELLOW}→ 清理依赖并重新安装...${NC}"
  rm -rf node_modules package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null || true
  npm install 2>/dev/null || true

  # 修复步骤4：删除系统恶意文件
  if [ ${#RISK_FILES[@]} -gt 0 ]; then
    echo -e "${YELLOW}→ 删除系统恶意文件...${NC}"
    for file in "${RISK_FILES[@]}"; do
      rm -f "$file" 2>/dev/null || true
    done
  fi

  echo -e "\n${GREEN}=====================================================${NC}"
  echo -e "${GREEN}✅ 安全修复完成！${NC}"
  echo -e "${GREEN}✅ 已卸载恶意版本 → 已安装官方最新 axios${NC}"
  echo -e "${GREEN}=====================================================${NC}"
  echo -e "\n${YELLOW}提示：修复后请重启项目生效！${NC}"
else
  echo -e "${GREEN}=====================================================${NC}"
  echo -e "${GREEN}✅ 项目安全，未检测到任何 Axios 投毒风险${NC}"
  echo -e "${GREEN}=====================================================${NC}"
fi
