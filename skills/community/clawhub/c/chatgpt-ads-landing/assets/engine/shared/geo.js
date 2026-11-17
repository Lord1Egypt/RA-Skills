/* ========================================================================
   Visitor country + measurement-consent state (shared by every page).
   scripts/build.js inlines this into <head>, after window.LP_CONFIG and
   before the OpenAI Pixel snippet, because the Pixel needs to know whether
   to start with consent off *before* `oaiq("init")`
   (https://developers.openai.com/ads/measurement-pixel#control-measurement-consent).

   Sets window.LP_GEO = { country, consent, consentKey }:
   - country: ISO-2 of a routing.sites entry, from the browser time zone (then
     the browser language region); '' when nothing matches. lp.js uses it for
     geo CTAs and per-country footer links.
   - consent: 'not_required' unless country is in page.json consent.countries;
     otherwise the visitor's stored choice ('granted' / 'denied') or 'pending'
     when they have not chosen yet.
   ======================================================================== */
(function (window) {
  'use strict';

  var cfg = window.LP_CONFIG || {};
  var sites = (cfg.routing || {}).sites || {};
  var consentCountries = (cfg.consent || {}).countries || [];
  var CONSENT_KEY = 'lp_measurement_consent';

  // IANA time zone -> ISO-2. Zones are fine-grained enough to tell US from
  // Canada, which a language tag (en-US is every default) cannot.
  // Extend this table when a page routes to a country not listed here.
  var TZ_COUNTRY = {
    'America/New_York': 'US', 'America/Chicago': 'US', 'America/Denver': 'US',
    'America/Phoenix': 'US', 'America/Los_Angeles': 'US', 'America/Anchorage': 'US',
    'America/Juneau': 'US', 'America/Sitka': 'US', 'America/Nome': 'US',
    'America/Adak': 'US', 'America/Boise': 'US', 'America/Detroit': 'US',
    'America/Menominee': 'US', 'Pacific/Honolulu': 'US', 'America/Puerto_Rico': 'US',
    'America/Toronto': 'CA', 'America/Montreal': 'CA', 'America/Vancouver': 'CA',
    'America/Edmonton': 'CA', 'America/Winnipeg': 'CA', 'America/Regina': 'CA',
    'America/Halifax': 'CA', 'America/St_Johns': 'CA', 'America/Moncton': 'CA',
    'America/Glace_Bay': 'CA', 'America/Goose_Bay': 'CA', 'America/Whitehorse': 'CA',
    'America/Yellowknife': 'CA', 'America/Iqaluit': 'CA', 'America/Swift_Current': 'CA',
    'America/Dawson_Creek': 'CA', 'America/Fort_Nelson': 'CA', 'America/Creston': 'CA',
    'Europe/London': 'GB', 'Europe/Belfast': 'GB', 'Europe/Dublin': 'IE',
    'Asia/Singapore': 'SG', 'Pacific/Auckland': 'NZ', 'Asia/Tokyo': 'JP',
    'Asia/Seoul': 'KR', 'Asia/Hong_Kong': 'HK', 'Asia/Macau': 'MO', 'Asia/Taipei': 'TW',
    'Asia/Shanghai': 'CN', 'Asia/Bangkok': 'TH', 'Asia/Kuala_Lumpur': 'MY',
    'Europe/Paris': 'FR', 'Europe/Berlin': 'DE', 'Europe/Madrid': 'ES',
    'Europe/Rome': 'IT', 'Europe/Amsterdam': 'NL'
  };
  var TZ_PREFIX = [
    ['America/Indiana/', 'US'], ['America/Kentucky/', 'US'], ['America/North_Dakota/', 'US'],
    ['US/', 'US'], ['Canada/', 'CA'], ['Australia/', 'AU']
  ];

  function countryFromTimeZone() {
    var tz = '';
    try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) { return ''; }
    if (TZ_COUNTRY[tz]) { return TZ_COUNTRY[tz]; }
    for (var i = 0; i < TZ_PREFIX.length; i++) {
      if (tz.indexOf(TZ_PREFIX[i][0]) === 0) { return TZ_PREFIX[i][1]; }
    }
    return '';
  }

  function countryFromLanguage() {
    var langs = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < langs.length; i++) {
      var m = /^[a-z]{2,3}-([A-Z]{2})$/i.exec(langs[i] || '');
      if (m) { return m[1].toUpperCase(); }
    }
    return '';
  }

  // Only a country that has a configured site counts as a match; otherwise
  // try the next signal, and finally fall back.
  function resolveCountry() {
    var tz = countryFromTimeZone();
    if (sites[tz]) { return tz; }
    var lang = countryFromLanguage();
    if (sites[lang]) { return lang; }
    return '';
  }

  var country = resolveCountry();

  var consent = 'not_required';
  if (consentCountries.indexOf(country) !== -1) {
    var stored = null;
    try { stored = window.localStorage.getItem(CONSENT_KEY); } catch (e) { stored = null; }
    consent = stored === 'granted' || stored === 'denied' ? stored : 'pending';
  }

  window.LP_GEO = { country: country, consent: consent, consentKey: CONSENT_KEY };

})(window);
