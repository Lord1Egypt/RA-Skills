# Fly Coworker 🪰

Let a simulated fly choose your next task. Watch it explore a 3D arena, veto its pick with a cartoon salt blaster, or click **Accept & start** to send the chosen task to your OpenClaw conversation.

## Install and try it

Install both the skill and its dashboard companion:

```sh
openclaw skills install @GrahamMcBain/fly-coworker
openclaw plugins install clawhub:openclaw-plugin-fly-coworker
```

See [companion setup and verification](plugin-install.md). Source: https://github.com/GrahamMcBain/fly-coworker .

Requires OpenClaw 2026.9.4+, Node.js 22+, Google Chrome and WebGL2. Enable **Settings → Labs → Custom plugin UI**.

Tell your agent:

> Let the fly decide: review the open PR in my project, fix its failing test, or draft release notes.

Supply 2–64 actionable choices. OpenClaw opens the Fly dashboard in Chrome. The fly picks; you accept or veto. Acceptance sends exactly the selected task to the owning conversation under your normal agent permissions. Keep Chrome open while the fly decides.

## What is simulated?

A 1,045-neuron MaleCNS brain-to-leg circuit drives movement, with FlyGym/NeuroMechFly anatomical meshes. This is a novelty decision aid, not a full fly brain, task-comprehension system, uniform random selector or MuJoCo simulation. See [scope](docs/SCOPE.md).

## Privacy and compatibility

The widget loads bundled assets from your authenticated Gateway. No external asset host, analytics, API key, iframe or separate server is needed. Rounds are stored in OpenClaw; accepting sends task text to the owning conversation, where your configured model/data routing applies. A durable one-time claim prevents duplicate submissions. An uncertain handoff requires checking the conversation before retrying.

macOS/Chrome is verified. Other platforms are unverified. The native Mac app has a known plugin-cookie issue over local HTTP; use Chrome. Do not weaken authentication. Private browser bootstrap URLs are never share links.

## Credits

Original code: MIT. DesktopFly neural engine: MIT. FlyGym/NeuroMechFly anatomy: Apache-2.0. MaleCNS data: CC BY 4.0. Three.js: MIT. See [third-party notices](THIRD_PARTY.md). No noncommercial FlyWire dataset or BUG-A-SALT brand assets are included.
