/**
 * trip-renderer.js - Universal renderer for travel-page-framework.
 *
 * Usage:
 *   <script src="path/to/trip-renderer.js"></script>
 *   <script>
 *     TripRenderer.init({ dataUrl: './data/trip-data.json', theme: 'light' });
 *   </script>
 *
 * Reads trip-data.json and populates all DOM sections defined in the HTML skeleton.
 * Theme colors come from TripThemes[themeName] (loaded via themes/light.js etc).
 */
;(function (global) {
  'use strict';

  /* ── helpers ─────────────────────────────────────────── */

  let _theme = null;
  let _metroColorMap = {};

  function theme() {
    return _theme || (global.TripThemes && global.TripThemes.light) || {};
  }

  function badgeClass(status) {
    const t = theme();
    if (t.badge && t.badge[status]) return t.badge[status];
    return (t.badge && t.badge._default) || '';
  }

  /** Build metro color map on first use from metroCoverage data. */
  function buildMetroColors(lines) {
    const palette = (theme().metroPalette) || [];
    lines.forEach(function (line, i) {
      if (!_metroColorMap[line.name] && palette[i % palette.length]) {
        var p = palette[i % palette.length];
        _metroColorMap[line.name] = p.bg + ' ' + p.text + ' ' + p.border;
      }
    });
  }

  function metroClass(line) {
    return _metroColorMap[line] || (theme().metro && theme().metro._default) || '';
  }

  function listItems(items) {
    return items.map(function (item) {
      return '<li class="flex gap-3"><span class="mt-2 h-1.5 w-1.5 rounded-full bg-orange-400"></span><span>' + esc(item) + '</span></li>';
    }).join('');
  }

  function esc(s) {
    if (typeof s !== 'string') return '';
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  /* ── modal ──────────────────────────────────────────── */

  function openDayModal(day) {
    var modal = document.getElementById('day-modal');
    if (!modal) return;
    document.body.classList.add('modal-open');
    modal.classList.remove('hidden');
    modal.classList.add('flex');

    setText('modal-meta', day.day + ' · ' + day.date + ' · ' + day.city);
    setText('modal-title', day.theme);
    setText('modal-note', '备注：' + day.note);
    setHTML('modal-morning', listItems(day.segments.morning));
    setHTML('modal-afternoon', listItems(day.segments.afternoon));
    setHTML('modal-evening', listItems(day.segments.evening && day.segments.evening.length ? day.segments.evening : ['自由安排 / 休整']));

    var attractions = day.attractions || [];
    setHTML('modal-gallery', attractions.length
      ? attractions.map(function (a) {
          return '<img src="' + esc(a.image) + '" alt="' + esc(a.name) + '" class="h-48 w-full rounded-2xl object-cover lg:h-[220px]" />';
        }).join('')
      : '<div class="rounded-2xl bg-white p-6 text-sm text-slate-500">暂无景点图。</div>');

    setHTML('modal-attractions', attractions.length
      ? attractions.map(function (a) {
          return '<article class="rounded-2xl border border-stone-200 bg-white p-4 shadow-soft">' +
            '<div class="text-lg font-bold text-slate-900">' + esc(a.name) + '</div>' +
            '<p class="mt-2 text-sm leading-7 text-slate-600">' + esc(a.description) + '</p>' +
            (a.reason ? '<div class="mt-3 rounded-xl bg-sky-50 px-3 py-2 text-sm text-slate-600">安排理由：' + esc(a.reason) + '</div>' : '') +
            '</article>';
        }).join('')
      : '<div class="rounded-2xl bg-slate-50 p-4 text-sm text-slate-500">这一天没有单独展开的景点说明。</div>');
  }

  function closeDayModal() {
    var modal = document.getElementById('day-modal');
    if (!modal) return;
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.classList.remove('modal-open');
  }

  function bindModalEvents() {
    var close = document.getElementById('modal-close');
    var modal = document.getElementById('day-modal');
    if (close) close.addEventListener('click', closeDayModal);
    if (modal) modal.addEventListener('click', function (e) { if (e.target === modal) closeDayModal(); });
  }

  /* ── tiny DOM helpers ───────────────────────────────── */

  function setText(id, val) { var el = document.getElementById(id); if (el) el.textContent = val || ''; }
  function setHTML(id, val) { var el = document.getElementById(id); if (el) el.innerHTML = val || ''; }

  /* ── main render ────────────────────────────────────── */

  function render(data) {
    // Build metro palette from data
    if (data.metroCoverage && data.metroCoverage.lines) {
      buildMetroColors(data.metroCoverage.lines);
    }

    // Title
    document.title = data.meta.title;

    // Hero
    setText('hero-title', data.hero.title);
    setText('hero-subtitle', data.hero.subtitle);
    setText('hero-date', data.hero.dateRange);
    setText('hero-summary', data.hero.summary);
    var heroBg = document.getElementById('hero-bg');
    if (heroBg && data.hero.heroImage) {
      heroBg.style.backgroundImage = "url('" + data.hero.heroImage + "')";
    }

    setHTML('hero-tags', (data.hero.tags || []).map(function (tag) {
      return '<span class="' + (theme().css && theme().css.heroTag || '') + '">' + esc(tag) + '</span>';
    }).join(''));

    setHTML('hero-quick', data.stats.slice(0, 4).map(function (s) {
      return '<div class="rounded-2xl border border-stone-200 bg-stone-50 p-4">' +
        '<div class="text-xs uppercase tracking-[0.2em] text-slate-400">' + esc(s.label) + '</div>' +
        '<div class="mt-2 text-sm font-semibold text-slate-900">' + esc(s.value) + '</div></div>';
    }).join(''));

    // Stats
    setHTML('stats-grid', data.stats.map(function (s) {
      return '<div class="' + (theme().css && theme().css.statCard || '') + '">' +
        '<div class="text-xs uppercase tracking-[0.2em] text-slate-400">' + esc(s.label) + '</div>' +
        '<div class="mt-3 text-lg font-bold text-slate-900">' + esc(s.value) + '</div></div>';
    }).join(''));

    // Hotels
    setHTML('hotel-grid', data.hotels.map(function (h) {
      return '<article class="overflow-hidden ' + (theme().css && theme().css.card || '') + '">' +
        '<img src="' + esc(h.image) + '" alt="' + esc(h.name) + '" class="h-52 w-full object-cover" />' +
        '<div class="p-5"><div class="flex items-start justify-between gap-3"><div>' +
        '<div class="text-xs uppercase tracking-[0.2em] text-slate-400">' + esc(h.phase) + '</div>' +
        '<h3 class="mt-2 text-lg font-bold text-slate-900">' + esc(h.name) + '</h3></div>' +
        '<span class="rounded-full border px-3 py-1 text-xs ' + badgeClass(h.status) + '">' + esc(h.status) + '</span></div>' +
        '<div class="mt-4 grid gap-2 text-sm text-slate-600">' +
        '<div>日期：' + esc(h.dateRange) + '</div><div>区域：' + esc(h.station) + '</div>' +
        '<div>价格：' + esc(h.price) + '</div><div>地铁：' + esc(h.distanceToMetro) + '</div></div>' +
        '<ul class="mt-4 space-y-2 text-sm text-slate-700">' + listItems(h.highlights) + '</ul></div></article>';
    }).join(''));

    // Metro
    setText('metro-goal', data.metroCoverage.goal);
    setHTML('metro-lines', data.metroCoverage.lines.map(function (l) {
      return '<div class="rounded-2xl border px-4 py-3 ' + metroClass(l.name) + '">' +
        '<div class="font-semibold">' + esc(l.name) + '</div>' +
        '<div class="mt-1 text-xs opacity-80">' + esc(l.day) + '</div></div>';
    }).join(''));

    // Days
    setHTML('day-list', data.days.map(function (day, idx) {
      var metroTags = day.metroLines.length
        ? day.metroLines.map(function (l) { return '<span class="rounded-full border px-3 py-1 text-xs ' + metroClass(l) + '">' + esc(l) + '</span>'; }).join('')
        : '<span class="rounded-full border border-stone-200 bg-stone-50 px-3 py-1 text-xs text-stone-500">当日无主补线任务</span>';
      var attrTags = (day.attractions || []).map(function (a) {
        return '<span class="' + (theme().css && theme().css.tag || '') + '">' + esc(a.name) + '</span>';
      }).join('');

      return '<article data-day-index="' + idx + '" class="day-card cursor-pointer ' + (theme().css && theme().css.card || '') + ' p-6 transition hover:-translate-y-1">' +
        '<div class="flex items-start justify-between gap-4"><div>' +
        '<div class="' + (theme().css && theme().css.sectionLabel || '') + '">' + esc(day.day) + ' · ' + esc(day.date) + '</div>' +
        '<h3 class="mt-2 text-2xl font-bold text-slate-900">' + esc(day.theme) + '</h3>' +
        '<div class="mt-3 text-sm text-slate-500">城市：' + esc(day.city) + ' · 酒店：' + esc(day.hotel || '无') + '</div></div>' +
        '<div class="rounded-full bg-orange-50 px-4 py-2 text-sm text-orange-700">查看详情</div></div>' +
        '<div class="mt-5 flex flex-wrap gap-2">' + metroTags + '</div>' +
        '<div class="mt-5 grid gap-4 md:grid-cols-3">' +
        '<div class="rounded-2xl bg-stone-50 p-4"><div class="text-sm font-semibold text-slate-900">上午</div><ul class="mt-3 space-y-2 text-sm text-slate-600">' + listItems(day.segments.morning) + '</ul></div>' +
        '<div class="rounded-2xl bg-stone-50 p-4"><div class="text-sm font-semibold text-slate-900">下午</div><ul class="mt-3 space-y-2 text-sm text-slate-600">' + listItems(day.segments.afternoon) + '</ul></div>' +
        '<div class="rounded-2xl bg-stone-50 p-4"><div class="text-sm font-semibold text-slate-900">晚上</div><ul class="mt-3 space-y-2 text-sm text-slate-600">' + listItems(day.segments.evening && day.segments.evening.length ? day.segments.evening : ['自由安排 / 休整']) + '</ul></div></div>' +
        (attrTags ? '<div class="mt-5 flex flex-wrap gap-2">' + attrTags + '</div>' : '') +
        '</article>';
    }).join(''));

    // Bind day card clicks
    document.querySelectorAll('.day-card').forEach(function (card) {
      card.addEventListener('click', function () {
        openDayModal(data.days[Number(card.dataset.dayIndex)]);
      });
    });

    // Side trips
    setHTML('side-trips-list', data.sideTrips.map(function (s) {
      return '<article class="overflow-hidden ' + (theme().css && theme().css.card || '') + '">' +
        '<img src="' + esc(s.image) + '" alt="' + esc(s.name) + '" class="h-48 w-full object-cover" />' +
        '<div class="p-5"><div class="text-xs uppercase tracking-[0.2em] text-slate-400">' + esc(s.date) + '</div>' +
        '<h3 class="mt-2 text-xl font-bold text-slate-900">' + esc(s.name) + '</h3>' +
        '<div class="mt-2 text-sm text-tealsoft">' + esc(s.role) + '</div>' +
        '<p class="mt-3 text-sm leading-7 text-slate-600">' + esc(s.description) + '</p></div></article>';
    }).join(''));

    // Tips
    setHTML('tips-panel', data.tips.map(function (tip) {
      return '<div class="' + (theme().css && theme().css.tipCard || '') + '">' + esc(tip) + '</div>';
    }).join(''));

    // Attractions
    setHTML('attraction-grid', data.attractions.map(function (a) {
      return '<article class="overflow-hidden ' + (theme().css && theme().css.card || '') + '">' +
        '<img src="' + esc(a.image) + '" alt="' + esc(a.name) + '" class="h-56 w-full object-cover" />' +
        '<div class="p-5"><div class="text-xs uppercase tracking-[0.2em] text-slate-400">' + esc(a.city) + ' · ' + esc(a.type) + '</div>' +
        '<h3 class="mt-2 text-xl font-bold text-slate-900">' + esc(a.name) + '</h3>' +
        '<p class="mt-3 text-sm leading-7 text-slate-600">' + esc(a.description) + '</p>' +
        '<div class="mt-4 flex flex-wrap gap-2">' +
        a.bestFor.map(function (b) { return '<span class="' + (theme().css && theme().css.tag || '') + '">' + esc(b) + '</span>'; }).join('') +
        '</div></div></article>';
    }).join(''));
  }

  /* ── public API ─────────────────────────────────────── */

  global.TripRenderer = {
    /**
     * @param {Object} opts
     * @param {string} opts.dataUrl  - path to trip-data.json (default: './data/trip-data.json')
     * @param {string} opts.theme    - theme name (default: 'light')
     * @param {Object} opts.data     - pass data directly instead of fetching
     */
    init: function (opts) {
      opts = opts || {};
      var themeName = opts.theme || 'light';
      _theme = (global.TripThemes && global.TripThemes[themeName]) || null;

      // Apply tailwind config if theme provides it
      if (_theme && _theme.tailwind && global.tailwind) {
        global.tailwind.config = {
          theme: {
            extend: {
              colors: _theme.tailwind,
              boxShadow: _theme.shadows || {}
            }
          }
        };
      }

      bindModalEvents();

      if (opts.data) {
        render(opts.data);
      } else {
        var url = opts.dataUrl || './data/trip-data.json';
        fetch(url)
          .then(function (r) { return r.json(); })
          .then(render)
          .catch(function (e) { console.error('[TripRenderer] Failed to load data:', e); });
      }
    },

    /** Expose for external use */
    render: render,
    metroClass: metroClass,
    badgeClass: badgeClass
  };

})(window);
