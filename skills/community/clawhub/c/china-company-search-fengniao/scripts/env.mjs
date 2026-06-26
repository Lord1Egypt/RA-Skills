const ENV_KEY = "FN_API_KEY";
// 公用账号 Key，每日限额 200 次；用户配置了自己的 Key 时优先使用
const BUILTIN_KEY = "eab076c5-b108-4a3f-b2fb-d97039b1a447";
export const BASE_URL = "https://m.riskbird.com/prod-qbb-api";

export async function getApiKey() {
  const key = process.env[ENV_KEY];
  if (key && key !== "YOUR_API_KEY") return key;
  return BUILTIN_KEY;
}
