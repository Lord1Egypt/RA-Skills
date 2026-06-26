# Daily Tutor Skill

Daily Tutor is an OpenClaw skill that helps you set up an automated daily review and learning system. 
The skill automatically tracks the items you have learned and ensures they are never repeated.

## Data Setup (`data.json`)

To use this skill, simply create (or update) the `data.json` file inside the `data/` directory with the content you want to learn. The system supports **any data structure**, so you are not restricted to any specific format!

1. Open the `data/data.json` file.
2. Write your learning content in a JSON Array format. In each element, you can freely name the data fields. For example:

**Language Learning:**
```json
[
  {
    "id": 1,
    "word": "Hello",
    "meaning": "Xin chào",
    "example": "Hello, how are you?"
  }
]
```

The system will use your first field (key) to track your learning progress (or you can manually configure this key in `data/config.json`).
For more examples, please refer to the `references/EXAMPLES.md` file.

## Configuration (`config.json`)

Open the `data/config.json` file to customize:
- `num_items`: The number of words/items to learn per session (default: 10)
- `subject_name`: The display name of the subject when the AI chats with you (e.g., "English Vocabulary")
- `primary_key`: The target field name used as the ID to mark completion.

## Learning Progress Management

The system automatically creates a `data/learned_items.json` file to remember what you have learned.
If you want to **start learning from scratch**, simply delete the `data/learned_items.json` file.
The `learned_items.json` file is already added to `.gitignore` to prevent accidentally pushing your personal learning data to the cloud!

## Generating Quizzes with MCP `quizbuild`

If you want to test your memory after learning the daily items, you can leverage the **MCP `quizbuild`** extension. 

To enable this feature, you first need to add the following MCP configuration to your `~/.openclaw/openclaw.json` (or your OpenClaw settings under the `mcp` block):

```json
"mcp": {
  "servers": {
    "quizbuild": {
      "url": "https://api.quizbuild.com/mcp/quizbuild",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer <TOKEN_API_QUIZBUILD>"
      }
    }
  }
}
```

### How to get your Quizbuild API Token:
1. Sign up for an account on Quizbuild and verify your email (you can skip email verification if you sign in via Google).
2. Visit [https://quizbuild.com/customer/api-tokens](https://quizbuild.com/customer/api-tokens).
3. Click **Generate New Token** to create a token. The token will have a format like `qb_tok_xxxxxxxx`.
4. Replace `<TOKEN_API_QUIZBUILD>` in the configuration above with your newly generated token.

Once `quizbuild` is installed and configured, simply ask your agent:
> *"Let's review my daily items and give me a practice quiz."*

The Agent will fetch your daily items and automatically use the `quizbuild__auto_create_exam` tool to generate a multiple-choice practice exam based on your vocab or subject data!
