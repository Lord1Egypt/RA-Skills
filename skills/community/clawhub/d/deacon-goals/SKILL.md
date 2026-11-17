---
name: deacon-goals
description: Send goals to Deacon from a web app so the founder's dashboard counts the moments that matter, such as sign ups, paywall hits and upgrades. Use when asked to add Deacon goals or tracking events to a site that already carries the Deacon widget.
---

# Deacon goals

Deacon is the support widget on this site. Its Analytics › Website page counts visitors, page views and goals. A goal is a moment the founder wants counted, sent by the site under a name of the founder's choosing: "Sign up", "Paywall hit", "Upgraded". The Deacon loader is already on every page and carries the site key, so sending a goal is one attribute on an element or one line of JavaScript. Nothing else is installed.

If the founder gave you the goals prompt from Deacon's dashboard, it carries the site key, the goals they have named and the address to verify at. Otherwise ask them for the site key, the `data-key` value in the snippet on the Install page. The goals they have named come back from the address in Verify below: under `waiting` until they arrive, and marked `named` once they have. This document carries everything else. Read it whole.

## How to work

1. Confirm the loader is on the site: search the code for `widget/v1/loader.js`. If it is missing, install it first with the deacon-install skill.
2. Send every goal the founder named, under exactly that name. If this app has no such moment, leave that goal unwired and say so at the end, with what you searched for. Never tag the nearest button that could pass for it: on a dashboard a made-up number looks exactly like a real one.
3. Add the moments from the list below that this app has and the founder did not name. Deacon builds funnels from goals read in order, so a journey with a missing step cannot be measured: a "Sign up" goal with no "Upgraded" goal cannot say how many of the people who signed up went on to pay.
4. Verify by polling until every goal has arrived, then report what you did, as the end of this document describes.

Work from the code. Do not stop to ask which goals to send: the founder reviews your choices at the end, and can rename or remove any goal on the dashboard.

## Which moments to count

The founders Deacon is built for run software products. These are the moments they ask for, what each looks like in an app, and where it is usually found.

| Goal | Fires when | Usually found in |
|---|---|---|
| Sign up | An account is created. | The registration form's submit, or the page that loads once it succeeds. |
| Onboarding complete | The setup a new account has to finish is finished. | The last step of the onboarding flow. |
| Paywall hit | A limit or a locked feature puts the upgrade offer in front of the person. | The upgrade dialog, the "upgrade to continue" banner, the pricing page opened from inside the app. |
| Upgraded | A paid plan starts. | The page a customer lands on after checkout succeeds. |
| Invited | A teammate is invited. | The invite form's submit. |
| Shared | Something leaves the account for someone else to see. | The share button, the "copy link" action. |
| Exported | Data is taken out. | The export or download action. |

Read in order, these are the funnels a founder wants: visited, Sign up, Onboarding complete; and Sign up, Paywall hit, Upgraded. The dashboard builds a funnel from any goals placed in order, counted within one visit, so a step left out is a step the founder cannot see.

A funnel joins steps one visitor reached in one visit, and a visit starts with a counted page view. If every goal fires behind a login, on pages that send no page views, each goal is still counted on its own but no funnel can form, so leave the pages in front of the login sending theirs.

Beyond the list, add a goal for any other moment that is plainly the point of this product: a booking made, a post published, a payment sent. Name it in the same plain style. Do not add goals for navigation, scrolling, hovering, or anything a visitor does without meaning to. Those are page views, and Deacon already counts them.

## Find the framework

Read the manifests before writing anything: `composer.json` and `package.json` at the root, then the routes and the views or pages directory. Use the matching section below. The three spellings after the framework sections apply everywhere.


## Laravel

The loader sits in the layout, usually `resources/views/app.blade.php` or `layouts/app.blade.php`, so it is on every page.

### Blade

A goal on a button, link or form is one attribute. The form still submits and the link still navigates: the loader holds the navigation for up to five seconds while the goal is sent, then lets it through.

```blade
<a href="{{ route('billing.plans') }}" data-deacon-goal="Paywall hit">Upgrade to continue</a>
```

For a moment that is not a click, or one the server can refuse, send it from the page that proves it happened: the page after registration, or after a successful checkout. Run the call on the window's `load` event, which waits for the loader.

```blade
@push('scripts')
<script>
    window.addEventListener('load', () => {
        window.Deacon?.track('Upgraded', { plan: '{{ $subscription->plan }}' });
    });
</script>
@endpush
```

