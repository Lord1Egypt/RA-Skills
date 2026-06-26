module.exports = async function main({ inputs, env }) {
  const { prompt, negative_prompt = "" } = inputs;

  const API_KEY = env.API_KEY;
  const API_BASE = env.API_BASE;
  const MODEL_NAME = env.MODEL_NAME;

  const res = await fetch(`${API_BASE}/txt2img`, {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: MODEL_NAME,
      prompt: prompt,
      negative_prompt: negative_prompt,
      ratio: "9:16"
    })
  });

  const data = await res.json();
  return { image_url: data.image_url };
};
