/**
 * Drop-in magic-link entry-point for a Supabase-powered portal.
 *
 * Place this inside your portal IIFE, AFTER `sb` (the Supabase client) is
 * created with `detectSessionInUrl: true` and `flowType: 'pkce'`.
 *
 * Handles three cases that arrive on URL load:
 *   1) ?token_hash=<h>&type=<t>   — the recommended path (this skill)
 *   2) #access_token=<jwt>&...    — Supabase's legacy hash redirect
 *   3) ?error_description=...     — auth server returned an error
 *
 * For (1) it calls verifyOtp manually; (2) is handled implicitly by
 * detectSessionInUrl; (3) surfaces a user-visible alert. In all cases the
 * URL is cleaned afterwards so a refresh does not replay a single-use token.
 */
(function () {
  try {
    var q = new URLSearchParams(window.location.search);

    // (3) error first — short-circuit and don't try to verify anything.
    var err = q.get('error_description') || q.get('error') || q.get('error_code');
    if (err) {
      setTimeout(function () {
        alert('הקישור פג או כבר נוצל. בקש מהסוכן לשלוח קישור חדש.\n\n('
              + decodeURIComponent(err) + ')');
      }, 300);
      history.replaceState(null, '', window.location.pathname);
      return;
    }

    // (1) token_hash flow — explicit verifyOtp.
    var tokenHash = q.get('token_hash');
    var type      = q.get('type');
    if (tokenHash && type) {
      sb.auth.verifyOtp({ token_hash: tokenHash, type: type })
        .then(function (res) {
          if (res.error) {
            console.warn('verifyOtp failed:', res.error.message);
            setTimeout(function () {
              alert('הקישור פג או כבר נוצל. בקש מהסוכן לשלוח קישור חדש.');
            }, 300);
          }
        })
        .finally(function () {
          // Strip the one-time token from the URL so a refresh doesn't replay.
          history.replaceState(null, '', window.location.pathname);
        });
    }
    // (2) hash-fragment flow is handled automatically by detectSessionInUrl
    //     on the supabase client — no code needed here.
  } catch (e) {
    console.warn('magic-link bridge error:', e);
  }
})();
