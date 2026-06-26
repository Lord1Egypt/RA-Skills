---
title: FAQ
description: Frequently asked questions about ComfyUI Skills, including CLI installation, workflow import, multi-server support, dependency management, and the optional web UI.
permalink: /faq/
---

<section class="hero">
  <div class="hero-inner">
    <div class="hero-copy">
      <p class="eyebrow">FAQ</p>
      <h1>Frequently asked questions about ComfyUI Skills</h1>
      <p class="lede">
        These answers cover CLI usage, workflow management, multi-server setup,
        and agent integration.
      </p>
      <div class="quick-links">
        <a class="quick-link" href="{{ '/getting-started/' | relative_url }}">Getting Started</a>
        <a class="quick-link" href="{{ '/architecture/' | relative_url }}">Architecture</a>
        <a class="quick-link" href="https://github.com/HuangYuChuh/ComfyUI_Skills_OpenClaw/stargazers">Star on GitHub</a>
      </div>
    </div>
  </div>
</section>

<div class="grid">
  {% for item in site.data.faq %}
  <section class="section-card">
    <h2>{{ item.question }}</h2>
    <p>{{ item.answer }}</p>
  </section>
  {% endfor %}
</div>
