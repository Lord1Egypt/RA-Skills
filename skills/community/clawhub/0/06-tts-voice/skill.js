module.exports = async function main({ inputs, env }) {
  const { dialogue } = inputs;

  const API_KEY = env.API_KEY;
  const API_BASE = env.API_BASE;
  const MODEL_NAME = env.MODEL_NAME;

  const res = await fetch(`${API_BASE}/tts`, {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: MODEL_NAME,
      text: dialogue
    })
  });

  const data = await res.json();
  return { audio_url: data.audio_url };
};
