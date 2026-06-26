#!/bin/bash
#
# AI 辅助代码生成工具 - 基于 PRD 自动生成代码
#
# 用法: bash scripts/ai-generate.sh <type> [选项]
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️${NC}  $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
step() { echo -e "${CYAN}▶ $1${NC}"; }

AI_CACHE_DIR=".ai-cache"

# 显示帮助
show_help() {
    echo "AI 辅助代码生成工具 (v2.0)"
    echo ""
    echo "用法: bash scripts/ai-generate.sh <类型> [选项]"
    echo ""
    echo "类型:"
    echo "  service --prd=<文件>     根据 PRD 生成服务代码"
    echo "  page --prd=<文件>        根据 PRD 生成页面代码"
    echo "  tests --for=<服务>       为指定服务生成测试用例"
    echo "  model --prd=<文件>       根据 PRD 生成数据模型"
    echo "  impl --method=<方法>     实现指定方法的业务逻辑"
    echo ""
    echo "选项:"
    echo "  --prd=<文件>             PRD 文档路径"
    echo "  --for=<名称>             目标服务/页面名称"
    echo "  --method=<方法名>        指定方法名"
    echo "  --output=<目录>          输出目录"
    echo "  --review                 生成后进入审阅模式"
    echo ""
    echo "示例:"
    echo "  bash scripts/ai-generate.sh service --prd=docs/prd/用户管理_PRD.md"
    echo "  bash scripts/ai-generate.sh tests --for=UserService"
    echo "  bash scripts/ai-generate.sh impl --method=UserService.processPayment"
    echo ""
}

# 确保缓存目录存在
ensure_cache() {
    mkdir -p "$AI_CACHE_DIR"
}

# 从 PRD 提取关键信息
extract_prd_info() {
    local prd_file="$1"

    if [ ! -f "$prd_file" ]; then
        error "PRD 文件不存在: $prd_file"
        return 1
    fi

    step "分析 PRD 文档..."

    # 提取功能名称
    local feature_name=$(grep -m1 "^# " "$prd_file" | sed 's/# //' || echo "Unknown")

    # 提取核心功能点
    local features=$(grep -E "^\s*[-*]\s+" "$prd_file" | head -10)

    # 提取接口定义
    local interfaces=$(sed -n '/## 接口定义/,/##/p' "$prd_file" | grep -E "(interface|type|export)" || echo "")

    # 提取业务规则
    local rules=$(sed -n '/## 业务规则/,/##/p' "$prd_file" | grep -E "^\s*[-*]" | head -5)

    # 保存到临时文件
    cat > "$AI_CACHE_DIR/prd_analysis.txt" << EOF
功能名称: $feature_name

核心功能:
$features

接口定义:
$interfaces

业务规则:
$rules
EOF

    success "PRD 分析完成"
    info "功能: $feature_name"
}

# 生成服务代码
gen_service() {
    local prd_file="$1"
    local output_dir="${2:-src/services}"

    ensure_cache
    extract_prd_info "$prd_file"

    # 从 PRD 提取服务名称
    local service_name=$(grep -oE "[A-Z][a-zA-Z]+Service" "$prd_file" | head -1)
    if [ -z "$service_name" ]; then
        service_name=$(basename "$prd_file" _PRD.md | sed 's/.*/\u&/' | sed 's/功能//' | sed 's/管理//' | sed 's/$/Service/')
    fi

    step "生成服务: $service_name"

    mkdir -p "$output_dir"
    local output_file="$output_dir/${service_name}.ts"

    # 读取 PRD 分析
    local feature_desc=$(head -1 "$AI_CACHE_DIR/prd_analysis.txt" | sed 's/功能名称: //')

    cat > "$output_file" << EOF
// services/${service_name}.ts
// ${feature_desc} - 业务服务
// 自动生成时间: $(date '+%Y-%m-%d %H:%M:%S')
// 基于: $(basename "$prd_file")

import { hilog } from '@kit.PerformanceAnalysisKit';
import { GlobalErrorHandler } from '../common/utils/GlobalErrorHandler';

const TAG = '${service_name}';
const DOMAIN = 0x0001;

/**
 * ${feature_desc}服务
 *
 * [AI生成说明]
 * - 基于 PRD 自动生成核心方法骨架
 * - 包含错误处理和日志记录
 * - [TODO] 需要根据具体业务补充实现细节
 */
export class ${service_name} {
  private static instance: ${service_name};
  private errorHandler: GlobalErrorHandler;

  private constructor() {
    this.errorHandler = GlobalErrorHandler.getInstance();
  }

  static getInstance(): ${service_name} {
    if (!${service_name}.instance) {
      ${service_name}.instance = new ${service_name}();
    }
    return ${service_name}.instance;
  }

  /**
   * 初始化服务
   */
  async init(): Promise<boolean> {
    try {
      hilog.info(DOMAIN, TAG, 'Service initialized');
      return true;
    } catch (error) {
      this.errorHandler.handle(error, 'init');
      return false;
    }
  }

$(generate_methods_from_prd "$prd_file")

  /**
   * 销毁服务
   */
  destroy(): void {
    hilog.info(DOMAIN, TAG, 'Service destroyed');
  }
}

// 类型定义
$(generate_types_from_prd "$prd_file")
EOF

    success "服务代码已生成: $output_file"
    info "建议下一步: bash scripts/ai-generate.sh tests --for=$service_name"
}

