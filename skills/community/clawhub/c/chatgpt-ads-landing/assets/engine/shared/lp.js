/* ========================================================================
   Landing-page runtime (shared by every page under pages/*).
   Copied by scripts/build.js into dist/<slug>/assets/lp.js; reads the
   per-page config that build injects as window.LP_CONFIG (from page.json)
   and the visitor country / consent state from window.LP_GEO (shared/geo.js,
   inlined into <head>).

   The page is fully readable and usable WITHOUT this script:
   - every CTA href is already a real destination (build writes the
     fixed country site, or the fallback site for geo CTAs);
   - every footer link (data-link) already points at its fallback URL;
   - page_viewed fires via the <noscript> Image Tag when JS is off.
   This script only adds:
   1. geo routing for `dest: "geo"` CTAs and `data-link` footer links —
      LP_GEO.country (time zone / language) mapped to routing.sites /
      links.<name>, then, with routing.ipLookup, re-pointed at the visitor's
      IP country once a lookup answers with a country that has a site (no
      cookies, no referrer, nothing stored; on failure the time-zone result
      stays). The page itself never redirects, so OAI-AdsBot always gets the
      HTML;
   2. oppref / utm_* forwarding onto every CTA href (never overriding a param
      the destination URL already has) plus lp_cta / v;
   3. OpenAI Pixel events from page.json `pixelEvents` (page_viewed itself is
      sent by the snippet build puts in <head>):
      - `click`: one custom event name fired on every CTA click (plus a CTA's
        own `event`, if it has one);
      - `engagement`: each fired at most once per page load, when
        `visible` (selector) is ≥50% in view, `scrollPercent` of the page is
        reached, or `seconds` of foreground time have passed. `standard: true`
        sends a standard event (e.g. contents_viewed) instead of a custom one;
   4. a cookie banner for page.json `consent.countries`. Until the visitor
      accepts, the Pixel runs with consent off (set in <head> before init) and
      events are held here, because the Pixel never replays blocked events.
      Accepting turns consent on and sends page_viewed plus the held events;
      declining drops them. The choice is stored, and a [data-consent-settings]
      control reopens the banner.
   ======================================================================== */
