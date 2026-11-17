# Embedding the signing form with Signature Requests JS

Signature Requests JS shows a signature request's signing form inside the user's own site, in a modal or in an
element on the page. It was called Data Requests JS before version 3.0.0. Full reference:
https://docspring.com/docs/forms/js-libraries/signature-requests-js/

## Contents

1. The flow
2. The page
3. Embed Domains
4. Options
5. Callbacks
6. Errors
7. After the signer submits
8. Moving code from Data Requests JS 2.x

## 1. The flow

1. The server creates the submission with its signature requests (`references/api.md`), with `send_email: false`:
   otherwise DocSpring also emails the person a link to sign. Use the `auth_type` the app really used to sign the
   person in.
2. When the person opens the signing page in the app, the server creates a token:
   `POST /signature_requests/{signature_request_id}/tokens` with no body (an `api` token, 24 hours).
3. The server passes the signature request's ID and the token's `id` and `secret` to the page. Never the API token.
4. The page loads the script and calls `DocSpring.createSignatureRequestForm`.
5. The server learns the outcome from webhooks (`signature_request.completed`, `submission.processed`,
   `submission.declined`), not from the page's callbacks alone.

## 2. The page

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />

<script src="https://cdn.docspring.com/embed/signature_request.v<version>.js"></script>
<script>
  DocSpring.createSignatureRequestForm({
    signatureRequestId: 'srq_...',
    tokenId: '<token id>',
    tokenSecret: '<token secret>',
    // region: 'EU',  // for an EU account
    onSave: function (data) {
      /* data.submissionId */
    },
    onDecline: function () {
      /* the whole submission is cancelled */
    },
    onError: function (error) {
      console.error(error.error, error.message)
    },
  })
</script>
```

- Take `<version>` from the current docs, never from memory: read
  https://docspring.com/docs/guides/embedded-forms/embedded-signature-requests.md or the changelog,
  https://docspring.com/docs/changelogs/signature-requests-js/. Pin that exact version.
- `signatureRequestURL` (the token's `signature_request_url`) can replace the three ID options.
- Pass a CSS selector first to put the form in an element: `createSignatureRequestForm('#sign-here', {...})`. Without
  one it opens in a modal. Phones, and windows under 768px wide, get a full-screen modal instead. The inline iframe is
  `height: 100%; min-height: 500px`, so give the element a height.
- The script bundles its own jQuery and sets the page's global `jQuery` and `$` to it when it loads. On a page that
  uses jQuery plugins, check that the page's own jQuery code still works after adding it.
- Keep the viewport meta tag without `maximum-scale=1` or `user-scalable=no`, so signers can zoom in.
- Enterprise installs can load the script from their own DocSpring host: `/assets/embed/signature_request.js`, with
  the `host` option (or `appHost` and `apiHost` for split domains).

## 3. Embed Domains

A live signature request's form only loads on the sites in its template's `embed_domains` setting. The browser
refuses to show it anywhere else, and `onError` gets `frame_blocked` a few seconds after the iframe loads.

- An empty list means a live form loads on no site. Test signature requests load on any site, including
  `localhost`, so development works before the list is set.
- Entries: `app.example.com`, a leading wildcard (`*.example.com`), a port (`localhost:3000`) or a scheme
  (`https://app.example.com`; without one, both `http` and `https` match).
- If the app's page is itself framed by another site, list that site too.
- Signing pages read the list from the template's draft, so a change applies straight away, without publishing.
- The hosted signing page (the `signature_request_url` opened as its own page) isn't affected by the list.
- The embedded template editor reads the same setting (`docspring-embedded-forms`): a site you leave out can't load the
  editor either.

## 4. Options

| Option                        | Default  | What it does                                                                                                                  |
| ----------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `region`                      | `US`     | `EU` for an EU account.                                                                                                       |
| `redirectURL`                 | none     | Where to go after submitting. Adds `submission_id`, `template_id` and `template_name` unless `redirectURLQueryParams: false`. |
| `showDecline`                 | `true`   | Show the **Decline** button. `declineButtonLabel` renames it.                                                                 |
| `closeModalOnSave`            | `false`  | Close the modal once the signer's values are saved.                                                                           |
| `closeModalOnProcessed`       | `false`  | Close it once the PDF is made.                                                                                                |
| `closeModalOnClickOverlay`    | `true`   | Let a click outside the modal close it.                                                                                       |
| `focusFirstFieldOnLoad`       | `false`  | Focus the first field when the form loads.                                                                                    |
| `showSignatureModalOnFocus`   | `false`  | Open the signature pad when a signature or initials field gets focus.                                                         |
| `allowSkippingOptionalFields` | template | Show **Continue** once the required fields are filled in.                                                                     |
| `loadingTimeout`              | `30000`  | Milliseconds before `onError` gets `load_timeout`.                                                                            |
| `iframeClass`, `iframeStyle`  | none     | Style the iframe.                                                                                                             |

