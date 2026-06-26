export default async function main(input) {
  // input 通常是结构化数据（由 agent 传入）
  if (!input || !input.text) {
    return "No input text provided.";
  }

  return input.text;
}