### Inertia

Inertia pages are React or Vue components rendered by Laravel. The loader is in `app.blade.php` and counts client-side navigations itself, so nothing is added to the router. Tag the element in the component:

```jsx
<button data-deacon-goal="Paywall hit">See plans</button>
```

```vue
<button data-deacon-goal="Paywall hit">See plans</button>
```

For a moment without a click, or one the server can refuse, call the loader from the handler that knows it happened. On a page that only renders because the moment happened, such as the page after registration or a successful checkout, the component can mount before the loader has run on a full page load, so wait for the window's `load` event when the document is not yet complete:

```jsx
useEffect(() => {
    const send = () => window.Deacon?.track('Upgraded', { plan: subscription.plan });

    if (document.readyState === 'complete') {
        send();
    } else {
        window.addEventListener('load', send, { once: true });
    }
}, []);
```

## Next.js and React

The loader belongs in the root layout so it runs once for the whole app; client-side navigations are counted by the loader itself. Tag elements in JSX with the attribute, and send moments without a click from the handler once the thing has happened:

```tsx
<button data-deacon-goal="Shared">Copy link</button>
```

```tsx
async function onExport() {
    await exportReport();
    window.Deacon?.track('Exported', { format: 'csv' });
}
```

A checkout that redirects to a payment provider never returns to the handler, so "Upgraded" goes on the page the customer lands on afterwards, sent as the Inertia section shows: on the window's `load` event when the document is not yet complete. That page usually arrives before the payment is confirmed, which a webhook does separately, so send from whatever the page does once it knows the plan is active, not from its first render.

If the project is TypeScript, declare the loader once so the call type-checks:

```ts
declare global {
    interface Window {
        Deacon?: {
            track(name: string, props?: Record<string, unknown>): void;
        };
    }
}
```

## Rails

Rails writes `data-deacon-goal` from a `data` hash, so the attribute goes on the helper that renders the element. Turbo navigations are counted by the loader itself.

```erb
<%= form_with model: @user, data: { deacon_goal: "Sign up" } do |f| %>
```

```erb
<%= button_to "Upgrade", billing_path, data: { deacon_goal: "Paywall hit" } %>
```

For a moment that is not a click, use the `load` event script the Blade section shows, with ERB in place of Blade.

## Plain HTML and site builders

On a static site, put the attribute on the element:

```html
<a href="/pricing" data-deacon-goal="Paywall hit">See pricing</a>
```

On a hosted builder, use whichever field it offers:

- Webflow: a custom attribute on the element, name `data-deacon-goal`, value `Sign up`. The class spelling below also works.
- WordPress: the block's "Additional CSS class(es)" field takes the class spelling, `deacon-goal--Sign+up`.
- Shopify: edit the theme's Liquid and put the attribute on the theme's own buttons, such as add to cart and checkout. Checkout and thank-you pages run no theme code, so a goal cannot be sent from there.
- Framer, Squarespace and Wix: no attribute or class field, so a code override or code injection calls the code spelling from a click handler.

## The three spellings

Every framework sends a goal one of three ways. The name is the goal's name, exactly as the founder wrote it.

1. The attribute, on the button, link or form that completes the moment. It fires on click or submit, and the element still does what it did.

   ```html
   <button data-deacon-goal="Sign up">Create account</button>
   ```

2. The class, where only a class field is available. A `+` stands for a space.

   ```html
   <button class="deacon-goal--Sign+up">Create account</button>
   ```

3. The call, for anything that is not a click. The details are optional: up to thirty keys, each a short string, a number or a boolean, kept with the goal.

   ```js
   window.Deacon?.track('Upgraded', { plan: 'pro' });
   ```

   The loader is asynchronous and `window.Deacon` exists only once it has run. From an event handler, call it directly. On a page that sends a goal as it opens, wait for the window's `load` event, which fires after the loader:

   ```js
   window.addEventListener('load', () => {
       window.Deacon?.track('Upgraded', { plan: 'pro' });
   });
   ```

The loader sends the goal to Deacon itself. Do not add a second analytics script, wrap the loader, or delay it.


## Naming and the rules