Text options (a string, or a function that returns one) change the form's messages, such as
`signatureLegalDisclaimerMessage`, `agreeToTermsTitle`, `waitingForSignatureRequestsTitle` and `completedTitle`. The
reference lists them all.

## 5. Callbacks

| Callback                       | Called when                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------- |
| `onLoad`                       | Every page of the form has loaded.                                           |
| `onSave`                       | The signer's values were saved: `{ submissionId }`.                          |
| `onRemainingSignatureRequests` | Other signers still have to sign: their count (public submissions only).     |
| `onProcessed`                  | The PDF is ready: `{ submissionId, downloadURL }` (public submissions only). |
| `onDecline`                    | The signer declined. The whole submission is cancelled.                      |
| `onError`                      | Something failed: `{ error, message }` (section 6).                          |

"Public submissions only" means the template's `public_submissions` setting is on. Otherwise the form shows its
thank-you message (or redirects) as soon as the values are saved, without waiting for the PDF.

## 6. Errors

`onError` gets an object with an `error` code and a `message`:

| `error`                                                              | What to do                                                              |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `frame_blocked`                                                      | Add the site to the template's `embed_domains`.                         |
| `token_expired`                                                      | Create a new token on the server and open the form again.               |
| `invalid_token`                                                      | The token ID or secret is wrong, or it's for another signature request. |
| `signature_request_completed`                                        | Already signed: show the app's own "done" state.                        |
| `signature_request_declined`                                         | Declined: start again with a new signature request if the user wants.   |
| `submission_declined`                                                | Another signer declined, so nobody can sign this document.              |
| `submission_expired`                                                 | The submission was expired (deleted).                                   |
| `not_found`                                                          | Wrong signature request ID, or the wrong `region`.                      |
| `save_failed`, `decline_failed`                                      | Has the HTTP `status`. Let the signer try again.                        |
| `processing_failed`, `processing_timeout`                            | The PDF failed, or takes over a minute (the form keeps waiting).        |
| `load_timeout`, `message_timeout`, `internal_error`, `unknown_error` | Log it; set `DocSpring.DEBUG = true` for console logs.                  |

## 7. After the signer submits

- The redirect URL comes from `redirectURL`, or the template's own redirect URL setting.
- With `public_submissions` off, the form redirects as soon as the signer's values are saved. With it on, the form
  waits for the PDF first; if other signers still have to sign, it calls `onRemainingSignatureRequests` and
  redirects a second later.
- The signer can only download the PDF from the form when `public_submissions` is on. Otherwise the app gives them a
  copy from `files.pdf` once the submission is `processed`.
- `DocSpring.closeModal()` closes every open form; `DocSpring.returnToForm()` goes back to the form after submitting.

## 8. Moving code from Data Requests JS 2.x

Pages that load `data_request.v2.x.js` keep working, but new code uses Signature Requests JS:

| 2.x (Data Requests JS)                             | Signature Requests JS                            |
| -------------------------------------------------- | ------------------------------------------------ |
| `embed/data_request.v<version>.js`                 | `embed/signature_request.v<version>.js`          |
| `DocSpring.createVisualForm()` (or `createForm()`) | `DocSpring.createSignatureRequestForm()`         |
| `dataRequestId`, `dataRequestURL`                  | `signatureRequestId`, `signatureRequestURL`      |
| `onRemainingDataRequests`                          | `onRemainingSignatureRequests`                   |
| `waitingForDataRequestsTitle`, `...Message`        | `waitingForSignatureRequestsTitle`, `...Message` |
| `onError` got a string                             | `onError` gets `{ error, message }`              |

- An option with its old name throws an error that names the new one.
- Removed: `DocSpring.setField()` and `DocSpring.submitForm()` (they no longer exist), and the `defaultFormData`,
  `staticFormData` and `domainVerification` options (they throw an error). Send prefilled values in the submission's
  `data` when you create the signature request.
- `domainVerification: false` no longer lets a live form load outside `embed_domains`, in 2.x either.
