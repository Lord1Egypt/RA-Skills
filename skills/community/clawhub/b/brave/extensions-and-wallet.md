# Extensions, Sync, Wallet, and Private Windows

## Extension Discipline

Treat each extension as a possible source of:
- blocked or rewritten page content
- extra permissions and tracking surface
- startup slowness or crashes
- automation instability

When diagnosing:
1. identify the smallest suspect set
2. disable one thing at a time
3. confirm whether the issue disappears

## Sync Boundaries

Sync can spread changes across devices.

Before changing extension state, startup pages, or browser defaults, confirm whether Brave Sync is active and whether the user wants those changes to propagate.

## Wallet Caution

Wallet-adjacent tasks are high trust.

Never:
- ask for seed phrases
- recommend copying secrets into notes
- treat wallet troubleshooting as routine browser cleanup

If wallet behavior is the issue, keep the scope narrow and ask before every change that touches accounts or permissions.

## Private Windows and Tor-Based Windows

Private browsing changes session assumptions.

Use private windows when the goal is short-lived isolation.
Use Tor-based private windows only when the user explicitly wants that mode and understands that it changes site behavior, login reliability, and some compatibility expectations.

Do not frame private or Tor-based windows as a bypass tool for restrictions.
