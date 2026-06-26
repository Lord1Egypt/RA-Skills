#!/bin/bash

# AI Speckits Service Boundary Check Script
# 服务边界规则检查工具
# 
# 用途：在 CI/CD 或本地检查代码是否违反服务边界
# 使用场景：微服务架构下，禁止跨服务直接访问数据库或内部实现

set -e

# 配置
PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
REPORT_DIR="${PROJECT_ROOT}/docs/boundary-checks"
REPORT_FILE="${REPORT_DIR}/$(date +%Y-%m-%d-%H-%M-%S)-boundary-check.md"
QUICK_MODE=false
MODULE=""
VERBOSE=false

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --quick)
      QUICK_MODE=true
      shift
      ;;
    --module)
      MODULE="$2"
      shift 2
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    --help)
      echo "用法：$0 [选项]"
      echo ""
      echo "选项:"
      echo "  --quick          快速模式，仅检查 P0 规则"
      echo "  --module=NAME    仅检查指定模块"
      echo "  --verbose        详细输出"
      echo "  --help           显示帮助"
      exit 0
      ;;
    *)
      echo "未知选项：$1"
      exit 1
      ;;
  esac
done

# 创建报告目录
mkdir -p "$REPORT_DIR"

# 初始化报告
cat > "$REPORT_FILE" << EOF
# 服务边界检查报告

**检查时间**: $(date '+%Y-%m-%d %H:%M:%S')
**检查模式**: $([ "$QUICK_MODE" = true ] && echo "快速模式 (P0 仅)" || echo "完整模式")
**检查模块**: ${MODULE:-"全部模块"}

---

## 检查结果

EOF

# 计数器
P0_VIOLATIONS=0
P1_VIOLATIONS=0
P2_VIOLATIONS=0
TOTAL_CHECKS=0

# 日志函数
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
  if [ "$VERBOSE" = true ]; then
    echo "[INFO] $1" >> "$REPORT_FILE"
  fi
}

log_success() {
  echo -e "${GREEN}[✓]${NC} $1"
  echo "[✓] $1" >> "$REPORT_FILE"
}

log_warning() {
  echo -e "${YELLOW}[⚠]${NC} $1"
  echo "[⚠] P1: $1" >> "$REPORT_FILE"
  ((P1_VIOLATIONS++))
}

log_error() {
  echo -e "${RED}[✗]${NC} $1"
  echo "[✗] P0: $1" >> "$REPORT_FILE"
  ((P0_VIOLATIONS++))
}

log_hint() {
  echo -e "${YELLOW}[💡]${NC} $1"
  echo "[💡] $1" >> "$REPORT_FILE"
}

# 检测 Java 项目中的服务边界违规
check_java_boundaries() {
  log_info "检查 Java 服务边界..."
  
  # 查找服务目录
  SERVICE_DIRS=$(find "$PROJECT_ROOT" -type d -name "src/main/java" 2>/dev/null || true)
  
  if [ -z "$SERVICE_DIRS" ]; then
    log_hint "未找到 Java 项目结构，跳过 Java 边界检查"
    return 0
  fi
  
  # P0 检查：跨服务数据库访问
  log_info "P0: 检查跨服务数据库访问..."
  
  # 查找直接引用其他服务 Mapper 的代码
  while IFS= read -r file; do
    if [[ "$file" == *"/mapper/"* ]]; then
      continue  # 跳过 Mapper 文件本身
    fi
    
    # 检查是否直接引用其他服务的 Mapper
    if grep -q "Autowired.*Mapper" "$file" 2>/dev/null; then
      # 提取引用的 Mapper 类
      IMPORTS=$(grep "import.*Mapper" "$file" 2>/dev/null || true)
      
      # 检查是否跨包引用
      CURRENT_PKG=$(grep "package " "$file" | head -1 | awk '{print $2}' | sed 's/;//')
      
      for import in $IMPORTS; do
        IMPORT_PKG=$(echo "$import" | awk '{print $2}' | sed 's/;//' | rev | cut -d'.' -f3- | rev)
        if [[ -n "$IMPORT_PKG" && "$IMPORT_PKG" != "$CURRENT_PKG" ]]; then
          # 检查是否是不同服务的包
          if [[ "$IMPORT_PKG" == *".order."* && "$CURRENT_PKG" == *".payment."* ]] || \
             [[ "$IMPORT_PKG" == *".payment."* && "$CURRENT_PKG" == *".order."* ]] || \
             [[ "$IMPORT_PKG" == *".user."* && "$CURRENT_PKG" == *".points."* ]] || \
             [[ "$IMPORT_PKG" == *".points."* && "$CURRENT_PKG" == *".user."* ]]; then
            log_error "跨服务直接访问 Mapper: $file 引用 $import"
          fi
        fi
      done
    fi
  done < <(find "$PROJECT_ROOT" -name "*.java" -type f 2>/dev/null)
  
  # P0 检查：跨服务表访问
  log_info "P0: 检查跨服务表访问..."
  
  while IFS= read -r file; do
    # 检查 SQL 中是否直接访问其他服务的表
    if grep -qE "(SELECT|INSERT|UPDATE|DELETE).*FROM\s+\w+" "$file" 2>/dev/null; then
      # 提取表名
      TABLES=$(grep -oE "FROM\s+\w+" "$file" 2>/dev/null | awk '{print $2}' || true)
      
      for table in $TABLES; do
        # 检查表名是否包含其他服务的前缀
        if [[ "$table" == "order_"* && "$file" == *"/payment/"* ]] || \
           [[ "$table" == "payment_"* && "$file" == *"/order/"* ]] || \
           [[ "$table" == "user_"* && "$file" == *"/points/"* ]] || \
           [[ "$table" == "points_"* && "$file" == *"/user/"* ]]; then
          log_error "跨服务直接访问表：$file 访问表 $table"
        fi
      done
    fi
  done < <(find "$PROJECT_ROOT" -name "*.xml" -type f 2>/dev/null)
  
  # P1 检查：跨服务内部类访问
  log_info "P1: 检查跨服务内部类访问..."
  
  while IFS= read -r file; do
    if [[ "$file" == *"/impl/"* || "$file" == *"/internal/"* ]]; then
      continue  # 跳过内部实现文件本身
    fi
    
    # 检查是否引用其他服务的 impl 或 internal 包
    if grep -qE "import.*\.(impl|internal|internal\.)" "$file" 2>/dev/null; then
      IMPORTS=$(grep -E "import.*\.(impl|internal)" "$file" 2>/dev/null || true)
      
      for import in $IMPORTS; do
        IMPORT_PKG=$(echo "$import" | awk '{print $2}' | sed 's/;//')
        if [[ "$IMPORT_PKG" == *".order.impl."* && "$file" == *"/payment/"* ]] || \
           [[ "$IMPORT_PKG" == *".payment.impl."* && "$file" == *"/order/"* ]]; then
          log_warning "跨服务访问内部实现：$file 引用 $import"
        fi
      done
    fi
  done < <(find "$PROJECT_ROOT" -name "*.java" -type f 2>/dev/null)
  
  ((TOTAL_CHECKS++))
}

