// keys.mjs — the only place pe reads API keys from the environment. A key is read only for a name on
// this list: the built-in providers' variables, or a PE_KEY_* variable the user created for their own
// adapter. Config cannot point an adapter at any other variable (AWS_*, GITHUB_TOKEN, …).
export const BUILTIN_KEY_ENVS = ['TYPESAFE_API_KEY', 'CLASSIFIER_API_KEY', 'CLASSIFY_API_KEY'];
export const allowedKeyEnv = n => BUILTIN_KEY_ENVS.includes(n) || /^PE_KEY_[A-Z0-9_]+$/.test(n);
export function checkKeyEnv(names, who) {
  const bad = names.filter(n => !allowedKeyEnv(n));
  if (bad.length) throw new Error(`适配器 ${who} 的 keyEnv 不允许读取 ${bad.join(', ')}：自定义适配器的 key 必须放在 PE_KEY_* 变量里`);
}
export const readKey = names => names.filter(allowedKeyEnv).map(n => process.env[n]).find(Boolean);
