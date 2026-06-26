#!/bin/bash
#
# 通用代码生成脚本
# 用法: bash scripts/generate.sh <type> <name> [options]
#
# 类型:
#   model      - 生成数据模型
#   service    - 生成服务类
#   page       - 生成页面组件
#   viewmodel  - 生成ViewModel
#   test       - 生成测试文件
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

show_banner() {
    echo ""
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     🏗️  代码生成工具                             ║"
    echo "║     基于模板快速生成代码骨架                     ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 检查依赖
check_dependencies() {
    if ! command -v handlebars &> /dev/null; then
        warn "Handlebars CLI 未安装"
        info "使用简单字符串替换模式"
        USE_SIMPLE_MODE=true
    else
        USE_SIMPLE_MODE=false
    fi
}

# 简单模板替换（不使用Handlebars）
simple_template_replace() {
    local template="$1"
    local output="$2"
    local name="$3"
    local description="$4"

    # 基本替换
    sed -e "s/{{name}}/$name/g" \
        -e "s/{{Name}}/$name/g" \
        -e "s/{{description}}/$description/g" \
        "$template" > "$output"
}

# 生成数据模型
generate_model() {
    local name="$1"
    step "生成数据模型: $name"

    local output_file="src/models/${name}.ts"
    mkdir -p src/models

    cat > "$output_file" << EOF
// models/${name}.ts
// ${name}数据模型

export interface ${name} {
  id: string;
  createdAt: number;
  updatedAt?: number;
}

export interface ${name}Request {
  id: string;
}

export interface ${name}Response {
  success: boolean;
  data?: ${name};
  error?: {
    code: string;
    message: string;
  };
}
EOF

    success "模型已生成: $output_file"
}

# 生成服务
generate_service() {
    local name="$1"
    step "生成服务: $name"

    local output_file="src/services/${name}.ts"
    mkdir -p src/services

    cat > "$output_file" << EOF
// services/${name}.ts
// ${name}业务服务

import { hilog } from '@kit.PerformanceAnalysisKit';
import { GlobalErrorHandler } from '../common/utils/GlobalErrorHandler';

const TAG = '${name}';
const DOMAIN = 0x0001;

export class ${name} {
  private static instance: ${name};
  private errorHandler: GlobalErrorHandler;

  private constructor() {
    this.errorHandler = GlobalErrorHandler.getInstance();
  }

  static getInstance(): ${name} {
    if (!${name}.instance) {
      ${name}.instance = new ${name}();
    }
    return ${name}.instance;
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

  /**
   * 主要业务方法
   * [TODO] 实现具体业务逻辑
   */
  async process(input: unknown): Promise<unknown> {
    try {
      hilog.info(DOMAIN, TAG, 'Process called');
      // [TODO] 实现业务逻辑
      return { success: true };
    } catch (error) {
      this.errorHandler.handle(error, 'process');
      throw error;
    }
  }
}
EOF

    success "服务已生成: $output_file"
}

# 生成页面
generate_page() {
    local name="$1"
    step "生成页面: ${name}Page"

    local output_file="src/pages/${name}Page.ets"
    mkdir -p src/pages

    cat > "$output_file" << EOF
// pages/${name}Page.ets
// ${name}页面

import { GlobalErrorHandler } from '../common/utils/GlobalErrorHandler';

@Entry
@Component
struct ${name}Page {
  private errorHandler: GlobalErrorHandler = GlobalErrorHandler.getInstance();

  @State loading: boolean = false;
  @State data: unknown = null;

  build() {
    Column() {
      // Header
      Row() {
        Text('${name}')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
      }
      .width('100%')
      .height(56)
      .padding({ left: 16, right: 16 })
      .backgroundColor(Color.White)

      // Content
      Scroll() {
        Column({ space: 16 }) {
          // [TODO] 实现页面内容
          Text('Page Content')
            .fontSize(16)
        }
        .width('100%')
        .padding(16)
      }
      .layoutWeight(1)

      // Footer
      Row() {
        Button('Submit')
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
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }

  private handleSubmit() {
    // [TODO] 实现提交逻辑
    hilog.info(0x0001, '${name}Page', 'Submit clicked');
  }
}
EOF

    success "页面已生成: $output_file"
}

# 生成ViewModel
generate_viewmodel() {
    local name="$1"
    local vmName="${name}ViewModel"
    step "生成ViewModel: $vmName"

    local output_file="src/viewmodels/${vmName}.ts"
    mkdir -p src/viewmodels

    cat > "$output_file" << EOF
// viewmodels/${vmName}.ts
// ${name}状态管理

import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG = '${vmName}';
const DOMAIN = 0x0001;

@ObservedV2
export class ${vmName} {
  @observable loading: boolean = false;
  @observable error: string | null = null;

  @computed get hasError(): boolean {
    return this.error !== null;
  }

  @action setLoading(value: boolean): void {
    this.loading = value;
  }

  @action setError(message: string | null): void {
    this.error = message;
  }

  @action reset(): void {
    this.loading = false;
    this.error = null;
    hilog.info(DOMAIN, TAG, 'State reset');
  }
}
EOF

    success "ViewModel已生成: $output_file"
}

# 生成测试
generate_test() {
    local name="$1"
    step "生成测试: ${name}.test.ts"

    local output_file="test/unittest/${name}.test.ts"
    mkdir -p test/unittest

    cat > "$output_file" << EOF
// test/${name}.test.ts
// ${name}单元测试

import { describe, it, expect, beforeEach } from '@ohos/hypium';

describe('${name}', () => {
  beforeEach(() => {
    // 测试前置条件
  });

  it('should pass basic test', () => {
    expect(true).assertTrue();
  });

  // [TODO] 添加更多测试用例
});
EOF

    success "测试已生成: $output_file"
}

# 生成列表页
generate_list_page() {
    local name="$1"
    step "生成列表页: ${name}ListPage"

    local output_file="src/pages/${name}ListPage.ets"
    mkdir -p src/pages

    cat > "$output_file" << EOF
// pages/${name}ListPage.ets
// ${name}列表页面

import { ${name}ViewModel } from '../viewmodels/${name}ViewModel';
import { ${name} } from '../models/${name}';
import { GlobalErrorHandler } from '../common/utils/GlobalErrorHandler';

@Entry
@Component
struct ${name}ListPage {
  private viewModel: ${name}ViewModel = new ${name}ViewModel();
  private errorHandler: GlobalErrorHandler = GlobalErrorHandler.getInstance();

  @State isLoading: boolean = false;
  @State isRefreshing: boolean = false;
  @State listData: ${name}[] = [];

  aboutToAppear() {
    this.loadData();
  }

  build() {
    Column() {
      // Header
      Row() {
        Text('${name}列表')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
      }
      .width('100%')
      .height(56)
      .padding({ left: 16, right: 16 })
      .backgroundColor(Color.White)

      // List
      List() {
        ForEach(this.listData, (item: ${name}) => {
          ListItem() {
            Text(item.id)
              .fontSize(16)
              .padding(16)
          }
          .backgroundColor(Color.White)
          .margin({ bottom: 8 })
        })
      }
      .width('100%')
      .layoutWeight(1)
      .padding(16)

      // Empty state
      if (this.listData.length === 0 && !this.isLoading) {
        Text('暂无数据')
          .fontSize(16)
          .fontColor('#999')
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }

  private async loadData() {
    // [TODO] 加载列表数据
  }
}
EOF

    success "列表页已生成: $output_file"
}

# 生成表单页
generate_form_page() {
    local name="$1"
    step "生成表单页: ${name}FormPage"

    local output_file="src/pages/${name}FormPage.ets"
    mkdir -p src/pages

    cat > "$output_file" << EOF
// pages/${name}FormPage.ets
// ${name}表单页面

import { ${name}ViewModel } from '../viewmodels/${name}ViewModel';
import { GlobalErrorHandler } from '../common/utils/GlobalErrorHandler';

@Entry
@Component
struct ${name}FormPage {
  private viewModel: ${name}ViewModel = new ${name}ViewModel();
  private errorHandler: GlobalErrorHandler = GlobalErrorHandler.getInstance();

  @State isEdit: boolean = false;
  @State isSubmitting: boolean = false;

  // Form fields
  @State name: string = '';
  @State description: string = '';

  build() {
    Column() {
      // Header
      Row() {
        Text(this.isEdit ? '编辑${name}' : '新建${name}')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
      }
      .width('100%')
      .height(56)
      .padding({ left: 16, right: 16 })
      .backgroundColor(Color.White)

      // Form
      Scroll() {
        Column({ space: 16 }) {
          // Name field
          TextInput({ placeholder: '名称', text: this.name })
            .width('100%')
            .height(48)
            .backgroundColor(Color.White)
            .onChange((value) => this.name = value)

          // Description field
          TextArea({ placeholder: '描述', text: this.description })
            .width('100%')
            .height(120)
            .backgroundColor(Color.White)
            .onChange((value) => this.description = value)
        }
        .width('100%')
        .padding(16)
      }
      .layoutWeight(1)

      // Footer
      Row({ space: 12 }) {
        Button('取消')
          .width(100)
          .height(48)
          .fontColor('#666')
          .backgroundColor('#F5F5F5')

        Button(this.isSubmitting ? '保存中...' : '保存')
          .layoutWeight(1)
          .height(48)
          .fontColor(Color.White)
          .backgroundColor('#FF6B35')
          .enabled(!this.isSubmitting)
          .onClick(() => this.handleSubmit())
      }
      .width('100%')
      .height(80)
      .padding(16)
      .backgroundColor(Color.White)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }

  private async handleSubmit() {
    this.isSubmitting = true;
    // [TODO] 实现提交逻辑
    this.isSubmitting = false;
  }
}
EOF

    success "表单页已生成: $output_file"
}

# 主函数
main() {
    show_banner

    local type="${1:-}"
    local name="${2:-}"

    if [ -z "$type" ] || [ -z "$name" ]; then
        error "缺少参数"
        echo ""
        echo "用法: bash scripts/generate.sh <type> <name>"
        echo ""
        echo "基础类型:"
        echo "  model      - 生成数据模型"
        echo "  service    - 生成服务类"
        echo "  page       - 生成基础页面"
        echo "  viewmodel  - 生成ViewModel"
        echo "  test       - 生成测试文件"
        echo ""
        echo "增强类型:"
        echo "  list-page  - 生成列表页(下拉刷新/加载更多)"
        echo "  form-page  - 生成表单页(新增/编辑)"
        echo ""
        echo "示例:"
        echo "  bash scripts/generate.sh model User"
        echo "  bash scripts/generate.sh service UserService"
        echo "  bash scripts/generate.sh list-page User"
        echo "  bash scripts/generate.sh form-page User"
        exit 1
    fi

    check_dependencies

    case "$type" in
        model)
            generate_model "$name"
            ;;
        service)
            generate_service "$name"
            ;;
        page)
            generate_page "$name"
            ;;
        list-page)
            generate_list_page "$name"
            ;;
        form-page)
            generate_form_page "$name"
            ;;
        viewmodel)
            generate_viewmodel "$name"
            ;;
        test)
            generate_test "$name"
            ;;
        *)
            error "未知类型: $type"
            echo "支持的类型: model, service, page, list-page, form-page, viewmodel, test"
            exit 1
            ;;
    esac

    echo ""
    success "代码生成完成！"
    echo ""
    echo "下一步:"
    echo "  1. 检查生成的代码"
    echo "  2. 实现 [TODO] 标记的业务逻辑"
    echo "  3. 运行编译验证: bash scripts/build-check.sh"
}

main "$@"