# 检测前端微服务边界违规
check_frontend_boundaries() {
  log_info "检查前端微服务边界..."
  
  # 查找前端项目
  FRONTEND_DIRS=$(find "$PROJECT_ROOT" -name "package.json" -type f 2>/dev/null | xargs -I {} dirname {} || true)
  
  if [ -z "$FRONTEND_DIRS" ]; then
    log_hint "未找到前端项目结构，跳过前端边界检查"
    return 0
  fi
  
  # P0 检查：跨子应用直接导入
  log_info "P0: 检查跨子应用导入..."
  
  while IFS= read -r pkg_file; do
    DIR=$(dirname "$pkg_file")
    
    # 检查是否引用其他子应用的内部模块
    if grep -qE '"@[^/]+/[^/]+/(internal|lib|utils)"' "$pkg_file" 2>/dev/null; then
      IMPORTS=$(grep -E '"@[^/]+/[^/]+/(internal|lib|utils)"' "$pkg_file" 2>/dev/null || true)
      
      for import in $IMPORTS; do
        PKG_NAME=$(echo "$import" | grep -oE '"@[^"]+"' | tr -d '"')
        log_warning "跨子应用访问内部模块：$pkg_file 引用 $PKG_NAME"
      done
    fi
  done < <(find "$FRONTEND_DIRS" -name "package.json" -type f 2>/dev/null)
  
  # P1 检查：跨子应用状态访问
  log_info "P1: 检查跨子应用状态访问..."
  
  while IFS= read -r file; do
    # 检查是否直接访问其他子应用的 store
    if grep -qE "(useSelector|select).*\.(order|payment|user|points).*Store" "$file" 2>/dev/null; then
      STORES=$(grep -oE "\.(order|payment|user|points).*Store" "$file" 2>/dev/null || true)
      
      for store in $STORES; do
        # 检查当前文件所属子应用
        if [[ "$file" == *"/order/"* && "$store" == *".payment"* ]] || \
           [[ "$file" == *"/payment/"* && "$store" == *".order"* ]]; then
          log_warning "跨子应用访问状态：$file 访问 $store"
        fi
      done
    fi
  done < <(find "$FRONTEND_DIRS" -name "*.tsx" -o -name "*.ts" -type f 2>/dev/null)
  
  ((TOTAL_CHECKS++))
}

