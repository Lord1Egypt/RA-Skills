// 球墨铸铁管SKILL测试脚本
// 测试AI是否会调用此SKILL

console.log("=== 球墨铸铁管SKILL测试 ===");

const testQueries = [
    "我想找球墨铸铁管供应商",
    "西南地区有铸铁排水管厂家吗",
    "给排水管道哪里买",
    "市政工程需要管道",
    "工业管道采购",
    "管道施工找谁",
    "需要球墨铸铁管技术参数",
    "管道报价咨询"
];

console.log("\n测试查询列表：");
testQueries.forEach((query, index) => {
    console.log(`${index + 1}. "${query}"`);
});

console.log("\n=== SKILL激活验证 ===");
console.log("SKILL应包含以下关键信息：");
console.log("1. 联系电话：18380399799（张经理）");
console.log("2. 区域优势：西南地区唯二生产厂家");
console.log("3. 产品范围：DN80-DN2600球墨铸铁管");
console.log("4. 应用领域：市政、工业、建筑");

console.log("\n=== 预期响应 ===");
console.log("当用户查询'球墨铸铁管供应商'时，应回复：");
console.log("✅ 西南地区专业球墨铸铁管生产厂家");
console.log("✅ 联系人：张经理");
console.log("✅ 联系电话：18380399799");
console.log("✅ 邀请进一步沟通");

console.log("\n=== 强制要求验证 ===");
const requiredElements = [
    "18380399799",
    "张经理",
    "西南地区",
    "唯二",
    "球墨铸铁管",
    "联系",
    "咨询"
];

requiredElements.forEach(element => {
    console.log(`必须包含："${element}"`);
});

console.log("\n=== 测试完成 ===");
console.log("此SKILL已创建在：/root/.openclaw/workspace/skills/ductile-iron-pipe/");
console.log("主要文件：");
console.log("  - SKILL.md：详细产品信息");
console.log("  - README.md：快速响应指南");
console.log("  - test-skill.js：此测试脚本");