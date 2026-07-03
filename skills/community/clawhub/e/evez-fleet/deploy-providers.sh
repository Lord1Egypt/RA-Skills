#!/bin/bash
# Fleet Free Models Deployment — wires free providers into all OpenClaw nodes
# Usage: ./fleet-free-models.sh <api_key_for_provider>
# 
# Free Providers & How to Get Keys:
# - Google Gemini:  aistudio.google.com → Get API Key (FREE, 1M context)
# - Groq:          console.groq.com → API Keys (FREE, fast inference)
# - Cerebras:      cloud.cerebras.ai → API Keys (FREE, fastest inference)
# - OpenRouter:    openrouter.ai → Keys (free models available)
# - Together:      api.together.ai → Settings ($5 free credit)
# - Chutes:        chutes.ai → API Key (FREE community models)
# - HuggingFace:   huggingface.co → Settings → Access Tokens (FREE serverless)

set -euo pipefail

PROVIDER="${1:-}"
KEY="${2:-}"

if [ -z "$PROVIDER" ] || [ -z "$KEY" ]; then
    echo "Usage: $0 <provider> <api_key>"
    echo "Providers: google groq cerebras openrouter together chutes huggingface"
    exit 1
fi

case "$PROVIDER" in
    google|gemini)
        BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai"
        ENV_VAR="GOOGLE_API_KEY"
        MODELS='[{"id":"gemini-2.5-flash","name":"Gemini 2.5 Flash","contextWindow":1048576,"maxTokens":65536,"reasoning":true,"cost":{"input":0,"output":0}},{"id":"gemini-2.0-flash","name":"Gemini 2.0 Flash","contextWindow":1048576,"maxTokens":8192,"cost":{"input":0,"output":0}}]'
        ;;
    groq)
        BASE_URL="https://api.groq.com/openai/v1"
        ENV_VAR="GROQ_API_KEY"
        MODELS='[{"id":"llama-3.3-70b-versatile","name":"Llama 3.3 70B Groq","contextWindow":131072,"maxTokens":32768,"cost":{"input":0.59,"output":0.79}},{"id":"llama-3.1-8b-instant","name":"Llama 3.1 8B Instant","contextWindow":131072,"maxTokens":8192,"cost":{"input":0,"output":0}}]'
        ;;
    cerebras)
        BASE_URL="https://api.cerebras.ai/v1"
        ENV_VAR="CEREBRAS_API_KEY"
        MODELS='[{"id":"llama-3.3-70b","name":"Llama 3.3 70B Cerebras","contextWindow":131072,"maxTokens":8192,"cost":{"input":0,"output":0}}]'
        ;;
    openrouter)
        BASE_URL="https://openrouter.ai/api/v1"
        ENV_VAR="OPENROUTER_API_KEY"
        MODELS='[{"id":"google/gemini-2.5-flash-preview","name":"Gemini 2.5 Flash OR","contextWindow":1048576,"maxTokens":65536,"reasoning":true,"cost":{"input":0,"output":0}}]'
        ;;
    together)
        BASE_URL="https://api.together.xyz/v1"
        ENV_VAR="TOGETHER_API_KEY"
        MODELS='[{"id":"meta-llama/Llama-3.3-70B-Instruct-Turbo","name":"Llama 3.3 70B Turbo","contextWindow":131072,"maxTokens":8192,"cost":{"input":0.88,"output":0.88}}]'
        ;;
    chutes)
        BASE_URL="https://llm.chutes.ai/v1"
        ENV_VAR="CHUTES_API_KEY"
        MODELS='[{"id":"deepseek-ai/DeepSeek-V3-0324","name":"DeepSeek V3 Chutes","contextWindow":131072,"maxTokens":8192,"cost":{"input":0,"output":0}}]'
        ;;
    huggingface)
        BASE_URL="https://api-inference.huggingface.co/models"
        ENV_VAR="HF_TOKEN"
        MODELS='[{"id":"meta-llama/Llama-3.3-70B-Instruct","name":"Llama 3.3 70B HF","contextWindow":131072,"maxTokens":8192,"cost":{"input":0,"output":0}}]'
        ;;
    *)
        echo "Unknown provider: $PROVIDER"
        exit 1
        ;;
esac

echo "Configuring $PROVIDER on local OpenClaw..."
openclaw config set "models.providers.$PROVIDER.baseUrl" "$BASE_URL"
openclaw config set "models.providers.$PROVIDER.auth" "api-key"
openclaw config set "models.providers.$PROVIDER.api" "openai-completions"
openclaw config set "models.providers.$PROVIDER.apiKey" "$KEY"

echo "Done! Restart the gateway to activate: openclaw gateway restart"
echo "Models: $MODELS"
