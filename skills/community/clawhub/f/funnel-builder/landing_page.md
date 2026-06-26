# Landing Page Templates — Funnel Revenue Engine

The agent uses these section templates to build landing pages.
Each section is a building block. The agent selects and assembles
the sections defined in funnel_config.json for the active business model,
then fills all `[PLACEHOLDERS]` with real business data.

---

## GLOBAL STYLE — Apply to all pages

```html
<!-- Paste this in the <head> of every landing page -->
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0a0a0a; color: #f0f0f0; line-height: 1.6;
  }
  .container { max-width: 720px; margin: 0 auto; padding: 0 24px; }
  .btn-primary {
    display: inline-block; background: #22c55e; color: #000;
    padding: 16px 32px; border-radius: 8px; font-weight: 700;
    font-size: 1.1rem; text-decoration: none; cursor: pointer;
    border: none; transition: background 0.2s;
  }
  .btn-primary:hover { background: #16a34a; }
  .btn-secondary {
    display: inline-block; border: 1px solid #444; color: #ccc;
    padding: 12px 24px; border-radius: 8px; text-decoration: none;
    font-size: 0.95rem;
  }
  .highlight { color: #22c55e; }
  .muted { color: #888; font-size: 0.9rem; }
  section { padding: 64px 0; border-bottom: 1px solid #1a1a1a; }
</style>
```

---

## SECTION: hero_headline

**Use for:** b2b-saas, b2c-subscription, services

```html
<section style="padding: 80px 0 64px; text-align: center;">
  <div class="container">
    <!-- EYEBROW — optional, use for social proof or category -->
    <p style="color:#22c55e; font-size:0.85rem; text-transform:uppercase;
              letter-spacing:2px; margin-bottom:16px;">
      [EYEBROW — ex: "Trusted by 200+ founders" or leave empty]
    </p>

    <!-- HEADLINE — the single most important line on the page -->
    <!-- Formula: [Result] for [ICP] without [Pain] -->
    <h1 style="font-size:clamp(2rem,5vw,3.2rem); font-weight:800;
                line-height:1.15; margin-bottom:24px;">
      [HEADLINE — ex: "Close 3x more B2B deals<br>
      without a sales team"]
    </h1>

    <!-- SUBHEADLINE — expand the headline, add specificity -->
    <p style="font-size:1.2rem; color:#aaa; max-width:560px;
              margin:0 auto 40px;">
      [SUBHEADLINE — ex: "Automated outreach + AI qualification
      that books calls while you sleep. Used by 200+ SaaS founders."]
    </p>

    <!-- CTA BLOCK -->
    <div style="display:flex; gap:16px; justify-content:center;
                flex-wrap:wrap; align-items:center;">
      <a href="[PAYMENT_OR_SIGNUP_LINK]" class="btn-primary">
        [CTA_PRIMARY — ex: "Start free 14-day trial"]
      </a>
      <a href="#how-it-works" class="btn-secondary">
        [CTA_SECONDARY — ex: "See how it works"]
      </a>
    </div>

    <!-- RISK REDUCER — just below the CTA -->
    <p class="muted" style="margin-top:16px;">
      [RISK_REDUCER — ex: "No credit card required. Cancel anytime."]
    </p>
  </div>
</section>
```

---

## SECTION: hero_result_proof

**Use for:** trading-signals, digital-product

