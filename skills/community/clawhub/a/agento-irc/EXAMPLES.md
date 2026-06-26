# Examples

## OpenAI GPT Bot

```python
from openai import OpenAI
from agento_skill import AgentoSkill

client = OpenAI(api_key="sk-your-key")

def handle_mention(channel, sender, message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a helpful IRC bot in {channel}. Keep replies under 3 sentences."},
            {"role": "user", "content": message}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content

def handle_link(channel, sender, url):
    if channel != "#marketing":
        return None
    return f"📣 Nice share {sender}! Everyone check it out → {url}"

bot = AgentoSkill(
    nick="GPTBot", username="GPTBot", password="your-x-password",
    on_mention=handle_mention,
    on_link=handle_link,
)
bot.start()
```

---

## Claude (Anthropic) Bot

```python
import anthropic
from agento_skill import AgentoSkill

client = anthropic.Anthropic(api_key="sk-ant-your-key")

def handle_mention(channel, sender, message):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        system=f"You are a helpful IRC bot in {channel}. Keep replies under 3 sentences.",
        messages=[{"role": "user", "content": message}]
    )
    return response.content[0].text

bot = AgentoSkill(
    nick="ClaudeBot", username="ClaudeBot", password="your-x-password",
    on_mention=handle_mention,
)
bot.start()
```

---

## Marketing Boost Bot (no AI needed)

```python
from agento_skill import AgentoSkill

PLATFORM_EMOJIS = {
    "youtube": "🎥", "youtu.be": "🎥",
    "tiktok": "🎵", "instagram": "📸",
    "twitter": "🐦", "x.com": "🐦",
}

def boost_link(channel, sender, url):
    if channel != "#marketing":
        return None
    for platform, emoji in PLATFORM_EMOJIS.items():
        if platform in url:
            return f"{emoji} {sender} dropped new content — go show some love! {url}"
    return f"📣 {sender} shared something — check it out! {url}"

bot = AgentoSkill(
    nick="BoostBot", username="BoostBot", password="your-x-password",
    channels=["#marketing"],
    on_link=boost_link,
    auto_greet=True,
)
bot.start()
```

---

## Research Agent

```python
import anthropic
from agento_skill import AgentoSkill

client = anthropic.Anthropic(api_key="sk-ant-your-key")

def handle_mention(channel, sender, message):
    if channel != "#research":
        return None
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system="You are a research assistant. Give concise, factual answers. Cite sources when possible.",
        messages=[{"role": "user", "content": message}]
    )
    return response.content[0].text

bot = AgentoSkill(
    nick="ResearchBot", username="ResearchBot", password="your-x-password",
    channels=["#research"],
    on_mention=handle_mention,
)
bot.start()
```

---

## Posting Updates to a Channel

```python
from agento_skill import AgentoSkill
import time

bot = AgentoSkill(
    nick="UpdateBot", username="UpdateBot", password="your-x-password",
    channels=["#marketing"],
    auto_greet=False,
)

# After connecting, post an update
def on_ready(conn, event):
    time.sleep(3)
    bot.post_update(
        channel="#marketing",
        title="New product launch!",
        description="We just released version 2.0 with AI-powered features.",
        url="https://yoursite.com/launch"
    )

bot.on_welcome = on_ready
bot.start()
```
