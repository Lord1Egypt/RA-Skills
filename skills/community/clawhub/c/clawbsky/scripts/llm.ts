/**
 * LLM Client Module
 * Ollama integration for local AI (qwen3.5:4b)
 */

export interface OllamaResponse {
  model: string;
  created_at: string;
  message: {
    role: string;
    content: string;
  };
  done: boolean;
}

export interface OllamaClient {
  chat(options: {
    model: string;
    messages: { role: string; content: string }[];
    stream?: boolean;
    format?: string;
  }): Promise<OllamaResponse>;
}

export const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || process.env.LLM_BASE_URL || 'http://localhost:11434';
export const DEFAULT_MODEL = process.env.OLLAMA_MODEL || process.env.LLM_MODEL || 'qwen3.5:4b';

let ollamaClient: OllamaClient | null = null;

/**
 * Get Ollama client instance
 */
export function getOllamaClient(): OllamaClient {
  if (!ollamaClient) {
    ollamaClient = createOllamaClient();
  }
  return ollamaClient;
}

/**
 * Create Ollama client
 */
function createOllamaClient(): OllamaClient {
  return {
    async chat(options: {
      model: string;
      messages: { role: string; content: string }[];
      stream?: boolean;
      format?: string;
    }): Promise<OllamaResponse> {
      const model = options.model || DEFAULT_MODEL;
      
      const response = await fetch(`${OLLAMA_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model,
          messages: options.messages,
          stream: options.stream || false,
          ...(options.format ? { format: options.format } : {})
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`Ollama error: ${response.status} - ${error}`);
      }

      return response.json();
    }
  };
}

/**
 * Check if Ollama is available
 */
export async function checkOllama(): Promise<boolean> {
  try {
    const response = await fetch(`${OLLAMA_BASE_URL}/api/tags`);
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * List available models
 */
export async function listModels(): Promise<string[]> {
  try {
    const response = await fetch(`${OLLAMA_BASE_URL}/api/tags`);
    const data = await response.json();
    return data.models?.map((m: any) => m.name) || [];
  } catch {
    return [];
  }
}

/**
 * Test LLM connection
 */
export async function testLLM(prompt: string = "Say 'Hello from Clawbsky!'"): Promise<string> {
  const client = getOllamaClient();
  
  const response = await client.chat({
    model: DEFAULT_MODEL,
    messages: [{ role: 'user', content: prompt }]
  });

  return response.message.content;
}