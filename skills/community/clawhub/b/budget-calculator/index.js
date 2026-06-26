/**
 * 装修大包预算计算服务
 * 基于《教波比做装修大包预算（极简步骤 + 固定规则）》文档
 */

class BudgetService {
  constructor() {
    this.DEFAULT_FLOOR_HEIGHT = 2.6
    this.MANAGEMENT_FEE_RATE = 0.06
    this.TILE_WASTAGE_RATE = 0.1
  }

  calculateSpaceAreas(totalArea) {
    let config = {}

    if (totalArea <= 60) {
      config = {
        '客餐厅': 0.35,
        '卧室': 0.25,
        '厨房': 0.10,
        '卫生间': 0.08,
        '阳台': 0.07,
      }
    } else if (totalArea <= 100) {
      config = {
        '客餐厅': 0.30,
        '主卧': 0.18,
        '次卧': 0.15,
        '厨房': 0.08,
        '卫生间': 0.12,
        '阳台': 0.07,
      }
    } else {
      config = {
        '客餐厅': 0.28,
        '主卧': 0.15,
        '次卧': 0.12,
        '书房/三卧': 0.10,
        '厨房': 0.07,
        '主卫': 0.07,
        '次卫': 0.06,
        '阳台': 0.08,
      }
    }

    const spaces = []
    let remainingArea = totalArea

    Object.entries(config).forEach(([name, ratio], index, arr) => {
      const floorArea = index === arr.length - 1
        ? Math.round(remainingArea)
        : Math.round(totalArea * ratio)
      remainingArea -= floorArea

      const perimeter = Math.sqrt(floorArea) * 4
      const wallArea = Math.round(perimeter * this.DEFAULT_FLOOR_HEIGHT * 0.85)

      spaces.push({
        name,
        floorArea,
        wallArea,
        ceilingArea: floorArea,
      })
    })

    return spaces
  }

  calculateWaterElectricFee(area, houseType) {
    const items = []

    let lineLength = Math.round(area * 4)

    if (houseType === 'new') {
      lineLength = Math.round(lineLength / 2)
    }

    items.push({
      name: houseType === 'new' ? '水电断点改造' : '水电全改',
      price: 45 * lineLength,
      unit: '米',
      quantity: lineLength,
      category: '半包施工',
      subCategory: '水电工程',
    })

    return items
  }

  calculateTileCount(area, tileSize) {
    const tileAreaMap = {
      '800×800': 0.64,
      '400×400': 0.16,
      '400×800': 0.32,
    }

    const singleTileArea = tileAreaMap[tileSize] || 0.64
    const baseCount = Math.round(area / singleTileArea)
    return Math.ceil(baseCount * (1 + this.TILE_WASTAGE_RATE))
  }

