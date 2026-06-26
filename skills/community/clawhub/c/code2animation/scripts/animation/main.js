// Deterministic CSS timeline runtime
(function () {
  const root = document.documentElement;

  const setTimelineTime = (time) => {
    const safeTime = Number.isFinite(time) ? Math.max(0, time) : 0;
    root.style.setProperty('--t', safeTime.toFixed(6));
    window.__timelineTime = safeTime;
    const safeGlobalTime = Number.isFinite(window.__globalTimelineTime)
      ? Math.max(0, window.__globalTimelineTime)
      : safeTime;

    if (typeof window.onTimelineUpdate === 'function') {
      window.onTimelineUpdate(safeTime, safeGlobalTime);
    }
  };

  window.setTimelineTime = setTimelineTime;
  window.syncTime = setTimelineTime;

  window.addEventListener('message', (event) => {
    const data = event.data;
    if (!data || typeof data !== 'object') return;

    if (data.type === 'seek') {
      const nextClipTime = Number(data.time) || 0;
      const nextGlobalTime = Number.isFinite(Number(data.globalTime))
        ? Number(data.globalTime)
        : nextClipTime;
      window.__globalTimelineTime = nextGlobalTime;
      setTimelineTime(nextClipTime);
      window.parent.postMessage({ type: 'iframeSynced', time: Number(data.time) || 0 }, '*');
    }
  });

  setTimelineTime(0);
  console.log('[DeterministicIframe] CSS timeline runtime loaded');
})();
