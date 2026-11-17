(() => {
  const norm = s => (s || '').replace(/\s+/g, '');
  const cands = [...document.querySelectorAll('button,div,span,a')].filter(el => {
    const t = norm(el.textContent);
    if (t !== '登录') return false;
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) return false;
    if (r.top > 220) return false; // header only
    return true;
  });
  if (!cands.length) return JSON.stringify({ clicked: false, reason: 'no-login-button' });
  const el = cands[cands.length - 1].closest('button,div[role=button],a') || cands[cands.length - 1];
  el.click();
  const dlg = !!document.querySelector('[class*=login], [class*=Login], [id*=login]');
  return JSON.stringify({ clicked: true, dialog: dlg, tag: el.tagName, text: norm(el.textContent).slice(0, 20) });
})()