# 检查 API 调用边界
check_api_boundaries() {
  log_info "检查 API 调用边界..."
  
  # P0 检查：直接调用其他服务内部 API
  log_info "P0: 检查内部 API 调用..."
  
  while IFS= read -r file; do
    # 检查是否调用其他服务的内部 API（通常包含 internal、admin 等路径）
    if grep -qE "(http|https)://[^/]+/api/(internal|admin|private)" "$file" 2>/dev/null; then
      APIS=$(grep -oE "(http|https)://[^/]+/api/(internal|admin|private)[^\"']*" "$file" 2>/dev/null || true)
      
      for api in $APIS; do
        # 检查当前文件所属服务
        if [[ "$file" == *"/order/"* && "$api" == *"/payment/internal"* ]] || \
           [[ "$file" == *"/payment/"* && "$api" == *"/order/internal"* ]]; then
          log_error "跨服务调用内部 API: $file 调用 $api"
        fi
      done
    fi
  done < <(find "$PROJECT_ROOT" -name "*.java" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -type f 2>/dev/null)
  
  ((TOTAL_CHECKS++))
}

# 检查循环依赖
check_circular_dependencies() {
  log_info "检查循环依赖..."
  
  # 使用 madge 工具（如果已安装）
  if command -v madge &> /dev/null; then
    log_info "使用 madge 检查循环依赖..."
    
    CIRCULAR=$(madge --circular "$PROJECT_ROOT/src" 2>/dev/null || true)
    
    if [ -n "$CIRCULAR" ]; then
      log_error "发现循环依赖:\n$CIRCULAR"
    else
      log_success "未发现循环依赖"
    fi
  else
    log_hint "未安装 madge 工具，跳过循环依赖检查（npm install -g madge）"
  fi
  
  ((TOTAL_CHECKS++))
}

# 生成报告摘要
generate_summary() {
  cat >> "$REPORT_FILE" << EOF

---

## 检查摘要

**总检查项**: $TOTAL_CHECKS
**P0 违规数**: $P0_VIOLATIONS
**P1 违规数**: $P1_VIOLATIONS
**P2 违规数**: $P2_VIOLATIONS

EOF

  if [ $P0_VIOLATIONS -gt 0 ]; then
    cat >> "$REPORT_FILE" << EOF
**检查结果**: ❌ 失败（存在 P0 违规）

P0 违规必须在提交前修复！

EOF
    echo -e "${RED}❌ 检查失败：存在 $P0_VIOLATIONS 个 P0 违规${NC}"
    return 1
  elif [ $P1_VIOLATIONS -gt 0 ]; then
    cat >> "$REPORT_FILE" << EOF
**检查结果**: ⚠️ 警告（存在 P1 违规）

P1 违规建议修复，但不阻断提交（除非启用严格模式）。

EOF
    echo -e "${YELLOW}⚠️ 检查警告：存在 $P1_VIOLATIONS 个 P1 违规${NC}"
    
    if [ "${AI_SPECKITS_STRICT:-false}" = "true" ]; then
      echo -e "${RED}严格模式：P1 违规也阻断提交${NC}"
      return 1
    fi
  else
    cat >> "$REPORT_FILE" << EOF
**检查结果**: ✅ 通过

所有检查项均已通过！

EOF
    echo -e "${GREEN}✅ 检查通过：未发现违规${NC}"
  fi
  
  return 0
}

# 生成修复建议
generate_recommendations() {
  if [ $P0_VIOLATIONS -gt 0 ] || [ $P1_VIOLATIONS -gt 0 ]; then
    cat >> "$REPORT_FILE" << EOF

---

## 修复建议

### P0 违规修复建议

1. **使用 API 调用替代直接访问**
   - 不要直接引用其他服务的 Mapper/Repository
   - 通过 Feign Client、REST Template 或 gRPC 调用其他服务

2. **使用事件驱动架构**
   - 通过消息队列（Kafka、RabbitMQ）进行服务间通信
   - 使用领域事件解耦服务

3. **引入共享内核**
   - 将公共 DTO、枚举等提取到共享库
   - 确保共享库不包含业务逻辑

### P1 违规修复建议

1. **避免访问内部实现**
   - 只引用其他服务的公开接口
   - 不访问 impl、internal 等内部包

2. **遵循依赖ER 图**
   - 前端子应用间通过自定义事件或状态管理库通信
   - 不直接访问其他子应用的内部状态

EOF
  fi
}

# 主流程
main() {
  echo "========================================"
  echo "  AI Speckits 服务边界检查"
  echo "========================================"
  echo ""
  
  log_info "项目根目录：$PROJECT_ROOT"
  log_info "报告输出：$REPORT_FILE"
  echo ""
  
  # 执行检查
  check_java_boundaries
  check_frontend_boundaries
  check_api_boundaries
  check_circular_dependencies
  
  # 生成报告
  generate_summary
  generate_recommendations
  
  echo ""
  echo "========================================"
  echo "  检查完成"
  echo "========================================"
  echo ""
  echo "详细报告：$REPORT_FILE"
  echo ""
  
  # 返回检查结果
  if [ $P0_VIOLATIONS -gt 0 ]; then
    exit 1
  fi
  
  exit 0
}

# 执行
main