  calculateBudget(input) {
    const { communityName, area, houseType = 'new' } = input
    const items = []

    const spaces = this.calculateSpaceAreas(area)

    const totalFloorArea = spaces.reduce((sum, s) => sum + s.floorArea, 0)
    const totalWallArea = spaces.reduce((sum, s) => sum + s.wallArea, 0)
    const totalCeilingArea = spaces.reduce((sum, s) => sum + s.ceilingArea, 0)
    const wallAndCeilingArea = totalWallArea + totalCeilingArea

    const bathroomCount = area > 100 ? 2 : 1
    const bathroomArea = spaces.filter(s => s.name.includes('卫')).reduce((sum, s) => sum + s.floorArea, 0) || Math.round(totalFloorArea * 0.12)
    const kitchenArea = spaces.filter(s => s.name.includes('厨房')).reduce((sum, s) => sum + s.floorArea, 0) || Math.round(totalFloorArea * 0.08)

    const halfPackageItems = []

    halfPackageItems.push(
      {
        name: '铲墙皮',
        price: 5 * wallAndCeilingArea,
        unit: 'm²',
        quantity: wallAndCeilingArea,
        category: '半包施工',
        subCategory: '油工工程',
      },
      {
        name: '刷墙固',
        price: 6 * wallAndCeilingArea,
        unit: 'm²',
        quantity: wallAndCeilingArea,
        category: '半包施工',
        subCategory: '油工工程',
      },
      {
        name: '刮腻子',
        price: 15 * wallAndCeilingArea,
        unit: 'm²',
        quantity: wallAndCeilingArea,
        category: '半包施工',
        subCategory: '油工工程',
      },
      {
        name: '砂纸打磨',
        price: 5 * wallAndCeilingArea,
        unit: 'm²',
        quantity: wallAndCeilingArea,
        category: '半包施工',
        subCategory: '油工工程',
      },
      {
        name: '刷乳胶漆',
        price: 12 * wallAndCeilingArea,
        unit: 'm²',
        quantity: wallAndCeilingArea,
        category: '半包施工',
        subCategory: '油工工程',
      }
    )

    const totalTileFloorArea = totalFloorArea - bathroomArea
    const wallTileArea = Math.round((bathroomArea + kitchenArea) * 2.6 * 2)

    halfPackageItems.push(
      {
        name: '地砖铺贴（800×800）',
        price: 85 * totalTileFloorArea,
        unit: 'm²',
        quantity: totalTileFloorArea,
        category: '半包施工',
        subCategory: '瓦工工程',
      },
      {
        name: '卫生间地砖铺贴（400×400）',
        price: 85 * bathroomArea,
        unit: 'm²',
        quantity: bathroomArea,
        category: '半包施工',
        subCategory: '瓦工工程',
      },
      {
        name: '墙砖铺贴（400×800）',
        price: 85 * wallTileArea,
        unit: 'm²',
        quantity: wallTileArea,
        category: '半包施工',
        subCategory: '瓦工工程',
      },
      {
        name: '厨卫防水',
        price: 85 * (bathroomArea + kitchenArea) * 1.8,
        unit: 'm²',
        quantity: Math.round((bathroomArea + kitchenArea) * 1.8),
        category: '半包施工',
        subCategory: '瓦工工程',
      },
      {
        name: '包立管',
        price: 450 * bathroomCount,
        unit: '项',
        quantity: bathroomCount,
        category: '半包施工',
        subCategory: '瓦工工程',
      },
      {
        name: '下水管降噪处理',
        price: 350 * bathroomCount,
        unit: '项',
        quantity: bathroomCount,
        category: '半包施工',
        subCategory: '瓦工工程',
      }
    )

    if (houseType === 'old') {
      halfPackageItems.push({
        name: '地面水泥砂浆找平',
        price: 45 * Math.round(totalFloorArea * 0.4),
        unit: 'm²',
        quantity: Math.round(totalFloorArea * 0.4),
        category: '半包施工',
        subCategory: '瓦工工程',
      })
    }

    const totalPerimeter = spaces.reduce((sum, s) => sum + Math.sqrt(s.floorArea) * 4, 0)
    halfPackageItems.push(
      {
        name: '石膏线/双眼皮',
        price: 15 * Math.round(totalPerimeter),
        unit: '米',
        quantity: Math.round(totalPerimeter),
        category: '半包施工',
        subCategory: '木工工程',
      },
      {
        name: '窗帘盒',
        price: 80 * Math.ceil(area / 30),
        unit: '米',
        quantity: Math.ceil(area / 30) * 2,
        category: '半包施工',
        subCategory: '木工工程',
      }
    )

    const waterElectricItems = this.calculateWaterElectricFee(area, houseType)
    halfPackageItems.push(...waterElectricItems)

    const minArea = Math.max(area, 30)
    halfPackageItems.push(
      {
        name: '材料上楼费',
        price: 8 * minArea,
        unit: 'm²',
        quantity: minArea,
        category: '半包施工',
        subCategory: '其他杂费',
      },
      {
        name: '成品保护费',
        price: 12 * minArea,
        unit: 'm²',
        quantity: minArea,
        category: '半包施工',
        subCategory: '其他杂费',
      },
      {
        name: '垃圾清运费',
        price: 15 * minArea,
        unit: 'm²',
        quantity: minArea,
        category: '半包施工',
        subCategory: '其他杂费',
      },
      {
        name: '地面固化处理',
        price: 5 * minArea,
        unit: 'm²',
        quantity: minArea,
        category: '半包施工',
        subCategory: '其他杂费',
      }
    )

    if (houseType === 'old') {
      let demolitionPricePerSqm
      if (area < 60) {
        demolitionPricePerSqm = 70
      } else if (area < 90) {
        demolitionPricePerSqm = 60
      } else {
        demolitionPricePerSqm = 50
      }
      halfPackageItems.push({
        name: '全屋拆砸费用',
        price: demolitionPricePerSqm * area,
        unit: 'm²',
        quantity: area,
        category: '半包施工',
        subCategory: '其他杂费',
      })
    }

    items.push(...halfPackageItems)

    const halfPackageBeforeManage = halfPackageItems.reduce((sum, item) => sum + item.price, 0)
    const halfPackageManagementFee = Math.round(halfPackageBeforeManage * this.MANAGEMENT_FEE_RATE)
    const halfPackagePrice = halfPackageBeforeManage + halfPackageManagementFee

    const mainMaterialItems = []

    const mainTileCount = this.calculateTileCount(totalTileFloorArea, '800×800')
    const bathroomFloorTileCount = this.calculateTileCount(bathroomArea, '400×400')
    const wallTileCount = this.calculateTileCount(wallTileArea, '400×800')

    mainMaterialItems.push(
      {
        name: '地砖（800×800）',
        price: 35 * mainTileCount,
        unit: '片',
        quantity: mainTileCount,
        category: '主材材料',
        subCategory: '瓷砖类',
      },
      {
        name: '卫生间地砖（400×400）',
        price: 12 * bathroomFloorTileCount,
        unit: '片',
        quantity: bathroomFloorTileCount,
        category: '主材材料',
        subCategory: '瓷砖类',
      },
      {
        name: '墙砖（400×800）',
        price: 15 * wallTileCount,
        unit: '片',
        quantity: wallTileCount,
        category: '主材材料',
        subCategory: '瓷砖类',
      },
      {
        name: '瓷砖美缝剂',
        price: 15 * (totalTileFloorArea + bathroomArea + wallTileArea),
        unit: 'm²',
        quantity: totalTileFloorArea + bathroomArea + wallTileArea,
        category: '主材材料',
        subCategory: '瓷砖类',
      }
    )

    const baseboardLength = Math.round(totalFloorArea * 0.4)
    mainMaterialItems.push({
      name: '地脚线',
      price: 25 * baseboardLength,
      unit: '米',
      quantity: baseboardLength,
      category: '主材材料',
      subCategory: '地板类',
    })

    mainMaterialItems.push({
      name: '铝扣板吊顶（厨卫）',
      price: 120 * (bathroomArea + kitchenArea),
      unit: 'm²',
      quantity: bathroomArea + kitchenArea,
      category: '主材材料',
      subCategory: '集成吊顶',
    })

    const doorCount = Math.ceil(area / 25)
    mainMaterialItems.push(
      {
        name: '室内套装门',
        price: 1280 * doorCount,
        unit: '套',
        quantity: doorCount,
        category: '主材材料',
        subCategory: '木门类',
      },
      {
        name: '厨房推拉门',
        price: 2500,
        unit: '套',
        quantity: 1,
        category: '主材材料',
        subCategory: '木门类',
      }
    )

    const cabinetLength = Math.max(2.5, area / 40)
    mainMaterialItems.push({
      name: '橱柜定制（地柜+吊柜）',
      price: 1200 * cabinetLength,
      unit: '米',
      quantity: Math.round(cabinetLength * 10) / 10,
      category: '主材材料',
      subCategory: '全屋定制',
    })

    mainMaterialItems.push({
      name: '卫浴三件套',
      price: 3680 * bathroomCount,
      unit: '套',
      quantity: bathroomCount,
      category: '主材材料',
      subCategory: '卫浴洁具',
    })

    mainMaterialItems.push({
      name: '开关插座套装',
      price: 798,
      unit: '套',
      quantity: 1,
      category: '主材材料',
      subCategory: '其他主材',
    })

    items.push(...mainMaterialItems)

    const mainMaterialBeforeManage = mainMaterialItems.reduce((sum, item) => sum + item.price, 0)
    const mainMaterialManagementFee = Math.round(mainMaterialBeforeManage * this.MANAGEMENT_FEE_RATE)
    const mainMaterialPrice = mainMaterialBeforeManage + mainMaterialManagementFee

    const totalPrice = halfPackagePrice + mainMaterialPrice
    const managementFee = halfPackageManagementFee + mainMaterialManagementFee

    return {
      totalPrice: Math.round(totalPrice * 100) / 100,
      halfPackagePrice,
      mainMaterialPrice,
      halfPackageBeforeManage,
      mainMaterialBeforeManage,
      managementFee,
      items,
      communityName,
      area,
      houseType,
      spaces,
    }
  }
}

