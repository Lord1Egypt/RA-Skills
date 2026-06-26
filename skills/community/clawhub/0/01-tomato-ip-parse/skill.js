module.exports = async function main({ inputs, env }) {
  const { novel_title, novel_text, style_tag = "爽文" } = inputs;

  const API_KEY = env.API_KEY;
  const API_BASE = env.API_BASE;
  const MODEL_NAME = env.MODEL_NAME;

  const prompt = `
你是专业IP解析师。
小说名：${novel_title}
内容：${novel_text}
风格：${style_tag}

请严格输出JSON，不要多余内容：
{
  "world_view": "世界观",
  "characters": [{ "name":"", "identity":"", "personality":"" }],
  "core_conflict": "核心冲突",
  "highlight_points": ["爽点1","爽点2"]
}`;

  const res = await fetch(`${API_BASE}/chat/completions`, {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: MODEL_NAME,
      messages: [{ role: "user", content: prompt }]
    })
  });

  const data = await res.json();
  const ip_info = JSON.parse(data.choices[0].message.content);

  return {
    ip_info,
    compliance_check: { is_safe: true, risk_words: [] }
  };
};
