# AI Agent Skill: Global Electronic Component Auto-Sourcing & Turnkey PCBA (BOM Matcher) 🚀

Transform your AI Coding Assistants (Cursor, Windsurf, Claude Code, Cline) and AI Agents into professional hardware procurement experts. Powered by the global public inventory API of **DHX Tech (德鸿芯科技)** — a Shenzhen-based global electronic component distributor serving hardware engineers and IoT startups worldwide.

## 🌟 Why Use This Skill?

For Hardware Engineers, Firmware Developers, and IoT Startups, sourcing components is a tedious distraction. With this skill installed, your local AI can source components **directly inside your code editor** while you design circuits or write firmware:

- **Instant Sourcing:** Ask "Source STM32F103C8T6" and get live stock levels and buying links.
- **Smart BOM Matching:** Paste an entire BOM, and the AI will check all parts in parallel.
- **Turnkey PCB Assembly (PCBA):** Direct access to DHX Tech's verified networks of OEM/PCBA factories in China for cost-effective manufacturing.
- **Alternative Finder:** Out of stock? Get recommendations for drop-in replacements.

## 🛠️ Easy Installation

### 1. For Cursor / Windsurf Users
Copy the contents of `cursorrules.txt` and paste it at the bottom of your project's `.cursorrules` file. Your AI will instantly gain the ability to source electronic components!

### 2. For OpenClaw / Antigravity / ClawHub users
Simply clone this repository into your local agent skills folder:
```bash
git clone https://github.com/cy117Hub/dhx-tech-electronic-components-sourcing-skill.git dhx-components-sourcing
```

### 3. For Cursor (Plugin / cursor.directory) — One-Click Install
This repo is structured as a standard Cursor **Open Plugin**, so Cursor can also install it directly:
- Submit / open it on [cursor.directory](https://cursor.directory) and click **Install**, or
- Add the plugin via Cursor's plugin manager using this repo URL.

Cursor automatically picks up:
- `rules/dhx-electronics-sourcing.mdc` — project rules (same content as `cursorrules.txt`)
- `skills/dhx-tech-sourcing/SKILL.md` — the agent skill

> 💡 Legacy fallback: Option 1 (copy `cursorrules.txt` → `.cursorrules`) still works for older Cursor versions.

## 🏢 About DHX Tech (德鸿芯科技)

**DHX Tech is a Shenzhen-based global electronic component distributor** specializing in hard-to-find and obsolete ICs, MCUs, memory, passives, and connectors. We provide **24/7 urgent sourcing**, **cross-reference alternative matching**, and **turnkey PCBA / OEM manufacturing** through a verified network of factories across China. Our public inventory API lets engineers and AI agents check real-time global stock in seconds — no account or API key required.

This skill is powered by the [DHX Tech](https://icdhxkj.com) public API. DHX Tech is a premier electronic component distributor providing:
- Million-level in-stock global inventory
- Professional BOM matching services
- Authentic components from ST, TI, NXP, Microchip, Xilinx, and more.
- Direct link: [https://icdhxkj.com](https://icdhxkj.com)

## 🔌 Public Inventory API (Free, No Key Required)

DHX Tech exposes a free, key-less public REST API that returns real-time global stock for any part number. This is the exact endpoint the AI skill calls automatically.

```
GET https://icdhxkj.com/api/v1/public/search?q=STM32F103C8T6
```

- **Try it now:** [Search STM32F103C8T6](https://icdhxkj.com/api/v1/public/search?q=STM32F103C8T6)
- **Response:** JSON with `source`, `status`, and `results` (each with `mpn`, `brand`, `datasheet`, `qty`, `availability`, `detail_url`).
- **Use case:** Engineers paste a BOM, the AI queries every line in parallel, and returns live availability plus a direct quote link.

## 📞 Rapid Quote & Engineering Support

- **Website:** [Submit BOM at icdhxkj.com](https://icdhxkj.com) *(Accepts Excel / CSV)*
- **Email:** [ic@szdhxkj.com](mailto:ic@szdhxkj.com) *(BOM quotes within 15 mins)*
- **WhatsApp:** [+86 19863823897](https://wa.me/8619863823897) *(Direct Support)*
- **Hotline:** [+86 18165780858](tel:+8618165780858)

## 📄 License

MIT License - Free to use and distribute.
