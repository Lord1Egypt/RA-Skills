export default function skill(context) {
  const userInput = (context.input || "").trim().toLowerCase();

  if (!userInput) {
    return {
      message: "Welcome to Aether Tarot. Ask for a 3‑card reading or describe your question.",
      context: {}
    };
  }

  return {
    message: "I’m ready. Provide your question, and I’ll share a gentle 3‑card tarot reflection.",
    context: {}
  };
}
