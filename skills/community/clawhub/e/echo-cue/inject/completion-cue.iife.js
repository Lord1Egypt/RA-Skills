// completion-cue v3 — local stop-gap for openclaw/openclaw#69186
// Plays a short Web Audio cue when an assistant message finishes rendering
// in the OpenClaw Control UI. Skips NO_REPLY / empty completions. Defaults to
// ring in both foreground and background. Per-browser opt-out via localStorage.
//
// Anchor: DOM nodes matching `.chat-group.assistant`. Fail-quiet if absent.
//
// localStorage keys (also editable via the floating 🔔 widget in the page):
//   milly.completionCue            = 'off'      → fully disable
//   milly.completionCue.onlyHidden = 'on'       → only ring when tab is hidden/unfocused
//   milly.completionCue.sound      = '<name>'   → pick preset, see SOUNDS keys below
//   milly.completionCue.widget     = 'off'      → hide the floating 🔔 settings button
(() => {
  if (typeof window === "undefined" || typeof document === "undefined") return;
  if (window.__milly_cue_v1__) return;
  window.__milly_cue_v1__ = true;

  const LS = (() => {
    try { return window.localStorage; } catch (_) { return null; }
  })();
  const get = (k) => { try { return LS && LS.getItem(k); } catch (_) { return null; } };
  const set = (k, v) => { try { LS && LS.setItem(k, v); } catch (_) { /* ignore */ } };
  const del = (k) => { try { LS && LS.removeItem(k); } catch (_) { /* ignore */ } };

  const Ctor = window.AudioContext || window.webkitAudioContext;
  if (!Ctor) return;

  let ctx = null;
  const ensureCtx = () => {
    if (!ctx) {
      try { ctx = new Ctor(); } catch (_) { ctx = null; }
    }
    if (ctx && ctx.state === "suspended") {
      try { ctx.resume(); } catch (_) { /* ignore */ }
    }
    return ctx;
  };
  const unlock = () => { ensureCtx(); };
  window.addEventListener("pointerdown", unlock, { once: true, capture: true, passive: true });
  window.addEventListener("keydown",     unlock, { once: true, capture: true });
  window.addEventListener("touchstart",  unlock, { once: true, capture: true, passive: true });

  // ---------- Sound preset registry ----------
  const playTone = (c, master, freq, start, dur, type, peak) => {
    const osc = c.createOscillator();
    const g = c.createGain();
    osc.type = type || "sine";
    osc.frequency.value = freq;
    const ts = c.currentTime + start;
    const p = peak == null ? 0.6 : peak;
    g.gain.setValueAtTime(0.0001, ts);
    g.gain.exponentialRampToValueAtTime(p, ts + 0.015);
    g.gain.exponentialRampToValueAtTime(0.0001, ts + dur);
    osc.connect(g).connect(master);
    osc.start(ts);
    osc.stop(ts + dur + 0.02);
  };

  // Tone with a frequency sweep from f0 → f1 over `dur`. Useful for pops,
  // droplets, retro blips. `curve` = 'exp' (musical) or 'lin' (sharper).
  const playSweep = (c, master, f0, f1, start, dur, type, peak, curve) => {
    const osc = c.createOscillator();
    const g = c.createGain();
    osc.type = type || "sine";
    const ts = c.currentTime + start;
    const p = peak == null ? 0.6 : peak;
    osc.frequency.setValueAtTime(f0, ts);
    if (curve === "lin") osc.frequency.linearRampToValueAtTime(f1, ts + dur);
    else osc.frequency.exponentialRampToValueAtTime(Math.max(1, f1), ts + dur);
    g.gain.setValueAtTime(0.0001, ts);
    g.gain.exponentialRampToValueAtTime(p, ts + 0.012);
    g.gain.exponentialRampToValueAtTime(0.0001, ts + dur);
    osc.connect(g).connect(master);
    osc.start(ts);
    osc.stop(ts + dur + 0.02);
  };

  // Short white-noise burst, optionally band-passed. Good for water splashes,
  // bubbles, fish-bite plonks, sand-rustle textures.
  let NOISE_BUF = null;
  const noiseBuf = (c) => {
    if (NOISE_BUF && NOISE_BUF.sampleRate === c.sampleRate) return NOISE_BUF;
    const len = Math.floor(c.sampleRate * 0.5);
    const buf = c.createBuffer(1, len, c.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < len; i++) data[i] = Math.random() * 2 - 1;
    NOISE_BUF = buf;
    return buf;
  };
  const playNoise = (c, master, start, dur, peak, bp) => {
    const src = c.createBufferSource();
    src.buffer = noiseBuf(c);
    const g = c.createGain();
    const ts = c.currentTime + start;
    const p = peak == null ? 0.3 : peak;
    g.gain.setValueAtTime(0.0001, ts);
    g.gain.exponentialRampToValueAtTime(p, ts + 0.008);
    g.gain.exponentialRampToValueAtTime(0.0001, ts + dur);
    let tail = g;
    if (bp) {
      const f = c.createBiquadFilter();
      f.type = "bandpass";
      f.frequency.value = bp.freq || 1200;
      f.Q.value = bp.q || 1.5;
      g.connect(f);
      tail = f;
    }
    src.connect(g);
    tail.connect(master);
    src.start(ts);
    src.stop(ts + dur + 0.02);
  };

  // label is shown in the picker UI. key is what's stored in localStorage.
  // group is the section header in the picker.
  const SOUNDS = [
    {
      group: "Basic",
      key: "chime",
      label: "Chime 叮咚 (default)",
      play: (c, m) => {
        playTone(c, m, 880, 0,    0.55, "sine", 0.6);  // A5
        playTone(c, m, 659, 0.18, 0.55, "sine", 0.6);  // E5
      },
    },
    {
      group: "Basic",
      key: "tritone",
      label: "Tritone (iPhone SMS-like)",
      play: (c, m) => {
        playTone(c, m, 1318, 0.00, 0.16, "triangle", 0.55);  // E6
        playTone(c, m, 1046, 0.13, 0.16, "triangle", 0.55);  // C6
        playTone(c, m, 1568, 0.26, 0.22, "triangle", 0.55);  // G6
      },
    },
    {
      // Bubble pop — quick upward swoop, ~110ms.
      group: "Basic",
      key: "pop",
      label: "Pop 🫭 (bubble)",
      play: (c, m) => {
        playSweep(c, m, 380, 1400, 0, 0.11, "sine", 0.55, "exp");
      },
    },
    {
      // Twinkle — fast C→E→G arpeggio, ~280ms.
      group: "Basic",
      key: "twinkle",
      label: "Twinkle ✨ (arpeggio)",
      play: (c, m) => {
        playTone(c, m, 1047, 0.00, 0.12, "triangle", 0.45);  // C6
        playTone(c, m, 1319, 0.09, 0.12, "triangle", 0.45);  // E6
        playTone(c, m, 1568, 0.18, 0.20, "triangle", 0.45);  // G6
      },
    },
    {
      // Water droplet — quick downward sweep with a soft tail, ~180ms.
      group: "Basic",
      key: "droplet",
      label: "Droplet 💧 (water)",
      play: (c, m) => {
        playSweep(c, m, 1600, 520, 0, 0.18, "sine", 0.5, "exp");
      },
    },

    // ---- Animal Crossing ----
    {
      // Animal Crossing fish-bite "plop" — low downward sine plonk +
      // tiny band-passed noise splash. ~220ms.
      group: "Animal Crossing",
      key: "fishbite",
      label: "Fish Bite 🐟 (AC plonk)",
      play: (c, m) => {
        playSweep(c, m, 520, 140, 0, 0.18, "sine", 0.55, "exp");
        playNoise(c, m, 0.005, 0.10, 0.18, { freq: 1800, q: 1.2 });
      },
    },
    {
      // Animal Crossing dialog "blip" — single short triangle chirp,
      // the soft talky beep characters make. ~90ms.
      group: "Animal Crossing",
      key: "villager",
      label: "Villager 🐾 (dialog blip)",
      play: (c, m) => {
        playSweep(c, m, 720, 880, 0, 0.09, "triangle", 0.45, "exp");
      },
    },
    {
      // Animal Crossing-ish item / shovel-hit short bell-tone "ding".
      // Bright single bell, ~260ms.
      group: "Animal Crossing",
      key: "acbell",
      label: "AC Bell 🔔 (item ding)",
      play: (c, m) => {
        playTone(c, m, 1760, 0,    0.22, "sine",     0.5);   // A6 body
        playTone(c, m, 3520, 0,    0.10, "triangle", 0.18);  // A7 shimmer
      },
    },

    // ---- Super Mario ----
    {
      // Mario coin — classic two-note B5 → E6 square chirp. ~220ms.
      group: "Super Mario",
      key: "coin",
      label: "Coin 🪙 (Mario coin)",
      play: (c, m) => {
        playTone(c, m, 988,  0.00, 0.08, "square", 0.32);  // B5
        playTone(c, m, 1319, 0.07, 0.18, "square", 0.32);  // E6
      },
    },
    {
      // Mario jump — fast upward square pitch sweep, ~150ms.
      group: "Super Mario",
      key: "mariojump",
      label: "Jump 🍄 (Mario jump)",
      play: (c, m) => {
        playSweep(c, m, 380, 880, 0, 0.15, "square", 0.3, "exp");
      },
    },
    {
      // Mario 1-Up — quick rising arpeggio E5-G5-E6-C6-E6-G6.
      // Simplified to fit under ~450ms.
      group: "Super Mario",
      key: "oneup",
      label: "1-Up 🍄 (life-up fanfare)",
      play: (c, m) => {
        const seq = [
          [659,  0.00, 0.09],  // E5
          [784,  0.08, 0.09],  // G5
          [1319, 0.16, 0.09],  // E6
          [1047, 0.24, 0.09],  // C6
          [1319, 0.32, 0.09],  // E6
          [1568, 0.40, 0.16],  // G6
        ];
        for (const [f, s, d] of seq) playTone(c, m, f, s, d, "square", 0.3);
      },
    },
    {
      // Mario power-up (mushroom) — fast rising blippy arpeggio.
      // Approximates the iconic ascending climb. ~360ms.
      group: "Super Mario",
      key: "powerup",
      label: "Power-up 🌟 (mushroom climb)",
      play: (c, m) => {
        const seq = [
          [523,  0.00, 0.06],  // C5
          [784,  0.05, 0.06],  // G5
          [1047, 0.10, 0.06],  // C6
          [659,  0.15, 0.06],  // E5
          [880,  0.20, 0.06],  // A5
          [1175, 0.25, 0.06],  // D6
          [784,  0.30, 0.10],  // G5
        ];
        for (const [f, s, d] of seq) playTone(c, m, f, s, d, "square", 0.28);
      },
    },
    {
      // Mario pipe / warp — descending square slide, ~280ms.
      group: "Super Mario",
      key: "pipe",
      label: "Pipe 🟢 (warp down)",
      play: (c, m) => {
        playSweep(c, m, 880, 110, 0, 0.28, "square", 0.3, "exp");
      },
    },
    {
      // Mario bump / kick (head-hit block when empty) — short low square
      // thump with a tiny noise click. ~120ms.
      group: "Super Mario",
      key: "bump",
      label: "Bump 🧱 (block bonk)",
      play: (c, m) => {
        playTone(c, m, 196, 0,    0.12, "square", 0.35);  // G3
        playNoise(c, m, 0,   0.04, 0.12, { freq: 1200, q: 1.0 });
      },
    },

    // ---- Retro ----
    {
      // Nokia tune — the iconic 13-note phrase from Tárrega's "Gran Vals".
      // Compressed to fit ~1.2s while staying recognizable.
      group: "Retro",
      key: "nokia",
      label: "Nokia Tune 📱 (Gran Vals)",
      play: (c, m) => {
        const N = 0.085;  // sixteenth ~85ms
        // E5 D5 F#5 G#5 | C#5 B4 D5 E5 | B4 A4 C#5 E5 | A4
        const seq = [
          [659,  0 * N, N * 1, "square", 0.32],   // E5
          [587,  1 * N, N * 1, "square", 0.32],   // D5
          [740,  2 * N, N * 2, "square", 0.32],   // F#5 (eighth)
          [831,  4 * N, N * 2, "square", 0.32],   // G#5 (eighth)

          [554,  6 * N, N * 1, "square", 0.32],   // C#5
          [494,  7 * N, N * 1, "square", 0.32],   // B4
          [587,  8 * N, N * 2, "square", 0.32],   // D5 (eighth)
          [659, 10 * N, N * 2, "square", 0.32],   // E5 (eighth)

          [494, 12 * N, N * 1, "square", 0.32],   // B4
          [440, 13 * N, N * 1, "square", 0.32],   // A4
          [554, 14 * N, N * 2, "square", 0.32],   // C#5 (eighth)
          [659, 16 * N, N * 2, "square", 0.32],   // E5 (eighth)
          [440, 18 * N, N * 4, "square", 0.32],   // A4 (quarter)
        ];
        for (const [f, s, d, t, p] of seq) playTone(c, m, f, s, d, t, p);
      },
    },
    {
      // Dial-up modem handshake mini-impression: a couple of "dee-dee" tones
      // followed by a short white-noise hiss — hints at the iconic
      // negotiation screech without the full 30s sequence. ~600ms.
      group: "Retro",
      key: "modem",
      label: "Modem 📞 (dial-up echo)",
      play: (c, m) => {
        playTone(c, m, 1100, 0.00, 0.10, "sine", 0.4);  // hi tone
        playTone(c, m, 1400, 0.12, 0.10, "sine", 0.4);  // higher tone
        playTone(c, m,  900, 0.26, 0.10, "sine", 0.4);  // dip back
        playNoise(c, m, 0.40, 0.18, 0.22, { freq: 2200, q: 1.5 }); // screech tail
      },
    },
  ];
  const SOUND_INDEX = Object.fromEntries(SOUNDS.map((s) => [s.key, s]));
  const DEFAULT_SOUND = "chime";

  const currentSoundKey = () => {
    const name = (get("milly.completionCue.sound") || DEFAULT_SOUND).toLowerCase();
    return SOUND_INDEX[name] ? name : DEFAULT_SOUND;
  };

  const playPreset = (key) => {
    const c = ensureCtx();
    if (!c) return;
    try {
      const master = c.createGain();
      master.gain.value = 0.5;
      master.connect(c.destination);
      (SOUND_INDEX[key] || SOUND_INDEX[DEFAULT_SOUND]).play(c, master);
    } catch (_) { /* swallow — never break the page */ }
  };

  // ---------- Dispatch / dedup ----------
  const seen = new WeakSet();
  const SILENT_TEXTS = new Set(["NO_REPLY", "REPLY_SKIP", "ANNOUNCE_SKIP"]);

  const MIN_GAP_MS = 4000;
  let lastDingAt = 0;
  const RECENT_TEXTS = new Map();
  const TEXT_TTL_MS = 10000;

  const shouldRing = (root) => {
    if (!root) return false;
    if (get("milly.completionCue") === "off") return false;
    const text = (root.textContent || "").trim();
    if (!text) return false;
    if (SILENT_TEXTS.has(text)) return false;
    if (get("milly.completionCue.onlyHidden") === "on") {
      const hidden = document.visibilityState === "hidden" || !document.hasFocus();
      if (!hidden) return false;
    }
    const now = Date.now();
    if (now - lastDingAt < MIN_GAP_MS) return false;
    for (const [t, ts] of RECENT_TEXTS) {
      if (now - ts > TEXT_TTL_MS) RECENT_TEXTS.delete(t);
    }
    const fp = text.length + "|" + text.slice(0, 80);
    if (RECENT_TEXTS.has(fp)) return false;
    RECENT_TEXTS.set(fp, now);
    if (seen.has(root)) return false;
    seen.add(root);
    return true;
  };

  let pending = null;
  const schedule = (root) => {
    if (pending) clearTimeout(pending);
    pending = setTimeout(() => {
      pending = null;
      if (shouldRing(root)) {
        lastDingAt = Date.now();
        playPreset(currentSoundKey());
      }
    }, 600);
  };

  const findAssistant = (node) => {
    if (!(node instanceof Element)) return null;
    const SEL = ".chat-group.assistant";
    if (node.matches && node.matches(SEL)) return node;
    if (node.querySelector) {
      const list = node.querySelectorAll ? node.querySelectorAll(SEL) : null;
      if (list && list.length) return list[list.length - 1];
    }
    return null;
  };

  const observer = new MutationObserver((muts) => {
    for (const m of muts) {
      for (const n of m.addedNodes) {
        const root = findAssistant(n);
        if (root) schedule(root);
      }
    }
  });

  // ---------- Floating settings widget ----------
  // Small bell button bottom-right. Click → popover with on/off + sound picker
  // (each row has a Preview button) + only-when-hidden toggle.
  // Set localStorage milly.completionCue.widget = 'off' to suppress.
  const mountWidget = () => {
    if (get("milly.completionCue.widget") === "off") return;
    if (document.getElementById("milly-cue-widget")) return;

    const root = document.createElement("div");
    root.id = "milly-cue-widget";
    root.style.cssText = [
      "position:fixed",
      "right:14px",
      "bottom:14px",
      "z-index:2147483646",
      "font:13px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif",
      "color-scheme:light dark",
    ].join(";");

    const btn = document.createElement("button");
    btn.type = "button";
    btn.title = "Completion sound (echo)";
    btn.setAttribute("aria-label", "Completion sound settings");
    btn.textContent = "🔔";
    btn.style.cssText = [
      "all:unset",
      "cursor:pointer",
      "width:36px",
      "height:36px",
      "border-radius:50%",
      "display:flex",
      "align-items:center",
      "justify-content:center",
      "font-size:18px",
      "background:rgba(0,0,0,0.55)",
      "color:#fff",
      "box-shadow:0 2px 6px rgba(0,0,0,0.25)",
      "opacity:0.55",
      "transition:opacity 120ms ease",
    ].join(";");
    btn.addEventListener("mouseenter", () => { btn.style.opacity = "1"; });
    btn.addEventListener("mouseleave", () => { btn.style.opacity = panel.hidden ? "0.55" : "1"; });

    const panel = document.createElement("div");
    panel.hidden = true;
    panel.style.cssText = [
      "position:absolute",
      "right:0",
      "bottom:44px",
      "min-width:260px",
      "padding:12px 14px",
      "background:rgba(28,28,30,0.96)",
      "color:#f5f5f7",
      "border-radius:10px",
      "box-shadow:0 6px 24px rgba(0,0,0,0.35)",
      "backdrop-filter:blur(8px)",
      "-webkit-backdrop-filter:blur(8px)",
    ].join(";");

    const renderPanel = () => {
      const enabled = get("milly.completionCue") !== "off";
      const onlyHidden = get("milly.completionCue.onlyHidden") === "on";
      const sound = currentSoundKey();

      panel.innerHTML = "";

      const title = document.createElement("div");
      title.textContent = "Completion sound";
      title.style.cssText = "font-weight:600;margin-bottom:8px;font-size:13px;";
      panel.appendChild(title);

      // Enable toggle
      const enableRow = document.createElement("label");
      enableRow.style.cssText = "display:flex;align-items:center;gap:8px;margin-bottom:6px;cursor:pointer;";
      const enableCb = document.createElement("input");
      enableCb.type = "checkbox";
      enableCb.checked = enabled;
      enableCb.addEventListener("change", () => {
        if (enableCb.checked) del("milly.completionCue");
        else set("milly.completionCue", "off");
        renderPanel();
      });
      const enableTxt = document.createElement("span");
      enableTxt.textContent = "Enabled";
      enableRow.append(enableCb, enableTxt);
      panel.appendChild(enableRow);

      // Only when hidden
      const hidRow = document.createElement("label");
      hidRow.style.cssText = "display:flex;align-items:center;gap:8px;margin-bottom:10px;cursor:pointer;opacity:" + (enabled ? "1" : "0.5") + ";";
      const hidCb = document.createElement("input");
      hidCb.type = "checkbox";
      hidCb.checked = onlyHidden;
      hidCb.disabled = !enabled;
      hidCb.addEventListener("change", () => {
        if (hidCb.checked) set("milly.completionCue.onlyHidden", "on");
        else del("milly.completionCue.onlyHidden");
        renderPanel();
      });
      const hidTxt = document.createElement("span");
      hidTxt.textContent = "Only when tab is hidden";
      hidRow.append(hidCb, hidTxt);
      panel.appendChild(hidRow);

      // Make the popover scrollable if presets grow.
      panel.style.maxHeight = "min(70vh, 520px)";
      panel.style.overflowY = "auto";

      const soundsTitle = document.createElement("div");
      soundsTitle.style.cssText = "font-size:11px;text-transform:uppercase;letter-spacing:0.04em;opacity:0.6;margin-bottom:6px;";
      panel.appendChild(soundsTitle);

      // Preset rows, grouped by `group` with section headers.
      const groupsOrder = [];
      const grouped = {};
      SOUNDS.forEach((preset) => {
        const g = preset.group || "Other";
        if (!grouped[g]) { grouped[g] = []; groupsOrder.push(g); }
        grouped[g].push(preset);
      });

      groupsOrder.forEach((gName, gi) => {
        // Section header (re-style the first one to look like the existing
        // "Sound" header; subsequent groups get a slim divider above).
        if (gi === 0) {
          soundsTitle.textContent = gName;
        } else {
          const sep = document.createElement("div");
          sep.textContent = gName;
          sep.style.cssText = "font-size:11px;text-transform:uppercase;letter-spacing:0.04em;opacity:0.6;margin:10px 0 6px;padding-top:8px;border-top:1px solid rgba(255,255,255,0.08);";
          panel.appendChild(sep);
        }

        grouped[gName].forEach((preset) => {
          const row = document.createElement("div");
          row.style.cssText = "display:flex;align-items:center;gap:8px;margin:4px 0;opacity:" + (enabled ? "1" : "0.5") + ";";

          const radio = document.createElement("input");
          radio.type = "radio";
          radio.name = "milly-cue-sound";
          radio.value = preset.key;
          radio.checked = sound === preset.key;
          radio.disabled = !enabled;
          radio.addEventListener("change", () => {
            if (radio.checked) {
              if (preset.key === DEFAULT_SOUND) del("milly.completionCue.sound");
              else set("milly.completionCue.sound", preset.key);
              renderPanel();
            }
          });

          const label = document.createElement("label");
          label.style.cssText = "flex:1;cursor:" + (enabled ? "pointer" : "default") + ";";
          label.textContent = preset.label;
          label.addEventListener("click", () => { if (enabled) radio.click(); });

          const preview = document.createElement("button");
          preview.type = "button";
          preview.textContent = "Preview";
          preview.style.cssText = [
            "all:unset",
            "padding:3px 10px",
            "border-radius:6px",
            "background:rgba(255,255,255,0.12)",
            "font-size:12px",
            "cursor:pointer",
          ].join(";");
          preview.addEventListener("click", (e) => {
            e.stopPropagation();
            playPreset(preset.key);
          });

          row.append(radio, label, preview);
          panel.appendChild(row);
        });
      });

      // Footer hint
      const foot = document.createElement("div");
      foot.style.cssText = "margin-top:10px;font-size:11px;opacity:0.55;line-height:1.4;";
      foot.textContent = "Hide this button: localStorage milly.completionCue.widget = off";
      panel.appendChild(foot);
    };

    const togglePanel = () => {
      panel.hidden = !panel.hidden;
      btn.style.opacity = panel.hidden ? "0.55" : "1";
      if (!panel.hidden) renderPanel();
    };
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      ensureCtx();   // count as a user gesture for AudioContext
      togglePanel();
    });

    document.addEventListener("click", (e) => {
      if (panel.hidden) return;
      if (root.contains(e.target)) return;
      panel.hidden = true;
      btn.style.opacity = "0.55";
    }, true);

    root.append(panel, btn);
    document.body.appendChild(root);
  };

  // ---------- Boot ----------
  const start = () => {
    if (!document.body) {
      requestAnimationFrame(start);
      return;
    }
    observer.observe(document.body, { subtree: true, childList: true });
    mountWidget();
  };
  start();

  // DevTools convenience hooks (kept for backwards compat).
  try {
    window.__milly_cue_sounds__ = SOUNDS.map((s) => s.key);
    window.__milly_cue_preview__ = (name) => playPreset(name);
  } catch (_) { /* ignore */ }
})();
