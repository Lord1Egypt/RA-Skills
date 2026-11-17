import type { Provider } from "./types";
import { deepseekProvider } from "./providers/deepseek";
import { deepinfraProvider } from "./providers/deepinfra";
import { codexProvider } from "./providers/codex";
import { grokProvider } from "./providers/grok";
import { mimoProvider } from "./providers/mimo";
import { apikeyfunProvider, codexbarProvider } from "./providers/codexbar";

/** All 10 providers, in stable display order. */
export const registry: Provider[] = [
  deepseekProvider,
  deepinfraProvider,
  codexProvider,
  grokProvider,
  mimoProvider,
  codexbarProvider("claude", "Claude (Anthropic)"),
  codexbarProvider("gemini", "Gemini (Google)"),
  codexbarProvider("kimi", "Kimi (Moonshot)"),
  codexbarProvider("openrouter", "OpenRouter"),
  apikeyfunProvider,
];

export function findProvider(id: string): Provider | undefined {
  return registry.find((p) => p.id === id);
}
