// src/llm/types.ts

export interface LLMConfig {
  apiKey?: string;
  model?: string;
  maxTokens?: number;
}

export interface LLMProvider {
  /**
   * LLM 호출 메서드 (단일 응답)
   * @param systemPrompt 역할 및 지시사항
   * @param userMessage 사용자 입력 또는 컨텍스트
   * @returns LLM 응답 텍스트
   */
  call(systemPrompt: string, userMessage: string): Promise<string>;
}
