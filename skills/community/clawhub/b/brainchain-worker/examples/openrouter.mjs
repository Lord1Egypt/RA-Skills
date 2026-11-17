// Does a BrainChain task with any model on OpenRouter: reads the prompt on
// stdin, prints the model's answer on stdout.
//   OPENROUTER_API_KEY=... OPENROUTER_MODEL=moonshotai/kimi-k3.1-pro \
//     brainchain-worker run --exec "node examples/openrouter.mjs"
let prompt = "";
for await (const chunk of process.stdin) prompt += chunk;

const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: { authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`, "content-type": "application/json" },
  body: JSON.stringify({
    model: process.env.OPENROUTER_MODEL ?? "moonshotai/kimi-k3.1-pro",
    messages: [{ role: "user", content: prompt }],
    max_tokens: 4000,
  }),
  signal: AbortSignal.timeout(300_000),
});
if (!response.ok) {
  console.error(`OpenRouter answered ${response.status}: ${(await response.text()).slice(0, 300)}`);
  process.exit(1);
}
const answer = (await response.json()).choices?.[0]?.message?.content;
if (!answer) {
  console.error("OpenRouter returned no answer");
  process.exit(1);
}
process.stdout.write(answer);
