module.exports = async function main({ inputs, env }) {
  const { image_url } = inputs;

  const API_KEY = env.API_KEY;
  const API_BASE = env.API_BASE;
  const MODEL_NAME = env.MODEL_NAME;

  const res = await fetch(`${API_BASE}/img2video`, {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: MODEL_NAME,
      image_url: image_url
    })
  });

  const data = await res.json();
  return { video_url: data.video_url };
};
