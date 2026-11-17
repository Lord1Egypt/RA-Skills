# 2FA Travel Protocol — Don't Lock Yourself Out Abroad

## Why travel breaks authentication
Four forces collide on day 1 of an international trip:
1. **New IP + new cell tower** = every provider's risk engine lights up.
2. **SMS OTP dependency** while your number is roaming (or disabled).
3. **New-device walls** (borrowed laptop, hotel business center, replaced
   phone after theft).
4. **No fallback channel** — the recovery phone is the one in your hand,
   which is the thing that's broken/away.

The protocol below removes single points of failure BEFORE departure.

## Lockout scenario catalog
| Scenario | Trigger | Pre-departure counter |
|---|---|---|
| Bank SMS OTP doesn't arrive | home SIM off / no roaming | home SIM stays on receive-only; or bank app-based 2FA |
| Google new-device challenge | login from abroad on new device | pre-trust travel device; print backup codes |
| iCloud lockout | password forgotten + recovery SMS unreachable | add travel number as trusted; print recovery key |
| WhatsApp re-verification | phone replaced/reinstalled | home SIM reachable for SMS |
| Exchange (crypto) 2FA on old device | TOTP seed lives on the phone you lost | move TOTP to a synced authenticator + offline codes |
| Card fraud block | foreign transaction pattern | bank/card travel notices |
| Password manager unreachable | needs 2FA that needs... the manager | offline cached vault + printed emergency kit |
| Email = recovery for everything | email lockout cascades | backup codes + second email + pre-trusted device |

Cascade rule: your PRIMARY EMAIL is the recovery path for everything else.
Its lockout is the master failure. Harden it first, hardest.

## The pre-departure hardening sequence (T-48h)
1. **Print offline backup codes** for: primary email, password manager,
   bank app, any account you'd need in week 1. Paper, two physical spots
   (wallet, luggage liner). Not photos, not cloud notes, not "I'll remember."
2. **Pre-trust the travel device**: sign in on the actual phone/laptop you
   bring, while on home soil, and accept the "remember this device" prompts.
3. **Enroll second-factor redundancy** everywhere it's offered:
   authenticator app + SMS + hardware key = at least two independent.
4. **Keep the home SIM alive, roaming, receive-only.** Verify with your
   carrier that inbound SMS abroad is free (it is on most postpaid plans).
5. **Add a travel number** where providers allow (Google trusted number,
   iCloud trusted number) — the eSIM's number works if it supports SMS.
6. **Bank travel notice** for each card + the bank app; note the
   international support phone number ON PAPER.
7. **Test the recovery paths**: actually use a backup code once; actually
   receive a bank OTP; actually see the password manager open offline.

## Account-class notes

### Banks
- SMS OTP is the dominant method and the weakest abroad. If app-based or
  hardware 2FA exists, enroll now.
- Card controls: raise or disable "international transaction" blocks via
  the app before departure.
- Keep TWO cards from different networks (Visa + Mastercard/Amex) — regional
  acceptance and fraud freezes differ.

### Primary email (Google/Apple/Microsoft)
- Google: Security checkup → 2-Step → backup codes + authenticator +
  trusted device. A new-device login abroad WITHOUT these can require
  photo ID verification that takes days.
- Apple: recovery key (print it) + trusted numbers. An iCloud lockout also
  bricks Find My and Apple Pay.
- Microsoft: alias + authenticator + backup codes.

### Messaging
- WhatsApp/Signal/Telegram bind to numbers/devices: verify your travel
  setup can re-verify (home SIM SMS) and export/restore chats to a new
  device if the phone is lost.

### Work accounts
- SSO/MFA is owned by IT, but YOU decide whether the travel device is
  enrolled. Do it before leaving; "call the helpdesk from abroad" is a bad
  plan at 3 AM their time.

### Crypto
- Hardware wallet stays home in a safe. Seed phrase does not travel as
  a photo, a cloud note, or luggage. Test that exchange 2FA lives on a
  synced authenticator, not a single device.

## If you're locked out abroad anyway
1. Airport/hotel wifi + backup codes: most walls accept printed codes.
2. Recovery via trusted device: your OTHER device (tablet) still signed in.
3. Phone the provider: that's why the support numbers are on paper.
4. Bank-specific: branch video-verify or in-app video ID where offered;
   as last resort a wire via a second institution while the first resolves.

The printed page beats all of this — which is why step 1 of the hardening
sequence is paper.
