# DigenAI Discord 服务器 - 欢迎词 & 规则

## 📌 在 #welcome 频道发布：

---
👋 **Welcome to DigenAI!** 🎉

Free AI image & video generation — permanently no charge.

**🚀 Get started in 3 steps:**

**1️⃣ Get your free API Key**
→ Type `!key` in any channel to get it instantly

**2️⃣ Install the Skill**
```
clawhub install digen-ai-free
```

**3️⃣ Set your key**
```
export DIGEN_API_KEY="your_key_here"
```

**📖 Skill Page:** https://clawhub.ai/eeoeofl/digen-ai-free

---

**🤖 Bot Commands:**
| Command | Description |
|---------|------------|
| `!key` | Get your free API key |
| `!mykey` | View your current key |
| `!quota` | Check daily usage |
| `!help` | Show help |

---

**❓ Questions?**
Check #help channel or ask in this server!
---

## 📌 在 #rules 频道发布：

---
🛡️ **Community Rules**

1️⃣ **Be respectful** — Keep it civil, no harassment or hate speech

2️⃣ **No spam** — Don't flood channels with repeated messages

3️⃣ **Share keys privately** — Never post your API key in public channels. Use `!mykey` to check your own key

4️⃣ **English in #general** — Use English so everyone can follow along

5️⃣ **One account per person** — Multiple accounts to farm keys = ban

6️⃣ **Keep it legal** — No illegal content generation

---

⚠️ **Violations may result in key revocation or server ban.**

Questions? DM a moderator or ask in #help.
---

## 📌 在 #api-key 频道发布：

---
🔑 **API Key Channel**

Send `!key` here to receive your personal free API key.

**⚠️ Important:**
- Your key is personal — do NOT share it publicly
- Daily quota: 50 requests/day
- Quota resets daily at UTC 00:00

**📖 Usage:**
```bash
export DIGEN_API_KEY="ak_xxxxx_your_key"
clawhub install digen-ai-free
```

**🧪 Test your key:**
```python
from digen_ai_client import DigenAIClient
client = DigenAIClient(api_key=os.getenv("DIGEN_API_KEY"))
result = client.generate_image_sync(
    prompt="a beautiful sunset over the ocean",
    resolution="16:9"
)
```

Need help? → `!help` or ask in #help
---

## 📌 在 #help 频道发布：

---
❓ **Help Channel**

**How do I get started?**
1. Send `!key` anywhere to get your free API key
2. Run `clawhub install digen-ai-free`
3. Set: `export DIGEN_API_KEY="your_key"`
4. Use the Python client to generate images/videos!

**📖 Resources:**
- Skill page: https://clawhub.ai/eeoeofl/digen-ai-free


**💬 Still stuck?**
Ask your question here and someone will help!
---

## 📌 在 #showcase 频道发布：

---
🎨 **Showcase Channel**

Share your AI-generated images and videos here!

**Post format:**
- What did you create?
- What prompt did you use? (optional)
- Which model/duration?

**💡 Tips:**
- Image: try `flux2-klein`, `image_motion`, `zimage` models
- Video: try `wan` (default), `turbo`, `2.6` models
- Aspect ratios: 1:1, 16:9, 9:16

Have questions about prompts? → #help channel
---

## 📌 更新 Bot 的在线状态/游戏状态

在 Bot 设置中，设置：
- **Playing**: "!key to get free API · clawhub install digen-ai-free"
