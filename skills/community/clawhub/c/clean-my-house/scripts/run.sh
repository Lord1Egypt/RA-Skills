#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-help}"

show_help() {
  cat <<'EOF'
clean-my-house skill helper

Usage:
  ./run.sh quick
  ./run.sh standard
  ./run.sh deep
  ./run.sh guests
  ./run.sh weekly

Modes:
  quick     Print a 20-minute whole-house reset checklist
  standard  Print a standard cleaning checklist
  deep      Print a deep-clean room-by-room checklist
  guests    Print a fast guest-prep cleaning checklist
  weekly    Print a weekly maintenance routine
EOF
}

quick_mode() {
  cat <<'EOF'
20-Minute Quick Reset
1. Open curtains / windows if appropriate
2. Grab a rubbish bag and remove trash from all main rooms
3. Collect dishes and move them to the kitchen
4. Put obvious clutter into a basket
5. Wipe kitchen bench and dining table
6. Wipe bathroom sink and toilet seat
7. Vacuum or sweep living room and entry
8. Put the basket away room by room if time remains
EOF
}

standard_mode() {
  cat <<'EOF'
Standard House Clean
- Kitchen
  - Clear benches
  - Load / wash dishes
  - Wipe surfaces
  - Clean sink
  - Sweep / mop floor

- Bathroom
  - Clean toilet
  - Clean sink
  - Wipe mirror
  - Rinse / scrub shower
  - Mop floor

- Living areas
  - Remove clutter
  - Dust visible surfaces
  - Vacuum / sweep floor

- Bedrooms
  - Make beds
  - Put away clothes
  - Clear surfaces
  - Vacuum floor

- Final
  - Empty bins
  - Replace towels if needed
EOF
}

deep_mode() {
  cat <<'EOF'
Deep Clean Checklist

Kitchen
- Clean stovetop
- Clean splashback
- Wipe cupboard fronts
- Clean microwave inside
- Clean fridge shelves / discard expired food
- Degrease sink area
- Mop floor thoroughly

Bathroom
- Descale taps and shower glass
- Scrub grout / corners
- Clean toilet fully
- Clean mirror
- Wipe cabinets and handles
- Mop floor

Living Room
- Dust all surfaces
- Vacuum under furniture edges
- Wipe switches / remotes
- Spot clean marks on walls if safe

Bedroom
- Change bedding
- Dust furniture
- Vacuum under bed if accessible
- Declutter bedside areas

General
- Wipe door handles / switches
- Empty bins
- Clean skirting boards if needed
EOF
}

guest_mode() {
  cat <<'EOF'
Guest Prep Priority Clean
1. Entry
   - Remove clutter
   - Quick sweep / vacuum

2. Living Room
   - Clear visible mess
   - Fluff cushions
   - Wipe table surfaces

3. Bathroom
   - Clean toilet
   - Wipe sink
   - Clean mirror
   - Replace hand towel
   - Empty bin

4. Kitchen
   - Hide / wash dishes
   - Wipe benches
   - Remove rubbish

5. Final 5 minutes
   - Fresh air
   - Lights on
   - Put stray items into a basket
EOF
}

weekly_mode() {
  cat <<'EOF'
Weekly Maintenance Routine

Daily
- Dishes
- Kitchen bench wipe
- 10-minute tidy
- Quick bathroom wipe if needed

Twice Weekly
- Vacuum / sweep high-traffic areas
- Empty bins
- Laundry reset

Weekly
- Bathroom clean
- Change bed sheets
- Dust surfaces
- Mop floors
- Fridge check
- Tidy bedrooms

Monthly
- Deep clean kitchen appliances
- Clean windows / mirrors more thoroughly
- Wipe cupboard fronts
- Declutter one small area
EOF
}

case "$MODE" in
  quick) quick_mode ;;
  standard) standard_mode ;;
  deep) deep_mode ;;
  guests) guest_mode ;;
  weekly) weekly_mode ;;
  help|--help|-h) show_help ;;
  *)
    echo "Unknown mode: $MODE"
    echo
    show_help
    exit 1
    ;;
esac