# eSIM Travel Setup

**Land connected, stay logged in — the two things international travel breaks.**

Every international traveler knows to plan flights and hotels. Almost nobody
plans the two failures that actually wreck trips: (1) landing with no data
and overpaying for it in a queue, and (2) discovering — standing in a
foreign airport — that their bank texts an OTP to a phone number that just
stopped receiving SMS. The second one strands money and email; it takes
days to fix and 20 minutes to prevent.

## The problem
1. **Connectivity by improvisation.** Carrier travel passes cost 3-10x an
   eSIM; airport SIM kiosks cost time and sometimes your home number's SMS
   slot; data needs are guessed, not sized.
2. **2FA lockouts abroad.** New IP + new device + roaming number = every
   security system challenges you at once, precisely when your recovery
   channels are weakest.
3. **Country traps.** China's VPN window, Brazil's IMEI registration,
   Turkey's phone tax, UAE's VoIP blocks — each has a deadline BEFORE
   arrival.

## What this toolkit does
- `plan` — data sizing by usage profile, eSIM type choice (local /
  regional / global), the dual-SIM doctrine, country gotcha flags.
- `twofa` — account-by-account lockout-risk audit with exact pre-departure
  fixes (backup codes, pre-trusted devices, receive-only home SIM).
- `costs` — eSIM vs roaming bundle vs airport SIM comparison with
  trip-length break-even.
- `checklist` — T-48h / T-24h / T-0 landing sequence + failure protocol.

## Quick start
```bash
# Size and plan a 12-day Japan trip
python3 scripts/esim_planner.py plan --destination Japan --days 12 --profile maps-heavy

# Audit the accounts that matter
python3 scripts/esim_planner.py twofa --bank --email-google --icloud

# Price the options
python3 scripts/esim_planner.py costs --destination Mexico --days 10 \
    --data-gb 5 --roaming-bundle 10 --roaming-gb 2

# Print the full checklist
python3 scripts/esim_planner.py checklist
```

Pure Python 3 stdlib. Offline. Nothing leaves the machine.

## Who needs this
- International leisure and business travelers (hundreds of millions of
  border crossings a year)
- First-time eSIM users confused by local/regional/global products
- Anyone whose bank uses SMS one-time codes (most people)
- Families setting up a relative's phone before a trip

## License
MIT — see LICENSE.