```html
<section style="padding: 80px 0 64px; text-align: center;">
  <div class="container">
    <!-- LEAD WITH THE RESULT — not the product -->
    <p style="font-size:0.85rem; color:#22c55e; text-transform:uppercase;
              letter-spacing:2px; margin-bottom:16px;">
      [TIMEFRAME — ex: "Last 30 days results"]
    </p>

    <h1 style="font-size:clamp(2rem,5vw,3rem); font-weight:800;
                line-height:1.2; margin-bottom:16px;">
      [BIG NUMBER RESULT — ex: "+€2,847 net profit<br>
      from 23 trades in March"]
    </h1>

    <!-- PROOF ELEMENT — screenshot placeholder -->
    <div style="background:#111; border:1px solid #2a2a2a; border-radius:12px;
                padding:24px; margin:32px auto; max-width:480px;">
      [INSERT_SCREENSHOT_OR_RESULTS_TABLE_HERE]
      <p class="muted" style="margin-top:12px;">
        [PROOF_CAPTION — ex: "Verified P&L — Binance account #****4821"]
      </p>
    </div>

    <a href="[SIGNUP_LINK]" class="btn-primary" style="margin-bottom:12px;">
      [CTA — ex: "Get the free weekly signal"]
    </a>
    <br>
    <p class="muted">[RISK_REDUCER — ex: "Free. No credit card. Unsubscribe anytime."]</p>
  </div>
</section>
```

---

## SECTION: pain_agitation

**Use for:** b2b-saas, services, digital-product

```html
<section id="problem">
  <div class="container">
    <h2 style="font-size:1.8rem; font-weight:700; margin-bottom:32px;">
      [PAIN_HEADER — ex: "Sound familiar?"]
    </h2>

    <!-- List the pains as statements the ICP recognizes immediately -->
    <ul style="list-style:none; display:flex; flex-direction:column; gap:16px;">
      <li style="display:flex; gap:12px; align-items:flex-start;">
        <span style="color:#ef4444; font-size:1.2rem;">✗</span>
        <span>[PAIN_1 — ex: "You spend 4+ hours/day on manual prospecting that goes nowhere"]</span>
      </li>
      <li style="display:flex; gap:12px; align-items:flex-start;">
        <span style="color:#ef4444; font-size:1.2rem;">✗</span>
        <span>[PAIN_2 — ex: "Your pipeline is full of leads that never convert"]</span>
      </li>
      <li style="display:flex; gap:12px; align-items:flex-start;">
        <span style="color:#ef4444; font-size:1.2rem;">✗</span>
        <span>[PAIN_3 — ex: "You've tried [X] but it didn't work for [reason]"]</span>
      </li>
    </ul>

    <!-- AGITATION — what it costs to stay in this situation -->
    <div style="background:#1a0000; border:1px solid #3a0000; border-radius:8px;
                padding:24px; margin-top:40px;">
      <p style="color:#fca5a5;">
        [COST_OF_INACTION — ex: "Every week you delay costs you approximately
        €[X] in potential revenue — and your competitors are moving faster."]
      </p>
    </div>
  </div>
</section>
```

---

## SECTION: what_you_get

**Use for:** b2c-subscription, trading-signals, content-media

```html
<section id="what-you-get">
  <div class="container">
    <h2 style="font-size:1.8rem; font-weight:700; margin-bottom:8px;">
      [SECTION_TITLE — ex: "What you get inside"]
    </h2>
    <p style="color:#888; margin-bottom:40px;">
      [SECTION_SUBTITLE — ex: "Everything included from day 1"]
    </p>

    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
                gap:20px;">

      <!-- Repeat this block for each feature/benefit (3-6 total) -->
      <div style="background:#111; border:1px solid #222; border-radius:10px; padding:24px;">
        <div style="font-size:1.8rem; margin-bottom:12px;">[EMOJI]</div>
        <h3 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">
          [FEATURE_NAME — ex: "Weekly trading signal"]
        </h3>
        <p style="color:#999; font-size:0.9rem;">
          [FEATURE_DESCRIPTION — ex: "Every Monday: 1 high-conviction trade
          with entry, target, and stop loss. Average +3.2% per signal."]
        </p>
      </div>

    </div>
  </div>
</section>
```

---

## SECTION: pricing_simple

**Use for:** b2c-subscription, trading-signals

