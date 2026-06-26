module.exports = async function main({ inputs, env }) {
  const { ip_info, episode_count = 1, duration = 90 } = inputs;

  const API_KEY = env.API_KEY;
  const API_BASE = env.API_BASE;
  const MODEL_NAME = env.MODEL_NAME;

  const prompt = `
根据以下IP信息，生成${duration}秒抖音/番茄短剧剧本，共${episode_count}集。
要求：节奏快、冲突强、台词短。
输出严格JSON格式：
{
  "scenes": [{"scene":"","role":"","lines":"","action":"","duration":0}],
  "total_duration": ${duration}
}`;

  const res = await fetch(`${API_BASE}/chat/completions`, {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: MODEL_NAME,
      messages: [
        { role: "user", content: JSON.stringify(ip_info) },
        { role: "user", content: prompt }
      ]
    })
  });

  const data = await res.json();
  return JSON.parse(data.choices[0].message.content);
};
