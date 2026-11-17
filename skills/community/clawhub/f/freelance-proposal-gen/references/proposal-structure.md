# Proposal Structure Reference

This document is the spec for the proposal template. WorkBuddy reads it while
building the fields JSON so output stays consistent and high-quality.

## Token Dictionary

All tokens are uppercase and wrapped in `{{ }}`. Pass lists/tables as ready HTML.

| Token | Type | Notes |
|-------|------|-------|
| `PROPOSAL_TITLE` | text | Headline of the proposal |
| `PROPOSAL_SUBTITLE` | text | One-line supporting statement |
| `PREPARED_FOR` | text | Client / company name |
| `YOUR_NAME` | text | Sender name |
| `YOUR_TITLE` | text | Sender role (e.g. 独立前端工程师) |
| `DATE` | text | Issue date (YYYY-MM-DD) |
| `PAIN_INTRO` | text | Lead-in sentence before pain list |
| `PAIN_POINTS` | HTML `<li>` list | 3 client problems |
| `SOLUTION_INTRO` | text | Lead-in before solution blocks |
| `SOLUTION_BLOCKS` | HTML blocks | 2–3 `<div class="block">…</div>` |
| `DELIVERABLES` | HTML `<li>` list | What the client gets |
| `PRICING_TABLE` | HTML `<tr>` rows | Package / scope / price |
| `CASE_INTRO` | text | Lead-in before cases |
| `CASES` | HTML cards | 1–2 `<div class="case">…</div>` |
| `CTA_TEXT` | text | The ask / next step |
| `CONTACT_LINE` | text | Email / WeChat / site |
| `WECHAT` | text | WeChat ID, used by the corner watermark (lead-gen) |
| `WEBSITE` | text | Portfolio / site URL, used by the corner watermark (optional) |
| `SHOW_CONTACT_WATERMARK` | text `true`/`false` | Toggle the corner watermark (default `true`) |
| `CONTACT_WATERMARK` | HTML | **Auto-built** by the renderer — do not set manually |
| `ACCENT` | CSS color | Theme accent (default #4f46e5) |

Any token left as `{{...}}` in the final HTML is blanked by the renderer.

## Section Anatomy (top → bottom)

1. **Cover** — title, subtitle, "Prepared for {client}", date, sender.
2. **Pain** — `PAIN_INTRO` + 3 `PAIN_POINTS`. Speak the client's words.
3. **Solution** — `SOLUTION_INTRO` + `SOLUTION_BLOCKS` (approach, not features).
4. **Deliverables** — concrete `DELIVERABLES` list (what ships).
5. **Pricing** — `PRICING_TABLE`, 2–3 tiers, at least one real number.
6. **Proof** — `CASE_INTRO` + `CASES` (result + metric).
7. **CTA** — `CTA_TEXT` + `CONTACT_LINE`.
8. **Corner watermark** — `CONTACT_WATERMARK`, a subtle always-on brand pill
   (name + `WECHAT` + `WEBSITE`) shown on screen, hidden on print. Toggle with
   `SHOW_CONTACT_WATERMARK=false`. This is the lead-gen hook: every shared
   screenshot or forwarded HTML carries your contact.

## Copywriting Principles

- Lead with the client's problem, not your bio. Bio appears only in the footer.
- One idea per block. Short paragraphs (≤ 3 sentences).
- Pricing: show 2–3 tiers; the middle tier is the "recommended" one.
-量化 everything: "提升 40% 转化率" beats "提升转化率".
- CTA must be a single, obvious next action with a deadline if possible.

## Default Copy (use when a field is missing)

- `PAIN_INTRO`: "在正式合作前，我们先把当前最关键的问题拆开看："
- `SOLUTION_INTRO`: "针对上面的问题，我们的做法是："
- `CTA_TEXT`: "如果你觉得方向对，我们这周就能启动。回复一句话即可安排首次沟通。"
- `CONTACT_LINE`: "微信：g13403583297 ｜ 邮箱：g13403583297@163.com"
- `WECHAT` (watermark default): "g13403583297"
- `WEBSITE` (watermark default): "" （留空则不显示站点）

## Pricing Table Row Format

```html
<tr>
  <td>
    <div class="pkg">基础版</div>
    <div class="pkg-note">适合刚起步的个人 / 小团队</div>
  </td>
  <td>核心交付物 A、B、C</td>
  <td class="price">¥X,XXX 起</td>
</tr>
```

Mark the recommended tier with class `recommended` on the `<tr>`.