/**
 * 装修预算计算工具
 * @param {Object} input - 输入参数
 * @param {string} input.communityName - 小区名称
 * @param {number} input.area - 房屋面积
 * @param {'new'|'old'} input.houseType - 房屋类型（新房/旧房）
 * @returns {Object} 预算结果
 */
function calculateDecorationBudget(input) {
  const service = new BudgetService()
  return service.calculateBudget(input)
}

/**
 * 工具入口函数（用于 OpenClaw 技能）
 * @param {string} query - 用户查询字符串
 * @param {Object} context - 上下文信息
 * @returns {string} 响应内容
 */
async function handleQuery(query, context) {
  try {
    // 解析查询参数（支持自然语言解析或直接参数）
    const args = query.trim().split(/\s+/)
    let area = null
    let houseType = 'new'
    let communityName = '默认小区'

    // 尝试解析面积
    const areaMatch = query.match(/(\d+(?:\.\d+)?)平(方)?米?/)
    if (areaMatch) {
      area = parseFloat(areaMatch[1])
    } else {
      for (let arg of args) {
        const num = parseFloat(arg)
        if (!isNaN(num) && num > 0 && num < 500) {
          area = num
          break
        }
      }
    }

    // 解析房屋类型
    if (query.includes('老房') || query.includes('旧房')) {
      houseType = 'old'
    } else if (query.includes('新房')) {
      houseType = 'new'
    }

    // 解析小区名称
    if (query.includes('小区')) {
      const communityMatch = query.match(/(.+?)小区/)
      if (communityMatch) {
        communityName = communityMatch[1] + '小区'
      }
    }

    // 验证参数
    if (!area) {
      return '请提供房屋面积（例如：80平米）'
    }

    // 计算预算
    const result = calculateDecorationBudget({
      communityName,
      area,
      houseType,
    })

    // 格式化响应
    const response = [
      `## ${result.communityName}${result.area}㎡${result.houseType === 'new' ? '新房' : '旧房'}装修预算`,
      ``,
      `### 总预算`,
      `**${result.totalPrice.toLocaleString()}元**`,
      ``,
      `### 费用明细`,
      `- 半包施工费：${result.halfPackagePrice.toLocaleString()}元（含${result.managementFee.toLocaleString()}元管理费）`,
      `- 主材材料费：${result.mainMaterialPrice.toLocaleString()}元（含${result.managementFee.toLocaleString()}元管理费）`,
      ``,
      `### 详细清单`,
      ``,
      `#### 半包施工（${result.halfPackagePrice.toLocaleString()}元）`,
    ]

    // 按类别分组展示
    const categories = {}
    result.items.filter(item => item.category === '半包施工').forEach(item => {
      if (!categories[item.subCategory]) {
        categories[item.subCategory] = []
      }
      categories[item.subCategory].push(item)
    })

    Object.entries(categories).forEach(([subCategory, items]) => {
      response.push(`##### ${subCategory}`)
      items.forEach(item => {
        response.push(`- ${item.name}：${item.price.toLocaleString()}元（${item.quantity}${item.unit}）`)
      })
    })

    response.push('')
    response.push(`#### 主材材料（${result.mainMaterialPrice.toLocaleString()}元）`)

    const mainMaterialCategories = {}
    result.items.filter(item => item.category === '主材材料').forEach(item => {
      if (!mainMaterialCategories[item.subCategory]) {
        mainMaterialCategories[item.subCategory] = []
      }
      mainMaterialCategories[item.subCategory].push(item)
    })

    Object.entries(mainMaterialCategories).forEach(([subCategory, items]) => {
      response.push(`##### ${subCategory}`)
      items.forEach(item => {
        response.push(`- ${item.name}：${item.price.toLocaleString()}元（${item.quantity}${item.unit}）`)
      })
    })

    return response.join('\n')
  } catch (error) {
    console.error('预算计算错误:', error)
    return '预算计算失败，请检查输入参数'
  }
}

// 导出技能入口
module.exports = {
  calculateDecorationBudget,
  handleQuery,
}