# 从 PRD 生成方法
generate_methods_from_prd() {
    local prd_file="$1"

    # 从功能列表提取方法名
    grep -E "^\s*[-*]\s+" "$prd_file" | head -5 | while read -r line; do
        local func=$(echo "$line" | sed 's/[-*]//g' | sed 's/^[[:space:]]*//' | cut -d'(' -f1)
        local method_name=$(echo "$func" | sed 's/功能//g' | sed 's/获取/get/g' | sed 's/创建/create/g' | sed 's/更新/update/g' | sed 's/删除/delete/g' | sed 's/处理/process/g' | tr -d ' ')

        if [ -n "$method_name" ]; then
            cat << METHOD_EOF

  /**
   * $func
   *
   * [AI生成] 基于 PRD 功能点自动生成
   * [TODO] 实现具体业务逻辑
   *
   * @param input - 输入参数
   * @returns 处理结果
   */
  async ${method_name}(input: unknown): Promise<unknown> {
    try {
      hilog.info(DOMAIN, TAG, '${method_name} called');

      // [TODO] 实现 ${func}

      return { success: true, data: null };
    } catch (error) {
      this.errorHandler.handle(error, '${method_name}');
      throw error;
    }
  }
METHOD_EOF
        fi
    done
}

# 从 PRD 生成类型
generate_types_from_prd() {
    local prd_file="$1"

    # 尝试从接口定义部分提取
    local interface_section=$(sed -n '/## 接口定义/,/##/p' "$prd_file")

    if [ -n "$interface_section" ]; then
        echo "$interface_section" | grep -E "(interface|type)" | head -5
    else
        cat << 'TYPE_EOF'
// [AI生成] 基础类型定义
export interface Request {
  id?: string;
  timestamp?: number;
}

export interface Response<T = unknown> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}
TYPE_EOF
    fi
}

# 生成测试用例
gen_tests() {
    local service_name="$1"
    local service_file="src/services/${service_name}.ts"

    if [ ! -f "$service_file" ]; then
        error "服务文件不存在: $service_file"
        return 1
    fi

    step "为 $service_name 生成测试用例..."

    # 提取类名和方法
    local class_name=$(grep -oE "export class [A-Za-z]+" "$service_file" | head -1 | sed 's/export class //')
    local methods=$(grep -oE "async [a-zA-Z]+" "$service_file" | sed 's/async //')

    mkdir -p "test/unittest"
    local test_file="test/unittest/${service_name}.test.ts"

    cat > "$test_file" << EOF
// test/unittest/${service_name}.test.ts
// ${service_name} 单元测试
// 自动生成时间: $(date '+%Y-%m-%d %H:%M:%S')

import { describe, it, expect, beforeEach, afterEach } from '@ohos/hypium';
import { ${service_name} } from '../../src/services/${service_name}';

describe('${service_name}', () => {
  let service: ${service_name};

  beforeEach(() => {
    service = ${service_name}.getInstance();
  });

  afterEach(() => {
    service.destroy();
  });

  describe('初始化', () => {
    it('should get singleton instance', () => {
      const instance1 = ${service_name}.getInstance();
      const instance2 = ${service_name}.getInstance();
      expect(instance1).assertEqual(instance2);
    });

    it('should initialize successfully', async () => {
      const result = await service.init();
      expect(result).assertTrue();
    });
  });

$(generate_test_methods "$service_file")

  describe('边界情况', () => {
    it('should handle null input', async () => {
      // [TODO] 测试空值处理
    });

    it('should handle error gracefully', async () => {
      // [TODO] 测试错误处理
    });
  });
});
EOF

    success "测试文件已生成: $test_file"
    info "运行测试: bash scripts/quick.sh test $service_name"
}