- The name matches the founder's, letter for letter. Names are trimmed and cut at 64 characters. Write new ones in the same style: plain words, a capital first letter, no punctuation. "Paywall hit", not "paywall_hit_v2".
- Fire on the real user action, never on render, mount or route change. The one page that may send a goal as it loads is a page that only exists because the moment happened, such as the page after a successful checkout. A goal counts once per visitor however many times it fires, so a refresh of that page does no harm.
- Any action the server can refuse — a registration, an invite, a payment — belongs on what runs after it succeeded, not on the submit. A form that a taken email address rejects would otherwise count a sign up that never happened.
- A sign up through Google or another sign-in provider usually lands on the same page as a returning login, so that page cannot tell the two apart. Have the server mark a new account on its way out of registration, with a flashed session value or a query flag on the redirect, and send "Sign up" from the page that reads the mark.
- A page marked `data-no-page-views` still sends goals: that attribute holds back page views and errors only. The moments inside a signed-in app are worth wiring even where the founder has turned page views off.
- Never hard-code the site key anywhere new. The loader already carries it.
- Never put personal data in the details: no email addresses, names or identifiers.
- Tag an element once. Do not combine the attribute and the class on one element, and do not tag both a container and the button inside it.
- A goal is dropped unless it comes from one of the site's allowed domains or a development address. Verify explains both.

## Verify

The goals seen for this site, newest first, with the goals named on the dashboard that have not arrived yet:

```
curl -s "https://heydeacon.com/api/goals/recent?k=SITE_KEY"
```

```json
{
  "goals": [
    { "name": "Sign up", "arrivedAt": "2026-09-08T09:05:00+00:00", "from": "localhost", "named": true }
  ],
  "waiting": ["Upgraded"]
}
```

`named` is whether the founder named that goal on their dashboard, so `false` is the expected state for one you added, not a failure. `waiting` is their names that have not arrived.

Run the app on a development server and do each thing the goals count: create an account, open the upgrade offer, finish a checkout in test mode. Poll the address every few seconds for up to a few minutes. You are done when every goal you sent is listed under `goals` and none of the founder's named goals is left under `waiting`.

Wire the moments you cannot reach. If a goal needs a paid plan, a second account or data this environment has not got, tag the code that would send it and tell the founder to confirm that one on the live site. Never change the product, the plan or the data to make a goal fire.

A name is listed from its first arrival and stays listed, so a name already under `goals` does not prove your latest change works. After a fix, read the beacon's own answer instead.

Arriving is not the same as being counted. Everything verified from a development address is listed here and deliberately kept out of the dashboard's numbers, so tell the founder their goals are wired and will start counting once the site is live.

A headless browser is fine to verify from. The goal arrives here as it would from anyone's browser; it is never counted as traffic, which is what you want, since you are not a visitor.

While you are building, the beacon itself answers with what happened to it, so a goal that goes nowhere names its own cause:

```json
{ "recorded": true, "counted": false, "reason": "localhost" }
```

Wait for `recorded: true`: the goal arrived and the wiring works. `counted` is false from every development address, which is right, because you are not traffic. Any other `reason` is the thing to fix: `origin-not-allowed` wants this host added to the site's allowed domains on Deacon's Install page, `no-page-url` means the page's URL is not on the origin it sent from, `no-name` means the name sent was blank or not text, and `bot` means the user agent reads as a crawler. If no beacon is sent at all, the loader is not on that page: search the HTML for `widget/v1/loader.js`. A live site answers 204 with no body whatever happens.

A development address is the machine you are working on: `localhost`, a private address, or a host ending `.test`, `.local` or `.localhost`. Verify from anywhere else — a forwarded port, a tunnel, a preview deploy on another domain — and that host has to be in the site's allowed domains first (a subdomain of a listed domain already is), or every beacon is dropped and answered with a bare 204.

## Leave a note

Append a short section to the project's agent instructions file (`AGENTS.md`, `CLAUDE.md` or the equivalent) so the next agent knows the goals exist:

```markdown
## Deacon goals

The Deacon loader sends goals to the founder's analytics dashboard. The goals and where each fires:
- Sign up: the registration form's submit (data-deacon-goal).
- Paywall hit: the upgrade dialog's open button (data-deacon-goal).
- Upgraded: the checkout success page (window.Deacon.track).
Names must match the dashboard exactly. Check they arrive with `curl -s "https://heydeacon.com/api/goals/recent?k=SITE_KEY"`, using the `data-key` value from the loader.
```

## When you are done

Tell the founder, in a few lines:

- the goals you sent and where each one fires;
- which goals you added beyond the ones they named, and why each is worth counting, such as the funnel it completes or the decision it informs;
- that every goal is now on Analytics › Website, where any can be renamed or removed.
