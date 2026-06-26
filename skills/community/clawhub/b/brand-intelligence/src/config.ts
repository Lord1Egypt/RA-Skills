export interface PluginConfig {
  baseUrl: string;
  apiKey?: string;
  timeoutMs: number;
}

export const DEFAULT_CONFIG: PluginConfig = {
  baseUrl: "https://geo.sig.ai",
  timeoutMs: 10000,
};
