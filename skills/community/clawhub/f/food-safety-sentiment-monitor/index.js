/**
 * Food Safety Sentiment Monitor | 食品安全舆情监控
 * Author: Kevin(凯文老师) | WeChat: ai94287
 */
const { chromium } = require('playwright');
// const { OpenClaw } = require('openclaw-sdk');

// 简化版配置（测试用）
const config = {
  keywords: process.argv[2] ? process.argv[2].split(',') : ["西贝", "食品安全"],
  platforms: {
    weibo: "https://s.weibo.com/weibo?q={{KEYWORDS}}"
  },
  riskLevels: {
    critical: { mentionCount: 100000, negativeRatio: 0.8 }
  },
  minimax: {
    apiKey: "", // 测试时先留空，后面教你填
    groupId: "",
    model: "minimax-abab5.5-chat",
    maxTokens: 1000,
    temperature: 0.3
  }
};

// 简化版抓取函数（只抓微博，测试更快）
async function crawlFoodSafetyEvents() {
  console.log("[测试] 开始抓取微博舆情...");
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const keywordStr = encodeURIComponent(config.keywords.join(' '));
  const url = config.platforms.weibo.replace("{{KEYWORDS}}", keywordStr);
  
  try {
    await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
    const events = await page.$$eval('.card-wrap', nodes => 
      nodes.slice(0, 5).map(n => ({ // 只抓前5条，测试更快
        platform: "微博",
        content: n.querySelector('.txt')?.innerText || "",
        author: n.querySelector('.name')?.innerText || "",
        interactCount: 1000 // 模拟数据，测试风险判断
      }))
    );
    await browser.close();
    console.log(`[测试] 抓取完成，共 ${events.length} 条数据`);
    return events;
  } catch (err) {
    await browser.close();
    console.log("[测试] 抓取模拟数据（避免网络问题）");
    return [{ // 模拟数据，确保测试能跑通
      platform: "微博",
      content: "罗永浩曝光西贝食材过期",
      author: "罗永浩",
      interactCount: 100000
    }];
  }
}

// 简化版分析函数
async function analyzeFoodSafetyRisk(events) {
  console.log("[测试] 开始风险分析...");
  // 测试时如果没填Minimax API，直接返回模拟结果
  if (!config.minimax.apiKey) {
    console.log("[测试] 使用模拟分析结果（未配置Minimax）");
    return {
      eventSummary: "罗永浩曝光西贝北京门店食材过期，转发量50万+",
      riskLevel: "critical",
      negativeRatio: 0.85,
      coreDemands: ["道歉", "整改", "补偿"]
    };
  }
  
  // 配置了API则调用真实分析（后面教你配置）
  const client = new OpenClaw({
    provider: 'minimax',
    apiKey: config.minimax.apiKey,
    groupId: config.minimax.groupId
  });
  const prompt = `分析舆情：${JSON.stringify(events)}，返回JSON：{"eventSummary":"","riskLevel":"critical","negativeRatio":0.85,"coreDemands":[""]}`;
  
  try {
    const res = await client.chat.completions.create({
      model: config.minimax.model,
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    return JSON.parse(res.choices[0].message.content);
  } catch (err) {
    console.log("[测试] API调用失败，使用模拟结果");
    return { eventSummary: "测试结果", riskLevel: "critical" };
  }
}

// 简化版响应生成
async function generateResponsePlan(risk) {
  console.log("[测试] 生成公关响应方案...");
  return `【西贝紧急声明】
  针对罗永浩曝光的食材过期问题，我们深表歉意！
  1. 涉事门店即刻停业整改
  2. 全国门店自查
  3. 联系消费者补偿
  ——Kevin(凯文老师) 舆情监控系统`;
}

// 测试主函数
async function test() {
  console.log("===== Kevin(凯文老师) 食品安全舆情监控 测试开始 =====");
  try {
    // 1. 抓取
    const events = await crawlFoodSafetyEvents();
    // 2. 分析
    const risk = await analyzeFoodSafetyRisk(events);
    console.log("[测试] 风险分析结果：", risk.eventSummary);
    // 3. 生成响应
    if (risk.riskLevel === "critical") {
      const plan = await generateResponsePlan(risk);
      console.log("[测试] 公关响应方案：\n", plan);
    }
    console.log("===== 测试完成（无报错即成功）=====");
  } catch (err) {
    console.error("===== 测试失败 =====", err.message);
  }
}

// 执行测试
test();