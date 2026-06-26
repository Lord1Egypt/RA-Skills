(() => {
  const OVERLAY_RUNTIME_ENABLED = true;
  const CANVAS_ID = 'oc-cyber-canvas-layer';
  const SCRIPT_FLAG = '__ocCyberHudBooted';
  const HUD_ENABLED = true;
  const AVATAR_PATCHING_ENABLED = true;
  const HEADER_SYNC_ENABLED = true;
  const QUOTA_BADGE_ENABLED = false;
  const SESSION_PICKER_FALLBACK_ENABLED = false;
  const LAYOUT_SYNC_ENABLED = true;
  const AVATAR_URL = '/assets/avatar2.png?v=2026-05-17b';
  const TOOL_AVATAR_URL = '/assets/avatar1.png?v=2026-05-29d';
  const HISTORY_AVATAR_URL = '/assets/history-avatar.png?v=2026-05-29d';
  const TOOL_CONTENT_SELECTOR = '.chat-tool-msg-summary, .chat-tool-msg-collapse, .chat-tool-card';
  const NORMALIZE_MESSAGE_TIMELINE = false;
  if (!OVERLAY_RUNTIME_ENABLED) return;
  if (window[SCRIPT_FLAG]) return;
  window[SCRIPT_FLAG] = true;

  let quotaAuthStatusCache = null;
  let quotaAuthStatusUpdatedAt = 0;
  let quotaAuthStatusPromise = null;
  let raf = 0;
  let canvas = null;
  let ctx = null;
  let host = null;
  let dpr = Math.min(window.devicePixelRatio || 1, 2);
  let width = 0;
  let height = 0;
  let particles = [];
  let lastTs = 0;
  let layoutSyncScheduled = false;
  let footerMetricsObserver = null;
  const observedFooterTargets = new WeakSet();

  function clearCanvasHost() {
    if (canvas && canvas.isConnected) {
      canvas.remove();
    }
    canvas = null;
    ctx = null;
    host = null;
    width = 0;
    height = 0;
  }

  function pickHost() {
    if (!HUD_ENABLED) return null;
    return (
      document.querySelector('.shell--chat .content.content--chat:has(> .content-header):has(> section.card.chat)') ||
      document.querySelector('.shell--chat .content.content--chat:has(section.card.chat)')
    );
  }

  function makeParticles() {
    const count = Math.max(18, Math.min(34, Math.round(width / 70)));
    particles = Array.from({ length: count }, (_, i) => ({
      x: Math.random() * width,
      y: Math.random() * height,
      r: 0.8 + Math.random() * 2.1,
      vx: (Math.random() - 0.5) * 0.045,
      vy: -0.02 - Math.random() * 0.07,
      hue: i % 3 === 0 ? 'cyan' : (i % 3 === 1 ? 'pink' : 'blue'),
      alpha: 0.12 + Math.random() * 0.24,
    }));
  }

  function observeFooterTarget(target) {
    if (!footerMetricsObserver || !target || observedFooterTargets.has(target)) return;
    footerMetricsObserver.observe(target);
    observedFooterTargets.add(target);
  }

  function ensureFooterMetricsObserver() {
    if (footerMetricsObserver || typeof ResizeObserver !== 'function') return;
    footerMetricsObserver = new ResizeObserver(() => {
      scheduleLayoutSync();
    });
  }

  function scheduleLayoutSync() {
    if (layoutSyncScheduled) return;
    layoutSyncScheduled = true;
    requestAnimationFrame(() => {
      layoutSyncScheduled = false;
      syncChatLayoutMetrics();
    });
  }

  function setImportantStyleVar(element, name, value) {
    if (
      element.style.getPropertyValue(name) === value &&
      element.style.getPropertyPriority(name) === 'important'
    ) {
      return;
    }
    element.style.setProperty(name, value, 'important');
  }

  function syncChatLayoutMetrics() {
    if (!LAYOUT_SYNC_ENABLED) return;

    const shell = document.querySelector('.shell--chat');
    const card = shell && shell.querySelector('section.card.chat');
    const composer = card && queryChatComposer(card);
    if (!shell || !card || !composer) return;

    ensureFooterMetricsObserver();
    observeFooterTarget(card);
    observeFooterTarget(composer);

    const statusStack = composer.querySelector('.agent-chat__composer-status-stack');
    const workspaceRail = card.querySelector('.chat-workspace-rail') || shell.querySelector('.chat-workspace-rail');
    observeFooterTarget(statusStack);
    observeFooterTarget(workspaceRail);

    const cardRect = card.getBoundingClientRect();
    const composerRect = composer.getBoundingClientRect();
    if (!cardRect.height || !composerRect.height) return;

    const composerBottom = isChatMainComposer(composer)
      ? chatMainComposerBottom()
      : Math.max(8, Math.round(cardRect.bottom - composerRect.bottom));
    const footerStackHeight = isChatMainComposer(composer)
      ? Math.max(74, Math.round(composerRect.height + composerBottom + 6))
      : Math.max(74, Math.round(cardRect.bottom - composerRect.top + 6));

    setImportantStyleVar(shell, '--oc-chat-footer-stack-height', `${footerStackHeight}px`);
    setImportantStyleVar(shell, '--oc-chat-composer-reserve', `${footerStackHeight}px`);
    setImportantStyleVar(shell, '--oc-chat-composer-bottom', `${composerBottom}px`);
  }

  function queryChatComposer(card) {
    if (!(card instanceof Element)) return null;
    return (
      card.querySelector('.chat-main > .agent-chat__input') ||
      card.querySelector(':scope > .agent-chat__input') ||
      card.querySelector('.agent-chat__input')
    );
  }

  function isChatMainComposer(composer) {
    return composer instanceof Element && composer.parentElement?.matches('.chat-main');
  }

  function chatMainComposerBottom() {
    return window.matchMedia('(max-width: 768px)').matches ? 10 : 14;
  }

  function ensureCanvas() {
    const nextHost = pickHost();
    if (!nextHost) {
      clearCanvasHost();
      return false;
    }
    if (host !== nextHost || !canvas || !canvas.isConnected) {
      if (host !== nextHost) {
        clearCanvasHost();
      }
      host = nextHost;
      canvas = document.createElement('canvas');
      canvas.id = CANVAS_ID;
      canvas.setAttribute('aria-hidden', 'true');
      host.prepend(canvas);
      ctx = canvas.getContext('2d');
      resize();
      makeParticles();
    }
    return true;
  }

  function resize() {
    if (!host || !canvas) return;
    const rect = host.getBoundingClientRect();
    width = Math.max(1, Math.round(rect.width));
    height = Math.max(1, Math.round(rect.height));
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function strokeHudCorners(t) {
    const pad = 18;
    const len = Math.min(128, Math.max(76, width * 0.11));
    const topGlow = 0.24 + Math.sin(t * 0.0018) * 0.06;
    const cyan = `rgba(122,232,255,${topGlow.toFixed(3)})`;
    const pink = `rgba(255,132,220,${(topGlow * 0.86).toFixed(3)})`;

    ctx.lineWidth = 2.2;
    ctx.strokeStyle = cyan;
    ctx.beginPath();
    ctx.moveTo(pad, pad + len); ctx.lineTo(pad, pad); ctx.lineTo(pad + len, pad);
    ctx.moveTo(width - pad - len, pad); ctx.lineTo(width - pad, pad); ctx.lineTo(width - pad, pad + len);
    ctx.stroke();

    ctx.strokeStyle = pink;
    ctx.beginPath();
    ctx.moveTo(pad, height - pad - len); ctx.lineTo(pad, height - pad); ctx.lineTo(pad + len, height - pad);
    ctx.moveTo(width - pad - len, height - pad); ctx.lineTo(width - pad, height - pad); ctx.lineTo(width - pad, height - pad - len);
    ctx.stroke();

    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(122,232,255,0.18)';
    ctx.beginPath();
    ctx.moveTo(pad + 10, pad + len * 0.58); ctx.lineTo(pad + 34, pad + len * 0.58);
    ctx.moveTo(width - pad - 34, pad + len * 0.42); ctx.lineTo(width - pad - 10, pad + len * 0.42);
    ctx.moveTo(pad + 10, height - pad - len * 0.42); ctx.lineTo(pad + 34, height - pad - len * 0.42);
    ctx.moveTo(width - pad - 34, height - pad - len * 0.58); ctx.lineTo(width - pad - 10, height - pad - len * 0.58);
    ctx.stroke();
  }

  function drawScanline(t) {
    const y = ((t * 0.045) % (height + 120)) - 60;
    const g = ctx.createLinearGradient(0, y - 24, 0, y + 24);
    g.addColorStop(0, 'rgba(80,220,255,0)');
    g.addColorStop(0.48, 'rgba(80,220,255,0.12)');
    g.addColorStop(0.52, 'rgba(255,132,220,0.08)');
    g.addColorStop(1, 'rgba(255,132,220,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, y - 24, width, 48);
  }

  function drawGrid(t) {
    const step = 42;
    const offsetX = (t * 0.01) % step;
    const offsetY = (t * 0.006) % step;
    ctx.lineWidth = 1;
    for (let x = -step; x < width + step; x += step) {
      ctx.strokeStyle = 'rgba(90,210,255,0.06)';
      ctx.beginPath();
      ctx.moveTo(x + offsetX, 0);
      ctx.lineTo(x + offsetX, height);
      ctx.stroke();
    }
    for (let y = -step; y < height + step; y += step) {
      ctx.strokeStyle = 'rgba(255,120,215,0.038)';
      ctx.beginPath();
      ctx.moveTo(0, y + offsetY);
      ctx.lineTo(width, y + offsetY);
      ctx.stroke();
    }
  }

  function drawParticles(t, dt) {
    for (const p of particles) {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      if (p.x < -20) p.x = width + 20;
      if (p.x > width + 20) p.x = -20;
      if (p.y < -20) {
        p.y = height + 20;
        p.x = Math.random() * width;
      }
      const color = p.hue === 'cyan'
        ? `rgba(130,236,255,${p.alpha})`
        : p.hue === 'pink'
          ? `rgba(255,146,224,${p.alpha})`
          : `rgba(108,170,255,${p.alpha * 0.9})`;
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function drawOrbitArcs(t) {
    const cx = width - 118;
    const cy = 164;
    ctx.lineWidth = 1.8;
    ctx.strokeStyle = 'rgba(118,228,255,0.22)';
    ctx.beginPath();
    ctx.arc(cx, cy, 52, Math.PI * 0.12, Math.PI * 1.62);
    ctx.stroke();
    ctx.strokeStyle = 'rgba(255,136,220,0.18)';
    ctx.beginPath();
    ctx.arc(cx, cy, 74, Math.PI * 1.08, Math.PI * 0.18, true);
    ctx.stroke();

    ctx.strokeStyle = 'rgba(122,232,255,0.12)';
    ctx.lineWidth = 1;
    for (let i = 0; i < 7; i++) {
      const a = -Math.PI * 0.25 + i * 0.24;
      const x1 = cx + Math.cos(a) * 82;
      const y1 = cy + Math.sin(a) * 82;
      const x2 = cx + Math.cos(a) * 92;
      const y2 = cy + Math.sin(a) * 92;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    }

    const ang = (t * 0.0011) % (Math.PI * 2);
    const px = cx + Math.cos(ang) * 74;
    const py = cy + Math.sin(ang) * 74;
    ctx.fillStyle = 'rgba(255,180,232,0.72)';
    ctx.beginPath();
    ctx.arc(px, py, 3, 0, Math.PI * 2);
    ctx.fill();
  }

  function drawVerticalDataStrips(t) {
    const left = 28;
    const baseY = 154;
    const h = Math.min(250, Math.max(170, height * 0.32));
    for (let i = 0; i < 4; i++) {
      const x = left + i * 18;
      const pulse = 0.24 + 0.11 * Math.sin(t * 0.002 + i * 0.7);
      ctx.fillStyle = `rgba(120,228,255,${pulse})`;
      ctx.fillRect(x, baseY, 3, h);
      ctx.fillStyle = `rgba(255,140,220,${pulse * 0.72})`;
      ctx.fillRect(x + 7, baseY + 28, 2, h - 46);
      ctx.fillStyle = `rgba(170,236,255,${Math.min(0.9, pulse + 0.18)})`;
      ctx.fillRect(x - 3, baseY + (i * 22) % Math.max(26, h - 20), 10, 2);
    }

    ctx.strokeStyle = 'rgba(122,232,255,0.22)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(left - 10, baseY - 14);
    ctx.lineTo(left + 72, baseY - 14);
    ctx.moveTo(left - 10, baseY + h + 12);
    ctx.lineTo(left + 72, baseY + h + 12);
    ctx.stroke();
  }

  function roundRectPath(x, y, w, h, r) {
    const rr = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + rr, y);
    ctx.arcTo(x + w, y, x + w, y + h, rr);
    ctx.arcTo(x + w, y + h, x, y + h, rr);
    ctx.arcTo(x, y + h, x, y, rr);
    ctx.arcTo(x, y, x + w, y, rr);
    ctx.closePath();
  }

  function drawCenterHoloPanels(t) {
    const screenX = width * 0.49;
    const screenY = height * 0.34;
    const screenW = Math.min(250, Math.max(170, width * 0.19));
    const screenH = Math.min(148, Math.max(96, height * 0.14));
    const floatY = Math.sin(t * 0.0013) * 4;

    ctx.save();
    ctx.translate(screenX, screenY + floatY);

    const panelGlow = 0.16 + Math.sin(t * 0.0018) * 0.04;
    ctx.shadowBlur = 18;
    ctx.shadowColor = 'rgba(120,228,255,0.18)';
    ctx.strokeStyle = `rgba(122,232,255,${(0.32 + panelGlow).toFixed(3)})`;
    ctx.fillStyle = 'rgba(10,22,34,0.10)';
    ctx.lineWidth = 1.2;
    roundRectPath(0, 0, screenW, screenH, 10);
    ctx.fill();
    ctx.stroke();

    ctx.shadowBlur = 0;
    ctx.strokeStyle = 'rgba(255,150,224,0.22)';
    ctx.beginPath();
    ctx.moveTo(16, 18); ctx.lineTo(52, 18);
    ctx.moveTo(screenW - 52, screenH - 18); ctx.lineTo(screenW - 16, screenH - 18);
    ctx.stroke();

    const chartBaseY = screenH - 28;
    const pts = 8;
    const gap = (screenW - 40) / (pts - 1);
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'rgba(122,232,255,0.72)';
    ctx.beginPath();
    for (let i = 0; i < pts; i++) {
      const x = 20 + i * gap;
      const y = chartBaseY - (18 + Math.sin(t * 0.002 + i * 0.65) * 14 + (i % 3) * 6);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();

    ctx.lineTo(screenW - 20, chartBaseY);
    ctx.lineTo(20, chartBaseY);
    ctx.closePath();
    const g = ctx.createLinearGradient(0, 10, 0, chartBaseY);
    g.addColorStop(0, 'rgba(122,232,255,0.12)');
    g.addColorStop(1, 'rgba(122,232,255,0.00)');
    ctx.fillStyle = g;
    ctx.fill();

    for (let i = 0; i < 4; i++) {
      const bx = screenW + 18;
      const by = 8 + i * 18;
      const bw = 46 + i * 10;
      const alpha = 0.16 + Math.sin(t * 0.0022 + i) * 0.05;
      ctx.fillStyle = `rgba(255,146,224,${alpha.toFixed(3)})`;
      ctx.fillRect(bx, by, bw, 5);
      ctx.strokeStyle = 'rgba(255,146,224,0.24)';
      ctx.strokeRect(bx, by, bw, 5);
    }

    const ringX = screenW + 72;
    const ringY = screenH - 10;
    ctx.strokeStyle = 'rgba(122,232,255,0.24)';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.arc(ringX, ringY, 24, Math.PI * 0.15, Math.PI * 1.75);
    ctx.stroke();
    ctx.strokeStyle = 'rgba(255,146,224,0.22)';
    ctx.beginPath();
    ctx.arc(ringX, ringY, 34, Math.PI * 1.1, Math.PI * 0.28, true);
    ctx.stroke();
    const a = (t * 0.0016) % (Math.PI * 2);
    ctx.fillStyle = 'rgba(122,232,255,0.82)';
    ctx.beginPath();
    ctx.arc(ringX + Math.cos(a) * 34, ringY + Math.sin(a) * 34, 2.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  }

  function isAssistantAvatarImage(node) {
    if (!(node instanceof HTMLImageElement)) return false;
    if (node.matches('img.chat-avatar.assistant')) return true;
    return node.matches('img.chat-avatar') && !!node.closest('.chat-group.assistant');
  }

  function groupHasToolContent(node) {
    return node instanceof Element && node.matches('.chat-group.assistant') && !!node.querySelector(TOOL_CONTENT_SELECTOR);
  }

  function avatarUrlFor(node) {
    const group = node.closest('.chat-group.assistant');
    return groupHasToolContent(group) ? TOOL_AVATAR_URL : AVATAR_URL;
  }

  function patchAvatar(node) {
    if (!isAssistantAvatarImage(node)) return;
    const nextUrl = avatarUrlFor(node);
    if (node.getAttribute('src') !== nextUrl) {
      node.removeAttribute('srcset');
      node.setAttribute('src', nextUrl);
    }
    // Let the theme CSS own portrait cropping so JS does not carry stale inline overrides.
    node.style.removeProperty('object-fit');
    node.style.removeProperty('object-position');
    node.dataset.ocAvatarPatched = nextUrl === TOOL_AVATAR_URL ? 'tool' : 'assistant';
  }

  function avatarFillUrlFor(node) {
    if (!(node instanceof Element)) return null;
    if (node.matches('.chat-group.tool .chat-avatar, .chat-avatar.tool')) return TOOL_AVATAR_URL;
    if (node.matches('.chat-group.other .chat-avatar')) return HISTORY_AVATAR_URL;
    return null;
  }

  function patchDecorativeAvatar(node) {
    if (!(node instanceof Element)) return;
    const nextUrl = avatarFillUrlFor(node);
    if (!nextUrl) return;

    if (node instanceof HTMLImageElement) {
      if (node.getAttribute('src') !== nextUrl) {
        node.removeAttribute('srcset');
        node.setAttribute('src', nextUrl);
      }
      node.dataset.ocAvatarPatched = nextUrl === TOOL_AVATAR_URL ? 'tool' : 'helper';
      return;
    }

    let fill = node.querySelector(':scope > .oc-theme-avatar-raster');
    if (!(fill instanceof HTMLImageElement)) {
      fill = document.createElement('img');
      fill.className = 'oc-theme-avatar-raster';
      fill.alt = '';
      fill.setAttribute('aria-hidden', 'true');
      node.appendChild(fill);
    }
    if (fill.getAttribute('src') !== nextUrl) {
      fill.removeAttribute('srcset');
      fill.setAttribute('src', nextUrl);
    }
    node.dataset.ocAvatarPatched = nextUrl === TOOL_AVATAR_URL ? 'tool' : 'helper';
  }

  function syncAssistantAvatars(root = document) {
    if (root instanceof HTMLImageElement) {
      patchAvatar(root);
      return;
    }
    if (!(root instanceof Document || root instanceof Element)) return;
    root.querySelectorAll('img').forEach(patchAvatar);
  }

  function syncDecorativeAvatars(root = document) {
    if (root instanceof Element) {
      patchDecorativeAvatar(root);
      if (root.matches('.chat-group.tool, .chat-group.other')) {
        const avatar = root.querySelector('.chat-avatar');
        if (avatar) patchDecorativeAvatar(avatar);
      }
    }
    if (!(root instanceof Document || root instanceof Element)) return;
    root
      .querySelectorAll('.chat-group.tool .chat-avatar, .chat-avatar.tool, .chat-group.other .chat-avatar')
      .forEach(patchDecorativeAvatar);
  }

  function syncChatHeaderControls(root = document) {
    if (!(root instanceof Document || root instanceof Element)) return;
    root.querySelectorAll('.shell--chat .content-header').forEach((header) => {
      const notice = header.querySelector('.chat-controls__session-notice');
      const hasNoticeText = !!notice && notice.textContent.trim().length > 0;
      header.dataset.ocHeaderNotice = hasNoticeText ? '1' : '0';
      if (notice) notice.dataset.ocEmpty = hasNoticeText ? '0' : '1';
    });
  }

  function currentChatSessionKey() {
    const url = new URL(window.location.href);
    return url.searchParams.get('session') || '';
  }

  function fallbackSwitchChatSession(nextSessionKey) {
    if (!nextSessionKey || nextSessionKey === currentChatSessionKey()) return;
    const url = new URL(window.location.href);
    url.searchParams.set('session', nextSessionKey);
    window.location.assign(url.toString());
  }

  function sessionOptionAtPoint(clientX, clientY) {
    const options = document.querySelectorAll('[data-chat-session-picker-option][data-session-key]');
    for (const option of options) {
      if (!(option instanceof HTMLElement)) continue;
      const rect = option.getBoundingClientRect();
      if (
        clientX >= rect.left &&
        clientX <= rect.right &&
        clientY >= rect.top &&
        clientY <= rect.bottom
      ) {
        return option;
      }
    }
    return null;
  }

  let pendingSessionPickerPointerIntent = null;
  function markSessionPickerPointerIntent(event) {
    if (event.defaultPrevented || event.button !== 0) return;
    if (!document.activeElement || !document.activeElement.matches('[data-chat-session-picker-search="true"]')) return;
    const target = event.target instanceof Element ? event.target : null;
    const option = (
      target && target.closest('[data-chat-session-picker-option][data-session-key]')
    ) || sessionOptionAtPoint(event.clientX, event.clientY);
    if (!(option instanceof HTMLElement)) return;
    const nextSessionKey = option.dataset.sessionKey || '';
    if (!nextSessionKey || nextSessionKey === currentChatSessionKey()) return;
    const token = { sessionKey: nextSessionKey };
    pendingSessionPickerPointerIntent = token;
    setTimeout(() => {
      if (pendingSessionPickerPointerIntent !== token) return;
      pendingSessionPickerPointerIntent = null;
      const app = document.querySelector('openclaw-app');
      if (!app) return;
      const liveSessionKey = typeof app.sessionKey === 'string' ? app.sessionKey : currentChatSessionKey();
      if (liveSessionKey === nextSessionKey) return;
      fallbackSwitchChatSession(nextSessionKey);
    }, 80);
  }

  function installSessionPickerFallback() {
    if (document.documentElement.dataset.ocSessionPickerFallbackInstalled === '1') return;
    document.documentElement.dataset.ocSessionPickerFallbackInstalled = '1';

    document.addEventListener('pointerdown', (event) => { markSessionPickerPointerIntent(event); }, true);

    document.addEventListener('click', (event) => {
      if (event.defaultPrevented || event.button !== 0) return;
      const target = event.target instanceof Element ? event.target : null;
      const option = (
        target && target.closest('[data-chat-session-picker-option][data-session-key]')
      ) || sessionOptionAtPoint(event.clientX, event.clientY);
      if (!(option instanceof HTMLElement)) return;
      pendingSessionPickerPointerIntent = null;

      const nextSessionKey = option.dataset.sessionKey || '';
      const currentSessionKey = currentChatSessionKey();
      if (!nextSessionKey || nextSessionKey === currentSessionKey) return;

      window.setTimeout(() => {
        const app = document.querySelector('openclaw-app');
        const liveSessionKey = app && typeof app.sessionKey === 'string' ? app.sessionKey : currentChatSessionKey();
        if (liveSessionKey === nextSessionKey) return;
        fallbackSwitchChatSession(nextSessionKey);
      }, 120);
    }, true);
  }

  function normalizeQuotaLabel(label, windowMinutes = null) {
    const raw = String(label || '').trim();
    const lower = raw.toLowerCase();
    if (lower === 'week' || lower === 'weekly') return '周';
    if (lower === '5h' || lower === '5 hr' || lower === '5 hour' || lower === '5 hours') return '5h';
    if (Number.isFinite(windowMinutes)) {
      if (windowMinutes === 300) return '5h';
      if (windowMinutes === 10080) return '周';
      if (windowMinutes > 0 && windowMinutes % 1440 === 0) return `${Math.round(windowMinutes / 1440)}d`;
      if (windowMinutes >= 60 && windowMinutes % 60 === 0) return `${Math.round(windowMinutes / 60)}h`;
      if (windowMinutes > 0) return `${Math.round(windowMinutes)}m`;
    }
    return raw || 'quota';
  }

  function normalizeQuotaResetAt(value) {
    const numeric = Number(value);
    if (!Number.isFinite(numeric) || numeric <= 0) return null;
    if (numeric >= 1e12) return numeric;
    if (numeric >= 1e9) return numeric * 1000;
    return null;
  }

  function normalizedUsageWindows(provider) {
    const windows = Array.isArray(provider?.usage?.windows) ? provider.usage.windows : [];
    return windows
      .map((window) => {
        const windowMinutes = Number(
          window?.windowDurationMins
          ?? window?.windowMinutes
          ?? window?.window_minutes
        );
        const used = Number(window?.usedPercent ?? window?.used_percent);
        if (!Number.isFinite(used)) return null;
        return {
          label: normalizeQuotaLabel(window?.label, windowMinutes),
          remaining: Math.max(0, Math.min(100, Math.round(100 - used))),
          resetAt: normalizeQuotaResetAt(window?.resetAt ?? window?.resetsAt ?? window?.resetsAtMs ?? window?.resets_at),
          windowMinutes: Number.isFinite(windowMinutes) ? windowMinutes : null,
        };
      })
      .filter(Boolean)
      .sort((a, b) => {
        const order = (window) => {
          if (window.label === '5h' || window.windowMinutes === 300) return 0;
          if (window.label === '周' || window.windowMinutes === 10080) return 1;
          return 2;
        };
        return order(a) - order(b)
          || (a.windowMinutes ?? Number.MAX_SAFE_INTEGER) - (b.windowMinutes ?? Number.MAX_SAFE_INTEGER)
          || a.label.localeCompare(b.label);
      });
  }

  function scoreQuotaProvider(provider, app) {
    const id = String(provider?.provider || provider?.id || '').toLowerCase();
    const displayName = String(provider?.displayName || provider?.name || '').toLowerCase();
    const model = String(app?.chatModel || app?.chatModelSelected || '').toLowerCase();
    let score = 0;
    if (id.includes('codex') || displayName.includes('codex')) score += 100;
    if (id.includes('openai') || displayName.includes('openai')) score += 40;
    if (model.includes('codex') || model.includes('gpt-5')) score += 10;
    return score;
  }

  function hasUsableQuotaProviders(providers) {
    return providers.some((provider) => normalizedUsageWindows(provider).length > 0);
  }

  async function resolveQuotaAuthStatus(forceRefresh = false) {
    const app = document.querySelector('openclaw-app');
    const liveProviders = app && Array.isArray(app.modelAuthStatusResult?.providers)
      ? app.modelAuthStatusResult.providers
      : [];
    if (hasUsableQuotaProviders(liveProviders)) {
      quotaAuthStatusCache = { ts: Date.now(), providers: liveProviders };
      quotaAuthStatusUpdatedAt = Date.now();
      return quotaAuthStatusCache;
    }

    if (!app?.client || !app.connected) return quotaAuthStatusCache;

    const now = Date.now();
    const cacheFresh = quotaAuthStatusCache && (now - quotaAuthStatusUpdatedAt) < 30_000;
    if (!forceRefresh && cacheFresh) return quotaAuthStatusCache;
    if (quotaAuthStatusPromise) return quotaAuthStatusPromise;

    quotaAuthStatusPromise = app.client.request('models.authStatus', forceRefresh ? { refresh: true } : {})
      .then((result) => {
        if (result && Array.isArray(result.providers)) {
          quotaAuthStatusCache = result;
          quotaAuthStatusUpdatedAt = Date.now();
        }
        return quotaAuthStatusCache;
      })
      .catch(() => quotaAuthStatusCache)
      .finally(() => {
        quotaAuthStatusPromise = null;
      });

    return quotaAuthStatusPromise;
  }

  function codexQuotaSnapshot(authStatus = null) {
    const app = document.querySelector('openclaw-app');
    const providers = authStatus && Array.isArray(authStatus.providers)
      ? authStatus.providers
      : app && Array.isArray(app.modelAuthStatusResult?.providers)
        ? app.modelAuthStatusResult.providers
      : [];
    const best = providers
      .map((provider) => ({ provider, windows: normalizedUsageWindows(provider) }))
      .filter((entry) => entry.windows.length > 0)
      .sort((a, b) => {
        const scoreDiff = scoreQuotaProvider(b.provider, app) - scoreQuotaProvider(a.provider, app);
        if (scoreDiff !== 0) return scoreDiff;
        const remainingA = Math.min(...a.windows.map((window) => window.remaining));
        const remainingB = Math.min(...b.windows.map((window) => window.remaining));
        return remainingA - remainingB;
      })[0];
    if (!best) return null;
    return {
      providerLabel: String(best.provider?.displayName || best.provider?.name || best.provider?.provider || best.provider?.id || 'Codex'),
      windows: best.windows,
    };
  }

  function quotaBadgeSeverity(windows) {
    const remaining = Math.min(...windows.map((window) => window.remaining));
    if (remaining <= 10) return 'danger';
    if (remaining <= 25) return 'warn';
    return 'ok';
  }

  function findQuotaBadgeHost(root = document) {
    if (!(root instanceof Document || root instanceof Element)) return null;
    return (
      root.querySelector('.shell--chat .dashboard-header__actions')
      || root.querySelector('.shell--chat .dashboard-header')
      || root.querySelector('.shell--chat .page-meta')
      || document.querySelector('.shell--chat .dashboard-header__actions')
      || document.querySelector('.shell--chat .dashboard-header')
      || document.querySelector('.shell--chat .page-meta')
    );
  }

  function ensureCustomQuotaBadge(root = document) {
    if (!(root instanceof Document || root instanceof Element)) return null;
    const host = findQuotaBadgeHost(root);
    if (!(host instanceof Element)) return null;

    let badge = host.querySelector('.chat-controls__quota[data-oc-quota-badge="true"]');
    if (!(badge instanceof HTMLElement)) {
      badge = document.createElement('div');
      badge.className = 'chat-controls__quota chat-controls__quota--topbar';
      badge.dataset.ocQuotaBadge = 'true';
      badge.setAttribute('role', 'status');

      const label = document.createElement('span');
      label.className = 'chat-controls__quota-label';
      label.textContent = 'Codex';

      const value = document.createElement('span');
      value.className = 'chat-controls__quota-value';

      badge.appendChild(label);
      badge.appendChild(value);
      host.appendChild(badge);
    }
    return badge;
  }

  function removeCustomQuotaBadges(root = document) {
    if (!(root instanceof Document || root instanceof Element)) return;
    root.querySelectorAll('.chat-controls__quota[data-oc-quota-badge="true"]').forEach((badge) => {
      badge.remove();
    });
  }

  async function syncCodexQuotaBadge(root = document, options = {}) {
    if (!QUOTA_BADGE_ENABLED) return;

    if (!(root instanceof Document || root instanceof Element)) return;
    const authStatus = await resolveQuotaAuthStatus(options.forceRefresh === true);
    const snapshot = codexQuotaSnapshot(authStatus);
    if (!snapshot || snapshot.windows.length === 0) {
      removeCustomQuotaBadges(root);
      return;
    }

    const windows = snapshot.windows;
    const compact = windows.map((window) => `${window.label} ${window.remaining}`).join(' / ');
    const detailed = windows
      .map((window) => `${window.label}: ${window.remaining}% left${window.resetAt ? `, resets ${new Date(window.resetAt).toLocaleString()}` : ''}`)
      .join(' · ');
    const builtInBadges = Array.from(
      root.querySelectorAll('.shell--chat .chat-controls__quota:not([data-oc-quota-badge="true"])')
    );
    const badges = builtInBadges.length > 0
      ? builtInBadges
      : [ensureCustomQuotaBadge(root)].filter(Boolean);

    if (builtInBadges.length > 0) removeCustomQuotaBadges(root);

    badges.forEach((badge) => {
      const value = badge.querySelector('.chat-controls__quota-value');
      if (!value) return;
      badge.classList.remove('chat-controls__quota--ok', 'chat-controls__quota--warn', 'chat-controls__quota--danger');
      badge.classList.add(`chat-controls__quota--${quotaBadgeSeverity(windows)}`);
      badge.dataset.ocQuotaExpanded = '1';
      badge.setAttribute('title', `${snapshot.providerLabel} usage: ${detailed}`);
      badge.setAttribute('aria-label', `${snapshot.providerLabel} usage: ${detailed}`);
      if (value.textContent.trim() !== compact) value.textContent = compact;
    });
  }

  function messageTimestamp(message) {
    return message && Number.isFinite(message.timestamp) ? message.timestamp : null;
  }

  function messageSequence(message) {
    const seq = message && message.__openclaw && message.__openclaw.seq;
    return Number.isFinite(seq) ? seq : null;
  }

  function contentBlocks(message) {
    return Array.isArray(message && message.content) ? message.content : [];
  }

  function isAssistantToolMessage(message) {
    return String(message && message.role || '').toLowerCase() === 'assistant'
      && contentBlocks(message).some((block) => {
        const type = String(block && block.type || '').toLowerCase();
        return type === 'toolcall' || type === 'toolresult';
      });
  }

  function messageSortRank(message) {
    const role = String(message && message.role || '').toLowerCase();
    if (role === 'user') return 0;
    if (role === 'assistant') return isAssistantToolMessage(message) ? 1 : 3;
    if (role === 'toolresult') return 2;
    if (role === 'system') return 4;
    return 5;
  }

  function compareMessages(a, b) {
    const seqA = messageSequence(a);
    const seqB = messageSequence(b);
    if (seqA != null && seqB != null && seqA !== seqB) {
      return seqA - seqB;
    }

    const tsA = messageTimestamp(a);
    const tsB = messageTimestamp(b);
    if (tsA == null && tsB == null) return 0;
    if (tsA == null) return 1;
    if (tsB == null) return -1;
    if (tsA !== tsB) return tsA - tsB;
    return messageSortRank(a) - messageSortRank(b);
  }

  function stableSortMessages(messages) {
    return messages
      .map((message, index) => ({ message, index }))
      .sort((a, b) => compareMessages(a.message, b.message) || a.index - b.index)
      .map(({ message }) => message);
  }

  function normalizeAssignedTimestamps(messages) {
    let changed = false;
    let lastAssignedTs = null;

    messages.forEach((message, index) => {
      if (!message || typeof message !== 'object') return;

      const originalTs = messageTimestamp(message);
      let assignedTs = originalTs;

      if (assignedTs == null) {
        assignedTs = lastAssignedTs == null ? Date.now() + index : lastAssignedTs + 1;
      } else if (lastAssignedTs != null && assignedTs <= lastAssignedTs) {
        assignedTs = lastAssignedTs + 1;
      }

      if (assignedTs !== originalTs) {
        if (!Object.prototype.hasOwnProperty.call(message, '__ocOriginalTimestamp') && originalTs != null) {
          message.__ocOriginalTimestamp = originalTs;
        }
        message.timestamp = assignedTs;
        changed = true;
      }

      lastAssignedTs = assignedTs;
    });

    return changed;
  }

  function normalizeMessageTimeline(messages) {
    const normalized = stableSortMessages(messages);
    const orderChanged = !sameMessageOrder(messages, normalized);
    const timestampChanged = normalizeAssignedTimestamps(normalized);

    return { messages: normalized, changed: orderChanged || timestampChanged };
  }

  function sameMessageOrder(current, next) {
    if (!Array.isArray(current) || current.length !== next.length) return false;
    return current.every((message, index) => message === next[index]);
  }

  function normalizeCombinedMessageTimelines(chatMessages, chatToolMessages) {
    const combined = [];

    chatMessages.forEach((message, index) => {
      combined.push({ source: 'chat', message, index });
    });
    chatToolMessages.forEach((message, index) => {
      combined.push({ source: 'tool', message, index });
    });

    const normalized = combined
      .map((entry, combinedIndex) => ({ ...entry, combinedIndex }))
      .sort((a, b) => compareMessages(a.message, b.message) || a.combinedIndex - b.combinedIndex);

    const nextChatMessages = [];
    const nextChatToolMessages = [];

    normalized.forEach((entry) => {
      if (entry.source === 'tool') {
        nextChatToolMessages.push(entry.message);
      } else {
        nextChatMessages.push(entry.message);
      }
    });

    const chatOrderChanged = !sameMessageOrder(chatMessages, nextChatMessages);
    const toolOrderChanged = !sameMessageOrder(chatToolMessages, nextChatToolMessages);
    const timestampChanged = normalizeAssignedTimestamps(normalized.map((entry) => entry.message));

    return {
      chatMessages: nextChatMessages,
      chatToolMessages: nextChatToolMessages,
      changed: chatOrderChanged || toolOrderChanged || timestampChanged,
    };
  }

  function normalizeChatMessageOrder(root = document) {
    if (!NORMALIZE_MESSAGE_TIMELINE) return;

    const app = root.querySelector ? root.querySelector('openclaw-app') : document.querySelector('openclaw-app');
    if (!app) return;

    let changed = false;
    const hasChatMessages = Array.isArray(app.chatMessages);
    const hasChatToolMessages = Array.isArray(app.chatToolMessages);

    if (hasChatMessages && hasChatToolMessages && (app.chatMessages.length + app.chatToolMessages.length) > 1) {
      const normalized = normalizeCombinedMessageTimelines(app.chatMessages, app.chatToolMessages);
      if (normalized.changed) {
        app.chatMessages = normalized.chatMessages;
        app.chatToolMessages = normalized.chatToolMessages;
        changed = true;
      }
    } else if (hasChatMessages && app.chatMessages.length > 1) {
      const normalized = normalizeMessageTimeline(app.chatMessages);
      if (normalized.changed) {
        app.chatMessages = normalized.messages;
        changed = true;
      }
    }

    if (!changed && hasChatToolMessages && app.chatToolMessages.length > 1) {
      const normalized = normalizeMessageTimeline(app.chatToolMessages);
      if (normalized.changed) {
        app.chatToolMessages = normalized.messages;
        changed = true;
      }
    }

    if (changed && typeof app.requestUpdate === 'function') {
      app.requestUpdate();
    }
  }

  function render(ts) {
    if (!ensureCanvas()) {
      raf = 0;
      return;
    }
    if (!ctx) return;
    if (!lastTs) lastTs = ts;
    const dt = Math.min(32, ts - lastTs);
    lastTs = ts;

    const rect = host.getBoundingClientRect();
    const nextWidth = Math.max(1, Math.round(rect.width));
    const nextHeight = Math.max(1, Math.round(rect.height));
    if (
      nextWidth !== width ||
      nextHeight !== height ||
      canvas.width !== Math.floor(nextWidth * dpr) ||
      canvas.height !== Math.floor(nextHeight * dpr)
    ) {
      resize();
      makeParticles();
    }

    ctx.clearRect(0, 0, width, height);
    drawGrid(ts);
    drawScanline(ts);
    drawVerticalDataStrips(ts);
    drawOrbitArcs(ts);
    drawCenterHoloPanels(ts);
    drawParticles(ts, dt);
    strokeHudCorners(ts);

    raf = requestAnimationFrame(render);
  }

  function boot() {
    const hasCanvas = ensureCanvas();
    if (AVATAR_PATCHING_ENABLED) {
      syncAssistantAvatars();
      syncDecorativeAvatars();
    }
    if (HEADER_SYNC_ENABLED) syncChatHeaderControls();
    if (QUOTA_BADGE_ENABLED) syncCodexQuotaBadge();
    if (SESSION_PICKER_FALLBACK_ENABLED) installSessionPickerFallback();
    if (NORMALIZE_MESSAGE_TIMELINE) normalizeChatMessageOrder();
    if (LAYOUT_SYNC_ENABLED) syncChatLayoutMetrics();
    if (HUD_ENABLED && hasCanvas && !raf) raf = requestAnimationFrame(render);
  }

  window.addEventListener('resize', () => {
    if (HUD_ENABLED) {
      resize();
      makeParticles();
    }
    if (LAYOUT_SYNC_ENABLED) scheduleLayoutSync();
  }, { passive: true });

  const mo = new MutationObserver((mutations) => {
    const nextHost = pickHost();
    if (!nextHost) {
      clearCanvasHost();
      return;
    }
    if (HUD_ENABLED && (!canvas || !canvas.isConnected || nextHost !== host)) {
      boot();
    }
    for (const mutation of mutations) {
      if (mutation.type === 'attributes' && mutation.target instanceof HTMLImageElement) {
        if (AVATAR_PATCHING_ENABLED) patchAvatar(mutation.target);
        continue;
      }
      if (AVATAR_PATCHING_ENABLED) {
        mutation.addedNodes.forEach(syncAssistantAvatars);
        mutation.addedNodes.forEach(syncDecorativeAvatars);
      }
      if (HEADER_SYNC_ENABLED) mutation.addedNodes.forEach(syncChatHeaderControls);
      if (QUOTA_BADGE_ENABLED) mutation.addedNodes.forEach(syncCodexQuotaBadge);
      if (NORMALIZE_MESSAGE_TIMELINE) mutation.addedNodes.forEach(normalizeChatMessageOrder);
    }
    if (LAYOUT_SYNC_ENABLED) syncChatLayoutMetrics();
  });
  mo.observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['src', 'srcset', 'alt', 'aria-label', 'class'] });

  if (QUOTA_BADGE_ENABLED) window.setInterval(syncCodexQuotaBadge, 2000);
  if (NORMALIZE_MESSAGE_TIMELINE) window.setInterval(normalizeChatMessageOrder, 1000);

  document.addEventListener('error', (event) => {
    if (AVATAR_PATCHING_ENABLED && event.target instanceof HTMLImageElement) {
      patchAvatar(event.target);
    }
  }, true);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot, { once: true });
  } else {
    boot();
  }
})();
