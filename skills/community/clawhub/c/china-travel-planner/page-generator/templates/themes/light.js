/**
 * Light theme for travel-page-framework.
 * Provides Tailwind config colors + component class mappings.
 */
window.TripThemes = window.TripThemes || {};
window.TripThemes.light = {
  name: 'light',
  tailwind: {
    paper: '#f8f6f1',
    ink: '#2b2b2b',
    sand: '#efe7d8',
    skysoft: '#dbeafe',
    mintsoft: '#dcfce7',
    peachsoft: '#ffedd5',
    goldsoft: '#fef3c7',
    coral: '#f97316',
    tealsoft: '#0f766e'
  },
  shadows: {
    card: '0 10px 30px rgba(15, 23, 42, 0.08)',
    soft: '0 8px 20px rgba(15, 23, 42, 0.06)'
  },
  css: {
    body: 'bg-paper text-ink antialiased',
    header: 'border-b border-stone-200 bg-gradient-to-br from-orange-50 via-white to-sky-50',
    nav: 'border-b border-stone-200 bg-white/90 backdrop-blur',
    navLink: 'rounded-full border border-stone-200 bg-white px-4 py-2 text-sm text-slate-700 shadow-soft',
    sectionLabel: 'text-sm uppercase tracking-[0.2em] text-tealsoft',
    sectionTitle: 'mt-2 text-2xl font-bold text-slate-900',
    card: 'rounded-[28px] border border-stone-200 bg-white shadow-card',
    statCard: 'rounded-2xl border border-stone-200 bg-white p-5 shadow-soft',
    tipCard: 'rounded-2xl border border-amber-200 bg-goldsoft p-4 text-sm leading-7 text-slate-700',
    noteCard: 'rounded-2xl bg-orange-50 px-4 py-3 text-sm leading-7 text-slate-600',
    tag: 'rounded-full bg-sky-50 px-3 py-1 text-xs text-sky-700',
    heroTag: 'rounded-full border border-white bg-white px-4 py-2 text-sm text-slate-700 shadow-soft',
    footer: 'border-t border-stone-200 bg-white py-8'
  },
  badge: {
    '已预订': 'bg-mintsoft text-emerald-700 border-emerald-200',
    '推荐': 'bg-skysoft text-sky-700 border-sky-200',
    _default: 'bg-peachsoft text-orange-700 border-orange-200'
  },
  metro: {
    _default: 'bg-stone-50 text-stone-700 border-stone-200'
    // Line-specific colors are auto-generated from a palette
  },
  metroPalette: [
    { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
    { bg: 'bg-sky-50', text: 'text-sky-700', border: 'border-sky-200' },
    { bg: 'bg-violet-50', text: 'text-violet-700', border: 'border-violet-200' },
    { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
    { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200' },
    { bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-200' },
    { bg: 'bg-cyan-50', text: 'text-cyan-700', border: 'border-cyan-200' },
    { bg: 'bg-teal-50', text: 'text-teal-700', border: 'border-teal-200' },
    { bg: 'bg-indigo-50', text: 'text-indigo-700', border: 'border-indigo-200' },
    { bg: 'bg-lime-50', text: 'text-lime-700', border: 'border-lime-200' }
  ]
};
