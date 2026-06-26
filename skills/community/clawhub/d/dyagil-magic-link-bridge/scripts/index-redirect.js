/**
 * Safety-net redirect for the site root (`/index.html`).
 *
 * If a customer ever lands on the marketing homepage carrying a Supabase auth
 * payload — either in the URL hash (`#access_token=…`) or as a PKCE
 * query (`?code=…`) — forward them to the portal so the auth handshake can
 * complete there. Without this, tokens get stuck on the homepage and the
 * customer sees marketing content instead of their account.
 *
 * Drop this inline in `<head>` of the homepage, BEFORE any analytics or
 * heavy scripts, so it runs before the page is fully rendered.
 */
(function () {
  var h = window.location.hash || '';
  var q = window.location.search || '';

  var hasHashAuth =
    h.indexOf('access_token=')  !== -1 ||
    h.indexOf('type=magiclink') !== -1 ||
    h.indexOf('type=recovery')  !== -1 ||
    h.indexOf('type=invite')    !== -1 ||
    h.indexOf('type=signup')    !== -1;

  var hasQueryAuth =
    q.indexOf('code=')              !== -1 ||
    q.indexOf('token_hash=')        !== -1 ||
    q.indexOf('error=')             !== -1 ||
    q.indexOf('error_code=')        !== -1 ||
    q.indexOf('error_description=') !== -1;

  if (hasHashAuth || hasQueryAuth) {
    // Preserve BOTH the query string and the hash. The portal handler reads
    // both: ?code= / ?token_hash= / ?error= from search, #access_token=…
    // from hash.
    window.location.replace('/portal/' + q + h);
  }
})();
