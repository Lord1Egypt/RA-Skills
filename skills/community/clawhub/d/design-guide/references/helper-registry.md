# Helper Registry

Use this registry to recommend or select helper skills/tools. Only name helpers that are visible in the current host environment; otherwise say they are not detected and continue with a fallback.

## Build And Polish

- `web-design-engineer`: build polished HTML/CSS/JS/React visual artifacts.
- `design-taste-frontend`: correct generic AI-looking landing pages, portfolios, and redesigns.
- `web-design-guidelines`: audit UI, UX, accessibility, and web-interface best practices.
- `webapp-testing`: browser-based testing and screenshot QA when available.
- Product design reviews use `design-guide` as the primary evaluator. Use `web-design-guidelines` for accessibility and UX critique, `webapp-testing` for screenshot/interaction evidence, and `design-taste-frontend` only for marketing-page, portfolio, or redesign taste signals that fit the artifact.

## Motion

- `css-animations`: simple CSS keyframes, transitions, and microinteractions.
- `waapi`: Web Animations API for native timeline control.
- `animejs`: lightweight JS animation where framework coupling is low.
- `gsap`: complex sequencing, scroll-triggered motion, SVG motion, and heavier choreography.

## 3D And Rich Media

- `three`: 3D/WebGL scenes and interactive 3D experiences.
- `lottie`: Lottie animation integration and asset handling.
- `web-video-presentation`: browser-rendered video/presentation work.
- `remotion-to-hyperframes`: Remotion migration or translation work when relevant.

## Screenshot, Image, And Asset Work

- `image-to-code`: turn screenshots into frontend code.
- `yueban-image-to-code`: pixel-level screenshot-to-code when available.
- `gpt-image-2`, `hoviw-image-gen`, `baoyu-image-gen`: generate image assets when the user asks for assets or the interface depends on them.
- `image-enhancer`: improve existing raster assets.

## Design Systems And Specialized UI

- `aceternity-ui`: animated component ideas; do not let it decide the whole product style.
- `minimalist-ui`: clean minimal UI direction when available.
- `ui-ux-pro-max`: high-level UI/UX critique or design enhancement when available.
- `weapp-tailwindcss`, `wechat-miniprogram-skill`, `miniprogram-development`: WeChat mini-program and related frontend work.

## Selection Rule

Prefer fewer helpers. Pick the smallest set that covers the task:

- New app screen: `design-guide` plus local framework/CSS, optionally `web-design-engineer`.
- Existing UI improvement: `design-guide` plus `design-taste-frontend` or `web-design-guidelines`.
- Existing product/page design evaluation: `design-guide` plus `web-design-guidelines` for critique depth, `webapp-testing` for screenshot/interaction evidence, and `design-taste-frontend` only when landing-page or visual taste heuristics apply.
- Animation: `design-guide` plus one motion helper.
- 3D: `design-guide` plus `three`.
- Screenshot recreation: `design-guide` plus one screenshot-to-code helper.
