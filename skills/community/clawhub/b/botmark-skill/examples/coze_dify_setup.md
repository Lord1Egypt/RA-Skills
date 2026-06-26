# Coze / Dify Setup

Both Coze and Dify support custom tool/plugin registration.

## Coze

1. Go to your bot's **Plugins** settings
2. Add a new **API Plugin**
3. Import the OpenAPI spec from:
   ```
   https://botmark.cc/api/v1/bot-benchmark/spec
   ```
   Or manually register tools from [`skill_openai.json`](../skill_openai.json)

4. In the plugin's **Authentication** settings:
   - Type: Bearer Token
   - Token: `bm_live_your_key_here`

5. Add the system prompt from [`system_prompt.md`](../system_prompt.md) to your bot's **Persona & Prompt** section

## Dify

1. Go to your app's **Tools** settings
2. Add a **Custom Tool**
3. Import tools from [`skill_generic.json`](../skill_generic.json)
4. Configure the tool's **Credentials**:
   - API Key: `bm_live_your_key_here`
   - Base URL: `https://botmark.cc`

5. Add the system prompt from [`system_prompt.md`](../system_prompt.md) to your app's system prompt

## Usage

Once configured, your bot's owner can say:
- "Run BotMark" / "benchmark" / "evaluate yourself" / "test yourself"
- The bot will use the registered tools to handle the evaluation
