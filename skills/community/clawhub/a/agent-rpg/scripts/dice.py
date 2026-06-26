# Dice Roller

import argparse
import random
import re

def roll(expression, advantage=False, disadvantage=False):
    # Support for simple standard rolls like 1d20+5
    match = re.match(r'(\d+)d(\d+)([+-]\d+)?', expression.lower())
    
    # Check for PbtA format "pbta+X"
    pbta_match = re.match(r'pbta([+-]\d+)?', expression.lower())
    
    if pbta_match:
        count = 2
        sides = 6
        modifier = int(pbta_match.group(1)) if pbta_match.group(1) else 0
    elif match:
        count = int(match.group(1))
        sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
    else:
        print("Invalid format. Use XdY+Z (e.g., 1d20+5) or pbta+Z (e.g., pbta+2)")
        return

    def do_roll():
        return [random.randint(1, sides) for _ in range(count)]
    
    if advantage and disadvantage:
        advantage = False
        disadvantage = False

    rolls1 = do_roll()
    total1 = sum(rolls1) + modifier
    
    if advantage or disadvantage:
        rolls2 = do_roll()
        total2 = sum(rolls2) + modifier
        print(f"Roll 1: {rolls1} + {modifier} = {total1}")
        print(f"Roll 2: {rolls2} + {modifier} = {total2}")
        
        if advantage:
            final_total = max(total1, total2)
            print(f"Advantage! Taking the highest: {final_total}")
        else:
            final_total = min(total1, total2)
            print(f"Disadvantage! Taking the lowest: {final_total}")
        
        total = final_total
        rolls = rolls1 if total == total1 else rolls2 # rough approx
    else:
        rolls = rolls1
        total = total1
        print(f"Expression: {expression}")
        print(f"Rolls: {rolls}")
        print(f"Modifier: {modifier:+}")
        print(f"Total: {total}")

    # Specific outputs
    if pbta_match:
        if total >= 10:
            print("PbtA Result: FULL SUCCESS (10+)")
        elif total >= 7:
            print("PbtA Result: PARTIAL SUCCESS (7-9) - Success with a cost")
        else:
            print("PbtA Result: MISS (6-) - GM makes a hard move")
    elif not pbta_match and sides == 20 and count == 1:
        if rolls[0] == 20:
            print("CRITICAL SUCCESS! (Nat 20)")
        elif rolls[0] == 1:
            print("CRITICAL FAILURE! (Nat 1)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("expression", help="Dice expression (e.g., 1d20+5 or pbta+2)")
    parser.add_argument("-a", "--advantage", action="store_true", help="Roll twice, take highest")
    parser.add_argument("-d", "--disadvantage", action="store_true", help="Roll twice, take lowest")
    args = parser.parse_args()
    roll(args.expression, args.advantage, args.disadvantage)

if __name__ == "__main__":
    main()