# 生成测试方法
generate_test_methods() {
    local service_file="$1"

    grep -oE "async [a-zA-Z]+" "$service_file" | sed 's/async //' | while read -r method; do
        if [ "$method" != "init" ] && [ "$method" != "destroy" ]; then
            cat << TEST_EOF
  describe('${method}', () => {
    it('should ${method} successfully', async () => {
      // Arrange
      const mockInput = {};

      // Act
      const result = await service.${method}(mockInput);

      // Assert
      expect(result).assertTrue();
    });

    it('should handle ${method} errors', async () => {
      // [TODO] 测试错误场景
    });
  });

TEST_EOF
        fi
    done
}

# 生成页面代码
gen_page() {
    local prd_file="$1"
    local page_name=$(basename "$prd_file" _PRD.md)

    step "生成页面: ${page_name}Page"

    local output_file="src/pages/${page_name}Page.ets"

    cat > "$output_file" << EOF
// pages/${page_name}Page.ets
// ${page_name}页面
// 基于: $(basename "$prd_file")

import { ${page_name}ViewModel } from '../viewmodels/${page_name}ViewModel';
import { GlobalErrorHandler } from '../common/utils/GlobalErrorHandler';

@Entry
@Component
struct ${page_name}Page {
  private viewModel: ${page_name}ViewModel = new ${page_name}ViewModel();
  private errorHandler: GlobalErrorHandler = GlobalErrorHandler.getInstance();

  @State isLoading: boolean = false;
  @State data: unknown = null;

  aboutToAppear() {
    this.viewModel.init();
  }

  build() {
    Column() {
      // Header
      this.buildHeader()

      // Content
      Scroll() {
        Column({ space: 16 }) {
          // [AI生成] 根据 PRD 功能点生成内容区域
          // [TODO] 根据具体需求调整 UI
          Text('${page_name} 页面内容')
            .fontSize(16)
            .fontColor('#666')
        }
        .width('100%')
        .padding(16)
      }
      .layoutWeight(1)

      // Footer
      this.buildFooter()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }

  @Builder
  buildHeader() {
    Row() {
      Text('${page_name}')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor(Color.White)
  }

  @Builder
  buildFooter() {
    Row({ space: 12 }) {
      Button('提交')
        .width('100%')
        .height(48)
        .fontColor(Color.White)
        .backgroundColor('#FF6B35')
        .onClick(() => this.handleSubmit())
    }
    .width('100%')
    .height(80)
    .padding(16)
    .backgroundColor(Color.White)
  }

  private async handleSubmit() {
    try {
      this.isLoading = true;
      // [TODO] 调用 ViewModel 处理提交
    } catch (error) {
      this.errorHandler.handle(error, 'handleSubmit');
    } finally {
      this.isLoading = false;
    }
  }
}
EOF

    success "页面代码已生成: $output_file"
}

# 实现具体方法
gen_impl() {
    local method_path="$1"  # 格式: ServiceName.methodName

    if [[ ! "$method_path" =~ \. ]]; then
        error "方法路径格式错误，应为: ServiceName.methodName"
        return 1
    fi

    local service_name="${method_path%%.*}"
    local method_name="${method_path##*.}"
    local service_file="src/services/${service_name}.ts"

    if [ ! -f "$service_file" ]; then
        error "服务文件不存在: $service_file"
        return 1
    fi

    step "实现方法: $method_path"

    # 检查方法是否存在
    if ! grep -q "async ${method_name}" "$service_file"; then
        error "方法 ${method_name} 不存在于 ${service_name}"
        return 1
    fi

    # 生成实现提示
    local impl_hints=$(generate_impl_hints "$service_name" "$method_name")

    # 创建实现辅助文件
    local impl_file=".ai-cache/${service_name}_${method_name}_impl.md"
    cat > "$impl_file" << EOF
# ${method_path} 实现辅助

## 方法签名
\`\`\`typescript
async ${method_name}(input: unknown): Promise<unknown>
\`\`\`

## AI 生成的实现建议

${impl_hints}

## 实现步骤

1. [ ] 参数校验
2. [ ] 前置条件检查
3. [ ] 核心业务逻辑
4. [ ] 结果封装
5. [ ] 错误处理

## 参考代码模板

\`\`\`typescript
async ${method_name}(input: unknown): Promise<unknown> {
  try {
    hilog.info(DOMAIN, TAG, '${method_name} started');

    // 1. 参数校验
    if (!input) {
      throw new Error('Invalid input');
    }

    // 2. 业务逻辑 [在此处实现]
    const result = await this.processBusiness(input);

    // 3. 返回结果
    return {
      success: true,
      data: result
    };
  } catch (error) {
    this.errorHandler.handle(error, '${method_name}');
    return {
      success: false,
      error: {
        code: 'ERR_${method_name^^}',
        message: error.message
      }
    };
  }
}
\`\`\`

## 相关文件
- 服务文件: ${service_file}
- 测试文件: test/unittest/${service_name}.test.ts
EOF

    success "实现辅助文档已生成: $impl_file"
    info "请查看文档并按步骤实现"

    # 如果设置了 REVIEW 模式，打开文件
    if [ "${REVIEW_MODE:-false}" = "true" ]; then
        cat "$impl_file"
    fi
}

# 生成实现提示
generate_impl_hints() {
    local service="$1"
    local method="$2"

    # 根据方法名推断业务逻辑
    case "$method" in
        *get*|*Get*|*查询*|*获取*)
            echo "- 从数据源查询数据"
            echo "- 实现缓存策略"
            echo "- 处理空结果情况"
            ;;
        *create*|*Create*|*创建*|*新增*)
            echo "- 参数校验和 sanitization"
            echo "- 生成唯一 ID"
            echo "- 写入数据源"
            ;;
        *update*|*Update*|*更新*|*修改*)
            echo "- 检查资源存在性"
            echo "- 部分更新支持"
            echo "- 乐观锁处理"
            ;;
        *delete*|*Delete*|*删除*)
            echo "- 软删除或硬删除"
            echo "- 关联数据清理"
            echo "- 权限校验"
            ;;
        *process*|*Process*|*处理*)
            echo "- 状态机流转"
            echo "- 副作用处理"
            echo "- 事务一致性"
            ;;
        *)
            echo "- 分析业务需求"
            echo "- 设计输入输出"
            echo "- 处理边界情况"
            ;;
    esac
}

# 主函数
main() {
    local cmd="${1:-}"
    shift || true

    # 解析参数
    local prd_file=""
    local target=""
    local method=""
    local output_dir=""
    REVIEW_MODE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --prd=*)
                prd_file="${1#*=}"
                shift
                ;;
            --for=*)
                target="${1#*=}"
                shift
                ;;
            --method=*)
                method="${1#*=}"
                shift
                ;;
            --output=*)
                output_dir="${1#*=}"
                shift
                ;;
            --review)
                REVIEW_MODE=true
                shift
                ;;
            *)
                shift
                ;;
        esac
    done

    case "$cmd" in
        service)
            if [ -z "$prd_file" ]; then
                error "请指定 PRD 文件: --prd=<文件>"
                exit 1
            fi
            gen_service "$prd_file" "$output_dir"
            ;;
        page)
            if [ -z "$prd_file" ]; then
                error "请指定 PRD 文件: --prd=<文件>"
                exit 1
            fi
            gen_page "$prd_file"
            ;;
        tests)
            if [ -z "$target" ]; then
                error "请指定服务名称: --for=<服务名>"
                exit 1
            fi
            gen_tests "$target"
            ;;
        impl)
            if [ -z "$method" ]; then
                error "请指定方法路径: --method=ServiceName.methodName"
                exit 1
            fi
            gen_impl "$method"
            ;;
        help|--help|-h|"")
            show_help
            ;;
        *)
            error "未知命令: $cmd"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
