# Permissions — Runtime Flow, Policy Restrictions, and Denials

Two different gatekeepers say no: the user, at runtime, and Play, at review. A permission strategy that only satisfies the first one gets rejected.

**Contents:** [The Runtime Flow](#the-runtime-flow) · [The Rationale State Machine](#the-rationale-state-machine) · [Permissions That Need Two Steps](#permissions-that-need-two-steps) · [Media and Storage](#media-and-storage) · [Notifications](#notifications) · [Policy-Restricted Permissions](#policy-restricted-permissions) · [Permissions You Can Avoid Entirely](#permissions-you-can-avoid-entirely) · [Auto-Reset and Revocation](#auto-reset-and-revocation) · [Permission Traps](#permission-traps)

**Before adding a permission**, read `## App Context` in `~/Clawic/data/android/memory.md` and open `artifacts/play-declarations.md` if the `## Boxes` index names it: the text already submitted to Play for a related permission is what the next submission must be consistent with.

## The Runtime Flow

1. Declare the permission in the manifest. Install-time (normal) permissions are granted automatically; dangerous ones are not.
2. Register a permission-request launcher **at construction time** — as a field, not inside a click handler. Registering late throws, because the registration must be restored before the lifecycle reaches STARTED (`lifecycle.md`).
3. Check the current grant state before requesting. Requesting a granted permission is a no-op but the code path around it usually is not.
4. Request at the moment of use, with the feature visible behind it. A request on first launch, before the user knows what the app does, is denied by reflex — and a denial is much more expensive than a delay.
5. Handle the denied path as a real product state, not an error dialog. The feature is unavailable; say what is lost and offer the settings route only if the user asks again.

The system's own dialog is the only legitimate prompt. A custom dialog *before* it that looks like a permission request trains the user to dismiss both.

## The Rationale State Machine

`shouldShowRequestPermissionRationale()` returns **false in two opposite situations**: the permission has never been requested, and the user has permanently denied it. It is a one-bit answer to a three-state question, and treating it as "permanently denied" is the most common permission bug on Android.

The three states, and how to distinguish them:

| State | Grant check | Rationale flag | Your own "has asked" flag |
|---|---|---|---|
| Never asked | denied | false | false |
| Denied once, can ask again | denied | true | true |
| Permanently denied | denied | false | true |

- Persist the "has asked" flag yourself (a DataStore key, `data.md`) the first time you launch the request. Without it the third row is indistinguishable from the first.
- In the permanently-denied state, the system dialog will not appear at all — the launcher returns denied immediately. The only remaining route is the app's settings page, offered as an explanation, never as an automatic redirect.
- Permission state can change while the app is running (the user visits settings, or auto-reset fires). Re-check on resume rather than caching the answer for the session.

## Permissions That Need Two Steps

- **Background location** cannot be requested together with foreground location on modern versions: request foreground first, get it granted, then request background separately with its own justification. Bundling them results in no dialog and a silent denial.
- Background location is also one of the most heavily scrutinized declarations at review, requiring a video and a justification that the core feature genuinely needs location while the app is closed. Most apps that request it do not need it.
- **Exact alarms** are a settings-page toggle rather than a dialog for the revocable variant; check the capability before every schedule (`background.md`).
- **Full-screen intents and notification-listener style capabilities** route through their own settings screens and are refused silently if requested as ordinary permissions.

## Media and Storage

- From targetSdk 33, `READ_EXTERNAL_STORAGE` no longer works: media reads split into per-type permissions for images, video and audio. An app that reads only photos requests only the image permission — requesting all three is a review question you do not want.
- Modern versions add *partial* media access: the user can grant access to selected items rather than the whole library, and the app must handle the resulting subset without complaining, including the case where the selection changes between launches.
- Writing your own media into the shared collections needs no permission. Reading someone else's does.
- The Storage Access Framework grants per-URI access with no permission at all, and it is the right answer for "open a document" and "save to a location the user chooses" (`data.md`).

## Notifications

- From targetSdk 33, `POST_NOTIFICATIONS` is a runtime permission. An app that never requests it posts notifications into nothing — no error, no dialog, no delivery.
- Request it in context, at the moment the user does something that implies wanting notifications, not on first launch. The denial here is permanent in practice, because users rarely revisit it.
- Channels remain mandatory and their importance is immutable after creation: getting importance wrong means creating a new channel with a new id and migrating, which resets the user's own customizations. Choose the importance deliberately the first time (`background.md`).
- On devices below the runtime-permission version, notifications are enabled by default and the user disables them in settings — so the app has two different states to handle across the `min_sdk` range.

## Policy-Restricted Permissions

These require a declaration form in Play Console, often with a demonstration video, and are the leading cause of rejection for otherwise-fine apps:

| Permission | Who is eligible |
|---|---|
| Background location | Apps whose core, user-visible feature needs location while closed |
| `QUERY_ALL_PACKAGES` | Narrow cases (some launchers, security and accessibility tools); most apps should use `<queries>` for the specific packages they interact with |
| `MANAGE_EXTERNAL_STORAGE` | File managers, backup and anti-virus style apps |
| SMS and Call Log | Default handler apps and a short list of approved use cases |
| Accessibility service | Apps genuinely serving users with disabilities; using it for automation is a removal risk |
| `USE_EXACT_ALARM` | Alarm clocks, timers, calendars |
| Camera or microphone in the background | Explicit justification, and a visible indicator the user cannot be denied |

- The permission arriving from a **dependency** counts as yours. Check the merged manifest after adding any SDK (`build-failures.md`).
- The declaration text must match observable behavior. Reviewers install the app and look; a justification that describes a feature the reviewer cannot find is rejected, and re-submitting the same text is rejected again.
- Every submitted declaration goes into `artifacts/play-declarations.md` with its date and outcome, because the next submission must be consistent with it.

## Permissions You Can Avoid Entirely

Removing a permission is worth more than justifying it: fewer dialogs, fewer denials, no declaration form, and a cleaner data-safety section.

| Instead of | Use |
|---|---|
| Media read permissions for "attach a photo" | The system photo picker — no permission, and the user selects exactly what they share |
| Storage permissions for import/export | The Storage Access Framework |
| Camera permission for "take a picture" | The system camera intent, which returns an image without your app holding the permission |
| Contacts permission for "pick a contact" | The contact picker intent |
| `QUERY_ALL_PACKAGES` | `<queries>` entries for the specific packages or intents |
| Location for "which country/region" | The device locale, the SIM's country, or an IP-based answer from your backend |
| `READ_PHONE_STATE` for an identifier | A locally generated, resettable id stored in app storage |

## Auto-Reset and Revocation

- Permissions of apps the user has not opened for a few months are reset automatically, and the app is not notified. Code that checked once at install and cached the result breaks silently, months later, for exactly the users who use the app least.
- The app can ask the user to disable auto-reset, and doing so is only defensible for apps whose whole purpose is background operation.
- Practical rule: check the grant at the point of use, every time. The check is cheap; the cached assumption is a bug with a long fuse.

## Permission Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Reading the rationale flag as "permanently denied" | It is false both before the first ask and after permanent denial | Persist your own "has asked" flag (→ The Rationale State Machine) |
| Requesting everything at first launch | Denied by reflex, and denials are hard to reverse | Request in context, at the moment of use |
| A custom dialog styled like the system prompt | Users dismiss both; some reviewers treat it as deceptive | Explain in the UI, then let the system ask |
| Bundling foreground and background location | No dialog appears; the request silently fails | Two steps, foreground granted first |
| Requesting all three media permissions "to be safe" | Extra review scrutiny and extra denials | Only the types the app actually reads |
| Caching the grant state for the session | Auto-reset and settings changes invalidate it | Check at the point of use |
| Assuming a dependency's permissions are harmless | They are declared as yours and reviewed as yours | Diff the merged manifest after adding an SDK |
| Declaration text written from the code | Reviewers look at the running app, not the source | Write it from the user-visible feature, and keep it in `artifacts/` |
| Redirecting to settings automatically after a denial | Feels like punishment and rarely converts | Offer it once, on a second explicit attempt |

## Write Down What It Was

- **Every declaration submitted to Play** — the exact text, the date, the outcome — goes to `artifacts/play-declarations.md`, with its `## Boxes` line reading "read before any submission that touches permissions or data safety" (`memory-template.md`).
- **A permission that had to be removed or replaced** and why is a line in `## Pain Points` of `~/Clawic/data/android/memory.md`; the same SDK will reintroduce it in a future version.
- **A rejection and the change that resolved it** belongs in the same artifact as the declaration, not in a chat log — a re-submission that contradicts the approved text is rejected again.