(function (window, document) {
  'use strict';

  document.documentElement.classList.remove('no-js');

  var cfg = window.LP_CONFIG || {};
  var geo = window.LP_GEO || {};
  var routing = cfg.routing || {};
  var sites = routing.sites || {};
  var ctas = cfg.ctas || {};
  var links = cfg.links || {};
  var consentCfg = cfg.consent || {};

  var country = geo.country || '';
  var consent = geo.consent || 'not_required';
  // The <head> snippet only sends page_viewed when consent was not blocked.
  var pageViewedSent = consent !== 'pending' && consent !== 'denied';
  var held = [];

  var pageParams;
  try { pageParams = new URLSearchParams(window.location.search); } catch (e) { pageParams = null; }

  function destinationFor(cta) {
    var c = ctas[cta];
    if (!c) { return ''; }
    var key = c.dest === 'geo' ? country : c.dest;
    return sites[key] || routing.fallback || '';
  }

  function decorate(dest, cta) {
    var url;
    try { url = new URL(dest); } catch (e) { return dest; }
    if (pageParams) {
      (routing.forwardKeys || []).forEach(function (k) {
        // The destination's own params win: a brand-issued tracking link
        // (e.g. utm_campaign from the advertiser) must never be overwritten
        // by whatever the ad URL happened to carry.
        var v = pageParams.get(k);
        if (v && !url.searchParams.has(k)) { url.searchParams.set(k, v); }
      });
    }
    url.searchParams.set('lp_cta', cta);
    if (routing.version) { url.searchParams.set('v', routing.version); }
    return url.toString();
  }

  function linkFor(name) {
    var l = links[name];
    if (!l) { return ''; }
    return l[country] || l.fallback || '';
  }

  // Every Pixel call goes through here so consent is honoured in one place.
  function send(args) {
    if (typeof window.oaiq !== 'function') { return; }
    if (consent === 'pending') { held.push(args); return; }
    if (consent === 'denied') { return; }
    window.oaiq.apply(window, args);
  }

  function track(eventName) {
    send(['measure', 'custom', { type: 'custom' }, { custom_event_name: eventName }]);
  }

  function trackStandard(eventName) {
    send(['measure', eventName, { type: 'contents' }]);
  }

  var pixelEvents = cfg.pixelEvents || {};

  // ---- engagement events: each fires once per page load ----
  (pixelEvents.engagement || []).forEach(function (e) {
    var fired = false;
    function fire() {
      if (fired) { return; }
      fired = true;
      if (e.standard) { trackStandard(e.event); } else { track(e.event); }
    }

    if (e.visible) {
      var el = document.querySelector(e.visible);
      if (!el) { return; }
      if (!('IntersectionObserver' in window)) { fire(); return; }
      var io = new IntersectionObserver(function (entries) {
        if (entries.some(function (en) { return en.isIntersecting; })) { io.disconnect(); fire(); }
      }, { threshold: 0.5 });
      io.observe(el);
    } else if (e.scrollPercent) {
      var onScroll = function () {
        var doc = document.documentElement;
        var max = doc.scrollHeight - window.innerHeight;
        if (max <= 0 || (window.scrollY / max) * 100 >= e.scrollPercent) {
          window.removeEventListener('scroll', onScroll);
          fire();
        }
      };
      window.addEventListener('scroll', onScroll, { passive: true });
    } else if (e.seconds) {
      // Count foreground time only: a background tab is not "time on page".
      var left = e.seconds * 1000;
      var timer = null;
      var startedAt = 0;
      var start = function () {
        if (timer || fired || document.hidden) { return; }
        startedAt = Date.now();
        timer = setTimeout(fire, left);
      };
      var pause = function () {
        if (!timer) { return; }
        clearTimeout(timer);
        timer = null;
        left -= Date.now() - startedAt;
      };
      document.addEventListener('visibilitychange', function () {
        if (document.hidden) { pause(); } else { start(); }
      });
      start();
    }
  });

  // Point every CTA and footer link at the current `country`. Runs on load
  // and again if the IP lookup answers with a different country.
  function applyRouting() {
    Array.prototype.slice.call(document.querySelectorAll('[data-cta]')).forEach(function (a) {
      var cta = a.getAttribute('data-cta');
      var dest = destinationFor(cta);
      if (dest) { a.setAttribute('href', decorate(dest, cta)); }
    });
    // Footer / compliance links: per-country URL, no tracking params, no events.
    Array.prototype.slice.call(document.querySelectorAll('[data-link]')).forEach(function (a) {
      var href = linkFor(a.getAttribute('data-link'));
      if (href) { a.setAttribute('href', href); }
    });
  }

  applyRouting();

  Array.prototype.slice.call(document.querySelectorAll('[data-cta]')).forEach(function (a) {
    var cta = a.getAttribute('data-cta');
    a.addEventListener('click', function () {
      if (pixelEvents.click) { track(pixelEvents.click); }
      var c = ctas[cta];
      if (c && c.event) { track(c.event); }
    });
  });

  // ---- IP country (routing.ipLookup) ----
  // A static site cannot see the visitor IP, so ask public lookup endpoints,
  // in order, each with a short timeout. Both allow any origin (CORS *).
  var IP_SOURCES = [
    ['https://www.cloudflare.com/cdn-cgi/trace', function (t) { var m = /^loc=([A-Z]{2})$/m.exec(t); return m ? m[1] : ''; }],
    ['https://api.country.is/', function (t) { try { return JSON.parse(t).country || ''; } catch (e) { return ''; } }]
  ];
  var IP_TIMEOUT_MS = 2000;

  function lookupIpCountry(done) {
    if (typeof window.fetch !== 'function') { return; }
    var i = 0;
    (function next() {
      if (i >= IP_SOURCES.length) { return; }
      var src = IP_SOURCES[i++];
      var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
      var timer = setTimeout(function () { if (ctrl) { ctrl.abort(); } }, IP_TIMEOUT_MS);
      window.fetch(src[0], { credentials: 'omit', referrerPolicy: 'no-referrer', cache: 'no-store', signal: ctrl ? ctrl.signal : undefined })
        .then(function (r) { if (!r.ok) { throw new Error(String(r.status)); } return r.text(); })
        .then(function (text) {
          clearTimeout(timer);
          var c = String(src[1](text) || '').toUpperCase();
          if (/^[A-Z]{2}$/.test(c)) { done(c); } else { next(); }
        })
        .catch(function () { clearTimeout(timer); next(); });
    })();
  }

  if (routing.ipLookup) {
    lookupIpCountry(function (ipCountry) {
      window.LP.ipCountry = ipCountry;
      // Only a country with a configured site wins; otherwise keep the time-zone result.
      if (sites[ipCountry] && ipCountry !== country) {
        country = ipCountry;
        window.LP.country = country;
        applyRouting();
      }
    });
  }

  // ---- cookie banner (only for consent.countries) ----
  var banner = null;

  function setConsent(value) {
    consent = value;
    try { window.localStorage.setItem(geo.consentKey, value); } catch (e) { /* private mode: ask again next visit */ }
    if (typeof window.oaiq === 'function') { window.oaiq('consent', value === 'granted'); }
    if (value === 'granted') {
      if (!pageViewedSent && cfg.pageViewed) {
        pageViewedSent = true;
        send(['measure', 'page_viewed', cfg.pageViewed]);
      }
      held.splice(0).forEach(send);
    } else {
      held.length = 0;
    }
    hideBanner();
  }

  // While the banner is up, pad the page bottom so it never covers the footer
  // (which holds the Privacy / Cookie links).
  function hideBanner() {
    if (!banner) { return; }
    banner.hidden = true;
    document.body.style.paddingBottom = '';
  }

  function showBanner() {
    if (!banner) {
      var style = document.createElement('style');
      style.textContent =
        '.lp-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:1000;max-width:720px;margin:0 auto;' +
        'display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px;padding:16px 20px;border-radius:10px;' +
        'background:var(--navy-deep,#08193A);color:#fff;border:1px solid rgba(255,255,255,.22);' +
        'box-shadow:0 8px 30px rgba(0,0,0,.25);font-size:.88rem;line-height:1.5}' +
        '.lp-consent[hidden]{display:none}' +
        '.lp-consent p{flex:1 1 300px;margin:0}' +
        '.lp-consent a{color:#fff;text-decoration:underline}' +
        '.lp-consent__actions{display:flex;gap:10px}' +
        // Accept and decline get identical weight: declining must be as easy as accepting.
        '.lp-consent button{font:inherit;font-weight:600;padding:8px 18px;border-radius:999px;cursor:pointer;' +
        'border:1.5px solid #fff;background:#fff;color:var(--navy,#0E2A54)}';
      document.head.appendChild(style);

      banner = document.createElement('div');
      banner.className = 'lp-consent';
      banner.setAttribute('role', 'region');
      banner.setAttribute('aria-label', consentCfg.label || 'Cookie consent');
      var p = document.createElement('p');
      p.appendChild(document.createTextNode((consentCfg.text || '') + ' '));
      var policy = consentCfg.policyLink && linkFor(consentCfg.policyLink);
      if (policy) {
        var a = document.createElement('a');
        a.href = policy;
        a.textContent = consentCfg.policyText || 'Cookie Policy';
        p.appendChild(a);
      }
      var actions = document.createElement('div');
      actions.className = 'lp-consent__actions';
      [['denied', consentCfg.decline || 'Decline'], ['granted', consentCfg.accept || 'Accept']].forEach(function (b) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = b[1];
        btn.addEventListener('click', function () { setConsent(b[0]); });
        actions.appendChild(btn);
      });
      banner.appendChild(p);
      banner.appendChild(actions);
      document.body.appendChild(banner);
    }
    banner.hidden = false;
    document.body.style.paddingBottom = (banner.offsetHeight + 32) + 'px';
  }

  if (consent !== 'not_required') {
    Array.prototype.slice.call(document.querySelectorAll('[data-consent-settings]')).forEach(function (el) {
      el.hidden = false;
      el.addEventListener('click', function (ev) { ev.preventDefault(); showBanner(); });
    });
    if (consent === 'pending') { showBanner(); }
  }

  window.LP = {
    country: country,
    ipCountry: '',
    track: track,
    consent: function () { return consent; },
    setConsent: setConsent
  };

})(window, document);
