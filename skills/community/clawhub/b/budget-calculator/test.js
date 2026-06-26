const { calculateDecorationBudget, handleQuery } = require('./index')

// 测试基本功能
console.log('=== 装修预算计算技能测试 ===\n')

// 1. 测试计算函数
console.log('1. 测试计算函数')
const test1 = calculateDecorationBudget({
  communityName: '测试小区',
  area: 80,
  houseType: 'new'
})
console.log(`小区: ${test1.communityName}`)
console.log(`面积: ${test1.area}㎡`)
console.log(`类型: ${test1.houseType === 'new' ? '新房' : '旧房'}`)
console.log(`总预算: ${test1.totalPrice.toLocaleString()}元`)
console.log(`半包施工: ${test1.halfPackagePrice.toLocaleString()}元`)
console.log(`主材材料: ${test1.mainMaterialPrice.toLocaleString()}元`)
console.log(`管理费: ${test1.managementFee.toLocaleString()}元`)
console.log(`项目数量: ${test1.items.length}个`)

// 2. 测试查询处理
console.log('\n2. 测试查询处理')
const testQueries = [
  '80平装修预算',
  '100平米装修多少钱',
  '95平旧房装修预算',
  '万科城市之光85平新房装修预算',
  '我家80平新房装修大概多少钱'
]

testQueries.forEach(async (query, index) => {
  try {
    console.log(`\n${index + 1}. 查询: "${query}"`)
    const result = await handleQuery(query)
    console.log('响应:')
    console.log(result)
  } catch (error) {
    console.error('错误:', error.message)
  }
})

// 3. 测试不同面积
console.log('\n3. 测试不同面积')
const areas = [50, 75, 120]
areas.forEach(async (area, index) => {
  try {
    console.log(`\n${index + 1}. ${area}㎡新房预算`)
    const result = await handleQuery(`${area}平新房装修预算`)
    console.log('总预算:', result.match(/\*\*(\d+,\d+)元\*\*/)[1], '元')
  } catch (error) {
    console.error('错误:', error.message)
  }
})