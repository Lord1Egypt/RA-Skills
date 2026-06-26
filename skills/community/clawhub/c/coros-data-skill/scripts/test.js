import { CorosClient } from "./coros.js";

const client = new CorosClient(process.env.COROS_ACCOUNT, process.env.COROS_PASSWORD);
await client.login();

// 查询指定日期范围内的跑步活动（日期格式：YYYYMMDD）
const activities = await client.fetchActivity("20250101", "20251231");
activities.forEach(activity => {  
  console.log("date:",activity.date, "distance:",activity.distance); 
});
console.log(`一共跑了${activities.length}次`)