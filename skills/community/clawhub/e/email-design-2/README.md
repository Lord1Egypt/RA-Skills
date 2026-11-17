# email-design

Email design skill for Claude Code. Stops AI-drafted emails from looking like AI drafted them.

The default failure mode of AI-composed email is plain: too much whitespace, no images, generic palettes, identical-looking layouts, lifeless footers. This skill replaces those defaults with anti-slop principles, six committed archetypes, brand-aware context, and a structured brief that any sending tool can execute.

Works with any ESP — built first for [Nitrosend](https://nitrosend.com), works equally well with Klaviyo, Mailchimp, ActiveCampaign, Resend, or anything else exposing an MCP.

## Install

### Claude Code

```bash
npx skills add CosmoBlk/email-design
```

Or manually:

```bash
git clone https://github.com/CosmoBlk/email-design ~/.claude/skills/email-design
```

### Anywhere else (Cursor, Cline, raw Claude API)

Drop [SKILL.md](./SKILL.md) into your prompt as a system message or skill file. The skill is self-contained — no other skills required.

## What it does

When you ask Claude to design or compose an email, the skill runs five steps:

1. **Context check (silent).** Pulls brand state from the connected ESP (logo, colours, voice, prior templates) and any project brand file. No questions yet.
2. **Up to three questions.** Bundled into one message. Only asked when the highest-leverage gaps are missing — purpose, tone, brand colour.
3. **Pick an archetype, write a structured brief.** Six archetypes: editorial, bold mono, minimal lux, founder letter, punk/character, lookbook. Commit before composing.
4. **Resolve image slots.** Brand assets first, then brand site (`og:image`, hero, /press, /about), then social profiles, then prompt the user. Never AI-generated stock.
5. **Hand the brief to the sending tool.** Translates archetype + brief into the section format the tool expects, with explicit padding overrides to defeat the platform's default whitespace.

## Why this exists

Every modern ESP now ships an AI composer. They all produce the same email: hero icon, three-card grid, generic palette, "Read more →" CTA, plain footer. The output is technically correct and visually forgettable.

This skill makes Claude commit. Pick a colour strategy. Pick an archetype. Source a real image. Write a real footer. Default to asymmetric padding instead of moonscape spacing. The result reads like a brand made it, not a model.

## Anti-slop principles

The full set is in [SKILL.md](./SKILL.md). Highlights:

- **Own a colour.** Restrained, committed, or drenched. Pick the strategy *before* the colour.
- **No category-reflex palettes.** If "fintech → navy + gold" or "wellness → white + sage" describes your draft, rework it.
- **Real imagery only.** No stock, no AI slop, no flat geometric shapes as decoration. A clearly-marked placeholder beats visual filler.
- **Whitespace is asymmetric.** Default to `padding_top: 0, padding_bottom: 32`. No orphan spacers, no double `<br>`, no margin+padding combos.
- **Footers do real work.** Mission line + 3–5 socials + physical address + visible unsubscribe.
- **Voice over template.** The strongest brands (theSkimm, Patagonia, Frank Body, Liquid Death) are recognisable by tone alone.

## Six archetypes

| Archetype | When | Reference |
|---|---|---|
| **Editorial** | Newsletters, brand stories | Patagonia, Tracksmith |
| **Bold mono** | Promo, launches, statements | Absolut, Liquid Death |
| **Minimal lux** | Premium, transactional | Stripe, Aesop, Apple |
| **Founder letter** | Welcome, win-back | Ugmonk, Superhuman |
| **Punk / character** | Brand voice carriers | Frank Body, Duolingo |
| **Lookbook** | Product, fashion, food | Dior, Clare Paint |

## Compatibility

- **Claude Code** — primary target. Loads from `~/.claude/skills/email-design/`.
- **Nitrosend** — first-class. Maps the brief directly to `nitro_compose_campaign` sections with explicit padding overrides.
- **Other ESPs** — works wherever Claude has tool access. The brief format is sending-tool-agnostic; translation tables for other platforms can be added as PRs.

## Contributing

Issues and PRs welcome. Especially helpful:

- New translation tables for other ESPs (Klaviyo, Mailchimp, Resend, etc.)
- Additional archetype examples
- Brand-context heuristics for non-Nitrosend setups

## License

MIT. See [LICENSE](./LICENSE).

## Related

- [email-marketing-bible](https://github.com/CosmoBlk/email-marketing-bible) — strategy, deliverability, copy, segmentation, 19 industry playbooks. Pairs well with this skill.
- [Nitrosend](https://nitrosend.com) — AI-native ESP, MCP-first.
