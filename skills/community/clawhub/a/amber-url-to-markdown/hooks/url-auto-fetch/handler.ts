import { exec } from "child_process";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

const handler = async (event: any) => {
  // 只处理 message:received 事件
  if (event.type !== "message" || event.action !== "received") {
    return;
  }

  const content = event.context?.content || "";
  const from = event.context?.from || "";

  // 如果消息来自机器人自己，跳过
  if (from === "bot" || from === "self") {
    return;
  }

  // URL 匹配正则
  const urlPattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/gi;
  
  // 意图关键词
  const intentKeywords = [
    "解析", "转换", "转成", "转为", "生成", "抓取", "爬取", "下载",
    "markdown", "md", "文章", "内容"
  ];

  // 检测是否有意图关键词
  const hasIntentKeyword = intentKeywords.some(keyword => 
    content.toLowerCase().includes(keyword.toLowerCase())
  );

  // 检测 URL
  const urls = content.match(urlPattern);
  
  if (!urls || urls.length === 0) {
    return;
  }

  // 判断是否应该自动触发
  const isPureUrl = content.trim().replace(urlPattern, "").trim().length === 0;
  const shouldTrigger = isPureUrl || hasIntentKeyword;

  if (!shouldTrigger) {
    return;
  }

  // 找到第一个符合条件的 URL（优先微信公众号）
  let targetUrl = urls[0];
  const wechatUrl = urls.find(url => url.includes("mp.weixin.qq.com"));
  if (wechatUrl) {
    targetUrl = wechatUrl;
  }

  console.log(`[url-auto-fetch] 检测到 URL: ${targetUrl}`);
  console.log(`[url-auto-fetch] 触发条件：${isPureUrl ? "纯 URL" : "URL + 意图关键词"}`);

  // 查找脚本路径 - 使用固定路径（更可靠）
  const scriptPath = "/root/openclaw/skills/amber-url-to-markdown/scripts/amber_url_to_markdown.py";
  
  console.log(`[url-auto-fetch] 脚本路径：${scriptPath}`);
  
  // 检查脚本是否存在
  if (!fs.existsSync(scriptPath)) {
    console.error(`[url-auto-fetch] 脚本不存在：${scriptPath}`);
    event.messages.push("⚠️ URL Auto Fetch: 未找到脚本文件，请检查技能安装路径");
    return;
  }
  
  console.log(`[url-auto-fetch] 脚本存在，准备执行`);

  console.log(`[url-auto-fetch] 脚本存在，准备执行`);

  // 发送提示消息
  event.messages.push(`🔗 检测到链接，正在抓取内容...\n\n${targetUrl}`);

  // 执行脚本（异步，不阻塞）
  const escapedUrl = targetUrl.replace(/"/g, '\\"');
  const command = `python3 "${scriptPath}" "${escapedUrl}"`;

  console.log(`[url-auto-fetch] 执行命令：${command}`);

  exec(command, { 
    cwd: "/root/openclaw/skills/amber-url-to-markdown",
    timeout: 120000 // 2 分钟超时
  }, (error, stdout, stderr) => {
    if (error) {
      console.error(`[url-auto-fetch] 执行失败：${error.message}`);
      console.error(`[url-auto-fetch] stderr: ${stderr}`);
      return;
    }
    
    console.log(`[url-auto-fetch] 执行完成`);
    console.log(`[url-auto-fetch] stdout: ${stdout}`);
    
    // 解析输出，提取文件路径
    const fileMatch = stdout.match(/📄 文件：(.+)/);
    const imageMatch = stdout.match(/🖼️ 图片：(\d+) 张/);
    
    if (fileMatch) {
      const filePath = fileMatch[1].trim();
      const imageCount = imageMatch ? imageMatch[1] : "0";
      
      console.log(`[url-auto-fetch] 文件已保存：${filePath}`);
      console.log(`[url-auto-fetch] 图片数量：${imageCount}`);
    }
  });
};

export default handler;
