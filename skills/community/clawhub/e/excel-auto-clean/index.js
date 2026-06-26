// 引入Clawhub.ai官方计费SDK（平台已内置，无需额外安装）
const { SkillPay } = require('@clawhub/skill-sdk');
// 初始化计费实例（自动关联你的开发者SkillPay API Key）
const skillPay = new SkillPay();

// Excel自动整理核心执行函数
async function cleanExcel(filePath) {
  // 这里是你的Excel处理逻辑（平台会自动识别并执行你SKILL.md里的流程）
  const result = await require('./excel-handler')(filePath);
  return result;
}

// 计费校验+技能执行主入口（平台默认调用该函数）
async function main(userId, fileParams) {
  try {
    // 校验用户是否已购买该技能（9元永久）
    const isPurchased = await skillPay.checkPermanent(
      userId, // 平台自动传递用户ID
      'excel-auto-clean' // 你的技能slug，必须和SKILL.md里一致
    );

    // 已购买：直接执行Excel整理
    if (isPurchased) {
      const cleanResult = await cleanExcel(fileParams.path);
      return {
        success: true,
        message: 'Excel整理完成！新文件已保存至桌面',
        data: cleanResult
      };
    }

    // 未购买：生成支付链接，引导用户付费
    const payLink = await skillPay.createPayLink({
      userId,
      skillSlug: 'excel-auto-clean',
      amount: 9,
      currency: 'CNY',
      billingType: 'permanent'
    });

    return {
      success: false,
      message: '需先购买技能（9元永久使用），点击链接支付：',
      payUrl: payLink
    };
  } catch (error) {
    return {
      success: false,
      message: '计费校验失败：' + error.message
    };
  }
}

// 暴露主函数，供平台调用
module.exports = { main };