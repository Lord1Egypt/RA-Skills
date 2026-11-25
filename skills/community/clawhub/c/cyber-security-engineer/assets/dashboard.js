// Behaviour for the compliance dashboard: tabs, filters, paging, CSV export, tooltips.
// Inlined into the page by compliance_dashboard.py; __PAGE_SIZE__ is replaced with the page size.
(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  var views = Array.prototype.slice.call(document.querySelectorAll('[data-view]'));
  var navs = Array.prototype.slice.call(document.querySelectorAll('.nav[data-target]'));
  var status = document.getElementById('filter-status');
  var risk = document.getElementById('filter-risk');
  var query = document.getElementById('filter-query');
  var empty = document.getElementById('empty');
  var pager = document.getElementById('pager');
  var pagerRange = document.getElementById('pager-range');
  var pagerPage = document.getElementById('pager-page');
  var prev = document.getElementById('pager-prev');
  var next = document.getElementById('pager-next');
  var PAGE_SIZE = __PAGE_SIZE__;
  var current = 'controls';
  var page = 1;
  var matched = [];

  function activeView() {
    return views.filter(function (v) { return v.getAttribute('data-view') === current; })[0];
  }

  function applyFilters() {
    var view = activeView();
    var rows = Array.prototype.slice.call(view.querySelectorAll('tbody tr'));
    var s = status.value, r = risk.value, q = query.value.trim().toLowerCase();
    matched = rows.filter(function (row) {
      return (!s || row.getAttribute('data-status') === s) &&
             (!r || row.getAttribute('data-risk') === r) &&
             (!q || row.textContent.toLowerCase().indexOf(q) !== -1);
    });
    rows.forEach(function (row) { row.hidden = true; });
    view.querySelector('.table-scroll').hidden = matched.length === 0;
    empty.hidden = matched.length !== 0;
    empty.textContent = rows.length === 0 ? view.getAttribute('data-empty') : 'No controls match these filters.';
    page = 1;
    showPage();
  }

  function showPage() {
    var pages = Math.max(1, Math.ceil(matched.length / PAGE_SIZE));
    page = Math.min(Math.max(1, page), pages);
    var first = (page - 1) * PAGE_SIZE, last = Math.min(first + PAGE_SIZE, matched.length);
    matched.forEach(function (row, i) {
      var on = i >= first && i < last;
      row.hidden = !on;
      row.classList.toggle('alt', on && (i - first) % 2 === 1);
      row.classList.toggle('last', on && i === last - 1 && pages === 1);
    });
    // The pager appears only when the rows do not fit on one page.
    pager.hidden = pages === 1;
    pagerRange.textContent = 'Showing ' + (first + 1) + '-' + last + ' of ' + matched.length;
    pagerPage.textContent = 'Page ' + page + ' of ' + pages;
    prev.disabled = page === 1;
    next.disabled = page === pages;
  }

  function turnPage(step) {
    page += step;
    showPage();
    var card = document.getElementById('records');
    if (card.getBoundingClientRect().top < 0) { card.scrollIntoView({ block: 'start' }); }
  }
  prev.addEventListener('click', function () { turnPage(-1); });
  next.addEventListener('click', function () { turnPage(1); });

  function markNav(target) {
    navs.forEach(function (n) { n.classList.toggle('is-active', n.getAttribute('data-target') === target); });
  }

  function showView(name) {
    current = name;
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-tab') === name;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
    });
    views.forEach(function (v) { v.hidden = v.getAttribute('data-view') !== name; });
    applyFilters();
  }

  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { showView(t.getAttribute('data-tab')); markNav(t.getAttribute('data-tab')); });
    t.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') { return; }
      var next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      next.focus(); next.click();
    });
  });

  navs.forEach(function (n) {
    n.addEventListener('click', function () {
      var target = n.getAttribute('data-target');
      markNav(target);
      if (target === 'overview') {
        document.getElementById('overview').scrollIntoView({ block: 'start' });
        window.scrollTo(0, 0);
        return;
      }
      showView(target);
      document.getElementById('records').scrollIntoView({ block: 'start' });
    });
  });

  [status, risk].forEach(function (el) { el.addEventListener('change', applyFilters); });
  query.addEventListener('input', applyFilters);

  function cellText(cell) { return cell.textContent.replace(/\s+/g, ' ').trim(); }
  function csvField(text) {
    // Neutralise spreadsheet formulas before quoting.
    if (/^[=+\-@]/.test(text)) { text = "'" + text; }
    return '"' + text.replace(/"/g, '""') + '"';
  }
  document.getElementById('export').addEventListener('click', function () {
    var view = activeView();
    var lines = [];
    [view.querySelector('thead tr')].concat(matched).forEach(function (row) {
      lines.push(Array.prototype.slice.call(row.children).map(function (c) { return csvField(cellText(c)); }).join(','));
    });
    var blob = new Blob([lines.join('\r\n') + '\r\n'], { type: 'text/csv;charset=utf-8' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'compliance-' + current + '.csv';
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(function () { URL.revokeObjectURL(link.href); }, 1000);
  });

  // One shared tooltip for chart marks; the same text is shown on keyboard focus.
  var tip = document.createElement('div');
  tip.className = 'tip';
  tip.hidden = true;
  document.body.appendChild(tip);
  function place(x, y) {
    tip.style.left = Math.max(8, Math.min(x + 12, window.innerWidth - tip.offsetWidth - 8)) + 'px';
    tip.style.top = Math.max(8, y - tip.offsetHeight - 10) + 'px';
  }
  Array.prototype.slice.call(document.querySelectorAll('[data-tip]')).forEach(function (el) {
    function open(x, y) { tip.textContent = el.getAttribute('data-tip'); tip.hidden = false; place(x, y); }
    el.addEventListener('pointermove', function (e) { open(e.clientX, e.clientY); });
    el.addEventListener('pointerleave', function () { tip.hidden = true; });
    el.addEventListener('focus', function () {
      var box = el.getBoundingClientRect();
      open(box.left + box.width / 2, box.top);
    });
    el.addEventListener('blur', function () { tip.hidden = true; });
  });

  showView(current);
})();
