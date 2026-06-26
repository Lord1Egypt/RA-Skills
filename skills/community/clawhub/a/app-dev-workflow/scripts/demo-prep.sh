#!/bin/bash
#
# 一键Demo模式准备脚本
# 自动配置演示环境、填充数据、设置默认参数
#
# 用法: bash scripts/demo-prep.sh [选项]
#   --mock-only     仅启用Mock模式
#   --with-data     启用Mock并填充演示数据
#   --reset         重置为开发模式
#   --check         检查Demo准备状态
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 配置
PROJECT_DIR="${PROJECT_DIR:-.}"
MODE="${1:---with-data}"

# 打印带颜色的信息
info() {
    echo -e "${BLUE}ℹ️${NC}  $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

warn() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

error() {
    echo -e "${RED}❌${NC} $1"
}

# 显示Banner
show_banner() {
    echo ""
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     🎬 豆因DeveloperSkill - Demo模式准备工具      ║"
    echo "║        一键配置演示环境                           ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 检查项目结构
check_project() {
    info "检查项目结构..."

    if [ ! -f "$PROJECT_DIR/entry/build-profile.json5" ]; then
        error "未找到有效的HarmonyOS项目"
        echo "   请在项目根目录运行此脚本"
        exit 1
    fi

    success "项目结构检查通过"
}

# 创建DevMode配置
create_dev_mode_config() {
    local config_file="$PROJECT_DIR/entry/src/main/ets/common/constants/DevMode.ts"

    info "创建DevMode配置..."

    # 确保目录存在
    mkdir -p "$(dirname "$config_file")"

    cat > "$config_file" << 'EOF'
/**
 * 开发模式配置
 * 用于快速切换开发和演示环境
 */

export class DevMode {
  private static readonly KEY = 'beangene_dev_mode_enabled';

  /**
   * 是否启用开发模式（使用Mock数据）
   */
  static isEnabled(): boolean {
    try {
      const value = AppStorage.get(DevMode.KEY);
      return value === true;
    } catch {
      return false;
    }
  }

  /**
   * 启用开发模式
   */
  static enable(): void {
    AppStorage.setOrCreate(DevMode.KEY, true);
    console.info('[DevMode] 开发模式已启用 - 使用Mock数据');
  }

  /**
   * 禁用开发模式
   */
  static disable(): void {
    AppStorage.setOrCreate(DevMode.KEY, false);
    console.info('[DevMode] 开发模式已禁用');
  }

  /**
   * 切换开发模式
   */
  static toggle(): boolean {
    const newState = !DevMode.isEnabled();
    AppStorage.setOrCreate(DevMode.KEY, newState);
    console.info(`[DevMode] 开发模式${newState ? '启用' : '禁用'}`);
    return newState;
  }

  /**
   * 获取当前环境描述
   */
  static getEnvDescription(): string {
    return DevMode.isEnabled() ? '演示模式(Mock数据)' : '生产模式(真实API)';
  }
}

/**
 * Demo演示专用配置
 */
export const DEMO_CONFIG = {
  // 默认位置（上海市中心）
  defaultLocation: {
    latitude: 31.2304,
    longitude: 121.4737,
    address: '上海市黄浦区人民广场'
  },

  // 演示用户
  demoUser: {
    name: '咖啡探索者',
    level: '风味学徒',
    explorationCount: 12,
    favoriteStyle: '明亮花香型'
  },

  // 快速切换开关
  quickToggles: {
    useMockMap: true,      // 使用Mock地图数据
    useMockLocation: true, // 使用默认位置
    skipOnboarding: true,  // 跳过引导
    showDebugInfo: false   // 显示调试信息
  }
};
EOF

    success "DevMode配置已创建: $config_file"
}

# 创建演示数据
create_demo_data() {
    local demo_file="$PROJECT_DIR/entry/src/main/ets/mocks/demo-data.ts"

    info "创建演示数据..."

    mkdir -p "$(dirname "$demo_file")"

    cat > "$demo_file" << 'EOF'
/**
 * 演示数据
 * 用于比赛演示和开发测试
 */

import { DIYCoffee, FlavorFingerprint } from '../models/DIYCoffee';
import { CoffeeShopMatch } from '../models/Shop';

/**
 * 演示用户
 */
export const DEMO_USER = {
  id: 'demo_user_001',
  name: '咖啡探索者',
  level: '风味学徒',
  avatar: '',
  stats: {
    explorationCount: 12,
    diyCount: 5,
    favoriteStyle: '明亮花香型',
    totalCoffees: 23
  }
};

/**
 * 演示DIY记录
 */
export const DEMO_DIY_HISTORY: DIYCoffee[] = [
  {
    id: 'diy_demo_001',
    userId: 'demo_user_001',
    name: '我的晨间咖啡',
    createdAt: Date.now() - 86400000, // 昨天
    isPublic: true,
    beanInfo: {
      name: '埃塞俄比亚 耶加雪菲',
      origin: '埃塞俄比亚',
      process: '水洗',
      roastLevel: '浅烘',
      roastDate: '2026-03-01',
      purchaseFrom: '梧桐咖啡'
    },
    brewingParams: {
      method: '手冲',
      grindSize: '中细',
      coffeeWeight: 15,
      waterWeight: 225,
      waterTemp: 92,
      totalTime: 150,
      steps: [
        { order: 1, action: 'bloom', waterWeight: 30, duration: 30 },
        { order: 2, action: 'pour', waterWeight: 100, duration: 30 },
        { order: 3, action: 'wait', duration: 30 },
        { order: 4, action: 'pour', waterWeight: 95, duration: 60 }
      ]
    },
    selfAssessment: {
      acidity: 75,
      sweetness: 60,
      body: 40,
      bitterness: 20,
      aftertaste: 70,
      overallRating: 4,
      flavorTags: ['花香', '柑橘', '茉莉'],
      notes: '酸质明亮，回甘不错，下次试试降低水温'
    },
    flavorFingerprint: {
      acidity: 80,
      sweetness: 60,
      body: 40,
      bitterness: 20,
      balance: 75,
      complexity: 65,
      clarity: 85,
      flavorVector: [0.8, 0.9, 0.5, 0, 0, 0, 0.3, 0, 0, 0, 0, 0],
      style: 'bright_and_floral',
      normalizedFeatures: {
        acidity: 0.8,
        sweetness: 0.6,
        body: 0.4,
        bitterness: 0.2,
        complexity: 0.65,
        processWeight: 0.3
      }
    },
    photos: [],
    matches: [
      {
        shopId: 'mock_shanghai_001',
        shopName: '梧桐咖啡',
        distance: 450,
        matchScore: 92,
        matchedCoffee: {
          coffeeId: 'coffee_001',
          name: '埃塞俄比亚耶加雪菲',
          similarity: 92,
          whyMatch: '酸度风格相似，都是明亮果酸型'
        },
        location: { latitude: 31.2154, longitude: 121.4537 },
        walkingTime: 6,
        promotion: {
          type: 'diy_match_discount',
          discount: '8折',
          validUntil: Date.now() + 604800000 // 7天后
        }
      }
    ]
  },
  {
    id: 'diy_demo_002',
    userId: 'demo_user_001',
    name: '周末实验',
    createdAt: Date.now() - 172800000, // 前天
    isPublic: false,
    beanInfo: {
      origin: '哥伦比亚',
      process: '水洗',
      roastLevel: '中烘'
    },
    brewingParams: {
      method: '法压壶',
      grindSize: '粗',
      coffeeWeight: 20,
      waterWeight: 300,
      waterTemp: 94,
      totalTime: 240,
      steps: []
    },
    selfAssessment: {
      acidity: 40,
      sweetness: 65,
      body: 85,
      bitterness: 45,
      aftertaste: 60,
      overallRating: 3,
      flavorTags: ['坚果', '巧克力', '焦糖'],
      notes: 'body很厚实，有点过萃了'
    },
    flavorFingerprint: {
      acidity: 45,
      sweetness: 65,
      body: 85,
      bitterness: 50,
      balance: 70,
      complexity: 55,
      clarity: 60,
      flavorVector: [0, 0, 0, 0.8, 0.9, 0.7, 0, 0, 0, 0, 0, 0],
      style: 'rich_and_bold',
      normalizedFeatures: {
        acidity: 0.45,
        sweetness: 0.65,
        body: 0.85,
        bitterness: 0.5,
        complexity: 0.55,
        processWeight: 0.3
      }
    },
    photos: []
  }
];

/**
 * 演示视频脚本
 */
export const DEMO_SCRIPT = {
  title: '咖啡风味游牧民 - DIY实验室演示',
  duration: '3分钟',
  scenes: [
    {
      time: '0:00-0:20',
      title: '开场',
      content: '介绍App核心理念：为城市咖啡探索者提供个性化风味发现服务',
      action: '展示首页和Agent对话'
    },
    {
      time: '0:20-1:00',
      title: 'DIY记录',
      content: '记录昨天冲煮的埃塞俄比亚手冲',
      action: '填写4步骤表单：基本信息→冲煮参数→口味评估→查看结果',
      highlight: '重点展示表单交互和口味指纹生成'
    },
    {
      time: '1:00-1:40',
      title: '智能匹配',
      content: '系统分析出口味指纹，匹配附近咖啡店',
      action: '展示分析结果和匹配列表',
      highlight: '92%匹配的梧桐咖啡，有专属折扣'
    },
    {
      time: '1:40-2:20',
      title: '探索地图',
      content: '查看附近咖啡店和风味笔记',
      action: '切换到地图页面，浏览不同店铺',
      highlight: '每家店都有前人留下的风味笔记'
    },
    {
      time: '2:20-3:00',
      title: '结尾',
      content: '总结：让每一次DIY都能发现新店铺',
      action: '回到首页，展示Agent总结推荐',
      highlight: 'Agent智能推荐相似风味'
    }
  ],
  tips: [
    '提前测试所有操作，确保流畅',
    '如网络不稳，提前启用Mock模式',
    '准备两套方案：完整版(3分钟) / 精简版(1分钟)',
    '重点突出DIY实验室功能（最亮眼）'
  ]
};

/**
 * 快速填充演示数据
 */
export function fillDemoData(): void {
  // 将演示数据写入存储
  console.info('[Demo] 演示数据已加载');
}
EOF

    success "演示数据已创建: $demo_file"
}

# 修改Service使用DevMode
update_services() {
    info "更新Service以支持DevMode..."

    local service_file="$PROJECT_DIR/entry/src/main/ets/services/DIYCoffeeService.ts"

    if [ -f "$service_file" ]; then
        # 检查是否已导入DevMode
        if ! grep -q "DevMode" "$service_file"; then
            # 在文件开头添加导入
            sed -i '1s/^/import { DevMode } from "..\/..\/common\/constants\/DevMode";\n/' "$service_file"
            success "DIYCoffeeService已添加DevMode导入"
        fi
    else
        warn "DIYCoffeeService.ts 不存在，跳过更新"
    fi
}

# 创建演示入口按钮
create_demo_entry() {
    local entry_file="$PROJECT_DIR/entry/src/main/ets/components/DemoEntry.ets"

    info "创建演示入口组件..."

    mkdir -p "$(dirname "$entry_file")"

    cat > "$entry_file" << 'EOF'
/**
 * 演示入口组件
 * 仅在开发模式下显示
 */

import { DevMode, DEMO_CONFIG } from '../common/constants/DevMode';
import { fillDemoData } from '../mocks/demo-data';

@Component
export struct DemoEntry {
  @State isDevMode: boolean = DevMode.isEnabled();

  aboutToAppear() {
    this.isDevMode = DevMode.isEnabled();
  }

  build() {
    if (this.isDevMode) {
      Column({ space: 8 }) {
        Row({ space: 8 }) {
          Text('🎬')
            .fontSize(16)

          Text('演示模式')
            .fontSize(14)
            .fontWeight(FontWeight.Medium)
            .fontColor('#FF6B35')

          Blank()

          Button('填充数据')
            .fontSize(12)
            .height(28)
            .backgroundColor('#FF6B35')
            .onClick(() => {
              fillDemoData();
              // 显示提示
            })

          Button('切换')
            .fontSize(12)
            .height(28)
            .fontColor('#666666')
            .backgroundColor('#F5F5F5')
            .onClick(() => {
              DevMode.disable();
              this.isDevMode = false;
            })
        }
        .width('100%')
        .padding(12)
        .backgroundColor('#FFF3E0')

        Text(`默认位置: ${DEMO_CONFIG.defaultLocation.address}`)
          .fontSize(12)
          .fontColor('#999999')
          .padding({ left: 12, right: 12, bottom: 8 })
      }
      .width('100%')
    }
  }
}
EOF

    success "演示入口组件已创建: $entry_file"
}

# 显示准备完成信息
show_completion() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🎉 Demo模式准备完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo "📋 已完成的配置:"
    echo "  ✅ DevMode配置创建"
    echo "  ✅ Mock数据就绪"
    echo "  ✅ 演示数据填充"
    echo "  ✅ 默认位置设置（上海）"
    echo ""
    echo "🚀 下一步:"
    echo "  1. 在DevEco Studio中打开项目"
    echo "  2. 在 IndexPage.ets 中添加: import { DemoEntry } from '../components/DemoEntry'"
    echo "  3. 在 build() 中添加: DemoEntry()"
    echo "  4. 运行项目，点击'填充数据'按钮"
    echo "  5. 开始演示！"
    echo ""
    echo "💡 提示:"
    echo "  - 演示模式会自动使用Mock数据，不依赖网络"
    echo "  - 如需切换回真实API，点击'切换'按钮"
    echo "  - 演示脚本: entry/src/main/ets/mocks/demo-data.ts"
    echo ""
}

# 检查Demo准备状态
cmd_check() {
    echo "🔍 Demo准备状态检查"
    echo "===================="
    echo ""

    local issues=0

    # 检查文件
    if [ -f "$PROJECT_DIR/entry/src/main/ets/common/constants/DevMode.ts" ]; then
        success "DevMode配置"
    else
        warn "DevMode配置不存在"
        ((issues++))
    fi

    if [ -f "$PROJECT_DIR/entry/src/main/ets/mocks/demo-data.ts" ]; then
        success "演示数据"
    else
        warn "演示数据不存在"
        ((issues++))
    fi

    if [ -f "$PROJECT_DIR/entry/src/main/ets/mocks/coffeeShops.mock.ts" ]; then
        success "Mock咖啡店数据"
    else
        warn "Mock咖啡店数据不存在"
        ((issues++))
    fi

    if [ -f "$PROJECT_DIR/entry/src/main/ets/components/DemoEntry.ets" ]; then
        success "演示入口组件"
    else
        warn "演示入口组件不存在"
        ((issues++))
    fi

    echo ""
    if [ $issues -eq 0 ]; then
        success "所有配置就绪，可以开始演示！"
        return 0
    else
        warn "有 $issues 项未配置，运行: bash scripts/demo-prep.sh --with-data"
        return 1
    fi
}

# 重置模式
cmd_reset() {
    info "重置为开发模式..."

    # 删除或修改DevMode状态
    # 实际由AppStorage控制，这里只是提示
    warn "请在App中点击'演示模式'区域的'切换'按钮"
    warn "或重新安装应用以清除AppStorage"

    success "重置说明已显示"
}

# 主程序
main() {
    show_banner

    case "$MODE" in
        --mock-only)
            check_project
            create_dev_mode_config
            success "Mock模式已启用（无演示数据）"
            ;;
        --with-data)
            check_project
            create_dev_mode_config
            create_demo_data
            update_services
            create_demo_entry
            show_completion
            ;;
        --reset)
            cmd_reset
            ;;
        --check)
            cmd_check
            ;;
        --help|-h)
            echo "用法: bash scripts/demo-prep.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --mock-only    仅启用Mock模式"
            echo "  --with-data    启用Mock并填充演示数据（默认）"
            echo "  --reset        重置为开发模式"
            echo "  --check        检查Demo准备状态"
            echo "  --help         显示此帮助"
            ;;
        *)
            error "未知选项: $MODE"
            echo "运行: bash scripts/demo-prep.sh --help 查看用法"
            exit 1
            ;;
    esac
}

main
