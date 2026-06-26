# Eval 04: Immunization Schedule Tracking

## Setup Context
Liam is 5 years old. His immunization record shows DTaP doses 1-4 complete, IPV doses 1-3 complete. No 4-6 year boosters logged yet.

## Input
"Is Liam up to date on his shots?"

## Expected Behavior
1. Reviews Liam's immunization record against the CDC schedule for his age
2. Identifies what's missing: DTaP 5th dose and IPV 4th dose (both due at 4-6 years)
3. Also flags MMR 2nd dose and Varicella 2nd dose if not logged
4. Presents clearly: what's complete, what's due
5. Suggests scheduling with his pediatrician

## What to Watch For
- Does it compare against the built-in CDC schedule accurately?
- Does it identify ALL missing vaccines for the age range, not just one?
- Is the output parent-friendly, not clinical?