```html
<section id="pricing">
  <div class="container" style="text-align:center;">
    <h2 style="font-size:1.8rem; font-weight:700; margin-bottom:8px;">
      [PRICING_TITLE — ex: "One price. Everything included."]
    </h2>

    <div style="background:#111; border:1px solid #22c55e; border-radius:16px;
                padding:40px; max-width:400px; margin:40px auto;">

      <!-- PRICE DISPLAY -->
      <div style="margin-bottom:24px;">
        <span style="font-size:3rem; font-weight:800; color:#22c55e;">
          €[PRICE]
        </span>
        <span style="color:#888;">/month</span>
      </div>

      <!-- WHAT'S INCLUDED -->
      <ul style="list-style:none; text-align:left; margin-bottom:32px;
                 display:flex; flex-direction:column; gap:10px;">
        <li>✅ [INCLUDE_1]</li>
        <li>✅ [INCLUDE_2]</li>
        <li>✅ [INCLUDE_3]</li>
        <li>✅ [INCLUDE_4]</li>
      </ul>

      <a href="[PAYMENT_LINK]" class="btn-primary" style="width:100%;
         display:block; text-align:center;">
        [CTA — ex: "Start 7-day free trial"]
      </a>

      <p class="muted" style="margin-top:16px;">
        [GUARANTEE — ex: "7-day money-back guarantee. No questions."]
      </p>
    </div>

    <!-- COMPARISON — optional, destroys objection -->
    <p style="color:#666; font-size:0.9rem; margin-top:24px;">
      [COMPARISON — ex: "Less than one coffee per week.
      One winning trade covers 6 months of subscription."]
    </p>
  </div>
</section>
```

---

## SECTION: guarantee

**Use for:** all models

```html
<section style="background:#0d1a0d; border-top:1px solid #1a2e1a;
               border-bottom:1px solid #1a2e1a;">
  <div class="container" style="text-align:center;">
    <div style="font-size:3rem; margin-bottom:16px;">🛡️</div>
    <h2 style="font-size:1.5rem; font-weight:700; margin-bottom:12px;">
      [GUARANTEE_TITLE — ex: "7-day money-back guarantee"]
    </h2>
    <p style="color:#aaa; max-width:480px; margin:0 auto;">
      [GUARANTEE_TEXT — ex: "Try it for 7 days. If you're not completely
      satisfied — for any reason — email us and we'll refund 100%.
      No forms. No questions. No hassle."]
    </p>
  </div>
</section>
```

---

## SECTION: faq

**Use for:** all models (3-5 questions max)

```html
<section id="faq">
  <div class="container">
    <h2 style="font-size:1.8rem; font-weight:700; margin-bottom:40px;">
      Frequently asked questions
    </h2>

    <!-- Repeat for each Q&A -->
    <details style="border-bottom:1px solid #1a1a1a; padding:20px 0; cursor:pointer;">
      <summary style="font-weight:600; font-size:1rem; list-style:none;">
        [QUESTION — ex: "Do I need trading experience?"]
      </summary>
      <p style="color:#aaa; margin-top:12px; padding-left:8px;">
        [ANSWER — ex: "No. Each signal comes with full instructions:
        exact entry price, take-profit, and stop-loss. You follow
        the signal — the system does the thinking."]
      </p>
    </details>

  </div>
</section>
```

---

## SECTION: final_cta

**Use for:** all models — always the last section

```html
<section style="text-align:center; padding:80px 0;">
  <div class="container">
    <h2 style="font-size:2rem; font-weight:800; margin-bottom:16px;">
      [FINAL_HEADLINE — ex: "Ready to start?"]
    </h2>
    <p style="color:#888; margin-bottom:32px;">
      [FINAL_SUBLINE — ex: "Join [N] subscribers already getting results."]
    </p>
    <a href="[CTA_LINK]" class="btn-primary">
      [CTA_TEXT — ex: "Start your free trial now"]
    </a>
    <p class="muted" style="margin-top:16px;">
      [RISK_REDUCER]
    </p>
  </div>
</section>
```
