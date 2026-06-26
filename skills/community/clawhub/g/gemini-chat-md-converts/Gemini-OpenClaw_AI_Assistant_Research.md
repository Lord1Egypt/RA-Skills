# OpenClaw AI Assistant Research

**Exported:** 2/13/2026 16:21:05  
**Link:** [https://gemini.google.com/u/1/app/bba697fe34421f27?pageId=none](https://gemini.google.com/u/1/app/bba697fe34421f27?pageId=none)

## Prompt:
help me find the open claw github repo so i can research it and see if it can help me.

## Response:
###### Gemini said

Found it! The project you're looking for has actually gone through a few name changes recently due to trademark reasons. It started as **Clawdbot**, briefly became **Moltbot**, and is now officially 
[OpenClaw](https://github.com/openclaw/openclaw)
.

### 🦞 
[OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)

It’s a viral open-source personal AI assistant created by Peter Steinberger (founder of PSPDFKit). It’s designed to run locally on your hardware rather than the cloud, giving it deep access to your system to perform "agentic" tasks.

**Why it might help you (based on your goals):**

*   **Recursive Learning & Automation:** You mentioned wanting self-improving bots. OpenClaw is built for "agentic" workflows—it doesn't just chat; it can read/write files, run shell commands, and drive a web browser.
*   **Cross-Platform Integration:** It connects to WhatsApp, Telegram, Discord, and Slack, which fits your interest in managing bots via hosted pages or messaging interfaces.
*   **Skill Extensibility:** There is a growing ecosystem of 
    [OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills)
     that allow it to interact with external services.
*   **Performance:** Since you’re after "speed demons" (Rust/Go/TS), you'll appreciate that this is a nimble, locally-run gateway architecture.

**A Quick "Spicy" Warning:** The documentation explicitly warns that giving an AI agent shell access to your machine is high-risk. Since it can execute commands, a prompt injection could potentially lead to it leaking files or running malicious code. If you’re building trading bots with it, definitely run it in a containerized or non-privileged environment as per your 
[Docker/Nix preferences](https://github.com/openclaw/openclaw/blob/main/docs/index.md)
.

Do you want me to dig into the 
[Skills registry](https://github.com/BankrBot/openclaw-skills)
 to see if there are already some crypto/trading modules you can fork?



---
Powered by [Gemini Exporter](https://www.ai-chat-exporter.com)