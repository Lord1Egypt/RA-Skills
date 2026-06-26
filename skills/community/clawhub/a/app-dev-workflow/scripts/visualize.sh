#!/bin/bash
#
# 架构可视化工具 - 生成项目架构图和依赖关系
#
# 用法: bash scripts/visualize.sh [命令] [选项]
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

OUTPUT_DIR="docs/architecture"

# 显示帮助
show_help() {
    echo "架构可视化工具"
    echo ""
    echo "用法: bash scripts/visualize.sh <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  all          生成所有图表"
    echo "  structure    生成目录结构图"
    echo "  deps         生成依赖关系图"
    echo "  flow         生成数据流图"
    echo "  class        生成类关系图"
    echo ""
    echo "选项:"
    echo "  --output     指定输出目录 (默认: docs/architecture)"
    echo "  --format     输出格式: mermaid|svg|png (默认: mermaid)"
    echo ""
}

# 确保输出目录存在
ensure_output_dir() {
    mkdir -p "$OUTPUT_DIR"
}

# 生成目录结构图
gen_structure() {
    step "生成目录结构图..."
    ensure_output_dir

    local output_file="$OUTPUT_DIR/structure.mmd"

    cat > "$output_file" << 'EOF'
%% 项目目录结构图
graph TD
    Root[项目根目录] --> Src[src]
    Root --> Test[test]
    Root --> Scripts[scripts]
    Root --> Docs[docs]
    Root --> Config[配置文件]

    Src --> Common[common]
    Src --> Pages[pages]
    Src --> Services[services]
    Src --> Models[models]
    Src --> ViewModels[viewmodels]
    Src --> Components[components]

    Common --> Utils[utils]
    Common --> Constants[constants]
    Common --> Types[types]

    Test --> UnitTest[unittest]
    Test --> Integration[integration]
    Test --> E2E[e2e]

    Docs --> Prd[prd]
    Docs --> Api[api]
    Docs --> Arch[architecture]

    style Root fill:#FF6B35,stroke:#333,stroke-width:2px,color:#fff
    style Src fill:#4ECDC4,stroke:#333,stroke-width:1px
    style Test fill:#96CEB4,stroke:#333,stroke-width:1px
    style Docs fill:#FFEAA7,stroke:#333,stroke-width:1px
EOF

    success "目录结构图: $output_file"
}

# 生成依赖关系图
gen_deps() {
    step "生成模块依赖关系图..."
    ensure_output_dir

    local output_file="$OUTPUT_DIR/dependencies.mmd"

    # 分析实际依赖
    local deps=""
    if [ -d "src" ]; then
        # 找出服务之间的依赖
        for service in src/services/*.ts 2>/dev/null; do
            if [ -f "$service" ]; then
                local name=$(basename "$service" .ts)
                # 查找导入的其他服务
                grep -h "import.*from.*services/" "$service" 2>/dev/null | \
                sed 's/.*services\/\([^'"'"'"'"']*\).*/\1/' | \
                while read -r dep; do
                    if [ "$dep" != "$name" ] && [ -n "$dep" ]; then
                        echo "    $name --> $dep"
                    fi
                done
            fi
        done
    fi

    cat > "$output_file" << EOF
%% 模块依赖关系图
graph LR
    %% 层定义
    subgraph UI层
        Pages[Pages]
        Components[Components]
    end

    subgraph 逻辑层
        ViewModels[ViewModels]
        Services[Services]
    end

    subgraph 数据层
        Models[Models]
        API[API Clients]
    end

    %% 依赖关系
    Pages --> ViewModels
    Pages --> Components
    ViewModels --> Services
    ViewModels --> Models
    Services --> Models
    Services --> API

    %% 实际依赖（自动检测）
$(if [ -d "src/services" ]; then
    for f in src/services/*.ts 2>/dev/null; do
        if [ -f "$f" ]; then
            name=$(basename "$f" .ts)
            imports=$(grep -o "from '../services/[^']*'" "$f" 2>/dev/null | sed "s/from '..\/services\//    $name --> /" | sed "s/'//g" || true)
            if [ -n "$imports" ]; then
                echo "$imports"
            fi
        fi
    done
fi)

    style UI层 fill:#E3F2FD,stroke:#1976D2
    style 逻辑层 fill:#FFF3E0,stroke:#F57C00
    style 数据层 fill:#E8F5E9,stroke:#388E3C
EOF

    success "依赖关系图: $output_file"
}

# 生成数据流图
gen_flow() {
    step "生成数据流图..."
    ensure_output_dir

    local output_file="$OUTPUT_DIR/dataflow.mmd"

    # 查找页面和对应的 ViewModel
    local page_flows=""
    if [ -d "src/pages" ]; then
        for page in src/pages/*.ets 2>/dev/null; do
            if [ -f "$page" ]; then
                local page_name=$(basename "$page" .ets)
                # 查找导入的 ViewModel
                local vm=$(grep -o "import.*ViewModel.*from.*viewmodels" "$page" 2>/dev/null | head -1)
                if [ -n "$vm" ]; then
                    local vm_name=$(echo "$vm" | grep -o "{[^}]*}" | tr -d '{}' | tr -d ' ')
                    page_flows="${page_flows}    $page_name --> $vm_name\n"
                fi
            fi
        done
    fi

    cat > "$output_file" << EOF
%% 数据流图
sequenceDiagram
    autonumber
    participant U as 用户
    participant P as Page
    participant VM as ViewModel
    participant S as Service
    participant API as API/DB

    %% 标准交互流程
    U->>P: 用户操作
    P->>VM: 调用方法
    activate VM
    VM->>VM: 更新状态(loading)
    VM->>S: 调用业务逻辑
    activate S
    S->>API: 请求数据
    activate API
    API-->>S: 返回数据
    deactivate API
    S-->>VM: 返回结果
    deactivate S
    VM->>VM: 更新状态(data/error)
    VM-->>P: 通知更新
    deactivate VM
    P-->>U: 显示结果

    %% 实际页面流程（自动检测）
$(if [ -d "src/pages" ]; then
    for f in src/pages/*.ets 2>/dev/null; do
        if [ -f "$f" ]; then
            name=$(basename "$f" .ets)
            echo "    Note over U,P: $name 页面"
        fi
    done
fi)
EOF

    success "数据流图: $output_file"
}

# 生成类关系图
gen_class() {
    step "生成类关系图..."
    ensure_output_dir

    local output_file="$OUTPUT_DIR/class-diagram.mmd"

    cat > "$output_file" << 'EOF'
%% 类关系图
classDiagram
    %% 基础类
    class BaseService {
        +getInstance()$ BaseService
        #errorHandler: GlobalErrorHandler
        +init() Promise~boolean~
        #handleError(error, context) void
    }

    class BaseViewModel {
        +loading: boolean
        +error: string
        +hasError() boolean
        +setLoading(value) void
        +setError(message) void
        +reset() void
    }

    class GlobalErrorHandler {
        +getInstance()$ GlobalErrorHandler
        +handle(error, context) void
        +report(error) void
    }

    %% 关系
    BaseService --> GlobalErrorHandler : uses
    BaseViewModel ..> GlobalErrorHandler : notifies

    %% 实际服务类（自动检测）
EOF

    # 添加检测到的服务类
    if [ -d "src/services" ]; then
        for service in src/services/*.ts 2>/dev/null; do
            if [ -f "$service" ]; then
                local name=$(basename "$service" .ts)
                if [ "$name" != "index" ]; then
                    echo "" >> "$output_file"
                    echo "    class $name {" >> "$output_file"
                    # 提取公共方法
                    grep -o "public async [a-zA-Z]*" "$service" 2>/dev/null | \
                    sed 's/public async /        +/' | \
                    sed 's/$/() Promise~any~/' >> "$output_file" || true
                    echo "    }" >> "$output_file"
                    echo "    BaseService <|-- $name" >> "$output_file"
                fi
            fi
        done
    fi

    # 添加检测到的 ViewModel 类
    if [ -d "src/viewmodels" ]; then
        for vm in src/viewmodels/*.ts 2>/dev/null; do
            if [ -f "$vm" ]; then
                local name=$(basename "$vm" .ts)
                echo "" >> "$output_file"
                echo "    class $name {" >> "$output_file"
                echo "    }" >> "$output_file"
                echo "    BaseViewModel <|-- $name" >> "$output_file"
            fi
        done
    fi

    success "类关系图: $output_file"
}

# 生成开发流程图
gen_dev_flow() {
    step "生成开发流程图..."
    ensure_output_dir

    local output_file="$OUTPUT_DIR/dev-workflow.mmd"

    cat > "$output_file" << 'EOF'
%% 开发工作流程图
flowchart TB
    subgraph Stage1[阶段1: 产品设计]
        P1[功能设计] --> P2[PRD文档]
        P2 --> P3[需求评审]
    end

    subgraph Stage2[阶段2: 代码生成]
        G1[选择模板] --> G2[生成骨架]
        G2 --> G3[目录结构]
    end

    subgraph Stage3[阶段3: 功能实现]
        I1[编写测试] --> I2[运行测试]
        I2 -->|Red| I3[实现代码]
        I3 --> I4[运行测试]
        I4 -->|Green| I5[重构优化]
        I5 --> I2
    end

    subgraph Stage4[阶段4: 验证测试]
        V1[单元测试] --> V2[集成测试]
        V2 --> V3[编译检查]
        V3 --> V4[代码规范]
    end

    subgraph Stage5[阶段5: 版本集成]
        R1[版本更新] --> R2[更新日志]
        R2 --> R3[代码提交]
    end

    Stage1 --> Stage2
    Stage2 --> Stage3
    Stage3 --> Stage4
    Stage4 --> Stage5

    style Stage1 fill:#E3F2FD,stroke:#1976D2
    style Stage2 fill:#FFF3E0,stroke:#F57C00
    style Stage3 fill:#F3E5F5,stroke:#7B1FA2
    style Stage4 fill:#E8F5E9,stroke:#388E3C
    style Stage5 fill:#FFEBEE,stroke:#C62828
EOF

    success "开发流程图: $output_file"
}

# 生成所有图表
gen_all() {
    step "生成所有架构图..."

    gen_structure
    gen_deps
    gen_flow
    gen_class
    gen_dev_flow

    echo ""
    success "所有图表生成完成！"
    info "输出目录: $OUTPUT_DIR"
    echo ""
    echo "生成的文件:"
    ls -1 "$OUTPUT_DIR/" 2>/dev/null | sed 's/^/  - /'
    echo ""
    echo "查看方式:"
    echo "  1. 安装 Mermaid 插件到 VS Code"
    echo "  2. 使用 Mermaid Live Editor: https://mermaid.live"
    echo "  3. 运行: bash scripts/visualize.sh --format=svg"
}

# 生成 HTML 预览
gen_html_preview() {
    step "生成 HTML 预览..."
    ensure_output_dir

    local html_file="$OUTPUT_DIR/index.html"

    cat > "$html_file" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>项目架构图</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .diagram {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .diagram h2 {
            color: #FF6B35;
            margin-bottom: 15px;
            font-size: 18px;
        }
        .mermaid {
            text-align: center;
        }
        .update-time {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏗️ 项目架构可视化</h1>
EOF

    # 为每个 mmd 文件添加图表
    for file in "$OUTPUT_DIR"/*.mmd; do
        if [ -f "$file" ]; then
            local name=$(basename "$file" .mmd)
            local title=$(echo "$name" | sed 's/-/ /g' | sed 's/.*/\u&/')
            echo "        <div class=\"diagram\">" >> "$html_file"
            echo "            <h2>📊 $title</h2>" >> "$html_file"
            echo "            <div class=\"mermaid\">" >> "$html_file"
            cat "$file" >> "$html_file"
            echo "" >> "$html_file"
            echo "            </div>" >> "$html_file"
            echo "        </div>" >> "$html_file"
        fi
    done

    cat >> "$html_file" << EOF
        <div class="update-time">
            更新时间: $(date '+%Y-%m-%d %H:%M:%S')
        </div>
    </div>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            flowchart: { useMaxWidth: true, htmlLabels: true },
            sequence: { useMaxWidth: true },
            class: { useMaxWidth: true }
        });
    </script>
</body>
</html>
EOF

    success "HTML 预览: $html_file"
    info "用浏览器打开查看完整架构图"
}

# 主函数
main() {
    local cmd="${1:-all}"

    case "$cmd" in
        all)
            gen_all
            gen_html_preview
            ;;
        structure)
            gen_structure
            ;;
        deps)
            gen_deps
            ;;
        flow)
            gen_flow
            ;;
        class)
            gen_class
            ;;
        workflow)
            gen_dev_flow
            ;;
        html)
            gen_html_preview
            ;;
        --help|-h)
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
